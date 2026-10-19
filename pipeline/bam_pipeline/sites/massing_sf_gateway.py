"""San Francisco Gateway: the two approved PDR buildings, drawn over their lots at 97 ft.

Sources:
- San Francisco Gateway Project Draft EIR (Case No. 2015-012491ENV, SCH 2022030286, August 2, 2023), Section 2.D.1
  (p. 2-10, PDF p. 90): "construct two new three-story buildings (plus active roof) ... Each building would have a
  maximum height of approximately 97 feet (115 feet with rooftop appurtenances included)"; "the proposed building
  west of I-280 at 749 Toland Street is 'building A,' and the proposed building east of I-280 at 2000 McKinnon
  Street is 'building B'"; "buildings A and B would be approximately the same size, shape, and dimensions".
- Table 2.D-1 (p. 2-11, PDF p. 91): per building, PDR 583,400 gsf, logistics yard 72,900, vehicle circulation
  147,750, parking 271,750 (27,950 on the ground level and 243,800 on the roof), retail 4,200; total 1,080,000.
- Figure 2.D-1, Site Plan (p. 2-12, PDF p. 92), and Figure 2.D-3, Level 1 floor plan (p. 2-14, PDF p. 94): each
  building fills most of its lot, with a 576-ft dimension across the PDR floor.
- The Responses to Comments (May 2025, Section 10.B) and the Planning Commission agenda of Sept 25, 2025 (items
  15a-e) keep the design: two buildings "up to 97 feet in height totaling 1,646,000 gross square feet", or 2,160,000
  gsf with the active roofs.

How it's drawn:
- Each building is drawn as its whole lot (DataSF parcels 5284A/008 for Building A and 5287/002 for Building B) at
  97 ft. The figures show the buildings nearly filling their lots, with sidewalks and planting at the edges and
  rounded ramp corners on the McKinnon Avenue side; those aren't traced, so the volumes are illustrative envelopes.
  The solar array, stair and elevator structures on the active roof (up to 115 ft) aren't drawn.

Stage: approved (Planning Commission, Sept 25, 2025; special use district and development agreement in effect
Dec 12, 2025); no building permit for the new buildings in DBI's records as of Oct 19, 2026. Both drawn as entitled.

    uv run --directory pipeline python -m bam_pipeline.sites.massing_sf_gateway
"""

from __future__ import annotations

import json

import geopandas as gpd
import shapely
from shapely.geometry import mapping

from .. import config, trace
from . import official_boundaries as ob

PROJECT_ID = "sf-gateway"
UTM = ob.UTM
SQFT = 10.7639

DEIR = {
    "title": "San Francisco Gateway Project Draft EIR (Case No. 2015-012491ENV, August 2, 2023)",
    "url": "https://ceqanet.lci.ca.gov/2022030286/2/Attachment/fYSuZM",
    "sha256": "1a606783febf200787d6d015da7ebc2fe99f99a1cd7a8968fd17bc30e834dd4c",
    "file": "sf-gateway-deir-2023-08-02.pdf",
}
LOTS = {"5284A008": "Building A (749 Toland Street)", "5287002": "Building B (2000 McKinnon Avenue)"}
LOT_SPEC = ob.socrata(ob.DATASF, ob.SF_PARCELS, f"blklot in ({ob._sql_list(LOTS)})")
HEIGHT_FT = 97


def main() -> None:
    trace.fetch_document(DEIR["url"], config.ROOT / "data" / "raw" / "docs" / DEIR["file"], DEIR["sha256"])
    fc_lots = ob.fetch(f"{PROJECT_ID}-lots", LOT_SPEC)
    site = shapely.union_all(ob._utm_shapes(ob.fetch(PROJECT_ID, ob.SPECS[PROJECT_ID])).to_numpy())
    features = []
    for f, geom in zip(fc_lots["features"], ob._utm_shapes(fc_lots)):
        blklot = f["properties"]["blklot"]
        lot = trace.largest_polygon(geom)
        if not lot.buffer(-1).within(site):
            raise SystemExit(f"sf-gateway: lot {blklot} falls outside the special use district")
        print(f"[sf-gateway] {LOTS[blklot]}: lot {blklot}, {lot.area * SQFT:,.0f} sq ft at {HEIGHT_FT} ft")
        wgs = gpd.GeoSeries([lot.simplify(0.2)], crs=UTM).to_crs(4326).iloc[0]
        features.append({
            "type": "Feature",
            "properties": {
                "kind": "building", "label": LOTS[blklot].split(" (")[0], "stage": "entitled", "height_ft": HEIGHT_FT,
                "podium_ft": None, "base_ft": 0,
                "use": "Production, distribution and repair (PDR) space on three levels, with ground-floor retail and "
                       "maker space, a logistics yard and an active roof for parking and vehicle staging",
                "phase": None, "illustrative": True,
                "source": (f"illustrative: the DataSF lot ({blklot[:-3]}/{blklot[-3:]}) at the 97-ft height in the "
                           f"{DEIR['title']}, Section 2.D.1 and Table 2.D-1 (PDF pp. 90-91)"),
                "note": (f"{LOTS[blklot]}: about 1,080,000 gsf including its active roof (Table 2.D-1). Drawn over the "
                         "whole lot; the building nearly fills it (Figures 2.D-1 and 2.D-3). Rooftop solar, stair and "
                         "elevator structures reach 115 ft."),
            },
            "geometry": mapping(wgs),
        })

    fc = {
        "type": "FeatureCollection",
        "properties": {
            "project": PROJECT_ID,
            "illustrative": True,
            "summary": ("Illustrative massing: the two approved three-story PDR buildings, each drawn over its whole lot "
                        "at 97 ft (115 ft with rooftop structures). The buildings nearly fill their lots; their edges "
                        "and rounded ramp corners aren't traced. Interstate 280 passes overhead between them."),
            "note": "The approved buildings as simple volumes on their lots, not the final design.",
            "sourceUrl": DEIR["url"],
            "sourceLabel": "San Francisco Gateway Draft EIR, 2023 (PDF)",
            "georeference": {"method": "DataSF parcels 5284A/008 and 5287/002 (no figure tracing)."},
            "license": "Heights: from a public SF Planning document. Lots: DataSF parcels (ODC-PDDL).",
        },
        "features": features,
    }
    out = config.ROOT / "data" / "massing" / f"{PROJECT_ID}.geojson"
    out.write_text(json.dumps(ob._round(fc), indent=1) + "\n")
    print(f"[sf-gateway] wrote {out.relative_to(config.ROOT)} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
