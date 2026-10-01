// Build MapLibre SDF glyph PBFs from the static font instances made by
// pipeline/bam_pipeline/fonts.py. Writes public/generated/glyphs/{Font Name}/{start}-{end}.pbf
// for every 256-codepoint range the font actually covers.
//
//   npm run glyphs

import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import { join, basename } from 'node:path';
import { promisify } from 'node:util';
import fontnik from 'fontnik';

const load = promisify(fontnik.load);
const range = promisify(fontnik.range);

const SRC = 'data/build/fonts';
const OUT = 'public/generated/glyphs';

const files = (await readdir(SRC)).filter((f) => f.endsWith('.ttf'));
if (files.length === 0) {
  console.error(`[glyphs] no fonts in ${SRC}; run the fonts pipeline step first`);
  process.exit(1);
}

for (const file of files) {
  const name = basename(file, '.ttf');
  const buf = await readFile(join(SRC, file));
  const [face] = await load(buf);
  const starts = [...new Set(face.points.map((p) => Math.floor(p / 256) * 256))]
    .filter((s) => s < 65536)
    .sort((a, b) => a - b);
  const dir = join(OUT, name);
  await mkdir(dir, { recursive: true });
  for (const start of starts) {
    const end = start + 255;
    const pbf = await range({ font: buf, start, end });
    await writeFile(join(dir, `${start}-${end}.pbf`), pbf);
  }
  console.log(`[glyphs] ${name}: ${starts.length} ranges`);
}
