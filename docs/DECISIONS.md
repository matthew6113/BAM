# Decisions

Choices that shape the map, in the order they were made. The evidence is in
`docs/PLANNING-AUDIT.md`. Newest last.

## 2026-10-01: build plan (approved by Matthew: "continue with all per recommendations")

**Stack**
- Vite + TypeScript + Preact for the UI.
- MapLibre GL JS 6 + PMTiles for the map.
- A Python (uv) and Tippecanoe 2.79 pipeline for the data.
- Playwright for screenshots.
- No deck.gl, because its interleaved mode crashes on MapLibre 6.

**Base data:** the Overture Maps release is pinned to `2026-09-23.1`.
- Buildings, water, counties, city points and context lines all come from Overture.
- The pipeline reads Overture with pyarrow. DuckDB is not used because its extensions are blocked in the build sandbox, and third-party copies are not trusted.

**Building heights:** only mapped (OpenStreetMap, Esri) or measured (USGS lidar) heights are kept. Microsoft's ML estimates are dropped, so 1,021,947 buildings stay flat, along with the ones that never had a height. 1,003,219 of 2,547,306 buildings have a height.

**Data corrections:** the three approved corrections are applied and logged in CHANGELOG.md:
- Potrero's stack is concrete, not brick.
- Potrero's acreage note now cites the Draft EIR.
- Mission Bay's unsourced figures are held out of the map.

**Parcels:** used only as tracing references, never shown, with each county's license checked before use.

**Network:** sfplanning.org and data.sfgov.org are needed before Milestone 2. They are blocked in the build environment.

## 2026-10-01: Milestone 1 defaults (open for Matthew's review)

**Default view:** frames every project's approximate center, not the full nine counties. Panning is limited to the nine counties plus a margin.

**Buildings below zoom 13:**
- "Every building" tiles (80 MB archive): no tile size limit, with Tippecanoe's tiny-polygon reduction keeping density.
- "Lighter" tiles (20 MB) drop too many buildings in the cores. They stay available as an option only.

**Building opacity:**
- The regional ramp starts at 60% at zoom 8 and reaches the spec's 85% at zoom 13.
- Flat 85% is the alternative.
- Both are in the theme (`opacity.buildingsRegional`, `opacity.buildings`).

**Land outside the nine counties:** a faint tint (`outsideRegion`) explains why the buildings stop at the county line.

**Salt ponds:** drawn as water. The toggle changes little, because most South Bay ponds are already mapped as water and the large white areas are tidal marsh.

**Context lines:** freeways, rail and ferries are off by default, as the spec says they are optional. (Superseded 2026-10-02: on by default.)

**Style panel:** on in development, or with `?style=1` in any build. The shortcut is Alt+Shift+S, not a bare "S", per WCAG 2.1.4.

**3D toggle:** 3D tilts the map and shows faint context massing (theme `contextExtrusion`) for buildings with real heights at zoom 14 and above. 2D is flat with tilt and rotate disabled.

**"Partly built" placeholder:** `#5A6B8C`. The spec has no color for this stage.

## 2026-10-02: context lines and hosting (Matthew)

**Context lines are on by default.** Matthew asked to keep the railroads and freeways. The layer now draws:
- Freeways (OSM motorways) and highways (trunk roads). On- and off-ramps appear from zoom 12.
- Railroads: transit (BART, Muni, VTA, cable cars, SFO AirTrain) and every active standard-gauge line (Caltrain, SMART, Union Pacific and BNSF track). Named lines and stretches over 1 km show from the regional view; unnamed yards and spurs only up close.
- Ferry routes.
- Left out: narrow-gauge, funicular and "unknown" track.

**Hosting:** GitHub Pages, with the repository made public.
- **Deploys:** every push to main via `.github/workflows/deploy.yml`.
- **Address:** the site is served from `/BAM/`.
- **Tile files:** street-level building tiles are split into one archive per zoom (13, 14, 15) so no file exceeds 100 MB.
- **Archive:** the Overture extract is kept as a GitHub release asset, so builds keep working after Overture removes the release.
- **Tiles on object storage:** still possible later through `VITE_TILE_BASE_URL`.

## 2026-10-02: Milestone 2, Potrero Power Station (open for Matthew's review)

**Source for the blocks: the approved Design for Development (2026-10-03).** Matthew asked for the D4D's height plan to be traced (2026-10-03). This replaces the 2018 Draft EIR blocks, which were dropped on 2026-10-02 as superseded.
- The site boundary and five sub-areas are still traced from DEIR Figure 2-2 (vector shapes, 13 street intersections, RMS 3.4 m), 29.1 acres.
- Blocks come from D4D Figure 6.2.3, Building Height Plan (p. 245). The legend's 85 and 125 ft fills are spot colours that PDF parsers can't read, so the page is rendered at 200 dpi and each block's pixels are classified against the legend; labels and dimension lines printed on the fills take the colour of the nearest fill.
- Georeferenced on seven street intersections measured from the figure's curb lines, including Phase 1 streets now in OpenStreetMap (Maryland, Humboldt): RMS 2.0 m. Registering the figure's dash-dot site line to the 2018 boundary failed (the two boundaries differ), so it isn't used.
- Each block is a solid to its height limit, labelled "Illustrative massing": the limits are an envelope, not building designs. "180'/85'" tower zones (Blocks 1, 5, 7) are an 85-ft solid with a faint envelope to 180, 220 or 240 ft. "MAX" dimensions in the figure are plan lengths and aren't used.
- Block 9 is a dashed outline: the D4D gives two configurations, with or without Unit 3.
- Every block is "entitled". The Sophie Maxwell Building (DBI permit complete Aug 28, 2026) is cut out of Block 7 and left to the base map; UCSF's Block 2 building has no official construction record yet.
- The 2026 amendments (Addendum 2: +8 ft on residential blocks and more on Blocks 1, 5, 11, 12, 15) aren't drawn until the Board adopts them.
- The stack is 300 ft (DEIR pp. 2-7, 4.D-8) on its OpenStreetMap footprint.

**Fly-in:** 4.5 s flight (`flyTo`, ease in and out), the boundary drawing itself from 35% to 90% of it; then the surroundings within 700 m extrude faintly (0.8 s fade) and the blocks rise over 1.2 s, staggered outward over 0.6 s. Escape, close or back flies back over 3 s to where the viewer was, in the mode (2D or 3D) they were in. Reduced motion: a 160 ms dip to paper, a jump, and no rise.

**Landing camera:** from the south-southwest (bearing -30), pitch 58, zoom 16.4 for a 1440 x 900 window with the panel; smaller views zoom out to keep the site in frame. Option shown: from the southeast.

**Massing opacity by stage (theme `massing.opacity`):** entitled 0.5 (the spec's "light fill"), under construction 0.92, complete 0.95 in ink. Option shown: entitled at 0.78.

**Panel:** 400 px on the right; a bottom sheet over the lower half below 720 px. The caveats (illustrative massing, approximate boundary, with the source link) sit right under the stage bar. Numbers are shown only as stored, so the affordable share stays a percentage. Renderings: none with permission yet, so the official pages are linked.

**Projects list:** a small "Projects" disclosure under the title is the keyboard route in until the Milestone 3 index.

**Deep links:** `/p/{id}`. The build writes `p/{id}/index.html` (with the project's title and summary) and `404.html`, since Pages has no rewrites.

## 2026-10-02: official sources only (Matthew)

Matthew: "I want only official." What it means here:
- **Sources:** every fact shown traces to a public agency or body: adopted plans, hearing minutes, permits, official GIS, the published code. A test enforces this for mapped projects (`src/projects/official.ts`).
- **Press-only facts** move to the project's `reported` record, which the map never shows. For Potrero that is the 2025–26 construction and opening dates, the 2026 amendment request, the "Fifth Space" name and the 30% affordable share. The panel says that reported details are held back.
- **Potrero's stage** is "entitled" until official records (permits, UCSF, the Mayor's Office of Housing) confirm construction and the completed building. Press reports put it at "partly built".
- **Potrero's blocks:** the 2018 Draft EIR blocks are superseded and are not drawn. The map shows the traced site boundary and the 300-ft stack only. The approved block heights come from the Design for Development once it can be read. The Planning Commission minutes of Jan 30, 2020 confirm the approved range for new buildings: 65 to 240 ft.
- **Unmapped projects:** they don't open from a deep link. Their records haven't been checked against official sources yet.
- **Network:** Matthew is broadening the environment's network access so the official sites (sfplanning.org, data.sfgov.org, the code, CEQAnet, UC Regents) can be read.


## Milestone 3 (2026-10-03)

**Boundaries from official GIS first.** 20 projects take their site from a layer their city or
county publishes (special use district, redevelopment area, height district, specific plan
boundary, planned development zoning, or the parcels named in the approval), fetched and
unioned by `make sites`. Where the layer is a proxy, the boundary is labelled approximate:
North Bayshore (approval parcels, which the plan only partly covers), Brisbane Baylands (the
city's draft boundary layer), Downtown West (net zoning acres, 58 of 80 gross) and Brooklyn Basin
(development parcels only, without the parks). Willow Village, Concord, Alameda Point and the
Suisun expansion have no usable layer and are traced from official figures.

**One control is both legend and filter.** The index shows each stage with its colour and count;
pressing a stage hides it from the list and the map. Search (name, aliases, city, county) and an
area select narrow it further. The same filter hides markers, sites and labels on the map, so
the legend always describes what is drawn. Labels stay sparse: the legend lives in the index,
not on the map.

**Records applied when mapped.** As each project went on the map its record was rewritten from
its findings file (official values only; press facts in `reported`), and the official-sources
test now covers it.

**Traced boundaries (four projects without a usable layer).** Willow Village is plotted from its
development agreement's legal description (13 courses, closes to 0.006 ft, 59.17 acres) and placed
on Menlo Park's parcel lines; the Hamilton Avenue parcels in a separate exhibit aren't included.
Concord is the Navy's EDC property map, read from its vector fills and fitted to OpenStreetMap
roads (scale within 0.1% of the map's bar). Alameda Point is the 2022 Site A plan's parcel diagram
on 8 street intersections. The Suisun annexation area is traced from a small raster figure and
labelled approximate (about 30 m). See `pipeline/bam_pipeline/sites/traced_boundaries.py`.

## 2026-10-03 to 10-05: Milestone 4 massing calls (Matthew)

**Piers 30–32 removed** from the map (2026-10-03); listed under `_meta.dropped`.

**Mission Rock H/I/J** stay drawn as a 90-ft podium with a 120-ft envelope (2026-10-05).

**When two official documents disagree, the more recent one wins** (2026-10-05). Downtown West's
block E1 is drawn at the approved Development Agreement's 260 ft (June 2021), not the October 2020
draft design standards' 280 ft. The other Downtown West heights still come from that draft, since
the approved 2021 standards couldn't be retrieved; they are labelled as such and flagged in the
record's `verify` list.

## 2026-10-07: overview look, option E (Matthew)

Chosen from five options (current, soft ink, knockout halos, both, warm paper with both).
The problem: at zooms 10 to 12 the city cores were near-black, and the darker stage dots
(partly built, under construction) disappeared into them.

**Warm paper.** Land `#FBFAF6`, outside the region `#F2F0EA`, water `#E3E8EA`, shoreline
`#9CA6AE`, buildings `#3A3631`, labels `#3A3835`. Still placeholders until Matthew's palette.
The previous cool white colors are kept as the "Cool white (before Oct 7)" preset.

**Soft ink until street level.** Overview buildings ramp 22% (zoom 8) to 45% (zoom 12.5),
then full ink (85%) at zoom 13, where the detail tiles take over. Theme keys
`opacity.buildingsRegional`, `opacity.buildingsCity`, `opacity.buildings`.

**Bigger dots with knockout halos.** Markers are 5 to 8.5 px with a 2 px land-colored ring, over
a soft land-colored halo that clears the building ink around each dot. Both fade out with the
markers between zoom 12 and 13.

Still open: SF's dots overlap at the whole-bay zoom; the slate "partly built" color stays close
to grey; UI chips are pure white on the off-white paper.

## 2026-10-07: stage colors, International orange (Matthew)

Chosen from five schemes (bay blue, International orange, bay teal, a hue per stage, night).
Placeholders still, until Matthew's palette; this supersedes the stage table in SPEC section 4.

| Stage | Color |
|---|---|
| Proposed | `#D0612C` |
| Entitlement | `#C04E1C` |
| Entitled | `#A93F12` |
| Infrastructure | `#8C310C` |
| Under construction | `#6C2408` |
| Partly built | `#8C6A55` |
| Complete | the building ink (`@buildings`) |
| Paused | `#4F6E8E` |
| Distressed | `#7A1E4A` |

- Every stage now has at least 3:1 against land and water (the old light blues failed); a test
  enforces it.
- Paused and distressed sit off the orange ramp (slate blue, plum) so they read as exceptions.
- The previous colors and blues are kept as the "Cool white and blue (before Oct 7)" preset;
  presets can now carry stage colors.
- Still open: the selection outline (`#000000`) is under 3:1 against the building ink; adjacent
  orange stages are close on small dots (the panel always names the stage).
