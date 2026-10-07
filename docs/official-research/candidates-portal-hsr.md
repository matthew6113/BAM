# Candidate projects: The Portal (Downtown Rail Extension) and California High-Speed Rail, San Francisco to San Jose

Checked 2026-10-07 against official records read in full text. Local copies are in `data/raw/official/the-portal/` and `data/raw/official/cahsr-sf-sj/` (git-ignored). Page numbers are PDF page numbers; the printed page is given where it differs. Draft records: `scratchpad/records/new/the-portal.json` and `scratchpad/records/new/cahsr-sf-sj.json` (both pass `tests/record-check.test.ts`).

These are the map's first linear transit projects. Both should be drawn as a line with station points, not as buildings or a site boundary.

Shorthand:
- TJ = `https://www.tjpa.org` (Transbay Joint Powers Authority)
- MSR = TJ`/media/40591?inline=` (TJPA, The Portal Monthly Status Report, September 2026, 30 pp.; Board item 11, Oct 8, 2026)
- PMOC = TJ`/media/40552/download?inline` (FTA Project Management Oversight Contractor, Monthly Monitoring Report, July 2026, 65 pp.; posted by TJPA)
- TFS = TJ`/media/40136/download?inline` (TJPA, "The Portal to San Francisco's Future" fact sheet, July 2025, 2 pp.)
- FTA26 = TJ`/media/40503/download` (FTA Region IX letter, environmental re-evaluation concurrence, Aug 26, 2026, 2 pp.)
- SEIS = TJ`/uploads/2015/12/Vol-1-TJPA-Final-SEIS-EIR_11-18.pdf` (Final Supplemental EIS/EIR, Vol. 1, Nov 2018, 493 pp.)
- SFCTA = `https://www.sfcta.org/sites/default/files/2026-01/SFCTA_CAC_Item9_TJPAPortalProjectFiscalYear2026MEMO_2026-01-28.pdf` (SFCTA memo, Jan 23, 2026, for Board Feb 10, 2026, 46 pp.)
- HSR = `https://hsr.ca.gov/wp-content/uploads/`
- BP26 = HSR`2026/06/2026-Final-Business-Plan-060126-A11Y.pdf` (2026 Business Plan, released June 1, 2026, 137 pp.)
- FEIS-FS = HSR`2022/05/Final_EIRS_FJ_V1-03_Fact_Sheet.pdf` (SF–SJ Final EIR/EIS Fact Sheet, June 2022)
- RES = HSR`2022/08/FJ-CEQA-Approval-Resolution-final-A11Y.pdf` (Resolution HSRA 22-20, Aug 17, 2022)
- ROD = HSR`2022/10/FJ-Final-ROD-Combined-A11Y.pdf` (Final Record of Decision, Sept 2022 cover, signed Oct 14, 2022, 528 pp.)
- NCFS = HSR`2026/09/Northern-California-At-a-Glance-Factsheet-A11Y.pdf` (Northern California at a Glance, map dated 09/16/2026)
- NCP = `https://hsr.ca.gov/project-overview/project-sections/northern-california/` (Authority's Northern California page)
- FJP = `https://hsr.ca.gov/high-speed-rail-in-california/project-sections/san-francisco-to-san-jose/` (SF–SJ environmental documents page)
- AGO = `https://services3.arcgis.com/rGGp0aiv6Rf11t2H/arcgis/rest/services/` (the Authority's ArcGIS Online organisation, owner `GeoPlatform_CHSRA`, portal `chsra.maps.arcgis.com`)

Access notes:
- hsr.ca.gov sits behind an Incapsula bot challenge; curl gets a 212-byte stub. A headless Chromium session that navigates to each page or PDF gets through (`scratchpad/bin/nav2.cjs`, Playwright from `node_modules`). The WordPress media API (`/wp-json/wp/v2/media?search=…`) lists current uploads.
- The fact sheet URL given as a lead (`HSR2025/10/2025-10-08_Factsheet_Northern_California_V11_A11Y_MD.pdf`) now returns 404. It has been replaced by NCFS (Sept 2026).
- `www.transit.dot.gov` returns 403 from the proxy, so FTA's Annual Report on Funding Recommendations wasn't read. The CIG figures here come from TJPA, SFCTA and the PMOC report.

Hosts:
- Added to `src/projects/official.ts`: `tjpa.org` (Transbay Joint Powers Authority, lead agency for The Portal and operator of the Salesforce Transit Center; its Board meets at SF City Hall) and `sfcta.org` (San Francisco County Transportation Authority).
- Already accepted: `hsr.ca.gov` (`.gov`) and `ceqanet.lci.ca.gov`.
- Not added: `services3.arcgis.com/rGGp0aiv6Rf11t2H/` (CHSRA's ArcGIS org). Its terms restrict redistribution (see geometry below), so it isn't cited as a record source. Add it as an `OFFICIAL_PREFIXES` entry only if the Authority grants permission. `geo.cloudhsr.com` (the Authority's Experience Builder app, linked from NCP) only points to it.

| candidate | recommendation | why |
|---|---|---|
| The Portal (DTX) | INCLUDE | A megaproject in its own right: an $8.255 billion budget (2025 estimate $7.57 billion), a 1.3-mile tunnel, two stations and the fit-out of the Salesforce Transit Center train box. It has a $3.38 billion FTA New Starts share and is in FTA's Engineering phase. It completes the Transbay Program, whose redevelopment area is already on the map's doorstep, and is the region's top rail capital priority (MTC "Level 1"). Stage `entitled`: environmentally cleared and 30% designed, with no construction or full funding yet. |
| California High-Speed Rail, SF to San Jose | INCLUDE (with caveats) | The Bay Area end of the state's largest infrastructure project. As a Bay Area project it is modest: shared ("blended") use of Caltrain's corridor, about 17.4 miles of track modifications, a maintenance facility in Brisbane and three station upgrades. The Final EIR/EIS put it at $5.3 billion (2021 dollars) and the 2026 Business Plan's reduced scope at $1.27 billion. It passes the "regionally significant" bar, but it is a line on existing tracks with no near-term construction. Draw it quietly, since much of the line is already Caltrain. If Matthew wants only projects that will physically transform a place, fold it into The Portal's panel instead. Stage `entitled`. |

---

## the-portal (The Portal / Downtown Rail Extension)

Documents read:
- TJ`/portaldtx`, `/portaldtx/about-portal`, `/portaldtx/frequently-asked-questions`, `/portaldtx/environmental-review`, `/portaldtx/project-schedule`, `/portaldtx/project-benefits` (read 2026-10-07)
- MSR (Sept 2026); PMOC (July 2026; May 2026 also downloaded); TFS; FTA26
- TJPA Board agenda, Oct 8, 2026 (TJ`/media/40582/download?inline`); minutes of Sept 10, 2026 (downloaded)
- SEIS Vol. 1 (Ch. 2) and Vol. 2 App. A Part 1 (downloaded)
- SFCTA memo (Jan 2026)
- CEQAnet SCH 1995063004 (`https://ceqanet.lci.ca.gov/Project/1995063004`): 17 documents, including the 2018 FIN and NOD and a 2023 CTC NOD (`/1995063004/17`)

| field | official value | source | verbatim quote |
|---|---|---|---|
| what it is | extends Caltrain and later HSR from Fourth and King to the Salesforce Transit Center | TJ`/portaldtx/about-portal` | "will extend Caltrain service from Fourth and King Streets and deliver the California High-Speed Rail Authority's future high-speed rail service to the multimodal Salesforce Transit Center" |
| official name | Transbay Downtown Rail Extension Project, Phase 2 | MSR p.7 (printed 4) | "Transbay Downtown Rail Extension Project, Phase 2, referred to as “The Portal,”" |
| lead agency | TJPA, with five partner agencies under the Implementation MOU | SFCTA p.2 | "TJPA is the lead agency for The Portal, with responsibility for the development, environmental clearance, design, procurement, construction, and commissioning of the project." |
| partners | MTC, SFCTA, Caltrain, CHSRA, City and County of SF | MSR p.4 (printed 1) | "Metropolitan Transportation Commission (MTC), San Francisco County Transportation Authority (SFCTA), Peninsula Corridor Joint Powers Board (Caltrain), California High-Speed Rail Authority (CHSRA), and the City and County of San Francisco (City)" |
| length | 1.3-mile tunnel; 2.2 miles total construction | TJ`/portaldtx/frequently-asked-questions`; MSR p.7 | "The project consists of 1.3 miles of tunnel that will connect two new rail stations"; "The total project length is 2.2 miles" |
| older lengths (superseded) | 2.7 mi with turnback, 2 mi without (2018) | SEIS p.89 | "The total project length is 2.7 miles from the end of the turnback track at Mariposa Street ... the project length is 2 miles from the western end of the Caltrain railyard to the eastern end of the train box. ... The 1.3 miles is the length of the DTX from the Fourth and King Station to the Transit Center." |
| route and method | under Townsend and Second Streets; cut-and-cover and mined | TJ`/portaldtx/about-portal` | "The Portal will be constructed principally below grade using cut-and-cover and mined tunneling methods underneath Townsend and Second Streets." |
| Fourth and Townsend station | 2 tracks, center platform and 2 side platforms | TJ`/portaldtx/about-portal` | "The platform level will feature two tracks, a center platform and two side platforms." |
| Transit Center station | 6 tracks, 3 center platforms (existing two-level train box) | TJ`/portaldtx/about-portal` | "On the platform level, two levels below ground, six tracks and three center platforms will serve commuter and high-speed trains." |
| 2026 scope changes | no intercity bus facility, no train box extension, no HSR platforms at Fourth and Townsend, stub box 750 ft shorter, 171 Second St acquired | FTA26 p.1 | "Modify the Fourth and Townsend Street Station design by eliminating high-speed train platforms and concourse-level facilities." "Shorten the tunnel stub box by approximately 750 feet." |
| CEQA | 2018 Final SEIS/EIR certified Dec 2018; Addendum 1 Jan 12, 2023; Addendum 2 Mar 12, 2026 (NOD filed Mar 18) | TJ`/portaldtx/environmental-review`; MSR p.6 | "In December 2018, the TJPA certified the Final Supplemental EIS/EIR." "Addendum 2 ... Adopted on March 12, 2026." "The TJPA filed the Notice of Determination on March 18, 2026." |
| NEPA | 2005 ROD; Amended ROD July 2019; re-evaluation concurrences June 9, 2023 and Aug 26, 2026 | PMOC p.4; FTA26 p.1–2 | "the National Environmental Policy Act (NEPA) action was completed in February 2005 with a Record of Decision (ROD). The Federal Transit Administration (FTA) amended the ROD in July 2019"; "The FTA finds that the changes described in the submitted materials would not result in significant environmental impacts that were not previously evaluated" |
| FTA CIG | Project Development Dec 2021; Engineering May 3, 2024; CIG share $3.38 billion | PMOC p.4; SFCTA p.1 | "The FTA notified TJPA on May 3, 2024, that Transbay DTX had been approved to enter the New Starts Engineering phase." "FTA established the project’s CIG funding share of $3.38 billion." |
| budget | $8.255 billion (2023 estimate, incl. train box) | MSR p.5 (printed 2) | "The project budget remains $8.255 billion, based on the 2023 capital cost estimate submitted at Entry into Engineering." |
| updated estimate | about $7.572 billion; $683 million kept as contingency | MSR p.5 | "The updated estimate is approximately $7.572 billion, including revised contingency requirements. The approximately $683 million difference has been retained in unallocated contingency" |
| cost excluding train box | $7.52 billion (2023), $6.84 billion (2025) | SFCTA p.3 | "excluding the already completed trainbox, project costs were estimated at $7.52 billion." "This indicative estimate of $7.57 billion ($6.84 billion excluding the completed trainbox)" |
| funding plan (July 2026) | committed non-CIG $1,304M; CIG $3,384M; planned state $1,303M; other planned $265M; train box $729M; gap $587M; total $7,572M | MSR p.22 (Table 3) | "Committed/Budgeted (non-Capital Investment Grant (CIG)) $1,304"; "FTA Capital Investment Grant (CIG) $3,384"; "Planned State $1,303"; "Funding Gap – To be Planned $587"; "July 2025 Project Cost $7,572" |
| gap (other counts) | $2,131M (July 2025); about $2.2B (Jan 2026) | TFS p.1; SFCTA p.3 | "leaving a remaining funding gap of $2,131 million"; "the project’s remaining funding need is approximately $2.2 billion" |
| state ask | TIRCP Cycle 8 application for $750M, May 18, 2026; awards slipped to Oct 2026 | MSR p.22 | "Applied for $750 million from Cycle 8 of the Cap-and-Invest Program’s Transit and Intercity Rail Capital Program (TIRCP) on May 18, 2026. Award announcements, expected in September 2026, have been delayed to October 2026." |
| AB 2308 | signed Sept 30, 2026 (tax increment +25 years past 2050) | MSR p.22 | "a legislative bill to extend the net tax increment ... by 25 years from the currently scheduled sunset year of 2050. The bill was approved by the legislature on August 26 and was signed by the Governor on September 30, 2026." |
| design | 30% tunnel/stations; 60% enabling works | MSR p.6, p.10 | "The design documents for enabling works—utility relocation and Fourth and King railyards site clearing—are at the 60% level" ; "40-CT Civil and Tunnel 30% complete" |
| procurement | 40-CT progressive design-build RFP Dec 2025; proposals due Oct 9, 2026; highest-scoring proposer Nov 6, 2026; award Feb 11, 2027 | MSR p.6, p.11 | "The 40-CT Civil and Tunnel progressive design-build (PDB) request for proposals (RFP) was issued in December 2025. ... proposals due on October 9, 2026." "40-CT Notification of highest-scoring proposer Nov 6, 2026"; "40-CT Award PDB contract Feb 11, 2027" |
| FFGA | target July 2027 | MSR p.10 | "Target FFGA execution July 2027" |
| opening | ready for service Nov 17, 2036 (forecast) | MSR p.9 | "The forecast target ready-for-service date of November 17, 2036, remains unchanged from the previous reporting period." |
| opening (older) | 2035 "funding dependent"; originally June 2035 | TJ`/portaldtx`; MSR p.19 | "anticipated revenue service date of 2035, funding dependent"; "The RSD was originally intended to be reached in June 2035." |
| first construction | utility relocation in 2028 | MSR p.29 | "in preparation for utility relocation construction in 2028" |
| ridership | over 125,000 average daily riders | TFS p.1 | "will activate downtown with over 125,000 average daily riders" |
| SFCTA role | largest Prop L investment, $300M programmed; $12.5M allocated FY2025/26 | SFCTA p.5; p.1 | "The Portal is the largest single investment in the Prop L program, with $300 million programmed to the project" |
| real estate | Tranche 1 of 4: five parcels; four appraisals done | MSR p.24 | "The acquisition process for five parcels (Tranche 1) continues. Appraisals of the required property interests are underway; four have been completed." |

Conflicts and open items (in the record's `verify`):
- Opening: 2035 (TJPA web page and TFS) vs Nov 17, 2036 (MSR, forecast) vs July 16, 2036 target and June 27, 2035 risk-based FFGA date (PMOC p.6). SFCTA says "start of Caltrain service on the project in 2036" (p.2). Use the MSR forecast and say it's a forecast.
- Cost: say "$8.3 billion budget" (MSR), with $7.57 billion as the updated estimate. Press figures of "$8.25B" (2023) and "$7.57B" are both official at different dates.
- Funding gap: three official figures ($2,131M, ~$2.2B, $587M) count planned state money differently. Don't show a single gap without saying what it excludes.
- Proposal due date: MSR p.6 says Oct 9, 2026; MSR p.11 lookahead says Sept 25, 2026.
- CHSRA's $550 million: BP26 p.44 (printed 16) says the Authority "remains committed to securing at least $550 million", while MSR p.18 says "the TJPA will need to recommence conversations with CHSRA regarding its funding commitment".

Geometry (the map must draw a line):
- SEIS Vol. 1 figures: Fig. 2-2 alignment (p.91), Fig. 2-6 project components (p.105), Fig. 2-9a Fourth and Townsend plan and profile (p.108), Fig. 2-12a tunnel stub box (traced from the 2018 design; the stub box is now 750 ft shorter), Fig. 2-21 construction methods by location (p.136). SEIS Vol. 2 App. A (TJ`/uploads/2018/11/Vol-2-TJPA-Final-SEIS-EIR-App-A-Part-1_11-18.pdf`) is downloaded but not yet checked for plan sheets.
- MSR Figure 1 "The Portal Alignment and Major Components" (p.7): the current scope, as a schematic.
- CHSRA GIS: AGO`HSR_Statewide_Alignment/FeatureServer/1`, feature `Section = 'DTX'` (LineString, 1.33 mi measured, from -122.39416, 37.79133 to -122.39487, 37.77642), and the same line in AGO`Alignment_Hybrid_Feb_8_2024/FeatureServer/4`. **Licence:** the item "HSR Statewide Alignment and Stations" (`7210a9f57f16407f8fdd4949ac90daea`) says "These data are not to be redistributed without the express approval from California High Speed Rail Authority." Use it only to check a trace unless the Authority grants permission. Local copy: `data/raw/official/cahsr-sf-sj/statewide-align-FJ-DTX-JY.geojson`.
- No TJPA, DataSF or SF Planning GIS layer for the alignment was found (DataSF catalog search: none).
- CEQAnet's 2018 point (37°47'10.87"N 122°23'51.82"W) is at the Transit Center, not the line's center.

Press or non-official only: none used. Press coverage (ABC7 on the $3.4B federal share) matches the official figures. A search summary claimed "Ready for Service targeted for 2034"; no official document says so, and it isn't used.

---

## cahsr-sf-sj (California High-Speed Rail, San Francisco to San Jose)

Documents read:
- FJP (document list, approvals) and NCP (read 2026-10-07)
- FEIS-FS; Final EIR/EIS Summary (downloaded); RES; Resolution 22-19/22-21 links; ROD (opening section, conclusion and signature)
- Exhibit A map (HSR`2022/08/22-19_FJ_CEQA_Approval_Resolution_Exhibit_A_Map.pdf`)
- BP26 (statutory table, Ch. 2 SF-B and Phase 1 scenarios, Ch. 3 funding, App. B cost tables, App. D schedules); OIG review of the 2026 Business Plan (HSR`2026/07/OIG-HSR-Review-of-2026-Business-Plan-A11Y.pdf`; nothing specific to SF–SJ)
- NCFS; Overview fact sheet (July 2026)
- AGO services: `NORCAL_LAYERS`, `HSR_Statewide_Alignment`, `Alignment_Hybrid_Feb_8_2024`

| field | official value | source | verbatim quote |
|---|---|---|---|
| section | SF to San Jose: ~43–49 mi blended with Caltrain, up to 6 mi dedicated (by alternative) | FEIS-FS p.1 | "The Project Section would include approximately 43 to 49 miles of blended1 system infrastructure with Caltrain and up to 6 miles of dedicated HSR infrastructure (depending on the alternative and viaduct option)" |
| stations | 4th and King (interim), Millbrae, San Jose Diridon; SFTC via the Portal | FEIS-FS p.1 | "HSR trains would stop at the 4th and King Street Station in San Francisco (an interim station until completion of the Downtown Rail Extension Project), the Millbrae Bay Area Rapid Transit/Caltrain Intermodal Station, and the San Jose Diridon Station." |
| Alt A scope | 48.9 mi existing track; 17.4 mi modified; East Brisbane LMF; 40 crossings; 8.8 mi fencing; 21 radio towers | FEIS-FS p.2 (Table 1), p.4 | "Length of existing Caltrain track (miles)2 48.9"; "would modify approximately 17.4 miles of existing Caltrain track, predominantly within the existing Caltrain right-of-way, build the East Brisbane LMF, modify eight existing stations or platforms" |
| FEIS cost | $5,317 million (2021 $) | FEIS-FS p.4 | "The Preferred Alternative is estimated to cost approximately $5,317 million (in 2021 dollars)" |
| lead agency | CHSRA (CEQA, and NEPA under FRA assignment) | FEIS-FS p.4 | "Pursuant to the MOU, the Authority is the federal lead agency." |
| approval | Alt A, 4th and King to Scott Blvd; vote 8–0, 8/17/2022 | RES pp.1–4 | "Approval of the Portion of the Preferred Alternative ... from 4th and King Streets in San Francisco to Scott Boulevard in Santa Clara"; "Vote: 8-0"; "Date: 8/17/2022" |
| Scott Blvd–Diridon | approved with San Jose–Merced, Apr 28, 2022 (Res. 22-10, 22-11) | RES p.1 | "the Authority Board of Directors approved the portion of the Preferred Alternative from Scott Boulevard in Santa Clara to West Alma Avenue in San Jose, including the San Jose Diridon Station, as part of the San Jose to Merced Project Section on April 28, 2022, through Resolution #HSRA 22-11" |
| ROD | signed Oct 14, 2022; FEIR/EIS dated June 10, 2022 | ROD p.8, p.48 | "Final Environmental Impact Report (EIR)/Environmental Impact Statement (EIS) (Final EIR/EIS) dated June 10, 2022"; "Brian P. Kelly October 14, 2022" |
| certification date (web) | Aug 18, 2022 | NCP | "On August 18, 2022, the Authority Board of Directors certified the Final EIR/EIS for the San Francisco to San José project section." |
| NorCal status | 159 mi SF–Merced cleared; eligible for advanced design | NCFS p.1 | "The full 159-mile segment between San Francisco and Merced has obtained environmental clearance and is eligible to begin advanced design." |
| 2026 plan | SF–Bakersfield via shared corridors; 4th and King interim; $61.2B by 2039 | BP26 p.44 (printed 16) | "In San Francisco, the existing 4th and King Street station can serve as the interim northern terminus, until the Portal ... is complete"; "A total of $61.2 billion in capital investments is needed to deliver SF-B by 2039." |
| 2026 plan release | final released June 1, 2026 | BP26 p.4 (printed IV) | "The Authority's final business plan was released June 1, 2026" |
| SF–Gilroy cost | $1,273M (SF-B); 2025 PUR $593M; 2024 BP $15,140M | BP26 p.76–77 (printed 48–49), Tables B.2, B.4 | "San Francisco to Gilroy Blended Approach3 593 1,273"; "Cost for the San Jose to Gilroy segment is not included. Estimates for this shared benefit project range from $2 billion to $5 billion." |
| Portal money | at least $550M committed; not in Phase 1 costs | BP26 p.44 | "While funding for the Portal is not included in the optimized Phase 1 capital costs, the Authority remains committed to securing at least $550 million in additional funding" |
| bookend spend | Caltrain electrification $714M | BP26 p.60 (printed 32); NCFS p.2 | "Caltrain Electrification: $714 million from the Authority leveraged with other funds"; "for the electrification of 51 miles of track between San Francisco and San José" |
| schedule | SF–SJ right-of-way, utility design, 4th and King, Millbrae, San Jose stations: not started | BP26 p.108 (printed 80), Exhibit D.1 | "San Francisco to San Jose ... Right-of-Way NOT STARTED ... 4th & King Station NOT STARTED ... Millbrae Station NOT STARTED San Jose Station NOT STARTED" |
| SF-B service | up to 18 trains daily; 12.21–14.2M riders (2040) | BP26 p.44 | "The service will include up to 18 trains daily"; "the expected ridership is between 12.21million and 14.2 million riders annually" |

San Jose to Merced (brief; mostly outside the Bay Area): certified Apr 28, 2022 (NCP; RES p.1), ROD dated June 1, 2022 (ROD p.8). Its only Bay Area station is Downtown Gilroy (Santa Clara County; AGO station layer "Downtown Gilroy Station, W 8th St and Monterey St"). BP26 estimates Gilroy to the Central Valley Wye (Pacheco Pass) at $18,619M (SF-B, Table B.2) and San Jose to Gilroy at $2–5B as a shared-benefit project ($2,033M in Table B.5). Schedule: not started (Exhibit D.1). Not recommended as a separate map record. Mention Gilroy in this record's panel instead.

Conflicts and open items:
- Certification date: 8/17/2022 (resolution) vs Aug 18, 2022 (NCP). The Board met Aug 17–18. Use Aug 17, the date on the resolution.
- The ROD's cover says "September 2022", but it was signed Oct 14, 2022.
- Cost: $5,317M (2021 $, full Alt A) vs $1,273M (2026 BP, reduced early scope, YOE) vs $15,140M (2024 BP "San Francisco to Gilroy"). They describe different scopes; don't present them as a change in one number.
- Press: a search summary gave "$60.34 billion" for SF–Bakersfield by 2039. That's the Feb 2026 draft plan; the final says $61.2 billion. KALW (June 3, 2026) headlined that the plan was "approved" with service by 2033. That date is the Merced–Bakersfield segment, not the Bay Area, and the Board adoption date wasn't confirmed in an official record read here.

Geometry:
- Final EIR/EIS Volume 3 (FJP): Books A-1 and A-2 "Composite Plan, Profile, and Typical Sections", A-3 "Stations", A-4 "Structures, Roadway, Light Maintenance Facility, and Alignment Data Table" (HSR`2022/05/Final_EIRS_FJ_V3-04_Alternative-A_Book_A1.pdf` to `…V3-07…A4.pdf`; not downloaded, large). The A-4 alignment data table may allow an exact centreline.
- RES Exhibit A map (2 pp., downloaded): the approved extent, 4th and King to Scott Blvd.
- CHSRA GIS (AGO): `HSR_Statewide_Alignment/FeatureServer/1` `Section='F-J'` (42.78 mi measured, 4th and King to Scott Blvd), layer 0 stations (Transbay Transit Center, 4th & King, Millbrae (SFO), San Jose Diridon, Downtown Gilroy with lat/long); `Alignment_Hybrid_Feb_8_2024/FeatureServer/4` "San Francisco to San Jose" (MultiLineString, 49.0 mi measured, to Diridon); `NORCAL_LAYERS/FeatureServer/1` "Preliminary Design Footprint" (polygons by `feattype`/`subsection`, Alternative A, last edited Aug 2024) and layer 0 parcels. **Same redistribution restriction as above.** The service description reads: "This map service shows the approved alignments for the Northern California portion of the California High Speed Rail including stations at San Francisco, Millbrae, San Jose, and Gilroy." Local copies in `data/raw/official/cahsr-sf-sj/*.geojson` (for checking only).
- Open alternative: U.S. DOT/BTS NTAD "North American Rail Network Lines – Passenger Rail" (`https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_North_American_Rail_Network_Lines_Passenger_Rail/FeatureServer`, item `2d932ad3623640f1affe28656577037e`; "a work of the United States government ... not protected by any U.S. copyrights"). It has the Caltrain line itself, which is the HSR alignment north of Diridon. Pair it with station points from the Final EIR/EIS and label it "Approximate alignment (shared Caltrain corridor)". The BTS host path isn't yet in `OFFICIAL_PREFIXES`; geodata.bts.gov is `.gov`.
- Design caution: most of this line already exists as Caltrain. Drawing it in full "future" color would overstate the change. Consider drawing only the station points and the Brisbane maintenance facility in color, with the corridor as a thin dashed line.

Press or non-official only: none used in the record.
