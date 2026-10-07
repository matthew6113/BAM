# Candidate projects: Link21 (transbay rail), Valley Link (Tri-Valley rail), San Francisco waterfront flood defenses

Checked 2026-10-07 against official records read in full text. Local copies are in `data/raw/official/link21/`, `data/raw/official/valley-link/` and `data/raw/official/sf-waterfront-flood-defense/` (git-ignored). Page numbers are PDF page numbers.

All three are linear infrastructure, which is new to the map. The record schema has no line geometry: `acres` is null with a note, and the program fields don't apply.

Shorthand:
- BLA = `https://bart.legistar1.com/bart/attachments/` (BART Board Legistar attachments; API `webapi.legistar.com/v1/bart/`)
- VL = `https://www.valleylinkrail.com/_files/ugd/` (Tri-Valley–San Joaquin Valley Regional Rail Authority board packets)
- VL-Feb26 = VL `95df9a_d5454624d39d4a078b0aa7b18dddc57c.pdf` (Feb 11, 2026 packet); VL-May26 = VL `95df9a_1336405d248b467fb082db9ecc4416ae.pdf` (May 13, 2026); VL-Jun26 = VL `8f09e7_9cca9a978bb14766a336566c3710ef3a.pdf` (June 10, 2026); VL-Sep26 = VL `95df9a_af705a6cc23f44438b8f9b29cb18bec9.pdf` (Sept 9, 2026)
- PSR = Port of SF staff report, Aug 7, 2026, item 12A: `https://www.sfport.com/media/11433/download`
- PPT = Port Commission presentation, Aug 11, 2026, item 12A: `https://www.sfport.com/media/11441/download`
- HL = Recommended Plan Highlights, Aug 2026: `https://www.sfport.com/sites/default/files/2026-08/260817_Highlights%20Document_Rec%20Plan.pdf`

| candidate | recommendation | why |
|---|---|---|
| Link21 (new transbay passenger rail crossing) | EXCLUDE (watch list) | Still pre-project planning. The only decision is the train technology (standard gauge, June 2025). There is no alignment, no station list, no proposed project and no environmental document, and federal Corridor ID work isn't expected to start until 2027. MTC removed the second crossing from the $50M RM3 project in June 2026. Every published map is an illustrative concept, and the BART-gauge concepts are now superseded. Drawing any line would invent a boundary. |
| Valley Link (Phase 1A, Dublin/Pleasanton BART to Vasco Road ACE) | INCLUDE | An 11-mile rail line with three stations, about $2.05B (YOE), cleared under CEQA (2024 SEIR) and NEPA (2025 FONSI), with a CM/GC contractor on board for preconstruction (June 2026). Its official schedule runs construction from summer 2029 to opening in summer 2033. A regionally significant BART–ACE link. |
| SF waterfront flood defenses (USACE Waterfront Coastal Flood Study, Port Waterfront Resilience Program) | INCLUDE (if Matthew accepts infrastructure lines) | A 7.5-mile, $17.8B (2026 $) Recommended Plan in a Final Report and EIS published July 31, 2026, the largest public works proposal on the SF waterfront. It is not yet authorized: no Chief's Report and no ROD under the new 35% design rule. Its early pieces are in design. |

---

## link21 (Link21 Program)

Documents read:
- link21program.org: home, `/en/program`, `/en/program/current-planning-activities`, `/en/program/business-case`, `/en/program/concepts`, `/en/about/financial-information` (fetched 2026-10-07; site footer "© 2026")
- BART Board, June 12, 2025, file 25-158 "Link21 Stage Gate 2 Approval": EDD BLA `7feec860-c0c3-412f-92fd-c5578e34b4d1.pdf`; presentation BLA `50b445a1-94c2-4aaa-b78e-dc62917c4e42.pdf`
- BART Board minutes, June 12, 2025 (file "Approval of Minutes of the Meetings of June 12, 2025"): BLA `90a05ac5-aefa-4ad1-8e54-c9cda4578b47.pdf`
- BART OIG, Performance Audit of the Link21 Program (BCA Watson Rice, Dec 19, 2025; Audit Committee Feb 12, 2026, file 26-067): report BLA `d6b91a80-867c-4941-923f-45dbf70d211e.pdf`, cover memo BLA `2d622784-550f-4bdf-af9a-c73f6df37667.pdf`
- BART Board, July 2026, file 26-280, RM3 Transbay Rail Crossing allocation: EDD BLA `8b1f9f4e-69a5-4554-87cf-a2a8a9fbd77c.pdf`
- Capitol Corridor JPA: news release June 19, 2025 `https://www.capitolcorridor.org/blogs/get_on_board/link21update2025/`; CCJPA Board packet Sept 16, 2026 `https://www.capitolcorridor.org/wp-content/uploads/2026/09/Sept-16-2026-CCJPA-Board-Meeting_Agenda-Packet_FINAL.pdf`

| field | official value | source | verbatim quote |
|---|---|---|---|
| what it is | new underground passenger rail crossing between Oakland and SF, plus related network improvements | link21 home; SG2 EDD p.1 | "At the core of Link21 is a new train crossing between Oakland and San Francisco"; "advancing a new underground passenger rail crossing of the San Francisco Bay" |
| phase | Phase 1, Project Identification, since mid-2022 | program page; current-planning page | "Phase 1 Project Identification (We are here)"; "Since mid-2022, we have been in the Project Identification phase, which will take us from concept development to a proposed project for Environmental Review" |
| technology decision | standard gauge (Stage Gate 2); BART Board 9-0, June 12, 2025 | minutes p.9 | "by unanimous vote, the Board approved the Link21 Program staff recommendation to: 1. Advance a standard-gauge crossing between Oakland and San Francisco ... Result: 9-0-0" |
| CCJPA action | CCJPA Board voted the same direction and took over day-to-day management (news release June 19, 2025; management from July 1, 2025) | CC release; CCJPA packet p.63 | "CCJPA has assumed day-to-day management of Link21 as of July 1, 2025" |
| alignment | not defined; to be studied | program page | "Over the next several years, options for new and improved station locations, and track alignment will be further defined to identify the proposed Project" |
| status, Sept 2026 | federal Corridor ID planning waits on a Caltrans–FRA agreement, expected 2027 | CCJPA packet p.63 | "We are waiting for Caltrans and FRA to execute an agreement before we can start work, which is anticipated sometime in 2027." |
| CCJPA budget | $11,276,000 TIRCP for "Planning and implementation strategies for a new Transbay Rail Crossing", projected completion June 2027 | CCJPA packet p.66 | "Link21 / Corridor Identification Program ... June-27 $ 11,276,000" |
| RM3 money | MTC (June 24, 2026) removed the second crossing from RM3 project #13; BART to use the $50M on Transbay Corridor Core Capacity | RM3 EDD p.1–2 | "to provide accommodation of additional Bay Area Rapid Transit District rail service in the Bay Bridge corridor and remove reference to a second transbay crossing"; "On June 24, 2026, the MTC Commission approved the RM3 project scope modifications" |
| cost (crossing) | $18–30B for crossing infrastructure at 1–2% design | concepts page | "Initial cost estimates for Link21 based on 1-2% design show that the new crossing infrastructure (e.g., tunneling, portals, and track systems) is comparable in costs: $18-$30B." |
| cost (connecting network) | standard gauge $15–25B; broad gauge $5–10B | concepts page | "Standard-gauge = $15-25B estimate"; "Broad-gauge = $5-10B estimate" |
| ridership | standard gauge ~90K–115K new daily riders (early evaluation) | concepts page | "Potential new daily riders range with early evaluation from approximately 90K to 115K" |
| spending | $139.5M spent 2017–2025; current funding $156.0M | SG2 presentation p.7 | "Total Spent: $139.5 M"; "Current Funding: $156.0 M" |
| program schedule | Phase 2 (project selection) est. 2029; Phase 3 (delivery) est. 2039 | OIG report p.45 | "Phase 2 – Project Selection (Stage Gate 4 and 5), Estimated Completion 2029"; "Phase 3 – Project Delivery (Stage Gate 6+), Estimated Completion 2039" |
| funding risk | $83M needed by end of 2026 to reach environmental stage; $187M more for project selection; federal funding uncertain | OIG report p.5 | "Link21 needs roughly $83 million by the end of 2026 to reach the environmental stage of Phase 2, and about $187 million more to complete that phase." (estimates as of June 30, 2024) |

Geometry: none is official as an alignment. What exists:
- Six draft concepts (A–F) on the Concepts page, drawn as schematic network maps ("Concepts demonstrate new tracks (thick lines) connecting to existing tracks (thin lines)"). C and D are BART-gauge, so the 2025 decision supersedes them; A, B, E and F are standard-gauge examples ("Example Concepts help to understand trade-offs", SG2 presentation p.15).
- The 2022 Environmental Constraints and Opportunities mapbook (study areas: Transbay Crossing, Southeast SF, Downtown Oakland, Downtown SF), hosted on HNTB's S3 (`hntb-public.s3.amazonaws.com/Link21/ECO-Report/...`). These are study-area corridors, not alignments, and the host is a consultant bucket.

Recommendation: EXCLUDE. The rules decide it: "never invent a boundary" and "Superseded documents aren't drawn as if current". There is no proposed project to draw, and the sponsors say alignment is "Over the next several years". The program is also losing momentum. Corridor ID work is not expected before 2027 (CCJPA, Sept 2026), the second-crossing RM3 money was redirected in June 2026, and the OIG flags that funding beyond Phase 1 "is not secure". What would tip it: a proposed project with an alignment and stations entering environmental review (CEQA NOP or NEPA NOI). Until then, consider a text-only mention or `candidatesNotYetResearched`.

Conflicts with press: CBS/KTVU (2020–21) "by 2040" roughly matches the OIG's Phase 3 estimate of 2039. The "upwards of $30 billion" press figure reflects only the crossing range; the official total for standard gauge is $18–30B plus $15–25B.

Hosts: link21program.org (BART/CCJPA program site), capitolcorridor.org (CCJPA) and bart.legistar1.com / webapi.legistar.com/v1/bart/ (BART) would need adding to `official.ts` if Link21 were mapped. They were not added, since there is no record.

---

## valley-link (Valley Link Rail Project, Phase 1A)

Documents read:
- valleylinkrail.com: `/valleylink-project`, `/environmental-ceqa`, news releases; board packets VL-Feb26, VL-May26, VL-Jun26 (includes the AB 1171 Initial Project Report, PDF pp. 27–41), VL-Sep26; SJCOG $10M release VL `95df9a_0f161a7a5be14083a255266808a38859.pdf`
- getvalleylinked.com (the Authority's environmental and design site): home page
- CEQAnet SCH 2018092027: `https://ceqanet.lci.ca.gov/Project/2018092027` (8 documents); FONSI `https://ceqanet.lci.ca.gov/2018092027/9`
- City of Dublin, `https://dublin.ca.gov/2107/Valley-Link-Rail-Project`: superseded, as it describes the 2019 plan to North Lathrop

| field | official value | source | verbatim quote |
|---|---|---|---|
| Phase 1A | ~11 miles along I-580, Dublin/Pleasanton BART to Vasco Road ACE, third station at Isabel Ave | VL-Jun26 p.30 | "Valley Link Phase 1A would establish approximately 11 miles of new passenger rail along I-580 to connect the existing BART rail system at Dublin/Pleasanton to the existing ACE rail system at Vasco Road in Livermore and includes a third station at Isabel Avenue in Livermore." |
| service | 15-minute weekday headways, six BEMU trains, Livermore OMF | VL-Jun26 p.30 | "The Project will provide weekday service on 15-minute headways operating six (6) battery electric multiple unit (BEMU) rail vehicles" |
| why phased | cost increases at 30% design; Board action June 11, 2025 | VL-Jun26 p.29; VL-May26 p.43 | "Due to cost increases identified as part of the Valley Link Phase 1 project's 30% design and cost estimate update, the Authority Board took action in June 2025 to further phase the delivery" |
| Phase 1B | Southfront Road to Mountain House, 11 miles, funding TBD; still environmentally cleared | valleylink-project page; VL-May26 p.43 | "Phase 1B: Southfront Road Station in Livermore to the Mountain House Community Station (Funding to be determined)"; "The Phase 1B project section (Southfront Road to Mountain House) remains environmentally cleared under CEQA and NEPA." |
| cost | total project budget $2,045.7M YOE; construction and rolling stock $1,676.4M; R/W $172.7M | VL-Jun26 p.39 | "Construction / Rolling Stock Acquisition (CON) $1,676,400"; "Total Project Budget (in thousands) $2,045,700" |
| schedule | 30% design Dec 2026; final design to fall 2028; R/W summer 2027–summer 2029; construction summer 2029 to open summer 2033 | VL-Jun26 p.38 | "Construction (Begin – Open for Use) / Rolling Stock Acquisition (CON) Summer 2029 Summer 2033" |
| schedule (other) | construction anticipated FY 2028–29 | VL-May26 p.43 | "while Phase 1A progresses toward anticipated construction in FY 2028–29" |
| ridership | ~16,000 weekday boardings in 2050 (Phase 1A) | VL-Jun26 p.35 | "Valley Link is estimated to have a 2050 ridership of approximately 16,000 per weekday" |
| CEQA | SEIR for 22-mile Phase 1 certified Oct 23, 2024 (NOD Oct 25) | VL-May26 p.43; CEQAnet | "On October 23, 2024, the Board adopted resolutions certifying the Final Subsequent Environmental Impact Report (SEIR)" |
| NEPA | FTA FONSI May 27, 2025 (CEQAnet received June 4, 2025) | VL-May26 p.43; FONSI p.1 | "on May 27, 2025, the Federal Transit Administration (FTA) issued a Finding of No Significant Impact (FONSI) for the Phase 1 Project" |
| Phase 1A environmental | joint CEQA addendum and NEPA re-evaluation for the 1.5-mile connection, fall 2026 | VL-May26 p.43; VL-Jun26 p.38 | "Staff anticipates completing the approximately 1.5-mile environmental update for the Phase 1A connection (I-580/First Street to Vasco Road) in Fall 2026"; "Certify Joint NEPA Re-evaluation and CEQA Addendum (Phase 1A) September 2026" |
| delivery | CM/GC; Kiewit preconstruction contract (Tier 1, NTE $3M) approved June 10, 2026 | VL-Sep26 p.7 (minutes) | "execute a Contract with Kiewit Infrastructure West Co., ... for a not-to- exceed amount of $3,000,000 for Tier 1 Work" |
| federal | preparing to request entry to FTA CIG Engineering phase | VL-Sep26 p.40 | "in preparation for the Authority's planned request to the Federal Transit Administration (FTA) to enter the Engineering phase of the Capital Investment Grants (CIG) Program" |
| funding to date | MTC $53.8M cumulative (Aug 26, 2026); $44M local and state (ACTC $4M, SJCOG $10M, AB 179 $5M, TIRCP $25M) | VL-Sep26 p.27; VL-Jun26 p.40 | "on August 26, 2026 the Authority secured a cumulative total of $53.8 million from the Metropolitan Transportation Commission"; "the Authority has secured $44 million in local and State funds" |
| construction funding | not secured | VL-Jun26 p.36 | "Potential impediments to project completion, however, are tied to available funds to advance final design and construction of the Project." |
| final-design match | $114.4M match proposed with $6M Alameda CTC CIP request | VL-Sep26 p.37 | "in the amount of$114.4 million anticipated to be from source(s) including $98.7 million of MTC bridge tolls" |
| litigation | Alameda County Taxpayers Association v. Authority (RG21110126) pending | VL-Sep26 p.36 | "except for the pending action, Alameda County Taxpayers Association et. v. Tri-valley—San Joaquin Valley Regional Rail Authority et al." |
| earlier plans | 2021 EIR: 42 miles, 7 stations to North Lathrop; April 2023 LPA: 22-mile Phase 1 | environmental-ceqa page; VL-Jun26 p.45 | "the full 42-mile, 7-station passenger rail system"; "April 2023: The Authority Board adopted the 22-mile Valley Link Phase 1 project alignment" |

Official stage: entitled (approvals in hand; design underway; no construction). The CEQA addendum for the Phase 1A connection is still pending, and construction money is not secured.

Geometry: no official GIS found. Trace from:
- VL-Jun26 Figure 3 (Phase 1A and 1B alignments, p.30) and Figure 4 (I-580 to Vasco Road connection, p.31). Figure 2 (the 22-mile 2024 SEIR/2025 FONSI alignment, p.29) gives context for 1B.
- CEQAnet SCH 2018092027 doc 6 (Draft SEIR, Apr 2024) and doc 8 (EA, Dec 2024): full alignment figures.
- End points from official stop data: Dublin/Pleasanton BART, BART GTFS stops.txt (`L30-1`, 37.701610, -121.899245); Vasco Rd ACE, Caltrans California Transit Stops (CC BY; stop `VAS`, 37.697062, -121.717655). The I-580 median portion could be snapped to Caltrans' State Highway Network.

Conflicts with press: Wikipedia and Hacienda (2026) say costs "doubled to about $4.4 billion" by 2025, that Phase 1A is "fully funded", and that construction runs 2028–2031. None of these appear in Authority documents. The official record has $2.05B YOE, construction funding not secured, and construction from summer 2029 to summer 2033. These are recorded in `reported`.

Internal inconsistency: one milestone list (VL-Jun26 p.45) says "May 2024: FTA approved NEPA EA FONSI". The FONSI, the CEQAnet entry and other Authority documents say May 2025.

Hosts added to `src/projects/official.ts`: `valleylinkrail.com` and `getvalleylinked.com` (Tri-Valley–San Joaquin Valley Regional Rail Authority). acerail.com (SJRRC) returns 403 to scripts.

Draft record: `scratchpad/records/new/valley-link.json` (passes `tests/record-check.test.ts`).

---

## sf-waterfront-flood-defense (San Francisco Waterfront Coastal Flood Study, Recommended Plan)

Documents read:
- PSR (Port staff report, Aug 7, 2026, 22 pp.), PPT (Aug 11, 2026 presentation, 23 pp.), HL (Recommended Plan Highlights, Aug 2026, 35 pp.)
- sfport.com `/wrp`, `/wrp/embarcadero-seawall-resilience`, `/wrp/library`
- 2024 Draft Plan: Port presentation `https://sfport.com/media/9510/download`; Capital Planning Committee, Mar 18, 2024, `https://www.onesanfrancisco.org/sites/default/files/2024-03/Agenda%20item%207%20-%20SF%20Waterfront%20Flood%20Study.pdf`
- SF Capital Plan FY2026–35 (May 2025), full PDF: `https://onesanfrancisco.org/sites/default/files/inline-files/Full%20Capital%20Plan%20FY2026-FY2035_0.pdf`
- Federal Register API listing: NOA 2026-15536 (July 31, 2026), NOI 2023-15898 (July 27, 2023). The page text is behind a CAPTCHA, so only the listing was read.
- DataSF "Port Jurisdiction" `jmv6-xier` (GeoJSON saved)

| field | official value | source | verbatim quote |
|---|---|---|---|
| extent | Port's 7.5-mile jurisdiction, Aquatic Park to Heron's Head Park | HL p.9; PSR p.1 | "within the Port of San Francisco's jurisdiction, from Aquatic Park to Heron's Head Park"; "the Port's entire 7½ mile jurisdiction" |
| final report | USACE NOA July 31, 2026 | PSR p.2; HL p.9 | "On July 31, 2026, USACE published a notice of availability of the San Francisco Waterfront Coastal Flood Study Final Integrated Feasibility Report and Environmental Impact Statement" |
| cost | $17.8B (2026 $): $14.1B design and construction + $3.7B real estate; Draft Plan $13.5B (2024 $) = $14.7B (2026 $) | PSR p.2, p.6; PPT p.14 | "to $17.8 billion ($14.1 billion design and construction cost, and $3.7 billion real estate cost)" |
| federal share | up to 65% if Congress approves | PPT p.7; HL p.4 | "if approved by Congress, the Federal government may pay up to 65% of the construction cost" |
| design maturity | 20%; conditionally certified Class 3 estimate | PPT p.14; HL p.19 | "The Recommended Plan has a 20% design maturity and a USACE conditionally certified Class 3 cost estimate." |
| no Chief's Report / ROD | 35% design rule; Port told it won't get a Chief's Report; no ROD | PSR p.9, p.10 | "He also confirmed that the Port will not receive a Chief's Report from LTG Graham due to the new 35% design maturity requirement."; "the Recommended Plan has not received a Record of Decision on the NEPA analysis" |
| cost of 35% design | $200–400M, several years | PSR p.12 | "An effort to develop a 35% design covering the full 7.5 miles would cost a projected $200-400 million and would take several years." |
| protection levels | Embarcadero 3.5 ft SLR; South Beach/Mission Bay 1.5 ft; later actions to 7 ft | HL pp.12, 24, 27 | "focuses on raising the seawall at the shoreline edge to defend against 3.5 feet of sea level rise"; "Defends against 3.5 to 7 feet of sea level rise" |
| key elements | 2.8 miles of nature-based features; Ferry Building seawall realigned bayward; 2 closure structures | PSR p.5–6 | "2.8 miles of natural and nature-based features across the Study area" |
| early actions | Rincon Park/Embarcadero (Pier 14–22.5, Downtown Coastal Resilience Project), Mission Creek, Islais Creek | PSR p.6 | "Early Resilience Actions, including Rincon Park/Embarcadero Shoreline (Pier 14 to Pier 22.5 – Downtown Coastal Resilience Project) and portions of Mission Creek and Islais Creek" |
| projects in design | Downtown (Broadway–Harrison), South Beach (Harrison–Townsend; $7.8M Coastal Conservancy grant) | PSR p.12 | "The Downtown Coastal Resilience Project will improve flood and earthquake resilience along the Embarcadero between Broadway and Harrison streets." |
| local design path | Section 221 MOU, Resolution 24-62 (Dec 10, 2024); design RFPs planned Aug 2026 | PSR p.11 | "On December 10, 2024, by Resolution 24-62, the Port Commission approved the Executive Director to enter a USACE Design and Construction Memorandum of Understanding" |
| timeline (approx.) | seek approval and funding 2026–~2030; phased construction ~2030 onward | PPT p.8; HL p.9 | "Note: Dates are approximate and subject to change." |
| study start | Congressional new start, 2018, $500,000 | PSR p.4 | "secured a new start with an initial $500,000 appropriation" |
| next | WRDA 2026 provisions; $10M FY2027 E&W request for Downtown design | PSR pp.13–14 | "submitted a $10 million community funding request to pay for design of the Downtown Coastal Resilience Project" |
| seawall bond | $425M Seawall Earthquake Safety Bond, 2018; $350M Waterfront Safety & Climate bond planned Mar 2028 | Capital Plan pp.19, 65 (Table 1.5) | "$425 million Seawall Earthquake Safety Bond passed by voters in 2018"; "Waterfront Safety & Climate G.O. Bond planned for 2028" |

Official stage: entitlement. Federal environmental review and the feasibility study are complete, but there is no decision (ROD or Chief's Report) and no authorization. "Proposed" would understate the study's status, and "entitled" would overstate it.

Geometry:
- No official line GIS of the Recommended Plan. The Final Report is on `https://www.swt.usace.army.mil/Library/Docs-and-Comms/`, and USACE hosts (spn., swt.) return 403 to scripts. The reach maps in HL (Fig. 2.2 jurisdiction p.10, Fig. 2.7 subreaches p.12, Fig. 2.8 early action areas p.13, section 3 reach maps pp.21–30) and the PPT phasing map (p.13) are the trace sources.
- DataSF "Port Jurisdiction" (`jmv6-xier`, MultiPolygon, 39 parts, updated 2023-10-19) is the official study-area polygon, but it includes piers and seawall lots, so it is context, not the defense line. License isn't stated in the metadata (DataSF default ODC PDDL; confirm). Also on DataSF: "100-Year Storm + 24\" Sea Level Rise" (esku-ejgv) and the 108" Inundation Vulnerability Zone (92e4-7ptg).
- Approximate center: midpoint of the Port Jurisdiction bounding box (-122.3964, 37.7632).

Recommendation: INCLUDE, at the line-infrastructure level, if Matthew wants infrastructure on the map. At $17.8B it is far above the bar, and it is an adopted federal–city recommendation, not a concept. Draw the Port shoreline line as "Approximate alignment", and possibly highlight the two projects in design. The caveat for the panel is that it has no Congressional authorization and the timing is open.

Conflicts with press: the SF Examiner (Jan 2025) said the plan would go before Congress in 2026. That is superseded, because no Chief's Report was sent (in `reported`). KQED's "$17 billion" headline rounds the official $17.8B.

Hosts: all sources are on sfport.com, onesanfrancisco.org, data.sfgov.org and federalregister.gov, all already accepted.

Draft record: `scratchpad/records/new/sf-waterfront-flood-defense.json` (passes `tests/record-check.test.ts`).
