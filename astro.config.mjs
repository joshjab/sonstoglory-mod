// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// NOTE: Root-relative asset paths in Markdown content (<img src="/images/...">,
// <a href="/pdfs/...">) are rebased to include the GitHub Pages base path via
// scripts/rebase-assets.mjs, which runs as part of `npm run build`.
// When the site moves to a custom domain at root, remove that script and revert
// `base` here to the real site URL with no subdirectory.

const base = '/sonstoglory-mod';

export default defineConfig({
  site: 'https://joshjab.github.io/sonstoglory-mod',
  base,
  integrations: [tailwind(), sitemap()],
});
