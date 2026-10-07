# Candidate projects: BART Silicon Valley Phase II (VTA), Diridon Station redevelopment (San José)

Checked 2026-10-07 against official records read in full text. Local copies are in `data/raw/official/bart-silicon-valley-phase-2/` and `data/raw/official/diridon-station/` (git-ignored). Page numbers are PDF page numbers. Draft records: `scratchpad/records/new/bart-silicon-valley-phase-2.json` and `scratchpad/records/new/diridon-station.json` (both pass `tests/record-check.test.ts`).

Shorthand:
- VB = `https://vtabart.org/wp-content/uploads/` (VTA's BSVII project site; vta.org's project page says "VTA has launched a Microsite for the BART Silicon Valley Phase II Extension Project ... vtabart.org")
- PMOC-07 = VB`2026/09/2026-07-CA-BSVII-OP25-ProjectMonitoringReport_08-28-2026-091626-v1.pdf` (FTA Project Monitoring Report, status June 30, 2026, final Aug 28, 2026, 71 pp.)
- PMOC-03 = VB`2026/05/2026-03-CA-BSVII-OP25-ProjectMonitoringReport-051926-v1-1.pdf` (same series, status Feb 28, 2026, final May 7, 2026, 78 pp.)
- EMR-07 = VB`2026/09/BSVII_Executive-Monthly-Report_July_2026.pdf` (VTA BSVII Executive Monthly Progress Report, July 2026, Rev. 0, Aug 31, 2026, 50 pp.)
- IQ = `https://santaclaravta.iqm2.com/Citizens/FileOpen.aspx` (VTA's agenda system; VTA Board, BSVII Oversight Committee and Diridon Station Steering Committee)
- DS = `https://www.diridonsj.org/` (the Diridon partner agencies' site; the City's June 2025 Council memo cites it, and its contact is City staff at `@sanjoseca.gov`)
- SJA = `https://legistar.granicus.com/sanjose/attachments/`

About the PMOC reports: they are written by FTA's Project Management Oversight Contractor (AtkinsRéalis) for FTA Region IX under an FTA contract, and VTA publishes them on vtabart.org. They are federal oversight records, so they're treated as official here; where they disagree with VTA's own reports, both are noted.

| candidate | recommendation | why |
|---|---|---|
| BART Silicon Valley Phase II | INCLUDE | A megaproject by any measure: $12.746 billion adopted budget, 6-mile BART extension with 4 stations and a yard, under early construction (tunnel launch structure). The Civil Grand Jury calls it "the most costly and complex project" VTA has undertaken. First transit project on the map; draw as a line plus station points. |
| Diridon Station redevelopment | INCLUDE (as the station project only) | $3–6 billion conceptual cost, regional hub for six rail operators plus BART; in environmental review since late 2025. Keep it separate from Google Downtown West (already mapped) and do not add the Diridon Station Area Plan as a project (it would double count Downtown West). |

---

## bart-silicon-valley-phase-2 (BART Silicon Valley Phase II, BSVII)

Documents read:
- PMOC-07 and PMOC-03 (above); PMOC-03 Appendix 3 is the Independent Peer Review final report (Sept 2025).
- EMR-07 (above).
- October 2026 Construction Update: VB`2026/09/2026_BSVII_October_ConstructionMonthlyUpdate-FINAL.pdf` (3 pp.).
- Fact sheets: overview, May 2026, VB`2026/08/VTABSV_FactSheet_Overview-Benefits-051226_v1-3.pdf`; Diridon station, Jan 2026, VB`2026/08/VTABSV_FactSheet_2025_Diridon_01062026.pdf`; Santa Clara station, VB`2026/08/VTABSV_FactSheet_2025_SantaClara_01062026-2.pdf`.
- vta.org project page `https://www.vta.org/projects/bart-sv/phase-ii` and Planning & Environmental page `https://www.vta.org/projects/bart-sv/phase-ii/planning-and-environmental`.
- CEQA Addendum, Feb 2026 (Diridon replacement parking): `https://www.vta.org/sites/default/files/2026-03/2026-02_BSVII_Diridon_Parking_Addendum.pdf` (20 pp.).
- CEQA Addendum, June 2024 (design refinements): `https://www.vta.org/sites/default/files/2024-07/ceqa_addendum.pdf` (125 pp.; sections 1–2).
- 2018 Final SEIS/SEIR: Executive Summary, Vol. III Appendix B Project Plans and Profiles (56 sheets), station site plan concepts (document list `https://www.vta.org/projects/documents?document_search=&document_category%5B%5D=3901&project=1533716`).
- VTA Board minutes: Oct 17, 2025 special meeting IQ`?Type=15&ID=3034&Inline=True`; June 26, 2026 IQ`?Type=15&ID=3133&Inline=True`.
- CEQAnet SCH 2002022004 (`https://ceqanet.lci.ca.gov/2002022004`), documents 38–42 (NODs for the four addenda, 2022–2026).
- 2025–2026 Santa Clara County Civil Grand Jury, "VTA's Management and Oversight of BART Silicon Valley Phase II", June 17, 2026: `https://santaclara.courts.ca.gov/system/files/civil/vtas-management-and-oversight-bart-silicon-valley-phase-ii.pdf` (41 pp.), and VTA's media statement on it (vta.org).
- VTA GTFS (`https://gtfs.vta.org/gtfs_vta.zip`, feed version 2026-08-27) for station coordinates.

| field | official value | source | verbatim quote |
|---|---|---|---|
| length, stations, yard | ~6.0 miles; 4 stations (3 underground in San José, 1 at grade in Santa Clara); Newhall Yard maintenance facility | PMOC-07 p.4; EMR-07 p.12 | "an approximately 6.0-mile extension of the BART system from the Berryessa/North San José Station ... to the proposed Santa Clara Terminal Station"; "three below-ground stations (28th Street/Little Portugal Station, Downtown San José Station, and Diridon Station) and one at-grade station (Santa Clara Station), and a maintenance facility at Newhall Yard" |
| tunnel | single bore, ~5 miles, ~53 ft diameter | PMOC-07 p.4 | "a single deep underground mega-tunnel five miles long and 53 feet in diameter" |
| tunnel (CEQA) | inner diameter ~41→48 ft, outer ~45→52 ft, TBM ~54 ft (2022 refinement) | 2024 Addendum p.9 | "increase in the tunnel's inner and outer diameters from approximately 41 to 48 feet and approximately 45 to 52 feet, respectively, with a corresponding increase in the size of the Tunnel Boring Machine (TBM) from 45 to approximately 54 feet in diameter" |
| configuration | Scenario 1, single 53-ft bore West Portal to East Portal, approved Oct 17, 2025 | EMR-07 p.14; Board minutes Oct 17, 2025 p.5 | "the construction of BSVII as a single 53' bore from the West Portal to the East Portal"; "M/S/C (Doung/Foley) to approve the advancement of the Scenario 1 Project Configuration ... AYES: Candelas, Cohen, Duong, Foley, Lopez, Sell, Turner, Weinberg NOES: Jain" |
| station locations | 28th St/Little Portugal near Santa Clara St and US 101; Downtown San José at Santa Clara St near Market St; Diridon at the Diridon Intermodal Transit Center; Santa Clara at grade next to Santa Clara Caltrain | PMOC-03 p.2 | "28th Street/Little Portugal, will be located underground near Santa Clara Street and U.S. 101 ... Downtown San José Station at Santa Clara Street near Market Street; and Diridon Station at the Diridon Intermodal Transit Center" |
| Diridon station | between Montgomery and Cahill streets, NE of Caltrain station | Diridon fact sheet p.1 | "adjacent to the San José Caltrain Diridon Station, between Montgomery and Cahill Streets, just northeast of the existing Diridon Caltrain Station" |
| riders | 55,000 weekday riders (2040) | vta.org project page; overview fact sheet p.1 | "serving 55,000 weekday riders"; "55,000 Weekday riders in 2040" |
| vehicles | 48 BART cars via BART's Alstom contract, est. $172.6M | PMOC-07 p.26 | "the purchase of 48 revenue vehicles ... estimated to total $172,600,000" |
| owner/operator | VTA owns; BART operates and maintains, VTA pays O&M | PMOC-07 p.4 | "will be owned by VTA, and will be operated and maintained by BART with the operating and maintenance costs provided by VTA" |
| cost (adopted) | $12.746B YOE (FTA P65 at Entry to Engineering) | PMOC-07 p.5 | "The adopted project budget remains $12.746B (year of expenditure [YOE]), consistent with the Entry to Engineering P65 forecast." |
| cost history | $9.148B (Oct 2021 FTA P65), $9.318B (Sept 2022 VTA), $12.237B (Oct 2023 VTA), $12.746B (Mar 2024 FTA P65) | PMOC-07 p.10 (Table 3) | "Capital Cost Estimate $9.148B $9.318B $12.237B $12.746B" |
| Scenario 1 estimate | $12.123B (peer review, not a re-baseline) | PMOC-03 p.68 | "the estimated cost for Scenario 1, which includes the VE savings, is $12.123 billion (Source: Table 7) compared to the baseline cost of $12.746 billion" |
| spent | ~$2.02B through May 2026; $2,100.4M paid through July 2026 | PMOC-07 p.5; EMR-07 p.18 (Table 8) | "Total project expenditure through May 2026 is approximately $2.02B"; "TOTAL $12,745.6 ($31.1) $12,714.5 $2,487.0 $2,100.4" |
| federal share | FTA cap $5.1B (40%); VTA had asked $6.296B (49.4%) | PMOC-03 p.3 | "VTA requested $6.296B (49.4 percent) in CIG program funds ... $5.1B (40 percent) represents the maximum amount of CIG funds" |
| funding plan | FTA $5,098M; TIRCP $750M; other state $750M; RM3 $375M; 2000 Measure A $2,062M; 2016 Measure B $2,512M; SCCP $75M; LPP $25M; supplemental Measure A $502M; gap $564M; total $12,714M | EMR-07 pp.20–21 (Table 10) | "Funding Gap – TBD $0 $564"; "Total Sources of Funds $12,746 $12,714" |
| FFGA | not executed; VTA roadmap: FFGA risk workshop Dec 2026, grant documents Apr 2027, execution Nov 2027 | PMOC-07 p.6 (Table 1) | "FFGA Risk Workshop December 2026"; "FTA, VTA Execute FFGA November 2027" |
| revenue service | FFGA/FTA date Feb 28, 2039 (Q1 2039); VTA target Q2 2037 | PMOC-07 p.10; EMR-07 p.13, p.15 | "Revenue Service Date February 28, 2039"; "VTA developed the new baseline schedule with a target Revenue Service Date (RSD) of Q2-2037"; "FFGA Revenue Service Date Q1 2039" |
| FTA phase | New Starts Engineering since Aug 1, 2024 | EMR-07 p.13 | "On August 1, 2024, FTA informed VTA of the approval of BSVII to enter the New Starts Engineering (NSE) phase ... The approval to NSE phase also indicated a $5.1B Federal share" |
| tunnel contract | CP2 restated with KST, target price up to $2,443,612,684, total up to $3,547,086,911; only $400M released; 9–1 vote June 26, 2026 | Board minutes June 26, 2026 p.9 | "M/S/C (Foley/Abe-Koga) on a vote of 9 ayes to 1 no ... for a total contract value up to $3,547,086,911. However, the authorization under this Board Action is limited to an amount not to exceed $400,000,000" |
| contract signed, NTP | signed Aug 9, 2026; NTP pre-tunneling Aug 14, 2026 | EMR-07 p.5 | "VTA signed the Amended and restated agreement with KST on August 9, 2026, and issued the NTP for pre-tunneling activities on August 14, 2026." |
| RM3 | MTC approved $192.5M allocation Aug 26, 2026 | EMR-07 p.5 | "Update as of August 26, 2026: MTC Commission voted to approve the $192.5M allocation of RM3 funds for BSVII." |
| construction status | West Portal launch structure excavation 100% (early Sept 2026); 3 million safe hours | Oct 2026 Construction Update p.1 | "In early September, our project celebrated 100% completion of excavation work for the West Portal Launch Structure" |
| launch structure finish | substantial completion forecast Mar 16, 2027 | EMR-07 p.6 | "Launch Structure Substantial Completion 31-Mar-27 16-May-27 02-Apr-27 16-Mar-27" |
| TBM | in storage in Germany; delivery est. second half of 2027 | PMOC-07 p.26 | "the TBM remains in storage in Germany ... Delivery is currently estimated for the second half of 2027." |
| other sites | 28th St station demolition June–Sept 2026; East Portal and Diridon utility work; Diridon soils testing to Oct 18, 2026 | PMOC-07 p.26; Oct 2026 update p.2 | "Demolition scheduled June – September 2026" |
| PMOC risk view | project "remains at high risk" | PMOC-07 p.6 | "the project remains at high risk due to unresolved contract re-packaging and re-baselining" |
| real estate | 75 parcels | EMR-07 p.26 (Table 15) | "Total Parcels* 75" |
| CEQA/NEPA | SEIR certified and project approved Apr 5, 2018; BART approval Apr 26, 2018; ROD Jun 4, 2018 (VTA); addenda Dec 2022, Apr 2023, Jun 2024, Mar 2026 | vta.org Planning & Environmental; CEQAnet 2002022004 docs 38–42 | "On March 5, 2026, the VTA Board of Directors approved a CEQA Addendum to the Final SEIR"; "FTA issued the Record of Decision (ROD) for the Project on June 4, 2018" |
| opening year (CEQA) | 2039, target 2037 | 2024 Addendum p.12 | "construction is expected to commence in 2024 with operations commencing (opening year) in 2039 and target revenue service in 2037" |
| LPA, CIG entry | LPA Nov 2001; CIG Project Development Mar 2016 | PMOC-03 p.3 | "VTA selected the locally preferred alternative (LPA) in November 2001. The project originally entered the Capital Investment Grants (CIG) program Project Development phase in March 2016." |
| CP2 award | Board award to KST May 5, 2022 | PMOC-03 pp.11–12 | "The Contract award was approved by the VTA Board of Directors on May 5, 2022." |
| off-ramp | Board authorized off-ramp June 27, 2025 (later replaced by the restatement) | PMOC-03 p.12 | "On June 27, 2025, the VTA Board of Directors authorized the General Manager/CEO to initiate the contractual off-ramp with KST for CP2" |
| context | Civil Grand Jury: "most costly and complex project" VTA has undertaken; "$12.7 billion" | Grand Jury p.3 | "the most costly and complex project it has ever undertaken. Known as BART Silicon Valley Phase II (BSVII), the $12.7 billion project" |

Conflicts and open items:
- ROD date: vta.org, both addenda and EMR-07 say June 4, 2018; PMOC-03 p.3 and PMOC-07 Attachment G say "June 18, 2018". The record uses June 4 (VTA's own pages link the signed ROD, `2-2018-06-04-VTA-BART-Phase-II-Signed-FTA-ROD.pdf`).
- Entry to Engineering: "August 1, 2024" (EMR-07, PMOC-03) vs "letter dated July 31, 2024" (PMOC-07 p.4).
- 2024 addendum: vta.org says Board approval June 28, 2024 and CEQAnet's NOD was received July 5, 2024; the Feb 2026 addendum (p.8) says "August 2024". Use June 28, 2024.
- EPD Letter of Intent: PMOC says October 2021; EMR-07 p.13 says "September 21, 2021". Not in the record.
- Funding gap: VTA's table shows $564M; the Grand Jury describes "a total outstanding gap of $1.075 billion" (p.7), counting $375 million it attributes to a "yet-to-be-approved regional sales tax measure"; VTA's media statement says that $375 million is Regional Measure 3 money and that no project funding depends on a 2026 ballot measure. The record cites VTA's table.
- PMOC-03 p.18 says "commitments ... total $22,330.6M" (an apparent typo; its own table says $2,330.6M). Not used.
- Grand Jury cost history ($4.7B in 2014, $6.9B in 2020) cites VTA's Auditor General; not used in the record.

Official stage: `infrastructure`. Early works (launch structure excavation, demolition, utility relocation) are under way, tunneling has not started, and there are no vertical buildings. FFGA not executed.

Geometry:
- VTA ArcGIS: `https://gis.vta.org/gis/rest/services/BART/BART/MapServer` (legend lists 31 Project boundary, 34 Stations, 35 Alignment, 44 Newhall Yard ROW, 47 All CSA, 49–58 station concepts). On 2026-10-07 every layer and query endpoint returned "Layer not found"; only `/export` (images) worked. Ask VTA or retry; check the license before use.
- Final SEIS/SEIR Vol. III Appendix B, Project Plans and Profiles (Feb 2018): `https://www.vta.org/sites/default/files/2022-04/VolumeIII_AppendixB_ProjectPlansandProfiles_feb20_2018.pdf` (56 sheets, 30 MB), and station site plan concepts `.../VolumeIII_AppendixBARTStationSitePlanConcepts_feb20_2018.pdf`. Trace the alignment from the plan sheets; the 2024 addendum notes shifts of up to 125 ft west of Diridon, so treat as "Approximate alignment".
- Alignment map: Feb 2026 addendum Figure 2-1 (p.9); PMOC-07 Attachment F (p.48); fact sheets have station-area plans (not to scale).
- Station points: VTA GTFS has Berryessa (PS_BRRS 37.388238, -121.86231), San Jose Diridon (PS_DRDN 37.330656, -121.902394) and Santa Clara Transit Center (PS_SCTC 37.352956, -121.93735) as existing stations; the new BART station positions need tracing.

Press-only: nothing in the record relies on press.

---

## diridon-station (Diridon Station redevelopment)

Documents read:
- DS home, `DS/disc` (DISC Plan page), and the two project updates: `DS/project-updates/committee-steers-at-grade-alternative-into-environmental-review` (May 22, 2025) and `DS/project-updates/august-2025-project-update-alternatives-development-report-published` (Aug 18, 2025).
- Alternatives Development Report (ADR), Executive Summary `DS/s/DiridonStation_AlternativesDevelopmentReport_ExecutiveSummary.pdf` (6 pp.) and Main Report `DS/s/DiridonStation_AlternativesDevelopmentReport_MainReport-accessible.pdf` (48 pp., file dated Feb 2026).
- San José file 25-672 (Council June 10, 2025, consent item 2.27), memo with T&E Committee memo of May 12, 2025: SJA`e09b1345-6450-452c-93a6-64d9facaee10.pdf` (42 pp.); same item at T&E as CC 25-081, SJA`f41b8b6e-4e35-4051-9226-5701e369cb22.pdf`.
- Diridon Station Steering Committee (VTA's iQM2): Aug 19, 2026 packet IQ`?Type=1&ID=4481&Inline=True` (96 pp.: May 20, 2026 minutes, Q2 2026 progress report, environmental review update); May 20, 2026 packet and minutes (IQ`?Type=1&ID=4442`, IQ`?Type=15&ID=3130`); Feb 11, 2026 packet and minutes; Dec 11, 2025 packet.
- San José Legistar API (`webapi.legistar.com/v1/sanjose`): all 2026 matters scanned; none on the Diridon station (only file 26-874, the City's response to the BSVII Grand Jury report).
- CEQAnet: no Diridon station NOP/NOI found (the site's search can't be scripted; the Steering Committee's Aug 2026 schedule shows none filed).

| field | official value | source | verbatim quote |
|---|---|---|---|
| partners | City of San José, Caltrain (PCJPB), VTA, CHSRA, MTC | T&E memo p.3 | "the City of San José, the Peninsula Corridor Joint Powers Authority (Caltrain), the Santa Clara Valley Transportation Authority (VTA), the California High-Speed Rail Authority (CHSRA), and the Metropolitan Transportation Commission" |
| cooperative agreement | July 2018; updated fall 2024 | T&E memo p.3, p.7 | "the Partner Agencies formed a public agency partnership via a Cooperative Agreement in July 2018"; "an updated cooperative agreement that all parties signed in fall 2024" |
| decision body | Diridon Station Steering Committee | T&E memo p.10 | "the Diridon Steering Committee is the official decision-making entity for the Diridon Station Project" |
| concept layout | accepted by Council, Caltrain and CHSRA boards Feb 2020 (elevated concept, superseded) | DS/disc | "In February, 2020, the San Jose City Council, Caltrain Board, and High-Speed Rail Authority Board accepted the staff-recommended Concept Layout." |
| preferred alternative | At-Grade Alternative, May 21, 2025 | ADR Exec. Summary p.5 | "At the May 21, 2025 meeting, the Steering Committee formally approved the At-Grade Alternative as the recommended station design to progress into environmental review." |
| program of projects | At-grade station plus West Virginia St closure/undercrossing, Auzerais Ave grade separation, San Carlos St bridge replacement, Park Ave reconfiguration, noise barriers, Stockton Ave/The Alameda | file 25-672 p.1 | "(a) At-Grade Station Alternative (platforms, tracks, historic station, concourse, plazas, bus facility, light rail station, other affected improvements); (b) West Virginia Street closure ..." |
| tracks and platforms | 3 tracks/2 platforms UP, Amtrak, ACE, CC; 4 electrified/2 platforms Caltrain; 3 electrified/2 platforms HSR (same in At-Grade) | ADR Main p.18 | "Four electrified tracks and two platforms are dedicated to Caltrain services. Another three electrified tracks and two platforms are dedicated to high-speed rail services"; "The track and platform layout within the At-Grade Alternative is the same" |
| retail | over 200,000 sq ft in the concourse | ADR Main p.17 | "concourse level will include over 200,000 square feet of new retail space" |
| cost, duration | $3–6B; 7–10 years to build | ADR Exec. Summary p.5; ADR Main p.37 (Table 3-5) | "The project cost in 2025 dollars is between $3 to $6 billion, with a construction timeline of 7 to 10 years"; "Cost ($2023) $3B-$6B" |
| elevated option | $5–10B, 10–12 years, fatal flaw (loses CEMOF access) | ADR Main p.37 | "The Elevated Alternative is projected to take 10 – 12 years to construct at a cost of $5B - $10B." |
| ridership | 100,000 daily trips by 2050 (2019 forecast) | ADR Exec. Summary p.3 | "projected to reach 100,000 daily trips by the year 2050" |
| station age | 90 years old in 2025 | ADR Exec. Summary p.3 | "The station is 90 years old as of 2025" |
| environmental phase | began Q4 2025; 3-year budget $41M; Caltrain leads env/engineering (ICF) | Aug 19, 2026 packet p.19 | "the third report covering Environmental Phase work, which began in Quarter 4 2025"; "The total 3-year approved budget for this phase of work is $41M." |
| env review duration | three to four years | ADR Exec. Summary p.5 | "anticipated to take three to four years" |
| CEQA exemption | Steering Committee supports SB 1375 (May 20, 2026) | Aug 19, 2026 packet p.13 (minutes) | "to recommend support of Senate Bill 1375, which would provide a targeted California Environmental Quality Act (CEQA) exemption for urban intermodal rail stations" |
| construction authority | subcommittee formed; draft bill for 2027 session | Aug 19, 2026 packet p.13, p.30 | "The goal is to submit a draft bill for the California Legislative session in 2027." |
| TOD sites | 32/60 Stockton Ave (VTA) and 698 W. Santa Clara St (Caltrain) | Aug 19, 2026 packet p.87 | "This analysis identified two sites to include in the environmental review." |
| next steps | program definition summer 2026; technical studies winter 2027; open house late 2026 | Aug 19, 2026 packet p.87 | "followed by engineering and technical studies required for environmental review in winter 2027"; "A community open house is anticipated in late 2026." |
| funding | next phase unfunded | Aug 19, 2026 packet p.30 | "Identifying funding for the next phase of work – preliminary engineering and operationalization of a construction authority subject to further consideration." |
| DSAP context | up to 12,900 homes and 14.7M sq ft office/commercial | ADR Exec. Summary p.4 | "The City's adopted Diridon Station Area Plan includes up to 12,900 new homes and a total of 14.7 million square feet of office and commercial space." |

Conflicts and open items:
- Cost basis: "$3 to $6 billion" is "in 2025 dollars" in the ADR executive summary (p.5) but "Cost ($2023)" in the ADR main report (p.37) and the City's memo (p.8). The record gives the range without a dollar year and flags it.
- Council action on file 25-672 (June 10, 2025): the item shows "RENUMBERED" with no recorded vote in the Legistar API; the outcome is unconfirmed.
- SB 1375 (2025–26): leginfo.legislature.ca.gov returns a Cloudflare challenge to scripts; status unknown.
- The T&E memo (p.10) says environmental review takes "up to three years"; the ADR and DS say three to four years.

Official stage: `entitlement` (formal environmental review phase under way; no approvals and no construction funding).

Relationship to other projects (avoid double counting):
- **Google Downtown West** (`downtown-west`, already mapped) lies in the Diridon Station Area Plan around the station; its homes and office space belong to that record. The station project adds no homes or office space of its own (only concourse retail and two TOD sites to be studied).
- **Diridon Station Area Plan** (City of San José, ~12,900 homes, 14.7M sq ft): don't map it as its own project. It overlaps Downtown West, and its plan documents are on sanjoseca.gov (blocked to scripts). Mention it in the station record's notes only.
- **BSVII's Diridon BART station** is part of `bart-silicon-valley-phase-2`; it sits underground on the northeast side. Show it as a station point on the BART line, and mention the link in each panel.
- **High-speed rail**: CHSRA's San José station is a partner element; if `cahsr-sf-sj` (researched separately) is added, its Diridon station should point to this record rather than repeat it.

Geometry:
- No GIS layer for the station footprint. Trace from ADR Figure 2-1 "DISC Boundary" (Main Report p.14), Figure 2-3 concourse plan and Figure 2-5 track layout; the Aug 19, 2026 Steering Committee slides (packet p.92) show the "Future Station Project Footprint" and TOD sites A and B. Earlier scaled layout drawings: DISC Layout Development Report Appendix B (2019, elevated concept, superseded): `DS/s/20191108_DISC_Layout-Development-Report_Appendix-B1_Layout-Drawings-for-online.pdf` (and B2, B3). Label "Approximate boundary" and "Concept design".
- Center: VTA GTFS parent stop PS_DRDN "San Jose Diridon Station" (37.330656, -121.902394).

Press-only: none used. SB 1375's text and status need an official source (leginfo).

Hosts added to `src/projects/official.ts` (OFFICIAL_HOSTS): `vta.org` (VTA; covers www., gis., gtfs.), `vtabart.org` (VTA's BSVII site), `diridonsj.org` (the Diridon partner agencies' site, run by the City of San José), `santaclaravta.iqm2.com` (VTA's agenda system: Board, BSVII Oversight Committee, Diridon Steering Committee). `santaclara.courts.ca.gov` and `ceqanet.lci.ca.gov` are already accepted.

Blocked or unreachable: `vta.legistar.com` returns "Invalid parameters!" and `webapi.legistar.com/v1/vta` has no client; VTA's board records are on `santaclaravta.iqm2.com` instead. `www.transit.dot.gov` (FTA CIG annual reports, FFGA pages) returns 403. `leginfo.legislature.ca.gov` returns a Cloudflare challenge. `sanjoseca.gov` returns 403 (DSAP documents). `gis.vta.org` BART layers can't be queried. CEQAnet's search can't be scripted (project pages by SCH number work).
