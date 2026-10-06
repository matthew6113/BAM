# Official-source findings: Esmeralda (Cloverdale)

Checked 2026-10-06 against documents downloaded and read in full text (local copies in `data/raw/official/esmeralda/`, git-ignored). Page numbers are PDF page numbers.

Matthew asked for "the Esmeralda project in Sonoma". There is one match: the **Esmeralda** mixed-use village proposed by Esmeralda Land Company, LP on the former Alexander Valley Resort (AVR) site in the City of Cloverdale, northern Sonoma County. No other development named Esmeralda (or a close spelling) turned up in Sonoma County, Permit Sonoma, the City of Sonoma, Santa Rosa or the other cities, or on CEQAnet. Matthew has already decided to include it, so the size test was skipped. By the map's bar it is small: 605 homes on about 261 acres, under the 1,000-home guide. Draft record: `scratchpad/records/candidates/esmeralda.json`.

URL shorthand:
- CLV = `https://www.cloverdale.net/DocumentCenter/View/` (City of Cloverdale's document center)
- PAGE = `https://www.cloverdale.net/esmeralda` (City's "Esmeralda Project Information" page)
- PCSR = CLV`6998/Agenda-Report` (Planning Commission staff report, Oct 1, 2026, 26 pp.)
- CCSR = `https://cloverdale.granicus.com/services/legistar/download/pdf/4407704/Agenda_Report.pdf` (City Council agenda report, Oct 7, 2026, 23 pp.; linked from the City Council agenda)
- SP = CLV`7035/Draft-Specific-Plan---Revised-92926` (draft Esmeralda Specific Plan, Version 7, Sept 25, 2026, posted as "Revised 9/29/26", 115 pp.)
- ADD = CLV`7006/EIR-Addendum---Revised-92926` (Addendum to the 2009 AVR Final EIR, revised Sept 29, 2026, 348 pp.)
- DA = CLV`7004/Draft-DA---Revised-92826` (draft Second Amended and Restated Development Agreement, revised Sept 28, 2026, 114 pp.)

Hosts not yet in `src/projects/official.ts`:
- `cloverdale.net`: the City of Cloverdale's own site. Its pages are titled "Cloverdale, CA - Official Website"; City agendas carry the letterhead "124 N. Cloverdale Boulevard ... www.cloverdale.net" and post at "www.cloverdale.net/agendacenter" (signed by the City Clerk; e.g. the Oct 7, 2026 agenda). A City Council agenda filed with the Sonoma County Superior Court's Grand Jury responses (`https://sonoma.courts.ca.gov/system/files/grand-jury/gj-response-city-cloverdale-animal-services-sonoma-county.pdf`) gives the same addresses, alongside City staff email at `@ci.cloverdale.ca.us`.
- `cloverdale.granicus.com`: the City's Granicus/Legistar file server. The City Clerk's posted Oct 7, 2026 agenda (`https://www.cloverdale.net/AgendaCenter/ViewFile/Agenda/_10072026-1438`) links its agenda report and attachments there. Only needed for CCSR; PCSR has the same facts on `cloverdale.net`.

With those two hosts added the record passes the record check. The schema already validates; the only failure is "unofficial sources".

---

## esmeralda

Recommendation: **INCLUDE** (Matthew's call; stage `entitlement`). It is below the usual size bar (605 homes, about 57,700 sq ft of non-hotel commercial space, 261 acres), but it is a master-planned, multi-building village in formal hearings with a full set of City documents.

Documents read:
- PAGE: City project page (process, document list, hearing dates), read 2026-10-06.
- PCSR: Planning Commission staff report, Oct 1, 2026.
- CLV`6999/Attachment-1---Resolution`: draft Planning Commission resolution (3 pp.).
- CCSR and the agenda `https://www.cloverdale.net/AgendaCenter/ViewFile/Agenda/_10072026-1438`: City Council special meeting, Oct 7, 2026.
- SP: draft Esmeralda Specific Plan, Version 7.
- ADD: EIR Addendum (sections 1–2, project description and phasing).
- DA: draft development agreement (recitals, pp. 1–9).
- CLV`6948/Esmeralda-Schedule`: City's hearing and ballot timeline (1 p.).
- CLV`6705/CEQA-Summary-Esmeralda`: City's CEQA summary (2 pp.).
- CLV`6704/E2---Processing-Proposed-Esmeralda-Project`: City Attorney presentation to Council, Apr 8, 2026 (10 pp.).
- CLV`6605/Item-E1---Agenda-Reportpdf`: Joint Council and Planning Commission agenda item, Nov 12, 2025 (2 pp.).
- CLV`6624/Adopted-Resolution-No-074-2025---Esmerelda-WSA-WSF`: Resolution 074-2025 adopting the water supply assessment, Dec 10, 2025.
- CEQAnet SCH 2003072142 (`https://ceqanet.lci.ca.gov/2003072142`): the AVR EIR (NOP, 2003).
- County of Sonoma parcel layer (`https://socogis.sonomacounty.ca.gov/map/rest/services/CRAPublic/ParcelsPublicShapeFile/FeatureServer/0`), queried for the 11 APNs.

| field | official value | source | verbatim quote |
|---|---|---|---|
| name, applicant, owner | Esmeralda Specific Plan; applicant Esmeralda Land Company, LP; owner Spight Properties II LLC | PCSR p.1 | "Project: Esmeralda Specific Plan / Esmeralda Alexander Valley Resort (AVR) Plan Applicant: Esmeralda Land Company, LP (ELC) Property owner(s): Spight Properties II LLC" |
| developer entity | Delaware limited partnership | DA p.1 recital | "between ESMERALDA LAND COMPANY, LP, a Delaware limited partnership, (“Developer”)" |
| location, acres | about 261.44 acres, 11 APNs | PCSR p.1 | "Approximately 261.44 acres east of Asti Road and U.S. 101, west of the Russian River, south of Santana Drive, and north of the Cloverdale Municipal Airport." "117-050-010, -011, -012, -017, -024, -026, -027, -028 and -029; 116-310-013 and 116-310-014" |
| why not 266 acres | the unincorporated Panhandle is excluded | PCSR p.2 | "The current Plan Area is smaller than the approximately 266-acre area described in earlier materials because the roughly 4-acre strip referred to as the Panhandle is excluded because it is located in the unincorporated area of the County" |
| map area | 266.84 acres, 45 lots | PCSR p.10 | "Its cover identifies a 45-lot map area totaling 266.84 acres, including a 5.4-acre parcel on which no development is proposed." |
| what it replaces | the approved, unbuilt AVR plan and DA | PCSR p.1–2 | "ELC proposes to replace the approved but unbuilt Alexander Valley Resort (AVR) Specific Plan and Development Agreement (DA) with a mixed-use resort-residential village." |
| site | former sawmill and wood-treatment land, largely vacant; SMART corridor splits it | PCSR p.4 | "The property formerly supported sawmill, wood-processing, wood-preserving and related industrial activities." "An 80-foot-wide Sonoma-Marin Area Rail Transit (SMART) railroad corridor divides the property into western and eastern portions." |
| homes | up to 605: 236 detached, 169 attached, 200 senior | SP p.28 (Table 2-3); PCSR p.5 (Table 1) | "Detached Single-family 236"; "Attached Single-family (Condo or Multi-family Rental) 169"; "Senior Living (Assisted & Independent) 200"; "Total Residential† 605" |
| hotel | 160 rooms (up to 30 hotel-residential) | SP p.28 | "Hotel and/or Attached Hotel-Residential Units†† 160 rooms"; "Up to 30 hotel rooms may be developed as Attached Hotel-Residential Units" |
| other uses | spa 14,000; retail 17,300; office 18,400; light industrial 8,000; preschool 8,000 sq ft; K–6 school up to 200 students and 500-seat amphitheater, each by CUP | SP p.28 | "Spa/Onsen 14,000 sq. ft. Retail (Piazza, outside of Hotel) 17,300 sq. ft. Office/Co-working Space 18,400 sq. ft. Light Industrial/Maker Space 8,000 sq. ft." "Preschool/Daycare 8,000 sq. ft. K-6 School Facilities, subject to CUP Up to 200 Students Outdoor Amphitheater, subject to CUP Up to 500 seats" |
| hotel floor area | not capped | SP p.28 | "The maximum floor area for the Resort-Hotel is not specified but would be limited by building height, FAR, other development standards, and CEQA mitigations." |
| open space | about 162 acres publicly accessible; 4.75-acre public sports park | SP p.37; PCSR p.12; DA p.9 | "Approximately 162 acres of the Site will become PAOS." "It also proposes to dedicate a 4.75-acre Public Sports Park at Asti Road and Santana Drive" |
| affordable housing | in-lieu fee, about $2.9 million; no on-site affordable units | PCSR p.16 | "The Developer must pay an inclusionary housing fee in lieu of providing on-site affordable units. If all residential units are built, the amount of the fee will be approximately $2.9 million, subject to inflationary increases." |
| hotel-first rule | 100 home permits before the hotel (80+ rooms) and sports park; 9-year hotel deadline | PCSR p.5 | "building permits for no more than 100 residential units may be issued before both a certificate of occupancy for a resort-hotel with at least 80 guest rooms and construction and dedication of the Public Sports Park." "If the hotel is not completed within 9 years, the City may terminate the DA." |
| heights | VMU 35 ft; VH 35 ft residential, 50 ft other; VR-1/VR-2 35 ft; VR-3 to VR-5 25 ft; open space 15 ft; airport limits override | SP p.26 (Table 2-2); PCSR p.6 (Table 2) | "Village Residential: VR-1 / VR-2 4–20 1.0 35 feet"; "Village Residential: VR-3 / VR-4 / VR-5 4–15 0.75 25 feet"; "Village Hospitality 5 0.3 Residential: 35 feet Other uses: 50 feet" |
| where building goes | west of the SMART corridor; east side mostly open space | PCSR p.4 | "Development would be concentrated west of the SMART corridor. The eastern portion would primarily contain recreation, conservation and trails, but also includes an optional VR-5A/VR-5B housing area" |
| CEQA | addendum to the certified 2009 AVR Final EIR (SCH 2003072142) | PCSR p.1 | "September 8, 2026, Addendum to the certified 2009 Alexander Valley Resort Final EIR (SCH No. 2003072142)" |
| phasing | eight phases, 2027–2036 (CEQA scenario); ~12 years after vesting (developer estimate); DA term 20 years | PCSR p.12; ADD | "The Addendum analyzes an eight-phase construction scenario beginning with Phase 0 and extending from 2027 to 2036. The Specific Plan describes the developer’s estimate of eight phases over approximately 12 years after vesting." "The proposed DA has a 20 year term." |
| earlier approvals | 2009 FEIR (Res. 028-2009), AVR SP (Res. 029-2009), SP-1 prezoning (Ord. 671-2009); LAFCO annexation Apr 7, 2010; 2016 addendum and DA (Ord. 704-2016, Feb 9, 2016); 2018 addendum and amended DA (Ord. 726-2018, Nov 13, 2018) | DA pp.1–3 recitals; PCSR p.2 | "On April 7, 2010, the Sonoma County Local Agency Formation Commission approved ... the annexation of the Property into the City"; "Approved an Amended and Restated Development Agreement between the City and Spight Properties II, LLC, by Ordinance No. 726-2018 (the “2018 DA”)." "The 2018 amended and restated DA expires in 2033" |
| old project size | AVR NOP: 267 acres, 100–150-room hotel, golf course, ~140 + ~25 homes, 60–70 resort units | CEQAnet 2003072142 | "Total Acres 267"; "A 100-150 room resort hotel"; "Approximately 140 single family detached homes" |
| existing entitlement (City summary) | hotel, spa, golf; over 100,000 sq ft commercial; up to 235 homes | CLV`6704` p.2 | "Existing approved project allows for a hotel, spa, and private golf course; over 100,000 SF of commercial uses; and a residential community with up to 235 low-density units" |
| water supply | WSA/WSV adopted Dec 10, 2025, 4–1 | Resolution 074-2025 | "adopted by the City Council of the City of Cloverdale at a regular meeting held on December 10, 2025"; "Ayes: (4) ... Noes: (1) Councilmember Morgenstern" |
| airport | ALUC consistency finding Mar 9, 2026 | PCSR p.2–3 | "On March 9, 2026, the Sonoma County Airport Land Use Commission (ALUC) reviewed the draft Esmeralda Specific Plan and associated SP-2 zoning and unanimously found them consistent with the Cloverdale Comprehensive Airport Land Use Plan (CALUP)." |
| public process | joint meeting Nov 12, 2025; town hall Feb 5, 2026; Council on processing Apr 8, 2026 | PCSR p.23 | "Public review has included a joint City Council/Planning Commission meeting on November 12, 2025, a February 5, 2026 town hall, and City Council consideration of project processing on April 8, 2026." |
| stage | PC hearing Oct 1, 2026; Council Oct 7 (first reading) and Oct 14 | PAGE; CCSR p.1 | "The Planning Commission will consider the project at a public hearing at the Cloverdale Vets’ Hall on Thursday October 1 at 6:00 p.m. ... The City Council will hold two hearings on the project, on Wednesday October 7 ... and October 14" ; "If the first reading is approved, a second reading of the ordinances will occur on October 14." |
| PC outcome | not yet posted | CCSR p.18 (section E.3) | "This staff report will be updated on Monday October 5 to include a summary of the Planning Commission meeting and recommendation." (No update or minutes found on 2026-10-06.) |
| possible vote | Council may send approvals to voters; earliest election Mar 9, 2027 | CLV`6948` | "City Council can provide direction to staff to prepare a resolution to submit the project to voters"; "Election March 9, 2027 or later" |
| ownership note | Nov 2025 summary says ELC acquired the property (conflicts with PCSR's owner line) | CLV`6605` p.1 | "Esmeralda Land Company (ELC) has since acquired the property and is proposing a revised master plan known as the Esmeralda Project" |

Superseded figures: the Nov 2025 and Apr 2026 City summaries describe 200 hotel rooms, 405 market-rate plus 200 senior homes, about 22,000 sq ft retail, 17,500 sq ft office and 168 acres of open space. The current draft (SP Version 7 and PCSR) has 160 rooms, 605 homes, 17,300 sq ft retail, 18,400 sq ft office and about 162 acres. Use the current figures.

Approvals: none yet for Esmeralda. The City adopted the water supply assessment (Res. 074-2025) and the ALUC found the plan consistent; the entitlements (GPA, specific plan, SP-2 zoning, ODS, DA, addendum) await Council action on Oct 7 and Oct 14, 2026.

Boundary lead:
- County of Sonoma parcel layer, `https://socogis.sonomacounty.ca.gov/map/rest/services/CRAPublic/ParcelsPublicShapeFile/FeatureServer/0`, filter `APN IN ('117-050-010','117-050-011','117-050-012','117-050-017','117-050-024','117-050-026','117-050-027','117-050-028','117-050-029','116-310-013','116-310-014')`. All 11 return (POCity Cloverdale), totalling 256.83 assessor acres (`LndSzAcre`), against 261.44 Plan Area acres. License CC BY-SA 3.0; attribution "County of Sonoma" (from the layer's copyright text). Parcel centroids run from about 38.780–38.791 N, 122.995–123.007 W; CEQAnet's point is 38°47'6"N 123°0'9"W.
- Check it against SP Figure 1-5 "Project Site and Potential SMART Path Connection" (PDF p.11) and ADD Exhibit 3 "Site Assessor's Parcel Map" (PDF p.23). The Plan Area excludes the SMART right-of-way (it may or may not be its own parcel) and the ~4-acre Panhandle; label it "Approximate boundary".
- No City of Cloverdale GIS layer for the SP-1/SP-2 district was found.

Massing lead: SP Figure 2-1 "Land Use Districts" (PDF p.22) maps the districts; Table 2-2 (PDF p.26) gives heights (35 ft VMU and VR-1/VR-2, 25 ft VR-3 to VR-5, 50 ft for non-residential in VH, 15 ft in open space, all subject to the Airport Safety Zones and FAA Part 77 overlays, Figures 2-3 and 2-5). The illustrative site plan is Figure 1-2 (PDF p.8); ADD Exhibit 5a (PDF p.43) is the land-use map used in CEQA. The draft master tentative map (CLV`7048`, DA Exhibit L) gives the parcel layout. Draw as "Illustrative massing".

Press or non-official only (kept in `reported`):
- Press Democrat, Feb 9, 2026: principals Devon Zuegel and Michael Yarne; 19 Bay Area families invest; Esmeralda Land Co. "intends to close on the purchase once we secure approvals"; homes from $600,000 to $4 million; about 1,500 residents. `https://www.pressdemocrat.com/2026/02/09/cloverdale-esmeralda-development-housing-resort/`
- California Planning & Development Report: Zuegel founded Esmeralda Land Company; the company holds "an option" on the property. `https://www.cp-dr.com/post/sonoma-development-hopes-to-break-california-s-new-urbanist-drought`
- Other coverage (not used): SF Chronicle, KRON4, The Real Deal, The Registry, Patch; the developer's own site `esmeralda.org`.
