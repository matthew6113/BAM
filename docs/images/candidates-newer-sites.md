# Image candidates: newer-sites group

This is research only. Nothing was downloaded into the repo and no one was contacted. Checked 2026-10-12.

Projects: ucsf-parnassus, tanforan, northgate-san-rafael, ravenswood-business-district,
bart-station-housing (West Oakland, Lake Merritt, North Berkeley, Ashby, El Cerrito Plaza and Amador),
oceanwide-center, 30-van-ness, west-midway-reshap, alameda-point-plan, encinal-terminals, alameda-marina.

How licenses were checked:
- Wikimedia Commons: for each file I read the license, author, date and coordinates on the file's
  own page, through the Commons API (extmetadata, plus wikitext for the public-domain tags).
- Flickr: for each photo I read the license, owner, date taken and geotag from the photo's own record
  (`flickr.photos.getInfo`).
- I opened a small preview of each listed image to confirm what it shows.
- NC, ND and "all rights reserved" images were left out.

How locations were checked: where an image has a geotag, I tested it against the project polygon in
`data/boundaries/<id>.geojson`. For BART, I tested it against the station's own sub-polygon. Each entry
gives the result as "inside" or "outside by about N m". A geotag marks where the camera stood, not what
it shows, so aerials and long views are often "outside" even when the site is in frame.

How credit lines work: they follow the TASL pattern (title, author, source, license), as in the
other candidates files. CC BY and CC BY-SA images need the author, a license link and a note of any
changes. CC BY-SA edits, such as crops, must be shared under the same license. CC0, PDM and US
government images need no credit, but giving one is good practice. Original URLs are listed for
reference only. Don't hotlink them; copy the file into the build if it's used.

"Current" means the photo matches conditions on the ground today as far as we can tell. "Old" means
the site has changed since it was taken, or the photo predates the project's present stage.

Coverage gaps and limits:
- **Wikimedia rate limiting:** Commons returned HTTP 429 many times. I spaced calls at least 2.5 s apart
  and honoured Retry-After (often 20–55 s). Every license listed here was read in the end. English
  Wikipedia's API refused requests outright ("too many requests"), so I couldn't check which images
  the Wikipedia articles use.
- **Searches run:** Commons was searched by geosearch around each site, by keyword and by category.
  Openverse (its anonymous API now works) and Flickr were also searched, using bounding-box searches
  over each site and keyword searches. Flickr was limited to CC BY, CC BY-SA, CC0 and PDM.
- **Missing coverage:**
  - No openly licensed photo of the Helen Diller hospital under construction (since 2024) was found.
  - No photo was found at Oceanwide, West Midway or Encinal Terminals.
  - No current photo was found at Alameda Marina.
- **City of Alameda pages:** they return 403 to plain curl but opened in a browser-style fetch.

---

## ucsf-parnassus (UCSF Parnassus Heights)

### 1. Openly licensed photos

1. **University of California San Francisco - Parnassus campus, September 2021** (best)
   - Page: https://commons.wikimedia.org/wiki/File:University_of_California_San_Francisco_-_Parnassus_campus.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/b/bc/University_of_California_San_Francisco_-_Parnassus_campus.jpg
   - Credit: "Alfred Twu, CC0, via Wikimedia Commons" (no credit required)
   - License: CC0 1.0, http://creativecommons.org/publicdomain/zero/1.0/deed.en
   - Taken: 21 September 2021
   - Location: the camera stood in Golden Gate Park, outside the boundary; the subject is the campus.
   - Shows: the Parnassus campus towers below Mount Sutro and Sutro Tower, with Golden Gate Park and
     the Academy of Sciences' green roof in front. A good context shot.
   - **Old for the hospital:** it's from before the 2024 groundbreaking, so it shows no new hospital
     construction.
2. **UCSF Parnassus from 15th Avenue Steps, October 2018**
   - Page: https://commons.wikimedia.org/wiki/File:UCSF_Parnassus_from_15th_Avenue_Steps,_October_2018.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/7/7b/UCSF_Parnassus_from_15th_Avenue_Steps%2C_October_2018.JPG
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL), https://creativecommons.org/licenses/by-sa/3.0
   - Taken: 7 October 2018
   - Location: the camera was about 1.2 km west, on the 15th Avenue Steps, outside the boundary.
   - Shows: a telephoto view of the hospital towers and Mount Sutro forest, with a tower crane. A sharp
     view of the campus. **Old** (before the CPHP).
3. **UCSF Medical Center and Sutro Tower in 2008**
   - Page: https://commons.wikimedia.org/wiki/File:UCSF_Medical_Center_and_Sutro_Tower_in_2008.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/7/73/UCSF_Medical_Center_and_Sutro_Tower_in_2008.jpg
   - Credit: "Hourann Bosci, CC BY-SA 2.0, via Wikimedia Commons"
   - License: CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0
   - Taken: 10 August 2008
   - Shows: the campus from the Academy of Sciences roof. **Old.**

Also on Commons:
- "Grandview Park from UCSF Parnassus, March 2019" is CC BY-SA 3.0. Its geotag is inside the boundary,
  but it looks away from the campus, so it isn't useful.
- Sarah Stierch's August 2022 Parnassus photos (CC BY 4.0) are interiors and elevator buttons, so
  they're weak.

### 2. Public-domain government images

None found. UC is a state body, and its photos aren't public domain by default.

### 3. Press/media kits with stated permission

None found. No UCSF press kit with stated terms turned up.

### 4. Permission leads

- **UCSF (UC Regents), owner and builder**
  - Release with the hospital renderings: "UCSF Releases the Latest Designs for New Hospital at
    Parnassus Heights" (December 2021),
    https://www.ucsf.edu/news/2021/12/422011/ucsf-releases-latest-designs-new-hospital-parnassus-heights
    (it returned 403 to a direct fetch).
  - Press coverage of the April 2024 groundbreaking release credits its rendering "© Herzog & de
    Meuron", so the architect holds those rights.
  - Design team as reported: Herzog & de Meuron (design architect), HDR (architect of record).
  - Ask UCSF's Office of Communications through its newsroom, https://www.ucsf.edu/news. No press
    email was confirmed.
- **Herzog & de Meuron**, credited for the hospital renderings: ask through the firm's own site. No
  contact was confirmed.

### 5. Official render pages to link

- https://regents.universityofcalifornia.edu/regmeet/jan21/f5.pdf (in officialLinks): the Regents
  item for the CPHP and the hospital.
- https://ceqanet.lci.ca.gov/2020010175 (in sources): the CPHP EIR record, with the design
  graphics in its attachments.
- Note: ucsf.edu isn't on the official-host list in `src/projects/official.ts`, so the UCSF release
  can't be an official link unless Matthew adds the host.

---

## tanforan (Tanforan redevelopment)

### 1. Openly licensed photos

1. **Parking lot and sears store, January 2018** (best exterior)
   - Page: https://commons.wikimedia.org/wiki/File:Parking_lot_and_sears_store.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/4/4b/Parking_lot_and_sears_store.jpg
   - Credit: "FuriousYogi, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 6 January 2018
   - Location: no geotag. The file's category is "The Shops at Tanforan".
   - Shows: the mall's big surface parking lot and the Sears anchor on an overcast day. It shows the
     scale of the parking and anchor buildings that the plan replaces. **Old-ish:** Sears has since
     closed, so check the current conditions.
2. **Tanforan overview, February 2023**
   - Page: https://www.flickr.com/photos/mliu92/52805521605/
   - Original: https://live.staticflickr.com/65535/52805521605_390732621e_o.jpg
   - Credit: "Tanforan overview" by mliu92, CC BY-SA 2.0, via Flickr
   - License: CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0/
   - Taken: 5 February 2023
   - Location: geotag 37.637219, -122.417539, inside the boundary.
   - Shows: the food court atrium inside the mall, from the upper level. Fairly current, but it's
     an interior.
3. **Tanforan, San Bruno, July 2023**
   - Page: https://www.flickr.com/photos/mliu92/53388157857/
   - Original: https://live.staticflickr.com/65535/53388157857_ff39bf7e4a_o.jpg
   - Credit: "Tanforan, San Bruno" by mliu92, CC BY-SA 2.0, via Flickr
   - License: CC BY-SA 2.0
   - Taken: 20 July 2023
   - Location: geotag 37.635150, -122.417423, inside the boundary.
   - Shows: a service ramp along the mall's blank exterior wall. It's weak but fairly current.

Not recommended:
- **"The Shops at Tanforan West Entrance" (2020).** It's tagged CC BY-SA 4.0 "own work" by WikiBoy06,
  but it looks like a professional marketing photo. Treat its provenance as doubtful.
- **BrokenSphere's 2005–2010 photos** (CC BY-SA 3.0): the entrance, the JCPenney and plaques. They're
  old.

### 2. Public-domain government images

- **Dorothea Lange, "American internees in mess hall line at Tanforan Assembly Center", 29 April 1942**
  - Page: https://commons.wikimedia.org/wiki/File:Dorothea_Lange_-_American_internees_in_mess_hall_line_at_Tanforan_Assembly_Center_San_Bruno_CA_April_29_1942.gif
  - Original: https://upload.wikimedia.org/wikipedia/commons/2/2f/Dorothea_Lange_-_American_internees_in_mess_hall_line_at_Tanforan_Assembly_Center_San_Bruno_CA_April_29_1942.gif
  - Credit: "Dorothea Lange, War Relocation Authority (National Archives 537677)"
  - Why it's public domain: Commons tags it PD-USGov-POTUS, as a work of the War Relocation Authority
    (Executive Office of the President). The source is NARA 537677.
  - Shows: the site's history as a wartime assembly center. It's small (600 px). **Historic only.**
    It's sensitive, so use it only with proper context, such as next to the Tanforan Memorial.
- Flickr (Anchor Editions, PDM): "San Bruno, California. A near- view of a horse stall left from days
  when what is now Tanforan Assembly center, was the famous Tanforan Race Track", 16 June 1942.
  https://www.flickr.com/photos/anchoreditions/31640743112/ . It's also a WRA photo, and higher
  resolution (3000 px).

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **Alexandria Real Estate Equities (ARE-San Francisco No. 96, LLC), applicant**
  - Project site per 2022 press: tanforanforsanbruno.com. I didn't open it, so confirm it first.
  - Press coverage credits the renderings to Gensler (architect) and James Corner Field Operations
    (landscape).
- **City of San Bruno, Community Development**
  - Peter Gilli, Community Development Director, is named in the CEQA notices. No email was
    confirmed.
  - City line: 650-616-7058, from https://www.sanbruno.ca.gov/1176/Environmental-Review-Documents-CEQAEIR

### 5. Official render pages to link

- https://www.sanbruno.ca.gov/1176/Environmental-Review-Documents-CEQAEIR (in officialLinks): the
  Draft and Final EIR. The project description figures are the official graphics.
- https://ceqanet.lci.ca.gov/2023120409 (in officialLinks).

---

## northgate-san-rafael (Northgate Town Square)

### 1. Openly licensed photos

1. **The Mall at Northgate, July 2014** (best)
   - Page: https://commons.wikimedia.org/wiki/File:The_Mall_at_Northgate.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/d/da/The_Mall_at_Northgate.jpg
   - Credit: "Mx. Granger, CC0, via Wikimedia Commons" (no credit required)
   - License: CC0 1.0, http://creativecommons.org/publicdomain/zero/1.0/deed.en
   - Taken: 20 July 2014
   - Location: geotag 38.002529, -122.543869, inside the boundary.
   - Shows: the "NORTHGATE" entrance with the Century Theatres canopy. Approval came in 2024, so this
     is the existing mall the plan replaces. **Old-ish but representative.**
2. **LensCrafters at Northgate Mall, August 2022**
   - Commons: https://commons.wikimedia.org/wiki/File:LensCrafters_San_Rafael_-_August_2022_-_Sarah_Stierch.jpg
     (CC BY 4.0, "Missvain")
   - Flickr: https://www.flickr.com/photos/sarahvain/52321301004/ (CC0, Sarah Stierch)
   - Original: https://upload.wikimedia.org/wikipedia/commons/e/e8/LensCrafters_San_Rafael_-_August_2022_-_Sarah_Stierch.jpg
   - Credit: under CC0 none is required; under the Commons terms, "Sarah Stierch, CC BY 4.0, via
     Wikimedia Commons"
   - Taken: 29 August 2022
   - Location: geotag 38.004467, -122.544869, inside the boundary.
   - Shows: a storefront entrance at the mall. **Fairly current** but tight and generic.
   - The same author published the same photo under CC0 on Flickr and CC BY 4.0 on Commons.
3. **Sustainable San Rafael 20th Anniversary, September 2025**
   - Page: https://commons.wikimedia.org/wiki/File:Sustainable_San_Rafael_20th_Anniversary.jpg
   - Credit: "Fabrice Florin, CC BY-SA 4.0, via Wikimedia Commons" (from Flickr fabola/54826361148)
   - Taken: 28 September 2025
   - Location: geotag inside the boundary (the event was at Ounces Outdoors).
   - Shows: an event crowd. **Current,** but it shows people rather than the site, so it's weak.

### 2. Public-domain government images

None found.

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **Merlone Geier Partners, owner and applicant**
  - Project site: https://futurenorthgatemall.com/ (Merlone Geier logo). It credits no renderings and
    lists no press contact.
  - Contacts: phone (415) 479-5956; a newsletter sign-up form.
- **City of San Rafael**
  - Project manager: Dan McLaughlin (TRB + Associates), dan.mclaughlin@cityofsanrafael.org.
  - Planning: community.development@cityofsanrafael.org, (415) 485-3085.
  - Both are from https://www.cityofsanrafael.org/northgatetownsquaredev/.

### 5. Official render pages to link

- https://www.cityofsanrafael.org/northgatetownsquaredev/ (in officialLinks). It shows a rendering
  captioned "Northgate Town Square Development", viewed from 4040 Civic Center Drive looking east. The
  rendering is uncredited, so link to it, don't copy it.
- https://www.cityofsanrafael.org/northgate-town-square-rev/ (in officialLinks): the archived
  entitlement page.

---

## ravenswood-business-district (Ravenswood / 4 Corners)

### 1. Openly licensed photos

1. **Aerial view of East Palo Alto, September 2019** (best)
   - Page: https://commons.wikimedia.org/wiki/File:Aerial_view_of_East_Palo_Alto,_September_2019.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/f/f6/Aerial_view_of_East_Palo_Alto%2C_September_2019.JPG
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL)
   - Taken: 17 September 2019
   - Location: the approximate geotag is about 155 m outside the boundary; it was taken from an
     airliner.
   - Shows: an oblique aerial of East Palo Alto with the Bay, Dumbarton Bridge and baylands beyond.
     The light industrial blocks toward the shore and Cooley Landing are the RBD area, but I haven't
     pinpointed the plan boundary in the frame. **Fairly old** (before the 2024 plan).
2. **East Palo Alto aerial view with Dumbarton Bridge, August 2021**
   - Page: https://commons.wikimedia.org/wiki/File:East_Palo_Alto_aerial_view_with_Dumbarton_Bridge.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/a/a5/East_Palo_Alto_aerial_view_with_Dumbarton_Bridge.jpg
   - Credit: "Alfred Twu, CC0, via Wikimedia Commons"
   - License: CC0 1.0
   - Taken: 11 August 2021
   - Shows: a hazy view southwest over the Dumbarton Bridge and salt ponds, with East Palo Alto and the
     Ravenswood shoreline in the middle distance. Good for regional context; the site is small in
     frame.
3. **Aerial East Palo Alto, September 2014**
   - Page: https://commons.wikimedia.org/wiki/File:Aerial_East_Palo_Alto_(17379698086).jpg
   - Credit: "Tony Webster, CC BY 2.0, via Wikimedia Commons"
   - Taken: 10 September 2014
   - Shows: an aerial while landing at SFO. **Old.**

No ground-level photo inside the plan area was found on Commons or Flickr. A geosearch within 900 m
found only a highway sign and rail photos.

### 2. Public-domain government images

None found.

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **City of East Palo Alto, Planning**
  - General contacts: planning@cityofepa.org, 650-853-3189.
  - For the EPA Waterfront project page renderings, two planners are named: Christopher Dacumos
    (consulting planner), cdacumos@cityofepa.org, and Alvin Jen (associate planner),
    ajen@cityofepa.org.
- **Sycamore Real Estate Investment LLC and Emerson Collective**, applicants for EPA Waterfront, the
  largest RBD project. Their renderings are on
  https://www.cityofepa.org/planning/project/east-palo-alto-epa-waterfront without credit. No
  applicant contact was found.

### 5. Official render pages to link

- https://www.cityofepa.org/planning/page/ravenswood4-corners-specific-plan-adopted-12172024 (in
  officialLinks). It has only plan PDFs; the vision chapters of the plan are the likely place for
  graphics.
- **Better for renderings:** https://www.cityofepa.org/planning/project/east-palo-alto-epa-waterfront
  (in sources, not officialLinks). It shows five renderings and site plans.

---

## bart-station-housing (BART station-area housing)

Each image here was checked against its own station's polygon in the boundary file.

### 1. Openly licensed photos

**Lake Merritt**
1. **TOD construction at Lake Merritt station, September 2025** (best overall for this project)
   - Page: https://commons.wikimedia.org/wiki/File:TOD_construction_at_Lake_Merritt_station,_September_2025.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/8/82/TOD_construction_at_Lake_Merritt_station%2C_September_2025.jpg
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 27 September 2025
   - Location: geotag 37.796966, -122.265176, inside the Lake Merritt polygon.
   - Shows: concrete columns and rebar rising on the former parking lot, with a crane. **Current.**
2. **TOD construction at Lake Merrit station, March 2025**
   - Page: https://commons.wikimedia.org/wiki/File:TOD_construction_at_Lake_Merrit_station,_March_2025.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/8/87/TOD_construction_at_Lake_Merrit_station%2C_March_2025.jpg
   - Credit and license: the same as above
   - Taken: 30 March 2025
   - Location: inside the Lake Merritt polygon.
   - Shows: an earlier construction stage. The file name misspells "Merrit".

**West Oakland**
- **South parking lot at West Oakland station, March 2024**
  - Page: https://commons.wikimedia.org/wiki/File:South_parking_lot_at_West_Oakland_station,_March_2024.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/3/36/South_parking_lot_at_West_Oakland_station%2C_March_2024.jpg
  - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
  - Taken: 17 March 2024
  - Location: geotag 37.804504, -122.294340, inside the West Oakland polygon.
  - Shows: an elevated view over the station parking lot, with port cranes and the SF skyline beyond.
    **Fairly current** (before construction).
- Also: "West Oakland station from parking lot, April 2018" (CC BY-SA 3.0, Pi.1415926535), inside
  the polygon; **old**.

**North Berkeley**
- **North Berkeley station east side, January 2026**
  - Page: https://commons.wikimedia.org/wiki/File:North_Berkeley_station_east_side_January_2026.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/9/9a/North_Berkeley_station_east_side_January_2026.jpg
  - Credit: "4300streetcar, CC BY 4.0, via Wikimedia Commons"
  - License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0
  - Taken: 29 January 2026
  - Location: geotag 37.873990, -122.282930, inside the North Berkeley polygon.
  - Shows: the round station headhouse and plaza. **Current,** but it shows the station, not the
    parking lots being built on.
- Also: "BART substation at North Berkeley, November 2024" (CC BY-SA 4.0, Pi.1415926535), at the
  edge of the site.

**Ashby (west lot)**
- **Berkeley Flea Market 2019 - 1**
  - Page: https://commons.wikimedia.org/wiki/File:Berkeley_Flea_Market_2019_-_1.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/5/5c/Berkeley_Flea_Market_2019_-_1.jpg
  - Credit: "Suiren2022, CC BY-SA 4.0, via Wikimedia Commons"
  - License: CC BY-SA 4.0
  - Taken: 11 May 2019
  - Location: geotag 37.853911, -122.270072, inside the Ashby (West Lot) polygon.
  - Shows: the weekend flea market on the west lot that the project will build on. **Old-ish** but
    characteristic. Files 2–6 in the same series are also inside the polygon.

**El Cerrito Plaza**
- **El Cerrito Plaza station from parking lot, October 2012**
  - Page: https://commons.wikimedia.org/wiki/File:El_Cerrito_Plaza_station_from_parking_lot,_October_2012.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/1/1f/El_Cerrito_Plaza_station_from_parking_lot%2C_October_2012.jpg
  - Credit: "Pedro Xing, CC0, via Wikimedia Commons"
  - License: CC0 1.0
  - Taken: 28 October 2012
  - Location: geotag about 5 m outside the El Cerrito Plaza polygon.
  - Shows: the surface parking lot with the elevated station and a train. **Old.**
- Also: "West side of El Cerrito Plaza station, July 2018" (CC BY-SA 3.0, Pi.1415926535), inside the
  polygon.
- Also: Flickr "El Cerrito Plaza Station" by Roadgeek Adam, 11 May 2023, CC BY-SA 2.0 (license from
  the search record), for example https://www.flickr.com/photos/9962140@N02/52908558524 . I didn't
  open these or check what they show.

**Amador (West Dublin/Pleasanton)**
- **West Dublin Pleasanton station from parking garage, May 2018**
  - Page: https://commons.wikimedia.org/wiki/File:West_Dublin_Pleasanton_station_from_parking_garage,_May_2018.JPG
  - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
  - Taken: 10 May 2018
  - Location: geotag about 40 m outside the Amador polygon.
  - Shows: the station and its pedestrian bridge over I-580. The vacant Golden Gate Drive parcel
    itself isn't clearly in frame. **Old; context only.**

### 2. Public-domain government images

None found.

### 3. Press/media kits with stated permission

None found. BART's TOD pages state no image terms.

### 4. Permission leads

- **BART Property Development**, from the station TOD pages:
  - Shannon Dodge, sdodge@bart.gov, for North Berkeley and Ashby.
  - Yvette McCoy, Yvette.McCoy@bart.gov, for Lake Merritt and West Oakland.
  - Carli Paine, carli.paine@bart.gov, for El Cerrito Plaza.
  - BART media relations: Jim Allison, (510) 464-7110, per a search snippet of the bart.gov media
    resources page; confirm first. The general media email was masked in the results.
- **North Berkeley:** BART credits its rendering to "David Baker Architects and Yes Community
  Architects" and its diagram to "North Berkeley Housing Partners". Developer site:
  https://www.northberkeleyhousingpartners.org/ (feedback and subscribe forms only).
- **Lake Merritt:**
  - BART credits the Building B rendering to EBALDC. Developer pages: https://ebaldc.org/chinatown-bart/
    and https://stradasf.com/projects/office/lake-merritt-bart-tod/.
  - On the Oakland page, the developer contact is William Goodman (STRADA/EBALDC), 314-276-0707, and
    the city contact is cpayne@oaklandca.gov.
- **West Oakland (Mandela Station):**
  - Oakland's gallery credits its six renderings "Courtesy JRDV Urban International".
  - Developer contact: Ronnie Turner, Turner Development Resource Group, rtdevelops@comcast.net,
    (510) 395-2766.
  - City contact: pvollmann@oaklandca.gov, (510) 238-6167.
- **El Cerrito Plaza:**
  - Developer site: https://elcerritotod.squarespace.com (Holliday Development and Related).
  - City: community@elcerrito.gov, 510-215-4300. The city's TOD renderings (dated 06-2024) are
    uncredited.
- **Ashby:**
  - Adeline Alliance Partners with Resources for Community Development. BART's page shows an
    uncredited rendering and links only the team's posterboard PDF.
- **Amador:**
  - KTGY, the architect, has a project page: https://ktgy.com/Work/amador-station/ (page only).
  - Developer: The Related Companies of California. No contact was found.

### 5. Official render pages to link

- https://www.bart.gov/about/business/tod/north-berkeley (in sources): a credited rendering.
- https://www.oaklandca.gov/Planning-Building/Major-Development-Projects/West-Oakland-BART-Development-Mandela-Station
  (in sources): a gallery of six credited renderings.
- Others: https://www.oaklandca.gov/Planning-Building/Major-Development-Projects/Lake-Merrit-BART-Transit-Oriented-Development
  and https://elcerrito.gov/1381/Transit-Oriented-Development-TOD (both in sources).
- The officialLinks entry https://www.bart.gov/about/business/tod/upcoming has no images.

---

## oceanwide-center (Oceanwide Center, 50 First Street)

### 1. Openly licensed photos

None found that show the site. Here's what was searched:
- Commons geosearch within 110 m.
- Commons keyword searches for "Oceanwide" (all results were Oceanwide Plaza in Los Angeles) and for
  "50 First Street".
- Openverse.
- A Flickr bounding-box search over the block, with 184 openly licensed photos, mostly food and
  events.

The nearest Commons files are a 2024 colonnade photo at Mission and First, which is outside the
polygon on the opposite side, and 2018 Transbay Transit Center views. Neither shows the excavation.

### 2. Public-domain government images

None found.

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **Foster + Partners with Heller Manus Architects**, credited for the 2016 approved design. The
  renderings appear in the SF Planning case packet below.
- A September 2026 SFist report says a new proposal, "Fifty at First" by Gensler, has been filed.
  This is press only. If it's confirmed, the 2016 renderings are superseded and shouldn't be shown as
  current. Before asking for any images, check SF Planning for the new record and its applicant.
- No developer contact was found. The 2016 entity, Oceanwide Center LLC, reportedly lost the site in
  foreclosure.

### 5. Official render pages to link

- https://commissions.sfplanning.org/cpcpackets/2006.1523DNXOFACUAVARSHDGPR.pdf (in sources): the
  2016 commission packet with the plans and renderings. Label it as the 2016 design.
- https://sfgov.legistar.com/LegislationDetail.aspx?ID=2694215&GUID=FE35D8F3-4DA8-432E-A2A3-BD70AD9B1EA0
  (in officialLinks).

---

## 30-van-ness (30 Van Ness)

### 1. Openly licensed photos

1. **Northeast entrance and surface stop at Van Ness station, January 2020** (best, but check what it
   shows)
   - Page: https://commons.wikimedia.org/wiki/File:Northeast_entrance_and_surface_stop_at_Van_Ness_station,_January_2020.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/8/82/Northeast_entrance_and_surface_stop_at_Van_Ness_station%2C_January_2020.JPG
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL)
   - Taken: 30 January 2020
   - Location: geotag 37.775423, -122.419075, about 13 m outside the boundary, at the corner.
   - Shows: a view east along Market Street. On the left is a mid-century office building with a
     Walgreens at street level, which appears to be the former 30 Van Ness office building on the
     site. **I haven't verified that identification.**
   - **Old:** the record says the building has gone and the site was excavated before work stopped
     in 2023.
2. **Covered entrance to Van Ness station, May 2021**
   - Page: https://commons.wikimedia.org/wiki/File:Covered_entrance_to_Van_Ness_station,_May_2021.jpg
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - Taken: 10 May 2021
   - Location: about 12 m outside the boundary.
   - Shows: a station entrance at the corner. The site is likely at the edge of the frame; I didn't
     open a preview.

No photo of the excavated or stalled site (2023 onward) was found on Commons, Openverse or Flickr.

### 2. Public-domain government images

None found.

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **Lendlease (30 Van Ness Development, LLC)**, developer.
  - The architect is Solomon Cordwell Buenz (SCB), per 2020–22 press. One press rendering is credited
    "Rendering by Steelblue".
  - No press contact was confirmed. Start with Lendlease's US newsroom.

### 5. Official render pages to link

- https://citypln-m-extnl.sfgov.org/Commissions/CPC/3_13_2025/Commission%20Packet/2024-008290DNX-02.pdf
  (in officialLinks): the 2025 packet with the current plans.
- https://commissions.sfplanning.org/cpcpackets/2017-008051DNXCUAOFASHDENV.pdf (in sources): the
  2020 approval packet.

---

## west-midway-reshap (West Midway and RESHAP)

### 1. Openly licensed photos

None found that clearly show the site:
- Commons geosearch within 380 m: nothing.
- Commons searches for "West Midway" and "Alameda Point Collaborative": nothing.
- Flickr bounding-box search: five photos, all interiors at Almanac Brewing.

The December 2022 Seaplane Lagoon aerial (see alameda-point-plan) looks across the base. West Midway
lies north of the lagoon, probably just outside or at the edge of that frame; I couldn't confirm it.

### 2. Public-domain government images

- **NAS Alameda aerial view, 1995**
  - Page: https://commons.wikimedia.org/wiki/File:NAS_Alameda_aerial_view_in_1995.JPEG
  - Original: https://upload.wikimedia.org/wikipedia/commons/3/3f/NAS_Alameda_aerial_view_in_1995.JPEG
  - Credit: "PH2 Bruce Trombecky, U.S. Navy (DefenseImagery VIRIN DN-ST-97-01688)"
  - Why it's public domain: Commons tags it "PD US Military", as a work of a US military employee
    made in the course of duty.
  - Shows: an overhead of the whole air station. The Navy housing area at West Midway should be in
    frame, but I haven't pinpointed it. **Historic only.**

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **Brookfield and Catellus (BC West Midway LLC)**, for the market-rate homes, and **MidPen Housing**
  with the Alameda Point Collaborative, for RESHAP. No contact pages were checked.
- **City of Alameda, Base Reuse and Economic Development**: econdev@alamedaca.gov; Jennifer Padilla,
  jpadilla@alamedaca.gov. These are from candidates-sf-west-islands.md and weren't re-checked.

### 5. Official render pages to link

- The City's Major Planning Projects page,
  https://www.alamedaca.gov/Departments/Planning-Building-and-Transportation/Planning-Division/Major-Planning-Projects,
  lists the following. **Not in officialLinks; recommend adding them.**
  - West Midway Development Plan (4 May 2023):
    https://www.alamedaca.gov/files/assets/public/v/1/major-planning-projects/west-midway-development-plan-may-4-2023.pdf
  - RESHAP Development Plan (8 May 2023):
    https://www.alamedaca.gov/files/assets/public/v/1/major-planning-projects/reshap-development-plan-may-8-2023.pdf
- Check that alamedaca.gov is on the official-host list. It isn't listed explicitly in
  `src/projects/official.ts`; the list does include a `.ca.us` suffix and `alameda.legistar.com`.

---

## alameda-point-plan (Alameda Point, rest of the base)

### 1. Openly licensed photos

1. **Aerial view of Alameda Seaplane Lagoon, December 2022** (best)
   - Page: https://commons.wikimedia.org/wiki/File:Aerial_view_of_Alameda_Seaplane_Lagoon,_December_2022.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/5/54/Aerial_view_of_Alameda_Seaplane_Lagoon%2C_December_2022.JPG
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL)
   - Taken: 15 December 2022
   - Location: the approximate geotag is in the lagoon, about 300 m outside the multipolygon.
   - Shows: Seaplane Lagoon, the former runways and wetlands, the hangar rows, and the USS Hornet at
     the carrier pier. Most of this is the plan area. **Fairly current.**
   - The same image is the best pick for alameda-point (Site A) in candidates-sf-west-islands.md.
2. **Seaplane Lagoon, September 2022**
   - Page: https://www.flickr.com/photos/pagedooley/52446417103/
   - Original: https://live.staticflickr.com/65535/52446417103_4f6793c694_o.jpg
   - Credit: "Seaplane Lagoon" by Kevin Dooley, CC BY 2.0, via Flickr
   - License: CC BY 2.0
   - Taken: 11 September 2022
   - Location: geotag at the Hornet.
   - Shows: the lagoon and the hangars beyond. **Fairly current.**
3. **Alameda Point, with San Francisco in distance, June 2010**
   - Page: https://www.flickr.com/photos/sirqitous/4798269016/
   - Original: https://live.staticflickr.com/4074/4798269016_25f7dd2807_o.jpg
   - Credit: "Alameda Point, with San Francisco in distance" by Eric Golub (sirqitous), CC BY 2.0,
     via Flickr
   - Taken: 30 June 2010
   - Location: geotag about 120 m outside the boundary, at the shoreline.
   - Shows: the base's open shoreline. **Old.** Eric Golub's other "Alameda Point, June 2" photos are
     also CC BY 2.0; the one I previewed was a reflection selfie, so check each.

### 2. Public-domain government images

- **NAS Alameda aerial view, 1995**: see west-midway-reshap above (PD US Military). **Historic.**
- **An overhead aerial horizontal view of Naval Air Station Alameda, 1 August 1993**
  - Page: https://commons.wikimedia.org/wiki/File:An_overhead_aerial_horizontal_view_of_Naval_Air_Station_Alameda_-_DPLA_-_d23230693c957cca0080731dbf739832.jpeg
  - Original: https://upload.wikimedia.org/wikipedia/commons/7/7a/An_overhead_aerial_horizontal_view_of_Naval_Air_Station_Alameda_-_DPLA_-_d23230693c957cca0080731dbf739832.jpeg
  - Credit: "Department of Defense, Defense Visual Information Center (National Archives)"
  - Why it's public domain: Commons tags it "PD US Military" (DoD).
  - Shows: an overhead of the air station. **Historic.**
- The Commons category "Naval Air Station Alameda" has many more Navy photos, mostly aircraft.

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **City of Alameda (landowner), Base Reuse and Economic Development**: econdev@alamedaca.gov;
  Jennifer Padilla, jpadilla@alamedaca.gov. These are from candidates-sf-west-islands.md and weren't
  re-checked. The plan graphics are City documents; ask about their reuse.
- The volunteer-run alamedapointinfo.com marks its images as copyrighted, so don't use them.

### 5. Official render pages to link

- https://www.alamedaca.gov/Departments/Alameda-Point (the Base Reuse page; not in officialLinks).
- Plan documents on the Major Planning Projects page:
  - Main Street Neighborhood Specific Plan (April 2017):
    https://www.alamedaca.gov/files/assets/public/v/1/major-planning-projects/alameda-point-main-street-neighborhood-specific-plan-april-2017.pdf
  - Town Center and Waterfront Precise Plan (July 2014):
    https://www.alamedaca.gov/files/assets/public/v/1/major-planning-projects/alameda-point-town-center-and-waterfront-precise-plan-july-2014.pdf
  - These are the illustrative graphics. The 2014 precise plan may be partly superseded, so label it
    by date.

---

## encinal-terminals (Encinal Terminals)

### 1. Openly licensed photos

1. **Aerial view of Alameda and Oakland, September 2019** (context only)
   - Page: https://commons.wikimedia.org/wiki/File:Aerial_view_of_Alameda_and_Oakland,_September_2019.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/e/e7/Aerial_view_of_Alameda_and_Oakland%2C_September_2019.JPG
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL)
   - Taken: 20 September 2019
   - Location: no geotag.
   - Shows: an oblique aerial looking northeast over Alameda to the estuary and downtown Oakland. In
     the middle is a pale paved wharf jutting into the estuary, with a marina to its right and Coast
     Guard Island further right. That matches Encinal Terminals and Alameda Marina, but it's my reading
     of the frame and **needs verification**. The site is small in frame.

No other photo of the wharf was found:
- Commons geosearch within 320 m: nothing.
- Openverse "Encinal Terminals": nothing.
- Flickr: the bounding-box hits were vonguard's 2021 photos of the Alameda Landing waterfront
  structure, geotagged about 30 m west of the boundary. They show the neighbouring site, not this one.

### 2. Public-domain government images

None verified for this site.

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **North Waterfront Cove, LLC c/o Tim Lewis Communities**, developer: 12667 Alcosta Blvd., Suite
  170, San Ramon, CA 94583. The address is from the 2016 scoping notice, as quoted in a search result;
  confirm it first. No press contact was found.
- The Alameda Post's coverage shows a conceptual plan image (press, not for use).

### 5. Official render pages to link

- Revised Encinal Master Plan 2022, from the City's Major Planning Projects page. **Not in
  officialLinks; recommend adding it.**
  https://www.alamedaca.gov/files/assets/public/v/1/major-planning-projects/revised-encinal-master-plan-2022.pdf
- https://webapi.legistar.com/v1/alameda/matters/15672/texts/16874 (in officialLinks): text only.

---

## alameda-marina (Alameda Marina)

### 1. Openly licensed photos

No current photo was found: none shows the new apartment building or the townhomes. Here's the best
available:

1. **Aerial view of Coast Guard Island, May 2025** (edge of frame)
   - Page: https://commons.wikimedia.org/wiki/File:Aerial_view_of_Coast_Guard_Island,_May_2025.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/d/de/Aerial_view_of_Coast_Guard_Island%2C_May_2025.JPG
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL)
   - Taken: 21 May 2025
   - Shows: Coast Guard Island, with Brooklyn Basin beyond. The marina at the bottom-left corner is
     probably Alameda Marina, but it's only partly in frame, which **needs verification**.
     **Current.**
2. **Alameda Marina, October 2010**
   - Page: https://www.flickr.com/photos/sirqitous/5103804422/
   - Original: https://live.staticflickr.com/1423/5103804422_5b2b813873_o.jpg
   - Credit: "Alameda Marina" by Eric Golub (sirqitous), CC BY 2.0, via Flickr
   - License: CC BY 2.0, https://creativecommons.org/licenses/by/2.0/
   - Taken: 13 October 2010
   - Location: no geotag; the location comes from the title only.
   - Shows: sailboats at the docks, with downtown Oakland across the estuary. **Old** (before
     redevelopment).
   - A companion photo, "Alameda Marina towards Oakland" (5103208651), has the same license and date.
3. **Aerial view of Alameda and Oakland, September 2019**: see encinal-terminals. It shows the marina
   small in frame (needs verification).

Not recommended: Tony Webster's 2014 "Alameda Marina" photos (CC BY 2.0). They're geotagged at Jack
London Square in Oakland, about 2.5 km away, and appear to show a different marina.

### 2. Public-domain government images

- **General Engineering yard, Alameda, c. 1944** (best historic)
  - Page: https://commons.wikimedia.org/wiki/File:12-2-1_Gen-Engg-Alameda-25.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/3/35/12-2-1_Gen-Engg-Alameda-25.jpg
  - Credit: "Edwards Cochrane, Navy Department Bureau of Ships"
  - Why it's public domain: Commons tags it PD-USGov, as a work of the Navy Bureau of Ships. The source
    is https://www.shipscribe.com/cochrane/shipyards/12th-ND.htm.
  - Location: geotag about 31 m outside the boundary.
  - Shows: an aerial across the estuary of the wartime General Engineering & Dry Dock yard on
    Alameda's north shore, which is the historic shipbuilding site now being redeveloped. Coast Guard
    Island is in the foreground. **Historic.**
- **ALAMEDA MARINA - NARA - 544661, August 1972** (EPA DOCUMERICA)
  - Page: https://commons.wikimedia.org/wiki/File:ALAMEDA_MARINA_-_NARA_-_544661.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/c/c9/ALAMEDA_MARINA_-_NARA_-_544661.jpg
  - Credit: "Belinda Rain, U.S. EPA DOCUMERICA (National Archives 544661)"
  - Why it's public domain: Commons tags it PD US EPA, as the work of an EPA contract photographer for
    DOCUMERICA.
  - Shows: sailboats at dusk with the Oakland skyline. **Historic.**

### 3. Press/media kits with stated permission

None found.

### 4. Permission leads

- **Alameda Marina, LLC**, developer. Press from 2016–2018 names Bay West Development as sponsor, with
  Sean Murphy as project lead. KTGY is the architect, and a 2018 rendering is reposted on KTGY's site
  (https://ktgy.com/?p=15045). No current developer site or contact was confirmed.
- **City of Alameda Planning:** City Hall (510) 747-7400. No planner was named on the projects page.

### 5. Official render pages to link

Documents on the City's Major Planning Projects page. **Not in officialLinks; recommend adding
them.**
- Master Plan Approved by Council (July 2018):
  https://www.alamedaca.gov/files/assets/public/v/1/minor-planning-projects/alameda-marina-master-plan-approved-by-council-july-2018.pdf
- Phase 1 design review submittal (June 2019):
  https://www.alamedaca.gov/files/assets/public/v/1/major-planning-projects/item-7-a-exhibit-3-ala-marina-phase-1-dr-submittal.pdf
- Wrap B plans (PLN23-0179):
  https://www.alamedaca.gov/files/assets/public/v/1/major-planning-projects/pln23-0179-alameda-marina-wrap-b-plans_reduced.pdf
