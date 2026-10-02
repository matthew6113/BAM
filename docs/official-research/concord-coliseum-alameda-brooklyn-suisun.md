# Official-source findings: Concord NWS, Oakland Coliseum, Alameda Point, Brooklyn Basin, Suisun expansion

Checked 2026-10-02. oaklandca.gov, alamedaca.gov, suisun.com and bracpmo.navy.mil returned an
Akamai 403 to scripts. What worked: the Legistar web API (`webapi.legistar.com/v1/oakland|alameda`)
and attachment stores, Concord's OnBase agendas (`stream.ci.concord.ca.us`),
`concordreuseproject.org` (which the City calls "the City's project's website"), acgov.org,
CEQAnet, the Solano County Registrar, `suisunexpansion.com` ("© 2025 City of Suisun City") and
Suisun's agenda store on CloudFront. The 2023 Oakland Brooklyn Basin staff report is an image
scan, read as images. Local copies go in `data/raw/official/<project>/` (git-ignored).

## concord-naval-weapons-station

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 2,422 | ~2,422 EDC property (Area Plan ~5,038) | CONFIRMED | concordreuseproject.org/DocumentCenter/View/2374 (5/26/2026 staff report) p2 | "the approximately 2,422 acres of property to be redeveloped by the Reuse Project under the Economic Development Conveyance" |
| homes | 12,000 | 12,272 | CONFLICT | same pp3–4 | "The Project's overall residential unit count of 12,272 adopted in the Area Plan (2012)." |
| affordablePct | 25 | 25% | CONFIRMED | same p4 | "The commitment to 25 percent affordable housing." |
| commercialSqftTotal | null | ~6,000,000 | NEW | same p4 | "The commitment to 6 million square feet of all types of commercial space" |
| openSpaceAcres | null | 868 local parks, paths and bikeways (plus the 2,600-acre regional park) | NEW | same p4 | "The 868 acres of local parks, paths, and bike ways" |
| Navy payment | ~$628M | ~$628M over 30 years | CONFIRMED | same p3 | "the Navy should receive approximately $628 million over a thirty-year build-out" |
| ~$6B | notes | not found | UNCONFIRMED | — | — |
| initial transfer | — | ~1,000 acres; $4.6M deposit at closing in 2030 | NEW | same p3 | "A deposit of $4.6 million at the close of the initial property transfer in 2030." |
| Lennar | 2016 selected; withdrew 2020 | selected in "Phase V (2013–2016)" for ~500 ac; agreement allowed to expire Mar 31, 2020 | PARTLY / CONFLICT (wording) | concordreuseproject.org/148/Overview-of-the-Reuse-Project | "the Exclusive Negotiating Agreement with Lennar was allowed to expire on March 31, 2020." |
| Concord First Partners | — | selected Aug 21, 2021; agreement approved Oct 27, 2021 | NEW | concordreuseproject.org/187/Master-Developer-Selection-2021 | "On Saturday, August 21, 2021 the Concord City Council selected Concord First Partners LLC" |
| Brookfield | 2023-08 | negotiating agreement Sept 19, 2023; term sheet Mar 19, 2024; revised May 26, 2026 | PARTLY (no Aug 2023 vote record) | concordreuseproject.org/DocumentCenter/View/2379 p4 | "The LRA entered into an Exclusive Agreement to Negotiate (ENA) on September 19, 2023, with Brookfield (BCUS Acquisitions LLC)" |
| Navy term sheet (City) | 2026-05-26 | accepted unanimously | CONFIRMED | 5/26/2026 minutes: stream.ci.concord.ca.us/OnBaseAgendaOnline/Documents/ViewAgenda?meetingId=1425&type=minutes&doctype=2 | "The motion passed by unanimous vote of the Council." |
| Navy approval | 2026-09 | executed Sept 23, announced Sept 24, 2026 | CONFIRMED | cityofconcord.org/CivicAlerts.aspx?AID=926; concordreuseproject.org/DocumentCenter/View/2384 | "the U.S. Navy has approved the Term Sheet for the Concord Community Reuse Project" |
| next | Specific Plan | consultants this winter; engagement early 2027 | CONFIRMED | AID=926 | "which will start this winter, with additional community engagement expected to start in early 2027" |
| SB 328 | — | signed, announced Sept 30, 2026 | NEW | cityofconcord.org/CivicAlerts.aspx?AID=927 | "Governor Newsom Signs SB 328" |
| developer | Brookfield | BCUS Acquisitions LLC (Brookfield) | CONFIRMED | View/2374 p1 | — |

Boundary: Navy term sheet Exhibit A, "Economic Development Conveyance (EDC) Property" (Navy map
dated 2026-03-30, View/2384 p15). A figure: trace and label approximate. Exhibit B is the
developer's unadopted concept plan. City GIS doesn't capture the site.

## oakland-coliseum

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 112 | ~112 (Arena ~9 + Stadium ~103) | CONFIRMED | oakland.legistar1.com/oakland/attachments/a0162d35-495c-43e2-868d-34820b195207.pdf (7/9/2026 report, File 26-0905) pp2–3 | "The Property is approximately 112-acres in size" |
| developer | AASEG + Loop Capital via OAC | same | CONFIRMED | same p2 | "OAC is a single purpose entity comprised of Loop Capital and the African American Sports and Entertainment Group (AASEG)." |
| sale | arena first, $50M | both parcels in one closing: Arena $50M cash, Stadium $60M seller-financed, $125M total | CONFLICT | same p2 | "OAC would purchase both parcels in a simultaneous transaction" |
| closing | Sept 2026–Jan 2027 | target Sept 1, 2026, no later than Jan 30, 2027 | CONFIRMED | same p4 | "target closing date (Closing) of September 1, 2026 and no later than January 30, 2027." |
| ordinance | — | Ord. 13895 C.M.S., final passage July 21, 2026 | NEW | Legistar matter 37487 | — |
| CalPERS | — | $50M of proceeds, Res. 91262 C.M.S., July 21, 2026 | NEW | Legistar matter 37494 | — |
| exclusive negotiations | 2023-01 | Nov 16, 2021, Res. 88922 C.M.S. | CONFLICT | report p3 | "On November 16, 2021, the City Council adopted Resolution No. 88922 C.M.S." |
| 2024 sale | 2024 | June 26, 2024, Ord. 13801 C.M.S.; agreement Aug 31, amended Sept 23, 2024 | CONFIRMED | report pp3–4 | — |
| 2025 amendment | — | Ord. 13842 C.M.S., May 6, 2025 | NEW | report p4 | — |
| County term sheet | 2026-05-28 | non-binding, among OAC, Coliseum Way Partners (the A's) and the County | CONFIRMED | report p4; acgov.org County_Term_Sheet_Final.pdf | "On May 28, 2026, the County Board of Supervisors approved a non-binding term sheet" |
| affordable | null | ≥25% of residential units at ≤60% AMI, Stadium Parcel deed restriction | NEW | report Attachment A p14 | "At least twenty-five percent (25%) of any residential units built on the Property shall be designated affordable" |
| $5B+ vision | notes | not official | UNCONFIRMED | — | — |
| plan | — | Coliseum Area Specific Plan, Res. 85491, Mar 31, 2015 | NEW | report p3 | — |
| closing happened? | verify | no record found | UNCONFIRMED | — | — |

County term sheet: https://acgov.org/board/bos_calendar/documents/DocsAgendaReg_05_28_26%20Spmtg/GENERAL%20ADMINISTRATION/Regular%20Calendar/County_Term_Sheet_Final.pdf

Boundary: Alameda County Assessor parcels (services5.arcgis.com/ROBnTHSNjoZ2Wm1P/.../Parcels/FeatureServer/0,
county disclaimer only): APN 41-3901-8 (Stadium, 103.2 ac) + 41-3901-9 (Arena, 8.7 ac) = 111.8 ac.

## alameda-point

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 68 | 68 | CONFIRMED | Legistar alameda matter 15589 (Planning Board, Mar 9, 2026), webapi.legistar.com/v1/alameda/matters/15589/texts/16781 | "a Development Agreement (DA) for the 68-acre Site A project at Alameda Point" |
| homes | 800 | cap ~1,300 since 2022 | CONFLICT (superseded) | 2022 Development Plan, legistar1.granicus.com/alameda/attachments/73ff7e59-888e-443a-afc5-9a808b1d2091.pdf p11 | "TOTAL SHALL NOT EXCEED 1,300 RESIDENTIAL UNITS ACROSS 'SITE A'" |
| affordableHomes | 200 | 321 (25%) | CONFLICT (superseded) | matter 12022 report (July 25, 2022) | "The 321 deed restricted affordable housing units will be located on Block 8 (128 completed units), Block 10 (90 units), and Block 17b (103 units)." |
| commercial | 600,000 | 2015: 600,000; 2022: minimum 300,000 in Phases 2–3 | CONFLICT (superseded) | matter 12070 | "a minimum of 300,000 square feet of commercial floor area will be provided between Phase 2 and Phase 3." |
| openSpaceAcres | 15 | ±10.14 public park/plaza | CONFLICT | 2022 Development Plan p12 | "+/- 10.14 ACRES PUBLIC PARK/PLAZA" |
| Phase 1 | ~673 homes | 674 planned (546 + 128); 454 built in Blocks 6–9 | CONFIRMED + NEW | matter 12022; 2025 annual report (legistar1.granicus.com/alameda/attachments/4ed2a440-9155-4809-8443-5c523301c557.pdf) p2 | "APP has completed construction on the vertical development for Blocks 6, 7, 8, and 9." |
| approval | 2015-06 | June 2015; DA Ord. 3128 (Aug 31, 2015); DDA Aug 6, 2015 | CONFIRMED | matter 12022 | "In June 2015, the City Council unanimously approved a Site A Development Plan" |
| groundbreaking | 2018-05 | infrastructure began March 2018 | CONFLICT | annual report letter p1 | "APP commenced infrastructure in March 2018." |
| 2022 amendments | — | DDA 6th amendment Sept 6, 2022; DA 1st amendment Ord. 3328 (Nov 14, 2022) | NEW | matter 15589 | "pursuant to City Council Ordinance No. 3328" |
| status | needs verification | milestones tolled under Economic Force Majeure since 2023 | NEW | matter 15589 | "since 2023, the Site A Project has been subject to Economic Force Majeure… the project's milestones are currently tolled" |
| ferry | — | terminal 2020; service from July 1, 2021 | CONFIRMED | letter p3 | "service commencing July 1, 2021" |
| Navy conveyance | — | Phase 2 conveyed; Phase 3 still with Navy (2022) | NEW | matter 12022 | — |
| Blocks 12/13 | — | Radium performing arts center (~53,000 sf), heard Mar 2026 | NEW (final action unconfirmed) | matters 15637, 15669 | — |
| developer members | TCR, srmERNST, Eden… | records name Alameda Point Partners, LLC; Eden Housing for Block 10B | UNCONFIRMED (members) | letter p3 | — |

Boundary: no Site A GIS layer; City of Alameda zoning `AP-WTC` is 150.1 ac (too big). Trace the
2022 Development Plan "Open Space & Parcel Diagrams" (p12; 16.33 ROW + 41.36 private + 10.14 park
≈ 68 ac), or assemble county parcels.

## brooklyn-basin

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 64 | 64.2 land (+7.95 water) | CONFIRMED | File 25-0862 report (7/1/2025) p2 | "approximately 64.2 acres of land area (and 7.95 acres of water surface area)" |
| homes | 3,100 | up to 3,700 since May 2023 | CONFLICT (superseded) | same; 2023 report oakland.legistar1.com/oakland/attachments/07b0c42f-e3a7-49c6-bb27-24a25c6eae73.pdf p2 | "an increase in residential density by 600 units for a project site total of up to 3,700 units" |
| affordableHomes | 465 | 465, all built (A 254 + F 211) | CONFIRMED | 2025 report p3 | "Parcel A … 254 … Completed and occupied" |
| commercial | 200,000 | up to 200,000 | CONFIRMED | 2025 report p2 | "up to 200,000 square feet of commercial space" |
| openSpaceAcres | 30 | ~31 (2025) | CONFLICT (minor) | File 25-0757 report p2 | "approximately 31 acres of parks and public open space, two renovated marinas" |
| +600 units | proposal | approved: Res. 89707–89709 (May 2, 2023); Ord. 13738, 13739 (May 16, 2023) | CONFIRMED | 2025 report p2 | "approved by Ordinance No. 13739 C.M.S. on May 16, 2023" |
| completion 2038 | — | not stated; last parcels "Construction to start approx. 2031" | UNCONFIRMED | 2025 report p3 | "Parcel M … Construction to start approx. 2031" |
| built | several | A, B, C, F complete and occupied; G, J complete and leasing (1,696 units total); D, E, H, K, L, M future | NEW | 2025 report p3 | "Parcel G 371 … Completed and under lease up" |
| original approval | — | Ord. 12760 (July 18, 2006); re-approved Jan 2009 (Res. 81769) | NEW | 2025 report p2 | — |
| affordable parcels | 2014 | early purchase authorized May 7, 2013 (Res. 84349); A/G swap Ord. 13413 (2017) | CONFLICT | matters 22206, 26980 | — |
| developer | Signature, Zarsion, R&B; MidPen | Zarsion-OHP I, LLC; MidPen and Oakland Housing Authority | PARTLY | matters 34148, 28098 | — |
| BCDC | — | permit 2006.007.00 (Feb 4, 2011), amended three times; +600 units needs a material amendment | NEW | BCDC letter Aug 10, 2021 (CEQAnet attachment) | "On February 4, 2011, the Commission issued Permit No. 2006.007.00" |

Boundary: Oakland zoning (services.arcgis.com/9tC74aDHuml0x5Yz/.../Zoning_Group_Layers_/FeatureServer/0),
`BASEZONE='D-OTN'`: 31.1 ac of development parcels; parks need county parcels or tracing the
2023 report's status figure (p3). "For reference only" terms.

## suisun-expansion

| field | data value | official value | status | source | quote |
|---|---|---|---|---|---|
| acres | 22,873 | 22,873 | CONFIRMED | ceqanet.lci.ca.gov/2025110452 (NOP, Nov 12, 2025), attachment nT6gPE p2 | "annexation of 22,873 acres of unincorporated Solano County land" |
| acresNote | 15,737 + 5,726 | same; Area Plan 7,136 incl. 1,410-ac Lambie Industrial Park | CONFIRMED + NEW | NOP pp2, 5 | "establish a 5,726-acre protection zone" |
| homes | null | 173,913 at buildout; 65,217 in the 20-year plan; 147M sq ft nonresidential; 400,000 people | NEW | NOP p7 Table 1 | "Total 15,737 100% 173,913 147,004,024 225,471 400,000" |
| 2024 measure withdrawn | 2024 | July 22, 2024 | CONFIRMED | content.solanocounty.gov/sites/default/files/2025-05/CA%20Forever%20Initiative%20Withdrawal%20Letter-07222024.pdf | "is withdrawn." |
| city explores | 2025-01 | January 2025 | CONFIRMED | suisunexpansion.com/vision-and-background/history-background/ | "the City Council directed the City Manager to explore annexation opportunities in January 2025." |
| reimbursement agreement | — | June 10, 2025, Res. No. 50, 3–1 | NEW | Suisun 6/17/2025 packet pp117–119 (d3n9y02raazwpg.cloudfront.net/suisuncityca/839016df-…-1749779358.pdf) | "AYES: Dawson, Hernandez, Shepherd NOES: Washington ABSENT: Pal" |
| application | 2025-10 | posted Oct 14, 2025; "accepted" not found | PARTLY | suisunexpansion.com/5843-2/; NOP p2 | "California Forever (applicant) submitted an application to Suisun City" |
| NOP | 2025-11 | received Nov 12, 2025 | CONFIRMED | CEQAnet 2025110452 | — |
| EIR schedule | fall 2026 etc. | no draft EIR on CEQAnet; no official schedule | UNCONFIRMED | — | city FAQ: "final decisions expected beyond 2026" |
| LAFCo | partner | no application found | UNCONFIRMED | solanolafco.gov | — |
| Solano Shipyard | notes | not in NOP | UNCONFIRMED | — | — |

Boundary: no official GIS. Trace NOP Figure 2 (p15), with Figures 5 and 6; label approximate.

## Hosts

City-run but not `.gov`/`.ca.us` (a policy call: add them to `src/projects/official.ts`?):
`concordreuseproject.org`, `cityofconcord.org`, `suisunexpansion.com`, `acgov.org`; Legistar
hosts `oakland.legistar1.com`, `legistar1.granicus.com`, `oakland.legistar.com`,
`alameda.legistar.com`, `webapi.legistar.com`. Path-scoped: the Suisun CloudFront store
(`d3n9y02raazwpg.cloudfront.net/suisuncityca/`), ArcGIS org paths, `gis.cityofconcord.org`.

Search-engine claims that were wrong: a "$44.6M total cost" for Concord (it's a $4.6M deposit
plus ≥$40M guaranteed); "Phase 1 ~673 homes built" at Alameda Point (454 are built).
