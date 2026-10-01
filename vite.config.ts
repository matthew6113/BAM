/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  plugins: [preact()],
  server: { port: 5173, strictPort: true },
  preview: { port: 4173, strictPort: true },
  // MapLibre alone is about 1 MB minified, so the default 500 kB warning always fires.
  build: { target: 'es2022', sourcemap: true, chunkSizeWarningLimit: 1400 },
  test: { include: ['tests/**/*.test.ts'] },
});
