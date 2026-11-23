"""530 Sansome: the approved 41-story tower and the new Fire Station 13, set out from the EIR's dimensioned plans.

Sources:
- 447 Battery and 530 Sansome Street Project, Draft EIR (SF Planning, case 2024-007066ENV, March 2025; CEQAnet SCH
  2024110311, document 2), Chapter 2, Project Description:
  - Figure 2-15 "High-Rise Building Levels 2-3 Floor Plan" (PDF p. 115): "OVERALL BUILDING DIMENSION 174'-3"" east
    to west by 92'-8 1/2" north to south; 3'-9" from the Sansome Street line, 3'-8" from the Washington Street line,
    2'-7 1/2" from the Merchant Street line.
  - Figures 2-16 and 2-17 (Levels 8 and 14, Levels 16-17; PDF pp. 116-117): 165'-0" by 96'-6", 2'-7" from the
    Sansome Street line, 1'-3" from the Washington and Merchant street lines.
  - Figure 2-18 (Levels 25 and 37; PDF p. 118): 165'-0" by 89'-6" at level 25 (8'-3" from Washington, 1'-3" from
    Merchant); 165'-0" by 67'-6" at level 37 (15'-9" from both).
  - Figure 2-19 (Roof level; PDF p. 119): 165'-0" by 60'-0" (23'-3" from Washington, 15'-9" from Merchant).
  - Figure 2-8 "High-Rise Building North/South Section" (PDF p. 106): level elevations (level 4 +63'-0", level 24
    +304'-4", level 28 +357'-4", level 32 +410'-4", level 36 +463'-4", level 40 +516'-4", lower roof +543'-4",
    upper roof +555'-0", top +573'-4") and the tower's steps. Its north face steps in at levels 24, 32 and 40 and
    its south face at levels 28 and 36, each by about 7 to 7.5 ft, which matches the plan offsets (1'-3", 8'-3",
    15'-9", 23'-3").
  - p. 2-7 (PDF p. 99): the fire station is "a 4-story, approximately 55-foot-tall building (60 feet total to the
    roof, including an amenity space on the fourth floor and rooftop mechanical equipment)" on the 447 Battery
    Street parcel; Figure 2-10 (PDF p. 109) shows it filling that lot.
- The approvals kept these figures: the Notice of Determination (Oct 29, 2025) describes the tower as "approximately
  544 feet tall (574 feet total, including rooftop mechanical equipment)" and the fire station as above.

How it's drawn:
- The tower lots (DataSF parcels 0206/013, 014 and 017) give the frame: the Sansome / Washington corner, with one
  axis east along Washington Street and one south along Sansome Street. The plans' offsets are laid out from the
  Washington and Sansome lines, keeping the plans' building dimensions (the mapped lots are about 101 ft deep on
  Sansome against the plans' 99 ft, so any difference falls on the Merchant Street side).
- The tower is six stacked steps, each a 165-ft-wide rectangle from its own north and south offsets, drawn as rings
  so each step rises from the ground to its own top. The east end of the three-story base (levels 1-3, to the level
  4 floor at 63 ft), which reaches farther east than the tower, is a seventh piece. The fire station is the 447
  Battery Street lot at 55 ft. The rooftop mechanical screen (to 574 ft) and canopies are not drawn. Illustrative.

Stage: approved in 2025 (FEIR certified July 17, 2025; legislation approved by the Board of Supervisors on Oct 21
and signed on Oct 27, 2025); no building permit yet. Drawn as "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_530_sansome
"""

from __future__ import annotations

import itertools
import json

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping, shape

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "530-sansome"
UTM = ob.UTM
FT = 0.3048
SQFT = 10.7639

DEIR = {
    "title": "447 Battery and 530 Sansome Street Project Draft EIR (case 2024-007066ENV, March 2025)",
    "url": "https://ceqanet.lci.ca.gov/2024110311/2/Attachment/NHEHNp",
    "sha256": "d127a20a5cd5cc768044be1817af9c50926607fc394629aebd7fe3a44efe9988",
    "file": "447Battery530SansomeDEIR_2025-03-11.pdf",
}
NOD_URL = "https://ceqanet.lci.ca.gov/2024110311/4/Attachment/BML5I0"

TOWER_LOTS = {"0206013", "0206014", "0206017"}
FIRE_LOT = "0206002"

PLAN_DEPTH_FT = 99.0  # Sansome Street frontage on the plans (offsets + building depth)
TOWER_WEST_FT = 2 + 7 / 12  # Figures 2-16 to 2-19: 2'-7" from the Sansome Street line
TOWER_WIDTH_FT = 165.0
BASE = {"west": 3.75, "width": 174.25, "north": 3 + 8 / 12, "south": 2 + 7.5 / 12, "top": 63.0}  # Figure 2-15

# (label, north offset, south offset, top of the step in ft, plan or section it comes from)
STEPS = [
    ("Tower, levels 4 to 23", 1.25, 1.25, 304 + 4 / 12, "Figures 2-16 and 2-17 (levels 8, 14, 16-17)"),
    ("Tower, levels 24 to 27", 8.25, 1.25, 357 + 4 / 12, "Figure 2-18 (level 25)"),
    ("Tower, levels 28 to 31", 8.25, 8.25, 410 + 4 / 12, "Figure 2-8 (section) with Figure 2-18"),
    ("Tower, levels 32 to 35", 15.75, 8.25, 463 + 4 / 12, "Figure 2-8 (section) with Figure 2-18"),
    ("Tower, levels 36 to 39", 15.75, 15.75, 516 + 4 / 12, "Figure 2-18 (level 37)"),
    ("Tower, levels 40 and 41", 23.25, 15.75, 544.0, "Figure 2-19 (roof level)"),
]
USES = {
    "Tower, levels 4 to 23": "Hotel (levels 4 to 14), office amenities (16 and 17) and office",
}
FIRE_STATION_FT = 55.0


def lots() -> dict[str, shapely.Geometry]:
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    out = {}
    for f in fc["features"]:
        g = gpd.GeoSeries([shapely.make_valid(shape(f["geometry"]))], crs=4326).to_crs(UTM).iloc[0]
        out[f["properties"]["blklot"]] = g
    return out


def frame(tower_lots: shapely.Geometry) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """The Sansome / Washington corner, a unit vector east along Washington and one south along Sansome."""
    poly = tower_lots.buffer(0.3).buffer(-0.3).simplify(0.05)
    if poly.geom_type != "Polygon":
        poly = max(poly.geoms, key=lambda p: p.area)
    xy = np.array(poly.exterior.coords)[:-1]
    i = int(np.argmax(xy[:, 1] - xy[:, 0]))  # north-west corner
    corner = xy[i]
    edges = [xy[(i + 1) % len(xy)] - corner, xy[i - 1] - corner]
    east = max(edges, key=lambda v: v[0])
    south = min(edges, key=lambda v: v[1])
    check = {
        "washington_frontage_ft": round(float(np.linalg.norm(east)) / FT, 1),
        "sansome_frontage_ft": round(float(np.linalg.norm(south)) / FT, 1),
        "corner_angle_deg": round(float(np.degrees(np.arccos(east @ south / np.linalg.norm(east) / np.linalg.norm(south)))), 2),
    }
    return corner, east / np.linalg.norm(east), south / np.linalg.norm(south), check


def main() -> None:
    # The plans and section this module transcribes, pinned (about 20 MB).
    trace.fetch_document(DEIR["url"], config.ROOT / "data" / "raw" / "docs" / DEIR["file"], DEIR["sha256"])
    parcels = lots()
    tower_lots = shapely.union_all([parcels[k].buffer(0.3) for k in TOWER_LOTS]).buffer(-0.3)
    fire_lot = parcels[FIRE_LOT]
    site = shapely.union_all([g.buffer(0.5) for g in parcels.values()]).buffer(-0.5)
    corner, east, south, check = frame(tower_lots)
    print(f"[530-sansome] tower lots {tower_lots.area * SQFT:,.0f} sq ft; as mapped: Washington {check['washington_frontage_ft']} ft "
          f"(EIR 179), Sansome {check['sansome_frontage_ft']} ft (EIR 99); corner {check['corner_angle_deg']} deg")

    def at(u: float, v: float) -> np.ndarray:
        return corner + east * u * FT + south * v * FT

    def rect(u0: float, u1: float, v0: float, v1: float) -> Polygon:
        return Polygon([at(u0, v0), at(u1, v0), at(u1, v1), at(u0, v1)])

    u0, u1 = TOWER_WEST_FT, TOWER_WEST_FT + TOWER_WIDTH_FT
    steps = [(label, rect(u0, u1, n, PLAN_DEPTH_FT - s), top, fig) for label, n, s, top, fig in STEPS]
    for (_, a, _, _), (_, b, _, _) in itertools.pairwise(steps):
        if not b.within(a.buffer(0.01)):
            raise SystemExit("530 Sansome: a tower step is not inside the one below it")
    base = rect(BASE["west"], BASE["west"] + BASE["width"], BASE["north"], PLAN_DEPTH_FT - BASE["south"])
    for g in [base, steps[0][1]]:
        if not g.within(tower_lots.buffer(0.05)):
            raise SystemExit("530 Sansome: the base or tower falls outside the tower lots")

    plan = f"{DEIR['title']}, Chapter 2"
    parts = []
    base_east = base.difference(steps[0][1])
    parts.append(("Base, levels 1 to 3 (east end)", base_east, BASE["top"],
                  "Lobbies, drop-off and loading, ballroom and meeting rooms",
                  f"illustrative: the levels 2-3 plan (174 ft 3 in by 92 ft 8 1/2 in) in the {plan}, Figure 2-15 (PDF p. "
                  f"115), less the tower; height to the level 4 floor (+63 ft) in Figure 2-8 (PDF p. 106)",
                  "The east end of the three-story base, which reaches farther east than the tower above it, over the "
                  "drive-through drop-off and the loading dock off Washington Street."))
    for i, (label, g, top, fig) in enumerate(steps):
        ring = g.difference(steps[i + 1][1]) if i + 1 < len(steps) else g
        last = i + 1 == len(steps)
        note = ("Roof at about 544 ft (lower roof +543 ft 4 in in the section); the upper roof is at 555 ft and the "
                "rooftop mechanical screen reaches about 574 ft (Notice of Determination: “574 feet total, including "
                "rooftop mechanical equipment”). 165 by 60 ft." if last else
                f"Steps in above +{top:.0f} ft. Each step is 165 ft east to west; the tower narrows from north to south "
                "as it rises.")
        parts.append((label, ring, round(top, 1), USES.get(label, "Office"),
                      f"illustrative: 165 ft wide at the offsets in the {plan}, {fig}; step heights from the level "
                      f"elevations in Figure 2-8 (PDF p. 106)",
                      note))
    parts.append(("Fire Station 13", fire_lot, FIRE_STATION_FT, "Fire station (San Francisco Fire Department)",
                  f"illustrative: the 447 Battery Street lot (DataSF parcel 0206/002) at the height in the {plan}, p. 2-7 "
                  f"(PDF p. 99) and Figure 2-10 (PDF p. 109)",
                  "A four-story replacement for Fire Station 13, about 55 ft tall (60 ft to the top of its rooftop "
                  "amenity space and equipment), with one basement level. The developer builds it for the City; the "
                  "existing station at 530 Sansome Street stays in service until it's done."))

    features = []
    for label, geom, h, use, source, note in parts:
        if not geom.within(site.buffer(0.1)):
            raise SystemExit(f"530 Sansome: {label} falls outside the site")
        # The step differences leave hairline slivers along the edges the steps share; open them away.
        geom = geom.buffer(-0.01, join_style="mitre").buffer(0.01, join_style="mitre")
        wgs = gpd.GeoSeries([geom.simplify(0.05)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "entitled", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": None, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        })
        print(f"[530-sansome] {label}: {geom.area * SQFT:,.0f} sq ft, {h} ft")

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the approved 41-story tower as six steps, set out from the dimensioned "
                        "floor plans in the 2025 Draft EIR (165 ft wide, narrowing from 96 ft 6 in deep at the hotel "
                        "floors to 60 ft at the top), to its roof at about 544 ft, with the east end of its three-story "
                        "base; and the four-story, 55-ft Fire Station 13 on the 447 Battery Street lot. The rooftop "
                        "screen to 574 ft is not drawn."),
            "note": "The approved buildings as simple stepped volumes, not the final design.",
            "sourceUrl": DEIR["url"],
            "sourceLabel": "Draft EIR, 2025 (PDF)",
            "envelopeSourceUrl": NOD_URL,
            "georeference": {
                "method": ("Plan offsets laid out from the Sansome Street / Washington Street corner of the DataSF "
                           "parcels for the tower (0206/013, 014, 017), along their two frontages."),
                "frontages_as_mapped": check,
            },
            "license": "Dimensions: from a public SF Planning document. Lots: DataSF parcels (ODC-PDDL).",
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[530-sansome] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
