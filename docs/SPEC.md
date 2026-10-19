# Build spec: Bay Area Megaprojects Map

Owner: Matthew Huguet. Draft 1, October 1, 2026; brought up to date October 17, 2026 with what was
built and decided since (the decisions themselves are in `docs/DECISIONS.md`).

## 1. What we're building

A public, shareable, interactive 3D web map of the Bay Area's largest development
projects. You can pan and zoom the whole region. Clicking a project triggers a slow
fly-in: the camera glides down and tilts toward the site, the site boundary draws itself,
and the proposed buildings rise in place. A panel then shows what the project is, where
it stands in its lifecycle, the key numbers, renderings, and sources.

Audience: urbanists, real estate and land use professionals, potential employers and
collaborators, and curious Bay Area residents. It has to hold up to an expert's scrutiny:
every figure sourced, every approximation labeled.

Design references Matthew chose:
- Structure and 3D: City of Melbourne's Development Activity Model
  (https://www.developmentactivity.melbourne.vic.gov.au/). It shows 3D buildings by
  status (applied, approved, under construction, built) with stage toggles and
  click-for-details.
- Aesthetic: The New York Times, "A Map of Every Building in America"
  (https://www.nytimes.com/interactive/2018/10/12/us/map-of-every-building-in-the-united-states.html).
  Monochrome building footprints and almost no labels; the shape of the city comes
  from the buildings alone.
- Palette: Matthew's own, to be supplied. Until then the map ships a placeholder palette (warm paper
  and International orange, chosen Oct 7, 2026; section 4).

## 2. Visual concept: the present as print, the future in color

- The existing city is drawn like the NYT map: every building footprint in one quiet ink
  tone, flat at regional zoom. Land and water are nearly monochrome. Labels are sparse.
- At regional scale, the projects are the only things with color and height.
- How solid a building looks tracks how certain it is. Proposed buildings are outlines,
  entitled ones get a light fill, buildings under construction a stronger tone, and
  completed ones turn ink, matching the existing city because they've joined it.
- Spend the boldness in one place: the fly-in. Everything else stays calm.

## 3. Lifecycle stages

Stages are defined in `data/projects.json` (`stages`). Each project has one stage. Each
modeled building also carries its own stage, so a partly built project shows delivered
buildings in ink and future ones as outlines.

| Key | Label | Meaning |
|---|---|---|
| proposed | Proposed | Plan announced or application filed; no approvals |
| entitlement | In entitlement | Formal review underway (EIR, specific plan, hearings, land deal) |
| entitled | Entitled | Approvals in hand, no construction |
| infrastructure | Site work | Demolition, remediation, grading, utilities or streets; no vertical buildings |
| construction | Under construction | Vertical construction on at least one building |
| partial | Partly built | Project level only: some buildings delivered, more planned |
| complete | Complete | Built out |
| paused | Paused | Developer or city has halted work; approvals may remain |
| distressed | Distressed | Default, receivership, failed financing or similar |

The panel shows a stage bar that runs from proposed to complete in order. Paused and
distressed appear as a break in the bar at the point where the project stalled.

## 4. Theme and color roles

All colors live in one theme file, `src/theme/theme.json`, exposed as CSS variables and map style
values; swapping in Matthew's palette is a one-file change. The current values are placeholders
(warm paper and International orange, Oct 7, 2026; `docs/DECISIONS.md`), so they aren't repeated
here. The roles:

- Map: land (paper), water, shoreline hairline, land outside the nine counties, existing buildings
  (ink), building heights in 3D, labels, context lines, selection highlight and selected site ground.
- Stages: one color per stage in section 3. Complete points at the buildings ink; proposed sites are
  drawn as a dashed outline with no fill.
- Land use (plan-scale projects): residential, mixed use, office, industrial and the other zones.
- Panel: background, text, rules, and field and filter outlines (`controlBorder`, at least 3:1 on the
  panel; Oct 16, 2026).
- Opacities and per-stage massing opacity ("the more certain, the more solid").

Tests check the palette's contrast (`tests/theme.test.ts`).

Style panel: a hidden panel (Alt+Shift+S, or `?style=1`; always available on the dev server) that
lets Matthew change any color role, switch presets, try type pairings, adjust building height
exaggeration and light direction, and toggle layers. It updates live, and exports and imports the
theme as JSON so a finished palette can be committed as the default.

## 5. Typography

Suggested starting point (Matthew may change it):
- Libre Franklin for UI and map labels. It descends from Franklin Gothic, which is close
  to the NYT graphics desk's typeface.
- Source Serif 4 for the project summaries and stage notes in the panel (shipped as Megaprojects
  Serif, a renamed subset; see `data/CREDITS.md`).
- Sentence case throughout. No all-caps labels. Tabular figures for numbers. City labels
  small, water names in italic.

## 6. Base map data

Pick sources, document why, and record licenses in `data/CREDITS.md`.

- Building footprints: Microsoft's US Building Footprints (the dataset the NYT used)
  and/or the Overture Maps buildings theme (newer, some heights). DataSF's footprints
  include heights for San Francisco. Choose one primary source for the region.
- Land and water: an OSM-derived land polygon or a California shoreline dataset, clipped
  to the region. It must include Treasure Island, Yerba Buena, Alameda, Bay Farm Island,
  Mare Island and the Delta channels near Antioch.
- Parcels: county assessor or open data portals, needed only around project sites.
- Project boundaries: from official plan documents, one file per project, with source
  and accuracy recorded.
- Optional faint context: freeways and rail lines (BART, Caltrain, VTA, ferry routes)
  from OSM or GTFS.
- Labels: a curated list of cities, water bodies and a few landmarks. Keep it short.
- Extent: the nine Bay Area counties. Default view shows the whole Bay. Constrain
  panning to the extent.

Pipeline: scripts that download, clip, simplify and tile the data (Tippecanoe to
PMTiles is a good default), runnable with one command. Raw downloads are cached in
`data/raw/` and git-ignored.

## 7. Project data model

- `data/projects.json` (provided): facts, stages, timeline, summary, sources, known gaps.
  Each project's `verify` list names things that still need checking. Each has a `category`
  (buildings or transportation).
- Official sources only (Matthew, 2026-10-02): every fact shown comes from a public agency or body,
  its adopted plans, hearing records, permits or GIS (`src/projects/official.ts` lists the hosts).
  Facts only the press or a developer reports go in the project's `reported` record, which the map
  never shows.
- `data/boundaries/{id}.geojson`: the site or plan boundary. Properties: `source`,
  `accuracy` ("official", "traced" or "approximate").
- `data/massing/{id}.geojson`: one feature per building, with properties `height_ft`,
  `base_ft`, `stage`, `use`, `phase`, `label` (optional), `source` ("traced: document,
  page" or "illustrative").
- A per-project `camera` setting (`center`, `zoom`, `pitch`, `bearing`) tuned so the
  site reads best when the fly-in lands.

Massing rules:
- Built and under-construction buildings: use real footprints and heights from the base
  data wherever they exist.
- Entitled designs: trace block footprints and height limits from design standards, EIR
  figures or master plan documents. Record the document and page.
- Illustrative massing is allowed only when it's labeled as such, in the data and in the
  UI.
- Plan-scale projects (Moffett Park, North Bayshore, Concord, Suisun Expansion, and
  Brisbane Baylands until it's approved) get a boundary and land-use zones only. No
  invented buildings.
- Landmarks to model specifically: the Potrero Power Station stack (300 ft) and Station
  A; Mission Rock's towers; Treasure Island's Isle House (22 stories); the historic Bayshore
  Roundhouse at the Baylands; Pier 70's Building 12.

## 8. Interaction spec

Regional view
- All project sites are filled and outlined in their stage color, with low extrusions
  once zoomed in past the regional level. Existing buildings are flat ink.
- Hovering a site shows its name and stage. A project too small to draw at the current
  zoom is a dot; names sit beside dots and sites from the regional view on, the biggest
  sites first (DECISIONS, 2026-10-13).

Fly-in (the signature moment)
- Clicking a site, a list entry or a deep link starts a slow flight of about 4 to 5
  seconds, easing in and out and ending at the project's camera setting (pitch around
  55 to 60 degrees).
- During the approach, the site boundary draws itself.
- On arrival, surrounding existing buildings extrude faintly to their true heights, and
  the project's buildings rise over about 1.2 seconds, staggered outward from the center.
- Escape, or the panel's close button, flies back out to where the viewer was.
- With reduced motion on, replace the flight with a quick crossfade and no rising
  animation.

Project panel (right side on desktop, bottom sheet on mobile), in this order:
1. Name, city and stage.
2. Stage bar (section 3).
3. Key numbers: homes (and affordable share), office/lab, retail, hotel keys, open
   space, acres. Show only what the data has.
4. Summary, then a "where it stands" note with its date.
5. Timeline of events.
6. Renderings (section 9), or links to official materials.
7. Developer and public partners.
8. Sources, plus the last-verified date and any open questions from the `verify` list,
   worded for readers.
9. Previous and next project.

Elsewhere
- Project index: a searchable list grouped by subregion, with filters by stage and size.
  Tabs at the top divide it into All, Buildings and Transportation (transportation and
  infrastructure: rail lines and ferry terminals), set by each record's `category`
  (Matthew, 2026-10-12). The tab filters the map too.
- Legend that doubles as a stage filter, with a count per stage.
- Deep links per project (for example `/p/potrero-power-station`) that open with the
  fly-in.
- Map controls: zoom, reset north, 2D/3D toggle, back to the whole Bay.
- About page (`/about`): what the map is, stage definitions, method, data sources and licenses,
  disclaimers (illustrative massing, approximate boundaries), credits, and a "Suggest a project"
  form (also linked from the foot of the Projects list; `scripts/suggest/README.md`).

## 9. Renderings

- Use only images with explicit permission (developer press kits) or Matthew's own work.
- Store them in `public/renders/{id}/` with a `renders.json` listing file, caption,
  credit and permission note.
- No permitted renders: show a link to the official project page or gallery, plus the
  map's own view of the massing.
- Photos: openly licensed or public-domain photos from Wikimedia Commons, approved by Matthew, listed
  in `data/photos.json` with author and license, resized and stored in `public/photos/`
  (`make photos`), never hotlinked. The outreach list for render permissions is
  `docs/images/PERMISSIONS.md`.

## 10. Tech stack (as built)

- Vite with TypeScript and Preact.
- MapLibre GL JS for the map and 3D extrusions; PMTiles for the base tiles.
- A Python pipeline (uv) for data prep, and Tippecanoe for tiling; `make data` runs it all.
- Vitest for data, provenance, theme and contrast tests; Playwright for interaction, accessibility
  (axe-core) and screenshot checks.
- GitHub Pages hosting, deployed on every push to main: map.matthewhuguet.com once the custom domain
  is set (`docs/share/README.md`), matthew6113.github.io/BAM/ before. Every tile file
  stays under 100 MB; `VITE_TILE_BASE_URL` can point the tiles at object storage later.

## 11. Quality bar

- Smooth fly-in and panning on a recent Mac; usable on a recent iPhone.
- First view on screen within about 3 seconds on broadband.
- Keyboard navigable with visible focus; legible contrast; reduced motion respected.
- No console errors. Each project panel renders with its full sources list.

## 12. Milestones and review checkpoints

All done. Matthew's reviews and calls along the way are in `docs/DECISIONS.md`.

- M0, setup: repo scaffold, README, data pipeline skeleton, `CREDITS.md`, `.gitignore`. Done.
- M1, base map: the NYT look with zero projects (footprints, land and water, minimal
  labels, theme file and style panel). Done Oct 1, 2026; reviewed by Matthew.
- M2, vertical slice: Potrero Power Station end to end (boundary, massing by block and
  stage, fly-in, panel, deep link). Done Oct 2, 2026; reviewed by Matthew.
- M3: every project as boundaries with panels, index, filters and legend. Done Oct 3, 2026 with the
  original 25; the map has since grown to 87.
- M4: massing for every project in batches of five, plus the plan-scale treatment. Done Oct 3 to 5.
- M5: about page, credits, performance, mobile, deployment. Done; the phone, accessibility and speed
  audit is `docs/AUDIT-2026-10.md` (Oct 16, 2026).
- M6, maintenance: a six-weekly update routine with a checklist script and a changelog (section 13).
  Done Oct 7, 2026.

## 13. Maintenance

Statuses change. Keep a `CHANGELOG.md` of data updates. About every six weeks (Matthew,
2026-10-07), a scheduled routine re-checks every project against official pages, updates
`lastVerified`, lists new project leads for Matthew, and opens a PR; merging it redeploys.
The procedure is `docs/UPKEEP.md`; `make upkeep` writes the checklist. Suggestions sent through the
map's form are leads like any other: researched against official sources, and added only if Matthew
says so.

## 14. Open questions for Matthew

Settled since the first draft:
- Title "Bay Area megaprojects", with the byline "by Matthew Huguet" linking to his site.
- Hosting on GitHub Pages, moving to map.matthewhuguet.com (Oct 9, 2026).
- Mission Bay stays on the map, as partly built.
- Mare Island, the Sonoma Developmental Center and BART station-area housing were researched and
  added. BART station-area housing is one project per station since Oct 19, 2026 (West Oakland, Lake
  Merritt, North Berkeley, Ashby, El Cerrito Plaza and Amador Station).

Still open:
- The final palette and type (the placeholders ship until then).
- Renderings: permissions to request (`docs/images/PERMISSIONS.md`); Matthew sends the requests.
- Oceanwide Center: keep the approved design until a new application is filed, and whether it reads
  as paused or distressed.
- Pre-approved additions waiting on environmental documents: the Harbor Bay ferry terminal and the
  Larkspur ferry expansion (`docs/UPKEEP.md`).
