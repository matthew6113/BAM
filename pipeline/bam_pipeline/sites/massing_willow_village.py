"""Willow Village: building footprints and maximum heights from the approved master plan.

Source:
- Willow Village Master Plan, Conditional Development Permit plan set dated October 19, 2022
  ("Project Plans", 66 sheets), approved by the Menlo Park City Council on December 13, 2022.
  Sheet G3.04 "Illustrative Building Height Plan" (PDF page 20) draws every proposed building and
  tabulates each one's maximum height ("Individual Bldg Max. Height") and the CDP height standards
  (R-MU 85 ft maximum, 62.5 ft average; O 120 ft maximum, 70 ft average).
- The recorded Conditional Development Permit (notice of its terms and conditions), Section 2.3.5:
  "Building heights shall not exceed the maximum heights provided on Sheet G3.04 of the Project
  Plans." Section 2.2.3 defines "Illustrative Plans" as one possible layout that ACPs may vary from.
- Cross-check: the Planning Commission approved architectural control plans (ACPs) for the Phase 1
  buildings between June and September 2023. Their building height analyses give the same maximum
  heights as G3.04 (to 0.1 ft; RS7 is 75.98 ft against 76.06 ft). They are listed in ACP_CHECK with
  their pages; `--check-acps` downloads them (about 500 MB) and confirms each figure is printed there.

What this is and isn't:
- Each footprint is the building outline drawn on G3.04, which the CDP calls illustrative, extruded
  to that building's maximum height. Real buildings step down from their maximum (the sheet's
  weighted average heights are 62-68 ft), so every feature is labelled illustrative.
- O7, the meeting and collaboration space, reaches 118.04 ft only at its atrium roof ridge (ACP
  weighted average 59.80 ft); it is drawn to the maximum like the others, with a note.
- G3.04 draws Town Square retail building TS3 as the west end of office building O4 without a line
  between them, so the two are one footprint at O4's height, with a note.
- The elevated park rides on the O7 roof and bridges Willow Road; it has no height of its own on
  G3.04 and is not massed. Parks, the town square and other open space are not massed. One small
  unlabelled shape on G3.04 (at the Main Street bend, next to RS3) is left out; RA2 (an alternative
  pump-station site, not drawn on G3.04) is left out.
- Nothing has been built: Meta paused the project on May 1, 2026 and the city suspended review of
  improvement plans and maps, so every building is "entitled". The existing Menlo Science and
  Technology Park buildings stay in the base map.

Georeferencing: the G3.04 site boundary is vector (dash-dot red lines). It is fitted to the site
boundary traced from the development agreement's legal description (data/boundaries/willow-village,
itself fitted to Menlo Park parcel lines at 0.2 m RMS) by trimmed ICP with a free similarity; the
fitted scale is checked against the sheet's nominal 1" = 100'. As a coarse independent check, five
roof corners of existing buildings in the sheet's aerial base are compared with OpenStreetMap
footprints (Overture). Street intersections were not used: the aerial base predates or differs
from OpenStreetMap's Hamilton Avenue, and Willow Road / Ivy Drive is hidden under a label.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_willow_village [--check-acps]
"""

from __future__ import annotations

import json
import os
import re
import sys

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import pypdfium2 as pdfium
import shapely
import shapely.ops
from shapely.geometry import LineString, Point, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "willow-village"
UTM = tb.UTM
DOCS = config.ROOT / "data" / "raw" / "docs"
MP = "https://www.menlopark.gov/files/sharedassets/public"
WV = f"{MP}/v/1/community-development/documents/projects/under-review/willow-village"

PLAN_SET = {
    "title": "Willow Village Master Plan, Conditional Development Permit plan set (Oct 19, 2022; approved Dec 13, 2022)",
    "url": f"{MP}/v/2/community-development/documents/projects/under-review/willow-village/october-2022/masterplan-plan-set.pdf",
    "sha256": "a1f943b4ab3bb7891eab5c28677329fef275e28aea1bcc3c0910885db32c2705",
    "file": "wv-masterplan-plan-set.pdf",
}
CDP = {
    "title": "Notice of terms and conditions of the Willow Village Conditional Development Permit",
    "url": f"{WV}/notice-of-terms-and-conditions-of-conditional-development-permit.pdf",
    "sha256": "3510de24e3bf4d4b1f4a82f15c5642a18e8de54209c40e6d87ea2759184a112b",
    "file": "wv-cdp-notice.pdf",
    "page_index": 9,  # CDP p. 5, Section 2.3.5
}
G304 = {"page_index": 19, "sheet": "G3.04", "figure": "Sheet G3.04, Illustrative Building Height Plan"}
RENDER = 3  # pixels per PDF point (0.14 m per pixel)
MAP_RIGHT = 1822  # map frame's right edge (PDF points); the tables are to its right
TAN = (239, 224, 185)  # building fill, RGB
NOMINAL_M_PER_PT = 0.3048 * 100 / 72  # "1 inch = 100 ft at 24 x 36"
# Independent check: roof corners of three existing buildings south of the site, read from
# G3.04's aerial base (PDF points, y down), against the nearest corner of their Overture
# (OpenStreetMap) footprints. Two flat-roofed buildings on O'Brien Drive / Adams Court.
CHECK = {
    "roof SW corner, building south of O'Brien Drive roundabout": (1211.7, 1508.3),
    "roof NW corner, same building": (1230.0, 1395.0),
    "roof NE corner, same building": (1296.0, 1405.0),
    "roof SW corner, building on Adams Court": (1577.3, 1494.3),
    "roof SE corner, building on Adams Court": (1790.7, 1494.3),
}
BBOX = (-122.162, 37.472, -122.136, 37.492)
LABEL = re.compile(r"(O\d|SP\d|TS\d|RS\d|RA\d|NG|SG)")
MAX_LABEL_GAP_PT = 60  # a shape belongs to the nearest building label within this distance

NAMES = {
    "O1": ("Office building O1", "office"), "O2": ("Office building O2", "office"),
    "O3": ("Office building O3", "office"), "O4": ("Office building O4 and Town Square retail TS3", "office, retail"),
    "O5": ("Office building O5", "office"), "O6": ("Office building O6", "office"),
    "O7": ("Meeting and collaboration space (O7)", "office"),
    "NG": ("North Garage", "parking"), "SG": ("South Garage", "parking"),
    "SP1": ("Security pavilion SP1", "office"), "SP2": ("Security pavilion SP2", "office"),
    "TS1": ("Hotel (TS1)", "hotel, retail"), "TS2": ("Town Square retail TS2", "retail"),
    "RS2": ("Parcel 2 residential (RS2)", "residential, retail"),
    "RS3": ("Parcel 3 residential (RS3)", "residential, retail"),
    "RS4": ("Parcel 4 residential (RS4)", "residential"), "RS5": ("Parcel 5 residential (RS5)", "residential, retail"),
    "RS6": ("Parcel 6 residential (RS6)", "residential"), "RS7": ("Parcel 7 residential (RS7)", "residential"),
    "RA1": ("Building RA1", None),
}

# The 2023 ACPs' maximum heights (ft), with the page that states them. Not used for drawing.
ACP_CHECK = {
    "office-campus": ("office-campus.pdf", {"O1": (108, "67.46"), "O2": (109, "83.41"),
        "O3": (110, "83.13"), "O4": (111, "82.31"), "O5": (112, "83.17"), "O6": (113, "82.27"),
        "SG": (114, "83.29"), "NG": (115, "92.55")}),
    "meeting-and-collaboration-space": ("meeting-and-collaboration-space-and-elevated-park.pdf", {"O7": (29, "118.04")}),
    "hotel": ("willow-village-hotel.pdf", {"TS1": (28, "84.48")}),
    "town-square": ("town-square.pdf", {"TS2": (19, "35.32")}),
    "parcel-2": ("mixed-use-parcel-2.pdf", {"RS2": (39, "78.14")}),
    "parcel-3": ("mixed-use-parcel-3-plan-set.pdf", {"RS3": (34, "84.15")}),
    "parcel-6": ("willow-village-parcel-6.pdf", {"RS6": (35, "79.78")}),
    "parcel-7": ("willow-village-parcel-7.pdf", {"RS7": (27, "75.98")}),
}
ACP_URL = f"{WV}/architectural-control-plans/"


# ---------------------------------------------------------------- documents

def _words(page) -> list[dict]:
    """Words on the sheet, with the map labels' doubled characters (fill + outline) collapsed."""
    out = []
    for w in page.extract_words():
        t = w["text"]
        if len(t) % 2 == 0 and len(t) > 1 and t[::2] == t[1::2]:
            t = t[::2]
        out.append(dict(w, text=t))
    return out


def height_table(pdf_path) -> tuple[dict[str, float], dict[str, float]]:
    """G3.04's 'Individual Bldg Max. Height' per building and the CDP maximum per zone."""
    text = pdfium.PdfDocument(str(pdf_path))[G304["page_index"]].get_textpage().get_text_range()
    if "Illustratvie Building Height Plan" not in text or "G3.04" not in text:
        raise SystemExit("PDF page 20 is not sheet G3.04")
    table = text[text.index("ILLUSTRATIVE BUILDING HEIGHT AS DEPICTED"):]
    heights = {m.group(1): float(m.group(2)) for m in re.finditer(r"\b(RS\d|RA\d|O\d|SP\d|NG|SG|TS\d)\**\s+(\d+\.\d+)", table)}
    cdp = text[text.index("CDP STANDARDS"):text.index("ILLUSTRATIVE BUILDING HEIGHT")]
    caps = {m.group(1): float(m.group(2)) for m in re.finditer(r"\b(R - MU|R-MU|O)\s+(\d+)\*?\s", cdp)}
    zones = {"R-MU": ["RS2", "RS3", "RS4", "RS5", "RS6", "RS7", "RA1", "RA2"],
             "O": ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "SP1", "SP2", "NG", "SG", "TS1", "TS2", "TS3"]}
    want = [b for ids in zones.values() for b in ids]
    if sorted(heights) != sorted(want) or caps != {"R-MU": 85.0, "O": 120.0}:
        raise SystemExit(f"G3.04 table not read as expected: {heights} {caps}")
    for z, ids in zones.items():
        for b in ids:
            if heights[b] > caps[z]:
                raise SystemExit(f"{b} {heights[b]} ft is above the CDP {z} maximum")
    return heights, {b: z for z, ids in zones.items() for b in ids}


def check_cdp(pdf_path) -> None:
    text = " ".join(pdfium.PdfDocument(str(pdf_path))[CDP["page_index"]].get_textpage().get_text_range().split())
    if "Building heights shall not exceed the maximum heights provided on Sheet G3.04" not in text:
        raise SystemExit("CDP Section 2.3.5 not found where expected")


def check_acps(heights: dict[str, float]) -> dict:
    out = {}
    for fname, items in ACP_CHECK.values():
        path = trace.fetch_document(ACP_URL + fname, DOCS / f"wv-acp-{fname}")
        doc = pdfium.PdfDocument(str(path))
        for b, (page, value) in items.items():
            text = doc[page - 1].get_textpage().get_text_range()
            if value not in text:
                raise SystemExit(f"ACP {fname} p. {page}: {value} not found for {b}")
            out[b] = {"acp": fname, "page": page, "max_ft": float(value), "g304_ft": heights[b]}
    return out


# ---------------------------------------------------------------- figure

def site_boundary_points(page) -> np.ndarray:
    """Points every 2 PDF units along G3.04's dash-dot red site boundary."""
    pts = []
    for o in page.lines + page.curves:
        dash = o.get("dash")
        if (str(o.get("stroking_color")) == "(0.824, 0.137, 0.165)" and o.get("linewidth") == 5
                and dash and len(dash[0]) > 2 and o["x1"] < MAP_RIGHT):
            line = LineString(o["pts"])
            pts += [line.interpolate(t).coords[0] for t in np.arange(0, line.length, 2.0)]
    if len(pts) < 1000:
        raise SystemExit(f"only {len(pts)} site-boundary points found on G3.04")
    return np.asarray(pts)


def building_shapes(pdf_path, page) -> tuple[dict[str, Polygon], list[Polygon]]:
    """Tan building fills on G3.04 (figure units), one shape per building label.

    Each fill (label holes filled) goes to the label printed inside it, or else to the nearest label
    within MAX_LABEL_GAP_PT; fills no label reaches are returned separately and left out. G3.04
    draws two pairs as one fill: O5 and O6 (joined by a connector) are split on the perpendicular
    bisector of their labels, which crosses the connector; security pavilion SP2 is the wing that
    sticks out of the North Garage's west wall, found as what a 45-pt opening of the fill removes.
    TS3 has no outline of its own and stays with O4.
    """
    img = np.asarray(pdfium.PdfDocument(str(pdf_path))[G304["page_index"]].render(scale=RENDER).to_pil().convert("RGB"))
    mask = (np.linalg.norm(img.astype(np.float32) - TAN, axis=2) < 22).astype(np.uint8)
    mask[:, int(MAP_RIGHT * RENDER):] = 0
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.medianBlur(mask * 255, 5) // 255  # smooth the JPEG-noisy edges
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # outer only: fills label holes
    labels = [("O4" if w["text"] == "TS3" else w["text"], Point((w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2))
              for w in _words(page) if LABEL.fullmatch(w["text"]) and w["x1"] < MAP_RIGHT]
    groups: dict[str, list] = {}
    dropped = []
    for c in contours:
        if cv2.contourArea(c) < 40 * RENDER ** 2:  # under ~7 m2: speckle
            continue
        poly = trace.largest_polygon(Polygon(c.reshape(-1, 2) / RENDER).buffer(0))
        inside = sorted({n for n, pt in labels if poly.contains(pt)})
        if not inside:
            n, gap = min(((n, poly.distance(pt)) for n, pt in labels), key=lambda t: t[1])
            if gap > MAX_LABEL_GAP_PT:
                dropped.append(poly)
                continue
            inside = [n]
        if inside == ["O5", "O6"]:
            (a,), (b,) = ([pt for n, pt in labels if n == k] for k in inside)
            mid = np.array([(a.x + b.x) / 2, (a.y + b.y) / 2])
            v = np.array([b.x - a.x, b.y - a.y]) / a.distance(b)
            far = 1000 * np.array([-v[1], v[0]])
            side_a = Polygon([mid + far, mid - far, mid - far - 1000 * v, mid + far - 1000 * v])
            groups.setdefault("O5", []).append(poly.intersection(side_a))
            groups.setdefault("O6", []).append(poly.difference(side_a))
            continue
        if len(inside) > 1:
            raise SystemExit(f"one G3.04 fill holds labels {inside}")
        groups.setdefault(inside[0], []).append(poly)
    out = {n: shapely.union_all(g) for n, g in groups.items()}

    # SP2: the wing on the North Garage's west wall.
    ng = trace.largest_polygon(out["NG"])
    k = 45 * RENDER
    reg = np.zeros(mask.shape, np.uint8)
    cv2.fillPoly(reg, [(np.asarray(ng.exterior.coords) * RENDER).round().astype(np.int32)], 1)
    body = cv2.morphologyEx(reg, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
    cs, _ = cv2.findContours(((reg > 0) & (body == 0)).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sp2_pt = next(pt for n, pt in labels if n == "SP2")
    wings = [trace.largest_polygon(Polygon(c.reshape(-1, 2) / RENDER).buffer(0)) for c in cs if cv2.contourArea(c) > 50 * RENDER ** 2]
    wing = min(wings, key=lambda g: g.distance(sp2_pt))
    if not 300 < wing.area < 3000 or wing.distance(sp2_pt) > 40:
        raise SystemExit(f"SP2 wing not found as expected (area {wing.area:.0f}, {wing.distance(sp2_pt):.0f} pt from its label)")
    out["SP2"] = wing
    out["NG"] = ng.difference(wing.buffer(0.3))
    return out, dropped


def overture_buildings() -> gpd.GeoSeries:
    """Overture building footprints (OpenStreetMap) around the site, cached, in UTM."""
    cache = config.RAW / "wv-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "names", "height", "num_floors", "sources"], filter=f)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    return gpd.GeoSeries(shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)), crs=4326).to_crs(UTM)


def georeference(page, site_utm, buildings) -> tuple[trace.Similarity, dict]:
    fig = site_boundary_points(page)
    target = site_utm.exterior
    init = trace.Similarity(NOMINAL_M_PER_PT, 0.0, 0.0, 0.0)
    c = init.apply([fig.mean(0)])[0]
    ring = np.asarray(target.coords)
    init.tx, init.ty = ring[:-1].mean(0) - c
    keep = 0.8
    sim, d = tb.icp(fig, [target], np.zeros(len(fig), int), init, keep, iterations=200)
    rep = tb.icp_report(sim, d, keep, "G3.04 site boundary vs the legal-description site boundary")
    rep["nominal_scale_m_per_unit"] = round(NOMINAL_M_PER_PT, 5)
    if abs(sim.scale / NOMINAL_M_PER_PT - 1) > 0.02 or sim.rms_m > 2:
        raise SystemExit(f"G3.04 fit off: scale {sim.scale:.5f} m/pt, RMS {sim.rms_m:.2f} m")
    corners = shapely.MultiPoint(np.vstack([np.asarray(g.exterior.coords) for g in buildings
                                            if g.geom_type == "Polygon"]))
    checks = []
    for label, xy in CHECK.items():
        got = Point(sim.apply([xy])[0])
        near = shapely.ops.nearest_points(got, corners)[1]
        checks.append({"label": label, "residual_m": round(got.distance(near), 2)})
    r = np.array([c["residual_m"] for c in checks])
    rep["check_rms_m"] = round(float(np.sqrt((r ** 2).mean())), 2)
    rep["check_note"] = ("Roof corners in the sheet's aerial base against OpenStreetMap footprints; roofs, eaves and "
                         "the aerial's own placement add a few metres, so this checks the fit only coarsely.")
    rep["check_points"] = checks
    return sim, rep


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> None:
    plan = trace.fetch_document(PLAN_SET["url"], DOCS / PLAN_SET["file"], PLAN_SET["sha256"])
    cdp = trace.fetch_document(CDP["url"], DOCS / CDP["file"], CDP["sha256"])
    check_cdp(cdp)
    heights, zone_of = height_table(plan)
    if "--check-acps" in argv:
        check_acps(heights)
    acp_max = {b: float(v) for _, items in ACP_CHECK.values() for b, (_, v) in items.items()}

    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM).geometry.iloc[0]
    with pdfplumber.open(plan) as pdf:
        page = pdf.pages[G304["page_index"]]
        sim, report = georeference(page, site, overture_buildings())
        shapes, dropped = building_shapes(plan, page)
    print(f"[willow-village] G3.04 georeference: trimmed RMS {report['rms_m']} m over {report['points']} boundary points, "
          f"scale {report['scale_m_per_unit']} m/pt (nominal {report['nominal_scale_m_per_unit']}), rotation "
          f"{report['rotation_deg']} deg; roof-corner check RMS {report['check_rms_m']} m {[c['residual_m'] for c in report['check_points']]}")
    missing = sorted(set(NAMES) - set(shapes))
    if missing or set(shapes) - set(NAMES) - {"TS3"}:
        raise SystemExit(f"G3.04 buildings not matched: missing {missing}, found {sorted(shapes)}")
    if "TS3" in shapes:  # drawn as the west end of O4
        shapes["O4"] = shapely.union_all([shapes["O4"], shapes.pop("TS3")])

    doc = f"{PLAN_SET['title']}, {G304['figure']} (PDF p. {G304['page_index'] + 1})"
    features, raw_area, trimmed = [], 0.0, 0.0
    order = ["TS1", "TS2", "O1", "O2", "O3", "O4", "O5", "O6", "O7", "NG", "SG", "SP1", "SP2",
             "RS2", "RS3", "RS4", "RS5", "RS6", "RS7", "RA1"]
    for b in order:
        g = shapely.make_valid(sim.geometry(shapes[b]))
        g = g.buffer(1.5, join_style="mitre").buffer(-1.5, join_style="mitre")  # close gaps left by labels and lines
        raw_area += g.area
        inside = g.intersection(site)
        trimmed += g.area - inside.area
        geom = trace.as_multipolygon(shapely.make_valid(inside.simplify(0.6)))
        geom = trace.as_multipolygon(shapely.MultiPolygon([p for p in geom.geoms if p.area >= 4]))
        label, use = NAMES[b]
        zone = zone_of[b]
        cap = 85 if zone == "R-MU" else 120
        props = {
            "kind": "building",
            "block": b,
            "label": label,
            "stage": "entitled",
            "height_ft": heights[b],
            "podium_ft": None,
            "base_ft": 0,
            "use": use,
            "phase": None,
            "illustrative": True,
            "source": (f"illustrative: footprint and maximum height ({heights[b]} ft) traced from {doc}; "
                       f"CDP Section 2.3.5 caps heights at G3.04's maxima ({zone} zone: {cap} ft)"),
        }
        notes = []
        if b == "O7":
            notes.append("118 ft is the top of the atrium roof; the architectural control plans give a weighted "
                         "average of about 60 ft. The elevated park runs over this building and is not drawn.")
        if b == "O4":
            notes.append(f"Includes Town Square retail building TS3 (maximum {heights['TS3']} ft), which G3.04 draws "
                         "as the west end of O4 without a dividing line.")
        if b in acp_max:
            notes.append(f"The approved architectural control plans (2023) give {acp_max[b]} ft.")
        if notes:
            props["note"] = " ".join(notes)
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(geom))})

    check = {"buildings_m2": round(raw_area), "outside_site_m2": round(trimmed),
             "outside_site_share": round(trimmed / raw_area, 4),
             "unlabelled_shapes_left_out_m2": [round(sim.scale ** 2 * p.area) for p in dropped]}
    print(f"[willow-village] {len(features)} buildings; {check['outside_site_m2']} m2 ({check['outside_site_share']:.1%}) "
          f"outside the site boundary trimmed; left out unlabelled shapes {check['unlabelled_shapes_left_out_m2']} m2")
    if check["outside_site_share"] > 0.02:
        raise SystemExit("too much of the traced massing falls outside the site; check the georeference")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each building in the approved 2022 Willow Village master plan (Sheet G3.04) is "
                "drawn on its plan footprint, which the permit calls illustrative, and extruded to its maximum "
                "height, from 15 ft to 118 ft for the meeting and collaboration space. Real buildings step down "
                "from their maximum. Parks, the town square and the elevated park aren't massed. Nothing has been "
                "built; Meta paused the project in May 2026."
            ),
            "note": "Buildings are drawn to their maximum heights in the approved 2022 master plan; real buildings step down from them.",
            "sourceUrl": PLAN_SET["url"],
            "sourceLabel": "Master plan, 2022 (PDF)",
            "georeference": {"sheet_g3_04": report, "check_against_site": check},
            "documents": {
                "master_plan": {"title": PLAN_SET["title"], "url": PLAN_SET["url"], "sha256": PLAN_SET["sha256"],
                                "pages": "Sheet G3.04 (PDF p. 20): footprints, building maximum heights, CDP standards"},
                "cdp": {"title": CDP["title"], "url": CDP["url"], "sha256": CDP["sha256"],
                        "pages": "Section 2.3.5 (p. 5): heights may not exceed G3.04's maxima; 2.2.3: illustrative plans"},
                "architectural_control_plans": {
                    "url": "https://www.menlopark.gov/Government/Departments/Community-Development/Projects/Approved-projects/Willow-Village",
                    "finding": "Approved June-Sept 2023 for the Phase 1 buildings; their maximum heights match G3.04 "
                               "(RS7 75.98 ft against 76.06 ft). No ACP for RS4 and RS5.",
                    "checked": {b: {"acp": ACP_URL + f, "page": p, "max_ft": float(v)}
                                for f, items in ACP_CHECK.values() for b, (p, v) in items.items()},
                },
            },
            "license": "Building shapes and heights from public City of Menlo Park documents; placed on the site boundary "
                       "traced from the development agreement (City of Menlo Park parcels, CC0); checked against "
                       "OpenStreetMap (ODbL 1.0) via Overture Maps.",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[willow-village] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1:])
