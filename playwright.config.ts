import { defineConfig, devices } from '@playwright/test';

// Headless Chromium renders WebGL2 through SwiftShader. Screenshots are for review,
// not pixel-diff tests: software rendering is slower and not identical to a GPU.
export default defineConfig({
  testDir: 'tests',
  testMatch: /.*\.spec\.ts/,
  timeout: 180_000,
  fullyParallel: false,
  workers: 1,
  reporter: [['list']],
  use: {
    baseURL: 'http://127.0.0.1:5173',
    launchOptions: {
      args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
    },
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'npx vite --host 127.0.0.1',
    url: 'http://127.0.0.1:5173',
    reuseExistingServer: true,
    timeout: 60_000,
  },
});
