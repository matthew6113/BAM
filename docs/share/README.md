# Sharing the map: map.matthewhuguet.com and the Squarespace page

The map stays on GitHub Pages: free, and deployed on every push to `main`. Your Squarespace site links
to it, and it lives at your own address, **https://map.matthewhuguet.com**. Links to single projects
look like `https://map.matthewhuguet.com/p/smart-healdsburg/`.

## Switching to map.matthewhuguet.com (about 15 minutes, plus waiting for DNS)

Do these in order. Steps 3 to 5 go back to back: from the moment you press Save in step 3 until the
build in step 5 finishes, the map shows a blank page at both the old and new addresses. The live build
still expects `/BAM/`, and saving the domain doesn't rebuild it.

1. **Verify your domain with GitHub.** This stops anyone else's GitHub account from claiming
   `map.matthewhuguet.com`.
   - Go to GitHub → your profile picture → **Settings → Pages → Add a domain** and enter
     `matthewhuguet.com`.
   - GitHub shows a TXT record. In Squarespace, go to **Settings → Domains → matthewhuguet.com → DNS →
     DNS Settings → Custom records** and add it:
     - **Type:** TXT
     - **Name:** `_github-pages-challenge-matthew6113`. Enter only this part: Squarespace adds
       `.matthewhuguet.com` itself, and pasting the full name doubles it.
     - **Data:** the code GitHub shows.
   - Back on GitHub, click **Verify**. It can take a while for DNS to update; wait until GitHub says
     *Verified*.
2. **Have the next two steps open in two tabs:**
   - the repository's **Settings → Pages**: https://github.com/matthew6113/BAM/settings/pages
   - Squarespace's **DNS Settings → Custom records**.
3. **Save the domain on GitHub.** Under **Custom domain**, enter `map.matthewhuguet.com` and press **Save**.
4. **Add the CNAME in Squarespace straight away.** Add a custom record:
   - **Type:** CNAME
   - **Name:** `map`
   - **Data:** `matthew6113.github.io`

   Your main site isn't affected. `map.matthewhuguet.com` was unused when this was written
   (Oct 9, 2026).
5. **Redeploy straight away.** Go to **Actions → Build and deploy → Run workflow** (branch `main`), or ask
   Claude to start it. It takes a few minutes. Each build asks GitHub Pages for the site's address, so
   this one builds for `https://map.matthewhuguet.com` without any code change.
6. **Turn on HTTPS.** When GitHub's DNS check on the Pages settings page passes (minutes, sometimes
   longer), tick **Enforce HTTPS**. No rebuild is needed: the build already uses https:// addresses.

Old links (`matthew6113.github.io/BAM/...`) redirect to the same page at the new address.

If you ever stop using GitHub Pages for the map, delete the `map` CNAME in Squarespace too.

## Check it

- Open https://map.matthewhuguet.com and a project link.
- To see the link-preview card, paste the address into LinkedIn's Post Inspector
  (https://www.linkedin.com/post-inspector/). This also refreshes LinkedIn's cached preview.

## The Squarespace project page

1. **Pages → + → Page → Blank**, named *Bay Area megaprojects*, with the URL slug `/bay-area-megaprojects`.
2. Add these blocks, in this order:
   - **Image:** `docs/share/project-desktop.png`
   - **Text:** the copy below
   - **Button:** "Open the map", linking to `https://map.matthewhuguet.com`
   - A second **Image** if you like: `project-phone.png` or `overview-desktop.png`
3. **Page settings → Social image:** `public/share-card.png`, so the page's own link preview matches the map's.
4. Add the page to your navigation or portfolio.

The screenshots leave out the project photos, which are Wikimedia Commons images and need their credit
next to them. Edit the copy freely; every claim in it matches what the map does.

---

### Copy

**Bay Area megaprojects**

*An interactive 3D map of the region's largest development projects.*

The Bay Area's biggest projects are recorded across dozens of agencies' agendas, environmental reports
and permit systems: former shipyards and power plants becoming neighborhoods, new rail lines, campus
plans. I built this map to put them in one place and to show where each one actually stands.

**How it reads.** Across the region, every existing building is drawn as a quiet, flat footprint, and
only the projects get color and height. Up close, neighboring buildings rise as faint gray context.
The more certain a project is, the more solid it's drawn:
- proposed projects, with no approvals yet, are dashed outlines;
- projects in formal review or already approved are solid outlines with a light fill;
- buildings under construction rise in fuller color.

Click a project and the camera flies in. The site boundary draws, the planned buildings rise, and a
panel explains what's planned, where it stands and where each fact comes from.

**Sources.** Every fact on the map comes from an official source: public agencies, adopted plans,
hearing records, permits, environmental documents and public GIS. Claims that only the press or a
developer has made are held back until an official record confirms them. Boundaries come from official
GIS or are traced from planning documents, and anything approximate is labelled as such.

**Built with** MapLibre, PMTiles and Overture Maps data, a reproducible Python data pipeline, and Preact
and TypeScript. Map data © OpenStreetMap contributors and the Overture Maps Foundation.

[Open the map →](https://map.matthewhuguet.com)

---

### Files here

- `project-desktop.png`: Potrero Power Station, opened (2880 × 1800).
- `overview-desktop.png`: the region (2880 × 1800).
- `project-phone.png`: SMART Healdsburg on a phone (1170 × 2532).
- `../../public/share-card.png`: the 1200 × 630 link-preview card. After a palette change, redraw it
  with `npm run share-card` while the dev server is running. Without local map data, start
  `npx vite --config vite.mock.config.ts` and run `SHOOT_BASE=http://localhost:5180 npm run share-card`.
  `npm test` flags a stale card locally.
