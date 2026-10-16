// The "Suggest a project" form: reachable from the Projects list and the about page, and (without
// a receiver configured, as in tests) it opens a prefilled GitHub issue.
//   npx playwright test tests/suggest.spec.ts

import { test, expect, type Page } from '@playwright/test';

async function ready(page: Page) {
  await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 120_000 });
}

test('the Projects list links to the form on the about page', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  await page.getByRole('button', { name: /^Projects/ }).click();
  await page.getByRole('button', { name: 'Suggest a project' }).click();
  await expect(page).toHaveURL(/\/about\?test=1(#|$)/);
  const heading = page.getByRole('heading', { name: 'Suggest a project' });
  await expect(heading).toBeFocused();
  await expect(heading).toBeInViewport();
  // Escape closes the page and returns focus to the link.
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button', { name: 'Suggest a project' })).toBeFocused();
});

test('the form needs a name and place, then opens a prefilled GitHub issue', async ({ page, context }) => {
  // Don't reach GitHub from a test: answer the new tab locally.
  await context.route('https://github.com/**', (r) => r.fulfill({ contentType: 'text/html', body: 'ok' }));
  await page.goto('/about?test=1');
  const about = page.getByRole('complementary', { name: 'About this map' });
  const submit = about.getByRole('button', { name: 'Suggest on GitHub' });
  await submit.click();
  // The browser's own validation stops an empty form.
  await expect(about.getByLabel('Project name')).toBeFocused();
  await about.getByLabel('Project name').fill('Example Yards');
  await about.getByLabel('City or location').fill('Oakland');
  await about.getByLabel(/Official link/).fill('https://www.oaklandca.gov/example');
  await about.getByLabel(/Anything else/).fill('About 2,000 homes.');
  const [popup] = await Promise.all([
    page.waitForEvent('popup'),
    submit.click(),
  ]);
  await popup.waitForURL(/^https:\/\/github\.com\//);
  const target = new URL(popup.url());
  expect(target.origin + target.pathname).toBe('https://github.com/matthew6113/BAM/issues/new');
  expect(target.searchParams.get('title')).toBe('Suggest: Example Yards');
  expect(target.searchParams.get('body')).toContain('**Where:** Oakland');
  expect(target.searchParams.get('body')).toContain('About 2,000 homes.');
});
