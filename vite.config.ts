/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';
import { projectPages } from './scripts/projectPages.ts';
import { siteMeta } from './scripts/siteMeta.ts';

export default defineConfig({
  // The deploy workflow sets BASE_PATH (and SITE_URL) to wherever GitHub Pages serves the site:
  // /BAM/ on github.io, / on the custom domain (map.matthewhuguet.com).
  base: process.env.BASE_PATH ?? '/',
  plugins: [preact(), siteMeta(import.meta.dirname), projectPages(import.meta.dirname)],
  server: { port: 5173, strictPort: true },
  preview: { port: 4173, strictPort: true },
  // MapLibre alone is about 1 MB minified, so the default 500 kB warning always fires.
  build: { target: 'es2022', sourcemap: true, chunkSizeWarningLimit: 1400 },
  test: { include: ['tests/**/*.test.ts'] },
});
