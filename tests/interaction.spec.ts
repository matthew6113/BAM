// Keyboard and control behaviour of the base map.
//   npx playwright test tests/interaction.spec.ts

import { test, expect, type Page } from '@playwright/test';
import theme from '../src/theme/theme.json' with { type: 'json' };

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

// index.html carries the title, byline and theme variables, so words paint before the script loads.
test.describe('before the script runs', () => {
  test.use({ javaScriptEnabled: false });

  test('the page already has the title, the byline and the theme', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1 })).toHaveText('Bay Area megaprojects');
    await expect(page.getByRole('link', { name: 'Matthew Huguet' })).toHaveAttribute('href', 'https://www.matthewhuguet.com/');
    await expect(page.getByRole('link', { name: 'About' })).toHaveAttribute('href', '/about');
    const land = await page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--color-land').trim());
    expect(land).toBe(theme.colors.land);
  });
});

test('the app draws its own title in place of the static one', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  await expect(page.getByRole('heading', { level: 1 })).toHaveCount(1);
  await expect(page.locator('header.title')).toHaveCount(1);
  await expect(page.getByRole('button', { name: /^Projects/ })).toBeVisible();
});

test('street-level building tiles load only once the map is zoomed in', async ({ page }) => {
  const detail: string[] = [];
  page.on('request', (r) => {
    if (/buildings-z1[345]\.pmtiles/.test(r.url())) detail.push(r.url());
  });
  await page.goto('/?test=1');
  await ready(page);
  expect(detail).toEqual([]);
  await page.evaluate(() => (window as any).__map.jumpTo({ center: [-122.4, 37.78], zoom: 15.5 }));
  await expect.poll(() => detail.some((u) => u.includes('buildings-z15'))).toBe(true);
  // The buildings draw: the street-level layer has features in view.
  await expect.poll(() => page.evaluate(() =>
    (window as any).__map.queryRenderedFeatures({ layers: ['buildings-z15'] }).length), { timeout: 60_000 }).toBeGreaterThan(0);
});
