// Milestone 3 screenshots: every project as a boundary, the index, its filters and legend.
//   npx playwright test tests/screenshots-m3.spec.ts         -> docs/screenshots/m3/
//   SHOTS_DIR=some/dir npx playwright test tests/screenshots-m3.spec.ts

import { test, expect, type Page } from '@playwright/test';

const DIR = process.env.SHOTS_DIR ?? 'docs/screenshots/m3';
const desktop = { width: 1440, height: 900 };

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

test('01 whole Bay with every project', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize(desktop);
  await page.goto('/?test=1');
  await waitForMap(page);
  await shot(page, '01-whole-bay');
  expect(errors).toEqual([]);
});

test('02 the index, legend and filters', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize(desktop);
  await page.goto('/?test=1');
  await waitForMap(page);
  await page.getByRole('button', { name: /^Projects/ }).click();
  await shot(page, '02-index-open');
  // Hide the stages that haven't started building, and narrow to the South Bay.
  for (const stage of ['Proposed', 'In entitlement', 'Entitled']) {
    await page.locator('.stage-toggle', { hasText: stage }).click();
  }
  await page.locator('.subregion select').selectOption('South Bay');
  await waitForMap(page);
  await shot(page, '03-index-filtered');
  expect(errors).toEqual([]);
});

test('04 San Francisco sites at city scale', async ({ page }) => {
  const errors = collectErrors(page);
  await page.setViewportSize(desktop);
  await page.goto('/?test=1#map=12.3/37.752/-122.41');
  await waitForMap(page);
  await shot(page, '04-sf-sites');
  expect(errors).toEqual([]);
});

for (const [n, id] of [
  ['05', 'candlestick-point'],
  ['06', 'concord-naval-weapons-station'],
  ['07', 'downtown-west'],
  ['08', 'willow-village'],
] as const) {
  test(`${n} landed: ${id}`, async ({ page }) => {
    const errors = collectErrors(page);
    await page.setViewportSize(desktop);
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(`/p/${id}?test=1`);
    await landed(page);
    await waitForMap(page);
    await page.waitForTimeout(600);
    await shot(page, `${n}-landed-${id}`);
    expect(errors).toEqual([]);
  });
}
