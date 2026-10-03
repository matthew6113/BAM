"""India Basin (700 Innes): parcel height limits traced from the adopted design standards.

Source:
- India Basin Design Standards and Guidelines (DSG), July 6, 2018, adopted by Planning Commission
  Motion 20252 on July 26, 2018. Figure 5-3 "Maximum Height" (PDF p. 277, printed p. 263) gives the
  maximum height zones; Figure 5-1 "Parcels and Parcel Breaks" (PDF p. 275, printed p. 261) names
  the parcels; Appendix A.1 "Parcel Control Plan" (PDF pp. 348-363) gives each parcel's primary use.
- Standard 5.2.3 (PDF p. 276): buildings in a tower location are at least 85 ft and at most 160 ft.
- DSG Amendment, Exhibits B and C, published by SF Planning on October 17, 2024: adds a "Small Lot
  Home" option in the Flats and keeps the Section 5.2 height limits (its list of amendments has no
  Section 5.2 or Figure 5-3 item, and its new roof standard 8.3.4.2 refers back to "the maximum height
  set forth in Section 5.2"). The module checks that list, so the 2018 heights are drawn as current.

What this is and isn't:
- Each height zone is drawn to its limit, not as a building design. Real buildings will be smaller
  and set back, stepped back and broken by parcel breaks (Sections 5.1, 5.4, 5.5), so the massing is
  labelled illustrative.
- The two tower locations (parcels C1 and H1) are drawn to 160 ft. The DSG requires 85-160 ft there
  and caps tower floor plates above 60 ft at 12,000 gsf.
- Open-space parcels (OS1-OS14, including the Big Green, which Figure 5-3 shows with a 30-ft limit for
  park structures) and the city's parks (900 Innes, India Basin Shoreline Park) are not massing.
- Nothing has been built on the private site: DBI's grading permits are still in plan check.

Georeferencing:
- Figure 5-3 is vector art. Its base map draws existing buildings, and 130-odd of them match
  OpenStreetMap footprints (via Overture) one to one. A rough start from three Innes Avenue
  intersections is refined by a raster correlation of the figure's buildings against Overture's, then
  by a least-squares similarity on the centroids of every figure building that overlaps an Overture
  footprint by IoU > 0.6. The fit and its residuals are recorded in the output.
- As a check, the traced zones are compared with the official India Basin SUD outline (DataSF):
  the zones should fall inside it. The slivers outside it are trimmed and their area is reported.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_india_basin
"""

from __future__ import annotations

import json
import os
import re

import cv2
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
from . import traced_boundaries as tb

PROJECT_ID = "india-basin"
UTM = tb.UTM
DOCS = config.ROOT / "data" / "raw" / "docs"

DSG = {
    "title": "India Basin Design Standards and Guidelines (July 6, 2018; Planning Commission Motion 20252)",
    "url": "https://sfplanning.s3.amazonaws.com/default/files/devagreements/indiabasin/IndiaBasin_Design_Standards_and_Guidelines.pdf",
    "sha256": "2ca5b5d804882ce430a54ff0c3967e61b0c13acc8af5e2527f0cce82d3a0ccc4",
    "file": "india-basin-dsg-2018.pdf",
}
FIG_5_3 = {"page_index": 276, "printed_page": "263", "figure": "Figure 5-3, Maximum Height"}
FIG_5_1 = {"page_index": 274, "printed_page": "261", "figure": "Figure 5-1, Parcels and Parcel Breaks"}
PARCEL_PLAN_PAGES = range(347, 363)  # Appendix A.1, Figures A-1 to A-16

# Linked from sfplanning.org/india-basin-mixed-use-project ("Design Standards and Guidelines
# Amendment, published October 17, 2024"); an M-Files shared link on SF Planning's server.
AMENDMENT = {
    "title": "India Basin DSG Amendment, Exhibits B and C (published by SF Planning Oct 17, 2024)",
    "url": "https://citypln-m-extnl.sfgov.org/REST/sharedlinks/%7ba4a7dacd-b0dc-4322-bd29-f6f07103c6e0%7d/"
           "390dc9ff22ed2e574daed0847aa9081f8a3ed41e5e0a7bc812723a2a59b93c1b/content",
    "page_url": "https://citypln-m-extnl.sfgov.org/SharedLinks.aspx?accesskey=390dc9ff22ed2e574daed0847aa9081f8a3ed41e5e0a7bc812723a2a59b93c1b"
                "&VaultGUID=A4A7DACD-B0DC-4322-BD29-F6F07103C6E0",
    "sha256": "a1b03e4d25f0b4430bd5cfbe378741bfef63458a70ad493253f2a3d5955b07a1",
    "file": "india-basin-dsg-amendment-2024.pdf",
    "list_pages": range(0, 4),  # Exhibit B, List of Proposed Amendments
}

TOWER_FT = 160
TOWER_MIN_FT = 85
# A rough start only (figure points, PDF units): where Griffith Street, Arelious Walker Drive and
# Earl Street meet Innes Avenue in the figure. The building match below does the real fit.
ROUGH_START = {("Innes Avenue", "Griffith Street"): (205, 297), ("Innes Avenue", "Arelious Walker Drive"): (372, 403),
               ("Innes Avenue", "Earl Street"): (526, 523)}
STREETS_BBOX = (-122.385, 37.726, -122.366, 37.740)
BUILDINGS_BBOX = (-122.384, 37.727, -122.368, 37.738)
FIGURE_BUILDINGS_BOX = (0, 60, 792, 560)  # figure area with base-map buildings (PDF units), legend excluded
PARCEL_LABEL = re.compile(r"(C|H|F|OS)\d+[AB]?(-F\d+)?")


# ---------------------------------------------------------------- documents

def check_amendment() -> None:
    """The 2024 amendment must not touch the height controls (Section 5.2 / Figure 5-3)."""
    import pypdfium2 as pdfium

    path = trace.fetch_document(AMENDMENT["url"], DOCS / AMENDMENT["file"], AMENDMENT["sha256"])
    doc = pdfium.PdfDocument(str(path))
    items = "\n".join(doc[i].get_textpage().get_text_range() for i in AMENDMENT["list_pages"])
    if "Exhibit B" not in items or "Small Lot Home" not in items:
        raise SystemExit("the 2024 DSG amendment's list of amendments was not where expected")
    if re.search(r"(?<![\d.])5\.2(?:\.\d+)?(?![\d.])|Figure 5-3|Building Height", items):
        raise SystemExit("the 2024 DSG amendment lists a change to Section 5.2 heights; review before drawing")


def _color(o) -> tuple:
    c = o.get("non_stroking_color")
    if isinstance(c, (int, float)):
        c = (c,)
    return tuple(round(v, 3) if isinstance(v, (int, float)) else str(v) for v in (c or ()))


def _fills(page) -> list[tuple[tuple, Polygon]]:
    out = []
    for o in page.curves + page.rects:
        pts = o.get("pts")
        if o.get("fill") and pts and len(pts) >= 3:
            g = shapely.make_valid(Polygon(pts))
            if not g.is_empty and g.area > 0:
                out.append((_color(o), g))
    return out


def height_labels(page) -> list[tuple[int, Point]]:
    """Every "(NN')" label on Figure 5-3, read char by char (the PDF's words run into nearby text)."""
    chars = page.chars
    out = []
    for c in chars:
        if c["text"] != "(":
            continue
        run = sorted((d for d in chars if abs(d["top"] - c["top"]) < 0.5 and c["x0"] <= d["x0"] < c["x0"] + 25),
                     key=lambda d: d["x0"])
        m = re.match(r"\((\d+)’\)", "".join(d["text"] for d in run))
        if m:
            end = run[len(m.group(0)) - 1]
            out.append((int(m.group(1)), Point((c["x0"] + end["x1"]) / 2, (c["top"] + c["bottom"]) / 2)))
    return out


def _is_height_colour(col) -> bool:
    """The legend runs from pale peach (30 ft) to dark red (80 ft): red clearly above green and blue."""
    return len(col) == 3 and col[0] > col[1] + 0.08 and col[0] > col[2] + 0.1


def height_zones(page) -> list[dict]:
    """Figure 5-3 height zones, in figure coordinates.

    Every zone fill carries a "(NN')" label, but some labels are split in the PDF's text. The
    complete labels give each fill colour its height (checked for consistency); the hatched tower
    locations are pattern fills labelled "(160')"; the white "(20')" zones are the white fills that
    hold exactly that one label.
    """
    labels = height_labels(page)
    fills = _fills(page)
    votes: dict[tuple, set] = {}
    labelled = []
    for i, (col, g) in enumerate(fills):
        inside = [h for h, pt in labels if g.contains(pt)]
        if len(inside) == 1 and g.area < 10000 and (_is_height_colour(col) or (col and col[0] == "P")):
            votes.setdefault(col, set()).add(inside[0])
            labelled.append(i)
    # The zones are drawn as one group; other art (landscape, buildings) reuses some of their colours.
    first, last = min(labelled), max(labelled)
    zones = []
    for i, (col, g) in enumerate(fills):
        if not first <= i <= last:
            continue
        hs = votes.get(col, set())
        is_pattern = bool(col) and col[0] == "P"
        if col == (1.0, 1.0, 1.0) or is_pattern:
            inside = [h for h, pt in labels if g.contains(pt)]
            if is_pattern and inside == [TOWER_FT]:
                zones.append({"height_ft": TOWER_FT, "tower": True, "px": g})
            elif col == (1.0, 1.0, 1.0) and inside == [20] and g.area < 1000:
                zones.append({"height_ft": 20, "tower": False, "px": g})
            continue
        # Height colours are the reds and oranges whose labelled fills agree on one height.
        if len(hs) == 1 and _is_height_colour(col):
            zones.append({"height_ft": next(iter(hs)), "tower": False, "px": g})
    for col, hs in votes.items():
        if _is_height_colour(col) and len(hs) > 1:
            raise SystemExit(f"Figure 5-3 colour {col} carries several heights {sorted(hs)}")
    found = sorted({z["height_ft"] for z in zones})
    if found != [20, 30, 35, 45, 50, 55, 60, 65, 70, 80, 160]:
        raise SystemExit(f"unexpected Figure 5-3 heights {found}")
    return zones


def parcels(page) -> tuple[dict[str, tuple[float, float]], dict[str, Polygon]]:
    """Figure 5-1 parcels, in figure coordinates: regions of the parcel-boundary linework around each label.

    The parcel boundary is a dash-dot path; drawn solid on a raster, it closes each parcel, which is
    flood-filled from its label. Figures 5-1 and 5-3 share one base map and page position.
    """
    labels = {}
    # Parcel labels are horizontal 8.8-9.6 pt text; rotated street names nearby are left out.
    bold = page.filter(lambda o: o.get("object_type") != "char"
                       or (8.5 < o.get("size", 0) < 9.7 and abs(o["matrix"][1]) < 1e-6 and abs(o["matrix"][2]) < 1e-6))
    for w in bold.extract_words(x_tolerance=1.5):
        if PARCEL_LABEL.fullmatch(w["text"]):
            labels[w["text"]] = ((w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2)
    k = 4
    h, w = int(page.height * k), int(page.width * k)
    img = np.zeros((h, w), np.uint8)
    for o in page.curves + page.lines:
        if o.get("stroke") and str(o.get("dash")).startswith("([3.998") and o.get("pts"):
            cv2.polylines(img, [(np.array(o["pts"]) * k).round().astype(np.int32)], False, 255, thickness=3)
    out = {}
    for name, (x, y) in labels.items():
        mask = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(img.copy(), mask, (int(x * k), int(y * k)), 128)
        reg = mask[1:-1, 1:-1]
        cs, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        poly = Polygon(max(cs, key=cv2.contourArea).reshape(-1, 2) / k).buffer(0)
        # A label printed on a street or a gap in the linework floods the street network: skip it
        # (the largest real parcel, OS3, is about 28,000 square units).
        if poly.area > 40000:
            continue
        out[name] = poly
    return labels, out


def assign_parcels(zones: list[dict], labels: dict, regions: dict) -> list[dict]:
    """Give each height zone its parcel name, in figure coordinates.

    A zone takes the parcel region it mostly lies in. Where one region carries two labels (F4 and F5
    share an outline in Figure 5-1), the label inside the zone wins. A zone drawn across a parcel line
    (H1/H2) is split along it. Zones on the townhome micro-lots (F9-F18), which the flood fill can't
    resolve, take the nearest parcel label.
    """
    def name_for(region_name: str, g) -> str:
        twins = [n for n, r in regions.items() if r.equals_exact(regions[region_name], 0.01)]
        inside = [n for n in twins if g.contains(Point(labels[n]))]
        return inside[0] if inside else region_name

    out = []
    for z in zones:
        shares = sorted(((r.intersection(z["px"]).area / z["px"].area, n) for n, r in regions.items()), reverse=True)
        (s1, n1), (s2, n2) = shares[0], shares[1]
        if s1 >= 0.25 and s2 >= 0.25 and not regions[n1].equals_exact(regions[n2], 0.01):
            rest = z["px"]
            pieces = []
            for share, n in shares:
                if share < 0.1:
                    break
                piece = rest.intersection(regions[n].buffer(1.0))
                rest = rest.difference(piece)
                pieces.append([n, piece])
            pieces[0][1] = shapely.union_all([pieces[0][1], rest])  # slivers on the parcel line
            out += [dict(z, px=g, parcel=n) for n, g in pieces if g.area > 1]
        elif s1 >= 0.5:
            out.append(dict(z, parcel=name_for(n1, z["px"])))
        else:
            c = z["px"].centroid
            n, d = min(((n, c.distance(Point(xy))) for n, xy in labels.items()), key=lambda t: t[1])
            if d > 40:
                raise SystemExit(f"a {z['height_ft']}-ft zone lies in no Figure 5-1 parcel")
            out.append(dict(z, parcel=n))
    return out


def primary_uses(pdf_path) -> dict[str, str]:
    """Parcel -> primary land use from the Parcel Control Plan (Appendix A.1)."""
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf_path))
    uses = {}
    for i in PARCEL_PLAN_PAGES:
        t = doc[i].get_textpage().get_text_range()
        fig = re.search(r"Figure A-\d+: Parcel (.+?) - Plan", t)
        use = re.search(r"Primary Land Use (Mixed-Use|Residential)", t)
        if not fig or not use:
            raise SystemExit(f"no parcel or primary use on DSG PDF page {i + 1}")
        spec = fig.group(1).strip()
        if " to " in spec:  # "F9 to F18"
            a, b = (int(n.strip()[1:]) for n in spec.split(" to "))
            names = [f"F{n}" for n in range(a, b + 1)]
        else:
            names = [n.strip() for n in spec.split("&")]
        for n in names:
            uses[n] = use.group(1).lower()
    return uses


def figure_buildings(page, zones_px) -> list[Polygon]:
    """Existing-building outlines in the figure's base map, away from the project's height zones."""
    keep_out = shapely.union_all([z["px"] for z in zones_px]).buffer(3)
    x0, y0, x1, y1 = FIGURE_BUILDINGS_BOX
    out = []
    for col, g in _fills(page):
        b = g.bounds
        if col == (1.0, 1.0, 1.0) and 8 < g.area < 1500 and b[0] > x0 and b[1] > y0 and b[2] < x1 and b[3] < y1 \
                and not g.intersects(keep_out):
            out.append(g)
    return out


# ---------------------------------------------------------------- base data

def overture_buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "buildings_india_basin.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BUILDINGS_BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326)
    return g.to_crs(UTM)


# ---------------------------------------------------------------- georeference

def _raster(geoms, x0, y_top, n, res) -> np.ndarray:
    img = np.zeros((n, n), np.float32)
    for g in geoms:
        for q in getattr(g, "geoms", [g]):
            if q.geom_type == "Polygon":
                a = np.asarray(q.exterior.coords)
                px = np.c_[(a[:, 0] - x0) / res, (y_top - a[:, 1]) / res].round().astype(np.int32)
                cv2.fillPoly(img, [px], 1.0)
    return img


def georeference(fig_bld: list[Polygon], osm_bld: gpd.GeoDataFrame, streets, centre) -> tuple[trace.Similarity, dict]:
    src = list(ROUGH_START.values())
    dst = [tb.intersection(streets, a, b) for a, b in ROUGH_START]
    rough = trace.fit_similarity(src, dst)

    # 1. Raster correlation of figure buildings against Overture buildings (0.5 m cells, +/-50 m shift).
    res, half, margin = 0.5, 500.0, 100
    n = int(2 * half / res)
    x0, y_top = centre.x - half, centre.y + half
    target = _raster(osm_bld.geometry.to_numpy(), x0, y_top, n, res)
    pivot = np.asarray(shapely.union_all(fig_bld).centroid.coords[0])
    best = None
    for ds_ in np.linspace(-0.02, 0.02, 5):
        for dr in np.radians(np.linspace(-2, 2, 9)):
            sim = trace.Similarity(rough.scale * (1 + ds_), rough.rotation + dr, 0.0, 0.0)
            sim.tx, sim.ty = rough.apply([pivot])[0] - sim.apply([pivot])[0]
            moving = _raster([sim.geometry(b) for b in fig_bld], x0, y_top, n, res)
            r = cv2.matchTemplate(target, moving[margin:-margin, margin:-margin], cv2.TM_CCORR_NORMED)
            _, score, _, loc = cv2.minMaxLoc(r)
            if best is None or score > best[0]:
                best = (score, sim, loc)
    score, sim, loc = best
    sim.tx += (loc[0] - margin) * res
    sim.ty -= (loc[1] - margin) * res

    # 2. Least squares on matched building centroids (IoU > 0.6), repeated until the matches settle.
    tree = shapely.STRtree(osm_bld.geometry.to_numpy())
    geoms = osm_bld.geometry.to_numpy()
    matched = None
    for _ in range(10):
        a, b = [], []
        for f in fig_bld:
            g = sim.geometry(f)
            for j in tree.query(g):
                o = geoms[j]
                if g.intersection(o).area / g.union(o).area > 0.6:
                    a.append(f.centroid.coords[0])
                    b.append(o.centroid.coords[0])
        if len(a) < 30:
            raise SystemExit(f"only {len(a)} figure buildings matched OpenStreetMap; the fit is not reliable")
        sim = trace.fit_similarity(a, b)
        if matched == len(a):
            break
        matched = len(a)
    r = np.asarray(sim.residuals_m)
    report = {
        "method": "building-footprint match: raster correlation, then least squares on the centroids of figure "
                  "buildings matching OpenStreetMap footprints (IoU > 0.6)",
        "scale_m_per_unit": round(sim.scale, 5),
        "rotation_deg": round(float(np.degrees(sim.rotation)), 3),
        "rms_m": round(sim.rms_m, 2),
        "median_m": round(float(np.median(r)), 2),
        "max_m": round(float(r.max()), 2),
        "controls": int(len(r)),
        "figure_buildings": len(fig_bld),
        "correlation": round(float(score), 3),
    }
    return sim, report


# ---------------------------------------------------------------- main

def main() -> None:
    check_amendment()
    pdf_path = trace.fetch_document(DSG["url"], DOCS / DSG["file"], DSG["sha256"])
    with pdfplumber.open(pdf_path) as pdf:
        zones = height_zones(pdf.pages[FIG_5_3["page_index"]])
        fig_bld = figure_buildings(pdf.pages[FIG_5_3["page_index"]], zones)
        parcel_labels, parcel_px = parcels(pdf.pages[FIG_5_1["page_index"]])

    uses = primary_uses(pdf_path)
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    sud = site.geometry.iloc[0]
    streets = tb.streets("india_basin", STREETS_BBOX)
    osm_bld = overture_buildings()
    sim, report = georeference(fig_bld, osm_bld, streets, sud.centroid)
    print(f"[india-basin] Figure 5-3 georeference: RMS {report['rms_m']} m over {report['controls']} matched buildings, "
          f"scale {report['scale_m_per_unit']} m/unit, rotation {report['rotation_deg']} deg")

    # Name each zone by its Figure 5-1 parcel; split zones drawn across a parcel line; drop open space.
    named = assign_parcels(zones, parcel_labels, parcel_px)
    open_space = [z for z in named if z["parcel"].startswith("OS")]
    zones = [z for z in named if not z["parcel"].startswith("OS")]

    # Georeference, trim to the official SUD outline, and merge zones of one height in one parcel.
    merged: dict[tuple, object] = {}
    raw_area = trimmed = 0.0
    for z in zones:
        g = shapely.make_valid(sim.geometry(z["px"]))
        raw_area += g.area
        inside = g.intersection(sud)
        trimmed += g.area - inside.area
        key = (z["parcel"], z["height_ft"], z["tower"])
        merged[key] = shapely.union_all([merged[key], inside]) if key in merged else inside
    check = {"zones_m2": round(raw_area), "outside_sud_m2": round(trimmed),
             "outside_sud_share": round(trimmed / raw_area, 4)}
    print(f"[india-basin] {len(merged)} height zones; {check['outside_sud_m2']} m2 "
          f"({check['outside_sud_share']:.1%}) fell outside the SUD outline and was trimmed")
    if check["outside_sud_share"] > 0.03:
        raise SystemExit("too much of the traced massing falls outside the SUD outline; check the georeference")

    def order(k):
        m = re.match(r"([A-Z]+)(\d+)", k[0])
        return ("CHF".index(m.group(1)), int(m.group(2)), k[0], k[1])

    dsg = f"{DSG['title']}, {FIG_5_3['figure']}, p. {FIG_5_3['printed_page']}"
    features = []
    for key in sorted(merged, key=order):
        parcel, h, tower = key
        geom = merged[key].buffer(0.25, join_style="mitre").buffer(-0.25, join_style="mitre").simplify(0.4)
        geom = trace.as_multipolygon(shapely.make_valid(geom))
        geom = trace.as_multipolygon(shapely.MultiPolygon([p for p in geom.geoms if p.area >= 15]))
        if geom.is_empty:
            continue
        use_key = parcel.split("-")[0]
        props = {
            "kind": "block",
            "block": parcel,
            "label": (f"Parcels {parcel.replace('-', '–')}" if "-" in parcel else f"Parcel {parcel}") + (" tower" if tower else ""),
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": None,
            "base_ft": 0,
            "use": uses.get(use_key),
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: drawn to the height limit traced from {dsg}"
                      + (f"; tower location, {TOWER_MIN_FT} ft minimum to {TOWER_FT} ft maximum (Standard 5.2.3, p. 262)"
                         if tower else ""),
        }
        if tower:
            props["note"] = (f"Tower location: buildings here must be {TOWER_MIN_FT}-{TOWER_FT} ft tall, with floor "
                             "plates above 60 ft capped at 12,000 gsf (DSG 5.2.3, 5.3.3).")
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(geom))})
    print(f"[india-basin] drew {len(features)} zones: "
          + ", ".join(f"{f['properties']['block']}:{f['properties']['height_ft']}" for f in features))
    print("[india-basin] left out open space: " + ", ".join(f"{z['parcel']}:{z['height_ft']}" for z in open_space))

    massing_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each part of a development parcel at 700 Innes is drawn to its maximum "
                "height in the design standards adopted in 2018 (Fig. 5-3), not as a building design. Towers at "
                "parcels C1 and H1 may rise to 160 ft. The open space and the city's India Basin Waterfront Park "
                "aren't massed, and nothing has been built on the private site yet."
            ),
            "note": ("Parcels are drawn to their height limits in the 2018 design standards, not as building designs; "
                     "real buildings will be smaller."),
            "sourceUrl": DSG["url"],
            "sourceLabel": "Design standards, 2018 (PDF)",
            "georeference": {"figure_5_3": report, "check_against_sud": check},
            "documents": {
                "design_standards": {"title": DSG["title"], "url": DSG["url"], "sha256": DSG["sha256"],
                                     "pages": "Fig. 5-1 p. 261, Fig. 5-3 p. 263, Std. 5.2.3 p. 262, App. A.1"},
                "amendment_2024": {"title": AMENDMENT["title"], "url": AMENDMENT["page_url"], "sha256": AMENDMENT["sha256"],
                                   "finding": "Adds a Small Lot Home option in the Flats; no change to Section 5.2 heights."},
            },
            "license": "Zone shapes: traced from a public SF Planning document. Georeferenced to OpenStreetMap "
                       "building footprints (ODbL 1.0) via Overture Maps.",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(massing_fc), indent=1) + "\n")
    print(f"[india-basin] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
