// The Potrero Power Station vertical slice: fly-in, panel, deep link and the way back.
//   npx playwright test tests/project.spec.ts

import { test, expect, type Page } from '@playwright/test';
import data from '../data/projects.json' with { type: 'json' };
import { formatDate } from '../src/ui/format';

const POTRERO = data.projects.find((p) => p.id === 'potrero-power-station')!;
const SITE: [number, number] = [-122.3838, 37.7563];

async function ready(page: Page) {
  await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 120_000 });
}

const phase = (page: Page) => page.evaluate(() => document.body.dataset.flight ?? null);
const camera = (page: Page) =>
  page.evaluate(() => {
    const m = (window as any).__map;
    return { zoom: m.getZoom(), pitch: m.getPitch(), lng: m.getCenter().lng, lat: m.getCenter().lat };
  });

async function clickSite(page: Page) {
  const pt = await page.evaluate((c) => (window as any).__map.project(c), SITE);
  await page.mouse.click(pt.x, pt.y);
}

test('a deep link opens the project with its full sources list', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/p/potrero-power-station?test=1');
  await ready(page);
  const panel = page.getByRole('complementary', { name: 'Potrero Power Station' });
  await expect(panel).toBeVisible();
  await expect(page).toHaveTitle('Potrero Power Station · Bay Area megaprojects');
  await expect(panel.getByRole('heading', { level: 2 })).toBeFocused();
  await expect(panel.locator('.sources li')).toHaveCount(POTRERO.sources.length);
  await expect(panel).toContainText('Approximate boundary');
  await expect(panel).toContainText('held back until official records confirm them');
  await expect(panel).toContainText(`Last verified ${formatDate(POTRERO.lastVerified)}`);
  await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('risen');
  const cam = await camera(page);
  expect(cam.pitch).toBeCloseTo(POTRERO.camera!.pitch, 0);
  expect(errors).toEqual([]);
});

test('Escape closes the panel and flies back to where the viewer was', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/?test=1#map=13.2/37.757/-122.39');
  await ready(page);
  const before = await camera(page);
  await clickSite(page);
  await expect(page.getByRole('complementary', { name: 'Potrero Power Station' })).toBeVisible();
  await expect(page).toHaveURL(/\/p\/potrero-power-station/);
  await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('risen');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('complementary', { name: 'Potrero Power Station' })).toHaveCount(0);
  await expect.poll(() => phase(page), { timeout: 30_000 }).toBeNull();
  const after = await camera(page);
  expect(after.zoom).toBeCloseTo(before.zoom, 1);
  expect(after.pitch).toBe(0);
  expect(new URL(page.url()).pathname).toBe('/');
  await expect(page).toHaveTitle('Bay Area megaprojects');
  // Back in the flat 2D map the viewer started in.
  await expect(page.getByRole('button', { name: '3D' })).toBeVisible();
});

test('the Projects list is a keyboard route in and focus comes back out', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/?test=1');
  await ready(page);
  await page.getByRole('button', { name: 'Projects' }).focus();
  await page.keyboard.press('Enter');
  const item = page.getByRole('button', { name: /Potrero Power Station/ });
  await item.focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { level: 2, name: 'Potrero Power Station' })).toBeFocused();
  await page.getByRole('button', { name: 'Close and fly back' }).click();
  await expect(item).toBeFocused();
});

test('the back button closes the project', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/?test=1#map=13.2/37.757/-122.39');
  await ready(page);
  await clickSite(page);
  await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('risen');
  await page.goBack();
  await expect(page.getByRole('complementary', { name: 'Potrero Power Station' })).toHaveCount(0);
  await page.goForward();
  await expect(page.getByRole('complementary', { name: 'Potrero Power Station' })).toBeVisible();
});

test('the full-motion fly-in draws the boundary, lands, then raises the blocks', async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 700 });
  await page.goto('/?test=1#map=13.2/37.757/-122.39');
  await ready(page);
  await clickSite(page);
  await expect.poll(() => phase(page)).toBe('flying');
  // Part-way through, the boundary is being drawn: a line, but not yet the whole ring.
  const site = await page.evaluate(async () => {
    const src = (window as any).__map.getSource('project-boundary-draw');
    return (await src.getData()).features.length;
  });
  expect(site).toBeLessThanOrEqual(1);
  await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('landed');
  await expect.poll(() => phase(page), { timeout: 30_000 }).toBe('risen');
  const cam = await camera(page);
  expect(cam.pitch).toBeCloseTo(POTRERO.camera!.pitch, 0);
  // Every building still to be built has finished rising (the stack is already built).
  const rises = await page.evaluate(async () => {
    const map = (window as any).__map;
    const data = await map.getSource('project-massing').getData();
    return data.features
      .filter((f: any) => f.properties.stage !== 'complete')
      .map((f: any) => map.getFeatureState({ source: 'project-massing', id: f.properties.fid }).rise);
  });
  expect(rises.every((r: number) => r === 1)).toBe(true);
});

test('on a phone the panel is a bottom sheet and the site stays in view above it', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/p/potrero-power-station?test=1');
  await ready(page);
  const panel = page.getByRole('complementary', { name: 'Potrero Power Station' });
  const box = (await panel.boundingBox())!;
  expect(box.width).toBe(390);
  expect(box.y).toBeGreaterThan(380);
  await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('risen');
  const pt = await page.evaluate((c) => (window as any).__map.project(c), SITE);
  expect(pt.y).toBeLessThan(box.y);
  expect(pt.x).toBeGreaterThan(0);
  expect(pt.x).toBeLessThan(390);
});

test('Whole Bay closes the project and goes back to the whole region', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/p/potrero-power-station?test=1');
  await ready(page);
  await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('risen');
  await page.getByRole('button', { name: 'Whole Bay' }).click();
  await expect(page.getByRole('complementary', { name: 'Potrero Power Station' })).toHaveCount(0);
  await expect.poll(() => phase(page), { timeout: 30_000 }).toBeNull();
  const cam = await camera(page);
  expect(cam.pitch).toBe(0);
  expect(cam.zoom).toBeLessThan(11);
});

test('a project not yet on the map does not open its unchecked record', async ({ page }) => {
  await page.goto('/p/mission-rock?test=1');
  await ready(page);
  await expect.poll(() => new URL(page.url()).pathname).toBe('/');
  await expect(page.locator('.project-panel')).toHaveCount(0);
});
