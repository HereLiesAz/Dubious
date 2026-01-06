import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  resolve: {
    alias: {
      $lib: path.resolve('./Src/lib'),
    },
  },
  // REPLACE '/dubious/' with '/<your-repo-name>/'
  base: '/dubious/',
})
