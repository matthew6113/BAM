# Image candidates: east-north-bay group

Research only. Nothing was downloaded into the repo and no one was contacted. Checked 2026-10-06.

Projects: concord-naval-weapons-station, brooklyn-basin, suisun-expansion,
sonoma-developmental-center, esmeralda.

How this was checked: each Wikimedia Commons file was read through the Commons API
(`imageinfo` + `extmetadata`, which returns the license template, author, credit and date on the
file page). Flickr photos were read on their own Flickr page and through Flickr's oEmbed record,
which carries the current license. Openverse was used only to find leads; every license below was
then confirmed on the image's own page. Camera locations were tested against the traced boundaries
in `data/boundaries/<id>.geojson` (point-in-polygon), and the key images were viewed at thumbnail
size to confirm what they show. NC, ND and "all rights reserved" images are not listed as usable.

Credit lines follow the TASL pattern (title, author, source, license). For CC BY and CC BY-SA, the
credit must name the author, link the license and say whether the image was changed. CC BY-SA
also requires that any edited version, such as a crop, be shared under the same license.

"Current" means the photo matches conditions on the ground today as far as we can tell. "Old"
means the site has changed since, or the photo predates the project's current state.

About the NAIP aerials listed under (2): these are USDA National Agriculture Imagery Program
quarter-quad orthophotos (flown 2022, published 2023), uploaded to Commons as large GeoTIFFs
(about 10,000 x 12,000 px, 100+ MB each). They are US federal works and public domain; Commons
asks for a courtesy credit. Each needs cropping to the site before use. Commons has 2016, 2018,
2020 and 2022 versions of each tile; 2022 is the newest there.

Official-host note: three of the better official pages below are on hosts that are not yet in
`src/projects/official.ts` (`oaklandca.gov`, `oakha.org`, `suisun.com`). They are public agencies,
but they would need adding to that list before they can appear in `officialLinks`.

---

## concord-naval-weapons-station (Concord Reuse Project, Inland Area)

The project is the former Inland Area. Images of the Tidal Area, Port Chicago and Military Ocean
Terminal Concord (still Army-run) are not this project and are left out, including the public-domain
USACE photo `File:Public_meeting_for_Military_Ocean_Terminal_Concord_(8693882958).jpg`.

### 1. Openly licensed photos

1. **Concord Naval Weapons Station, aerial, 2015** (best)
   - Page: https://commons.wikimedia.org/wiki/File:Concord_Naval_Weapons_Station_20150201.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/f/f2/Concord_Naval_Weapons_Station_20150201.jpg (6000 x 4000)
   - Credit: "Wing, CC BY-SA 4.0, via Wikimedia Commons" (own work; also on Flickr as
     https://www.flickr.com/photos/98862796@N00/16783611619 by "陈霆, Ting Chen, Wing", CC BY-SA 2.0)
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 1 February 2015, from a UA903 flight
   - Shows: an oblique aerial of the Inland Area's grid of ammunition bunkers against the
     edge of Concord's neighborhoods, with the hills beyond. The geotag (37.9942, -121.9828) sits
     just outside the traced boundary, but the view is of the site. **Probably still
     representative** (the site is largely undeveloped), but it's 11 years old and from before
     the 2024 Brookfield selection. It is hazy, low-contrast winter light.
2. **CA Concord Naval Weapons Station aerial, 2006**
   - Page: https://commons.wikimedia.org/wiki/File:CA_Concord_Naval_Weapons_Station_aerial_USA.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/5/58/CA_Concord_Naval_Weapons_Station_aerial_USA.jpg (2272 x 1704)
   - Credit: "Daniel Schwen, CC BY-SA 2.5, via Wikimedia Commons" (own work)
   - License: CC BY-SA 2.5, https://creativecommons.org/licenses/by-sa/2.5
   - Taken: 25 August 2006
   - Shows: a sharp, close aerial of the bunker grid, Mt. Diablo Creek and the edge of the
     neighborhood, in summer light. The camera point is inside the traced boundary. A clearer
     picture than (1), but **old** (2006, before the base closed in 2007).
3. **C75 interlocking, Concord Naval Weapons Station track, and cows, January 2019**
   - Page: https://commons.wikimedia.org/wiki/File:C75_interlocking,_Concord_Naval_Weapons_Station_track,_and_cows,_January_2019.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/6/6f/C75_interlocking%2C_Concord_Naval_Weapons_Station_track%2C_and_cows%2C_January_2019.JPG
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons" (own work)
   - License: CC BY-SA 3.0, https://creativecommons.org/licenses/by-sa/3.0
   - Taken: 20 January 2019
   - Shows: the BART tracks north of North Concord station with a grazed hillside of the former
     station and its munitions rail line behind. The camera is just outside the boundary, looking
     onto the site. A ground-level view of the land by the BART station; **current enough**.
   - The same photographer's `File:North_Concord_Martinez_station_from_Panoramic_Drive,_May_2018.jpg`
     (CC BY-SA 3.0) shows the station the plan centers on, but not the site itself.

### 2. Public-domain government images

- **USDA NAIP aerial, 2022, quarter-quad 3712101 NW**
  - Page: https://commons.wikimedia.org/wiki/File:M_3712101_nw_10_060_20220519.tif
  - Original: https://upload.wikimedia.org/wikipedia/commons/3/3b/M_3712101_nw_10_060_20220519.tif
  - Credit (courtesy): "USDA-FSA Aerial Photography Field Office, NAIP 2022, via NOAA Office for Coastal Management"
  - Why it's public domain: a US federal government work (USDA). Commons tags it public domain.
  - Shows: an orthophoto covering roughly 37.94–38.00 N, 122.00–121.94 W, which takes in most of
    the Inland Area. The western strip (west of 122.00 W) is on tile 3712208 NE, and the
    northernmost edge is on 3812157 SW. **Current** as of May 2022.
- No Navy, NAVFAC, HABS/HAER, Library of Congress or National Archives photo of the Inland Area
  was found on Commons or in the LOC catalog. The Navy's BRAC program site (linked from
  concordreuseproject.org) is a lead for PD Navy photos, but no specific image was found there.

### 3. Press/media kits with stated permission

None found. Brookfield's project site (concordbpproject.com) has event photos but no press kit
or use terms.

### 4. Permission leads

- **Conceptual Land Use Plan, March 2024** (Brookfield's plan diagram, hosted by the city)
  - Page: https://www.concordreuseproject.org/196/Master-Developer-2024---Year-One (document
    "Conceptual Land Use Plan - March 2024", DocumentCenter 2348), plus the Q2 and Q3/Q4 2024
    Brookfield project updates (2349, 2350)
  - Owner: BCUS Acquisitions LLC (Brookfield) as master developer. No credit is printed on the page.
  - Contact: Brookfield project team, engage.concord@brookfieldrp.com, 925-430-7378
    (from https://concordbpproject.com/). City: Concord Community Reuse Project, (925) 671-3001.
    Staff emails listed on older pages (guy.bjerke@cityofconcord.org on the 2021 selection page;
    meredith.rupp@cityofconcord.org on the Specific Plan page, last updated 2021) may be out of date.
- Brookfield's site (https://concordbpproject.com/) is run jointly by the City and Brookfield.
  Same contact as above.

### 5. Official render pages to link

- https://www.concordreuseproject.org/196/Master-Developer-2024---Year-One (the current
  conceptual land use plan and Brookfield updates). **Better than the record's current links**
  for a "see the plans" link.
- https://www.concordreuseproject.org/152/The-Area-Plan (adopted Area Plan diagram; already in
  `sources`).
- The record's `officialLinks` (homepage and /148 overview) are fine as general links, but /148
  mostly shows the Area Plan and the tidal/inland map. The 2021 selection page (/187) names the
  former master developer (Concord First Partners), so it's superseded and shouldn't be used as a
  render link.

---

## brooklyn-basin (Oak to Ninth, Oakland)

No openly licensed photo was found that shows the new buildings or Township Commons. Commons has
no geotagged photo inside the traced boundary that shows the site (the only hits are unrelated
portraits and a pill photo). This is the weakest project in the group for images.

### 1. Openly licensed photos

1. **Brooklyn Basin, Oakland, California (marina series), July 2016** (weak; best of what exists)
   - Pages (all by the same owner, all CC BY 2.0, all titled "Brooklyn Basin, Oakland, California"):
     - https://www.flickr.com/photos/41980486@N07/27850922384 (marina dock and boats, daylight)
     - https://www.flickr.com/photos/41980486@N07/28388958001 (marina at golden hour)
     - https://www.flickr.com/photos/41980486@N07/28359886372 (wooden boat, through a window screen)
     - https://www.flickr.com/photos/41980486@N07/28435126616 and /28388799931 (night shots)
   - Larger image (Flickr "b" size, from oEmbed), e.g. https://live.staticflickr.com/8408/27850922384_31fae323b7_b.jpg
     (the original size has to be taken from the Flickr download menu)
   - Credit: "Brooklyn Basin, Oakland, California" by Sharon Hahn Darlin, CC BY 2.0, via Flickr
   - License: CC BY 2.0, https://creativecommons.org/licenses/by/2.0/
   - Taken: 21 July 2016 (date read on the Flickr page for 28435126616)
   - Shows: estuary marina scenes with a heavy tilt-shift/blur filter. No geotag; the exact spot
     isn't verified (it may be Embarcadero Cove, east of the traced boundary). **Old**: before the
     first buildings opened in 2020. Not recommended for the panel.
   - Also in the series: "Brotzeit Lokal, Brooklyn Basin" (https://www.flickr.com/photos/41980486@N07/28184544100,
     CC BY 2.0), a restaurant that is likely outside the project boundary.
- Left out: `File:Lightship_Relief_(Oakland,_CA).JPG` (CC BY-SA 3.0) says "Brooklyn Basin" but
  was taken at Jack London Square, outside the project.

### 2. Public-domain government images

- **USDA NAIP aerial, 2022, quarter-quad 3712214 SE** (best usable image for this project)
  - Page: https://commons.wikimedia.org/wiki/File:M_3712214_se_10_060_20220518.tif
  - Original: https://upload.wikimedia.org/wikipedia/commons/8/87/M_3712214_se_10_060_20220518.tif
  - Credit (courtesy): "USDA-FSA Aerial Photography Field Office, NAIP 2022, via NOAA Office for Coastal Management"
  - Why it's public domain: a US federal government work (USDA).
  - Shows: an orthophoto covering roughly 37.75–37.81 N, 122.31–122.25 W, which takes in the
    whole traced site. **Current** as of May 2022, mid-build-out.
- **Coast Guard Island, May 2009** (background only)
  - Page: https://commons.wikimedia.org/wiki/File:Coast_Guard_Island_May_2009.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/5/52/Coast_Guard_Island_May_2009.jpg
  - Credit: "U.S. Coast Guard photo by Petty Officer 3rd Class Erik Swanson" (photo ID 090514-G-5394S-055)
  - Why it's public domain: a US federal government work (US Coast Guard).
  - Shows: Coast Guard Island in the foreground, with the Oakland shore and a marina at the top
    edge. **Old** (2009, before construction), and the project is only at the edge of the frame.
    Historical context at most.

### 3. Press/media kits with stated permission

None found. brooklynbasin.com returns an empty page. Signature Development's site says
"All rights reserved".

### 4. Permission leads

- **Developer renderings and photos**: https://www.signaturedevelopment.com/development/brooklyn-basin/
  - Owner: Signature Development Group (with Zarsion America, as Zarsion-OHP I, LLC). No architect
    credit on the page. "©2014-2026 Signature Development Group. All rights reserved."
  - Contact: info@signaturedevelopment.com (on https://www.signaturedevelopment.com/contact/),
    510-251-9270 (phone from a search snippet, not checked on the page).
- **Kite aerial photo of Township Commons** (photo, not a rendering):
  https://www.flickr.com/photos/ml_kap/51079669172 by Michael Layefsky. "All Rights Reserved"
  (confirmed through Flickr oEmbed), so not usable without permission. Ask through Flickr mail.
- **Oakland Housing Authority page** (aerial and street photos of the affordable parcels, no
  credits or terms): https://www.oakha.org/about/assetmanagement/portfolio/brooklynbasin/. OHA
  main line (510) 874-1500; no media contact is listed.

### 5. Official render pages to link

- https://www.oaklandca.gov/Planning-Building/Major-Development-Projects/Brooklyn-Basin-Mixed-Use-Development
  (City of Oakland's project page, with CEQA and approval documents). **Better than the record's
  Legistar link** for a general link, but `oaklandca.gov` isn't yet in `official.ts`. (Note: the
  record's `sources` already use `oaklandca.gov` PDFs, which returned 403 to an automated download
  here, so it may be bot-blocking rather than missing.)
- The record's `officialLinks` Legistar item (ID 34148) works as an approval-record link. The
  Parcel H Planning Commission staff report (in `sources`) is the most likely official document
  with current building drawings. Couldn't open it here (403), so not checked.

---

## suisun-expansion (California Forever, Suisun City annexation)

### 1. Openly licensed photos

1. **Wind turbines, September 2023** (best openly licensed photo, with caveats)
   - Page: https://commons.wikimedia.org/wiki/File:Wind_turbines_-_September_2023_-_Sarah_Stierch.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/9/9c/Wind_turbines_-_September_2023_-_Sarah_Stierch.jpg
   - Credit: "Missvain (Sarah Stierch), CC BY 4.0, via Wikimedia Commons" (own work; author field is "Missvain")
   - License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0
   - Taken: 7 September 2023
   - Shows: dry grassland with wind turbines near Birds Landing. The camera point (38.1836,
     -121.8108) falls inside the traced boundary, on its southern edge along Hwy 12. The turbines
     are likely the Montezuma Hills wind farms, which may be outside the annexation area. Shows the
     landscape type (dry farmland) honestly; **current**. Label as "near the site" unless the
     view direction is confirmed.
2. **CA-12 W in Birds Landing, September 2023**
   - Page: https://commons.wikimedia.org/wiki/File:CA-12_W_in_Birds_Landing_-_September_2023_-_Sarah_Stierch.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/2/2e/CA-12_W_in_Birds_Landing_-_September_2023_-_Sarah_Stierch.jpg
   - Credit: "Missvain (Sarah Stierch), CC BY 4.0, via Wikimedia Commons"
   - License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0
   - Taken: 7 September 2023
   - Shows: a Hwy 12 route sign in front of plowed and dry fields. The camera point is inside the
     traced boundary on its southern edge. **Current**, but the subject is mostly the sign.
     (The file description says "Sonoma, California", which is a mistake; Birds Landing is in Solano County.)

### 2. Public-domain government images

- **USDA NAIP aerials, 2022, quarter-quads 3812150 NW and NE**
  - Pages: https://commons.wikimedia.org/wiki/File:M_3812150_nw_10_060_20220518.tif and
    https://commons.wikimedia.org/wiki/File:M_3812150_ne_10_060_20220518.tif
  - Originals: https://upload.wikimedia.org/wikipedia/commons/5/5a/M_3812150_nw_10_060_20220518.tif and
    https://upload.wikimedia.org/wikipedia/commons/4/48/M_3812150_ne_10_060_20220518.tif
  - Credit (courtesy): "USDA-FSA Aerial Photography Field Office, NAIP 2022, via NOAA Office for Coastal Management"
  - Why it's public domain: a US federal government work (USDA).
  - Shows: farmland orthophotos centered inside the traced boundary (tile centers at 38.219 N,
    121.844 W and 121.781 W). The site spans many tiles; these two are central. **Current** as of May 2022.
- **A wind farm off California Rt. 12 near Rio Vista**, Carol M. Highsmith, 22 Dec 2012
  - Page: https://commons.wikimedia.org/wiki/File:A_wind_farm_off_California_Rt._12_near_Rio_Vista_in_Solano_County,_California_LCCN2013631240.tif
    (also LCCN2013631238 and LCCN2013631239)
  - Original: https://upload.wikimedia.org/wikipedia/commons/b/b5/A_wind_farm_off_California_Rt._12_near_Rio_Vista_in_Solano_County%2C_California_LCCN2013631240.tif
  - Credit (requested by LOC): "The Jon B. Lovelace Collection of California Photographs in Carol M. Highsmith's America Project, Library of Congress, Prints and Photographs Division"
  - Why it's public domain: Highsmith dedicated this archive to the public through the Library of
    Congress. It isn't a federal work, but Commons and LOC both mark it public domain with no known
    restrictions (catalog: http://lccn.loc.gov/2013631240).
  - Shows: wind turbines off Hwy 12. Camera points sit inside the boundary on its southern edge,
    but like the photo in (1), the turbines may be outside it. **Old-ish** (2012); the landscape is
    largely unchanged.

### 3. Press/media kits with stated permission

None with stated permission. California Forever has a press kit with renderings
(https://californiaforever.com/press-kit/renderings/) but the page states no use terms, and the
site's Terms (https://californiaforever.com/terms-conditions/) say "Except as expressly authorized
by California Forever, you may not make use of the Materials." So it goes under (4).

### 4. Permission leads

- **California Forever press kit renderings**: https://californiaforever.com/press-kit/renderings/
  (titles include "Specific plan aerial", "Neighborhood aerial", "Residential street", "Market
  plaza", "Greenbelt around city", "Foundry aerial"; also maps and diagrams at
  https://californiaforever.com/press-kit/maps/).
  - Owner: California Forever LP (no architect credit shown).
  - Contact: press@californiaforever.com (stated on the press kit page).
- **City outreach site**: https://suisunexpansion.com/ (© City of Suisun City; contact
  suisun@tripepismith.com, the City's outreach consultant). It links the applicant's Specific Plan
  PDF on suisun.com.

### 5. Official render pages to link

- https://www.suisun.com/Departments/Development-Services/Suisun-Expansion-Project-Application-and-Documents
  (City of Suisun City: application, Specific Plan and NOP). Found through search. It blocks
  automated requests (403), so not opened here. `suisun.com` isn't yet in `official.ts`.
- https://suisunexpansion.com/vision-and-background/overview/ (City-run; host already in
  `official.ts`). The record's `officialLinks` (suisunexpansion.com homepage and the CEQAnet NOP)
  are fine.

---

## sonoma-developmental-center (SDC, Eldridge)

This project has the best openly licensed coverage in the group.

### 1. Openly licensed photos

1. **View of the main SDC campus, December 2022** (best)
   - Commons page: https://commons.wikimedia.org/wiki/File:Sonoma_Developmental_Center_-_Demember_2022_-_Sarah_Stierch_01.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/0/09/Sonoma_Developmental_Center_-_Demember_2022_-_Sarah_Stierch_01.jpg (4032 x 3024)
   - Credit: "Missvain (Sarah Stierch), CC BY 4.0, via Wikimedia Commons"
   - License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0
   - The same photo is on Flickr as "View of the main SDC campus" by Sarah Stierch,
     https://www.flickr.com/photos/sarahvain/52571611820/, now marked **CC0 1.0**
     (https://creativecommons.org/publicdomain/zero/1.0/; checked on the Flickr page and in oEmbed;
     Openverse still lists it as CC BY 2.0). Either source works; crediting the CC BY 4.0 Commons
     copy is the cautious option.
   - Taken: 16 December 2022
   - Shows: the campus buildings among trees in the valley, seen from a hillside to the west, with
     the Mayacamas ridge behind. **Current** (closed campus, unchanged since).
2. **SDC grounds from the Main Building porch, April 2018**
   - Page: https://commons.wikimedia.org/wiki/File:Sonoma_County_-_Sonoma_Developmental_Center_-_20180424152358.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/4/4e/Sonoma_County_-_Sonoma_Developmental_Center_-_20180424152358.jpg
   - Credit: "JessaDMay, CC BY-SA 4.0, via Wikimedia Commons" (own work)
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 24 April 2018
   - Shows: the oval lawn with flagpole and flowering trees in front of the Main Building, hills
     behind. Probably part of the historic core around the Central Green (not confirmed against the
     plan's figures). Taken while the center was still open (it closed in late 2018); the landscape
     and buildings are **largely current**, but the parked cars and upkeep reflect an operating campus.
3. **SDC Main Building, April 2018** (the historic structure the plan keeps)
   - Page: https://commons.wikimedia.org/wiki/File:Sonoma_County_-_Sonoma_Developmental_Center_-_20180424153731.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/5/5e/Sonoma_County_-_Sonoma_Developmental_Center_-_20180424153731.jpg
   - Credit: "JessaDMay, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 24 April 2018
   - Shows: the red-brick 1908 Main Building (National Register listed) behind trees. **Current**
     for the building.
- Also usable:
  - `File:Sonoma_State_Home,_Main_Building,_15000_Arnold_Dr.,_Eldridge,_CA_6-12-2010_6-03-39_PM.JPG`
    (Sanfranman59, CC BY-SA 3.0, 12 June 2010, Main Building facade; old but the building is unchanged).
  - `File:Sonoma_County_-_Sonoma_Developmental_Center_-_20180424153940.jpg` (JessaDMay, CC BY-SA 4.0):
    the Main Building's plaque (1908, Sellon & Hemmings, NRHP 2001). Useful for facts, not as a hero image.
  - `File:Sonoma_Developmental_Center_-_Demember_2022_-_Sarah_Stierch_02.jpg`, `_03` (cemetery,
    memorial) and `_04` (Fern Lake). All CC BY 4.0, Dec 2022, but they show the cemetery and
    open space, not the plan's development core.
  - **Drone video**: https://commons.wikimedia.org/wiki/File:SDC_-_Sonoma_Developmental_Center_-_Glen_Ellen_-_Eldridge_-_4K_Drone_Footage.webm
    (Evan Hess, CC BY 3.0, 24 Oct 2022, 3840 x 2160). Still frames could be taken as derivatives
    (credit "Evan Hess, CC BY 3.0", note the change). Probably the best aerial of the campus; **current**.

### 2. Public-domain government images

- **USDA NAIP aerial, 2022, quarter-quad 3812244 NE**
  - Page: https://commons.wikimedia.org/wiki/File:M_3812244_ne_10_060_20220524.tif
  - Original: https://upload.wikimedia.org/wikipedia/commons/9/9b/M_3812244_ne_10_060_20220524.tif
  - Credit (courtesy): "USDA-FSA Aerial Photography Field Office, NAIP 2022, via NOAA Office for Coastal Management"
  - Why it's public domain: a US federal government work (USDA).
  - Shows: an orthophoto covering roughly 38.31–38.38 N, 122.56–122.50 W, which takes in the
    whole traced campus. **Current** as of May 2022.
- **Historic, public domain by age (not government-PD)**:
  - `File:Home_for_Feeble-minded_Children,_Eldridge,_Sonoma_County.jpg`, from the 1907 California
    Blue Book (State of California). Public domain because it was published before 1931, not
    because it's a state work. https://commons.wikimedia.org/wiki/File:Home_for_Feeble-minded_Children,_Eldridge,_Sonoma_County.jpg
  - `File:Sonoma_state_home.jpg` (1913 postcard) and `File:Sonoma_state_home1.jpg` (about 1910
    postcard), unknown author, public domain on Commons (pre-1931). Low resolution. **Old**, for
    history only. The title wording of the first one is historical and would need care in the UI.

### 3. Press/media kits with stated permission

None found. The applicant has no public website (eldridgerenewal.com didn't resolve).

### 4. Permission leads

- **Applicant's architectural plans, elevations, design guidelines and site photos**: Eldridge
  Renewal's application package (PLP24-0005), linked from https://permitsonoma.org/sdchousingproject.
  The Feb 4, 2025 cover letter lists files such as `SDC_128_07_0_PrelimArchitecturalPlansElevations`,
  `SDC_128_07_1_DesignGuidelines` and `SDC_128_13_Photographs`. The share folder is at
  https://share.sonoma-county.org/link/7NXJIdFZm-A/.
  - Owner: Eldridge Renewal, LLC (letters signed by Rob Toste). No architect credit found in the letter.
  - Contact: no public applicant email found. Go through Permit Sonoma, SDC@sonomacounty.gov
    (project page), or Planner@sonomacounty.gov, (707) 565-1900 option 5.
- Visual simulations in the County's 2025 review: Permit Sonoma lists "3C_Visual Character and
  Public Views" and "3B_Proposed Site Plan and Development Program" on the same page. These are
  County documents and need permission too (California county works aren't automatically PD).

### 5. Official render pages to link

- https://permitsonoma.org/sdchousingproject (Permit Sonoma page for the Eldridge Renewal
  application, with the site plan, development program and visual-character documents). **Better
  than the record's current CEQAnet links** for a "see the plans" link; host already in `official.ts`.
- https://permitsonoma.org/sdcplan (the County's Specific Plan page). The record's CEQAnet NOP
  links are fine as sources. The 2022 adopted-plan pages on permitsonoma.org are superseded by
  the 2024 court ruling and shouldn't be used as render links.

---

## esmeralda (Cloverdale)

### 1. Openly licensed photos

None found. No Commons file is geotagged inside the traced boundary. The nearest are
Pi.1415926535's July 2022 photos of Cloverdale SMART station (CC BY-SA 4.0, e.g.
`File:Cloverdale_station_from_the_southeast,_July_2022.JPG`), which is north of the site and
not part of it. Openverse and Flickr searches for Cloverdale, the Russian River at Cloverdale and the
Alexander Valley Resort site turned up nothing of the site. Left out:
`File:Redwood_Empire_Sawmill_-_February_2023-_Sarah_Stierch.jpg` (CC BY 4.0), an active mill
elsewhere in Cloverdale, not the former mill site.

### 2. Public-domain government images

- **USDA NAIP aerials, 2022, quarter-quads 3812316 SE and 3812209 SW** (best usable image; the site straddles both)
  - Pages: https://commons.wikimedia.org/wiki/File:M_3812316_se_10_060_20220520.tif (west part,
    west of 123.0 W) and https://commons.wikimedia.org/wiki/File:M_3812209_sw_10_060_20220520.tif
    (east part, toward the river)
  - Originals: https://upload.wikimedia.org/wikipedia/commons/3/3d/M_3812316_se_10_060_20220520.tif and
    https://upload.wikimedia.org/wikipedia/commons/c/cf/M_3812209_sw_10_060_20220520.tif
  - Credit (courtesy): "USDA-FSA Aerial Photography Field Office, NAIP 2022, via NOAA Office for Coastal Management"
  - Why it's public domain: a US federal government work (USDA).
  - Shows: orthophotos of the Russian River valley at Cloverdale's southern edge (viewed: Hwy 101,
    the rail line and the river along the west edge of 3812209 SW). The two tiles need joining and
    cropping to the site. **Current** as of May 2022.

### 3. Press/media kits with stated permission

None found. esmeralda.org has no press page (/press returns 404).

### 4. Permission leads

- **Renderings in the Draft Specific Plan** (Version 7, Sept 25, 2026):
  https://www.cloverdale.net/DocumentCenter/View/7035/Draft-Specific-Plan---Revised-92926.
  Figure 1-1 "Illustrative Neighborhood Aerial", Figure 1-2 "Illustrative Site Plan", Figure 1-3
  "Rendering of Promenade", Figure 1-4 "Rendering of Esmeralda Piazza". There are also historic
  aerials (Figure 1-9) and photos of the Russian River from the site (Figure 3-4).
  - Owner: not credited in the document. Presumably the applicant, Esmeralda Land Company, LP; the
    plan credits only its community-engagement photos ("Credit: Esmeralda Land Company") and an
    archival source for Figure 1-8.
  - Contact: team@esmeralda.org (stated on https://esmeralda.org/support). Applicant site:
    https://esmeralda.org/ (the city's page sends project questions there).
- **Visual impact simulations**: the City's Esmeralda page links "Visual Impact Simulation"
  appendices to the EIR Addendum. The authors weren't checked here. Ask the City (City Hall, 707-894-2521)
  or the applicant about who owns them.

### 5. Official render pages to link

- https://www.cloverdale.net/esmeralda (City of Cloverdale project page: Specific Plan, EIR
  Addendum with visual simulations, hearing schedule). Already the record's first `officialLinks`
  entry; good as is.
- https://www.cloverdale.net/DocumentCenter/View/7035/Draft-Specific-Plan---Revised-92926 (the
  revised Draft Specific Plan with the renderings above; already in `officialLinks`). Note that it's
  a 36 MB PDF.
