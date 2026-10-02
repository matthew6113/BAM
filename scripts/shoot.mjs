// Quick screenshot helper for design iteration:
//   node scripts/shoot.mjs <outdir> name=<url-path>[@WxH] ...
import { chromium } from '@playwright/test';

const [outdir, ...specs] = process.argv.slice(2);
const browser = await chromium.launch({
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
for (const spec of specs) {
  const name = spec.slice(0, spec.indexOf('='));
  const rest = spec.slice(spec.indexOf('=') + 1);
  const [path, size = '1440x900'] = rest.split('@');
  const [width, height] = size.split('x').map(Number);
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  const t0 = Date.now();
  await page.goto(`http://127.0.0.1:5173${path}`);
  await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 120000 });
  await page.evaluate(() => new Promise((resolve) => {
    const map = window.__map;
    const done = () => (map.areTilesLoaded() && !map.isMoving() ? resolve() : map.once('idle', done));
    map.once('idle', done);
    map.triggerRepaint();
  }));
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${outdir}/${name}.png`, timeout: 180000 });
  console.log(`${name}: ${Date.now() - t0} ms${errors.length ? ' ERRORS: ' + errors.join(' | ') : ''}`);
  await page.close();
}
await browser.close();
