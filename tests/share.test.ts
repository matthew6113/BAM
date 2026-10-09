import { existsSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import theme from '../src/theme/theme.json';
import { iconPng, iconSvg } from '../scripts/siteMeta';
import { retitle } from '../scripts/projectPages';

describe('sharing', () => {
  it('has a link-preview card', () => {
    expect(existsSync('public/share-card.png')).toBe(true);
  });

  // Local only: a palette swap shouldn't block a deploy, but the card should be redrawn before the
  // next one (`npm run share-card`, see docs/share/README.md). CI sets CI=true.
  it.skipIf(!!process.env.CI)('drew the card with the current palette', () => {
    const drawn = JSON.parse(readFileSync('public/share-card.json', 'utf8'));
    expect(drawn.colors).toEqual(theme.colors);
    expect(drawn.stages).toEqual(theme.stages);
  });

  it('draws the icon from the theme as SVG and PNG', () => {
    expect(iconSvg('#111111', '#c04e1c')).toContain('fill="#c04e1c"');
    const png = iconPng(32, '#111111', '#c04e1c');
    expect(png.subarray(1, 4).toString('ascii')).toBe('PNG');
    expect(png.readUInt32BE(16)).toBe(32);
  });

  it('keeps dollar amounts in project page titles and descriptions', () => {
    const html = '<title>x</title><meta name="description" content="x" />'
      + '<meta property="og:title" content="x" /><meta property="og:description" content="x" />';
    const out = retitle(html, 'SMART · $1 test', 'Funded at about $269 million, $& more, $2.', 'p/x/');
    expect(out).toContain('<title>SMART · $1 test</title>');
    expect(out).toContain('content="Funded at about $269 million, $&amp; more, $2."');
    expect(out.match(/\$269 million/g)).toHaveLength(2);
  });
});
