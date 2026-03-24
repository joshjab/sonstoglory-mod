/**
 * Fetches the latest videos from Paul's YouTube channel RSS feed and writes
 * them to src/data/videos.json for use at build time.
 *
 * Runs as a prebuild step: `node scripts/fetch-youtube-feed.mjs`
 * Fails silently (keeps existing videos.json) if the network is unavailable.
 */

import { writeFileSync, existsSync, readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = resolve(__dirname, '../src/data/videos.json');

const CHANNEL_ID = 'UCNcpfgCgr1RavvcWZXSb9kA';
const FEED_URL = `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`;

function extractTag(xml, tag) {
  const m = xml.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`));
  return m ? m[1].trim() : '';
}

function extractAttr(xml, tag, attr) {
  const m = xml.match(new RegExp(`<${tag}[^>]*\\s${attr}="([^"]*)"[^>]*>`));
  return m ? m[1] : '';
}

function parseEntries(xml) {
  const entries = [];
  const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
  let m;
  while ((m = entryRegex.exec(xml)) !== null) {
    const entry = m[1];
    const id = extractTag(entry, 'yt:videoId');
    const title = extractTag(entry, 'title')
      .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');
    const published = extractTag(entry, 'published');
    const thumbnail = extractAttr(entry, 'media:thumbnail', 'url');
    if (id && title) {
      entries.push({ id, title, published, thumbnail });
    }
  }
  return entries;
}

try {
  console.log('[youtube] Fetching RSS feed...');
  const res = await fetch(FEED_URL, { signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const xml = await res.text();
  const videos = parseEntries(xml);
  writeFileSync(OUT, JSON.stringify(videos, null, 2));
  console.log(`[youtube] Wrote ${videos.length} videos to src/data/videos.json`);
} catch (err) {
  if (existsSync(OUT)) {
    console.warn(`[youtube] Fetch failed (${err.message}) — using existing videos.json`);
  } else {
    console.warn(`[youtube] Fetch failed (${err.message}) — writing empty fallback`);
    writeFileSync(OUT, '[]');
  }
}
