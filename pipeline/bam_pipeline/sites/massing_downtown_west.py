"""Downtown West (San José): block height limits traced from the Downtown West Design Standards and Guidelines.

Sources:
- Downtown West Design Standards and Guidelines (DWDSG), October 2020, published as Appendix M of the
  Downtown West Mixed-Use Plan Draft EIR (SCH 2019080493) on CEQAnet. Section 5.6 "Building Heights"
  (PDF pp. 198-200, printed pp. 179-181):
  - Figure 5.9 "Block plan" (PDF p. 194, printed p. 175) gives the new development blocks (S5.5.1:
    above-grade new development is limited to them), the historic buildings to be rehabilitated and the
    existing Creekside Walk buildings (D8-D13) that stay unless they can't reasonably be retained.
  - Figure 5.12 "Illustrative maximum height per block above current ground level" (PDF p. 200,
    printed p. 181) colours each block by its maximum height (180-290 ft above current ground).
  - S5.6.3 (same page) caps blocks D5 and F6 at 40 ft, D6 at 80 ft and H1 at 150 ft.
  - Figure 3.3 "Conceptual land use plan" (PDF p. 71, printed p. 52) gives each block's conceptual use.
- Check: Development Agreement, Ordinance 30610 (June 2021), Section 4.2.3(a) table "Maximum Building
  Height Desired (AGL)" for nine buildings (A1 180, B1 200, C2 230, C3 230, D4 255, D7 270, E1 260,
  F1 280, G1 290). Eight match Figure 5.12; E1 is 260 ft in the DA and 280 ft in Figure 5.12, whose
  FAA contours (Figure 5.13) run from about 260 ft at E1's north end to 280 ft at its south end.

Approved changes found (Council item 10.2, May 25, 2021, Legistar matter 9022): the General Plan
resolution (item 10.2(c), PDF p. 91) lists lower height limits on blocks D5, D6, D8-13, F6, H1, H5 and
H6 under the approved DWDSG. H5 and H6 don't exist in the October 2020 draft; the Development
Agreement's Schedule D1 (affordable housing sites) places them in the Auzerais Avenue arm of the draft's
block H3. Their limits aren't given, so that arm is drawn as an outline only (height null). No other
attachment of the item contains the approved DWDSG, its errata list or a height table.

Which version: the City Council approved the DWDSG dated March 1, 2021 with errata dated April 5, 2021
(PD Permit resolution, May 25, 2021). That edition is posted only on sanjoseca.gov, which refuses
scripted downloads, so it couldn't be checked here. The October 2020 edition is the newest one on an
official host that could be read; the DA table (adopted after the March 2021 edition) agrees with it
except on E1. Treat block heights as needing verification against the approved edition.

What this is and isn't:
- Each new development block is drawn to its maximum height, not as a building design, so it is
  labelled illustrative. The DWDSG itself calls Figure 5.12 illustrative: the binding limits are the
  FAA NAVD 88 contours (Figure 5.11), and the FAA can lower any building through its own review.
- Streets, parks and open space (the hatched areas in Figure 5.12), the historic buildings to be
  rehabilitated (40 and 150 South Montgomery Street, 374 West Santa Clara Street) and the Creekside Walk
  buildings at Autumn Street (D8-D13) aren't drawn: they stay in the base map.
- Nothing has been built: the city reported in November 2024 that no new construction has begun, so
  every block is "entitled".

Georeferencing:
- Figures 5.9 and 5.12 are raster images on the same 1800 x 1168 base map. Its existing buildings are
  traced (white fills inside thin outlines) and matched to OpenStreetMap footprints (via Overture): a
  rough start from four street intersections, a raster correlation, then least squares on the
  centroids of every figure building that overlaps a footprint by IoU > 0.6. The fit is recorded.
- The traced blocks are trimmed to the 16 DC(PD) polygons of rezoning file PDC19-039 in the City of
  San José zoning layer (CC-BY 4.0); the share trimmed is recorded. Two of those polygons carry the
  file number as "19039" (blocks D5-D7 lie on them) and are missing from data/boundaries/downtown-west,
  whose query only matches 'PDC19-039%'.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_downtown_west
"""

from __future__ import annotations

import json
import os
import re

import cv2
import geopandas as gpd
import numpy as np
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.parquet as pq
import shapely
from shapely.geometry import Point, Polygon, mapping

from .. import config, trace
from . import massing_india_basin as ib
from . import traced_boundaries as tb

PROJECT_ID = "downtown-west"
UTM = tb.UTM
DOCS = config.ROOT / "data" / "raw" / "docs"

DWDSG = {
    "title": "Downtown West Design Standards and Guidelines (October 2020), Draft EIR Appendix M (SCH 2019080493)",
    "url": "https://ceqanet.lci.ca.gov/2019080493/4/Attachment/WFPURX",
    "listing": "https://ceqanet.lci.ca.gov/2019080493/4",
    "sha256": "8bbb0fb8dbb7545ee039cf5a9de96231e0bfecf1506972a02a7d398b69db6ff1",
    "file": "dtw-dwdsg-2020-deir-apxM.pdf",
}
FIG_5_9 = {"page_index": 193, "printed_page": "175", "figure": "Figure 5.9, Block plan"}
FIG_5_12 = {"page_index": 199, "printed_page": "181",
            "figure": "Figure 5.12, Illustrative maximum height per block above current ground level"}
FIG_3_3 = {"page_index": 70, "printed_page": "52", "figure": "Figure 3.3, Conceptual land use plan"}
IMAGE_SIZE = (1800, 1168)

DA = {
    "title": "Downtown West Development Agreement, Ordinance 30610 (June 2021), Section 4.2.3(a)",
    "url": "https://legistar.granicus.com/sanjose/attachments/d9985f7d-1a96-43f8-a1e5-96ad5a17618b.pdf",
    "sha256": "a147cd89355aa892846fdff1ee65513a24be7d80142eca58b571b281822f3860",
    "file": "dtw-ord-30610-da.pdf",
}

# Block label centres in the figure images (pixels). Figures 5.9 and 5.12 share the base map pixel for pixel.
LABELS = {
    "A1": (1612, 230), "B1": (1395, 358), "C1": (1305, 428), "C2": (1158, 507), "C3": (1265, 578),
    "D4": (1022, 668), "D5": (962, 688), "D6": (906, 684), "D7": (845, 678),
    "E1": (1025, 858), "E2": (942, 840), "E3": (975, 910),
    "F1": (662, 614), "F2": (770, 672), "F3": (568, 648), "F4": (720, 690), "F5": (575, 544), "F6": (662, 686),
    "G1": (470, 565), "H1": (420, 703), "H2": (358, 640), "H3": (240, 599), "H4": (186, 655),
}
# Figure 5.9 fills (RGB in the image).
NEW_BLOCK_RGB = (180, 213, 220)  # "New development blocks"
HISTORIC_RGB = (31, 76, 97)  # "Existing historic buildings to be rehabilitated"
# S5.6.3 "Blocks with limited heights" (PDF p. 200), checked against the page text below.
LIMITED = {"D5": 40, "F6": 40, "D6": 80, "H1": 150}
LIMITED_TEXT = [r"Blocks D5 and F6: 40 feet\s+maximum height", r"Block D6: 80 feet maximum height",
                r"Block H1: 150 feet maximum height"]
# Figure 3.3 conceptual land use, read block by block (blue office, yellow residential, magenta active
# use; C3 is striped office/residential; C1 has a small residential/hotel corner).
USE = {
    "A1": "Office", "B1": "Office", "C1": "Residential", "C2": "Office", "C3": "Residential or office",
    "D4": "Office", "D5": "Active use", "D6": "Active use", "D7": "Office",
    "E1": "Office", "E2": "Residential", "E3": "Residential",
    "F1": "Office", "F2": "Residential", "F3": "Office", "F4": "Residential", "F5": "Office", "F6": "Active use",
    "G1": "Office", "H1": "Residential", "H5/H6": "Residential", "H2": "Residential", "H3": "Residential", "H4": "Residential",
}
# A rough start only (figure pixels): street intersections read off the base map. The building match does the fit.
ROUGH_START = {
    ("West Santa Clara Street", "South Montgomery Street"): (1075, 630),
    ("West San Fernando Street", "South Montgomery Street"): (803, 641),
    ("West Julian Street", "North Montgomery Street"): (1413, 465),
    ("West Julian Street", "Stockton Avenue"): (1256, 269),
}
GPA = {
    "title": "General Plan Amendment resolution GP19-009, Council item 10.2(c), May 25, 2021 (Legistar matter 9022)",
    "url": "https://legistar.granicus.com/sanjose/attachments/4fa89312-fd9b-4f85-932d-8d5c463c0e8f.pdf",
    "sha256": "a7f67eb35a25ff290d754d7062ce34410233b7858dc49447eb24bc2dde00e1ab",
    "file": "dtw-res-c-gp19-009.pdf",
    "page_index": 90,
    "quote": r"blocks\s+D5,\s+D6,\s+D8-13,\s+F6,\s+H1,\s+H5,\s+and\s+H6\s+include\s+lower\s+height\s+limits",
}
# DA Exhibit (Affordable Housing Plan) Schedule D1, "Project site plan generally depicting location of H1, H5,
# and H6 properties" (Feb 11, 2021): H5 and H6 are carved from the arm of the October 2020 block H3 along Auzerais Avenue.
DA_D1_PAGE = 274
# Where the Auzerais Avenue arm of H3 meets the rest of the block in Figure 5.9 (pixels): the dashed parcel line
# nearer the block's corner. H5 and H6 lie west of it (towards Auzerais Avenue), per Schedule D1.
H56_LINE = ((186.25, 570.0), (205.0, 598.0))
H56_SIDE = (150.0, 600.0)  # a point in that arm, on the H5/H6 side

ZONING = {
    "title": "City of San José Zoning Districts (OPN_OpenDataService layer 401), Downtown West DC(PD) districts",
    "url": "https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/401",
    # Two of the 16 polygons approved with PDC19-039 carry the file number as "19039".
    "where": "REZONINGFILE LIKE 'PDC19-039%' OR REZONINGFILE = '19039'",
    "file": config.ROOT / "data" / "raw" / "massing" / "dtw-zoning-pdc19-039.geojson",
}
STREETS_BBOX = (-121.912, 37.318, -121.890, 37.342)
BUILDINGS_BBOX = (-121.9100, 37.3205, -121.8935, 37.3405)


# ---------------------------------------------------------------- documents

def _image(doc, page_index: int) -> np.ndarray:
    imgs = [o for o in doc[page_index].get_objects() if o.type == 3]  # FPDF_PAGEOBJ_IMAGE
    big = max(imgs, key=lambda o: o.get_bitmap(render=False).width)
    rgb = np.asarray(big.get_bitmap(render=False).to_pil().convert("RGB"))
    if (rgb.shape[1], rgb.shape[0]) != IMAGE_SIZE:
        raise SystemExit(f"unexpected figure image size {rgb.shape} on PDF page {page_index + 1}")
    return rgb


def legend(pdf_path) -> dict[int, tuple]:
    """Figure 5.12's legend: each filled swatch and the "NNN feet" label to its right."""
    import pdfplumber

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[FIG_5_12["page_index"]]
        words = page.extract_words()
        out = {}
        for c in page.curves:
            col = c.get("non_stroking_color")
            if not c.get("fill") or not col or len(col) != 3:
                continue
            near = [w for w in words if abs(w["top"] - c["top"]) < 6 and 0 < w["x0"] - c["x1"] < 20]
            if near and near[0]["text"].isdigit():
                out[int(near[0]["text"])] = tuple(round(v * 255) for v in col)
    if sorted(out) != [180, 200, 215, 230, 255, 265, 270, 280, 290]:
        raise SystemExit(f"unexpected Figure 5.12 legend {sorted(out)}")
    return out


def check_limits(doc) -> None:
    text = doc[FIG_5_12["page_index"]].get_textpage().get_text_range()
    for pat in LIMITED_TEXT:
        if not re.search(pat, text):
            raise SystemExit(f"S5.6.3 text not found on DWDSG PDF p. {FIG_5_12['page_index'] + 1}: {pat}")


def check_approved_changes() -> None:
    """Approved records that change the October 2020 heights: H5 and H6 get lower (unstated) limits."""
    import pypdfium2 as pdfium

    path = trace.fetch_document(GPA["url"], DOCS / GPA["file"], GPA["sha256"])
    t = pdfium.PdfDocument(str(path))[GPA["page_index"]].get_textpage().get_text_range()
    if not re.search(GPA["quote"], t):
        raise SystemExit("the GP resolution's list of lower-height blocks has changed; review before drawing")
    da_path = trace.fetch_document(DA["url"], DOCS / DA["file"], DA["sha256"])
    d1 = pdfium.PdfDocument(str(da_path))[DA_D1_PAGE].get_textpage().get_text_range()
    if not all(re.search(rf"\b{b}\b", d1) for b in ("H1", "H3", "H4", "H5", "H6")) or "H5, and H6" not in d1:
        raise SystemExit("DA Schedule D1 (H1, H5 and H6 properties) was not where expected")


def split_h56(poly: Polygon) -> tuple[Polygon, Polygon]:
    """Split the October 2020 block H3 into (H3, H5 and H6) along the parcel line in Figure 5.9."""
    (x1, y1), (x2, y2) = H56_LINE
    dx, dy = x2 - x1, y2 - y1
    a, b = (x1 - 50 * dx, y1 - 50 * dy), (x1 + 50 * dx, y1 + 50 * dy)
    nx, ny = -dy, dx
    side = 1 if (H56_SIDE[0] - x1) * nx + (H56_SIDE[1] - y1) * ny > 0 else -1
    half = Polygon([a, b, (b[0] + side * 5000 * nx / np.hypot(nx, ny), b[1] + side * 5000 * ny / np.hypot(nx, ny)),
                    (a[0] + side * 5000 * nx / np.hypot(nx, ny), a[1] + side * 5000 * ny / np.hypot(nx, ny))])
    h56 = trace.largest_polygon(poly.intersection(half))
    h3 = trace.largest_polygon(poly.difference(half))
    if not h56.contains(Point(H56_SIDE)) or not 0.15 < h56.area / poly.area < 0.5:
        raise SystemExit(f"unexpected H5/H6 split ({h56.area / poly.area:.0%} of H3)")
    return h3, h56


def da_heights() -> dict[str, int]:
    """The Development Agreement's 'Maximum Building Height Desired (AGL)' table."""
    import pypdfium2 as pdfium

    path = trace.fetch_document(DA["url"], DOCS / DA["file"], DA["sha256"])
    doc = pdfium.PdfDocument(str(path))
    for i in range(80, 100):
        t = doc[i].get_textpage().get_text_range()
        if "Minimum Crane Height" in t:
            return {b: int(h) for b, h, _ in re.findall(r"\b([A-H]\d)\s+(\d{3})\s+(\d{2})\b", t)}
    raise SystemExit("the DA's building height table was not found")


# ---------------------------------------------------------------- tracing

def blocks(p59: np.ndarray, p512: np.ndarray, leg: dict[int, tuple]) -> dict[str, dict]:
    """New development blocks (figure pixels) with the Figure 5.12 height colour inside each.

    A block is a Figure 5.9 "new development" fill, plus the solid (unhatched) Figure 5.12 fill on the
    same pixels, which recovers block H2 where Figure 5.9 tints it with the riparian overlay. The
    hatched streets and open space in Figure 5.12 are removed by an opening; historic buildings and
    black outlines are cut out, so blocks that touch stay apart.
    """
    a59, a512 = p59.astype(float), p512.astype(float)
    keys = list(leg)
    cols = np.array([leg[k] for k in keys], float)
    dist = np.linalg.norm(a512[:, :, None, :] - cols[None, None], axis=3)
    nearest, coloured = dist.argmin(2), dist.min(2) < 45
    solid = cv2.morphologyEx(coloured.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)) > 0
    new = np.linalg.norm(a59 - NEW_BLOCK_RGB, axis=2) < 28
    historic = np.linalg.norm(a59 - HISTORIC_RGB, axis=2) < 40
    black = ((a59.max(2) < 90) | (a512.max(2) < 40)) & ~historic
    historic = cv2.dilate(historic.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    mask = (new | solid) & ~historic & ~black
    mask = cv2.morphologyEx(mask.astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=4)
    out: dict[str, dict] = {}
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < 150:
            continue
        cs, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        poly = Polygon(max(cs, key=cv2.contourArea).reshape(-1, 2) + 0.0).buffer(0)
        poly = max(getattr(poly, "geoms", [poly]), key=lambda q: q.area)
        name = min(LABELS, key=lambda k: poly.distance(Point(LABELS[k])))
        if poly.distance(Point(LABELS[name])) > 8:
            raise SystemExit(f"a traced block at {poly.centroid} has no block label")
        counts = np.bincount(nearest[(lab == i) & coloured], minlength=len(keys))
        share = counts.max() / max(1, counts.sum())
        if share < 0.9:
            raise SystemExit(f"Block {name}: mixed Figure 5.12 colours ({share:.0%} {keys[counts.argmax()]} ft)")
        if name in out:
            raise SystemExit(f"Block {name} traced twice")
        # Fills stop just inside the black outlines (about 1.5 px wide): grow to the outline's middle.
        out[name] = {"px": poly.buffer(1.5, join_style="mitre"), "fig_ft": keys[counts.argmax()]}
    if set(out) != set(LABELS):
        raise SystemExit(f"blocks not traced: {sorted(set(LABELS) - set(out))}")
    return out


def figure_buildings(p59: np.ndarray) -> list[Polygon]:
    """Existing buildings in the base map: white fills (no colour) enclosed by thin outlines."""
    a = p59.astype(int)
    white = ((a.mean(2) >= 250) & (a.max(2) - a.min(2) < 6)).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(white, connectivity=4)
    out = []
    for i in range(1, n):
        if 25 <= stats[i, cv2.CC_STAT_AREA] <= 4000:  # streets are one huge white region
            x, y, w, h = stats[i, :4]
            cs, _ = cv2.findContours((lab[y:y + h, x:x + w] == i).astype(np.uint8), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
            c = max(cs, key=cv2.contourArea).reshape(-1, 2) + [x, y]
            if len(c) >= 3:
                p = shapely.make_valid(Polygon(c + 0.0).buffer(0.5, join_style="mitre"))
                if p.area > 0:
                    out.append(p)
    return out


def pd_zoning() -> gpd.GeoDataFrame:
    """All 16 DC(PD) polygons of rezoning file PDC19-039, as published."""
    import urllib.parse
    import urllib.request

    out = ZONING["file"]
    if not out.exists():
        q = urllib.parse.urlencode({"where": ZONING["where"], "outFields": "*", "outSR": 4326, "f": "geojson"})
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(f"{ZONING['url']}/query?{q}") as r:
            out.write_bytes(r.read())
    g = gpd.read_file(out)
    if len(g) != 16:
        raise SystemExit(f"expected 16 PDC19-039 zoning polygons, found {len(g)}")
    return g.to_crs(UTM)


def overture_buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "dtw-buildings.parquet"
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


def georeference(fig_bld: list[Polygon], osm_bld: gpd.GeoDataFrame) -> tuple[trace.Similarity, dict]:
    streets = tb.streets("dtw", STREETS_BBOX)
    streets = streets[streets["subtype"] == "road"]
    rough = trace.fit_similarity(list(ROUGH_START.values()), [tb.intersection(streets, a, b) for a, b in ROUGH_START])

    # 1. Raster correlation of figure buildings against Overture buildings (2 m cells, +/-80 m shift).
    res, margin = 2.0, 40
    centre = Point(rough.apply([(IMAGE_SIZE[0] / 2, IMAGE_SIZE[1] / 2)])[0])
    half = 1100.0
    n = int(2 * half / res)
    x0, y_top = centre.x - half, centre.y + half
    target = ib._raster(osm_bld.geometry.to_numpy(), x0, y_top, n, res)
    pivot = np.asarray(shapely.union_all(fig_bld).centroid.coords[0])
    best = None
    for ds_ in np.linspace(-0.06, 0.06, 13):
        for dr in np.radians(np.linspace(-3, 3, 13)):
            sim = trace.Similarity(rough.scale * (1 + ds_), rough.rotation + dr, 0.0, 0.0)
            sim.tx, sim.ty = rough.apply([pivot])[0] - sim.apply([pivot])[0]
            moving = ib._raster([sim.geometry(b) for b in fig_bld], x0, y_top, n, res)
            r = cv2.matchTemplate(target, moving[margin:-margin, margin:-margin], cv2.TM_CCORR_NORMED)
            _, score, _, loc = cv2.minMaxLoc(r)
            if best is None or score > best[0]:
                best = (score, sim, loc)
    score, sim, loc = best
    sim.tx += (loc[0] - margin) * res
    sim.ty -= (loc[1] - margin) * res

    # 2. Least squares on matched building centroids (IoU > 0.6), repeated until the matches settle.
    geoms = osm_bld.geometry.to_numpy()
    tree = shapely.STRtree(geoms)
    matched = None
    for _ in range(12):
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
    return sim, {
        "method": "building-footprint match: rough start from four street intersections, raster correlation, "
                  "then least squares on the centroids of figure buildings matching OpenStreetMap footprints "
                  "(IoU > 0.6)",
        "scale_m_per_px": round(sim.scale, 5),
        "rotation_deg": round(float(np.degrees(sim.rotation)), 3),
        "rms_m": round(sim.rms_m, 2),
        "median_m": round(float(np.median(r)), 2),
        "max_m": round(float(r.max()), 2),
        "controls": int(len(r)),
        "figure_buildings": len(fig_bld),
        "correlation": round(float(score), 3),
    }


# ---------------------------------------------------------------- main

def main() -> None:
    import pypdfium2 as pdfium

    pdf_path = trace.fetch_document(DWDSG["url"], DOCS / DWDSG["file"], DWDSG["sha256"])
    doc = pdfium.PdfDocument(str(pdf_path))
    check_limits(doc)
    p59, p512 = _image(doc, FIG_5_9["page_index"]), _image(doc, FIG_5_12["page_index"])
    if np.abs(p59.astype(float).mean(2)[:300, :1000] - p512.astype(float).mean(2)[:300, :1000]).mean() > 2:
        raise SystemExit("Figures 5.9 and 5.12 no longer share one base map")
    leg = legend(pdf_path)
    traced = blocks(p59, p512, leg)
    check_approved_changes()
    h3, h56 = split_h56(traced["H3"]["px"])
    traced["H3"]["px"] = h3
    traced["H5/H6"] = {"px": h56, "fig_ft": traced["H3"]["fig_ft"]}

    da = da_heights()
    checks = {}
    for b, h in sorted(da.items()):
        checks[b] = {"figure_5_12_ft": traced[b]["fig_ft"], "da_ft": h}
    print("[downtown-west] DA desired heights vs Figure 5.12: "
          + ", ".join(f"{b} {v['da_ft']}/{v['figure_5_12_ft']}" for b, v in checks.items()))
    differ = [b for b, v in checks.items() if v["da_ft"] != v["figure_5_12_ft"]]
    if differ != ["E1"]:
        raise SystemExit(f"DA and Figure 5.12 heights differ on {differ}; review before drawing")

    fig_bld = figure_buildings(p59)
    osm_bld = overture_buildings()
    sim, report = georeference(fig_bld, osm_bld)
    print(f"[downtown-west] georeference: RMS {report['rms_m']} m over {report['controls']} matched buildings, "
          f"scale {report['scale_m_per_px']} m/px, rotation {report['rotation_deg']} deg")

    zoning = shapely.union_all(pd_zoning().geometry.to_numpy())
    raw_area = outside = 0.0
    fig512 = f"{DWDSG['title']}, {FIG_5_12['figure']}, p. {FIG_5_12['printed_page']}"
    fig59 = f"{FIG_5_9['figure']}, p. {FIG_5_9['printed_page']}"
    features = []
    order = sorted(traced, key=lambda k: (k[0], int(k[1])))
    for name in order:
        t = traced[name]
        g = shapely.make_valid(sim.geometry(t["px"]))
        raw_area += g.area
        inside = g.intersection(zoning)
        outside += g.area - inside.area
        inside = inside.buffer(2.0, join_style="mitre").buffer(-2.0, join_style="mitre").intersection(zoning)
        geom = trace.as_multipolygon(shapely.make_valid(inside.simplify(0.4)))
        geom = trace.as_multipolygon(shapely.MultiPolygon([p for p in geom.geoms if p.area >= 15]))
        limited = LIMITED.get(name)
        draft = ("heights are from the October 2020 draft DWDSG; the approved DWDSG (March 2021, with errata) "
                 "couldn't be retrieved")
        if name == "H5/H6":
            height = None
            source = (f"illustrative: outline only. Traced from {fig59} as the arm of the draft's block H3 along Auzerais Avenue, "
                      f"split at its parcel line; named from the Development Agreement (Ord. 30610, {DA['url']}), "
                      f"Schedule D1 (affordable housing sites H1, H5, H6). The approved General Plan resolution "
                      f"({GPA['url']}, PDF p. {GPA['page_index'] + 1}) says H5 and H6 have lower height limits "
                      f"under the approved DWDSG, which aren't available, so no height is drawn")
        else:
            height = limited or t["fig_ft"]
            da_note = (f"; the approved Development Agreement (Ord. 30610, Sec. 4.2.3(a)) gives {da[name]} ft"
                       + (" (matches)" if da[name] == height else "") if name in da else "")
            source = (f"illustrative: block outline traced from {fig59}; drawn to the maximum height in {fig512}"
                      + (f", limited to {limited} ft by Standard S5.6.3 (p. 181)" if limited else "")
                      + f" ({draft}){da_note}")
        props = {
            "kind": "block",
            "block": name,
            "label": "Blocks H5 and H6" if name == "H5/H6" else f"Block {name}",
            "stage": "entitled",
            "height_ft": height,
            "podium_ft": None,
            "base_ft": 0,
            "use": USE[name],
            "phase": None,
            "illustrative": True,
            "source": source,
        }
        if name == "H5/H6":
            props["note"] = ("Approximate boundary. Affordable housing sites with a lower height limit in the "
                             "approved design standards; the limit isn't available, so only the outline is drawn.")
        elif limited:
            props["note"] = (f"Height from the October 2020 draft design standards: {limited} ft to the top of "
                             f"the roof (S5.6.3), below the {t['fig_ft']}-ft limit around it. Needs checking "
                             "against the approved version.")
        elif name == "E1":
            # Where the two disagree, the newer approved document wins (Matthew, 2026-10-05).
            props["height_ft"] = da[name]
            props["source"] = (f"illustrative: block outline traced from {fig59}; height {da[name]} ft from the "
                               f"approved Development Agreement (Ord. 30610, June 2021, Sec. 4.2.3(a), {DA['url']}), "
                               f"which is newer than the {t['fig_ft']} ft in {fig512} ({draft})")
            props["note"] = (f"Height from the approved Development Agreement (June 2021), {da[name]} ft; the "
                             f"October 2020 draft design standards show {t['fig_ft']} ft, and the FAA contours "
                             "(Fig. 5.13) run about 260-280 ft across the block.")
        elif name in da:
            props["note"] = (f"Height from the October 2020 draft design standards; the approved Development "
                             f"Agreement gives the same {da[name]} ft.")
        else:
            props["note"] = ("Height from the October 2020 draft design standards; needs checking against the "
                             "approved version.")
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(geom))})
    share = outside / raw_area
    print(f"[downtown-west] {len(features)} blocks; {outside:.0f} m2 ({share:.1%}) fell outside the PD zoning "
          "and was trimmed")
    if share > 0.05:
        raise SystemExit("too much of the traced massing falls outside the PD zoning; check the georeference")
    print("[downtown-west] " + ", ".join(f"{f['properties']['block']}:{f['properties']['height_ft']}" for f in features))
    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    massing_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each new development block is drawn to its maximum height in the "
                "October 2020 draft of the Downtown West design standards (Fig. 5.12), from 180 ft at the north "
                "end to 290 ft at the south, not as a building design; four smaller blocks are held to "
                "40-150 ft. The version the City Council approved in May 2021 couldn't be retrieved. Where the "
                "approved Development Agreement gives heights (nine blocks), they match, except E1, drawn at the "
                "agreement's 260 ft rather than the draft's 280 ft because the agreement is newer. Blocks H5 and H6, added in the approved plan with lower "
                "limits that aren't available, are drawn as an outline only. The FAA's airspace limits govern "
                "the real heights. Streets, parks, the historic buildings being kept and the Creekside Walk "
                "buildings aren't drawn, and nothing has been built."
            ),
            "note": ("Heights are from the October 2020 draft design standards, drawn as limits, not building "
                     "designs; real buildings will be smaller."),
            "sourceUrl": DWDSG["url"],
            "sourceLabel": "Draft design standards, 2020 (PDF)",
            "georeference": {"figures_5_9_and_5_12": report,
                             "check_against_pd_zoning": {"blocks_m2": round(raw_area), "outside_m2": round(outside),
                                                         "outside_share": round(share, 4)}},
            "documents": {
                "design_standards": {"title": DWDSG["title"], "url": DWDSG["url"], "listing": DWDSG["listing"],
                                     "sha256": DWDSG["sha256"],
                                     "pages": "Fig. 3.3 p. 52, Fig. 5.9 p. 175, S5.6 and Figs. 5.11-5.13 pp. 179-182"},
                "development_agreement": {"title": DA["title"], "url": DA["url"], "sha256": DA["sha256"],
                                          "check": checks},
                "general_plan_resolution": {"title": GPA["title"], "url": GPA["url"], "sha256": GPA["sha256"],
                                            "page": GPA["page_index"] + 1,
                                            "finding": "Lower height limits on D5, D6, D8-13, F6, H1, H5 and H6 "
                                                       "under the approved DWDSG."},
                "needs_verification": ("The approved DWDSG (dated March 1, 2021, with errata; adopted with the PD "
                                       "Permit on May 25, 2021) is posted only on sanjoseca.gov, which refuses "
                                       "scripted downloads, and none of the Council item 10.2 attachments on "
                                       "Legistar (matter 9022) includes it or its errata list. Heights are from "
                                       "the October 2020 draft."),
            },
            "license": ("Block shapes: traced from a public City of San José document. Georeferenced to "
                        "OpenStreetMap building footprints (ODbL 1.0) via Overture Maps; trimmed to the City of "
                        "San José zoning layer (CC-BY 4.0, City of San José)."),
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(massing_fc), indent=1) + "\n")
    print(f"[downtown-west] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
