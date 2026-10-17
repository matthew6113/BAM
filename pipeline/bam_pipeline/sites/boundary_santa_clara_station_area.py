"""Santa Clara Station Area Specific Plan: the plan area traced from the City's Notice of Preparation.

The City of Santa Clara has published no GIS layer for the plan area. Its Notice of Preparation of a
Draft Program EIR (June 12, 2026, CEQAnet SCH 2026060462) draws the "Project Boundary" as a black
dashed line on Figure 2, Vicinity Map (PDF p. 4), a vector map on an Esri street base map at about
1:30,000 (0-5,000 ft scale bar). The CEQAnet record also lists about 190 assessor's parcels, but the
county's parcel service isn't reachable from the pipeline's network, so the figure is used.

1. The page is rendered at 4 px per PDF point. Street pixels (the base map's white streets and
   yellow arterials) are thinned to centrelines and fitted to OpenStreetMap street centrelines
   (Overture) by trimmed ICP (line_georef.register_roads), starting from the De La Cruz Boulevard /
   Coleman Avenue junction and the scale bar.
2. The dashes are read straight from the PDF (filled shapes in the dash colour, outside the legend),
   joined across their gaps, and the centre of the dashed stroke is taken as the boundary.

At this scale the dashed line is about 18 m wide on the ground and the figure generalises the
street grid, so the boundary is approximate (the fit RMS is reported); it is not a parcel line.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_santa_clara_station_area
"""

from __future__ import annotations

import numpy as np
import pdfplumber
import pypdfium2 as pdfium
import shapely
from shapely.geometry import Polygon

from .. import trace
from . import line_georef as lg
from . import traced_boundaries as tb

PROJECT = "santa-clara-station-area"
NOP_URL = "https://ceqanet.lci.ca.gov/2026060462/Attachment/mtsQbf"
NOP_SHA = "72ad0561f3af491cdabba82b3907f8e1440e5348bbf5cb2f30e7f1838384b03a"
NOP = tb.DOCS / "santa-clara-station-area-nop-2026-06.pdf"
CEQANET = "https://ceqanet.lci.ca.gov/2026060462"
PAGE = 3  # zero-based: PDF p. 4, Figure 2, Vicinity Map
K = 4.0  # render scale, px per PDF point
DASH = (0.69531, 0.67188, 0.63672, 0.73828)  # CMYK of the "Project Boundary" dashes
MAP_PT = (285.0, 150.0, 560.0, 450.0)  # window used for the street fit (PDF points: x0, top, x1, bottom)
SITE_PT = (340.0, 210.0, 470.0, 380.0)  # the dashed boundary lies inside this box (PDF points)
ANCHOR_PT = (370.0, 252.0)  # De La Cruz Boulevard meets Coleman Avenue
SCALE_M_PER_PT = 5000 * 0.3048 / 132.0  # 0-5,000 ft scale bar, about 132 pt long (refined by the fit)
STATED_ACRES = 244  # NOP p. 2 and CEQAnet "Total Acres"
BBOX = (-121.975, 37.330, -121.905, 37.375)
ROAD_CLASSES = {"motorway", "trunk", "primary", "secondary", "tertiary", "residential", "unclassified",
                "living_street"}


def _street_pixels(rgb: np.ndarray) -> np.ndarray:
    """Centreline pixels of the base map's streets (white) and arterials (pale yellow), in PDF points."""
    a = rgb.astype(int)
    white = (a.min(2) >= 252)
    yellow = (a[..., 0] >= 245) & (a[..., 1] >= 240) & (a[..., 2] >= 170) & (a[..., 2] <= 215)
    m = white | yellow
    x0, y0, x1, y1 = (int(v * K) for v in MAP_PT)
    win = np.zeros_like(m)
    win[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    skel = lg._thin(win)
    ys, xs = np.nonzero(skel)
    return np.c_[xs, ys].astype(float) / K


def dash_shape(pts) -> Polygon:
    """A dash as drawn. Corner and curved dashes have outlines that touch themselves, so the outline
    is repaired and its filled parts kept (their convex hull would fill the inside of the corner)."""
    g = shapely.make_valid(Polygon(pts))
    parts = [p for p in shapely.get_parts(g) if p.geom_type == "Polygon" and p.area > 0]
    shape = shapely.union_all(parts).buffer(0.1).buffer(-0.1) if parts else shapely.MultiPoint(pts).convex_hull
    return max(shapely.get_parts(shape), key=lambda p: p.area)


def _dashes() -> list[Polygon]:
    page = pdfplumber.open(str(NOP)).pages[PAGE]
    out = []
    for o in page.curves:
        if o.get("non_stroking_color") != DASH:
            continue
        x0, t0, x1, b0 = SITE_PT
        if not (x0 <= o["x0"] and o["x1"] <= x1 and t0 <= o["top"] and o["bottom"] <= b0):
            continue  # the legend's sample dash and other symbols in the dash colour
        out.append(dash_shape(o["pts"]))
    return out


def _enclosed(dashes, max_gap_m: float = 120.0):
    """The area a dashed line encloses. Each dash is joined to its two nearest dashes by the
    shortest line between them, which closes the gaps and follows the line round corners; the
    enclosed faces (the main area and, where the line crosses itself, the lobe south of The
    Alameda) are then grown by half a stroke so the boundary runs down the middle of the dashes."""
    polys = list(dashes)
    stroke = float(np.median([2 * p.area / p.length for p in polys]))
    joins = []
    for i, p in enumerate(polys):
        d = shapely.distance(p, polys)
        d[i] = np.inf
        for j in np.argsort(d)[:2]:
            if d[j] <= max_gap_m:
                joins.append(shapely.shortest_line(p, polys[j]).buffer(stroke / 2, cap_style="square"))
    ink = shapely.union_all(polys + joins)
    faces = [Polygon(h) for g in shapely.get_parts(ink) for h in g.interiors]
    faces = [f for f in faces if f.area > 0.05 * tb.ACRE_M2]
    if not faces:
        raise SystemExit("the dashed boundary did not close")
    site = shapely.union_all(faces).buffer(stroke / 2, join_style="mitre")
    # Smooth the steps the joins leave at each gap (a closing at the stroke width), then drop the
    # spurs a join can leave into a corner dash (an opening at half the stroke width).
    site = site.buffer(stroke, join_style="mitre").buffer(-stroke, join_style="mitre")
    return site.buffer(-stroke / 2, join_style="mitre").buffer(stroke / 2, join_style="mitre")


def build() -> None:
    trace.fetch_document(NOP_URL, NOP, NOP_SHA)
    rgb = np.asarray(pdfium.PdfDocument(str(NOP))[PAGE].render(scale=K).to_pil().convert("RGB"))
    streets = tb.streets("scsa-santa_clara_station", BBOX)
    roads = streets[(streets["subtype"] == "road") & streets["class"].isin(ROAD_CLASSES)]
    target = shapely.union_all(roads.geometry.to_numpy())
    anchor = tb.intersection(streets, "De La Cruz Boulevard", "Coleman Avenue")
    init = lg.anchored(ANCHOR_PT, anchor, SCALE_M_PER_PT, 0.0)
    px = _street_pixels(rgb)
    sim, rep = lg.register_roads(px, target, init, keep=0.6, what="base-map street centrelines")

    dashes = [sim.geometry(d) for d in _dashes()]
    site = _enclosed(dashes).simplify(1.0, preserve_topology=True)
    acres = site.area / tb.ACRE_M2
    props = {
        "source": ("Traced from the City of Santa Clara's Notice of Preparation of a Draft Program EIR for the Santa "
                   "Clara Station Area Specific Plan (June 12, 2026; CEQAnet SCH 2026060462), Figure 2, Vicinity Map, "
                   "PDF p. 4: the dashed \"Project Boundary\""),
        "sourceLabel": "Notice of preparation, Figure 2 (PDF)",
        "sourceUrl": NOP_URL,
        "documents": [CEQANET, NOP_URL],
        "documentSha256": NOP_SHA,
        "accuracy": "approximate",
        "accuracyNote": (
            "Approximate boundary: the plan area as the NOP's small-scale vicinity map draws it (about 1:30,000; the "
            "dashed line is about 18 m wide on the ground), fitted to OpenStreetMap streets. The NOP describes about "
            f"{STATED_ACRES} acres of properties bounded by De La Cruz Boulevard, Reed Street and Martin Avenue to the "
            "northeast and Franklin Street and El Camino Real to the southwest. The City has published no plan-area "
            "layer; the parcels listed on CEQAnet would give a parcel-exact line. "
            f"{acres:,.1f} acres as drawn, streets included."),
        "georeference": {**rep, "anchor": "De La Cruz Boulevard / Coleman Avenue (OpenStreetMap via Overture)"},
        "license": f"Boundary traced from a public CEQA document (City of Santa Clara); fit to {tb.OSM_LICENSE}",
    }
    tb.write(PROJECT, site, props)
    print(f"[{PROJECT}] fit: scale {sim.scale:.3f} m/pt, rotation {np.degrees(sim.rotation):.2f} deg, "
          f"RMS {rep['rms_m']} m, median {rep['median_m']} m; {acres:,.1f} acres vs {STATED_ACRES} stated")


def main() -> None:
    build()


if __name__ == "__main__":
    main()
