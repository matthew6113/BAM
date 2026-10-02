// Milestone 2 checkpoint screenshots: the Potrero Power Station vertical slice.
//   npx playwright test tests/screenshots-m2.spec.ts         -> docs/screenshots/m2/
//   SHOTS_DIR=some/dir npx playwright test tests/screenshots-m2.spec.ts
// Frames inside the fly-in are held still at a moment (?at=seconds, test builds only):
// software WebGL is far too slow to catch the real 4.5 s flight in motion.

import { test, expect, type Page } from '@playwright/test';

const DIR = process.env.SHOTS_DIR ?? 'docs/screenshots/m2';
const desktop = { width: 1440, height: 900 };
const SITE: [number, number] = [-122.3838, 37.7563];

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

const landed = (page: Page) =>
  page.waitForFunction(() => document.body.dataset.flight === 'risen', null, { timeout: 120_000 });

function collectErrors(page: Page) {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  return errors;
}

const shot = (page: Page, name: string) => page.screenshot({ path: `${DIR}/${name}.png`, timeout: 180_000 });

test('01 whole Bay with the project marker', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize(desktop);
  await page.goto('/?test=1');
  await waitForMap(page);
  await shot(page, '01-whole-bay-marker');
  expect(errors).toEqual([]);
});

test('02 hovering the site', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize(desktop);
  await page.goto('/?test=1#map=13.6/37.7575/-122.392');
  await waitForMap(page);
  const pt = await page.evaluate((c) => (window as any).__map.project(c), SITE);
  await page.mouse.move(pt.x, pt.y);
  await expect(page.locator('.map-tooltip')).toBeVisible();
  await shot(page, '02-site-hover-z13');
  expect(errors).toEqual([]);
});

// Seconds into the sequence: flight 0 to 4.5 s (boundary draws 1.6 to 4.0 s), then the rise.
const FRAMES: [string, number][] = [
  ['03a-approach-1.5s', 1.5],
  ['03b-boundary-drawing-3.0s', 3.0],
  ['03c-blocks-rising-5.0s', 5.0],
];

for (const [name, at] of FRAMES) {
  test(`03 fly-in frame ${name}`, async ({ page }) => {
    const errors = collectErrors(page);
    await page.setViewportSize(desktop);
    await page.goto(`/?test=1&at=${at}#map=12.6/37.757/-122.392`);
    await waitForMap(page);
    const pt = await page.evaluate((c) => (window as any).__map.project(c), SITE);
    await page.mouse.click(pt.x, pt.y);
    await page.waitForFunction(() => document.body.dataset.flight, null, { timeout: 30_000 });
    // The held camera keeps redrawing, so wait on tiles rather than idle.
    await page.waitForFunction(() => (window as any).__map.areTilesLoaded(), null, { timeout: 120_000, polling: 500 });
    await page.waitForTimeout(3000);
    await shot(page, name);
    expect(errors).toEqual([]);
  });
}

test('04 landed, with the panel', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize(desktop);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/p/potrero-power-station?test=1');
  await landed(page);
  await waitForMap(page);
  await page.waitForTimeout(900);
  await shot(page, '04-landed-panel');
  // The rest of the panel: timeline, links, developer, sources.
  await page.locator('.project-panel').evaluate((el) => el.scrollTo(0, el.scrollHeight));
  await page.waitForTimeout(200);
  await page.locator('.project-panel').screenshot({ path: `${DIR}/05-panel-lower.png` });
  expect(errors).toEqual([]);
});

test('06 phone: bottom sheet', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/p/potrero-power-station?test=1');
  await landed(page);
  await waitForMap(page);
  await page.waitForTimeout(900);
  await shot(page, '06-phone-sheet');
  expect(errors).toEqual([]);
});

test('07 traced boundary and blocks from above', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize(desktop);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/p/potrero-power-station?test=1');
  await landed(page);
  await page.evaluate(() => (window as any).__map.jumpTo({ pitch: 0, bearing: 0, zoom: 16.6 }));
  await waitForMap(page);
  await page.waitForTimeout(900);
  await shot(page, '07-traced-top-down');
  expect(errors).toEqual([]);
});

// Options for review: one change each from the landed view.
const OPTIONS: { name: string; tweak: string }[] = [
  {
    // Shipped: the spec's "light fill" for entitled buildings, so Block 2 (under construction) reads as more certain.
    name: 'a-entitled-light-fill-0.5',
    tweak: '',
  },
  {
    name: 'a-entitled-solid-0.78',
    tweak: "window.__map.setPaintProperty('project-massing-entitled', 'fill-extrusion-opacity', 0.78)",
  },
  {
    name: 'b-camera-from-southeast',
    tweak: "window.__map.jumpTo({ center: [-122.3838, 37.7566], zoom: 16.4, pitch: 58, bearing: 30 })",
  },
];

for (const option of OPTIONS) {
  test(`options: ${option.name}`, async ({ page }) => {
    await page.setViewportSize(desktop);
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/p/potrero-power-station?test=1');
    await landed(page);
    if (option.tweak) await page.evaluate(option.tweak);
    await waitForMap(page);
    await page.waitForTimeout(900);
    await shot(page, `options/${option.name}`);
  });
}
