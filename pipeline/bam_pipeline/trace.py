"""Georeference figures in official plan PDFs and trace polygons from them.

Plan documents rarely ship GIS files, but their figures are drawn to scale. This module:

1. Fits a similarity transform (scale, rotation, shift) from figure coordinates to
   projected metres, using control points: street intersections located in the figure
   (from street-name labels or by hand) matched to the same intersections in
   OpenStreetMap. It reports the residual at every control point and the RMS, which is
   the honest accuracy figure to publish.
2. Extracts filled vector shapes (CMYK colour match) straight from a PDF page.
3. Traces colour regions in raster figures with OpenCV.
4. Registers one figure to another by matching a shared outline (trimmed ICP).

Figure coordinates are x to the right and y DOWN (PDF points or image pixels).
"""

from __future__ import annotations

import hashlib
import shutil
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import LineString, MultiPolygon, Polygon


# ---------------------------------------------------------------- documents

def fetch_document(url: str, dest: Path, sha256: str | None = None) -> Path:
    """Download a source document once into data/raw/docs and check its hash."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        with urllib.request.urlopen(url) as r, open(tmp, "wb") as f:
            shutil.copyfileobj(r, f)
        tmp.rename(dest)
    if sha256:
        got = hashlib.sha256(dest.read_bytes()).hexdigest()
        if got != sha256:
            raise SystemExit(f"{dest.name}: sha256 {got} does not match the pinned {sha256}")
    return dest


# ---------------------------------------------------------------- transforms

@dataclass
class Similarity:
    """Figure (x right, y down) -> projected metres (x east, y north)."""

    scale: float
    rotation: float  # radians, counter-clockwise
    tx: float
    ty: float
    labels: list[str] = field(default_factory=list)
    residuals_m: list[float] = field(default_factory=list)

    @property
    def rms_m(self) -> float:
        r = np.asarray(self.residuals_m, float)
        return float(np.sqrt((r**2).mean())) if len(r) else float("nan")

    def matrix(self) -> np.ndarray:
        c, s = np.cos(self.rotation), np.sin(self.rotation)
        return self.scale * np.array([[c, -s], [s, c]])

    def apply(self, pts) -> np.ndarray:
        a = np.asarray(pts, float).reshape(-1, 2).copy()
        a[:, 1] *= -1
        return (self.matrix() @ a.T).T + [self.tx, self.ty]

    def geometry(self, g):
        return shapely.transform(g, lambda xy: self.apply(xy))

    def report(self) -> dict:
        return {
            "scale_m_per_unit": round(self.scale, 5),
            "rotation_deg": round(float(np.degrees(self.rotation)), 3),
            "rms_m": round(self.rms_m, 2),
            "controls": [
                {"label": label, "residual_m": round(r, 2)} for label, r in zip(self.labels, self.residuals_m)
            ],
        }


def fit_similarity(src, dst, labels: list[str] | None = None) -> Similarity:
    """Least-squares similarity (Umeyama) from figure points to projected points."""
    a = np.asarray(src, float).copy()
    a[:, 1] *= -1
    b = np.asarray(dst, float)
    ma, mb = a.mean(0), b.mean(0)
    A, B = a - ma, b - mb
    U, S, Vt = np.linalg.svd(B.T @ A / len(a))
    D = np.eye(2)
    if np.linalg.det(U @ Vt) < 0:
        D[1, 1] = -1
    R = U @ D @ Vt
    scale = float(np.trace(np.diag(S) @ D) / ((A**2).sum() / len(a)))
    t = mb - scale * R @ ma
    sim = Similarity(scale, float(np.arctan2(R[1, 0], R[0, 0])), float(t[0]), float(t[1]), list(labels or []))
    sim.residuals_m = [float(x) for x in np.linalg.norm(sim.apply(src) - b, axis=1)]
    return sim


def icp_similarity(points, target: LineString, init: Similarity, iterations: int = 60, keep: float = 0.7) -> Similarity:
    """Refine a transform so figure points land on a target outline (trimmed ICP).

    `points` are figure coordinates of pixels drawn on a shared outline (e.g. the project
    site boundary); `target` is the same outline already in projected metres. Each round
    matches every point to its nearest spot on the target, keeps the closest `keep`
    share (dropping text and other ink), and refits.
    """
    pts = np.asarray(points, float)
    sim = init
    for _ in range(iterations):
        moved = sim.apply(pts)
        geoms = shapely.points(moved)
        nearest = shapely.line_interpolate_point(target, shapely.line_locate_point(target, geoms))
        near = shapely.get_coordinates(nearest)
        d = np.linalg.norm(moved - near, axis=1)
        cut = np.quantile(d, keep)
        sel = d <= cut
        new = fit_similarity(pts[sel], near[sel])
        if abs(new.scale - sim.scale) < 1e-9 and abs(new.tx - sim.tx) < 1e-6 and abs(new.ty - sim.ty) < 1e-6:
            sim = new
            break
        sim = new
    moved = sim.apply(pts)
    near = shapely.get_coordinates(
        shapely.line_interpolate_point(target, shapely.line_locate_point(target, shapely.points(moved)))
    )
    d = np.linalg.norm(moved - near, axis=1)
    inliers = d <= np.quantile(d, keep)
    sim.labels = [f"outline inliers ({int(inliers.sum())} of {len(d)} pixels)"]
    sim.residuals_m = [float(np.sqrt((d[inliers] ** 2).mean()))]
    return sim


# ---------------------------------------------------------------- PDF vectors and labels

def pdf_label_center(page, text: str, max_gap: float = 20) -> tuple[float, float]:
    """Centre of a text label on a pdfplumber page, horizontal or vertical.

    Labels are matched word by word (vertical street names come out as separate words),
    and the label must occur at exactly one position.
    """
    tokens = text.split()
    # Some figures print labels twice for a bold effect; drop the duplicate glyphs.
    words = page.dedupe_chars().extract_words()
    hits = set()
    for w in (w for w in words if w["text"] == tokens[0]):
        parts = [w]
        for tok in tokens[1:]:
            cands = [v for v in words if v["text"] == tok]
            if not cands:
                break
            prev = parts[-1]

            def gap(v, prev=prev):
                along_x = abs(v["x0"] - prev["x1"]) + abs(v["top"] - prev["top"])  # horizontal text
                along_y = abs(v["top"] - prev["bottom"]) + abs(v["x0"] - prev["x0"])  # vertical text
                return min(along_x, along_y)

            near = min(cands, key=gap)
            if gap(near) > max_gap:
                break
            parts.append(near)
        if len(parts) != len(tokens):
            continue
        hits.add((round(min(p["x0"] for p in parts), 1), round(min(p["top"] for p in parts), 1),
                  round(max(p["x1"] for p in parts), 1), round(max(p["bottom"] for p in parts), 1)))
    if len(hits) != 1:
        raise SystemExit(f"label {text!r} found {len(hits)} times on page {page.page_number}")
    x0, top, x1, bottom = hits.pop()
    return (x0 + x1) / 2, (top + bottom) / 2


def pdf_filled_polygons(page, cmyk: tuple[float, ...], tol: float = 0.01, max_top: float | None = None) -> list[Polygon]:
    """Filled vector shapes of one colour on a pdfplumber page, in page points (y down)."""
    out = []
    for obj in page.curves + page.rects:
        color = obj.get("non_stroking_color")
        if not obj.get("fill") or color is None or len(color) != len(cmyk):
            continue
        if max(abs(a - b) for a, b in zip(color, cmyk)) > tol:
            continue
        if max_top is not None and obj["top"] > max_top:
            continue
        pts = obj.get("pts") or [(obj["x0"], obj["top"]), (obj["x1"], obj["top"]), (obj["x1"], obj["bottom"]), (obj["x0"], obj["bottom"])]
        if len(pts) >= 3:
            poly = shapely.make_valid(Polygon(pts))
            if not poly.is_empty and poly.area > 0:
                out.append(poly)
    return out


# ---------------------------------------------------------------- rasters

def raster_color_polygons(rgb: np.ndarray, color: tuple[int, int, int], tol: int = 18,
                          min_area_px: float = 150, close_px: int = 5, simplify_px: float = 1.5) -> list[Polygon]:
    """Regions of one colour in an RGB image, as polygons in pixel coordinates (y down).

    A morphological close fills the gaps left by text printed over the fill.
    """
    import cv2

    diff = np.abs(rgb.astype(int) - np.array(color, int)).max(axis=2)
    mask = (diff <= tol).astype(np.uint8) * 255
    if close_px:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (close_px, close_px))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    polys = []
    if hierarchy is None:
        return polys
    for i, c in enumerate(contours):
        if hierarchy[0][i][3] != -1:  # holes are attached to their parent below
            continue
        shell = cv2.approxPolyDP(c, simplify_px, True).reshape(-1, 2)
        if len(shell) < 3:
            continue
        holes = []
        child = hierarchy[0][i][2]
        while child != -1:
            h = cv2.approxPolyDP(contours[child], simplify_px, True).reshape(-1, 2)
            if len(h) >= 3 and cv2.contourArea(h) >= min_area_px:
                holes.append(h)
            child = hierarchy[0][child][0]
        fixed = shapely.make_valid(Polygon(shell, holes))
        parts = fixed.geoms if hasattr(fixed, "geoms") else [fixed]
        polys.extend(p for p in parts if isinstance(p, Polygon) and p.area >= min_area_px)
    return polys


def raster_classify_regions(rgb: np.ndarray, palette: dict, max_dist: float = 30, open_px: int = 3,
                            close_px: int = 9, min_area_px: float = 600, simplify_px: float = 1.5) -> list[tuple]:
    """Label every pixel with its nearest palette colour (within `max_dist`) and trace regions.

    Sturdier than one colour at a time: printed colours drift from the legend swatches,
    and anti-aliased text sits between colours. An opening removes thin text strokes,
    a closing fills the holes text leaves inside a fill. Returns (key, polygon) pairs
    in pixel coordinates (y down).
    """
    import cv2

    keys = list(palette)
    cols = np.array([palette[k] for k in keys], float)
    dist = np.linalg.norm(rgb[:, :, None, :].astype(float) - cols[None, None, :, :], axis=3)
    nearest = dist.argmin(axis=2)
    valid = dist.min(axis=2) <= max_dist
    out = []
    for i, key in enumerate(keys):
        mask = ((nearest == i) & valid).astype(np.uint8) * 255
        if open_px:
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((open_px, open_px), np.uint8))
        if close_px:
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((close_px, close_px), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            shell = cv2.approxPolyDP(c, simplify_px, True).reshape(-1, 2)
            if len(shell) < 3:
                continue
            fixed = shapely.make_valid(Polygon(shell))
            for p in (fixed.geoms if hasattr(fixed, "geoms") else [fixed]):
                if isinstance(p, Polygon) and p.area >= min_area_px:
                    out.append((key, p))
    return out


def largest_polygon(g) -> Polygon:
    if isinstance(g, Polygon):
        return g
    parts = [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]
    return max(parts, key=lambda p: p.area)


def as_multipolygon(g) -> MultiPolygon:
    if isinstance(g, MultiPolygon):
        return g
    if isinstance(g, Polygon):
        return MultiPolygon([g])
    return MultiPolygon([p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)])
