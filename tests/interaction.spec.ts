// Keyboard and control behaviour of the base map.
//   npx playwright test tests/interaction.spec.ts

import { test, expect, type Page } from '@playwright/test';

async function ready(page: Page) {
  await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 120_000 });
}

test('style panel opens with Alt+Shift+S, closes with Escape and returns focus', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  await page.keyboard.press('Alt+Shift+S');
  const panel = page.getByRole('complementary', { name: 'Style panel' });
  await expect(panel).toBeVisible();
  await expect(page.getByRole('button', { name: 'Close style panel' })).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(panel).toBeHidden();
  await expect(page.getByRole('button', { name: 'Style' })).toBeFocused();
});

test('a bare S does not open the style panel', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  await page.keyboard.press('s');
  await expect(page.getByRole('complementary', { name: 'Style panel' })).toHaveCount(0);
});

test('3D toggle tilts the map and 2D flattens it', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/?test=1#map=15/37.7575/-122.386');
  await ready(page);
  await page.getByRole('button', { name: '3D' }).click();
  await expect.poll(() => page.evaluate(() => (window as any).__map.getPitch())).toBeGreaterThan(50);
  await page.getByRole('button', { name: '2D' }).click();
  await expect.poll(() => page.evaluate(() => (window as any).__map.getPitch())).toBe(0);
});

test('Whole Bay returns to the default frame', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/?test=1');
  await ready(page);
  const home = await page.evaluate(() => (window as any).__map.getZoom());
  await page.evaluate(() => (window as any).__map.jumpTo({ center: [-122.4, 37.78], zoom: 14 }));
  await page.getByRole('button', { name: 'Whole Bay' }).click();
  await expect.poll(() => page.evaluate(() => (window as any).__map.getZoom())).toBeCloseTo(home, 1);
});

test('map controls are reachable by keyboard', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  const names: string[] = [];
  for (let i = 0; i < 12; i++) {
    await page.keyboard.press('Tab');
    names.push(await page.evaluate(() => document.activeElement?.getAttribute('aria-label') ?? document.activeElement?.textContent ?? ''));
  }
  expect(names).toEqual(expect.arrayContaining(['Zoom in', 'Zoom out', 'Reset north', 'Whole Bay']));
});
