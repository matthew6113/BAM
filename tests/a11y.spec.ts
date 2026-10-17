// Accessibility, phone layout and loading checks from the October 2026 audit (docs/AUDIT-2026-10.md).
//   npx playwright test tests/a11y.spec.ts

import { test, expect, type Page } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';
import photos from '../data/photos.json' with { type: 'json' };

async function ready(page: Page) {
  await page.waitForFunction(() => document.body.dataset.mapReady === 'true', null, { timeout: 120_000 });
}
const phase = (page: Page) => page.evaluate(() => document.body.dataset.flight ?? null);

/** Serious and critical axe violations (WCAG 2.2 A/AA), as "rule: target" lines. */
async function axe(page: Page): Promise<string[]> {
  const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
  return r.violations
    .filter((v) => v.impact === 'serious' || v.impact === 'critical')
    .flatMap((v) => v.nodes.map((n) => `${v.id}: ${n.target.join(' ')}`));
}

for (const [name, viewport] of [['desktop', { width: 1280, height: 800 }], ['phone', { width: 390, height: 664 }]] as const) {
  test.describe(`axe on ${name}`, () => {
    test.use({ viewport });

    test('landing, the open index and its tabs have no serious violations', async ({ page }) => {
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await page.goto('/?test=1');
      await ready(page);
      expect(await axe(page)).toEqual([]);
      await page.getByRole('button', { name: /^Projects/ }).click();
      expect(await axe(page)).toEqual([]);
      await page.getByRole('tab', { name: /^Transportation/ }).click();
      expect(await axe(page)).toEqual([]);
    });

    test('a project panel with a photo has no serious violations', async ({ page }) => {
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await page.goto('/p/potrero-power-station?test=1');
      await ready(page);
      await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('risen');
      expect(await axe(page)).toEqual([]);
    });

    test('the about page has no serious violations', async ({ page }) => {
      await page.goto('/about?test=1');
      await ready(page);
      expect(await axe(page)).toEqual([]);
    });
  });
}

test('the page has a main landmark holding the map and its controls', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  const main = page.getByRole('main');
  await expect(main).toHaveCount(1);
  await expect(main.getByRole('region', { name: 'Map of the Bay Area' })).toHaveCount(1);
  await expect(main.getByRole('navigation', { name: 'Map controls' })).toHaveCount(1);
});

test('Escape closes the Projects list and returns focus to its toggle', async ({ page }) => {
  await page.goto('/?test=1');
  await ready(page);
  const toggle = page.getByRole('button', { name: /^Projects/ });
  await toggle.click();
  await page.getByRole('searchbox', { name: 'Search projects' }).focus();
  await page.keyboard.press('Escape');
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  await expect(toggle).toBeFocused();
  await expect(page.locator('#project-index-body')).toBeHidden();
});

test('closing a deep-linked project puts focus on the map, not nowhere', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/p/potrero-power-station?test=1');
  await ready(page);
  await expect.poll(() => phase(page), { timeout: 60_000 }).toBe('risen');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('region', { name: 'Map of the Bay Area' })).toBeFocused();
});

test('with reduced motion the fly-in jumps and the panel does not slide', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/?test=1');
  await ready(page);
  await page.getByRole('button', { name: /^Projects/ }).click();
  // A flight moves the camera every frame; with reduced motion it jumps (one move) behind a dip to paper.
  await page.evaluate(() => {
    (window as any).__moves = 0;
    (window as any).__map.on('move', () => (window as any).__moves++);
  });
  await page.getByRole('button', { name: /^Potrero Power Station/ }).click();
  await expect.poll(() => phase(page), { timeout: 30_000 }).toBe('risen');
  expect(await page.evaluate(() => (window as any).__moves)).toBeLessThanOrEqual(2);
  const animation = await page.locator('.project-panel').evaluate((el) => getComputedStyle(el).animationName);
  expect(animation).toBe('none');
});

test('photos load only for the open project, lazily, with its caption and a credit', async ({ page }) => {
  const requested: string[] = [];
  page.on('request', (r) => {
    if (/\/photos\//.test(r.url())) requested.push(new URL(r.url()).pathname);
  });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/?test=1');
  await ready(page);
  expect(requested).toEqual([]);
  const photo = photos.photos.find((p) => p.id === 'potrero-power-station')!;
  await page.getByRole('button', { name: /^Projects/ }).click();
  await page.getByRole('button', { name: /^Potrero Power Station/ }).click();
  const img = page.locator('.project-panel .photo img');
  await expect(img).toHaveAttribute('loading', 'lazy');
  // The figcaption names the photo, so the image itself is silent (alt="") rather than read twice.
  await expect(img).toHaveAttribute('alt', '');
  await expect(page.locator('.project-panel .photo figcaption')).toContainText(photo.caption);
  await expect(page.locator('.project-panel .photo .credit')).toContainText('Wikimedia Commons');
  await img.scrollIntoViewIfNeeded();
  await expect.poll(() => requested).toEqual([`/${photo.src}`]);
});

test.describe('on a phone', () => {
  test.use({ viewport: { width: 390, height: 664 }, hasTouch: true, isMobile: true });

  test('nothing scrolls sideways and the open list stays clear of the credits', async ({ page }) => {
    await page.goto('/?test=1');
    await ready(page);
    await page.getByRole('button', { name: /^Projects/ }).tap();
    const list = (await page.locator('#project-index-body').boundingBox())!;
    const credits = (await page.locator('.credits').boundingBox())!;
    expect(list.y + list.height).toBeLessThanOrEqual(credits.y);
    expect(await page.evaluate(() => document.scrollingElement!.scrollWidth)).toBeLessThanOrEqual(390);
  });

  test('the panel close button is a 44 px target', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/p/potrero-power-station?test=1');
    await ready(page);
    const box = (await page.getByRole('button', { name: 'Close and fly back' }).boundingBox())!;
    expect(box.width).toBeGreaterThanOrEqual(44);
    expect(box.height).toBeGreaterThanOrEqual(44);
  });

  test('the about sheet takes the controls behind it out of the tab order', async ({ page }) => {
    await page.goto('/about?test=1');
    await ready(page);
    await expect(page.getByRole('button', { name: 'Zoom in' })).toBeHidden();
    await expect(page.getByRole('button', { name: 'Close about' })).toBeVisible();
  });
});
