# Official-source findings: Related Santa Clara, Downtown West, Moffett Park, The Rise

Checked 2026-10-02. The main city sites (santaclaraca.gov, sanjoseca.gov, sunnyvale.ca.gov,
cupertino.gov) returned an Akamai 403 to scripts, so everything here comes from the cities'
Legistar systems (detail pages, web API, attachment stores santaclara.legistar1.com and
legistar.granicus.com), city GIS servers, Santa Clara County open data and the State
legislature. Local copies go in `data/raw/official/<project>/` (git-ignored). Page numbers are
PDF pages. Matter IDs are Legistar matter IDs.

## related-santa-clara

Sources (attachments at `https://santaclara.legistar1.com/santaclara/attachments/<id>.pdf`):
- 2016 report: Council report June 28, 2016, `097f41c1-1cf5-4b30-8f97-3036e448ab46`; matter 11541 https://santaclara.legistar.com/LegislationDetail.aspx?ID=11541&GUID=B390333B-FB40-4778-A7F3-02C7B44B3D2D
- Ord 1956: 2016 development agreement, `3f1462b1-c840-4ae8-b2cf-20565e67a6e5`
- PC 2025: Planning Commission report June 11, 2025, `9fffc632-0218-4698-8724-556a02aee1fc`
- Res 25-9467: rezone with the Scheme C supplement, `9db31837-65bc-485b-a1ef-ce58bade9f50`
- CC 2025: Council report July 8, 2025, https://santaclara.legistar.com/LegislationDetail.aspx?ID=24933&GUID=38CEF124-14D5-41B3-9083-8DE1E25581AC
- Votes: https://webapi.legistar.com/v1/santaclara/eventitems/228984/votes (July 8, 2025), /232352/votes (Sept 16, 2025)
- Ordinance 2078: https://santaclara.legistar.com/LegislationDetail.aspx?ID=25312&GUID=AF23DEE1-7B57-4309-8889-60BC46051875

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 240 | ~240 | CONFIRMED | PC 2025 p1 | "Site Area: 240 acres" |
| homes | 1,680 | max 1,680, min 200 | CONFIRMED (cap) | 2016 report p1; Res 25-9467 p14 | "A minimum of 200 residential units and a maximum of 1,680 residential units" |
| affordable | null | 2016: 10% at ≤120% AMI; 2025: 15% at ≤100% AMI after the first 200 units | NEW | PC 2025 p8 | "15% of the units must be affordable to households with income that does not exceed one hundred percent (100%)" |
| officeLabSqft | 5,000,000 | 2016 DA up to 5,724,400; Scheme C (2025) 4,517,400 office + 1,600,000 light industrial | CONFLICT | Ord 1956 p11; Res 25-9467 p14 | "4,517,400 square feet (sf) commercial office; 800,000 sf commercial retail ... 1,600,000 square feet of light industrial, 700 hotel rooms; 1,680 residential dwelling units; approximately 90 acres of open space" |
| commercialSqftTotal | 9,200,000 | 9.16M gross sq ft all uses | CONFLICT (rounding) | 2016 report p1 | "a maximum of 9.16 million gross square feet of overall floor area for all uses" |
| retail | null (~1M in notes) | 2016 up to 1,526,000; Scheme C 800,000 | CONFLICT / NEW | Ord 1956 p11; Res 25-9467 p14 | "retail/restaurant/entertainment (up to 1,526,000 square feet)" |
| hotelKeys | 700 | 700 | CONFIRMED | Ord 1956 p11 | "hotel (up to 700 hotel rooms)" |
| openSpaceAcres | 30 | park "more than 30" ac (~31); Scheme C counts ~90 ac of all open space | CONFIRMED | Ord 1956 p11; 2016 report p9 | "approximately 31 acres for a new City park on Parcel 3" |
| heights | — | up to 17 stories; 219 ft above sea level limit; Scheme C allows ~10–12 stories on Parcel 4 | NEW | 2016 report p1; PC 2025 p6 | "buildings up to 17 stories in height" |
| 2016 approval | 2016 | June 28, 2016: Res 16-8338 to 16-8341; Ords 1956 (DA) and 1957 (leases) passed to print. $6.5B not official | CONFIRMED | matter 11541 | — |
| 2019 construction announcement | timeline | none | UNCONFIRMED | — | — |
| office→industrial vote | July, year unknown | July 8, 2025: Res 25-9465 (addendum), 25-9466 (GPA), 25-9467 (rezone, Scheme C); DA amendment introduced; 4–3 (Ayes Gonzalez, Hardy, Cox, Gillmor; Nays Chahal, Park, Jain). Ordinance 2078 adopted Sept 16, 2025, 4–3 | CONFIRMED + NEW | votes API; CC 2025 | — |
| data centers double rent | stageNote | confirmed | CONFIRMED | CC 2025 | "Any land within Parcels 1 and 2 that is developed as a data center will be subject to twice the rent that would otherwise be charged." |
| unbuilt | — | site vacant | CONFIRMED | PC 2025 p1 | "Existing Conditions: The site is currently vacant." |
| phasing | verify | development area plan 1 (Parcel 5) Mar 24, 2020; plan 2 (Parcel 4) July 13, 2020; plan 1 vesting tentative map Nov 15, 2022 (Res 22-9152); Scheme C lets Parcels 1–2 go first; Phase 2 deadline extended for "Materially Adverse Economic Conditions" | NEW | matters 16305, 16525, 21197; CC 2025 | "The Developer may ground lease any of the three phases within Parcels 1 and 2 for industrial development ahead of ground leasing Phase 2 within Parcel 4." |
| 2026 lawsuit | — | closed session Aug 2026: Related Santa Clara, LLC vs. Jennifer Osborn, et al, case 26CV489245 (subject unknown) | NEW | matter 26733 | — |

Boundary: Santa Clara County parcels (data.sccgov.org `ubcd-cewv`), APNs 104-03-043, -042,
-041, -036, 104-01-102, 097-01-039, 097-01-073 (~238.8 ac). License not stated in metadata;
check the county's terms. Fallback: Scheme C site plan figure.

## downtown-west

Sources (attachments at `https://legistar.granicus.com/sanjose/attachments/<id>.pdf`):
- Memo 2021: Planning Commission memo May 14, 2021, `268a6356-aa92-4cd6-b1ef-2ec5e34ff2a7`; matter 9022 https://sanjose.legistar.com/LegislationDetail.aspx?ID=9022&GUID=A707E4E6-4619-43CD-A312-DDC466FF9F25
- DA draft: May 18, 2021, `0eb2a75e-4aea-49f4-af9e-6c153efe0a4a`
- Supp 0517: `ae66b756-04ad-47b1-b28f-5b1547b990e0`
- Final adoption (June 8, 2021): https://sanjose.legistar.com/LegislationDetail.aspx?ID=9066&GUID=153A21E6-3F49-4E8C-9E35-EA0B9127E6D2
- CB 2023: committee memo Jan 23, 2023, `1c8ecd38-02ca-489d-9ca2-c708a1102813`
- CB 2024: Council memo Nov 25, 2024, `0b810cf1-d5af-4c58-9bf1-2f86f9063689`
- Fee 2025: Council memo Oct 27, 2025, `af5e6a1f-78d7-45f1-8ae2-734b42733ffc`
- SB 7: https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202120220SB7

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 80 | rezoning ~80 gross; PD permit ~78; tentative map ~84 | CONFIRMED | Memo 2021 pp1–3 | "Rezoning Approximately 80 Acres of Real Property Situated in Downtown San José" |
| homes | 4,000 | DA assumes 4,000; zoning allows up to 5,900 | CONFIRMED | DA draft p14; Memo 2021 p1 | "A MAXIMUM OF 5,900 RESIDENTIAL UNITS" |
| affordablePct | 25 | 25% is a shared goal for the whole Diridon Station Area Plan; project ~1,000 affordable units | CONFLICT (framing) | DA draft p14; CB 2023 p1 | "shared goal that development within the DSAP results in twenty-five percent (25%)" |
| officeLabSqft | 7,300,000 | max 7.3M | CONFIRMED | Memo 2021 p1 | "A MAXIMUM OF 7.3 MILLION GROSS SQUARE FEET (GSF) OF COMMERCIAL OFFICE SPACE" |
| retail | null | up to 500,000 gsf active uses | NEW | Memo 2021 p1 | "A MAXIMUM OF 500,000 GSF OF ACTIVE USES" |
| hotelKeys | null | 300 rooms + 800 limited-term corporate accommodations | NEW | Memo 2021 p1 | "A MAXIMUM OF 300 HOTEL ROOMS" |
| openSpaceAcres | null | ~15 (10.2 private publicly accessible + 4.8 dedicated) | NEW | DA draft p44 | "approximately fifteen (15) acres of new open space" |
| approval | 2021 | May 25, 2021; Ords 30608, 30609, 30610 passed for publication, final adoption set June 8, 2021 | CONFIRMED (final passage numbers unconfirmed) | CB 2024 p1 | "On May 25, 2021, City Council approved Google's Downtown West Mixed-Use Plan" |
| state law | 2021 | SB 7 signed May 20, 2021, extending AB 900 for this project | CONFIRMED | SB 7; Supp 0517 p10 | "05/20/21 Approved by the Governor" |
| 2023 pause | 2023 | official: delayed, no new construction, no restart timeline (2024); no 2023 date | UNCONFIRMED (year) | CB 2024 p3 | "no new construction has begun. At this time, there is no estimated timeline as to when the project may restart major development activities." |
| stage paused | — | consistent | CONFIRMED | CB 2024 pp2–3 | "These same challenges have delayed the Downtown West project." |
| 2026-03 empty/fenced; sports district | — | none | UNCONFIRMED | — | — |
| community benefit advance | — | $5M advance approved Dec 2024 | NEW | CB 2024 p3 | "make an advanced community benefits payment in the amount of $5,000,000" |

Boundary: City of San José Zoning Districts open data (CC-BY), MapServer layer 401 at
https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/401, query
`REZONINGFILE like 'PDC19-039%'`: 14 DC(PD) polygons approved 2021-05-25, ~58 net acres
(streets and creek excluded; 80 is gross). Credit "City of San José".

## moffett-park

Keep the plan-area framing.

Sources (attachments at `https://legistar.granicus.com/Sunnyvale/attachments/<id>`):
- PC 2023: report June 12, 2023, `95154818-6491-440c-84a3-d5ace8ab67ea.pdf`; matter 13792 https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=13792&GUID=26BD054A-EB50-4DB3-A67B-4DC62C5B6E01
- Min 7/11: https://legistar.granicus.com/Sunnyvale/meetings/2023/7/3762_M_City_Council_23-07-11_Meeting_Minutes.pdf
- Ord 3218-23: `898afbde-8963-4d24-bc5c-90e388ebed42.PDF` (matter 13874)
- Att9: `690d021e-457c-4a2e-8b95-76fd2c9d4f15.pdf`

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 1,270 | ~1,270 | CONFIRMED | PC 2023 p3 | "The Moffett Park Specific Plan Area is approximately 1,270 acres" |
| homes | 20,000 | 20,000 net new | CONFIRMED | PC 2023 p5 | "20,000 residential units" |
| affordable | null | min 15% deed-restricted, goal 20% | CONFIRMED | Att9 p1 | "Require a minimum of 15% of all residential units in Moffett Park as deed restricted affordable ... The goal of the Specific Plan is to reach 20%" |
| officeLabSqft | 10,000,000 | 10.0M net new office/industrial/R&D | CONFIRMED | PC 2023 p5 | "10.0 million square feet of office/industrial/R&D use" |
| retailSqft | 650,000 | 500,000 retail + 150,000 hospitality | CONFLICT | PC 2023 p5 | "500,000 square feet of retail use / 150,000 square feet of hospitality use / 200,000 square feet of institutional use" |
| existing | ~22M | 22.6M entitled (18.5M built) | CONFIRMED | PC 2023 pp2, 4 | "approved entitlements for about 22.6 million square feet" |
| adoption | 2023-07 | July 11, 2023: plan adopted, EIR certified (Res 1199-23), 7–0 as amended (Lockheed exemption 4–3); Ordinance 3218-23 adopted July 25, 2023 | CONFIRMED + numbers | Min 7/11 p12; Ord 3218-23 p7 | "The motion as amended carried with the following vote: Yes: 7" |
| projects since 2023 | verify | 333–385 Moffett Park Dr: 293,996 sq ft office/R&D, approved Dec 9, 2025, DA Ord 3250-25 adopted Jan 13, 2026. 1215 Bordeaux Dr: 8 stories, 265 apartments (40 affordable), Planning Commission June 8, 2026 | NEW | matters 16515/16567 (https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=16567&GUID=502BC91B-5390-4A9D-9E29-D467232F4A1E), 16913 | "construct a three-story building totaling 293,996 square feet" |

Boundary: Sunnyvale GIS General Plan service layer 8 "Specific Plan Boundary"
(`SP_Code='MP'`), https://gis.sunnyvale.ca.gov/arcgis/rest/services/GeneralPlan/MapServer/8,
one polygon of 1,271.6 ac (plus a separate 161-ac Lockheed Core Campus). No license stated.

## the-rise

Official framing: SB 35 ministerial approval (Gov. Code 65913.4) plus a 50% density bonus, not
builder's remedy.

Sources (attachments at `https://legistar.granicus.com/cupertino/attachments/<id>`):
- Approval 2024: second modification letter Feb 16, 2024, `61c2b68e-c1ce-44ee-9a66-55f5ebbc08e0.pdf`; matter 14268 https://cupertino.legistar.com/LegislationDetail.aspx?ID=14268&GUID=F7106253-9635-4B07-B568-9D7CA128BF5A
- Settlement: July 10, 2024 (Res 24-077), `6be5c2dd-eac9-422f-96a7-5c000b37ccc2.pdf`
- Memo 3/2024: `568033f5-3a3a-483f-9f6b-e769c05374db.docx`
- FM 2026: final map staff report July 21, 2026, `7813d568-939a-4160-a867-6912a65bfdfe.pdf`
- SIA 2026: `4e3bbad6-3215-4bd4-a4ea-ca168b6a8332.pdf`; matter 16200 https://cupertino.legistar.com/LegislationDetail.aspx?ID=16200&GUID=EE4A59A8-D22F-49F8-93DE-8033F1DE8237
- TEFRA: hearing for Oct 6, 2026, `a48ffc4f-a6db-4f2c-a12c-c966dfb6dfbf.pdf` (matter 16451)
- Status 2021: `7e0e84b1-2eae-4b09-91ab-f0a3d43beafe.docx`

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 50 | 50.82 | CONFIRMED | Approval 2024 p1 | "the 50.82-acre Vallco Mall property" |
| homes | 2,669 | 2,669 (2,402 + density bonus) | CONFIRMED | Approval 2024 p1; SIA 2026 p5 | "from 2,402 units to 2,669 units" |
| affordableHomes | 356 | 356 lower-income (2026); 890 in Feb 2024 | CONFIRMED | SIA 2026 p5 | "with 356 units of those residential units being affordable to lower income households" |
| officeLabSqft | 1,950,000 | 2024 ~1,954,613; 2026 "up to 1,474,946" | CONFLICT (newer wins) | SIA 2026 p5 | "a minimum of 226,644 square feet of retail uses and up to 1,474,946 square feet of office uses" |
| retailSqft | 226,400 | min 226,644 (2026) | CONFLICT (small) | SIA 2026 p5 | as above |
| openSpaceAcres | 7 | 7.48 public parkland + up to 4.805 private | CONFIRMED | Settlement p6 | "the 7.48 acres of public parkland as shown in Exhibit E is approved for dedication" |
| tallest ~200 ft | notes | no official height; no height limit applies | UNCONFIRMED | Approval 2024 p13 | "there are no height limits applicable to the original or modified project" |
| approvals | SB 35 | first approved Sept 21, 2018; modified 2022, Feb 16 2024, Feb 27 2026 (M-2025-001, TM-2026-006) | CONFIRMED + NEW | FM 2026 p1 | "the third and most recent modification application on February 27, 2026" |
| 2019 mall demolished | timeline | 2021: only above-ground demolition permits issued; JCPenney garage pending | UNCONFIRMED | Status 2021 | "Demolition permits have been issued for the above ground portions of the former Macy's and mall parking structures" |
| 2025-11 revision | timeline | official approval Feb 27, 2026 | CONFLICT (date) | FM 2026 p1 | — |
| first building | 232 affordable | Block 5: 234 units (174 VLI + 58 LI + 2 managers), Eden Housing; $135M bond hearing Oct 6, 2026; no permit application found | PARTLY | TEFRA p1 | "174 very low-income units, 58 low-income units, and 2 manager units" |
| stage | infrastructure | west-side soil cleanup signed off, excavation finished Feb 2024; Phase 1 final map (Tract 10706) on July 21, 2026 agenda (Res 26-080); no vertical permits until it records | CONFIRMED (not started as of July 2026) | Memo 3/2024; FM 2026 p1 | "No building permits for vertical construction on the westside parcel will be issued prior to recordation of the final map." |
| developer | — | Vallco Property Owner LLC (Sand Hill Property Company) | NEW | Approval 2024 | — |

Boundary: Santa Clara County parcels (`ubcd-cewv`), APN 316-20-121 (16.85 ac) and 316-20-122
(32.93 ac), 49.8 ac. License not stated. Fallbacks: Phase 1 final map, open-space layout.

## New official hosts used

Not `.gov`/`.ca.us`, so they'd need adding to `src/projects/official.ts`:
`legistar.granicus.com` (shared vendor host: match host and city path prefix), `santaclara.legistar1.com`,
`santaclara.legistar.com`, `sanjose.legistar.com`, `sunnyvaleca.legistar.com`,
`cupertino.legistar.com`, `webapi.legistar.com` (optional), `data.sccgov.org`.
