# Build spec: Bay Area Megaprojects Map

Owner: Matthew Huguet. Draft 1, October 1, 2026.

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
- Palette: Matthew's own, to be supplied. Ship with the placeholders in section 4.

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

All colors live in one theme file (for example `src/theme/theme.json`), exposed as CSS
variables and map style values. These are placeholders until Matthew supplies his palette.

| Role | Placeholder |
|---|---|
| Land (paper) | #FFFFFF |
| Water | #ECEFF2 |
| Shoreline hairline | #A7B0BA |
| Existing buildings (ink) | #1E1E1E at 85% opacity |
| Labels | #3B3B3B, halo matching land or water |
| Stage: proposed | #9DB4E0 (outline only) |
| Stage: entitlement | #7898D4 |
| Stage: entitled | #4F78C4 |
| Stage: site work | #3459A8 |
| Stage: under construction | #1E3F86 |
| Stage: complete | Same as existing buildings |
| Stage: paused | #C08A1E |
| Stage: distressed | #A3242B |
| Selection highlight | #000000 |
| Panel background / text / rules | #FFFFFF / #1E1E1E / #E3E3E3 |

Style panel: a hidden panel (toggle with the S key or a small control) that lets Matthew
change any color role, switch presets, try type pairings, adjust building height
exaggeration and light direction, and toggle layers. It should update live, then export
and import the theme as JSON so a finished palette can be committed as the default.

## 5. Typography

Suggested starting point (Matthew may change it):
- Libre Franklin for UI and map labels. It descends from Franklin Gothic, which is close
  to the NYT graphics desk's typeface.
- Source Serif 4 for the project summaries and stage notes in the panel.
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
  Each project's `verify` list names things that still need checking.
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
- Hovering a site shows its name and stage. Labels for projects appear only when zoomed
  in, or on hover.

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
- Legend that doubles as a stage filter, with a count per stage.
- Deep links per project (for example `/p/potrero-power-station`) that open with the
  fly-in.
- Map controls: zoom, reset north, 2D/3D toggle, back to the whole Bay.
- About page: what the map is, stage definitions, method, data sources and licenses,
  disclaimers (illustrative massing, approximate boundaries), and credits.

## 9. Renderings

- Use only images with explicit permission (developer press kits) or Matthew's own work.
- Store them in `public/renders/{id}/` with a `renders.json` listing file, caption,
  credit and permission note.
- No permitted renders: show a link to the official project page or gallery, plus the
  map's own view of the massing.

## 10. Tech stack (recommended; propose changes with reasons)

- Vite with TypeScript; a light UI layer (vanilla or a small framework).
- MapLibre GL JS for the map and 3D extrusions; PMTiles for the base tiles.
- Python (geopandas/shapely) or Node for data prep; Tippecanoe for tiling.
- Playwright for screenshot checks of key views.
- Static hosting (Vercel, Netlify, Cloudflare Pages or GitHub Pages), with large tile
  files on object storage if needed. No paid map service is required.

## 11. Quality bar

- Smooth fly-in and panning on a recent Mac; usable on a recent iPhone.
- First view on screen within about 3 seconds on broadband.
- Keyboard navigable with visible focus; legible contrast; reduced motion respected.
- No console errors. Each project panel renders with its full sources list.

## 12. Milestones and review checkpoints

- M0, setup: repo scaffold, README, data pipeline skeleton, `CREDITS.md`, `.gitignore`.
- M1, base map: the NYT look with zero projects (footprints, land and water, minimal
  labels, theme file and style panel). Stop for Matthew's review.
- M2, vertical slice: Potrero Power Station end to end (boundary, massing by block and
  stage, fly-in, panel, deep link). Stop for Matthew's review.
- M3: all 25 projects as boundaries with panels, index, filters and legend.
- M4: massing for every project in batches of five, plus the plan-scale treatment.
- M5: about page, credits, performance, mobile, deployment.
- M6, maintenance: a quarterly status-check checklist (or script) and a changelog.

## 13. Maintenance

Statuses change. Keep a `CHANGELOG.md` of data updates. Each quarter, re-check every
project's stage and stage note against current reporting and official pages, update
`lastVerified`, and redeploy. This could later run as a scheduled task.

## 14. Open questions for Matthew

- Final palette and type choices (or keep the placeholders for now).
- The map's public title and how he wants to be credited.
- Domain and hosting preference.
- Whether to keep Mission Bay as a "completed" reference project.
- Whether to add candidates not yet researched: Mare Island, the Sonoma Developmental
  Center, BART station-area housing.
