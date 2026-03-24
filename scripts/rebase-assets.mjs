/**
 * Post-build script: rewrites root-relative asset paths in dist/ HTML files
 * to include the GitHub Pages base path.
 *
 * Needed because pandoc outputs <img src="/images/..."> and <a href="/pdfs/...">
 * in Markdown content, and Astro does not rewrite raw HTML attributes inside
 * rendered Markdown when a base path is configured.
 *
 * Run automatically via the `build` script in package.json.
 * Remove (or skip by unsetting BASE) when the site moves to a custom domain at root.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

const BASE = process.env.SITE_BASE ?? '/sonstoglory-mod';
const DIST = './dist';

function walk(dir) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      walk(full);
    } else if (entry.endsWith('.html')) {
      let html = readFileSync(full, 'utf8');
      const before = html;
      // Rewrite root-relative src/href that don't already have the base prefix.
      // Negative lookahead (?!BASE) prevents double-prefixing nav links.
      // Negative lookahead (?!\/) prevents touching protocol-relative URLs (//).
      const escaped = BASE.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      html = html.replace(
        new RegExp(`\\bsrc="\/(?!${escaped.slice(1)})(?!\/)`, 'g'),
        `src="${BASE}/`
      );
      html = html.replace(
        new RegExp(`\\bhref="\/(?!${escaped.slice(1)})(?!\/)`, 'g'),
        `href="${BASE}/`
      );
      if (html !== before) writeFileSync(full, html);
    }
  }
}

walk(DIST);
console.log(`[rebase-assets] Rewrote asset paths with base: ${BASE}`);
