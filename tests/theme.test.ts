import { readFileSync } from 'node:fs';
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
    // Proposed (#9DB4E0) is about 2.1:1 on white.
    expect(issues).toContain('Stage: proposed/land');
  });

  it('draws the selection boundary on a light ground it contrasts with', () => {
    expect(contrastIssues(defaultTheme).filter((i) => i.subject === 'Selection')).toEqual([]);
    const dark = normalizeTheme({ colors: { selectionFill: '#333333' } });
    expect(contrastIssues(dark).map((i) => `${i.subject}/${i.against}`)).toContain('Selection/site ground');
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

// The interface's muted text is panel text mixed toward transparent (styles.css). Every such tone, in
// the index and its tabs, the project and about panels, photo credits and the stage key, must keep
// 4.5:1 on the panel, as must stage colors used as text (a paused or distressed project's label).
describe('interface text contrast', () => {
  const css = readFileSync('src/styles.css', 'utf8');
  const rules = [...css.matchAll(/([^{}]+)\{([^{}]*)\}/g)].map(([, sel, body]) => ({ sel: sel.trim(), body }));
  const muted = rules.flatMap(({ sel, body }) =>
    [...body.matchAll(/(?:^|[;\s])color:\s*color-mix\(in srgb, var\(--color-panel-text\) (\d+(?:\.\d+)?)%, transparent\)/g)]
      .map((m) => ({ sel, pct: Number(m[1]) })));

  it('finds the muted text tones', () => {
    expect(muted.length).toBeGreaterThan(10);
    for (const s of ['.category-tabs button', '.photo .credit', '.about-panel .notes', ".stage-toggle[aria-pressed='false']"]) {
      expect(muted.some((m) => m.sel.includes(s)), s).toBe(true);
    }
  });

  it('gives every muted text tone 4.5:1 on the panel', () => {
    const { panelText, panelBackground } = defaultTheme.colors;
    const low = muted
      .map((m) => ({ ...m, ratio: contrast(over(panelText, m.pct / 100, panelBackground), panelBackground) }))
      .filter((m) => m.ratio < 4.5)
      .map((m) => `${m.sel} (${m.pct}%): ${m.ratio.toFixed(2)}:1`);
    expect(low).toEqual([]);
  });

  it('gives off-ramp stage colors used as text 4.5:1 on the panel', () => {
    for (const s of ['paused', 'distressed'] as const) {
      expect(contrast(stageColor(defaultTheme, s), defaultTheme.colors.panelBackground), s).toBeGreaterThanOrEqual(4.5);
    }
  });

  it('outlines fields and filters at 3:1 on the panel (WCAG 1.4.11)', () => {
    expect(contrast(defaultTheme.colors.controlBorder, defaultTheme.colors.panelBackground)).toBeGreaterThanOrEqual(3);
  });

  it('gives labels and the byline 4.5:1 on land', () => {
    expect(contrast(defaultTheme.colors.labels, defaultTheme.colors.land)).toBeGreaterThanOrEqual(4.5);
  });
});
