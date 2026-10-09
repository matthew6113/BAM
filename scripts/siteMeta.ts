import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { deflateSync } from 'node:zlib';
import type { Plugin } from 'vite';

/**
 * Sharing and identity tags for every page:
 * - link previews: og:image (public/share-card.png, made by `npm run share-card`), og:url and a
 *   canonical link, from SITE_URL (the deploy workflow passes the address GitHub Pages reports, so
 *   it is map.matthewhuguet.com once the custom domain is set, and github.io/BAM before);
 * - the icon: an ink tile with a stage-coloured dot, drawn from src/theme/theme.json at build time,
 *   so swapping the palette updates it too. SVG for browsers, PNGs for Safari and iOS home screens.
 * Without SITE_URL (local builds, dev) the absolute tags are left out.
 */

export const SHARE_CARD = { file: 'share-card.png', width: 1200, height: 630 };

interface ThemeColors {
  colors: Record<string, string>;
  stages: Record<string, string>;
}

function iconColors(root: string): { ink: string; dot: string } {
  const theme = JSON.parse(readFileSync(resolve(root, 'src/theme/theme.json'), 'utf8')) as ThemeColors;
  const resolveRef = (v: string) => (v.startsWith('@') ? theme.colors[v.slice(1)] : v);
  return { ink: resolveRef(theme.colors.buildings), dot: resolveRef(theme.stages.entitlement) };
}

export function iconSvg(ink: string, dot: string): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="${ink}"/>`
    + `<circle cx="16" cy="16" r="7.5" fill="${dot}"/></svg>`;
}

const hex = (c: string): [number, number, number] => {
  const h = c.replace('#', '');
  return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
};

/** The same icon as a PNG (4x4 supersampled), for browsers and devices that don't take SVG icons. */
export function iconPng(size: number, ink: string, dot: string): Buffer {
  const [ir, ig, ib] = hex(ink);
  const [dr, dg, db] = hex(dot);
  const s = size / 32;
  const radius = 7 * s;
  const dotR = 7.5 * s;
  const c = size / 2;
  const insideTile = (x: number, y: number) => {
    const qx = Math.max(radius - x, 0, x - (size - radius));
    const qy = Math.max(radius - y, 0, y - (size - radius));
    return qx * qx + qy * qy <= radius * radius;
  };
  const rows: Buffer[] = [];
  for (let y = 0; y < size; y++) {
    const row = Buffer.alloc(1 + size * 4);
    for (let x = 0; x < size; x++) {
      let tile = 0;
      let disc = 0;
      for (let sy = 0; sy < 4; sy++) {
        for (let sx = 0; sx < 4; sx++) {
          const px = x + (sx + 0.5) / 4;
          const py = y + (sy + 0.5) / 4;
          if (insideTile(px, py)) {
            tile++;
            if ((px - c) ** 2 + (py - c) ** 2 <= dotR * dotR) disc++;
          }
        }
      }
      const a = tile / 16;
      const mix = tile ? disc / tile : 0;
      const o = 1 + x * 4;
      row[o] = Math.round(ir + (dr - ir) * mix);
      row[o + 1] = Math.round(ig + (dg - ig) * mix);
      row[o + 2] = Math.round(ib + (db - ib) * mix);
      row[o + 3] = Math.round(a * 255);
    }
    rows.push(row);
  }
  const crcTable = Array.from({ length: 256 }, (_, n) => {
    let k = n;
    for (let i = 0; i < 8; i++) k = k & 1 ? 0xedb88320 ^ (k >>> 1) : k >>> 1;
    return k >>> 0;
  });
  const crc32 = (buf: Buffer) => {
    let k = 0xffffffff;
    for (const b of buf) k = crcTable[(k ^ b) & 0xff] ^ (k >>> 8);
    return (k ^ 0xffffffff) >>> 0;
  };
  const chunk = (type: string, data: Buffer) => {
    const len = Buffer.alloc(4);
    len.writeUInt32BE(data.length);
    const body = Buffer.concat([Buffer.from(type, 'ascii'), data]);
    const crc = Buffer.alloc(4);
    crc.writeUInt32BE(crc32(body));
    return Buffer.concat([len, body, crc]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // RGBA
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', deflateSync(Buffer.concat(rows))),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}

const escapeAttr = (s: string) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');

export function siteMeta(root: string): Plugin {
  const site = process.env.SITE_URL?.replace(/\/+$/, '');
  let base = '/';
  let building = false;
  return {
    name: 'bam-site-meta',
    configResolved(config) {
      base = config.base;
      building = config.command === 'build';
    },
    transformIndexHtml(html) {
      const { ink, dot } = iconColors(root);
      const svg = `data:image/svg+xml,${encodeURIComponent(iconSvg(ink, dot))}`;
      const tags = [
        `<link rel="icon" type="image/svg+xml" href="${escapeAttr(svg)}" />`,
        ...(building
          ? [
              `<link rel="icon" type="image/png" sizes="32x32" href="${base}favicon-32.png" />`,
              `<link rel="apple-touch-icon" href="${base}apple-touch-icon.png" />`,
            ]
          : []),
        ...(site
          ? [
              `<link rel="canonical" href="${site}/" />`,
              `<meta property="og:url" content="${site}/" />`,
              `<meta property="og:image" content="${site}/${SHARE_CARD.file}" />`,
              `<meta property="og:image:width" content="${SHARE_CARD.width}" />`,
              `<meta property="og:image:height" content="${SHARE_CARD.height}" />`,
              `<meta property="og:image:alt" content="Bay Area megaprojects: a map of the region's largest developments, by Matthew Huguet" />`,
              `<meta name="twitter:image" content="${site}/${SHARE_CARD.file}" />`,
            ]
          : []),
      ];
      return html.replace(/\s*<link rel="icon" href="data:," \/>/, () => `\n    ${tags.join('\n    ')}`);
    },
    generateBundle() {
      const { ink, dot } = iconColors(root);
      this.emitFile({ type: 'asset', fileName: 'favicon-32.png', source: iconPng(32, ink, dot) });
      this.emitFile({ type: 'asset', fileName: 'apple-touch-icon.png', source: iconPng(180, ink, dot) });
    },
  };
}

/** The absolute site address the build was made for, if any (used by the project pages). */
export const siteUrl = () => process.env.SITE_URL?.replace(/\/+$/, '');
