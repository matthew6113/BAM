"""Candlestick Point: block height limits and tower zones, traced from the 2024 height map.

Sources:
- Height map: Addendum 7 to the CP-HPS2 2010 FEIR (OCII, Aug 2024), Figure 5 "Proposed 2024 CP
  Maximum Building Heights" (PDF p. 23, printed p. 17). Vector art. It is the whole Candlestick Point
  height plan as amended in 2024: the Design for Development's Figure 4.3 heights outside
  Candlestick Center (unchanged in 2024: "No changes in the maximum heights of CP development that
  are directly adjacent to existing neighborhoods", Addendum 7, PDF p. 46) and the new Candlestick
  Center heights of D4D Section A5.3, Figure A5.3N "Building Height Block Area Map", which repeats
  the same map without a legend. CCII Resolution 28-2024 (Sept 3, 2024) adopted the amendment.
- Tower heights and podiums: Candlestick Point Design for Development (2024 Amendment edition,
  OCII), Table 4.2 "Maximum High-rise Podium Heights and Building Heights" (PDF p. 146, printed
  p. 84). Figure 5 prints the same tower heights next to each tower symbol; the module checks they
  agree.
- Block numbers and neighborhoods: D4D Figure 4.1 "Development Blocks" (PDF p. 139, printed p. 77).
  Candlestick Center parcel letters: D4D Figure A5.3N (Section A5.3 p. 36).
- Built buildings: Alice Griffith replacement housing, DBI building permits 201401166470 (2600
  Arelious Walker Dr., 5 stories, 93 homes), 201401166475 (2700, 5 stories, 91), 201608296272 (2800,
  3 stories, 31) and 201501236565 (2500, 5 stories, 122), all complete in DataSF's permit table;
  337 homes in all, as OCII's Sept 2024 memo says. Footprints are OpenStreetMap (via Overture).

What this is and isn't:
- Each block is drawn to its height limit, not as a building design, so the massing is
  labelled illustrative. Where a block has several height zones the D4D lets the change of height
  move ("the precise location of the height change ... is flexible").
- Towers: Table 4.2 allows 11 towers (Addendum 7 notes the 2019 change from 12). A fixed tower
  location is drawn as Figure 5's square symbol; a tower with an "allowable zone" is drawn as the
  whole hatched zone. Either way the zone is the tower's height over its podium height
  (height_ft over podium_ft), and the tower can sit anywhere in its zone, so it's flexible.
  Hatched pieces with no tower symbol take the tower height only when every nearby candidate
  tower has the same limits; otherwise they stay at the block's base height.
- Candlestick Center is drawn under the 2024 Innovation District alternative (Section A5.3,
  85-180 ft), which applies if that alternative is chosen for the whole Center; otherwise the
  2019 limits (85-120 ft) apply.
- The block marked "40 ft if park, 65 ft if development parcel" is outlined only (Figure 4.3 of the
  D4D says 85 ft if a development parcel).
- The Candlestick Point State Recreation Area, parks, streets and mid-block breaks aren't massing.
- Alice Griffith blocks already built (337 homes, 2017-2019 and 2026) are drawn as their
  buildings instead of as envelopes. Their mapped heights are machine estimates that don't fit
  the permitted stories, so they have stories but no height.
- All other blocks are "entitled": the groundbreaking (Sept 9, 2026) began infrastructure, and the
  permits filed for Harney Way and Gilman Avenue buildings haven't been issued.

Georeferencing: Figure 5 draws the city blocks around the site. They are matched to SF's parcel
map (DataSF acdm-wktn, parcels merged into blocks): a raster correlation for the rough fit, then a
least-squares similarity on the centroids of whole blocks matching with IoU > 0.7. The fit and its
residuals are recorded in the output. As a check, the traced massing is compared with the official
site boundary.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_candlestick_point
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse
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
from shapely.geometry import Point, Polygon, box, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "candlestick-point"
UTM = tb.UTM
DOCS = config.ROOT / "data" / "raw" / "docs"
FT = 0.3048

ADD7 = {
    "title": "Addendum 7 to the CP-HPS2 2010 FEIR (OCII, Aug 2024)",
    "url": "https://sfocii.org/sites/default/files/2024-09/Addendum%207%20to%20the%20CP-HPS2%202010%20FEIR.pdf",
    "sha256": "c75cb08b1bb08516997b9164f86d8b6ed93f07195d1b19f68d57deb8ba2763e6",
    "file": "candlestick-addendum-7-2024.pdf",
}
FIG5 = {"page_index": 22, "printed_page": "17", "figure": "Figure 5, Proposed 2024 CP Maximum Building Heights"}
ADD7_NO_CHANGE_PAGE = 45  # "No changes in the maximum heights of CP development that are directly adjacent ..."

D4D = {
    "title": "Candlestick Point Design for Development, 2024 Amendment edition (OCII; CCII Resolution 28-2024)",
    "url": "https://sfocii.org/sites/default/files/2025-10/Candlestick%20Point%20Design%20for%20Development%202024%20Amendment.pdf",
    "sha256": "2336041638fcf03cb1cac5b2be114414b552756093354da8f1df6a37088e2ef2",
    "file": "candlestick-d4d-2024-amendment.pdf",
}
TABLE_4_2 = {"page_index": 145, "printed_page": "84"}
FIG_4_1 = {"page_index": 138, "printed_page": "77"}
A53N = {"page_index": 37, "printed_page": "Section A5.3 p. 36"}

# The Planning Commission's 2024 packet (case 2007.0946GPRCWP-04, PDF p. 6) counts the Center's
# new limits: "Of the 14 blocks, four would allow up to 180 feet in height, five would allow up to
# 160 feet, three would allow up to 120 feet, and the remaining two limiting building height to 85 feet."
PC_PACKET = "https://citypln-m-extnl.sfgov.org/Commissions/CPC/9_12_2024/Commission%20Packet/2007.0946GPRCWP-04.pdf"
CENTER_COUNTS = {180: 4, 160: 5, 120: 3, 85: 2}

# Figure 5's map frame (PDF points): fills are clipped to it.
FRAME = (80.8, 112.3, 531.4, 525.6)
SCALE_BAR = (464.74, 524.82, 750 * FT)  # Figure 5 scale bar: x from, x to (points), length (m)

# Candlestick Center parcels: Figure A5.3N's letters (a raster figure with no legend), placed in
# Figure 5 points by matching the two drawings by eye, with the colour each has in Figure A5.3N.
# The module checks every point falls in a Figure 5 fill of that height.
CENTER_PARCELS = {
    "A": ((236, 410), 180), "B": ((228, 392), 180), "C": ((222, 372), 120), "D": ((220, 350), 180),
    "E": ((220, 330), 180), "F": ((218, 307), 160), "G": ((253, 397), 160), "H": ((245, 383), 120),
    "I": ((248, 350), 160), "J": ((240, 322), 160), "K": ((270, 377), 120), "L": ((262, 350), 160),
    "M": ((283, 363), 85), "N": ((282, 348), 85),
}

# Table 4.2 letters for Figure 5's tower symbols. Figure 5 prints heights but no letters; where two
# towers share a height and kind of symbol, Table 4.2's siting text puts the first-listed one
# further north (A on Egbert vs C on Earl; B at Harney/Egbert vs G at Gilman; D on Gilman vs K on
# Ingerson in the south; F2 at Ingerson/Harney vs H at Harney's southern extension).
TOWER_ORDER = {(220, "encouraged"): ["A", "C"], (240, "fixed"): ["B", "G"], (320, "encouraged"): ["D", "K"],
               (320, "fixed"): ["F2", "H"], (170, "encouraged"): ["E2"], (420, "fixed"): ["I"], (370, "fixed"): ["J"]}

# Alice Griffith replacement housing: DBI permits (DataSF i98e-djp9), all "complete".
PERMIT_URL = "https://data.sf.gov/resource/i98e-djp9.json?permit_number={}"
ALICE_GRIFFITH = [
    {"permit": "201501236565", "address": "2500 Arelious Walker Dr.", "stories": 5, "homes": 122, "completed": "2026-09-21",
     "point": (-122.384303729, 37.719624244)},
    {"permit": "201401166470", "address": "2600 Arelious Walker Dr.", "stories": 5, "homes": 93, "completed": "2017-10-27",
     "point": (-122.384952769, 37.718877792)},
    {"permit": "201401166475", "address": "2700 Arelious Walker Dr.", "stories": 5, "homes": 91, "completed": "2017-10-27",
     "point": (-122.385505386, 37.718268961)},
    {"permit": "201608296272", "address": "2800 Arelious Walker Dr.", "stories": 3, "homes": 31, "completed": "2019-05-02",
     "point": (-122.386020747, 37.717667637)},
]
AG_MATCH_M = 80  # a footprint joins the nearest permit's address point within this distance
AG_MIN_AREA_M2 = 400

PARCELS_URL = "https://data.sf.gov/resource/acdm-wktn.geojson"
PARCELS_BBOX = (37.727, -122.400, 37.704, -122.370)  # north, west, south, east
STREETS_BBOX = (-122.398, 37.705, -122.370, 37.726)
BUILDINGS_BBOX = (-122.395, 37.707, -122.373, 37.723)


# ---------------------------------------------------------------- documents and base data

def parcel_blocks() -> list[Polygon]:
    """SF parcels around the site (DataSF acdm-wktn, active), merged into city blocks, in UTM."""
    cache = config.ROOT / "data" / "raw" / "massing" / "candlestick-parcels.geojson"
    if not cache.exists():
        n, w, s, e = PARCELS_BBOX
        q = urllib.parse.urlencode({"$where": f"active=true AND within_box(shape, {n}, {w}, {s}, {e})", "$limit": 50000})
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(f"{PARCELS_URL}?{q}") as r:
            cache.write_bytes(r.read())
    p = gpd.read_file(cache).to_crs(UTM)
    merged = shapely.union_all(p.geometry.buffer(0.05).to_numpy()).buffer(-0.05)
    return [g for g in getattr(merged, "geoms", [merged]) if g.geom_type == "Polygon"]


def overture_buildings() -> gpd.GeoDataFrame:
    cache = config.RAW / "buildings_candlestick.parquet"
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
    g["osm"] = g["sources"].apply(lambda s: next((x.get("record_id") for x in s if x.get("dataset") == "OpenStreetMap"), None))
    g["height_from"] = g["sources"].apply(
        lambda s: next((x.get("dataset") for x in s if x.get("property") == "/properties/height"), "OpenStreetMap"))
    return g.to_crs(UTM)


def check_d4d(pdf_path) -> dict[str, tuple[int, int]]:
    """Table 4.2 tower limits (overall height, podium) as printed, and the A5.3 height text."""
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf_path))
    t = doc[TABLE_4_2["page_index"]].get_textpage().get_text_range()
    if "Table 4.2 Maximum High-rise Podium Heights and Building Heights" not in t:
        raise SystemExit("D4D Table 4.2 is not on the expected page")
    towers = {}
    for m in re.finditer(r"^([A-K]2?) SS – (\d+)\s+SS – (\d+)", t, re.M):
        towers[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    # Tower D's row is split: "D SS – 320" / "SS – 65" / "Fronting Gilman ..." / "SS – 85 ... Fronting Harney".
    m = re.search(r"^D SS – (\d+)\s*\n\s*SS – (\d+)", t, re.M)
    if m:
        towers["D"] = (int(m.group(1)), int(m.group(2)))
    expected = {"A", "B", "C", "D", "E2", "F2", "G", "H", "I", "J", "K"}
    if set(towers) != expected:
        raise SystemExit(f"D4D Table 4.2: found towers {sorted(towers)}")
    if "Fronting Gilman" not in t or "SS – 85" not in t:
        raise SystemExit("D4D Table 4.2: tower D's 85-ft podium fronting Harney Way is not where expected")
    a53 = doc[A53N["page_index"]].get_textpage().get_text_range()
    if "Figure A5.3N Building Height Block Area Map" not in a53:
        raise SystemExit("D4D Figure A5.3N is not on the expected page")
    return towers


# ---------------------------------------------------------------- Figure 5

def _color(o) -> str:
    c = o.get("non_stroking_color")
    if isinstance(c, (int, float)):
        c = (c,)
    return str(tuple(round(v, 3) if isinstance(v, (int, float)) else v for v in (c or ())))


def _fills(page) -> list[tuple[str, Polygon]]:
    x0, y0, x1, y1 = FRAME
    frame = box(x0, y0, x1, y1)
    out = []
    for o in page.curves + page.rects:
        pts = o.get("pts")
        if not o.get("fill") or not pts or len(pts) < 3:
            continue
        g = shapely.make_valid(Polygon(pts)).intersection(frame)
        if g.area > 0.5:
            out.append((_color(o), g))
    return out


def legend(page) -> dict[int, np.ndarray]:
    """Height (ft) -> CMYK of its legend swatch, read from the "NNN Feet" labels."""
    words = [w for w in page.extract_words() if w["top"] > FRAME[3] and w["x0"] < 120 and w["text"].isdigit()]
    swatches = []
    for o in page.rects + page.curves:
        c = o.get("non_stroking_color")
        if o.get("fill") and isinstance(c, (tuple, list)) and len(c) == 4 and o["x1"] < 105 and o["top"] > FRAME[3]:
            swatches.append(((o["top"] + o["bottom"]) / 2, np.array(c, float)))
    out = {}
    for w in words:
        y = (w["top"] + w["bottom"]) / 2
        near = [c for sy, c in swatches if abs(sy - y) < 4]
        if len(near) != 1:
            raise SystemExit(f"Figure 5 legend: no unique swatch for {w['text']} ft")
        out[int(w["text"])] = near[0]
    if sorted(out) != [40, 65, 80, 85, 120, 160, 180]:
        raise SystemExit(f"Figure 5 legend heights {sorted(out)}")
    return out


def _inradius(g) -> float:
    return 2 * g.area / g.length


def read_figure_5(page) -> dict:
    """Height zones, tower zones and symbols, mid-block breaks and the park-or-parcel block."""
    pal = legend(page)
    keys = list(pal)
    cols = np.array([pal[k] for k in keys])
    zones, patterns, white = [], [], []
    for col, g in _fills(page):
        if col.startswith("('P") or col.startswith("(P") or col.startswith("P"):
            patterns.append((col, g))
            continue
        try:
            v = np.array(eval(col), float)  # noqa: S307 - a tuple of numbers we formatted above
        except Exception:
            continue
        if len(v) != 4:
            continue
        if v.max() == 0:
            white.append(g)
            continue
        d = np.abs(cols - v).max(axis=1)
        i = int(d.argmin())
        if d[i] <= 0.08 and np.sort(d)[1] > 0.2:
            zones.append({"height_ft": keys[i], "px": g})
    # Tower symbols: the white squares, 7.7 points a side.
    squares = []
    for g in white:
        r = g.minimum_rotated_rectangle
        c = np.asarray(r.exterior.coords)
        sides = sorted([np.linalg.norm(c[1] - c[0]), np.linalg.norm(c[2] - c[1])])
        if 7 < sides[0] < 9 and sides[1] < 9 and g.area > 50:
            squares.append(g)
    # Patterns: mid-block breaks are thin strips; the tower hatch is the pattern holding symbols.
    thin = [g for _, g in patterns if _inradius(g) < 4]
    wide = [(c, g) for c, g in patterns if _inradius(g) >= 4]
    holds = {}
    for c, g in wide:
        holds[c] = holds.get(c, 0) + sum(g.buffer(1).contains(s.centroid) for s in squares)
    hatch_key = max(holds, key=holds.get)
    hatched = [g for c, g in wide if c == hatch_key]
    others = [g for c, g in wide if c != hatch_key]
    if len(squares) != 11 or len(hatched) != 7 or len(others) != 1:
        raise SystemExit(f"Figure 5: {len(squares)} tower symbols, {len(hatched)} hatched zones, {len(others)} other patterns")
    return {"zones": zones, "squares": squares, "hatched": hatched, "park_or_parcel": others[0], "breaks": thin}


def tower_labels(page) -> list[tuple[int, Point]]:
    """The rotated "NNN’" labels beside the tower symbols, assembled from single characters."""
    x0, y0, x1, y1 = FRAME
    chars = [c for c in page.chars if (c["text"].isdigit() or c["text"] == "’") and x0 < c["x0"] < x1 and y0 < c["top"] < y1]
    pts = np.array([((c["x0"] + c["x1"]) / 2, (c["top"] + c["bottom"]) / 2) for c in chars])
    n = len(chars)
    group = list(range(n))

    def find(i):
        while group[i] != i:
            group[i] = group[group[i]]
            i = group[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(pts[i] - pts[j]) < 4.5:
                group[find(i)] = find(j)
    out = []
    for root in {find(i) for i in range(n)}:
        idx = [i for i in range(n) if find(i) == root]
        p = pts[idx]
        axis = np.linalg.svd(p - p.mean(0))[2][0] if len(idx) > 1 else np.array([1.0, 0.0])
        if axis[0] < 0:
            axis = -axis
        text = "".join(chars[i]["text"] for i in sorted(idx, key=lambda i: pts[i] @ axis))
        m = re.fullmatch(r"(\d{3})’", text)
        if not m:
            raise SystemExit(f"Figure 5: unreadable tower label {text!r}")
        out.append((int(m.group(1)), Point(p.mean(0))))
    return out


def towers(fig: dict, labels, table: dict) -> list[dict]:
    """Each tower symbol with its Table 4.2 letter, kind (fixed or encouraged) and limits."""
    out = []
    used = set()
    for s in fig["squares"]:
        c = s.centroid
        j = min((j for j in range(len(labels)) if j not in used), key=lambda j: labels[j][1].distance(c))
        if labels[j][1].distance(c) > 15:
            raise SystemExit("Figure 5: a tower symbol has no height label beside it")
        used.add(j)
        kind = "encouraged" if any(h.buffer(1).contains(c) for h in fig["hatched"]) else "fixed"
        out.append({"height_ft": labels[j][0], "kind": kind, "px": s})
    for (h, kind), letters in TOWER_ORDER.items():
        group = sorted((t for t in out if t["height_ft"] == h and t["kind"] == kind), key=lambda t: t["px"].centroid.y)
        if len(group) != len(letters):
            raise SystemExit(f"Figure 5: {len(group)} {kind} towers at {h} ft, Table 4.2 order expects {len(letters)}")
        for t, letter in zip(group, letters):
            t["letter"] = letter
            if table[letter][0] != h:
                raise SystemExit(f"Tower {letter}: Figure 5 says {h} ft, Table 4.2 says {table[letter][0]} ft")
    if sorted(t["letter"] for t in out) != sorted(table):
        raise SystemExit("Figure 5's towers don't match Table 4.2")
    return out


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


def figure_city_blocks(page) -> tuple[list[Polygon], list[Polygon]]:
    """City blocks around the site in Figure 5 (light grey fills merged), and those not cut by the frame."""
    grey = [g for col, g in _fills(page) if col == "(0.0, 0.0, 0.0, 0.063)"]
    merged = shapely.union_all(grey)
    blocks = [g for g in getattr(merged, "geoms", [merged]) if g.geom_type == "Polygon"]
    x0, y0, x1, y1 = FRAME
    inner = box(x0 + 1, y0 + 1, x1 - 1, y1 - 1)
    return blocks, [g for g in blocks if inner.contains(g)]


def georeference(page, city: list[Polygon], pivot, centre_utm) -> tuple[trace.Similarity, dict]:
    """`pivot` (figure points) starts at `centre_utm`: the development's middle and the site's."""
    blocks, whole = figure_city_blocks(page)
    scale = SCALE_BAR[2] / (SCALE_BAR[1] - SCALE_BAR[0])
    # 1. Raster correlation (2 m cells) of the figure's city blocks against SF's, near the scale bar's scale.
    res, half, margin = 2.0, 1600.0, 150
    n = int(2 * half / res)
    x0, y_top = centre_utm[0] - half, centre_utm[1] + half
    target = _raster(city, x0, y_top, n, res)
    best = None
    for ds_ in np.linspace(-0.03, 0.03, 7):
        for dr in np.radians(np.linspace(-4, 4, 17)):
            sim = trace.Similarity(scale * (1 + ds_), dr, 0.0, 0.0)
            sim.tx, sim.ty = np.asarray(centre_utm) - sim.apply([pivot])[0]
            moving = _raster([sim.geometry(b) for b in blocks], x0, y_top, n, res)
            r = cv2.matchTemplate(target, moving[margin:-margin, margin:-margin], cv2.TM_CCORR_NORMED)
            _, score, _, loc = cv2.minMaxLoc(r)
            if best is None or score > best[0]:
                best = (score, sim, loc)
    score, sim, loc = best
    sim.tx += (loc[0] - margin) * res
    sim.ty -= (loc[1] - margin) * res
    # 2. Least squares on the centroids of whole blocks matching SF's (IoU > 0.7); drop outliers
    # (blocks drawn differently) beyond three times the median residual, and repeat until stable.
    tree = shapely.STRtree(city)
    pairs = None
    for _ in range(10):
        a, b = [], []
        for f in whole:
            g = sim.geometry(f)
            for j in tree.query(g):
                o = city[j]
                if g.intersection(o).area / g.union(o).area > 0.7:
                    a.append(f.centroid.coords[0])
                    b.append(o.centroid.coords[0])
        if len(a) < 8:
            raise SystemExit(f"only {len(a)} Figure 5 city blocks matched SF's parcel map; the fit is not reliable")
        a, b = np.array(a), np.array(b)
        fit = trace.fit_similarity(a, b)
        keep = np.asarray(fit.residuals_m) <= max(3 * np.median(fit.residuals_m), 2.0)
        fit = trace.fit_similarity(a[keep], b[keep])
        new = (len(a), int(keep.sum()))
        sim = fit
        if new == pairs:
            break
        pairs = new
    r = np.asarray(sim.residuals_m)
    report = {
        "method": "city-block match: raster correlation, then least squares on the centroids of whole Figure 5 "
                  "city blocks matching SF's parcel map merged into blocks (DataSF acdm-wktn, IoU > 0.7)",
        "scale_m_per_unit": round(sim.scale, 5),
        "scale_bar_m_per_unit": round(scale, 5),
        "rotation_deg": round(float(np.degrees(sim.rotation)), 3),
        "rms_m": round(sim.rms_m, 2),
        "median_m": round(float(np.median(r)), 2),
        "max_m": round(float(r.max()), 2),
        "controls": int(len(r)),
        "dropped_as_outliers": int(pairs[0] - pairs[1]),
        "correlation": round(float(score), 3),
    }
    return sim, report


# ---------------------------------------------------------------- block names (Figure 4.1)

def block_numbers(d4d_page) -> list[tuple[str, str, Point]]:
    """(neighborhood, number, point) for every numbered circle in D4D Figure 4.1, in its page points.

    The neighborhoods follow the figure's numbering: Alice Griffith's blocks are plain numbers,
    Candlestick North's carry a/b suffixes, and Candlestick South's lie beyond the diagonal
    x + y = 735 points (its 1, 3 and 5 are plain numbers too). Candlestick Center's single block is
    the circle that lands in the Center.
    """
    out = []
    for o in d4d_page.curves:
        if not (o.get("fill") and _color(o) == "(0.0, 0.0, 0.0, 0.0)" and o.get("pts") and o["top"] < 700):
            continue
        g = Polygon(o["pts"])
        if not 40 < g.area < 70:
            continue
        c = g.centroid
        text = "".join(ch["text"] for ch in sorted(d4d_page.chars, key=lambda ch: ch["x0"])
                       if abs((ch["x0"] + ch["x1"]) / 2 - c.x) < 5 and abs((ch["top"] + ch["bottom"]) / 2 - c.y) < 5)
        if not re.fullmatch(r"\d{1,2}[ab]?", text):
            raise SystemExit(f"D4D Figure 4.1: unreadable block number {text!r}")
        if c.x + c.y > 735:
            hood = "Candlestick South"
        elif text[-1] in "ab":
            hood = "Candlestick North"
        else:
            hood = "Alice Griffith"
        out.append((hood, text, c))
    return out


def register_numbers(numbers, blocks_px: list[Polygon], center_px) -> list[tuple[str, str, Point]]:
    """Place Figure 4.1's block numbers on Figure 5: the similarity that puts the most of them in a block."""
    k = 2.0  # raster cells per point
    x0, y0, x1, y1 = FRAME
    w, h = int((x1 - x0) * k), int((y1 - y0) * k)
    ids = np.zeros((h, w), np.int32)
    for i, b in enumerate(blocks_px, start=1):
        for q in getattr(b, "geoms", [b]):
            a = np.asarray(q.exterior.coords)
            cv2.fillPoly(ids, [np.c_[(a[:, 0] - x0) * k, (a[:, 1] - y0) * k].round().astype(np.int32)], i)
    pts = np.array([[p.x, p.y] for _, _, p in numbers])
    c0 = pts.mean(0)
    target_c = np.asarray(shapely.union_all(blocks_px).centroid.coords[0])
    best = None
    shifts = np.stack(np.meshgrid(np.arange(-60, 60.1, 1.0), np.arange(-60, 60.1, 1.0)), -1).reshape(-1, 1, 2)
    for s in np.arange(0.80, 1.001, 0.01):
        for rot in np.radians(np.arange(-6, 6.01, 0.5)):
            R = np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
            q = ((pts - c0) @ R.T * s + target_c)[None] + shifts  # (shifts, numbers, 2)
            ix = np.clip(((q[..., 0] - x0) * k).astype(int), 0, w - 1)
            iy = np.clip(((q[..., 1] - y0) * k).astype(int), 0, h - 1)
            hit = ids[iy, ix]
            score = (hit > 0).sum(1)
            i = int(score.argmax())
            if best is None or score[i] > best[0]:
                best = (int(score[i]), q[i])
    score, q = best
    placed = [(hood, num, Point(xy)) for (hood, num, _), xy in zip(numbers, q)]
    out = []
    for hood, num, p in placed:
        if center_px.contains(p):
            hood = "Candlestick Center"
        out.append((hood, num, p))
    return out


# ---------------------------------------------------------------- main

def main() -> None:
    add7_path = trace.fetch_document(ADD7["url"], DOCS / ADD7["file"], ADD7["sha256"])
    d4d_path = trace.fetch_document(D4D["url"], DOCS / D4D["file"], D4D["sha256"])
    table = check_d4d(d4d_path)

    with pdfplumber.open(add7_path) as pdf:
        page = pdf.pages[FIG5["page_index"]]
        if "PROPOSED 2024 CP MAXIMUM BUILDING HEIGHTS" not in page.extract_text():
            raise SystemExit("Addendum 7 Figure 5 is not on the expected page")
        fig = read_figure_5(page)
        labels = tower_labels(page)
        tw = towers(fig, labels, table)
        site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM).geometry.iloc[0]
        city = parcel_blocks()
        pivot = np.asarray(shapely.union_all([z['px'] for z in fig['zones']]).centroid.coords[0])
        sim, report = georeference(page, city, pivot, np.asarray(site.centroid.coords[0]))
    print(f"[candlestick] Figure 5 georeference: RMS {report['rms_m']} m over {report['controls']} city blocks "
          f"({report['dropped_as_outliers']} dropped), scale {report['scale_m_per_unit']} m/pt "
          f"(scale bar {report['scale_bar_m_per_unit']}), rotation {report['rotation_deg']} deg")

    # Candlestick Center: the 14 parcels, checked against Figure A5.3N's colours and the packet's counts.
    center_zones = []
    for z in fig["zones"]:
        hit = [p for p, (xy, h) in CENTER_PARCELS.items() if z["px"].contains(Point(xy))]
        if hit:
            p = hit[0]
            if len(hit) > 1 or CENTER_PARCELS[p][1] != z["height_ft"]:
                raise SystemExit(f"Candlestick Center parcel {p}: Figure 5 says {z['height_ft']} ft")
            z["parcel"] = p
            center_zones.append(z)
    counts = {}
    for z in center_zones:
        counts[z["height_ft"]] = counts.get(z["height_ft"], 0) + 1
    if len(center_zones) != 14 or counts != CENTER_COUNTS:
        raise SystemExit(f"Candlestick Center: {len(center_zones)} parcels, heights {counts}")
    center_px = shapely.union_all([z["px"] for z in center_zones])

    # Development blocks in Figure 5 (mid-block breaks and streets separate them), named from Figure 4.1.
    allpx = shapely.union_all([z["px"] for z in fig["zones"]] + fig["hatched"] + [fig["park_or_parcel"]])
    blocks_px = [g for g in getattr(allpx, "geoms", [allpx]) if g.area > 3]
    with pdfplumber.open(d4d_path) as pdf:
        numbers = block_numbers(pdf.pages[FIG_4_1["page_index"]])
    placed = register_numbers(numbers, blocks_px, center_px)

    # Each Figure 5 block takes the Figure 4.1 number(s) that land in it. Where two Figure 4.1 blocks
    # share one Figure 5 outline (no street between them), each fill takes the nearer number.
    block_numbers_in = []
    for b in blocks_px:
        inside = [(hood, num, p) for hood, num, p in placed if b.buffer(0.5).contains(p)]
        block_numbers_in.append(inside)
        if len(inside) != 1:
            print(f"[candlestick] Figure 5 block at {tuple(round(v) for v in b.centroid.coords[0])} "
                  f"holds Figure 4.1 numbers {[(h, n) for h, n, _ in inside]}")
    lost = [(hood, num) for hood, num, p in placed if not any(b.buffer(0.5).contains(p) for b in blocks_px)]
    if lost:
        print(f"[candlestick] Figure 4.1 numbers outside every Figure 5 block: {lost}")

    def name_of(g) -> tuple[str | None, str | None, int]:
        """The name of the Figure 5 block that holds most of `g` (and that block's index)."""
        i = max(range(len(blocks_px)), key=lambda i: blocks_px[i].intersection(g).area)
        inside = block_numbers_in[i]
        if not inside:
            return None, None, i
        c = g.representative_point()
        hood, num, _ = min(inside, key=lambda t: t[2].distance(c))
        return hood, num, i

    # Tower zones: hatched zones with an encouraged symbol take that tower; symbol-less hatched
    # pieces take the tower limits only when all candidate towers within 30 points agree.
    tower_zones = []
    unassigned: dict[tuple, list[str]] = {}
    for t in tw:
        if t["kind"] == "fixed":
            tower_zones.append({"tower": t, "px": t["px"], "shared": None})
    for hz in fig["hatched"]:
        own = [t for t in tw if t["kind"] == "encouraged" and hz.buffer(1).contains(t["px"].centroid)]
        if own:
            tower_zones.append({"tower": own[0], "px": hz, "shared": None})
            continue
        near = [t for t in tw if t["kind"] == "encouraged" and t["px"].centroid.distance(hz.centroid) < 30]
        limits = {table[t["letter"]] for t in near}
        if len(limits) == 1:
            tower_zones.append({"tower": near[0], "px": hz, "shared": sorted(t["letter"] for t in near)})
        else:
            print(f"[candlestick] hatched piece near towers {sorted(t['letter'] for t in near)} "
                  f"(limits differ) stays at its block's base height")
            hood, num, _ = name_of(hz)
            unassigned[(hood, num)] = sorted(t["letter"] for t in near)
    tower_union = shapely.union_all([z["px"] for z in tower_zones])
    breaks = shapely.union_all(fig["breaks"])

    to_utm = lambda g: shapely.make_valid(sim.geometry(g))  # noqa: E731

    # Built Alice Griffith buildings, matched to their permits' address points.
    bld = overture_buildings()
    permit_pts = gpd.GeoSeries([Point(a["point"]) for a in ALICE_GRIFFITH], crs=4326).to_crs(UTM)
    built = []
    for i, row in bld.iterrows():
        if row.geometry.area < AG_MIN_AREA_M2 or not site.contains(row.geometry.centroid):
            continue
        d = permit_pts.distance(row.geometry)
        j = int(d.values.argmin())
        if d.iloc[j] <= AG_MATCH_M:
            built.append((ALICE_GRIFFITH[j], row, float(d.iloc[j])))
    if {a["permit"] for a, _, _ in built} != {a["permit"] for a in ALICE_GRIFFITH}:
        raise SystemExit("not every Alice Griffith permit matched a footprint")
    built_union = shapely.union_all([r.geometry for _, r, _ in built])

    # Height zones (minus tower zones and mid-block breaks), per block and height.
    pieces: dict[tuple, object] = {}
    for z in fig["zones"]:
        g = z["px"].difference(tower_union).difference(breaks).difference(fig["park_or_parcel"])
        if g.area < 1:
            continue
        hood, num, i = ("Candlestick Center", z["parcel"], -1) if "parcel" in z else name_of(z["px"])
        key = (hood, num, z["height_ft"]) if num else (None, f"#{i}", z["height_ft"])
        pieces[key] = shapely.union_all([pieces[key], g]) if key in pieces else g

    raw_area = trimmed = 0.0
    features = []
    dropped_built = []
    add7 = f"{ADD7['title']}, {FIG5['figure']}, p. {FIG5['printed_page']}"

    def finish(g_px):
        nonlocal raw_area, trimmed
        g = to_utm(g_px)
        raw_area += g.area
        inside = g.intersection(site)
        trimmed += g.area - inside.area
        inside = inside.buffer(0.25, join_style="mitre").buffer(-0.25, join_style="mitre").simplify(0.4)
        inside = trace.as_multipolygon(shapely.make_valid(inside))
        return trace.as_multipolygon(shapely.MultiPolygon([p for p in inside.geoms if p.area >= 15]))

    def label_for(hood, num):
        if hood == "Candlestick Center":
            return f"Candlestick Center parcel {num}", f"CC-{num}"
        if hood and num:
            short = {"Alice Griffith": "AG", "Candlestick North": "CN", "Candlestick South": "CS"}[hood]
            return f"{hood} block {num}", f"{short}-{num}"
        return "Development block", None

    def order(k):
        hood, num, h = k
        m = re.match(r"(\d*)(\w*)", num or "")
        return (hood or "~", int(m.group(1)) if m.group(1) else 0, m.group(2), h)

    for key in sorted(pieces, key=order):
        hood, num, h = key
        geom = finish(pieces[key])
        if geom.is_empty:
            continue
        if geom.intersects(built_union) and geom.intersection(built_union).area > 0.15 * geom.area:
            dropped_built.append(label_for(hood, num)[0])
            continue
        geom = trace.as_multipolygon(shapely.make_valid(geom.difference(built_union)))
        label, block = label_for(hood, num)
        center = hood == "Candlestick Center"
        props = {
            "kind": "block",
            "block": block,
            "label": label,
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": None,
            "base_ft": 0,
            "use": "R&D, office and mixed use (Innovation District)" if center else None,
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: drawn to the {h}-ft height limit traced from {add7}"
                      + (f"; parcel letter from D4D Figure A5.3N ({A53N['printed_page']})" if center
                         else f"; block number from D4D Figure 4.1 (p. {FIG_4_1['printed_page']})" if num else ""),
        }
        if (hood, num) in unassigned:
            letters = unassigned[(hood, num)]
            props["note"] = (f"Part of this block is hatched as an allowable tower zone, but Figure 5 doesn't say whether it "
                             f"belongs to tower {', '.join(letters[:-1])} or {letters[-1]}, whose limits differ, so it is "
                             f"drawn at the block's base height.")
        if center:
            props["note"] = ("Under the 2024 Innovation District alternative (D4D Section A5.3), which applies if it is "
                             "chosen for the whole Center; otherwise the 2019 limits of 85-120 ft apply.")
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(geom))})

    # The park-or-parcel block: outline only.
    geom = finish(fig["park_or_parcel"].difference(breaks))
    hood, num, _ = name_of(fig["park_or_parcel"])
    label, block = label_for(hood, num)
    if not block:
        label = "Park or development block"
    features.append({"type": "Feature", "properties": {
        "kind": "block", "block": block, "label": label, "stage": "entitled", "height_ft": None, "podium_ft": None,
        "base_ft": 0, "use": None, "phase": None, "illustrative": True,
        "source": f"illustrative: outline traced from {add7} (\"40 Feet if Park, 65 Feet, if Development Parcel\")",
        "note": ("Outlined only: 40 ft if it becomes a park, otherwise a development parcel (65 ft in the 2024 map; "
                 "85 ft in the D4D's Figure 4.3)."),
    }, "geometry": mapping(tb.to_wgs(geom))})

    # Tower zones.
    for tz in sorted(tower_zones, key=lambda z: (z["tower"]["letter"], z["shared"] is not None)):
        t = tz["tower"]
        letter = t["letter"]
        height, podium_table = table[letter]
        fixed = t["kind"] == "fixed"
        if fixed:
            # A fixed tower's symbol straddles zone colours; its podium is Table 4.2's.
            base_parts = [(podium_table, tz["px"])]
        else:
            # A hatched zone's podium is the block height under it (tower D's zone sits on both its
            # 65-ft Gilman side and its 85-ft Harney side, as Table 4.2 says).
            base_parts = []
            for hz in sorted({z["height_ft"] for z in fig["zones"]}):
                region = shapely.union_all([z["px"].intersection(tz["px"]) for z in fig["zones"] if z["height_ft"] == hz])
                if region.area > 0.5:
                    base_parts.append((hz, region))
            expected = {65, 85} if letter == "D" else {podium_table}
            if {hz for hz, _ in base_parts} != expected:
                raise SystemExit(f"tower {letter}: Figure 5 podiums {[hz for hz, _ in base_parts]}, Table 4.2 expects {expected}")
        for hz, region in base_parts:
            geom = finish(region)
            if geom.is_empty:
                continue
            hood, num, _ = name_of(tz["px"])
            where, block = label_for(hood, num)
            if tz["shared"]:
                lbl = f"Tower {' or '.join(tz['shared'])} zone"
                note = (f"Part of the allowable zone of tower {' or '.join(tz['shared'])} (Figure 5 doesn't say which; "
                        f"both allow {height} ft over a {hz}-ft podium). One tower may rise anywhere in its zone, so its "
                        f"location is flexible.")
            elif fixed:
                lbl = f"Tower {letter}"
                note = (f"Fixed tower location (D4D Table 4.2): up to {height} ft over a {hz}-ft podium. The footprint is "
                        f"Figure 5's tower symbol, not a building design.")
            else:
                lbl = f"Tower {letter} zone"
                note = (f"Allowable tower zone (D4D Table 4.2): one tower up to {height} ft over a {hz}-ft podium may rise "
                        f"anywhere in this zone, so its location is flexible.")
            features.append({"type": "Feature", "properties": {
                "kind": "block", "block": block, "label": lbl, "stage": "entitled", "height_ft": height,
                "podium_ft": hz, "base_ft": 0, "use": None, "phase": None, "illustrative": True,
                "source": (f"illustrative: {'symbol' if fixed else 'zone'} traced from {add7}; tower {letter}: "
                           f"{height} ft overall, {podium_table}-ft podium"
                           + (" (85 ft fronting Harney Way)" if letter == "D" else "")
                           + f" in {D4D['title']}, Table 4.2, p. {TABLE_4_2['printed_page']}"
                           + (f"; in {where}" if block else "")),
                "note": note,
            }, "geometry": mapping(tb.to_wgs(geom))})

    # Built buildings.
    for a, row, dist in sorted(built, key=lambda br: (br[0]["address"], br[2])):
        permit = f"DBI permit {a['permit']} ({PERMIT_URL.format(a['permit'])}): {a['stories']} stories, {a['homes']} homes, complete {a['completed']}"
        h_src = row["height_from"]
        features.append({"type": "Feature", "properties": {
            "kind": "building", "block": None, "label": f"Alice Griffith, {a['address']}", "stage": "complete",
            "height_ft": None, "podium_ft": None, "base_ft": 0, "use": "Residential (Alice Griffith replacement housing)",
            "phase": "Alice Griffith", "illustrative": False,
            "source": (f"footprint: OpenStreetMap {row['osm']} via Overture {config.OVERTURE_RELEASE}, matched to the nearest "
                       f"permit address point ({dist:.0f} m away); stories: {permit}"),
            "stories": a["stories"],
            "note": (f"Built: {a['stories']} stories (DBI). No height is drawn: "
                     + ("the footprint has no mapped height." if row["height"] != row["height"] else
                        f"its mapped height ({row['height']:.1f} m{', a ' + h_src + ' estimate' if h_src != 'OpenStreetMap' else ''}) "
                        "doesn't fit the permitted stories.")
                     + (" Matched to this permit by distance: it may be a separate wing of the same development."
                        if dist > 20 else "")),
        }, "geometry": mapping(tb.to_wgs(shapely.make_valid(row.geometry.simplify(0.3))))})

    check = {"zones_m2": round(raw_area), "outside_site_m2": round(trimmed), "outside_site_share": round(trimmed / raw_area, 4)}
    print(f"[candlestick] {check['outside_site_m2']} m2 ({check['outside_site_share']:.1%}) fell outside the site and was trimmed")
    if check["outside_site_share"] > 0.03:
        raise SystemExit("too much of the traced massing falls outside the site boundary; check the georeference")
    unnamed = [f for f in features if f["properties"]["kind"] == "block" and not f["properties"]["block"]]
    print(f"[candlestick] {len(features)} features; {len(unnamed)} blocks without a Figure 4.1 number; "
          f"built blocks drawn as buildings: {sorted(set(dropped_built))}")

    massing_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each block is drawn to its height limit in the 2024 height map (40-180 ft), not "
                "as a building design. The 11 towers (170-420 ft) are drawn over a 65- or 85-ft podium: six at fixed "
                "spots and five as zones they may rise anywhere in. Candlestick Center shows the 2024 Innovation "
                "District alternative. The Alice Griffith homes already built are footprints with their permitted "
                "stories but no height; the State Recreation Area, parks and streets aren't massed."
            ),
            "note": ("Blocks and tower zones are drawn to their height limits, not as building designs; real buildings "
                     "will be smaller, and tower locations are flexible."),
            "sourceUrl": D4D["url"],
            "sourceLabel": "Design for Development, 2024 (PDF)",
            "georeference": {"figure_5": report, "check_against_site": check},
            "documents": {
                "height_map": {"title": ADD7["title"], "url": ADD7["url"], "sha256": ADD7["sha256"],
                               "pages": f"Fig. 5 p. {FIG5['printed_page']} (PDF p. {FIG5['page_index'] + 1}); "
                                        f"no change outside Candlestick Center, PDF p. {ADD7_NO_CHANGE_PAGE + 1}"},
                "design_for_development": {"title": D4D["title"], "url": D4D["url"], "sha256": D4D["sha256"],
                                           "pages": f"Table 4.2 p. {TABLE_4_2['printed_page']}, Fig. 4.1 p. "
                                                    f"{FIG_4_1['printed_page']}, Fig. A5.3N ({A53N['printed_page']})"},
                "center_counts": {"title": "Planning Commission packet, Sept 12, 2024 (case 2007.0946GPRCWP-04)",
                                  "url": PC_PACKET, "pages": "PDF p. 6",
                                  "finding": "Candlestick Center: four parcels to 180 ft, five to 160, three to 120, two to 85."},
                "alice_griffith_permits": [PERMIT_URL.format(a["permit"]) for a in ALICE_GRIFFITH],
            },
            "license": "Block shapes: traced from public OCII documents. Georeferenced to SF's parcel map (DataSF, "
                       "ODC PDDL). Building footprints: OpenStreetMap contributors (ODbL 1.0), via Overture Maps.",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tb._round(massing_fc), indent=1) + "\n")
    print(f"[candlestick] wrote {path.relative_to(config.ROOT)} ({len(features)} features, {path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
