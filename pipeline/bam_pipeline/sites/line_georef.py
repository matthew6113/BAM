"""Georeferencing helpers for line projects traced from raster figures.

Two ways to fit a figure to the ground, both ending in trace.fit_similarity so the residuals
and RMS are reported the same way as elsewhere:

- register_roads: figures drawn on a street map. Street pixels in the figure are matched to
  street centrelines (OpenStreetMap via Overture, or an agency's street layer) by trimmed ICP,
  starting from two or three hand-located control points.
- register_buildings: figures drawn on an aerial photo. Building footprints (OpenStreetMap via
  Overture) are rendered in the figure's frame and correlated with the photo: first a coarse
  search over scale and rotation (translation by template matching), then tile by tile, so each
  tile with enough buildings gives one control point (its local shift). The control points go
  through trace.fit_similarity; tiles more than 3x the median residual away are dropped and
  counted in the report.

Line helpers: colour masks, thinning (Zhang-Suen, from lines_the_portal) and column centrelines.
"""

from __future__ import annotations

import cv2
import geopandas as gpd
import numpy as np
import shapely
from pypdf import PdfReader
from shapely.geometry import LineString

from .. import trace
from . import traced_boundaries as tb
from .lines import UTM
from .lines_the_portal import _longest_path, _thin  # noqa: F401  (re-exported for the line modules)


def pdf_image(pdf_path, page_index: int, size: tuple[int, int]) -> np.ndarray:
    """The embedded raster image of a given size (width, height) on a PDF page, as RGB."""
    for im in PdfReader(pdf_path).pages[page_index].images:
        rgb = np.asarray(im.image.convert("RGB"))
        if rgb.shape[1::-1] == tuple(size):
            return rgb
    raise SystemExit(f"{pdf_path.name}: no {size[0]}x{size[1]} image on page index {page_index}")


def anchored(fig_xy, utm_xy, scale: float, rotation_deg: float) -> trace.Similarity:
    """A similarity with a given scale and rotation that maps one figure point onto one ground point."""
    sim = trace.Similarity(scale, np.radians(rotation_deg), 0.0, 0.0)
    o = sim.apply([fig_xy])[0]
    sim.tx, sim.ty = utm_xy[0] - o[0], utm_xy[1] - o[1]
    return sim


def to_figure(sim: trace.Similarity, xy) -> np.ndarray:
    """Inverse of sim.apply: projected metres -> figure pixels (y down)."""
    a = (np.linalg.inv(sim.matrix()) @ (np.asarray(xy, float).reshape(-1, 2) - [sim.tx, sim.ty]).T).T
    a[:, 1] *= -1
    return a


def footprint(sim: trace.Similarity, w: int, h: int, pad_m: float = 300) -> shapely.Polygon:
    return shapely.Polygon(sim.apply([(0, 0), (w, 0), (w, h), (0, h)])).buffer(pad_m)


# ---------------------------------------------------------------- street maps

def register_roads(street_px: np.ndarray, roads, init: trace.Similarity, keep: float = 0.6,
                   what: str = "street lines") -> tuple[trace.Similarity, dict]:
    """Trimmed ICP of figure street pixels (N x 2, x right / y down) onto street centrelines (UTM)."""
    sim, d = tb.icp(street_px, [roads], np.zeros(len(street_px), int), init, keep, iterations=80)
    rep = tb.icp_report(sim, d, keep, what)
    return sim, rep


def coarse_roads(street_mask: np.ndarray, roads, init: trace.Similarity, scale_range: float = 0.15,
                 rot_range: float = 10.0, rot_step: float = 1.0, pad: int = 150) -> tuple[trace.Similarity, float]:
    """A starting fit for register_roads when no control points are at hand: street centrelines are
    drawn in the figure's frame over a grid of scales and rotations around `init` (which only needs
    to put the figure's centre near the right place), and template matching finds the shift."""
    h, w = street_mask.shape
    fig = _highpass(cv2.GaussianBlur(street_mask.astype(np.float32), (0, 0), 1.5))
    near = roads[roads.intersects(footprint(init, w, h, pad * init.scale * 1.5))]
    lines = [np.asarray(ls.coords) for g in near.geometry for ls in getattr(g, "geoms", [g])]
    centre = init.apply([(w / 2, h / 2)])[0]
    best = None
    rot0 = np.degrees(init.rotation)
    for s in np.linspace(init.scale * (1 - scale_range), init.scale * (1 + scale_range), 31):
        for r in np.arange(rot0 - rot_range, rot0 + rot_range + 1e-9, rot_step):
            sim = anchored((w / 2, h / 2), centre, s, r)
            m = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
            for c in lines:
                cv2.polylines(m, [np.round(to_figure(sim, c) + pad).astype(np.int32)], False, 1.0, 2)
            res = cv2.matchTemplate(_highpass(cv2.GaussianBlur(m, (0, 0), 1.5)), fig, cv2.TM_CCORR_NORMED)
            _, v, _, loc = cv2.minMaxLoc(res)
            if best is None or v > best[0]:
                best = (v, sim, loc)
    v, sim, loc = best
    shift = sim.apply([(loc[0] - pad, loc[1] - pad)])[0] - sim.apply([(0, 0)])[0]
    sim.tx, sim.ty = sim.tx + shift[0], sim.ty + shift[1]
    return sim, float(v)


def street_pixels(rgb: np.ndarray, exclude: list[tuple[int, int, int, int]], v_range=(150, 215), max_sat=14,
                  n: int = 25000) -> np.ndarray:
    """Light grey, unsaturated pixels (street casings on agency base maps), minus boxes to exclude."""
    a = rgb.astype(int)
    sat, v = a.max(2) - a.min(2), a.mean(2)
    m = ((sat < max_sat) & (v > v_range[0]) & (v < v_range[1])).astype(np.uint8)
    for x0, y0, x1, y1 in exclude:
        m[y0:y1, x0:x1] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    ys, xs = np.nonzero(m)
    sel = np.random.default_rng(0).choice(len(xs), min(len(xs), n), replace=False)
    return np.c_[xs[sel], ys[sel]].astype(float)


# ---------------------------------------------------------------- aerial photos

def _highpass(a: np.ndarray, s: float = 6) -> np.ndarray:
    return a - cv2.GaussianBlur(a, (0, 0), s)


def _render(polys: list[np.ndarray], sim: trace.Similarity, w: int, h: int, pad: int) -> np.ndarray:
    m = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
    for c in polys:
        cv2.fillPoly(m, [np.round(to_figure(sim, c) + pad).astype(np.int32)], 1.0)
    return m


def register_buildings(rgb: np.ndarray, buildings: gpd.GeoDataFrame, init: trace.Similarity,
                       exclude: list[tuple[int, int, int, int]] = (), scale_range: float = 0.1,
                       rot_range: float = 3.0, pad: int = 60, tile: int = 120, search: int = 10,
                       min_fill: float = 0.08) -> tuple[trace.Similarity, dict]:
    """Fit an aerial-photo figure to building footprints (UTM). See the module docstring."""
    h, w = rgb.shape[:2]
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    sat = rgb.max(2).astype(int) - rgb.min(2)
    valid = (sat < 40).astype(np.float32)  # drop coloured annotations
    for x0, y0, x1, y1 in exclude:
        valid[y0:y1, x0:x1] = 0
    fig = _highpass(cv2.GaussianBlur(gray, (0, 0), 1.5)) * valid
    near = buildings[buildings.intersects(footprint(init, w, h, 600))]
    polys = [np.asarray(p.exterior.coords) for g in near.geometry for p in getattr(g, "geoms", [g])]

    def frame(scale, rot_deg):
        c = init.apply([(w / 2, h / 2)])[0]
        return anchored((w / 2, h / 2), c, scale, rot_deg)

    best = None
    rot0 = np.degrees(init.rotation)
    for s in np.linspace(init.scale * (1 - scale_range), init.scale * (1 + scale_range), 21):
        for r in np.arange(rot0 - rot_range, rot0 + rot_range + 1e-9, 0.25):
            sim = frame(s, r)
            m = _highpass(cv2.GaussianBlur(_render(polys, sim, w, h, pad), (0, 0), 1.5))
            res = cv2.matchTemplate(m, fig, cv2.TM_CCORR_NORMED)
            _, v, _, loc = cv2.minMaxLoc(res)
            if best is None or v > best[0]:
                best = (v, s, r, loc)
    v, s, r, loc = best
    sim = frame(s, r)
    shift = sim.apply([(loc[0] - pad, loc[1] - pad)])[0] - sim.apply([(0, 0)])[0]
    sim.tx, sim.ty = sim.tx + shift[0], sim.ty + shift[1]

    # Tile by tile: the local shift that best lines the footprints up with the photo.
    mask = _render(polys, sim, w, h, search)
    mhp = _highpass(cv2.GaussianBlur(mask, (0, 0), 1.5))
    src, dst = [], []
    for y0 in range(0, h - tile + 1, tile // 2):
        for x0 in range(0, w - tile + 1, tile // 2):
            win = mask[y0 + search:y0 + search + tile, x0 + search:x0 + search + tile]
            if win.mean() < min_fill or valid[y0:y0 + tile, x0:x0 + tile].mean() < 0.6:
                continue
            t = fig[y0:y0 + tile, x0:x0 + tile]
            res = cv2.matchTemplate(mhp[y0:y0 + tile + 2 * search, x0:x0 + tile + 2 * search], t, cv2.TM_CCORR_NORMED)
            _, tv, _, tl = cv2.minMaxLoc(res)
            if tv < 0.25 or tl[0] in (0, 2 * search) or tl[1] in (0, 2 * search):
                continue  # weak or at the edge of the search window
            cx, cy = x0 + tile / 2, y0 + tile / 2
            # figure point (cx, cy) shows what the footprints place at (cx + dx, cy + dy)
            dx, dy = tl[0] - search, tl[1] - search
            src.append((cx, cy))
            dst.append(sim.apply([(cx + dx, cy + dy)])[0])
    if len(src) < 4:
        raise SystemExit(f"building registration: only {len(src)} usable tiles")
    src, dst = np.asarray(src), np.asarray(dst)
    fit = trace.fit_similarity(src, dst)
    r_ = np.asarray(fit.residuals_m)
    keep = r_ <= max(3 * np.median(r_), 1e-6)
    fit = trace.fit_similarity(src[keep], dst[keep], [f"tile at ({x:.0f}, {y:.0f}) px" for x, y in src[keep]])
    rep = fit.report()
    rep.update({
        "method": ("building-footprint match: OpenStreetMap footprints rendered in the figure's frame and correlated "
                   "with the aerial photo (coarse search over scale and rotation), then tile by tile "
                   f"({tile} px tiles, half overlapping); each tile's local shift is a control point for "
                   "trace.fit_similarity"),
        "coarse_correlation": round(float(v), 3),
        "tiles_used": int(keep.sum()), "tiles_dropped_as_outliers": int((~keep).sum()),
        "median_m": round(float(np.median(fit.residuals_m)), 2),
        "max_m": round(float(np.max(fit.residuals_m)), 2),
    })
    rep["controls"] = rep["controls"][:0]  # per-tile residuals are summarised, not listed
    return fit, rep


# ---------------------------------------------------------------- line pixels

def column_centreline(mask: np.ndarray, min_pixels: int = 1, midrange: bool = False, smooth: int = 1) -> LineString:
    """For a line running left to right: the median row of the mask in every column that has one
    (or the middle of its top and bottom rows, for a pair of tracks), smoothed over `smooth` columns."""
    xs, ys = [], []
    for x in range(mask.shape[1]):
        col = np.nonzero(mask[:, x])[0]
        if len(col) >= min_pixels:
            xs.append(x + 0.5)
            ys.append((col.min() + col.max()) / 2 + 0.5 if midrange else float(np.median(col)) + 0.5)
    ys = np.asarray(ys)
    if smooth > 1 and len(ys) > smooth:
        k = np.ones(smooth) / smooth
        ys = np.convolve(np.pad(ys, smooth // 2, mode="edge"), k, mode="valid")[:len(xs)]
    return LineString(np.c_[xs, ys])


def component_paths(skel: np.ndarray, min_px: int = 15) -> list[LineString]:
    """The longest end-to-end path through each connected piece of a one-pixel skeleton, as pixel
    LineStrings (x, y). Spurs left by thinning fall off; pieces under `min_px` pixels are dropped."""
    n, lab = cv2.connectedComponents(skel.astype(np.uint8), connectivity=8)
    out = []
    for i in range(1, n):
        part = lab == i
        if part.sum() >= min_px:
            out.append(LineString([(x + 0.5, y + 0.5) for x, y in _longest_path(part)]))
    return out


def chain_paths(paths: list[LineString], max_gap: float) -> tuple[LineString, list[float]]:
    """Join path pieces end to end into one line, starting from the westernmost end and always
    taking the piece whose nearer end is closest (gaps up to `max_gap` px, where labels or
    symbols interrupt the drawn line). Returns the line and the gaps bridged."""
    left = [list(p.coords) for p in paths]
    start = min(range(len(left)), key=lambda i: min(left[i][0][0], left[i][-1][0]))
    cur = left.pop(start)
    if cur[-1][0] < cur[0][0]:
        cur.reverse()
    gaps = []
    while left:
        end = np.asarray(cur[-1])
        best = min(((np.hypot(*(np.asarray(c[k]) - end)), i, k) for i, c in enumerate(left) for k in (0, -1)))
        if best[0] > max_gap:
            break
        nxt = left.pop(best[1])
        if best[2] == -1:
            nxt.reverse()
        gaps.append(float(best[0]))
        cur += nxt
    return LineString(cur), gaps


def largest_blob(mask: np.ndarray) -> np.ndarray:
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
    if n < 2:
        raise SystemExit("no blob found")
    return lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))


def blob_centroid(mask: np.ndarray) -> tuple[float, float]:
    ys, xs = np.nonzero(mask)
    return float(xs.mean()) + 0.5, float(ys.mean()) + 0.5


def utm_to_wgs(g):
    return gpd.GeoSeries([g], crs=UTM).to_crs(4326).iloc[0]


def wgs_to_utm(g):
    return gpd.GeoSeries([g], crs=4326).to_crs(UTM).iloc[0]
