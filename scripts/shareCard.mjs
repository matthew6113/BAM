// The link-preview card (1200 x 630) that LinkedIn, iMessage, Slack and others show for the map:
//   npm run share-card        (with the dev server on 5173: `npm run dev`, or the mock config)
// Renders the live map with its interface hidden, sets the title, byline and data credit beside it
// in the map's own fonts and theme colours, and writes public/share-card.png. It also writes
// public/share-card.json with the theme it was drawn from; a unit test flags a stale card after a
// palette change, so the card is redrawn with the new colours.
import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const read = (p) => readFileSync(new URL(p, root));
const theme = JSON.parse(read('src/theme/theme.json'));
const W = 1200;
const H = 630;
const BASE = process.env.SHOOT_BASE ?? 'http://127.0.0.1:5173';
// The middle of the Bay, set right of centre so the text has the left side.
const CAMERA = { center: [-122.5, 37.66], zoom: 8.85, pitch: 0, bearing: 0 };

const c = theme.colors;
const accent = theme.stages.entitlement;
const rgba = (hex, a) => {
  const h = hex.replace('#', '');
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
  return `rgba(${r}, ${g}, ${b}, ${a})`;
};
const font = (file) => `data:font/woff2;base64,${read(`public/generated/fonts/${file}`).toString('base64')}`;

const browser = await chromium.launch({
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});

// 1. The map, interface hidden.
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
await page.goto(`${BASE}/?test=1`);
await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 180000 });
await page.addStyleTag({
  content: '.title, .controls, .credits, .style-toggle, .skip-link { display: none !important; }',
});
await page.evaluate((cam) => window.__map.jumpTo(cam), CAMERA);
await page.evaluate(() => new Promise((resolve) => {
  const map = window.__map;
  const done = () => (map.areTilesLoaded() && !map.isMoving() ? resolve() : map.once('idle', done));
  map.once('idle', done);
  map.triggerRepaint();
}));
await page.waitForTimeout(500);
const mapPng = (await page.screenshot({ type: 'png' })).toString('base64');
await page.close();

// 2. The card.
const card = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await card.setContent(`<!doctype html><html><head><style>
  @font-face { font-family: 'Libre Franklin'; src: url(${font('LibreFranklin-Variable.woff2')}) format('woff2'); font-weight: 100 900; }
  @font-face { font-family: 'Source Serif 4'; src: url(${font('SourceSerif4-Variable.woff2')}) format('woff2'); font-weight: 200 900; }
  html, body { margin: 0; }
  body { width: ${W}px; height: ${H}px; position: relative; overflow: hidden; background: ${c.land}; }
  .map { position: absolute; inset: 0; background: url(data:image/png;base64,${mapPng}) center / cover; }
  .veil { position: absolute; inset: 0; background: linear-gradient(90deg, ${c.land} 0%, ${c.land} 42%, ${rgba(c.land, 0.8)} 49%, ${rgba(c.land, 0)} 64%); }
  .text { position: absolute; left: 64px; top: 0; bottom: 0; width: 430px; display: flex; flex-direction: column; justify-content: center; }
  .kicker { font: 600 17px/1 'Libre Franklin'; color: ${accent}; }
  h1 { font: 700 58px/1.02 'Libre Franklin'; letter-spacing: -0.01em; color: ${c.panelText}; margin: 16px 0 20px; }
  p { font: 400 24px/1.38 'Source Serif 4'; color: ${c.labels}; margin: 0; }
  .by { margin-top: 30px; font: 600 18px/1.3 'Libre Franklin'; color: ${c.panelText}; }
  .by span { font-weight: 400; color: ${c.labels}; }
  .rule { width: 56px; height: 3px; background: ${accent}; margin-top: 30px; }
  .credit { position: absolute; left: 64px; bottom: 24px; font: 400 12px/1 'Libre Franklin'; color: ${c.labels}; }
</style></head><body>
  <div class="map"></div><div class="veil"></div>
  <div class="text">
    <div class="kicker">Interactive 3D map</div>
    <h1>Bay Area megaprojects</h1>
    <p>The region's largest development projects, where each one stands, drawn from official records.</p>
    <div class="rule"></div>
    <div class="by">Matthew Huguet <span>· map.matthewhuguet.com</span></div>
  </div>
  <div class="credit">Map data © OpenStreetMap contributors, Overture Maps Foundation</div>
</body></html>`);
await card.evaluate(() => document.fonts.ready);
await card.screenshot({ path: new URL('public/share-card.png', root).pathname, type: 'png' });
await browser.close();

writeFileSync(new URL('public/share-card.json', root), `${JSON.stringify({
  note: 'Theme the share card was drawn with (scripts/shareCard.mjs). Redraw it after a palette change: npm run share-card.',
  colors: theme.colors,
  stages: theme.stages,
}, null, 2)}\n`);
console.log('wrote public/share-card.png and public/share-card.json');
