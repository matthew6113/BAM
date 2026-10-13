import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';

// The web fonts keep only the characters in WEB_UNICODES (pipeline/bam_pipeline/fonts.py). A character
// outside it still shows, but in a fallback system font, so the data and the interface must stay inside.
const FONTS_PY = readFileSync('pipeline/bam_pipeline/fonts.py', 'utf8');
const LIST = /WEB_UNICODES = \(([^)]*)\)/.exec(FONTS_PY)?.[1] ?? '';
const RANGES = [...LIST.matchAll(/U\+([0-9A-F]+)(?:-([0-9A-F]+))?/g)]
  .map((m) => [parseInt(m[1], 16), parseInt(m[2] ?? m[1], 16)] as const);

const covered = (cp: number) => cp === 0x0a || RANGES.some(([a, b]) => cp >= a && cp <= b);

const files = (dir: string, ext: RegExp): string[] =>
  readdirSync(dir, { recursive: true, encoding: 'utf8' }).filter((f) => ext.test(f)).map((f) => join(dir, f));

const GEOMETRY = ['boundaries', 'massing', 'landuse', 'lines'].flatMap((d) => files(`data/${d}`, /\.geojson$/));
const DATA = ['data/projects.json', 'data/photos.json', ...GEOMETRY];
const SOURCE = files('src', /\.tsx?$/);

describe('web font subset', () => {
  it('reads the character list from the font pipeline', () => {
    expect(RANGES.length).toBeGreaterThan(3);
    expect(covered('a'.codePointAt(0)!)).toBe(true);
  });

  it('covers every character the data and the interface can show', () => {
    const missing = new Map<string, string>();
    for (const file of [...DATA, ...SOURCE]) {
      const code = SOURCE.includes(file);
      for (const ch of readFileSync(file, 'utf8')) {
        // Combining marks in source code are regex ranges (accent folding in search), not text.
        if (code && /\p{Mn}/u.test(ch)) continue;
        if (!covered(ch.codePointAt(0)!) && !missing.has(ch)) missing.set(ch, file);
      }
    }
    const hex = (ch: string) => ch.codePointAt(0)!.toString(16).toUpperCase().padStart(4, '0');
    const list = [...missing].map(([ch, file]) => `U+${hex(ch)} ${ch} (${file})`);
    expect(list, 'add these to WEB_UNICODES in pipeline/bam_pipeline/fonts.py').toEqual([]);
  });
});
