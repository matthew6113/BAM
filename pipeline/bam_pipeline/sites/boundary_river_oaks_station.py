"""River Oaks Station transit-oriented development (VTA): the headquarters parcel at 3331 North First Street.

VTA describes the site as its River Oaks administrative headquarters and park-and-ride lot, "located at
3331 North First Street in San Jose" (fact sheet, Jan 2025; "17-acre"), "an 18-acre property located at
the corner of North First Street and River Oaks Parkway" (project page), and its "17-acre headquarters
site and park-and-ride lot" (River Oaks Station Access Study, Mar 25, 2026, p. 1). None of the VTA
documents read gives an assessor's parcel number or a surveyed site map, so the boundary is the one
parcel in the Santa Clara County parcel layer (data.sccgov.org ubcd-cewv) whose situs address is 3331 N
1st Street, APN 097-06-032 (17.5 acres), between North First Street and the Guadalupe River south of
River Oaks Parkway. It is marked approximate until a VTA or City document names the parcel.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_river_oaks_station
"""

from __future__ import annotations

from . import official_boundaries as ob

PROJECT = "river-oaks-station"
APNS = ["09706032"]  # situs 3331 N 1ST ST in the County layer

SPEC = {
    "label": "Santa Clara County parcels",
    **ob.socrata(*ob.SCC_PARCELS, f"apn in ({ob._sql_list(APNS)})"),
    "layer": ("Santa Clara County parcels (data.sccgov.org ubcd-cewv): APN 097-06-032, the parcel with the situs "
              "address 3331 N 1st Street, the address VTA gives for its River Oaks campus"),
    "accuracy": "approximate",
    "note": ("Approximate boundary: the County parcel at 3331 North First Street, the address VTA's fact sheet "
             "gives for its River Oaks headquarters and park-and-ride site. VTA's documents don't name the "
             "parcel or publish a surveyed site map; the parcel lies between North First Street and the "
             "Guadalupe River south of River Oaks Parkway, as the developer concept in the River Oaks Station "
             "Access Study (Figure 9) shows the site. VTA gives the site as 17 acres (access study and fact "
             "sheet) and as 18 acres (project page). Against those:"),
    "license": "Santa Clara County open data (terms of use)",
}


def main() -> None:
    ob.SPECS[PROJECT] = SPEC
    ob.build(PROJECT)


if __name__ == "__main__":
    main()
