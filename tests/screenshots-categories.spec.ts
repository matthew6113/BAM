// The Projects index with each tab (All, Buildings, Transportation), desktop and phone.
//   npx playwright test tests/screenshots-categories.spec.ts   -> docs/screenshots/categories/

import { test, expect, type Page } from '@playwright/test';

const DIR = process.env.SHOTS_DIR ?? 'docs/screenshots/categories';

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

for (const [size, viewport] of [
  ['desktop', { width: 1440, height: 900 }],
  ['phone', { width: 390, height: 844 }],
] as const) {
  test(`index tabs, ${size}`, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.setViewportSize(viewport);
    await page.goto('/?test=1');
    await waitForMap(page);
    await page.getByRole('button', { name: /^Projects/ }).click();
    for (const tab of ['All', 'Buildings', 'Transportation']) {
      await page.getByRole('tab', { name: new RegExp(`^${tab}`) }).click();
      await waitForMap(page);
      await page.screenshot({ path: `${DIR}/${size}-${tab.toLowerCase()}.png`, timeout: 180_000 });
    }
    expect(errors).toEqual([]);
  });
}
