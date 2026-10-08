# Official-source pass, 2026-10-07: Peninsula and South Bay

Saved from the research agent's report. Status key: CONFIRMED, CORRECTED, NEW, UNCONFIRMED (looked, nothing official), CONTRADICTED.



**Method.** Every document was downloaded and read in full text (pdftotext; the docx XML for Cupertino's Word attachments). "p." means PDF page unless a document page is named. WebSearch was used once, only to find a CEQAnet URL (Berryessa).

**Access (2026-10-07).**
- menlopark.gov answers plain curl but not a browser user agent.
- These return 403: mountainview.gov, sanjoseca.gov, santaclaraca.gov, sunnyvale.ca.gov, cupertino.gov, sjeconomy.com, portal.scscourt.org.
- Mountain View attachments are cited by their `mountainview.legistar.com/gateway.aspx?M=F&ID=<guid>.pdf` URL. It redirects to the same PDF on `legistar1.granicus.com/mountainview/attachments/`, which isn't in official.ts.

**New host needing Matthew's approval** (only if the Tasman East license change is applied):
- `public-gis-missioncity.opendata.arcgis.com`, plus the item page at `www.arcgis.com/home/item.html?id=99705d50527048679319785fb31df6f0`.
- Why it counts as agency-run: it is the City of Santa Clara's ArcGIS Hub site. Its domain record gives orgTitle "City of Santa Clara", orgId evwJC31SSJVvbZfF. The zoning item is owned by the city's `missioncitygeo` account.

---

## brisbane-baylands

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R stageNote: remediation and grading could start in 2027, buildings 1–2 years later | CORRECTED | The plan's Measure JJ table says the approved remedial action plans project site remediation (west of Caltrain) to be **complete** in mid-2027; schedules are to be updated in the RDIPs. Landfill closure is due within 10 years of the closure plan's approval. The development agreement would require remediation to finish before construction, and it sets each phase's timing. No official building start date. | https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12570,plainText=false) ; https://www.brisbaneca.gov/DocumentCenter/View/2994/09-Implementation-PDF | Sept 14, 2026 Council packet, Attachment 3 pp. 16–18 of 151; Specific Plan ch. 9 §9.2 (PDF p. 3) | "The projected completion date for site remediation is mid-2027. These schedules will be updated in the RDIP documents"; "the requirement that remediation be completed prior to initiating construction activities"; "The specific timing for development within each phase and district is specified in the Development Agreement" |
| R summary: former rail yard and landfill on the San Francisco border | CONFIRMED | Former Southern Pacific railyard and San Francisco municipal sanitary landfill; borders San Francisco across the county line | https://www.brisbaneca.gov/DocumentCenter/View/2987/01-IntroductionPDF | ch. 1 pp. 1-4 to 1-5 (PDF pp. 5–6) | "the main railyard for freight train activity in and out of San Francisco"; "San Francisco began using the area east of the tracks as a municipal sanitary landfill"; "immediately to the north across the San Francisco county line" |
| R summary: could roughly double Brisbane, a city of under 5,000 | UNCONFIRMED | The draft General Plan table gives the Baylands 4,032–4,928 residents. Brisbane's current population isn't in the documents read. | fileId=12570 (above) | Attachment 10 Exh. D, Table 1, p. 63 of 151 | "Planned Development - 4,032-4,928 residents" |
| R summary: two decades in planning | CONFIRMED (substance) | First EIR notice of preparation received Feb 27, 2006 (Case SP-1-06); later notices 2010, 2012, 2020, 2023 | https://ceqanet.lci.ca.gov/Project/2006022136 | CEQAnet document list | "NOP City of Brisbane 2/27/2006 Brisbane Baylands Specific Plan (Case SP-1-06)" |
| R acresNote: a small portion lies in San Francisco | CONTRADICTED | The whole plan area is within Brisbane | https://www.brisbaneca.gov/DocumentCenter/View/2987/01-IntroductionPDF | p. 1-4 (PDF p. 5) | "The Specific Plan area is within the limits of the City of Brisbane" |
| V Council vote, resolution and ordinance numbers | UNCONFIRMED (no action yet) | Hearings held Sept 14, Sept 29 and Oct 6, 2026. Revised schedule: Oct 15 (phasing and remediation), Oct 20 (water; financing and revenue-positive), Oct 26 (development agreement and public financing; consider closing the hearing), Nov 9 (responses; deliberations). The fiscal analysis is still under peer review. | https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12608,plainText=false) ; https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12627,plainText=false) ; https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12679,plainText=false) | Sept 29 packet Attachment 2, p. 10; Oct 6 report pp. 3, 7; Sept 14 minutes p. 3 | "Thursday Oct 15, 5:30 PM Phasing and Remediation"; "Development Agreement and Public Financing Mechanisms / Consider closing public hearing"; "Monday, Nov 9 ... Deliberations" |
| V whether a development agreement is part of the approvals | NEW | Yes. It is required by General Plan Policy BL1 (Measure JJ). It is not among the entitlements recommended Sept 14 / Oct 6. The Planning Commission reviews it before the Council; the Council's agreement hearing is Oct 26. | fileId=12570 ; fileId=12608 | Attachment 3 p. 16; PC Aug 13 minutes (Attachment 14) p. 143 | "A Development Agreement will be required pursuant to General Plan Policy GP-1-18 and will be considered in connection with implementation of the Specific Plan"; "the forthcoming Development Agreement, which will be reviewed by the Commission before proceeding to the City Council" |
| V the Notice of Determination | UNCONFIRMED (not filed) | No NOD for the Specific Plan; the latest filing is an RC dated May 18, 2026. Related NODs: Landfill Closure Plan (Mar 7, 2025), OU-SM remediation (Oct 11, 2021), GP-1-19 (Feb 3, 2020). | https://ceqanet.lci.ca.gov/Project/2006022136 ; https://ceqanet.lci.ca.gov/2006022136/11 | CEQAnet document list | "NOD ... 3/7/2025 Brisbane Baylands Project—Brisbane Landfill Closure Plan" |
| V a non-draft GIS boundary | UNCONFIRMED | The city's ArcGIS org still has only the DRAFT boundary layer, plus the Nov 10, 2025 General Plan and zoning layers | https://services9.arcgis.com/UGpGSV1ugL0pHSgX/arcgis/rest/services?f=json | service list | — |
| V when remediation, grading and construction would start | CORRECTED | See row 1. Phase I (west side) proceeds as each district's grading and remediation are done; Phase II (east side) follows landfill closure. | https://www.brisbaneca.gov/DocumentCenter/View/2994/09-Implementation-PDF | §9.2 (PDF p. 3) | "Phase I development will proceed as grading and remediation for each district are completed." |

**Proposed data changes (brisbane-baylands)**
- **stageNote:** append "The Council's revised schedule sets further hearings on Oct 15 (phasing and remediation), Oct 20 (water and financing), Oct 26 (the development agreement) and Nov 9, 2026 (deliberations)."
- **nextMilestone:** "City Council hearings on phasing and remediation (Oct 15), water and financing (Oct 20) and the development agreement (Oct 26), then deliberations (Nov 9, 2026)."
- **timeline:** add `{"date":"2006-02-27","event":"City issues the first notice of preparation for the Baylands Specific Plan EIR (Case SP-1-06)."}`
- **summary:** may mention "a former rail yard and San Francisco landfill on the San Francisco line".
- **verify:**
  - Remove the development-agreement item.
  - Add "the development agreement's terms (Council hearing Oct 26, 2026; the Planning Commission reviews it first)".
  - Replace the remediation item with "updated remediation schedules in the RDIPs (the plan projects remediation complete in mid-2027) and the phase timing the development agreement will set".
  - Keep the vote, NOD and GIS items.
- **reported:**
  - Delete `acresNote` (contradicted).
  - Cut `stageNote` to "Buildings one to two years after remediation."
  - Keep "double the size" in `summary`.
- **sources:** add fileId=12570, fileId=12679, DocumentCenter/View/2987, DocumentCenter/View/2994, https://ceqanet.lci.ca.gov/Project/2006022136.

---

## willow-village

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R stageNote: Meta paused citing economic uncertainty and AI spending | UNCONFIRMED | The city gives no reason | https://www.menlopark.gov/files/sharedassets/public/v/3/agendas-and-minutes/planning-commission/2026-meetings/agenda/20260518-planning-commission-agenda-packet-amended.pdf | Staff report 26-020-PC p. 8 (packet p. 286) | "on May 1, 2026, Meta announced their intention to pause the project, and therefore, City staff has suspended its review of these actions" |
| R stageNote: nothing has been built | CONFIRMED (substance) | Improvement plans, the final map and the Hamilton parcel map were still in review; most development agreement terms depend on construction starting | same | p. 8 (packet p. 286) | "Many of the terms of the DA are conditioned on commencement of the project and, therefore, most DA items are not applicable at this time." |
| R stageNote: development agreement in force through 2032 | CORRECTED | Still in effect. 10-year initial term from the Effective Date: the date Ordinance 1095 took effect, 30 days after its Dec 13, 2022 adoption, so Jan 12, 2023 (computed). That runs to January 2033. One 7-year extension is possible, only after certificates of occupancy for at least 865 homes and the grocery store. | https://www.menlopark.gov/files/sharedassets/public/v/1/community-development/documents/projects/under-review/willow-village/1095-willow-village-development-agreement.pdf ; https://www.menlopark.gov/Government/Departments/Community-Development/Projects/Approved-projects/Willow-Village | Ord. 1095 §9 (p. 3); agreement §§2.1–2.2 (pp. 21–22) | "This ordinance shall become effective thirty (30) days after the date of its adoption."; "The 'Initial Term' of this Agreement shall be ten (10) years, commencing on the Effective Date"; "certificates of occupancy must be issued for at least eight hundred and sixty-five (865) residential units" |
| R summary: next to Meta's campus in Belle Haven | CONFIRMED (partly) | A tunnel would connect the site to Meta's West and East campuses. The elevated park links Belle Haven to the site. "In Belle Haven" isn't stated. | project page; development agreement | project page "Key project components"; agreement §5.1A (p. 45) | "connecting the project with the West and East campuses"; "an elevated park to provide direct and convenient access from Belle Haven to the Main Project Site" |
| R summary: largest project in the city's history | UNCONFIRMED | Not found in official records | — | — | — |
| V resolution numbers for Dec 6, 2022 | NEW | Dec 6, 2022: Res. 6790 (EIR/MMRP), 6791 (circulation map), 6792 (main-site vesting tentative map), 6793 (Hamilton vesting tentative map), 6794 (BMR agreements). Dec 13, 2022: Ord. 1094 (zoning map and conditional development permit) and Ord. 1095 (development agreement), Ord. 1095 passed 4–0 with Combs recused. | development agreement (above) | Recital H (pp. 12–13); Ord. 1095 p. 4 | "by Resolution No. 6790, adopted by the City Council on the sixth day of December, 2022"; "AYES: Mueller, Nash, Taylor, Wolosin ... RECUSED: Combs" |
| V development agreement effective and recording dates | NEW | Effective 30 days after Dec 13, 2022 (Jan 12, 2023, computed). Recorded Mar 31, 2023, San Mateo County 2023-014495. Also recorded: BMR agreement Apr 21, 2023 (2023-017941); conditional development permit notice May 5, 2023 (2023-021208). | agreement (above); https://www.menlopark.gov/files/sharedassets/public/v/1/community-development/documents/projects/under-review/willow-village/project-wide-affordable-housing-agreement.pdf ; https://www.menlopark.gov/files/sharedassets/public/v/1/community-development/documents/projects/under-review/willow-village/notice-of-terms-and-conditions-of-conditional-development-permit.pdf | agreement p. 5; BMR p. 1; permit notice p. 1 | "2023-014495 8:52 am 03/31/2023 ... Recorded in Official Records County of San Mateo" |
| V reason for the pause | UNCONFIRMED | Not stated | 26-020-PC | p. 8 | — |
| (extra) architectural control plans | NEW | Approved June 26, July 24 and Sept 18, 2023 | project page | Related documents | "approved by the Planning Commission at its September 18, 2023 meeting" |
| (extra) Housing Element | NEW | Willow Village's homes are counted in the 2023–31 Housing Element; the city will evaluate the impact | project page | Project update | "The City will evaluate potential impacts to the City's Housing Element." |

**Proposed data changes (willow-village)**
- **timeline 2022-12-06:** "City Council certifies the EIR (Resolution 6790) and approves the circulation map amendment, vesting tentative maps and below-market-rate housing agreements (Resolutions 6791–6794)."
- **timeline 2022-12-13:** "City Council adopts the zoning and conditional development permit ordinance (Ordinance 1094) and the development agreement (Ordinance 1095), 4–0 with one recusal."
- **timeline:** add `{"date":"2023-03-31","event":"Development agreement recorded in San Mateo County."}`. Optionally split the 2023-06 entry into the three ACP dates (June 26, July 24, Sept 18, 2023).
- **stageNote:** end with "The city says the development agreement is still in effect; its initial term runs to January 2033."
- **verify:** remove the resolution-number and agreement-date items; keep the reason for the pause.
- **reported.stageNote:** keep only "Meta paused it citing economic uncertainty and AI spending."
- **sources:** add the BMR agreement PDF.

---

## parkline

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R stageNote: Phase 2 assumes SRI leaves the campus | CORRECTED | SRI has decided to vacate Buildings P, S and T, which the 2025 approval kept, and may occupy one of the new office/R&D buildings. Phase 2 demolishes about 1.38M sq ft in 38 buildings. | https://www.menlopark.gov/files/sharedassets/public/v/1/agendas-and-minutes/city-council/2026-meetings/20260922/j1-20260922-cc-parkline-phase-2.pdf | 26-161-CC pp. J-1.2–1.3 (PDF pp. 2–3), Table 1 | "SRI has determined they will vacate Buildings P, S, and T ... with the potential for SRI to occupy one of the proposed office/R&D buildings" |
| R stageNote: demolition before the end of 2027 | UNCONFIRMED | Phasing has no dates. The development agreement requires the Building T BSL-3 lab to be decertified by Jan 1, 2027. | https://www.menlopark.gov/files/sharedassets/public/v/2/agendas-and-minutes/planning-commission/2026-meetings/agenda/20260914-planning-commission-agenda-packet.pdf | 26-041-PC pp. 18–19 (packet pp. 272–273), Table 9 | "decertification process for the BSL-3 lab located in Building T no later than January 1, 2027" |
| R nextMilestone: applicant hopes for about 12 months | UNCONFIRMED | In completeness review. Environmental review (planned as an EIR addendum by ICF) starts after the Council study session. Housing Commission, Planning Commission and Council actions follow. | 26-161-CC | pp. J-1.5–1.6 | "The project is currently in the completeness review stage and staff intends to commence the environmental analysis of the proposed revised project following the City Council study session." |
| R program.notes: 220 single-family homes and 108 townhomes | CONFIRMED | 122 single-family plus 98 small-lot single-family (220) and 108 townhomes | https://www.menlopark.gov/Government/Departments/Community-Development/Projects/Under-review/Parkline-Phase-2 ; 26-161-CC | Phase 2 page; Table 1 | "122 single-family homes and 98 small lot, single-family homes; 108 townhomes" |
| V 2025 resolution and ordinance numbers | NEW | Sept 30, 2025: Res. 6996 (EIR), 6997 (General Plan amendment), 6998 (vesting tentative map), 6999 (BMR). Oct 7, 2025: Ord. 1125 (C-1-S, rezoning, X overlay, conditional development permit) and Ord. 1126 (development agreement). | https://www.menlopark.gov/files/sharedassets/public/v/2/agendas-and-minutes/city-council/2025-meetings/20251007/i2-parkline-second-readings_reduced.pdf | Ord. 1125 (PDF p. 5); agreement Recital L (PDF pp. 353–354) | "by Resolution No. 6996, adopted by the City Council on September 30, 2025"; "Approval of this Agreement by Ordinance No. 1126 ... adopted by the City Council on October 7, 2025" |
| V outcome of the Sept 22, 2026 study session | UNCONFIRMED | A study session (feedback only, no action). Minutes not posted; the latest posted Council minutes are Aug 25, 2026. | https://www.menlopark.gov/files/sharedassets/public/v/4/agendas-and-minutes/city-council/2026-meetings/20260922/20260922-city-council-special-and-regular-agenda.pdf ; https://www.menlopark.gov/Agendas-and-minutes | item J1 | "Review and provide feedback on proposed revisions to the approved Parkline masterplan project" |
| V whether SRI will leave | NEW | See row 1 | 26-161-CC | p. J-1.2 | — |
| (extra) BMR count | NEW (conflict) | Project page says 293; staff report Table 1 says 294 | 26-161-CC | Table 1 | "Total BMR units 251 294" |
| (extra) open space | NEW | 26.9 acres, about 13.8 publicly accessible (the page says about 14) | 26-161-CC | Table 1 | "approximately 13.8 publicly accessible" |

**Proposed data changes (parkline)**
- **timeline:** add "(Resolutions 6996–6999)" to 2025-09-30 and "(Ordinances 1125 and 1126)" to 2025-10-07.
- **stageNote:** replace the last two sentences with "A Phase 2 application, resubmitted Aug 13, 2026, would raise the total to 1,082 homes and demolish every campus building; city staff report that SRI has decided to vacate Buildings P, S and T, which the 2025 approval kept, and may occupy one of the new office buildings. The application is in completeness review."
- **nextMilestone:** "Completeness and environmental review (a planned addendum to the certified EIR) of the Phase 2 application."
- **program.notes:** Phase 2 becomes "two 300-unit apartment buildings, 122 single-family and 98 small-lot single-family homes, 108 townhomes and up to 154 affordable homes".
- **verify:**
  - Remove the numbers and SRI items.
  - Sept 22 item becomes "the Sept 22, 2026 study session minutes (not posted)".
  - Add "Phase 2 BMR count (293 on the page vs 294 in the staff report) and publicly accessible open space (about 14 vs 13.8 acres)".
  - Add "when demolition starts (press: before the end of 2027)".
- **reported:**
  - Delete `program.notes` (confirmed).
  - `stageNote` becomes "Demolition is targeted before the end of 2027."
  - Keep `nextMilestone`.
- **sources:** add the 26-161-CC report and the Oct 7, 2025 report.

---

## related-santa-clara

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R developer: Related Companies | UNCONFIRMED | The development agreement party is Related Santa Clara, LLC. City closed-session agendas name "Related California" (project parcels, May 2016) and "Related Companies" (Tasman garage, 2019–20) as negotiating parties; ownership isn't stated. | https://santaclara.legistar.com/LegislationDetail.aspx?ID=4657&GUID=7871E5B8-3D90-4841-9FB1-951EEF552789 ; https://santaclara.legistar.com/LegislationDetail.aspx?ID=16284&GUID=44F5129A-D47C-407E-A9D7-C5486D9DC46B | matter titles | "Negotiating Party: Stephen F. Eimer, Related California"; "Stephen Eimer, Executive Vice President, Related Companies" |
| R summary: former landfill and golf course across from Levi's Stadium | CONFIRMED | Santa Clara Golf and Tennis Club plus parcels along Tasman Dr. across from the stadium; a closed landfill | https://santaclara.legistar1.com/santaclara/attachments/097f41c1-1cf5-4b30-8f97-3036e448ab46.pdf | 2016 report pp. 1, 5 | "all of the current Santa Clara Golf and Tennis Club, as well as the vacant parcels across from Levi's Stadium along Tasman Drive"; "This adaptive reuse of a closed landfill facility" |
| R summary: then CityPlace | CONFIRMED | Called CityPlace Santa Clara; the development agreement is titled "City Place Santa Clara" | same; https://santaclara.legistar1.com/santaclara/attachments/3f1462b1-c840-4ae8-b2cf-20565e67a6e5.pdf | p. 1; agreement cover | "CityPlace Santa Clara is a proposed phased development of approximately 240 acres of City-owned land" |
| R summary: largest-ever; $6.5B | UNCONFIRMED | — | — | — | — |
| R timeline 2019 announcement | UNCONFIRMED | — | — | — | — |
| V building permits for Parcels 1–2 | UNCONFIRMED | Nothing on Legistar since Sept 2025. Oct 6, 2026 report: data centers on Parcels 1–2 need a conditional use permit; Silicon Valley Power has accepted no new data-center applications since 2023. The city's Oct 2026 map of approved data centers doesn't include the site. | https://santaclara.legistar.com/LegislationDetail.aspx?ID=26904&GUID=00091789-34A7-4A75-8D97-2EC0CA9B1A9C ; https://santaclara.legistar1.com/santaclara/attachments/f7bb976a-2acf-4498-a4c1-8a395872cacf.pdf | report text; map | "In 2025, the City created additional regulations to conditionally permit data centers for the Related Santa Clara project's northeast area (parcels 1 and 2)"; "SVP has not accepted applications for new data centers since 2023." |
| V lawsuit subject (26CV489245) | UNCONFIRMED | Only the case name, from the Council closed session (agenda date Aug 18, 2026); court portal 403 | https://santaclara.legistar.com/LegislationDetail.aspx?ID=26733&GUID=EB0B81E1-4F16-476F-9BBE-4972282E876C | matter 26-867 | "Related Santa Clara, LLC vs. Jennifer Osborn, et al, Santa Clara Superior Court, Case no. 26CV489245" |
| V Related Companies as parent | UNCONFIRMED | See row 1 | — | — | — |

**Proposed data changes (related-santa-clara)**
- **summary:** may add "on the former Santa Clara Golf and Tennis Club, a closed city landfill across Tasman Drive from Levi's Stadium".
- **stageNote:** append "The city's October 2026 data-center report says data centers on Parcels 1 and 2 need a conditional use permit and that Silicon Valley Power has accepted no new data-center applications since 2023."
- **verify:** lawsuit item becomes "...(Council closed session, Aug 18, 2026; court portal not reachable)". Keep the other two.
- **reported.summary:** cut to "Silicon Valley's largest-ever approved private development; a $6.5B plan."
- **sources:** add the 26904 matter and the Oct 2026 map.

---

## downtown-west

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R stageNote / timeline: paused in 2023 | UNCONFIRMED | No official pause date; the earliest official statement found is the Nov 25, 2024 memo | https://legistar.granicus.com/sanjose/attachments/0b810cf1-d5af-4c58-9bf1-2f86f9063689.pdf | pp. 2–3 | "These same challenges have delayed the Downtown West project." |
| R stageNote: blocks cleared and fenced | UNCONFIRMED | Nov 2024: interim activation of some existing buildings through Jamestown. Permit data (2025–26) show Google work on existing buildings: tenant improvements at 450 W. Santa Clara St. (2026-126188-CI, issued Jul 20, 2026; 2026-135054-CI, Sept 1, 2026); reroof at 150 S. Montgomery St. (2025-112975-CI); "Spark Social" alteration at 140 S. Montgomery St. (2026-135655-CI, issued Sept 11, finaled Oct 2, 2026). Completed demolitions aren't in the open data. | memo above; https://data.sanjoseca.gov/dataset/active-building-permits ; https://data.sanjoseca.gov/dataset/last-30-days-building-permits | memo pp. 2–3; dataset rows (CC0) | "focused on interim activation of select existing buildings through Google's partner, Jamestown, no new construction has begun" |
| R stageNote: city has little power to compel construction | UNCONFIRMED | — | — | — | — |
| R stageNote: sports-and-entertainment district floated | UNCONFIRMED | No San José Legistar matter found (2025–26) | sanjose.legistar.com | — | — |
| R summary: nothing built | CONFIRMED (in part) | "No new construction has begun" is confirmed; "cleared" is not | memo | p. 3 | as above |
| R timeline 2026-03 | UNCONFIRMED | Press only | — | — | — |
| V final adoption of the 2021 ordinances | CONFIRMED | June 8, 2021: Ord. 30608 (Title 20 §20.70.700), 30609 (rezoning about 80 gross acres to DC(PD)), 30610 (development agreement with Google LLC) | https://ceqanet.lci.ca.gov/2019080493/6 ; https://ceqanet.lci.ca.gov/2019080493/6/Attachment/W5vOXu ; https://legistar.granicus.com/sanjose/attachments/66868dd5-a380-449a-b2ed-a205a2c36e4f.pdf ; https://legistar.granicus.com/sanjose/attachments/f58ac6d8-c967-4adf-b435-2216e8ee13b2.pdf ; https://legistar.granicus.com/sanjose/attachments/d9985f7d-1a96-43f8-a1e5-96ad5a17618b.pdf | NOD No. 2 p. 6 ("Approved On 6/8/2021"); ordinance headers | "This is to advise that on June 8, 2021, the City Council of the City of San Jose approved the following actions"; "ORDINANCE NO. 30610" |
| V when paused | UNCONFIRMED | See row 1 | — | — | — |
| V current condition | NEW (partial) | See row 2. Google LLC also filed 2026 ministerial development permits, none with a final date; contents unknown (the city's Downtown West page is on blocked sanjoseca.gov): MP26-002 at 105 S. Montgomery St. ("Residential", Apr 24, 2026); MPA24-003-01 at 140 S. Montgomery St. ("Mixed Use", Apr 24, 2026); MP26-005 at 35 Barack Obama Blvd. ("Mixed Use", June 3, 2026). | https://data.sanjoseca.gov/dataset/last-60-180-days-planning-permits | rows 2026-098329-DEV, 2025-129459-DEV, 2026-113516-DEV | "Development Permit / Ministerial Permit / Residential" |
| V heights vs the approved Design Standards and Guidelines | UNCONFIRMED | The 2021 guidelines aren't reachable (only the Oct 2020 draft is on CEQAnet). Ord. 30609 gives 160–290 ft above ground, subject to FAA clearance, with maximums in the guidelines §5.6. | https://legistar.granicus.com/sanjose/attachments/f58ac6d8-c967-4adf-b435-2216e8ee13b2.pdf | p. 9 | "allowable building heights that range from 160 feet to 290 feet above ground level (AGL), contingent on required Federal Aviation Administration (FAA) review clearance" |

**Proposed data changes (downtown-west)**
- **timeline:** add `{"date":"2021-06-08","event":"City Council adopts the zoning amendment, rezoning and development agreement ordinances (30608, 30609 and 30610)."}`
- **stageNote:** middle sentence becomes "A November 2024 city memo says the project has focused on interim use of some existing buildings, no new construction has begun and there is no estimated timeline for restarting major development."
- **program.notes:** add "Allowed heights 160 to 290 ft above ground, subject to FAA review (Ordinance 30609)."
- **verify:**
  - Remove the final-adoption item.
  - Site-condition item becomes "what Google's 2026 ministerial permit filings cover (MP26-002, 105 S. Montgomery St., residential; MPA24-003-01, 140 S. Montgomery St.; MP26-005, 35 Barack Obama Blvd., mixed use) and whether blocks are cleared (press)".
  - Keep the pause-date and guidelines items.
- **sources:** add the CEQAnet NOD 2 and the planning-permit dataset.

---

## north-bayshore

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R stageNote / timeline 2024: Landings terminated | CONFIRMED (Feb 2024) | Landings (2001 Landings Dr.) was approved June 23, 2020 as a separate 799,482 sq ft office project. Grading permit May 31, 2022; building permit Aug 19, 2022. In Feb 2024 Google told the city it would not proceed. The partly built underground garage was demolished and the site restored; the Alta Garage was completed. | https://mountainview.legistar.com/gateway.aspx?M=F&ID=ac366809-4f75-496d-a4ad-c6404fdf9dce.pdf ; https://mountainview.legistar.com/gateway.aspx?M=F&ID=2523973b-8c57-4cff-8fb2-d3e1868c3a34.pdf | Sept 9, 2025 report pp. 1–2; June 10, 2025 report p. 1 | "In February 2024, Google informed the City that it would no longer proceed with construction of the Landings Project and that it intended to demolish the partially constructed improvements on the site" |
| R Middlefield Park sale (2025) | UNCONFIRMED | June 2026: Google still owns 485/495 Clyde Ave (see middlefield-park) | — | — | — |
| R no homes broken ground | UNCONFIRMED | Consistent with Legistar: master-plan phases need Planned Community Permits at Administrative Zoning hearings, and none has appeared since June 2023 | https://mountainview.legistar.com/gateway.aspx?M=F&ID=c5d191b7-b2bd-4e61-a167-15b425bc8c98.pdf | June 13, 2023 report p. 12 | "subsequent zoning permit applications ... to have a final action at an Administrative Zoning (ZA) public hearing" |
| R summary: three walkable neighborhoods | CONFIRMED | Spans three Complete Neighborhoods (the same report's principles say "four") | same | p. 3 | "The project spans across three Complete Neighborhoods (Joaquin, Shorebird, and Pear)" |
| R Google pulling back | UNCONFIRMED | Only the Landings termination is official | — | — | — |
| V construction or permit status 2025–26 | UNCONFIRMED | No permit, public-improvement or zoning item for the master plan on Legistar since June 2023; mountainview.gov 403 | mountainview.legistar.com | webapi title searches | — |
| V amendments since 2023 | UNCONFIRMED (none found) | Related but different: on May 26, 2026 the Shoreline Regional Park Community board amended the North Bayshore Area Plan (Res. S-186), incorporating the master plan by reference | https://mountainview.legistar.com/LegislationDetail.aspx?ID=10243&GUID=7D2B5356-0697-4F70-9AB8-F23A414A3F2D ; https://mountainview.legistar.com/gateway.aspx?M=F&ID=43e50474-fcb3-4a36-ae2e-28b107031e14.pdf | history; report pp. 2–3 | "To Adopt Resolution No. S-186 of the Board of Directors of the Shoreline Regional Park Community Amending the Shoreline Plan" |
| V Landings and Middlefield status | CONFIRMED / NEW | See rows above and middlefield-park | — | — | — |

**Proposed data changes (north-bayshore)**
- **stageNote:** last sentence becomes "No permit for a phase of the master plan has come before the city since approval. Nearby, Google stopped building its separately approved Landings office project in February 2024 and restored the site."
- **timeline:** add `{"date":"2024-02","event":"Google tells the city it will not proceed with its separately approved Landings office building nearby, and later demolishes the partly built garage."}`
- **summary:** may mention three complete neighborhoods (Joaquin, Shorebird and Pear).
- **verify:** third item becomes "whether Google has sold or is marketing any master-plan land (press, 2025)"; keep the other two (none found through Oct 2026).
- **reported:** remove the Landings timeline entry and the Landings clause of `stageNote`; keep the Middlefield sale and "pulling back".
- **sources:** add the Sept 9, 2025 report.

---

## moffett-park

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| V resolution certifying the EIR | CONFIRMED | Res. 1199-23 (SCH 2021080338; approved July 11, 2023). Ord. 3218-23 takes effect Sept 22, 2023. | https://legistar.granicus.com/Sunnyvale/attachments/898afbde-8963-4d24-bc5c-90e388ebed42.PDF ; https://ceqanet.lci.ca.gov/2021080338/5 | Ord. 3218-23 p. 7 | "adopted a Mitigation Monitoring and Reporting Program (Resolution No. 1199-23)"; "This ordinance shall be in full force and effect on September 22, 2023." |
| V affordable homes at 1215 Bordeaux | CONFIRMED | 40 of 265 (27 low-income, 13 very low-income) | https://legistar.granicus.com/Sunnyvale/attachments/9e4fb7da-780f-4864-a6b3-1d608964884b.pdf ; https://legistar.granicus.com/Sunnyvale/attachments/0dbe0dae-4d77-45bd-a243-ec3e78651b09.pdf | data table p. 1; findings p. 16 | "27 low-income (10%) 13 very low-income (5%) 40 total (15% min.)" |
| V appealed? | UNCONFIRMED | Planning Commission approved June 8, 2026 (owner Deerfield 1215 Bordeaux LLC). No Council appeal item on Legistar through Oct 2026. | https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=16913&GUID=6E9B7856-EBBC-4C89-87B0-E0D76ED6C74B | matter 26-0541 | "The motion carried by the following vote" |
| V other projects since 2023 | NEW (partial) | On Legistar only 333–385 Moffett Park Dr. (Dec 2025; Ord. 3250-25), 1215 Bordeaux, and a padel facility permit at 1365 Geneva Dr. (Planning Commission Mar 26, 2025; outcome not recorded). Staff-level approvals aren't on Legistar. | https://sunnyvaleca.legistar.com (matter 15733, file 25-0425) | matter title | "SPECIAL DEVELOPMENT PERMIT: to allow a recreational and athletic facility use (padel ball) in the Moffett Park Specific Plan area. Location: 1365 Geneva Drive" |
| V GIS license | UNCONFIRMED | No license or copyright text in the service metadata; no ArcGIS Online item | https://gis.sunnyvale.ca.gov/arcgis/rest/services/GeneralPlan/MapServer?f=json | — | — |

**Proposed data changes (moffett-park)**
- **timeline 2023-07-11:** add "(Resolution 1199-23)".
- **stageNote:** "...an 8-story, 265-unit apartment building with 40 affordable homes at 1215 Bordeaux Dr...."
- **verify:**
  - Remove the resolution item.
  - Bordeaux item becomes "whether the approval was appealed (none on Legistar as of Oct 2026)".
  - "Other projects" becomes "other approvals, including staff-level ones and the 1365 Geneva Dr. padel facility (Mar 2025)".
  - Keep the license item.
- **sources:** add the 1215 Bordeaux data table.

---

## the-rise

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R program.notes: tallest about 200 ft | CORRECTED | Feb 2024 approved plans: tallest total height from average grade is 228'-3" (an office tower, Block 15 east in the repo massing); tallest residential is 200'-1" (Block 8). The Feb 2026 plans aren't published; the city says no height limit applies. | https://apps.cupertino.org/pdf/Attachment%20A%20-%20Approved%20Plans.pdf | P-0832 (PDF p. 90); P-0831 (PDF p. 89) | "TOTAL HEIGHT FROM AVG. GRADE" "228'-3"" |
| R timeline 2019: mall demolished | CONTRADICTED (completion in 2019) | Sept 2021: above-ground demolition permits issued for Macy's and the mall parking structures; the JCPenney garage demolition (BLD-2020-1628) still pending | https://legistar.granicus.com/cupertino/attachments/7e0e84b1-2eae-4b09-91ab-f0a3d43beafe.docx | Sept 7, 2021 status report | "Demolition permits have been issued for the above ground portions of the former Macy's and mall parking structures"; "Demolition Zone B-1 (JC Penny garage) – BLD-2020-1628 ... which are pending" |
| R timeline 2025-11: affordable cut 890 to 356 | CORRECTED (date) | Third modification approved Feb 27, 2026 (M-2025-001, TM-2026-006) | https://legistar.granicus.com/cupertino/attachments/7813d568-939a-4160-a867-6912a65bfdfe.pdf | p. 1 | "the third and most recent modification application on February 27, 2026" |
| R timeline 2026-02: permit application for the first building (232 affordable) | UNCONFIRMED | Block 5 (Eden Housing) is 234 units: 174 very low-income, 58 low-income, 2 managers. No permit-application record found. | https://legistar.granicus.com/cupertino/attachments/a48ffc4f-a6db-4f2c-a12c-c966dfb6dfbf.pdf | TEFRA report p. 1 | "174 very low-income units, 58 low-income units, and 2 manager units" |
| R stageNote: Eden building to start by end of 2026 | UNCONFIRMED | Eden Housing is confirmed as developer; no start date | same | p. 1 | "for the benefit of Eden Housing, Inc." |
| V July 21, 2026 final map outcome; recording | NEW / UNCONFIRMED | Res. 26-080 adopted 4–0, Moore abstaining: approves Tract 10706 and authorizes recording. Recording date not found. Source is the draft minutes, up for approval Sept 1. The map was submitted April 2026. | https://legistar.granicus.com/cupertino/attachments/dcf6feac-214c-4f56-abb7-f17893ce6df0.pdf ; https://cupertino.legistar.com/LegislationDetail.aspx?ID=15774&GUID=95B3D959-8631-4DD6-872F-A15B007FAAD1 | draft minutes pp. 8–9 | "Ayes: Chao, Fruen, Mohan, and Wang. Noes: None. Abstain: Moore." |
| V July 16, 2024 fee waiver | NEW | Res. 24-077 adopted 4–1, Chao voting no | https://legistar.granicus.com/cupertino/attachments/9c30adf3-983b-47c6-9a4b-f68edac9bb11.docx ; https://cupertino.legistar.com/LegislationDetail.aspx?ID=13758&GUID=E5971CF8-F0AE-444C-82A0-54A93B60D955 | draft minutes | "MOTION: Wei moved and Mohan seconded to adopt Resolution No. 24-077 ... Noes: Chao." |
| V 2022 modification date | NEW | June 3, 2022 | https://legistar.granicus.com/cupertino/attachments/bf1ecb1d-7707-4f6a-9c15-e3382cc6e1e8.pdf | Dec 5, 2023 memo p. 1 | "On June 3, 2022, the City approved the modifications." |
| V demolition finished | UNCONFIRMED | See the 2019 row | — | — | — |
| V Block 5 permit application | UNCONFIRMED | — | — | — | — |
| (extra) remediation | NEW | Oct 6, 2026 Council information session on the county-approved soil remediation plan | https://cupertino.legistar.com/LegislationDetail.aspx?ID=16569&GUID=CED1746F-1BC8-438A-9E49-00C0D62F9473 | title | "Public Information Session regarding Santa Clara County Department of Environmental Health approved remediation plan for soil contamination at The Rise" |

**Proposed data changes (the-rise)**
- **timeline:**
  - The 2022 entry becomes 2022-06-03.
  - 2024-07-16 becomes "City Council waives below-market-rate housing and planning fees under the settlement (Resolution 24-077), 4–1."
  - 2026-07-21 becomes "City Council approves the Phase 1 final map (Tract 10706) and authorizes its recording (Resolution 26-080), 4–0 with one abstention."
  - Add 2026-10-06: "City Council holds a public information session on the county-approved soil remediation plan for the site."
- **program.notes:** add "In the February 2024 approved plans the tallest building is an office tower at about 228 ft and the tallest residential tower about 200 ft (total height from average grade); the 2026 plans aren't published."
- **nextMilestone:** "Recording of the Phase 1 final map; no vertical building permits on the west side until it records." (The Oct 6 TEFRA hearing has passed; its outcome isn't posted.)
- **verify:**
  - Remove the fee-waiver and 2022 items.
  - Final-map item becomes "when Tract 10706 records".
  - Add "the Oct 6, 2026 TEFRA hearing outcome".
  - Keep the demolition and Block 5 items.
- **reported:** delete the 2019 demolition entry (contradicted), the 2025-11 entry and `program.notes`; keep the 2026-02 entry and `stageNote`.
- **sources:** add the July 21 draft minutes, the Dec 2023 memo and matter 16569.

---

## middlefield-park

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| R stageNote: Google looking to sell (2025) | UNCONFIRMED | June 2026: Google is the owner of 485/495 Clyde Ave and negotiated a lease with the City | https://mountainview.legistar.com/gateway.aspx?M=F&ID=96fd7425-1e3a-493c-ad8c-35e070c634f6.pdf | lease report p. 1 | "With the cooperation of the property owner (Google)" |
| R timeline 2025-05 sale | UNCONFIRMED | — | — | — | — |
| V development agreement ordinance number | NEW | Ordinance 19.22, second reading Dec 13, 2022, 6–0 (Hicks recused) | https://mountainview.legistar.com/LegislationDetail.aspx?ID=6117&GUID=9B048072-F48C-47AE-BF71-838CCB9AB708 ; https://webapi.legistar.com/v1/mountainview/matters/6117/histories | history, event 2104, item 4.3 | "Adopt Ordinance No. 19.22 of the City of Mountain View Approving a Development Agreement for the Middlefield Park Master Plan Project" |
| V building or demolition permits | UNCONFIRMED / NEW (partial) | None found. The Clyde lease starts after Google demolishes the two vacant buildings (anticipated before end of 2026); Google applies for the demolition permit after the lease is signed (expected Sept 2026). | lease report | pp. 3–4 | "Following execution of the agreement, Google will apply for a demolition permit from the City and demolish the buildings." |
| V Council action on the Clyde lease | NEW | Approved June 23, 2026 on consent, 7–0: 7-year lease with an option for Google to sell to the City for park credits. Source is the draft minutes, up for approval Sept 8. | https://mountainview.legistar.com/gateway.aspx?M=F&ID=ff19b980-985d-4bc2-992e-6f51cd948659.pdf ; https://mountainview.legistar.com/LegislationDetail.aspx?ID=10628&GUID=4A061632-B564-43A4-BCC6-3F8C277FE3B9 | draft minutes pp. 2–3, 9 (item 4.31) | "To approve the balance of the Consent Calendar ... The motion carried, except for Item 4.14 ... Yes: 7" |
| V sold? | NEW (partial) | Google owned at least the two Clyde parcels in June 2026; no sale record | lease report | p. 1 | — |
| V O1 height (125 vs 115 ft) | UNCONFIRMED (conflict confirmed) | Fig. 8.3.1 labels O1 "115'". Table 8.3.2 gives 125 ft as "Total proposed height maximums (with height bonuses; not to exceed CLUP limit)". The resolution and Council report don't state O1's height. | https://mountainview.legistar.com/gateway.aspx?M=F&ID=e1878a1f-8e37-45c4-84e4-04e0da99f46d.pdf | pp. 123–124 (PDF pp. 129–130) | "O11 182 ft 56 ft 126 ft 95 ft Up To 10 ft N/A 125 ft" |

**Proposed data changes (middlefield-park)**
- **timeline 2022-12-13:** "City Council adopts the development agreement (Ordinance 19.22) on second reading, 6–0 with one recusal."
- **timeline 2026-06-23:** "City Council approves business terms for a seven-year City lease of 485 and 495 Clyde Ave from Google for a park and pickleball courts, with an option for Google to sell the land to the City."
- **stageNote:** last sentence becomes "On June 23, 2026 the Council approved terms to lease two of the site's parcels (485 and 495 Clyde Ave, about 3.72 acres) from Google for a public park with pickleball courts; Google is to demolish the two vacant buildings there first, which the city anticipates before the end of 2026."
- **verify:**
  - Remove the ordinance and lease items.
  - Permits item becomes "demolition permits for 485/495 Clyde (after the lease signing, expected by Sept 2026) and any master-plan permits".
  - Keep the sale item (Google was the owner in June 2026) and the O1 item.
- **sources:** add the draft June 23 minutes and matter 6117.

---

## tasman-east

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| V certificates of occupancy in 2026 | UNCONFIRMED | APR Table A2 (updated Oct 6, 2026) has no 2026 rows | https://data.ca.gov/dataset/housing-element-annual-progress-report-apr-data-by-jurisdiction-and-year | resource fe505d9b-8c36-42ba-ba30-08bc4f34e022 | — |
| V 2240 Calle de Luna (311 homes) | NEW | Same parcel (APN 097-46-019) as 5123 Calle Del Sol: Ensemble, 311 units, entitled July 17, 2019, permit Apr 18, 2022. The Aug 2026 Draft SEIR lists it as "Constructed". No CO in the APR yet. | https://ceqanet.lci.ca.gov/2016122027/7/Attachment/wRdzt5 ; APR | Draft SEIR Table 2.2-1, Fig. 2.0-3 (PDF pp. 36–37) | "Constructed ... 6 5123 Calle Del Sol Construction of up to 311 residential units ... within two buildings" |
| V the 1,500-home amendment: environmental report and hearings | NEW | NOP July 6, 2022. Draft SEIR released Aug 28, 2026 (PLN22-00359), comments to Oct 13, 2026; hearings not yet set. Supports up to 6,000 units; the 220 ft cap stays; island-parcel parkland minimum rises from 1 to 1.5 acres. | https://ceqanet.lci.ca.gov/2016122027/7 ; https://ceqanet.lci.ca.gov/2016122027/7/Attachment/3mpUYy | NOA p. 1; Draft SEIR p. 11 | "Distribution Date: August 28, 2026"; "between Friday, August 28, 2026 and Tuesday, October 13, 2026"; "would support a maximum of 6,000 units" |
| V open-data license for the zoning layer | NEW (needs host approval) | PDDL 1.0 unless stated otherwise (terms revised May 21, 2018). The item's licenseInfo points to these terms; the MapServer copyright reads "City of Santa Clara". | https://public-gis-missioncity.opendata.arcgis.com/pages/terms-of-use ; https://www.arcgis.com/home/item.html?id=99705d50527048679319785fb31df6f0 ; https://map.santaclaraca.gov/maps/rest/services/OPENDATA/RegionalZoningOpenData/MapServer?f=json | terms §IX | "Data is made available under the Public Domain Dedication and License v1.0" |
| V Draft SEIR figures | CONFIRMED | 2,664 units active or completed; about 12.0 acres left. About 4,183 units applied for, including two abandoned approvals (2200 Calle De Luna, 580/583; 2101 Tasman Dr., 939). Built: 2,076 units on six sites, including 191 senior assisted living. Approved but unbuilt: 588 (2263 Calle Del Mundo 301, 5185 Lafayette St 198, 2354 Calle Del Mundo 89). | Draft SEIR | pp. 5, 8–9 (PDF pp. 32, 35–36) | "Currently, the total number of dwelling units for active and completed projects is 2,664 dwelling units."; "Two of the approved projects (2200 Calle De Luna and 2101 Tasman Drive) have since been abandoned." |
| (extra) conflicts | NEW | The Draft SEIR dates Amendment #1 to "September 2020" (the record has Nov 17, 2020) and gives 46 gross acres (the record has about 45) | Draft SEIR | pp. 1, 8 | "In September 2020, the City of Santa Clara adopted an amendment to the Specific Plan (Amendment #1)" |

**Proposed data changes (tasman-east)**
- **stageNote:** "Partly built. The City's state housing reports list certificates of occupancy for about 1,748 homes in seven buildings between Dec 2022 and Nov 2025. The city's August 2026 Draft SEIR counts 2,664 homes in built and approved projects, notes that two approved projects (2200 Calle de Luna and 2101 Tasman Dr.) have been abandoned, and leaves about 12 acres to redevelop under an amendment that would add 1,500 homes."
- **timeline:** add 2022-07-06 (notice of preparation for the amendment) and 2026-08-28 (Draft SEIR released; comments close Oct 13, 2026).
- **nextMilestone:** "Final Supplemental EIR and hearings on the amendment adding 1,500 homes."
- **program.notes:** append "The amendment would allow up to 6,000 homes in all, keep the 220-ft height limit and raise the minimum public parkland on the interior 'island' parcels from 1 to 1.5 acres."
- **verify:**
  - Remove the Draft SEIR figures item.
  - 2240 item becomes "a certificate of occupancy date for the 311-home building at 5123 Calle del Sol (also 2240 Calle de Luna, APN 097-46-019), listed as constructed".
  - Amendment item becomes "hearing dates".
  - License item: remove once the Hub host is approved, and record PDDL 1.0 and "City of Santa Clara" in data/CREDITS.md.
  - Add "Amendment #1 date (Sept vs Nov 17, 2020) and plan area (46 vs 45 acres)".
- **sources:** add the CEQAnet SEIR record and its attachment.

---

## berryessa-flea-market

| Item | Status | Official value | Source (exact URL) | Where | Quote |
|---|---|---|---|---|---|
| V Ord. 30646 final adoption date | UNCONFIRMED | Listed for final adoption Aug 3, 2021 (item 2.2(e)). Legistar records no action, and the minutes are on blocked sanjoseca.gov. The CEQAnet NOD gives approval June 29, 2021; the 2025 memo treats Ord. 30646 as the rezoning. | https://sanjose.legistar.com/LegislationDetail.aspx?ID=9356&GUID=DD9ABCD2-ABAE-458F-9C21-4CB6528F7B4D ; https://ceqanet.lci.ca.gov/2018082005/4 ; https://legistar.granicus.com/sanjose/attachments/78a6d04f-bc8f-4766-88eb-08854d2b0a74.pdf | item (e); NOD; memo p. 2 | "(e) Ordinance No. 30646 ... [Passed for Publication on 6/29/2021- Item 10.5(b) - (21-1627)]"; "Approved On 6/29/2021" |
| V new development application since March 2025 | UNCONFIRMED (none found) | No planning permit on APNs 254-17-052, -053, -007, -084, -095 in the city's planning data for filings Apr 10–Aug 7 and Sept 8–Oct 5, 2026. No Legistar item since the May 13, 2025 report. Gaps: Mar 2025–Apr 2026 and Aug 8–Sept 7, 2026. | https://data.sanjoseca.gov/dataset/last-60-180-days-planning-permits ; https://data.sanjoseca.gov/dataset/last-30-days-planning-permits | APN filter | — |
| V height diagram vs the adopted plan | UNCONFIRMED | The adopted plan's Fig. 5-4 and Fig. 3-3 aren't in Legistar; the Ch. 3 text there refers to them. None of the nine June 22–29, 2021 Council memos mentions height. | https://legistar.granicus.com/sanjose/attachments/6a470a5f-c429-4338-a04a-8e4af2e07c00.pdf | Ch. 3 pp. 14–15 | "See Figure 5-4 Building Heights Diagram in Urban Design Chapter" |

**Proposed data changes (berryessa-flea-market)**
- No field changes.
- **verify:** application item becomes "...(city planning data show none for the site's parcels in filings Apr 10–Aug 7 and Sept 8–Oct 5, 2026)".
- **Lead:** a search result says the City's Office of Economic Development page (sjeconomy.com, 403 here; not a .gov host, so it would need Matthew's approval) reports the owner's Oct 2025 quarterly report.