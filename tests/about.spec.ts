// The about page: entry point, deep link, Escape, back button and focus.
//   npx playwright test tests/about.spec.ts

import { test, expect, type Page } from '@playwright/test';
import data from '../data/projects.json' with { type: 'json' };
import { formatDate } from '../src/ui/format';

async function ready(page: Page) {
  await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 120_000 });
}

const about = (page: Page) => page.getByRole('complementary', { name: 'About this map' });

test('a deep link to /about opens the about page with data-driven facts', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto('/about?test=1');
  await expect(about(page)).toBeVisible();
  await expect(page).toHaveTitle(/^About · /);
  await expect(page.getByRole('heading', { name: 'About this map' })).toBeFocused();
  // Every stage is in the key, with its meaning from the data.
  for (const s of data.stages) await expect(about(page).getByText(s.meaning)).toBeVisible();
  await expect(about(page)).toContainText(`last checked ${formatDate(data._meta.lastVerified)}`);
  await expect(about(page)).toContainText('© OpenStreetMap contributors');
  await ready(page);
  expect(errors).toEqual([]);
});

test('the About link opens the page; Escape closes it and returns focus', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  const link = page.getByRole('link', { name: 'About' });
  await link.click();
  await expect(about(page)).toBeVisible();
  await expect(page).toHaveURL(/\/about\?test=1(#|$)/);
  await page.keyboard.press('Escape');
  await expect(about(page)).toHaveCount(0);
  await expect(page).toHaveURL(/:\d+\/\?test=1(#|$)/);
  await expect(link).toBeFocused();
});

test('the close button and the back button both close the about page', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  await page.getByRole('link', { name: 'About' }).click();
  await page.getByRole('button', { name: 'Close about' }).click();
  await expect(about(page)).toHaveCount(0);
  await page.goBack();
  await expect(about(page)).toBeVisible();
  await page.goBack();
  await expect(about(page)).toHaveCount(0);
  await page.goForward();
  await expect(about(page)).toBeVisible();
});

test('opening a project from the about page replaces it', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/about?test=1');
  await ready(page);
  await page.getByRole('button', { name: /^Projects/ }).click();
  await page.getByRole('button', { name: /^Potrero Power Station/ }).click();
  await expect(page.getByRole('complementary', { name: 'Potrero Power Station' })).toBeVisible();
  await expect(about(page)).toHaveCount(0);
  await page.goBack();
  await expect(about(page)).toBeVisible();
  await expect(page.getByRole('complementary', { name: 'Potrero Power Station' })).toHaveCount(0);
});
