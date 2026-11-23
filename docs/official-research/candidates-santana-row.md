# Official-source findings: Santana Row Master Plan Update (San José)

Checked 2026-10-19 against documents downloaded and read in full text (local copies in
`data/raw/official/santana-row/`, git-ignored), the CEQAnet project and document pages, and live queries of the
Santa Clara County parcel layer (`data.sccgov.org` `ubcd-cewv`). Page numbers are PDF page numbers.

Matthew asked on 2026-10-19 to add Santana Row. An earlier session had listed it as a lead
(`candidates-south-bay-2026-10.md`, "Candidates named in the brief, and other leads"). Santana Row itself is a
built shopping, housing, office and hotel district; what is in review is Federal Realty's plan to add four office
buildings to it, the **Santana Row Master Plan Update**.

Hosts: none to add. Every source is on `ceqanet.lci.ca.gov` or `data.sccgov.org`. The City's own pages
(`sanjoseca.gov/activeeirs`, `sanjose.legistar.com`) and its GIS server (`geo.sanjoseca.gov`, the zoning layer
that would hold the PDC13-050 planned development district) were refused by the proxy and weren't opened.

URL shorthand:
- PRJ = `https://ceqanet.lci.ca.gov/Project/2013122059` (project page: three documents)
- D1 = `https://ceqanet.lci.ca.gov/2013122059` (NOP, Santa Row [sic] Expansion (PDC13-050), received 12/23/2013; no attachments)
- D2 = `https://ceqanet.lci.ca.gov/2013122059/2` (Draft EIR, same project, received 3/23/2015; no attachments)
- D3 = `https://ceqanet.lci.ca.gov/2013122059/3` (revised NOP, Santana Row Master Plan Update, received 2/13/2026)
- NOP26 = `https://ceqanet.lci.ca.gov/2013122059/3/Attachment/lrKplZ` (Revised Notice of Preparation, February
  2026, 11 pp.; sha256 `7710e9c5…f874f9`)
- NOC26 = `https://ceqanet.lci.ca.gov/2013122059/3/Attachment/TUaXzI` (notice of completion, 2 pp.)
- DTSC = `https://ceqanet.lci.ca.gov/2013122059/3/Attachment/NZb2Ef`, CT = `…/YQW02n` (Caltrans), NAHC = `…/Plmaeq`
  (state comment letters on NOP26)
- PRJ22 = `https://ceqanet.lci.ca.gov/Project/2022110177`; D22 = `https://ceqanet.lci.ca.gov/2022110177` (NOP,
  received 11/9/2022); NOP22 = `https://ceqanet.lci.ca.gov/2022110177/Attachment/TJVTCQ` (Notice of Preparation,
  November 2022, 11 pp.)
- SCC = `https://data.sccgov.org/d/ubcd-cewv` (Santa Clara County parcels)

| project | stage | size | recommendation |
|---|---|---|---|
| Santana Row Master Plan Update (`santana-row`) | entitlement (EIR being prepared; revised NOP Feb 2026) | four office buildings, 1,500,000 sq ft (+1,272,081 sq ft over the existing entitlement), 139–162 ft, on a 42.53-acre site | **include** (Matthew's request) |

---

## santana-row

Recommendation: **INCLUDE** (Matthew's request; stage `entitlement`). Well over a million square feet of new
offices in four buildings up to 162 ft, in formal environmental review since 2022.

Documents read: NOP26 (all 11 pp., incl. Figure 4 p. 8 and Table 4.0-1 p. 9), NOC26, DTSC, CT and NAHC (first
pages), NOP22 (pp. 1–3, 7–9), the CEQAnet pages PRJ, D1, D2, D3, PRJ22, D22; a CEQAnet search of every document
received for San José from Feb 1 to Oct 19, 2026 (no later Santana Row document).

| field | official value | source | verbatim quote |
|---|---|---|---|
| name, files, applicant | Santana Row Master Plan Update; PDC22-004 and ER22-107; Federal Realty Investment Trust | NOP26 p. 1 | "REVISED NOTICE OF PREPARATION OF AN ENVIRONMENTAL IMPACT REPORT FOR THE SANTANA ROW MASTER PLAN UPDATE PROJECT FILE NOs: PDC22-004 & ER22-107 PROJECT APPLICANT: Federal Realty Investment Trust (Attn: Stuart MacDonald)" |
| APNs | nine | NOP26 p. 1 | "APNs: 277-33-017, 277-33-019, 277-33-020 277-40-029, 277-40-031, 277-38-003 277-38-004, 277-38-005, & 277-38-012" (NOC26 and D3 list the first eight; NOP22 listed six: "277-40-031, 277-33-019, 277-33-017, 277- 38-005, 277-38-004, & 277-38-003") |
| project description | rezoning, total floor area, Lot 22, parking | NOP26 p. 1 | "Planned Development Rezoning from an A(PD) Planned Development Zoning District (File No. PDC13-050) to a PD Planned Development Zoning District to modify the development standards to allow up to approximately 2,780,000 square feet of office (existing and proposed), establish new maximum height limits, add an approximately 0.54-acre parcel, remove approximately 22 street parking spaces to widen the sidewalk on both sides of Dudley Avenue, and allow approximately 2,147 new parking spaces on an approximately 42.53-gross acre site." |
| 2022 wording | "office and commercial"; late-night use; 2,150 spaces | NOP22 p. 1 | "to allow up to approximately 2,780,000 square feet of office and commercial square footage (existing and proposed), establish new maximum height limits, allow late night use, and allow approximately 2,150 new parking spaces on an approximately 42.53- gross acre site" |
| site | 42.53 acres, SE corner of Stevens Creek and Winchester | NOP26 p. 4 | "The approximately 42.53-acre project site is located at the southeast corner of Stevens Creek Boulevard and Winchester Boulevard." |
| components | five | NOP26 p. 4 | "1) modify the existing PD zoning for Santana Row to conform with the now-adopted Santana Row/Valley Fair Urban Village Plan which allows for additional office square footage, 2) establish the new conforming heights for existing Lots 1, 2B, and 10A of 150 feet (plus allowable mechanical screening parapet) consistent with the adopted Santana Row/Valley Fair Urban Village Plan, 3) merge existing Lots 1A, 1B, and 1C into a single parcel, 3) merge 524, 534, and 544 Dudley Avenue into a single parcel (Lot 17) with a maximum height limit of 162 feet (plus allowable mechanical screening parapet), and 4) remove 22 existing street parking spaces on both sides of Dudley Avenue to widen the Lot 17 sidewalk, and 5) addition of an approximately 0.54-acre parcel (Lot 22)." |
| parking | ~2,147 new | NOP26 p. 4 | "The new development includes approximately 2,147 new parking spaces with an increase of 1,460 spaces on Lot 1 and 831 spaces on Lot 17, and a loss of 97 spaces on Lot 2B." (1,460 + 831 − 97 = 2,194; see open items) |
| proposed program | four office buildings, 1,500,000 sq ft; +1,272,081 sq ft over PDC13-050 | NOP26 p. 9, Table 4.0-1 | "Lot 1A/B/C 700,000 (144 feet tall) + 579,629 sf Office"; "Lot 2B 325,000 (144 feet tall) + 245,797 sf Office"; "Lot 10A 200,000 (139 feet tall) + 171,655 sf Office"; "Lot 17 275,000 (162 feet tall) + 275,000 sf Office"; "Lot 22 0 +0 Potential location for new signage"; "Total 1,500,000 + 1,272,081 sf"; footnote "The increase/decrease in land uses is over the existing entitlement (PDC13-050)". Column header: "Square Footage (Maximum No. of Stories)" |
| 2022 table | same figures, use "Office/Commercial", no Lot 22 | NOP22 p. 7 | "Lot 1A/B/C 700,000 (144 feet tall) + 579,629 sf Office/Commercial" … "Total 1,500,000 + 1,272,081 sf" |
| approvals needed | new PD zoning and PD permits | NOP26 p. 9 | "The proposed changes to the existing entitlements would require a new Planned Development Zoning and new Planned Development permit(s), which would be part of the Project approvals." |
| existing (2026) | 834 homes built, 258 under construction, 1,229 approved; 214 of 220 hotel rooms; retail/restaurant 584,395 sf and office 606,535 sf built | NOP26 p. 4, Table 3.0-1 | "Hotel Rooms 220 214 --- 6"; "Residential 1,229 834 258 137"; "Commercial Space 1,506,341 sf 1,193,508 sf --- 312,833 sf"; "Retail Combined 708,141 sf 584,395 sf --- 121,168 sf"; "- Retail 562,941 sf 479,176 sf --- 81,187 sf"; "- Restaurant 145,200 sf 105,219 sf --- 39,981 sf"; "Office 798,200 sf 606,535 sf --- 191,665 sf" |
| existing (2022) | nothing under construction; 395 homes remaining | NOP22 p. 7 | "Residential 1,229 834 --- 395" |
| existing uses, parking | | NOP26 p. 4 | "The existing uses on this site include hotel, retail, office, restaurant, theater, and residential"; "The existing uses have approximately 6,231 parking spaces allocated across all the parking areas. The site is zoned Planned Development (PD) and is designated Urban Village in the General Plan." |
| why re-issued | Lot 22 added | NOP26 p. 3 | "In November 2022, the City of San José issued a Notice of Preparation (NOP) … The City held a public scoping meeting on November 17, 2022. Since the NOP was originally issued in November 2022, an approximately 0.54-acre parcel (Lot 22) was added to the project. The City is re-issuing the NOP to ensure that the CEQA scoping process remains current." |
| dates | signed 2/12/26; received 2/13/2026; review Feb 23 – Mar 25, 2026 | NOP26 p. 2; D3; NOC26 | "2/12/26"; D3: "Received 2/13/2026"; NOC26: "Starting Date February 23, 2026 Ending Date March 25, 2026" |
| scoping meeting | Mar 11, 2026, Zoom | NOP26 p. 1 | "When: Thursday, March 11, 2026 from 6:00 to 7:30 p.m. Where: Via Zoom" (March 11, 2026 was a Wednesday; not put in the timeline) |
| CEQAnet record | 1,272,081 sq ft office, 42.53 acres, 4,240 employees | D3 | "Development Types Office (Sq. Ft. 1272081, Acres 42.53, Employees 4240)" |
| prior EIR | certified; PDC13-050 is the existing zoning | NOP26 p. 9; p. 1 | "The analysis will be based off the data from the previously certified EIR"; "from an A(PD) Planned Development Zoning District (File No. PDC13-050)" |
| 2013 expansion | Lot 17 (1.91 acres), +510,000 sf office, +55,641 sf retail, +47 homes, +6 hotel rooms | D1, D2 | "The project proposes to expand the Santana Row site by 1.91 acres (the expansion area is referred to as Lot 17), increase the allowable office space entitlement by 510,000 sf, and increase the retail entitlement by 55,641 sf. In addition, the project proposes to increase the allowable number of residential units by 47 and the allowable number of hotel rooms by six." D1 "Received 12/23/2013", "Total Acres 42.71"; D2 "Received 3/23/2015", "State Review Period Start 3/23/2015 State Review Period End 5/6/2015", "Total Acres 42.53" |
| DTSC oversight | the site is within the Town & Country Village Shopping Center Site, with land use covenants | DTSC p. 2 | "The Project is within a site that DTSC has regulatory oversight over: Town & Country Village Shopping Center Site. This Site has multiple Land Use Covenants (LUCs), dated 7/24/2004" |

Program reconciliation. Table 4.0-1's four lots add up to 1,500,000 sq ft of office; the notice counts this as
1,272,081 sq ft more than the existing entitlement (PDC13-050), so about 227,919 sq ft of what the four lots
would hold is already entitled. The "approximately 2,780,000 square feet of office (existing and proposed)" in
the 2026 description matches the approved commercial space (1,506,341 sq ft, Table 3.0-1, which is retail,
restaurant and office) plus 1,272,081 = 2,778,422 sq ft; office alone would be 798,200 + 1,272,081 = 2,070,281.
So the 2,780,000 is the total commercial space, as the 2022 notice and Caltrans' 2026 letter put it ("office and
commercial square footage (existing and proposed)", CT p. 1). The record shows `officeLabSqft` 1,500,000 (the
four new buildings) and explains the rest in `program.notes`; `commercialSqftTotal` is left null so the panel
doesn't show the existing district's space as new.

Stage: **entitlement**. The City is preparing an EIR (NOP Nov 2022, re-issued Feb 2026); no Draft EIR or any
later document is on CEQAnet as of Oct 19, 2026 (PRJ lists three documents; PRJ22 one; the San José document list
for Feb–Oct 2026 has nothing more for Santana Row). Next milestone: the Draft EIR (no date published).

Boundary (`pipeline/bam_pipeline/sites/boundary_santana_row.py`, accuracy **approximate**): the nine APNs the
notice names come to only 5.90 acres in the County layer: they are the lots that would change (Lot 1A/B/C =
277-33-020, -019, -017 along Stevens Creek Boulevard from Winchester Boulevard to Santana Row; Lot 2B =
277-40-029, 300 Santana Row; Lot 10A = 277-40-031, 3088 Olsen Drive; Lot 17 = 277-38-003, -004, -005, 544, 534 and
524 Dudley Avenue; Lot 22 = 277-38-012, 0.539 acres in the County layer, the notice's "approximately 0.54-acre
parcel"). So the boundary is not the APN list but the County parcels inside the dashed project boundary of
Figure 4 (Lot Division Diagram, p. 8, "Source: WRNS Studio, February 18, 2022"), together with the nine. The main
outline is part of the figure's raster base (only Lot 22's dashes are vector), so it is traced from the page
rendered at 4 px/pt (blue pixels), placed by a similarity from the five lot labels to the NOP parcels (RMS
4.8 m) and refined by trimmed ICP of the dashed line to the selected parcels' outline (RMS 1.39 m, 11,856 of
14,820 pixels). Result: 605 parcels (8 without APN: the private streets and common areas; most of the rest
stacked condominium parcels inside the blocks), **42.83 acres** against the notice's 42.53 (Lot 22, 0.54 acres,
was added after the 42.53 was first published, and the stated acreage wasn't changed). The traced outline is 42.7 acres
and lies within about 11 m of the parcels except at Lot 22, which the figure draws smaller than the County's
parcel (17 m). The parcel 277-33-003 at Winchester Boulevard, which the figure leaves out (a notch in the
outline), is left out. Each NOP lot's label lands inside its parcels after the fit. No overlap with any mapped
boundary (the nearest, `santa-clara-station-area`, is 2.9 km away).

Massing (`pipeline/bam_pipeline/sites/massing_santana_row.py`, illustrative, stage `entitlement`): Figure 4's lot
lines are raster, and the lots are the parcels the notice names, so each lot is drawn from the County parcels
rather than traced (the traced figure confirms the placement; see above). Each is a whole-lot envelope at Table
4.0-1's height: Lot 1A/B/C 108,515 sq ft at 144 ft; Lot 2B 44,056 sq ft at 144 ft; Lot 10A 37,741 sq ft at 139 ft;
Lot 17 43,205 sq ft at 162 ft. The notice shows no building design; the stated floor areas are 5.3 to 7.4 times
these lot areas, and the lots would also hold new parking. The parapets allowed above the heights aren't drawn,
nor is Lot 22 (signage only) or any existing building. Every output polygon is valid (checked after rounding).

Press-only facts: none recorded; every shown fact is from the CEQAnet record. No press search was needed.

Open items (in `verify`):
- When the City approved the 2013–15 Santana Row Expansion (PDC13-050) and certified its EIR: CEQAnet holds no
  notice of determination, but the notice calls PDC13-050 the existing zoning and entitlement and refers to "the
  previously certified EIR". Whether that approval included Lot 17 (the 2013 notice added Lot 17 as 1.91 acres
  with APN 277-38-010 too; Table 4.0-1 counts all 275,000 sq ft on Lot 17 as new) is unclear.
- The 2,780,000 sq ft wording (office vs office and commercial), above.
- Parking: 2,147 stated against 2,194 from the lot-by-lot changes.
- Where each building would stand on its lot; what stands on Lots 1A/B/C, 2B and 10A now.
- The site's acreage, unchanged at 42.53 after Lot 22 was added.
- Smaller slips in the notice, not carried into the record: the comment deadline on p. 2 says "March 25, 2025"
  (NOC26 and CEQAnet say 2026); "Thursday, March 11, 2026" was a Wednesday; Table 3.0-1's built retail (479,176 sf)
  and the "Retail Combined" remaining entitlement (121,168 sf) are 2,578 sq ft off the other columns' arithmetic.
- The Draft EIR's date.

## Leads not added

- **Santana Row/Valley Fair Urban Village Plan** (San José): the adopted plan the update would conform to (NOP26
  p. 4: "the now-adopted Santana Row/Valley Fair Urban Village Plan"). An area plan with many owners; the City's
  pages weren't reachable and no CEQAnet record was opened. Not recommended (like other urban village plans).
