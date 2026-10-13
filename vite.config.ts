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
  build: {
    target: 'es2022',
    sourcemap: true,
    // MapLibre alone is about 1 MB minified, so the default 500 kB warning always fires.
    chunkSizeWarningLimit: 1400,
    rolldownOptions: {
      output: {
        // MapLibre in a file of its own: its name only changes when MapLibre does, so a returning
        // visitor's browser keeps it across deploys instead of downloading it with every data update.
        codeSplitting: { groups: [{ name: 'maplibre', test: /[\\/]node_modules[\\/]maplibre-gl[\\/]/ }] },
      },
    },
  },
  test: { include: ['tests/**/*.test.ts'] },
});
