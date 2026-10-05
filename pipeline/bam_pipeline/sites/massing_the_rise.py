"""The Rise (former Vallco mall, Cupertino): building massing from the approved 2024 SB 35 plan set.

Source:
- "Attachment A - Approved Plans", the plan set approved with the City of Cupertino's second
  modification of the SB 35 project (approval letter Feb 16, 2024; cases M-2023-002, ASA-2023-010,
  TR-2023-055, TM-2023-002; every sheet carries the Planning Division's "APPROVED 02/16/24" stamp).
  Published by the city at apps.cupertino.org (190 PDF pages, 275 MB).
  Footprints: P-0800.01 "Building plan - street level" (PDF p. 78), P-0800.05 "Typical above podium"
  (p. 82) and P-0800.06 "Typical tower" (p. 83). The three sheets share one frame.
  Heights: P-0831 "Building sections - west side" (p. 89) and P-0832 "east side" (p. 90). Each
  section labels floor elevations (TOFF, NAVD 88 feet) and most blocks carry a "TOTAL HEIGHT FROM
  AVG. GRADE" dimension. Where a block has that dimension it is used as printed; otherwise the
  height is the printed roof elevation minus the printed average grade (HEIGHTS says which).
  Uses: P-0101 "Building block allocation" table (p. 2).
- The approval letter (Feb 16, 2024, p. 13): "there are no height limits applicable to the original
  or modified project", so the plan set's own heights are the only official heights.
- The third modification (Feb 27, 2026; M-2025-001, TM-2026-006) is the newest approval, but its
  plans are not published. The city's own summary of it (Phase 1 final map, July 2026, draft
  resolution recital 4) caps office at 1,474,946 sq ft: exactly the 2024 total (1,954,613) minus
  Block 13's 479,667 sq ft of office. Block 13 is therefore drawn as an outline only.

What this is and isn't:
- Each block is drawn in up to three pieces, each extruded from the ground to one height: the
  street-level footprint (the podium of parking, shops and lobbies) to the top of the podium; the
  buildings above the podium to the block's height; and the tower floors (P-0800.06) to the tower
  height. Real buildings step and vary within each piece (Block 4 steps from 3 to 12 storeys; Block
  11's wings are 74 and 84.5 ft), so every piece is drawn to its tallest point and labelled
  illustrative. Block 15's three office towers above one garage are told apart west to east.
- Block 14's street-level plan includes a lower service wing whose height the sections don't give;
  only the office tower is drawn. Parks, plazas, the town squares and streets aren't massed.
- Nothing has been built: the mall's above-ground structures were demolished and the city will issue
  no vertical building permits on the west side until the Phase 1 final map records (staff report,
  July 21, 2026), so every piece is "entitled".

Georeferencing: the plan sheets draw the existing property line as a red dash-dot raster line. It is
fitted by trimmed ICP (free similarity) to the Santa Clara County parcels that form the site boundary
(data/boundaries/the-rise.geojson, APNs 316-20-121 and 316-20-122), and the fitted scale is checked
against the sheets' nominal 1/64" = 1'-0".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_the_rise
"""

from __future__ import annotations

import json
import math
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
from shapely.geometry import Point, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "the-rise"
UTM = tb.UTM
DOCS = config.ROOT / "data" / "raw" / "docs"

PLAN_SET = {
    "title": "The Rise SB 35 modification, Attachment A - Approved Plans (approved Feb 16, 2024)",
    "url": "https://apps.cupertino.org/pdf/Attachment%20A%20-%20Approved%20Plans.pdf",
    "sha256": "a062268d82d44200142ec5e838799bab93b994fd4366a686a096eb67cb7885a7",
    "file": "rise-attachment-a-approved-plans-2024.pdf",
}
APPROVAL_URL = "https://legistar.granicus.com/cupertino/attachments/61c2b68e-c1ce-44ee-9a66-55f5ebbc08e0.pdf"
FINAL_MAP_RES_URL = "https://legistar.granicus.com/cupertino/attachments/4e3bbad6-3215-4bd4-a4ea-ca168b6a8332.pdf"
TEFRA_URL = "https://legistar.granicus.com/cupertino/attachments/a48ffc4f-a6db-4f2c-a12c-c966dfb6dfbf.pdf"

# PDF page indexes (0-based) and the sheet number each must carry.
SHEETS = {"street": (77, "P-0800.01"), "podium_up": (81, "P-0800.05"), "tower": (82, "P-0800.06"),
          "roof": (83, "P-0800.24"), "west": (88, "P-0831"), "east": (89, "P-0832"), "info": (1, "P-0101")}
RENDER = 1.5  # pixels per PDF point (about 0.18 m per pixel)
NOMINAL_M_PER_PT = 0.3048 * 64 / 72  # 1/64" = 1'-0"
MAP_X_MAX = 3100  # the title block starts here (PDF points)
LEGEND = (2780, 0, 3100, 330)  # legend swatches on the plan sheets
ROOF_SHIFT = (3.5, -1.3)  # P-0800.24's frame is offset from P-0800.01/.05/.06 by this much (points)
BBOX = (-122.0135, 37.3205, -122.0035, 37.3285)
YELLOW = (252, 212, 4)
BLUE = (128, 196, 228)

USES = {  # P-0101 building block allocation
    1: "residential, retail, parking", 2: "residential, retail, parking", 3: "residential, retail, parking",
    4: "residential, retail, parking", 5: "residential, retail, parking", 6: "residential, parking",
    7: "residential, retail, parking", 8: "residential, retail, parking", 9: "residential, parking",
    10: "residential, parking", 11: "residential, retail, parking", 12: "residential, retail, parking",
    13: "office, parking", 14: "office, parking", 15: "office, parking",
}


def ft(s: str) -> float:
    m = re.fullmatch(r"(\d+)'-(\d+)\"", s)
    return int(m.group(1)) + int(m.group(2)) / 12


# Heights in feet above average grade. Each entry: (value, sheet key, how, printed strings that must
# appear on that sheet). "dim" = the sheet's TOTAL HEIGHT FROM AVG. GRADE dimension; "elev" = roof
# (or deck) elevation minus average grade, both printed on the section.
def _elev(top: str, grade: str) -> float:
    return round(ft(top) - ft(grade), 2)


HEIGHTS = {
    # podium = top of the parking/retail podium (the courtyard deck): first residential level's TOFF
    # above average grade, from the section through the block.
    (1, "podium"): (_elev("232'-2\"", "195'-6\""), "west", "elev", ["LEVEL 3 TOFF 232'-2\"", "EL. AVG GRADE 195'-6\""],
                    "section 2 (Perimeter Way): level 3 deck 232'-2\" over average grade 195'-6\""),
    (1, "upper"): (ft("80'-6\""), "west", "dim", ["ROOF TOS 276'-0\""], "section 2: total height 80'-6\""),
    (2, "podium"): (_elev("223'-7\"", "193'-6\""), "west", "elev", ["LEVEL 4 TOFF 223'-7\"", "EL. AVG GRADE 193'-6\""],
                    "section 1 (Wolfe Road): level 4 deck 223'-7\" over average grade 193'-6\""),
    (2, "upper"): (ft("84'-6\""), "west", "dim", ["ROOF TOFF 278'-0\""], "sections 1 and 5: total height 84'-6\""),
    (3, "podium"): (_elev("221'-5\"", "194'-6\""), "west", "elev", ["LEVEL 3 TOFF 221'-5\"", "EL. AVG GRADE 194'-6\""],
                    "section 6: level 3 deck 221'-5\" over average grade 194'-6\""),
    (3, "upper"): (ft("84'-6\""), "west", "dim", ["ROOF TOFF 279'-0\""], "sections 2 and 6: total height 84'-6\""),
    (4, "podium"): (_elev("235'-11\"", "192'-6\""), "west", "elev", ["LEVEL 5 TOFF 235'-11\"", "EL. AVG GRADE 192'-6\""],
                    "section 3 (Street B): level 5 deck 235'-11\" over average grade 192'-6\""),
    (4, "upper"): (_elev("325'-11\"", "192'-6\""), "west", "elev", ["ROOF TOFF 325'-11\"", "EL. AVG GRADE 192'-6\""],
                   "section 6: roof 325'-11\" over average grade 192'-6\" (no total-height dimension); the building steps from 3 to 12 storeys"),
    (5, "podium"): (_elev("219'-6\"", "188'-6\""), "west", "elev", ["LEVEL 4 TOFF 219'-6\"", "EL. AVG GRADE 188'-6\""],
                    "section 1: level 4 amenity deck 219'-6\" over average grade 188'-6\""),
    (5, "upper"): (ft("85'-0\""), "west", "dim", ["ROOF TOFF 273'-6\""], "sections 1 and 6: total height 85'-0\""),
    (6, "podium"): (_elev("216'-11\"", "187'-0\""), "west", "elev", ["TOFF 216'-11\"", "TOFF 187'-0\""],
                    "section 7: townhouse roof 216'-11\" over their ground floor 187'-0\" (no average grade is printed)"),
    (7, "podium"): (_elev("225'-9\"", "189'-6\""), "west", "elev", ["LEVEL 4 TOFF 225'-9\"", "EL. AVG GRADE 189'-6\""],
                    "sections 3 and 7: level 4 deck 225'-9\" over average grade 189'-6\""),
    (7, "upper"): (ft("85'-0\""), "west", "dim", ["ROOF TOFF 274'-6\""], "section 3: total height 85'-0\""),
    (8, "podium"): (_elev("228'-8\"", "187'-6\""), "west", "elev", ["LEVEL 5 TOFF 228'-8\"", "EL. AVG GRADE 187'-6\""],
                    "sections 1 and 7: level 5 deck 228'-8\" over average grade 187'-6\""),
    (8, "upper"): (ft("85'-0\""), "west", "dim", ["ROOF TOFF 272'-6\""], "section 1: total height 85'-0\""),
    (8, "tower"): (ft("200'-1\""), "west", "dim", ["ROOF TOFF 387'-7\"", "EL. AVG GRADE 187'-6\""],
                   "section 7: total height 200'-1\" (roof 387'-7\", 18 storeys)"),
    (9, "podium"): (_elev("215'-7\"", "184'-6\""), "west", "elev", ["LEVEL 4 TOFF 215'-7\"", "EL. AVG GRADE 184'-6\""],
                    "section 4 (Street C): level 4 deck 215'-7\" over average grade 184'-6\""),
    (9, "upper"): (ft("85'-0\""), "west", "dim", ["ROOF TOFF 269'-6\""], "sections 4 and 8: total height 85'-0\""),
    (10, "podium"): (_elev("213'-0\"", "182'-0\""), "west", "elev", ["LEVEL 4 TOFF 213'-0\"", "EL. AVG GRADE 182'-0\""],
                     "section 1: level 4 deck 213'-0\" over average grade 182'-0\""),
    (10, "upper"): (ft("85'-0\""), "west", "dim", ["ROOF TOFF 267'-0\""], "sections 1 and 8: total height 85'-0\""),
    (11, "podium"): (_elev("214'-6\"", "184'-0\""), "east", "elev", ["LEVEL 4 TOFF 214'-6\"", "EL. AVG GRADE 184'-0\""],
                     "section 3: level 4 deck 214'-6\" over average grade 184'-0\""),
    (11, "upper"): (ft("84'-6\""), "east", "dim", ["ROOF TOFF 268'-6\"", "ROOF TOFF 258'-3\""],
                    "sections 1 and 3: total height 84'-6\" (the other wing's roof, 258'-3\", is about 74 ft)"),
    (12, "podium"): (_elev("213'-10\"", "182'-6\""), "east", "elev", ["LEVEL 4 TOFF 213'-10\"", "EL. AVG GRADE 182'-6\""],
                     "section 3: level 4 deck 213'-10\" over average grade 182'-6\""),
    (12, "upper"): (_elev("268'-0\"", "182'-6\""), "east", "elev", ["ROOF TOFF 268'-0\"", "EL. AVG GRADE 182'-6\""],
                    "section 2: roof 268'-0\" over average grade 182'-6\" (no total-height dimension)"),
    (12, "tower"): (ft("166'-1\""), "east", "dim", ["ROOF TOFF 349'-1\""],
                    "section 3: total height 166'-1\" (roof 349'-1\", 15 storeys)"),
    (14, "tower"): (ft("185'-6\""), "east", "dim", ["ROOF TOFF 367'-6\"", "EL. AVG GRADE 182'-0\""],
                    "section 1 (east Wolfe Road): total height 185'-6\" (roof 367'-6\")"),
    (15, "podium"): (_elev("242'-9\"", "181'-0\""), "east", "elev", ["LEVEL 7 TOFF 242'-9\"", "EL. AVG GRADE 181'-0\""],
                     "section 4: the garage's top deck (level 7) 242'-9\" over average grade 181'-0\""),
    (15, "tower-w"): (ft("198'-3\""), "east", "dim", ["ROOF TOFF 379'-3\""],
                      "section 1 (east Wolfe Road): total height 198'-3\" (roof 379'-3\", 9 office floors over the garage)"),
    (15, "tower-m"): (_elev("394'-3\"", "181'-0\""), "east", "elev", ["LEVEL 16 TOFF 377'-9\"", "EL. AVG GRADE 181'-0\""],
                      "section 4: 10 office floors; its roof is not labelled, so 394'-3\" is level 16 (377'-9\") plus the 16'-6\" top floor the sheet gives the other two towers, over average grade 181'-0\""),
    (15, "tower-e"): (ft("228'-3\""), "east", "dim", ["ROOF TOFF 409'-3\""],
                      "sections 2 and 4: total height 228'-3\" (roof 409'-3\", 11 office floors over the garage)"),
}
DIMS = {"west": ["80'-6\"", "84'-6\"", "85'-0\"", "200'-1\""], "east": ["84'-6\"", "166'-1\"", "185'-6\"", "198'-3\"", "228'-3\""]}


# ---------------------------------------------------------------- documents

def check_sheets(pdf_path) -> None:
    doc = pdfium.PdfDocument(str(pdf_path))
    for key, (i, sheet) in SHEETS.items():
        text = doc[i].get_textpage().get_text_range()
        if sheet not in text:
            raise SystemExit(f"PDF page {i + 1} is not sheet {sheet}")
        if key != "info" and "02/16/24" not in text:
            raise SystemExit(f"sheet {sheet} lacks the 02/16/24 approval stamp")
    info = doc[SHEETS["info"][0]].get_textpage().get_text_range()
    for b, use in USES.items():
        if not re.search(rf"BLOCK {b} [\d,]+ {use.upper()}", info):
            raise SystemExit(f"P-0101 block allocation: block {b} is not '{use}'")
    if not re.search(r"BLOCK 13 479,667 OFFICE", info):
        raise SystemExit("P-0101: Block 13 office area is not 479,667 sq ft")


def _rotated_strings(page) -> list[str]:
    """Vertical text (the dimension strings) read bottom to top."""
    ch = sorted((c for c in page.chars if not c["upright"]), key=lambda c: (round(c["x0"]), -c["top"]))
    out: list[dict] = []
    for c in ch:
        if out and abs(out[-1]["x"] - c["x0"]) < 0.8 and out[-1]["top"] - c["bottom"] < 3:
            out[-1]["t"] += c["text"]
            out[-1]["top"] = c["top"]
        else:
            out.append({"x": c["x0"], "top": c["top"], "t": c["text"]})
    return [s["t"] for s in out]


def check_heights(pdf) -> None:
    """Every printed figure HEIGHTS relies on must be on its sheet."""
    texts = {k: " ".join(pdf.pages[SHEETS[k][0]].extract_text().split()) for k in ("west", "east")}
    rotated = {k: set(_rotated_strings(pdf.pages[SHEETS[k][0]])) for k in ("west", "east")}
    for k, dims in DIMS.items():
        missing = [d for d in dims if d not in rotated[k]]
        if missing:
            raise SystemExit(f"{SHEETS[k][1]}: height dimensions {missing} not found")
    for key, (_, sheet, _, strings, _) in HEIGHTS.items():
        for s in strings:
            if s not in texts[sheet]:
                raise SystemExit(f"{SHEETS[sheet][1]}: '{s}' (for {key}) not found")


# ---------------------------------------------------------------- figure

def render(pdf_path, key) -> np.ndarray:
    return np.asarray(pdfium.PdfDocument(str(pdf_path))[SHEETS[key][0]].render(scale=RENDER).to_pil().convert("RGB"))


def _blank_margins(m: np.ndarray) -> np.ndarray:
    m[:, int(MAP_X_MAX * RENDER):] = 0
    m[:, : int(140 * RENDER)] = 0
    x0, y0, x1, y1 = (int(v * RENDER) for v in LEGEND)
    m[y0:y1, x0:x1] = 0
    return m


def _polygons(mask: np.ndarray, min_pt2: float) -> list[Polygon]:
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # outer only: fills holes
    out = []
    for c in cs:
        if cv2.contourArea(c) >= min_pt2 * RENDER ** 2:
            out.append(trace.largest_polygon(Polygon(c.reshape(-1, 2) / RENDER).buffer(0)))
    return out


def property_line_points(img: np.ndarray) -> np.ndarray:
    """Pixels of the red dash-dot existing property line (figure points)."""
    a = img.astype(int)
    red = ((a[..., 0] > 200) & (a[..., 1] < 110) & (a[..., 2] < 110)).astype(np.uint8)
    fills = cv2.dilate(cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)), np.ones((15, 15), np.uint8))
    line = _blank_margins(red & (1 - fills))
    ys, xs = np.nonzero(line)
    pts = (np.c_[xs, ys] / RENDER)[::3]
    if len(pts) < 3000:
        raise SystemExit(f"only {len(pts)} property-line points found on P-0800.01")
    return pts


def street_footprints(img: np.ndarray) -> list[Polygon]:
    """Building footprints on the street-level plan: every coloured or grey program fill and the bold
    outlines, closed and filled, without trees (green) or the light-grey base map."""
    a = img.astype(int)
    mx, mn = a.max(2), a.min(2)
    green = (a[..., 1] > a[..., 0] + 12) & (a[..., 1] > a[..., 2] + 12)
    coloured = ((mx - mn) > 14) & ~green
    grey = ((mx - mn) <= 20) & (mx < 200) & (mx >= 70)
    ink = mx < 70
    m = _blank_margins((coloured | grey | ink).astype(np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((19, 19), np.uint8))
    return _polygons(m, 3000)


def program_fills(img: np.ndarray) -> list[Polygon]:
    """Residential (yellow) and office (blue) floor plates on the above-podium and tower plans."""
    a = img.astype(np.float32)
    m = ((np.linalg.norm(a - YELLOW, axis=2) < 45) | (np.linalg.norm(a - BLUE, axis=2) < 40)).astype(np.uint8)
    m = _blank_margins(m)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))  # unit lines, cores, labels
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    return _polygons(m, 1500)


def block_labels(page) -> dict[int, Point]:
    """Block numbers on the roof plan (P-0800.24), moved into the other sheets' frame."""
    out = {}
    for w in page.extract_words():
        t = w["text"].strip()
        # the plan's block numbers are about 25 pt tall; section-marker numbers are 6-10 pt
        if t.isdigit() and 1 <= int(t) <= 15 and w["bottom"] - w["top"] > 20 and w["x1"] < 2900 and w["x0"] > 300:
            b = int(t)
            if b in out:
                raise SystemExit(f"block {b} labelled twice on the roof plan")
            out[b] = Point((w["x0"] + w["x1"]) / 2 + ROOF_SHIFT[0], (w["top"] + w["bottom"]) / 2 + ROOF_SHIFT[1])
    if sorted(out) != list(range(1, 16)):
        raise SystemExit(f"roof plan block labels not all found: {sorted(out)}")
    return out


def georeference(points: np.ndarray, site) -> tuple[trace.Similarity, dict]:
    rings = [p.exterior for p in getattr(site, "geoms", [site])]
    target = shapely.MultiLineString(rings)
    init = trace.Similarity(NOMINAL_M_PER_PT, -math.pi / 2, 0.0, 0.0)  # sheets are drawn with north to the left
    c = init.apply([points.mean(0)])[0]
    init.tx, init.ty = np.asarray(site.centroid.coords[0]) - c
    keep = 0.8
    sim, d = tb.icp(points, [target], np.zeros(len(points), int), init, keep, iterations=200)
    rep = tb.icp_report(sim, d, keep, "P-0800.01 existing property line vs Santa Clara County parcels 316-20-121/122")
    rep["nominal_scale_m_per_unit"] = round(NOMINAL_M_PER_PT, 5)
    if abs(sim.scale / NOMINAL_M_PER_PT - 1) > 0.01 or sim.rms_m > 1:
        raise SystemExit(f"P-0800.01 fit off: scale {sim.scale:.5f} m/pt, RMS {sim.rms_m:.2f} m")
    return sim, rep


def overture_buildings() -> gpd.GeoDataFrame:
    """Overture building footprints (OpenStreetMap and others) around the site, cached, in UTM."""
    cache = config.RAW / "rise-buildings.parquet"
    if not cache.exists():
        for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
            os.environ.pop(k, None)
        fs = pafs.S3FileSystem(anonymous=True, region=config.OVERTURE_REGION)
        path = f"{config.OVERTURE_BUCKET}/release/{config.OVERTURE_RELEASE}/theme=buildings/type=building/"
        d = ds.dataset(path, filesystem=fs, format="parquet")
        xmin, ymin, xmax, ymax = BBOX
        f = ((pc.field("bbox", "xmin") < xmax) & (pc.field("bbox", "xmax") > xmin)
             & (pc.field("bbox", "ymin") < ymax) & (pc.field("bbox", "ymax") > ymin))
        t = d.to_table(columns=["id", "geometry", "height", "num_floors"], filter=f)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(t, cache)
    t = pq.read_table(cache)
    return gpd.GeoDataFrame({"id": t.column("id").to_pylist()},
                            geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)),
                            crs=4326).to_crs(UTM)


# ---------------------------------------------------------------- main

def _short_side(p: Polygon) -> float:
    xy = np.asarray(p.minimum_rotated_rectangle.exterior.coords)
    return float(min(np.linalg.norm(xy[1] - xy[0]), np.linalg.norm(xy[2] - xy[1])))


TOWNHOUSE_MAX_PT2 = 15000  # a townhouse row is 6,700-9,000 pt2 on the sheet; every podium is far larger


def _assign(polys: list[Polygon], labels: dict[int, Point]) -> tuple[dict[int, list], list]:
    """Group street-level footprints by the block label inside them. Block 6's label sits between its
    townhouse rows, so unlabelled small footprints within 450 pt of it are its rows."""
    groups: dict[int, list] = {}
    dropped = []
    for p in polys:
        inside = [b for b, pt in labels.items() if p.contains(pt)]
        if len(inside) > 1:
            raise SystemExit(f"one footprint holds blocks {inside}")
        if not inside:
            if p.area < TOWNHOUSE_MAX_PT2 and p.distance(labels[6]) < 450:
                inside = [6]
            else:
                dropped.append(p)
                continue
        groups.setdefault(inside[0], []).append(p)
    return groups, dropped


def main(argv: list[str]) -> None:
    plan = trace.fetch_document(PLAN_SET["url"], DOCS / PLAN_SET["file"], PLAN_SET["sha256"])
    check_sheets(plan)
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM).geometry.iloc[0]
    with pdfplumber.open(plan) as pdf:
        check_heights(pdf)
        labels = block_labels(pdf.pages[SHEETS["roof"][0]])
    street_img = render(plan, "street")
    sim, report = georeference(property_line_points(street_img), site)
    print(f"[the-rise] P-0800.01 georeference: trimmed RMS {report['rms_m']} m over {report['points']} property-line "
          f"points (median {report['median_m']} m), scale {report['scale_m_per_unit']} m/pt (nominal "
          f"{report['nominal_scale_m_per_unit']}), rotation {report['rotation_deg']} deg")

    def to_utm(g):
        return shapely.make_valid(sim.geometry(g))

    # Street-level footprints on the site, grouped by block.
    streets_all = [p for p in street_footprints(street_img) if to_utm(p).intersection(site).area > 0.5 * to_utm(p).area]
    street, dropped = _assign(streets_all, labels)
    # A long thin strip along Perimeter Road by the hotel (a planting strip, under 8 m wide) is not a building.
    strips = [p for p in dropped if _short_side(p) < 30]
    dropped = [p for p in dropped if _short_side(p) >= 30]
    if dropped:
        raise SystemExit("street-level footprints in no block: "
                         + str([(round(p.centroid.x), round(p.centroid.y), round(p.area)) for p in dropped]))
    if len(street[6]) != 8 or set(street) != set(range(1, 16)):
        raise SystemExit(f"street-level footprints by block not as expected: { {b: len(g) for b, g in street.items()} }")
    up_polys = program_fills(render(plan, "podium_up"))
    tw_polys = program_fills(render(plan, "tower"))
    street_union = {b: shapely.union_all(g) for b, g in street.items()}

    def by_block(polys):
        out: dict[int, list] = {}
        for p in polys:
            hits = [(b, p.intersection(u).area) for b, u in street_union.items()]
            b, area = max(hits, key=lambda t: t[1])
            if area < 0.5 * p.area:
                continue  # not over a building (stray swatch)
            out.setdefault(b, []).append(p)
        return out

    upper, tower = by_block(up_polys), by_block(tw_polys)
    expect_tower = {4, 8, 12, 13, 15}
    if set(tower) != expect_tower:
        raise SystemExit(f"tower plates found in blocks {sorted(tower)}, expected {sorted(expect_tower)}")

    doc = PLAN_SET["title"]
    features = []
    trimmed = total = 0.0

    def emit(block: int, piece: str, geom_fig, label: str, use: str, note: str | None = None):
        nonlocal trimmed, total
        g = to_utm(geom_fig)
        g = g.buffer(0.8, join_style="mitre").buffer(-0.8, join_style="mitre")
        total += g.area
        inside = g.intersection(site)
        trimmed += g.area - inside.area
        geom = trace.as_multipolygon(shapely.make_valid(inside.simplify(0.5)))
        geom = trace.as_multipolygon(shapely.MultiPolygon([p for p in geom.geoms if p.area >= 15]))
        if geom.is_empty:
            return
        if block == 13:
            h, src = None, None
        else:
            h, sheet, how, _, why = HEIGHTS[(block, piece)]
            src = f"{SHEETS[sheet][1]} (PDF p. {SHEETS[sheet][0] + 1}), {why}"
        footprint_sheet = {"podium": "street", "upper": "podium_up"}.get(piece, "tower")
        if block in (14, 15) and piece != "podium":
            footprint_sheet = "podium_up"
        fs = f"{SHEETS[footprint_sheet][1]} (PDF p. {SHEETS[footprint_sheet][0] + 1})"
        props = {
            "kind": "building",
            "block": str(block),
            "label": label,
            "stage": "entitled",
            "height_ft": None if h is None else round(h, 2),
            "podium_ft": None,
            "base_ft": 0,
            "use": use,
            "phase": None,
            "illustrative": h is not None,
            "source": (f"illustrative: footprint traced from {doc}, sheet {fs}; height to its tallest point from {src}"
                       if h is not None else f"traced: {doc}, sheet {fs} (outline only)"),
        }
        if note:
            props["note"] = note
        # 6 decimals (about 0.1 m) keep the file small; the trace itself is good to about a metre
        wgs = shapely.set_precision(tb.to_wgs(geom), 1e-6)
        features.append({"type": "Feature", "properties": props, "geometry": mapping(trace.as_multipolygon(wgs))})

    eden = ("Block 5 holds the 234-unit affordable apartments (174 very low-income, 58 low-income, 2 managers) "
            "for which the city held a bond-financing (TEFRA) hearing in 2026.")
    for b in range(1, 16):
        foot = shapely.union_all(street[b])
        up = shapely.union_all(upper.get(b, [])) if b in upper else Polygon()
        tw = shapely.union_all(tower.get(b, [])) if b in tower else Polygon()
        use = USES[b]
        if b == 13:
            emit(13, "podium", foot, "Block 13 (offices, superseded)", "office, parking",
                 "Drawn as an outline only. The 2024 plans put two office buildings here (about 146 and 161 ft) over a "
                 "six-level garage, with 479,667 sq ft of office. The 2026 modification cut the project's office to "
                 "1,474,946 sq ft, exactly the 2024 total less Block 13's office; its new plans are not published.")
            continue
        if b == 14:
            emit(14, "tower", up, "Block 14 office building", "office",
                 "Office floors from the ground up; the street-level plan's lower service wing is not drawn.")
            continue
        if b == 15:
            emit(15, "podium", foot.difference(up.buffer(0.5)), "Block 15 garage", "parking",
                 "Six-level office garage under the three towers (three more levels below ground).")
            towers = sorted(upper[15], key=lambda p: to_utm(p).centroid.x)
            if len(towers) != 3:
                raise SystemExit(f"Block 15: {len(towers)} office towers found, expected 3")
            for p, key, name in zip(towers, ("tower-w", "tower-m", "tower-e"), ("west", "middle", "east")):
                emit(15, key, p, f"Block 15 {name} office tower", "office")
            continue
        podium_note = None
        if b == 6:
            emit(6, "podium", foot, "Block 6 townhouses", "residential")
            continue
        if b in (5,):
            podium_note = eden
        emit(b, "podium", foot.difference(up.buffer(0.5)), f"Block {b} podium", "parking, retail, lobbies", podium_note)
        if b == 4:  # one stepped building: above-podium and tower plates drawn together to the top
            emit(4, "upper", shapely.union_all([up, tw]), "Block 4 residential", "residential",
                 "Steps up from 3 to 12 storeys; drawn to its top.")
            continue
        upper_note = eden if b == 5 else None
        if b == 11:
            upper_note = "The two wings are 84.5 and about 74 ft; drawn to the taller."
        emit(b, "upper", up.difference(tw.buffer(0.5)) if not tw.is_empty else up, f"Block {b} residential",
             "residential", upper_note)
        if not tw.is_empty:
            emit(b, "tower", tw, f"Block {b} tower", "residential")

    # Built buildings: the mall's structures are gone; say so if the base data still has any on the site.
    ob = overture_buildings()
    on_site = ob[ob.intersection(site).area > 0.5 * ob.area]
    print(f"[the-rise] Overture buildings on the site: {len(on_site)}"
          + (f" ({round(on_site.area.sum())} m2: {list(on_site['id'])[:5]})" if len(on_site) else ""))

    share = trimmed / total
    print(f"[the-rise] {len(features)} pieces; {trimmed:.0f} m2 ({share:.1%}) outside the site trimmed; "
          f"left out {len(strips)} thin strip(s) of {[round(sim.scale ** 2 * p.area) for p in strips]} m2")
    if share > 0.02:
        raise SystemExit("too much of the traced massing falls outside the site; check the georeference")
    def rng(word: str, use: str | None = None) -> str:
        hs = sorted(f["properties"]["height_ft"] for f in features if f["properties"]["height_ft"]
                    and word in f["properties"]["label"].lower() and (use is None or f["properties"]["use"] == use)
                    and not (word == "tower" and "office" in f["properties"]["label"].lower()))
        if word == "office":
            hs = sorted(f["properties"]["height_ft"] for f in features
                        if f["properties"]["use"] == "office" and f["properties"]["height_ft"])
        lo, hi = round(hs[0]), round(hs[-1])
        return f"{lo}" if lo == hi else (f"{lo} and {hi}" if len(hs) == 2 else f"{lo} to {hi}")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing from the plan set Cupertino approved in February 2024: each block's podium, the "
                "buildings above it and its towers, traced from the plans and extruded to the heights in the "
                f"approved building sections: podiums of {rng('podium')} ft, townhouses of {rng('townhouses')} ft, "
                f"residential buildings of {rng('residential')} ft, residential towers of {rng('tower', 'residential')} ft "
                f"and office towers of {rng('office')} ft. Each piece is drawn to its tallest point; real buildings step. "
                "Block 13 is an outline only: the 2026 modification cut the project's office space by exactly Block 13's "
                "amount, and its new plans aren't published. Nothing has been built yet."
            ),
            "note": "Drawn from the 2024 approved plans to each piece's tallest point; the 2026 changes aren't published.",
            "sourceUrl": PLAN_SET["url"],
            "sourceLabel": "Approved plans, 2024 (PDF)",
            "georeference": {"street_level_plan": report,
                             "check_against_site": {"massing_m2": round(total), "outside_site_m2": round(trimmed),
                                                    "outside_site_share": round(share, 4)},
                             "overture_buildings_on_site": len(on_site)},
            "documents": {
                "approved_plans": {
                    "title": PLAN_SET["title"], "url": PLAN_SET["url"], "sha256": PLAN_SET["sha256"],
                    "pages": "P-0101 (PDF p. 2): block uses; P-0800.01/.05/.06 (pp. 78, 82, 83): footprints; "
                             "P-0800.24 (p. 84): block numbers; P-0831/P-0832 (pp. 89-90): heights",
                },
                "approval_letter": {"url": APPROVAL_URL,
                                    "pages": "p. 1: approves the plan set in Attachment A; p. 13: no height limits apply"},
                "third_modification": {"url": FINAL_MAP_RES_URL,
                                       "finding": "Recital 4: up to 1,474,946 sq ft of office (2024 plans: 1,954,613, "
                                                  "of which Block 13 479,667). The Feb 27, 2026 plans are not published."},
                "block_5": {"url": TEFRA_URL, "finding": "Block 5 apartments: 234 affordable units with Eden Housing."},
            },
            "license": "Building shapes and heights from public City of Cupertino documents; placed on Santa Clara "
                       "County parcel boundaries (county open data).",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    # Readable properties, one compact line per geometry (keeps the file small).
    fc = tb._round(fc)
    geoms = [f.pop("geometry") for f in fc["features"]]
    for i, f in enumerate(fc["features"]):
        f["geometry"] = f"@@GEOM{i}@@"
    text = json.dumps(fc, indent=1)
    for i, g in enumerate(geoms):
        text = text.replace(f'"@@GEOM{i}@@"', json.dumps(g, separators=(",", ":")))
    path.write_text(text + "\n")
    print(f"[the-rise] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1:])
