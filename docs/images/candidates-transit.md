# Image candidates: transit group

Research only. Nothing was downloaded into the repo, no repo file other than this one was changed
(`data/photos.json` was not touched), and no one was contacted. Checked 2026-10-12.

Projects: the-portal, cahsr-sf-sj, bart-silicon-valley-phase-2, diridon-station, valley-link,
smart-healdsburg, smart-cloverdale, mission-bay-ferry-landing, berkeley-pier-ferry,
redwood-city-ferry-terminal.

How I searched:
- I ran Wikimedia Commons geosearches around each project's stations and sites, using the traced
  boundaries in `data/boundaries/<id>.geojson` to pick the points: 16th Street (Mission Bay), the Port
  of Redwood City wharf, the foot of University Avenue and along the pier (Berkeley), Diridon, Fourth
  and Townsend and Second Street (Portal), downtown San José, 28th Street/Little Portugal and Santa
  Clara (BART), the Healdsburg depot, Geyserville, Cloverdale, Isabel Avenue and Mountain House
  (Valley Link). I also searched Commons by keyword and category (Berkeley Pier, Construction of the
  Transbay Transit Center, San Jose Diridon station, Port of Redwood City, Dublin/Pleasanton station,
  California High-Speed Rail, Northwestern Pacific Railroad, Mission Bay). Then I ran Openverse with
  the license filter set to CC0, PDM, CC BY and CC BY-SA, which also covers Flickr.
- Wikimedia Commons rate-limited this environment (HTTP 429). I spaced calls at least 3 seconds apart
  and honoured Retry-After, but many requests still failed. To check licenses I read the license
  template, author, date and source for each Commons file I list. Three came from the Commons API
  itself. The rest came from the file page as parsed by Magnus Manske's Toolforge Commons API
  (`magnus-toolserver.toolforge.org/commonsapi.php`), which reads the same file page. I read each
  Flickr item's own photo page for its license, date and geotag.
- Because of the rate limit, I opened previews of only three images to see what they show (marked
  "seen" below). Every other description comes from the file's own caption. Some Commons keyword
  searches never finished: "Port of Redwood City ferry", "Caltrain electrification Millbrae",
  "Russian River railroad bridge", "Valley Link rail" and "Isabel Avenue Livermore". The Openverse
  searches on the same terms did finish, so the gap is small, but I can't rule out a file I missed.
- I left out all NC, ND and "all rights reserved" images, and photos where identifiable people are
  the subject (for example the 2018 "MLK Day" set at 4th and King, and the political event photos at
  the Caltrain electrification groundbreaking).

How credit lines work: they follow the TASL pattern (title, author, source, license). CC BY and
CC BY-SA need the author named, a link to the license, and a note if the image was changed. CC BY-SA
crops must stay CC BY-SA. CC0 and public-domain US government images need no credit, but giving one
is good practice. "Current" means the photo matches conditions on the ground today as far as I can
tell. "Old" means the site has changed since. Direct original URLs are for reference only. Don't
hotlink them: copy the file into the build if it's used.

For line projects (Portal, high-speed rail, BART, Valley Link, both SMART legs), no single photo shows
the project. The best candidates show a station site, the corridor, or the existing structure the
project reuses or replaces, and the captions should say so ("The empty train box under construction,
2015", "Healdsburg's 1928 depot, July 2022").

Agency media terms, checked on each agency's own pages:
- **VTA**: the newsroom lists Media Relations, (408) 464-7810, media.relations@vta.org. It also
  names Stacey Hendler Ross (Public Information Officer, stacey.hendlerross@vta.org) and media
  spokespersons Sandra Bermudez (sandra.bermudez@vta.org) and Marina Chakmakjian
  (Marina.Chakmakjian@vta.org): https://vta.gov/about/newsroom. There's a photo library at
  https://www.vta.org/all-photosvideos, but it states no reuse terms, and the site footer reads
  "Copyright 2026 Santa Clara Valley Transportation Authority (VTA). All rights reserved." Not usable
  without permission.
- **Caltrain**: the Terms of Use (https://www.caltrain.com/terms-of-use) say "All text, images,
  graphics, and other content on the Site is owned or licensed by us and may not be used, copied,
  modified, or duplicated without prior written consent." The media relations page
  (https://www.caltrain.com/about-caltrain/media-relations) names Dan Lieberman, public information
  officer, (650) 622-2492, liebermand@samtrans.com. I got the contact through search and didn't open
  the page.
- **California High-Speed Rail Authority**: hsr.ca.gov sits behind a bot wall (Incapsula), so I
  couldn't open the newsroom, the press kit or the San Francisco–San Jose page. Search snippets
  describe a 2019 news release saying the newsroom offers downloadable high-resolution photos and
  video, and that the content is free for public use. **I couldn't verify that wording**, so I've
  treated it as a permission lead, not a grant. General contact: info@hsr.ca.gov. A CalSTA page lists
  Annie Parker, (916) 403-6931, as the Authority's press contact (unverified; may be out of date).
- **TJPA**: the media gallery (https://www.tjpa.org/about-tjpa/media-gallery) has a "The Portal"
  album and says "Select from the albums below to view renderings of the new Transbay Transit Center,
  historical photos of the former Transbay Terminal and other images related to the project." It
  states no usage terms. The contact page says "Media inquiries and/or Public Records requests should
  be emailed to info@tjpa.org."
- **SMART**: no media kit or usage terms. Healdsburg Extension contact: Allison Mattioli,
  Communications + Marketing Specialist, (707) 285-8248, amattioli@sonomamarintrain.org (on the
  extension and Geyserville pages). The September 2025 Healdsburg contract release names Julia
  Gonzalez, Communications and Marketing Manager, 707-794-3063, jgonzalez@sonomamarintrain.org
  (https://www.sonomamarintrain.org/node/625).
- **WETA (San Francisco Bay Ferry)**: the Media and Reports page
  (https://www.sfbayferry.com/media-and-reports/) lists Media@sanfranciscobayferry.com and a media kit:
  "For media professionals, our media kit offers high-resolution images and logos. Download the
  materials you need to cover our services accurately." The kit is a Bynder brand portal
  (https://weta.bynder.com/share/A840DBDE-2ADE-4435-9DF75A2D79EFE5CC/) that asks for a download
  reason. **No license is stated**, and it's framed for news coverage, so it goes under permission
  leads, not section 3.
- **Port of Redwood City**: no media page. Contact: info@redwoodcityport.com, (650) 306-4150, 675
  Seaport Blvd. (https://www.redwoodcityport.com/ferry).
- **City of Berkeley**: no media kit. The project page lists the project manager at
  LMcNulty@berkeleyca.gov (https://berkeleyca.gov/node/9711).
- **Port of San Francisco**: the Mission Bay Ferry Landing page lists Project Manager Simon Betsalel,
  simon.betsalel@sfport.com (https://sfport.com/mission-bay-ferry-landing). Port press releases have
  used media@sfport.com (found through search; not verified on a current page).

Result: **no agency in this group publishes a press kit with an explicit reuse grant** I could
verify. Every rendering is a permission request.

---

## the-portal (The Portal / Downtown Rail Extension, San Francisco)

### 1. Openly licensed photos

1. **Transbay Transit Center construction from above, June 2015** (best: the train box being built)
   - Page: https://commons.wikimedia.org/wiki/File:Transbay_Transit_Center_construction_from_above,_June_2015.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/8/86/Transbay_Transit_Center_construction_from_above%2C_June_2015.jpg
     (2994 × 2288)
   - Credit: "RChin, CC BY-SA 2.0, via Wikimedia Commons" (from Flickr, IMG_3957b,
     https://www.flickr.com/photos/10713366@N08/16377088245; passed FlickreviewR)
   - License: CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0
   - Taken: Commons says "Taken on 26 January 2015"; the title says June 2015. Use "2015".
   - Shows (caption): "Construction of the Transbay Transit Center in June 2015. The curve of the
     future rail tunnel is at top." This is the below-grade train box the Portal would finally use.
     **Old** (the box has been finished and empty since 2018). Not visually confirmed.
2. **Transbay Transit Center Tour below**
   - Page: https://commons.wikimedia.org/wiki/File:Transbay_Transit_Center_Tour_below.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/e/e1/Transbay_Transit_Center_Tour_below.jpg
     (5330 × 3558)
   - Credit: "SPUR, CC BY 2.0, via Wikimedia Commons" (Flickr user urbanists,
     https://www.flickr.com/photos/urbanists/9157861620/; passed FlickreviewR)
   - License: CC BY 2.0, https://creativecommons.org/licenses/by/2.0
   - Taken: 25 June 2013
   - Shows (caption): "View of the under-construction Transbay Transit Center from below", from
     SPUR's 25 June 2013 construction tour, which went down into the excavation. **Old.** Not visually
     confirmed. Check that the frame shows the lower (train box) levels before captioning it that way.
     The rest of the tour set is in
     https://commons.wikimedia.org/wiki/Category:Transbay_Transit_Center_construction_tour,_June_25,_2013
3. **San Francisco (4th & Townsend) station** (the Portal's new underground station site)
   - Page: https://commons.wikimedia.org/wiki/File:San_Francisco_(4th_%26_Townsend)_station_(29103882797).jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/9/97/San_Francisco_%284th_%26_Townsend%29_station_%2829103882797%29.jpg
     (3036 × 4048, portrait)
   - Credit: "mliu92 from San Mateo, CC BY-SA 2.0, via Wikimedia Commons" (Flickr
     https://www.flickr.com/photos/mliu92/29103882797/)
   - License: CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0
   - Taken: 14 August 2018. Geotagged 37.776438, −122.394678, at the Fourth and Townsend corner of
     the existing Caltrain station.
   - Shows: the surface Caltrain terminal at Fourth and Townsend. **Current-ish** (the station is still
     there, now with electric trains). Not visually confirmed.
- Also on Commons: "Transbay Transit Center construction from TJPA office, August 2017" (Pi.1415926535,
  CC BY-SA 3.0, 11 August 2017,
  https://commons.wikimedia.org/wiki/File:Transbay_Transit_Center_construction_from_TJPA_office,_August_2017.jpg).
  It's an above-ground view, so it's less relevant to the rail levels.
- No Commons or Openverse photo of the finished, empty train box interior found. The public hasn't
  been allowed into it. TJPA's own construction photos would be the source (see 4).

### 2. Public-domain government images
- None found. The US DOT/FRA has published no photos of the site on Commons.

### 3. Press kits with stated permission
- None. The TJPA media gallery states no usage terms (see the header).

### 4. Permission leads
- **TJPA** owns the Portal renderings and the train-box construction photos. Media gallery, "The
  Portal" album: https://www.tjpa.org/about-tjpa/media-gallery (filter by album; the filter needs
  JavaScript). Contact: info@tjpa.org ("Media inquiries and/or Public Records requests").
- Architect of the Transit Center (and of its train box): Pelli Clarke & Partners. I didn't look up a
  media contact.

### 5. Official render pages to link
- https://www.tjpa.org/portaldtx/about-portal (already in officialLinks)
- https://www.tjpa.org/about-tjpa/media-gallery ("The Portal" album)

---

## cahsr-sf-sj (California High-Speed Rail: San Francisco to San Jose)

### 1. Openly licensed photos
The project runs high-speed trains on Caltrain's newly electrified corridor, so the most honest photo
is the corridor as it is now.

1. **Caltrain KISS set at 4th and King, April 2024** (best: the electrified terminus HSR would share)
   - Page: https://commons.wikimedia.org/wiki/File:Caltrain_KISS_set_at_4th_and_King,_April_2024.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/d/d7/Caltrain_KISS_set_at_4th_and_King%2C_April_2024.jpg
     (4032 × 3024)
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 23 April 2024
   - Shows (caption): "A Caltrain KISS trainset at 4th and King station in April 2024. Three sets were
     temporarily stored at the station during testing of the new electrification." **Current.**
2. **Caltrain Stadler KISS at San Francisco station (1, August 2025)**
   - Page: https://commons.wikimedia.org/wiki/File:Caltrain_Stadler_KISS_at_San_Francisco_station_(1,_August_2025).jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/2/2d/Caltrain_Stadler_KISS_at_San_Francisco_station_%281%2C_August_2025%29.jpg
     (5712 × 4284)
   - Credit: "Evan0512, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 17 August 2025
   - Shows: "Three Stadler KISS EMUs at San Francisco station". **Current.**
3. **Caltrain electrification infrastructure, just south of Burlingame station** (Flickr)
   - Page: https://www.flickr.com/photos/23807199@N00/46022914714
   - Original: the Flickr page's download menu (I didn't take a static URL)
   - Credit: "mliu92, CC BY-SA 2.0" (Flickr username only; no real name given)
   - License: CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0 (read on the photo page)
   - Taken: 4 January 2019
   - Shows: catenary poles going up on the corridor. **Old** (construction stage), but it shows the
     corridor itself. Not visually confirmed. The Commons category with more of these is
     https://commons.wikimedia.org/wiki/Category:Electrification_of_Caltrain
- Diridon photos (see diridon-station) work for the San José end.

### 2. Public-domain government images
- None found for the Bay Area section. The Commons CAHSR category holds Central Valley construction
  photos, which are the wrong place for this project.

### 3. Press kits with stated permission
- None verified. The Authority's newsroom/press kit may state "free for public use" (2019 release),
  but hsr.ca.gov blocked automated access and I couldn't read the terms (see the header).

### 4. Permission leads
- **California High-Speed Rail Authority**, owner of the San Francisco, Millbrae and Brisbane
  light-maintenance-facility renderings in the 2022 Final EIR/EIS. Newsroom:
  https://hsr.ca.gov/communications-outreach/newsroom/ ; general contact info@hsr.ca.gov. Ask
  whether the newsroom's "free for public use" policy covers renderings, and get it in writing.

### 5. Official render pages to link
- https://hsr.ca.gov/high-speed-rail-in-california/project-sections/san-francisco-to-san-jose/
  (already in officialLinks; I couldn't open it because of the bot wall)
- https://hsr.ca.gov/project-overview/project-sections/northern-california/ (already in officialLinks)

---

## bart-silicon-valley-phase-2 (BART Silicon Valley Phase II, San Jose and Santa Clara)

### 1. Openly licensed photos

1. **Proposed BART yard site in San Jose, October 2017** (best: the Newhall Yard site)
   - Page: https://commons.wikimedia.org/wiki/File:Proposed_BART_yard_site_in_San_Jose,_October_2017.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/5/50/Proposed_BART_yard_site_in_San_Jose%2C_October_2017.jpg
     (4320 × 2433)
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL), https://creativecommons.org/licenses/by-sa/3.0
   - Taken: 29 October 2017
   - Shows (caption): "Former Newhall Yard in San Jose and Santa Clara, proposed for a BART yard,
     photographed from Caltrain". **Old**: early works are now under way nearby, and this predates
     them. More files may be in https://commons.wikimedia.org/wiki/Category:Newhall_Yard_(BART)
2. **Caltrain 923 at Santa Clara, Dec 2024, with BART expansion signs** (the Santa Clara station end)
   - Page: https://commons.wikimedia.org/wiki/File:Caltrain_923,_MPI_MP36_at_Santa_Clara,_Dec_2024_%E2%80%93_front_view_with_BART_expansion_signs.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/f/fd/Caltrain_923%2C_MPI_MP36_at_Santa_Clara%2C_Dec_2024_%E2%80%93_front_view_with_BART_expansion_signs.jpg
     (4080 × 3072)
   - Credit: "Mliu92, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 4 December 2024
   - Shows (caption): a Caltrain locomotive at Santa Clara station, "showing BART Silicon Valley Phase
     2 expansion signs applied to fence in background". **Current.** The locomotive dominates, so the
     BART part is small.
3. **Santa Clara (downtown SJ) station SB in May 2026** (Santa Clara Street, over the future
   Downtown San José BART station)
   - Page: https://commons.wikimedia.org/wiki/File:Santa_Clara_(downtown_SJ)_station_SB_in_May_2026.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/f/fc/Santa_Clara_%28downtown_SJ%29_station_SB_in_May_2026.jpg
     (5712 × 4284)
   - Credit: "Evan0512, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 24 May 2026
   - Shows: the VTA light-rail stop on Santa Clara Street with a train and a bus. **Current.** It's a
     street scene, not the BART work. Use it only if a "the street the tunnel runs under" caption fits.
- No photo of the tunnel launch site or of early works found.

### 2. Public-domain government images
- None found. (FTA hasn't put any site photos on Commons.)

### 3. Press kits with stated permission
- None. VTA's photo library states no terms, and the site is "All rights reserved" (see the header).
- A caution: Commons hosts "Rendering of Diridon BART Station.jpg"
  (https://commons.wikimedia.org/wiki/File:Rendering_of_Diridon_BART_Station.jpg, 933 × 418, author
  VTA, 2023, source https://www.vta.org/projects/bart-sv/phase-ii/diridon-station). It's tagged
  `{{PD-California}}`, an uploader's claim that California local-government records are public
  domain. That conflicts with the brief's rule that state and city works aren't automatically PD, and
  with VTA's "All rights reserved" footer, and it's a rendering. **Don't use it** without VTA's
  permission.

### 4. Permission leads
- **VTA** owns the station renderings (the design team for the stations is credited on VTA's pages; I
  didn't verify the names). Media Relations: media.relations@vta.org, (408) 464-7810. Project
  inbox: vtabart@vtabsv.com (listed on https://www.vta.org/projects/bart-sv/phase-ii).

### 5. Official render pages to link
- https://www.vta.org/bart/station-aesthetics (station renderings; better than the officialLinks for
  "see the renderings")
- https://www.vta.org/projects/bart-sv/phase-ii (already in officialLinks)

---

## diridon-station (Diridon Station redevelopment, San Jose)

### 1. Openly licensed photos

1. **San Jose Diridon station, November 2019** (best: the 1935 station building the plan rebuilds
   around)
   - Page: https://commons.wikimedia.org/wiki/File:San_Jose_Diridon_station,_November_2019.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/5/5d/San_Jose_Diridon_station%2C_November_2019.JPG
     (4840 × 3458)
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL), https://creativecommons.org/licenses/by-sa/3.0
   - Taken: 29 November 2019
   - Shows: "San Jose Diridon station in November 2019". **Current** (the building is unchanged).
2. **Diridon Station aerial** (the whole station and rail yard)
   - Page: https://commons.wikimedia.org/wiki/File:Diridon_Station_aerial.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/5/58/Diridon_Station_aerial.jpg
     (2102 × 1288)
   - Credit: "Dicklyon, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 25 April 2018
   - Shows: "Aerial view of San Jose's Diridon station and vicinity, on approach to SJC". **Old-ish**
     (before electrification, and the Google Downtown West site around it has changed).
3. **San Jose Diridon tracks 2 and 3 facing north, 2026-04-17** (the platforms)
   - Page: https://commons.wikimedia.org/wiki/File:San_Jose_Diridon_tracks_2_and_3_facing_north_20260417.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/7/70/San_Jose_Diridon_tracks_2_and_3_facing_north_20260417.jpg
     (5712 × 4284)
   - Credit: "Evan0512, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 17 April 2026
   - Shows: the tracks 2/3 platform with an ACE train. **Current.**
- More: https://commons.wikimedia.org/wiki/Category:San_Jose_Diridon_station (about 30 files,
  including Southern Pacific depot details from 2012).

### 2. Public-domain government images
- None found.

### 3. Press kits with stated permission
- None.

### 4. Permission leads
- The renderings (at-grade concourse, Cahill plaza, The Alameda crossing) are on diridonsj.org,
  which is run by the City of San José for the five partners (Caltrain, City of San José, VTA, CAHSR,
  MTC). Media contact: Colin Heyne, City of San José Department of Transportation, Public
  Information Manager, colin.heyne@sanjoseca.gov. Planning contact: Eric Eidlin, Station Planning
  Manager, eric.eidlin@sanjoseca.gov (https://www.diridonsj.org/contact). The renderings aren't
  credited to an architect on the page. Ask who holds the rights.

### 5. Official render pages to link
- https://www.diridonsj.org/ (already in officialLinks; shows the at-grade station renderings)
- https://www.diridonsj.org/disc (Diridon Integrated Station Concept page)

---

## valley-link (Valley Link, Dublin, Pleasanton and Livermore)

### 1. Openly licensed photos
Valley Link starts at the Dublin/Pleasanton BART station and runs east in the I-580 median.

1. **Dublin Pleasanton station from garage, May 2018** (best: the BART terminus and the I-580 median)
   - Page: https://commons.wikimedia.org/wiki/File:Dublin_Pleasanton_station_from_garage,_May_2018.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/2/28/Dublin_Pleasanton_station_from_garage%2C_May_2018.JPG
     (5184 × 3462)
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL), https://creativecommons.org/licenses/by-sa/3.0
   - Taken: 10 May 2018
   - Shows: "Dublin/Pleasanton station from the parking garage". **Current-ish.** Not visually
     confirmed. Check that the median tracks, where Valley Link would connect, are in frame.
2. **East Dublin – Pleasanton BART station 2539 14** (no credit needed)
   - Page: https://commons.wikimedia.org/wiki/File:East_Dublin_-_Pleasanton_BART_station_2539_14.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/9/94/East_Dublin_-_Pleasanton_BART_station_2539_14.JPG
     (2048 × 1536)
   - Credit: "Pedro Xing, CC0, via Wikimedia Commons" (not required)
   - License: CC0 1.0, http://creativecommons.org/publicdomain/zero/1.0/deed.en
   - Taken: 20 October 2012
   - Shows: the Dublin/Pleasanton station. **Old** (2012). Fifteen more frames from the same visit are
     in https://commons.wikimedia.org/wiki/Category:Dublin/Pleasanton_station
3. **Dublin-Pleasanton BART station transit center (October 2023)**
   - Page: https://commons.wikimedia.org/wiki/File:Dublin-Pleasanton_BART_station_transit_center_(October_2023).jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/c/c8/Dublin-Pleasanton_BART_station_transit_center_%28October_2023%29.jpg
   - Credit: "Evan0512, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 14 October 2023
   - Shows: buses at the station's transit center, including a San Joaquin RTD commuter bus. **Current.**
- Not found: Isabel Avenue or Vasco Road station sites, or the I-580 median east of the BART tail
  tracks. The Isabel geosearch returned only Costco and parking-lot photos.

### 2. Public-domain government images
- None found.

### 3. Press kits with stated permission
- None. valleylinkrail.com has no media page or usage terms.

### 4. Permission leads
- **Tri-Valley–San Joaquin Valley Regional Rail Authority**. Its project page shows maps and diagrams
  only, with no station renderings. Contact form: https://www.valleylinkrail.com/contact-us. Search
  results from CEQA filings name Candice Kendall, ckendall@valleylinkrail.com, (925) 453-1600 (2024
  filing), and an office at 2600 Kitty Hawk Road, Suite 103, Livermore (unverified on the authority's
  own site). Renderings, if any exist, are likely in the EIR documents on CEQAnet (SCH 2018092027).

### 5. Official render pages to link
- https://www.valleylinkrail.com/valleylink-project (already in officialLinks; maps only)
- No official rendering page found.

---

## smart-healdsburg (SMART Healdsburg extension, Windsor and Healdsburg)

### 1. Openly licensed photos

1. **NWP bridge in Healdsburg, July 2022** (best: the Russian River rail bridge the project replaces)
   - Page: https://commons.wikimedia.org/wiki/File:NWP_bridge_in_Healdsburg,_July_2022.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/8/8c/NWP_bridge_in_Healdsburg%2C_July_2022.JPG
     (5184 × 3457)
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 21 July 2022
   - Shows (caption): "The former Northwestern Pacific Railroad bridge over the Russian River in
     Healdsburg". **Current** until the replacement is built. Related frames: "Main span of NWP bridge
     in Healdsburg, July 2022.JPG" (same license and date, checked), plus "Middle span…" and "West
     abutment…" (found through Openverse, not separately checked).
2. **Old and new Healdsburg stations, July 2022** (the depot area, one of the two station sites under
   consideration)
   - Page: https://commons.wikimedia.org/wiki/File:Old_and_new_Healdsburg_stations,_July_2022.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/0/0e/Old_and_new_Healdsburg_stations%2C_July_2022.JPG
     (5024 × 3766)
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 21 July 2022
   - Shows: "The two Healdsburg station buildings - the 1891 structure at left, and the 1928 structure
     at right". **Current.** The station location is being reconsidered (Depot/Hudson or Vine/West
     Plaza/Downtown), so caption it as the historic depot, not "the new station site".
3. **Healdsburg station from the west, July 2022**
   - Page: https://commons.wikimedia.org/wiki/File:Healdsburg_station_from_the_west,_July_2022.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/b/b1/Healdsburg_station_from_the_west%2C_July_2022.JPG
     (5184 × 3888)
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 21 July 2022
   - Shows: "The newer Healdsburg station, built in 1928". **Current.**
- Also: "Northbound SMART train approaching Windsor station, July 2025" and others from the same
  set (Pi.1415926535, CC BY-SA 4.0 per Openverse; not separately checked), for the Windsor end of
  the extension.

### 2. Public-domain government images
- None found.

### 3. Press kits with stated permission
- None.

### 4. Permission leads
- **SMART** owns the two station-location renderings on
  https://www.sonomamarintrain.org/healdsburgstationlocation (Depot/Hudson and Vine/West Plaza/Downtown;
  the files are `DepotHudsonSt_8x10.5.jpg` and `DowntownWPlaza_8x10.5.jpg` on sonomamarintrain.org).
  Contact: Allison Mattioli, amattioli@sonomamarintrain.org, (707) 285-8248; or Julia Gonzalez,
  jgonzalez@sonomamarintrain.org.

### 5. Official render pages to link
- https://www.sonomamarintrain.org/healdsburgstationlocation (already in officialLinks; renderings of
  both station options)
- https://www.sonomamarintrain.org/healdsburgextension (already in officialLinks)

---

## smart-cloverdale (SMART Cloverdale extension, Healdsburg, Geyserville and Cloverdale)

### 1. Openly licensed photos

1. **Cloverdale station from the northeast, July 2022** (best: the existing, never-used rail station
   at Cloverdale)
   - Page: https://commons.wikimedia.org/wiki/File:Cloverdale_station_from_the_northeast,_July_2022.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/8/8f/Cloverdale_station_from_the_northeast%2C_July_2022.JPG
     (5184 × 3888)
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 21 July 2022
   - Shows: "Cloverdale station in July 2022". **Current.** **Confirm** that SMART's planned Cloverdale
     station is this site before captioning it as the station site. I didn't verify it against a SMART
     document.
2. **Unused platform at Cloverdale station, July 2022**
   - Page: https://commons.wikimedia.org/wiki/File:Unused_platform_at_Cloverdale_station,_July_2022.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/d/d4/Unused_platform_at_Cloverdale_station%2C_July_2022.JPG
     (5184 × 3888)
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 21 July 2022
   - Shows: "The never-used railroad platform at Cloverdale station". **Current.** It tells the "track
     waiting for trains" story well.
3. **Cloverdale Depot**
   - Page: https://commons.wikimedia.org/wiki/File:Cloverdale_Depot.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/6/61/Cloverdale_Depot.jpg (3223 × 2045)
   - Credit: "Mjdestroyerofworlds, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 12 August 2021
   - Shows: "Cloverdale Depot seen from Asti Road". **Current-ish.** Not visually confirmed.
- Geyserville: none found. The geosearch returned only the school, a house and the old hotel, nothing
  of the rail line or the adopted station site.

### 2. Public-domain government images
- None found.

### 3. Press kits with stated permission
- None.

### 4. Permission leads
- **SMART** owns the Geyserville station rendering:
  https://www.sonomamarintrain.org/sites/default/files/Document%20Library/SMART%20Geyserville%20%20Station%20Rendering.pdf
  (linked from the Geyserville page). Contact: Allison Mattioli, amattioli@sonomamarintrain.org.

### 5. Official render pages to link
- https://www.sonomamarintrain.org/geyserville (already in officialLinks; links the station rendering)

---

## mission-bay-ferry-landing (Mission Bay Ferry Landing, San Francisco)

### 1. Openly licensed photos

1. **Remains of SP freight pier off 16th Street, October 2020** (best: the landing site, **seen**)
   - Page: https://commons.wikimedia.org/wiki/File:Remains_of_SP_freight_pier_off_16th_Street,_October_2020.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/1/16/Remains_of_SP_freight_pier_off_16th_Street%2C_October_2020.JPG
     (5184 × 3888)
   - Credit: "Pi.1415926535, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0 (also GFDL), https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 4 October 2020. The camera is about 90 m from the centroid of the traced boundary.
   - Shows (seen): the rusting timber-and-steel remnant of the Southern Pacific freight pier standing
     in the bay off the foot of 16th Street, with the Bay Bridge and Oakland's cranes behind. A clean,
     calm frame. **Current** until construction (the contract was awarded July 2026). Check the final
     MND for whether these remnants are removed; I didn't read it for that.
2. **Agua Vista Park Public Fishing Pier**
   - Page: https://commons.wikimedia.org/wiki/File:Agua_Vista_Park_Public_Fishing_Pier.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/b/b2/Agua_Vista_Park_Public_Fishing_Pier.jpg
     (4032 × 3024)
   - Credit: "Lovelano, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 27 August 2023. It's about 120 m from the boundary centroid, beside the landing site.
   - Shows: the fishing pier at Agua Vista Park on Terry A. Francois Boulevard. **Current.** Not
     visually confirmed.
3. **Pier 52 ferry slip** (Flickr; low priority)
   - Page: https://www.flickr.com/photos/22359271@N04/32881930820 (eleven more frames in the same set)
   - Credit: "Morten Jensen, CC BY 2.0"
   - License: CC BY 2.0, https://creativecommons.org/licenses/by/2.0 (read on the photo page)
   - Taken: 1 August 2016. Not geotagged.
   - Shows (caption): "The old ferry slip at pier 52 in San Francisco." **I couldn't confirm** how
     close Pier 52 is to the 16th Street landing. Use only after checking the location.

### 2. Public-domain government images
- None found.

### 3. Press kits with stated permission
- None. WETA's media kit states no license (see the header).

### 4. Permission leads
- **Port of San Francisco** (sponsor; the aerial rendering on its page). Project manager: Simon
  Betsalel, simon.betsalel@sfport.com. Port press: media@sfport.com (unverified).
- **WETA / San Francisco Bay Ferry** (project page image `Mission-bay-ferry-landing.jpg`; the charging
  float). Media@sanfranciscobayferry.com.

### 5. Official render pages to link
- https://sfport.com/mission-bay-ferry-landing (Port page with the "Mission Bay Ferry Landing Aerial
  View" rendering; better than officialLinks for renderings)
- https://www.sfbayferry.com/project/mission-bay-ferry-landing/ (already in officialLinks)

---

## berkeley-pier-ferry (Berkeley Pier and ferry terminal)

### 1. Openly licensed photos
The pier closed in 2015 and is now in disrepair, so pre-2015 photos show it open and post-2015
photos show it fenced off.

1. **Berkeley pier** (Flickr, 2020; best recent view of the closed pier)
   - Page: https://www.flickr.com/photos/74486811@N00/52315327725
   - Original: the Flickr page's download menu
   - Credit: "Eric (eb78), CC BY 2.0"
   - License: CC BY 2.0, https://creativecommons.org/licenses/by/2.0 (read on the photo page)
   - Taken: 29 January 2020. Geotagged 37.860963, −122.32418, about 500 m out along the pier from the
     shore.
   - Shows: the Berkeley Pier. **Current** (closed condition). Not visually confirmed, because Flickr
     rate-limited the preview.
2. **Berkeley Pier Blue Hour** (Flickr, 2020)
   - Page: https://www.flickr.com/photos/42914481@N00/50771323468
   - Credit: "David Abercrombie (albategnius), CC BY-SA 2.0"
   - License: CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0 (read on the photo page)
   - Taken: 27 December 2020, from Shorebird Park (geotagged 37.862064, −122.317142)
   - Shows (caption): "Mount Tamalpais and Angel Island float above the Berkeley Pier in this twilight
     view from Berkeley's Shorebird Park. This pier is now in disrepair…" **Current.** Not visually
     confirmed.
3. **Berkeley pier old part 3308** (Commons; the abandoned outer section)
   - Page: https://commons.wikimedia.org/wiki/File:Berkeley_pier_old_part_3308.jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/3/38/Berkeley_pier_old_part_3308.jpg
     (3300 × 2205)
   - Credit: "Amatulic, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0, https://creativecommons.org/licenses/by-sa/3.0
   - Taken: 8 March 2014
   - Shows: "Inaccessible portion of the Berkeley pier with the Golden Gate bridge in the background".
     These are the pilings of the original 1926 three-mile pier. **Old** but unchanged in substance.
- Also: "Berkeley Pier and Golden Gate Bridge aerial" (Dicklyon, CC BY-SA 4.0, 21 February 2018,
  933 × 1096: small; https://commons.wikimedia.org/wiki/File:Berkeley_Pier_and_Golden_Gate_Bridge_aerial.jpg).
  It's an aerial with the pier in the foreground, good for a sense of its length. And Flickr "Old
  Berkeley Pier remnants in Bay" (Hitchster, CC BY 2.0, 9 August 2008,
  https://www.flickr.com/photos/15786211@N00/2747416303), which is old.

### 2. Public-domain government images
- None found.

### 3. Press kits with stated permission
- None.

### 4. Permission leads
- **City of Berkeley** owns the two "Illustrative rendering" images on the project page
  (`img_PierFerry_conceptual-design1.jpg`, "Illustrative rendering of entry to Berkeley Pier", and
  `img_PierFerry_perspective-view.jpg`, "Illustrative rendering of Berkeley Pier"). Project manager:
  LMcNulty@berkeleyca.gov. The page doesn't credit the consultant who drew them; the feasibility
  studies linked there name the consultant teams.
- **WETA** has a rendering on its project page (`Berkeley-Rendering.jpg`):
  Media@sanfranciscobayferry.com.

### 5. Official render pages to link
- https://berkeleyca.gov/node/9711 (already in officialLinks; renderings in its image carousel)
- https://www.sfbayferry.com/project/berkeley-ferry-project/ (already in officialLinks)

---

## redwood-city-ferry-terminal (Redwood City ferry terminal)

### 1. Openly licensed photos

1. **Aerial view of Pacific Shores, September 2019** (best recent aerial; the port is in frame)
   - Page: https://commons.wikimedia.org/wiki/File:Aerial_view_of_Pacific_Shores,_September_2019.JPG
   - Original: https://upload.wikimedia.org/wikipedia/commons/b/b9/Aerial_view_of_Pacific_Shores%2C_September_2019.JPG
     (5184 × 3888)
   - Credit: "Pi.1415926535, CC BY-SA 3.0, via Wikimedia Commons"
   - License: CC BY-SA 3.0 (also GFDL), https://creativecommons.org/licenses/by-sa/3.0
   - Taken: 17 September 2019
   - Shows: "Aerial view of the Pacific Shore development in Redwood City". It's filed in the Port of
     Redwood City category. **Confirm** that the terminal site (the port's wharf near Seaport
     Boulevard) is in frame. Not visually confirmed.
2. **Valhalla Dredging Port of Redwood City (01 of 22)**
   - Page: https://commons.wikimedia.org/wiki/File:Valhalla_Dredging_Port_of_Redwood_City(01_of_22).jpg
   - Original: https://upload.wikimedia.org/wikipedia/commons/2/2c/Valhalla_Dredging_Port_of_Redwood_City%2801_of_22%29.jpg
     (3264 × 2448)
   - Credit: "Jeanjung212, CC BY-SA 4.0, via Wikimedia Commons"
   - License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0
   - Taken: 1 December 2016
   - Shows: "Valhalla dredging Redwood Creek at the Port of Redwood City to maintain and increase depth
     for cargo ships". It shows the working port channel, not the terminal site itself. Twenty-one more
     frames in the set. Not visually confirmed.
- Flickr leads I checked but rank low: "Redwood City Seaport" (profernity, CC BY 2.0, 2014;
  geotagged about 2 km from the site, at the Docktown/Seaport area) and "Port of Redwood City"
  (bgwashburn, CC BY 2.0, 2019; a distant view from Edgewood Preserve).

### 2. Public-domain government images
- **Redwood City port aerial view** (US Army Corps of Engineers; **seen**)
  - Page: https://commons.wikimedia.org/wiki/File:Redwood_City_port_aerial_view.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/b/bb/Redwood_City_port_aerial_view.jpg
    (1500 × 1000)
  - Credit: "U.S. Army Corps of Engineers, public domain, via Wikimedia Commons"
  - PD basis: `{{PD-US Army USACE}}`, work of the US federal government. Source: USACE Digital Visual
    Library.
  - Date: not given. The Pacific Shores office campus is built, so it's roughly 2000s. **Old.**
  - Shows (seen): an oblique aerial looking along Redwood Creek to the bay, with marinas, the Pacific
    Shores campus, salt ponds, and the port's deepwater terminal at right. It's the best overall
    picture of where the terminal goes, but it's small and dated.

### 3. Press kits with stated permission
- None.

### 4. Permission leads
- **Port of Redwood City** (lead agency). The "Ferry Terminal Concept" and "Ferry Terminal Sheet"
  PDFs are linked from https://www.redwoodcityport.com/ferry. Contact: info@redwoodcityport.com,
  (650) 306-4150. The CEQA record (SCH 2024041306) names project manager Don Snaman (found through
  search; address not verified on the Port's site).
- **WETA**: Media@sanfranciscobayferry.com.

### 5. Official render pages to link
- https://www.redwoodcityport.com/ferry (Port project page with the concept PDFs; better than the
  CEQAnet link in officialLinks)
- https://www.sfbayferry.com/project/redwood-city-ferry-study/ (already in officialLinks; I saw no
  rendering on it)
