# Planning audit: Bay Area megaprojects map

Oct 1, 2026. This is the detail behind the short build plan in chat. Ten agents produced it. Two measured the data and tooling in this environment. Four reviewed the spec and data, each from a different angle, and four more checked those findings against the files. Findings that didn't hold up are dropped or corrected here. Anything labeled **lead** comes from search-result excerpts only and is not verified.

## 1. What this environment can reach

| Reachable | Blocked |
|---|---|
| Overture Maps on S3, GitHub, npm, PyPI, apt, Google Fonts, `sfplanning.s3.amazonaws.com` (some SF Planning EIR PDFs) | data.sfgov.org, sfplanning.org, county GIS portals, ArcGIS Hub, OSM download servers, census.gov, every news host in `sources`, CEQAnet, amlegal |

Web search works but returns only titles and excerpts. I can't open source articles from here, so I can't verify them.

## 2. Measured base data (Overture release 2026-09-23.1)

**Buildings.** 2,547,306 footprints fall inside the nine counties.

- Source of the footprint shapes: OSM 83.4%, Microsoft ML 14.1%, Esri Community Maps 2.5%.
- Licenses: OSM ODbL; Microsoft ODbL as published by Overture; Esri CC BY 4.0 with OSM waivers.
- 79.5% of buildings have a height. Coverage by county:
  - San Francisco 96%: 86% from OSM, 8% from USGS lidar.
  - Santa Clara 95%.
  - Elsewhere, heights are mostly Microsoft ML estimates, which never exceed 35.8 m.
- At Potrero:
  - "Sophie Maxwell Building" is present by name (OSM w1499496425), with no height.
  - One OSM footprint is exactly 91.44 m (300 ft) tall with an 87 m² footprint (w678950945). It is very likely the stack, but that is unconfirmed.
  - No footprint is named Station A or Unit 3.

**Land and water.** Land polygons come from the OSM coastline, and the Bay is a set of ocean polygons that reach into the Delta (to −121.50).

- Treasure Island, Yerba Buena, Alameda, Bay Farm and Mare Island all test as land.
- Mare Island Strait, Lake Merritt, reservoirs and Delta channels are separate river and lake polygons on top of the land.
- Salt ponds are a mix: 45 `salt_pond` polygons, plus pond and water polygons, over wetland. How to draw them is a decision for you.

**Counties and labels.** All nine county polygons exist. Contra Costa and Solano include bay water, so they must be clipped to land. All 25 city label points exist.

**Rail and ferries.**
- BART is tagged `subway` but is mostly unnamed, so it can only be picked out by class plus location.
- Caltrain, VTA and Muni can be identified by name.
- There are 29 ferry segments.

**Tile size.** Region-wide building tiles measure about 185–220 MB, about 142 MB of it at zooms 13–15. Low-zoom tiles exceed Tippecanoe's per-tile limits unless buildings are dropped or merged.

**Release lifetime.** Overture keeps releases for only about 60 days, so the clipped extract has to be archived for the pipeline to stay reproducible.

## 3. Toolchain tested here

What works:
- Tippecanoe: 2.49 from apt; 2.79.0 builds from source in about 1 minute. It writes PMTiles directly.
- go-pmtiles 1.31.2.
- MapLibre GL JS 6.11.2 and pmtiles 4.5.0 under Vite 8. Two fixes are needed: `import * as maplibregl` and `setWorkerUrl(...?worker&url)`.
- Headless Chromium renders WebGL2 through SwiftShader, so Playwright screenshots work.
- fontnik builds glyph files from Libre Franklin. The variable font's default weight is Thin, so I make static instances first.
- geopandas, shapely and pyarrow, plus the `overturemaps` Python API with a pinned release.

What fails:
- DuckDB's spatial and httpfs extensions are blocked here. The only copies are third-party PyPI repackages, which I won't use.
- deck.gl's interleaved mode crashes on MapLibre 6, because MapLibre removed `map.transform`.

MapLibre facts that shape the design:
- **Extrusion opacity is per layer only.** `fill-extrusion-opacity` can't vary per building, and alpha in `fill-extrusion-color` is ignored.
- **No outlines in 3D.** Line layers can't be raised off the ground, and extrusions have no stroke.
- **Animating heights.** `fill-extrusion-height` accepts feature-state, so per-building rise animation is cheap. Updating a data-driven paint property every frame reloads the source, which is slow.
- **Built-in reduced motion.** MapLibre already turns `flyTo` into an instant jump under `prefers-reduced-motion`.

## 4. Spec: wrong or missing (verified)

**At regional zoom**
1. **Sites are invisible at the default view.** Framing all nine counties lands at about z8 on a 1440×900 screen. A 29-acre site is then about 1.4 px wide, and 23 of 25 sites are still under 24 px at z9. Potrero and Pier 70 are 4.6 px apart at z9. The fix is stage-colored point markers at regional zoom, a cluster for the SF waterfront, polygons from about z12, and tap-to-preview on touch screens. The projects fill only 6.5% of a nine-county frame, so the default camera should frame the projects (about z9), with panning still limited to the nine counties.
2. **"Every building" at regional zoom needs a strategy.** The median footprint is 18 m, which is a fraction of a pixel at z8–z11. I'll show you options side by side in M1.
3. **Suisun dominates the color.** It is 22,873 acres, 77% of all project area, and the least certain project. Plan-scale sites should be outline only at regional zoom.

**Stages and color**
4. **No color for Partly built.** No color role exists for it, yet 7 of 25 projects use it, Potrero included.
5. **Nothing records where a paused or distressed project stalled.** Six projects need it for the stage-bar break. Add a sourced `stalledAt` field, and until it's filled, draw the bar without a stall position.
6. **Placeholder ramp problems.** This is your palette's job, but the theme should check it. Site work (#3459A8) is darker than Entitled even though it's meant to be a "light fill". Under construction (#1E3F86) has almost the same lightness as ink (1.04:1). Proposed (#9DB4E0) is 2.1:1 against white, below the 3:1 minimum for graphics. The selection color #000 is 2:1 against the ink composite.
7. **Missing theme roles:** partly built, context extrusion, hatch and dash patterns, approximate and illustrative styling, land-use zones, hover, and light settings.

**3D and massing**
8. **Outlines and wireframes aren't native to MapLibre 3D.** Options: thin "edge" extrusions with no new dependency, or a translucent ghost plus a dashed ground outline. I'll show both in M2.
9. **Delivered project buildings are already in the base data**, Sophie Maxwell for one. Without a rule to remove them from the base layer where the massing replaces them, they get drawn twice.
10. **Not all base heights are real.** Outside SF and Santa Clara, the heights for "surrounding buildings rise to true heights" are mostly ML estimates, and 20% of buildings have none. I recommend extruding only OSM and lidar heights.

**Data model**
11. **The plan-scale list in the spec doesn't match the data.**
    - Concord's notes say boundary only.
    - Hunters Point Phase 2 and Oakland Coliseum aren't on the list.
    - The fix is a `treatment` field on each project.

**Sharing and hosting**
12. **Deep links and share cards.** I'll prerender `/p/{id}/index.html` with share-card tags for each project. That works on any static host.
13. **Tile hosting.** The tiles need object storage that supports range requests, such as R2 or S3. They are too big for Cloudflare Pages' 25 MiB file limit and too big to commit to git.

**Small fixes**
14. **Style panel shortcut.** A bare "S" key fires while typing in search and fails WCAG 2.1.4. Make the panel dev-only or `?style=1`, with a modifier key.
15. **Reduced motion.** MapLibre already jumps, so the "crossfade" has to be a short fade to the paper color, a jump, then a fade back.

## 5. Data: facts to fix or flag (not changed yet)

**Potrero (the M2 slice)**
- **"Brick stack" is wrong; it's concrete.** The DEIR has "the adjacent 300-foot tall concrete boiler exhaust stack" (printed p. 2-7) and "The reinforced concrete Boiler Stack" (Historic Resources section). Brick describes Station A's Turbine Hall: "a four-story, unreinforced brick structure some 65 feet in height (nearly 80 feet to the peaked rooftop)". The DEIR is at https://sfplanning.s3.amazonaws.com/sfmea/2017-011878ENV_DEIR_Volume_1.pdf.
- **29 vs 21 acres is resolved** by the same DEIR: "approximately 29.0-acre site" made up of "the 21-acre Power Station sub-area, a 4.8-acre PG&E sub-area" and others.
- **Block numbering and heights (lead):** Sophie Maxwell is "Block 7B". Foster + Partners' tower is "Block 7A": 27 stories, 264 ft, 325 units. Block 2 has 8 floors above ground and is about 130 ft tall, but the data says seven stories.
- **Pending amendments (lead):** the Planning Commission recommended amendments in 2026 that change heights. The Board of Supervisors' decision is unknown. Recommendation: trace the 2020 approved Design for Development and label it as such.
- **Missing for the slice:** the block footprints, block heights, block stages and the boundary geometry. The Design for Development is on sfplanning.org, which is blocked here.

**Other projects**
- **Mission Bay:** program.notes says "Approximate figures from general knowledge". Hide those figures until they're sourced.
- **Mission Rock:** heights come from a SkyscraperPage forum thread. The Mission Rock EIR Ch. 2 is reachable here and gives 90–240 ft. Use it instead.
- **Ranges stored as exact numbers:**
  - Brisbane: 1,800–2,200 homes stored as 2200.
  - Concord: "12,000+".
  - Moffett Park: "up to" 20,000 homes and "10M+" sq ft of office.
  - Pier 70: "2,000+".
  - The panel would show an upper bound as a plain fact. Add a qualifier field.
- **Arithmetic that doesn't add up:**
  - Suisun: 15,737 + 5,726 = 21,463, but acres is 22,873.
  - India Basin: 24.5 acres of open space plus a 15-acre private parcel exceeds the 29-acre total.
  - Candlestick and Hunters Point give different decoupling years: late 2024 vs 2025.
- **Willow Village:** the verify list is empty, but outside reports differ on acres, units, hotel rooms and office space (leads).
- **Sources:** all are bare URLs with no field-level mapping. Seven are category or tag pages, one is a staging host (`preview-prod.w.sfchronicle.com`), one is a forum thread and two are Wikipedia. 15 projects have no official link.
- **lastVerified:** it's 2026-10-01 on every record, including ones whose stage note says the status needs verification.
