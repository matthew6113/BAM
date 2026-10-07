// Dev helper: serve the deployed site's generated tiles, glyphs and labels (for containers without `make data`).
import base from './vite.config';
import { mergeConfig } from 'vite';
export default mergeConfig(base, {
  server: {
    port: 5180,
    proxy: { '/generated': { target: 'https://matthew6113.github.io/BAM', changeOrigin: true, secure: true } },
  },
});
