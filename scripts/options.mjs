// Render look options side by side without touching the shipped theme:
//   node scripts/options.mjs <outdir> <options.json>
// options.json: [{ name, theme?: partial theme, paint?: { layerId: { prop: value } },
//                  add?: [[layerSpec, beforeId]],
//                  views: [{ name, path?, camera?: {center, zoom, pitch, bearing}, size?, flight? }] }]
// flight: true waits for a project deep link to land and raise its blocks (with reduced motion).
// The theme is merged over theme.json and injected through localStorage (as the style panel does);
// paint overrides are applied to the live map, for things the theme doesn't cover yet.
import { chromium } from '@playwright/test';
import { readFileSync } from 'node:fs';

const [outdir, file] = process.argv.slice(2);
const options = JSON.parse(readFileSync(file, 'utf8'));
const base = JSON.parse(readFileSync(new URL('../src/theme/theme.json', import.meta.url), 'utf8'));

const merge = (a, b) => {
  if (!b || typeof b !== 'object' || Array.isArray(b)) return b ?? a;
  const out = { ...a };
  for (const [k, v] of Object.entries(b)) out[k] = merge(a?.[k], v);
  return out;
};

const browser = await chromium.launch({
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
for (const opt of options) {
  const theme = merge(base, opt.theme ?? {});
  for (const view of opt.views) {
    const [width, height] = (view.size ?? '1440x900').split('x').map(Number);
    const page = await browser.newPage({
      viewport: { width, height }, deviceScaleFactor: view.dpr ?? 1, reducedMotion: view.flight ? 'reduce' : 'no-preference',
    });
    await page.addInitScript((t) => localStorage.setItem('bam.theme.v1', JSON.stringify(t)), theme);
    await page.goto(`http://127.0.0.1:5173${view.path ?? '/'}`);
    await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 180000 });
    if (view.flight) await page.waitForFunction(() => document.body.dataset.flight === 'risen', null, { timeout: 180000 });
    await page.evaluate(({ paint, add, camera }) => {
      const map = window.__map;
      for (const [layer, before] of add ?? []) map.addLayer(layer, before);
      for (const [layer, props] of Object.entries(paint ?? {})) {
        for (const [prop, value] of Object.entries(props)) {
          if (prop.startsWith('layout:')) map.setLayoutProperty(layer, prop.slice(7), value);
          else map.setPaintProperty(layer, prop, value);
        }
      }
      if (camera) map.jumpTo(camera);
    }, { paint: opt.paint, add: opt.add, camera: view.camera });
    await page.evaluate(() => new Promise((resolve) => {
      const map = window.__map;
      const done = () => (map.areTilesLoaded() && !map.isMoving() ? resolve() : map.once('idle', done));
      map.once('idle', done);
      map.triggerRepaint();
    }));
    await page.waitForTimeout(400);
    await page.screenshot({ path: `${outdir}/${opt.name}-${view.name}.png`, timeout: 180000 });
    console.log(`${opt.name}-${view.name}`);
    await page.close();
  }
}
await browser.close();
