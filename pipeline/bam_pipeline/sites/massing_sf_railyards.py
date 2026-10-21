"""SF Railyards: illustrative height envelopes from the proposed height district plan.

Source: San Francisco Planning Department, Notice of Preparation of an EIR, Railyards Mixed-Use Development
Project (Case No. 2026-002123ENV, Sept 30, 2026; CEQAnet SCH 2026091295), Figure 3, Height District Plan
(PDF p. 13; "SOURCE: Prologis 4th and King LLC, 2026"). The figure shows the sponsor's proposed height
districts for a new Railyards Special Use District, which the Board of Supervisors hasn't adopted: blocks 1
(855 ft, with a second tower to 575 ft), 2A (500), 2B (625), 3A (500), 3B (400), 3C (550), 4 (350) and 5
(450). The NOP's text (p. 7) gives the same ranges: 400 to 855 ft on the Eastern Parcels, 350 to 450 ft on
the Western Parcels.

Method: the figure (a 500-ppi raster) is rendered at 200 dpi; each pixel inside the dashed project
boundary takes the nearest legend colour; regions are traced and named by block from where they sit in
the figure. The figure is drawn to scale with Townsend Street level, so it is registered to the parcel
union (data/boundaries/sf-railyards.geojson) by a similarity fit on the four corners of the dashed
project boundary (Townsend at Seventh and Fourth, King at Fourth, Seventh at the site's southern tip);
the zones are then clipped to the parcels.

Each block is drawn whole and raised to its height limit: an envelope, not a building. The plan allows
towers, not 855-ft slabs: the figure's note limits Block 1 to one tower of 855 ft and a second of 575 ft.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_sf_railyards
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import box, mapping, shape

from .. import config, trace
from . import traced_boundaries as tb

PROJECT = "sf-railyards"
NOP_URL = "https://ceqanet.lci.ca.gov/2026091295/Attachment/tPsmWg"
NOP_SHA = "049ffb000b0bd9a8b34d363cb676683746c3feef9187c4056e113c24444c598c"
NOP = tb.DOCS / "sf-railyards-nop-2026-09.pdf"
PAGE = 12  # zero-based: PDF p. 13, Figure 3, Height District Plan
DPI = 200
SOURCE = ("San Francisco Planning, Notice of Preparation of an EIR, Railyards Mixed-Use Development Project "
          "(Case No. 2026-002123ENV, Sept 30, 2026), Figure 3, Height District Plan, p. 13")

# Legend swatches (RGB, sampled from the 200-dpi render) -> height limit in feet.
LEGEND = {
    855: (85, 50, 144),
    625: (128, 107, 172),
    550: (145, 40, 141),
    500: (198, 30, 126),
    450: (223, 120, 175),
    400: (236, 180, 209),
    350: (251, 224, 233),
}
# The dashed project boundary's corners in the 200-dpi render (pixels; measured from the dash rows and
# columns) and the matching corners of the parcel union.
CORNERS_PX = {
    "Townsend Street at Seventh Street": (301.0, 309.0),
    "Townsend Street at Fourth Street": (1896.0, 309.0),
    "King Street at Fourth Street": (1896.0, 474.5),
    "Seventh Street at the site's southern tip": (301.0, 668.0),
}
# Independent check: street centrelines crossing Townsend Street in the figure (midway between the curb
# lines, px along Townsend) against OpenStreetMap's Townsend intersections (via Overture).
CHECK_STREETS_PX = {"4th Street": 1922.0, "5th Street": 1375.5}
WINDOW_PX = (301, 309, 1897, 669)  # inside the dashed boundary
# Blocks by their x-range in the render (px), left to right, as labelled in the figure.
BLOCKS_X = [("5", 301, 560), ("4", 300, 830), ("3C", 830, 1035), ("3B", 1035, 1200), ("3A", 1200, 1350),
            ("2B", 1395, 1530), ("2A", 1530, 1670), ("1", 1690, 1897)]
PHASE = {"1": "Development Phase 1 (Phase 1.1)", "5": "Development Phase 1 (Phase 1.2)",
         "2A": "Development Phase 2 (Phase 2.1)", "2B": "Development Phase 2 (Phase 2.1)",
         "3A": "Development Phase 2 (Phase 2.2)", "3B": "Development Phase 2 (Phase 2.2)",
         "3C": "Development Phase 2 (Phase 2.2)", "4": "Development Phase 2 (Phase 2.3)"}


def _render() -> np.ndarray:
    import pypdfium2 as pdfium

    trace.fetch_document(NOP_URL, NOP, NOP_SHA)
    return np.asarray(pdfium.PdfDocument(str(NOP))[PAGE].render(scale=DPI / 72).to_pil().convert("RGB"))


def _site_utm():
    fc = json.loads((tb.OUT / f"{PROJECT}.geojson").read_text())
    site = shape(next(f for f in fc["features"] if f["properties"].get("kind") == "site")["geometry"])
    return gpd.GeoSeries([site], crs=4326).to_crs(tb.UTM).iloc[0]


def _corners_utm(site) -> list[tuple[float, float]]:
    """The parcel union's corners matching CORNERS_PX: extreme points along and across Townsend Street."""
    pts = np.asarray(site.exterior.coords[:-1])
    along = np.array([1.0, 1.0]) / np.sqrt(2)  # Townsend runs about 45 degrees east of north here
    across = np.array([1.0, -1.0]) / np.sqrt(2)
    a, c = pts @ along, pts @ across
    nw = pts[np.argmin(a - 0.001 * c)]
    ne = pts[np.argmax(a - c)]  # the Fourth/Townsend corner: far along, on the Townsend side
    se = pts[np.argmax(a + c)]
    sw = pts[np.argmax(c - a)]  # the southern tip on Seventh Street
    return [tuple(nw), tuple(ne), tuple(se), tuple(sw)]


def _street_check(sim: trace.Similarity) -> list[dict]:
    """How far each figure street lies along Townsend Street from OpenStreetMap's (metres)."""
    streets = tb.streets("sf-railyards", (-122.405, 37.768, -122.388, 37.781))
    inv = np.linalg.inv(sim.matrix())
    out = []
    for name, x in CHECK_STREETS_PX.items():
        p = np.asarray(tb.intersection(streets, "Townsend Street", name)) - [sim.tx, sim.ty]
        fx = (inv @ p)[0]
        out.append({"label": f"Townsend Street / {name} (along Townsend)", "residual_m": round(abs(fx - x) * sim.scale, 1)})
    return out


def _block_of(x: float) -> str:
    for name, x0, x1 in BLOCKS_X:
        if x0 <= x < x1:
            return name
    raise SystemExit(f"no block at x={x:.0f}px")


def build() -> None:
    rgb = _render()
    site = _site_utm()
    sim = trace.fit_similarity(list(CORNERS_PX.values()), _corners_utm(site), list(CORNERS_PX))
    if sim.rms_m > 5:
        raise SystemExit(f"corner fit too loose: {sim.report()}")

    x0, y0, x1, y1 = WINDOW_PX
    sub = rgb[y0:y1, x0:x1]
    palette = {h: c for h, c in LEGEND.items()}
    regions = trace.raster_classify_regions(sub, palette, max_dist=22, open_px=3, close_px=25, min_area_px=1500)
    zones: dict[tuple[str, int], list] = {}
    for height, poly in regions:
        poly = shapely.affinity.translate(poly, x0, y0)
        c = poly.representative_point()
        # The 350-ft pink also tints the "rail transitioning below grade" edges and labels; Block 4 is the
        # only 350-ft district, and Block 5 the only 450-ft one.
        block = "4" if height == 350 else "5" if height == 450 else _block_of(c.x)
        zones.setdefault((block, height), []).append(poly)

    features = []
    for (block, height), polys in sorted(zones.items(), key=lambda kv: -kv[0][1]):
        px = shapely.union_all(polys).buffer(4, join_style="mitre").buffer(-4, join_style="mitre")
        geom = shapely.make_valid(sim.geometry(px)).intersection(site)
        geom = geom.simplify(0.4, preserve_topology=True)
        if geom.is_empty or geom.area < 200:
            continue
        label = "Block 1 (1A and 1B)" if block == "1" else f"Block {block}"
        note = None
        if block == "1":
            note = ("The figure limits Block 1 to one tower of 855 ft and a second tower of 575 ft (marked on 1A); "
                    "the block also holds the new Caltrain Station Hall. The rest of the block would be lower.")
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "block", "block": block, "label": label, "stage": "entitlement",
                "height_ft": height, "podium_ft": None, "base_ft": 0, "use": None, "phase": PHASE[block],
                "illustrative": True,
                "source": f"illustrative: drawn to the proposed height limit traced from {SOURCE}; phases from NOP pp. 23-26",
                **({"note": note} if note else {}),
            },
            "geometry": mapping(trace.as_multipolygon(tb.to_wgs(geom))),
        })
    found = {f["properties"]["block"] for f in features}
    expected = {b for b, _, _ in BLOCKS_X}
    if found != expected:
        raise SystemExit(f"blocks traced {sorted(found)} != expected {sorted(expected)}")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT,
            "illustrative": True,
            "summary": ("Illustrative height envelopes: the eight development blocks of the sponsor's proposed height "
                        "district plan in the Planning Department's September 2026 notice of preparation (Figure 3), "
                        "each drawn whole and raised to its proposed limit, 350 to 855 ft. The heights are proposed, "
                        "not adopted, and are limits, not building designs: Block 1 would have one 855-ft tower and a "
                        "second of 575 ft, not an 855-ft block. Streets, parks, the station plazas and the rail "
                        "corridor are left empty."),
            "note": "Proposed height limits from the 2026 notice of preparation; limits, not buildings, and not yet adopted.",
            "sourceUrl": NOP_URL,
            "sourceLabel": "Notice of preparation, Figure 3, 2026 (PDF)",
            "georeference": {"figure_3": sim.report(), "check": _street_check(sim), "method": "similarity fit on the dashed project boundary's "
                             "four corners to the DataSF parcel union, then clipped to the parcels"},
            "license": "Zones traced from a public City document; site: DataSF parcels (ODC-PDDL)",
            "documents": [NOP_URL, "https://ceqanet.lci.ca.gov/2026091295", "https://data.sf.gov/d/acdm-wktn"],
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT}.geojson"
    out.write_text(json.dumps(tb._round(fc), indent=1) + "\n")
    print(f"[massing] {PROJECT}: {len(features)} blocks, corner fit RMS {sim.rms_m:.1f} m")
    for f in features:
        p = f["properties"]
        print(f"  {p['label']}: {p['height_ft']} ft")


def main() -> None:
    build()


if __name__ == "__main__":
    main()
