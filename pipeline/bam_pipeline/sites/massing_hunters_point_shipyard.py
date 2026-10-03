"""Hunters Point Shipyard Phase 2: block height limits traced from the adopted Design for Development.

Sources:
- Hunters Point Shipyard Phase 2 Design for Development (D4D), October 15, 2018 edition, the
  "HUNTERS POINT SHIPYARD PHASE 2 DESIGN FOR DEVELOPMENT" in OCII's CP-HPS2 document library. It is
  the 2018 replacement D4D (Planning Commission Resolution 20165, Apr 26, 2018). Figure 4.4c
  "Maximum Building Height", printed p. 61 (PDF page 67). Standard 4.4.1: "Maximum height
  requirements are established for all development blocks, as illustrated in Figure 4.4c."
  Its legend: 40, 55, 65, 75, 85, 100 and 120 ft, plus "370 ft. (Tower A)" and "270 ft. (Tower B)".
- Tower controls, D4D Section 4.9 (p. 92): towers stand in the flexible tower zones on Blocks 15
  and 23, at least 160 ft apart, with floor plates of at most 12,500 sq ft; Standard 4.3.1 allows
  more than 120 ft only on "blocks 15 and 23" (Section 4.9.3 and Figure 4.9a print the
  second tower block as "33"; Figure 4.4c puts Tower B on Block 23, which is drawn here). Standard
  4.3.1 is on printed p. 59.
- The 370-ft ceiling: Hunters Point Shipyard Redevelopment Plan as amended Nov 14, 2024, Sec.
  II.D.4, printed p. 23 (PDF page 28): "No building may exceed 370 feet in height", with heights
  "prescribed in the ... Hunters Point Shipyard Phase 2 Design for Development".
- Still current: the 2024 actions amended the Candlestick Point D4D, not this one (OCII
  Commission memo, Sept 3, 2024, p. 4, list of resolutions), and EIR Addendum 7 (Aug 2024, p. 33)
  says the R&D/office transfer to Candlestick "would not result in an increase in the area of
  development or building heights at HPS2 from what is already approved". The module checks
  the redevelopment plan's text.

What this is and isn't:
- Each development block is drawn to its height limit, not as a building design; real buildings
  will be smaller and broken by mid-block breaks, stepbacks and coverage limits (D4D 4.3, 4.4.2),
  so the massing is labelled illustrative.
- Towers A (370 ft) and B (270 ft) are drawn where Figure 4.4c shows them, over the 85-ft limit of
  the rest of their blocks. The D4D lets each tower stand anywhere in its block's flexible tower
  zone, so the position is illustrative too.
- Parks and open space (Northside Park, the Green Room, the Water Room, the shoreline parks) carry
  no height colour in the figure and aren't massed. Neither are the Phase 1 hilltop (outside the
  site) or the Navy-era buildings the plan keeps (they stay in the base map).
- Nothing has been built: OCII's FY 2023-24 housing report (p. 6) says Phase 2 is a Superfund site
  "still owned by the Navy" and "No construction is currently occurring on any of the HPSY Phase II
  parcels", so every block is "entitled". OCII's Sept 3, 2024 commission memo (pp. 10-11) reports
  the Navy's expectation that the land, except Parcel F, is conveyed in 2036-2038.
- Blocks are not clipped to the site outline: the D4D draws Blocks 1, 5 and 6 partly on land the
  zoning map puts in the Phase 1 height district (HP-RA) or, at Block 1's west end, 40-X. They are
  drawn as the D4D shows them, with a note.

Georeferencing: Figure 4.4c is vector art, rendered at 300 dpi. Its street network (the white
road fills) is aligned to OpenStreetMap roads (via Overture): a raster correlation over scale and
rotation finds the start, then a trimmed ICP refines it. The streets the plan keeps (Crisp Road,
Spear Avenue, Lockwood and Donahue Streets) and the built Phase 1 streets carry the fit; the plan's
new streets have no counterpart yet and drop out as outliers. As a check, the traced blocks are
compared with the official HP height district (the site boundary): what falls outside is
reported and trimmed.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_hunters_point_shipyard
"""

from __future__ import annotations

import json
import re

import cv2
import geopandas as gpd
import numpy as np
import pdfplumber
import shapely
import shapely.affinity
from shapely.geometry import Point, Polygon, mapping

from .. import config, trace
from . import traced_boundaries as tb

PROJECT_ID = "hunters-point-shipyard"
UTM = tb.UTM

D4D = {
    "title": "Hunters Point Shipyard Phase 2 Design for Development (Oct 15, 2018; OCII)",
    "url": "https://sfocii.org/sites/default/files/inline-files/1.%20HUNTERS%20POINT%20SHIPYARD%20PHASE%202%20DESIGN%20FOR%20DEVELOPMENT.pdf",
    "sha256": "0e0f0f99d47888427c9ceb640ef4de65d19a1bce5f9a47f71d70cda0ef6bfeac",
    "file": "hps-phase2-d4d-2018.pdf",
}
FIG = {"page_index": 66, "printed_page": "61", "figure": "Figure 4.4c, Maximum Building Height"}
REDEV_PLAN = {
    "title": "Hunters Point Shipyard Redevelopment Plan (as amended Nov 14, 2024; OCII)",
    "url": "https://sfocii.org/sites/default/files/2025-10/2024%20Hunters%20Point%20Shipyard%20Redevelopment%20Plan.pdf",
    "sha256": "4842f6211a6c67d9057a009b5982d48cb0906c9bae0d65af74888201c63d6aea",
    "file": "hps-redevelopment-plan-2024.pdf",
    "page_index": 27,
    "printed_page": "23",
}
HOUSING_REPORT = "OCII Annual Housing Production Report FY 2023-24, p. 6"
OCII_MEMO = "OCII Commission memo, Sept 3, 2024 (2024 Modified Project Variant), pp. 10-11"

DPI = 300
PT_TO_PX = DPI / 72
IMAGE_SIZE = (3301, 2550)  # rows, columns of the render
MAP_BOX_PT = (55, 109, 557, 718)  # the map frame (left, top, right, bottom in PDF points)
LEGEND_BOX_PT = (66, 562, 381, 720)  # the legend panel inside the frame

# Height fills as the map draws them (RGB 0-1 as stored in the PDF). The legend swatches are a
# little darker; each map fill is checked to sit nearest its own swatch below.
MAP_FILLS = {
    40: (1.0, 0.957, 0.557), 55: (0.941, 0.776, 0.184), 65: (0.604, 0.812, 0.553), 75: (0.282, 0.522, 0.486),
    85: (0.592, 0.851, 0.922), 100: (0.231, 0.463, 0.737), 120: (0.173, 0.302, 0.475),
}
LEGEND_FILLS = {  # legend swatches, top to bottom (RGB 0-1 as stored)
    40: (1.0, 0.91, 0.478), 55: (0.957, 0.773, 0.086), 65: (0.588, 0.808, 0.541), 75: (0.165, 0.51, 0.467),
    85: (0.545, 0.835, 0.906), 100: (0.0, 0.482, 0.757), 120: (0.039, 0.275, 0.439),
}
MAX_COLOUR_DIST = 15  # RGB 0-255: the fills are flat; blends at hatching and gradients take the nearest fill
LOOSE_COLOUR_DIST = 32  # fills with their anti-aliased edges, for telling blocks apart
MIN_ZONE_PX = 600  # about 300 m2: smaller height patches are anti-aliasing, not zones
BRIDGE_PX = 11  # closing within one block: hatching, outlines and stepback marks (not streets between blocks)

# The two tower footprints in the figure (dark fills, RGB 0-1 as stored), cut by the hatching.
TOWERS = {
    "A": {"rgb": (0.133, 0.125, 0.039), "block": "15", "height_ft": 370},
    "B": {"rgb": (0.106, 0.212, 0.243), "block": "23", "height_ft": 270},
}
TOWER_BASE_FT = 85
TOWER_FLOORPLATE_SQFT = 12_500
SQFT_M2 = 0.09290304

BLOCK_LABEL = re.compile(r"\d{1,2}[AB]?")
# Blocks the D4D draws partly outside the HP height district (see the check in main()).
OVERHANG_BLOCKS = {"1", "5", "6"}
# Labelled in the figure but drawn without a height fill: the Green Room, an eight-acre park (D4D 3.5).
OPEN_SPACE_BLOCKS = {"39"}
# Rough figure scale from the scale bar (0-900 ft over about 88.6 pt): start of the search only.
SCALE_SEARCH = np.arange(0.62, 0.86, 0.01)  # metres per pixel at 300 dpi
ROTATION_SEARCH_DEG = np.arange(-4, 4.1, 0.5)
STREETS_BBOX = (-122.392, 37.712, -122.352, 37.735)
ICP_KEEP = 0.5


# ---------------------------------------------------------------- documents

def check_height_ceiling() -> None:
    """The redevelopment plan must still cap heights at 370 ft and defer to the Phase 2 D4D."""
    import pypdfium2 as pdfium

    path = trace.fetch_document(REDEV_PLAN["url"], tb.DOCS / REDEV_PLAN["file"], REDEV_PLAN["sha256"])
    text = " ".join(pdfium.PdfDocument(str(path))[REDEV_PLAN["page_index"]].get_textpage().get_text_range().split())
    if "No building may exceed 370 feet in height" not in text or "Phase 2 Design for Development" not in text:
        raise SystemExit("the redevelopment plan's height limit is not where expected; review before drawing")


def _render(pdf_path) -> np.ndarray:
    import pypdfium2 as pdfium

    page = pdfium.PdfDocument(str(pdf_path))[FIG["page_index"]]
    rgb = np.asarray(page.render(scale=PT_TO_PX).to_pil().convert("RGB"))
    if rgb.shape[:2] != IMAGE_SIZE:
        raise SystemExit(f"unexpected Figure 4.4c render size {rgb.shape}")
    return rgb


def _in_box(x, y, box) -> bool:
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


def read_figure(pdf_path) -> tuple[dict[str, Point], dict[str, Polygon], dict[str, Polygon]]:
    """Block labels (centres and glyph boxes) and the two tower footprints, in render pixels."""
    with pdfplumber.open(pdf_path, pages=[FIG["page_index"] + 1]) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
        if "Maximum Building Height" not in text or "370 ft. (Tower A)" not in text or "270 ft. (Tower B)" not in text:
            raise SystemExit("Figure 4.4c's legend is not where expected")
        # Block numbers: DIN Demi at about 10.5 pt, rotated with the street grid.
        chars = [c for c in page.dedupe_chars().chars
                 if c["fontname"].endswith("DIN2014-Demi") and 10.3 < c["size"] < 10.9
                 and _in_box(c["x0"], c["top"], MAP_BOX_PT) and not _in_box(c["x0"], c["top"], LEGEND_BOX_PT)]
        labels: dict[str, Point] = {}
        glyphs: dict[str, Polygon] = {}
        run: list[dict] = []

        def flush():
            if run:
                t = "".join(c["text"] for c in run)
                xs = [v for c in run for v in (c["x0"], c["x1"])]
                ys = [v for c in run for v in (c["top"], c["bottom"])]
                if BLOCK_LABEL.fullmatch(t):
                    labels[t] = Point((min(xs) + max(xs)) / 2 * PT_TO_PX, (min(ys) + max(ys)) / 2 * PT_TO_PX)
                    glyphs[t] = shapely.union_all([shapely.box(c["x0"] * PT_TO_PX, c["top"] * PT_TO_PX, c["x1"] * PT_TO_PX,
                                                               c["bottom"] * PT_TO_PX) for c in run])

        for c in chars:
            if run and np.hypot(c["x0"] - run[-1]["x0"], c["top"] - run[-1]["top"]) > 7.5:
                flush()
                run = []
            run.append(c)
        flush()

        towers = {}
        for key, t in TOWERS.items():
            parts = []
            for o in page.curves + page.rects:
                col = o.get("non_stroking_color")
                if not o.get("fill") or not isinstance(col, (list, tuple)) or len(col) != 3:
                    continue
                if max(abs(a - b) for a, b in zip(col, t["rgb"])) > 0.004 or not o.get("pts") or len(o["pts"]) < 3:
                    continue
                g = shapely.make_valid(Polygon(o["pts"]))
                if g.area > 0:
                    parts.append(g)
            if not parts:
                raise SystemExit(f"no Tower {key} fill in Figure 4.4c")
            # The hatching cuts each footprint into strips; the footprint is their hull.
            towers[key] = shapely.affinity.scale(shapely.union_all(parts).convex_hull, PT_TO_PX, PT_TO_PX, origin=(0, 0))
    expected = {str(n) for n in range(1, 57) if n != 36} | {"36A", "36B"}
    if set(labels) != expected:
        raise SystemExit(f"Figure 4.4c block labels: missing {sorted(expected - set(labels))}, "
                         f"unexpected {sorted(set(labels) - expected)}")
    return labels, glyphs, towers


# ---------------------------------------------------------------- georeference

def road_pixels(rgb: np.ndarray) -> np.ndarray:
    """Centres of the figure's white road fills (render pixels), legend and frame left out."""
    white = (rgb.min(axis=2) > 245).astype(np.uint8)
    mask = np.zeros_like(white)
    x0, y0, x1, y1 = (int(v * PT_TO_PX) for v in MAP_BOX_PT)
    mask[y0 + 6:y1 - 6, x0 + 6:x1 - 6] = 1
    lx0, ly0, lx1, ly1 = (int(v * PT_TO_PX) for v in LEGEND_BOX_PT)
    mask[ly0 - 6:ly1 + 6, lx0 - 6:lx1 + 6] = 0
    white &= mask
    n, lab, stats, _ = cv2.connectedComponentsWithStats(white, connectivity=8)
    keep = np.isin(lab, [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 4000])
    ys, xs = np.nonzero(keep)
    return np.c_[xs, ys].astype(float)


def georeference(pts: np.ndarray, roads: gpd.GeoDataFrame) -> tuple[trace.Similarity, dict]:
    res = 3.0
    X0, Y0, X1, Y1 = 553600.0, 4173400.0, 557600.0, 4177400.0
    n = int((X1 - X0) / res)
    target = np.zeros((n, n), np.float32)
    for g in roads.geometry:
        for line in getattr(g, "geoms", [g]):
            a = np.asarray(line.coords)
            px = np.c_[(a[:, 0] - X0) / res, (Y1 - a[:, 1]) / res].round().astype(np.int32)
            cv2.polylines(target, [px], False, 1.0, thickness=3)
    target = cv2.GaussianBlur(target, (0, 0), 2)

    # 1. Raster correlation over scale and rotation (translation from the correlation peak).
    sample = pts[::7]
    best = None
    for s in SCALE_SEARCH:
        for rot in np.radians(ROTATION_SEARCH_DEG):
            m = trace.Similarity(float(s), float(rot), 0.0, 0.0).apply(sample)
            lo, hi = m.min(0), m.max(0)
            w, h = int((hi[0] - lo[0]) / res) + 1, int((hi[1] - lo[1]) / res) + 1
            tmpl = np.zeros((h, w), np.float32)
            tmpl[((hi[1] - m[:, 1]) / res).astype(int), ((m[:, 0] - lo[0]) / res).astype(int)] = 1
            r = cv2.matchTemplate(target, tmpl, cv2.TM_CCORR_NORMED)
            _, score, _, loc = cv2.minMaxLoc(r)
            if best is None or score > best[0]:
                best = (score, trace.Similarity(float(s), float(rot), X0 + loc[0] * res - lo[0], Y1 - loc[1] * res - hi[1]))
    score, start = best

    # 2. Trimmed ICP of the road pixels onto the OpenStreetMap road centrelines.
    lines = shapely.union_all(roads.geometry.to_numpy())
    icp_pts = pts[::12]
    sim, d = tb.icp(icp_pts, [lines], np.zeros(len(icp_pts), int), start, keep=ICP_KEEP)
    report = tb.icp_report(sim, d, ICP_KEEP, "figure road pixels to OpenStreetMap road centrelines")
    report["method"] = ("raster correlation of the figure's road fills with OpenStreetMap roads (scale, rotation, "
                        "shift), then trimmed ICP of road pixels onto road centrelines; road pixels span the "
                        "road width, so part of the residual is half a road's width")
    report["correlation"] = round(float(score), 3)
    report.pop("controls", None)
    return sim, report


# ---------------------------------------------------------------- tracing

def _palette_check() -> None:
    for h, c in MAP_FILLS.items():
        near = min(LEGEND_FILLS, key=lambda k: np.linalg.norm(np.subtract(LEGEND_FILLS[k], c)))
        if near != h:
            raise SystemExit(f"the {h}-ft map fill is nearer the {near}-ft legend swatch")


def _polys(mask: np.ndarray):
    contours, hier = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hier is None:
        return Polygon()
    polys = []
    for i, c in enumerate(contours):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < 300:
            continue
        holes = []
        child = hier[0][i][2]
        while child != -1:
            if cv2.contourArea(contours[child]) >= 300:
                holes.append(contours[child].reshape(-1, 2) + 0.5)
            child = hier[0][child][0]
        polys.append(shapely.make_valid(Polygon(c.reshape(-1, 2) + 0.5, holes)))
    return shapely.union_all(polys) if polys else Polygon()


def trace_blocks(rgb: np.ndarray, labels: dict[str, Point], glyphs: dict[str, Polygon],
                 towers_px: dict[str, Polygon]) -> list[dict]:
    """Height zones per block, in render pixels.

    Pixels take the nearest height fill colour. Coloured regions split by the black block outlines
    are the blocks; each takes the label inside it, and unlabelled pieces (strips between the tower
    zone hatching, a cap cut off by a line) join the labelled region they touch. Inside a block,
    text, hatching and outline pixels take the height of the nearest fill.
    """
    _palette_check()
    heights = list(MAP_FILLS)
    pal = np.array([MAP_FILLS[h] for h in heights], float) * 255
    dist = np.linalg.norm(rgb[:, :, None, :].astype(float) - pal[None, None], axis=3)
    # Strict: pixels that are a flat fill (they carry the heights). Loose: fills and their
    # anti-aliased edges, e.g. the narrow strips between tower-zone hatching (they carry the blocks).
    cls = np.where(dist.min(axis=2) <= MAX_COLOUR_DIST, dist.argmin(axis=2), -1)
    loose = dist.min(axis=2) <= LOOSE_COLOUR_DIST
    x0, y0, x1, y1 = (int(v * PT_TO_PX) for v in MAP_BOX_PT)
    lx0, ly0, lx1, ly1 = (int(v * PT_TO_PX) for v in LEGEND_BOX_PT)
    frame = np.zeros(cls.shape, bool)
    frame[y0:y1, x0:x1] = True
    frame[ly0:ly1, lx0:lx1] = False
    cls[~frame] = -1
    coloured = cv2.morphologyEx((loose & frame).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cls[coloured == 0] = -1

    n, comp, stats, _ = cv2.connectedComponentsWithStats(coloured, connectivity=4)
    owner: dict[int, str] = {}
    for name, pt in labels.items():
        # The label's own glyphs are holes in the fill: look in a small window around it.
        x, y = int(pt.x), int(pt.y)
        ids, counts = np.unique(comp[y - 25:y + 26, x - 25:x + 26], return_counts=True)
        cands = [(c, i) for i, c in zip(ids, counts) if i != 0]
        if not cands:
            if name in OPEN_SPACE_BLOCKS:
                continue
            raise SystemExit(f"block {name}'s label sits on no height fill")
        if name in OPEN_SPACE_BLOCKS:
            raise SystemExit(f"block {name} has a height fill; it was expected to be open space")
        owner.setdefault(int(max(cands)[1]), name)
    # Unlabelled pieces join a labelled region within a line's width (not across a street).
    grow = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    pending = [i for i in range(1, n) if i not in owner and stats[i, cv2.CC_STAT_AREA] >= 40]
    for _ in range(60):
        left = []
        for i in pending:
            x, y, w, h = stats[i, :4]
            sl = (slice(max(y - 8, 0), y + h + 8), slice(max(x - 8, 0), x + w + 8))
            ring = cv2.dilate((comp[sl] == i).astype(np.uint8), grow) > 0
            near = [owner[int(j)] for j in np.unique(comp[sl][ring]) if int(j) in owner]
            if near:
                owner[i] = max(set(near), key=near.count)
            else:
                left.append(i)
        if len(left) == len(pending):
            break
        pending = left
    big_orphans = [i for i in pending if stats[i, cv2.CC_STAT_AREA] > 3000]
    if big_orphans:
        raise SystemExit(f"{len(big_orphans)} coloured regions belong to no labelled block")

    # Block extents: each block's fills plus its label glyphs (some are white) and tower fill,
    # closed (bridging hatching, outlines and the stepback marks on its edges) with holes filled.
    names = sorted(set(owner.values()), key=_block_order)
    lut = np.zeros(n, np.int32)
    for i, o in owner.items():
        lut[i] = names.index(o) + 1
    seed = lut[comp]
    extra: dict[str, list] = {nm: [glyphs[nm]] for nm in names}
    for k, t in TOWERS.items():
        extra[t["block"]].append(towers_px[k])
    # Each block's own marks (its label glyphs, its tower), so a neighbour's hull can't take them.
    marks = np.zeros(seed.shape, np.int32)
    for bi, nm in enumerate(names, start=1):
        for g in extra[nm]:
            for q in getattr(g, "geoms", [g]):
                cv2.fillPoly(marks, [np.asarray(q.exterior.coords).round().astype(np.int32)], bi)
    block_img = np.zeros(seed.shape, np.int32)
    # Black outlines and hatching, and the navy stepback marks; not the grey road casings.
    hi, lo = rgb.max(axis=2).astype(int), rgb.min(axis=2).astype(int)
    dark = (hi < 45) | ((hi < 75) & (hi - lo > 12))
    pad = 20
    # Small blocks first: a block notched into a bigger one (36B in 36A) keeps its own ground.
    for b in sorted(range(1, len(names) + 1), key=lambda i: int((seed == i).sum())):
        ys, xs = np.nonzero(seed == b)
        y0_, y1_, x0_, x1_ = max(ys.min() - pad, 0), ys.max() + pad, max(xs.min() - pad, 0), xs.max() + pad
        win = (slice(y0_, y1_), slice(x0_, x1_))
        m = ((seed[win] == b) | (marks[win] == b)).astype(np.uint8)
        # Black ink inside the block's hull: outlines, hatching, the stepback marks on its edges.
        hull = np.zeros_like(m)
        cv2.fillConvexPoly(hull, cv2.convexHull(np.c_[xs - x0_, ys - y0_].astype(np.int32)), 1)
        hull = cv2.dilate(hull, np.ones((9, 9), np.uint8))  # marks at a corner sit just outside the fill
        m |= (hull > 0) & dark[win] & (seed[win] == 0) & ((marks[win] == 0) | (marks[win] == b))
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (BRIDGE_PX, BRIDGE_PX)))
        contours, _ = cv2.findContours(m * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        m[:] = 0
        cv2.drawContours(m, contours, -1, 1, cv2.FILLED)
        view = block_img[win]
        view[(m > 0) & (view == 0) & ((seed[win] == 0) | (seed[win] == b))] = b
    # Inside a block, every pixel takes the height of the block's nearest flat fill pixel.
    zones = []
    for b, name in enumerate(names, start=1):
        ys, xs = np.nonzero(block_img == b)
        crop = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
        in_block = block_img[crop] == b
        hs = (cls[crop] >= 0) & (seed[crop] == b)
        while True:
            _, nearest = cv2.distanceTransformWithLabels((~hs).astype(np.uint8), cv2.DIST_L2, 5,
                                                         labelType=cv2.DIST_LABEL_PIXEL)
            height = cls[crop].ravel()[np.flatnonzero(hs.ravel())[nearest.ravel() - 1]].reshape(in_block.shape)
            ks, counts = np.unique(height[in_block], return_counts=True)
            small = [k for k, c in zip(ks, counts) if c < MIN_ZONE_PX]
            if not small or len(small) == len(ks):
                break
            # A speck of another colour (anti-aliasing at a label) takes the block's own height.
            hs &= ~np.isin(cls[crop], small)
        for k in np.unique(height[in_block]):
            part = (in_block & (height == k)).astype(np.uint8)
            part = cv2.morphologyEx(part, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)) > 0
            geom = _polys(part)
            if not geom.is_empty:
                geom = shapely.affinity.translate(geom, xs.min(), ys.min())
                zones.append({"block": name, "height_ft": heights[int(k)], "px": geom})
    return zones


# ---------------------------------------------------------------- main

def _block_order(name: str) -> tuple:
    m = re.match(r"(\d+)([AB]?)", name)
    return int(m.group(1)), m.group(2)


def main() -> None:
    check_height_ceiling()
    pdf_path = trace.fetch_document(D4D["url"], tb.DOCS / D4D["file"], D4D["sha256"])
    rgb = _render(pdf_path)
    labels, glyphs, towers_px = read_figure(pdf_path)

    roads = tb.streets("hunters_point_shipyard", STREETS_BBOX)
    roads = roads[roads["subtype"] == "road"]
    sim, report = georeference(road_pixels(rgb), roads)
    print(f"[{PROJECT_ID}] Figure 4.4c georeference: trimmed RMS {report['rms_m']} m (median {report['median_m']} m) "
          f"over {report['points']} road pixels, scale {report['scale_m_per_unit']} m/px, "
          f"rotation {report['rotation_deg']} deg, correlation {report['correlation']}")

    site = gpd.read_file(config.ROOT / "data" / "boundaries" / f"{PROJECT_ID}.geojson").to_crs(UTM)
    site_utm = site[site["kind"] == "site"].geometry.iloc[0]

    zones = trace_blocks(rgb, labels, glyphs, towers_px)
    towers = {}
    for key, px in towers_px.items():
        g = sim.geometry(px)
        block = TOWERS[key]["block"]
        if px.distance(shapely.union_all([z["px"] for z in zones if z["block"] == block])) > 15:
            raise SystemExit(f"Tower {key} does not sit on Block {block}")
        towers[key] = g
        print(f"[{PROJECT_ID}] Tower {key} on Block {block}: {g.area / SQFT_M2:,.0f} sq ft as drawn "
              f"(floor plates up to {TOWER_FLOORPLATE_SQFT:,} sq ft)")
    tower_cut = shapely.union_all(list(towers.values()))

    merged: dict[tuple[str, int], object] = {}
    for z in zones:
        key = (z["block"], z["height_ft"])
        g = shapely.make_valid(sim.geometry(z["px"]))
        merged[key] = shapely.union_all([merged[key], g]) if key in merged else g

    # Check against the site (the HP height district). Blocks are not clipped to it: the 2018 D4D
    # draws Blocks 1, 5 and 6 partly on land the zoning map still puts in Phase 1's HP-RA district
    # (and, at the west end of Block 1, a 40-X district). Any other block outside the site points
    # to a georeferencing error.
    by_block: dict[str, list[float]] = {}
    for (block, _), g in merged.items():
        a = by_block.setdefault(block, [0.0, 0.0])
        a[0] += g.area
        a[1] += g.difference(site_utm).area
    outside = {b: round(o / a, 3) for b, (a, o) in by_block.items() if o / a > 0.005}
    total = sum(a for a, _ in by_block.values())
    check = {
        "blocks_m2": round(total),
        "outside_site_m2": round(sum(o for _, o in by_block.values())),
        "outside_share_by_block": outside,
        "note": "Blocks are drawn as the D4D draws them, not clipped to the site. Blocks 1, 5 and 6 reach onto "
                "land the zoning map puts in the Phase 1 height district (HP-RA) or a 40-X district.",
    }
    print(f"[{PROJECT_ID}] {len(merged)} height zones; outside the HP height district: "
          + ", ".join(f"Block {b} {s:.0%}" for b, s in outside.items()))
    stray = {b: s for b, s in outside.items() if b not in OVERHANG_BLOCKS and s > 0.06}
    if stray:
        raise SystemExit(f"blocks fall outside the site {stray}; check the georeference")

    fig = f"{D4D['title']}, {FIG['figure']}, p. {FIG['printed_page']}"
    features = []
    for (block, h) in sorted(merged, key=lambda k: (_block_order(k[0]), k[1])):
        geom = merged[(block, h)]
        if block in {t["block"] for t in TOWERS.values()}:
            geom = geom.difference(tower_cut)
        # Pixel-traced: 0.6 m takes out the pixel staircase (the fit itself is good to a few metres).
        geom = geom.buffer(0.3, join_style="mitre").buffer(-0.3, join_style="mitre").simplify(0.6)
        geom = trace.as_multipolygon(shapely.make_valid(geom))
        geom = trace.as_multipolygon(shapely.MultiPolygon([p for p in geom.geoms if p.area >= 40]))
        if geom.is_empty:
            continue
        props = {
            "kind": "block",
            "block": block,
            "label": f"Block {block}",
            "stage": "entitled",
            "height_ft": h,
            "podium_ft": None,
            "base_ft": 0,
            "use": None,
            "phase": None,
            "illustrative": True,
            "source": f"illustrative: drawn to the {h}-ft height limit traced from {fig}",
        }
        if block == "45" and h == 120:
            props["note"] = ("Above 85 ft, a residential building on Block 45 may cover at most 30,000 sq ft "
                             "(D4D Standard 4.3.1, p. 59).")
        elif block in OVERHANG_BLOCKS:
            props["note"] = ("The D4D draws this block partly outside the Phase 2 height district on the zoning map "
                             "(the site outline here), on land zoned for Phase 1 (HP-RA)"
                             + (" or 40-X" if block == "1" else "") + ". It is drawn as the D4D shows it.")
        elif block == "36B":
            props["note"] = ("Block 36B is the identified fire station lot, which the D4D exempts from its height "
                             "limit (Fig. 4.0a note, p. 45); drawn to the figure's limit.")
        features.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(geom))})

    for key, g in towers.items():
        t = TOWERS[key]
        geom = trace.as_multipolygon(shapely.make_valid(g.simplify(0.3)))
        features.append({"type": "Feature", "properties": {
            "kind": "block",
            "block": t["block"],
            "label": f"Tower {key}, Block {t['block']}",
            "stage": "entitled",
            "height_ft": t["height_ft"],
            "podium_ft": TOWER_BASE_FT,
            "base_ft": 0,
            "use": None,
            "phase": None,
            "illustrative": True,
            "source": (f"illustrative: drawn to the {t['height_ft']}-ft Tower {key} limit where {fig} shows it, over the "
                       f"block's {TOWER_BASE_FT}-ft limit; tower controls, D4D Section 4.9, p. 92"),
            "note": (f"Tower {key} may stand anywhere in Block {t['block']}'s flexible tower zone (D4D Fig. 4.9a), "
                     f"with floor plates of at most {TOWER_FLOORPLATE_SQFT:,} sq ft; Towers A and B must be at least "
                     "160 ft apart. No building may exceed 370 ft (Redevelopment Plan, 2024)."),
        }, "geometry": mapping(tb.to_wgs(geom))})

    print(f"[{PROJECT_ID}] drew {len(features)} zones: "
          + ", ".join(f"{f['properties']['block']}:{f['properties']['height_ft']}" for f in features))
    blocks_drawn = {f["properties"]["block"] for f in features}
    missing = sorted(set(labels) - blocks_drawn, key=_block_order)
    print(f"[{PROJECT_ID}] labelled blocks without a height fill (open space): {missing}")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": (
                "Illustrative massing: each Phase 2 development block is drawn to its height limit in the 2018 "
                "Design for Development (Fig. 4.4c), from 40 to 120 ft, not as a building design. Two towers, "
                "370 ft and 270 ft, are drawn where the figure places them; the plan lets each move within its "
                "block. Parks and open space, the Phase 1 hilltop and the Navy-era buildings the plan keeps aren't "
                "massed. Blocks 1, 5 and 6 are drawn as the plan draws them, partly beyond the Phase 2 zoning "
                "district. Nothing has been built on Phase 2: it is a Superfund site still owned by the Navy, "
                "which expects to hand it over, except Parcel F, in 2036–2038."
            ),
            "note": ("Blocks are drawn to their height limits in the 2018 Design for Development, not as building "
                     "designs; real buildings will be smaller."),
            "sourceUrl": D4D["url"],
            "sourceLabel": "Design for Development, 2018 (PDF)",
            "georeference": {"figure_4_4c": report, "check_against_site": check},
            "documents": {
                "design_for_development": {"title": D4D["title"], "url": D4D["url"], "sha256": D4D["sha256"],
                                           "pages": "Fig. 4.4c p. 61, Std. 4.3.1 p. 59, Sec. 4.9 and Fig. 4.9a p. 92, Fig. 4.0a note p. 45"},
                "redevelopment_plan": {"title": REDEV_PLAN["title"], "url": REDEV_PLAN["url"], "sha256": REDEV_PLAN["sha256"],
                                       "finding": f"Sec. II.D.4, p. {REDEV_PLAN['printed_page']}: no building may exceed 370 ft; "
                                                  "heights are set by the Phase 2 Design for Development."},
                "status": [HOUSING_REPORT + ": Phase 2 is a Superfund site still owned by the Navy; no construction "
                           "on any Phase 2 parcel.",
                           OCII_MEMO + ": conveyance of the Shipyard Site, excluding Parcel F, expected 2036-2038."],
            },
            "license": "Block shapes: traced from a public OCII document. Georeference: " + tb.OSM_LICENSE + ".",
        },
        "features": features,
    }
    path = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".geojson.tmp")
    tmp.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    tmp.rename(path)
    print(f"[{PROJECT_ID}] wrote {path.relative_to(config.ROOT)} ({len(features)} features, "
          f"{path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
