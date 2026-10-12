# Official-source findings: Oceanwide Center and 30 Van Ness (San Francisco)

Checked 2026-10-12 against documents downloaded and read in full text (local copies in
`data/raw/official/oceanwide-center/` and `data/raw/official/30-van-ness/`, git-ignored), and live
queries of DataSF (building permits `i98e-djp9`, DBI inspections `vckc-dh2h`, DBI complaints `gm2e-bten`,
Planning records `qvu5-m3a2` and `y673-d69b`, development pipeline `6jgi-cpb4`, parcels `acdm-wktn`).
Page numbers are PDF page numbers.

Matthew asked on 2026-10-12 to add "Oceanside center" and "30 Van Ness". Both are single-site projects
well below the usual 1,000-home bar. They are added because Matthew asked for them (noted in each record's
`massingNotes` and in the CHANGELOG).

**Which project "Oceanside center" means.** No San Francisco Planning, Board or DBI record uses the name
"Oceanside Center". The match is **Oceanwide Center** (50 First Street, case 2006.1523): Planning's own
record is titled "Oceanwide Center (50 1st Street)". One complication: the press reports (September
2026) that a new owner has shown a different, office-only tower for the same site, "Fifty at First".
No official record of that proposal exists yet (no Planning application on the site's lots after 2023
except a 2026 development-rights determination), so the map shows the approved Oceanwide Center and
keeps "Fifty at First" in `reported`. If Matthew meant the new proposal, the record would need to wait
for a Planning application.

Hosts: none to add. Every source is on `sfplanning.org` (incl. `sfmea.` and `commissions.`), `sfgov.org`
(incl. `citypln-m-extnl.sfgov.org`), `sfbos.org`, `sfgov.legistar.com`, `webapi.legistar.com/v1/sfgov/`
or `data.sf.gov`. The Board's attachment store `sanfrancisco.legistar1.com` and Planning's property map
`sfplanninggis.org` were avoided by citing the `sfgov.legistar.com` and DataSF copies.

URL shorthand:
- CPE = `https://sfmea.sfplanning.org/2006.1523E_Checklist.pdf` (Community Plan Exemption Checklist,
  50 First Street (Oceanwide Center), Case 2006.1523E, 112 pp., PDF dated March 31, 2016)
- MEMO = `https://commissions.sfplanning.org/cpcpackets/2006.1523DNXOFACUAVARSHDGPR.pdf` (staff memo for
  the March 17, 2016 informational hearing, 97 pp.)
- LEG = `https://sfgov.legistar.com/View.ashx?M=F&ID=` (Board of Supervisors file 160382 attachments):
  M19634 = LEG`4454989&GUID=A607B5ED-2BAF-45E0-B68A-0F7144DFE111`, M19635 = LEG`4454990&GUID=A40F1C7E-8BCB-4D64-AC85-1CFCDFB96DF1`,
  M19636 = LEG`4455071&GUID=C79112F3-6AF1-4550-8F1D-752503B854C9`, M19637 = LEG`4455072&GUID=3A31535A-431D-439D-938F-DC9B031B1FC6`,
  M19638 = LEG`4455073&GUID=04D84447-104D-49A2-94EC-20C093ED3B12`, O137 = LEG`4607514&GUID=63A81AD4-51FC-4983-90E4-5D42DDF0EE87`
  (Ordinance 137-16 as finally passed)
- F160382 = `https://sfgov.legistar.com/LegislationDetail.aspx?ID=2694215&GUID=FE35D8F3-4DA8-432E-A2A3-BD70AD9B1EA0`
- O01-25 = `https://www.sfbos.org/sites/default/files/o0001-25.pdf` (Ordinance 01-25, File 240872, 13 pp.)
- DNX02 = `https://citypln-m-extnl.sfgov.org/Commissions/CPC/3_13_2025/Commission%20Packet/2024-008290DNX-02.pdf`
  (Planning Commission packet for March 13, 2025: executive summary, draft Motion, Exhibit A plans, 130 pp.)
- MIN0313 = `https://citypln-m-extnl.sfgov.org/Commissions/CPC/3_27_2025/Commission%20Packet/20250313_cpc_min.pdf`
  (minutes of March 13, 2025, in the March 27 packet)
- PKT2020 = `https://commissions.sfplanning.org/cpcpackets/2017-008051DNXCUAOFASHDENV.pdf` (Planning
  Commission packet for May 21, 2020, 526 pp., 105 MB)
- AG1107 = `https://sfplanning.org/sites/default/files/agendas/2024-11/20241107_cpc%20(ID%201480316).pdf`
- TR240872 = `https://sfgov.legistar.com/View.ashx?M=F&ID=13549190&GUID=41501879-C86D-4470-8C24-BA49C2117FFF`
  (Planning's transmittal of Resolution 21642 to the Board, Nov 13, 2024)
- DBI(n) = `https://data.sf.gov/resource/i98e-djp9.json?permit_number=n`; INSP(n) =
  `https://data.sf.gov/resource/vckc-dh2h.json?reference_number=n`

---

## oceanwide-center

Recommendation: **INCLUDE** (Matthew's call; stage `paused`). Two towers approved in 2016; demolition,
shoring, excavation and the first foundation pours were done under 2017 permits; nothing rose above ground.

Documents read:
- CPE (project description pp. 1–20, Table 2 p. 10, Figures 1–13), MEMO (pp. 1–4 incl. Table 1).
- Planning Commission Motions 19634 to 19638 (May 5, 2016), from Board file 160382.
- O137 (Ordinance 137-16, 18 pp.) and F160382 (file history and attachment list); Resolution 226-16 file
  `https://sfgov.legistar.com/LegislationDetail.aspx?ID=2694454&GUID=17F014EE-EA60-459F-B69D-CA1A98DDE517`.
- `https://sfbos.org/sites/default/files/bag071916_160701_notice.pdf` (notice of the July 19, 2016 hearing).
- DataSF building permits on block 3708 (site permits, demolition, shoring, excavation), DBI inspections
  for the two site permits, DBI complaints, and Planning records for the eight lots.

| field | official value | source | verbatim quote |
|---|---|---|---|
| name, sponsor | Oceanwide Center; sponsor Oceanwide Center LLC | CPE p.1; `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=2006.1523` | "Project Title: 50 First Street (Oceanwide Center) Project" "Project Sponsor: Oceanwide Center LLC"; Planning record: "project_name": "Oceanwide Center (50 1st Street)" |
| site, acres | 8 lots on block 3708 plus vacated street areas, 59,445 sq ft (1.36 acres) | CPE p.1 and p.2 | "Block/Lot: 3708 / Lots 3, 6, 7, 9, 10, 11, 12, and 55 (plus vacated portions of Jessie Street and Elim Alley) Lot Size: 59,445 square feet (1.36 acres)"; "comprising 54,586 square feet (1.25 acres), as well as portions of Elim Alley and Jessie Street totaling an additional approximately 4,859 square feet (1.36 acres in all)" |
| program | 265 homes, 169-room hotel, about 1.08 million gsf office, 12,500 sq ft retail | M19635 p.1 (title) | "CONSTRUCTION OF TWO TOWERS, MEASURING A MAXIMUM OCCUPIED HEIGHT OF 605. FEET AND 850 FEET, SHARING A FOUR-STORY BASEMENT, FOR A PROJECT CONTAINING 265 RESIDENTIAL UNITS, A 169 ROOM TOURIST HOTEL, APPROXIMATELY 1.08 MILLION GROSS SQUARE FEET OF OFFICE SPACE, AND 12,500 SQUARE FEET OF RETAIL SPACE" |
| program detail | office 1,079,925 gsf; retail 12,501 sf; hotel 255,346 gsf; residential 788,638 gsf; total 2,136,410 | CPE p.10 (Table 2) | "Residential -- 109 units (409,919 gsf) 156 units (378,719 gsf) 265 units (788,638 gsf)"; "Hotel -- -- 169 rooms (255,346 gsf)"; "Office 22,376 gsf 1,057,549 gsf -- 1,079,925 gsf"; "Retail 5,942 sf 1,095 sf 5,464 sf 12,501 sf"; "Total Built Area 28,318 sf 1,468,563 sf 639,529 sf 2,136,410 sf" |
| First Street Tower height | 850 ft roof, 910 ft top of features, 60 stories | M19635 p.2; CPE p.1 | "The First Street Tower is proposed to reach a roof height of approximately 850 feet with mechanical and architectural features extending to a height of 910"; "The tower on First Street would be 850 feet tall to the roofline, 910 feet tall to the top of the parapet, and have 60 stories." |
| Mission Street Tower height | 605 ft roof, 625 ft screening, 636 ft elevator equipment, 54 stories | M19635 p.2; CPE p.1, p.10 | "The Mission Street Tower is proposed to reach a height of approximately 605 feet with mechanical screening and features extending to 625 feet, further extending to a maximum of 636 feet to the top of elevator equipment"; CPE p.1 gives "605 feet tall, 636.5 feet to the top of the parapet, and have 54 stories" (Table 2 says 625 ft to the parapet) |
| uses by tower | First St: office floors 7–40, 109 homes on 43–60; Mission St: hotel floors 3–21, 156 homes on 22–54 | CPE pp.5, 10 | "Floors 7 (the first office level) through 40 of the First Street Tower would contain approximately 1.1 million gross square feet of office space"; "Floors 43 through 60 would contain approximately 109 dwelling units"; "amenities would occupy floors 3 through 21, along with 169 hotel rooms ... Floors 22 through 54 would contain 156 residential units" |
| urban room / open space | 68-ft ground-floor urban room; 26,348 sq ft public open space | CPE p.5, p.10 | "An open publicly accessible area (“urban room”) would be located at the ground floor, which would be 68 feet tall"; "Public Open Space -- 21,200 sf 5,148 sf 26,348 sf" |
| buildings kept | 88 First kept; front 45% of 76–78 First kept | CPE p.1 | "The proposed project would retain approximately the front (easternmost) 45 percent of the historic 16,200 square foot office building, located at 76-78 First Street"; "The existing 19,800 square foot building at 88 First Street ... would remain under its present use" |
| bulk | Mission tower lower floors 133 ft long, 164 ft 11 in diagonal, ~13,619 sq ft average | M19635 p.17 | "The length of typical lower tower floors is 133feet ... The typical diagonal dimension is approximately 164feet 11 inches ... Its average floor size is approximately 13,619 square feet" |
| approvals | Planning Commission, May 5, 2016: Motions 19634 (shadow), 19635 (DPA, 5–1), 19636 (office allocation), 19637 (hotel CUA), 19638 (GP findings) | M19635 p.39; M19637 | "I hereby certify that the Planning Commission ADOPTED the foregoing Motion on May 5, 2016." "AYES: Fong, Richards, Antonini, Hillis, Johnson NAYS: Moore"; M19637: "On May 5, 2016 the Commission adopted Motion No. 19635, approving a Section 309 Determination of Compliance" |
| CEQA | Community Plan Exemption under the Transit Center District Plan EIR | CPE p.1; M19635 p.4 | "Community Plan Exemption Checklist Case No.: 2006.1523E"; "the Transit Center District EIR and the Community Plan Exemption certificate" |
| affordable housing | fee, not on-site; then swapped for a fund payment | M19635 p.19; O137 p.1 | "Pursuant to Planning Code Section 415.5, the Project must pay the Affordable Housing Fee"; "waiving approximately $27,000,000 of affordable housing fees under Planning Code, Sections 413 et seq. and 415 et seq., and requiring Oceanwide Center, LLC, as part of the agreement for the sale of real estate, to pay the equivalent fee amount to the aforementioned Fund" |
| street vacation, sale | about 5,000 sq ft of Jessie St and Elim Alley for $22,619,000 + about $13 million; finally passed July 26, 2016 | O137 pp.1, 18 | "approving and authorizing the sale and quitclaim of City's interest in the approximately 5,000 square foot vacation area for $22,619,000 plus an additional payment to the aforementioned Fund of approximately $13,000,000 for a total of approximately $36,000,000"; "July 26, 2016 Board of Supervisors - FINALLY PASSED Ayes: 10 ... Noes: 1 - Peskin" |
| resolution of intention | Resolution 226-16, June 7, 2016 | O137 p.2 | "On June 7, 2016, the Board of Supervisors adopted Resolution No. 226-16 (the "Resolution of Intention")" |
| site permits | Mission St tower 201510301302 issued 2017-02-01 (first construction document 2017-06-09); First St tower 201510301303 issued 2017-07-05; both still "issued" | DBI(201510301302), DBI(201510301303) | "description": "construct (n) hotel/residential building", "status": "issued", "issued_date": "2017-02-01", "first_construction_document_date": "2017-06-09", "number_of_proposed_stories": "55", "proposed_units": "156.0"; "description": "to erect 60 stories, 4 basement, type ia, 109 units residential, office, retail building", "issued_date": "2017-07-05" |
| demolition | 50 and 62 First complete 2017-10-11; 40 First complete 2018-01-05 | DBI(201604215374), DBI(201604215375), DBI(201604215368) | "to demolish 7 stories, office / retail building." status "complete" 2017-10-11; "to demolish 5 stories office / retail building." complete 2017-10-11; "to demolish 5 stories, office / retail building." complete 2018-01-05 |
| shoring, excavation | CSM shoring walls complete 2018; First St excavation/bracing complete 2019-08-27 | DBI(201611223362), DBI(201703030650), DBI(201708296204) | "cutter soil mix csm shoring/cut off wall for tower 2" complete 2018-08-09; "cutter soil mix (csm) wall for tower 1." complete 2018-11-09; "bracing and excavation for new building approved under pa #2015-1030-1303s" complete 2019-08-27 |
| last inspection | 2020-09-21 under the Mission St tower site permit; none recorded under the First St tower permit | INSP(201510301302); INSP(201510301303) | 39 inspections 2017-07-24 to 2020-09-21; last two: "2020-09-03 REINFORCING STEEL PASSED", "2020-09-21 OK TO POUR, PARTIAL PASSED"; the First St permit returns no inspection rows |
| 2026 status | Zoning Administrator determination: TDRs "previously owned by Oceanwide Center LLC and now owned by Applicant"; record titled "formerly Oceanwide" | `https://data.sf.gov/resource/y673-d69b.json?record_id=2026-004804ZAD` | "project_name": "3708/055 (formerly Oceanwide)", "description": "To document the ownership of certain Transferable Development Rights (TDR) previously owned by Oceanwide Center LLC and now owned by Applicant", "record_status": "Closed - Issued", opened 2026-06-02, closed 2026-08-17 |
| no new application | No Planning project record on the eight lots after 2006.1523 (only records requests, signs and the 2026 ZAD) | `https://data.sf.gov/resource/qvu5-m3a2.json` and `y673-d69b.json` (block 3708) | — (absence; checked 2026-10-12). The neighbouring Golden Gate University site, 536 Mission (lot 098), has its own tower application (2025-007507PRJ), which is a different project. |
| pipeline | The site is not in the Planning Department's current development pipeline dataset | `https://data.sf.gov/d/6jgi-cpb4` | — (absence; 30 Van Ness is listed, Oceanwide's lots are not) |

Stage: **paused**. The official record shows work (2017–2020) and then none; no official document says in so
many words that it stopped, who owns the site now, or whether the 2016 approvals and 2017 permits remain in
force (all in `verify`). A DBI complaint of May 16, 2024 calls it an "abandoned construction site", but that is
a member of the public's wording, not DBI's, so it isn't used.

Boundary: DataSF Parcels (`acdm-wktn`), blklot 3708003, 3708006, 3708007, 3708009, 3708010, 3708011,
3708012, 3708055 (the lots in Motion 19635 and the CPE) plus 3708176 and 3708177, the vacated Jessie Street
and Elim Alley areas (added to the layer July 26, 2016; 3,573 + 1,269 sq ft against the CPE's 4,859 sq ft).
Union about 59,340 sq ft (CPE: 59,445). Lot 008 (82–84 First / 510 Mission) is "Not Part of Project", so
lot 009 (88 First Street) is a separate piece. ODC PDDL. Accuracy: official.

Massing: CPE Figure 2 (level 1, PDF p. 6) and Figure 3 (typical office floor, p. 7) are vector drawings
with the property line in red. Figure 2's corners were matched to 11 parcel vertices (similarity, RMS
0.30 m); Figure 3 to Figure 2 through 7 shared property-line corners (RMS 0.37 pt). Mission Street Tower =
corner-column rectangle in Figure 2 (about 96 x 127 ft; Motion: 133 ft long, 164 ft 11 in diagonal);
First Street Tower = office slab and two cores in Figure 3 (about 35,100 sq ft, which matches about 1.06
million gsf of office over 34 floors). Heights 850 and 605 ft to the roof (Motion 19635). Illustrative;
both at stage `paused`. Note: Motion 19635 gives the First Street Tower's lower-tower average floor size
as 23,505 sq ft, smaller than the traced office floor; the drawn outline follows the figure.

Press-only (kept in `reported`):
- Creditors took over the project in October 2021 after Oceanwide subsidiaries missed payments on $321.5
  million of notes (`https://www.bisnow.com/news/san-francisco/office/creditors-take-over-stalled-2m-sf-oceanwide-center-in-san-francisco-110715`).
- A settlement with the contractors and a foreclosure (2024); a sale to the San Francisco Recovery Fund,
  reported at about $95 million as pending in December 2025
  (`https://www.sfchronicle.com/realestate/article/sf-oceanwide-sale-downtown-21235668.php`) and as closed in
  January 2026 at about $60 million; "Fifty at First", a 915-ft, 56-floor, ~1.5 million sq ft office tower,
  shown in September 2026 with no permits filed
  (`https://sfyimby.com/2026/09/oceanwide-center-no-more-renderings-revealed-for-fifty-at-first-san-francisco.html`).
  The press disagrees on when work stopped (2019 or 2020).

Photo: no openly licensed Commons photo of the site or the pit was found (Commons search for "Oceanwide
Center", "50 First Street San Francisco", Oct 12, 2026; the only hit is an 1901 sketch of a saloon at 50
First Street, `https://commons.wikimedia.org/wiki/File:Bar_of_Saloon_at_50_First_Street_2.png`, public
domain, not useful). Candidate: none.

---

## 30-van-ness

Recommendation: **INCLUDE** (Matthew's call; stage `paused`). One 47-story tower on a 0.88-acre lot;
construction started in 2022 and was halted in 2023; re-approved with lower affordable housing terms in
2024–25.

Documents read:
- O01-25 (Ordinance 01-25, all 13 pp.: findings, Section 249.99, Board history).
- DNX02 (executive summary and draft Motion pp. 1–21; Exhibit A plan sheets skimmed; Ordinance copy pp. 109–121).
- MIN0313 (minutes of March 13, 2025), AG1107 (agenda of Nov 7, 2024), TR240872 (Resolution 21642).
- PKT2020 (executive summary pp. 1–7, draft Motion pp. 8–46, plan sheets pp. 470–500).
- `https://sfbos.org/sites/default/files/lut111824_240872_Notice.pdf` (Land Use Committee notice).
- `https://www.sfbos.org/sites/default/files/o0124-20.pdf`, `https://www.sfbos.org/sites/default/files/o0126-20.pdf` (Hub Plan zoning).
- Board files via the Legistar API: `https://webapi.legistar.com/v1/sfgov/matters/29638` (Ordinance 153-15) and
  `https://webapi.legistar.com/v1/sfgov/matters/31789` (Resolution 95-17); `https://sfgov.legistar.com/LegislationDetail.aspx?ID=2974444&GUID=9094FC64-BA1F-43EF-99C4-181477D6237D`.
- DataSF: permits on 0835/004, DBI inspections, Planning records 2017-008051 and 2024-008290, development pipeline.

| field | official value | source | verbatim quote |
|---|---|---|---|
| lot | 0835/004, 38,123 sq ft, 275 ft on Van Ness, 196 ft on Market, 164 ft on Fell | DNX02 p.7 (draft Motion 21700, finding 3) | "The Project Site (“Site”) is a 38,123 square-foot irregularly-shaped corner lot located on the east side of Van Ness Avenue, between Market Street and Fell Street, with 275’ of frontage along Van Ness Avenue, 196’ of frontage along Market Street, and 164’ of frontage along Fell Street." |
| project (2025) | 47 stories, roof up to 520 ft (540 ft with screening); 722,000 sq ft; 333 homes; 252,905 sq ft office; 6,414 sq ft retail | DNX02 p.7; MIN0313 p.2 | "construction of a 47-story mixed-use building reaching a roof height up to 520 feet tall (540 feet inclusive of rooftop screening/mechanical equipment) that includes approximately 722,000 square feet of Gross Floor Area, containing 333 dwelling units, 252,905 square feet of Office use, and 6,414 square feet of ground floor Retail use." |
| other program | 146 parking + 5 car share; 1,555 sq ft POPOS; unit mix | DNX02 p.7 | "three-below grade levels that would accommodate up to 146 vehicle parking and five car share spaces. The 30 Van Ness Project includes approximately 1,555 square feet of privately-owned public open space (POPOS)"; "21 studio units, 104 one-bedroom units, 161 two-bedroom units, and 47 three-bedroom units" |
| existing building | the 5-story building is altered, not demolished | DNX02 p.7 | "The Project includes a significant alteration to an existing 5-story building containing non-residential uses (already commenced as of July 18, 2022, under the prior approvals)" |
| site now | excavated, initial foundation work | DNX02 p.8 | "Because the Project Sponsor commenced and subsequently halted construction of the 30 Van Ness Project, the Site is currently an excavated construction site, with initial foundation work performed under the First Addendum to the Site Permit." |
| construction start, fees, halt | started July 18, 2022; $41,000,577.28 fees paid March 14, 2023; halted after 16 months | O01-25 p.4 | "Developer commenced construction of the Original Project on July 18, 2022 and paid all development impact fees in connection therewith on March 14, 2023, which impact fees totaled $41,000,577.28. After diligently pursuing construction of the Original Project for 16 months, Developer halted construction due to feasibility concerns." |
| sale | PSA with Lendlease Feb 21, 2017 (Res. 95-17); conveyed to 30 Van Ness Development LLC May 5, 2017 | O01-25 pp.2–3 | "On February 21, 2017, the City and County of San Francisco ("City") and Lendlease Development, Inc. entered into an Agreement for Sale of Real Estate"; "the City conveyed the Property to Developer pursuant to a Grant Deed ... dated May 5, 2017" |
| sale price | $70 million with lease-back | `https://webapi.legistar.com/v1/sfgov/matters/31789` | "Resolution approving a purchase and sale agreement by and between the City and County of San Francisco and Lendlease Development, Inc. for the sale of City-owned property located at 30 Van Ness Avenue for $70,000,000; including a City lease-back"; enacted 2017-03-30 (095-17) |
| 2015 sale authorization | Ordinance 153-15, at least $87 million, enacted Aug 6, 2015 | `https://webapi.legistar.com/v1/sfgov/matters/29638` | "Ordinance authorizing the sale, by public competitive bid, of City-owned property located at 30 Van Ness Avenue for not less than $87,000,000"; MatterEnactmentDate 2015-08-06 |
| 2020 approval | May 21, 2020: Motions 20714, 20717–20719; FEIR Res. 20707; CEQA findings Motion 20708; 25% on-site affordable | O01-25 pp.1–4 | "On May 21, 2020, the Planning Commission adopted Motions No. 20714, 20717, 20718, and 20719, approving the entitlements for the Original Project"; "In accordance with the requirements of the NSR, 25% of the units in the Original Project were to be provided as on-site inclusionary units"; "in Resolution No. 20707, certified the Final Environmental Impact Report for the Hub Plan, 30 Van Ness Avenue Project" |
| podium, tower size (2020) | 9-story podium up to 130 ft; tower 13,200 sq ft footprint; max length 141 ft, diagonal 169 ft 4 in | PKT2020 pp.4, 15, 35 | "The Project would construct a 9-story podium reaching a maximum height of 130’, with a center tower reaching a maximum finished roof height of up to 520’"; "The footprint of the residential tower occupies 13,200 square feet"; "the maximum plan length is 141’ and the maximum diagonal dimension is 169’-4”" |
| tower position | 12 ft from Van Ness line; 40 ft 7 in + 15 ft from Fell line; 141 ft long; lot 164 x 275 ft | PKT2020 p.488 (Typical residential floor plan L13-L15) | dimension strings "164' - 0"", "12' - 0"", "40' - 7"", "LINE OF 115' TOWER SEPARATION SETBACK TO 100 VAN NESS", "15' - 0"", "141' - 0"", "275' - 0"" |
| Hub zoning | Ordinances 124-20 and 126-20 finally passed July 28, 2020 | o0124-20 p.19; o0126-20 | "July 28, 2020 Board of Supervisors - FINALLY PASSED" |
| site permit | 201912139539 issued 2021-08-25; first construction document 2023-03-16; 47 stories, 515 ft 4 in, 348 units | DBI(201912139539) | "(e) walls to remain - (n) high rise bldg w/ appoxi 853,400 gsf/515'-4" tall w/ family/office mixed use type 1 construction ... residences from level 11-47. total 348 units."; "issued_date": "2021-08-25", "first_construction_document_date": "2023-03-16" |
| Nov 2024 changes | Motion 21643 (DPA amendment) and Resolution 21642 (recommend SUD); OFA large-cap request on the same agenda | DNX02 p.2; AG1107 items 15a–c; TR240872 | "On November 7, 2024, the Project was modified by the Commission (Case No. 2024-008290DNX) under Motion No. 21643 to (i) add 18,805 square feet of additional office space (for a total of 252,905 gross square feet) at the second floor, (ii) reduce the retail use area from approximately 21,000 gross square feet to approximately 6,414 gross square feet, and (iii) modify the Project’s inclusionary affordable housing requirements."; "The Modified Project would not change the building envelope approved under the Initial Project" |
| SUD ordinance | Ordinance 01-25, finally passed Jan 28, 2025 | O01-25 p.12 | "January 28, 2025 Board of Supervisors - FINALLY PASSED Ayes: 11" |
| SUD terms | fee 16.4%, on-site 12%, off-site 16.4%; fee credit; sunset May 1, 2029 unless construction recommenced | O01-25 pp.7–11 | "the applicable percentage shall be 17.4%16.4%" (struck/added); "shall be 12.8% 12%"; "(4) May 1, 2029, unless the project subject to this 30 Van Ness Special Use District has recommenced construction before such date" |
| March 2025 | Motion 21700: Condition 8 amended to the SUD; fee path; approved 6–0, one recusal | DNX02 p.2; MIN0313 pp.2–3 | "As modified, the Project would change its method of compliance with the requirements of Planning Code Section 415 through satisfaction of the affordable housing fee in Planning Code Section 415.5, subject to the fee credit provisions in the 30 Van Ness Special Use District."; "ACTION: Approved with Conditions AYES: McGarry, Williams, Braun, Imperial, Moore, So NAYS: None RECUSED: Campbell MOTION: 21700" |
| sponsor | 30 Van Ness Development, LLC | DNX02 p.1 | "Project Sponsor: 30 Van Ness Development, LLC" |
| 2025 permit | added excavation bracing "for extended design live", issued 2025-06-17 | DBI(202208100237) | "rev 202103227002: supplemental level 3 bracing of (e) support of excavation system for extended design live. nc 4.7.25." |
| inspections | site verification visits 2024-01-16 to 2026-08-18; no construction inspections listed under the site permit | INSP(201912139539) | "2024-01-16 SITE VERIFICATION PASSED" ... "2026-08-18 SITE VERIFICATION PASSED" |

Stage: **paused** (Ordinance 01-25: "Developer halted construction"; Motion 21700: "excavated construction
site"). No official record found of construction restarting as of Oct 12, 2026.

Boundary: DataSF Parcels (`acdm-wktn`), blklot 0835004, the whole SUD (Section 249.99(a): "consisting of
Assessor's Parcel Block No. 0835, Lot No. 004"). 38,365 sq ft as mapped (Motion: 38,123). The mapped Van Ness
frontage measures 282.7 ft against the plan's 275 ft. ODC PDDL. Accuracy: official.

Massing: the 130-ft podium on the lot less the tower, and a 141 x 93.6 ft tower (13,200 sq ft / 141 ft) at
520 ft, laid out from PKT2020 p.488's dimensions from the Van Ness / Fell corner of the parcel. The 2024 and
2025 approvals say the envelope is unchanged, so the 2020 plan is still the latest dimensioned geometry (the
2025 Exhibit A plans are construction drawings without clean dimensions). Illustrative, stage `paused`.
Not drawn: the faceted floor plate and the sloped top five floors. Open item: the DBI site permit says
348 units and 515 ft 4 in; the approvals say 333 and 520 ft.

Press-only (kept in `reported`): construction halted in August 2023 "due to market conditions"
(`https://sfyimby.com/2025/03/meeting-tomorrow-for-30-van-ness-avenue-san-francisco.html`).

Photo: candidate `https://commons.wikimedia.org/wiki/File:Overhead_view_of_Market_and_Van_Ness,_April_2022.JPG`
(Pi.1415926535, own work, 1 April 2022, CC BY-SA 4.0 / GFDL): an overhead view of the Market and Van Ness
intersection taken before construction began; its description doesn't name 30 Van Ness, so check by eye
that the corner building is in frame before using it. Not downloaded.
