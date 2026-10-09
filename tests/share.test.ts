import { existsSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import theme from '../src/theme/theme.json';
import { iconPng, iconSvg } from '../scripts/siteMeta';

describe('sharing', () => {
  it('has a link-preview card drawn with the current palette', () => {
    // After a palette change, redraw it: `npm run share-card` with the dev server running.
    expect(existsSync('public/share-card.png')).toBe(true);
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
});
