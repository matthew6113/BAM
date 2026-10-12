# Official-source findings: City of Alameda (Alameda Point beyond Site A, Northern Waterfront, the rest)

Checked 2026-10-12. Matthew asked on 2026-10-12: "can you add whatever is going on with Alameda". The map had
one Alameda project, `alameda-point` (Site A, up to 1,300 homes). This file surveys the rest of the city's
large development activity from official records and recommends what to map.

How it was read: `www.alamedaca.gov` still answers scripts with an Akamai 403, so everything here comes from
the City's Legistar records through the Legistar web API (`webapi.legistar.com/v1/alameda/`, staff reports and
minutes in full text) and the City's attachment store (`legistar1.granicus.com/alameda/`, PDFs read in full),
the City of Alameda's ArcGIS Online organisation (`services9.arcgis.com/ucDLsG1EwPnOGY4c/`, zoning) and Alameda
County Assessor parcels (`services5.arcgis.com/ROBnTHSNjoZ2Wm1P/`). Local copies are in
`data/raw/official/alameda-candidates/` (git-ignored). Page numbers are PDF pages.

Hosts: none to add. All of the above are already in `src/projects/official.ts` (`.gov`, `alameda.legistar.com`,
`webapi.legistar.com/v1/alameda/`, `legistar1.granicus.com/alameda/`, `services9.arcgis.com/ucdlsg1ewpnogy4c/`
(City of Alameda), `services5.arcgis.com/robnthsnjoz2wm1p/` (Alameda County)).

URL shorthand:
- `MT(n/t)` = `https://webapi.legistar.com/v1/alameda/matters/n/texts/t` (a staff report or minutes, full text)
- `ATT(x)` = `https://legistar1.granicus.com/alameda/attachments/x.pdf`
- ZONING = `https://services9.arcgis.com/ucDLsG1EwPnOGY4c/arcgis/rest/services/Zoning_v03/FeatureServer/0`
  (City of Alameda "Zoning v03", item 5e69b7ebbee34a8d8d5fb21cddc651c8, last edited Jan 2026; no license stated)
- ALCO = `https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Parcels/FeatureServer/0`

## Summary

| # | item | homes / space | stage (date) | recommendation |
|---|---|---|---|---|
| 1 | West Midway and RESHAP (Alameda Point, Main Street Neighborhood) | 810 homes (478 + 332), 40% very low/low income | site work: demolition done, RESHAP infrastructure nearly complete (Aug 2026); West Midway vertical construction aimed at Q1 2027 | **INCLUDE**, mapped as `west-midway-reshap` |
| 2 | Alameda Point, rest of the base (Main Street Neighborhood North, Town Center, Adaptive Reuse, Enterprise District, open space) | MSNN study: ~600–1,000 homes; Enterprise ~100+ ac job land | zoning, EIR and plans adopted 2014–2017; no developer outside Site A and West Midway; MSNN developer RFQ being weighed (2026) | **INCLUDE**, mapped plan-scale as `alameda-point-plan` |
| 3 | Encinal Terminals (Northern Waterfront) | 589 homes (80 affordable), 50,000 sq ft, 160-slip marina | entitled (2022); milestones extended (Jan 2025); interim EV storage permitted to 2028 | **INCLUDE**, mapped as `encinal-terminals` |
| 4 | Alameda Marina (Northern Waterfront) | 801 homes, up to 250,000 sq ft, 530-slip marina | partly built: Phase I done, Phase II under construction, Phase III approved (amended July 2026) | **INCLUDE**, mapped as `alameda-marina` |
| 5 | 2433 Mariner Square Loop | 356 homes, one 8-story building | entitled 2025 | BORDERLINE (single building, < 500 homes) |
| 6 | Oakland Roots and Soul interim stadium, Harbor Bay Business Park | up to 8,000 seats, temporary | proposed (workshops June 22 and Aug 2026) | BORDERLINE (not housing, interim, not approved) |
| 7 | 2022 Housing Element rezoning (shopping centers, Park/Webster corridors) | sites for 5,353 RHNA homes citywide | adopted Nov 2022 | EXCLUDE (a citywide rezoning, not a project) |
| 8 | Del Monte warehouse (1501 Buena Vista) | about 380 homes (press) | complete: all DA obligations met by Dec 2024 | EXCLUDE (complete) |
| 9 | Alameda Landing (Catellus, Bay 37) | — | complete: Certificate of Completion issued | EXCLUDE (complete) |
| 10 | Enterprise District / Pacific Fusion | 220,000 sq ft R&D facility | option terminated (Sept 2025) | EXCLUDE as its own project; part of #2 |

Four new projects, the limit. Smaller and finished items are listed for Matthew below.

---

## 1. west-midway-reshap

Recommendation: **INCLUDE**, stage `infrastructure`. Two linked projects on one 34.5-acre block of the Main
Street Neighborhood, bounded by Pan Am Way, West Midway Avenue, Main Street and West Tower Avenue: 478
market-rate, workforce and moderate-income homes (West Midway, Brookfield and Catellus) and 332 supportive and
affordable homes replacing the Navy-era housing of the Collaborating Partners (RESHAP, MidPen Housing).

Documents read:
- City Council staff report, West Midway agreements, July 18, 2023 (matter 12958): MT(12958/13834); RESHAP
  report, same night (matter 12957): MT(12957/13833).
- Council minutes July 18, 2023: MT(13172/14074); Sept 5, 2023: MT(13200/14105); Mar 19, 2024: MT(13713/14683).
- Planning Board, RESHAP amendment to 332 homes, Dec 4, 2023 (matter 13437): MT(13437/14367); RESHAP
  Development Plan (May 8, 2023): ATT(d3ee17a1-dd9a-4874-99d4-ae7134ed1c5b).
- Planning Board, West Midway Phase A design review, Dec 8, 2025 (matter 15369): MT(15369/16553); exhibits
  incl. the 2023 Development Plan ATT(5be8021b-f3c6-4a76-8312-60267b458f36); minutes MT(15541/16731).
- Alameda Point Housing Update & Walking Tour deck, Dec 6, 2025: ATT(f39cda77-9fb6-4fe0-a9e7-2408361ab198).
- West Midway DA annual review, May 26, 2026 (matter 15831): MT(15831/17037); developer's letter
  ATT(45e7c77c-b08a-43c0-849b-849eb0a24404). RESHAP annual review 2025 (matter 14589), letter
  ATT(92316771-b2ab-4769-96ad-d00f312cff52).
- Council report on a Stardust Gardens operating subsidy, Aug 2026 (matter 16042): MT(16042/17254).
- Tract 8696 final map (matter 14761): ATT(bbbc4de9-eb75-4e85-ba12-558cf678e02e).

| field | official value | source | quote |
|---|---|---|---|
| homes | 810 (478 + 332) | MT(13437/14367) | "8 manager units at RESHAP, and 478 market rate and moderate income at the West Midway project which results in 810 total units of which 324 (40%) are deed restricted to very low and low income households." |
| affordable | 324 very low/low (40%) + 44 moderate in West Midway | MT(13437/14367); MT(12958/13834) | "the remaining obligation for 44 moderate income housing units will be fulfilled by the West Midway Project" |
| workforce | 43 "affordable by design" units, not deed-restricted | MT(12958/13834) | "The West Midway project includes 43 \"affordable by design\" units designed for \"workforce\" households" |
| acres | West Midway ~26; RESHAP ~8.5 (8 in 2023) | MT(12958/13834); MT(13437/14367) | "on approximately 26 acres of land"; "approximately 8.5 acres of City-owned land at the corner of Pan Am Way and West Midway Avenue" |
| non-residential | West Midway up to 10,000 sq ft; RESHAP ~40,000 sq ft | MT(12958/13834); MT(13437/14367) | "up to 10,000 square feet of non-residential uses"; "Approximately 40,000 square feet of non-residential space for community serving commercial and administrative office uses" |
| heights | West Midway 40 ft (50 ft for 4-story condos); RESHAP ±50 ft | 2023 Development Plan sheet 10; RESHAP plan p. 13 | "HEIGHT: 40' Max."; "ALL BUILDING HEIGHTS LIMITED TO +/- 50' HEIGHT" |
| approvals | PB: RESHAP plan May 8, 2023; WM plan May 22, 2023; Council introduced July 18, 2023 (4–1); Ordinances 3345–3348 finally passed Sept 5, 2023 | MT(13200/14105) | "Ordinance No. 3348, \"Authorizing the City Manager to Execute a Development Agreement Between the City of Alameda and \"BC West Midway LLC\"…\" Finally passed." |
| RESHAP to 332 | PB Dec 4, 2023; Ordinance 3364 (Mar 19, 2024) | MT(13713/14683) | "Ordinance No. 3364 \"Approving a First Amendment to the Rebuilding the Existing Supportive Housing at Alameda Point (RESHAP) Development Agreement…\"" |
| developer | BC West Midway LLC (Brookfield + Catellus JV); MidPen Housing and the Collaborating Partners | MT(12958/13834) | "The Brookfield and Catellus development companies created a joint venture entity, BC West Midway LLC" |
| Phase A design | 284 homes in 62 buildings on ~12.4 ac, approved 6–0 Dec 8, 2025 | MT(15541/16731) | "passed 6-0 with one absence (Vice President Ariza)" |
| status (City, Dec 2025) | WM demolition complete, site prep underway; RESHAP Phase 1 infrastructure underway | ATT(f39cda77…) p. 11–12 | "Demolition Complete: demolition of former commissary and other structures; Site preparation underway"; "Vertical construction: Q1 2027, market dependent" |
| status (City, Aug 2026) | infrastructure for Stardust Gardens done; RESHAP site work nearly complete | MT(16042/17254) | "The West Midway developer, Catellus and Brookfield, has completed the infrastructure improvements required under the West Midway DDA to support Stardust Gardens… Site work supporting RESHAP is nearly complete." |
| RESHAP phase 1 | Stardust Gardens, 80 homes; operating subsidy commitment proposed Aug 2026 | MT(16042/17254) | "The first phase of the project, the 80-unit Stardust Gardens building" |

Developer-only (in the City's record but written by the developer, kept as context, not shown as fact):
the 2026 annual letter says demolition of Phases 1–3a/b is "substantially complete" and that CFD 25-1 was
approved on Sept 2, 2025. The City's own Dec 2025 deck ("Complete: Community Facilities District formed")
covers the CFD.

Boundary lead (used): ALCO parcels, the 23 lots of Tract 8696 in the block (APN books 74-1385 to 74-1388),
closed over the internal streets: 34.4 acres, matching 26 + 8.5. Massing lead (used): the 2023 Development
Plan sheet 10 "Land Use Diagram & Building Heights" (raster, six colour-coded blocks with heights) and the
RESHAP plan p. 13 land use diagram (1" = 100'), both fitted to the Tract 8696 lots.

---

## 2. alameda-point-plan (the rest of the former naval air station)

Recommendation: **INCLUDE** as a plan-scale project (boundary and land-use zones only, SPEC §7), stage
`entitled` (the zoning, EIR and plans are adopted; nothing beyond Site A and West Midway/RESHAP has a
developer). Site A and West Midway/RESHAP are cut out and stay their own projects, so nothing is double-drawn
and Site A's geometry is unchanged.

Why one combined project rather than "Main Street Neighborhood North" alone: MSNN has no application or
developer yet (a feasibility study and study sessions only), and the Enterprise District, Town Center
waterfront and Adaptive Reuse area are each in the same position. One plan-scale record shows where the
remaining land is, what the adopted zoning allows, and the live steps (MSNN RFQ, Navy fee change, Enterprise
repositioning) without inventing a project.

Documents read:
- Planning Board study session on Main Street Neighborhood North, June 8, 2026 (matter 15882): MT(15882/17089);
  exhibits: Dec 6, 2025 housing update deck ATT(f39cda77-9fb6-4fe0-a9e7-2408361ab198), Main Street Neighborhood
  Specific Plan ATT(8389ebfc-3f86-47a1-9c23-57713c4c6175).
- Council report on the Navy EDC agreement's third amendment (matter 15167): MT(15167/16344); adopted as
  Resolution 16333 on Oct 21, 2025: MT(15287/16468).
- Enterprise District: Mayor's Economic Development Advisory Panel report, Nov 2025 (matter 15362)
  MT(15362/16546); Council report on the Pacific Fusion purchase option, May 2025 (matter 14861) MT(14861/16009).
- ZONING layer (the AP- districts), queried live.

| field | official value | source | quote |
|---|---|---|---|
| MSNN area | ~31 ac north of West Midway; 600–1,000 homes in feasibility scenarios | MT(15882/17089) | "approximately 600 to 1,000 existing and new residential units could potentially be accommodated within the broader MSNN area" |
| MSNN next step | RFQ for a developer "in late 2026/early 2027" being explored; no approvals | MT(15882/17089) | "exploring the possibility of releasing a developer Request for Qualifications (\"RFQ\") in late 2026/early 2027"; "No formal policy decisions or project approvals are being requested at this time." |
| housing totals | 677 market-rate homes built, 1,084 entitled, 250 left under the 2,011-unit Navy baseline | MT(15882/17089) | "approximately 677 market-rate units have been constructed, with another 1,084 entitled, leaving 250 available under the 2,011-unit cap" |
| land left | ~129 undeveloped acres zoned residential or mixed use | MT(15167/16344) | "There are roughly 129 undeveloped acres of land remaining at Alameda Point that are zoned for residential or mixed-use development." |
| Navy fee | cut from ~$103,000 to $73,000 per market-rate unit over the baseline; prepayment discounts | MT(15167/16344); Res. 16333, MT(15287/16468) | "the City will pay the Navy a per unit fee, which is reduced from its current level of approximately $103,000 to $73,000" |
| first conveyance | 2013 | MT(15167/16344) | "the first major conveyance approached (completed in 2013)" |
| plans | Alameda Point zoning and EIR (2014), Master Infrastructure Plan (2014, 2020), Main Street Neighborhood Specific Plan (2017), Town Center & Waterfront Precise Plan (2014) | MT(15882/17089); deck p. 6, 14 | "Main Street Neighborhood Specific Plan (2017)"; "On March 21, 2017, the City Council approved the Main Street Neighborhood Specific Plan" (MT(12958/13834)) |
| EIR | certified Feb 2014, Resolution 14891, SCH 2013012043 | MT(15369/16553) | "In February 2014, per City Resolution No. 14891, the City Council certified the Alameda Point Project Final Environmental Impact Report" |
| Enterprise | ~100+ ac, job uses only; Pacific Fusion (13 ac, 220,000 sq ft) chose Albuquerque Sept 2025 and terminated its option | MT(15362/16546) | "In September of this year, Pacific Fusion notified Alameda of their intent to proceed with constructing this facility in Albuquerque, New Mexico." |
| AP-AR | no new housing (except Building 17) | MT(15882/17089) | "does not currently allow new residential development, with the exception of the reuse of Building 17" |
| infrastructure | MIP cost now ~$900 million | deck p. 19 | "as called for in the MIP, whose total cost has risen to approximately $900 million" |
| wider vision | up to 2,300 homes by relocating all Collaborating Partners housing (staff estimate) | MT(16042/17254) | "the City could deliver up to 2,300 new homes in the area, at least 25 percent of which would be affordable" |

Not found officially: a single acreage for "the rest of the base" (the zoning drawn here is about 787 acres
incl. ~298 acres of open space); the Navy's remaining (unconveyed) parcels as a map. Site B is the former name
of the Enterprise District ("Tour of the Enterprise District (Formerly Site B)", matter 8508).

Boundary and zones (used): ZONING, `zone LIKE 'AP-%'` as published (AP-MS, AP-WTC, AP-AR, AP-E1–E4, AP-OS),
less Site A (traced) and the West Midway/RESHAP parcels; AP-NR/G (Nature Reserve) left out.

---

## 3. encinal-terminals

Recommendation: **INCLUDE**, stage `entitled`. A vacant 23-acre former container terminal at 1521 Buena Vista
Avenue between the Alaska Basin and Fortman Marina, entitled for 589 homes; held up by the market, with
milestones extended and an interim EV storage lot allowed until 2028.

Documents read: Planning Board staff report on the milestone amendment, Nov/Dec 2024 (matter 14385)
MT(14385/15452) with the redlined Master Plan ATT(6e80b41d-a385-45cf-89fc-f1475d4a2cb1); Council minutes Feb 1,
2022 MT(11554/12276) and Jan 21, 2025 MT(14561/15654); Council report on the tidelands lease amendment, May 2026
(matter 15672) MT(15672/16874); minutes May 5, 2026 MT(15841/17048); DA annual review May 26, 2026 (matter 15830)
MT(15830/17036).

| field | official value | source | quote |
|---|---|---|---|
| acres | 23 | MT(15672/16874) | "authorizing redevelopment of the 23-acre site for up to 589 multifamily housing units (including 80 deed-restricted affordable units), up to 50,000 square feet of commercial and maritime commercial space, a 160-slip marina, and 4.5 acres of public open space" |
| homes / affordable | 589 / 80 (45 low and very low, 35 moderate) | same; redlined Master Plan, affordable housing section | "The 45 Low-/Very Low- units…"; "The 35 moderate income units…" |
| approvals | Ordinances 3311 (DDA), 3312 (Master Plan and density bonus), 3313 (DA), Feb 1, 2022; DA dated Mar 3, 2022; 15-year term | MT(11554/12276); MT(15830/17036) | "Ordinance No. 3312, \"Approving the Amended Encinal Terminals Tidelands Exchange Master Plan and Density Bonus Application…\" Finally passed" |
| EIRs | Northern Waterfront EIR (Res. 14134–14135, July 17, 2007); Focused Supplemental EIR (Res. 15337, Dec 19, 2017) | MT(14385/15452) | "on December 19, 2017, the City Council adopted Resolution No. 15337 certifying a Focused Supplemental Environmental Impact Report" |
| tidelands exchange | State Exchange Agreement recorded Feb 2023; legislation July 2023; title validation Feb 2024 | MT(14385/15452) | "Negotiating the State Exchange Agreement: signed and recorded in February 2023" |
| milestones | extended by Ordinance 3379 (final passage Jan 21, 2025); first site milestone March 2028 | MT(14561/15654); MT(15672/16874) | "The amended deadline for first of these amended internal milestones is March 2028." |
| why | market | MT(14385/15452) | "an economic environment that has obliterated the present residual land value of the property" |
| interim use | 2-year outdoor storage of new EVs, use permit PB-26-2 (Mar 23, 2026); lease amendment introduced May 5, 2026 | MT(15672/16874); MT(15841/17048) | "allowing for an interim outdoor use for the non-retail, commercial storage of new electric vehicles (EVs) on the vacant 23-acre Encinal Terminals" |
| parties | DA: North Waterfront Cove, LLC; land: Bayview Landing LP (lease assigned Mar 19, 2025; owns the other three parcels) | MT(15830/17036); MT(15672/16874) | "The other three parcels that comprise Encinal Terminals are owned by the Lessee." |
| next | assessment district: kickoff by Aug 2026, draft RMA by Dec 2026, first hearings by June 2027 | MT(14385/15452) | "First Formation Document Hearings no later than June 2027" |

Boundary (used): ALCO parcels 72-382-1, 72-382-2, 72-382-9 (31.0 acres as drawn, more than the 23-acre site
because the parcels run over the wharf and water; the ordinance's fourth APN, 072-0383-003, is now the
Clement Avenue extension strip 72-383-3-1, left out). Massing: none. The Master Plan sets no block plan or
building design: heights follow the MF district (AMC 30-4.23) with waivers possible (Master Plan "Building
Height, Setbacks and Blocks"), so drawing envelopes would be invented. A land-use split (developer lands vs
public trust waterfront) could be traced later from the Tidelands Trust Exchange Diagram,
ATT(218a2f69-a717-4836-9192-6b4c8d5878b9).

---

## 4. alameda-marina

Recommendation: **INCLUDE**, stage `partial`. The 44-acre Alameda Marina between Grand and Willow streets on
Clement Avenue, approved in 2018 for 760 homes, raised to 801 in 2023.

Documents read: Planning Board staff report on the Master Plan (May 2018, matter 7315) MT(7315/7770); Council
minutes July 10, 2018 MT(7605/8081); Phase I (Wrap A) design review, Oct 14, 2019 (matter 9050) MT(9050/9650);
Phase II (matter 9483) MT(9483/10108); Phase III design review, July 10, 2023 (matter 13013) MT(13013/13902);
Council report on the 801-unit amendment (matter 13098) MT(13098/13998); Tract 8711 final map (matter 14310)
MT(14310/15369) and ATT(5e058a67-4738-4a31-8fb8-09ab86c063a5); 2026 affordable amendment (matter 15877)
MT(15877/17084); Council minutes July 7, 2026 MT(16009/17219).

| field | official value | source | quote |
|---|---|---|---|
| acres | 44 (27 private uplands and submerged; ~17 City tidelands) | MT(14310/15369) | "on the 44-acre site located at 1815 Clement Avenue and commonly known as Alameda Marina. The development includes 27 acres of uplands and submerged lands and approximately 17 acres of waterfront and submerged lands (tidelands)" |
| homes | 801 (760 in 2018 + 41 by density bonus, Ordinance 3351, Sept 19, 2023) | MT(14310/15369) | "On September 19, 2023, City Council adopted Ordinance 3351 amending the Alameda Marina Master Plan and approving a density bonus to increase the Alameda Marina sitewide housing unit count from 760 to 801 units" |
| commercial / open space / marina | up to 250,000 sq ft; ~3.59 ac open space; 530 slips | MT(15877/17084) | "up to 760 multifamily housing units, up to 250,000 square feet of commercial and maritime commercial space, approximately 3.59 acres of shoreline open space, and a 530-slip marina" |
| affordable | Phase I 49, Phase II 25, Phase III 43 → 21 (2026) = 95 | MT(13013/13902); MT(15877/17084) | "Phase I was completed with 49 affordable units and Phase II is already under construction with 25 affordable units"; "to provide 21 very low-income deed restricted units within the 259 unit building instead of 23 very low-income units, seven (7) low-income units, and 13 moderate-income units" |
| 2026 amendment | Ordinance 3406, finally passed July 7, 2026 | MT(16009/17219) | "Ordinance No. 3406, \"Amending the Alameda Marina Master Plan to Modify the Affordable Housing Requirement for Phase III of Alameda Marina Master Plan.\" Finally passed." |
| status | Phase I complete and occupied; Phase II under construction; Phase III not begun | MT(15877/17084) | "Currently, the Phase I residential rental building is complete and occupied, and the Phase II ownership buildings are under construction." |
| Phase III start | applicant says "this summer" (2026) if amended | MT(15877/17084) | "they will be able to begin construction of the 259-unit residential building this summer" |
| heights | 65 ft for the two wrap buildings, 45 ft elsewhere | MT(7315/7770) | "the Master Plan establishes a building height limit of 65 feet for the two major residential buildings on each side of the commercial core area and a 45-foot height limit for the balance of the site" |
| Wrap A (The Launch) | 360 homes, 4–5 stories, ~50–60 ft | MT(9050/9650) | "The new four- to five-story building varies between approximately 50' to 60' in height." |
| Wrap B (The Foundry) | 259 homes, 5 stories, 50–65 ft | MT(13013/13902) | "Wrap B is a 5-story multifamily building that varies in height between 50 and 65 feet" |
| Phase II | 182 townhomes in 31 buildings | MT(9483/10108) | "a Development Plan and Design Review application for 182 townhouse units in 31 buildings" |
| EIR / approval | EIR certified Res. 15413, July 10, 2018; master plan ordinance introduced the same night | MT(7605/8081) | "Resolution No. 15413, \"Certifying the Final Environmental Impact Report (EIR)…for the Alameda Marina Project.\" Adopted" |
| developer | Alameda Marina, LLC (Pacific Shops in 2018–19) | MT(15877/17084); MT(9050/9650) | — |

Boundary (used): ZONING, the M-X polygon at Clement Avenue between Grand and Willow streets (27.3 acres as
drawn), i.e. the master plan's private uplands; the City tidelands (marina) aren't zoned M-X and aren't drawn.
Massing (used): The Launch from OpenStreetMap (r16011797) at 60 ft; Phase II as the Tract 8610 lots (ALCO
71-292/71-293) at the 45-ft limit; The Foundry as Tract 8711's lot (ALCO 71-291-12) at 65 ft.

---

## Borderline and excluded (not mapped)

**2433 Mariner Square Loop (BORDERLINE).** An 8-story, 356-home building on a 2.39-acre Housing Element site,
approved through objective design review in 2025: MT(15023/16197) ("There would be 356 dwelling units"), and the
2025 General Plan annual report MT(15576/16768) ("Approved planning entitlements for 356 units at Mariner Square
Loop"). Below the 500-home default; a single building. Would tip if Matthew wants single large buildings.

**Oakland Roots and Soul stadium, 1150 and 1220 Harbor Bay Parkway (BORDERLINE).** Proposed interim venue for
"up to 8,000 attendees, up to 24 times per year" for five years with modular stands on the 17-acre training
site; Planning Board workshops June 22 and Aug 2026, no approval: MT(16035/17247). Not housing, temporary.

**2022 Housing Element rezoning (EXCLUDE).** Adopted with zoning amendments in Nov 2022 (MT(12287/13055),
final passage MT(12392/13168)): rezoned sites "to permit multifamily housing and residential densities of at
least 30 units per acre"; shopping centers (South Shore, Harbor Bay, Alameda Landing, Marina Village) carry
19% of the 5,353-home RHNA and the Park and Webster corridors 8%; 64% is at Alameda Point and the Northern
Waterfront, i.e. the projects mapped above. A citywide policy, not a project; only 663 permits had been issued
by early 2026 (MT(15576/16768)).

**Del Monte warehouse, 1501 Buena Vista (EXCLUDE, complete).** "ABV has completed construction of the project
and has transferred ownership to Star Harbor Property, LLC. All obligations under the DA were completed prior to
the transfer as of December 2024." Ten townhomes on the leftover pad were approved in 2024: MT(15588/16780).

**Alameda Landing (EXCLUDE, complete).** "The project is fully developed and all obligations under the
development agreement have been satisfied", Certificate of Completion issued: MT(15829/17035).

**Enterprise District / Site B (part of #2).** No active project after Pacific Fusion's withdrawal; listed in
`alameda-point-plan`.

**Bachelor Enlisted Quarters (Buildings 2, 3, 4), Adaptive Reuse area.** "Open to proposals; multiple active
proposals under review" (Dec 2025 deck p. 9). Too early; inside #2.

## Press-only

Nothing press-only was needed: every fact above is from City records. Names of the joint-venture members beyond
the City's own wording ("Brookfield and Catellus") were not added.

## Open items (verify)

- West Midway: whether the Tract 8696 final map and CFD 25-1 dates match the Council minutes (the City deck says
  the CFD is formed; the developer letter says Sept 2, 2025).
- RESHAP: the outcome of the Aug 2026 Stardust Gardens subsidy item and whether Phase 1A construction has started.
- Encinal Terminals: final passage of the third lease amendment (introduced May 5, 2026).
- Alameda Marina: whether Phase III construction started in summer 2026; whether Phase II is complete.
- Alameda Point: whether the Council directed the MSNN RFQ after the June 2026 study sessions.
