# Official-source findings: India Basin, Balboa Reservoir, Stonestown, Parkmerced

Checked 2026-10-02 against documents downloaded from SF Planning's document store and read in full text (local copies go in `data/raw/official/`, git-ignored). Page numbers are PDF page numbers.

URL shorthand:
- MIN = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/YYYYMMDD_cal_min.pdf` (Planning Commission minutes)
- CPC = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/`
- MEA = `https://sfplanning.s3.amazonaws.com/sfmea/`

---

## india-basin

Documents: MIN 20180726 (items 2, 15a–15g), MIN 20180823 (development agreement), MIN 20181018 and 20181025 (Board reports); CPC `2014-002541ENV.pdf` (final EIR certification motion and Responses to Comments, 2018-07-11); CPC `2014-002541DVA.pdf` (development agreement memo and text, hearing 2018-08-23); CPC `2014-002541GPA.pdf` (executive summary, hearing 2018-06-21).

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 29 | BUILD portion 29.26 ac; with the Rec and Park parks 38.24 ac; development agreement site "approximately 28 acres" | CONFIRMED (29.26) | ENV.pdf p.1 | "BUILD PORTION ... ABOUT 29.26 UNDEVELOPED ACRES"; "TOTALING ABOUT 38.24 ACRES" |
| acresNote: "~29 ac including public parks" | — | 29.26 ac is the BUILD portion only; with the parks 38.24 ac | CONFLICT | ENV.pdf p.1; MIN 20180726 item 15b | "redevelop approximately 39 acres located along the India Basin shoreline" |
| acresNote: "700 Innes parcel about 15 acres" | ~15 | 22.42 ac (17.12 developer-controlled plus 5.30 rights-of-way) | CONFLICT | DVA.pdf p.167 | "approximately 22.42 acres that includes 17.12 acres of property controlled by the Developer" |
| homes | 1,575 | 1,575 | CONFIRMED | MIN 20180726 item 15e (Res. 20250) | "approximately 1,575 residential units" |
| affordablePct | null | 25% | NEW | MIN 20180726 item 2 / MIN 20180823 (Res. 20261); DVA.pdf p.36 | "25% affordable housing and 11 acres of parks and open space" |
| commercialSqftTotal | 209,100 | 209,106 gsf (minutes round to 209,000) | CONFIRMED | ENV.pdf p.27 (RTC Table 2-1) | "Commercial Space—retail, office, R&D ... 209,106 gsf" |
| openSpaceAcres | 24.5 | 24.5 ac whole project (about 15.5 BUILD plus about 8.98 Rec and Park); the DA digest says "11 acres" for BUILD's commitment | CONFIRMED | ENV.pdf p.27 | "Publicly Accessible Recreation/Open Space ... (24.5 acres)" |
| heights | ~14 stories / 160 ft | 20–160 ft, up to 14 stories; height district 20/160-IB adopted 2018-07-26 (the GPA executive summary says 30/160-IB) | CONFIRMED | ENV.pdf p.28; MIN 20180726 item 15f (Res. 20251) | "ranging from one to 14 stories (20–160 feet tall)"; "from 40-X to 20/160-IB" |
| developer | BUILD | India Basin Investment, LLC "(aka BUILD)" | CONFIRMED | DVA.pdf p.1 | "India Basin Investment, LLC (aka BUILD)" |
| park construction (900 Innes 2022–24; Shoreline Park 2025–27) | — | none reachable (the BCDC deck is the applicant's presentation) | UNCONFIRMED | — | — |
| distressed stage; Sept 2026 default | — | none | UNCONFIRMED (press only) | — | — |

Approvals in the minutes:
- 2018-07-26, Planning Commission: final EIR certified (Motion 20247); CEQA findings (Motion 20248); shadow findings (Motion 20249); General Plan amendments (Res. 20250); Planning Code and zoning map amendments (Res. 20251); design standards and guidelines (Motion 20252).
- 2018-08-23: development agreement recommended (Res. 20261).
- October 2018: Board files 180816, 180680 and 180681 passed first and second reading (reported in MIN 20181018 p.5 and MIN 20181025 p.9; exact Board dates not given).

Boundary leads:
- Development and SUD lots (MIN 20180726 items 15d, 15g): 4606/100, 026; 4607/024, 025; 4620/001, 002; 4621/016, 018, 021, 100, 101; 4630/002, 005, 006, 007, 100; 4631/001, 002; 4644/001, 004a, 005, 006, 006a, 007–010, 010A–C, 011; 4645/001, 002b, 003a, 004, 006, 007, 007a, 010, 010A, 011–015; 4596/025, 026; 4597/025, 026.
- The whole EIR site (item 15b) adds 4629A/003–006, 010–013; 4646/001–003, 003A, 019, 020; 4622/007, 008, 012, 013, 016–019; 4605/010–019.
- Best for tracing: the metes-and-bounds legal descriptions in the development agreement, Exhibits A (developer property), B (India Basin Open Space) and D (rights-of-way), around DVA.pdf pp.100–107.
- EIR Figures 2-4b, 2-5b, 2-6a, 2-7a show massing and heights.

Still open: Board final-passage dates and ordinance numbers; later DA amendments; official source for park construction and the 2026 default.

---

## balboa-reservoir

Documents: MIN 20190613, 20190912, 20200409, 20200528 (items 17–18f), 20200730, 20200827; CPC `2018-007883GPA.pdf` (executive summary for initiating the General Plan amendments, with draft DA key terms and design standards; 87 MB).

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 17 | 17.6 ac (key terms and design standards say "approximately 17-acre") | CONFIRMED (17.6 preferred) | MIN 20200528 item 17; GPA.pdf p.31 | "a 17.6-acre project site within the Balboa Park Station Plan Area" |
| homes | 1,100 | about 1,100 (EIR also studied a 1,550-unit option) | CONFIRMED | MIN 20200528 item 18a (Motion 20731) | "approximately 1,100 dwelling units" |
| affordablePct | 50 | 50% | CONFIRMED (draft key terms, pre-approval) | GPA.pdf pp.4, 31 | "Fifty percent (50%) of the residential units produced by the Project will be affordable housing units" |
| affordableHomes | 550 | not stated as a number | UNCONFIRMED (derived) | — | — |
| openSpaceAcres | 4.2 | about 4 ac | CONFLICT (minor) | MIN 20200528 item 18a; GPA.pdf p.3 | "approximately 4 acres of open space" |
| 2-acre central park | — | about 2-acre Reservoir Park | CONFIRMED | GPA.pdf p.3 | "the approximately 2-acre "Reservoir Park."" |
| educator housing | City College and SFUSD | about 150 units with a City College preference; SFUSD not mentioned | PARTLY CONFIRMED | GPA.pdf p.33 | "approximately 150 units with a preference for City College employees" |
| retail / community | — | about 7,500 gsf retail; about 10,000 gsf community space and childcare | NEW | MIN 20200528 item 18a | "approximately 7,500 gross square feet of retail" |
| heights | — | 25–78 ft; 48-X for blocks TH1, TH2 and H, 78-X elsewhere | NEW | MIN 20200528 items 18a, 18e | "New buildings would range in height from 25 to 78 feet" |
| developer | BRIDGE and AvalonBay | DA party Reservoir Community Partners, LLC (draft key terms name BHC Balboa Builders, LLC) | UNCONFIRMED (the company names) | MIN 20200528 item 18f; GPA.pdf p.31 | "Reservoir Community Partners, LLC" |
| site owner | — | SFPUC | CONFIRMED | MIN 20190613 | "3180/190, owned by the San Francisco Public Utilities Commission" |
| Board approval 2020-08 | 2020-08 | Board denied the CEQA appeal and approved all four items (reported 2020-08-27) | CONFIRMED (month) | MIN 20200827 pp.6–7 | "The Board then voted to approve the General Plan, Planning Code, Zoning Map and Development Agreement" |
| DA executed 2021 | 2021 | none | UNCONFIRMED | — | — |
| Building A (159 homes) April 2026; first ~290 affordable homes | — | not reachable (sf.gov, sfbos blocked) | UNCONFIRMED | — | — |

Approvals in the minutes:
- 2020-04-09: General Plan amendments initiated (Res. 20679).
- 2020-05-28, Planning Commission: subsequent EIR certified (Motion 20730); CEQA findings (Motion 20731); General Plan amendments (Res. 20732); Planning Code and map amendments (Res. 20733); design standards and guidelines (Res. 20734); development agreement (Motion 20735, as printed).
- August 2020, Board: MIN 20200827 says second reading passed "on October 18th", which can't be right in an August report; exact date open.

Boundary leads: Block 3180, Lot 190 (partial); the SUD excludes "the 80-foot wide strip along the southern boundary containing SFPUC pipelines" (MIN 20200528 item 18e). Design standards figures 1.3-1, 1.3-2, 1.4-1 in GPA.pdf.

Still open: exact Board dates and ordinance numbers; whether the final DA kept 50%; whether construction started in 2026. The record's existing `sfbos.org/.../r0339-23.pdf` and sf.gov loan-committee sources may confirm these but weren't reachable.

---

## stonestown

No official document for the 2021–2024 redevelopment was reachable:
- The 2015–2022 minutes cover only mall permits (400 Winston Drive, Motions 20240 and 20332 in 2018; Motion 21114 in 2022).
- Every bucket key tried for case 2021-012028 (ENV, DVA, PRJ, GPA, PCA, MAP; DEIR, RTC, NOP on sfmea) returned 403.
- CEQAnet, media.api.sf.gov, sfbos.archive.sf.gov and sfplanning.org are blocked.

Every fact in the record is UNCONFIRMED (30 acres, 3,491 homes, 20% affordable, office/retail/community figures, 6 acres open space, 4–18 stories, ~200 senior homes, 2024 Board approval, $438M tax district). Search summaries mention a 43-acre site and a May 9, 2024 EIR certification; neither has been read in a document.

Leads (not yet read):
- Mall parcel: Block 7295, Lot 004 (400 Winston Drive), MIN 20180719 item 11.
- CEQAnet SCH 2022040571; notice of determination `media.api.sf.gov/documents/2024-0000037_NOD_-_Stonestown_Development_Project.pdf`.
- Board ordinance `sfbos.archive.sf.gov/sites/default/files/o0208-24.pdf`.
- EIFD No. 2 financing plan `media.api.sf.gov/documents/Stonestown_IFP_1-8-26.pdf`.

---

## parkmerced

Documents: CPC `2008.0021EMTZW.pdf` (memo for the 2010-12-16 hearing plus the 2010-10-21 executive summary); MEA `2008.0021E_Parkmerced_DEIR_VI-01.pdf` (draft EIR, 2010-05-12). No Parkmerced items in the 2013–2022 minutes. All figures are from 2010 pre-approval documents and may be superseded by the 2011 development agreement or later amendments.

| field | data value | official value | status | source | verbatim quote |
|---|---|---|---|---|---|
| acres | 152 | 152 ac including streets (about 116 without) | CONFIRMED | DEIR_VI-01 p.16; EMTZW.pdf p.47 | "approximately 116‐acre site (152‐acres including streets)" |
| homes | 5,679 net new, 8,900 total | same | CONFIRMED | DEIR_VI-01 p.16; EMTZW.pdf p.48 | "an additional 5,679 net new units ... a total of 8,900 units" |
| affordableHomes | null | 852 on-site | NEW (2010) | EMTZW.pdf p.48 | "5,679 new homes (852 of which are on‐site affordable units)" |
| retailSqft | 230,000 | 230,000 | CONFIRMED (2010) | EMTZW.pdf p.48 | "230,000 sf of neighborhood retail space" |
| officeLabSqft | 80,000 | 80,000 | CONFIRMED (2010) | EMTZW.pdf p.48 | "80,000 sf of office space" |
| community center | 64,000 sf | 64,000 sf | CONFIRMED (2010) | EMTZW.pdf p.48 | "64,000 sf dedicated to a community center" |
| openSpaceAcres | null | 68 ac | NEW | EMTZW.pdf p.48 | "68 acres of open space and new parks" |
| 11 towers stay | — | about 1,683 units in 11 towers kept; 1,538 replaced | CONFIRMED | DEIR_VI-01 p.16 | "About 1,683 of the existing apartments located in 11 tower buildings would be retained" |
| heights | — | new buildings 35–145 ft | NEW | EMTZW.pdf p.48 | "range in height from 35 feet to 145 feet" |
| 2011-05-24 Board approval; 2015 Phase 1; 2019 refinancing; 2025 receivership; 2026 Yellowstone | — | none | UNCONFIRMED | — | — |

Boundary leads: bounds and Assessor's Blocks on DEIR_VI-01 p.16 (Vidal Dr, Font Blvd, Pinto Ave and Serrano Dr to the north; 19th Ave and Junipero Serra Blvd to the east; Brotherhood Way to the south; Lake Merced Blvd to the west; Blocks 7303, 7303A, 7308–7311, 7314, 7316, 7319–7326, 7330–7345, 7333 A-B, 7333E, 7353–7373). Full block/lot list on EMTZW.pdf p.1. DEIR Figure III.1 (page III.5).

Still open: the development agreement (`default.sfplanning.org/publications_reports/parkmerced/R18273_PM_DA.pdf`, blocked); the EIR certification motion and date; 2015 Phase 1 records.
