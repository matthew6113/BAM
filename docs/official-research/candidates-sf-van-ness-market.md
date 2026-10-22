# Official-source findings: towers at Market Street and Van Ness Avenue (San Francisco)

Checked 2026-10-19 against documents downloaded and read in full text (local copies in
`data/raw/official/10-south-van-ness/`, `data/raw/official/one-oak/`, `data/raw/official/98-franklin/` and
`data/raw/official/30-van-ness-recheck/`, git-ignored), and live queries of DataSF (development pipeline
`6jgi-cpb4`, 2026 Q2 snapshot; Planning records `qvu5-m3a2` and `y673-d69b`; building permits `i98e-djp9`; DBI
inspections `vckc-dh2h`; DBI complaints `gm2e-bten`; parcels `acdm-wktn`; height and bulk districts `h9wh-cg3m`) and
CEQAnet. Page numbers are PDF page numbers.

Matthew said on 2026-10-19 that there is a tower going in "down near Van Ness and Market". `30-van-ness` is
already on the map (paused). The pipeline has two more approved towers at the intersection: **10 South Van Ness**,
a 67-story tower on the former San Francisco Honda dealership block (most likely the one he means), and **One
Oak**, a 400-ft tower across Market Street from it. Both are recommended.

Hosts: none to add. Every source is on `sfplanning.org`, `sfplanning.s3.amazonaws.com` (SF Planning's document
store, the S3 copy of `commissions.sfplanning.org`, which this session couldn't reach), `data.sf.gov` or
`ceqanet.lci.ca.gov`.

What couldn't be reached (all refused by this session's proxy): SF Planning's 2023+ packets and minutes
(`citypln-m-extnl.sfgov.org`), the Board of Supervisors (`sfbos.org`, Legistar), the California Transportation
Commission (`catc.ca.gov`), the press. So the 2026 One Oak motions and plans, the 10 South Van Ness approval letter
and plans, and the One Oak zoning ordinance weren't read.

URL shorthand:
- PRJ(n) = `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=n`; REC(n) =
  `https://data.sf.gov/resource/y673-d69b.json?record_id=n`; DBI(n) =
  `https://data.sf.gov/resource/i98e-djp9.json?permit_number=n`; INSP(n) =
  `https://data.sf.gov/resource/vckc-dh2h.json?reference_number=n`; PIPE(b) =
  `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=b`
- AG1107 = `https://sfplanning.org/sites/default/files/agendas/2024-11/20241107_cpc%20(ID%201480316).pdf`
  (Planning Commission agenda, Nov 7, 2024)
- AG0119 = `https://sfplanning.org/sites/default/files/agendas/2023-01/20230119_cal%20%28ID%201350880%29.pdf`
  (agenda, Jan 19, 2023)
- AG0319 = `https://sfplanning.org/sites/default/files/agendas/2026-03/20260319_cpc%20%28ID%201559820%29.pdf`
  (agenda, March 19, 2026)
- MIN0521 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200521_cal_min.pdf`; MIN0611 =
  `.../20200611_cal_min.pdf`; MIN0714 = `.../20220714_cal_min.pdf` (Planning Commission minutes)
- PKT2020 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2009.0159DNXCUA-02.pdf` (One Oak, packet
  for the Jan 16, 2020 hearing, 192 pp.: executive summary, draft motions, Exhibit B plans approved in 2017, the
  2018 note to file, the 2017 EIR appeal response, and Motions 19943 and 19944 as adopted on June 15, 2017)
- CQ10 = `https://ceqanet.lci.ca.gov/2017072018` (10 South Van Ness Avenue Mixed-Use Project, NOP, Initial Study
  `/2`, Draft EIR); CQ1O = `https://ceqanet.lci.ca.gov/2012102025` (One Oak EIR)

## Summary

| project | stage | size (official) | recommendation |
|---|---|---|---|
| 10 South Van Ness (`10-south-van-ness`) | entitled | 67 stories, 921 homes, 2,360 sq ft retail, 1.17 acres; height not confirmed officially | **include**, boundary only |
| One Oak (`one-oak`) | entitled | 41-story tower, 400-ft roof (436 ft to the screen), 14-story 139-ft podium, 541 homes, ~508,000 sq ft, 0.42 acres | **include**, boundary + illustrative massing |
| 98 Franklin Street | entitled (2020; height increase pending a development agreement) | 36 stories, about 365 ft, 345 homes over a high school | lead, not added |
| `30-van-ness` (on the map) | paused | — | no change since Oct 12 |

---

## 10-south-van-ness

Recommendation: **INCLUDE** (Matthew's call; stage `entitled`), **boundary only for now**. This is the tower at
"Van Ness and Market" the press calls the city's future third-tallest. SF Planning's record shows a streamlined
(SB 423) approval with an approval letter issued for a 67-story, 921-home building. No official document that
could be opened gives its height, so no massing is drawn; the 2020 design (55 stories, 590 ft) is superseded and
isn't drawn either.

Documents read:
- PRJ(2024-008986PRJ), REC(2024-008986PPS), REC(2024-008986TDM) and the other Planning records on block 3506
  lots 003A and 004 (`y673-d69b` by block/lot, 2023–2026).
- PRJ(2015-004568PRJ) and its child records (ENV, DNX, CUA, VAR, SHD, -02 records, MCM).
- PIPE(3506004) (2026 Q2).
- AG1107 (item 14, p. 6); AG0119 (items 13a–13d, pp. 7–8).
- MIN0521 (item 23, p. 19); MIN0611 (items 16a–16e, pp. 12–14); `.../20200604_cal_min.pdf` (continuance).
- CQ10 project page, NOP (`/1` summary on the project page) and Initial Study record (`/2`).
- DBI(202206176565), DBI(202609047753), all DBI permits on block 3506 since 2019.
- DataSF parcels for block 3506.
- Not used: `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/10%20South%20Van%20Ness_Project%20Sponsor%20Presentation.pdf`
  (the sponsor's 2020 slides; downloaded, a developer document, not cited).

| field | official value | source | verbatim quote |
|---|---|---|---|
| current project | 67 stories, 921 homes, 2,360 sq ft retail, 38,282 sq ft roof-deck open space, 105 parking, 352 bike | PRJ(2024-008986PRJ) `description` | "The proposed project (“Project”) would demolish an existing two-story commercial building and construct a new 67-story mixed-use residential building with ground-floor retail. The Project includes 921 dwelling units and 2,360 square feet of ground-floor retail space, with 38,282 square feet of common usable open space across several roof decks. Finally, the Project includes a 31,561-square-foot two-level basement garage, two off-street loading spaces, 105 off-street car parking spaces, and 352 bicycle parking spaces." |
| approval status | approval letter issued; record opened Mar 4, 2025, closed Aug 18, 2026; decision "Approved" (no decision date in the record) | PRJ(2024-008986PRJ) | `"record_status": "Closed - Approval Ltr Issued"`, `"open_date": "2025-03-04"`, `"close_date": "2026-08-18"`, `"project_decision": "Approved"`, `"sb35": "CHECKED"`, `"state_density_bonus_individual": "CHECKED"`, `"building_permits": "202206176565, 202609047753"` |
| unit fields (disagree with the description) | 1,019 homes, 930 market rate, 89 affordable; unit mix 143/465/144/106 (sums to 858) | PRJ(2024-008986PRJ) | `"number_of_units_prop": "1019"`, `"number_market_rate_units_1": "930"`, `"number_affordable_units_prop": "89"`, `"residential_prop": "1179304"`, `"parking_spaces_prop": "255"`, `"retail_commercial_prop": "11416"` (these look like an earlier version; in `verify`) |
| SB 423 notice of intent | 65 stories, 952 homes, 18,770 sq ft retail | REC(2024-008986PPS) | "This preliminary application serves as the Notice of Intent to submit a project application pursuant to Government Code section 65913.4(b) [and (q)]. ... construct a new 65-story mixed-use residential building with ground-floor retail. The building proposes 952 residential units and 18,770 square feet of retail space." |
| filed application (TDM, cancelled) | 67 stories, 13-story podium, 1,104 homes, 1,491,015 gsf residential | REC(2024-008986TDM) | "construction of a new 67-story mixed-use residential building consisting of a 13-story podium and ground floor retail. The building proposes 1,104 residential units with approximately 1,491,015 GSF of residential uses and 18,568 GSF of ground-floor retail." |
| informational hearing | Nov 7, 2024: SB 423, State Density Bonus, 65 stories over a 13-story podium, ~1,492,000 gsf residential, 952 homes (73 affordable); NOI filed Oct 2, 2024 | AG1107 p. 6 (item 14) | "Informational Presentation for the proposed construction of a housing development project pursuant to Government Code Section 65913.4 (SB 423), in an area subject to Government Code section 65913.4(q). The Project would utilize the State Density Bonus Law to demolish the existing two-story commercial building and construct a 65-story mixed-use residential building with a 13-story podium containing approximately 1,492,000 gross square feet of residential uses ... a total of 952 dwelling units ... with 73 of the dwelling units provided as affordable units. ... The Project Sponsor submitted a notice of intent to construct the project on October 2, 2024." |
| pipeline (2026 Q2) | "BP Filed" on the 2022 site permit application; Planning description of the filed SB 423 project | PIPE(3506004) | `"current_status": "BP Filed"`, `"bpa_no": "202206176565"`, `"has_approved_entitlement": false`, `"description_planning": "... construct a new 65-story mixed-use residential building with ground-floor retail. The building proposes 1,104 residential units and 18,568 square feet of ground retail space."`, `"height_district": "120/400-R-2 / 120-R-2 // 140/590-R-2"`, `"sponsor": "c/o Crescent Haights"` (sic) |
| site | Lots 003A and 004, Block 3506; the triangle bounded by Market, South Van Ness and 12th Street | MIN0611 p. 12 | "located at the southwest corner of the intersection of Market Street and South Van Ness Avenue, bound by those two streets and 12th Street to the west; Lots 003A and 004 in Assessor’s Block 3506" |
| acres, sponsor | 1.17 acres; sponsor 10 SVN, LLC; Honda dealership building | CQ10 `/2` (Initial Study record) | "The project sponsor, 10 SVN, LLC, proposes to redevelop the 1.17-acre triangle-shaped property located at 10 South Van Ness Ave. ... The project site is currently occupied by the San Francisco Honda Dealership, a two story, 30 to 45 ft high building" |
| existing building | 1927, 91,088 gsf, last the San Francisco Honda dealership | MIN0521 p. 19 | "demolition of the existing two-story, 30- to 45-foot-tall, 91,088 gross-square-foot (gsf) historic building, built in 1927 which most recently operated as the San Francisco Honda auto dealership" |
| EIR options (2017) | two 41-story 400-ft towers, or a single 55-story 590-ft variant | CQ10 (NOP) | "Two project design options are being considered: a two tower design with two separate 41-story, 400-ft tall towers on top of podiums; and the single tower project variant with a single 55 story, 590 ft tall tower on top of a podium." |
| FEIR | certified May 21, 2020, Motion 20720 (6–0) | MIN0521 p. 19 | "Certification of the Final Environmental Impact Report ... construction of up to 966 residential units in a mixed-use residential building comprised of a 55-story, 590-foot-tall tower over a single podium"; "ACTION: Certified AYES: Diamond, Fung, Imperial, Johnson, Koppel, Moore MOTION: 20720" |
| 2020 approval | June 11, 2020: CEQA findings 20741, shadow 20742, DPA 20743, CUA 20744 | MIN0611 pp. 12–14 | "construction of a new 55-story, 590-foot tall, mixed-use residential building (approximately 906,811 gross square feet) with 966 dwelling units"; "MOTION: 20741" ... "MOTION: 20742" ... "ACTION: Approved with Conditions AYES: Chan, Diamond, Fung, Johnson, Koppel, Moore NAYS: Imperial MOTION: 20743" ... "MOTION: 20744"; variance: "ZA Closed the PH and indicated an intent to Grant" |
| 2023 modification | Jan 19, 2023: 55 stories, 590 ft roof (610 ft with equipment), 939,570 gsf, 1,012 homes; site permit deadline March 15, 2026 | AG0119 p. 7; PRJ(2015-004568PRJ) | "construction of a new 55-story building reaching a roof height of 590 feet tall (610 feet tall inclusive of mechanical equipment, elevator overrun and rooftop screening). The Modified Project includes a total Gross Floor Area of 939,570 gross square feet ... with a total of 1,012 dwelling units"; record: "Project sponsor proposes that each above-mentioned condition of approval be modified to require a Site or Building Permit to be issued no later than March 15, 2026", `"project_decision": "Approved"`, `"project_decision_date": "2023-01-19"` |
| 2020-design site permit | filed June 17, 2022, never issued: 55 stories, 966 units, $430 million | DBI(202206176565) | "erect 55-stories over 2-basement, mixed use residential building with 966 dwelling units, retail and services use, and parking. ... project will includer merger of lots 004 and 003a on block 3506", `"status": "filed"`, `"number_of_proposed_stories": "55"`, `"estimated_cost": "430000000.0"` |
| demolition | application filed Sept 4, 2026, in triage | DBI(202609047753) | `"permit_type_definition": "demolitions"`, `"permit_creation_date": "2026-09-04"`, "demolish a 2-story, type 1 commercial building.", `"status": "triage"` |
| interim use | event space pending a temporary use authorization | REC(2026-004476GEN) | "Temporary Use Authorization - Seeking approval for the interim use of 10 South Van Ness Ave (Development Site) as a community, cultural and private event space." (status "Submitted") |

Stage reasoning: **entitled**. The current application's record shows an approval letter issued and is closed
(Aug 18, 2026). Nothing has been built or demolished; the demolition permit is only filed. No new site permit
application for the 67-story design appears in DBI's data. The 2020 approvals' site-permit deadline (March 15,
2026) has passed with the 2022 application still "filed", which suggests (but no document says) that the 2020
entitlement has lapsed; in `verify`.

Which design is current: the 2024–2026 SB 423 project. It's a new application (2024-008986PRJ) by the same
sponsor on the same lots, its record is the one the pipeline and DBI's demolition application are tied to, and it
was approved after the 2020 approvals' permit deadline. The 2017 two-tower option (two 41-story, 400-ft towers)
was the EIR's base design but the Commission approved the single-tower variant in 2020; both older designs are
superseded.

Boundary: DataSF parcels, blklot 3506003A and 3506004 (48,969 + 2,766 sq ft as mapped), the lots the minutes and
agendas name; union 51,698 sq ft (1.19 acres) against the CEQA filings' 1.17 acres. Accuracy: official.

Massing: **none**. The height of the approved 67-story building isn't in any document that could be opened (the
approval letter and plans are in Planning's document system on `citypln-m-extnl.sfgov.org`; DBI has no site
permit application for it yet). Drawing the 2020 590-ft design would show a superseded building, and taking the
height from the press is not allowed. When the approval letter, plans, a site permit or the CTC item can be read,
add `massing_10_south_van_ness.py` (the 13-story podium in the TDM record is the only massing detail on record).

Press-only (in `reported`; the articles couldn't be opened here, so these are from search-result excerpts and
must be checked before any use): approved in December 2025 as a 67-story, about 820-ft tower with 1,019 homes,
"the city's third-tallest" (`https://sfstandard.com/2025/12/31/plans-approved-third-tallest-building-san-francisco/`,
`https://sfyimby.com/2025/12/67-story-skyscraper-approved-for-10-south-van-ness-avenue-san-francisco.html`); a
revised approval in September 2026 cut it to 921 homes at the same height and extended the entitlement to August
2029 (`https://sfyimby.com/2026/09/approval-for-revised-10-south-van-ness-avenue-san-francisco.html`); developer
Crescent Heights; construction start expected 2027.

Open items:
- The tower's height and the exact date and terms of the approval (approval letter not reachable).
- 921 vs 1,019 homes, and how many are affordable (89 in the unit fields).
- Whether the 2020 approvals lapsed.
- Not opened: California Transportation Commission, May 2026 meeting, item 2.4c.(1), Caltrans' request to
  directly negotiate a tieback airspace lease with the developer under South Van Ness Avenue (US 101):
  `https://catc.ca.gov/-/media/ctc-media/documents/ctc-meetings/2026/2026-05/59-2-4c1-a11y.pdf` (the host is
  refused by this session's proxy). A search excerpt describes it as an 800-ft tower with 849 units, construction
  from Q1 2027, about 180 tieback rods reaching 53 ft into the State Route 101 right of way, and a $180,000 fee;
  none of that is used until the document itself is read. If it is, it's an official (.ca.gov) source for the
  height.
- Photo: not searched.

---

## one-oak

Recommendation: **INCLUDE** (stage `entitled`). It's an approved 400-ft tower on the Market Street corner across
from 10 South Van Ness and 30 Van Ness, with 541 homes; smaller than the usual bar, but it is one of the "large
towers" at Van Ness and Market Matthew asked about, and the official record is complete enough to draw it.

Documents read:
- AG0319 (items 7a–7e, pp. 4–5).
- PRJ(2024-005509PRJ) and its child records REC(2024-005509ENV), DNX, VAR, TDM, CUA, GPA, MAP, PRV, SHD.
- PIPE(0836001); the height and bulk layer (`h9wh-cg3m`) at each of the five lots.
- MIN0714 (items 12a–12d, pp. 10–12), `.../20220616_cal_min.pdf` and `.../20220630_cal_min.pdf` (continuances).
- PKT2020: executive summary and draft motions (pp. 1–10), Exhibit B plans approved in 2017 (pp. 40–65; level 1
  p. 48, tower plan measurement p. 45, amenity level 14 p. 52, typical lower tower p. 53), Motion 19943 (pp.
  109–158) and Motion 19944 (pp. 159–192).
- CQ1O (NOP record); the 2016 Draft EIR (`https://sfplanning.s3.amazonaws.com/sfmea/2009.0159E_DEIR.pdf`) and
  the 2017 FEIR certification packet (`https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2009.0159E.pdf`)
  were downloaded and searched for the site area and bulk, not cited.
- DBI permits on block 0836 lots 001–005.

| field | official value | source | verbatim quote |
|---|---|---|---|
| project (2026) | ~508,000 sq ft, 541 homes; 14-story podium, ~139 ft; 41-story tower, 400 ft roof (416 ft with mechanical, 436 ft with overrun and screening) | AG0319 p. 4 (item 7b; repeated in 7c–7e) | "construct a new, approximately 508,000-square-foot residential building with a tower over podium design containing 541 dwelling units. The podium portion of the building is 14 stories high, with a roof height of approximately 139 feet, while the tower extends to 41 stories, reaching a roof height of 400 feet (or approximately 416 feet inclusive of mechanical equipment, and 436 feet tall inclusive of elevator overrun and rooftop screening)." |
| parking, bikes, plaza | 135 parking, 3 car share, 1 freight + 2 service loading, 210 Class 1 + 27 Class 2 bikes; Oak Plaza in Oak Street | AG0319 p. 4 | "In total, the Project includes 135 off-street accessory parking spaces, three car share spaces, one off-street freight loading space, two off-street service loading vehicle spaces, as well as 210 Class 1 and 27 Class 2 bicycle parking spaces. To further activate the ground floor experience, the Project would construct a public plaza and shared public right-of-way within a portion of the Oak Street (Oak Plaza)." |
| ground floor, Muni elevator, basements | community room, leasing, lobby; Muni elevator kept and enclosed; three basement levels | PRJ(2024-005509PRJ) | "Three underground floor levels accommodate area for accessory off-street parking spaces, Class 1 bicycle parking, and MEP ... The ground floor will contain a community room and leasing office, residential lobby ... the existing on-site Muni elevator will remain in its current location, and a new weather protective enclosure will be constructed around it." |
| site | Lots 001–005, Block 0836, north side of Market between Oak and Van Ness | AG0319 p. 4 | "1500-1540 MARKET STREET (AKA “ONE OAK”) – north side between Oak Street and Van Ness Avenue; Lots 001, 002, 003, 004, and 005 in Assessor’s Block 0836 (District 6)" |
| lot area | about 18,219 sq ft | PKT2020 p. 117 (Motion 19943) | "The Project Site has a lot area ofapproximately 18,219 squarefeet." (OCR spacing as in the scan) |
| CEQA (2026) | addendum to the 2017 FEIR published March 4, 2026 | AG0319 p. 4 (item 7c); PRJ(2024-005509PRJ) | "On June 15, 2017, the FEIR was certified by the Planning Commission through approval of Motion No. 19938. On March 4, 2026, the Planning Department published an Addendum to the FEIR determining that the FEIR adopted remains valid and that no supplemental environmental review is required."; `"environmental_document_type": "Addendum"`, `"environmental_document_date": "03/04/2026"` |
| approval (2026) | approved March 19, 2026; DPA and shadow records closed approved Apr 2, 2026; variance May 11, 2026 | PRJ(2024-005509PRJ); REC(2024-005509DNX) | `"project_decision": "Approved"`, `"project_decision_date": "2026-03-19"`, `"record_status": "Closed - Approval Ltr Issued"`, `"close_date": "2026-09-14"`; DNX `"record_status": "Closed - Approved"`, `"close_date": "2026-04-02"`. Motion numbers not found (minutes on a blocked host). |
| exceptions (2026) | incl. bulk (Sections 270 and 272), lot coverage, unit mix | AG0319 p. 5; REC(2024-005509DNX) | "with exceptions for useable open space (Section 135); permitted obstructions ... (Section 136); lot coverage (Section 249.33); dwelling unit mix requirements (Section 207.6); volumetric limitations for roof enclosures and screens (Section 260); and bulk (Sections 270 and 272)" |
| bigger footprint | the 2026 design enlarges the podium's and the tower's footprints | REC(2024-005509PRV) | "As part of this modification, Project Sponsor seeks to increase the podium height from 120 feet to 140 feet and increase the footprint (and massing) of both the podium and the tower." |
| change from 2022 | 460 → 541 homes; GFA 461,727 → 510,569; 40 → 41 stories, same height | REC(2024-005509ENV) | "The modified project seeks to increase the total residential unit count from 460 to 541 units within a 41-story residential building, and increase GFA by 10.5% from 461,727 to 510,569. The increase in stories from 40 to 41 will not result in a height change. The total rooftop is 400' with crown reaching 437 feet to cover elevator overrun." |
| zoning change | Board file 260083; Planning's MAP record closed approved June 15, 2026; layer now shows 140/400//140/450-R-4 on lots 001–005 | AG0319 p. 4 (item 7a); REC(2024-005509MAP); `h9wh-cg3m` | "an ordinance, sponsored by Supervisor Dorsey, amending the Zoning Map ... to increase the allowed height for the podium of the building, from the current base height limit of 120 feet to 140 feet"; MAP `"record_status": "Closed - Approved"`, `"close_date": "2026-06-15"`; layer `"height": "140/400//140/450-R-4"` at all five lots (the pipeline's 2026 Q2 row still says 120/400-R-2). Ordinance number not found. |
| units by type | 107 studios, 266 one-bedroom, 168 two-bedroom; all 541 market rate in the record | PRJ(2024-005509PRJ) | `"residential_studio_prop": "107"`, `"residential_1br_prop": "266"`, `"residential_2br_prop": "168"`, `"number_of_market_rate_units": "541"` |
| sponsor | Emerald Fund, Inc. | PRJ(2024-005509PRJ); PIPE(0836001) | `"applicant_org": "Emerald Fund, Inc."`; `"sponsor": "Emerald Fund, Inc."` |
| 2022 approval | July 14, 2022: 40 stories, 400 ft roof, 460 homes; Motions 21139 (CEQA), 21140 (shadow), 21141 (DPA), 4–3 | MIN0714 pp. 10–12 | "construct a new 40-story building reaching a roof height up to 400 feet tall (approximately 416 feet tall inclusive of mechanical equipment, or 437 feet tall inclusive of elevator overrun and rooftop screening) ... with a total of 460 dwelling units"; "MOTION: 21139" ... "MOTION: 21140" ... "ACTION: Approved with Conditions AYES: Diamond, Fung, Koppel, Tanner NAYS: Ruiz, Imperial, Moore MOTION: 21141" |
| 2017 approval | June 15, 2017: FEIR Motion 19938; DPA Motion 19943; CUA Motion 19944; 40 stories, 400 ft, 304 homes | PKT2020 pp. 109–111, 145 | "TO CONSTRUCT A 40-STORY,400- FOOT-TALL RESIDENTIAL BUILDING WITH 304 DWELLING UNITS"; "The FEIR was certified by the Commission on June 15,2017 by adoption of its Motion No. 19938."; p. 145: "the Planning Commission ADOPTED the foregoing Motion on June 15, 2017." |
| 2017 tower bulk | average floor 9,637 sq ft; max plan length 90 ft 4 in, diagonal 144 ft | PKT2020 p. 125 | "The maximum diagonal dimension for the project is 144feet whereas the maximum plan length is 90feet,4 inches. The average floor area of the tower is 9,637 squarefeet" |
| site permit | 2016 application for the 2017 design, still "filed"; no construction permits | DBI(201612094535) | "erect 40 stories of 300 dwelling unit mix use type one contration.", `"status": "filed"`, `"filed_date": "2016-12-09"` |

Stage reasoning: **entitled**. Approved by the Planning Commission on March 19, 2026 (Planning's record), the
zoning change is reflected in the City's height map, and nothing has been permitted or built; the only site
permit application is the 2016 one for the 2017 design.

Boundary: DataSF parcels, blklot 0836001–0836005 (1,095 + 1,426 + 1,774 + 4,594 + 9,504 sq ft as mapped), the
lots the 2017 motions and the 2026 agenda name; union 18,388 sq ft (0.42 acres) against Motion 19943's 18,219 sq
ft. Oak Plaza (in the Oak Street roadway) is not drawn. Accuracy: official.

Massing (`pipeline/bam_pipeline/sites/massing_one_oak.py`, `data/massing/one-oak.geojson`): two volumes, both
`entitled`, illustrative.
- Tower, 400 ft (2026 roof height; 416/436 ft to equipment and screening in the note): the outline of the level-14
  floor on PKT2020 p. 52 ("Amenity plan level 14", Snøhetta, May 15, 2017), the union of its filled rooms, cores
  and corridors (about 9,210 sq ft as drawn; Motion 19943's 2017 average tower floor is 9,637 sq ft). The plan's
  four property-line corners, read from the ends of its dimension lines (177'-0" Oak Street, 39'-2" Van Ness
  Avenue, 166'-8" west side; the sheet reads to within 0.3 ft of each), were matched to the parcel corners:
  similarity RMS 0.22 m, scale 0.2774 ft/pt against the plan's 0.2778 (1" = 20').
- Podium, 139 ft (2026): the rest of the lots (about 9,180 sq ft).
- Caveat, stated in the file's summary, the tower's note and the record's `massingNotes`: the outline is the 2017
  design's. The 2026 plans couldn't be opened, and the 2026 interdepartmental review record says the modification
  increases "the footprint (and massing) of both the podium and the tower", so the real tower is wider than drawn.
  **Option for Matthew / the lead:** if a 2017 outline under 2026 heights is too loose, drop
  `data/massing/one-oak.geojson` and show the boundary only until the 2026 plans can be read.

Press-only: none recorded (the press wasn't reachable; search excerpts mention a new owner after a loan default,
not used).

Open items: the 2026 motion numbers; the zoning ordinance's number and date (Board file 260083); the 2026 plans and
tower footprint; affordable housing compliance (all 541 homes market rate in the record; a 2024 variance record
mentions "an in-lieu fee reduction to 16.4%"). Not opened: the Board's 2017 decision on the EIR appeal
(`https://www.sfbos.org/sites/default/files/m17-0150.pdf`, blocked host); the 2022 and 2026 packets
(`citypln-m-extnl.sfgov.org`). Photo: not searched.

---

## 30-van-ness: recheck since 2026-10-12 (report only, record not edited)

Nothing new. DBI permits on 0835/004 (`i98e-djp9`, 208 rows): no permit filed, issued or changed since the last
check (latest status change Jan 27, 2026, a cancelled 2008 fire alarm permit). Inspections under the site permit
INSP(201912139539): the latest is still the site verification of Aug 18, 2026 (the dataset now lists 4 rows:
2024-01-16, 2025-07-15, 2026-02-11 with no result, 2026-08-18). No inspections on the parcel after Aug 1, 2026
other than that one; no DBI complaints since June 1, 2026 (`gm2e-bten`). Planning: no new record on the lot in
2026; 2024-008290OFA still "Accepted" (outcome still unknown) and 2024-008290MAP still "Under Review";
2024-008290PRJ still "Under Review" with decision "Approved". No 2026 Planning Commission agenda (Jan–Oct) lists
30 Van Ness.

---

## Leads not added

- **98 Franklin Street** (block 0836 lots 008, 009, 013; next to One Oak): a 36-story mixed-use building, about
  365 ft, 345 homes over the French American International School's high school; approved May 28, 2020
  (PRJ(2016-014802PRJ), "Approved", 2020-05-28; Hub Plan EIR, SCH 2018052060). A development agreement to raise
  the height limit to 400 ft and allow up to 385 homes (Board file 221163) is still "Under Review"
  (REC(2016-014802DVA)), though the related zoning records closed approved in July–August 2023
  (REC(2016-014802MAP), REC(2016-014802DNX-02)); addendum REC(2016-014802ENV-02): "Analysis of a 400-foot-tall
  building." Not under construction: site permit DBI(202102184905), "erect new 37 stories 345 residential unit",
  is still "filed" (filed Feb 18, 2021) and INSP(202102184905) returns no inspections. Stage entitled. Recommend
  **hold**: add it with One Oak if Matthew wants every ~350–400 ft tower in the Hub; the 2020 packet and the Hub
  Plan EIR on the S3 store would give geometry.
- **1338 Mission Street** (3508/022): a proposed 30-story, about 327 ft 4 in tower with 287 homes
  (PIPE(3508022), "PL Filed" Aug 25, 2021; PRJ(2021-008648PRJ) "Under Review", but its DNX record was withdrawn in
  2023 and its ENV record cancelled in 2024). Dormant proposal; not added.
- **1965 Market Street** (3534/058): a proposed 23-story, 218-home State Density Bonus project
  (PRJ(2025-001378PRJ), "Under Review"). Below the size of interest; not added.
- **Freedom West** (blocks 0770/0783, 2,537 homes, PIPE(0770027) tracking record 2023-007911PRX): within 1 km of
  the intersection, but it's being researched by another group (its boundary constants are already in
  `official_boundaries.py`); not duplicated here.
- No other pipeline project within 1 km of Market and Van Ness is over 20 stories or 200 ft (DataSF `6jgi-cpb4`,
  `within_circle` 1,000 m, 82 rows).
