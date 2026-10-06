"""Potrero HOPE SF: block height limits from the adopted Design Standards and Guidelines, and the
buildings built so far.

Sources:
- Height limits: Potrero HOPE SF Design Standards and Guidelines (DSG), November 2016, adopted with
  the Special Use District and development agreement (the version SF Planning links as the project's
  design standards). Figure 5.1 "Zoning Height Diagram" (printed p. 67, PDF page 70), a raster
  map over an aerial photo: 40 ft or less (pale yellow), 50-60 ft (yellow) and 65 ft (orange), with
  each zone's limit printed in it (30', 40', 50', 55', 65'). Control 5.1.1 No. 1: "Maximum building
  heights are established in the Zoning Height Diagram." The printed limits are raster text, so they
  are transcribed below (ZONES), one point inside each zone; each zone is traced as the colour region
  around its point.
- Georeference: the figure's pink dashed "PROJECT BOUNDARY" is fitted (trimmed ICP) to the Potrero
  HOPE SF Special Use District boundary (DataSF 5yf5-ms5f, the site file), from a two-corner start.
- Built buildings: DBI permits (DataSF i98e-djp9) 202006108345 (Block B, 1801 25th St, 7 stories,
  157 homes, complete Dec 4, 2025) and 201603172392 (1101 Connecticut St, 5 stories, 72 homes,
  complete Oct 28, 2019). MOHCD's Apr 4, 2025 Phase III loan evaluation names "the 157 units at
  Block B" and Phase I "at 1101 Connecticut, a 72-unit" building; the Phase 2 approval (Oct 13, 2017)
  table lists Phase 1 as Block X with 72 units. Block X sits outside the Special Use District and the
  development agreement's Project Area (DA exhibit notes), but is the master plan's Phase 1.

What this is and isn't:
- Unbuilt blocks are drawn to their height limits, not as building designs, so they are illustrative.
- Neither built building has an official height in feet. 1101 Connecticut (5 stories) is drawn to its
  block's 50-ft limit. Block B (7 stories) is drawn to the DSG's 65-ft cap for Block B (Control 5.1.1
  No. 6: above the 50-ft limit on no more than 30% of the block, never over 65 ft), over a 50-ft base.
  The Phase 2 approval's table (Oct 2017) lists 40 ft for Block B; the newer permit (7 stories) shows
  it was built under the DSG's Block B exception, so that value is only noted.
- Where OpenStreetMap (via Overture) maps the built footprint it is drawn; otherwise the block's
  Figure 5.1 zone stands in, labelled.
- Section 5.2 caps parts of Blocks C, D, J, K and L at elevations above sea level (view protection),
  which aren't drawn. Nor are streets, parks and open space (unfilled in the figure), or the existing
  public housing to be demolished, which stays in the base map.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_potrero_hope_sf
"""

from __future__ import annotations

import json
import os
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
from shapely.geometry import Point, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "potrero-hope-sf"
TAG = "potrero"
UTM = tb.UTM
BBOX = (-122.4010, 37.7495, -122.3920, 37.7590)  # lon/lat window over the site
RAW = config.ROOT / "data" / "raw" / "massing"

DSG = {
    "title": "Potrero HOPE SF Design Standards and Guidelines (November 2016)",
    "url": "https://default.sfplanning.org/devagreements/HOPE-SF/Potrero/HOPE-SF_Potrero_Design_Controls_Guidelines.pdf",
    "file": "hope-potrero-dsg.pdf",
    "sha256": "a234d783826b4aa4304c732128ff1fcf5dd9d9ab17cd1668144d9f0efe54fcc1",
}
FIG = {"page_index": 69, "printed_page": "67", "figure": "Figure 5.1, Zoning Height Diagram"}
DPI = 200
FRAME = (150, 440, 1350, 1965)  # the map, in 200-dpi pixels (left, top, right, bottom)
LEGEND = (820, 1590, 1350, 1965)  # the legend box, skipped
BOUNDARY_LABEL = (300, 1800, 560, 1840)  # the "PROJECT BOUNDARY" caption, skipped

# Figure 5.1's zones: (block, a point inside the zone in 200-dpi pixels, the printed limit in feet).
# Transcribed from the figure; each point is beside the zone's printed height.
ZONES = [
    ("R", (945, 680), 40),
    ("Q and O", (880, 800), 55),
    (None, (995, 815), 40),  # no letter printed; beside Block O, east of Texas Street
    ("N", (880, 975), 55),
    ("P", (995, 965), 40),
    ("J", (410, 1072), 30),
    ("J", (410, 1115), 40),
    ("J", (410, 1180), 65),
    ("K", (565, 1100), 40),
    ("K", (565, 1180), 65),
    ("L", (690, 1100), 40),
    ("L", (745, 1100), 50),
    ("L", (720, 1180), 65),
    ("M", (875, 1150), 55),
    ("G", (580, 1300), 50),
    ("H", (875, 1300), 55),
    ("F", (438, 1341), 50),
    ("F", (430, 1440), 40),
    ("C", (570, 1460), 50),
    ("D", (730, 1460), 50),
    ("E", (880, 1460), 55),
    ("A", (410, 1680), 40),
    ("B", (565, 1660), 50),
    ("X", (720, 1620), 50),
]
# Legend classes as OpenCV HSV ranges (H 0-179): (h_min, h_max, s_min, s_max).
CLASSES = {30: (23, 31, 60, 125), 40: (23, 31, 60, 125), 50: (19, 27, 150, 235), 55: (19, 27, 150, 235), 65: (10, 19, 170, 255)}
RECT_SHARE = 0.84  # a traced zone this close to its minimum rectangle is drawn as the rectangle
CLOSE_PX = 7  # bridges the thin building outlines inside a zone
DARK_V = 80  # zone outlines and text
PINK = {"r_min": 170, "r_minus_g": 70, "b_minus_g": 25, "b_max": 190}  # the dashed project boundary
# Starting fit: the boundary's north-west corner (by Block J) and south-west corner (by Block A),
# in pixels, to the Special Use District's corners (UTM).
INIT = {"north-west corner": ((341, 1029), (552969, 4178774)), "south-west corner": ((345, 1793), (553002, 4178365))}
KEEP = 0.8

# Documents tying the permits to blocks; each quote is checked and its page recorded.
SUPPORT = {
    "mohcd": {"title": "MOHCD Loan Committee, Potrero HOPE SF Phase III predevelopment loan evaluation (Apr 4, 2025)",
              "url": "https://media.api.sf.gov/documents/Approved-Potrero_HOPE_SF_Phase_III_Predevelopment_Loan_"
                     "Evaluation_LC_4-04-2025.pdf",
              "file": "hope-potrero-phase3-loan-evaluation.pdf",
              "sha256": "eeb8b2e78179f9f1ba08d89772def0c5f154f0ea0c5c575f8d7659ae13739e5b",
              "quotes": ["Out of the 157 units at Block B", "at 1101 Connecticut, a 72-unit"]},
    "phase2": {"title": "SF Planning, Potrero HOPE SF Phase 2 approval (Oct 13, 2017)",
               "url": "https://sfplanning.s3.amazonaws.com/default/files/devagreements/HOPE-SF/Potrero/"
                      "HOPE-SF_Potrero_Phase2_Approval_20171013.pdf",
               "file": "hope-potrero-phase2-approval.pdf",
               "sha256": "f8489226852361e57d3c3101f397ed5e49506c6b91d8bbd1183d27d753a5c80d",
               "quotes": ["Potrero HOPE SF Vertical Development Summary Table",
                          "Temporary Certificate of Occupancy Received for Block X"]},
}
PERMIT_URL = "https://data.sf.gov/resource/i98e-djp9.json?permit_number={}"
BUILT = [
    {"block": "B", "label": "Block B, 1801 25th St", "permit": "202006108345", "use": "Affordable housing, 157 homes",
     "phase": "Phase 2", "height_ft": 65, "podium_ft": 50,
     "height_src": ("7 stories in DBI permit 202006108345; drawn to the DSG's Block B cap (Control 5.1.1 No. 6: "
                    "\"In no case is any portion of any building greater than 65-feet\") over its 50-ft limit, "
                    "since parts above 50 ft are limited to 30% of the block"),
     "via": "MOHCD's Phase III loan evaluation (Apr 2025): \"Out of the 157 units at Block B\"",
     "extra": " The Phase 2 approval's table (Oct 2017) listed 40 ft for Block B."},
    {"block": "X", "label": "Block X, 1101 Connecticut St", "permit": "201603172392", "use": "Affordable housing, 72 homes",
     "phase": "Phase 1", "height_ft": 50, "podium_ft": None,
     "height_src": "5 stories in DBI permit 201603172392; drawn to Block X's 50-ft limit in Figure 5.1",
     "via": ("MOHCD's Phase III loan evaluation: \"completed Phase I construction and lease-up at 1101 Connecticut, "
             "a 72-unit\" building; the Phase 2 approval lists Phase 1 as Block X, 72 units"),
     "extra": " Block X is outside the Special Use District and the development agreement's Project Area."},
]


def _overture_buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / f"hope-{TAG}-buildings.parquet"
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
        pq.write_table(d.to_table(columns=["id", "geometry", "height", "num_floors", "sources"], filter=f), cache)
    t = pq.read_table(cache)
    g = gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                         geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)),
                         crs=4326).to_crs(UTM)
    g["osm"] = g["sources"].apply(lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None))
    return g


def _permits() -> dict:
    cache = RAW / f"hope-{TAG}-dbi-permits.json"
    if not cache.exists():
        rows = []
        for b in BUILT:
            with urllib.request.urlopen(PERMIT_URL.format(b["permit"])) as r:
                rows += json.loads(r.read())
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(rows))
    out = {}
    for r in json.loads(cache.read_text()):
        out.setdefault(r["permit_number"], r)
    return out


def _check_support() -> dict[str, str]:
    """Each supporting document's quotes, with the PDF pages they are on."""
    import re

    out = {}
    for key, doc in SUPPORT.items():
        path = trace.fetch_document(doc["url"], tb.DOCS / doc["file"], doc["sha256"])
        pages = {}
        with pdfplumber.open(str(path)) as pdf:
            for i, page in enumerate(pdf.pages):
                t = re.sub(r"\s+", " ", page.extract_text() or "")
                for q in doc["quotes"]:
                    if q in t and q not in pages:
                        pages[q] = i + 1
        missing = [q for q in doc["quotes"] if q not in pages]
        if missing:
            raise SystemExit(f"{doc['title']} no longer says: {missing}")
        out[key] = f"{doc['title']}, {doc['url']} (" + "; ".join(f'\"{q}\", p. {n}' for q, n in pages.items()) + ")"
    return out


def _render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    with pdfplumber.open(str(pdf_path), pages=[FIG["page_index"] + 1]) as pdf:
        if "ZONING HEIGHT DIAGRAM - FIGURE 5.1" not in (pdf.pages[0].extract_text() or ""):
            raise SystemExit("Figure 5.1 is not on the expected DSG page")
    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    return np.asarray(page.render(scale=DPI / 72).to_pil().convert("RGB"))


def _inside(x, y, box) -> bool:
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


def _georeference(rgb: np.ndarray, site_utm) -> tuple[trace.Similarity, dict]:
    r, g, b = (rgb[..., i].astype(int) for i in range(3))
    mask = (r > PINK["r_min"]) & (r - g > PINK["r_minus_g"]) & (b - g > PINK["b_minus_g"]) & (b < PINK["b_max"])
    ys, xs = np.nonzero(mask)
    keep = [(x, y) for x, y in zip(xs, ys) if _inside(x, y, FRAME) and not _inside(x, y, LEGEND)
            and not _inside(x, y, BOUNDARY_LABEL)]
    pts = np.asarray(keep, float)
    init = trace.fit_similarity([a for a, _ in INIT.values()], [b for _, b in INIT.values()], list(INIT))
    sim, d = tb.icp(pts, [site_utm.boundary], np.zeros(len(pts), int), init, keep=KEEP)
    rep = tb.icp_report(sim, d, KEEP, "Figure 5.1's dashed project boundary to the Special Use District boundary")
    return sim, rep


def _class_components(hsv: np.ndarray, ft: int) -> np.ndarray:
    """Connected regions of one legend class. The class mask is closed (to bridge the thin building
    outlines drawn inside the zones), then cut along the figure's thick black zone outlines (dark
    strokes that survive a 3-px opening)."""
    h0, h1, s0, s1 = CLASSES[ft]
    m = ((hsv[..., 0] >= h0) & (hsv[..., 0] <= h1) & (hsv[..., 1] >= s0) & (hsv[..., 1] <= s1)
         & (hsv[..., 2] >= 90)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((CLOSE_PX, CLOSE_PX), np.uint8))
    dark = (hsv[..., 2] < DARK_V).astype(np.uint8)
    m[cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0] = 0
    return cv2.connectedComponents(m, connectivity=4)[1]


def _component_at(lab: np.ndarray, xy) -> int:
    x, y = xy
    win = lab[y - 15:y + 16, x - 15:x + 16]
    ids, counts = np.unique(win[win > 0], return_counts=True)
    if not len(ids):
        raise SystemExit(f"no zone colour near Figure 5.1 point {xy}")
    return int(ids[np.argmax(counts)])


def _polygon(mask: np.ndarray) -> Polygon:
    """The outline of a region, with the holes left by text filled. The zones are drawn as rectangles
    (except Q and O, and R): where the traced region fills most of its minimum rectangle, the rectangle
    is used, which drops the notches the red and blue dotted borders leave along some edges."""
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    poly = shapely.make_valid(Polygon(cv2.approxPolyDP(c, 1.5, True).reshape(-1, 2)))
    rect = shapely.minimum_rotated_rectangle(poly)
    return rect if poly.area / rect.area > RECT_SHARE else poly


def _trace_zones(hsv: np.ndarray) -> list[Polygon]:
    """Each ZONES entry's region. Where two entries fall in one region (Block J's 30-ft and 40-ft
    strips, divided by a thin line), the region is split at the darkest row between their points."""
    labs = {CLASSES[ft]: _class_components(hsv, ft) for ft in {ft for _, _, ft in ZONES}}
    keys = [(labs[CLASSES[ft]], _component_at(labs[CLASSES[ft]], xy)) for _, xy, ft in ZONES]
    out = []
    for i, (_, xy, ft) in enumerate(ZONES):
        lab, cid = keys[i]
        mask = lab == cid
        for j, (_, xy2, _) in enumerate(ZONES):
            if j != i and keys[j][0] is lab and keys[j][1] == cid:
                cols = np.nonzero(mask.any(axis=0))[0]
                y0, y1 = sorted((xy[1], xy2[1]))
                rows = range(y0 + 1, y1)
                darkness = [np.mean(hsv[r, cols, 2]) for r in rows]
                cut = rows[int(np.argmin(darkness))]
                print(f"[{TAG}]   split one region between points {xy} and {xy2} at row {cut}")
                if xy[1] < xy2[1]:
                    mask[cut:] = False
                else:
                    mask[:cut + 1] = False
        out.append(_polygon(mask))
    return out


def main() -> None:
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    pdf_path = trace.fetch_document(DSG["url"], tb.DOCS / DSG["file"], DSG["sha256"])
    rgb = _render(pdf_path)
    sim, georef = _georeference(rgb, site_utm)
    print(f"[{TAG}] Figure 5.1 → UTM: scale {sim.scale:.4f} m/px, rotation {np.degrees(sim.rotation):.2f}°, "
          f"trimmed RMS {sim.rms_m:.2f} m (median {georef['median_m']} m over {georef['points']} boundary pixels)")
    if sim.rms_m > 3:
        raise SystemExit("Figure 5.1 fit is poor")

    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(int)
    zones = []
    for (block, xy, ft), px in zip(ZONES, _trace_zones(hsv)):
        if px.area > 60000:
            raise SystemExit(f"Block {block} {ft}-ft zone leaked ({px.area:.0f} px²)")
        utm = shapely.make_valid(sim.geometry(px))
        share = utm.intersection(site_utm).area / utm.area
        zones.append({"block": block, "ft": ft, "px": px, "utm": utm, "in_site": share})
    # Zones of one colour that touch would trace as one region: check none was traced twice.
    for i, a in enumerate(zones):
        for b in zones[i + 1:]:
            if a["px"].intersection(b["px"]).area > 0.2 * min(a["px"].area, b["px"].area):
                raise SystemExit(f"Figure 5.1 zones {a['block']} {a['ft']} ft and {b['block']} {b['ft']} ft overlap")

    permits = _permits()
    support = _check_support()
    bldgs = _overture_buildings()
    fig = f"{DSG['title']}, {FIG['figure']}, p. {FIG['printed_page']}"
    features, cut = [], []
    for b in BUILT:
        r = permits[b["permit"]]
        if r["status"] != "complete":
            raise SystemExit(f"permit {b['permit']} is not complete")
        mine = [z for z in zones if z["block"] == b["block"]]
        area = shapely.union_all([z["utm"] for z in mine])
        cand = bldgs[bldgs.geometry.area > 300]
        cand = cand[[g.intersection(area.buffer(5)).area / g.area > 0.8 for g in cand.geometry]]
        cand = cand[[g.area / area.area > 0.3 for g in cand.geometry]]
        base = {"block": b["block"], "label": b["label"], "stage": "complete", "base_ft": 0,
                "height_ft": b["height_ft"], "podium_ft": b["podium_ft"], "use": b["use"], "phase": b["phase"],
                "illustrative": True}
        note = f"DBI permit {b['permit']}, complete {r['completed_date'][:10]}. Block: {b['via']}." + b["extra"]
        if len(cand):
            g = shapely.union_all(cand.geometry.to_numpy())
            rec = ", ".join(sorted(f"OSM {o}" if o else f"Overture {i}" for o, i in zip(cand["osm"], cand["id"])))
            props = {**base, "kind": "building",
                     "source": f"illustrative: footprint from OpenStreetMap via Overture {config.OVERTURE_RELEASE} ({rec}); {b['height_src']}",
                     "note": note}
            print(f"[{TAG}]   built: {b['label']}: OSM footprint {g.area:.0f} m², {b['height_ft']} ft")
        else:
            g = area
            props = {**base, "kind": "block",
                     "source": (f"illustrative: the block's zone in {fig}, standing in for the building's footprint, "
                                f"which OpenStreetMap doesn't map yet; {b['height_src']}"),
                     "note": note + " Drawn as its block: the building's own footprint isn't mapped yet."}
            print(f"[{TAG}]   built: {b['label']}: no OSM footprint; block zone {g.area:.0f} m², {b['height_ft']} ft")
        cut.append(g)
        features.append({"props": props, "geom": g})

    built = {b["block"] for b in BUILT}
    cut_u = shapely.union_all(cut).buffer(1.0)
    for z in zones:
        if z["block"] in built:
            continue
        if z["in_site"] < 0.8:
            raise SystemExit(f"Block {z['block']} {z['ft']}-ft zone lies outside the Special Use District")
        # Clipped to the Special Use District: blocks along its edge spill a few metres over it, within
        # the figure's fit error.
        g = z["utm"].intersection(site_utm).difference(cut_u)
        label = f"Block {z['block']}" if z["block"] else "Unlettered block beside Block O"
        restricted = z["block"] in ("C", "D", "J", "K", "L")
        note = (f"Height limit: {z['ft']} ft. Drawn as an envelope, not a building design."
                + (" Section 5.2 also caps parts of this block at an elevation above sea level, to keep views from "
                   "Potrero Recreation Center; that cap isn't drawn." if restricted else "")
                + ("" if z["block"] else " Figure 5.1 prints no letter here; Section 5.2.12 groups the east-side "
                   "walk-up blocks as P and R."))
        props = {"kind": "block", "label": label, "stage": "entitled", "height_ft": z["ft"], "podium_ft": None,
                 "base_ft": 0, "use": None, "phase": None, "illustrative": True,
                 "source": f"illustrative: drawn to the {z['ft']}-ft height limit printed in {fig}", "note": note}
        if z["block"]:
            props = {"block": z["block"], **props}
        features.append({"props": props, "geom": g})
        print(f"[{TAG}]   {label:>32}: {z['ft']:>3} ft, {g.area:6.0f} m² ({z['in_site']:.0%} in the SUD)")

    out = []
    for i, f in enumerate(features):
        g = shapely.make_valid(f["geom"].simplify(0.4))
        g = shapely.union_all([p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.area > 10])
        out.append({"type": "Feature", "properties": {**f["props"], "fid": i + 1},
                    "geometry": mapping(tb.to_wgs(trace.as_multipolygon(g)))})

    n = sum(f["properties"]["stage"] == "entitled" for f in out)
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing. The two buildings built so far are drawn from their permits: Block X "
                "(1101 Connecticut St, 72 homes, Phase 1), drawn at its block's 50-ft limit, and Block B (157 homes, "
                "Phase 2), drawn as its block at the 65-ft cap the standards allow on part of it. "
                f"The other {n} zones are drawn to the height limits of the adopted Design Standards "
                "and Guidelines (30 to 65 ft), not as building designs. The old public housing stays in the base "
                "map; streets and parks aren't drawn."
            ),
            "note": "Unbuilt blocks are drawn to their height limits, not as building designs.",
            "sourceUrl": DSG["url"],
            "sourceLabel": "Design standards and guidelines, 2016 (PDF)",
            "georeference": {"figure_5_1": {**georef, "units": "metres per 200-dpi pixel",
                                            "start": list(INIT)}},
            "sources": {
                "heights": f"{fig} (PDF page {FIG['page_index'] + 1}); DSG 5.1.1",
                "permits": "DataSF Building Permits (i98e-djp9): " + ", ".join(b["permit"] for b in BUILT),
                "blocks": support,
            },
            "license": ("Zones traced from the DSG (SF Planning); boundary and permits from DataSF (Public Domain); "
                        f"footprints {tb.OSM_LICENSE}."),
        },
        "features": out,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"[{TAG}] wrote {path.relative_to(config.ROOT)} ({len(out)} features, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
