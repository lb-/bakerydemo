import { resolve } from 'path';
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    emptyOutDir: true,
    outDir: '../static/wryneck/',
    lib: {
      // Could also be a dictionary or array of multiple entry points
      entry: resolve(__dirname, 'lib/main.js'),
      formats: ['iife'],
      name: 'Wryneck',
      // the proper extensions will be added
      fileName: 'wryneck',
    },
    rollupOptions: {
      // make sure to externalize deps that shouldn't be bundled
      // into your library
      external: ['@hotwired/stimulus'],
      output: {
        // Provide global variables to use in the UMD build
        // for externalized deps
        globals: {
          "@hotwired/stimulus": 'window.Stimulus.constructor',
        },
      },
    },
  },
})