"""536 Mission Street: a simple volume over the lot at the approved office variant's roof height.

Sources:
- Planning Commission agenda, Sept 10, 2026 (sfplanning.org), items 5a-5c, PDF p. 4: approvals for "a project to
  demolish the existing buildings on the Project Site and construct one of the following tower variants: 1) a
  700-foot-tall, approximately 1.22 million square foot building with retail, office, and laboratory uses; or 2) a
  649-foot-tall, approximately 991,000 square foot building with retail, office, and residential uses (up to 385
  dwelling units)", in the 700-S-2 height and bulk district.
- Planning records (DataSF y673-d69b, 2025-007507DNX): "46-stories development with two variants. The first is a
  700-foot-tall (752 feet to the top of the parapet) ... office building ... The second variant is a 650-foot-tall
  (698 feet to top of the parapet) ... building"; the Downtown Project Authorization was approved (closed Sept 24,
  2026, after the Sept 10 hearing).

How it's drawn:
- No floor plan or site plan for the tower was in a document that could be opened (the Planning Commission packet
  and the CEQA general plan evaluation are on a host this pipeline can't reach). The volume is the whole lot (DataSF
  parcel 3708/098, the boundary file) extruded to 700 ft, the office variant's roof. The real tower is set back in
  places and its parapet reaches 752 ft; the mixed-use variant would be 649 ft (698 ft to the parapet). The gross
  floor areas suggest the tower's floors average roughly four-fifths of the lot. Illustrative.

Stage: approved by the Planning Commission on Sept 10, 2026; no building permit yet. Drawn as "entitled".

    uv run --directory pipeline python -m bam_pipeline.sites.massing_536_mission
"""

from __future__ import annotations

import json

import geopandas as gpd
import shapely
from shapely.geometry import mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "536-mission"
UTM = ob.UTM
SQFT = 10.7639

AGENDA = {
    "title": "San Francisco Planning Commission agenda, Sept 10, 2026",
    "url": "https://sfplanning.org/sites/default/files/agendas/2026-09/20260910_cpc%20%28ID%201586266%29.pdf",
    "sha256": "ac9a9af5cd5294e94460886e014c204a2e49919039ec5e6875fc873837f56717",
    "file": "20260910_cpc_ID_1586266.pdf",
}
RECORD_URL = "https://data.sf.gov/resource/y673-d69b.json?record_id=2025-007507DNX"
ROOF_FT = 700.0


def main() -> None:
    trace.fetch_document(AGENDA["url"], config.ROOT / "data" / "raw" / "docs" / AGENDA["file"], AGENDA["sha256"])
    fc = ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])
    lot = shapely.union_all(ob._utm_shapes(fc).buffer(0.5).to_numpy()).buffer(-0.5)
    print(f"[536-mission] lot {lot.area * SQFT:,.0f} sq ft")
    wgs = gpd.GeoSeries([lot.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
    feature = {
        "type": "Feature",
        "properties": {
            "kind": "building", "label": "Tower (office variant)", "stage": "entitled", "height_ft": ROOF_FT,
            "podium_ft": None, "base_ft": 0, "use": "Office and laboratory, with ground-floor retail",
            "phase": None, "illustrative": True,
            "source": (f"illustrative: the whole lot (DataSF parcel 3708/098) at the office variant's 700-ft roof in "
                       f"the {AGENDA['title']}, PDF p. 4, and Planning record 2025-007507DNX"),
            "note": ("46 stories, 700 ft to the roof and 752 ft to the top of the parapet. The approval also allows a "
                     "mixed-use variant, 649 ft (698 ft to the parapet) with up to 385 homes. Drawn over the whole lot: "
                     "the tower's footprint wasn't in a document we could open."),
        },
        "geometry": mapping(wgs),
    }
    out_fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: a simple volume over the whole Golden Gate University lot at 700 ft, the "
                        "roof of the approved office variant (752 ft to its parapet). The tower's real footprint is "
                        "smaller in places; the approved mixed-use variant would be 649 ft."),
            "note": "A placeholder volume at the approved height, not the design.",
            "sourceUrl": AGENDA["url"],
            "sourceLabel": "Planning Commission agenda, Sept 10, 2026 (PDF)",
            "envelopeSourceUrl": RECORD_URL,
            "georeference": {"method": "The DataSF parcel, as in the boundary file."},
            "license": "Height: from public SF Planning documents. Lot: DataSF parcels (ODC-PDDL).",
        },
        "features": [feature],
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(out_fc), indent=1) + "\n")
    print(f"[536-mission] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
