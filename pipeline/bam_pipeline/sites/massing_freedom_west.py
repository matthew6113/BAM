"""Freedom West 2.0: the 15 building parcels at the heights of the proposed special use district.

Sources (Draft EIR, Freedom West 2.0, Case No. 2020-006887ENV, SCH 2025050078, January 13, 2026, Volume 1;
the CEQAnet copy, whose text layer can't be extracted, so the pages were read as images):
- Figure 2-9, "Proposed Project Common Parcel/Building Identifiers and Total Development" (p. 2-21, PDF p. 147),
  1:1,800: the project site's dashed outline and the dashed lines between the 15 building parcels (NW-CO-OP,
  NE-A to NE-D, SW-A to SW-F, SE-A to SE-D) and the two halves of Octavia Green. Totals box: "Unit Count:
  2,291 Units", "Hotel: 108,000 SF".
- Figure 2-8, "Proposed Height and Bulk Map" (p. 2-19, PDF p. 145): one height district per parcel: 85-X on
  most parcels, 185-X on NE-D, 165-X on SW-A and SW-F, 335-X on SE-A, 105-X on SE-C, 225-X on SE-D, OS on the
  two halves of Octavia Green.
- Figure 2-10, "Proposed Project Aerial Perspective: Facing Southeast" (p. 2-22, PDF p. 148): each building
  labelled with the same heights ("SE-A 335 ft", "SE-D 225 ft", "NE-D 185 ft", "SW-A 165 ft", "SW-F 165 ft",
  "SE-C HOTEL 105 ft", the others "85 ft").
- Table 2-2, "Characteristics of Proposed Buildings on the Project Site" (p. 2-25, PDF p. 151): homes and
  floor area per building; Table 2-3, "Preliminary Construction Phasing Program" (p. 2-38, PDF p. 164): the
  phases (1A NW-CO-OP; 1B NE-B, NE-C, NE-D; 1C NE-A; 2A SW-E, SW-F; 2B SW-A to SW-D; 3A SE-B, SE-D; 3B SE-A,
  SE-C).
- Text, p. 2-20: "Although the building designs have not been finalized, the building characteristics and land
  uses for each locational prefix at maximum buildout are summarized in Table 2-2".

What this is and isn't:
- Each parcel is drawn over its whole area at its proposed height limit. That is an envelope, not a building:
  Figure 2-10 shows courtyards, podiums and setbacks, and the towers (e.g. SE-A, 335 ft) don't fill their
  parcels. All 15 volumes are illustrative and drawn as proposed, since nothing is approved.
- The two halves of Octavia Green (privately owned public open space) aren't drawn.

Georeferencing: Figure 2-9 is rendered at 250 dpi; the dashed lines were read off that render and are snapped
to the nearest dark column or row (within 4 px) before use. The figure's corners of the block between McAllister
and Fulton streets (all of Block 0783) and the two Gough Street corners of the block to the north are matched to
the same corners of the DataSF parcels (the boundary file's lots) with a least-squares similarity fit; residuals
are recorded. The site's west edge on the north block comes from the figure, so the 870-880 McAllister corner,
which the parcel layer still includes in lot 0770/027, is left out of the massing.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_freedom_west
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import box, mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "freedom-west"
UTM = ob.UTM
SQFT = 10.7639

DEIR = {
    "title": "Freedom West 2.0 Draft EIR, Volume 1 (Case No. 2020-006887ENV, January 13, 2026)",
    "url": "https://ceqanet.lci.ca.gov/2025050078/2/Attachment/wdfI_L",
    "sha256": "0c8b1de5b6a2a773d0b6da1dcc6ecf9970b8c5d9bdff609161255e5b6f2d7869",
    "file": "freedom-west-2-deir-vol1-2026-01-13.pdf",
}
FIG_PAGE = 147  # Figure 2-9 (p. 2-21)
DPI = 250

# Dashed lines of Figure 2-9 in the 250-dpi render (px, y down).
X = {"s_west": 573, "n_west": 796, "notch": 813, "sw_ac": 793, "sw_ce": 991, "sw_os": 1218, "se_os": 1359,
     "se_ab": 1613, "se_bd": 1803, "n_os": 1187, "ne_os": 1327, "ne_ab": 1543, "ne_bc": 1727, "east": 1972}
Y = {"n_top": 465, "ne_cd": 715, "notch_top": 681, "notch_bot": 791, "n_bot": 895, "s_top": 1005, "sw_mid": 1219,
     "se_ac": 1231, "s_bot": 1435}

# label -> (x0, y0, x1, y1 keys), height (ft, Figure 2-8 / 2-10), phase (Table 2-3), use and homes (Table 2-2).
PARCELS = {
    "NW-CO-OP": (("n_west", "n_top", "n_os", "n_bot"), 85, "Phase 1A",
                 "Homes (267 replacement co-op homes), an innovation center, a community event space and shops"),
    "NE-A": (("ne_os", "n_top", "ne_ab", "n_bot"), 85, "Phase 1C", "Homes (133), a childcare center and shops"),
    "NE-B": (("ne_ab", "n_top", "ne_bc", "n_bot"), 85, "Phase 1B", "Homes (176) and shops"),
    "NE-C": (("ne_bc", "n_top", "east", "ne_cd"), 85, "Phase 1B", "Homes (135)"),
    "NE-D": (("ne_bc", "ne_cd", "east", "n_bot"), 185, "Phase 1B", "Homes (224) and shops"),
    "SW-A": (("s_west", "s_top", "sw_ac", "sw_mid"), 165, "Phase 2B", "Homes (166)"),
    "SW-B": (("s_west", "sw_mid", "sw_ac", "s_bot"), 85, "Phase 2B", "Homes (74) and shops"),
    "SW-C": (("sw_ac", "s_top", "sw_ce", "sw_mid"), 85, "Phase 2B", "Homes (72) and shops"),
    "SW-D": (("sw_ac", "sw_mid", "sw_ce", "s_bot"), 85, "Phase 2B", "Homes (74) and shops"),
    "SW-E": (("sw_ce", "s_top", "sw_os", "sw_mid"), 85, "Phase 2A", "Homes (81) and shops"),
    "SW-F": (("sw_ce", "sw_mid", "sw_os", "s_bot"), 165, "Phase 2A", "Homes (140) and shops"),
    "SE-A": (("se_os", "s_top", "se_ab", "se_ac"), 335, "Phase 3B", "Homes (311) and shops"),
    "SE-C": (("se_os", "se_ac", "se_ab", "s_bot"), 105, "Phase 3B", "Hotel (150 rooms) and shops"),
    "SE-B": (("se_ab", "s_top", "se_bd", "s_bot"), 85, "Phase 3A", "Homes (151) and shops"),
    "SE-D": (("se_bd", "s_top", "east", "s_bot"), 225, "Phase 3A", "Homes (287) and shops"),
}
NOTES = {
    "NW-CO-OP": "The 267 replacement homes for Freedom West's co-op shareholders, built first (Phase 1A).",
    "SE-A": "The tallest building, up to 335 ft and 32 stories (Table 2-1 gives 8 to 32 stories). Under the "
            "Draft EIR's land use variant the 150-room hotel could be here instead of on SE-C.",
    "SE-C": "A 105-ft, 108,000 gsf, 150-room hotel with its entrance on Fulton Street (p. 2-24).",
}


def render_page(path) -> np.ndarray:
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(path))
    return np.asarray(pdf[FIG_PAGE - 1].render(scale=DPI / 72).to_pil().convert("RGB"))


def snap(rgb: np.ndarray) -> tuple[dict, dict, list]:
    """Move each read-off line to the darkest column/row within 4 px; report the shifts."""
    dark = rgb.astype(int).sum(axis=2) < 250
    xs, ys, moved = dict(X), dict(Y), []
    for k, x in X.items():
        span = dark[Y["n_top"]:Y["s_bot"], x - 4:x + 5].sum(axis=0)
        xs[k] = x - 4 + int(np.argmax(span))
        if xs[k] != x:
            moved.append((k, x, xs[k]))
    for k, y in Y.items():
        span = dark[y - 4:y + 5, X["s_west"]:X["east"]].sum(axis=1)
        ys[k] = y - 4 + int(np.argmax(span))
        if ys[k] != y:
            moved.append((k, y, ys[k]))
    return xs, ys, moved


def corners(poly) -> dict:
    """NW, NE, SE and SW vertices of a near-rectangular polygon in UTM (x east, y north)."""
    poly = trace.largest_polygon(poly)
    xy = np.array(poly.exterior.coords)[:-1]
    return {"nw": xy[np.argmin(xy[:, 0] - xy[:, 1])], "ne": xy[np.argmax(xy[:, 0] + xy[:, 1])],
            "se": xy[np.argmax(xy[:, 0] - xy[:, 1])], "sw": xy[np.argmin(xy[:, 0] + xy[:, 1])]}


def main() -> None:
    pdf = trace.fetch_document(DEIR["url"], config.ROOT / "data" / "raw" / "docs" / DEIR["file"], DEIR["sha256"])
    rgb = render_page(pdf)
    xs, ys, moved = snap(rgb)
    print(f"[freedom-west] figure lines snapped: {moved or 'none moved'}")

    fc_lots = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    lots = gpd.GeoDataFrame(
        {"blklot": [f["properties"].get("blklot") for f in fc_lots["features"]]},
        geometry=ob._utm_shapes(fc_lots).to_numpy(), crs=UTM,
    )
    site = shapely.union_all(lots.buffer(0.5).to_numpy()).buffer(-0.5)
    south = shapely.union_all(lots[lots.blklot.str.startswith("0783")].buffer(0.5).to_numpy()).buffer(-0.5)
    north = lots[lots.blklot == "0770027"].geometry.iloc[0]
    sc, nc = corners(south), corners(north)

    src = [(xs["s_west"], ys["s_top"]), (xs["east"], ys["s_top"]), (xs["east"], ys["s_bot"]),
           (xs["s_west"], ys["s_bot"]), (xs["east"], ys["n_top"]), (xs["east"], ys["n_bot"])]
    dst = [sc["nw"], sc["ne"], sc["se"], sc["sw"], nc["ne"], nc["se"]]
    labels = ["Laguna/McAllister (Block 0783)", "Gough/McAllister (Block 0783)", "Gough/Fulton", "Laguna/Fulton",
              "Gough/Golden Gate (lot 0770/027)", "Gough/McAllister (lot 0770/027)"]
    sim = trace.fit_similarity(src, dst, labels)
    rep = sim.report()
    print(f"[freedom-west] fit: {sim.scale / 0.3048:.4f} ft/px, rotation {rep['rotation_deg']} deg, RMS {sim.rms_m:.2f} m; "
          + ", ".join(f"{c['label']} {c['residual_m']} m" for c in rep["controls"]))

    notch = box(xs["n_west"], ys["notch_top"], xs["notch"], ys["notch_bot"])
    features = []
    total = 0.0
    for label, ((k0, k1, k2, k3), h, phase, use) in PARCELS.items():
        fig = box(xs[k0], ys[k1], xs[k2], ys[k3])
        if label == "NW-CO-OP":
            fig = fig.difference(notch)
        geom = sim.geometry(fig).intersection(site)
        geom = geom if geom.geom_type == "Polygon" else max(geom.geoms, key=lambda p: p.area)
        total += geom.area
        wgs = gpd.GeoSeries([geom.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
        note = (f"Parcel {label} drawn whole at its proposed {h}-ft height limit (Figure 2-8), an envelope rather than "
                f"a building: the real building has courtyards, setbacks or a lower podium. {NOTES.get(label, '')}").strip()
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": f"Building {label}", "stage": "proposed", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": phase, "illustrative": True,
                "source": (f"illustrative: parcel traced from {DEIR['title']}, Figure 2-9 (PDF p. {FIG_PAGE}); height "
                           f"from Figure 2-8 (PDF p. 145) and Figure 2-10 (PDF p. 148)"),
                "note": note,
            },
            "geometry": mapping(wgs),
        })
        print(f"[freedom-west] {label}: {geom.area * SQFT:,.0f} sq ft at {h} ft ({phase})")
    print(f"[freedom-west] {len(features)} parcels, {total * SQFT:,.0f} sq ft; site as drawn {site.area * SQFT:,.0f} sq ft")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the 15 building parcels of the Draft EIR's site plan (Figure 2-9), each "
                        "drawn whole at its proposed height limit (Figure 2-8): 85 ft on most parcels, 105 ft for the "
                        "hotel, 165 ft on SW-A and SW-F, 185 ft on NE-D, 225 ft on SE-D and 335 ft on SE-A. These are "
                        "envelopes, not building designs, which aren't final; the real buildings have courtyards and "
                        "setbacks. Octavia Green isn't drawn."),
            "note": "Proposed height limits over each building parcel, not buildings.",
            "sourceUrl": DEIR["url"],
            "sourceLabel": "Freedom West 2.0 Draft EIR, January 2026 (PDF)",
            "georeference": {
                "method": ("Figure 2-9 (250-dpi render) fitted to the DataSF parcel corners of Block 0783 and the Gough "
                           "Street corners of lot 0770/027 (least-squares similarity)."),
                "fit": rep,
            },
            "license": "Parcel lines and heights: from a public SF Planning document. Lots: DataSF parcels (ODC-PDDL).",
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[freedom-west] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
