// About page screenshots, desktop and phone.
//   npx playwright test tests/screenshots-about.spec.ts      -> docs/screenshots/about/
//   SHOTS_DIR=some/dir npx playwright test tests/screenshots-about.spec.ts

import { test, expect, type Page } from '@playwright/test';

const DIR = process.env.SHOTS_DIR ?? 'docs/screenshots/about';

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

const shot = (page: Page, name: string) => page.screenshot({ path: `${DIR}/${name}.png`, timeout: 180_000 });

for (const [name, viewport] of [
  ['desktop', { width: 1440, height: 900 }],
  ['phone', { width: 390, height: 844 }],
] as const) {
  test(`about page, ${name}`, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
    await page.setViewportSize(viewport);
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/about?test=1');
    await waitForMap(page);
    await shot(page, `01-about-${name}`);
    // The rest of the page, scrolled to the end.
    await page.locator('.about-panel').evaluate((el) => el.scrollTo(0, el.scrollHeight));
    await shot(page, `02-about-${name}-end`);
    expect(errors).toEqual([]);
  });
}
