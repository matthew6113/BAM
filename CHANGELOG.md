# Changelog

Data changes to `data/projects.json` and other project facts, newest first. Each entry
says what changed, why and against which source. Code changes live in git history.

## 2026-11-23 (six-weekly update)

The update due Nov 15 (`docs/UPKEEP.md`). The scheduled run stopped before it began because it had no
push access, so this one was run by hand on Nov 23. All 85 projects were worked through against official
sources only; the checklist and results are in `docs/upkeep/2026-11-23.md` and the new project leads in
`docs/upkeep/leads-2026-11-23.md`. 80 projects were re-checked and move to `lastVerified` 2026-11-23; 67 records
changed. Five could not be opened and keep their old date: willow-village, parkline, cahsr-sf-sj, northgate-san-rafael, ravenswood-business-district.
`_meta.lastVerified` moves to 2026-11-23. No geometry was redrawn.

Stage changes, each resting on the agency's own record:
- **tanforan:** in entitlement → entitled. San Bruno's notice of determination says the City approved the project on
  Nov 17, 2026 (https://ceqanet.lci.ca.gov/2023120409/4). The zoning and development agreement ordinances have a second
  reading on Dec 8, 2026; the Council's minutes aren't posted yet.
- **esmeralda:** in entitlement → entitled. Cloverdale's notice of determination gives approval on Nov 11, 2026
  (https://ceqanet.lci.ca.gov/2003072142/5).
- **berkeley-pier-ferry:** in entitlement → entitled. The Berkeley City Council certified the EIR and approved the project
  on Nov 17, 2026 (Resolutions 72,526 and 72,527).

Records that were out of date rather than changed since October (their sources couldn't be reached before):
- **transbay-block-4:** the 683-home, 47-story design never took effect. OCII now plans about 314 homes, 311 affordable,
  on Block 4 West (Resolution 07-2026, Apr 7, 2026: https://sfocii.org/files/inline-files/2026007.pdf).
- **potrero-yard:** the housing above the bus facility was dropped in 2025; the remaining 104-home building is an option
  the Board did not approve (Resolution 157-26, Mar 2026), so the home count is removed from the key numbers.
- **3333-california:** the development agreement's second amendment passed in 2024 (Ordinance 271-24); affordable homes
  185 → about 124 (Resolution 35-26).
- **98-franklin:** its development agreement was approved in July 2023 (Ordinance 152-23), not pending.

Links: 48 Legistar links that answered "Invalid parameters!" (they were built from the Legistar API's IDs, which the
public site doesn't accept) were replaced with the working page for the same file, in the records and in the two
geometry files and tracer scripts that cite them (`berryessa-flea-market` massing, `moffett-park` land use).

Per project (re-checked with no change: hunters-point-shipyard, stonestown, parkmerced, north-bayshore, concord-naval-weapons-station, sonoma-developmental-center, west-oakland-bart, lake-merritt-bart, el-cerrito-plaza-bart, amador-station, smart-cloverdale, 30-van-ness, southline, 5m):

- **candlestick-point:** Updated: `stageNote`. Timeline: 2026-10-28: City issues a grading permit for the development blocks south of Harney Way. `verify`: 1 settled or reworded, 0 added. Sources added: https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202603026735, https://sfocii.org/files/minutes/2026-11/20261020_OCII%20Minutes.pdf, https://sfocii.org/files/inline-files/MEMO_3rd%20Lien%20TABs%20Contracts.pdf.
- **potrero-power-station:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-10-13: Mayor approves the amended and restated development agreement (Ordinance 208-26) and the Special Use District amendments (Ordinance 209-26). `verify`: 1 settled or reworded, 2 added. Sources added: https://media.api.sf.gov/documents/o0208-26.pdf, https://media.api.sf.gov/documents/o0209-26.pdf.
- **pier-70:** Updated: `stageNote`, `nextMilestone`, `developer`. Timeline: 2026-11-10: Port Commission considers extending Phase 1's down-market delay to as late as June 26, 2027 (Resolution 26-55). `verify`: 0 settled or reworded, 1 added. Sources added: https://www.sfport.com/sites/default/files/2026-11/item_10b_pier_70_down_market_delay_extension.pdf, https://www.sfport.com/media/11635/download?inline.
- **mission-rock:** Updated: `nextMilestone`. Sources added: https://www.sfport.com/media/11635/download?inline.
- **mission-bay:** Updated: `stageNote`. Timeline: 2026-10-06: OCII's commission authorizes a memorandum of understanding with FOCIL-MB to pursue about 535 homes on Block 12 West (Resolution 23-2026). 2026-11-19: OCII seeks proposals for affordable rental homes on Block 12 West, due Jan 14, 2027. `verify`: 1 settled or reworded, 1 added. Sources added: https://sfocii.org/files/minutes/2026-10/20261006_OCII%20Minutes.pdf, https://sfocii.org/rfps-rfqs-bids, https://sfocii.org/files/inline-files/INFO%20MEMO_MBS%2012W_RFP%20w%20Att.pdf.
- **treasure-island:** Updated: `nextMilestone`, `program.notes`. Timeline: 2026-10-15: Planning Commission initiates General Plan amendments tied to the proposed unit increase (Resolution 21973), with a hearing to follow on or after Nov 19, 2026. 2026-11-06: TIDA board hears an update on the unit increase as an informational item. Sources added: https://citypln-m-extnl.sfgov.org/Commissions/CPC/11_5_2026/Commission%20Packet/20261015_cpc_min.pdf, https://www.sf.gov/meeting-20261106-november-6-2026-tida-board-of-directors-special-meeting-agenda/, https://citypln-m-extnl.sfgov.org/Commissions/CPC/10_15_2026/Commission%20Packet/2007.0903GPA-03.pdf, https://www.sf.gov/meeting-20261014-october-14-2026-tida-board-of-directors-meeting/.
- **india-basin:** Timeline: 2026-11-13: Mayor approves a $4 million EPA brownfield cleanup grant for the park's northern section at India Basin Shoreline Park (Resolution 622-26). Sources added: https://sfgov.legistar.com/LegislationDetail.aspx?ID=8283731&GUID=DF6098B8-1ADE-4E82-8CAA-746A1DDE7B5D.
- **balboa-reservoir:** Timeline: 2026-06-16: Board of Supervisors gives final passage to an amendment to the Balboa Reservoir Special Use District (Ordinance 113-26) allowing a connecting element between two buildings along South Street. 2026-10-06: Crane permit filed for Building E, to hoist prefabricated wall and floor panels. Sources added: https://sfgov.legistar.com/LegislationDetail.aspx?ID=7978143&GUID=2B33417B-E9D8-45F1-ADAC-8DC121060AE0, https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202608206888.
- **brisbane-baylands:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-11-19: City Council holds the eighth night of its hearing on the plan (after Oct 15, Oct 20, Oct 26 and Nov 9), on water infrastructure, public safety and EIR alternatives; no vote yet. `verify`: 0 settled or reworded, 2 added. Sources added: https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12784,plainText=false), https://www.brisbaneca.gov/baylands, https://brisbaneca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=12742,plainText=false).
- **related-santa-clara:** 5 broken links replaced. Sources added: https://santaclara.legistar.com/LegislationDetail.aspx?ID=4239313&GUID=AAE09BF9-4648-4B45-ABEB-58CED0C88584, https://santaclara.legistar.com/LegislationDetail.aspx?ID=7455918&GUID=AEF2FA4D-ECCE-48F6-A477-AA103E275420, https://santaclara.legistar.com/LegislationDetail.aspx?ID=7660315&GUID=815DA1DE-4859-4DC1-A0BC-8665B7568F3B, https://santaclara.legistar.com/LegislationDetail.aspx?ID=8260886&GUID=2791DE9D-56B5-49B5-9998-BC1264149D06 and 1 more.
- **downtown-west:** 2 broken links replaced. Sources added: https://sanjose.legistar.com/LegislationDetail.aspx?ID=4942606&GUID=95647CEF-77C3-4823-94A3-C8F237EEC832, https://sanjose.legistar.com/LegislationDetail.aspx?ID=4959970&GUID=A669CEDF-974D-4CE0-A5F0-439E6174923F.
- **moffett-park:** Updated: `nextMilestone`. `verify`: 1 settled or reworded, 1 added. 5 broken links replaced. Sources added: https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=6279900&GUID=3D3D73F4-F04E-4923-B1EB-857C1239B1FD, https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=6295721&GUID=47A18B74-19BA-426E-BEF4-27499DD5822B, https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=7773739&GUID=0FC3A0E2-161D-4932-874F-98AFA1606130, https://sunnyvaleca.legistar.com/LegislationDetail.aspx?ID=7796915&GUID=5F6AB8EB-3382-4CC1-B41F-47C04B67CBC5 and 2 more.
- **the-rise:** Updated: `stageNote`. Timeline: 2026-10-06: City Council postpones the bond hearing for the Block 5 affordable apartments (234 homes with Eden Housing) to Oct 20, 5-0. 2026-10-20: City Council tables the bond hearing for the Block 5 affordable apartments, 5-0, without holding it. `verify`: 1 settled or reworded, 2 added. 6 broken links replaced. Sources added: https://cupertino.legistar.com/LegislationDetail.aspx?ID=6779489&GUID=7D773B61-0A62-422C-9CC2-975EA4A91931, https://cupertino.legistar.com/LegislationDetail.aspx?ID=8139774&GUID=6969F75B-0A62-4D16-B3B6-0BB0BA14BF57, https://cupertino.legistar.com/LegislationDetail.aspx?ID=8257705&GUID=3A616707-35F9-4C81-A7EF-4E72BB30A0C9, https://cupertino.legistar.com/LegislationDetail.aspx?ID=8192826&GUID=C5D2FA5A-905D-4204-BBD6-4F6C74FE0FD8 and 5 more.
- **oakland-coliseum:** Updated: `stageNote`. `verify`: 2 settled or reworded, 2 added. 2 broken links replaced. Sources added: https://oakland.legistar.com/LegislationDetail.aspx?ID=8130453&GUID=5AFD9A11-F95D-42F4-B396-245C29D5D252, https://oakland.legistar.com/LegislationDetail.aspx?ID=8137317&GUID=B85D5978-183F-40EE-85E8-67B249C82045, https://alamedacounty.granicus.com/DocumentViewer.php?file=alamedacounty_6a9f300f359f2b86fa94b5db9f60e1d3.pdf&view=1, https://alamedacounty.granicus.com/DocumentViewer.php?file=alamedacounty_30ba8280d2b9f00f587a211bff53b1be.pdf&view=1.
- **alameda-point:** 6 broken links replaced. Sources added: https://alameda.legistar.com/LegislationDetail.aspx?ID=7933472&GUID=0A29DDC0-5697-401F-A920-7D774BD542A3, https://alameda.legistar.com/LegislationDetail.aspx?ID=5729459&GUID=5F880BAD-910F-4C9C-89B0-B3027C5FEB02, https://alameda.legistar.com/LegislationDetail.aspx?ID=5779285&GUID=F5314EB6-3179-41A9-9A35-4C0E39BD7138, https://alameda.legistar.com/LegislationDetail.aspx?ID=7977228&GUID=3D50F487-A822-4CEE-B0B8-B74E80D742C4 and 2 more.
- **brooklyn-basin:** Updated: `stageNote`. Timeline: 2026-10-20: City Council accepts a $250,000 federal grant to pass through to the developer for the Brooklyn Plaza park's shoreline cleanup and Bay Trail work (Resolution 91365). 6 broken links replaced. Sources added: https://oakland.legistar.com/LegislationDetail.aspx?ID=6101966&GUID=FB67D826-4FBE-4D65-9AD0-4740988AA665, https://oakland.legistar.com/LegislationDetail.aspx?ID=6101963&GUID=FE4676F2-7AEF-49BD-919F-2A033EF9365F, https://oakland.legistar.com/LegislationDetail.aspx?ID=7405588&GUID=36230CB8-87D4-4222-ADE5-CEC98ADCA06F, https://oakland.legistar.com/LegislationDetail.aspx?ID=1344901&GUID=275DD8A1-FC37-4619-819B-F04769658426 and 4 more.
- **suisun-expansion:** `verify`: 1 settled or reworded, 1 added.
- **berryessa-flea-market:** 4 broken links replaced. Sources added: https://sanjose.legistar.com/LegislationDetail.aspx?ID=4994843&GUID=EAF4E8F3-2F0B-4918-A6D2-64A540B70ABD, https://sanjose.legistar.com/LegislationDetail.aspx?ID=4994842&GUID=0406B7EA-EE4D-4FFA-BA01-C3871EE4AF9B, https://sanjose.legistar.com/LegislationDetail.aspx?ID=5036012&GUID=2814C991-D7E0-4ADD-BBE5-EB0C6FC53A67, https://sanjose.legistar.com/LegislationDetail.aspx?ID=7356352&GUID=698A8EE5-D43D-4FA6-A1AF-1F675B288306.
- **mare-island:** Updated: `nextMilestone`. `verify`: 1 settled or reworded, 1 added. Sources added: https://ceqanet.lci.ca.gov/search?City=Vallejo&StartRange=2026-07-01&EndRange=2026-11-23.
- **middlefield-park:** 1 broken link replaced. Sources added: https://mountainview.legistar.com/LegislationDetail.aspx?ID=5962472&GUID=822FF3FC-A868-4655-B32D-259947C8A171.
- **potrero-hope-sf:** Updated: `stageNote`, `nextMilestone`, `developer`. Timeline: 2026-04-15: BRIDGE Housing and the Mayor's Office of Housing and Community Development select MidPen Housing as replacement master developer, after a request for qualifications. 2026-10-29: Housing Authority Commission approves transferring BRIDGE's remaining master development obligations to MidPen Housing, subject to HUD approval. 2026-11-06: City's affordable housing loan committee considers a $2,000,000 master planning loan to MidPen Housing for work through June 2027. `verify`: 0 settled or reworded, 2 added. Sources added: https://www.sf.gov/meeting--20261106--citywide-affordable-housing-loan-committee-meeting/.
- **schlage-lock:** Sources added: https://sfplanning.org/sites/default/files/documents/citywide/VisValley/visvalley_planning_presentation-102926.pdf.
- **sunnydale-hope-sf:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-10-20: Ordinance introduced at the Board of Supervisors to accept the Phase 3 streets and public infrastructure (File 261150). `verify`: 0 settled or reworded, 1 added. Sources added: https://sfgov.legistar.com/LegislationDetail.aspx?ID=8298234&GUID=68D6ABF0-4B25-463D-869B-BF6BE4A3B073, https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202611090571, https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202611120686.
- **tasman-east:** Updated: `stageNote`. 8 broken links replaced. Sources added: https://santaclara.legistar.com/LegislationDetail.aspx?ID=3726712&GUID=E712D56A-E8CC-471C-98A4-B293B7C08392, https://santaclara.legistar.com/LegislationDetail.aspx?ID=3760176&GUID=2DE69108-3D74-4C26-8CED-0438D0668897, https://santaclara.legistar.com/LegislationDetail.aspx?ID=4622127&GUID=DCAE295E-AAB0-49D6-9B25-1297B03B9705, https://santaclara.legistar.com/LegislationDetail.aspx?ID=4696394&GUID=1F303F43-7109-4BAD-A95F-A3B4938FD293 and 5 more.
- **esmeralda:** `stage`: entitlement → **entitled**. Updated: `stageNote`, `nextMilestone`. Timeline: 2026-10-14: The City Council holds its second hearing and introduces the development agreement ordinance. 2026-10-28: The Council holds the first of three question-and-answer sessions and gives direction on changes to the development agreement. 2026-11-04: The Council reintroduces the development agreement ordinance as amended, with Councilmember Morgenstern voting no; the applicant agrees to a sitewide human health risk assessment. 2026-11-11: City Council approves the project: General Plan amendment, specific plan and zoning, objective design standards and development agreement, with the EIR addendum. 2026-11-18: The City files a notice of determination for the addendum (SCH 2003072142). `verify`: 1 settled or reworded, 4 added. Sources added: https://ceqanet.lci.ca.gov/2003072142/5, https://www.cloverdale.net/DocumentCenter/View/7140/Agenda-Report, https://cloverdale.granicus.com/services/legistar/download/pdf/4480131/CC_Minutes_-_November_4__2026.pdf, https://www.cloverdale.net/DocumentCenter/View/7138/Draft-Specific-Plan---Revised-111026.
- **the-portal:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-10-09: TJPA receives a proposal for the civil and tunnel progressive design-build contract. 2026-11-10: The California State Transportation Agency awards the project $750 million from the Transit and Intercity Rail Capital Program: $100 million in Cycle 8 for preconstruction and $650 million for construction. `verify`: 3 settled or reworded, 6 added. Sources added: https://www.tjpa.org/media/40613/download?inline, https://www.tjpa.org/about-tjpa/news-information/press-releases/transbay-joint-powers-authority-statement-transit-and, https://www.tjpa.org/media/40618/download?inline, https://www.tjpa.org/media/40625/download?inline.
- **cahsr-sf-sj:** `verify`: 1 settled or reworded, 0 added. Sources added: https://hsr.ca.gov/wp-content/uploads/2026/07/OIG-HSR-Review-of-2026-Business-Plan-A11Y.pdf.
- **bart-silicon-valley-phase-2:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-08-27: Excavation of the West Portal launch structure is complete. 2026-10-24: Crews pour the concrete floor of the West Portal launch shaft. `verify`: 0 settled or reworded, 4 added. Sources added: https://santaclaravta.iqm2.com/Citizens/FileOpen.aspx?Type=1&ID=4546&Inline=True, https://santaclaravta.iqm2.com/Citizens/FileOpen.aspx?Type=1&ID=4508&Inline=True.
- **diridon-station:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-09: SB 1375 is signed, giving the station project a statutory exemption from CEQA; federal environmental review is still required. 2026-11-04: The Steering Committee receives updates on the construction-authority legislation, funding and environmental review, and approves the program director's 2026-27 goals. `verify`: 2 settled or reworded, 3 added. 1 broken link replaced. Sources added: https://sanjose.legistar.com/LegislationDetail.aspx?ID=7423311&GUID=43A0E4F0-B5F2-4A88-B787-3CB71EC423D0, https://santaclaravta.iqm2.com/Citizens/FileOpen.aspx?Type=1&ID=4534&Inline=True, https://santaclaravta.iqm2.com/Citizens/FileOpen.aspx?Type=15&ID=3179&Inline=True, https://santaclaravta.iqm2.com/Citizens/Detail_Meeting.aspx?ID=4676.
- **valley-link:** Updated: `nextMilestone`. `verify`: 0 settled or reworded, 2 added. Sources added: https://www.valleylinkrail.com/_files/ugd/95df9a_356dbeca5ccb4849bcc50e9e65a9276f.pdf.
- **ucsf-parnassus:** Updated: `stageNote`. 1 broken link replaced. Sources added: https://ceqanet.lci.ca.gov/Project/2020010175.
- **tanforan:** `stage`: entitlement → **entitled**. Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2026-10-20: Planning Commission opens its hearing on the project, continued to Oct 26 and Nov 5. 2026-11-05: Planning Commission recommends certifying the EIR and approving the project, 4–0 (Resolutions 2026-03 and 2026-04). 2026-11-17: City Council approves the project and certifies the EIR; Notice of Determination filed Nov 18. `verify`: 2 settled or reworded, 2 added. Sources added: https://ceqanet.lci.ca.gov/2023120409/4/Attachment/EpUqLP, https://www.sanbruno.ca.gov/AgendaCenter/ViewFile/Agenda/_11172026-2687, https://www.sanbruno.ca.gov/AgendaCenter/ViewFile/Agenda/_11162026-2683, https://ceqanet.lci.ca.gov/2023120409/4.
- **north-berkeley-bart:** Timeline: 2026-11-17: Berkeley City Council approves the final map of Tract 8713 for the North Berkeley station site (Resolution 72,519-N.S.) and gives second reading to Ordinance 8,036-N.S., transferring four small adjacent pieces of City land to BART. Sources added: https://berkeleyca.gov/sites/default/files/city-council-meetings/2026-11-17%20Annotated%20Agenda%20-%20Council.pdf, https://berkeleyca.gov/sites/default/files/city-council-meetings/2026-10-27%20Annotated%20Agenda%20-%20Council.pdf.
- **ashby-bart:** Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2026-11-10: California State Transportation Agency awards $25 million for the Ashby West Lot's station entrance plaza, walking and biking connections and BART rider parking garage. 2026-11-17: Berkeley City Council adopts the Ashby West Lot objective design standards (Resolution 72,528-N.S.), unanimously. `verify`: 0 settled or reworded, 1 added. Sources added: https://berkeleyca.gov/sites/default/files/city-council-meetings/2026-11-17%20Annotated%20Agenda%20-%20Council.pdf.
- **smart-healdsburg:** Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2026-09-16: (Replace the existing Sept 16 entry) SMART's Board directs staff to run more public outreach on the Healdsburg station location, Depot/Hudson or Downtown. 2026-10-21: SMART's Board awards the first construction package, Windsor Station to Front Street, to Stacy and Witbeck/Herzog for $190,537,469 (Resolution 2026-36, 7-0 with five absent). 2026-10-22: SMART holds a community meeting at Healdsburg High School on the station location. `verify`: 2 settled or reworded, 4 added. Sources added: https://www.sonomamarintrain.org/sites/default/files/Documents/11.18.2026%20Board%20of%20Directors%20Packet%20COMPLETE.pdf, https://www.sonomamarintrain.org/sites/default/files/Documents/0%2010.21.2026%20Complete%20Agenda%20Package.pdf, https://www.sonomamarintrain.org/bod.
- **oceanwide-center:** Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2026-10-11: An application to modify the approved project is filed with the Planning Department as the “First and Mission Project” (2026-008984PRJ): a redesigned First Street Tower of about 1.5 million sq ft of office, with the Mission Street Tower unchanged. 2026-10-29: An environmental review application for the modification is opened (2026-008984ENV). `verify`: 1 settled or reworded, 3 added. Sources added: https://data.sfgov.org/resource/qvu5-m3a2.json?record_id=2026-008984PRJ, https://data.sfgov.org/resource/y673-d69b.json?record_id=2026-008984OFA, https://data.sfgov.org/resource/y673-d69b.json?record_id=2026-008984ENV, https://data.sfgov.org/resource/y673-d69b.json?record_id=2026-008984DNX.
- **west-midway-reshap:** Updated: `stageNote`, `nextMilestone`. Timeline: 2025-05-20: City Council approves the Tract 8696 final map for West Midway and RESHAP (Resolution 16275). 2026-10-06: City Council authorizes the State funding agreements for Stardust Gardens, RESHAP's 80-home first building: a $15 million Multifamily Housing Program loan (Resolution 16462) and the cooperation agreement for its $44.6 million AHSC award (Resolution 16461). `verify`: 1 settled or reworded, 1 added. Sources added: https://webapi.legistar.com/v1/alameda/matters/16087/texts/17300, https://webapi.legistar.com/v1/alameda/matters/14900/texts/16066, https://webapi.legistar.com/v1/alameda/matters/16208/texts/17430, https://webapi.legistar.com/v1/alameda/matters/16006/texts/17216.
- **alameda-point-plan:** Timeline: 2026-11-04: City Council, 4–1, directs an exclusive negotiating agreement with Neptune Beach Surf Club for a surf park at the 21-acre Enterprise Park, conditioned on a City-led master plan that includes a scenario without a surf park. Sources added: https://webapi.legistar.com/v1/alameda/matters/16274/texts/17505, https://webapi.legistar.com/v1/alameda/matters/16198/texts/17419.
- **encinal-terminals:** Timeline: 2026-05-19: City Council gives final passage to Ordinance 3403, the third amendment to the tidelands lease with Bayview Landing LP. `verify`: 1 settled or reworded, 0 added. Sources added: https://webapi.legistar.com/v1/alameda/matters/15886/texts/17093.
- **alameda-marina:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-07-21: City Council approves a settlement with Alameda Marina over development impact fees: the City waives $2.3 million of park and transportation fees if The Foundry pulls building permits by Oct 31, 2026. `verify`: 0 settled or reworded, 1 added. Sources added: https://webapi.legistar.com/v1/alameda/matters/16063/texts/17276.
- **mission-bay-ferry-landing:** Updated: `stageNote`. Timeline: 2025-05-13: The Port Commission awards the Phase 2a marine demolition and mattress contract to Vortex Marine Construction ($13,114,750; Resolution 25-26). `verify`: 1 settled or reworded, 0 added. Sources added: https://www.sfport.com/media/10697/download?inline, https://www.sfport.com/projects-programs/mission-bay-ferry-landing.
- **berkeley-pier-ferry:** `stage`: entitlement → **entitled**. Updated: `stageNote`, `nextMilestone`, `summary`, `program.notes`. Timeline: 2026-01-21: The Planning Commission recommends approval of the use permit for public ferry service at the pier. 2026-02-26: The Zoning Adjustments Board approves Use Permit ZP2026-0014 (5-0-3), subject to City Council action. 2026-09-16: The Governor certifies the project for streamlined judicial review under SB 149. 2026-11: The City publishes the Final EIR (on its website Nov 3; received by the State Clearinghouse Nov 5). 2026-11-17: The City Council unanimously certifies the Final EIR (Resolution 72,526) and approves the project and Use Permit ZP2026-0014 (Resolution 72,527), adopting the shortened-breakwater alternative. `verify`: 2 settled or reworded, 4 added. Sources added: https://berkeleyca.gov/sites/default/files/city-council-meetings/2026-11-17%20Annotated%20Agenda%20-%20Council.pdf, https://berkeleyca.gov/sites/default/files/city-council-meetings/2026-11-17%20Agenda%20Packet%20-%20Council%20-%20WEB.pdf, https://ceqanet.lci.ca.gov/2025040995/3, https://berkeleyca.gov/sites/default/files/2026-11-06%20%20%20Berkeley%20Pier-Ferry%20Project%20Frequently%20Asked%20Questions_0.pdf and 3 more.
- **redwood-city-ferry-terminal:** Updated: `stageNote`, `nextMilestone`.
- **santa-clara-station-area:** Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2026-10-15: The City's Station Area Task Force reviews the complete draft specific plan, dated October 2026. `verify`: 2 settled or reworded, 4 added. Sources added: https://santaclara.legistar.com/LegislationDetail.aspx?ID=8283112&GUID=9584BBD9-E098-4F80-B1AC-47C852C8D5E6, https://santaclara.legistar1.com/santaclara/attachments/469250e5-7551-4388-be56-f9e8cfbeccc6.pdf.
- **the-orchards:** Sources added: https://www.sanramon.ca.gov/news/what_s_new/the_orchards_appeal_denied/.
- **redwood-life:** Updated: `stageNote`. `verify`: 0 settled or reworded, 1 added.
- **eastridge-bart-regional-connector:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-07-31: VTA reports about 72% of the contract work complete, with more than two miles of bridge structure built. 2026-08: A Teamsters strike disrupts the project's concrete supply from Aug 7 until a settlement on Aug 20. `verify`: 0 settled or reworded, 2 added. Sources added: https://santaclaravta.iqm2.com/Citizens/FileOpen.aspx?Type=1&ID=4508&Inline=True.
- **larkspur-ferry-expansion:** Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2026-10-19: The District releases the Draft EIR for comment through Dec 3, 2026; it is filed with the State Clearinghouse on Oct 22. `verify`: 3 settled or reworded, 4 added. Sources added: https://ceqanet.lci.ca.gov/2024091190/4/Attachment/7jYVzt, https://ceqanet.lci.ca.gov/2024091190/4, https://ceqanet.lci.ca.gov/2024091190/4/Attachment/avs4zf.
- **sf-railyards:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-10-30: The scoping comment period on the notice of preparation closes. Sources added: https://ceqanet.lci.ca.gov/Project/2026091295.
- **655-4th-street:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-11-03: The Planning Department closes the project record. `verify`: 2 settled or reworded, 2 added. Sources added: https://data.sfgov.org/api/views/6jgi-cpb4.json, https://citypln-m-extnl.sfgov.org/Commissions/CPC/1_11_2024/Commission%20Packet/20231214_cpc_min.pdf, https://data.sfgov.org/resource/i98e-djp9.json?block=3787&lot=026, https://data.sfgov.org/resource/y673-d69b.json?record_id=2022-011490PCA.
- **88-bluxome:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-10-09: The city issues three revisions, filed in 2021, to the 2019 office project's site permits, removing basement levels (permits 202107265067, 202107265087 and 202107265105). `verify`: 1 settled or reworded, 3 added. Sources added: https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202107265067, https://data.sfgov.org/api/views/6jgi-cpb4.json, https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202107265087, https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20190725_cal_min.pdf and 1 more.
- **flower-mart:** Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2019-07-18: The Planning Commission approves the large project authorization and office allocation (Motions 20484 and 20485) and recommends the Planning Code and zoning map amendments and the development agreement (Resolutions 20483 and 20486). 2020-01-07: The Board of Supervisors finally passes the development agreement with KR Flower Mart, LLC (Ordinance 2-20) and the Planning Code and zoning map amendments (Ordinance 1-20); the Mayor signs them Jan 10. 2025-01: The wholesale flower market moves to its new permanent building at 901 16th Street, built by the project sponsor under the development agreement. 2026-10-01: The Planning Commission hears an informational presentation on the development agreement amendment and the revised project (up to 3,532 homes, heights of 350 to 600 ft) and takes no action. `verify`: 3 settled or reworded, 3 added. Sources added: https://citypln-m-extnl.sfgov.org/Commissions/CPC/10_1_2026/Commission%20Packet/2025-008569PRJ.pdf, https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20190718_cal_min.pdf, https://sfgov.legistar.com/LegislationDetail.aspx?ID=3983662&GUID=AD90D189-2F67-434C-8E57-4E9D960076D2, https://citypln-m-extnl.sfgov.org/Commissions/CPC/10_15_2026/Commission%20Packet/20261001_cpc_min.pdf and 3 more.
- **freedom-west:** Updated: `stageNote`, `nextMilestone`, `developer`, `program.notes`. Timeline: 2026-09-03: Planning Commission initiates the General Plan amendments (Resolution 21951) after an informational presentation. 2026-10-20: Ordinances for the development agreement (File 261144) and the Freedom West Special Use District (File 261146) are introduced at the Board of Supervisors; the Special Use District ordinance is substituted on Nov 3. 2026-11-16: The Planning Department publishes the responses to comments on the Draft EIR, with a Final EIR certification hearing set for Dec 3, 2026. `verify`: 1 settled or reworded, 2 added. Sources added: https://sfgov.legistar.com/View.ashx?M=F&ID=16087758&GUID=ECB36B3E-C019-4610-8437-7C5CE48D1E55, https://citypln-m-extnl.sfgov.org/Commissions/Agenda_or_Minutes/20260903_cpc_min.pdf, https://sfgov.legistar.com/LegislationDetail.aspx?ID=8298230&GUID=24933EA0-903C-4529-948A-D93064FD3FD4, https://sfgov.legistar.com/LegislationDetail.aspx?ID=8298231&GUID=5EFE4518-22E5-4AEE-8FD9-97A5E18110A8 and 2 more.
- **matson-block:** Updated: `stageNote`. Timeline: 2026-10-30: Permit applications are filed to drill groundwater test borings and wells under 77 Beale Street and 45 Beale Street (202610300149 and 202610300147). 2026-11-19: A permit application is filed for interior soft demolition and asbestos abatement at 77 Beale Street (202609188382), after similar applications for 45 Beale Street on Nov 2 (202609158122 and 202609238535). `verify`: 1 settled or reworded, 1 added. Sources added: https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202609188382, https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202610300149, https://ceqanet.lci.ca.gov/2025120794/Attachment/gufVD2, https://data.sfgov.org/resource/i98e-djp9.json?permit_number=202609158122.
- **3333-california:** `program.affordableHomes`: 185 → 124. Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2019-11-19: Board of Supervisors gives final passage to the development agreement (Ordinance 276-19); the Mayor approves it on Nov 27. 2024-11-19: Board of Supervisors gives final passage, 11–0, to the second amendment to the development agreement (Ordinance 271-24), extending the term to Sept 11, 2043 and reducing the required affordable homes; it is recorded on May 7, 2025. 2026-01-27: Board of Supervisors approves the infrastructure financing plan for Enhanced Infrastructure Financing District No. 3 (3333/3700 California Street) (Resolution 35-26). 2026-08-26: Permits filed to demolish the one-story medical office (annex) building and clear the site; an asbestos abatement permit follows on Sept 22. `verify`: 2 settled or reworded, 2 added. Sources added: https://sfgov.legistar.com/LegislationDetail.aspx?ID=6816059&GUID=2DE80F2E-8C1E-44C4-B2E4-71E275D4C016, https://sfgov.legistar.com/LegislationDetail.aspx?ID=4077307&GUID=55716B46-F3FC-49B3-96C1-774C7C2E5F52, https://sfgov.legistar.com/View.ashx?M=F&ID=13603964&GUID=1DC50036-3430-494C-A6BB-90C4A143C7F7, https://sfgov.legistar.com/LegislationDetail.aspx?ID=7785988&GUID=2B610238-AF2D-4CC9-8331-BA795FAB53EC and 3 more.
- **san-francisco-gateway:** Updated: `stageNote`, `nextMilestone`, `program.notes`. Timeline: 2025-12-02: The Board of Supervisors finally passes the San Francisco Gateway Special Use District with its height change to 97-X (Ordinance 248-25) and the development agreement with Prologis, L.P. (Ordinance 247-25), 11–0; the Mayor signs both on Dec 12. `verify`: 3 settled or reworded, 2 added. Sources added: https://sfgov.legistar.com/LegislationDetail.aspx?ID=7353452&GUID=1DE567B3-B28A-43A8-A161-99002EEE6B9E, https://data.sfgov.org/resource/i98e-djp9.json?block=5284A&lot=008, https://sfgov.legistar.com/LegislationDetail.aspx?ID=7353451&GUID=A2B164CB-7B89-4D1A-A9DB-F2E6D063A40D, https://sfgov.legistar.com/View.ashx?M=F&ID=14878372&GUID=35227FFD-033D-4497-99DC-57903E45DA41 and 2 more.
- **400-2nd-street:** Updated: `nextMilestone`. `verify`: 0 settled or reworded, 1 added. Sources added: https://data.sfgov.org/resource/i98e-djp9.json?permit_number=201912068933.
- **transbay-parcel-f:** Updated: `stageNote`, `nextMilestone`. Timeline: 2023-05-02: OCII records that the developer has told it Parcel F's development has stalled because of economic conditions, so the affordable housing fee meant to fund Transbay Block 4 was not secured (Resolution 17-2023). Sources added: https://sfocii.org/sites/default/files/inline-files/2023017.pdf.
- **524-howard:** Updated: `stageNote`, `nextMilestone`.
- **transbay-block-4:** `program.homes`: 683 → 314. `program.affordableHomes`: None → 311. `program.retailSqft`: 8339 → 4200. Updated: `stageNote`, `nextMilestone`, `summary`, `developer`, `program.notes`. Timeline: 2022-06-21: OCII's commission approves a 681-home project with F4 Transbay Partners: a redevelopment plan amendment, a disposition and development agreement and schematic designs (Resolutions 18-2022 to 23-2022). 2022-11-01: Board of Supervisors disapproves the General Plan amendment and sends the redevelopment plan amendment and agreement to committee, after the developer could not finance the project. 2023-05-02: OCII's commission grants F4 Transbay Partners a new option to buy Block 4, preserving the 2022 agreement while the developer waits for financing (Resolution 17-2023). 2025-05-08: OCII issues a request for proposals for affordable rental housing on the western part of the block, Block 4 West. 2026-04-07: OCII's commission authorizes exclusive negotiations and a $5 million predevelopment loan with Transbay Block 4 West, LP (Mercy Housing California and Young Community Developers) for about 314 affordable homes (Resolution 07-2026), and an agreement to design the East Tehama Street extension (Resolution 08-2026). `verify`: 3 settled or reworded, 4 added. Sources added: https://sfocii.org/files/inline-files/2026007.pdf, https://sfocii.org/files/inline-files/MEMO_TB%204W%20ENA%20Predev%20Loan%20Tehama%20Infrastructure%20and%20Attach%201-6_0.pdf, https://sfocii.org/sites/default/files/inline-files/2023017.pdf, https://sfocii.org/adopted-resolutions-2026 and 2 more.
- **10-south-van-ness:** Timeline: 2026-11-02: The Planning Department approves a temporary use authorization for interim use of the site as a community, cultural and private event space (2026-004476GEN). Sources added: https://data.sfgov.org/resource/y673-d69b.json?record_id=2026-004476GEN.
- **one-oak:** Timeline: 2026-09-14: The Planning Department closes the modified project's record with an approval letter (2024-005509PRJ). `verify`: 1 settled or reworded, 0 added.
- **98-franklin:** Updated: `stageNote`, `nextMilestone`, `summary`, `developer`, `program.notes`. Timeline: 2023-03-30: Planning Commission recommends the height and Planning Code changes and the development agreement (Resolutions 21297 and 21299). 2023-07-25: Board of Supervisors finally passes Ordinance 152-23, approving the development agreement with 98 Franklin Street, LLC; the Mayor approves it on July 28. `verify`: 4 settled or reworded, 4 added. Sources added: https://sfgov.legistar.com/LegislationDetail.aspx?ID=5941746&GUID=9463E8F0-C597-4226-A6C7-D24E0B71E7D2, https://sfgov.legistar.com/View.ashx?M=F&ID=12195250&GUID=02A8697E-BD65-4186-9386-603BFDF02BE7.
- **potrero-yard:** `program.homes`: 513 → None. `program.affordableHomes`: 513 → None. `program.retailSqft`: 3000 → None. Updated: `stageNote`, `nextMilestone`, `summary`, `developer`, `program.notes`. Timeline: 2024-03-12: The Board of Supervisors finally passes the Potrero Yard Special Use District and height change (Ordinance 58-24) and the General Plan amendment (Ordinance 57-24); the Mayor signs them Mar 22. 2026-02-04: The Planning Department records a second project modification, eliminating the housing above the transit facility's podium and keeping a 104-home building on Bryant Street, and finds no further environmental review is needed. 2026-03-24: The Board of Supervisors approves the project agreement with PRG - Potrero Properties LLC to design, build and finance the bus facility, with substantial completion scheduled for 2030 (Resolution 157-26, 10–0); the Mayor signs it Mar 26. `verify`: 3 settled or reworded, 4 added. Sources added: https://sfgov.legistar.com/View.ashx?M=F&ID=15342706&GUID=82EE0322-A57D-463A-8AE1-DC2C18835057, https://sfgov.legistar.com/LegislationDetail.aspx?ID=7933673&GUID=94D0AC27-66BA-40E1-BA4C-8BF674B1C8D8, https://sfgov.legistar.com/LegislationDetail.aspx?ID=6446241&GUID=8F25D96D-30DE-40BC-A3FD-B524C4AE7A2A, https://sfgov.legistar.com/View.ashx?M=F&ID=15280362&GUID=66F1AFE1-C6CC-4252-B55E-144E71D82819 and 4 more.
- **598-brannan:** Updated: `stageNote`, `nextMilestone`. Timeline: 2026-11-05: The sponsor applies for a five-year extension of the approvals' performance period and changes to their validity conditions (2012.0640ENX-02 and OFA-03). `verify`: 1 settled or reworded, 2 added. 1 broken link replaced. Sources added: https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20190606_cal.pdf, https://data.sfgov.org/resource/y673-d69b.json?record_id=2012.0640ENX-02, https://data.sfgov.org/resource/y673-d69b.json?record_id=2012.0640OFA-03.
- **725-harrison:** Updated: `stageNote`, `nextMilestone`, `developer`. Timeline: 2026-09-24: The Planning Commission extends the Large Project Authorization and conditional use authorization by eighteen months, to Mar 24, 2028 (Motions 21962 and 21963, 6–0); the acting Zoning Administrator indicates an intent to grant the variance. `verify`: 1 settled or reworded, 2 added. Sources added: https://citypln-m-extnl.sfgov.org/Commissions/CPC/10_15_2026/Commission%20Packet/20260924_cpc_min.pdf, https://sfplanning.org/sites/default/files/agendas/2026-09/20260924_cpc%20%28ID%201588046%29.pdf, https://citypln-m-extnl.sfgov.org/Commissions/CPC/9_24_2026/Commission%20Packet/2005.0759ENX-03CUA-03VAR-04_Final.pdf.
- **kaiser-2190-ofarrell:** Sources added: https://data.sfgov.org/resource/y673-d69b.json?record_id=2026-004681SHD, https://data.sfgov.org/resource/y673-d69b.json?record_id=2026-004681TDM.

## 2026-11-04 (sixteen San Francisco projects added)

Matthew asked for "any final projects that you think I should add, focus on san francisco", then "add all six and the towers" from the Oct 28 scan (`docs/official-research/candidates-sf-scan-2026-10-28.md`), and then "the projects near van ness and market". Fourteen come from the scan (researched and checked Oct 28; their records were re-checked for changes Nov 4 and keep `lastVerified` 2026-10-28) and two from Van Ness and Market (checked Nov 4). Facts from DataSF's Planning Department records, Development Pipeline (Q2 2026) and building permits, SF Planning's environmental review listing, project pages and Planning Commission agendas and minutes, and CEQAnet. No press was read, so nothing is recorded as reported. Boundaries are each site's lots from DataSF parcels (for 3333 California, its special use district), official except where no lot list could be reached (Freedom West, Kaiser), which are marked approximate. No massing: no plan set could be reached. `_meta.lastVerified` moves to 2026-11-04. Not added: 1338 Mission Street (a 30-story, 287-home tower near Van Ness), whose environmental review was cancelled in March 2024 and project authorization withdrawn in 2023.

- **freedom-west** (new, buildings): in entitlement. The rebuilding of the Freedom West housing cooperative (382 homes) on two Fillmore blocks into 15 buildings of 85 to 335 ft with up to 2,393 homes, an optional 150-room hotel, 68,600 sq ft of commercial and 14,800 sq ft of community space, about 3.7 million gross sq ft; sponsor MacFarlane Partners (2020-006887PRJ). Notice of preparation Apr 30, 2025; Draft EIR Jan 13, 2026; general plan, rezoning and development agreement applications May 5, 2026. Boundary: lots 0770/027 and 0783/023-025 from DataSF parcels, approximate (10.8 acres as drawn against 10.37; no lot list reachable, and the adjacent 880 McAllister senior building shares lot 0770/027).
- **matson-block** (new, buildings): in entitlement. Hines's plan for the block of Market, Main, Mission and Beale streets: a mostly office tower of up to 1,225 ft plus a 75-ft crown replacing 77 Beale Street, the 215 and 245 Market Street buildings renovated, 25 Beale converted to 44-120 homes, up to 1,919,847 sq ft of office and 250,000 sq ft of retail, 2,402,347 gross sq ft in all (2021-012562PRJ). Notice of preparation of an EIR Dec 17, 2025 (CEQAnet SCH 2025120794). Boundary: the eleven lots CEQAnet lists (3711/005-014 and 019) from DataSF parcels, official (3.48 acres as drawn; 3.47 stated).
- **3333-california** (new, buildings): entitled. Prado Group's redevelopment of the 10.25-acre office campus at California Street and Presidio Avenue: the 455,000-sq-ft office building split into two residential buildings and 13 new buildings, 744 homes (25% affordable under the development agreement), about 35,000 sq ft of retail, a childcare center and 4.47 acres of open space, about 1,428,000 gross sq ft (2015-014028). EIR hearing and clearance Sept 5, 2019; development agreement and special use district recorded as approved Apr 14, 2022; an amendment reducing the affordable housing under review since Sept 2024; building permit applications filed Feb-Aug 2026. Boundary: the 3333 California Street Special Use District from DataSF, official (10.26 acres as drawn).
- **5m** (new, buildings): partly built. The 5M district at Fifth and Mission (about 4 acres; development agreement with 5M Project, LLC and the Fifth and Mission Special Use District recorded as approved Dec 2, 2015; applicant Forest City). A 25-story office building at 415 Natoma (completed Apr 1, 2022) and a 21-story, 302-home building at 434 Minna (completed Sept 29, 2022) are built; the pipeline counts 688 homes in all, 386 still to build, and 676,000 sq ft of office. Boundary: the 16 active lots inside DataSF's Fifth and Mission Special Use District, joined across the alleys, official (4.4 acres as drawn).
- **san-francisco-gateway** (new, buildings): entitled. Prologis, L.P.'s plan for two industrial buildings up to 97 ft (1,646,000 gross sq ft, up to 1,637,600 sq ft of PDR, 8,400 sq ft of retail) on two Bayview blocks at 749 Toland Street and 2000 McKinnon Avenue (2015-012491). The Planning Commission took up the Final EIR, special use district, height change, development agreement and conditional use on Sept 25, 2025, and the Planning Department's record shows the project approved that day; the Board's adoption is in `verify`. Boundary: the two lots the agendas name (13.33 acres; 17.1 with street portions).
- **400-2nd-street** (new, buildings): entitled. One Vassar (2012.1384, One Vassar, LLC): a 350-ft residential tower with 489 homes, a 350-ft office tower and a 200-ft hotel building over 645 Harrison Street, about 1.5 million gross sq ft, approved by the Planning Commission Feb 20, 2020 (Motion 20665). The office building's permit was approved in 2023 but not issued. Boundary: the eleven still-active lots of the hearing's list (Block 3763; 2.01 acres); lot 112, split in 2017, isn't drawn.
- **transbay-parcel-f** (new, buildings): entitled. Parcel F Owner LLC's 61-story tower at 542-550 Howard Street, about 750 ft (800 ft with its screen), with 165 homes, 189 hotel rooms and 275,674 gross sq ft of offices, approved by the Planning Commission Jan 9, 2020 (2016-013312); a 2021 development agreement lets it pay an affordable housing fee. Permits filed 2019 and 2021, not issued. Boundary: block 3721 lots 016 and 136 (lot 136 replaced the records' lot 015A in 2017), about 0.50 acres.
- **524-howard** (new, buildings): entitled. A 72-story residential tower at 524 and 530 Howard Street, about 795 ft, with 672 homes (68 at 50% of area median income) and a bridge to Salesforce Park; approved 2024 (pipeline approval June 18; record closed with an approval letter Sept 17, 2024, 2023-010883PRJ). Site permit filed Nov 2023, not issued. Boundary: block 3721 lots 013 and 014 (the site permit's lots), about 0.40 acres.
- **transbay-block-4** (new, buildings): in entitlement. OCII's Transbay Block 4 at 200 Main Street: a 47-story, 501-ft building and a 16-story building with 683 homes (site permits for 491 and 192 homes filed Dec 2019, not issued). CEQA clearance Jan 31, 2023 (2018-015785ENV); the 2022 height and zoning map amendments were withdrawn in 2025, and no approval is recorded in the sources read, so OCII's status is in `verify`. Boundary: block 3739 lot 010, about 1.04 acres.
- **10-south-van-ness** (new, buildings): entitled. Crescent Heights' tower at Market and South Van Ness: a 67-story building with 921 homes, approved with a letter Aug 18, 2026 (2024-008986, filed under the state's streamlined approval law); a 55-story, 590-ft design with 966 homes was approved in 2020 after an EIR (2015-004568). Home counts differ between records, so they're in `verify`. Demolition permit filed Oct 23, 2026. Boundary: block 3506 lots 003A and 004, about 1.19 acres.
- **one-oak** (new, buildings): entitled. Emerald Fund's tower at 1500-1540 Market Street, at Market, Van Ness and Oak: 41 stories, 400 ft to the roof, 541 homes over a 14-story podium and a public plaza in Oak Street, approved Mar 19, 2026 after an addendum dated Mar 4 (2024-005509PRJ); first approved June 15, 2017 with 304 homes (2009.0159) and modified in July 2022 for 460. The pipeline estimates 91 affordable homes; the record lists none, so it's in `verify`. The 2016 building permit application hasn't been issued. Boundary: block 0836 lots 001-005, the project record's lot and the four the Planning Department's project review names (0.42 acres).
- **98-franklin** (new, buildings): entitled. A 36-story tower at 98 Franklin Street with 345 homes (69 affordable on site) over classrooms for the International High School of the French American International School, approved May 28, 2020 (2016-014802, Motion 20728). A revision to 400 ft and up to 385 homes cleared its code and zoning map amendments (July 2023), revised authorization (Aug 2023) and environmental addendum (Jan 30, 2025); its development agreement (Board file 221163) is still under review. The building permit filed Feb 18, 2021 hasn't been issued. Boundary: block 0836 lots 008, 009 and 013, as the record names them (0.51 acres).
- **potrero-yard** (new, transportation): entitled. SFMTA's Potrero Yard Modernization (2019-021884): one building of about 1,250,000 gross sq ft, 70 to 150 ft, with a bus facility for up to 213 buses and up to 513 homes on top through a joint development (Potrero Neighborhood Collective LLC), on the block at 2500 Mariposa Street. The Planning Commission took up the Final EIR and approvals Jan 11, 2024; the record closed with an approval letter Nov 26, 2024, and the plan and code amendments closed as approved Mar 10, 2026. Asbestos removal ahead of demolition was permitted Oct 7, 2026. The Oct 17 lead scan had excluded it on a press figure of about 100 homes. Boundary: Block 3971 Lot 001 (4.45 acres).
- **598-brannan** (new, buildings): entitled. The Central SoMa Plan's Park Block (2012.0640, Brannan & Bryant Street LLC): three office buildings with 922,737 sq ft of office up to 185 ft, a public park and a land dedication for affordable housing, approved June 6, 2019 (Motions 20459 and 20460). Two office building permits were issued in 2021 and the site cleared, but no office construction followed; the affordable building on the dedicated parcel (160 Freelon Street, 85 homes) is under construction separately. Boundary: the four lots the hearing lists, with lot 052 drawn as its 2025 successors (Block 3777; 4.51 acres).
- **725-harrison** (new, buildings): entitled. Boston Properties' 14-story, 185-ft office building of about 981,000 gross sq ft (810,000 office) at 725-765 Harrison Street (2005.0759), approved Dec 12, 2019 and revised June 16, 2022 (Motions 21128-21130); its approvals, expired June 2025, were extended in 2026 (Large Project Authorization, Sept 29). Lot 149 is dedicated for affordable housing. Boundary: Block 3762 lots 152 (148 and 113, merged 2022) and 149 (2.40 acres; 104,188 sq ft in the record).
- **kaiser-2190-ofarrell** (new, buildings): proposed. Kaiser Permanente's Replacement Hospital Project at 2190 O'Farrell Street: a 14-story, 266-ft hospital (694,012 sq ft) and a 12-level, 1,003-space garage (534,274 sq ft), filed May 29, 2026 (2026-004681PRJ) with environmental review, conditional use and rezoning applications June 12; record on hold. Boundary: block 1098 lots 009 and 050, the lots the records name, about 3.2 acres (approximate).

## 2026-10-27 (three Central SoMa key sites beside the railyards added)

Matthew asked to "locate all the projects happening around the cal train railyard" and then to add the
three largest. All three are Central SoMa Plan key development sites within about 250 m of `sf-railyards`.
Facts from DataSF's Planning Department records and Development Pipeline (Q2 2026), the 2018 Central SoMa
Plan and SF Planning's environmental review listing; research in
`docs/official-research/candidates-around-railyards.md`. No press was read, so nothing is recorded as
reported. Boundaries are the sites' lots from DataSF parcels (official). No massing: no approved plan set
could be reached. `_meta.lastVerified` moves to 2026-10-27.

- **655-4th-street** (new, buildings): entitled. The Planning Commission approved a mixed-use project on
  June 20, 2019 (Motions 20470 and 20471); the modified, residential project (2022-011490PRJ, sponsor 655 4th
  Owner, L.L.C.) was approved Dec 14, 2023 after a community plan evaluation dated Nov 30, 2023. Two towers
  of about 380 and 400 ft with 1,096 homes (1,105 in the project description) and 9,857 sq ft of retail, on
  a 71,290-sq-ft lot at Fourth and Townsend (lots 3787/026, 028, 050, 161-164; 1.66 acres as drawn).
- **88-bluxome** (new, buildings): entitled. Filed May 27, 2025 (2025-004642PRJ) and closed Dec 12, 2025 with
  an approval letter and a decision of Approved. The pipeline doesn't mark it as holding an approved
  entitlement, so the approval's basis is in `verify`. Two towers of 599 and 528 ft with 1,500 rental homes
  (150 affordable in the pipeline), a 22,690-sq-ft parcel for the City's future affordable housing and
  Bluxome Linear Park, on the 2.6-acre Bay Club tennis lot (3786/037). The site's 2019 office project
  (Alexandria Real Estate; Motion 20493, modified 2023) is in the timeline.
- **flower-mart** (new, buildings): entitled. Approved in 2019 (office allocation, large project
  authorization, development agreement, Planning Code and zoning map amendments; community plan evaluation
  and addendum dated Sept 17, 2019) for three buildings with 2,061,380 sq ft of offices, 47,586 sq ft of retail
  and a replacement wholesale flower market; owner KR Flower Mart, LLC. The program shows the approved
  project. The revised project filed Sept 12, 2025 (2025-008569PRJ, in environmental review; amendment
  applications May 6, 2026) is in the notes: offices and labs, or variants with up to about 3,500 homes in
  buildings of up to 500 ft. Boundary: block 3778 lots 1B, 2B, 4, 5, 47 and 48 (6.84 acres as drawn; 295,144 sq
  ft in a 2016 record).

## 2026-10-21 (SF Railyards added)

**sf-railyards** (new, buildings): Matthew asked to include "the potential redevelopment of Caltrain's
railyards near Mission Bay". The Railyards Mixed-Use Development Project at 700 4th Street is added in
entitlement: Prologis 4th & King LLC filed its application with the Planning Department on Mar 11, 2026
(record 2026-002123PRJ) and a development agreement application on Apr 15, and the Department issued a
notice of preparation of an EIR on Sept 30, 2026 (Case 2026-002123ENV, CEQAnet SCH 2026091295; comments to
Oct 30). The NOP studies two scenarios on the 18.63-acre station and yard between Townsend, Fourth, King and
Seventh streets: up to 1,765 homes with 5.64 million sq ft of commercial space, or up to 5,834 homes with
1.59 million sq ft, about 7.8 million sq ft above grade either way, with the terminal tracks moved into a new
tunnel next to The Portal's, a 19,560-sq-ft station hall, 3.73 acres of open space, an offsite train yard
not yet sited, and proposed height limits of 350 to 855 ft; construction is assumed from 2029 to 2042. The
boundary is the four lots the NOP names, from DataSF parcels (official, 18.6 acres). Illustrative height
envelopes for the eight blocks are traced from the NOP's Figure 3, Height District Plan, and labelled
proposed. Facts from CEQAnet, the NOP, DataSF's Planning Department records and SF Planning's program, RAB
and environmental review pages; research in `docs/official-research/candidates-4th-king-railyards.md`.
Caltrain's Board packets and press pages couldn't be reached, so nothing is recorded as reported.
`_meta.lastVerified` moves to 2026-10-21.

## 2026-10-19 (Larkspur ferry expansion added; Harbor Bay held)

**larkspur-ferry-expansion** (new, transportation): Matthew asked to add the proposed ferry projects
"farther down the line", the two he pre-approved on Oct 12. The Golden Gate Bridge, Highway and
Transportation District's Larkspur ferry service and parking expansion is added at its current stage,
in entitlement: notice of preparation of a Draft EIR, Sept 30, 2024 (CEQAnet SCH 2024091190); no Draft
EIR yet. Service would grow "from 42 daily trips to as many as 76 daily trips through 2050", possibly with
a new route to the foot of 16th Street, plus more parking and better access to the SMART station. The
site (terminal, main and overflow lots, SMART station link, 14.5 acres as drawn) is traced from the
NOP's Figure 2 and drawn as approximate. Facts from CEQAnet, the NOP, the District's study page and Plan
Bay Area 2050+; research in `docs/official-research/candidates-harbor-bay-larkspur-ferries.md`. The
District's site, goldengate.org, joins the official hosts.

**Harbor Bay replacement terminal** (WETA, not added): WETA has published no site, CEQA document or
figure for the new terminal, only that it will be "north of the existing terminal" (FY27 budget, p. 19).
A boundary around the existing terminal would be the wrong place, and one to the north would be
invented, so it stays on the pre-approved list until WETA shows a site.

## 2026-10-19 (BART station-area housing split into six station projects)

Matthew asked to separate the BART station housing into each station. `bart-station-housing` is removed
and replaced by six projects, each built only from the facts, sources and geometry the program record
already had for that station (nothing re-checked, so `lastVerified` stays 2026-10-07):

- **west-oakland-bart** (West Oakland BART, Mandela Station): under construction (240 affordable homes since
  Sept 14, 2026); 762 homes (240 affordable, 31% per BART), about 300,000 sq ft of office and 53,000 sq ft of
  retail (BART's West Oakland page); 5.5 acres.
- **lake-merritt-bart**: under construction (senior Building B since Oct 2024, completion spring 2027 per
  BART); 557 homes, 40% affordable (BART Board report, 2022), up to 500,000 sq ft of office; 2.8 acres. The
  program record's "233 affordable" was a sum of BART's per-building figures and is now stated as those
  figures in the notes, with the share as the Board report gives it.
- **north-berkeley-bart**: entitled (City of Berkeley, Dec 11, 2024, under AB 2011); 739 homes, 381
  affordable; 8.1 acres. Adds the February 2024 AB 2011 application, from the City's 2024 General Plan
  progress report already cited.
- **ashby-bart** (Ashby BART, West Lot): proposed (developer selected, negotiating agreement February 2026,
  no application with the City yet); up to 600 homes, half affordable; 4.5 acres. Adds the Dec 20, 2024
  exchange agreement from BART's Ashby page, already cited. The envelope's 80-ft R-BMU limit is now cited to
  the City's Preliminary Objective Design Standards for the Ashby West Lot (Dec 2024, Sec. 1.2, posted on
  bart.gov) instead of the North Berkeley standards; same limit.
- **el-cerrito-plaza-bart**: under construction (Parcel A South since Nov 2025); 743 homes, 350 affordable by
  the City's approvals (BART: 351), stated in the notes; 7.5 acres. Keeps the building-heights `verify` item.
- **amador-station** (Amador Station, West Dublin/Pleasanton BART): entitled (Dublin Planning Commission,
  Aug 10, 2021); 300 homes, all affordable; 3.6 acres.

Each gets its own boundary (`data/boundaries/<id>.geojson`, the same BART TOD Work Plan parcels and accuracy
as its part of the old boundary) and massing (`data/massing/<id>.geojson`, the same features), written by
`bam_pipeline.sites.bart_stations` (renamed from `bart_station_housing`; `make sites`). Each has its own
landing camera. The Lake Merritt photo moves to `lake-merritt-bart`. The program's other notes (Walnut
Creek Phase III, Fremont, Bay Fair, Richmond Phase II) move to `_meta.candidatesNotYetResearched`. The
program-level facts (3,701 homes in all; 4,232 homes delivered at 15 stations) are no longer shown.

## 2026-10-18 (Esmeralda: the Oct 7 council hearing)

**esmeralda**: Matthew asked for an update after the City Council hearings. The City's agenda report
for Oct 14, 2026 (https://www.cloverdale.net/DocumentCenter/View/7092/Agenda-Report) says the Council
held a public hearing on Oct 7, "decided not to take any action at that meeting, and instead provided
direction regarding potential changes to the Development Agreement", and that on Oct 14 it would
consider introducing the zoning and development agreement ordinances, with "a second reading of the
ordinances" on Nov 11 if the first reading is approved, when it "will also consider action to approve the
other proposed entitlements and Addendum". The Oct 7 event is added to the timeline, the stage note and
next milestone now point to Nov 11, and the Oct 14 outcome stays a `verify` item: the minutes of
neither meeting are posted yet. A press report of a 3–2 vote on Oct 14 was seen only as a search
snippet and isn't recorded. Stage unchanged (in entitlement).

## 2026-10-17 (five new projects from the Oct 17 lead scan)

Matthew asked to add the six strong leads in `docs/upkeep/leads-2026-10-17.md`. Five are added; the
sixth (CityView Plaza) is held back. Research and every figure's source are in
`docs/official-research/candidates-santa-clara-station-redwood-life.md`,
`candidates-orchards-cityview.md` and `candidates-southline-eastridge.md`.

**santa-clara-station-area** (new): the City of Santa Clara's Station Area Specific Plan, about
244 acres around the Santa Clara Caltrain station and planned BART station: up to 8,300 homes,
2.1 million sq ft of office and 1.7 million sq ft of light industrial (notice of preparation, June 12,
2026, CEQAnet SCH 2026060462). In entitlement. Boundary approximate, traced from the notice's Figure 2
and fitted to OpenStreetMap streets; no land use until a plan is published.

**the-orchards** (new): the former Chevron Park campus in San Ramon, approved for up to 2,510 homes on
about 92 acres: Planning Commission Resolution 02-26 (Feb 3, 2026), appeal denied by the City Council
on Apr 7, 2026. Sources: the City of San Ramon's project and news pages, the CEQAnet notice of
exemption (SCH 2026020219) and the 2040 General Plan notice of determination. Entitled. Boundary
(APN 213-120-008) approximate, traced from the 2040 General Plan Draft EIR's land-use map (88.6 acres
as drawn, against 92 official). No massing yet: the approved plans are on City hosts this environment
couldn't reach.

**southline** (new): an office and research campus of up to 2.8 million sq ft on 28.5 acres by San
Bruno BART in South San Francisco, approved by the City Council on July 13, 2022 (notices of
determination). Entitled. Boundary and illustrative massing (height envelopes from the revised
Specific Plan's Figure 2-8) traced from the Final EIR (CEQAnet SCH 2020050452). Press reports of
Phase 1 construction were found only as search snippets (the press sites were unreachable), so they
aren't recorded; whether Phase 1 is built is a `verify` item.

**redwood-life** (new): the Redwood LIFE Precise Plan in Redwood Shores, Redwood City: 11 life science
buildings of about 2.7 million sq ft, a hotel and 42 acres of open space replacing a 20-building office
park (notice of preparation, Aug 22, 2025, SCH 2025081015). In entitlement. Boundary approximate, traced
from the notice's Figure 3 and fitted to OpenStreetMap buildings. Two press items seen only in search
snippets (the study session that chose "Alternative 2", a schedule slip) aren't recorded.

**eastridge-bart-regional-connector** (new, transportation): VTA's 2.4-mile light rail extension from
Alum Rock to the Eastridge Transit Center, with elevated Story Road and at-grade Eastridge stations.
Under construction (contract awarded March 7, 2024; VTA reported it 67% complete on May 31, 2026;
service expected early 2028). Line and stations traced from VTA's 2018 Draft SEIR-2 plan sheets; facts
from VTA's fact sheet, newsletters and CEQA notices (SCH 2001092014).

**CityView Plaza** (San José, not added): a 2025 amendment (a new eight-story retail and parking
building, office space converted to 330 homes) may have partly superseded the 2020 three-tower
approval, and the documents that settle it are on sanjoseca.gov, which this environment couldn't
reach. It stays a lead.

`_meta.lastVerified` is 2026-10-17, the newest record date.

## 2026-10-17 (later: official boundaries for the new projects; the Orchards plans)

The County parcel services (`data.sccgov.org`, `data.smcgov.org`) and the City of San Ramon's document server
(`docs.sanramon.ca.gov`) became reachable, so the four traced boundaries added earlier today were redone from them.
Details and quotes are in the same research notes.

**redwood-life**: boundary now `official`, the County of San Mateo parcels (nr6j-72z7) for the four APNs the notice of
preparation names (095-012-150, -220, -450, -460): 84.2 acres against the notice's 84 (the trace was 81.9; up to 35 m
apart). Its `verify` item on the exact line is resolved.

**southline**: boundary now `official`. The six APNs on the CEQA filing aren't in the County layer any more (the site was
re-mapped after 2022); the County's five parcels on the same assessor's page (014-250-110, -120, -130, -150, -170) fill
the revised Specific Plan's plan line, and are joined over the new Southline Avenue: 28.0 acres against the plan's 28.5
(the trace was 28.4; up to 27 m apart, at a street corner). The massing was re-run on the new boundary (unchanged
otherwise). The `verify` item on the County parcels is resolved.

**santa-clara-station-area**: boundary redrawn from the Santa Clara County parcels (ubcd-cewv) for the 185 APNs on the
City's CEQAnet record (174 found; four re-mapped successors inside the notice's boundary added), joined over the streets:
about 249 acres against the notice's 244 (the trace from the notice's small-scale Figure 2 was 208). It stays
`approximate`: the parcel list fits the notice's written bounds and acreage but takes in blocks the figure leaves out
(residential blocks along Franklin Street, a Santa Clara University parcel, parcels on De La Cruz Boulevard, Grant Street
and Campbell Avenue), up to about 300 m from the traced line. The `verify` item now asks for the City's plan-area map.

**the-orchards**: from the approved record on `docs.sanramon.ca.gov` (City Council Resolution 2026-040, Apr 7, 2026; the
Applicant's Project Plans of Sept 5, 2025 with Vesting Tentative Map 9693; the Orchards Design Guidelines of Nov 14,
2025; the Affordable Housing Plan of Dec 4, 2025):
- program: 397 affordable homes, 16.2% of the 2,452 homes (163 very low, 212 low and 22 moderate income), and 125,000 sq ft
  of ground-floor retail, entertainment and commercial uses in the Mixed-Use District (Resolution 2026-040); notes now
  give the 2,452 homes plus 58 optional ADUs and the 85-ft height limit.
- boundary: now `traced` from the tentative map's sheet C3.0 (Parcel A, 91.55 acres), a CAD sheet at 1" = 100' placed on
  OpenStreetMap footprints by the existing buildings it draws (trimmed RMS 0.8 m): 91.6 acres (the General Plan EIR trace
  was 88.6; up to 35 m apart). Contra Costa County's parcel map still can't be reached, so it isn't `official`.
- massing (new, illustrative): the tentative map's development parcels and lots (sheet C2.0) raised to the design
  guidelines' limits: 85 ft in the Mixed-Use District and on the Multi-Family B and C parcels, 65 ft on the E, F, G and H
  parcels, 40 ft on the attached row townhome lots and 35 ft on the single-family lots.
- `verify`: the affordable/commercial and massing items are resolved; the County parcel check stays, and two new items
  record the resolution's two APNs (213-701-002 in its heading, 213-120-008 in its text) and the 30-ft single-family
  limit in the plan set's standards table against the guidelines' 35 ft.

No new official hosts were needed (`docs.sanramon.ca.gov` is a `.gov` host). `data/CREDITS.md` lists the new geometry;
the County parcel layers were already credited.

## 2026-10-13 (Berkeley ferry: dredged channel drawn apart)

**berkeley-pier-ferry**: Matthew asked for the site not to run so far into the Bay, so I re-checked it
against the Draft EIR (CEQAnet SCH 2025040995). The official project site really does run about 3 miles
from the shoreline (p. 3.4-12), because the existing 100-ft federal navigation channel along the closed
pier is dredged for the ferries (p. 2-28). Figures 2-2 and 2-3 draw it that way, and the trace matches
them. What gets built is much shorter: a pier of at most 1,080 by 22 ft, a 400 by 15 ft breakwater and
two 135 by 42 ft floats (pp. 2-6 and 2-10).

The boundary file now splits the site where its outline narrows, about 1,600 ft out (the end of the
southern staging area):
- the 54 acres around the pier, plaza and streets stay the filled site that the fly-in frames and the
  marker sits on;
- the 132 acres of channel beyond are a separate "dredging" feature, drawn dotted and unfilled, with a
  note in the panel.

Together they are the same 186 acres as before. No facts changed and `lastVerified` is unchanged.

## 2026-10-12 (Alameda Point photo)

**alameda-point-plan**: photo swapped at Matthew's request from the 1995 Navy aerial to Bill Abbott's
October 2018 aerial of Alameda Point's piers and hangars (CC BY-SA 2.0, Wikimedia Commons).

## 2026-10-12 (photos: transit and newer sites)

Fourteen more project photos approved by Matthew from `docs/images/candidates-transit.md` and
`docs/images/candidates-newer-sites.md`, downloaded from Wikimedia Commons (credits in
`data/CREDITS.md`): the-portal, cahsr-sf-sj, bart-silicon-valley-phase-2, diridon-station, valley-link,
smart-healdsburg, smart-cloverdale, mission-bay-ferry-landing, berkeley-pier-ferry,
redwood-city-ferry-terminal, ucsf-parnassus, northgate-san-rafael, bart-station-housing and
alameda-point-plan.

- **smart-cloverdale:** SMART's stations page still lists the Cloverdale station site as "TBD", so the
  caption says only "the existing Cloverdale station" and a note says the site is to be determined.
- **berkeley-pier-ferry:** the recommended Flickr photo ("berkeley pier", eb78) isn't on Commons, so the
  Commons alternative "Berkeley pier old part 3308" (Amatulic, 2014) is used.
- **redwood-city-ferry-terminal:** the USACE aerial has no date on Commons or in its file, so it's shown
  as an undated photo.
- **alameda-point-plan:** the recommended Seaplane Lagoon aerial is the same Commons file alameda-point
  already uses, and the next two candidates are Flickr-only, so the next listed Commons candidate is
  used: the 1995 Navy aerial of Naval Air Station Alameda (public domain), marked as historic.
- **the-portal:** Commons dates the photo 26 January 2015, although its title says June 2015; the
  credit uses the Commons date.
- `docs/images/PERMISSIONS.md` gains the permission contacts from both research files (rows 39-68,
  with rows 27 and 34 extended) and all 21 of their projects in the per-project checklist.

## 2026-10-12 (photos)

Four more approved project photos downloaded from Wikimedia Commons: berryessa-flea-market,
concord-naval-weapons-station, suisun-expansion and sonoma-developmental-center (credits in
`data/CREDITS.md`). The Rise's is still pending (Wikimedia rate limits).

## 2026-10-12 (New ferry terminals: Mission Bay, Berkeley, Redwood City)

Three new ferry terminals added at Matthew's request ("please check for upcoming ferry terminals, and add as
applicable"). Survey, with the terminals left out (Harbor Bay's planned replacement, the Vallejo reconfiguration,
Larkspur's expansion, Treasure Island and other electrification work, Carquinez Strait ideas, finished terminals):
`docs/official-research/candidates-ferry-terminals.md`. Each is its own project (different lead agencies, stages
and CEQA records), not a program. No press facts were needed, so none has a `reported` block.

- **mission-bay-ferry-landing** (`infrastructure`): a two-berth landing at Terry A. Francois Boulevard and 16th
  Street. Final MND June 18, 2018 (Case 2017-008824ENV), permits 2019-2025, Phase 1 dredging finished 2020. On July
  23, 2026 the Public Works Commission awarded the $33,018,200 Phase 2B contract (landing, plaza, Agua Vista Park);
  construction expected August 2026 to May 2028. WETA builds the charging float and expects electric service in
  November 2028.
- **berkeley-pier-ferry** (`entitlement`): the City of Berkeley's new 1,080-ft public pier, breakwater and ferry
  terminal replacing the pier closed in 2015. Draft EIR Feb 27, 2026 (SCH 2025040995); Final EIR to the Council in
  fall 2026; $105.8 million at 60% design (City, Sept 2026), with no construction funding yet.
- **redwood-city-ferry-terminal** (`entitlement`): the Port of Redwood City's two-berth terminal for service to San
  Francisco and Oakland, with a rezoning for a future hotel and restaurants. Draft EIR Sept 17, 2026 (SCH
  2024041306), comments to Nov 2, 2026; construction assumed from 2027.
- **Geometry:** Mission Bay and Redwood City boundaries from the parcels named in their CEQA documents (DataSF;
  County of San Mateo; new entries in `official_boundaries.py`). Berkeley's traced from the Draft EIR's Figure 2-2
  with its inset (`boundary_berkeley_pier_ferry.py`, added to `make sites`). No massing for any of them. Screenshots
  `docs/screenshots/m4/40`–`42`.
- **Hosts:** WETA's `sfbayferry.com` (and its former `sanfranciscobayferry.com`), WETA's document store
  (`d262kwcyxl71on.cloudfront.net/wp-content/uploads/`, prefix only) and San Francisco Public Works'
  `sfpublicworks.org`, with the proof in the findings file.

## 2026-10-12 (Alameda: West Midway and RESHAP, the rest of Alameda Point, Encinal Terminals, Alameda Marina)

Four City of Alameda projects added at Matthew's request ("whatever is going on with Alameda"). Research,
with the items left out: `docs/official-research/candidates-alameda.md`. Every fact is from City of Alameda
Legistar records (staff reports, minutes, attachments) and City and County GIS; no press facts were needed, so
none of the four has a `reported` block. No new hosts were needed. `alameda-point` (Site A) is unchanged.

- **west-midway-reshap** (`infrastructure`): 478 Brookfield/Catellus townhomes and condominiums (West Midway) and
  RESHAP's 332 supportive and affordable homes on one 34.5-acre block of the Main Street Neighborhood; 324 homes
  (40%) deed-restricted very low and low income (Dec 2023 staff report). Ordinances 3345–3348 (Sept 5, 2023) and
  3364 (Mar 19, 2024); Phase A design (284 homes) approved Dec 8, 2025. Demolition is done and RESHAP's site work is
  nearly complete (City, Aug 2026); West Midway vertical construction aimed at Q1 2027.
- **alameda-point-plan** (`entitled`, plan-scale): the rest of the former naval air station outside Site A and West
  Midway/RESHAP, drawn as the City's Alameda Point zoning districts (Main Street Neighborhood, Waterfront Town Center,
  Adaptive Reuse, Enterprise District, open space). No homes figure: the City's 2026 study of Main Street Neighborhood
  North (600–1,000 homes, a developer RFQ being weighed) and the October 2025 Navy fee cut (Resolution 16333) are in
  the notes; Pacific Fusion's 2025 withdrawal from the Enterprise District is in the timeline.
- **encinal-terminals** (`entitled`): 589 homes (80 affordable), 50,000 sq ft, a 160-slip marina and 4.5 acres of
  waterfront park on a vacant 23-acre site (Ordinances 3311–3313, Feb 1, 2022). Milestones extended by Ordinance 3379
  (Jan 21, 2025); a two-year EV storage use permit (Mar 23, 2026) runs to the first site milestone in March 2028.
- **alameda-marina** (`partial`): 801 homes on the 44-acre marina site (760 in 2018; Ordinance 3351, 2023). The Launch
  (360) is complete, 182 townhomes are under construction, The Foundry (259) is approved; Ordinance 3406 (July 7, 2026)
  cut The Foundry's affordable homes from 43 to 21, so 95 affordable homes in all.
- **Geometry:** boundaries from Alameda County Assessor parcels (West Midway/RESHAP, Encinal Terminals; new entries in
  `official_boundaries.py`, which gains a `close_m` option to join a subdivision's lots over its streets) and the City
  of Alameda's zoning GIS (Alameda Marina; the Alameda Point plan area, written by its land-use module). Massing:
  West Midway's blocks traced from its 2023 Development Plan (40/50 ft) and RESHAP's buildings from its 2023 land use
  diagram (±50 ft), fitted to the parcels (`massing_west_midway_reshap.py`); Alameda Marina's Launch from OpenStreetMap
  at 60 ft with the unbuilt phases as lots at 45 and 65 ft (`massing_alameda_marina.py`); Alameda Point land-use zones
  as published (`landuse_alameda_point_plan.py`). Encinal Terminals has a boundary only (its master plan sets no
  blocks or designs). All three modules are in `make sites`. Screenshots `docs/screenshots/m4/36`–`39`.
- Credits: the City of Alameda's zoning layer states no license (open item, `data/CREDITS.md`); the in-map credits
  now name the City of Alameda.

## 2026-10-12 (Oceanwide Center and 30 Van Ness added)

Two single-site San Francisco towers added at Matthew's request ("Oceanside center" and 30 Van Ness). Both are
well below the usual 1,000-home bar. Research: `docs/official-research/candidates-oceanwide-30-van-ness.md`.
No San Francisco record uses the name "Oceanside Center"; the match is Oceanwide Center at 50 First Street.
No new hosts were needed.

- **oceanwide-center** (`paused`): two towers approved by the Planning Commission on May 5, 2016 (Motions
  19634–19638): an 850-ft First Street Tower (910 ft to its top, office and 109 homes) and a 605-ft Mission Street
  Tower (169-room hotel and 156 homes), 265 homes and about 1.08 million sq ft of office in all. Ordinance 137-16
  (July 26, 2016) vacated and sold parts of Jessie Street and Elim Alley. DBI issued both site permits in 2017;
  demolition, shoring and excavation followed, and the last inspection recorded under the Mission Street Tower's
  site permit is Sept 21, 2020. An Aug 17, 2026 Zoning Administrator record calls the site "formerly Oceanwide".
  The creditor takeover, foreclosure, January 2026 sale and the new owner's "Fifty at First" office tower are
  press-only and sit in `reported` (with the press stage, `distressed`).
- **30-van-ness** (`paused`): a 47-story, 520-ft tower (540 ft with screening) with 333 homes over a nine-story
  office podium, approved May 21, 2020 and amended Nov 7, 2024 (Motion 21643) and March 13, 2025 (Motion 21700).
  Construction began July 18, 2022 and was halted about 16 months later (Ordinance 01-25, finally passed Jan 28,
  2025, which also created the 30 Van Ness Avenue Special Use District with lower affordable housing terms and a
  May 1, 2029 sunset unless construction restarts).
- **Geometry:** boundaries from DataSF parcels (new entries in `official_boundaries.py`). Massing is illustrative
  and drawn as paused: Oceanwide's two towers traced from the 2016 CPE checklist's floor plans (registered to the
  parcels, RMS 0.3 m; `massing_oceanwide_center.py`); 30 Van Ness's podium and tower laid out from the 2020 plan
  set's dimensions (`massing_30_van_ness.py`). Both modules are in `make sites`. Tuned landing cameras; screenshots
  `docs/screenshots/m4/34-landed-oceanwide-center.png` and `35-landed-30-van-ness.png`.
- `_meta.lastVerified` moves to 2026-10-12, the date these two were checked.

## 2026-10-08 (SMART Healdsburg and Cloverdale extensions added)

Two line projects added at Matthew's request ("the green line additions for SMART"). Research:
`docs/official-research/candidates-smart.md`. Every claim was then re-checked adversarially on Oct 8: 270 held,
37 corrections were applied (several of them newer official facts, such as the Phase I amendment and the CTC's
Oct 15-16 allocation) and 3 flags were overturned. Hosts approved: `sonomamarintrain.org` and
`planbayarea.org`.

- **smart-healdsburg** (`entitled`): about 9 miles from Windsor to Lytton Springs Road, with a new Healdsburg station.
  - Funded at $268,749,000 per the CTC baseline agreement and the CTC's January 2026 item.
  - CEQA addendum adopted Dec 17, 2025.
  - Progressive design-build Phase I awarded Sept 17, 2025 and amended Aug 19, 2026 ($22.5 million).
  - The CTC considers a $162.2 million construction allocation on Oct 15-16, 2026.
  - SMART's schedule: construction from 2027, service December 2028.
  - The station is drawn at the Depot/Hudson site and named "site under review" (SMART is consulting on a
    Downtown alternative; decision aimed at December 2026).
- **smart-cloverdale** (`proposed`, dashed): about 13.5 miles to Cloverdale, with stations at Geyserville (adopted
  Aug 19, 2026; notice of exemption SCH 2026080751) and Cloverdale (site to be determined).
  - Environmentally cleared in 2006/2008, but no construction funding or schedule.
  - Plan Bay Area 2050+ lists it at $353 million capital.
- **Geometry** (`pipeline/bam_pipeline/sites/lines_smart.py`, new `make sites` step):
  - NTAD rail lines (SMART-owned, out-of-service track), cut at County of Sonoma street crossings.
  - Stations from the National Transit Map, SMART's station layer and the County's Geyserville parcel.
  - 8.86 and 13.45 miles as drawn, a median 4 and 6 m from SMART's own track layer.
- `_meta.lastVerified` moves to 2026-10-08, the date of the SMART re-check.

## 2026-10-07 (San Francisco waterfront flood defenses removed)

Removed `sf-waterfront-flood-defense` from the map at Matthew's request. The record moves to `_meta.dropped`; its
line and corridor files (`data/lines/`, `data/boundaries/`), its pipeline step and its credits row are deleted. The
research notes and draft record stay in `docs/official-research/` as history.

## 2026-10-07 (hosts approved; held facts applied)

Matthew approved the eight agency hosts listed in `docs/OFFICIAL-SOURCES.md` ("Hosts approved 2026-10-07"), and
the facts held for them are applied. Findings: `docs/official-research/update-2026-10-07-east-north.md` and
`update-2026-10-07-peninsula-south.md`; key quotes re-checked against the documents on Oct 7. `lastVerified` unchanged.

- **mare-island:**
  - Acres 5,250 → 3,131: the City's April 27, 2026 report gives about 3,131 acres (1,302 developable) for the
    draft new plan, which keeps the existing plan boundary (the drawn 2005 plan area measures about 3,090). The
    5,250 is the whole island in the 2005 EIR.
  - The April 2026 range (9,750 to 14,400 homes, 895 dormitory units) and the City's tentative schedule: NOP late
    summer 2026, public draft EIR winter 2026–27, adoption hearings fall or winter 2027.
  - Timeline: 2001 Lennar development agreement; the July 31, 2019 consent to transfer to the Nimitz Group (escrow
    closed November 2019); the Connolly Street pause (Apr 27, 2026); the final extension to Sept 11, 2031
    (Resolution 138 N.C., July 28, 2026).
  - Press corrected: the 2019 purchase was Lennar's South Island, about 670 acres, not "about 500". Both press
    timeline entries are dropped from `reported`, which is now empty.
- **oakland-coliseum:** the County Board was still negotiating price and terms in closed session on Oct 6, 2026;
  no closing recorded. Next milestone notes the Sept 1 target has passed (deadline Jan 30, 2027).
- **suisun-expansion:**
  - No annexation application filed with Solano LAFCo as of Aug 10, 2026.
  - The County's airport land use commission calls the Draft EIR "forthcoming" (Aug 2026).
  - The posted (unsigned) reimbursement agreement phases growth to full buildout in 2071.
  - Solano County opposed the shipbuilding bill 3–2 (Aug 25, 2026).
  - The June 10, 2025 Council approval is now also sourced to County file 25-577.
- **bart-station-housing:**
  - Resolved from BART Board records:
    - Lake Merritt stays at 557 homes, approved by the Oakland Planning Commission on May 19, 2021.
    - The senior building's final development plan was approved July 20, 2022, with completion expected spring 2027.
    - West Oakland is 522 market rate and 240 affordable.
    - North Berkeley stays at 739; its option agreement was executed June 2026.
    - The Ashby West Lot negotiating agreement was executed February 2026.
  - Amador Station (City of Dublin): Site Development Review approved Aug 10, 2021 for 300 affordable homes in two
    buildings of 5 stories and 61 ft; agreements Sept 21, 2021; building permits for the first building under
    review. Its illustrative envelope is now drawn at the approved 61 ft instead of the 90-ft zoning limit
    (`make sites` output; only that feature changed).
- **tasman-east:** the City of Santa Clara's open-data terms (May 21, 2018, §IX) put the zoning layer under ODC
  PDDL 1.0; recorded in `data/CREDITS.md` and the boundary file. The license verify item is resolved.

## 2026-10-07 (official-source pass: East Bay, North Bay and BART)

Findings: `docs/official-research/update-2026-10-07-east-north.md`. `lastVerified` unchanged. Facts whose only
source is on a host not yet approved (see `docs/OFFICIAL-SOURCES.md`, "Hosts awaiting approval") are not applied.

- **concord-naval-weapons-station:**
  - Area Plan adopted Jan 24, 2012 (Resolution 12-4823.2).
  - Concord First Partners' agreement was allowed to expire Jan 31, 2023 (3–2, Jan 28).
  - Brookfield was picked Aug 26, 2023.
  - SB 328 was signed Sept 29, 2026 (Chapter 785), not Sept 30.
  - The press's "Lennar withdrew" is corrected: the Council declined to extend Lennar's agreement, which
    expired Mar 31, 2020.
  - All verify items resolved; the $6B cost estimate stays press-only.
- **alameda-point:** the Radium arts center's lease option passed May 5, 2026 (Ordinance 3399; Planning Board
  approval Mar 23). Block 11 was never built. Phase 2 land was conveyed Dec 29, 2022. The press's "May 2018
  groundbreaking" is dropped: the city record says infrastructure began in March 2018.
- **brooklyn-basin:** developer structure confirmed from the City's 2025 bond statement: Zarsion-OHP I, a joint
  venture of Oakland Harbor Partners (Signature and Reynolds & Brown) and Zarsion America. The City bought the
  affordable parcels Aug 28, 2014, and consented to the agreement's transfer Apr 22, 2014. BCDC has amended
  the permit three times, none for the 600 added homes.
- **suisun-expansion:** Solano LAFCo added as the responsible agency for the annexation (the notice of
  preparation). The June 10, 2025 reimbursement agreement is dated from the City's FAQ. The CEO's
  "175,000 homes" is dropped in favor of the official 173,913.
- **mare-island:** from the North Mare Island agreement (cityofvallejo.net): plan adopted March 1999,
  exclusive negotiation from July 2018, agreement signed May 24, 2022 (about 157 acres). The October 2024 draft
  plan's maximum is about 14,400 homes (356 existing) and 8.22 million sq ft. The City's April 2026 report
  and the July 2026 extension of the South Mare Island agreement are on Vallejo's CivicClerk host, which awaits
  approval.
- **sonoma-developmental-center:** added the 2024 CAL FIRE transfer (about 58 acres) and the applicant's
  proposed three phases (March 2027 to August 2036). The Draft EIR is still not expected in 2026.
- **esmeralda:**
  - The Planning Commission voted 4–1 on Oct 1, 2026 to recommend approval. The Council's first reading is
    Oct 7 and final action Oct 14.
  - The developer is in contract to buy the land; Spight Properties II still owns it.
  - Up to 1,524 residents (EIR addendum).
  - The build-out phases are estimates, not guaranteed dates.
  - Re-check after Oct 14.
- **bart-station-housing:** Lake Merritt's senior building broke ground Oct 17, 2024 (ABAG; BART's project
  page). El Cerrito Plaza's affordable total is the City's 350. The heights, Walnut Creek parcel and Fremont
  items are narrowed. The items resolved by BART Board and Dublin records wait for host approval.

## 2026-10-07 (official-source pass: Peninsula and South Bay)

Findings: `docs/official-research/update-2026-10-07-peninsula-south.md`. `lastVerified` unchanged. No stage changes.

- **brisbane-baylands:**
  - The press's "small portion in San Francisco" is contradicted: the plan area is entirely within Brisbane.
  - The press's "2027 start" is the plan's projected completion of remediation west of Caltrain (mid-2027),
    not a construction start.
  - A development agreement is required; the Council hears it Oct 26, after more hearings Oct 15 and
    Oct 20, with deliberations Nov 9, 2026.
  - Confirmed for the summary: a former rail yard and San Francisco landfill on the city line, two decades
    in planning (first EIR notice Feb 27, 2006).
- **willow-village:** the approval numbers are Resolutions 6790–6794 (Dec 6, 2022) and Ordinances 1094 and
  1095 (Dec 13, 2022, 4–0 with one recusal). The development agreement was recorded Mar 31, 2023, and its
  initial term runs to January 2033, not 2032. The reason for the pause stays press-only.
- **parkline:** the approval numbers are Resolutions 6996–6999 and Ordinances 1125–1126. City staff report
  that SRI has decided to vacate Buildings P, S and T and may occupy a new office building. The Phase 2
  home mix (220 single-family, 108 townhomes) is confirmed. The city's page and staff report differ on
  the below-market-rate count (293 vs 294).
- **related-santa-clara:** confirmed: the former golf course and closed landfill across from Levi's Stadium,
  and the CityPlace name. Added: the city's Oct 2026 note that data centers on Parcels 1–2 need a
  conditional use permit and that Silicon Valley Power has accepted no new data-center applications since 2023.
- **downtown-west:** the ordinances were finally adopted June 8, 2021 (30608–30610). Heights are 160–290 ft
  above ground, subject to FAA review. The Nov 2024 memo's interim-use note is added. Google's 2026
  ministerial permit filings are noted as an open question.
- **north-bayshore:** Google's termination of the Landings office project (Feb 2024) is confirmed by city
  reports and moves out of `reported`. No permit for a master-plan phase has come before the city since 2023.
- **moffett-park:** confirmed Resolution 1199-23 (EIR) and 40 affordable homes at 1215 Bordeaux Dr.
- **the-rise:**
  - The press's "2019 mall demolished" is contradicted (demolition permits were issued in Sept 2021), so it
    is dropped.
  - Votes: Resolution 24-077 (fee waiver, 4–1) and Resolution 26-080 (Phase 1 final map, 4–0 with one
    abstention). The 2022 modification is dated June 3, 2022.
  - Tallest building: about 228 ft (an office tower) in the 2024 approved plans. The press's "about 200 ft"
    is the tallest residential tower.
- **middlefield-park:** the development agreement is Ordinance 19.22. The Council approved the Clyde Ave park
  lease terms June 23, 2026 (7–0).
- **tasman-east:** the Draft Supplemental EIR for the 1,500-home amendment was released Aug 28, 2026
  (comments to Oct 13). Its status figures are added: 2,664 homes in built and approved projects, two
  approvals abandoned, about 12 acres left. The zoning layer's PDDL license is on a city ArcGIS Hub host
  that needs Matthew's approval, so it stays open.
- **berryessa-flea-market:** no new application found in the city's planning data (verify item narrowed).

## 2026-10-07 (official-source pass: east San Francisco)

Findings: `docs/official-research/update-2026-10-07-sf-east.md`. `lastVerified` unchanged (only these items re-checked).

- **potrero-power-station:**
  - The Board of Supervisors passed the amended development agreement and Special Use District on first
    reading Sept 29, 2026 (11–0) and finally on Oct 6, 2026. Legistar status is "Mayors Office"; there are
    no ordinance numbers yet. Next milestone: the Mayor's signature.
  - UCSF's Block 2 building is under construction, on the Planning Commission's finding in Resolution
    21945 (July 30, 2026). The massing shows Block 2 as under construction: `STAGES` in
    `pipeline/bam_pipeline/sites/potrero_power_station.py` and the massing file. The press's Aug 2025
    start month stays in `reported`.
  - The amended heights (to 248 ft) aren't drawn until the amendments take effect.
  - The Sophie Maxwell opening (Oct 2025) stays held back: the only record is a developer release
    reposted on sfbos.org.
- **candlestick-point:**
  - Developer confirmed as FivePoint Holdings, LLC (OCII). The "Lennar spinoff" wording stays in `reported`.
  - OCII's Candlestick-only affordable share is about 34%, counting workforce homes.
  - Confirmed from OCII: the first phase's seven blocks (six residential, one commercial), infrastructure
    first, and no building permits yet.
  - The groundbreaking date is Sept 9 (not the press's Sept 10). Final map recorded June 22, 2026.
  - The 2024 changes don't alter tower limits outside Candlestick Center.
- **hunters-point-shipyard:**
  - The 2038 date is the Navy's conveyance estimate (2036–2038), not a FivePoint start date, so the press
    note is dropped.
  - Confirmed: the Phase 1 roads and about 7 acres of parks (2026 capital plan), and Lennar/BVHP's
    selection on Mar 30, 1999.
  - New: retesting on Parcel C since Aug 2022, and 767 Phase 1 homes complete by June 30, 2025 (OCII
    draft report).
- **pier-70:**
  - Port (Aug 2026): Building 12 is nearly 90% leased and still the only vertical building; Buildings 2
    and 21 aren't rehabilitated. The approved Phase 1 anticipates 588 homes; the press's "about 700" is the
    developer's proposal.
  - The July 2026 neighborhood presentations are confirmed. General Catalyst stays unconfirmed: the Port
    names two venture capital firms without naming them.
- **mission-rock:** developer confirmed (Seawall Lot 337 Associates, whose sole member is Mission Rock
  Partners: the Giants and Tishman Speyer). Block heights confirmed against the 2018 Design Controls. Retail
  at build-out: 241,000–244,800 gsf of retail and production space (Port, 2019).
- **mission-bay:**
  - The density increase is partly enacted. Block 4 East: OCII approval (Nov 2025), Ordinance 22-26
    (Feb 2026; plan cap 3,440 to 3,690 homes, 250-ft height) and two building permits (June and Sept 2026).
    Block 12 West: about 535 homes proposed, approvals expected in early 2027.
  - New parks schedule: nine parks in four years (2026 capital plan). Mission Bay North has no hotel.
  - Fixed a broken OCII source link.
- **india-basin:**
  - 900 Innes opened in October 2024 (Rec and Park).
  - No Board amendment to the development agreement was found. Planning approved Phase 1 (2020), a
    design-standards amendment (Oct 2024) and Phase 2 (Nov 2024).
  - The default stays unconfirmed, so the stage stays entitled.

## 2026-10-07 (official-source pass: west San Francisco and HOPE SF)

Each project's held-back press facts (`reported`) and open questions (`verify`) were checked against
official records. Findings, with URLs, pages and quotes: `docs/official-research/update-2026-10-07-sf-west.md`.
`lastVerified` is unchanged, because only these items were re-checked, not whole records.

- **treasure-island:** developer now names its owners (Stockbridge, Wilson Meany, Kenwood Investments,
  Lennar; Board Budget and Legislative Analyst, 2024), replacing the press's "TIDG" in `reported`. Homes
  completed: more than 1,200 by May 2026 (City Administrator), up from about 1,000. The press's
  "phase one complete in July 2026" is contradicted: Planning says Major Phase 1 builds out through 2027.
  It and its timeline entry are dropped. Added: the 2016 start of Stage 1 infrastructure (TIDA schedule),
  the Bay FC facility permit (Jan 6, 2026), TIDA's unit-increase schedule (Board action targeted for
  November) and 490 Avenue of the Palms switching to rentals (TIDA, Sept 2026).
- **stonestown:** the 30 acres are "parking lots and streets" (Mayor's Office), so `reported.acresNote` is
  removed. The affordable options are now spelled out from the development agreement (up to three parcels for
  100% affordable buildings, inclusionary homes, or a fee on up to 390 homes). Added the Board's
  approval of the financing plan (Resolution 36-26, Jan 27, 2026).
- **balboa-reservoir:** the educator housing is confirmed by the adopted development agreement: about 150
  homes, with City College first priority and SFUSD second. The press note is removed, and the open-space split
  is added (park 2.0, SFPUC 1.2, paseos 0.8 acres).
- **parkmerced:** no official record of the default, receivership or takeover, so the stage stays
  entitled. Added Planning's Sept 2024 finding of no construction since 2011. Phase 1 affordable
  homes corrected to 48 + 37 on site plus about $59.4M in fees, and heights corrected to the zoning's
  45–145 ft (Ordinance 91-11; the 35-ft figure came from the 2010 staff report).
- **potrero-hope-sf:** affordable homes now 800 (about 619 replacement + 200 tax-credit; MOHCD, 2025).
  Phase 3 demolition has started: 23 permits (153 units) issued in April 2026, 19 marked complete by
  Sept 1, 2026 (DBI, re-checked today). The City's 2022 schedule (last phase in 2034) is added.
- **sunnydale-hope-sf:** EIR/EIS certified July 9, 2015 (Motion 19409), with CEQA findings Nov 17, 2016;
  the buildings are Block 6 (242 Hahn St) and Block 7 (65 Santos St). The development agreement counts
  694 market-rate and 1,074 affordable homes. All verify items are resolved.
- **schlage-lock:** the agreement took effect Feb 27, 2015 for 15 years. The 2009 ordinances were finally
  passed Apr 28, 2009. Grading began in 2016 and site preparation finished in early 2019. Zone 1 is about
  20 acres (parcels listed). The Dec 2019 filings were three buildings, not two (146, 152 and 258 homes).

## 2026-10-07 (ten projects added; line projects)

Ten projects added after official-source research (notes in `docs/official-research/candidates-*.md`,
Oct 7): The Portal, California High-Speed Rail San Francisco to San Jose, BART Silicon Valley Phase II,
Diridon Station, Valley Link (Phase 1A), the San Francisco waterfront flood defenses, UCSF Parnassus
Heights, Tanforan, Northgate Town Square and the Ravenswood Business District / 4 Corners plan. Link21 is
listed under `_meta.dropped` as a watch item: no alignment yet, and federal corridor planning isn't
expected to start until 2027. Corrections to commonly reported figures are in each record (for example,
UCSF's "1,200 homes" is the citywide MOU commitment; the plan adds 762 on campus).

Line projects (Matthew chose the cased-line style, option C): six projects are drawn as alignments with
stations (`data/lines/`, written by `bam_pipeline.sites.lines`), with a 60 m corridor as their boundary
for selection. Sources: TJPA's Sept 2026 status report figure (The Portal, traced, RMS 1.2 m); US DOT BTS
NTAD rail network and Caltrain GTFS (HSR; CHSRA's own layers forbid redistribution and were used only to
check); VTA's public alignment layers (BART Phase II); Valley Link's June 2026 packet and 2024 Draft SEIR
figures (traced, RMS 1.3–3.0 m); the Port's Aug 2026 phasing map (waterfront, traced, RMS 2.6 m; drawn
11.3 mi along the water's edge against the official 7.5 mi, flagged). Diridon is a traced station
footprint (partial). Site boundaries: DataSF parcels (UCSF, approximate), San Mateo County parcels
(Tanforan), Marin County parcels (Northgate) and East Palo Alto's plan boundary minus University Village
(Ravenswood). Open licence items: VTA GIS, Marin County parcels and East Palo Alto's layers state none.

## 2026-10-07 (BART station-area housing, added)

New project `bart-station-housing`, added at Matthew's request as one program-level entry: BART's
housing on its own station land where the work isn't finished. No single site reaches the usual
1,000-home bar (see `docs/official-research/candidates-transit-south-bay.md`). Re-checked BART's
upcoming and completed TOD pages today: Millbrae's Gateway is now listed as completed (2025), so it
is left out with the other 15 delivered stations (4,232 homes, 874,000 sq ft). Six sites are drawn:
West Oakland (762 homes; 240 affordable under construction since Sept 14, 2026), Lake Merritt (557
homes and up to 500,000 sq ft of office; the senior building is under construction), North Berkeley
(739 homes, entitled Dec 2024), the Ashby West Lot (up to 600 homes; developer selected), El Cerrito
Plaza (743 homes; first building under construction since Nov 2025) and Amador Station at West
Dublin/Pleasanton (300 affordable homes; awaiting funding). Homes total 3,701, an explicit sum of the
official per-site figures (Ashby at its "up to" figure). Walnut Creek's last phase, Fremont, Bay Fair
and Richmond are named in the record but not drawn: no official source places a defined project on a
parcel yet.

Boundary: one part per site from BART's own TOD Work Plan GIS layer (BART's ArcGIS organisation,
added to `src/projects/official.ts`), selected by BART's "in progress" status or by APNs named in City
of Oakland and City of Dublin records. Massing: West Oakland (2020 revised PDP), Lake Merritt (2021 tract
map and zoning table) and El Cerrito Plaza (2024 approved master plan) are traced from the approved plans
with their heights; North Berkeley, Ashby and Amador Station are illustrative height-limit envelopes (80 ft
R-BMU, 90 ft at Amador). Conflicts between official documents (Lake Merritt 557 vs 636 homes, start date,
El Cerrito heights) are in the record's `verify` list. Pipeline: `bam_pipeline.sites.bart_station_housing`
(in `make sites`). The landing camera frames all six stations from El Cerrito to Dublin (centred on the
sites' centroid, as the camera test requires); because the sites are only a few pixels across at that
scale, a site whose centroid falls more than 1 km off it now gets one regional marker per station, and
those markers stay visible (slightly larger) while the program is open. No other project's markers change.

## 2026-10-06 (project photos and official links)

Project photos, approved by Matthew: one openly licensed or public-domain photo for each of 23
projects (18 downloaded so far; Wikimedia rate-limited the other five, which `make photos` fetches), from Wikimedia Commons (`data/photos.json`, research in `docs/images/`). `make photos`
reads each file's license and author from its own Commons page, refuses anything outside CC0,
public domain, CC BY and CC BY-SA, and copies a resized version into `public/photos/`, so the site
never hotlinks. Parkline's approved photo (an abstract atrium detail) was dropped at Matthew's
request. The panel shows each photo after the summary with its caption and credit. Ten
projects have no usable open photo yet. Renderings still need written permission; the outreach
list is `docs/images/PERMISSIONS.md`.

Official links: mission-bay's `sfocii.org/mission-bay` returned 404 and is replaced by the OCII
Mission Bay North and South overview pages. Added the project pages for mission-rock (Port),
india-basin, stonestown and balboa-reservoir (SF Planning) and sonoma-developmental-center
(Permit Sonoma). Each was opened on 2026-10-06.

## 2026-10-06 (the nine new projects on the map)

All nine new projects now have site boundaries and massing or land-use zones, each source added
to `sources` and described in `massingNotes`. Notable calls: Mare Island's boundary uses Vallejo's
2005 specific plan area (the SP-4 zoning area runs over the bay); Schlage Lock's historic office
building is outlined without a height (no official figure); Middlefield Park's O1 height conflict
(125 vs 115 ft) and Berryessa's height diagram source are in `verify`.

## 2026-10-06 (Esmeralda, Cloverdale)

**esmeralda** added at Matthew's request: the Esmeralda Specific Plan in Cloverdale (up to 605
homes and a 160-room hotel on about 261 acres; below the usual 1,000-home bar), from City of
Cloverdale records (`docs/official-research/candidates-esmeralda.md`). `cloverdale.net` and
`cloverdale.granicus.com` join the official hosts. The City Council hearings are Oct 7 and 14, 2026.

## 2026-10-06 (eight new projects)

Added at Matthew's request after official-source research (`docs/official-research/candidates-*.md`,
checked 2026-10-05): **tasman-east**, **sunnydale-hope-sf**, **potrero-hope-sf**,
**middlefield-park**, **schlage-lock**, **berryessa-flea-market**, **mare-island** and
**sonoma-developmental-center** (990 homes, just under the 1,000-home bar). BART station-area
housing (no single site reaches 1,000 homes) and the East Whisman Precise Plan (a zoning plan,
covered by Middlefield Park) were not added. `cityofvallejo.net` and `permitsonoma.org` (Permit
Sonoma) join the official hosts. The records are on file; they go on the map once their boundaries
are drawn.

## 2026-10-05 (Milestone 4: land-use zones for the plan-scale projects)

**moffett-park**, **north-bayshore**, **concord-naval-weapons-station**, **suisun-expansion** and
**brisbane-baylands** get land-use zones (`data/landuse/`), not buildings, per the SPEC; each
plan document is added to `sources` and `massingNotes` says what was drawn. Suisun's zones are
proposed (NOP) and Brisbane's are from the draft 2026 specific plan, both labelled so. Brisbane
also gets the Bayshore Roundhouse landmark (about 25 ft, Council staff report). **north-bayshore**'s
boundary is now traced from the master plan's project-area line (189.3 acres as drawn, with
internal streets and the Shoreline Amphitheatre), replacing the parcel assembly that cut off
about 7 acres of plan residential (Matthew, 2026-10-05).

## 2026-10-05 (Milestone 4, batch 4: The Rise, Alameda Point, Brooklyn Basin, Oakland Coliseum)

`massingNotes` updated and each massing source added to `sources` for **the-rise**,
**alameda-point** and **brooklyn-basin**. **oakland-coliseum** gets no massing: no plan is filed
or approved, and its D-CO-2 zoning (159 ft above mean sea level, Ord. 13302 and 13894) covers the
whole site; both ordinances are now cited. **downtown-west** block E1 is drawn at the approved
Development Agreement's 260 ft (Matthew: the more recent document wins). `apps.cupertino.org`
(the City of Cupertino's document server) added to the official hosts.

## 2026-10-03 (Milestone 4, batch 3: Parkmerced, Parkline, Willow Village, Related Santa Clara, Downtown West)

`massingNotes` updated and each massing source added to `sources` for **parkmerced**,
**parkline**, **willow-village**, **related-santa-clara** and **downtown-west**. Related Santa
Clara now cites CEQA Addendum 4 (Res. 25-9465) for its 190-ft cap. **downtown-west**: the
boundary now includes the two DC(PD) zoning polygons filed as "19039" (62.8 acres as drawn,
was 58.3); its heights come from the October 2020 draft design standards because the approved
2021 version could not be retrieved, so a `verify` item was added.

## 2026-10-03 (Piers 30–32 removed)

**piers-30-32** removed from the map at Matthew's request: the record, its boundary and its
massing are deleted and the project is listed under `_meta.dropped`. 24 projects remain.

## 2026-10-03 (Milestone 4, batch 2: massing for five more San Francisco projects)

`massingNotes` updated and each massing source (design documents, DBI permits for built
buildings) added to `sources` for **candlestick-point**, **hunters-point-shipyard**,
**treasure-island**, **mission-bay** and **piers-30-32**. Hunters Point's notes now give its
two towers (370 and 270 ft), which the 2018 Design for Development allows beyond the 40–120 ft
block limits. Mission Bay's only unbuilt plan blocks are 4 East and 12 West (MOHCD pipeline,
DBI permits); its official page in `sources` (sfocii.org/mission-bay) now returns 404 and is
due for replacement at its next re-check.

## 2026-10-03 (Milestone 4, batch 1: massing for five San Francisco projects)

`massingNotes` updated and each massing source added to `sources` for **balboa-reservoir**,
**mission-rock**, **pier-70**, **stonestown** and **india-basin**. All massing is traced from
adopted design standards or the zoning map and drawn to the height limit, labelled illustrative.
India Basin's Oct 2024 design-standards amendment (draft) changes no heights; the 2018
Figure 5-3 limits stand.

## 2026-10-03 (Milestone 3: official records for every project)

Every project record other than Potrero was rewritten from the official findings in
`docs/official-research/` (checked 2026-10-02): official values in, conflicts settled by the
newest official document, press-only facts and their sources moved to each record's
`reported` object, `unsourced` removed (Mission Bay's figures are now official). Stage changes:
- **india-basin**: distressed → entitled (no official record of the default; private site has no issued permits).
- **parkmerced**: distressed → entitled (no official record of the receivership).
- **balboa-reservoir**: entitled → construction (DBI first construction documents for Buildings E and A).
Notable corrections: Candlestick groundbreaking Sept 9, 2026 (not 10) and office 2.8M sq ft;
Mission Rock Phase 1 finished 2025; Piers 30–32 split July 2025, Seawall Lot 330 application 568
homes; Treasure Island density increase not approved; Willow Village 1,730 homes; Alameda Point
1,300-home cap; Brooklyn Basin 3,700 homes; Concord 12,272 homes; Coliseum sold as one closing.
Each record's `sources` also cites the GIS layer its boundary comes from.

## 2026-10-03 (official records and the Design for Development)

For **potrero-power-station**, from official records read once network access opened:
- `program.affordablePct`: null → **30**, from the recorded development agreement (Recital H).
- `stage`: entitled → **partial**: DBI permit 202212229038 for the Sophie Maxwell Building
  (8 stories, 105 affordable homes) was marked complete Aug 28, 2026 (permit dates count for
  stages, Matthew 2026-10-03).
- `developer`: **California Barrel Company LLC (Fifth Space)**, as named in Addendum 2.
- `timeline`: Board approval corrected to Apr 21, 2020 (Ordinance 62-20, effective May 24,
  not May 25); added Station A, office allocation and phasing actions (2020–2022), the
  Sophie Maxwell permits, UC Regents' Block 2 approval, Addendum 2 and the 2026 amendment
  hearings.
- Massing: block height limits traced from the D4D's Figure 6.2.3 (see docs/DECISIONS.md).
- `verify`: now the Sophie Maxwell opening date, UCSF construction start and the Board's
  final action on the 2026 amendments.

## 2026-10-02 (official sources only)

Matthew asked for official sources only. For **potrero-power-station**:
- Press-only facts moved into a new `reported` record that the map never shows: the
  "partly built" stage and its stage note, the developer name "Fifth Space (formerly Associate Capital)",
  the 30% affordable share, the 2025 and 2026 timeline entries, and the press sources.
- `stage`: partial → **entitled**, the latest status official sources confirm so far.
  It returns to "partly built" once city or UC records confirm the construction and the completed building.
- `stageNote`: rewritten from the minutes (EIR certified and Design for Development
  approved Jan 30, 2020) and the existing sfplanning.org source (agreement effective May 25, 2020).
- `developer`: **California Barrel Company, LLC (Associate Capital)**, the Development
  Agreement party and project sponsor named in the minutes of Jan 30, 2020 and Sept 5, 2019.
- `timeline`: added the Jan 30, 2020 Planning Commission approvals.
- `program.affordablePct`: 30 → null (moved to `reported` until the Development Agreement is read).
- `verify`: added the affordable share, construction status, approved block heights and the
  status of the 2025–26 amendments.
- Massing: the 2018 Draft EIR blocks and the Sophie Maxwell Building are no longer drawn;
  only the 300-ft stack remains.

## 2026-10-02 (official sources)

Matthew asked for official sources only. Checked against the San Francisco Planning
Commission's minutes of January 30, 2020, the hearing that certified the EIR and
approved the Design for Development (Motion 20638), the Special Use District, the
zoning map change and the Development Agreement:
https://sfplanning.s3.amazonaws.com/commissions/cpcpackets/20200130_cal_min.pdf

- **potrero-power-station, program.officeLabSqft:** 1,600,000 → **1,459,978** (gross sq ft
  of "commercial office/laboratory use", minutes items 13 and 14a, p. 9). The 1.6 million
  figure came from press coverage and has no official source.
- **potrero-power-station, program.retailSqft:** null → **99,464** (gross sq ft of
  "commercial-retail use", same items).
- **potrero-power-station, sources:** added the minutes.
- Confirmed by the same minutes, unchanged: 2,601 homes, 250 hotel rooms, 6.9 acres of
  open space, approximately 29 acres. The minutes also give the approved height range
  for new buildings (65 to 240 ft) and the new height district (65/240-PPS on map HT08).

`lastVerified` was not changed: the rest of the record has not been re-checked yet.

## 2026-10-02

- **potrero-power-station, camera:** added (`center` [-122.3838, 37.7566], zoom 16.4,
  pitch 58, bearing -30). A display setting, not a fact; tuned from screenshots.
- **potrero-power-station, traced geometry:** new `data/boundaries/potrero-power-station.geojson`
  (site and five sub-areas, Draft EIR Fig. 2-2, p. 2-6) and
  `data/massing/potrero-power-station.geojson` (illustrative height districts, Fig. 2-7,
  p. 2-20; stack 300 ft, pp. 2-7 and 4.D-8). Source:
  https://sfplanning.s3.amazonaws.com/sfmea/2017-011878ENV_DEIR_Volume_1.pdf
- **schema:** projects may carry an optional `camera`.

`lastVerified` was not changed: no project facts were re-checked.

## 2026-10-01

Approved by Matthew after the planning audit (`docs/PLANNING-AUDIT.md`).

- **potrero-power-station, summary and massingNotes:** "brick stack" changed to
  "concrete boiler stack". Source: Potrero Power Station Mixed-Use Development Project
  Draft EIR, Oct 2018, p. 2-7 ("the adjacent 300-foot tall concrete boiler exhaust
  stack") and p. 4.D-8 ("The reinforced concrete Boiler Stack ... at 300 feet in
  height"). The brick structure on the site is Station A's Turbine Hall (p. 4.D-7).
  https://sfplanning.s3.amazonaws.com/sfmea/2017-011878ENV_DEIR_Volume_1.pdf
- **potrero-power-station, acresNote:** the 29 vs 21 acre question is answered by the
  same Draft EIR, p. S-2: an approximately 29.0-acre site including a 21-acre Power
  Station sub-area. `acres` stays 29. The Draft EIR was added to `sources`. The
  "Final site acreage" verify item stays, because the 2026 amendments could change it.
- **mission-bay:** `acres` (303), `program.homes` (6,500), `developer` and the 1998
  timeline entry are moved into a new `unsourced` object, so the map never shows
  them. The research notes said these were approximate figures from general knowledge.
  They come back once each one has a citable source.

`lastVerified` was not changed. Only the facts listed above were re-checked.
