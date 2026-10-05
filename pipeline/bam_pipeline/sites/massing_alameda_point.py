"""Alameda Point Site A: block height limits from the 2022 Development Plan, the Radium theater
approved in 2026, and the finished Phase 1 buildings.

Sources (City of Alameda records, Legistar):
- Blocks and height limits: Alameda Point Site A Development Plan, Second Amendment (BAR
  Architects, July 25, 2022; approved by the Planning Board that day and attached again to the
  Mar 9, 2026 annual review), p. 11 "Land Use Diagram". The diagram is a raster image with vector
  text on top: block numbers and heights ("+40'", "+65'**") are read from the text layer, and
  each block's fill is traced from the image (one flat colour per land use). The figure is
  georeferenced on eight street-centreline intersections (centrelines midway between the block
  fills) and the centroids of three existing buildings it draws (Hangars 40 and 41, Building 77),
  all matched to OpenStreetMap via Overture. The heights are the Waterfront Town Center Precise
  Plan limits block by block: the Planning Board staff reports quote the same values (65 ft on
  Blocks 9 and 11, 50 ft on Block 8, 40 ft on Blocks 6 and 7).
- Block 11 (220 homes, design approved in 2016, amended 2019 and 2022, not yet built): drawn at the
  78 ft of its approved design. The diagram gives 65 ft with "Per precise plan, height may exceed
  65' with special consideration"; the Board used that finding (staff report, Mar 14, 2016:
  "Block 11 is 78 feet to the top of the parapet").
- Blocks 12 and 13: the Planning Board approved the Radium Performing Arts Center Development Plan
  Amendment on Mar 23, 2026, superseding the 2022 diagram there (a 35-ft theater on 12b with
  retail beside it). The theater's footprint is the "Performing Arts Center" rectangle of its
  Development Plan (Bora Architecture, Nov 7, 2025), p. 10, a vector site plan placed by its
  Naval Air Museum (Building 77) outline, matched to the museum's OpenStreetMap footprint, at the
  scale of its own 436-ft dimension. Its fly tower is located from the p. 17 roof plan. Heights
  are the conceptual elevations on p. 35 (35, 43 and 72 ft); design review is still to come.
- Finished buildings (Blocks 6, 7, 8 and 9; "APP has completed construction on the vertical
  development for Blocks 6, 7, 8, and 9", 2025 annual report, Jan 23, 2026): footprints from
  OpenStreetMap via Overture; heights from the Planning Board design review records: Block 6
  "+/- 40'-0"" to top of parapet (KTGY elevations, June 15, 2016), Block 7 roof at 31'-6"
  (KwanHenmi elevations, June 15, 2016), Block 8 "50 feet high to the top of the parapet" and
  Block 9 "a maximum height of 59 feet to the top of the parapet" (staff reports).

What this is and isn't:
- Unbuilt blocks are drawn to their height limits over the whole block, not as building designs,
  so they're labelled illustrative. Block outlines are the diagram's, which is "illustrative" in
  places; parcel lines weren't available.
- Parks and plazas (Blocks 2, 18a–c, 19, 5a/5b and the Radium plaza), public parking, streets,
  the existing Cartwright substation and the Navy-era buildings (Hangars 40 and 41, Buildings 77
  and 113) aren't drawn. Neither are the small State Lands retail pavilions (5a, 5b), which have
  no height in the plan.
- The Phase 2 warehouses north of Coronado, still standing until the Phase 2 blocks are built,
  stay in the base map.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_alameda_point
"""

from __future__ import annotations

import json
import os
import re
import urllib.request

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import Polygon, box, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "alameda-point"
UTM = "EPSG:26910"
FT = 0.3048
ACRE_M2 = 4046.8564224
DOCS = tb.DOCS
BBOX = (-122.3080, 37.7720, -122.2850, 37.7860)  # lon/lat window over Site A and the hangars
OSM_LICENSE = tb.OSM_LICENSE

PLAN = tb.ALAMEDA_PLAN  # 2022 Site A Development Plan (same PDF as the boundary trace)
PLAN_TITLE = "Alameda Point Site A Development Plan, Second Amendment (BAR Architects, July 25, 2022)"
LUD = {"page_index": 10, "printed_page": "11", "figure": "Land Use Diagram"}
LUD_RASTER_PX = (4995, 2407)
PLAN_PHASING = "Illustrative Site Plan – Phasing table, p. 9"

RADIUM = {
    "title": "Radium Theatre Revised Development Plan (Bora Architecture & Interiors, Nov 7, 2025)",
    "url": "https://legistar1.granicus.com/alameda/attachments/cc7a429d-3973-4f6f-83a1-6cef51878c67.pdf",
    "file": "ap-radium-development-plan-2026.pdf",
    "sha256": "0aa9aeb316355f38ceaf37a75c129ea09ef8e77db80a5eccfdd0b2919d149376",
}
BLOCK6_PLANS = {
    "title": "Alameda Point Block 6 design review plans (KTGY, June 15, 2016)",
    "url": "https://legistar1.granicus.com/alameda/attachments/dfc15a4c-b254-4699-b53d-2b4f7118c903.pdf",
    "file": "ap-block6-dr-plans.pdf",
    "sha256": "f381b80ecfa32aef2c4c90e0d2bd310edf15ebc11f93a2b2f2a172990993b8ac",
}
BLOCK7_PLANS = {
    "title": "Alameda Point Block 7 design review plans (KwanHenmi, June 15, 2016)",
    "url": "https://legistar1.granicus.com/alameda/attachments/0a9551c2-cd42-4dcf-82bd-4e84b38110c0.pdf",
    "file": "ap-block7-dr-plans.pdf",
    "sha256": "91b51b32a38c971f2766b94499c4b7c918fd55642af3a87dd69d9b9346ca66a5",
}


def _legistar(matter: int, text_id: int, guid: str, title: str) -> dict:
    return {
        "matter": matter, "text_id": text_id, "title": title,
        "api": f"https://webapi.legistar.com/v1/alameda/matters/{matter}/texts/{text_id}",
        "url": f"https://alameda.legistar.com/LegislationDetail.aspx?ID={matter}&GUID={guid}",
    }


# Planning Board staff reports (text read from the Legistar API; each quote is checked).
SR_2016_03 = _legistar(4388, 4658, "86CB9634-CF02-45CE-B727-207C9DAC8CA3",
                       "Planning Board staff report, design review for Blocks 11 and 8 (Mar 14, 2016)")
SR_2016_06 = _legistar(4757, 5051, "CCABEA15-048B-4DCE-AB2C-F9C1B2DE49A7",
                       "Planning Board staff report, design review for Blocks 6, 7 and 10 (June 27, 2016)")
SR_2017_12 = _legistar(6711, 7146, "6634ADEE-5B8D-42B2-A475-3097540463FB",
                       "Planning Board staff report, design review for Block 9 (Dec 11, 2017)")
SR_2022_07 = _legistar(12022, 12769, "20068886-A972-46BC-A300-2C70A91CBB55",
                       "Planning Board staff report, Site A Development Plan amendment (July 25, 2022)")
CC_2026_04 = _legistar(15669, 16870, "3F0A0DF1-528E-4FB6-A635-3D46C9DA144E",
                       "City Council staff report, Radium project agreements (Apr 21, 2026)")
QUOTES = {
    4388: ["The Precise Plan establishes a maximum height of 65 feet for Block 11 and 50 feet for Block 8",
           "The two buildings on Block 8 are 50 feet high to the top of the parapet",
           "Block 11 is 78 feet to the top of the parapet",
           "Both buildings are four stories tall"],
    4757: ["the townhomes are within the 40 foot height limit for Blocks 6 and 7",
           "The commercial buildings on Block 10 are well below the 60 foot height limit",
           "All of the buildings are three stories in height"],
    6711: ["The Precise Plan establishes a maximum height of 65 feet for Block 9",
           "designed with a maximum height of 59 feet to the top of the parapet",
           "a parapet that rises to approximately 50 feet"],
    12022: ["220 units on block 11 (approved in 2016)"],
    15669: ["the Planning Board unanimously approved an amendment to the Site A Development Plan for Blocks 12 and 13"],
}

# Block labels in the Land Use Diagram's text layer (PDF points, top-left of the "(NN)" label), the
# height printed in the block, and the use and homes it lists. Blocks 6-9 are built (drawn from
# their footprints); 12a, 12b and 13 are superseded by the 2026 Radium plan.
BLOCKS = {
    "17b": {"at": (969.0, 298.7), "height": "+50’", "use": "Affordable residential (103 homes)", "phase": "Phase 2"},
    "17a": {"at": (1198.2, 296.2), "height": "+50’", "use": "Residential (42–52 homes)", "phase": "Phase 2"},
    "16": {"at": (1513.9, 298.7), "height": "+ 40’", "use": "Residential (73–88 homes)", "phase": "Phase 2"},
    "15": {"at": (1939.8, 294.6), "height": "+40’", "use": "Residential (128–153 homes)", "phase": "Phase 2"},
    "14": {"at": (1023.6, 477.3), "height": "+50’", "use": "Residential (20–25 homes)", "phase": "Phase 2"},
    "11": {"at": (1023.6, 631.3), "height": "+65’**", "use": "Mixed use (about 220 homes, 50,000 sq ft retail)",
           "phase": "Phase 1"},
    "10a": {"at": (1240.1, 531.7), "height": "+50’", "use": "Residential (70–88 homes)", "phase": "Phase 1B"},
    "10b": {"at": (1239.1, 710.2), "height": "+65’",
            "use": "Mixed use (91 affordable homes, 10,500 sq ft retail)", "phase": "Phase 1B"},
    "04": {"at": (1259.2, 949.4), "height": "+65’", "use": "Mixed use (6,000 sq ft retail and hotel)", "phase": "Phase 3"},
    "03": {"at": (1518.1, 949.4), "height": "+65’", "use": "Commercial (about 70,000 sq ft)", "phase": "Phase 3"},
    "01a": {"at": (2054.2, 944.6), "height": "+40’", "use": "Residential (17–21 homes)", "phase": "Phase 1B"},
    "01b": {"at": (1856.6, 1032.1), "height": "+40’", "use": "Commercial (about 38,000 sq ft)", "phase": "Phase 3"},
}
BUILT_BLOCKS = {"06": (2216.7, 637.2), "07": (1960.8, 637.2), "08": (1710.2, 637.2), "09": (1509.3, 637.2)}
# Block 15 is drawn in two pieces either side of Skylark Street; only the west one is labelled.
# The Parcel Diagram (p. 12) gives Block 15 as one 7.13-acre parcel spanning both.
EXTRA_PIECES = {"15": [(4560, 510)]}  # raster pixel inside the east piece
BLOCK_NOTES = {
    "10a": "The 2016 design review gave Block 10 a 60-ft limit; the 2022 Development Plan split it into 10a at 50 ft "
           "and 10b at 65 ft.",
    "10b": "The 2016 design review gave Block 10 a 60-ft limit; the 2022 Development Plan split it into 10a at 50 ft "
           "and 10b at 65 ft. Eden Housing is the affordable developer (2025 annual report).",
    "15": "Drawn in two pieces either side of the Skylark Street extension, as in the plan.",
}

# Georeference controls: street pairs whose centrelines cross inside the diagram, and three existing
# buildings it draws (a pixel inside each outline; OSM ids of the same buildings).
STREET_NS = {"Ardent Way": (2880, "east"), "Orion Street": (3420, "both"), "Corsair Street": (3825, "both"),
             "Skylark Street": (4335, "west")}
STREET_EW = {"Coronado Avenue": 936, "West Atlantic Avenue": 1566}
LANDMARKS = {"Hangar 40": ((630, 600), "w202009359"), "Hangar 41": ((1510, 600), "w202009361"),
             "Building 77 (Naval Air Museum)": ((1500, 1030), "w202009369")}

# Radium Development Plan p. 10 (vector): rectangles in PDF points (x0, top, x1, bottom).
RADIUM_P10 = {"page_index": 9, "museum": (389.0, 50.8, 543.7, 98.3), "theater": (288.4, 167.9, 447.5, 331.8),
              "lot_ft": 436.0, "lot_pt": (245.8, 614.2)}
# p. 17 roof plan: the building outline and the fly tower (rounded rectangle), PDF points.
RADIUM_P17 = {"page_index": 16, "outline": (196.42, 157.25, 392.4, 355.5), "fly": (220.09, 200.79, 260.16, 290.38)}
RADIUM_HEIGHTS = {"body": 43, "fly": 72, "low": 35}  # p. 35 conceptual elevations

# Finished buildings: their block in the diagram, and the height record.
BUILT = {
    "06": {"label": "Leeward at Alameda Point", "homes": 64, "stories": 3, "height": 40,
           "height_src": (f"height: \"+/- 40'-0\"\" to top of parapet (+/- 41'-0\" on some elevations; zoning max shown "
                          f"as 50 ft) on the approved elevations, {BLOCK6_PLANS['title']}, elevations on PDF pp. 34–40 "
                          f"({BLOCK6_PLANS['url']})"),
           "check": (BLOCK6_PLANS, 33, "+/- 40'-0\""),
           "note": "64 townhomes in eleven buildings, three stories with a two-story corner at Main Street."},
    "07": {"label": "Crest at Alameda Point", "homes": 60, "stories": 3, "height": 32,
           "height_src": (f"height: roof at 31'-6\" on the approved elevations, {BLOCK7_PLANS['title']}, sheets 15–16 "
                          f"({BLOCK7_PLANS['url']})"),
           "check": (BLOCK7_PLANS, 15, "31’-6”"),
           "note": "60 three-story townhomes. Sawtooth roof forms rise a little above the 31.5-ft roof line."},
    "08": {"label": "Corsair Flats and The Starling", "homes": 130, "stories": 4, "height": 50,
           "height_src": f"height: \"50 feet high to the top of the parapet\", {SR_2016_03['title']} ({SR_2016_03['url']})",
           "note": "Two four-story Eden Housing buildings: Corsair Flats (60 senior homes) and The Starling (70 family "
                   "homes), 128 of them affordable."},
    "09": {"label": "Aero Apartments", "homes": 200, "stories": 4, "height": 59,
           "height_src": (f"height: \"a maximum height of 59 feet to the top of the parapet\", {SR_2017_12['title']} "
                          f"({SR_2017_12['url']})"),
           "note": "Four stories around a parking garage; 59 ft on West Atlantic Avenue, about 50 ft at the sides "
                   "and rear."},
}
ANNUAL_REPORT = ("Alameda Point Partners' 2025 annual report to the City, Jan 23, 2026 "
                 "(https://legistar1.granicus.com/alameda/attachments/4ed2a440-9155-4809-8443-5c523301c557.pdf)")


# ---------------------------------------------------------------- inputs

def _legistar_text(rec: dict) -> str:
    cache = DOCS / f"ap-legistar-{rec['matter']}-{rec['text_id']}.json"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(rec["api"]) as r:
            cache.write_bytes(r.read())
    text = re.sub(r"\s+", " ", json.loads(cache.read_text())["MatterTextPlain"])
    for q in QUOTES.get(rec["matter"], []):
        if q not in text:
            raise SystemExit(f"Legistar matter {rec['matter']} no longer says {q!r}")
    return text


def _buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "ap-buildings.parquet"
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
    g["osm"] = g["sources"].apply(
        lambda s: (next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None) or "").split("@")[0])
    return g.to_crs(UTM)


def _land_use_diagram(pdf_path):
    """The p. 11 raster (no text), its placement on the page, and the page's words."""
    import pypdfium2 as pdfium
    import pypdfium2.raw as pdfium_c

    page = pdfium.PdfDocument(str(pdf_path))[LUD["page_index"]]
    h = page.get_size()[1]
    img = [o for o in page.get_objects() if o.type == pdfium_c.FPDF_PAGEOBJ_IMAGE and o.get_px_size()[0] > 4000]
    if len(img) != 1 or tuple(img[0].get_px_size()) != LUD_RASTER_PX:
        raise SystemExit("the Land Use Diagram raster is not where expected")
    rgb = np.asarray(img[0].get_bitmap(render=False).to_pil().convert("RGB")).astype(int)
    left, bottom, right, top = img[0].get_bounds()
    place = (left, h - top, right, h - bottom)  # x0, top, x1, bottom in top-down points
    with pdfplumber.open(str(pdf_path), pages=[LUD["page_index"] + 1]) as pdf:
        words = pdf.pages[0].extract_words(keep_blank_chars=True, x_tolerance=2)
    if not any(w["text"] == "LAND USE DIAGRAM" for w in words) and "LAND USE DIAGRAM" not in " ".join(
            w["text"] for w in words):
        raise SystemExit("p. 11 is not the Land Use Diagram")
    return rgb, place, words


def _to_px(place, xy):
    x0, t0, x1, t1 = place
    return ((xy[0] - x0) * LUD_RASTER_PX[0] / (x1 - x0), (xy[1] - t0) * LUD_RASTER_PX[1] / (t1 - t0))


# ---------------------------------------------------------------- georeference

def _gap(line: np.ndarray, c0: int, w: int = 200, min_w: int = 40) -> float | None:
    """Centre of the uncoloured run (a street) nearest c0 in a row or column of the fill mask."""
    seg = ~line[c0 - w:c0 + w]
    best, i = None, 0
    while i < len(seg):
        if seg[i]:
            j = i
            while j < len(seg) and seg[j]:
                j += 1
            if j - i >= min_w and i > 0 and j < len(seg):
                m = c0 - w + (i + j - 1) / 2 + 0.5
                if best is None or abs(m - c0) < abs(best - c0):
                    best = m
            i = j
        else:
            i += 1
    return best


def _georeference(rgb: np.ndarray, bldgs: gpd.GeoDataFrame) -> trace.Similarity:
    coloured = (rgb.max(axis=2) - rgb.min(axis=2)) > 40
    g = tb.streets("alameda_point", (-122.31, 37.77, -122.28, 37.79))
    g = g[g.intersects(box(561700, 4181640, 562600, 4182200))]  # the rebuilt West Atlantic Avenue only
    src, dst, labels = [], [], []
    for ns, (x0, side) in STREET_NS.items():
        for ew, y0 in STREET_EW.items():
            # The N-S street's centre: rows inside the blocks between Coronado and West Atlantic.
            rows = range(y0 + 60, y0 + 200, 4) if ew == "Coronado Avenue" else range(y0 - 200, y0 - 60, 4)
            xs = [v for v in (_gap(coloured[y], x0) for y in rows) if v is not None]
            x = float(np.median(xs))
            side = side if ew == "Coronado Avenue" else "both"  # Coronado jogs at Ardent; blocks 15/18c at Skylark
            cols = ([] if side == "west" else list(range(int(x) + 60, int(x) + 200, 4))) + \
                   ([] if side == "east" else list(range(int(x) - 200, int(x) - 60, 4)))
            ys = [v for v in (_gap(coloured[:, c], y0) for c in cols) if v is not None]
            y = float(np.median(ys))
            if len(xs) < 15 or len(ys) < 15 or np.std(xs) > 3 or np.std(ys) > 3:
                raise SystemExit(f"{ns} / {ew}: street centre not found cleanly in the diagram")
            src.append((x, y))
            dst.append(tb.intersection(g, ns, ew))
            labels.append(f"{ns} / {ew}")
    dark = (rgb.max(axis=2) < 150).astype(np.uint8) * 255
    for name, (seed, osm) in LANDMARKS.items():
        img = dark.copy()
        mask = np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8)
        cv2.floodFill(img, mask, seed, 128)
        ys, xs = np.nonzero(img == 128)
        if not 10_000 < len(xs) < 400_000:
            raise SystemExit(f"{name}: outline not closed in the diagram")
        poly = bldgs[bldgs["osm"] == osm].geometry
        if len(poly) != 1:
            raise SystemExit(f"{name}: OpenStreetMap footprint {osm} not found")
        c = poly.iloc[0].centroid
        src.append((xs.mean() + 0.5, ys.mean() + 0.5))
        dst.append((c.x, c.y))
        labels.append(f"{name} (outline centroid)")
    sim = trace.fit_similarity(src, dst, labels)
    if sim.rms_m > 3.5 or max(sim.residuals_m) > 6:
        raise SystemExit(f"Land Use Diagram fit is poor: RMS {sim.rms_m:.1f} m")
    return sim


# ---------------------------------------------------------------- blocks

def _fill_region(rgb: np.ndarray, lines: np.ndarray, seed: tuple[int, int]):
    """The flat-colour fill containing a pixel, as a pixel polygon grown back over its outline."""
    x, y = seed
    col = rgb[y, x]
    m = ((np.abs(rgb - col).max(axis=2) <= 6) & (lines == 0)).astype(np.uint8)
    _, cc = cv2.connectedComponents(m, connectivity=4)
    reg = (cc == cc[y, x]).astype(np.uint8)
    reg = cv2.morphologyEx(reg, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    contours, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    # The fills stop at the black outline; grow back to its centre (about 2 px).
    return Polygon(c.reshape(-1, 2) + 0.5).buffer(0).buffer(2.0, join_style="mitre").simplify(1.0), tuple(col)


def _blocks(rgb, place, words, sim):
    dark = (rgb.max(axis=2) < 120).astype(np.uint8)
    # Outlines (some dashed): close along rows and columns so dashes still separate the fills.
    lines = (cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((1, 31), np.uint8))
             | cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((31, 1), np.uint8)))
    text = [(w["x0"], w["top"], w["x1"], w["bottom"], w["text"].strip()) for w in words]

    def label_word(name, at):
        hit = [t for t in text if t[4] == f"({name})" and abs(t[0] - at[0]) < 1 and abs(t[1] - at[1]) < 1]
        if len(hit) != 1:
            raise SystemExit(f"label ({name}) not found in the Land Use Diagram's text")
        x0, t0, x1, t1, _ = hit[0]
        return _to_px(place, ((x0 + x1) / 2, (t0 + t1) / 2))

    out = {}
    for name, spec in BLOCKS.items():
        cx, cy = label_word(name, spec["at"])
        poly, col = _fill_region(rgb, lines, (int(cx), int(cy)))
        pieces = [poly]
        for seed in EXTRA_PIECES.get(name, []):
            p2, col2 = _fill_region(rgb, lines, seed)
            if col2 != col:
                raise SystemExit(f"Block {name}: the extra piece isn't the same land use colour")
            pieces.append(p2)
        px = shapely.union_all(pieces)
        # The block's height must be printed inside its fill.
        heights = [t[4] for t in text if re.fullmatch(r"\+\s?\d+’\**", t[4])
                   and px.contains(shapely.Point(_to_px(place, ((t[0] + t[2]) / 2, (t[1] + t[3]) / 2))))]
        if heights != [spec["height"]]:
            raise SystemExit(f"Block {name}: expected height {spec['height']!r} in the fill, found {heights}")
        out[name] = sim.geometry(px)
    built = {}
    for name, at in BUILT_BLOCKS.items():
        cx, cy = label_word(name, at) if name != "08" else _to_px(place, (at[0] + 25, at[1] + 14))
        poly, _ = _fill_region(rgb, lines, (int(cx), int(cy)))
        built[name] = sim.geometry(poly)
    return out, built


# ---------------------------------------------------------------- Radium

def _radium(bldgs: gpd.GeoDataFrame):
    pdf_path = trace.fetch_document(RADIUM["url"], DOCS / RADIUM["file"], RADIUM["sha256"])
    with pdfplumber.open(str(pdf_path), pages=[RADIUM_P10["page_index"] + 1, RADIUM_P17["page_index"] + 1,
                                               35]) as pdf:
        p10, p17, p35 = pdf.pages
        rects = [(round(r["x0"], 1), round(r["top"], 1), round(r["x1"], 1), round(r["bottom"], 1)) for r in p10.rects]
        for key in ("museum", "theater"):
            if not any(max(abs(a - b) for a, b in zip(r, RADIUM_P10[key])) < 0.3 for r in rects):
                raise SystemExit(f"Radium p. 10: the {key} rectangle has moved")
        t10 = p10.extract_text()
        t17 = p17.extract_text()
        t35 = p35.extract_text()
    for s in ("Performing Arts Center", "Museum", "436.0", "PROPERTY LINE"):
        if s not in t10:
            raise SystemExit(f"Radium p. 10 no longer shows {s!r}")
    if "70'-6\"" not in t17 or not all(f"{h}'" in t35 for h in RADIUM_HEIGHTS.values()):
        raise SystemExit("Radium heights not found on pp. 17 and 35")

    # Scale from the 436-ft lot dimension; rotation and shift from the museum's outline.
    scale = RADIUM_P10["lot_ft"] * FT / (RADIUM_P10["lot_pt"][1] - RADIUM_P10["lot_pt"][0])
    mx0, mt, mx1, mb = RADIUM_P10["museum"]
    plan = np.array([(mx0, mt), (mx1, mt), (mx1, mb), (mx0, mb)], float)
    plan[:, 1] *= -1  # y up
    plan *= scale
    museum = bldgs[bldgs["osm"] == LANDMARKS["Building 77 (Naval Air Museum)"][1]].geometry.iloc[0]
    rr = np.asarray(museum.minimum_rotated_rectangle.exterior.coords)[:4]
    # Order the footprint's corners like the plan's: NW, NE, SE, SW.
    c = rr.mean(axis=0)
    ang = np.arctan2(rr[:, 1] - c[1], rr[:, 0] - c[0])
    order = [int(np.argmin(np.abs(((ang - a + np.pi) % (2 * np.pi)) - np.pi))) for a in
             np.arctan2(plan[:, 1] - plan[:, 1].mean(), plan[:, 0] - plan[:, 0].mean())]
    dst = rr[order]
    pa, pb = plan - plan.mean(0), dst - dst.mean(0)
    u, _, vt = np.linalg.svd(pa.T @ pb)
    rot = (u @ vt).T
    if np.linalg.det(rot) < 0:
        raise SystemExit("Radium fit flipped")

    def to_utm(xy):
        a = np.asarray(xy, float).reshape(-1, 2).copy()
        a[:, 1] *= -1
        return (rot @ (a * scale - plan.mean(0)).T).T + dst.mean(0)

    resid = np.linalg.norm(to_utm(np.array([(mx0, mt), (mx1, mt), (mx1, mb), (mx0, mb)])) - dst, axis=1)
    theater_pt = box(*RADIUM_P10["theater"][:2], *RADIUM_P10["theater"][2:])
    # Fly tower: p. 17 outline mapped onto the p. 10 rectangle (same building, two drawings).
    ox0, ot, ox1, ob = RADIUM_P17["outline"]
    tx0, tt, tx1, tb_ = RADIUM_P10["theater"]
    fx0, ft, fx1, fb = RADIUM_P17["fly"]
    sx, sy = (tx1 - tx0) / (ox1 - ox0), (tb_ - tt) / (ob - ot)
    fly_pt = box(tx0 + (fx0 - ox0) * sx, tt + (ft - ot) * sy, tx0 + (fx1 - ox0) * sx, tt + (fb - ot) * sy)
    theater = shapely.transform(theater_pt, to_utm)
    fly = shapely.transform(fly_pt, to_utm)
    report = {
        "method": ("vector site plan; scale from its 436-ft lot dimension, rotation and shift fitted to the Naval Air "
                   "Museum outline's corners against the museum's OpenStreetMap footprint (w202009369)"),
        "scale_m_per_pt": round(scale, 5),
        "rotation_deg": round(float(np.degrees(np.arctan2(rot[1, 0], rot[0, 0]))), 3),
        "rms_m": round(float(np.sqrt((resid ** 2).mean())), 2),
        "residuals_m": [round(float(r), 2) for r in resid],
        "note": "The plan's museum outline is 17 m deep against 15.5 m in OpenStreetMap (its porch), which sets the RMS.",
        "fly_tower": "p. 17 roof plan's fly tower, mapped from that plan's building outline onto the p. 10 rectangle",
    }
    return theater, fly, report


# ---------------------------------------------------------------- main

def main() -> None:
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    for rec in (SR_2016_03, SR_2016_06, SR_2017_12, SR_2022_07, CC_2026_04):
        _legistar_text(rec)
    for name, spec in BUILT.items():
        if "check" in spec:
            doc, page_no, s = spec["check"]
            path = trace.fetch_document(doc["url"], DOCS / doc["file"], doc["sha256"])
            import pypdfium2 as pdfium

            if s not in pdfium.PdfDocument(str(path))[page_no].get_textpage().get_text_range():
                raise SystemExit(f"Block {name}: {s!r} not on page index {page_no} of {doc['file']}")

    pdf_path = trace.fetch_document(PLAN["url"], DOCS / PLAN["file"], PLAN["sha256"])
    rgb, place, words = _land_use_diagram(pdf_path)
    bldgs = _buildings()
    sim = _georeference(rgb, bldgs)
    print(f"[alameda-point] Land Use Diagram fit: RMS {sim.rms_m:.2f} m over {len(sim.labels)} controls, "
          f"scale {sim.scale:.4f} m/px, rotation {np.degrees(sim.rotation):.2f}°")
    blocks, built_blocks = _blocks(rgb, place, words, sim)

    # Finished buildings: OpenStreetMap footprints whose centre is in the block.
    osm = bldgs[bldgs["osm"] != ""]
    built = {}
    for name, poly in built_blocks.items():
        rows = osm[osm.geometry.centroid.within(poly.buffer(3))]
        if rows.empty:
            raise SystemExit(f"Block {name}: no OpenStreetMap footprints")
        built[name] = rows
        print(f"[alameda-point] Block {name}: {len(rows)} footprints ({', '.join(rows['osm'])}), "
              f"{rows.geometry.area.sum():.0f} m² in a {poly.area:.0f} m² block")
    built_union = shapely.union_all([g for r in built.values() for g in r.geometry])

    theater, fly, radium_report = _radium(bldgs)
    print(f"[alameda-point] Radium site plan fit: RMS {radium_report['rms_m']} m on the museum's corners")

    to_wgs = lambda g: gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]  # noqa: E731
    fig = f"{PLAN_TITLE}, {LUD['figure']}, p. {LUD['printed_page']}"
    features = []
    for name, spec in BLOCKS.items():
        geom = blocks[name]
        if geom.intersects(built_union):
            geom = geom.difference(built_union)
        geom = trace.as_multipolygon(shapely.make_valid(geom.simplify(0.4)))
        h = int(re.search(r"\d+", spec["height"]).group())
        props = {
            "kind": "block",
            "block": name,
            "label": f"Block {name.lstrip('0')}",
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": None,
            "base_ft": 0,
            "use": spec["use"],
            "phase": spec["phase"],
            "illustrative": True,
            "source": (f"illustrative: drawn to the {h}-ft height shown for the block in {fig} ({PLAN['url']}); "
                       f"block outline traced from the same diagram; phase from {PLAN_PHASING}"),
        }
        if name in BLOCK_NOTES:
            props["note"] = BLOCK_NOTES[name]
        if name == "11":
            props["height_ft"] = 78
            props["source"] = (f"illustrative: drawn to the 78 ft of the Block 11 design the Planning Board approved "
                               f"(\"Block 11 is 78 feet to the top of the parapet\", {SR_2016_03['title']}, "
                               f"{SR_2016_03['url']}; still \"approved in 2016\" in {SR_2022_07['title']}, "
                               f"{SR_2022_07['url']}); block outline traced from {fig} ({PLAN['url']})")
            props["note"] = ("220 homes approved in 2016 (amended 2019 and 2022), not yet built. The plan's limit is "
                             "65 ft, which the Precise Plan lets the Planning Board exceed for exceptional design; "
                             "the approved building is about 78 ft.")
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(geom))})
        print(f"[alameda-point] Block {name}: {geom.area / ACRE_M2:.2f} ac at {props['height_ft']} ft")

    # Radium Performing Arts Center (Blocks 12 and 13), 2026.
    rad_src = (f"illustrative: footprint traced from the \"Performing Arts Center\" on {RADIUM['title']}, p. 10 "
               f"({RADIUM['url']}), approved by the Planning Board on Mar 23, 2026 ({CC_2026_04['title']}, "
               f"{CC_2026_04['url']}); ")
    body = theater.difference(fly)
    features.append({"type": "Feature", "properties": {
        "kind": "building", "block": "12–13", "label": "Radium Performing Arts Center", "stage": "entitled",
        "height_ft": RADIUM_HEIGHTS["body"], "podium_ft": None, "base_ft": 0,
        "use": "Performing arts center (about 600 + 210 seats, 53,000 sq ft)", "phase": "Phase 2",
        "illustrative": True,
        "source": rad_src + f"height: the {RADIUM_HEIGHTS['body']}-ft roof of the conceptual elevations, p. 35",
        "note": ("Conceptual design: roofs step from about 32–35 ft at the edges to 43–44.5 ft over the house. "
                 "Design review is still to come. The 2022 plan showed a 35-ft theater here."),
    }, "geometry": mapping(to_wgs(body))})
    features.append({"type": "Feature", "properties": {
        "kind": "building", "block": "12–13", "label": "Radium fly tower", "stage": "entitled",
        "height_ft": RADIUM_HEIGHTS["fly"], "podium_ft": None, "base_ft": 0,
        "use": "Performing arts center (stage house)", "phase": "Phase 2", "illustrative": True,
        "source": rad_src + (f"fly tower located from the roof plan, p. 17 (spot height 70'-6\"); height: "
                             f"{RADIUM_HEIGHTS['fly']} ft on the conceptual elevations, p. 35"),
        "note": "The stage's fly tower, the tallest part of the theater.",
    }, "geometry": mapping(to_wgs(fly))})

    for name, spec in BUILT.items():
        rows = built[name]
        ids = ", ".join(rows["osm"])
        geom = shapely.make_valid(shapely.union_all(rows.geometry.to_numpy()).simplify(0.3))
        props = {
            "kind": "building",
            "block": name,
            "label": spec["label"],
            "stage": "complete",
            "height_ft": spec["height"],
            "podium_ft": None,
            "base_ft": 0,
            "use": "Residential" + (" over ground-floor retail" if name == "09" else ""),
            "phase": "Phase 1",
            "illustrative": False,
            "source": (f"footprint{'s' if len(rows) > 1 else ''}: OpenStreetMap {ids} via Overture "
                       f"{config.OVERTURE_RELEASE}; {spec['height_src']}; complete per {ANNUAL_REPORT}"),
            "stories": spec["stories"],
            "homes": spec["homes"],
            "note": spec["note"],
        }
        features.append({"type": "Feature", "properties": props, "geometry": mapping(to_wgs(geom))})

    for f in features:
        c = shapely.geometry.shape(f["geometry"])
        if not site_utm.buffer(30).contains(gpd.GeoSeries([c.centroid], crs=4326).to_crs(UTM).iloc[0]):
            raise SystemExit(f"{f['properties']['label']} is off the site")
    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    massing_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                f"Illustrative massing: Site A's {len(BLOCKS)} unbuilt development blocks are drawn to the heights in the "
                "2022 Development Plan (40 to 65 ft; Block 11 at its approved 78 ft), over whole blocks, not as building "
                "designs. The Radium theater on Blocks 12–13, approved in 2026, is drawn from its conceptual plan. "
                "The finished buildings on Blocks 6–9 use their real footprints and the heights in their approved "
                "designs. Parks, streets, parking and the Navy-era buildings aren't drawn."
            ),
            "note": "Unbuilt blocks are drawn to their height limits, not as building designs.",
            "sourceUrl": PLAN["url"],
            "sourceLabel": "Site A development plan, 2022 (PDF)",
            "georeference": {
                "land_use_diagram": {**sim.report(), "method": (
                    "raster figure; street centrelines midway between block fills at eight intersections and the "
                    "outline centroids of Hangars 40 and 41 and Building 77, matched to OpenStreetMap via Overture")},
                "radium_site_plan": radium_report,
            },
            "license": ("Shapes traced from public City of Alameda documents. Building footprints and georeference: "
                        + OSM_LICENSE + "."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round(massing_fc), separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"[alameda-point] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
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
