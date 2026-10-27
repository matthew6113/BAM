"""Three Central SoMa Plan key development sites beside the Caltrain railyard: their lots.

The Central SoMa Plan (2018, Implementation Strategy D, "Key Development Site Guidelines") maps each key
site by block and lot. Each boundary here is the union of those lots in DataSF's parcel layer
(acdm-wktn), checked against the site area in the project's own Planning Department record:

- 655 4th Street (Plan Site 8, "4th and Townsend"): lots 3787/026, /028, /050, /161 and the condominium
  lots 3787/162-164, which share one footprint. 1.65 acres; the 2022 application (2022-011490PRJ)
  gives "a 71,290 square foot development lot" (1.64 acres).
- 88 Bluxome Street (Site 7, "88 Bluxome/Tennis Club"): lot 3786/037. 2.66 acres; the 2025
  application (2025-004642PRJ) gives "an approximately 2.6-acre development lot".
- Flower Mart (Site 4): "Block 3778; Lots 1B, 2B, 4, 5, 47, and 48" (2017-000663PRJ). 6.83 acres;
  the 2016 preliminary assessment (2015-004256PPA-04) gives "295,144 square feet" (6.78 acres).

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_central_soma_key_sites
"""

from __future__ import annotations

from . import official_boundaries as ob

PLAN = "Central SoMa Plan (2018), Key Development Site Guidelines"
LICENSE = "ODC Public Domain Dedication and License (DataSF)"


def _spec(blklots: list[str], lots_text: str, note: str) -> dict:
    return {
        "label": "DataSF parcels",
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, f"blklot in ({ob._sql_list(blklots)})"),
        "layer": f"DataSF Parcels – Active and Retired, {lots_text}",
        "accuracy": "official",
        "note": note,
        "license": LICENSE,
    }


SPECS = {
    "655-4th-street": _spec(
        ["3787026", "3787028", "3787050", "3787161", "3787162", "3787163", "3787164"],
        "block 3787, lots 026, 028, 050 and 161-164",
        f"The lots the {PLAN} maps as Site 8, \"4th and Townsend\": the corner lots on Fourth and Townsend "
        "streets and, in the northeast corner, the condominium lots 162-164. The Planning Department's record "
        "for the project (2022-011490PRJ) gives \"a 71,290 square foot development lot\" (1.64 acres).",
    ),
    "88-bluxome": _spec(
        ["3786037"],
        "block 3786, lot 037",
        f"The lot the {PLAN} maps as Site 7, \"88 Bluxome/Tennis Club\", fronting Brannan, Fifth and Bluxome "
        "streets. The Planning Department's record (2025-004642PRJ) gives \"an approximately 2.6-acre "
        "development lot\", to be split into three parcels, the easternmost (22,690 sq ft) dedicated to the City "
        "for affordable housing.",
    ),
    "flower-mart": _spec(
        ["3778001B", "3778002B", "3778004", "3778005", "3778047", "3778048"],
        "block 3778, lots 1B, 2B, 4, 5, 47 and 48",
        f"The lots the Planning Department's record for the approved project names, \"Block 3778; Lots 1B, 2B, "
        f"4, 5, 47, and 48\" (2017-000663PRJ), and the {PLAN} maps as Site 4, \"Flower Mart\", on Brannan "
        "Street between Fifth and Sixth streets. A 2016 Planning record (2015-004256PPA-04) gives the site as "
        "295,144 sq ft (6.78 acres). The revised project filed in 2025 (2025-008569PRJ) doesn't list its lots.",
    ),
}


def main() -> None:
    for project, spec in SPECS.items():
        ob.SPECS[project] = spec
        ob.build(project)


if __name__ == "__main__":
    main()
