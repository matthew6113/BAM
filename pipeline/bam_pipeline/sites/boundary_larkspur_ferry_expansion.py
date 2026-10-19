"""Larkspur Ferry Service and Parking Expansion: the project location traced from the District's NOP.

The Golden Gate Bridge, Highway and Transportation District publishes no GIS layer for the project.
Its Notice of Preparation of a Draft EIR (filed Sept 30, 2024, CEQAnet SCH 2024091190) draws the
project location in Figure 2, Project Location (PDF p. 5): four coloured outlines on an aerial photo,
"Larkspur Ferry Terminal" (pink), "Main Parking Lot" (orange), "Overflow Parking" (green) and
"Larkspur SMART Station" (purple), with the Corte Madera Channel as a yellow line. The NOP's text
says the parking expansion would be "on the main terminal parking lot and/or the north parking lot
located in the Country Mart shopping center"; the figure outlines no Country Mart lot, so none is drawn.

1. The page is rendered at 4 px per PDF point and cropped to the map frame (the photo is tiled
   JPEG strips; the outlines are part of the photo, not vectors).
2. The four outline colours are picked by hue; together they are the barrier, and each area they
   enclose is named by the colour that dominates its edge. The fill runs to the outer edge of the
   drawn line, so it is shrunk back by half the line width.
3. The photo is north-up with a 0-600 ft scale bar (144 pt). It is placed by matching it to
   OpenStreetMap building footprints (line_georef.register_buildings: a coarse search over scale
   and rotation, then a tile-by-tile fit whose residuals are reported), starting from the scale bar
   and the ferry route's terminal end in OpenStreetMap.

The yellow channel line (the dredged approach) isn't an area and isn't drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_larkspur_ferry_expansion
"""

from __future__ import annotations

import cv2
import numpy as np
import pypdfium2 as pdfium
import shapely
from shapely.geometry import Polygon

from .. import trace
from . import line_georef as lg
from . import traced_boundaries as tb

PROJECT = "larkspur-ferry-expansion"
NOP_URL = "https://ceqanet.lci.ca.gov/2024091190/2/Attachment/9FEu4G"
NOP_SHA = "8839ae049d667eb3d5c8a10038e3241dec4933d761838412e2cbaa32eafbb41a"
NOP = tb.DOCS / "larkspur-ferry-nop-2024-09.pdf"
CEQANET = "https://ceqanet.lci.ca.gov/Project/2024091190"
PAGE = 4  # zero-based: PDF p. 5, Figure 2
K = 4.0  # render scale, px per PDF point
FRAME_PT = (43.2, 36.0, 936.0, 756.0)  # the map frame (x0, top, x1, bottom), PDF points
SCALE_M_PER_PT = 600 * 0.3048 / 144.0  # 0-600 ft scale bar: ticks at 952.7 and 1096.7 pt
# (name, OpenCV hue range of the outline colour); the legend gives the strokes as RGB
AREAS = [
    ("Larkspur Ferry Terminal", (150, 168)),  # (1.0, 0.4, 0.863): hue 157
    ("Main Parking Lot", (12, 27)),  # (0.941, 0.757, 0.4)
    ("Overflow Parking", (40, 56)),  # (0.58, 0.941, 0.4)
    ("Larkspur SMART Station", (134, 149)),  # (0.796, 0.4, 0.941): hue 142
]
LINE_PX = 9  # drawn line width at K, about 2.2 pt
BBOX = (-122.525, 37.935, -122.495, 37.955)


def _render() -> np.ndarray:
    trace.fetch_document(NOP_URL, NOP, NOP_SHA)
    page = np.asarray(pdfium.PdfDocument(str(NOP))[PAGE].render(scale=K).to_pil().convert("RGB"))
    x0, t0, x1, b0 = (round(v * K) for v in FRAME_PT)
    return page[t0 + 4:b0 - 4, x0 + 4:x1 - 4].copy()  # inside the frame's black border


def _outlines(rgb: np.ndarray) -> dict[str, np.ndarray]:
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    strong = (hsv[..., 1] > 120) & (hsv[..., 2] > 110)
    return {name: ((hsv[..., 0] >= lo) & (hsv[..., 0] <= hi) & strong).astype(np.uint8) * 255
            for name, (lo, hi) in AREAS}


def _areas(rgb: np.ndarray) -> tuple[dict[str, list[Polygon]], dict]:
    """Pixel polygons for each named area, and how each was identified."""
    lines = _outlines(rgb)
    barrier = cv2.dilate(np.maximum.reduce(list(lines.values())), np.ones((5, 5), np.uint8))
    barrier = cv2.morphologyEx(barrier, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))  # labels break the lines
    n, lab = cv2.connectedComponents((barrier == 0).astype(np.uint8), connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    out: dict[str, list[Polygon]] = {name: [] for name, _ in AREAS}
    report = {}
    for i in range(1, n):
        if i in border:
            continue
        region = (lab == i).astype(np.uint8)
        if region.sum() < 1500:  # gaps between parallel lines, letters
            continue
        ring = cv2.dilate(region, np.ones((15, 15), np.uint8)) & ~region.astype(bool)
        votes = {name: int((m[ring.astype(bool)] > 0).sum()) for name, m in lines.items()}
        name = max(votes, key=votes.get)
        share = votes[name] / max(1, sum(votes.values()))
        cs, _ = cv2.findContours(cv2.dilate(region, np.ones((5, 5), np.uint8)), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_NONE)
        c = max(cs, key=cv2.contourArea)
        # The region stops at the inner edge of the line: grow it to the line's centre.
        poly = shapely.make_valid(Polygon(c[:, 0, :].astype(float))).buffer(LINE_PX / 2 - 2.5, join_style="mitre")
        out[name].append(poly)
        report.setdefault(name, []).append({"px": int(region.sum()), "edge_share": round(share, 2)})
    # Thin strips have no inside once the lines are thickened: the SMART station outline along the
    # tracks, and the terminal's strip along the shore to the ferry slip. So each area also takes the
    # outer edge of its own outline (closed, filled, and shrunk to the line's centre).
    for name, m in lines.items():
        # The "NWP RR" label breaks the SMART outline by about 30 px: a 61 px closing joins it again.
        k = 61 if name == "Larkspur SMART Station" else 15
        closed = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
        cs, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cs = [c for c in cs if cv2.contourArea(c) >= 1500]
        for c in cs:
            poly = shapely.make_valid(Polygon(c[:, 0, :].astype(float))).buffer(-LINE_PX / 2, join_style="mitre")
            if not poly.is_empty:
                out[name].append(poly)
        report.setdefault(name, []).append({"px": int(sum(cv2.contourArea(c) for c in cs)),
                                            "method": "outer edge of its own outline"})
    return out, report


def georeference(rgb: np.ndarray):
    """crop pixels -> UTM, fitted to OpenStreetMap building footprints.

    The fit runs on the photo at half resolution (2 px per point, about 0.64 m per pixel): enough for
    the footprints, and a quarter of the work. The figure is a north-up GIS export, so the search over
    rotation is kept to a degree either way."""
    streets = tb.streets("larkspur_ferry", BBOX)
    buildings = tb.buildings("larkspur_ferry", BBOX)
    route = streets[streets["name"] == "Larkspur - San Francisco Ferry Building"]
    ends = np.array([c for g in route.geometry for c in (g.coords[0], g.coords[-1])])
    terminal = ends[np.argmax(ends[:, 1])]  # the route's northern end, at the Larkspur slip
    lines = _outlines(rgb)
    ys, xs = np.nonzero(lines["Larkspur Ferry Terminal"])
    small = cv2.resize(rgb, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    start_px = (float(xs.mean()) / 2, float(ys.mean()) / 2)  # the terminal outline's centre
    init = lg.anchored(start_px, terminal, 2 * SCALE_M_PER_PT / K, 0.0)
    # Coloured outlines are left out of the match inside register_buildings (by saturation).
    half, rep = lg.register_buildings(small, buildings, init, scale_range=0.06, rot_range=1.0,
                                      pad=250, tile=120, search=15)
    sim = trace.Similarity(half.scale / 2, half.rotation, half.tx, half.ty)  # back to full-resolution pixels
    return sim, rep, streets


def build() -> None:
    rgb = _render()
    areas, ident = _areas(rgb)
    sim, rep, _ = georeference(rgb)
    parts = {}
    for name, polys in areas.items():
        if not polys:
            raise SystemExit(f"[{PROJECT}] no area found for {name}")
        g = shapely.union_all([sim.geometry(p) for p in polys])
        parts[name] = g.simplify(0.5, preserve_topology=True)
    # The terminal and the main lot share an edge; close the hairline between their traced halves.
    site = shapely.union_all(list(parts.values())).buffer(2.0, join_style="mitre").buffer(-2.0, join_style="mitre")
    site = shapely.union_all([p for p in shapely.get_parts(site) if p.area > 0.02 * tb.ACRE_M2])
    acres = {k: round(v.area / tb.ACRE_M2, 1) for k, v in parts.items()}
    total = site.area / tb.ACRE_M2
    tb.write(PROJECT, site, {
        "source": ("traced: Golden Gate Bridge, Highway and Transportation District, Notice of Preparation of a Draft "
                   "EIR, The Larkspur Ferry Service and Parking Expansion Project (Oct 1, 2024; CEQAnet SCH 2024091190), "
                   "Figure 2, Project Location (PDF p. 5)"),
        "sourceLabel": "Notice of Preparation, Figure 2 (Sept 2024)",
        "sourceUrl": NOP_URL,
        "documents": [CEQANET, NOP_URL],
        "documentSha256": NOP_SHA,
        "accuracy": "approximate",
        "accuracyNote": (
            "Traced from the four outlines in the Notice of Preparation's Figure 2, Project Location: the Larkspur Ferry "
            f"Terminal ({acres['Larkspur Ferry Terminal']} acres as drawn), the Main Parking Lot "
            f"({acres['Main Parking Lot']}), the Overflow Parking lot by Victoria Way "
            f"({acres['Overflow Parking']}) and the Larkspur SMART Station ({acres['Larkspur SMART Station']}); "
            f"{total:,.1f} acres in all. The NOP gives no acreage. It is a location map, not a site plan: the parking "
            "expansion may go on the main lot and/or the Country Mart's north lot, which the figure doesn't outline, "
            "and the Draft EIR will define the project. The photo is placed on OpenStreetMap building footprints "
            f"(fit RMS {rep['rms_m']:.1f} m)."),
        "license": ("Traced facts from a public Golden Gate Bridge, Highway and Transportation District document (the "
                    f"PDF is not redistributed). Georeference: {tb.OSM_LICENSE}."),
        "areas": acres,
        "identification": ident,
        "georeference": {"method": "fitted to OpenStreetMap building footprints (line_georef.register_buildings)",
                         "start_m_per_px": round(SCALE_M_PER_PT / K, 4),
                         "fitted_on": "the photo at 2 px per point (scale_m_per_unit is per pixel at that size)",
                         **rep},
    })
    print(f"[{PROJECT}] {total:,.1f} acres: {acres}; fit {rep}")


if __name__ == "__main__":
    build()
