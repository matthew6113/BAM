import { readdirSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CLIENT_OMITTED_FIELDS, clientProjects } from '../scripts/clientData';

const raw = readFileSync('data/projects.json', 'utf8');
const source = (dir: string): string =>
  readdirSync(dir, { withFileTypes: true })
    .map((e) => (e.isDirectory() ? source(`${dir}/${e.name}`) : /\.tsx?$/.test(e.name) ? readFileSync(`${dir}/${e.name}`, 'utf8') : ''))
    .join('\n');

describe('the data the browser downloads', () => {
  const client = JSON.parse(clientProjects(raw));
  const full = JSON.parse(raw);

  it('leaves out only fields the app never reads', () => {
    const app = source('src');
    for (const f of CLIENT_OMITTED_FIELDS) expect(app, `src/ reads ${f}; take it off CLIENT_OMITTED_FIELDS`).not.toMatch(new RegExp(`\\b${f}\\b`));
    for (const p of client.projects) for (const f of CLIENT_OMITTED_FIELDS) expect(p).not.toHaveProperty(f);
  });

  it('keeps press-only facts out of the bundle but remembers that a project has them', () => {
    full.projects.forEach((p: Record<string, unknown>, i: number) => {
      expect('reported' in client.projects[i]).toBe('reported' in p);
      if ('reported' in p) expect(client.projects[i].reported).toBe(true);
    });
  });

  it('keeps everything else as it is', () => {
    full.projects.forEach((p: Record<string, unknown>, i: number) => {
      for (const [k, v] of Object.entries(p)) {
        if (k === 'reported' || (CLIENT_OMITTED_FIELDS as readonly string[]).includes(k)) continue;
        expect(client.projects[i][k], `${p.id}.${k}`).toEqual(v);
      }
    });
    expect(client.stages).toEqual(full.stages);
    expect(client._meta).toEqual(full._meta);
  });
});
