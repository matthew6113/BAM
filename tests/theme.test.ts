import { describe, expect, it } from 'vitest';
import themeJson from '../src/theme/theme.json';
import projects from '../data/projects.json';
import { contrast, contrastIssues, defaultTheme, normalizeTheme, over, stageColor, STAGE_KEYS } from '../src/theme/theme';

const HEX = /^#[0-9A-Fa-f]{6}$/;

describe('theme.json', () => {
  it('gives every color role a #rrggbb value', () => {
    for (const [role, value] of Object.entries(themeJson.colors)) expect(value, role).toMatch(HEX);
    expect(themeJson.map.light.color).toMatch(HEX);
  });

  it('has a color for every stage in projects.json', () => {
    for (const s of projects.stages) {
      expect(STAGE_KEYS, s.key).toContain(s.key);
      expect(stageColor(defaultTheme, s.key as (typeof STAGE_KEYS)[number])).toMatch(HEX);
    }
  });

  it('draws complete buildings in the same ink as the existing city', () => {
    expect(stageColor(defaultTheme, 'complete')).toBe(defaultTheme.colors.buildings);
  });
});

describe('contrast helpers', () => {
  it('computes WCAG ratios', () => {
    expect(contrast('#000000', '#FFFFFF')).toBeCloseTo(21, 5);
    expect(contrast('#FFFFFF', '#FFFFFF')).toBeCloseTo(1, 5);
  });

  it('composites ink over paper', () => {
    expect(over('#1E1E1E', 0.85, '#FFFFFF')).toBe('#404040');
  });

  it('gives every stage at least 3:1 against land and water', () => {
    const issues = contrastIssues(defaultTheme).filter((i) => i.subject.startsWith('Stage'));
    expect(issues).toEqual([]);
  });

  it('still reports the old blue palette issues found in the planning audit', () => {
    const old = normalizeTheme({
      colors: { land: '#FFFFFF', water: '#ECEFF2', buildings: '#1E1E1E' },
      stages: { proposed: '#9DB4E0' },
    });
    const issues = contrastIssues(old).map((i) => `${i.subject}/${i.against}`);
    // Proposed (#9DB4E0) is about 2.1:1 on white; selection (#000) is about 2:1 on the ink.
    expect(issues).toContain('Stage: proposed/land');
    expect(issues).toContain('Selection/buildings');
  });
});

describe('normalizeTheme', () => {
  it('fills gaps from the defaults and ignores junk', () => {
    const t = normalizeTheme({ colors: { land: '#FAFAFA', bogus: 3 }, layers: { context: true, overview: 7 } });
    expect(t.colors.land).toBe('#FAFAFA');
    expect(t.colors.water).toBe(defaultTheme.colors.water);
    expect(t.layers.context).toBe(true);
    expect(t.layers.overview).toBe(defaultTheme.layers.overview);
  });
});
