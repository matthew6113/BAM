# Sharing the map: map.matthewhuguet.com and the Squarespace page

The map stays on GitHub Pages (free, deployed on every push to `main`). Your Squarespace site links to it,
and it lives at your own address, **https://map.matthewhuguet.com**. Links to single projects look like
`https://map.matthewhuguet.com/p/smart-healdsburg/`.

## 1. Point the subdomain at GitHub (Squarespace, about 2 minutes)

1. Squarespace → **Settings → Domains → matthewhuguet.com → DNS → DNS Settings**.
2. Under **Custom records**, add a record:
   - **Type:** CNAME
   - **Host:** `map`
   - **Data:** `matthew6113.github.io`
3. Save. Nothing else changes; your main site keeps working. `map.matthewhuguet.com` was unused when
   this was written (Oct 9, 2026).

## 2. Tell GitHub Pages about it (GitHub, about 1 minute)

1. https://github.com/matthew6113/BAM → **Settings → Pages → Custom domain**: enter
   `map.matthewhuguet.com` and press **Save**.
2. Wait for GitHub's DNS check to pass. It can take from minutes up to a day after step 1.
3. Once it passes, tick **Enforce HTTPS**.
4. Recommended: in your GitHub account **Settings → Pages**, **verify** `matthewhuguet.com`. GitHub
   gives you a TXT record to add in Squarespace the same way as step 1. This stops anyone else from
   claiming the subdomain on GitHub.

## 3. Redeploy (GitHub, one click)

Do this right after step 2. Go to **Actions → Build and deploy → Run workflow** (branch `main`),
or ask Claude to start it.

Each build asks GitHub Pages for the site's address, so this build switches from `/BAM/` to the new
domain by itself. Until it finishes (a few minutes), pages at the new address will look broken. Old
links (`matthew6113.github.io/BAM/...`) redirect to the new address.

## 4. Check it

- Open https://map.matthewhuguet.com and a project link.
- To see the link-preview card, paste the address into LinkedIn's Post Inspector
  (https://www.linkedin.com/post-inspector/). This also refreshes LinkedIn's cached preview.

## 5. The Squarespace project page

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

**How it reads.** Every existing building in the region is drawn as a quiet, flat footprint, and only
the projects get color and height. The more certain a building is, the more solid it's drawn:
- proposed projects are dashed outlines;
- approved ones are solid;
- buildings under way rise in fuller color.

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
- `../../public/share-card.png`: the 1200 × 630 link-preview card. Redraw it with `npm run share-card`
  (dev server running) after any palette change; a unit test flags it if you forget.
