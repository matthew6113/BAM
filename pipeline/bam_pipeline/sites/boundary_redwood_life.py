"""Redwood LIFE Precise Plan: the project site traced from the City of Redwood City's Notice of Preparation.

The City's Notice of Preparation of an EIR (Aug 22, 2025, CEQAnet SCH 2025081015) names four
assessor's parcels (095-012-150, -220, -450 and -460; about 84 acres), but the County of San Mateo's
parcel service isn't reachable from the pipeline's network, so the site is traced from the NOP's
Figure 3, Aerial Photograph and Surrounding Area (PDF p. 7): a black dashed "Project Boundary" drawn
in vector over an aerial photo (Google Earth, photo date April 2022; 0-1,400 ft scale bar).

1. The page is rendered at 2 px per PDF point and the map frame cropped. The photo is fitted to
   OpenStreetMap building footprints (Overture) with line_georef.register_buildings: a coarse search
   over scale and rotation around the scale bar, then tile-by-tile control points through a
   similarity fit (RMS reported).
2. The dashes are read straight from the PDF and closed into the enclosed area with the helper from
   the Santa Clara Station Area module (each dash's centre line, joined across the gaps).

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_redwood_life
"""

from __future__ import annotations

import numpy as np
import pdfplumber
import pypdfium2 as pdfium

from .. import trace
from . import line_georef as lg
from . import traced_boundaries as tb
from .boundary_santa_clara_station_area import _enclosed, dash_shape

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


def build() -> None:
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
    acres = site.area / tb.ACRE_M2
    props = {
        "source": ("Traced from the City of Redwood City's Notice of Preparation of an EIR for the Redwood Life Precise "
                   "Plan (Aug 22, 2025; CEQAnet SCH 2025081015), Figure 3, Aerial Photograph and Surrounding Area, "
                   "PDF p. 7: the dashed \"Project Boundary\""),
        "sourceLabel": "Notice of preparation, Figure 3 (PDF)",
        "sourceUrl": NOP_URL,
        "documents": [CEQANET, NOP_URL],
        "documentSha256": NOP_SHA,
        "accuracy": "approximate",
        "accuracyNote": (
            "Approximate boundary: the project site as the NOP's aerial figure draws it, fitted to OpenStreetMap "
            "building footprints. The NOP gives about 84 acres on four assessor's parcels (095-012-150, -220, -450 "
            "and -460) at Bridge Parkway, Marine Parkway and Island Drive, along Belmont Slough; the County's parcels "
            f"would give a parcel-exact line. {acres:,.1f} acres as drawn."),
        "georeference": {**rep, "scale_m_per_unit": round(sim.scale, 5), "unit": "PDF point",
                         "start": "scale bar and the Marine Parkway / Bridge Parkway crossing (OpenStreetMap via Overture)"},
        "license": f"Boundary traced from a public CEQA document (City of Redwood City); fit to {tb.OSM_LICENSE}",
    }
    tb.write(PROJECT, site, props)
    print(f"[{PROJECT}] fit: {sim.scale:.3f} m/pt, rotation {np.degrees(sim.rotation):.2f} deg, RMS {rep['rms_m']} m, "
          f"{rep['tiles_used']} tiles; {acres:,.1f} acres vs {STATED_ACRES} stated")


def main() -> None:
    build()


if __name__ == "__main__":
    main()
