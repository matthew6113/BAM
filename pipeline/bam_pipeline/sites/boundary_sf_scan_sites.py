"""Sixteen large San Francisco projects (the Oct 28, 2026 citywide scan and Van Ness and Market): their sites.

Each site is the lots the project's Planning Department records name (for 3333 California, the special
use district created for it), from DataSF, checked against the site area the records give. Where no
official lot list was reachable the boundary is marked approximate. The research and sources are in
docs/official-research/candidates-sf-scan-2026-10-28.md.

    uv run --directory pipeline python -m bam_pipeline.sites.boundary_sf_scan_sites
"""

from __future__ import annotations

from . import official_boundaries as ob

SPECS = {
    'freedom-west': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('0770027', '0783023', '0783024', '0783025')"),
        "layer": 'DataSF Parcels – Active and Retired, lots 0770/027 and 0783/023, 024 and 025',
        "accuracy": 'approximate',
        "note": "The Freedom West lots on the two blocks the Planning Department's project page describes (bounded by Gough Street, Golden Gate Avenue, Laguna Street and Fulton Street, bisected by McAllister Street; a 10.37-acre site). No official lot list was reachable; the lots are those carrying the project's addresses in the Planning records (710 and 867 McAllister Street; 0770/027) and the rest of the block south of McAllister. Lot 0770/027 also holds the adjacent 880 McAllister Street senior housing site, a separate project, which is drawn inside.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    'matson-block': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3711005', '3711006', '3711007', '3711008', '3711009', '3711010', '3711011', '3711012', '3711013', '3711014', '3711019')"),
        "layer": 'DataSF Parcels – Active and Retired, block 3711, lots 005-014 and 019',
        "accuracy": 'official',
        "note": 'The lots CEQAnet lists for the Matson Block Project\'s notice of preparation (SCH 2025120794, Dec 17, 2025): "3711/005-014 and 019", 3.47 acres, the block bounded by Market, Main, Mission and Beale streets.',
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    '3333-california': {
        "label": 'DataSF special use districts',
        **ob.socrata(ob.DATASF, ob.SF_SUD, "name = '3333 California Street SUD'"),
        "layer": 'DataSF Zoning Map – Special Use Districts, 3333 California Street Special Use District',
        "accuracy": 'official',
        "note": 'The 3333 California Street Special Use District (Planning Code Section 249.86), created for the project; it is the single lot 1032/003. The development agreement ordinance (2015-014028DVA) describes an approximately 10.25-acre site at California Street and Presidio Avenue.',
        "license": 'Public Domain U.S. Government (DataSF)',
    },
    '5m': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3725042', '3725076', '3725093', '3725094', '3725099', '3725100', '3725124', '3725125', '3725126', '3725127', '3725128', '3725129', '3725130', '3725131', '3725133', '3725134')"),
        "layer": 'DataSF Parcels – Active and Retired, block 3725, the 16 active lots inside the Fifth and Mission Special Use District',
        "accuracy": 'official',
        "close_m": 4,
        "note": "The active lots inside DataSF's Fifth and Mission Special Use District (5yf5-ms5f), the zoning district created for the 5M project, joined across the alleys between them (Minna, Natoma and Mary streets). The Planning Department describes an approximately 4-acre site of 23 parcels at Fifth Street between Mission and Howard streets (2011.0409B); several have since been merged and renumbered. The district itself extends into the surrounding streets and isn't used as the outline.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    'san-francisco-gateway': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('5284A008', '5287002')"),
        "layer": 'DataSF Parcels – Active and Retired, Block 5284A Lot 008 and Block 5287 Lot 002',
        "accuracy": 'official',
        "note": "The two lots the Planning Commission's agendas (Sept 7, 2023; Sept 25, 2025) give as the San Francisco Gateway site, bounded by Kirkwood Avenue, Rankin Street, McKinnon Avenue and Toland Street (749 Toland Street and 2000 McKinnon Avenue). The agendas' approximately 17.1-acre site also includes portions of the surrounding streets and Selby Street, which aren't drawn.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    '400-2nd-street': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3763001', '3763078', '3763079', '3763080', '3763080A', '3763081', '3763099', '3763100', '3763101', '3763105', '3763113')"),
        "layer": 'DataSF Parcels – Active and Retired, Block 3763, lots 001, 078, 079, 080, 080A, 081, 099, 100, 101, 105 and 113',
        "accuracy": 'official',
        "note": 'The still-active lots of those the Planning Commission\'s Feb 20, 2020 agenda lists for One Vassar (Block 3763, lots 001, 078, 079, 080, 080A, 081, 099, 100, 101, 105, 112 and 113), which the Central SoMa Plan maps as key site 3, "2nd and Harrison". Lot 112 was split in 2017 into lot 125 (416 2nd Street) and lot 126 (452 2nd Street, a Transbay bus storage facility); neither is drawn. The approvals don\'t state a site area.',
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    'transbay-parcel-f': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3721016', '3721136')"),
        "layer": 'DataSF Parcels – Active and Retired, block 3721, lots 016 and 136',
        "accuracy": 'official',
        "note": "The lots of the Planning Department's records for 542-550 Howard Street (2016-013312): lot 016 (546 Howard Street), named in the conditional use record and the site permit, and lot 136, which replaced the records' lot 015A in DataSF's parcel map on May 22, 2017. No site area is given in the records read.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    '524-howard': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3721013', '3721014')"),
        "layer": 'DataSF Parcels – Active and Retired, block 3721, lots 013 and 014',
        "accuracy": 'official',
        "note": "The two lots the project's site permit (202311170986) lists, 524 and 530 Howard Street, the addresses the Planning Department's record (2023-010883PRJ) names. No site area is given in the records read.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    'transbay-block-4': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3739010')"),
        "layer": 'DataSF Parcels – Active and Retired, block 3739, lot 010',
        "accuracy": 'official',
        "note": "The lot the Planning Department's record (2018-015785PRJ) and the city's pipeline name, created in DataSF's parcel map in 2021 from lot 008, on which the 2019 site permits were filed. No site area is given in the records read.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    '10-south-van-ness': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3506003A', '3506004')"),
        "layer": 'DataSF Parcels – Active and Retired, block 3506, lots 003A and 004',
        "accuracy": 'official',
        "note": 'The two lots the project merges: "The Project will include the merger of Lots 003A and 004 on Block 3506" (2015-004568ENV), also listed on building permit 202206176565. The 2024 application names lot 004. No site area is given in the records read.',
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    'one-oak': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('0836001', '0836002', '0836003', '0836004', '0836005')"),
        "layer": 'DataSF Parcels – Active and Retired, block 0836, lots 001-005',
        "accuracy": 'official',
        "note": 'The project record\'s lot (0836/001, 1500 Market Street, 2024-005509PRJ) and the four the Planning Department\'s project review names, "1510-1540 Market Street & 11 Oak Street (0836/002, 003, 004, & 005)" (10833PRV). No site area is given in the records read.',
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    '98-franklin': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('0836008', '0836009', '0836013')"),
        "layer": 'DataSF Parcels – Active and Retired, block 0836, lots 008, 009 and 013',
        "accuracy": 'official',
        "note": 'The lots the project record names: "Block 0836, Lots 008, 009, & 013" (2016-014802PRJ). No site area is given in the records read.',
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    'potrero-yard': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3971001')"),
        "layer": 'DataSF Parcels – Active and Retired, Block 3971, Lot 001',
        "accuracy": 'official',
        "note": "Assessor's Block 3971 Lot 001, the whole block bounded by 17th, Hampshire, Mariposa and Bryant streets, which the Planning Commission's Jan 11, 2024 agenda gives as the Potrero Yard site. The approvals don't state its area.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    '598-brannan': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3777045', '3777050', '3777051', '3777176', '3777177')"),
        "layer": 'DataSF Parcels – Active and Retired, block 3777, lots 045, 050, 051, 176 and 177',
        "accuracy": 'official',
        "note": 'The lots the Planning Commission\'s June 6, 2019 agenda lists for 598 Brannan Street (Block 3777, lots 045, 050, 051 and 052), which the Central SoMa Plan maps as key site 5, "Park Block". Lot 052 was split in January 2025 into lot 176 (160 Freelon Street, the parcel dedicated for affordable housing) and lot 177; both are drawn. The approvals don\'t state a site area.',
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    '725-harrison': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('3762152', '3762149')"),
        "layer": 'DataSF Parcels – Active and Retired, Block 3762, lots 152 and 149',
        "accuracy": 'official',
        "note": 'The lots the Planning Commission\'s June 16, 2022 agenda lists for 725-765 Harrison Street (Block 3762, lots 148, 149 and 113); lots 148 and 113 were merged into lot 152 in December 2022. The Planning Department\'s environmental record gives "seven (was six) lots totaling 104,188 square feet". Lot 149 is the lot to be dedicated for affordable housing.',
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
    'kaiser-2190-ofarrell': {
        "label": 'DataSF parcels',
        **ob.socrata(ob.DATASF, ob.SF_PARCELS, "blklot in ('1098009', '1098050')"),
        "layer": 'DataSF Parcels – Active and Retired, block 1098, lots 009 and 050',
        "accuracy": 'approximate',
        "note": "The two lots the Planning Department's record (2026-004681PRJ, lot 009) and the city's pipeline (lot 050) name for the Replacement Hospital Project; the records don't list the site's lots or area. Lot 050 holds Kaiser Foundation Hospital's garages at 2130 and 2190 O'Farrell Street (2015-003372MIS). Lot 038 (2201 Geary Boulevard) on the same block isn't named and isn't drawn.",
        "license": 'ODC Public Domain Dedication and License (DataSF)',
    },
}


def main() -> None:
    for project, spec in SPECS.items():
        ob.SPECS[project] = spec
        ob.build(project)


if __name__ == "__main__":
    main()
