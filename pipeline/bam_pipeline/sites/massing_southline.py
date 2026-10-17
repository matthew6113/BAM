"""Southline: illustrative massing from the Revised Southline Specific Plan's height figure.

Source: Revised Southline Specific Plan (Final EIR Appendix 2.1, May 2022, CEQAnet SCH 2020050452),
Figure 2-8, Conceptual Building Heights (plan p. 2-23, Final EIR PDF p. 935). It colours each
conceptual building footprint by height: 80, 105, 115 or 120 ft. The plan's own height standard is
the FAA Part 77 / SFO ALUCP limit, about 120 ft (Table 2-1), and it calls its site plans one possible
design, so every footprint here is an illustrative envelope, not a building design.

Phases come from Figure 2-9, Conceptual Phasing Plan (p. 2-35), drawn on the same photo frame:
Buildings 1, 2 and 7 and Parking Structure D in Phase 1; Buildings 3 to 6 and Parking Structure C
in future phases.

Georeference: the figure's aerial photo fitted to OpenStreetMap building footprints, shared with
boundary_southline.py. Colour regions are classified against the legend swatches, with the photo's
greys as extra classes so pale fills don't bleed into the background; each region is named by the
building label printed inside it. Buildings 4 and 5 touch in the figure and are drawn as one zone.

No building is drawn as built: the press reports Phase 1 under construction, but no City permit
record could be checked (ssf.net could not be reached), so Phase 1 stays at the entitled stage.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_southline
"""

from __future__ import annotations

import json

import geopandas as gpd
import shapely
from shapely.geometry import Point, mapping

from .. import config, trace
from . import boundary_southline as bs
from . import traced_boundaries as tb

PROJECT = "southline"
OUT = config.ROOT / "data" / "massing" / f"{PROJECT}.geojson"
PALETTE = {
    80: (245, 234, 194), 105: (210, 233, 247), 115: (220, 240, 217), 120: (248, 175, 166),
    "photo light": (238, 238, 238), "photo grey": (226, 226, 226), "photo mid": (210, 210, 210), "white": (252, 252, 252),
}
# Building labels printed in Figure 2-8 (px) -> (label, use, phase).
LABELS = [
    ((600, 170), "Buildings 4 and 5", "office/R&D", "Future phase"),
    ((449, 424), "Buildings 4 and 5", "office/R&D", "Future phase"),
    ((771, 304), "Parking Structure C", "parking", "Future phase"),
    ((886, 408), "Building 6", "office/R&D", "Future phase"),
    ((586, 536), "Building 3", "office/R&D", "Future phase"),
    ((918, 584), "Building 7", "office/R&D", "Phase 1"),
    ((710, 712), "Building 1", "office/R&D", "Phase 1"),
    ((536, 754), "Building 2 (amenities)", "amenities, retail and dining", "Phase 1"),
    ((875, 738), "Parking Structure D", "parking", "Phase 1"),
]
# Phase 1 figures from the Final EIR (Alternative D, Table 5-4) and the Draft EIR (Table 3-10), for the notes.
NOTES = {
    "Building 1": "Final EIR Alternative D (which the revised plan follows): about 318,380 sq ft; the Draft EIR's Phase 1 description gave 6 stories, 113 ft.",
    "Building 7": "Final EIR Alternative D (which the revised plan follows): about 296,620 sq ft; the Draft EIR's Phase 1 description gave 6 stories, 113 ft.",
    "Building 2 (amenities)": "Final EIR Alternative D: about 69,710 sq ft, reduced from four stories to three; the Draft EIR gave 4 stories, 60 ft.",
    "Parking Structure D": "Added by Final EIR Alternative D on the 80 Tanforan Avenue property, in place of building Parking Structure C in Phase 1.",
    "Parking Structure C": "The Draft EIR described a nine-story garage, 90 ft to the parapet; the revised plan builds it in a future phase.",
}
SOURCE = ("illustrative: drawn to the {h}-ft height in the Revised Southline Specific Plan (Final EIR Appendix 2.1, "
          "May 2022), Figure 2-8, Conceptual Building Heights, p. 2-23; phase from Figure 2-9")


def main() -> None:
    sim, rep = bs.georeference()
    rgb = bs.figure().astype(int)
    regions = trace.raster_classify_regions(rgb, PALETTE, max_dist=40, open_px=3, close_px=9, min_area_px=1500)
    regions = [(k, p) for k, p in regions if isinstance(k, int)]
    site = shapely.geometry.shape(json.loads((tb.OUT / f"{PROJECT}.geojson").read_text())["features"][0]["geometry"])
    site_utm = gpd.GeoSeries([site], crs=4326).to_crs(tb.UTM).iloc[0]

    zones: dict[str, dict] = {}
    for (x, y), label, use, phase in LABELS:
        hit = [(k, p) for k, p in regions if p.buffer(3).contains(Point(x, y))]
        if len(hit) != 1:
            raise SystemExit(f"{label}: {len(hit)} colour regions under its label at ({x}, {y})")
        h, poly = hit[0]
        z = zones.setdefault(label, {"height": h, "use": use, "phase": phase, "px": poly})
        if z["height"] != h:
            raise SystemExit(f"{label}: two heights")
    feats = []
    for label, z in zones.items():
        g = bs.to_utm(sim, z["px"].simplify(1.2)).intersection(site_utm.buffer(1.0))
        g = g.simplify(0.4, preserve_topology=True)
        props = {
            "kind": "block",
            "block": label.split(" (")[0],
            "label": label,
            "stage": "entitled",
            "height_ft": z["height"],
            "podium_ft": None,
            "base_ft": 0,
            "use": z["use"],
            "phase": z["phase"],
            "illustrative": True,
            "source": SOURCE.format(h=z["height"]),
        }
        if label in NOTES:
            props["note"] = NOTES[label]
        feats.append({"type": "Feature", "properties": props, "geometry": mapping(tb.to_wgs(g))})
        print(f"  {label}: {z['height']} ft, {g.area:,.0f} m2, {z['phase']}")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT,
            "illustrative": True,
            "summary": (
                "Illustrative massing: the conceptual building footprints of the Revised Southline Specific Plan "
                "(May 2022), each raised to the height its Figure 2-8 gives (80 to 120 ft), not a building design. "
                "The plan's binding height limit is the airport (FAA and SFO ALUCP) limit of about 120 ft, and its "
                "site plans are one possible layout. Buildings 1, 2 and 7 and Parking Structure D are Phase 1; the "
                "rest are future phases. No building is drawn as built: the City's permit records were not checked."),
            "note": "Conceptual footprints raised to the heights in the 2022 Specific Plan figure; real buildings will differ.",
            "sourceUrl": bs.FEIR["url"],
            "sourceLabel": "Revised Specific Plan, Figure 2-8 (Final EIR, May 2022, PDF)",
            "georeference": {"Figure 2-8": rep},
            "license": ("Footprints: traced from a public City of South San Francisco document (the PDF is not "
                        f"redistributed). Georeference: {tb.OSM_LICENSE}."),
        },
        "features": feats,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tb._round(fc), indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(config.ROOT)}: {len(feats)} zones")


if __name__ == "__main__":
    main()
