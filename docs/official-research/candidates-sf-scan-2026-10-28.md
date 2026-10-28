# Official-source findings: large San Francisco projects not yet on the map

Checked 2026-10-28. Matthew asked: "any final projects that you think I should add, focus on san francisco
and see any large buildings or projects. I feel like we are still missing a lot". Nothing here is on the map
yet; this is a list to choose from, against the bar in `docs/UPKEEP.md` (a master-planned, multi-building
project of roughly 1,000+ homes or 1M+ sq ft, plus single large buildings Matthew has chosen before, such as
`oceanwide-center`, `30-van-ness` and `655-4th-street`).

How it was found: every record in the Planning Department's Development Pipeline (DataSF, Q2 2026 snapshot
published Aug 28, 2026; CC0) with 300+ net homes, 300,000+ sq ft of non-residential space or a development
agreement (113 rows), each point checked against the map's site outlines; then SF Planning's listing of EIRs
and negative declarations (the 50 latest, back to Nov 2023); then each candidate's current status in the
Planning Department's project records (DataSF), which are newer than the pipeline. Projects already mapped,
`_meta.dropped` (Piers 30–32 and Seawall Lot 330, the waterfront flood defenses) and the Oct 17 lead scan
(`docs/upkeep/leads-2026-10-17.md`) were set aside or noted. No press was read.

URL shorthand:
- `PIPE` = `https://data.sfgov.org/resource/6jgi-cpb4.json?case_no=<id>` (Development Pipeline, Q2 2026)
- `PRJ:<id>` = `https://data.sfgov.org/resource/qvu5-m3a2.json?record_id=<id>` (Planning records – Projects)
- `NPR:<id>` = `https://data.sfgov.org/resource/y673-d69b.json?record_id=<id>` (Planning records – Non-Projects)
- `EIRS` = `https://sfplanning.org/environmental-review-documents?field_environmental_review_categ_target_id=212&items_per_page=50`

## Over the bar: master-planned, multi-building

| project | where | program | status (latest record) | sources |
|---|---|---|---|---|
| **Freedom West 2.0** (710 McAllister St) | Western Addition, 10.37 acres | 22 low-rise buildings replaced by 15 new ones, 85 to 335 ft; the 267 co-op homes replaced plus 2,024 more; a 150-room hotel; retail, childcare, community and STEM space; about 3.7M gross sq ft in three phases over about seven years; rezoned to a new special use district | In entitlement: Draft EIR (listing dated Jan 13, 2026); general plan, zoning map, Planning Code and development agreement applications filed May 5, 2026. Sponsor MacFarlane Partners | `PRJ:2020-006887PRJ`, `NPR:2020-006887ENV`, `NPR:2020-006887DVA`, `PIPE` (2023-007911PRX: 2,155 net homes, 597 affordable), `EIRS` |
| **Matson Block** (77 Beale St / 50 Main St) | Financial District, the block of Market, Main, Mission and Beale | A tower of up to 1,225 ft plus a 75-ft crown replacing the 474-ft 77 Beale building, mainly offices (or institutional, hotel or homes) with a possible observation deck; 25 Beale converted to 44–120 homes; 215 and 245 Market renovated (up to 340,000 sq ft); up to 250,000 sq ft of retail. The pipeline counts 1,919,847 sq ft of office, 2,419,847 sq ft non-residential and 437 homes | In entitlement: notice of preparation of an EIR (listing dated Dec 17, 2025; scoping meeting Jan 7, 2026). Project record "Under Review", environmental record "On Hold" | `PRJ:2021-012562PRJ`, `NPR:2021-012562ENV`, `PIPE`, `EIRS`. In the Oct 17 lead scan as borderline (one block) |
| **3333 California Street** (Laurel Heights) | Presidio Heights | The 455,000-sq-ft office building split and reused as two residential buildings, plus 13 new buildings (townhouses to 6-story apartments and mixed-use buildings): 744 homes, about 35,000 sq ft of retail, a 15,000-sq-ft childcare center; about 1,428,000 gsf | Approved, with a development agreement (pipeline "PL Approved", tracking record 2023-007909PRX); EIR cleared Sept 2019; sponsor Prado Group, Inc. Whether construction has started isn't in the records read | `PRJ:2015-014028PRJ`, `NPR:2015-014028ENV`, `PIPE` |
| **5M** (Fifth and Mission) | SoMa, about 4 acres, 23 parcels | Mixed residential, office and retail under the Fifth and Mission Special Use District; still to build per the pipeline: 386 homes and 676,000 sq ft of office | Partly built: development agreement with 5M Project, LLC closed as approved Dec 2, 2015 (applicant Forest City), the buildings' conditional use and office approvals closed as approved Jan 2016; the pipeline still lists the remainder as approved | `NPR:2011.0409DVA`, `NPR:2011.0409MAP`, `NPR:2011.0409B`, `PIPE` (2018-011363PRX). The full program (homes and office in all) needs the 2015 approval documents |
| **San Francisco Gateway** (749 Toland St and 2000 McKinnon Ave) | Bayview | Four industrial buildings (two of 4 stories, two of 2) around a truck court, 1,091,790 sq ft of PDR | Entitled: approved Sept 25, 2025, environmental clearance closed Oct 2, 2025 (the listing shows a notice of preparation, Draft EIR and responses to comments; the project record names a negative declaration, May 7, 2025); project record "On Hold" | `PRJ:2015-012491PRJ`, `NPR:2015-012491ENV`, `PIPE`, `EIRS` |
| **400 2nd Street** | SoMa, at Harrison | Three new buildings: 489 homes, about 493,000 sq ft of office, 237,750 sq ft of visitor (hotel) space, PDR and retail; about 824,000 sq ft non-residential | Entitled: approved Feb 20, 2020; building permit approved Nov 13, 2023 (pipeline) | `PRJ:2012.1384`, `PIPE` |

## Single large buildings (like Oceanwide Center and 30 Van Ness)

| project | program | status | sources |
|---|---|---|---|
| 10 South Van Ness Ave (next to `30-van-ness`) | 65 stories, 1,104 homes in the description (966 net in the pipeline), 18,568 sq ft retail | Approval letter, record closed Aug 18, 2026 (first approved June 11, 2020) | `PRJ:2024-008986PRJ`, `PIPE` |
| 542–550 Howard St (Transbay Parcel F) | About 800 ft, 61 stories: 189-room hotel, about 276,000 sq ft office, 165 homes | Approved Jan 9, 2020 | `PRJ:2016-013312PRJ`, `PIPE` |
| 524 & 530 Howard St | 72 stories, about 795 ft, 672 homes | Approval letter, Sept 17, 2024 | `PRJ:2023-010883PRJ`, `PIPE` |
| Transbay Block 4 (200 Main St) | 47 stories, 501 ft, 683 homes (OCII) | Application accepted | `PRJ:2018-015785PRJ`, `PIPE` |
| Kaiser Permanente replacement hospital (2190 O'Farrell St) | A 14-story, 266-ft hospital (694,012 sq ft) and a 12-level garage (534,274 sq ft, 1,003 spaces) | Filed May–June 2026; project record "On Hold" | `PRJ:2026-004681PRJ`, `NPR:2026-004681ENV`, `PIPE` |
| Potrero Yard Modernization (2500 Mariposa St, SFMTA) | A 150-ft building: three-story bus garage and 513 homes above, 1,243,000 sq ft | Approved (approval letter; environmental clearance Jan 11, 2024). The Oct 17 scan excluded it on a press figure of about 100 homes; the official record says 513 | `PRJ:2019-021884PRJ`, `NPR:2019-021884ENV`, `PIPE` |
| Park Block (598 Brannan St; Central SoMa key site 5) | Four buildings: about 922,737 sq ft office, PDR, childcare, up to 72 affordable homes | Site permit filed Dec 13, 2019; Planning record "On Hold" | `PRJ:2012.0640`, `PIPE` |
| 725 Harrison St (Central SoMa) | 14 stories, 185 ft, about 981,000 gsf (810,000 office) | Approved Dec 12, 2019, modified June 16, 2022; permit filed | `PRJ:2005.0759`, `PRJ:2023-002967PRJ`, `PIPE` |

Below 750 homes and under 1M sq ft, not listed in detail: 11 & 15 Marina Blvd (790 homes on the Marina
Safeway site, filed Dec 2025), 850 La Playa (562 homes on the Ocean Beach Safeway site, filed May 2026, on
hold), 620 Folsom St (640 ft, 826 homes, on hold), One Oak (541 homes, approved again Mar 19, 2026), 469
Stevenson St (495 homes, approved).

## Considered and not recommended

- **HOPE SF Hunters View**: about 668 affordable homes in 66 buildings (2008 approval), mostly built; the
  pipeline lists 175 homes left. Under the bar, though `potrero-hope-sf` and `sunnydale-hope-sf` are mapped.
- **VA Fort Miley campus** (1,139,700 sq ft medical): a tracking record filed Oct 2025 describes the VA's
  "Alternative 1 Construction 2013–2020"; what is current isn't clear from the records. Needs the VA's own
  documents.
- **Amazon, 900 7th St** (650,000 sq ft parcel delivery, NOP Jan 28, 2026): already in
  `candidates-around-railyards.md`; one large logistics building.
- **SFO Recommended Airport Development Plan** (EIR, Feb 2026): an airport, a category the map hasn't
  included (see the Oakland airport lead, Oct 17).
- **Infrastructure without buildings or transit**: the Biosolids Digester Facilities, Ocean Beach Climate
  Change Adaptation (like the removed waterfront flood defenses), Pier 92 and the Islais Creek works.
- **The Housing Element's Family Zoning Plan** (EIR Dec 2025): a citywide rezoning, not a site.
- **555 Beale St (Seawall Lot 330)**: in `_meta.dropped` at Matthew's request.
