# Official-source findings: Brisbane Baylands, Willow Village, Parkline, North Bayshore

Checked 2026-10-02 against documents downloaded from city sites and agenda systems and read in
full text (local copies go in `data/raw/official/<project>/`, git-ignored). Page numbers are PDF
pages.

Headline: all four records conflict with official documents. Willow Village's program numbers
are wrong; North Bayshore's office, retail and hotel figures are wrong or missing; Brisbane
Baylands is now before City Council, its 2027 start isn't official, and its open space is
148–157 acres, not 100.

## brisbane-baylands

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 684 | 680.1 (558.3 land + 121.8 lagoon) | CONFLICT | brisbaneca.gov/774/2026-Final-EIR; Specific Plan ch.2 brisbaneca.gov/DocumentCenter/View/2988 p11 | "approximately 680.1 acres (558.3 acres of existing land area and 121.8 acres of lagoon) within the City of Brisbane" |
| acresNote: part in SF | yes | whole area within Brisbane | CONFLICT | same | "within the City of Brisbane in northeast San Mateo County" |
| homes | 2,200 | 2,200 proposed; General Plan allows 1,800–2,200 | CONFIRMED | /View/2986 p3; /View/2988 p11 | "The General Plan Baylands provisions require 1,800 to 2,200 units of housing" |
| affordable | null | goal 514 units; minimum 15% | NEW | /View/2988 pp4, 26 | "a goal of 514 affordable units"; "a minimum of 15% of the total housing units" |
| officeLabSqft | 6,500,000 | 6.5M sq ft of all commercial uses, not office/lab only | CONFLICT (label) | Final EIR notice /View/3010 p1 | "6.5 million square feet of commercial, office, retail, conference, life science, and office campus uses" |
| commercialSqftTotal | 7,000,000 | 7,000,000 including 500,000 hotel | CONFIRMED | /View/2988 p11 (Table 2.3.1) | "TOTAL SPECIFIC PLAN AREA 680.1 2,200 7,000,000" |
| hotelKeys | null | ~800 rooms | NEW | /View/3010 p1 | "500,000 square feet of hotel use (approximately 800 rooms)" |
| openSpaceAcres | 100 | 148.4 designated Open Space; notices say 157 acres of open space/open area, parks and trails | CONFLICT | /View/2988 p14; /View/3010 p2 | "A total of 148.4 acres (approximately 27.9%) is designated as Open Space" |
| school | — | grade 6–8 middle school | NEW | /View/3010 p1 | "a grade 6–8 middle school" |
| heights | — | up to four towers ≤270 ft; 80 ft within 350 ft of US 101; 40 ft within 200 ft of the Roundhouse | NEW | Specific Plan ch.3 /View/2996 pp8, 9, 21 | "a maximum of four tower buildings (two commercial and two residential) … not exceeding 270 feet in height" |
| Roundhouse | restored | preserved and repurposed | CONFIRMED | /View/2986 p9 | "The historic Roundhouse building is to be preserved and repurposed" |
| 2018 Measure JJ | yes | GP-1-18 approved by voters as Measure JJ, Nov 2018 | CONFIRMED | /View/2986 p3 | "GP-1-18 was introduced as Measure JJ and was then voted in by the citizens of Brisbane" |
| Draft EIR | 2025-04 | Apr 3, 2025; comments closed Sept 2, 2025 | CONFIRMED | brisbaneca.gov/774 | "The Draft EIR published on April 3, 2025" |
| Final EIR | 2026-05-14 | May 14, 2026 | CONFIRMED | brisbaneca.gov/775 | "The Final EIR was published on May 14, 2026." |
| Planning Commission | 2026-06/08 | hearings June 25, June 30, July 23; Aug 13, 2026 recommended approval 5-0 | CONFIRMED + NEW | PC minutes Aug 13, 2026 (CivicClerk fileId 12583) pp1–3 | "to adopt the Staff-Recommended Specific Plan (May 2026) … The motion was approved 5-0." |
| Bayshore Mobility Plan | — | Res. PC-01-26 (July 23, 2026), excluding the Bayshore Blvd road diet | NEW | Council packet Oct 6, 2026 (fileId 12627) p4 | "the Planning Commission adopted Resolution PC-01-26" |
| City Council | "this fall" | hearings began Sept 14, 2026, continued Sept 29 and Oct 6; no action yet; fiscal review pending | UPDATE | fileId 12627 pp3, 8 | "Tonight is the third meeting in a series of meetings … that began on September 14, 2026" |
| 2027 start | stageNote | only the developer's housing schedule quoted in the plan | UNCONFIRMED | /View/2988 p5 | "based on developer's schedule for 2,200 total units**: 2027: 362 units" |
| CEQA | — | SCH 2006022136; applications 2021-ER-1/2021-SP-1/2021-RZ-3/2021-GPA-2 | NEW | /View/3010 p1 | — |

Sources: https://www.brisbaneca.gov/DocumentCenter/View/3010,
https://www.brisbaneca.gov/DocumentCenter/View/2988,
https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12583,plainText=false),
https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12627,plainText=false)

Boundary: the city's ArcGIS layer "Baylands Specific Plan Boundary" (services9.arcgis.com,
org UGpGSV1ugL0pHSgX, `Baylands_Specific_Plan_Boundary_DRAFT_Map_WFL1/FeatureServer/1`) is
titled DRAFT, last edited June 2022, ~702 acres (vs 680.1), no posted license: approximate
only. Better: trace the 2026 plan figures (General Plan land use map /View/3039, zoning map
/View/3038, Specific Plan Fig. 2.3.1 /View/2988 pp10–11). City parcels and zoning layers are on
the same host.

Still open: Council vote and resolution/ordinance numbers; development agreement; Notice of
Determination; a non-draft GIS boundary. `thebaylands.com` is the developer's site (reported).

## willow-village

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 56 | ~59 main site (59.17 by legal description); ~62 with Hamilton parcels | CONFLICT | DA (Ord. 1095) pp11, 76 | "The Property comprises approximately 59 acres intended as the primary development location" |
| homes | 1,500 | up to 1,730 | CONFLICT | city project page; DA p2 | "Up to 1,730 multifamily housing units, including 312 below market rate units" |
| affordable | null | 312 BMR (260 inclusionary = 15%, plus 52), including 119 senior | NEW | project page | "312 below market rate units (260 inclusionary units or 15%, plus 52 units per the city's commercial linkage fee…)" |
| officeLabSqft | 1,750,000 | 1.6M office and accessory (≤1.25M office) | CONFLICT | DA p2 | "up to 1.6 million square feet of office and accessory uses (a maximum of 1,250,000 square feet for offices…)" |
| retailSqft | 125,000 | up to 200,000 | CONFLICT | DA p2 | "up to 200,000 square feet of retail uses" |
| hotelKeys | 200 | up to 193 | CONFLICT | DA p2 | "an up to 193-room hotel" |
| openSpaceAcres | null | 20 (≈8 publicly accessible) | NEW | DA p12 | "20 acres of open space including approximately 8 acres of publicly accessible parks and pathways" |
| parks | 3.5 + 1.5 + 2 ac | same | CONFIRMED | project page | "approximately 3.5-acre park, 1.5-acre town square, a dog park, 2-acre elevated linear park" |
| approval | 2022-12-06 | Dec 6 and 13, 2022; DA Ordinance 1095 adopted Dec 13, 2022 | CONFIRMED + NEW | project page; DA p4 | "PASSED AND ADOPTED … on the thirteenth day of December, 2022" |
| later approvals | — | architectural control plans June–Sept 2023; Chevron rebuild Aug 27, 2024 | NEW | project page | "On August 27, 2024, the City Council approved the use permit and architectural control to redevelop the Chevron station" |
| pause | 2026-05-01 | paused per Meta as of May 1 | CONFIRMED | city news 2026-05-04 | "The Willow Village project has been paused per Meta as of May 1." |
| good-faith finding | 2026-05-18, Meta | applicant Peninsula Innovation Partners, LLC; passed 5-0 | CONFIRMED (party corrected) | June 8, 2026 PC packet p39 (draft minutes) | "to adopt a resolution of determination of good faith compliance as stated for Item F6; passes 5-0" |
| nothing built | — | city suspended review of improvement plans and maps | CONFIRMED | staff report 26-020-PC p286 | "City staff has suspended its review of these actions at this time" |
| DA through 2032 | 2032 | 10-year term from the effective date (30 days after Dec 13, 2022), so ~Jan 2033; one 7-year extension possible | CONFLICT | DA p3 §9; p21 §2.2 | "The 'Initial Term' of this Agreement shall be ten (10) years, commencing on the Effective Date" |

Sources: https://www.menlopark.gov/Government/Departments/Community-Development/Projects/Approved-projects/Willow-Village,
DA https://www.menlopark.gov/files/sharedassets/public/v/1/community-development/documents/projects/under-review/willow-village/1095-willow-village-development-agreement.pdf,
https://www.menlopark.gov/News-articles/City-news/20260504-Willow-Village-project-paused,
https://www.menlopark.gov/files/sharedassets/public/v/3/agendas-and-minutes/planning-commission/2026-meetings/agenda/20260518-planning-commission-agenda-packet-amended.pdf,
https://www.menlopark.gov/files/sharedassets/public/v/1/agendas-and-minutes/planning-commission/2026-meetings/agenda/20260608-planning-commisison-agenda-packet.pdf

Boundary: the DA's Exhibit A-2-1 metes-and-bounds description of the 59.17-acre main site (DA
pp75–76) with the Exhibit A-1-1 map; traceable exactly. Alternative: Menlo Park parcels (CC0)
services7.arcgis.com/uRrQ0O3z2aaiIWYU/arcgis/rest/services/City_of_Menlo_Park_Parcels/FeatureServer/7
(1350–1390 Willow Rd, 925–1098 Hamilton Ave, 1005–1275 Hamilton Ct). Avoid the 2018 zoning layer.

Still open: Council resolution numbers for Dec 6, 2022; DA effective and recording date.

## parkline

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 63 | ~64.3 (63-acre SRI campus + 1-acre 201 Ravenswood) | CONFLICT | Council report 25-143-CC pp3, 11 | "approximately 64.3 acre site commonly known as 201, 301 and 333 Ravenswood Avenue and 555 and 565 Middlefield Road" |
| homes | 800 | 800 (646 market-rate + parcel for up to 154 affordable) | CONFIRMED | same p8 | "The proposed project would add 800 residential units, including 251 BMR units" |
| affordableHomes | 251 | 251 | CONFIRMED | same | as above |
| officeLabSqft | 925,000 | 925,000, within a 1M non-residential cap (75,000 amenity/retail) | CONFIRMED + NEW | Sept 30, 2025 minutes p5 | "office/research and development (R&D) spaces (925,000 square feet) and commercial amenity or commercial/retail uses (75,000 square feet)" |
| openSpaceAcres | 12 | 12 (≈2.6 dedicated parkland) | CONFIRMED | city news 2026-06-22 | "12 acres of publicly accessible open space, with approximately 2.6 acres of dedicated parkland" |
| approval | 2025-09-30 | 5-0 resolutions; ordinances adopted Oct 7, 2025 (4-0) | CONFIRMED + NEW | Oct 7, 2025 minutes p3 | "On October 7, 2025, the City Council adopted (4-0) the ordinances for the approval of the master plan" |
| PC recommendation | — | Res. 2025-038 | NEW | 25-143-CC p11 | "PLANNING COMMISSION RESOLUTION NO. 2025-038" |
| Phase 2 | 2026-06-04 | submitted; 1,082 units (293 BMR); ~901,493 sq ft office/R&D; ~40,629 sq ft retail; 14 acres open space | CONFIRMED | Phase 2 page; news 2026-06-22 | "An increase of 282 residential units for a total of 1,082 units (293 below market rate units)" |
| Phase 2 process | — | deemed incomplete July 2, 2026; consultant contract Aug 11; resubmitted Aug 13; PC study session Sept 14; Council study session Sept 22 | NEW | Phase 2 page | "The Planning Commission held a study session on the proposed project at its meeting on Sept. 14" |
| SRI leaves | stageNote | city: all buildings demolished, including P, S and T kept in 2025; "SRI will vacate" is the applicant's claim | PARTLY | Phase 2 page | "including Buildings P, S, and T, which were proposed to be retained as part of the 2025 approval" |
| demolition by end of 2027 | stageNote | not found | UNCONFIRMED | — | — |

Sources: https://www.menlopark.gov/Government/Departments/Community-Development/Projects/Approved-projects/Parkline,
https://www.menlopark.gov/files/sharedassets/public/v/2/agendas-and-minutes/city-council/2025-meetings/20250930/j1-20250930-cc-parkline.pdf,
https://www.menlopark.gov/files/sharedassets/public/v/1/agendas-and-minutes/city-council/2025-meetings/minutes/20251007-city-council-special-and-regular-minutes-approved.pdf

Boundary: Menlo Park parcels (CC0), union of APNs 062390050, 062390660, 062390670, 062390730,
062390760, 062390780 (LotArea sum ≈64.2 acres, matching 64.3).

Still open: Council resolution and ordinance numbers; outcome of the Sept 22, 2026 study session.

## north-bayshore

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 153 | ~153 | CONFIRMED | Council report June 13, 2023 (mountainview.legistar.com gateway c5d191b7…) p3 | "Project Area: Approximately 153 acres." |
| homes | 7,000 | up to 7,000 (5,950 market-rate + ~1,050 affordable) | CONFIRMED | report p17 | "up to 5,950 market-rate units and up to an estimated 1,050 affordable units (15% of units)" |
| affordablePct | 15 | 15% via ~7 acres of land dedication | CONFIRMED | report pp4, 12 | "including 15% affordable units by land dedication" |
| officeLabSqft | 3,000,000 | 3,117,931 | CONFLICT | report p4 | "3,117,931 square feet of office development, including 1,814,681 square feet of existing office to be rebuilt" |
| retailSqft | null | 233,990 ground-floor retail (+55,000 community) | NEW | Res. 18810 title | "233,990 Square Feet of Ground-Floor Retail, 55,000 Square Feet of Community Space" |
| hotelKeys | null | up to 525 | NEW | report p4 | "Up to 525 hotel rooms in two locations with building heights ranging from 10 to 13 stories" |
| openSpaceAcres | 26 | 26.1 (14.8 public park + 11.3 POPOS) | CONFIRMED | report pp1, 4 | "Approximately 14.8 Acres of Dedicated Public Park Land, Approximately 11.3 Acres of Privately Owned, Publicly Accessible Open Space" |
| heights | — | residential 5–15 stories; office 4–8; hotel 10–13 | NEW | report p4 | "7,000 high-density residential housing units with heights ranging from five to 15 stories" |
| approval | 2023-06-13 | Resolutions 18809 (EIR), 18810 (master plan), 18811 (map), 18812, 18813/S-172 | CONFIRMED + NEW | Legistar event 2504 minutes | "Adopt Resolution No. 18810 of the City Council … Approving a Master Plan to Construct Up to 7,000 Residential Units…" |
| DA | — | 30-year DA, Ordinance 9.2023, second reading June 27, 2023 | NEW | Legistar event 2505, matter 7495 | "Adopt Ordinance No. 9.2023 … Approving a Development Agreement Between the City of Mountain View and Google LLC" |
| precise plan cap | 9,850 | 9,850 units, 3.6M sq ft office (plan EIR); plan adopted Nov 25, 2014; residential added Dec 12, 2017 (Res. 18186) | CONFIRMED | North Bayshore Precise Plan (showpublisheddocument/4406) pp3, 253 | "9,850 units and 3.6 million square feet" |
| 2024 Landings terminated; 2025 Middlefield Park sale | timeline | not found officially (Middlefield is in East Whisman) | UNCONFIRMED | — | — |
| 2026 status | — | no master plan or DA amendment since 2023 | UNCONFIRMED | Legistar | — |

Sources: https://www.mountainview.gov/our-city/departments/community-development/planning/active-projects/google-projects/north-bayshore-master-plan,
https://mountainview.legistar.com/gateway.aspx?M=F&ID=c5d191b7-b2bd-4e61-a167-15b425bc8c98.pdf,
https://www.mountainview.gov/Home/Components/News/News/647/

Boundary: Mountain View parcels (maps.mountainview.gov/arcgis/rest/services/Public/Parcel/MapServer/0)
filtered to the 39 APNs in Legistar matter 7641 (37 matched); approximate, since the plan covers
parts of the Gateway parcels and Lot C. Open-data terms allow use "at your own risk". The zoning
layer's `PRECPLAN='P(39)'` is the whole precise plan district, not the master plan. Or trace the
master plan figure (showpublisheddocument/7175).

Still open: construction or permit status 2025–26; precise plan amendments after 2021.

## New official hosts used

`brisbaneca.api.civicclerk.com` (Brisbane agendas), `mountainview.legistar.com` and
`legistar1.granicus.com` (Mountain View Legistar), `services9.arcgis.com` (Brisbane GIS, org
UGpGSV1ugL0pHSgX) and `services7.arcgis.com` (Menlo Park GIS, org uRrQ0O3z2aaiIWYU). ArcGIS hosts
should be accepted by org path, not the whole host. `.gov` city hosts already pass.
