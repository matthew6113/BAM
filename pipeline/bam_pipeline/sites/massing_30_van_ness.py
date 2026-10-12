"""30 Van Ness: the approved podium and tower, set out from the plan sheet's dimensions.

Sources:
- Planning Commission packet for Record No. 2017-008051 (hearing May 21, 2020), PDF page 488: the
  architect's "Typical residential floor plan L13-L15", dimensioned on the lot. The lot is 164 ft on Fell
  Street and 275 ft on Van Ness Avenue; the tower's west face is 12 ft east of the Van Ness Avenue line
  and its north face 55 ft 7 in south of the Fell Street line (40 ft 7 in to the "line of 115' tower
  separation setback to 100 Van Ness" plus 15 ft); the tower is 141 ft long.
- The same packet's draft Downtown Project Authorization (PDF pp. 34-35): "a 9-story podium reaching a
  maximum height of 130'", a tower roof "up to 520'", a maximum plan length of 141 ft and a 169 ft 4 in
  maximum diagonal; and (p. 15) "The footprint of the residential tower occupies 13,200 square feet".
- Motion 21700 (March 13, 2025), the latest approval, keeps the envelope: "a 47-story mixed-use building
  reaching a roof height up to 520 feet tall (540 feet inclusive of rooftop screening/mechanical
  equipment)", and the November 2024 changes (Motion 21643) "would not change the building envelope".

How it's drawn:
- The lot is the DataSF parcel (0835/004), as in the boundary file. The tower is a 141 ft by 93.6 ft
  rectangle (13,200 sq ft over the 141 ft length, which also gives the 169 ft diagonal) at the plan's
  offsets from the Van Ness and Fell corner; the real floor plate is faceted, and the top five floors
  slope down toward Fell Street. The podium is the rest of the lot at 130 ft. Illustrative.

Stage: the developer began construction on July 18, 2022 and halted it after about 16 months (Ordinance
01-25); in March 2025 the site was "an excavated construction site, with initial foundation work
performed" (Motion 21700). Both volumes are drawn as "paused".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_30_van_ness
"""

from __future__ import annotations

import json

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import Polygon, mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "30-van-ness"
UTM = ob.UTM
FT = 0.3048
SQFT = 10.7639

PACKET = {
    "title": "Planning Commission packet, Record No. 2017-008051 (30 Van Ness Avenue), hearing May 21, 2020",
    "url": "https://commissions.sfplanning.org/cpcpackets/2017-008051DNXCUAOFASHDENV.pdf",
    "sha256": "d5855a89d13516965cd5dff3ccf30d4297688e670403858ebebb060da93c3bf0",
    "file": "2017-008051DNXCUAOFASHDENV.pdf",
    "plan_page": 488,
}
MOTION_2025_URL = "https://citypln-m-extnl.sfgov.org/Commissions/CPC/3_13_2025/Commission%20Packet/2024-008290DNX-02.pdf"

LOT_FELL_FT = 164.0  # plan dimension, Fell Street frontage
LOT_VAN_NESS_FT = 275.0  # plan dimension, Van Ness Avenue frontage
TOWER_FROM_VAN_NESS_FT = 12.0
TOWER_FROM_FELL_FT = 40 + 7 / 12 + 15.0
TOWER_LENGTH_FT = 141.0
TOWER_FOOTPRINT_SQFT = 13_200
TOWER_WIDTH_FT = TOWER_FOOTPRINT_SQFT / TOWER_LENGTH_FT
TOWER_ROOF_FT = 520
PODIUM_FT = 130


def lot_utm() -> Polygon:
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    g = shapely.union_all(ob._utm_shapes(fc).to_numpy())
    return g if g.geom_type == "Polygon" else max(g.geoms, key=lambda p: p.area)


def corner_axes(lot: Polygon) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """The Van Ness / Fell corner, a unit vector south along Van Ness and one east along Fell."""
    xy = np.array(lot.exterior.coords)[:-1]
    i = int(np.argmax(xy[:, 1] - xy[:, 0]))  # north-west corner
    corner = xy[i]
    edges = [xy[(i + 1) % len(xy)] - corner, xy[i - 1] - corner]
    east = max(edges, key=lambda v: v[0])  # Fell Street edge
    south = min(edges, key=lambda v: v[1])  # Van Ness Avenue edge
    check = {
        "fell_frontage_ft": round(float(np.linalg.norm(east)) / FT, 1),
        "van_ness_frontage_ft": round(float(np.linalg.norm(south)) / FT, 1),
        "corner_angle_deg": round(float(np.degrees(np.arccos(east @ south / np.linalg.norm(east) / np.linalg.norm(south)))), 2),
    }
    return corner, south / np.linalg.norm(south), east / np.linalg.norm(east), check


def main() -> None:
    # The plan sheet and motion text this module transcribes, pinned (about 105 MB).
    trace.fetch_document(PACKET["url"], config.ROOT / "data" / "raw" / "docs" / PACKET["file"], PACKET["sha256"])
    lot = lot_utm()
    corner, south, east, check = corner_axes(lot)
    print(f"[30-van-ness] lot {lot.area * SQFT:,.0f} sq ft; frontages as mapped: Fell {check['fell_frontage_ft']} ft "
          f"(plan {LOT_FELL_FT:.0f}), Van Ness {check['van_ness_frontage_ft']} ft (plan {LOT_VAN_NESS_FT:.0f}); "
          f"corner {check['corner_angle_deg']} deg")

    def at(s_ft: float, e_ft: float) -> np.ndarray:
        return corner + south * s_ft * FT + east * e_ft * FT

    s0, s1 = TOWER_FROM_FELL_FT, TOWER_FROM_FELL_FT + TOWER_LENGTH_FT
    e0, e1 = TOWER_FROM_VAN_NESS_FT, TOWER_FROM_VAN_NESS_FT + TOWER_WIDTH_FT
    tower = Polygon([at(s0, e0), at(s0, e1), at(s1, e1), at(s1, e0)])
    if not tower.within(lot):
        raise SystemExit("30 Van Ness: the tower falls outside the lot")
    podium = lot.difference(tower)
    print(f"[30-van-ness] tower {tower.area * SQFT:,.0f} sq ft ({TOWER_LENGTH_FT:.0f} x {TOWER_WIDTH_FT:.1f} ft), "
          f"podium {podium.area * SQFT:,.0f} sq ft")

    plan = f"{PACKET['title']}, PDF p. {PACKET['plan_page']} (typical residential floor plan L13-L15)"
    parts = [
        ("Podium", podium, PODIUM_FT, "Office, with shops and lobbies on the ground floor",
         f"illustrative: the lot (DataSF parcel 0835/004) less the tower, at the 130-ft podium height in the "
         f"{PACKET['title']}, draft Downtown Project Authorization, PDF p. 34",
         "A nine-story podium of about 253,000 gross sq ft of office (Motion 21700, 2025). The existing "
         "building's walls are kept as part of it."),
        ("Tower", tower, TOWER_ROOF_FT, "Homes (333)",
         f"illustrative: a 141 x 93.6 ft rectangle set out from the dimensions on the {plan}; roof height "
         f"from the same packet (PDF p. 34) and Motion 21700 (2025)",
         "Roof up to 520 ft, 540 ft with rooftop screening and equipment (Motion 21700). The real floor plate "
         "is faceted, and the top five floors slope down toward Fell Street."),
    ]
    features = []
    for label, geom, h, use, source, note in parts:
        wgs = gpd.GeoSeries([geom.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": label, "stage": "paused", "height_ft": h, "podium_ft": None,
                "base_ft": 0, "use": use, "phase": None, "illustrative": True, "source": source, "note": note,
            },
            "geometry": mapping(wgs),
        })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the approved 130-ft podium over the whole lot and a 520-ft tower set "
                        "out from the dimensions on the 2020 plan set (12 ft from Van Ness Avenue, 55 ft 7 in from "
                        "Fell Street, 141 ft long, 13,200 sq ft). The 2024 and 2025 approvals kept the same "
                        "envelope. The tower's faceted plan and sloped top are not drawn; construction stopped at "
                        "the excavation and foundations."),
            "note": "The approved podium and tower as simple volumes, not the final design.",
            "sourceUrl": PACKET["url"],
            "sourceLabel": "Planning Commission packet, 2020 (PDF)",
            "envelopeSourceUrl": MOTION_2025_URL,
            "georeference": {
                "method": ("Plan dimensions laid out from the Van Ness Avenue / Fell Street corner of the DataSF "
                           "parcel, along its two frontages."),
                "frontages_as_mapped": check,
            },
            "license": "Dimensions: from a public SF Planning document. Lot: DataSF parcels (ODC-PDDL).",
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[30-van-ness] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
