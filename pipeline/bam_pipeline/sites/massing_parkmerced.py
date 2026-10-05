"""Parkmerced: height limits from the zoning map, checked against the adopted Design Standards and
Guidelines' Maximum Height Plan.

Sources:
- Height limits: DataSF "Zoning Map – Height and Bulk Districts" (h9wh-cg3m, Public Domain U.S.
  Government), the "-PM" districts adopted with the Parkmerced approvals in 2011 (zoning map
  amendments, Ordinance 91-11). The layer is drawn block by block, with most streets left out:
  "45-PM" and "65-PM" are the low-rise neighborhood fabric; "85-PM" to "145-PM" are the mid-rise
  and tower buildable envelopes; "130-PM" holds the 11 existing towers that stay; "40-OS-PM" is
  open space.
- Height check and block numbers: Parkmerced Design Standards and Guidelines (DSG), the version SF
  Planning links as adopted ("Revised 09-16-14"), Figure 03.03.C "Maximum Height Plan" (printed
  p. 103, PDF page 103; the page still carries the 06.23.11 date of the original). Standard
  03.03.01: "The height of structures shall not exceed the applicable maximum height as shown on the
  Maximum Height Plan (Fig. 03.03.C)." The figure's 61 height labels are matched to the zoning
  districts of the same height and a similarity is fitted to them (RMS about 6 m, mostly where the
  labels sit inside their boxes). Every label then falls in a zoning district of its height, and
  32 of 33 drawn fabric zones have the figure's fill for their height (the odd one: a 609 m² corner
  of Block 20 is 45 ft in the zoning map and 65 ft in the figure; the zoning map is drawn).
- Why the zoning layer and not a trace of Figure 03.03.C: they are the same plan (the check above),
  the zoning map is the legal height control, and the layer is surveyed GIS without a page figure's
  fit error. So the layer gives the shapes and the DSG gives the check and the block numbers.

What this is and isn't:
- Every zone is drawn to its height limit, not as a building design, so the massing is labelled
  illustrative. The DSG says the height zones "describe the three-dimensional maximum height
  envelopes without defining specific locations, numbers or shapes of buildings or parcels", and
  that mid-rise envelopes "locate areas where taller buildings than the neighborhood fabric height
  limit are allowed". So envelopes are drawn as their height over the fabric limit around them
  (podium_ft). The Regulating Plan (DSG Appendix A) also caps the footprint at each height per
  block; that isn't drawn.
- Blocks are numbered as in the Regulating Plan (01 to 23). The zoning map joins some sub-blocks
  the figure splits (02W and 02E, 16NW and 16NE), so sub-block letters aren't used.
- The 130-ft districts are the 11 existing towers that stay (about 1,683 homes); the base map
  already draws them, so those districts aren't drawn, and the towers' footprints are cut out
  where they reach a few metres past them. Open space ("40-OS-PM") isn't drawn. Nor are the zoning
  pieces that are streets in the plan: thin strips (medians, the Lake Merced Boulevard edge, the Muni
  corridor), roundabouts, and fabric pieces the figure shows as street (no fill).
- Built buildings: none. DBI permits for new buildings in the Special Use District are filed or
  approved only, except 199 Vidal Drive (64 homes, permit 201511132572, issued 2018-10-29), for
  which DBI records no construction. So no new building footprint is drawn.
- The DSG's finer limits (35-ft buildings on narrow streets, rooftop allowances, step-backs) aren't
  drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_parkmerced
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
from shapely.geometry import Point, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "parkmerced"
UTM = tb.UTM
BBOX = (-122.4880, 37.7110, -122.4710, 37.7240)  # lon/lat window over the site
RAW = config.ROOT / "data" / "raw" / "massing"

HEIGHTS = {
    "title": "DataSF Zoning Map – Height and Bulk Districts",
    "landing": "https://data.sf.gov/d/h9wh-cg3m",
    "url": "https://data.sf.gov/resource/h9wh-cg3m.geojson?" + urllib.parse.urlencode({
        "$where": "height like '%-PM%'",
        "$limit": 5000,
    }),
    "cache": RAW / "pm-height-bulk.geojson",
}
DSG = {
    "title": "Parkmerced Design Standards and Guidelines (revised 09-16-14)",
    "url": "https://default.sfplanning.org/publications_reports/parkmerced/"
           "Parkmerced_Final_Design_Standards_and_Guidelines_Revised-09-16-14.pdf",
    "file": "pm-dsg-2014.pdf",
    "sha256": "48ae9412c168ac65d20d0851a0448e551117bd8b05ca51316d33945405df8a8a",
}
FIG = {"page_index": 102, "printed_page": "103", "figure": "Figure 03.03.C, Maximum Height Plan"}
STANDARD = "Standard 03.03.01"
DPI = 200
MAP_BOTTOM_PT = 560  # the map frame is above this (footer below)
LEGEND_X_PT = 640  # the legend is right of this and above LEGEND_BOTTOM_PT
LEGEND_BOTTOM_PT = 130

# Starting fit: four height labels in Figure 03.03.C (PDF points) and a point inside the zoning
# district of the same height (UTM). The fit is then refined on every matched label.
INIT = {
    "85 ft, Block 01": ((160.6, 99.1), (545530, 4174980)),
    "115 ft, Block 18": ((535.5, 170.5), (546249, 4174804)),
    "85 ft, Block 04": ((160.1, 397.0), (545511, 4174415)),
    "145 ft, Block 22": ((684.9, 520.5), (546507, 4174160)),
}
LABEL_TOL_M = 10  # a label counts as in a zone within this distance (labels sit off-centre; fit RMS ~6 m)
FILL_OPACITY = 0.71  # the map's fills are the legend colours at about 71% over white (measured)
TOWER_FT = 130  # "130-PM": the existing towers, which stay
OPEN_SPACE = "40-OS-PM"
FABRIC = (45, 65)
FILL_CMYK = {45: (0.0, 0.051, 0.149, 0.0), 65: (0.0, 0.161, 0.443, 0.0), "open space": (0.416, 0.298, 0.455, 0.012)}

# DBI permits for new buildings on the site (DataSF i98e-djp9), checked for any that are under
# construction or complete before drawing none.
PERMITS = ["201511132572", "201511092111", "201510260810", "201510230640", "201510230639",
           "202212208799", "202212198663", "202212138195"]
PERMIT_URL = "https://data.sf.gov/resource/i98e-djp9.json?permit_number={}"


def _fetch_heights() -> gpd.GeoDataFrame:
    out = HEIGHTS["cache"]
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(HEIGHTS["url"]) as r:
            out.write_bytes(r.read())
    return gpd.read_file(out).to_crs(UTM)


def _parse(district: str) -> int | None:
    """'85-PM' -> 85; '40-OS-PM' -> None (open space)."""
    if district == OPEN_SPACE:
        return None
    m = re.fullmatch(r"(\d+)-PM", district)
    if not m:
        raise SystemExit(f"unexpected Parkmerced district {district!r}")
    return int(m.group(1))


def _buildings() -> gpd.GeoDataFrame:
    """Overture buildings over the site (for the tower check)."""
    cache = config.RAW / "pm-buildings.parquet"
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
        pq.write_table(d.to_table(columns=["id", "geometry", "height", "num_floors"], filter=f), cache)
    t = pq.read_table(cache)
    return gpd.GeoDataFrame(t.drop(["geometry"]).to_pandas(),
                            geometry=shapely.from_wkb(t.column("geometry").to_numpy(zero_copy_only=False)),
                            crs=4326).to_crs(UTM)


def _permits() -> list[dict]:
    cache = RAW / "pm-dbi-permits.json"
    if not cache.exists():
        rows = []
        for p in PERMITS:
            with urllib.request.urlopen(PERMIT_URL.format(p)) as r:
                rows += json.loads(r.read())
        cache.write_text(json.dumps(rows))
    return json.loads(cache.read_text())


def _labels(pdf_path) -> tuple[list[tuple[int, float, float]], list[tuple[str, float, float]]]:
    """Height labels ("85’") and block labels ("02W") in Figure 03.03.C, as (text, x, y) in PDF points."""
    with pdfplumber.open(str(pdf_path), pages=[FIG["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        if "FIGURE 03.03.C / Maximum Height Plan" not in page.extract_text():
            raise SystemExit("Figure 03.03.C is not on the expected DSG page")
        # Characters in content-stream order; a word is a run on one baseline with touching boxes.
        # (Some labels are drawn twice, about 3 pt apart, so position-sorted grouping would mix them.)
        runs: list[list[dict]] = []
        for c in page.chars:
            r = runs[-1] if runs else None
            if r and abs(r[-1]["matrix"][5] - c["matrix"][5]) < 0.05 and abs(c["x0"] - r[-1]["x1"]) < 0.3:
                r.append(c)
            else:
                runs.append([c])
    heights, blocks = [], []
    for r in runs:
        t = "".join(c["text"] for c in r)
        x, y = (r[0]["x0"] + r[-1]["x1"]) / 2, (r[0]["top"] + r[0]["bottom"]) / 2
        if y > MAP_BOTTOM_PT or (x > LEGEND_X_PT and y < LEGEND_BOTTOM_PT):
            continue
        m = re.fullmatch(r"(\d+)’", t)
        if m and not any(h == int(m.group(1)) and abs(hx - x) < 6 and abs(hy - y) < 6 for h, hx, hy in heights):
            heights.append((int(m.group(1)), x, y))
        elif re.fullmatch(r"\d\d(N|S|E|W|O|NW|NE|SW|SE)?|JBC", t) and abs(r[0]["size"] - 6.0) < 0.1:
            blocks.append((t, x, y))
    return heights, blocks


def _georeference(heights, zones: gpd.GeoDataFrame) -> trace.Similarity:
    """Fit the figure to the zoning layer: each height label to the centroid of the nearest zoning
    district of that height (the mid-rise boxes; the 130-ft tower bands hold two labels, so they
    are left out of the fit)."""
    src, dst = [], []
    for name, (fig_xy, utm_xy) in INIT.items():
        hit = zones[zones.geometry.contains(Point(utm_xy))]
        if len(hit) != 1:
            raise SystemExit(f"starting point for {name} is not in exactly one zoning district")
        c = hit.geometry.iloc[0].centroid
        src.append(fig_xy)
        dst.append((c.x, c.y))
    sim = trace.fit_similarity(src, dst, list(INIT))
    boxes = [(h, g.centroid) for h, g in zip(zones["ft"], zones.geometry) if h and h > 65 and h != TOWER_FT]
    for _ in range(5):
        src, dst, labels = [], [], []
        for h, x, y in heights:
            if h == TOWER_FT:
                continue
            p = Point(sim.apply([(x, y)])[0])
            d, c = min(((c.distance(p), c) for bh, c in boxes if bh == h), key=lambda t: t[0])
            if d < 30:
                src.append((x, y))
                dst.append((c.x, c.y))
                labels.append(f"{h}-ft label at figure ({x:.0f}, {y:.0f}) pt")
        sim = trace.fit_similarity(src, dst, labels)
    if len(src) < 40 or sim.rms_m > 8:
        raise SystemExit(f"Figure 03.03.C fit is poor: {len(src)} matches, RMS {sim.rms_m:.1f} m")
    return sim


def _to_figure(sim: trace.Similarity, g):
    """UTM geometry -> 200-dpi figure pixels."""
    m = np.linalg.inv(sim.matrix())

    def f(xy):
        a = (m @ (np.asarray(xy) - [sim.tx, sim.ty]).T).T
        a[:, 1] *= -1
        return a * DPI / 72

    return shapely.transform(g, f)


def _render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    return np.asarray(page.render(scale=DPI / 72).to_pil().convert("RGB"))


def _legend_colours(rgb: np.ndarray, pdf_path) -> dict:
    """Render colours of the legend swatches (40' O.S., 45', 65'): the pixel right of each label."""
    with pdfplumber.open(str(pdf_path), pages=[FIG["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        rects = [r for r in page.rects if r["x0"] > LEGEND_X_PT and r["bottom"] < LEGEND_BOTTOM_PT and r.get("fill")]
    out = {}
    for name, y in (("open space", 64.5), (45, 75.3), (65, 86.1)):
        sw = [r for r in rects if r["top"] - 1 < y < r["bottom"] + 1 and r["width"] > 10]
        if not sw:
            raise SystemExit(f"no legend swatch for {name}")
        r = sw[0]
        cx, cy = (r["x0"] + r["x1"]) / 2 * DPI / 72, (r["top"] + r["bottom"]) / 2 * DPI / 72
        out[name] = tuple(int(v) for v in np.median(rgb[int(cy) - 3:int(cy) + 4, int(cx) - 6:int(cx) + 7].reshape(-1, 3), axis=0))
    return out


def _fill_shares(rgb: np.ndarray, colours: dict, poly_px) -> dict:
    """Share of a zone's figure pixels in each legend fill, as drawn on the map (about 70% opacity)."""
    import cv2

    mask = np.zeros(rgb.shape[:2], np.uint8)
    for p in getattr(poly_px, "geoms", [poly_px]):
        cv2.fillPoly(mask, [np.round(np.asarray(p.exterior.coords)).astype(np.int32)], 1)
        for h in p.interiors:
            cv2.fillPoly(mask, [np.round(np.asarray(h.coords)).astype(np.int32)], 0)
    px = rgb[mask.astype(bool)].astype(int)
    if not len(px):
        return {k: 0.0 for k in colours}
    return {k: float((np.abs(px - (255 - FILL_OPACITY * (255 - np.array(c)))).max(axis=1) <= 12).mean())
            for k, c in colours.items()}


def _plan_blocks(pdf_path, blocks, sim: trace.Similarity) -> list[tuple[str, object]]:
    """The figure's block fills (45-ft, 65-ft and open-space colours, vector shapes in the PDF), in UTM,
    each named by the block names printed inside it."""
    with pdfplumber.open(str(pdf_path), pages=[FIG["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        fills = [q for c in FILL_CMYK.values() for q in trace.pdf_filled_polygons(page, c, max_top=MAP_BOTTOM_PT)
                 if not (q.bounds[0] > LEGEND_X_PT and q.bounds[3] < LEGEND_BOTTOM_PT)]
    pts = {k: Point(sim.apply([(x, y)])[0]) for k, x, y in blocks}
    out = []
    for q in fills:
        u = sim.geometry(q)
        names = [k for k, p in pts.items() if u.buffer(5).contains(p)]
        out.append((names, u))
    return out, pts


def _blocks(zones: gpd.GeoDataFrame, plan, pts) -> list[str]:
    """Each zone's DSG block: the figure fill it overlaps most, and of the block names printed in that
    fill, the nearest. Where a zone holds two names of one block (02W and 02E, which the zoning map
    joins across a planned street), it takes the shared number ("02"). A zone that overlaps no named
    fill (a box the figure leaves white) takes the name of the zone it borders most, or of the nearest
    fill within 15 m."""
    geoms = list(zones.geometry)
    out: list[str | None] = []
    for g in geoms:
        direct = sorted(k for k, p in pts.items() if g.buffer(6).contains(p))
        nums = {re.match(r"\d+|JBC", k).group(0) for k in direct}
        if len(direct) > 1 and len(nums) == 1:
            out.append(nums.pop())
            continue
        area, names = max(((u.intersection(g.buffer(3)).area, names) for names, u in plan if names),
                          key=lambda t: t[0])
        out.append(min(names, key=lambda k: g.distance(pts[k])) if area > 0 else None)
    for i, g in enumerate(geoms):
        if out[i] is None:
            shared = [(geoms[j].intersection(g.buffer(2)).area, out[j]) for j in range(len(geoms))
                      if j != i and out[j] is not None]
            area, name = max(shared, key=lambda t: t[0])
            if area <= 0:
                # A lone zone: the nearest named fill, if it's close.
                d, names = min(((u.distance(g), names) for names, u in plan if names), key=lambda t: t[0])
                if d > 15:
                    raise SystemExit(f"no Figure 03.03.C block for the zone at {g.centroid}")
                name = min(names, key=lambda k: g.distance(pts[k]))
            print(f"[parkmerced]   zone at ({g.centroid.x:.0f}, {g.centroid.y:.0f}) overlaps no named fill; "
                  f"takes the block of its neighbour or the nearest fill, {name}")
            out[i] = name
    return out


def main() -> None:
    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    hb = _fetch_heights()
    zones = hb.explode(index_parts=False).reset_index(drop=True)
    zones = zones[zones.geometry.area > 20].reset_index(drop=True)
    zones["ft"] = [_parse(h) for h in zones["height"]]
    print(f"[parkmerced] {len(zones)} Parkmerced zoning height zones: "
          + ", ".join(f"{k} ×{v}" for k, v in zones["height"].value_counts().sort_index().items()))
    pdf_path = trace.fetch_document(DSG["url"], tb.DOCS / DSG["file"], DSG["sha256"])
    heights, blocks = _labels(pdf_path)
    print(f"[parkmerced] Figure 03.03.C: {len(heights)} height labels, {len(blocks)} block labels")
    sim = _georeference(heights, zones)
    print(f"[parkmerced] Figure 03.03.C fit to the zoning layer: RMS {sim.rms_m:.2f} m over "
          f"{len(sim.labels)} height labels, scale {sim.scale:.4f} m/pt, rotation {np.degrees(sim.rotation):.2f} deg")
    label_pts = [(h, Point(sim.apply([(x, y)])[0]), x, y) for h, x, y in heights]

    # Check 1: every height label falls in a zoning district of that height.
    label_misses = []
    for h, p, x, y in label_pts:
        hit = zones[zones.geometry.buffer(LABEL_TOL_M).contains(p)]
        if h not in set(hit["ft"]):
            near = min(g.distance(p) for g in zones.geometry[zones["ft"] == h])
            label_misses.append(f"{h}-ft label at figure ({x:.0f}, {y:.0f}) pt falls in "
                                f"{sorted(set(hit['height'])) or 'no district'}, {near:.0f} m from a {h}-ft district")

    # Which zoning pieces are development blocks in the plan. The zoning map also carries heights over
    # some rights-of-way (medians, roundabouts, the Muni corridor, realigned streets): those pieces are
    # thin, or are street (no fill) in Figure 03.03.C, and aren't drawn.
    rgb = _render(pdf_path)
    colours = _legend_colours(rgb, pdf_path)
    kind, dropped, fabric_diff = [], [], []
    for h, d, g in zip(zones["ft"], zones["height"], zones.geometry):
        n_labels = sum(1 for lh, p, _, _ in label_pts if lh == h and g.buffer(LABEL_TOL_M).contains(p))
        shares = _fill_shares(rgb, colours, _to_figure(sim, g))
        why = None
        if h is None or h != h:  # NaN once in the frame
            k = "open space"
        elif g.buffer(-4).is_empty:
            k, why = "street", "thin strip"
        elif h == TOWER_FT:
            k = "tower"
        elif h in FABRIC:
            k = "fabric" if max(shares[45], shares[65]) >= 0.3 else "street"
            if k == "street":
                why = "street or right-of-way in the figure"
            elif max(shares, key=shares.get) != h:
                fabric_diff.append(f"zoning {d} ({g.area:.0f} m², at {g.centroid.x:.0f} E {g.centroid.y:.0f} N) is "
                                   f"{max(shares, key=shares.get)} ft in the figure")
        else:
            k = "envelope" if n_labels or g.area >= 700 else "street"
            if k == "street":
                why = "unlabelled sliver of an envelope across a street"
        kind.append(k)
        if why:
            dropped.append(f"{d} {g.area:.0f} m² ({why})")
    zones["kind"] = kind
    unlabelled = [d for d, k, g in zip(zones["height"], zones["kind"], zones.geometry)
                  if k == "envelope" and not any(g.buffer(LABEL_TOL_M).contains(p) for _, p, _, _ in label_pts)]
    n_fabric = sum(k == "fabric" for k in kind)
    print(f"[parkmerced] check: {len(heights) - len(label_misses)} of {len(heights)} height labels in a zoning "
          f"district of that height; {n_fabric - len(fabric_diff)} of {n_fabric} fabric zones have the "
          f"figure's fill for their height; {len(unlabelled)} envelope zones unlabelled")
    for m in label_misses + fabric_diff + [f"unlabelled {d} envelope" for d in unlabelled]:
        print(f"[parkmerced]   differs: {m}")
    print(f"[parkmerced] left out as streets: {len(dropped)} pieces, {sum(float(x.split()[1]) for x in dropped):.0f} m²")
    if label_misses or unlabelled or len(fabric_diff) > 0.15 * n_fabric:
        raise SystemExit("zoning and Figure 03.03.C disagree; review before drawing")

    for d, k, g in zip(zones["height"], zones["kind"], zones.geometry):
        if k in ("fabric", "envelope") and g.intersection(site_utm).area / g.area < 0.9:
            raise SystemExit(f"zone {d} at {g.centroid} lies outside the Special Use District")

    named = zones["kind"].isin(["fabric", "envelope"])
    zones["block"] = None
    plan, pts = _plan_blocks(pdf_path, blocks, sim)
    # Named by block number, as in the DSG's Regulating Plan (Appendix A, "BLOCK 01" to "BLOCK 23"):
    # the zoning map joins some sub-blocks (02W and 02E, 16NW and 16NE) that the figure splits.
    zones.loc[named, "block"] = [re.match(r"\d+|JBC", b).group(0) for b in _blocks(zones[named], plan, pts)]

    # The towers that stay: every tall existing building should be in a 130-ft district.
    bldgs = _buildings()
    bldgs = bldgs[bldgs.geometry.centroid.within(site_utm)]
    tall = bldgs[bldgs["height"].fillna(0) > 30]
    towers = shapely.union_all(zones[zones["ft"] == TOWER_FT].geometry.to_numpy())
    in_tower = int(tall.geometry.centroid.within(towers.buffer(2)).sum())
    print(f"[parkmerced] {len(tall)} existing buildings over 30 m mapped on the site; {in_tower} in the 130-ft districts")
    if in_tower != 11 or len(tall) != 11:
        raise SystemExit("expected the 11 retained towers, each in a 130-ft district")

    # No new building is under construction or complete.
    permits = _permits()
    started = [r for r in permits if r.get("first_construction_document_date") or r.get("status") == "complete"]
    if started:
        raise SystemExit(f"a Parkmerced permit shows construction: {[r['permit_number'] for r in started]}")
    issued = sorted({(r["permit_number"], r["status"]) for r in permits})
    print(f"[parkmerced] DBI new-building permits: {', '.join(f'{p} {s}' for p, s in issued)}; none started")

    drawn = zones[zones["kind"].isin(["fabric", "envelope"])].reset_index(drop=True)
    # The towers' footprints reach a few metres past their 130-ft districts in places: cut them out.
    clash = [round(drawn.geometry.intersection(b).area.sum()) for b in tall.geometry]
    print(f"[parkmerced] tower footprint area under drawn zones, cut out (m²): {clash}")
    if max(clash) > 100:
        raise SystemExit("an existing tower lies well inside a drawn zone")
    tower_cut = shapely.union_all(tall.geometry.to_numpy()).buffer(1.0)

    fig = f"{DSG['title']}, {FIG['figure']}, p. {FIG['printed_page']}"

    def order(z):
        m = re.match(r"(\d+)?(.*)", z["block"])
        return (int(m.group(1)) if m.group(1) else 99, m.group(2), z["ft"])

    features = []
    for _, z in sorted(drawn.iterrows(), key=lambda kv: order(kv[1])):
        print(f"[parkmerced]   Block {z['block']:>5}: {z['height']:>7}, {z.geometry.area:6.0f} m² "
              f"at ({z.geometry.centroid.x:.0f}, {z.geometry.centroid.y:.0f})")
        h = int(z["ft"])
        geom = shapely.make_valid(z.geometry.difference(tower_cut).simplify(0.4))
        geom = shapely.union_all([g for g in getattr(geom, "geoms", [geom])
                                  if g.geom_type == "Polygon" and g.area > 20 and not g.buffer(-1.0).is_empty])
        fabric = h in FABRIC
        base = None
        if not fabric:
            # The fabric limit around the envelope applies to any part of it not built taller.
            shared = [(f.intersection(z.geometry.buffer(2)).area, int(fh)) for f, fh, k in
                      zip(drawn.geometry, drawn["ft"], drawn["kind"]) if k == "fabric"]
            area, fh = max(shared, key=lambda t: t[0])
            base = fh if area > 1 else None
        props = {
            "kind": "block",
            "block": z["block"],
            "label": f"Block {z['block']}",
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": base,
            "base_ft": 0,
            "use": None,
            "phase": None,
            "illustrative": True,
            "source": (f"illustrative: drawn to the height limit of zoning district \"{z['height']}\" in "
                       f"{HEIGHTS['title']} ({HEIGHTS['landing']}); {STANDARD} and block number from {fig}"
                       + (f"; envelope over the {base}-ft limit of the fabric around it" if base else "")),
            "note": ("Neighborhood fabric: low-rise buildings up to this height." if fabric else
                     f"Mid-rise buildable envelope: a building may rise to {h} ft here"
                     + (f" over the {base}-ft fabric limit" if base else "")
                     + "; the DSG's Regulating Plan caps the footprint at each height per block (Appendix A)."),
        }
        features.append({"type": "Feature", "properties": props,
                         "geometry": mapping(tb.to_wgs(trace.as_multipolygon(geom)))})
    for i, f in enumerate(features):
        f["properties"]["fid"] = i + 1

    n_blocks = len({f["properties"]["block"] for f in features})
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                f"Illustrative massing: Parkmerced's {n_blocks} development blocks are drawn to the height limits "
                "of the city's zoning map, which matches the Maximum Height Plan in the adopted Design Standards "
                "and Guidelines, not as building designs: a low-rise fabric of 45 and 65 ft, with mid-rise and "
                "tower envelopes of 85 to 145 ft shown over the fabric height, where taller buildings may rise. "
                "The 11 existing towers that stay are in the base map and aren't redrawn; streets and open space "
                "aren't drawn. No new building has been built."
            ),
            "note": ("Blocks are drawn to their height limits, not as building designs; real buildings will be "
                     "smaller and the taller envelopes won't be filled."),
            "sourceUrl": DSG["url"],
            "sourceLabel": "Design standards and guidelines, 2014 (PDF)",
            "georeference": {
                "zoning": "GIS layer, used as published (no tracing)",
                "figure_03_03_c": {
                    **sim.report(),
                    "method": "height labels matched to the zoning districts of the same height; similarity "
                              "fitted to their centroids",
                    "use": "block numbers and a zone-by-zone height check (the label offsets inside the boxes "
                           "account for most of the RMS)",
                    "check": (f"{len(heights) - len(label_misses)} of {len(heights)} height labels fall in a zoning "
                              f"district of that height; {n_fabric - len(fabric_diff)} of {n_fabric} drawn fabric zones "
                              "have the figure's fill for their height"),
                    "differences": label_misses + fabric_diff,
                    "left_out": (f"{len(dropped)} zoning pieces ({sum(float(x.split()[1]) for x in dropped):.0f} m²) "
                                 "that are streets, medians or rights-of-way in the figure"),
                },
            },
            "license": "Block shapes: DataSF zoning map (Public Domain U.S. Government).",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(fc), separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"[parkmerced] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
