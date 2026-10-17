"""Redwood LIFE Precise Plan: the project site as the County of San Mateo's parcels for its four APNs.

The City's Notice of Preparation of an EIR (Aug 22, 2025, CEQAnet SCH 2025081015, p. 2) names the site:
"800, 1400, 1600, and 3400 Bridge Parkway ... approximately 84 acres and consists of four parcels
(Assessor's Parcel Numbers [APNs]: 095-012-220, -450, -460, and -150)". The boundary is the union of those
four parcels in the County of San Mateo parcel layer (data.smcgov.org nr6j-72z7, Public Domain).

The outline first drawn for the map was traced from the NOP's Figure 3 aerial (PDF p. 7): the photo
fitted to OpenStreetMap building footprints with line_georef.register_buildings, the dashed "Project
Boundary" read straight from the PDF and closed with the helper from the Santa Clara Station Area
module. It is still traced here, only to report how far the parcels lie from it.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_redwood_life
"""

from __future__ import annotations

import numpy as np
import pdfplumber
import pypdfium2 as pdfium

from .. import trace
from . import line_georef as lg
from . import official_boundaries as ob
from . import traced_boundaries as tb
from .boundary_santa_clara_station_area import _enclosed, compare, dash_shape, parcel_site

PROJECT = "redwood-life"
NOP_URL = "https://ceqanet.lci.ca.gov/2025081015/Attachment/yselzM"
NOP_SHA = "ddeef1afb1db098078819fe7f967e4db870f75e54f814ff10b61c59dad10ae39"
NOP = tb.DOCS / "redwood-life-nop-2025-08.pdf"
CEQANET = "https://ceqanet.lci.ca.gov/2025081015"
PAGE = 6  # zero-based: PDF p. 7, Figure 3
K = 2.0  # render scale, px per PDF point
FRAME_PT = (47.0, 72.0, 757.0, 516.0)  # the map frame (x0, top, x1, bottom), PDF points
LEGEND_PT = (53.0, 80.0, 210.0, 142.0)  # legend, scale bar and photo credit
DASH = (0.695, 0.672, 0.637, 0.738)  # CMYK of the "Project Boundary" dashes
SCALE_M_PER_PT = 1400 * 0.3048 / 129.7  # 0-1,400 ft scale bar, about 129.7 pt long
ANCHOR_PT = (390.0, 345.0)  # roughly where Marine Parkway meets Bridge Parkway (a start for the search)
STATED_ACRES = 84  # NOP and CEQAnet "Total Acres"
APNS = ["095012150", "095012220", "095012450", "095012460"]  # NOP p. 2
PARCELS = {
    "label": "San Mateo County parcels",
    "url": f"{ob.SMC_PARCELS[0]}/resource/{ob.SMC_PARCELS[1]}.json?"
           + ob.urllib.parse.urlencode({"$where": f"apn in ({ob._sql_list(APNS)})", "$limit": 5000}),
    "landing": f"{ob.SMC_PARCELS[0]}/d/{ob.SMC_PARCELS[1]}",
    "wkt": {"field": "shape", "crs": "EPSG:2227"},
}
BBOX = (-122.29, 37.52, -122.23, 37.56)


def _dashes() -> list:
    page = pdfplumber.open(str(NOP)).pages[PAGE]
    x0, t0, x1, b0 = FRAME_PT
    lx0, lt, lx1, lb = LEGEND_PT
    out = []
    for o in page.curves:
        if tuple(round(v, 3) for v in (o.get("non_stroking_color") or ())) != DASH:
            continue
        if not (x0 <= o["x0"] and o["x1"] <= x1 and t0 <= o["top"] and o["bottom"] <= b0):
            continue
        if lx0 <= o["x0"] <= lx1 and lt <= o["top"] <= lb:
            continue  # the legend's sample dash
        out.append(dash_shape(o["pts"]))
    return out


def traced_outline():
    """The NOP Figure 3 outline (UTM) and its fit report: kept to compare with the parcels."""
    trace.fetch_document(NOP_URL, NOP, NOP_SHA)
    page = np.asarray(pdfium.PdfDocument(str(NOP))[PAGE].render(scale=K).to_pil().convert("RGB"))
    fx0, ft, fx1, fb = (round(v * K) for v in FRAME_PT)
    rgb = page[ft:fb, fx0:fx1]
    lx0, lt, lx1, lb = LEGEND_PT
    exclude = [(int((lx0 - FRAME_PT[0]) * K), int((lt - FRAME_PT[1]) * K),
                int((lx1 - FRAME_PT[0]) * K), int((lb - FRAME_PT[1]) * K))]
    streets = tb.streets("rlife-redwood_life_wide", BBOX)
    buildings = tb.buildings("rlife-redwood_life_wide", BBOX)
    anchor = tb.intersection(streets, "Marine Parkway", "Bridge Parkway")
    to_px = lambda xy: ((xy[0] - FRAME_PT[0]) * K, (xy[1] - FRAME_PT[1]) * K)
    init = lg.anchored(to_px(ANCHOR_PT), anchor, SCALE_M_PER_PT / K, 0.0)
    sim_px, rep = lg.register_buildings(rgb, buildings, init, exclude=exclude, pad=400, tile=200, search=25)
    # PDF points -> crop pixels -> UTM
    sim = trace.Similarity(sim_px.scale * K, sim_px.rotation, 0.0, 0.0)
    o = sim_px.apply([to_px((0.0, 0.0))])[0]
    sim.tx, sim.ty = o[0], o[1]

    dashes = [sim.geometry(d) for d in _dashes()]
    site = _enclosed(dashes).simplify(1.0, preserve_topology=True)
    return site, rep, sim


def build() -> None:
    site, n = parcel_site("redwood-life", PARCELS)
    acres = site.area / tb.ACRE_M2
    traced, rep, sim = traced_outline()
    cmp = compare(site, traced)
    props = {
        "source": ("County of San Mateo parcels (data.smcgov.org nr6j-72z7): APNs 095-012-150, -220, -450 and -460, "
                   "the four parcels the City of Redwood City's Notice of Preparation (Aug 22, 2025; CEQAnet "
                   "SCH 2025081015, p. 2) names for the Redwood Life Precise Plan site"),
        "sourceLabel": "San Mateo County parcels",
        "sourceUrl": PARCELS["landing"],
        "query": PARCELS["url"],
        "documents": [CEQANET, NOP_URL, PARCELS["landing"]],
        "documentSha256": NOP_SHA,
        "accuracy": "official",
        "accuracyNote": (
            "The four parcels the Notice of Preparation names (800, 1400, 1600 and 3400 Bridge Parkway, between "
            f"Belmont Slough and Marine Parkway; \"approximately 84 acres\"), as the County of San Mateo maps them. "
            f"{acres:,.1f} acres as drawn. The outline traced earlier from the notice's Figure 3 aerial came to "
            f"{cmp['traced_acres']:,.1f} acres and lies within {cmp['max_deviation_m']:.0f} m of the parcels."),
        "license": "Public Domain (County of San Mateo)",
        "features_used": n,
        "tracedComparison": {**cmp, "traced_from": "NOP Figure 3, PDF p. 7 (dashed Project Boundary), fitted to "
                             "OpenStreetMap building footprints", "traced_fit_rms_m": rep["rms_m"]},
    }
    tb.write(PROJECT, site, props)
    print(f"[{PROJECT}] parcels: {n} features, {acres:,.1f} acres vs {STATED_ACRES} stated; traced "
          f"{cmp['traced_acres']:,.1f} acres, max deviation {cmp['max_deviation_m']} m")


def main() -> None:
    build()


if __name__ == "__main__":
    main()
