// Checkpoint screenshots of key views (CLAUDE.md: take them before each review).
//   npx playwright test tests/screenshots.spec.ts            -> docs/screenshots/m1/
//   SHOTS_DIR=some/dir npx playwright test tests/screenshots.spec.ts
// Rendering is SwiftShader in headless Chromium: right for judging the look, not for
// pixel diffs or performance.

import { test, expect, type Page } from '@playwright/test';

const DIR = process.env.SHOTS_DIR ?? 'docs/screenshots/m1';

interface Shot {
  name: string;
  path: string;
  viewport?: { width: number; height: number };
  /** Runs in the page after the map is idle, before the screenshot. */
  tweak?: string;
  fullPage?: boolean;
}

const desktop = { width: 1440, height: 900 };

const SHOTS: Shot[] = [
  { name: '01-whole-bay', path: '/?test=1' },
  { name: '02-nine-counties', path: '/?test=1#map=7.55/37.88/-122.37' },
  { name: '03-east-bay-z10', path: '/?test=1#map=10.4/37.82/-122.24' },
  { name: '04-san-francisco-z12', path: '/?test=1#map=12/37.765/-122.43' },
  { name: '05-potrero-z15', path: '/?test=1#map=15.2/37.7575/-122.386' },
  { name: '06-potrero-3d-preview', path: '/?test=1&view=3d#map=16/37.7565/-122.3855/-25/55' },
  { name: '07-mobile-whole-bay', path: '/?test=1', viewport: { width: 390, height: 844 } },
  { name: '08-style-panel', path: '/?test=1&style=1#map=10.6/37.79/-122.33' },
  // Options for review: same view, one change each.
  { name: 'options/a-overview-every-building-z10', path: '/?test=1&overview=all#map=10.2/37.79/-122.33' },
  { name: 'options/a-overview-lighter-tiles-z10', path: '/?test=1&overview=light#map=10.2/37.79/-122.33' },
  { name: 'options/b-opacity-ramp-z9', path: '/?test=1#map=9.4/37.80/-122.30' },
  {
    name: 'options/b-opacity-flat-85-z9',
    path: '/?test=1#map=9.4/37.80/-122.30',
    tweak: "window.__map.setPaintProperty('buildings-overview', 'fill-opacity', 0.85)",
  },
  { name: 'options/c-salt-ponds-as-water', path: '/?test=1&salt=1#map=11/37.47/-122.05' },
  { name: 'options/c-salt-ponds-as-land', path: '/?test=1&salt=0#map=11/37.47/-122.05' },
  { name: 'options/d-context-lines-on', path: '/?test=1&context=1#map=10.6/37.79/-122.30' },
  { name: 'options/e-outside-region-tint-on', path: '/?test=1&mask=1#map=8.6/38.05/-121.75' },
  { name: 'options/e-outside-region-tint-off', path: '/?test=1&mask=0#map=8.6/38.05/-121.75' },
];

async function waitForMap(page: Page) {
  await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 120_000 });
  await page.evaluate(
    () =>
      new Promise<void>((resolve) => {
        const map = (window as any).__map;
        const done = () => (map.areTilesLoaded() && !map.isMoving() ? resolve() : map.once('idle', done));
        map.once('idle', done);
        map.triggerRepaint();
      }),
  );
}

for (const shot of SHOTS) {
  test(shot.name, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('console', (m) => {
      if (m.type() === 'error') errors.push(m.text());
    });
    await page.setViewportSize(shot.viewport ?? desktop);
    await page.goto(shot.path);
    await waitForMap(page);
    if (shot.tweak) {
      await page.evaluate(shot.tweak);
      await waitForMap(page);
    }
    await page.waitForTimeout(500);
    await page.screenshot({ path: `${DIR}/${shot.name}.png`, timeout: 180_000 });
    expect(errors, errors.join('\n')).toEqual([]);
  });
}
