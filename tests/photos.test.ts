import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { ALLOWED_PHOTO_LICENSES, getProject, PHOTOS } from '../src/projects/data';

// Photos are openly licensed or public domain, copied into the build (never hotlinked), and
// always shown with their credit. Renderings need written permission and aren't listed here.
describe('project photos', () => {
  it('has at most one photo per project, each for a real project', () => {
    const ids = PHOTOS.map((p) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
    for (const id of ids) expect(getProject(id), id).toBeDefined();
  });

  it.each(PHOTOS.map((p) => [p.id, p] as const))('%s: allowed license with a full credit', (_id, p) => {
    expect(ALLOWED_PHOTO_LICENSES).toContain(p.license);
    expect(p.author.trim()).not.toBe('');
    expect(p.page).toMatch(/^https:\/\/commons\.wikimedia\.org\/wiki\/File:/);
    if (p.license.startsWith('CC BY')) {
      expect(p.licenseUrl).toMatch(/^https?:\/\/creativecommons\.org\/licenses\//);
      expect(p.modified).toBeTruthy();
    }
    expect(p.caption).toMatch(/^[A-Z].*\.$/);
    if (p.note) expect(p.note).toMatch(/^[A-Z].*\.$/);
  });

  it.each(PHOTOS.map((p) => [p.id, p] as const))('%s: the file is in the build and matches its hash', (_id, p) => {
    expect(p.src).toBe(`photos/${p.id}.jpg`);
    const path = `public/${p.src}`;
    expect(existsSync(path)).toBe(true);
    const bytes = readFileSync(path);
    expect(createHash('sha256').update(bytes).digest('hex')).toBe(p.sha256);
    expect(bytes.length).toBeLessThan(400_000);
  });
});
