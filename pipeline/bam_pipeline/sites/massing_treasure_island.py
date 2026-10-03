"""Treasure Island: block height limits from the zoning map, checked against the 2024 Design for
Development, and the project buildings that are finished.

Sources:
- Block height limits: DataSF "Zoning Map – Height and Bulk Districts" (h9wh-cg3m, Public Domain
  U.S. Government), the "-TI" districts. On Treasure Island the layer is drawn block by block, with
  streets, parks and the shoreline in "25-TI" (open space), which is left out. The values already
  carry the 2024 amendment (45, 65 and 75 ft, up from 40, 60 and 70 ft; TIDA, Mar 13, 2024, item 7:
  "Adds 5 feet to the maximum height limits ... of the zoning map"), and "<base>-TI/<tower> Flex
  Zone-TI" districts are the flex height zones of the Design for Development: a building may rise to
  the tower height there under its tower rules (D4D T4.4.2), otherwise the base height applies.
- Block names and the height check: Treasure Island and Yerba Buena Island Design for Development
  (D4D), April 4, 2024 update, Figure T4.q "Maximum Height Plan" (printed p. 169, PDF page 187),
  georeferenced on the zoning layer itself: the figure's solid height fills (vector shapes in the
  PDF) are matched to the zoning blocks of the same height and a similarity is fitted to their
  centroids. Every zoning zone is then checked against the figure's colour (base height) and hatch
  (flex zone) inside it: 116 of 120 agree. The four that don't are the plain 65-ft strips between
  the two flex zones of Blocks E6 and E8, which the figure hatches as 240-ft flex, and two edge
  slivers of C11 and C12 that the figure leaves blank. The zoning map, the legal control, is drawn. Uses come from Figure T3.d "Key Plan to the Treasure Island Land Use Table"
  (printed p. 157): TI-R residential, TI-MU mixed use, TI-PCI the school site.
- Why the zoning layer and not a trace of Figure T4.q: they're the same map (the 2024 amendment
  brought the zoning map into line with the D4D height plan) and the check below finds them in
  agreement zone by zone, but the zoning layer is surveyed GIS while a trace of a page figure carries
  the fit error (about 2 m). So the layer gives the shapes and the D4D gives the names.
- Built buildings (DBI permits marked complete; footprints from OpenStreetMap via Overture):
  Isle House (Parcel C2.4, 22 stories, permit 201912169619) is the landmark; its height is mapped in
  OpenStreetMap (67 m). The others have no mapped height, so their heights are estimated from their
  permitted stories at 10.3 ft a story, the average of the two Phase 1 towers SF Planning described in
  2019 (C2.1 "approximately 31-story, 315-foot", C2.4 "approximately 19-story, 200-foot"; memo
  2007.0903PHA, Aug 22, 2019, p. 2), and are labelled illustrative. Isle House checks the rule:
  22 stories at 10.3 ft is 227 ft against its mapped 220 ft. The five Meadow Drive townhouse buildings
  on Yerba Buena Island (Parcel 4Y; four DBI permits complete, 3 and 4 stories) can't be matched one
  to one with their permits, so they are drawn together at the 35-ft limit of their district.

What this is and isn't:
- Unbuilt blocks are drawn to their height limits, not as building designs, so the massing is
  labelled illustrative. Flex zones are drawn at the tower limit over the base height (podium_ft);
  the D4D limits how many towers rise and how big they are, so most of each flex zone will stay at
  its base height.
- The D4D's Special Height District around historic Buildings 1–3 (heights vary, Figure T4.t) is
  not in the zoning layer's "-TI" districts and isn't drawn; nor are the historic buildings.
- The wastewater plant and SFPUC site (TI-PCI utilities) and the Job Corps campus aren't drawn.
- Yerba Buena Island's height districts are drawn over whole hillside areas, with roads and existing
  homes inside them, so only the island's new buildings are drawn there.
- Issued but unfinished permits aren't drawn as buildings (no footprint yet): Parcel B1 (5 stories,
  117 homes, issued 2021), 401 California Avenue (6 stories, 150 homes, issued July 2026), two
  buildings at 150 4th Street (issued 2025 and 2026) and the 449 Avenue H training facility.
- Rooftop allowances above the limits (D4D T4.4.5) and the 55-ft Shared Public Way allowance in
  45-ft zones (T4.4.8) aren't drawn. The developer's 2026 request for more homes isn't approved and
  isn't drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_treasure_island
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request

import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import Point, Polygon, mapping

from .. import config, trace

PROJECT_ID = "treasure-island"
UTM = "EPSG:26910"
FT = 0.3048
BBOX = (-122.3800, 37.8080, -122.3580, 37.8340)  # lon/lat window over both islands
DOCS = config.ROOT / "data" / "raw" / "docs"

HEIGHTS = {
    "title": "DataSF Zoning Map – Height and Bulk Districts",
    "landing": "https://data.sf.gov/d/h9wh-cg3m",
    "url": "https://data.sf.gov/resource/h9wh-cg3m.geojson?" + urllib.parse.urlencode({
        "$where": "height like '%-TI%' or height like '%YBI%'",
        "$limit": 5000,
    }),
    "cache": config.ROOT / "data" / "raw" / "massing" / "ti-height-bulk.geojson",
}
D4D = {
    "title": "Treasure Island and Yerba Buena Island Design for Development (April 4, 2024 update)",
    "url": "https://api.sf.gov/documents/36177/240404-D4D_UPDATE.pdf",
    "file": "ti-240404-D4D_UPDATE.pdf",
    "sha256": "b09cb66477de5844720d244c3fd7f3f3c9fcce8ffce87af1ae0b89f0151986d8",
}
FIG = {"page_index": 186, "printed_page": "169", "figure": "Figure T4.q, Maximum Height Plan"}
LANDUSE_FIG = "Figure T3.d, Key Plan to the Treasure Island Land Use Table, p. 157"
PLAN_2019 = {
    "title": "SF Planning memo to the Planning Commission, Treasure Island Subphase 1C, Blocks C2.1 & C2.4 "
             "(Record 2007.0903PHA, Aug 22, 2019)",
    "url": "https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2007.0903PHA.pdf",
    "file": "ti-2007.0903PHA.pdf",
    "sha256": "dca95f054b09fb86cc8c5158e24437e45565b784e7053e9a1cb2d9a98b09500e",
}
TIDA_2024 = "https://www.sf.gov/sites/default/files/2024-03/031324%20Item%207%20DDA%20Amendments.pdf"
# 2019 Planning memo, p. 2: the two Phase 1 towers' stories and heights, for the story-height rule.
TOWERS_2019 = [("approximately 31-story, 315-foot", 31, 315), ("approximately 19-story, 200-foot", 19, 200)]
FT_PER_STORY = round(sum(h for _, _, h in TOWERS_2019) / sum(s for _, s, _ in TOWERS_2019), 1)  # 10.3

# Figure T4.q's solid fills (RGB in the PDF) for each base height, and the render's hatch colours.
FILL = {65: (1.0, 0.731, 0.387), 75: (1.0, 0.502, 0.242), 85: (0.675, 0.851, 0.911),
        125: (0.0, 0.637, 0.863), 50: (0.741, 0.598, 0.602)}
RENDER_BASE = {45: (255, 238, 187), 50: (190, 152, 155), 65: (255, 188, 99), 75: (255, 128, 62),
               85: (174, 218, 233), 125: (0, 162, 220)}
RENDER_HATCH = {240: (34, 64, 117), 315: (219, 56, 133), 450: (179, 22, 25)}
DPI = 200
# Starting fit: four blocks named in the figure (label centre, PDF points) and a point inside the
# matching zoning block (UTM). The fit is then refined on every matched fill.
INIT = {
    "School": ((245.7, 310.0), (555090, 4186883)),
    "C12": ((361.8, 305.2), (555248, 4186594)),
    "P1": ((622.4, 199.5), (555927, 4186020)),
    "B1-B": ((632.7, 454.2), (555250, 4185673)),
}
# Block labels in Figure T4.q (centre of the text, PDF points; read with pdfplumber).
LABELS = {
    "E7": (480.5, 150.3), "E8": (542.0, 150.2), "E5": (489.8, 175.8), "E6": (553.0, 175.8),
    "E3": (500.3, 201.3), "E4": (562.5, 201.3), "E2": (512.0, 226.8), "E1": (574.3, 226.8),
    "P1": (622.4, 199.5), "B3": (631.1, 251.0), "B3-A": (655.4, 250.8), "B2": (631.1, 312.6),
    "B2-A": (655.5, 312.6), "IC1": (537.5, 259.5), "IC2": (587.9, 259.5), "IC4": (540.1, 297.5),
    "IC3": (600.3, 297.5), "C13": (299.5, 305.2), "C12": (361.8, 305.2), "School": (245.7, 310.0),
    "C8-A": (236.1, 356.7), "C8-B": (232.0, 369.7), "C9-A": (256.5, 347.4), "C9-B": (264.7, 369.5),
    "C10-A": (319.3, 346.7), "C10-B": (326.8, 366.0), "C11": (377.8, 347.7), "M1-A": (622.5, 360.1),
    "M1-B": (647.1, 360.1), "C7-A": (229.0, 390.8), "C6-A": (274.6, 392.0), "C5-A": (335.2, 391.1),
    "C4-A": (397.2, 392.0), "C3-A": (459.4, 392.0), "C2-A": (520.2, 392.1), "C1": (582.1, 393.8),
    "B1-A": (635.5, 391.1), "B1": (633.7, 408.6), "C2-B": (528.2, 414.5), "C7-B": (241.2, 420.7),
    "C6-B": (285.1, 420.2), "C5-B": (347.0, 420.0), "C4-B": (408.6, 420.2), "C3-B": (468.6, 420.0),
    "C2-H": (564.0, 432.3), "B1-B": (632.7, 454.2), "WWTP": (253.3, 154.0), "PUC": (286.1, 154.3),
    "Cultural Park": (594.2, 417.6),
}
NOT_DRAWN = {"WWTP", "PUC", "Cultural Park"}  # TI-PCI utility sites; a park zoned 65-TI
MIXED_USE = {"C1", "C2-H", "IC1", "IC2", "IC3", "IC4", "B1", "B1-A", "B1-B", "B2", "B2-A", "B3", "B3-A",
             "M1-A", "M1-B", "P1"}


def _use(label: str) -> str:
    if label == "School":
        return "School (public, civic and institutional)"
    if label == "P1":
        return "Mixed use (sailing center)"
    return "Mixed use" if label in MIXED_USE else "Residential"


# Finished project buildings: OSM ids of the footprints in Overture, and the DBI permits.
PERMIT_URL = "https://data.sf.gov/resource/i98e-djp9.json?permit_number={}"
BUILT = [
    {"label": "Isle House", "osm": ["w1249412094"], "permit": ["201912169619"], "stories": 22, "homes": 250,
     "parcel": "C2.4", "complete": "2024-12-10", "landmark": True},
    {"label": "Hawkins", "osm": ["w1249412093"], "permit": ["201912169614"], "stories": 6, "homes": 178,
     "parcel": "C2.2", "complete": "2025-08-29"},
    {"label": "Maceo May", "osm": ["r19685981"], "permit": ["201810223762"], "stories": 6, "homes": 105,
     "parcel": None, "complete": "2023-12-28"},
    {"label": "Star View Court", "osm": ["w1212173437"], "permit": ["201912139581"], "stories": 7, "homes": 138,
     "parcel": None, "complete": "2024-06-27"},
    {"label": "490 Avenue of the Palms", "osm": ["w1272162518"], "permit": ["202011199306"], "stories": 6,
     "homes": 148, "parcel": "C3.4", "complete": "2026-03-09"},
    {"label": "The Bristol", "osm": ["w813225688"], "permit": ["201808137195"], "stories": 6, "homes": 124,
     "parcel": None, "complete": "2022-06-24", "ybi": True},
    {"label": "Meadow Drive townhouses", "parcel": "4Y", "ybi": True, "zone_limit": True,
     "osm": ["w1228080320", "w1228080321", "w1228080322", "w1249412140", "w1375946326"],
     "permit": ["201905170929", "201905170931", "201905170934", "201905170935"], "stories": None, "homes": 30,
     "complete": "2025-02-20 and 2025-02-24"},
]


def _fetch_heights() -> gpd.GeoDataFrame:
    out = HEIGHTS["cache"]
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(HEIGHTS["url"]) as r:
            out.write_bytes(r.read())
    return gpd.read_file(out).to_crs(UTM)


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "ti-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f), cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    g["name"] = g["names"].apply(lambda n: (n or {}).get("primary"))
    g["osm"] = g["sources"].apply(
        lambda s: (next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None) or "").split("@")[0])
    g["height_from"] = g["sources"].apply(
        lambda s: next((x.get("dataset") for x in s if x.get("property") == "/properties/height"), "OpenStreetMap"))
    return g.to_crs(UTM)


def _text(pdf_path, page_index: int) -> str:
    import pypdfium2 as pdfium

    return re.sub(r"\s+", " ", pdfium.PdfDocument(str(pdf_path))[page_index].get_textpage().get_text_range())


def _figure(pdf_path):
    """Figure T4.q: its solid height fills (PDF points) and a 200-dpi render."""
    import pypdfium2 as pdfium

    if "Figure T4.q: Maximum Height Plan" not in _text(pdf_path, FIG["page_index"]):
        raise SystemExit("Figure T4.q is not on the expected D4D page")
    with pdfplumber.open(str(pdf_path), pages=[FIG["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        fills = []
        for h, col in FILL.items():
            polys = []
            for o in page.curves + page.rects:
                c, pts = o.get("non_stroking_color"), o.get("pts")
                if (not o.get("fill") or not isinstance(c, (tuple, list)) or len(c) != 3 or not pts or len(pts) < 3
                        or o["top"] > 480):  # the legend is below
                    continue
                if max(abs(a - b) for a, b in zip(c, col)) <= 0.01:
                    polys.append(shapely.make_valid(Polygon(pts)))
            u = shapely.union_all(polys)
            fills += [(h, g) for g in getattr(u, "geoms", [u]) if g.geom_type == "Polygon" and g.area > 4]
    rgb = np.asarray(pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]].render(scale=DPI / 72).to_pil().convert("RGB"))
    return fills, rgb


def _georeference(fills, zones: gpd.GeoDataFrame) -> trace.Similarity:
    """Fit Figure T4.q to the zoning layer: match each solid fill to the zoning zone of the same height."""
    src, dst = [], []
    for name, (fig_xy, utm_xy) in INIT.items():
        hit = zones[zones.geometry.contains(Point(utm_xy))]
        if len(hit) != 1:
            raise SystemExit(f"starting point for {name} is not in exactly one zoning zone")
        c = hit.geometry.iloc[0].centroid
        src.append(fig_xy)
        dst.append((c.x, c.y))
    sim = trace.fit_similarity(src, dst, list(INIT))
    plain = [(int(r["height"].split("-")[0]), r.geometry) for _, r in zones.iterrows() if "Flex" not in r["height"]]
    for _ in range(5):
        src, dst, labels = [], [], []
        for h, g in fills:
            c = sim.geometry(g)
            cands = [(zg.centroid.distance(c.centroid), zg) for zh, zg in plain if zh == h]
            if not cands:
                continue
            d, zg = min(cands, key=lambda t: t[0])
            if d < 30 and 0.7 < c.area / zg.area < 1.4:
                src.append((g.centroid.x, g.centroid.y))
                dst.append((zg.centroid.x, zg.centroid.y))
                labels.append(f"{h}-ft fill at figure ({g.centroid.x:.0f}, {g.centroid.y:.0f}) pt")
        sim = trace.fit_similarity(src, dst, labels)
    if len(src) < 15 or sim.rms_m > 4:
        raise SystemExit(f"Figure T4.q fit is poor: {len(src)} matches, RMS {sim.rms_m:.1f} m")
    return sim


def _to_figure(sim: trace.Similarity, g):
    """UTM geometry -> 200-dpi figure pixels."""
    m = np.linalg.inv(sim.matrix())

    def f(xy):
        a = (m @ (np.asarray(xy) - [sim.tx, sim.ty]).T).T
        a[:, 1] *= -1
        return a * DPI / 72

    return shapely.transform(g, f)


def _check_zone(rgb: np.ndarray, poly_px) -> tuple[int | None, int | None]:
    """The base height (majority legend colour) and flex hatch found inside a zone in the figure."""
    import cv2

    inner = poly_px.buffer(-4)
    if inner.is_empty:
        inner = poly_px
    mask = np.zeros(rgb.shape[:2], np.uint8)
    for p in getattr(inner, "geoms", [inner]):
        cv2.fillPoly(mask, [np.round(np.asarray(p.exterior.coords)).astype(np.int32)], 1)
    px = rgb[mask.astype(bool)].astype(int)
    if not len(px):
        return None, None

    def share(col):
        return float((np.abs(px - col).max(axis=1) <= 18).mean())

    base = {h: share(c) for h, c in RENDER_BASE.items()}
    hatch = {h: share(c) for h, c in RENDER_HATCH.items()}
    b = max(base, key=base.get)
    t = max(hatch, key=hatch.get)
    return (b if base[b] > 0.2 else None), (t if hatch[t] > 0.04 else None)


def _parse(district: str) -> tuple[int, int | None]:
    """'65-TI' -> (65, None); '65-TI/240 Flex Zone-TI' -> (65, 240)."""
    m = re.fullmatch(r"(\d+)-TI(?:/(\d+) Flex Zone-TI)?", district)
    if not m:
        raise SystemExit(f"unexpected district {district!r}")
    return int(m.group(1)), (int(m.group(2)) if m.group(2) else None)


def _labels(zones: gpd.GeoDataFrame, sim: trace.Similarity) -> list[str]:
    """Each zone's D4D block: zones that touch form a block; it takes the Figure T4.q label in it."""
    merged = shapely.union_all([g.buffer(1.0) for g in zones.geometry])
    blocks = list(getattr(merged, "geoms", [merged]))
    pts = {k: Point(sim.apply([xy])[0]) for k, xy in LABELS.items()}
    out = []
    for g in zones.geometry:
        blk = next(b for b in blocks if b.intersects(g))
        inside = [k for k, p in pts.items() if blk.buffer(8).contains(p)]
        if not inside:
            # Small detached pieces whose label sits on a neighbour: the nearest label.
            near = min(pts, key=lambda k: g.distance(pts[k]))
            if g.distance(pts[near]) > 100:
                raise SystemExit(f"no Figure T4.q label near the zoning zone at {g.centroid}")
            print(f"[treasure-island]   zone at ({g.centroid.x:.0f}, {g.centroid.y:.0f}) takes the nearest label, "
                  f"{near} ({g.distance(pts[near]):.0f} m)")
            inside = [near]
        out.append(min(inside, key=lambda k: g.distance(pts[k])))
    return out


def main() -> None:
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    hb = _fetch_heights()
    zones = hb[hb["height"].str.contains("-TI") & (hb["height"] != "25-TI")]
    zones = zones.explode(index_parts=False).reset_index(drop=True)
    zones = zones[zones.geometry.area > 20].reset_index(drop=True)
    if any("/40 " in h or re.match(r"(40|60|70)-TI", h) for h in zones["height"]):
        raise SystemExit("zoning layer still has pre-2024 height values")
    print(f"[treasure-island] {len(zones)} Treasure Island height zones (25-TI open space left out)")

    pdf_path = trace.fetch_document(D4D["url"], DOCS / D4D["file"], D4D["sha256"])
    fills, rgb = _figure(pdf_path)
    sim = _georeference(fills, zones)
    print(f"[treasure-island] Figure T4.q fit to the zoning layer: RMS {sim.rms_m:.2f} m over "
          f"{len(sim.labels)} matched height fills, scale {sim.scale:.4f} m/pt")

    zones["block"] = _labels(zones, sim)

    # Zone by zone check against the figure.
    mismatches = []
    for _, z in zones.iterrows():
        base, tower = _parse(z["height"])
        got_base, got_tower = _check_zone(rgb, _to_figure(sim, z.geometry))
        if got_base != base or got_tower != tower:
            mismatches.append((z["height"], got_base, got_tower, round(z.geometry.area), z["block"]))
    agree = len(zones) - len(mismatches)
    print(f"[treasure-island] zoning vs Figure T4.q: {agree} of {len(zones)} zones agree on base height and flex zone")
    for m in mismatches:
        print(f"[treasure-island]   differs: {m[4]}, zoning {m[0]} vs figure base {m[1]}, flex {m[2]} ({m[3]} m²)")
    if agree / len(zones) < 0.9:
        raise SystemExit("zoning and Figure T4.q disagree; review before drawing")

    zones = zones[~zones["block"].isin(NOT_DRAWN)].reset_index(drop=True)

    # Story-height rule from the 2019 Planning memo.
    memo = trace.fetch_document(PLAN_2019["url"], DOCS / PLAN_2019["file"], PLAN_2019["sha256"])
    memo_text = _text(memo, 1).replace("19- story", "19-story")
    for quote, _, _ in TOWERS_2019:
        if quote not in memo_text:
            raise SystemExit(f"2019 Planning memo no longer says {quote!r}")

    bldgs = _buildings()
    built = []
    for spec in BUILT:
        rows = bldgs[bldgs["osm"].isin(spec["osm"])]
        if len(rows) != len(spec["osm"]):
            raise SystemExit(f"{spec['label']}: expected {len(spec['osm'])} footprints, found {len(rows)}")
        geom = shapely.union_all(rows.geometry.to_numpy())
        if not site_utm.buffer(10).contains(geom.centroid):
            raise SystemExit(f"{spec['label']} is off the site")
        built.append((spec, rows, geom))
        print(f"[treasure-island] {spec['label']}: {', '.join(spec['osm'])}, {geom.area:.0f} m², "
              f"mapped height {rows['height'].tolist()} from {rows['height_from'].tolist()}")
    built_union = shapely.union_all([g for _, _, g in built])

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731
    fig = f"{D4D['title']}, {FIG['figure']}, p. {FIG['printed_page']}"
    features = []

    def order(z):
        b = z["block"]
        m = re.match(r"([A-Z]+)(\d*)", b)
        return (m.group(1), int(m.group(2) or 0), b, -_parse(z["height"])[0])

    for _, z in sorted(zones.iterrows(), key=lambda kv: order(kv[1])):
        geom = z.geometry.difference(built_union) if z.geometry.intersects(built_union) else z.geometry
        geom = shapely.make_valid(geom.simplify(0.4))
        # Drop slivers left between a building and its zone's edge.
        geom = shapely.union_all([g for g in getattr(geom, "geoms", [geom])
                                  if g.geom_type == "Polygon" and g.area > 40 and not g.buffer(-1.5).is_empty])
        if geom.is_empty:
            continue
        base, tower = _parse(z["height"])
        blk = z["block"]
        props = {
            "kind": "block",
            "block": blk,
            "label": blk if blk in ("School",) else f"Block {blk}",
            "stage": "entitled",
            "height_ft": tower or base,
            "podium_ft": base if tower else None,
            "base_ft": 0,
            "use": _use(blk),
            "phase": None,
            "illustrative": True,
            "source": (f"illustrative: drawn to the height limit of zoning district \"{z['height']}\" in "
                       f"{HEIGHTS['title']} ({HEIGHTS['landing']}); block name and check from {fig}; "
                       f"use from {LANDUSE_FIG}"),
        }
        if tower:
            props["note"] = (f"Flex height zone: {base} ft, with towers allowed to {tower} ft under the "
                             "Design for Development's tower rules (T4.4.2).")
        elif base == 45:
            props["note"] = "45 ft, up to 55 ft along the Shared Public Way in some cases (D4D T4.4.8)."
        features.append({"type": "Feature", "properties": props,
                         "geometry": mapping(to_wgs(trace.as_multipolygon(geom)))})

    ybi_limit = 35  # "35-Low Rise YBI"; D4D Figure Y4.k: 35 feet
    for spec, rows, geom in built:
        permits = ", ".join(f"{p} ({PERMIT_URL.format(p)})" for p in spec["permit"])
        footprint = (f"footprint{'s' if len(spec['osm']) > 1 else ''}: OpenStreetMap {', '.join(spec['osm'])} "
                     f"via Overture {config.OVERTURE_RELEASE}")
        stories = spec["stories"]
        row = rows.iloc[0]
        note = None
        if spec.get("zone_limit"):
            height_ft = ybi_limit
            illustrative = True
            height_src = (f"height: drawn to the {ybi_limit}-ft limit of zoning district \"35-Low Rise YBI\" "
                          f"({HEIGHTS['landing']}); the permits give 3 and 4 stories")
            note = ("Five buildings of 3 and 4 stories under four permits that can't be matched one to one, "
                    f"so they're drawn together at their district's {ybi_limit}-ft limit.")
        elif len(rows) == 1 and row["height_from"] == "OpenStreetMap" and row["height"] == row["height"]:
            height_ft = round(float(row["height"]) / FT)
            illustrative = False
            height_src = f"height: {row['height']:.0f} m as mapped in OpenStreetMap"
        else:
            height_ft = round(stories * FT_PER_STORY)
            illustrative = True
            height_src = (f"height estimated from the permitted stories at {FT_PER_STORY} ft a story "
                          f"({stories} × {FT_PER_STORY} ft), the average of the two Phase 1 towers in "
                          f"{PLAN_2019['title']}, p. 2 ({PLAN_2019['url']})")
            note = "No mapped height: the height is estimated from the permitted stories."
        source = (f"{footprint}; stories: DBI permit{'s' if len(spec['permit']) > 1 else ''} {permits}, "
                  f"marked complete {spec['complete']}; {height_src}")
        props = {
            "kind": "landmark" if spec.get("landmark") else "building",
            "block": spec.get("parcel"),
            "label": spec["label"],
            "stage": "complete",
            "height_ft": height_ft,
            "podium_ft": None,
            "base_ft": 0,
            "use": "Residential",
            "phase": None,
            "illustrative": illustrative,
            "source": ("illustrative: " if illustrative else "") + source,
            "stories": stories,
            "homes": spec["homes"],
        }
        if note:
            props["note"] = note
        if spec.get("landmark"):
            props["note"] = (f"22 stories (DBI permit); the 2019 Planning memo described the C2.4 design at about "
                             f"19 stories and 200 ft before it grew to the permitted 22.")
        if not props["block"]:
            del props["block"]
        g = shapely.make_valid(geom.simplify(0.3))
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(g))})

    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    n_blocks = len({f["properties"]["block"] for f in features if f["properties"]["kind"] == "block"})
    massing_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                f"Illustrative massing: Treasure Island's {n_blocks} development blocks are drawn to the height "
                "limits of the city's zoning map, which matches the 2024 Design for Development, not as building "
                "designs. Flex zones show the tower limit over the base height, though only a few towers may "
                "be built. The finished buildings, including the 22-story Isle House, are drawn from their "
                "real footprints with stories from building permits; heights not mapped are estimated. Parks, "
                "streets, historic Buildings 1–3 and Yerba Buena Island's height districts aren't drawn."
            ),
            "note": ("Blocks are drawn to their height limits, not as building designs; "
                     "real buildings will be smaller and only a few towers are allowed."),
            "sourceUrl": D4D["url"],
            "sourceLabel": "Design for Development, 2024 (PDF)",
            "georeference": {
                "zoning": "GIS layer, used as published (no tracing)",
                "figure_t4q": {**sim.report(), "method": "solid height fills matched to zoning blocks of the "
                               "same height; similarity fitted to their centroids",
                               "use": "block names and a zone-by-zone height check",
                               "check": f"{agree} of {agree + len(mismatches)} zoning zones match the figure's base "
                                        "height and flex zone",
                               "differences": [f"Block {m[4]}: zoning {m[0]} ({m[3]} m²); figure "
                                               + (f"{m[1]} ft with {m[2]}-ft flex hatching" if m[1] and m[2]
                                                  else "no height fill (edge sliver)") for m in mismatches]},
            },
            "license": ("Block shapes: DataSF zoning map (Public Domain U.S. Government). Building footprints and "
                        "mapped heights: OpenStreetMap contributors (ODbL 1.0), via Overture Maps."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round(massing_fc), separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"[treasure-island] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size // 1024} KB)")


def _round(obj, nd=7):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round(v, nd) for v in obj]
    return obj


if __name__ == "__main__":
    main()
