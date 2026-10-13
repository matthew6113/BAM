import { describe, expect, it } from 'vitest';
import data from '../data/projects.json' with { type: 'json' };
import { areaOf, isLineProject, MAPPED_PROJECTS, siteOf } from '../src/projects/data';
import { handover, handoverZoom, LAST_DOT_ZOOM } from '../src/map/handover';

const ACRE_M2 = 4046.856;

describe('dots and site shapes', () => {
  it('measures a site’s area', () => {
    // Candlestick Point's boundary is DataSF's (about 271.1 acres); the record gives 272.
    const acres = areaOf(siteOf('candlestick-point')!.geometry) / ACRE_M2;
    const record = data.projects.find((p) => p.id === 'candlestick-point')!.acres!;
    expect(Math.abs(acres - record) / record).toBeLessThan(0.02);
  });

  it('hands every site over from its dot by street level', () => {
    for (const p of MAPPED_PROJECTS.filter((p) => !isLineProject(p.id))) {
      const at = handoverZoom(p.id);
      expect(Number.isFinite(at), p.id).toBe(true);
      expect(at, p.id).toBeLessThanOrEqual(LAST_DOT_ZOOM);
    }
  });

  it('draws a big site as its shape from the whole-bay view, and keeps a small one a dot', () => {
    // The whole-bay view is about zoom 8.9 on a 1440 × 900 screen.
    expect(handoverZoom('concord-naval-weapons-station')).toBeLessThan(8.9);
    expect(handoverZoom('30-van-ness')).toBe(LAST_DOT_ZOOM);
    expect(handoverZoom('treasure-island')).toBeLessThan(handoverZoom('mission-rock'));
  });

  it('swaps the dot for the shape at the handover zoom', () => {
    expect(handover(10, 9.99)).toBe(0);
    expect(handover(10, 10)).toBe(1);
    expect(handover(10, 12)).toBe(1);
  });
});
