# First prompt for Claude Code

Paste everything below the line into Claude Code after opening this folder.

---

I'm building an interactive 3D map of the Bay Area's largest development projects. It's a public portfolio piece, so it needs to look great and every fact needs to hold up.

Everything you need is in this folder. CLAUDE.md has the ground rules. docs/SPEC.md has the full design, interaction and technical spec, including milestones. data/projects.json has my research on 25 projects: current stage, program numbers, timelines, summaries and sources, verified as of Oct 1, 2026.

Read all three, then give me a short build plan before writing any code: your stack choice, which data sources you'll use for building footprints, the shoreline and parcels, and anything in the spec you think is wrong or missing. Wait for my OK.

Once I approve, build Milestones 0 and 1 and show me the base map in the NYT style with no projects on it yet. I want to react to the look before anything else goes on top. After my feedback, build Milestone 2: Potrero Power Station as a complete vertical slice, then stop again for review.

Use the placeholder colors for now. I'll bring my own palette.

Don't guess at facts. If a number, boundary or height isn't in the data or a source you can cite, flag it for verification instead.
