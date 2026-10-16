import { readFileSync } from 'node:fs';
import type { Plugin } from 'vite';

/**
 * Trims the data the browser downloads, without changing anything it draws or shows:
 * - the traced GeoJSON in data/ (imported with ?raw) loses its pretty-printing whitespace. The
 *   files stay readable in the repo; the parsed geometry is identical (about half the characters,
 *   ~12 KB gzip off the main bundle, more off the per-project massing and land-use chunks);
 * - data/projects.json loses the fields the app never reads (CLIENT_OMITTED_FIELDS), and a project's
 *   `reported` record (press-only facts the map never shows) becomes `true`, so the panel still
 *   knows to say that reported details are held back.
 * Tests (Vitest) read the data untouched. A field that the UI starts showing must come off the list.
 */
export const CLIENT_OMITTED_FIELDS = ['massingNotes', 'acresNote', 'nextMilestone'] as const;

const GEOJSON_RAW = /[\\/]data[\\/](boundaries|lines|massing|landuse)[\\/][^\\/]+\.geojson\?raw$/;
const PROJECTS_JSON = /[\\/]data[\\/]projects\.json$/;

export function clientProjects(json: string): string {
  const data = JSON.parse(json) as { projects: Record<string, unknown>[] };
  for (const p of data.projects) {
    for (const f of CLIENT_OMITTED_FIELDS) delete p[f];
    if ('reported' in p) p.reported = true;
  }
  return JSON.stringify(data);
}

export function clientData(): Plugin {
  return {
    name: 'bam-client-data',
    enforce: 'pre',
    async load(id) {
      if (!GEOJSON_RAW.test(id)) return null;
      const file = id.replace(/\?raw$/, '');
      this.addWatchFile(file);
      const min = JSON.stringify(JSON.parse(readFileSync(file, 'utf8')));
      // No source map: the data is not code, and a map would carry a second copy of it.
      return { code: `export default ${JSON.stringify(min)};`, map: { mappings: '' } };
    },
    transform(code, id) {
      if (process.env.VITEST || !PROJECTS_JSON.test(id)) return null;
      return { code: clientProjects(code), map: null };
    },
  };
}
