"""Site boundaries traced from official documents: Willow Village, Concord, Alameda Point, Suisun.

None of these projects has an official GIS layer for its site, so each boundary is rebuilt
from an official document and georeferenced:

- willow-village: the metes-and-bounds legal description of the 59.17-acre Main Project Site
  (Menlo Park Ordinance 1095, Development Agreement Exhibit A-2-1, pp. 75-76). The courses
  are plotted exactly (they close to 0.01 ft and give 59.17 acres), then placed by a rigid fit
  (rotation and shift; scale fixed at the US survey foot) to the City of Menlo Park parcel
  lines (CC0), which the description follows.
- concord-naval-weapons-station: the Navy's Exhibit A "Economic Development Conveyance (EDC)
  Property" map dated 2026-03-30 (executed term sheet, p. 15). The map is vector: the EDC
  fills are read straight from the PDF, and its road lines are fitted to OpenStreetMap roads
  and tracks (trimmed ICP). The map is drawn rotated about 9 degrees from grid north.
- alameda-point: the 2022 Site A Development Plan, p. 12 "Parcel Diagram" (a raster image
  in the PDF). The dotted Site A boundary is traced from a 300-dpi render; the figure is
  georeferenced from eight street intersections (centrelines midway between block edges)
  matched to OpenStreetMap.
- suisun-expansion: Notice of Preparation Figure 2 (CEQAnet SCH 2025110452, PDF p. 15), a
  raster map. The annexation area is the union of its Specific Plan, Travis Protection Zone
  and Lambie Industrial Park fills (15,737 + 5,726 + 1,410 = 22,873 acres) including the
  dash-dot boundary line; the figure is fitted to SR-12 and SR-113 in OpenStreetMap.

Each output records the source page, the control points or fit statistics, and the acreage
drawn against the official figure.

    uv run --directory pipeline python -m bam_pipeline.sites.traced_boundaries [project-id ...]
"""

from __future__ import annotations

import json
import math
import os
import sys
import urllib.parse
import urllib.request

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import shapely
from shapely.geometry import LineString, Polygon, mapping

from .. import config, trace

UTM = "EPSG:26910"
ACRE_M2 = 4046.8564224
DOCS = config.ROOT / "data" / "raw" / "docs"
RAW_BOUNDARIES = config.ROOT / "data" / "raw" / "boundaries"
OUT = config.ROOT / "data" / "boundaries"
OSM_LICENSE = "OpenStreetMap contributors (ODbL 1.0), via Overture Maps"


# ---------------------------------------------------------------- shared helpers

def streets(name: str, bbox: tuple[float, float, float, float]) -> gpd.GeoDataFrame:
    """Overture transportation segments (OpenStreetMap) in a lon/lat bbox, cached, in UTM."""
    out = config.RAW / f"streets_{name}.parquet"
    if not out.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=transportation/type=segment/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = bbox
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "subtype", "class"], filter=f)
        g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                             geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
        g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
        out.parent.mkdir(parents=True, exist_ok=True)
        g[["id", "name", "subtype", "class", "geometry"]].to_parquet(out)
    return gpd.read_parquet(out).to_crs(UTM)


def intersection(g: gpd.GeoDataFrame, a: str, b: str) -> tuple[float, float]:
    la = shapely.union_all(g[g["name"] == a].geometry.to_numpy())
    lb = shapely.union_all(g[g["name"] == b].geometry.to_numpy())
    x = la.intersection(lb)
    if x.is_empty:
        raise SystemExit(f"{a} and {b} do not intersect in OpenStreetMap")
    c = x.centroid  # divided roads cross at several points; use their middle
    return c.x, c.y


def nearest_on(points: np.ndarray, target) -> np.ndarray:
    return shapely.get_coordinates(shapely.shortest_line(shapely.points(points), target))[1::2]


def icp(points: np.ndarray, targets: list, groups: np.ndarray, init: trace.Similarity,
        keep: float, iterations: int = 60, scale: float | None = None) -> tuple[trace.Similarity, np.ndarray]:
    """Trimmed ICP: each point (group i) is matched to its nearest spot on targets[i].

    With `scale` set, only rotation and shift are fitted (a rigid fit in those units).
    Returns the transform and every point's final distance in metres.
    """
    sim = init
    for _ in range(iterations):
        cur = sim.apply(points)
        near = np.zeros_like(cur)
        for i, tg in enumerate(targets):
            sel = groups == i
            near[sel] = nearest_on(cur[sel], tg)
        d = np.linalg.norm(cur - near, axis=1)
        inl = d <= np.quantile(d, keep)
        new = trace.fit_similarity(points[inl], near[inl])
        if scale is not None:  # refit rotation and shift with the scale held
            a = points[inl].copy()
            a[:, 1] *= -1
            b = near[inl]
            ma, mb = a.mean(0), b.mean(0)
            H = (a - ma).T @ (b - mb)
            U, _, Vt = np.linalg.svd(H)
            R = Vt.T @ U.T
            if np.linalg.det(R) < 0:
                Vt[1] *= -1
                R = Vt.T @ U.T
            rot = math.atan2(R[1, 0], R[0, 0])
            t = mb - scale * R @ ma
            new = trace.Similarity(scale, rot, float(t[0]), float(t[1]))
        done = abs(new.rotation - sim.rotation) < 1e-9 and abs(new.tx - sim.tx) < 1e-4 and abs(new.ty - sim.ty) < 1e-4
        sim = new
        if done:
            break
    cur = sim.apply(points)
    near = np.zeros_like(cur)
    for i, tg in enumerate(targets):
        sel = groups == i
        near[sel] = nearest_on(cur[sel], tg)
    return sim, np.linalg.norm(cur - near, axis=1)


def icp_report(sim: trace.Similarity, d: np.ndarray, keep: float, what: str) -> dict:
    inl = d <= np.quantile(d, keep)
    rms = float(np.sqrt((d[inl] ** 2).mean()))
    sim.labels = [f"{what}: trimmed RMS over the closest {int(keep * 100)}% of {len(d)} points"]
    sim.residuals_m = [rms]
    rep = sim.report()
    rep.update({"method": "trimmed ICP", "points": int(len(d)), "inlier_share": keep,
                "median_m": round(float(np.median(d)), 2), "p90_m": round(float(np.quantile(d, 0.9)), 2)})
    return rep


def to_wgs(g):
    return gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]


def write(project: str, site_utm, props: dict) -> None:
    fc = {
        "type": "FeatureCollection",
        "properties": {"project": project, **props},
        "features": [{"type": "Feature", "properties": {"kind": "site", "name": "Project site"},
                      "geometry": mapping(to_wgs(site_utm))}],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{project}.geojson"
    path.write_text(json.dumps(_round(fc), indent=1) + "\n")
    print(f"[traced] wrote {path.relative_to(config.ROOT)}: {site_utm.area / ACRE_M2:,.1f} acres ({props['accuracy']})")


def _round(obj, nd=7):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    return obj


def clean(g, min_acres: float = 1.0):
    """Drop slivers and pinholes under `min_acres` (gaps under road lines in the figures)."""
    parts = []
    for p in getattr(g, "geoms", [g]):
        if not isinstance(p, Polygon) or p.area < min_acres * ACRE_M2:
            continue
        holes = [h for h in p.interiors if Polygon(h).area >= min_acres * ACRE_M2]
        parts.append(Polygon(p.exterior, holes))
    return trace.largest_polygon(parts[0]) if len(parts) == 1 else shapely.MultiPolygon(parts)


# ---------------------------------------------------------------- Willow Village

WILLOW_DA = {
    "title": "Menlo Park Ordinance No. 1095, Willow Village Development Agreement (adopted Dec 13, 2022)",
    "url": "https://www.menlopark.gov/files/sharedassets/public/v/1/community-development/documents/projects/"
           "under-review/willow-village/1095-willow-village-development-agreement.pdf",
    "sha256": "aefb43a93bf4a952a88e7b9b2a8a088645c1beb4a7c9e7135b8222d0b7b45963",
    "file": "willow-village-da-ord-1095.pdf",
}
MENLO_PARCELS = "https://services7.arcgis.com/uRrQ0O3z2aaiIWYU/arcgis/rest/services/City_of_Menlo_Park_Parcels/FeatureServer/7"
US_FOOT_M = 1200 / 3937

# Exhibit A-2-1 (Freyer & Laureta, Sept 30, 2022), from the southwesterly corner of Parcel S,
# Menlo Industrial Center (99 M 81-83). ("line", quadrant bearing, feet) or ("curve left",
# radius, length); the curves are tangent to the course before them. Bearings checked
# against the plat's line and curve tables on Exhibit A-1-1 (p. 70).
WILLOW_COURSES = [
    ("line", ("N", 22, 5, 0, "E"), 120.17),
    ("line", ("N", 24, 45, 44, "E"), 143.14),
    ("curve left", 1536.52, 74.34),   # delta 02°46'19"
    ("line", ("N", 22, 5, 0, "E"), 864.41),
    ("curve left", 1032.50, 55.72),   # delta 03°05'31"
    ("line", ("N", 25, 35, 47, "E"), 2.12),
    ("line", ("N", 19, 19, 9, "E"), 144.98),
    ("line", ("N", 22, 5, 0, "E"), 71.06),
    ("line", ("N", 84, 59, 41, "E"), 1324.41),
    ("curve left", 11509.17, 251.79),  # delta 01°15'13"
    ("line", ("S", 10, 8, 21, "W"), 1612.25),
    ("line", ("S", 88, 8, 54, "W"), 1182.95),
    ("line", ("N", 79, 51, 49, "W"), 668.96),
]
WILLOW_STATED_SQFT = 2_577_434.20  # "Containing 2,577,434.20 square feet (59.17 acres), more or less."
# Rough placement of the point of beginning (UTM 10N), refined by the fit to parcel lines.
WILLOW_INIT = {"rotation_deg": -0.4, "pob": (574950.0, 4148100.0)}


def _azimuth(ns, d, m, s, ew) -> float:
    a = d + m / 60 + s / 3600
    return {("N", "E"): a, ("S", "E"): 180 - a, ("S", "W"): 180 + a, ("N", "W"): 360 - a}[(ns, ew)]


def willow_traverse() -> np.ndarray:
    """The legal description's courses as (east, north) feet from the point of beginning."""
    x = y = 0.0
    az = None
    pts = [(0.0, 0.0)]
    for c in WILLOW_COURSES:
        if c[0] == "line":
            az = _azimuth(*c[1])
            x += c[2] * math.sin(math.radians(az))
            y += c[2] * math.cos(math.radians(az))
            pts.append((x, y))
        else:
            radius, length = c[1], c[2]
            delta = -length / radius  # to the left
            n = max(4, int(abs(math.degrees(delta)) * 4))
            for i in range(1, n + 1):
                t = delta * i / n
                chord = 2 * radius * math.sin(abs(t) / 2)
                a = az + math.degrees(t) / 2
                pts.append((x + chord * math.sin(math.radians(a)), y + chord * math.cos(math.radians(a))))
            x, y = pts[-1]
            az += math.degrees(delta)
    return np.array(pts)


def build_willow_village() -> None:
    trace.fetch_document(WILLOW_DA["url"], DOCS / WILLOW_DA["file"], WILLOW_DA["sha256"])
    ft = willow_traverse()
    misclosure = float(np.hypot(*ft[-1]))
    area_sqft = Polygon(ft).area
    if misclosure > 0.1 or abs(area_sqft - WILLOW_STATED_SQFT) > 50:
        raise SystemExit(f"willow-village: legal description misclosure {misclosure:.3f} ft, area {area_sqft:,.0f} sq ft")

    cache = RAW_BOUNDARIES / "menlo-park-parcels-willow-village.geojson"
    if not cache.exists():
        q = urllib.parse.urlencode({"where": "1=1", "geometry": "-122.158,37.476,-122.136,37.490",
                                    "geometryType": "esriGeometryEnvelope", "inSR": 4326,
                                    "spatialRel": "esriSpatialRelIntersects", "outFields": "APN",
                                    "outSR": 4326, "f": "geojson"})
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(f"{MENLO_PARCELS}/query?{q}", timeout=120) as r:
            cache.write_bytes(r.read())
    parcels = gpd.GeoDataFrame.from_features(json.loads(cache.read_text())["features"], crs=4326).to_crs(UTM)
    edges = shapely.union_all(parcels.boundary.to_numpy())

    # Fit points every 2 m along the described boundary (figure coordinates: feet, y down).
    ring = LineString(np.vstack([ft, ft[:1]]))
    dense = np.array([ring.interpolate(t).coords[0] for t in np.arange(0, ring.length, 2 / US_FOOT_M)])
    fig = np.c_[dense[:, 0], -dense[:, 1]]
    rot = math.radians(WILLOW_INIT["rotation_deg"])
    init = trace.Similarity(US_FOOT_M, rot, 0, 0)
    o = init.apply([(0, 0)])[0]
    init.tx, init.ty = WILLOW_INIT["pob"][0] - o[0], WILLOW_INIT["pob"][1] - o[1]
    keep = 0.8
    sim, d = icp(fig, [edges], np.zeros(len(fig), int), init, keep, iterations=200, scale=US_FOOT_M)
    rep = icp_report(sim, d, keep, "described boundary vs Menlo Park parcel lines")
    site = Polygon(sim.apply(np.c_[ft[:, 0], -ft[:, 1]]))
    acres = site.area / ACRE_M2
    print(f"[willow-village] misclosure {misclosure:.3f} ft; fit rotation {np.degrees(sim.rotation):.3f} deg, "
          f"trimmed RMS {sim.rms_m:.2f} m, median {np.median(d):.2f} m, p90 {np.quantile(d, 0.9):.2f} m")
    write("willow-village", site, {
        "source": f"traced: {WILLOW_DA['title']}, Exhibit A-2-1 Main Project Site legal description (pp. 75-76) "
                  f"and Exhibit A-1-1 site plat (p. 70)",
        "sourceUrl": WILLOW_DA["url"],
        "sourceLabel": "development agreement map (PDF)",
        "accuracy": "traced",
        "accuracyNote": (
            f"The Main Project Site drawn from its metes-and-bounds description (closes to {misclosure:.2f} ft), "
            f"placed on the City of Menlo Park parcel lines by a rotation-and-shift fit (RMS {sim.rms_m:.1f} m over the "
            f"closest 80% of boundary points; 90% within {np.quantile(d, 0.9):.1f} m). {acres:.2f} acres as drawn; "
            f"the description states 59.17 acres. The two Hamilton parcels (about 3 acres) are not included."),
        "license": "Shape from a public City of Menlo Park ordinance; placement on City of Menlo Park parcels (CC0).",
        "georeference": rep,
        "legalDescription": {"courses": len(WILLOW_COURSES), "misclosure_ft": round(misclosure, 4),
                             "area_sqft": round(area_sqft, 1), "stated_sqft": WILLOW_STATED_SQFT},
    })


# ---------------------------------------------------------------- Concord Naval Weapons Station

CONCORD_TS = {
    "title": "Navy-City of Concord Term Sheet for the Economic Development Conveyance of NWS Concord (executed Sept 23, 2026)",
    "url": "https://www.concordreuseproject.org/DocumentCenter/View/2384",
    "sha256": "6210b7dbd166192a071ad408bce5cfe51de9c945c5ac7027490b63f2b80f725b",
    "file": "concord-nws-edc-term-sheet-2026-09-23.pdf",
}
CONCORD_PAGE = 14  # p. 15, Exhibit A
CONCORD_MAP_BOTTOM = 440  # map frame content above this (PDF points from the top); legend below
# The EDC fill and the same fill seen through the road, building and water symbols drawn
# over it (ArcGIS exports those as blended fills). CMYK as stored in the PDF.
CONCORD_EDC_FILLS = [
    (0.3314, 0.0, 0.015747, 0.0), (0.5084, 0.1143, 0.1238, 0.0), (0.4456, 0.0634, 0.0827, 0.0),
    (0.4013, 0.0226, 0.0511, 0.0), (0.627, 0.2335, 0.2079, 0.0), (0.5481, 0.1261, 0.0, 0.0),
    (0.4833, 0.2125, 0.0, 0.0), (0.5057, 0.1314, 0.2025, 0.0), (0.5601, 0.1813, 0.2488, 0.0),
    (0.5819, 0.2043, 0.2683, 0.0003), (0.6148, 0.1969, 0.1608, 0.0),
]
# Road symbols: on white, over the EDC fill, over the EBRPD fill.
CONCORD_ROADS = [(0.0, 0.0, 0.0, 0.2267), (0.627, 0.2335, 0.2079, 0.0), (0.374, 0.0596, 0.599, 0.0)]
# Starting transform: the scale bar (1,000 ft = 22 pt), the map's rotation found by a coarse
# search (about -9 degrees), and Willow Pass Road crossing SR-4 at the top of the white road strip.
CONCORD_INIT = {"scale": 0.3048 * 1000 / 22, "rotation_deg": -9.0, "fig": (267.0, 121.0), "utm": (588040.0, 4207700.0)}
CONCORD_ACRES = 2422


def build_concord() -> None:
    pdf_path = trace.fetch_document(CONCORD_TS["url"], DOCS / CONCORD_TS["file"], CONCORD_TS["sha256"])
    g = streets("concord", (-122.07, 37.93, -121.90, 38.05))
    g = g[g.intersects(shapely.box(583000, 4199000, 597000, 4212000))]
    g = g[~g["class"].isin(["footway", "cycleway", "steps", "path", "residential"])]
    target = shapely.union_all(g.geometry.to_numpy())
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[CONCORD_PAGE]
        base = [p for p in trace.pdf_filled_polygons(page, CONCORD_EDC_FILLS[0], tol=0.0006, max_top=CONCORD_MAP_BOTTOM)]
        over = [p for c in CONCORD_EDC_FILLS[1:] for p in trace.pdf_filled_polygons(page, c, tol=0.0006, max_top=CONCORD_MAP_BOTTOM)]
        roads = [p for c in CONCORD_ROADS for p in trace.pdf_filled_polygons(page, c, tol=0.0006, max_top=CONCORD_MAP_BOTTOM)]
    pts = np.unique(np.round(np.vstack([shapely.get_coordinates(p) for p in roads]), 0), axis=0)
    init = trace.Similarity(CONCORD_INIT["scale"], math.radians(CONCORD_INIT["rotation_deg"]), 0, 0)
    o = init.apply([CONCORD_INIT["fig"]])[0]
    init.tx, init.ty = CONCORD_INIT["utm"][0] - o[0], CONCORD_INIT["utm"][1] - o[1]
    keep = 0.6
    sim, d = icp(pts, [target], np.zeros(len(pts), int), init, keep, iterations=80)
    rep = icp_report(sim, d, keep, "map road lines vs OpenStreetMap roads and tracks")
    print(f"[concord] fit scale {sim.scale:.4f} m/pt (scale bar {CONCORD_INIT['scale']:.4f}), rotation "
          f"{np.degrees(sim.rotation):.2f} deg, trimmed RMS {sim.rms_m:.1f} m, median {np.median(d):.1f} m")
    # Symbols over the fill count only where they sit inside it: the same colours are used for
    # creeks and roads outside the EDC Property.
    base_u = shapely.union_all([p.buffer(0.2, join_style="mitre") for p in base]).buffer(-0.2, join_style="mitre")
    within = base_u.buffer(1.0, join_style="mitre").buffer(-1.0, join_style="mitre")
    over_u = shapely.union_all(over).intersection(within)
    fig_union = shapely.union_all([base_u.buffer(0.2, join_style="mitre"), over_u.buffer(0.2, join_style="mitre")]
                                  ).buffer(-0.2, join_style="mitre")
    site = clean(shapely.make_valid(sim.geometry(fig_union)).simplify(1.0))
    acres = site.area / ACRE_M2
    write("concord-naval-weapons-station", site, {
        "source": f"traced: {CONCORD_TS['title']}, Exhibit A, Economic Development Conveyance (EDC) Property map "
                  f"(Navy, dated 2026-03-30), p. 15",
        "sourceUrl": CONCORD_TS["url"],
        "sourceLabel": "Navy term sheet map (PDF)",
        "accuracy": "traced",
        "accuracyNote": (
            f"The EDC Property fills read from the vector map, georeferenced by fitting its road lines to OpenStreetMap "
            f"roads and tracks (RMS {sim.rms_m:.1f} m over the closest 60% of {len(d):,} points; median {np.median(d):.0f} m). "
            f"{acres:,.0f} acres as drawn; the City's staff report gives approximately {CONCORD_ACRES:,}. The water tank parcel "
            f"(EDC share to be sited later) and road strips left white on the map are not included."),
        "license": "Shape traced from a public U.S. Navy / City of Concord document. Georeference: " + OSM_LICENSE + ".",
        "georeference": rep,
    })


# ---------------------------------------------------------------- Alameda Point Site A

ALAMEDA_PLAN = {
    "title": "Alameda Point Site A Development Plan (BAR Architects, July 25, 2022), Open Space & Parcel Diagrams",
    "url": "https://legistar1.granicus.com/alameda/attachments/73ff7e59-888e-443a-afc5-9a808b1d2091.pdf",
    "sha256": "d6c786ba93bd7c07ee5a77648bfcf7605af4bf01140420b08899b937994659d2",
    "file": "alameda-point-site-a-development-plan-2022.pdf",
}
ALAMEDA_PAGE = 11  # p. 12
ALAMEDA_DPI = 300
ALAMEDA_CROP_PT = (490, 80, 1505, 525)  # the Parcel Diagram (left, top, right, bottom in PDF points)
ALAMEDA_PARCEL_GREY = 223  # parcel fill in the render
# Street centrelines in the render (pixels), each the midpoint of the gap between the parcel
# blocks on either side, measured on rows/columns 60-200 px either side of the crossing.
ALAMEDA_CONTROLS = {
    ("Ardent Way", "Coronado Avenue"): (2438.5, 725.5),
    ("Ardent Way", "West Atlantic Avenue"): (2439.75, 1260.25),
    ("Orion Street", "Coronado Avenue"): (2894.0, 725.5),
    ("Orion Street", "West Atlantic Avenue"): (2894.0, 1269.75),
    ("Corsair Street", "Coronado Avenue"): (3235.0, 726.0),
    ("Corsair Street", "West Atlantic Avenue"): (3235.0, 1274.0),
    ("Skylark Street", "Coronado Avenue"): (3662.5, 726.0),
    ("Skylark Street", "West Atlantic Avenue"): (3662.0, 1276.5),
}
ALAMEDA_INSIDE_PX = (2500, 700)  # a pixel inside Site A
ALAMEDA_ACRES = 67.8  # "+/- 67.8 SITE A" in the diagram's legend (68 acres in the DA)


def _alameda_render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[ALAMEDA_PAGE]
    w, h = page.get_size()
    left, top, right, bottom = ALAMEDA_CROP_PT
    rgb = np.asarray(page.render(scale=ALAMEDA_DPI / 72, crop=(left, h - bottom, w - right, top)).to_pil().convert("RGB"))
    if rgb.shape[:2] != (1854, 4228):
        raise SystemExit(f"unexpected Parcel Diagram render size {rgb.shape}")
    return rgb


def build_alameda_point() -> None:
    pdf_path = trace.fetch_document(ALAMEDA_PLAN["url"], DOCS / ALAMEDA_PLAN["file"], ALAMEDA_PLAN["sha256"])
    rgb = _alameda_render(pdf_path)
    g = streets("alameda_point", (-122.31, 37.77, -122.28, 37.79))
    # West Atlantic Avenue's old alignment runs further south; use the rebuilt street only.
    g = g[g.intersects(shapely.box(561700, 4181640, 562600, 4182200))]
    src, dst, labels = [], [], []
    for (a, b), xy in ALAMEDA_CONTROLS.items():
        src.append(xy)
        dst.append(intersection(g, a, b))
        labels.append(f"{a} / {b}")
    sim = trace.fit_similarity(src, dst, labels)
    print(f"[alameda-point] RMS {sim.rms_m:.2f} m over {len(labels)} intersections, scale {sim.scale:.4f} m/px")

    # The dotted Site A line: black dashes. Bridge the dash gaps, fill from outside, keep the
    # enclosed region, then grow it back to the middle of the line.
    v = rgb.max(axis=2)
    dark = (v < 70).astype(np.uint8)
    k = 13
    walls = cv2.dilate(dark, np.ones((k, k), np.uint8))
    flood = walls * 255
    mask = np.zeros((flood.shape[0] + 2, flood.shape[1] + 2), np.uint8)
    cv2.floodFill(flood, mask, (5, 5), 128)
    _, lab = cv2.connectedComponents((flood == 0).astype(np.uint8))
    inside = (lab == lab[ALAMEDA_INSIDE_PX[1], ALAMEDA_INSIDE_PX[0]]).astype(np.uint8)
    # Labels printed against the line, e.g. "(18c) 0.31 ACRE", merge with it and leave notches;
    # a closing fills them (the site's own steps are far wider than the 101-px kernel).
    inside = cv2.morphologyEx(inside, cv2.MORPH_CLOSE, np.ones((101, 101), np.uint8))
    contours, _ = cv2.findContours(inside, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    px = Polygon(c.reshape(-1, 2) + 0.5).buffer(0)
    # Distance from the inside edge back to the dash centre: the dilation radius plus half the dash.
    # Measured on the top edge (West Tower Avenue), where the dashes run straight across.
    top_edge = px.bounds[1]
    dash_rows = np.nonzero(dark[: int(top_edge), 2200:3600])[0]
    if not len(dash_rows):
        raise SystemExit("alameda-point: dotted boundary not found above the traced area")
    grow = top_edge - float(np.median(dash_rows))
    px = px.buffer(grow, join_style="mitre").simplify(1.5)
    site = trace.largest_polygon(sim.geometry(px))
    acres = site.area / ACRE_M2
    write("alameda-point", site, {
        "source": f"traced: {ALAMEDA_PLAN['title']}, Parcel Diagram, p. 12",
        "sourceUrl": ALAMEDA_PLAN["url"],
        "sourceLabel": "Site A development plan (PDF)",
        "accuracy": "traced",
        "accuracyNote": (
            f"The dotted Site A boundary traced from the plan's Parcel Diagram, georeferenced to OpenStreetMap street "
            f"centrelines at {len(labels)} intersections (RMS {sim.rms_m:.1f} m). {acres:.1f} acres as drawn; the "
            f"diagram states +/- {ALAMEDA_ACRES} acres. Approximate boundary: parcel lines were not available."),
        "license": "Shape traced from a public City of Alameda document. Georeference: " + OSM_LICENSE + ".",
        "georeference": {**sim.report(), "dash_offset_px": round(grow, 2)},
    })


# ---------------------------------------------------------------- Suisun City expansion

SUISUN_NOP = {
    "title": "Suisun Expansion Project Notice of Preparation (City of Suisun City, SCH 2025110452, Nov 2025)",
    "url": "https://ceqanet.lci.ca.gov/2025110452/Attachment/nT6gPE",
    "sha256": "323d68604838ea6c122b73eb9fd33020ed1895e0699ba47e7f49375df4eedc47",
    "file": "suisun-expansion-nop-2025110452.pdf",
}
SUISUN_PAGE = 14  # p. 15, Figure 2
SUISUN_IMAGE_SIZE = (2500, 1419)
SUISUN_LEGEND_X = 2200  # legend panel starts here (image pixels)
# Fill colours in the figure: Specific Plan, Travis Protection Zone (plain and hatched) and
# Lambie Industrial Park, plus the hatch lines.
SUISUN_FILLS = [(243, 239, 178), (165, 177, 141), (159, 192, 237), (158, 167, 134), (120, 130, 100)]
# Hand-traced guides (image pixels) along the two highways used as control lines; road
# casing pixels within 8 px of a guide are fitted to that highway in OpenStreetMap.
SUISUN_GUIDES = {
    "SR-12": [(450, 745), (770, 745), (1012, 990), (1500, 990)],
    "SR-113": [(1176, 985), (1177, 424), (1096, 422), (1096, 5)],
}
# Starting transform: the 2-mile scale bar (about 19.5 m per image pixel) and SR-12 meeting SR-113.
SUISUN_INIT = {"scale": 19.5, "rotation_deg": 0.0, "fig": (1176.0, 989.0), "utm": (604500.0, 4226850.0)}
SUISUN_ACRES = 22873


def _suisun_image(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[SUISUN_PAGE]
    for obj in page.get_objects():
        if obj.type == 3:  # image
            rgb = np.asarray(obj.get_bitmap(render=False).to_pil().convert("RGB"))
            if rgb.shape[1::-1] == SUISUN_IMAGE_SIZE:
                return rgb
    raise SystemExit("Figure 2 image not found")


def build_suisun() -> None:
    pdf_path = trace.fetch_document(SUISUN_NOP["url"], DOCS / SUISUN_NOP["file"], SUISUN_NOP["sha256"])
    rgb = _suisun_image(pdf_path).astype(float)
    g = streets("suisun", (-122.10, 38.05, -121.60, 38.40))
    osm = {
        "SR-12": g[(g["class"] == "trunk") & g.intersects(shapely.box(588000, 4224000, 612000, 4234000))],
        "SR-113": g[(g["class"] == "primary") & g.intersects(shapely.box(601000, 4226500, 606000, 4260000))],
    }
    v = rgb.mean(axis=2)
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    casing = (v < 120) & (sat < 14) & (v > 45)
    pts, groups, targets = [], [], []
    for i, (name, guide) in enumerate(SUISUN_GUIDES.items()):
        m = np.zeros(casing.shape, np.uint8)
        cv2.polylines(m, [np.array(guide, np.int32)], False, 1, 17)
        ys, xs = np.nonzero(m.astype(bool) & casing)
        pts.append(np.c_[xs, ys].astype(float))
        groups.append(np.full(len(xs), i))
        targets.append(shapely.union_all(osm[name].geometry.to_numpy()))
    pts, groups = np.vstack(pts), np.concatenate(groups)
    init = trace.Similarity(SUISUN_INIT["scale"], math.radians(SUISUN_INIT["rotation_deg"]), 0, 0)
    o = init.apply([SUISUN_INIT["fig"]])[0]
    init.tx, init.ty = SUISUN_INIT["utm"][0] - o[0], SUISUN_INIT["utm"][1] - o[1]
    keep = 0.8
    sim, d = icp(pts, targets, groups, init, keep, iterations=60)
    rep = icp_report(sim, d, keep, "SR-12 and SR-113 casings vs OpenStreetMap")
    rep["per_road_median_m"] = {n: round(float(np.median(d[groups == i])), 1) for i, n in enumerate(SUISUN_GUIDES)}
    print(f"[suisun] scale {sim.scale:.2f} m/px, rotation {np.degrees(sim.rotation):.2f} deg, "
          f"trimmed RMS {sim.rms_m:.0f} m, median {np.median(d):.0f} m")

    pal = np.array(SUISUN_FILLS, float)
    dist = np.linalg.norm(rgb[:, :, None, :] - pal[None, None], axis=3).min(axis=2)
    fill = (dist < 22).astype(np.uint8)
    fill[:, SUISUN_LEGEND_X:] = 0
    fill = cv2.morphologyEx(fill, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # The dash-dot annexation line (and the 20-year-plan dashes inside) belong to the area.
    dark = ((v < 110) & (sat < 25)).astype(np.uint8)
    area = fill | (dark & cv2.dilate(fill, np.ones((13, 13), np.uint8)))
    area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    contours, _ = cv2.findContours(area, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(contours, key=cv2.contourArea)
    px = Polygon(c.reshape(-1, 2) + 0.5).buffer(0).simplify(1.0)
    site = trace.largest_polygon(sim.geometry(px))
    acres = site.area / ACRE_M2
    write("suisun-expansion", site, {
        "source": f"traced: {SUISUN_NOP['title']}, Figure 2, Annexation Area, Area Plan, Specific Plan, and "
                  f"20 Year Plan Boundaries, p. 15",
        "sourceUrl": SUISUN_NOP["url"],
        "sourceLabel": "notice of preparation figure (PDF)",
        "accuracy": "approximate",
        "accuracyNote": (
            f"Approximate boundary: the annexation area traced from a small-scale raster figure (about "
            f"{sim.scale:.0f} m per pixel), fitted to SR-12 and SR-113 in OpenStreetMap (RMS {sim.rms_m:.0f} m over the "
            f"closest 80% of road pixels; median {np.median(d):.0f} m). {acres:,.0f} acres as drawn; the NOP states "
            f"{SUISUN_ACRES:,} acres."),
        "license": "Shape traced from a public City of Suisun City CEQA notice. Georeference: " + OSM_LICENSE + ".",
        "georeference": rep,
    })


BUILDERS = {
    "willow-village": build_willow_village,
    "concord-naval-weapons-station": build_concord,
    "alameda-point": build_alameda_point,
    "suisun-expansion": build_suisun,
}


def main(ids: list[str]) -> None:
    for project in ids or list(BUILDERS):
        BUILDERS[project]()


if __name__ == "__main__":
    main(sys.argv[1:])
