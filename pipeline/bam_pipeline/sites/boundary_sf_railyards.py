"""SF Railyards (Railyards Mixed-Use Development Project, 700 4th Street): the four railyard parcels.

The San Francisco Planning Department's Notice of Preparation of an EIR (Case No. 2026-002123ENV,
Sept 30, 2026; CEQAnet SCH 2026091295) gives the project site as "Blocks/Lots 8701/003, 8701/004,
8700/001, and 8703/005", "18.63 acres", "generally bounded by Townsend Street to the north, Fourth
Street to the east, King Street to the south, and Seventh Street to the west". The boundary is the union
of those four lots in DataSF's parcel layer (acdm-wktn), which comes to 18.6 acres, as in the notice's
Figure 1. The offsite train storage and maintenance facility the project also includes has no site yet
(NOP p. 2) and isn't drawn.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_sf_railyards
"""

from __future__ import annotations

from . import official_boundaries as ob

PROJECT = "sf-railyards"
BLKLOTS = ["8701003", "8701004", "8700001", "8703005"]  # NOP p. 1, "Blocks/Lot Nos."
NOP_URL = "https://ceqanet.lci.ca.gov/2026091295/Attachment/tPsmWg"

SPEC = {
    "label": "DataSF parcels",
    **ob.socrata(ob.DATASF, ob.SF_PARCELS, f"blklot in ({ob._sql_list(BLKLOTS)})"),
    "layer": "DataSF Parcels – Active and Retired, blocks/lots 8701/003, 8701/004, 8700/001 and 8703/005",
    "accuracy": "official",
    "note": ("The four lots the Planning Department's Notice of Preparation names as the project site (Case No. "
             "2026-002123ENV, Sept 30, 2026, p. 1: 18.63 acres, bounded by Townsend, Fourth, King and Seventh "
             "streets): the Caltrain station and railyard at Fourth and King. The project's offsite train storage "
             "and maintenance facility has no site yet and isn't drawn."),
    "license": "ODC Public Domain Dedication and License (DataSF)",
}


def main() -> None:
    ob.SPECS[PROJECT] = SPEC
    ob.build(PROJECT)


if __name__ == "__main__":
    main()
