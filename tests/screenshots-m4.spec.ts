// Milestone 4 screenshots: projects with traced 3D massing, landed after the fly-in.
//   npx playwright test tests/screenshots-m4.spec.ts         -> docs/screenshots/m4/
//   SHOTS_DIR=some/dir npx playwright test tests/screenshots-m4.spec.ts

import { test, expect, type Page } from '@playwright/test';

const DIR = process.env.SHOTS_DIR ?? 'docs/screenshots/m4';
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

for (const [n, id] of [
  ['01', 'balboa-reservoir'],
  ['02', 'mission-rock'],
  ['03', 'pier-70'],
  ['04', 'stonestown'],
  ['05', 'india-basin'],
  ['06', 'candlestick-point'],
  ['07', 'hunters-point-shipyard'],
  ['08', 'treasure-island'],
  ['09', 'mission-bay'],
  ['11', 'parkmerced'],
  ['12', 'parkline'],
  ['13', 'willow-village'],
  ['14', 'related-santa-clara'],
  ['15', 'downtown-west'],
  ['16', 'the-rise'],
  ['17', 'alameda-point'],
  ['18', 'brooklyn-basin'],
  ['19', 'moffett-park'],
  ['20', 'north-bayshore'],
  ['21', 'concord-naval-weapons-station'],
  ['22', 'suisun-expansion'],
  ['23', 'brisbane-baylands'],
  ['24', 'tasman-east'],
  ['25', 'sunnydale-hope-sf'],
  ['26', 'potrero-hope-sf'],
  ['27', 'middlefield-park'],
  ['28', 'schlage-lock'],
  ['29', 'berryessa-flea-market'],
  ['30', 'mare-island'],
  ['31', 'sonoma-developmental-center'],
  ['32', 'esmeralda'],
  ['33', 'bart-station-housing'],
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
