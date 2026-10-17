"""Southline: the Specific Plan area as the County of San Mateo's parcels, joined over Southline Avenue.

The Revised Southline Specific Plan (Final EIR Appendix 2.1, May 2022, CEQAnet SCH 2020050452, document 4)
and the City's notices of determination (July 2022) give a 28.5-acre plan area, including the 80 Tanforan
Avenue property that Alternative D added. The CEQA filing lists six APNs (014-250-090, -080, -050,
014-241-030, -040 and 014-232-030). None of them is in the County of San Mateo's parcel layer
(data.smcgov.org nr6j-72z7, Public Domain; last updated Aug 2024): the site has been re-mapped since the
2022 approvals. The County's parcels there now are 014-250-110 (20 Southline Avenue), -120 (30 Southline
Avenue), -130 (40 Dollar Avenue), -150 and -170 (325 South Maple Avenue), all on the same assessor's page
as three of the listed APNs. Each lies at least 97% inside the plan line of the revised plan's Figure 2-8,
and together they fill it except for the new Southline Avenue between them, which the plan area includes.
So the boundary is the union of those five parcels, joined over Southline Avenue by a 40 m closing (which
also fills the street's mouths at Huntington Avenue and South Linden Avenue).

The outline first drawn for the map, traced from the dotted "Specific Plan Area" line of Figure 2-8
(Conceptual Building Heights, plan p. 2-23, Final EIR PDF p. 935; one embedded raster, 1,500 x 900 px), is
still traced here to report the difference. Its georeference (the photo fitted to OpenStreetMap building
footprints via Overture with line_georef.register_buildings, from two hand-located street points) is also
what massing_southline.py uses for the plan's building heights.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_southline
"""

from __future__ import annotations

from functools import lru_cache

import cv2
import numpy as np
import shapely

from .. import trace
from . import line_georef as lg
from . import official_boundaries as ob
from . import traced_boundaries as tb
from .boundary_santa_clara_station_area import compare, parcel_site

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
CEQA_APNS = ["014-250-090", "014-250-080", "014-250-050", "014-241-030", "014-241-040", "014-232-030"]
APNS = ["014250110", "014250120", "014250130", "014250150", "014250170"]  # the County's parcels in the plan line now
CLOSE_M = 40.0
PARCELS = {
    "label": "San Mateo County parcels",
    "url": f"{ob.SMC_PARCELS[0]}/resource/{ob.SMC_PARCELS[1]}.json?"
           + ob.urllib.parse.urlencode({"$where": f"apn in ({ob._sql_list(APNS)})", "$limit": 5000}),
    "landing": f"{ob.SMC_PARCELS[0]}/d/{ob.SMC_PARCELS[1]}",
    "wkt": {"field": "shape", "crs": "EPSG:2227"},
}


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


def traced_outline() -> tuple[shapely.Geometry, dict]:
    """The Figure 2-8 plan line (UTM) and its fit report: kept to compare with the parcels."""
    sim, rep = georeference()
    site = tb.clean(to_utm(sim, plan_area_px()))
    return site.simplify(0.5, preserve_topology=True), rep


def main() -> None:
    site, n = parcel_site(PROJECT, PARCELS, CLOSE_M)
    acres = site.area / tb.ACRE_M2
    traced, rep = traced_outline()
    cmp = compare(site, traced)
    tb.write(PROJECT, site, {
        "source": ("County of San Mateo parcels (data.smcgov.org nr6j-72z7): APNs 014-250-110, -120, -130, -150 and "
                   "-170, the County's parcels inside the Specific Plan Area line of the Revised Southline Specific Plan "
                   "(Final EIR Appendix 2.1, May 2022, Figure 2-8), joined over Southline Avenue"),
        "sourceLabel": "San Mateo County parcels",
        "sourceUrl": PARCELS["landing"],
        "query": PARCELS["url"],
        "documents": [FEIR["url"], PARCELS["landing"]],
        "accuracy": "official",
        "accuracyNote": (
            f"The plan area as the County of San Mateo's parcels draw it: the five parcels that fill the revised plan's "
            f"Specific Plan Area line, joined over the new Southline Avenue between them ({CLOSE_M:.0f} m closing). "
            f"{acres:.1f} acres as drawn, against the plan's and the notices of determination's {PLAN_ACRES} acres; the "
            "rest is street frontage at the edges. The six APNs on the CEQA filing (014-250-090, -080, -050, 014-241-030, "
            "-040 and 014-232-030) are no longer in the County's layer; the site has been re-mapped since 2022, and the "
            "five current parcels are on the same assessor's page. The outline traced earlier from Figure 2-8 came to "
            f"{cmp['traced_acres']:.1f} acres; the two lie up to {cmp['max_deviation_m']:.0f} m apart, at the street "
            "corners."),
        "license": "Public Domain (County of San Mateo)",
        "features_used": n,
        "ceqaApns": CEQA_APNS,
        "tracedComparison": {**cmp, "traced_from": "Revised Specific Plan Figure 2-8, Specific Plan Area line (Final EIR "
                             "PDF p. 935), fitted to OpenStreetMap building footprints", "traced_fit_rms_m": rep["rms_m"]},
    })
    print(f"[{PROJECT}] parcels: {n} features, {acres:.1f} acres vs {PLAN_ACRES}; traced {cmp['traced_acres']} acres, "
          f"max deviation {cmp['max_deviation_m']} m")


if __name__ == "__main__":
    main()
