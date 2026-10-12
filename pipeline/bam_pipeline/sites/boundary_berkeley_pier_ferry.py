"""Berkeley Water Transportation Pier Ferry: the project site traced from the City's Draft EIR.

The City of Berkeley publishes no GIS layer for the project, and the three parcels its CEQA
filing lists don't outline it. The Draft EIR (Feb 2026, CEQAnet SCH 2025040995) draws the
"Berkeley WTPF Project Site" in yellow on an aerial photo in Figure 2-2, Project Site Location
(PDF p. 54), with an inset that shows the whole site, including the dredged approach channel
that runs about 2.5 miles out into the Bay along the closed pier.

1. The main frame (one embedded raster, 3,059 x 2,202 px) is north-up with a 0-650 ft scale bar
   (349 px between its end ticks, 0.5677 m/px). It is placed by one control point: the centre of
   the University Avenue/Marina Boulevard roundabout (pixel 1892, 672), matched to the centroid of
   the roundabout ring in OpenStreetMap. Overlaying OSM streets on the photo (Seawall Drive, the
   Seawall parking aisles, the plaza lot and the I-80 loop ramp 1.1 km away) agrees to within
   about 5 m, so neither rotation nor scale needed a fit.
2. The yellow outline is filled: outside is everything reachable from the frame's corners without
   crossing it; the frame's left edge closes the part that runs off the image.
3. The inset (5.5 m/px) is fitted to the traced main outline by trimmed ICP, and only its part west
   of the main frame (the outer dredged channel) is added.

The small separate square for a wayfinding sign is left out.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_berkeley_pier_ferry
"""

from __future__ import annotations

import io

import cv2
import numpy as np
import pypdf
import shapely
from PIL import Image
from shapely.geometry import Polygon

from .. import config, trace
from . import traced_boundaries as tb

PROJECT = "berkeley-pier-ferry"
DEIR_URL = "https://ceqanet.lci.ca.gov/2025040995/2/Attachment/-QKY5z"
DEIR_SHA = "9bcc5677bbd5f7ac2339d378b60d3c775a5b396835f136d5e6d0502943557f1e"
DEIR = tb.DOCS / "berkeley-wtpf-draft-eir-2026-02.pdf"
PAGE = 53  # zero-based: PDF p. 54, Figure 2-2

M_PER_PX = 650 * 0.3048 / 349  # scale bar: 0 and 650 ft ticks 349 px apart
ANCHOR_PX = (1892.0, 672.0)  # roundabout centre in the photo
ANCHOR_UTM = (560593.8, 4191082.4)  # centroid of the roundabout ring, OpenStreetMap via Overture
INSET = (1960, 1390, 3059, 2202)  # x0, y0, x1, y1 of the inset map
LEGEND = (0, 1745, 600, 2202)
INSET_M_PER_PX = 1.2 * 1609.344 / 350.5  # inset scale bar: 0 and 1.2 mi ticks


def _image() -> np.ndarray:
    trace.fetch_document(DEIR_URL, DEIR, DEIR_SHA)
    page = pypdf.PdfReader(str(DEIR)).pages[PAGE]
    img = Image.open(io.BytesIO(page.images[0].data)).convert("RGB")
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def _yellow(im: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, (20, 110, 150), (36, 255, 255))


def _fill(barrier: np.ndarray, seeds: list[tuple[int, int]]) -> np.ndarray:
    """Everything not reachable from the seeds without crossing the barrier."""
    ff = barrier.copy()
    mask = np.zeros((ff.shape[0] + 2, ff.shape[1] + 2), np.uint8)
    for x, y in seeds:
        if ff[y, x] == 0:
            cv2.floodFill(ff, mask, (x, y), 128)
    return (ff != 128).astype(np.uint8) * 255


def _polygons(mask: np.ndarray, min_px: int) -> list[Polygon]:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in contours:
        if cv2.contourArea(c) >= min_px:
            out.append(shapely.make_valid(Polygon(c[:, 0, :].astype(float))))
    return out


def _main_to_utm(pts: np.ndarray) -> np.ndarray:
    pts = np.asarray(pts, float)
    return np.column_stack([ANCHOR_UTM[0] + (pts[:, 0] - ANCHOR_PX[0]) * M_PER_PX,
                            ANCHOR_UTM[1] - (pts[:, 1] - ANCHOR_PX[1]) * M_PER_PX])


def _apply(poly, fn):
    return shapely.transform(poly, lambda xy: fn(xy))


def main() -> None:
    im = _image()
    H, W = im.shape[:2]
    y = _yellow(im)

    # Main frame: blank the legend and the inset, close the left edge, fill.
    main = y.copy()
    main[LEGEND[1]:LEGEND[3], LEGEND[0]:LEGEND[2]] = 0
    main[INSET[1]:INSET[3], INSET[0]:INSET[2]] = 0
    barrier = cv2.dilate(main, np.ones((5, 5), np.uint8))
    barrier[:, 0:14] = 255
    seeds = [(1500, 100), (1200, 2150), (2900, 1000), (1000, 600), (2500, 1200)]
    inside = _fill(barrier, seeds)
    inside[:, 0:14] = 0
    pieces = _polygons(inside, min_px=2000)  # drops the wayfinding-sign square
    # The fill runs to the outer edge of the drawn line (about 9 px plus the 2 px dilation): back to its centre.
    main_px = shapely.union_all(pieces).buffer(-6.5)
    main_utm = _apply(main_px, _main_to_utm)

    # Inset: fill its outline, fit it to the main outline, keep the part west of the main frame.
    ins = y[INSET[1]:INSET[3], INSET[0]:INSET[2]].copy()
    # The "Dredging" leader line breaks the inset outline; a 15 px closing joins it again.
    ins_b = cv2.dilate(cv2.morphologyEx(ins, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)), np.ones((3, 3), np.uint8))
    ins_fill = _fill(ins_b, [(5, 5), (ins.shape[1] - 5, ins.shape[0] - 160)])
    ins_poly = shapely.union_all(_polygons(ins_fill, min_px=300)).buffer(-4.5)  # 7 px line, 1 px dilation
    ring = np.asarray(ins_poly.exterior.coords if ins_poly.geom_type == "Polygon"
                      else max(ins_poly.geoms, key=lambda g: g.area).exterior.coords)
    # Initial placement: inset scale bar, north-up, the site's northern tip at Frontage Road matched
    # by eye (inset pixel 2988, 1533; main pixel 2867, 60).
    k = INSET_M_PER_PX
    init = trace.Similarity(k, 0.0, 0.0, 0.0)
    tip_ins = np.array([[2988 - INSET[0], 1533 - INSET[1]]], float)
    tip_utm = _main_to_utm(np.array([[2867.0, 60.0]]))
    shift = tip_utm[0] - init.apply(tip_ins)[0]
    init = trace.Similarity(k, 0.0, float(shift[0]), float(shift[1]))
    # Fit on the inset's outline points that land inside the main frame (away from its edges).
    frame = Polygon(_main_to_utm(np.array([[30, 30], [W - 30, 30], [W - 30, H - 30], [30, H - 30]])))
    frame = frame.difference(Polygon(_main_to_utm(np.array(
        [[INSET[0], INSET[1]], [W, INSET[1]], [W, H], [INSET[0], H]]))))
    dense = np.asarray(shapely.segmentize(shapely.LineString(ring), 2.0).coords)
    on = np.array([frame.contains(shapely.Point(*p)) for p in init.apply(dense)])
    sim, d = tb.icp(dense[on], [main_utm.boundary], np.zeros(int(on.sum()), int), init, keep=0.8, scale=k)
    rep = tb.icp_report(sim, d, 0.8, "inset outline against the traced main outline")
    ins_utm = _apply(Polygon(ring), lambda xy: sim.apply(xy)).simplify(4.0)  # smooth the 5.5 m pixel steps
    west_edge = _main_to_utm(np.array([[14, 0], [14, H]]))[0, 0]
    x0 = min(ins_utm.bounds[0], main_utm.bounds[0]) - 100
    west = shapely.box(x0, ins_utm.bounds[1] - 100, west_edge + 25, ins_utm.bounds[3] + 100)
    site = shapely.union_all([main_utm, ins_utm.intersection(west)])
    site = site.buffer(8, join_style="mitre").buffer(-8, join_style="mitre").simplify(1.0, preserve_topology=True)
    acres = site.area / tb.ACRE_M2

    tb.write(PROJECT, site, {
        "source": ("traced: City of Berkeley, Berkeley Water Transportation Pier Ferry Project Draft EIR (Feb 2026), "
                   "Figure 2-2, Project Site Location (PDF p. 54), main frame and inset"),
        "sourceLabel": "Draft EIR, Figure 2-2 (Feb 2026)",
        "sourceUrl": DEIR_URL,
        "accuracy": "traced",
        "accuracyNote": (
            "Traced from the yellow project-site outline in the Draft EIR's Figure 2-2: the new pier, breakwater and "
            "ferry floats off the end of University Avenue, the plaza, Seawall Drive and its parking lot, University "
            "Avenue to Frontage Road, and the dredged channel along the closed pier. The figure's photo is placed by "
            "its scale bar and the University Avenue roundabout (OpenStreetMap streets agree to about 5 m); the outer "
            f"2 miles of channel come from the figure's small inset, fitted to the main frame (trimmed RMS "
            f"{rep['rms_m']:.0f} m), so that part is good to a few tens of metres. The CEQAnet filing gives 195.6 "
            f"total acres. {acres:,.1f} acres as drawn."),
        "license": ("Traced facts from a public City of Berkeley document (the PDF is not redistributed). "
                    f"Georeference: {tb.OSM_LICENSE}."),
        "georeference": {
            "method": "north-up, scale from the scale bar, one control point; inset by rigid trimmed ICP at its own scale bar",
            "m_per_px": round(M_PER_PX, 4),
            "control": {"label": "University Ave / Marina Blvd roundabout centre", "px": list(ANCHOR_PX),
                        "utm10n": list(ANCHOR_UTM)},
            "inset": rep,
        },
    })


if __name__ == "__main__":
    main()
