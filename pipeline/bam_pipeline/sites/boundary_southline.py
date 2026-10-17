"""Southline: the Specific Plan area traced from the Revised Southline Specific Plan.

The City of South San Francisco's parcel and plan-area GIS could not be reached from the build
(ssf.net and data.smcgov.org refused the connection on 2026-10-17), so the site is traced from the
plan itself. The Final EIR (May 2022, CEQAnet SCH 2020050452, document 4) carries the Revised
Southline Specific Plan as its Appendix 2.1, the version aligned with Alternative D (Reduced
Underground Parking), which adds the 80 Tanforan Avenue property: 28.5 acres in the plan's own
words (p. 1-3) and in the City's notices of determination (July 2022).

Figure 2-8, Conceptual Building Heights (plan p. 2-23, Final EIR PDF p. 935), draws the "Specific
Plan Area" as a dotted black line on an aerial photo (one embedded raster, 1,500 x 900 px):

1. Georeference: the photo is fitted to OpenStreetMap building footprints (via Overture) with
   line_georef.register_buildings, starting from two hand-located street points: Huntington Avenue
   at Sneath Lane / South Maple Avenue (the future Southline Avenue intersection) and South Linden
   Avenue at Dollar Avenue. The fit and its RMS are recorded in the file.
2. The dots are bridged and the enclosed area filled (traced_boundaries._enclosed), then pulled back
   to the line of the dot centres.

Figure 2-8's frame is also what massing_southline.py traces, so the georeference lives here.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_southline
"""

from __future__ import annotations

from functools import lru_cache

import cv2
import numpy as np
import shapely

from .. import trace
from . import line_georef as lg
from . import traced_boundaries as tb

PROJECT = "southline"
FEIR = {
    "url": "https://ceqanet.lci.ca.gov/2020050452/4/Attachment/i50fMG",
    "file": "southline-specific-plan-feir-2022-05.pdf",
    "sha256": "9325a7fec68e43e44deb7d19a2a6a472b74dc2d718c19764c270b3aecb2d0791",
}
FIG_PAGE = 934  # zero-based: Final EIR PDF p. 935, Revised Specific Plan Figure 2-8
FIG_SIZE = (1500, 900)
BBOX = (-122.425, 37.630, -122.400, 37.652)
LEGEND = (1170, 70, 1430, 480)  # x0, y0, x1, y1 in the figure
CITY_LABELS = (0, 120, 340, 230)
# Hand-located street points (figure px) and their OpenStreetMap positions (UTM 10N), for the first guess.
START = [
    ((375, 695), "Huntington Avenue / Sneath Lane / South Maple Avenue", (551434.0, 4166026.0)),
    ((1085, 500), "South Linden Avenue / Dollar Avenue", (551721.0, 4166279.0)),
]
INSIDE = (700, 450)  # a figure point inside the plan area
DOT_BRIDGE_PX = 19
PLAN_ACRES = 28.5


@lru_cache(maxsize=1)
def figure() -> np.ndarray:
    pdf = trace.fetch_document(FEIR["url"], tb.DOCS / FEIR["file"], FEIR["sha256"])
    return lg.pdf_image(pdf, FIG_PAGE, FIG_SIZE)


@lru_cache(maxsize=1)
def georeference() -> tuple[trace.Similarity, dict]:
    """Figure 2-8 (px, y down) -> UTM 10N, fitted to OpenStreetMap building footprints."""
    rgb = figure()
    buildings = tb.buildings("southline", BBOX)
    init = trace.fit_similarity(np.array([p for p, _, _ in START], float), np.array([u for _, _, u in START], float))
    sim, rep = lg.register_buildings(rgb, buildings, init, exclude=[LEGEND, CITY_LABELS], scale_range=0.15,
                                     rot_range=4.0, pad=120, tile=150, search=20)
    rep["start"] = [{"label": label, "px": list(p)} for p, label, _ in START]
    return sim, rep


def to_utm(sim: trace.Similarity, g):
    return shapely.transform(g, lambda xy: sim.apply(xy))


def plan_area_px() -> shapely.Polygon:
    """The area inside Figure 2-8's dotted Specific Plan Area line, at the dot centres (px)."""
    rgb = figure().astype(int)
    dark = (rgb.max(axis=2) < 80) & (rgb.max(axis=2) - rgb.min(axis=2) < 40)
    x0, y0, x1, y1 = LEGEND
    dark[y0:y1, x0:x1] = False
    # An opening with a 5 px disc removes the thin street and kerb lines the dots touch in places.
    dots = cv2.morphologyEx(dark.astype(np.uint8), cv2.MORPH_OPEN,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    # Keep only dot-sized specks: the dots are about 6 px across; text strokes join into larger blobs.
    n, lab, stats, _ = cv2.connectedComponentsWithStats(dots, connectivity=8)
    keep = np.zeros(n, bool)
    keep[1:] = (stats[1:, cv2.CC_STAT_AREA] >= 6) & (stats[1:, cv2.CC_STAT_AREA] <= 60) \
        & (stats[1:, cv2.CC_STAT_WIDTH] <= 10) & (stats[1:, cv2.CC_STAT_HEIGHT] <= 10)
    walls = keep[lab].astype(np.uint8)
    poly = tb._enclosed(walls, DOT_BRIDGE_PX, INSIDE)
    # The fill reaches half the bridge width plus half a dot beyond the dot centres.
    return poly.buffer(-(DOT_BRIDGE_PX / 2 + 2.5), join_style="mitre").simplify(1.0)


def main() -> None:
    sim, rep = georeference()
    site = tb.clean(to_utm(sim, plan_area_px()))
    site = site.simplify(0.5, preserve_topology=True)
    acres = site.area / tb.ACRE_M2
    tb.write(PROJECT, site, {
        "source": ("traced: City of South San Francisco, Revised Southline Specific Plan (Final EIR Appendix 2.1, "
                   "May 2022), Figure 2-8, Conceptual Building Heights, 'Specific Plan Area' line (Final EIR PDF p. 935)"),
        "sourceLabel": "Revised Specific Plan, Figure 2-8 (May 2022)",
        "sourceUrl": FEIR["url"],
        "accuracy": "approximate",
        "accuracyNote": (
            f"Approximate boundary traced from the dotted 'Specific Plan Area' line on the aerial photo of the Revised "
            f"Specific Plan's Figure 2-8. The photo is fitted to OpenStreetMap building footprints (RMS {rep['rms_m']:.1f} m "
            f"over {rep['tiles_used']} tiles), and the dots are about 6.5 m apart on the ground, so the line is good to a few "
            f"metres. {acres:.1f} acres as drawn; the plan and the City's notices of determination give about "
            f"{PLAN_ACRES} acres (the Draft EIR's 26.5 acres predates the added 80 Tanforan Avenue property). The six "
            "parcels the CEQA filing lists (APNs 014-250-090, -080, -050, 014-241-030, -040 and 014-232-030) were not "
            "checked against the County parcel layer, which could not be reached."),
        "license": (f"Traced facts from a public City of South San Francisco document (the PDF is not redistributed). "
                    f"Georeference: {tb.OSM_LICENSE}."),
        "georeference": {"Figure 2-8": rep},
    })


if __name__ == "__main__":
    main()
