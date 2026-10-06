"""Sunnydale HOPE SF: block height limits from the adopted Design Standards and Guidelines, and the
buildings built or under construction so far.

Sources:
- Height limits: Sunnydale HOPE SF Design Standards and Guidelines (DSG), approved Nov 17, 2016 by
  Planning Commission Motion 19790 and revised Sept 14, 2023 by Motion 21390 (the version SF Planning
  links on the project page). Figure 7.1 "Building Height Diagram" (printed p. 84, PDF page 86). Its
  zones are vector fills in the PDF, read directly: 40 ft (salmon), 50 ft (yellow), 60 ft (green).
  Section 7.1.1: "Where the number of stories is listed, the number of stories is the limitation,
  regardless of the height limit", so zones labelled "N STORIES" are capped at N stories.
- Block numbers and property lines: the same DSG, Figure 7.4 "Setback Diagram" (printed p. 88, PDF
  page 90), which draws the same plan with its block numbers and its setback lines along every block's
  property lines. Figure 7.1 is carried onto Figure 7.4 by a similarity fitted to four outer block
  corners of the plan (RMS under 1 pt, about 1.3 m).
- Georeference: Figure 7.4's property lines are fitted (trimmed ICP) to the Special Use District
  boundary (DataSF 5yf5-ms5f, the site file) and to SF's parcel map (DataSF acdm-wktn, ODC-PDDL)
  where the new blocks have been recorded (lots mapped since 2019, on the east side: Blocks 1, 3, 6,
  7, 8 and 9 and the new streets). Only the plan's outer edge and the blocks east of Block 14 are
  used: west of there the old lots and streets are still on the parcel map.
- Built and under-construction buildings: DBI building permits (DataSF i98e-djp9) for Parcel Q
  (1491 Sunnydale, 5 stories), Block 6 (242 Hahn, "290 Malosi", 5 stories), Blocks 3A and 3B (1501
  Sunnydale, 5 stories each), the community center (1500 Sunnydale, 2 stories), all complete, and
  Block 9 (1652 Sunnydale) and Block 7 (89 homes), under construction. Block numbers of the permits
  come from the permits themselves (3A, 3B) or from MOHCD's Jan 24, 2025 Block 9 loan evaluation,
  which names Casala (Parcel Q), 290 Malosi, 3A, 3B, B9 and B7 (89 units, "a 5-story, 89-unit" project).

What this is and isn't:
- Unbuilt blocks are drawn to their height limits, not as building designs, so they are illustrative.
- Where OpenStreetMap (via Overture) maps a new building's footprint (Parcel Q and Block 6), that
  footprint is drawn. The other new buildings aren't in OpenStreetMap yet (it still shows the old
  public housing there), so their blocks' Figure 7.1 zones stand in for the footprint, labelled.
- No building has an official height in feet, so heights are estimated from the permitted stories
  at 12.5 ft a story (DSG 7.1.1: the 50-ft limit "is intended to allow four story buildings"),
  capped at the block's height limit; these are illustrative too.
- The existing public housing to be demolished stays in the base map and isn't drawn. Streets, parks
  and open space aren't drawn (Figure 7.1 leaves them unfilled).

    uv run --directory pipeline python -m bam_pipeline.sites.massing_sunnydale_hope_sf
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
from shapely.geometry import LineString, Point, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "sunnydale-hope-sf"
TAG = "sunnydale"
UTM = tb.UTM
BBOX = (-122.4260, 37.7080, -122.4130, 37.7160)  # lon/lat window over the site
RAW = config.ROOT / "data" / "raw" / "massing"

DSG = {
    "title": "Sunnydale HOPE SF Design Standards and Guidelines (approved 2016, revised Sept 14, 2023)",
    "url": "https://sfplanning.s3.amazonaws.com/default/files/devagreements/HOPE-SF/Sunnydale/"
           "HOPE-SF_Sunnydale_Design_Controls_Guidelines.pdf",
    "file": "hope-sunnydale-dsg.pdf",
    "sha256": "7384dd4d0d026a8e82e285aad9316decf436fa81c21c3e4d0534bb5b41a7c1e4",
}
FIG71 = {"page_index": 85, "printed_page": "84", "figure": "Figure 7.1, Building Height Diagram"}
FIG74 = {"page_index": 89, "printed_page": "88", "figure": "Figure 7.4, Setback Diagram"}
MOHCD = {
    "title": "MOHCD Loan Committee, Sunnydale HOPE SF Block 9 loan evaluation (Jan 24, 2025)",
    "url": "https://media.api.sf.gov/documents/Approved_Sunnydale_Block_9_Loan_Evaluation_-_LC_1-24-25.pdf",
    "file": "hope-sunnydale-block9-loan-evaluation.pdf",
    "sha256": "c59d7dbe4ecbe9536bfecc8beeb8d6f724001e884cc52ce1c361a73585b86862",
}

# Figure 7.1 fills (PDF colours) -> height limit in feet. The legend swatches sit right of LEGEND_X
# and below LEGEND_TOP (PDF points) and are skipped.
FILLS = {40: (0.053, 0.35, 0.35, 0.0), 50: (0.998, 0.88, 0.525), 60: (0.5,)}
LEGEND_X, LEGEND_TOP = 465, 250
FT_PER_STORY = 12.5  # DSG 7.1.1: "A 50' height limit at select locations is intended to allow four story buildings"

# Figure 7.4 -> Figure 7.1: block corners on the shared base plan (PDF points), outer corners of the
# plan's frame of blocks: Block 13 top-left, Block 1 top-right, Block 35 bottom-left, Block 8a
# bottom-right. Figure 7.4's corners are where its setback lines meet; Figure 7.1's are its fills.
FIG74_TO_71 = {
    "Block 13, top-left": ((57.6, 84.0), (87.6, 98.6)),
    "Block 1, top-right": ((474.4, 84.0), (460.1, 95.9)),
    "Block 35, bottom-left": ((112.4, 352.4), (137.4, 337.7)),
    "Block 8a, bottom-right": ((446.5, 355.5), (437.2, 341.1)),
}

# The one zone too far from any block number to name by distance: the "1 STORIES" zone sits in the
# middle of Block 4 (Figure 7.4), which MOHCD's Block 9 evaluation calls "Block 2 and 4 open space".
UNLABELLED = {1: "4"}

# Figure 7.4's property lines used for the fit: its coloured setback lines (the label circles and
# leader lines excluded), on the plan's outer edge (the rear-yard colours) or east of FIT_X (PDF points).
SKIP_STROKES = {(0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0), (0.0,), (1.0,), (1.0, 1.0, 1.0), (0.5, 0.5, 0.5),
                (0.15, 0.14, 0.14)}
EDGE_STROKES = {(0.15, 0.25, 0.83), (0.53, 0.28, 0.62)}  # "10' minimum at rear yard", "15' minimum at rear yard"
FIT_X = 340
FIG74_BOTTOM, FIG74_RIGHT = 370, 500  # the plan is above and left of these (legend and notes beyond)
# Starting fit: rough centres of Blocks 9 and 1 in Figure 7.4 (PDF points) to their recorded lots.
INIT = {"Block 9": ((310.0, 105.0), "6310008"), "Block 1": ((430.0, 105.0), "6310003")}
KEEP = 0.8
SF_PARCELS = "https://data.sf.gov/resource/acdm-wktn.geojson"

# DBI permits (DataSF i98e-djp9) for the new buildings, with the plan block each one is.
PERMIT_URL = "https://data.sf.gov/resource/i98e-djp9.json?permit_number={}"
BUILT = [
    {"block": "Q", "label": "Parcel Q, 1491 Sunnydale Ave (Casala)", "permits": ["201612225710"],
     "use": "Affordable housing, 55 homes", "phase": None,
     "via": "MOHCD's Block 9 loan evaluation lists Casala (55 units)", "quote": "Casala (55)"},
    {"block": "6", "label": "Block 6, 242 Hahn St (290 Malosi)", "permits": ["201806202372"],
     "use": "Affordable housing, 167 homes", "phase": None,
     "via": "MOHCD's Block 9 loan evaluation lists 290 Malosi (167 units); Figure 7.4 numbers it 6a and 6b",
     "quote": "290 Mal. (167)"},
    {"block": "1", "label": "Block 1, community center, 1500 Sunnydale Ave", "permits": ["202107124132"],
     "use": "Community center with childcare", "phase": None,
     "via": "the permit's 2 stories matches Figure 7.1's \"2 STORIES\" on Block 1, the only 2-story block on the street"},
    {"block": "3", "label": "Blocks 3A and 3B, 1501 Sunnydale Ave", "permits": ["202106031523", "202106031549"],
     "use": "Affordable housing, 170 homes (80 and 90), with retail and childcare", "phase": None,
     "via": "the permits name \"sunnydale block 3a\" and \"sunnydale block 3b\"; Figure 7.1 draws Block 3 as one zone"},
    {"block": "9", "label": "Block 9, 1652 Sunnydale Ave", "permits": ["202211146447"],
     "use": "Affordable housing, 95 homes", "phase": None,
     "via": "MOHCD's Block 9 loan evaluation gives 1652 Sunnydale Avenue as Block 9's address",
     "quote": "1652 Sunnydale Avenue"},
    {"block": "7", "label": "Block 7", "permits": ["202211297323"],
     "use": "Affordable housing, 89 homes", "phase": None,
     "via": "MOHCD's Block 9 loan evaluation describes Block 7 as \"a 5-story, 89-unit\" project starting "
            "construction in mid-2025, matching this 89-unit, 5-story permit", "quote": "a 5-story, 89-unit"},
]
# The MOHCD evaluation (Jan 2025) gives Block 9 as "a total of 5 stories, 4-story wood over 1-story
# concrete podium"; DBI's permit (issued Aug 2024) says 4 stories. The newer document is used.
NEWER_STORIES = {"9": (5, "MOHCD's Jan 2025 loan evaluation: \"a total of 5 stories, 4-story wood over 1-story "
                          "concrete podium\" (DBI's permit, issued Aug 2024, says 4 stories)")}
MOHCD_QUOTES = ["a total of 5 stories, 4-story wood over 1-story", "B7 (89)", "Casala (55)", "290 Mal. (167)",
                "1652 Sunnydale Avenue", "a 5-story, 89-unit"]


# ---------------------------------------------------------------- data

def _overture_buildings() -> gpd.GeoDataFrame:
    """Overture buildings over the site, with their heights and source records."""
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


def _parcels() -> gpd.GeoDataFrame:
    """Active DataSF parcels over the site."""
    cache = RAW / f"hope-{TAG}-parcels.geojson"
    if not cache.exists():
        xmin, ymin, xmax, ymax = BBOX
        q = urllib.parse.urlencode({"$where": f"active = true AND within_box(shape, {ymax}, {xmin}, {ymin}, {xmax})",
                                    "$limit": 5000})
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(f"{SF_PARCELS}?{q}") as r:
            cache.write_bytes(r.read())
    return gpd.read_file(cache).to_crs(UTM).set_index("blklot")


def _permits() -> dict:
    cache = RAW / f"hope-{TAG}-dbi-permits.json"
    if not cache.exists():
        rows = []
        for b in BUILT:
            for n in b["permits"]:
                with urllib.request.urlopen(PERMIT_URL.format(n)) as r:
                    rows += json.loads(r.read())
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(rows))
    out = {}
    for r in json.loads(cache.read_text()):
        out.setdefault(r["permit_number"], r)
    return out


def _check_mohcd() -> dict:
    """The MOHCD evaluation's statements used above, with the PDF page each is on."""
    path = trace.fetch_document(MOHCD["url"], tb.DOCS / MOHCD["file"], MOHCD["sha256"])
    pages = {}
    with pdfplumber.open(str(path)) as pdf:
        for i, page in enumerate(pdf.pages):
            t = re.sub(r"\s+", " ", page.extract_text() or "")
            for q in MOHCD_QUOTES:
                if q in t and q not in pages:
                    pages[q] = i + 1
    missing = [q for q in MOHCD_QUOTES if q not in pages]
    if missing:
        raise SystemExit(f"MOHCD evaluation no longer says: {missing}")
    return pages


# ---------------------------------------------------------------- figure

def _colour(c):
    return (c,) if isinstance(c, (int, float)) else tuple(c) if c is not None else None


def _zones(pdf_path) -> list[dict]:
    """Figure 7.1's height zones (vector fills) and its "N STORIES" labels, in PDF points."""
    with pdfplumber.open(str(pdf_path), pages=[FIG71["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        if "Diagram (Figure 7.1) above" not in re.sub(r"\s+", " ", page.extract_text() or ""):
            raise SystemExit("Figure 7.1 is not on the expected DSG page")
        zones = []
        for o in page.curves + page.rects:
            c = _colour(o.get("non_stroking_color"))
            if not o.get("fill") or c is None or (o["x0"] > LEGEND_X and o["top"] > LEGEND_TOP):
                continue
            ft = next((h for h, k in FILLS.items() if len(k) == len(c) and max(abs(a - b) for a, b in zip(c, k)) < 0.01), None)
            if ft is None:
                continue
            pts = o.get("pts") or [(o["x0"], o["top"]), (o["x1"], o["top"]), (o["x1"], o["bottom"]), (o["x0"], o["bottom"])]
            zones.append({"ft": ft, "fig": shapely.make_valid(Polygon(pts))})
        words = page.extract_words()
    stories = []
    for a, b in zip(words, words[1:]):
        if b["text"] == "STORIES" and a["text"].isdigit() and abs(a["top"] - b["top"]) < 1:
            stories.append((int(a["text"]), Point((a["x0"] + b["x1"]) / 2, (a["top"] + b["bottom"]) / 2)))
    for n, p in stories:
        d, z = min(((z["fig"].distance(p), z) for z in zones), key=lambda t: t[0])
        if d > 3:
            raise SystemExit(f"\"{n} STORIES\" label at {p} is in no Figure 7.1 zone")
        if z.get("stories"):
            raise SystemExit("two story labels in one Figure 7.1 zone")
        z["stories"] = n
    return zones, len(stories)


def _block_labels(pdf_path) -> dict[str, Point]:
    """Figure 7.4's block numbers, carried into Figure 7.1's PDF points."""
    with pdfplumber.open(str(pdf_path), pages=[FIG74["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        if "Setback Diagram (Figure 7.4)" not in (page.extract_text() or ""):
            raise SystemExit("Figure 7.4 is not on the expected DSG page")
        words = [w for w in page.extract_words() if w["top"] < 370 and w["x1"] < 500]
    src = [a for a, _ in FIG74_TO_71.values()]
    dst = [b for _, b in FIG74_TO_71.values()]
    # A similarity in figure space: flip y on both sides so trace.fit_similarity's y-down convention cancels.
    sim = trace.fit_similarity(src, [(x, -y) for x, y in dst], list(FIG74_TO_71))
    out = {}
    for w in words:
        t = w["text"]
        if re.fullmatch(r"\d{1,2}[ab]?|Q", t):
            x, y = sim.apply([((w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2)])[0]
            out.setdefault(t, Point(x, -y))
    return out, sim


def _name_blocks(zones: list[dict], labels: dict[str, Point]) -> None:
    """Each zone takes the block label inside it. A zone with none takes the block of a labelled zone
    it touches (the 3-story strips along Block 6's east side), else the nearest label within 20 pt."""
    for z in zones:
        inside = sorted(k for k, p in labels.items() if z["fig"].buffer(2).contains(p))
        if len(inside) > 1 and len({k.rstrip("ab") for k in inside}) == 1:
            z["merged"] = [k.upper() for k in inside]  # one zone over sub-blocks of one block (3a and 3b)
            inside = [inside[0].rstrip("ab")]
        if len(inside) > 1:
            raise SystemExit(f"Figure 7.1 zone at {z['fig'].centroid} holds blocks {inside}")
        if inside:
            z["block"] = inside[0]
    for z in zones:
        if "block" in z:
            continue
        touching = {o["block"] for o in zones if "block" in o and o["fig"].distance(z["fig"]) < 1}
        if len(touching) == 1:
            z["block"] = touching.pop()
        elif z.get("stories") in UNLABELLED:
            z["block"] = UNLABELLED[z["stories"]]
        else:
            d, k = min(((z["fig"].distance(p), k) for k, p in labels.items()), key=lambda t: t[0])
            if d > 20:
                raise SystemExit(f"no Figure 7.4 block near the Figure 7.1 zone at {z['fig'].centroid}")
            z["block"] = k


def _fig74_lines(pdf_path) -> np.ndarray:
    """Points every 1 pt along Figure 7.4's property lines used for the fit."""
    with pdfplumber.open(str(pdf_path), pages=[FIG74["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        objs = page.curves + page.lines + page.rects
    pts = []
    for o in objs:
        c = _colour(o.get("stroking_color")) if o.get("stroke") else None
        if c is None or o["top"] > FIG74_BOTTOM or o["x1"] > FIG74_RIGHT:
            continue
        c = tuple(round(v, 2) for v in c)
        if c in SKIP_STROKES or len(o["pts"]) < 2:
            continue
        line = LineString(o["pts"])
        n = max(int(line.length), 2)
        for i in range(n + 1):
            x, y = line.interpolate(i / n, normalized=True).coords[0]
            if x >= FIT_X or c in EDGE_STROKES:
                pts.append((x, y))
    return np.asarray(pts)


def _georeference(pdf_path, parcels: gpd.GeoDataFrame, site_utm) -> tuple[trace.Similarity, dict]:
    """Figure 7.4 (PDF points) -> UTM: trimmed ICP of its property lines onto the SUD boundary and the
    parcel lines recorded since 2019."""
    new = parcels[(parcels["date_map_add"] >= "2019-01-01")]
    new = new[new.geometry.representative_point().within(site_utm.buffer(5))]
    target = shapely.union_all([site_utm.boundary] + [g.boundary for g in new.geometry])
    init = trace.fit_similarity([xy for xy, _ in INIT.values()],
                                [parcels.geometry[k].centroid.coords[0] for _, k in INIT.values()], list(INIT))
    pts = _fig74_lines(pdf_path)
    sim, d = tb.icp(pts, [target], np.zeros(len(pts), int), init, keep=KEEP)
    rep = tb.icp_report(sim, d, KEEP, "Figure 7.4 property lines to the SUD boundary and DataSF parcel lines")
    rep["target"] = (f"Special Use District boundary and the lines of {len(new)} DataSF parcels mapped since 2019 "
                     f"({', '.join(sorted(new.index))})")
    return sim, rep


# ---------------------------------------------------------------- main

def main() -> None:
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    pdf_path = trace.fetch_document(DSG["url"], tb.DOCS / DSG["file"], DSG["sha256"])
    zones, n_story_labels = _zones(pdf_path)
    labels, sim74 = _block_labels(pdf_path)
    _name_blocks(zones, labels)
    counts = ", ".join(f"{h} ft ×{sum(z['ft'] == h for z in zones)}" for h in FILLS)
    print(f"[{TAG}] Figure 7.1: {len(zones)} zones ({counts}), "
          f"{n_story_labels} story labels; Figure 7.4 → 7.1 fit RMS {sim74.rms_m:.1f} pt over 4 corners")

    parcels = _parcels()
    sim, georef = _georeference(pdf_path, parcels, site_utm)
    print(f"[{TAG}] Figure 7.4 → UTM: scale {sim.scale:.4f} m/pt, rotation {np.degrees(sim.rotation):.2f}°, "
          f"trimmed RMS {sim.rms_m:.2f} m (median {georef['median_m']} m over {georef['points']} points)")
    if sim.rms_m > 2.5:
        raise SystemExit("Figure 7.4 fit is poor")
    # Figure 7.1 -> Figure 7.4 (the inverse of the corner fit, in y-down figure points) -> UTM.
    to74 = trace.fit_similarity([b for _, b in FIG74_TO_71.values()], [(x, -y) for (x, y), _ in FIG74_TO_71.values()])

    def fig71_to_utm(g):
        return sim.geometry(shapely.transform(g, lambda xy: to74.apply(xy) * [1, -1]))

    for z in zones:
        z["utm"] = shapely.make_valid(fig71_to_utm(z["fig"]))
        if z["utm"].intersection(site_utm.buffer(3)).area / z["utm"].area < 0.95:
            raise SystemExit(f"Block {z['block']} zone falls outside the Special Use District")

    permits = _permits()
    mohcd_pages = _check_mohcd()
    bldgs = _overture_buildings()

    fig = f"{DSG['title']}, {FIG71['figure']}, p. {FIG71['printed_page']}"
    features = []
    built_cut = []
    built_blocks = {}
    for b in BUILT:
        rows = [permits[n] for n in b["permits"]]
        nums = " and ".join(b["permits"])
        if len({r["number_of_proposed_stories"] for r in rows}) != 1:
            raise SystemExit(f"permits {nums} differ in stories")
        stories = int(rows[0]["number_of_proposed_stories"])
        story_src = f"{stories} stories in DBI permit{'s' if len(rows) > 1 else ''} {nums}"
        if b["block"] in NEWER_STORIES:
            stories, story_src = NEWER_STORIES[b["block"]]
        complete = all(r["status"] == "complete" for r in rows)
        started = all(r.get("first_construction_document_date") for r in rows)
        if not (complete or started):
            raise SystemExit(f"permit {nums} shows no construction")
        r = max(rows, key=lambda r: r.get("completed_date") or r["first_construction_document_date"])
        stage = "complete" if complete else "construction"
        when = (f"complete {r['completed_date'][:10]}" if complete
                else f"first construction document {r['first_construction_document_date'][:10]}")
        mine = [z for z in zones if z["block"] == b["block"] or z["block"].rstrip("ab") == b["block"]]
        if not mine:
            raise SystemExit(f"no Figure 7.1 zone for Block {b['block']}")
        area = shapely.union_all([z["utm"] for z in mine])
        limit = max(z["ft"] for z in mine)
        height = min(round(stories * FT_PER_STORY), limit)
        height_src = (f"height estimated from {story_src} at {FT_PER_STORY} ft a story (DSG 7.1.1)"
                      + (f", capped at the block's {limit}-ft limit" if stories * FT_PER_STORY > limit else ""))
        # The footprint: an OpenStreetMap building over most of the block, if there is one.
        cand = bldgs[bldgs.geometry.area > 400]
        cand = cand[[g.intersection(area.buffer(4)).area / g.area > 0.8 for g in cand.geometry]]
        cand = cand[[g.area / area.area > 0.3 for g in cand.geometry]]
        base = {"block": b["block"], "label": b["label"],
                "stage": stage, "base_ft": 0, "podium_ft": None, "use": b["use"], "phase": b["phase"]}
        note = (f"DBI permit{'s' if len(rows) > 1 else ''} {nums}, {when}. Block: {b['via']}"
                + (f" (p. {mohcd_pages[b['quote']]})" if b.get("quote") else "") + ".")
        if len(cand):
            g = shapely.union_all(cand.geometry.to_numpy())
            rec = ", ".join(sorted(f"OSM {o}" if o else f"Overture {i}" for o, i in zip(cand["osm"], cand["id"])))
            mapped = [h for h in cand["height"] if h == h and h]
            props = {**base, "kind": "building", "height_ft": height, "illustrative": True,
                     "source": (f"illustrative: footprint from OpenStreetMap via Overture {config.OVERTURE_RELEASE} "
                                f"({rec}); {height_src}"),
                     "note": note + (f" OpenStreetMap maps it {max(mapped):.0f} m tall." if mapped else "")}
            print(f"[{TAG}]   built: {b['label']}: OSM footprint {g.area:.0f} m², {stories} stories → {height} ft ({stage})")
        else:
            g = area
            props = {**base, "kind": "block", "height_ft": height, "illustrative": True,
                     "source": (f"illustrative: the block's zone in {fig}, standing in for the building's footprint, "
                                f"which OpenStreetMap doesn't map yet; {height_src}"),
                     "note": note + " Drawn as its block: the building's own footprint isn't mapped yet."}
            print(f"[{TAG}]   built: {b['label']}: no OSM footprint; block zone {g.area:.0f} m², "
                  f"{stories} stories → {height} ft ({stage})")
        built_blocks.setdefault(b["block"].rstrip("ab"), []).append(b["block"])
        built_cut.append(g)
        features.append({"props": props, "geom": g})

    # Unbuilt blocks: Figure 7.1's zones at their height limits (story-limited ones capped).
    built_keys = {k for v in built_blocks.values() for k in v} | set(built_blocks)
    cut = shapely.union_all(built_cut).buffer(1.0)
    for z in sorted(zones, key=lambda z: (int(re.match(r"\d+", z["block"]).group(0)) if z["block"][0].isdigit() else 99, z["block"])):
        if z["block"] in built_keys or z["block"].rstrip("ab") in built_keys:
            continue
        g = z["utm"].difference(cut)
        if g.area < 20:
            continue
        h, n = z["ft"], z.get("stories")
        height = min(h, round(n * FT_PER_STORY)) if n else h
        src = f"illustrative: drawn to the {h}-ft height limit in {fig}"
        if n:
            src = (f"illustrative: {fig} limits this zone to {n} {'story' if n == 1 else 'stories'} within a {h}-ft "
                   f"height limit; drawn at {height} ft ({n} × {FT_PER_STORY} ft a story, DSG 7.1.1)"
                   if height < h else f"illustrative: drawn to the {h}-ft height limit ({n} stories) in {fig}")
        name = z["block"].upper() if re.fullmatch(r"\d+[ab]", z["block"]) else z["block"]
        label = f"Blocks {' and '.join(z['merged'])}" if z.get("merged") else f"Block {name}"
        props = {"kind": "block", "block": name, "label": label, "stage": "entitled",
                 "height_ft": height, "podium_ft": None, "base_ft": 0, "use": None, "phase": None,
                 "illustrative": True, "source": src,
                 "note": (f"Height limit: {h} ft" + (f", and no more than {n} {'story' if n == 1 else 'stories'}" if n else "")
                          + ". Drawn as an envelope, not a building design.")}
        features.append({"props": props, "geom": g})

    out = []
    for i, f in enumerate(features):
        g = shapely.make_valid(f["geom"].simplify(0.4))
        g = shapely.union_all([p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.area > 10])
        out.append({"type": "Feature", "properties": {**f["props"], "fid": i + 1},
                    "geometry": mapping(tb.to_wgs(trace.as_multipolygon(g)))})
        p = f["props"]
        if p["stage"] == "entitled":
            print(f"[{TAG}]   {p['label']:>10}: {p['height_ft']:>3} ft, {g.area:6.0f} m²")

    n_entitled = sum(f["properties"]["stage"] == "entitled" for f in out)
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing. The new buildings are drawn from their building permits: Parcel Q, Block 6, "
                "Blocks 3A and 3B and the community center are built, and Blocks 7 and 9 are under construction; "
                "Parcel Q's and Block 6's footprints are mapped, the others are drawn as their blocks, and every "
                "height is estimated from the permitted stories. The other "
                f"{n_entitled} zones are drawn to the height limits of the adopted Design Standards and Guidelines "
                "(40, 50 and 60 ft, and fewer stories where the plan says so), not as building designs. The old "
                "public housing stays in the base map; streets and parks aren't drawn."
            ),
            "note": "Unbuilt blocks are drawn to their height limits, not as building designs.",
            "sourceUrl": DSG["url"],
            "sourceLabel": "Design standards and guidelines, 2023 (PDF)",
            "georeference": {
                "figure_7_4": {**georef, "units": "metres per PDF point",
                               "lines": "coloured setback lines on the plan's outer edge and east of Block 14"},
                "figure_7_1_to_7_4": {**sim74.report(), "units": "PDF points",
                                      "use": "carries Figure 7.1's zones onto Figure 7.4 and its block numbers back"},
            },
            "sources": {
                "heights": f"{fig} (PDF page {FIG71['page_index'] + 1}); DSG 7.1.1",
                "blocks": f"{DSG['title']}, {FIG74['figure']}, p. {FIG74['printed_page']}",
                "fit": ("DataSF Parcels – Active and Retired (acdm-wktn) and the Special Use District boundary "
                        "(DataSF 5yf5-ms5f, data/boundaries)"),
                "permits": "DataSF Building Permits (i98e-djp9): " + ", ".join(n for b in BUILT for n in b["permits"]),
                "mohcd": f"{MOHCD['title']}, {MOHCD['url']} (pp. {', '.join(str(v) for v in sorted(set(mohcd_pages.values())))})",
            },
            "license": ("Zones traced from the DSG (SF Planning); parcels and permits from DataSF (ODC-PDDL / Public "
                        f"Domain); footprints {tb.OSM_LICENSE}."),
        },
        "features": out,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"[{TAG}] wrote {path.relative_to(config.ROOT)} ({len(out)} features, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
