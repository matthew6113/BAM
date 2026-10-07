import defaults from './theme.json';

export type ColorRole = keyof typeof defaults.colors;
export type StageKey = keyof typeof defaults.stages;
export type Theme = typeof defaults;

export const STAGE_KEYS = Object.keys(defaults.stages) as StageKey[];
export const COLOR_ROLES = Object.keys(defaults.colors) as ColorRole[];

export const defaultTheme: Theme = structuredClone(defaults);

/** Stage colors may point at a color role ("@buildings" = complete matches the city). */
export function stageColor(theme: Theme, stage: StageKey): string {
  const value = theme.stages[stage];
  if (value.startsWith('@')) {
    const role = value.slice(1) as ColorRole;
    return theme.colors[role] ?? '#ff00ff';
  }
  return value;
}

/** Fill in anything an imported or older theme lacks, so the map never sees undefined. */
export function normalizeTheme(input: unknown): Theme {
  const t = (input ?? {}) as Partial<Theme>;
  const merged: Theme = structuredClone(defaultTheme);
  if (typeof t.name === 'string') merged.name = t.name;
  if (typeof t.note === 'string') merged.note = t.note;
  Object.assign(merged.colors, pickStrings(t.colors));
  Object.assign(merged.stages, pickStrings(t.stages));
  Object.assign(merged.opacity, pickNumbers(t.opacity));
  if (t.massing) Object.assign(merged.massing.opacity, pickNumbers(t.massing.opacity));
  if (t.landUse) {
    Object.assign(merged.landUse.colors, pickStrings(t.landUse.colors));
    if (typeof t.landUse.opacity === 'number') merged.landUse.opacity = t.landUse.opacity;
  }
  Object.assign(merged.type, pickStrings(t.type));
  if (t.map) {
    if (typeof t.map.shorelineWidth === 'number') merged.map.shorelineWidth = t.map.shorelineWidth;
    if (typeof t.map.heightExaggeration === 'number') merged.map.heightExaggeration = t.map.heightExaggeration;
    Object.assign(merged.map.light, pickNumbers(t.map.light));
    if (typeof t.map.light?.color === 'string') merged.map.light.color = t.map.light.color;
  }
  if (t.layers) {
    for (const [k, v] of Object.entries(t.layers)) {
      if (k in merged.layers && typeof v === typeof (merged.layers as Record<string, unknown>)[k]) {
        (merged.layers as Record<string, unknown>)[k] = v;
      }
    }
  }
  return merged;
}

function pickStrings(o: unknown): Record<string, string> {
  const out: Record<string, string> = {};
  if (o && typeof o === 'object') {
    for (const [k, v] of Object.entries(o)) if (typeof v === 'string') out[k] = v;
  }
  return out;
}

function pickNumbers(o: unknown): Record<string, number> {
  const out: Record<string, number> = {};
  if (o && typeof o === 'object') {
    for (const [k, v] of Object.entries(o)) if (typeof v === 'number' && Number.isFinite(v)) out[k] = v;
  }
  return out;
}

/** Expose the theme to CSS as custom properties on :root. */
export function applyCssVariables(theme: Theme, root: HTMLElement = document.documentElement): void {
  for (const role of COLOR_ROLES) root.style.setProperty(`--color-${kebab(role)}`, theme.colors[role]);
  for (const stage of STAGE_KEYS) root.style.setProperty(`--stage-${stage}`, stageColor(theme, stage));
  for (const [cat, color] of Object.entries(theme.landUse.colors)) root.style.setProperty(`--landuse-${cat}`, color);
  root.style.setProperty('--font-ui', `'${theme.type.ui}', system-ui, sans-serif`);
  root.style.setProperty('--font-text', `'${theme.type.text}', Georgia, serif`);
}

function kebab(s: string): string {
  return s.replace(/[A-Z]/g, (m) => `-${m.toLowerCase()}`);
}

// ---------------------------------------------------------------- contrast checks

function channel(c: number): number {
  const s = c / 255;
  return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
}

export function luminance(hex: string): number {
  const m = /^#?([0-9a-f]{6})$/i.exec(hex.trim());
  if (!m) return NaN;
  const n = parseInt(m[1], 16);
  return 0.2126 * channel((n >> 16) & 255) + 0.7152 * channel((n >> 8) & 255) + 0.0722 * channel(n & 255);
}

/** WCAG contrast ratio between two #rrggbb colors. */
export function contrast(a: string, b: string): number {
  const la = luminance(a);
  const lb = luminance(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

/** Composite a color at an opacity over a background (both #rrggbb). */
export function over(fg: string, alpha: number, bg: string): string {
  const f = parseInt(fg.slice(1), 16);
  const b = parseInt(bg.slice(1), 16);
  const mix = (shift: number) =>
    Math.round(((f >> shift) & 255) * alpha + ((b >> shift) & 255) * (1 - alpha));
  return `#${[16, 8, 0].map((s) => mix(s).toString(16).padStart(2, '0')).join('')}`;
}

export interface ContrastIssue {
  subject: string;
  against: string;
  ratio: number;
  needed: number;
}

/**
 * Palette checks from the planning audit: stage colors are graphics (WCAG 1.4.11,
 * 3:1 against land and water), labels are text (4.5:1).
 */
export function contrastIssues(theme: Theme): ContrastIssue[] {
  const issues: ContrastIssue[] = [];
  const grounds: [string, string][] = [
    ['land', theme.colors.land],
    ['water', theme.colors.water],
  ];
  for (const stage of STAGE_KEYS) {
    const c = stageColor(theme, stage);
    for (const [name, bg] of grounds) {
      const ratio = contrast(c, bg);
      if (ratio < 3) issues.push({ subject: `Stage: ${stage}`, against: name, ratio, needed: 3 });
    }
  }
  for (const [name, bg] of grounds) {
    const ratio = contrast(theme.colors.labels, bg);
    if (ratio < 4.5) issues.push({ subject: 'Labels', against: name, ratio, needed: 4.5 });
  }
  // The boundary sits on the selected site's ground (selectionFill), not on the building ink.
  const sel = contrast(theme.colors.selection, theme.colors.selectionFill);
  if (sel < 3) issues.push({ subject: 'Selection', against: 'site ground', ratio: sel, needed: 3 });
  return issues;
}
