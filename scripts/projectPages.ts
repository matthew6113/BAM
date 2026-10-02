import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import type { Plugin } from 'vite';
import data from '../data/projects.json' with { type: 'json' };

const escape = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** Swap the page's title and description (plain and Open Graph) for a project's. */
function retitle(html: string, title: string, description: string): string {
  const t = escape(title);
  const d = escape(description);
  return html
    .replace(/<title>[^<]*<\/title>/, `<title>${t}</title>`)
    .replace(/(<meta name="description" content=")[^"]*(")/, `$1${d}$2`)
    .replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${t}$2`)
    .replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${d}$2`);
}

/**
 * Static hosts have no rewrites, so every deep link gets a real page: dist/p/{id}/index.html
 * is the app with that project's title and summary (for link previews), and dist/404.html
 * catches anything else. The app reads the path and opens the project with the fly-in.
 */
export function projectPages(root: string): Plugin {
  return {
    name: 'bam-project-pages',
    apply: 'build',
    // After Vite's own HTML plugin has emitted index.html.
    enforce: 'post',
    generateBundle(_options, bundle) {
      const index = bundle['index.html'];
      if (!index || index.type !== 'asset') return;
      const html = String(index.source);
      const site = /<title>([^<]*)<\/title>/.exec(html)?.[1] ?? '';
      for (const p of data.projects) {
        // Only projects drawn on the map get a page; the rest arrive with Milestone 3.
        if (!existsSync(resolve(root, 'data/boundaries', `${p.id}.geojson`))) continue;
        this.emitFile({
          type: 'asset',
          fileName: `p/${p.id}/index.html`,
          source: retitle(html, `${p.name} · ${site}`, p.summary),
        });
      }
      this.emitFile({ type: 'asset', fileName: '404.html', source: html });
    },
  };
}
