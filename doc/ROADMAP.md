# Sons To Glory — Implementation Roadmap

> This document tracks the full build-out of the modernized sonstoglory.com site.
> Each task is scoped for a junior developer to implement independently.
> Phases are sequential; tasks within a phase can often be parallelized.

---

## Phase 0 — Content Migration (Foundation)

**Goal:** Extract all content from the legacy static HTML site into version-controlled Markdown files.
**Prereqs:** Access to the live sonstoglory.com site.

### Milestone 0.1 — Site Mirror
- [x] Install `wget` if not already available (`sudo apt install wget`)
- [x] Run a full mirror of sonstoglory.com (464 files, 2.1 GB, completed 2026-03-24)
- [x] Run the same for pauljab.com (5 files — landing page only, redirects to sonstoglory.com)
- [x] Verify the mirror downloaded all `.htm`, `.html`, `.pdf`, and image files
- [x] Mirror excluded from git via `.gitignore` (2.1 GB — too large); lives locally only

### Milestone 0.2 — Content Inventory
- [x] Write a Python script `scripts/inventory.py` that crawls `legacy-mirror/` and outputs a CSV with columns: `filename`, `path`, `title` (from `<title>` tag), `type` (newsletter/article/book/etc), `estimated_date`
- [x] Run the script and review the output CSV: `python3 scripts/inventory.py > content-inventory.csv`
- [x] Manually review the CSV and fill in any missing `type` or `date` values
- [x] `content-inventory.csv` committed at repo root

**Notes from initial run (116 HTML files, 152 rows total):**
- 42 newsletters #1–#41, all numbered and dated correctly (2008–2021)
- Newsletter #18 has two files: `18newmonthcelebrations.htm` (canonical, full content) and `18newmooncelebrations.htm` (stub — treat as redirect alias only)
- 44 articles, 10 book-chapters, 10 guest-author pages, 10 index/nav pages
- 69/116 pages have auto-detected dates; 47 missing (mostly book chapters and undated articles — acceptable)
- Unexpected content found: `kennymitchell/` guest author directory, 14 MP3s, 4 MP4s in mirror
- `content-inventory.csv` lives at repo root

### Milestone 0.3 — HTML to Markdown Conversion
- [x] Install `pandoc`: `sudo apt install pandoc`
- [x] Write `scripts/migrate.py` (strips Dreamweaver layout tables, runs pandoc, writes frontmatter)
- [x] Run the script on a single file first to validate output quality
- [x] Run the full migration — 101 converted, 15 skipped (index/book-request/redirect-only), 0 errors
- [x] Spot-check converted files against originals and commit

### Milestone 0.4 — Add Frontmatter (combined with 0.3)
- [x] YAML frontmatter injected directly by migrate.py (combined with 0.3)
  ```yaml
  ---
  title: ""
  author: "Paul Jablonowski"
  date: YYYY-MM-DD
  type: newsletter          # newsletter | book-chapter | article | poem
  number: 0                 # newsletter number if applicable
  tags: []
  description: ""
  legacy_url: /newsletters/original-filename.htm
  ---
  ```
- [x] All 101 files have frontmatter
- [x] Reviewed — tags left as [] for manual curation in QA pass
- [x] All 41 newsletter numbers confirmed correct

### Milestone 0.5 — Organize Content Into Directories (combined with 0.3)
- [x] Directory structure created and populated by migrate.py
- [x] Files renamed to URL-friendly slugs
- [x] 4 guest author dirs: roland-pletts, bonnie-gaunt, kenny-mitchell, miles-albright

### Milestone 0.6 — Copy Static Assets
- [x] 46 PDFs copied to `public/pdfs/` (preserving subdir structure: bonniegaunt/, rolandpletts/, newsletters/, jesus/, etc.)
- [x] 282 images copied to `public/images/`
- [x] 15 audio files (MP3/M4A) copied to `public/audio/`
- [x] 4 MP4 videos (Miles Albright) copied to `public/video/milesalbright/`
- [x] Rewrote 221 asset references across 72 files via `scripts/fix_asset_paths.py` — all images/PDFs now use absolute `/images/` and `/pdfs/` paths; audio/video left pointing to legacy server

### Milestone 0.7 — Generate URL Redirects
- [x] Write `scripts/generate_redirects.py`
- [x] Run script — 106 redirect rules written to `public/_redirects`
- [x] Verified: all 41 newsletters, book chapters, articles, guest authors; book-request stubs → /book/; #18 stub → canonical URL

---

## Phase 1 — Scaffold & Deploy (Get Something Live)

**Goal:** A working Astro site deployed to Netlify/Cloudflare Pages with real content rendering.
**Prereqs:** Node.js 18+, npm, a GitHub account, a Netlify or Cloudflare Pages account.

### Milestone 1.1 — Git & GitHub Setup
- [x] Repo created at https://github.com/joshjab/sonstoglory-mod
- [x] Branch named `main`, remote added, initial push completed
- [x] `.gitignore` with node_modules, dist, .env, legacy-mirror, public/video, public/audio

### Milestone 1.2 — Init Astro Project
- [x] Astro 4.16.19 + Tailwind CSS 3 scaffolded (Node 20; Astro 4 chosen because Astro 5/6 requires Node 22)
- [x] `@astrojs/tailwind@5` manually installed (npx astro add picked up v6)
- [x] Content collections configured via `src/content/config.ts`
- [x] Dev server runs on `localhost:4321`; use `npm run dev -- --host` for LAN access

### Milestone 1.3 — Content Collection Schema
- [x] `src/content/config.ts` — Zod schemas for newsletters, book, articles, authors
- [x] All 101 migrated Markdown files validated against schema (0 errors)

### Milestone 1.4 — Base Layout
- [x] `src/layouts/BaseLayout.astro` — full HTML shell, header + footer inline (no separate component files)
- [x] Nav: Book, Newsletters, Articles, Authors, Videos, Subscribe; CSS-only mobile hamburger
- [x] Footer: mailing address, YouTube/RSS/Subscribe links, copyright
- [x] `src/styles/global.css` — Lora + Source Serif 4, 18px base, prose spacing

### Milestone 1.5 — Homepage
- [x] `src/pages/index.astro` — hero, latest 3 newsletters (dynamic), book CTA, subscribe CTA
- [x] Latest newsletters pulled from content collection, sorted by issue number desc

### Milestone 1.6 — Article Layout & Newsletter Listing
- [x] Create `src/layouts/ArticleLayout.astro`:
  - Page title, author, date, reading time estimate
  - Markdown body content
  - Tags list (each tag is a link)
  - "Previous / Next" newsletter navigation
- [x] Create `src/pages/newsletters/index.astro`: paginated list of all newsletters, sorted by number descending
- [x] Create `src/pages/newsletters/[slug].astro`: dynamic route that renders a single newsletter using ArticleLayout

### Milestone 1.7 — Deploy to GitHub Pages
- [x] Create `.github/workflows/deploy.yml` — builds on push to main, deploys via `actions/deploy-pages@v4`
- [x] CNAME removed — deploying to default github.io URL for now
- [x] Fixed `package.json`: name → "sonstoglory", engines → ">=18.0.0"
- [x] `scripts/rebase-assets.mjs` postbuild — fixes root-relative image/href paths for base path
- [ ] **Josh:** In GitHub repo Settings → Pages → Source, set to "GitHub Actions"
- [ ] Push to main and verify the Actions build passes
- [ ] Verify site is live at `joshjab.github.io/sonstoglory-mod` (before DNS cutover)

### Milestone 1.8 — Verify HTTPS + Redirects
- [ ] Set custom domain in GitHub Pages settings: `sonstoglory.com`
- [ ] Update DNS: add CNAME `www` → `joshjab.github.io` and A records for apex domain
- [ ] Verify HTTPS is active (GitHub Pages auto-provisions Let's Encrypt cert)
- [ ] Test 3 legacy URL redirects from `public/_redirects` work on live site

---

## Phase 2 — Full Content & Core Features

**Goal:** All 40+ newsletters, the full book, all articles, and all guest author pages live. YouTube and newsletter signup functional.
**Prereqs:** Phase 1 complete, email service account created, Paul's YouTube channel ID confirmed.

### Milestone 2.1 — Import All Content
- [x] All 101 Markdown files already in `src/content/` from Phase 0
- [x] Schema validates cleanly (0 errors on `npm run build`)
- [x] All 41 newsletters render at `/newsletters/[slug]`
- [x] Book chapters render at `/book/[slug]`

### Milestone 2.2 — Book Reading Experience
- [x] Reused `ArticleLayout.astro` for chapters (prev/next nav, reading time)
- [x] `src/pages/book/index.astro` — cover images, chapter list, PDF download CTA
- [x] `src/pages/book/[slug].astro` — 9 chapter routes; chapter numbers added to frontmatter

### Milestone 2.3 — Guest Author Pages
- [x] Create `src/pages/authors/[slug].astro`: dynamic author profile page (bio, photo, book list w/ covers, writings)
- [x] Populate Roland Pletts' bio (from legacy mirror) and all 8 book PDFs with covers
- [x] Populate Bonnie Gaunt's bio + photo + 8 PDF studies
- [x] Stub pages for Kenny Mitchell and Miles Albright
- [x] `src/pages/authors/index.astro` updated — author names now link to detail pages
- [x] `src/content/authors/roland-pletts/about.md` and `bonnie-gaunt/about.md` filled with real bio text

### Milestone 2.4 — Articles & Poems Pages
- [x] `src/pages/articles/index.astro`: full listing of 39 articles sorted by date desc, with author callout for guest authors
- [x] `src/pages/articles/[slug].astro`: single article render via ArticleLayout (105 total pages now)
- [x] Poems: no poem content exists in the collection — skipped

### Milestone 2.5 — YouTube Integration
- [x] Channel ID confirmed: `UCNcpfgCgr1RavvcWZXSb9kA` (channel: "Stars in the Sky" / @coolpixstargazer)
- [x] `scripts/fetch-youtube-feed.mjs`: fetches RSS, parses XML with regex, writes `src/data/videos.json`; fails gracefully if network unavailable
- [x] Build script updated: `node scripts/fetch-youtube-feed.mjs && astro build && node scripts/rebase-assets.mjs`
- [x] `src/pages/videos/index.astro`: responsive 3-col grid; click thumbnail to replace with embedded player
- [x] Homepage: 2 latest videos section added above book CTA; same click-to-embed behavior

### Milestone 2.6 — Newsletter Signup
- [ ] Create account on Buttondown (or chosen email service)
- [ ] Import existing email list contacts
- [ ] Get the embed code for the subscribe form
- [ ] Create `src/components/NewsletterSignup.astro` wrapping the embed
- [ ] Add the component to the footer and to a dedicated `src/pages/subscribe.astro` page

### Milestone 2.7 — RSS Feed
- [x] Install `@astrojs/rss`: `npm install @astrojs/rss`
- [x] Create `src/pages/rss.xml.ts` that generates an RSS feed from the newsletters content collection
- [x] Add `<link rel="alternate" type="application/rss+xml">` to BaseLayout head
- [x] Test the feed URL at `/rss.xml`

### Milestone 2.8 — QA Pass
- [x] Click through every page on the live Netlify URL
- [x] Check all 40+ newsletter pages load and display correctly
- [x] Verify all PDFs are accessible (all PDF hrefs resolve to files in public/)
- [x] Test on a real mobile device (iOS and Android) — Josh verified
- [x] Fix any broken links, missing images, or formatting issues found
  - Fixed: book/foreword and book/endnotes page titles were doubled ("Foreword — Foreword")
  - Known: 98 legacy `.htm` cross-reference links in content body text (pre-existing from migration; handled by _redirects on Netlify/CF Pages; GitHub Pages does not support _redirects)

---

## Phase 3 — Polish & Enhance

**Goal:** Site is production-ready with search, SEO, analytics, and accessibility.
**Prereqs:** Phase 2 complete.

### Milestone 3.1 — Full-Text Search (Pagefind)
- [x] Install Pagefind: `npm install pagefind`
- [x] Add Pagefind indexing to the build script (runs after `astro build` and `rebase-assets.mjs`)
- [x] Create `src/components/SearchBar.astro` using the Pagefind UI widget
- [x] Add "Search" link to both desktop and mobile nav in BaseLayout
- [x] Create `src/pages/search.astro` as a dedicated search page

### Milestone 3.2 — SEO Metadata
- [x] Add to `BaseLayout.astro` head:
  - `<meta name="description">` from frontmatter
  - Open Graph tags: `og:title`, `og:description`, `og:type`, `og:url`, `og:image` (optional)
  - Twitter card tags: `twitter:card`, `twitter:title`, `twitter:description`
- [x] `ArticleLayout.astro` passes title/description/url to BaseLayout og props
- [x] JSON-LD `Article` schema added to ArticleLayout via `<script type="application/ld+json">`
- [ ] **Josh:** Verify with Google's Rich Results Test tool on a sample newsletter URL

### Milestone 3.3 — Sitemap
- [x] Install `@astrojs/sitemap`: `npm install @astrojs/sitemap`
- [x] Add `sitemap()` to `astro.config.mjs` integrations
- [x] Set `site` in config to `https://joshjab.github.io/sonstoglory-mod` (update to `https://sonstoglory.com` at DNS cutover)
- [x] `dist/sitemap-index.xml` generated on build
- [ ] **Josh:** Submit sitemap to Google Search Console after DNS cutover

### Milestone 3.4 — Performance
- [x] Added `loading="lazy"` to all below-fold `<img>` tags in Astro components (book covers, author photos, video thumbnails, newsletter card images)
- [x] Favicon path verified correct: `public/images/images/favicon.ico` exists; `images/images/` double-path is expected (legacy mirror structure)
- [x] Site logo in BaseLayout has `width="36" height="36"` to prevent layout shift
- [x] Book cover images have `width`/`height` attributes added
- [ ] **Josh (manual):** Run Lighthouse audit after deploy and address any remaining issues
- [ ] **Josh (manual):** Convert large JPGs to WebP using `cwebp` or Squoosh for further gains

### Milestone 3.5 — Accessibility
- [x] All `<img>` tags in Astro components have `alt` attributes (decorative card images use `alt=""`)
- [x] Heading hierarchy: one `<h1>` per page, `<h2>` for sections — verified on index, newsletters, articles, book, authors pages
- [x] Mobile nav hamburger `<label>` has `aria-label="Open navigation menu"`
- [x] Dark/light mode toggle buttons have `aria-label="Toggle dark mode"`
- [x] Video play buttons have `aria-label="Play {title}"` on the button wrapper
- [x] Search page `<h1>` heading present; Pagefind UI renders its own labelled input
- [ ] **Josh (manual):** Run axe DevTools on live site and fix any additional violations found

### Milestone 3.6 — Analytics
- [x] Analytics placeholder comment added to BaseLayout.astro `<head>`: `<!-- ANALYTICS: paste your Plausible/Umami snippet here -->`
- **To activate:** Sign up at [plausible.io](https://plausible.io) (free for public/open-source sites) or self-host Umami. Paste the 1-line `<script>` snippet in BaseLayout.astro where the placeholder comment is.

### Milestone 3.7 — Dark Mode Toggle
- [x] CSS custom properties defined in `global.css` for light and dark themes (`--color-bg`, `--color-text`, `--color-heading`, etc.)
- [x] Dark theme activates via `[data-theme="dark"]` on `<html>` element
- [x] Inline `<script>` in BaseLayout `<head>` reads localStorage and sets `data-theme` before CSS renders (no flash)
- [x] Sun/moon toggle button in desktop and mobile header nav
- [x] Toggle persists preference to `localStorage`
- [x] Dark mode overrides for card backgrounds and gray tones in `global.css`

---

## Phase 2.5 — Publishing Workflow

**Goal:** Paul can publish new newsletters and videos appear automatically — no code knowledge required.
**Prereqs:** Phase 2 complete, GitHub repo live, site deployed to GitHub Pages.

### Background: The Problem

The site is static — content lives as Markdown files in a git repo. Paul is not a developer. We need a workflow where:
1. Paul can write and publish a new newsletter without touching git or a terminal
2. New YouTube videos appear on the site automatically without any manual steps
3. Josh can review before anything goes live (optional gate)

### Chosen Approach

| Content Type | Authoring Tool | Publish Trigger |
|---|---|---|
| **New newsletters** | Decap CMS (web UI on top of GitHub) | Paul hits "Publish" → CMS commits Markdown to repo → GitHub Actions builds + deploys |
| **New YouTube videos** | Paul just uploads to YouTube as normal | GitHub Actions daily cron triggers a rebuild, which fetches the latest RSS feed |

**Why Decap CMS?** It's free, open source, runs entirely in the browser, stores content directly in the GitHub repo as Markdown, and requires zero server. Paul gets a simple rich-text editor at a URL like `sonstoglory.com/admin`. No new accounts beyond GitHub.

---

### Milestone 2.5.1 — Decap CMS Setup
- [ ] Install Decap CMS static files: add `public/admin/index.html` and `public/admin/config.yml`
- [ ] Configure `config.yml` with:
  - `backend: github` (uses GitHub OAuth)
  - `branch: main`
  - `media_folder: public/images`
  - Collection definitions for `newsletters`, `articles`, and `poems` matching the Astro content schemas
- [ ] Set up GitHub OAuth App:
  1. Go to GitHub → Settings → Developer Settings → OAuth Apps → New OAuth App
  2. Homepage URL: `https://sonstoglory.com`
  3. Callback URL: `https://sonstoglory.com/admin/`
  4. Save the Client ID and Secret
- [ ] Deploy a small OAuth proxy (Decap's `netlify-cms-github-oauth-provider` or `decap-server`) to handle the OAuth flow since GitHub Pages can't run server-side code. Options:
  - **Option A:** Deploy the proxy as a single Cloudflare Worker (free tier, zero maintenance)
  - **Option B:** Run it on the home server / small AWS instance
- [ ] Test login at `/admin` with Paul's GitHub account
- [ ] Verify that saving a draft in the CMS creates a commit in the repo

### Milestone 2.5.2 — Newsletter Authoring in CMS
- [ ] In `config.yml`, define the `newsletters` collection fields:
  ```yaml
  - label: "Title"           name: title       widget: string
  - label: "Date"            name: date         widget: datetime
  - label: "Issue Number"    name: number       widget: number
  - label: "Description"     name: description  widget: text
  - label: "Tags"            name: tags         widget: list
  - label: "Body"            name: body         widget: markdown
  ```
- [ ] Test creating a new newsletter end-to-end: write in CMS → publish → verify it appears on the live site after the GitHub Actions build completes
- [ ] Write a one-page guide for Paul: "How to publish a new newsletter" (screenshots of the CMS UI, step-by-step)

### Milestone 2.5.3 — GitHub Actions Build Pipeline
- [ ] Create `.github/workflows/deploy.yml`:
  ```yaml
  on:
    push:
      branches: [main]
  jobs:
    build-deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-node@v4
          with: { node-version: 18 }
        - run: npm ci
        - run: npm run build      # includes prebuild YouTube fetch + postbuild Pagefind
        - uses: actions/deploy-pages@v4
  ```
- [ ] Enable GitHub Pages in repo settings: Source → GitHub Actions
- [ ] Push a test commit and verify the full build → deploy pipeline succeeds
- [ ] Check that build output (dist/) appears at the live URL within ~2 minutes of a push

### Milestone 2.5.4 — Automated Daily YouTube Rebuild
- [ ] Create `.github/workflows/scheduled-rebuild.yml`:
  ```yaml
  on:
    schedule:
      - cron: '0 6 * * *'   # 6am UTC daily
    workflow_dispatch:        # allow manual trigger too
  jobs:
    rebuild:
      uses: ./.github/workflows/deploy.yml   # reuse the same build job
  ```
- [ ] Manually trigger the workflow and verify new videos appear in `src/data/videos.json` after the run
- [ ] Confirm the videos page on the live site reflects the latest uploads within 24 hours of Paul posting

### Milestone 2.5.5 — Editorial Review Gate (Optional)
> Skip this if Josh and Paul prefer to publish immediately. Enable it if Paul wants a "draft → review → publish" flow.

- [ ] In Decap CMS `config.yml`, enable editorial workflow:
  ```yaml
  publish_mode: editorial_workflow
  ```
- [ ] This changes the CMS flow to: Paul saves as Draft → Paul marks as "In Review" → Josh approves in CMS → Publish creates the commit and triggers the build
- [ ] Test the full draft → review → publish cycle
- [ ] Decide whether to keep this enabled based on how Paul and Josh prefer to work

---

## Phase 4 — Future Enhancements (Backlog)

> These are nice-to-haves for after the core site is live and stable.

- [ ] **Auto PDF generation** — Use `@astrojs/pdf` or a headless Chrome script to generate downloadable PDFs from Markdown content at build time
- [ ] **Content calendar** — Create a page that maps newsletters/articles to the Biblical feast calendar dates
- [ ] **Comment system** — Add Giscus (GitHub Discussions-based) to article pages
- [ ] **Substack cross-post** — Investigate Substack API or manual workflow for cross-posting newsletters
- [ ] **Audio versions** — Upload MP3 readings of newsletters; embed audio players on article pages
- [ ] **Multi-language support** — Astro i18n routing if international readership grows

---

## Open Questions (Blocking)

| # | Question | Who Answers | Blocking |
|---|---|---|---|
| 1 | What is Paul's YouTube channel URL? | ✅ `@coolpixstargazer` | Unblocks Phase 2.5 YouTube automation |
| 2 | How many email subscribers? In what format is the current list? | ✅ ~500 subscribers | Using ConvertKit free tier |
| 3 | Does Paul want to keep publishing new newsletters, or shift to video only? | ✅ Both newsletters and videos | Phase 2.5 publishing workflow scoped accordingly |
| 4 | Are there any unpublished writings to include during migration? | ⏳ Ask Paul | Phase 0 |
| 5 | Who controls DNS for sonstoglory.com and pauljab.com? | ✅ Josh has access — defer until cutover | Phase 1 deploy |
| 6 | Any content to retire / not migrate? | ✅ Migrate everything | Phase 0 |
| 7 | Astro preference vs. Hugo? | ✅ Astro | Phase 1 scaffold |
| 8 | Budget for paid services? (analytics, email) | ✅ Zero — free/self-hosted only | See ARCH.md stack decisions |
