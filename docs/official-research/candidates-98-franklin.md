# Official-source findings: 98 Franklin Street (San Francisco)

Checked 2026-10-19 against documents downloaded and read in full text (local copies in
`data/raw/official/98-franklin/`, git-ignored; the 2020 packet is also pinned in `data/raw/docs/`), and live queries
of DataSF (Planning records `qvu5-m3a2` and `y673-d69b`, every `2016-014802` record and every record on block 0836
lots 008, 009 and 013; building permits `i98e-djp9` and DBI inspections `vckc-dh2h` on the same lots; the
development pipeline `6jgi-cpb4`, 2026 Q2; parcels `acdm-wktn`; height and bulk districts `h9wh-cg3m`) and CEQAnet.
Page numbers are PDF page numbers.

Matthew asked on 2026-10-19 to add 98 Franklin Street, the tower next to One Oak in the Hub (Market Street and
Van Ness Avenue). The earlier Van Ness and Market note (`candidates-sf-van-ness-market.md`) left it as a lead. It's
a single-site project well below the usual 1,000-home bar; it's added because Matthew asked for it.

Hosts: none to add. Every source is on `sfplanning.org`, `sfplanning.s3.amazonaws.com` (SF Planning's document store;
the S3 form of `commissions.sfplanning.org`, which the 2020 agenda links to and which this session can't reach),
`data.sf.gov` or `ceqanet.lci.ca.gov`.

What couldn't be reached (refused by this session's proxy): the 2023 Planning Commission packet
(`https://citypln-m-extnl.sfgov.org/Commissions/CPC/3_30_2023/Commission%20Packet/2016-014802DNX-02PCAMAPDVASHD-02.pdf`,
linked from the March 30, 2023 agenda) and the minutes of that hearing
(`https://citypln-m-extnl.sfgov.org/Commissions/Agenda_or_Minutes/20230330_cal_min.pdf`); the 2023 addendum to the EIR
and the Aug 3, 2023 notice of determination (both `citypln-m-extnl.sfgov.org` shared links on SF Planning's
environmental review documents page); the Board of Supervisors' files 221163 and 221164 (`sfbos.org`, Legistar). So
the 2023 motions, ordinance and plans weren't read.

URL shorthand:
- PKT = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/2016-014802PRJ.pdf` (Planning Commission packet
  for the May 28, 2020 hearing, 375 pp., 32 MB, sha256 `b4f63cd5…60dd`: executive summary pp. 1–3, draft CEQA motion
  pp. 4–36, draft Downtown Project Authorization pp. 37–87, draft shadow motion pp. 88–99, Exhibit B plan set by
  Skidmore, Owings & Merrill dated May 11, 2020 pp. 100–150, MMRP, shadow memo, maps, letters, affidavits). Linked
  from the May 28, 2020 agenda and minutes as `https://commissions.sfplanning.org/cpcpackets/2016-014802PRJ.pdf`.
- MIN0528 = `https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200528_cal_min.pdf`; MIN0521 =
  `.../20200521_cal_min.pdf` (Planning Commission minutes)
- AG0330 = `https://sfplanning.org/sites/default/files/agendas/2023-03/20230330_cal%20%28ID%201361438%29.pdf`
  (Planning Commission agenda, March 30, 2023, items 14a–14d); EV199 = `https://sfplanning.org/event/planning-commission-199`
  (its hearing notice)
- ERD = `https://sfplanning.org/environmental-review-documents?title=98%20Franklin` (SF Planning's environmental
  review documents listing)
- CQ = `https://ceqanet.lci.ca.gov/2018052060` (The Hub Plan, 30 Van Ness Avenue Project, 98 Franklin Street Project,
  and Hub Housing Sustainability District: NOP 5/23/2018, EIR 7/24/2019, NOD received 8/7/2020); DEIR =
  `https://ceqanet.lci.ca.gov/2018052060/2/Attachment/je2iTJ` (Draft EIR Vol. I, July 2019, 858 pp.); NOD =
  `https://ceqanet.lci.ca.gov/2018052060/3/Attachment/XWsd0-` (notice of determination, Aug 7, 2020, 3 pp.)
- PRJ(n) = `https://data.sf.gov/resource/qvu5-m3a2.json?record_id=n`; REC(n) =
  `https://data.sf.gov/resource/y673-d69b.json?record_id=n`; DBI(n) =
  `https://data.sf.gov/resource/i98e-djp9.json?permit_number=n`; INSP(n) =
  `https://data.sf.gov/resource/vckc-dh2h.json?reference_number=n`; PIPE(b) =
  `https://data.sf.gov/resource/6jgi-cpb4.json?blklot=b`

## Summary

| project | stage | size (official) | recommendation |
|---|---|---|---|
| 98 Franklin Street (`98-franklin`) | entitled | 36 stories, 365-ft roof (396 ft 8 in to the screen), 345 homes (69 affordable), ~84,815 sq ft high school, ~524,014 gross sq ft, 0.55 acres; a 2023 modification to 38 stories, 400 ft and 385 homes awaits its development agreement | **include**, boundary + illustrative massing (2020 design) |

---

## 98-franklin

Recommendation: **INCLUDE** (Matthew's call; stage `entitled`). Approved in 2020; the parking lot is still there.

Documents read:
- PKT: executive summary (pp. 1–3), draft Downtown Project Authorization (pp. 37–45, 60–61, 74), plan set (pp.
  100–150; elevations and sections pp. 110–113, lower tower floor plan p. 126, bulk diagram p. 129, Market Street
  elevation p. 136).
- MIN0528 (items 15a–15c, pp. 7–9); MIN0521 (item 20, pp. 9–10).
- AG0330 (items 14a–14d, pp. 9–10); EV199; ERD; the 2023 agendas from January to December on `sfplanning.org` (no
  other 2023 agenda lists 98 Franklin; the April 13, May 11, May 18, June 8 and June 15 regular agendas weren't
  found on the site).
- CQ (project page, the EIR and NOD records), NOD (pp. 1–3), DEIR (Chapter 2, pp. 135–136 and 192–193).
- PRJ(2016-014802PRJ), PRJ(2022-011628PRJ); all fourteen `2016-014802` child records in `y673-d69b`; all other
  Planning records on the three lots (1970–2026); PIPE(0836013) (lots 008 and 009 have no pipeline row).
- DBI permits on the three lots (9 rows) and inspections on them (5 rows, none under the site permit).
- DataSF parcels and height and bulk districts at the three lots.

| field | official value | source | verbatim quote |
|---|---|---|---|
| project (2020) | 36 stories, 365-ft roof, 396 ft 8 in to the screen, ~524,014 gsf, 379,003 gsf housing, 5-story podium with ~84,815 sq ft of school, ~3,229 sq ft retail, 345 homes | MIN0528 p. 7 (item 15a; repeated in 15b, 15c) | "construction of a new 36-story mixed-use building reaching a roof height of up to 365 feet tall (396’8” inclusive of rooftop screening/mechanical equipment). The Project includes a total gross floor area of approximately 524,014 square feet, with approximately 379,003 gross square feet of residential use within a tower situated atop a 5-story podium containing approximately 84,815 gross square feet of institutional use (French American International School), and approximately 3,229 square feet of retail uses on the ground floor." |
| homes, unit mix, affordable | 345 homes: 259 studio or 1-bedroom, 52 two-bedroom, 35 three-bedroom; 69 (20%) below market rate | MIN0528 p. 7 | "The Project would contain a mix of 259 studio and one-bedroom units, 52 two-bedroom units, and 35 three-bedroom units totaling 345 dwelling units, with 20 percent of the total units (69 dwelling units) provided as affordable (Below Market Rate)." |
| affordability level | 50% of area median income | PKT p. 3 | "The Project proposes to satisfy the requirements by providing 20% of the Project’s 345 units (69 units) as affordable to households at 50% of Area Median Income (AMI)." |
| parking | three basement levels, up to 111 parking and 3 car share | MIN0528 p. 7 | "three below-grade levels that would accommodate up to 111 vehicle parking and 3 car share spaces provided for the residential and school uses" |
| floors | homes on floors 7 to 36 | PKT p. 41 | "(at least 345 dwelling units situated on floors 7 through 36)" |
| 2020 approval | May 28, 2020: CEQA findings Motion 20726, shadow findings Motion 20727, Downtown Project Authorization Motion 20728, all 7–0 | MIN0528 pp. 8–9 | "ACTION: Adopted Findings AYES: Chan, Diamond, Fung, Imperial, Johnson, Koppel, Moore MOTION: 20726"; "MOTION: 20727"; "ACTION: Approved with Conditions including minor corrections and cross-references to comply with the HUB Plan AYES: Chan, Diamond, Fung, Imperial, Johnson, Koppel, Moore MOTION: 20728" |
| height district (2020) | 120/365-R-2 (85-X // 120/365-R-2 in the packet) | MIN0528 p. 8; PKT p. 1 | "Market and Van Ness Downtown Residential Special Use District and 120/365-R-2 Height and Bulk District"; "85-X // 120/365-R-2 Height and Bulk District" |
| podium and tower heights | podium 68 ft; tower roof 365 ft | PKT p. 60; plans p. 110 | "The Project would construct a 5-story podium reaching a maximum height of 68’, with a tower reaching a maximum finished roof height of 365’"; sheet 11: "TOP OF PARAPET: 396’-8”", "TOP OF ROOF: 365’-0”", "TOP OF PODIUM ROOF: 68’-0”" |
| tower bulk | average floor 11,577 sq ft, plan length 130 ft, diagonal 170 ft 3.5 in; top third ~5% smaller | PKT p. 61 | "The Project’s tower includes an average floor area of approximately 11,577 sf, while the maximum plan length is 130’ and the maximum diagonal dimension is 170’3.5”, all of which are within the limits established by Code. However, the gross floor area of the top one-third of the height of the tower is only reduced by approximately 5 percent from the maximum floor plates" |
| site | ~23,750 sq ft (0.55 acres), lots 008, 009, 013 of block 0836 | PKT pp. 41, 43 | "The Project Site (“Site”) is an approximately 23,750 square-foot irregular-shaped corner lot located on the east side of Franklin Street, between Market Street and Oak Street, with approximately 142’ of frontage along Oak Street, 54’ of frontage along Market Street, and 154‘ of frontage along Franklin Street. The subject property (Lots 008, 009 and 013 of Assessor’s Block 0836)"; "The Site is 23,750 square feet (0.55 acres) in area." |
| site shape (EIR) | L-shaped; 142 ft on Oak, 54 ft on Market, 125 ft on Franklin | DEIR p. 135 (2-15) | "It is an L-shaped site at the corner of Franklin and Oak streets and bounded by approximately 142 feet of frontage on Oak Street to the north, the 1546–1564 Market Street building (Assessor’s Block 0836/Lot 007) to the east, approximately 54 feet of frontage on Market Street to the south, and approximately 125 feet of frontage on Franklin Street to the west." |
| tower and podium (EIR) | tower in the northwest of the site, 130 × 110 ft; podium 142 × 125 ft, 68 ft | DEIR p. 192 (2-72) | "The podium (floors 1 through 5) would be constructed to the lot lines, while the tower (floors 6 through 36) would be set back about 0 to 10 feet from Franklin Street, about 0 to 10 feet from Oak Street, and about 150 feet from Market Street. The tower would be situated in the northwest portion of the site. The podium would be approximately 68 feet tall at the roofline." ... "the tower would be approximately 130 feet long by 110 feet wide." |
| sponsor (EIR) | Related California and the French American International School | DEIR p. 192 | "The project sponsor for the 98 Franklin Street Project is a partnership between Related California and the FAIS." |
| owner | 98 Franklin Street, LLC | PKT p. 1; AG0330 p. 9 | "Property Owner: 98 Franklin Street, LLC"; "a Development Agreement between the City and County of San Francisco and 98 Franklin Street, LLC" |
| school size (EIR) | up to 440 students | DEIR p. 193 | "when completed, the development would accommodate up to 440 students at the site for the 98 Franklin Street Project" |
| EIR certification | May 21, 2020, Motion 20707 | MIN0521 pp. 9–10 | "THE HUB PLAN, 30 VAN NESS AVENUE PROJECT, 98 FRANKLIN STREET PROJECT, AND HUB HOUSING SUSTAINABILITY DISTRICT ... Certification of the Final Environmental Impact Report"; "ACTION: Certified AYES: Diamond, Fung, Imperial, Johnson, Koppel, Moore MOTION: 20707" |
| City approval date | Aug 3, 2020, after the mayor signed the Hub Plan legislation | NOD p. 2 | "The City and County of San Francisco decided to carry out or approve the project on August 3, 2020, which is the first business day after the mayor signed the legislation on July 31, 2020." (NOD p. 1 lists "Matt Witte, Related California; (98 Franklin Street)" as project sponsor) |
| approval validity | three years to get a site permit, unless extended | PKT p. 74 (draft conditions) | "The authorization and right vested by virtue of this action is valid for three (3) years from the effective date of the Motion. The Department of Building Inspection shall have issued a Building Permit or Site Permit to construct the project and/or commence the approved use within this three-year period, unless an extension is granted by the Zoning Administrator" |
| 2023 modification | 38 stories, 400-ft roof (431 ft 6 in with screen), ~560,543 gsf, 385 homes on floors 6–38, ~84,991 sq ft school, ~2,978 sq ft retail, 110 parking | AG0330 p. 10 (item 14d; same in 14b, p. 9) | "a new 38-story mixed-use building reaching a roof height of up to 400 feet tall (431’6” inclusive of rooftop screening/mechanical equipment) with approximately 560,543 gross square feet, including approximately 416,286 gross square feet of residential use (385 dwelling units situated on floors six through 38) situated atop a five-story podium containing approximately 84,991 square feet of school use (French American International High School) and approximately 2,978 square feet of retail" |
| 2023 zoning change | height district 85-X // 120/365-R-2 → 85-X // 120/400-R-2 | AG0330 p. 9 (item 14a) | "revise Height Map HT07 to change the maximum height at Assessor’s Block 0836, Lots 008, 009, and 013, from 85-X // 120/365-R-2 to 85-X // 120/400-R-2" |
| development agreement | 400-ft limit, 385 homes, land dedication at 600 Van Ness Avenue, fee waivers, five-year vesting | AG0330 pp. 9–10 (item 14c) | "The Development Agreement would enable the modification of the Project to (1) increase the Project’s height limit to 400 feet (excluding permitted rooftop screen/mechanical equipment), (2) increase the number of dwelling units to 385, (3) permit a land dedication to the City of real property at 600 Van Ness Avenue (Block 0763, Lots 006 through 009; the “Affordable Housing Site”) ... (4) waive all but one million dollars ($1,000,000) of the Project’s applicable Market and Octavia Affordable Housing fee ... and waive all of the Project’s applicable Van Ness Residential Special Use District Affordable Housing fee ... and (5) vest the Project’s Approvals for five years following the effective date of the Development Agreement" |
| Board files | 221163 and 221164 | EV199 | "2016-014802DNX-02/PCA/MAP/DVA/SHD/ ENV/VAR: 98 FRANKLIN STREET [Board File Nos. 221163 and 221164]" |
| 2023 record status | MAP and PCA closed approved July 28, 2023; DNX-02 and SHD-02 closed approved Aug 15, 2023; DVA "Under Review" (opened Mar 16, 2023) | REC(2016-014802MAP), REC(2016-014802PCA), REC(2016-014802DNX-02), REC(2016-014802SHD-02), REC(2016-014802DVA) | MAP `"record_status": "Closed - Approved"`, `"close_date": "2023-07-28"`; DNX-02 `"record_status": "Closed - Approved"`, `"close_date": "2023-08-15"`; DVA: "Development Agreement ... the principal change would increase the applicable height limit from 365 feet to 400 feet, which would allow the Project to include up to 385 dwelling units.", `"record_status": "Under Review"` |
| height map now | 85-X // 120/400-R-2 on all three lots | `h9wh-cg3m` | `"height": "85-X // 120/400-R-2"`, `"gen_hght": "400"` (the whole of each lot) |
| 2023 CEQA | addendum for a 400-ft building; NOD for DNX-02 | REC(2016-014802ENV-02); PRJ(2016-014802PRJ); ERD | "Analysis of a 400-foot-tall building. The project proposes an additional 35 feet over what was previously evaluated in the Hub Plan, 30 Van Ness Avenue, 98 Franklin Street, and Hub HSD EIR" (closed "CEQA Clearance Issued" 2025-01-30); PRJ `"environmental_document_type": "Addendum"`, `"environmental_document_date": "03/08/2023"`; ERD: "98 Franklin Street Mixed-Use Project 2016-014802DNX-02 Notices of Determination and Notices of Exemption Notice of Determination 08/03/2023" and "Addendum to Environmental Impact Report – 98 Franklin Street 03/09/2023" |
| pipeline (2026 Q2) | approved May 28, 2020; 345 homes, 69 affordable (on site, very low income) | PIPE(0836013) | `"current_status": "PL Approved"`, `"current_status_date": "2020-05-28T00:00:00.000"`, `"has_approved_entitlement": true`, `"proposed_units": "345"`, `"pipeline_affordable_units": "69"`, `"bmr_units_very_low": "69"`, `"bpa_no": "202102184905"`, `"height_district": "85-X // 120/400-R-2"`, `"sponsor": "J. Abrams Law, P.C."` |
| project record | decision approved 2020-05-28; record closed 2022-07-11; 345 homes (unit-mix fields sum to 385) | PRJ(2016-014802PRJ) | `"project_decision": "Approved"`, `"project_decision_date": "2020-05-28T00:00:00.000"`, `"number_of_units_prop": "345"`, `"number_affordable_units_prop": "69"`, `"residential_studio_prop": "275"`, `"residential_2br_prop": "72"`, `"residential_3br_prop": "38"`, `"residential_prop": "416286"` |
| site permit | filed Feb 18, 2021, still "filed"; 37 stories, 345 homes, $120 million; no inspections | DBI(202102184905); INSP(202102184905) | "erect new 37 stories 345 residential unit, type 1-a construction, two basements, mix use building with private school new building on 3 lots: 0836/13, 08 & 09", `"status": "filed"`, `"filed_date": "2021-02-18T11:34:13.000"`, `"estimated_cost": "120000000.0"`, `"last_permit_activity_date": "2023-07-10T00:00:00.000"`; inspections: `[]` |
| site today | still a commercial parking lot | REC(2026-003860MIS) | "POL referral - Commercial Parking Lot; Recommend approval - Parking Lot use was authorized under Resolution No. 6678, CU71.04. Continuation of legal nonconforming use." (`"project_name": "98 Franklin Street - Tower Valet Parking, Inc."`, closed approved 2026-05-06) |

Other records read (not shown): REC(2016-014802GPR) (General Plan referral for street improvements, opened Aug 22,
2024, "On Hold") still describes the 2020 design ("approximately 524,014 square feet ... the Project would include at
lest 345 residential units on floors 7 through 36"); REC(2021-007798SUB), a 3-lot merger and vertical subdivision,
"ON HOLD 1/6/22 - Waiting for designation of BMR"; PRJ(2022-011628PRJ), a duplicate filing of the 2022 modification
(385 homes, all market rate), cancelled the next day; REC(2016-014802PPA) (2016, "a new 31-story, 320-foot tall
mixed-use project"); REC(2016-014802TDM) and TDM-02, "Under Review". DBI permit 201606109681 on lot 008 was
temporary shoring for One Oak's 2016 design (expired).

Stage reasoning: **entitled**. The Planning Commission approved the project on May 28, 2020, and the City's 2026 Q2
pipeline lists it as approved with an approved entitlement. Nothing has been built: the only construction permit is
the 2021 site permit application, still "filed" with no inspections, and in May 2026 Planning recommended renewing
the lot's parking permit.

Which design is current: drawn as the **2020 design** (365 ft, 36 stories, 345 homes). In 2023 the sponsor sought a
400-ft, 38-story, 385-home version. The Commission heard it on March 30, 2023; Planning's records of the zoning map
and code amendments closed approved on July 28, 2023, its records of the revised Downtown Project Authorization and
shadow findings on Aug 15, 2023, and the City's height map now shows the 400-ft district. But the development
agreement, which the agenda says "would enable the modification", is still "Under Review" in Planning's records three
years later; the agreement is also what would let the project replace its 69 on-site affordable homes with a land
dedication (the 2022 filing lists all 385 homes as market rate). The pipeline and DBI's application still carry the
2020 design, and a 2024 Planning record still describes it. Neither the 2023 minutes, motions, ordinance nor plans
could be opened. So the 2020 approval is the one that can be shown to be in effect, and the 400-ft version is
described in the record and `verify` but not drawn. **Option for Matthew / the lead:** if the Board's adoption of the
agreement can be confirmed, set `TOWER_ROOF_FT = 400` in `massing_98_franklin.py` (the 2023 footprint is unknown;
the 2020 outline would stand in for it), and update the program to 385 homes.

Boundary: DataSF parcels, blklot 0836008, 0836009 and 0836013 (7,505 + 2,665 + 12,212 sq ft as mapped), the lots the
2020 minutes, packet, EIR and 2023 agenda name; union 22,382 sq ft (0.51 acres) against the approval's 23,750 sq ft
(0.55 acres). As mapped: 141.7 ft on Oak Street, 125.0 ft on Franklin Street, 54.2 ft on Market Street, matching the
EIR's frontages (142, 125 and 54 ft); the packet's "154‘ of frontage along Franklin Street" doesn't match either
(probably a typo). Accuracy: official. The boundary is valid and doesn't touch any mapped project: One Oak's lots are
20 m east (lot 007, 1546–1564 Market Street, lies between), 10 South Van Ness 37 m south across Market Street.

Massing (`pipeline/bam_pipeline/sites/massing_98_franklin.py`, `data/massing/98-franklin.geojson`): two volumes,
both `entitled`, illustrative.
- Tower, 365 ft (396 ft 8 in to the screen, in the note): the outline of the "Lower Tower Floor Plan" (PKT p. 126,
  vector, 1/32" = 1'-0"), the closed ring of the sheet's heaviest lines (0.84 pt: the faceted curtain wall and the
  east and west balconies), about 12,430 sq ft as drawn (the approval's average tower floor is 11,577 sq ft; the
  lower floors are the largest, and the balconies are included). The plan's three property-line corners, read from
  the ends of its dimension lines (141'-9" on Oak Street, 125'-0" on Franklin Street, from the Oak and Franklin
  corner; the sheet reads to within 0.05 ft), were matched to the parcel corners: similarity RMS 0.01 m, scale 0.4443
  ft/pt against the plan's 0.4444. The tower's 130'-0" and 110'-0" extents are checked on the same sheet. Nothing
  was trimmed outside the lots.
- Podium, 68 ft: the rest of the lots (about 9,920 sq ft in three parts: the main podium and two thin wedges between
  the tower's inset faces and the Oak and Franklin street lines). The approval describes "a full lot coverage
  podium"; its roof terraces (the Market Street elevation, p. 136, shows a "ROOF TERRACE: 54’-9”" and a 72'-6"
  parapet) aren't drawn.
- Every output polygon is valid (`shape(f["geometry"]).is_valid` checked after rounding); the two volumes don't
  overlap and stay inside the boundary.
- Not used: the executive summary's "approximately 64% of lot coverage" for the tower footprint (64% of 23,750 sq ft
  is about 15,200 sq ft, more than the 130 × 110 ft extent allows), and the Draft EIR's earlier 31-story design.

Press-only: none recorded (the press wasn't searched; nothing needed it).

Open items:
- Whether the development agreement (file 221163) was adopted, and with it the 400-ft, 385-home modification; the
  2023 motions and the zoning ordinance's number and date (file 221164). Not opened: AG0330's packet and the March 30,
  2023 minutes (`citypln-m-extnl.sfgov.org`), the Aug 3, 2023 NOD and the March 2023 addendum (ERD links on the same
  host), the Board's files.
- Whether the 2020 approval is still valid (three years to a site permit unless extended; the 2023 agreement would
  have vested the approvals for five years).
- Story count: 36 in the approval, 37 on the DBI application. Class 2 bike spaces: 57 in the packet, 53 in the
  minutes (not shown).
- Photo: not searched.

---

## Leads not added

- **600 Van Ness Avenue** (block 0763, lots 006–009): the "Affordable Housing Site" that the 98 Franklin development
  agreement would dedicate to the City (AG0330 p. 10). Planning's records show only a temporary use authorization for
  youth soccer on the vacant lot, valid to Sept 2027 (`REC(2025-008841PRL)`), and no housing project. Not a project
  yet; not added.
