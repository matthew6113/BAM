// Try landing cameras for a project: node scripts/cameras.mjs <outdir> <id> name=lng,lat,zoom,pitch,bearing ...
// Opens the deep link with reduced motion, then jumps to each camera (with the panel's padding).
import { chromium } from '@playwright/test';

const [outdir, id, ...specs] = process.argv.slice(2);
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
await page.goto(`http://127.0.0.1:5173/p/${id}?test=1`);
await page.waitForFunction(() => document.body.dataset.flight === 'risen', null, { timeout: 120000 });
const idle = () => page.evaluate(() => new Promise((r) => {
  const m = window.__map;
  const done = () => (m.areTilesLoaded() && !m.isMoving() ? r() : m.once('idle', done));
  m.once('idle', done);
  m.triggerRepaint();
}));
await idle();
console.log(await page.evaluate(() => JSON.stringify(window.__map.queryRenderedFeatures({ layers: ['project-massing-labels'] }).map((f) => f.properties))));
for (const spec of specs) {
  const [name, v] = spec.split('=');
  const [lng, lat, zoom, pitch, bearing] = v.split(',').map(Number);
  await page.evaluate((c) => window.__map.jumpTo(c), { center: [lng, lat], zoom, pitch, bearing });
  await idle();
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${outdir}/${name}.png`, timeout: 180000 });
  console.log(name);
}
await browser.close();
