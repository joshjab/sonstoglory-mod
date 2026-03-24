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
- [ ] Commit the mirror to a `legacy/` branch: `git checkout -b legacy && git add legacy-mirror/ && git commit -m "chore: archive legacy site mirror"`

### Milestone 0.2 — Content Inventory
- [x] Write a Python script `scripts/inventory.py` that crawls `legacy-mirror/` and outputs a CSV with columns: `filename`, `path`, `title` (from `<title>` tag), `type` (newsletter/article/book/etc), `estimated_date`
- [x] Run the script and review the output CSV: `python3 scripts/inventory.py > content-inventory.csv`
- [x] Manually review the CSV and fill in any missing `type` or `date` values
- [ ] Commit the inventory CSV to the repo

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
- [ ] Create a new GitHub repository (e.g., `sonstoglory-site`)
- [ ] Rename local branch to `main`: `git branch -m main`
- [ ] Add GitHub remote and push: `git remote add origin <url> && git push -u origin main`
- [ ] Create a `.gitignore` with: `node_modules/`, `dist/`, `.env`, `.DS_Store`

### Milestone 1.2 — Init Astro Project
- [ ] Install Node 18+ if not present
- [ ] Scaffold the project in the repo root:
  ```bash
  npm create astro@latest -- --template minimal --yes
  ```
- [ ] Add Tailwind CSS integration:
  ```bash
  npx astro add tailwind
  ```
- [ ] Add the Astro content collections integration (built-in, just configure `src/content/config.ts`)
- [ ] Run `npm run dev` and verify the dev server starts on `localhost:4321`
- [ ] Commit the scaffolded project: `git commit -m "feat: init Astro project with Tailwind"`

### Milestone 1.3 — Content Collection Schema
- [ ] Create `src/content/config.ts` defining Zod schemas for:
  - `newsletters` collection (title, author, date, number, tags, description, legacy_url)
  - `book` collection (title, chapter number, description)
  - `articles` collection (title, author, date, tags, description, legacy_url)
  - `authors` collection (name, bio, books)
  - `poems` collection (title, author, date)
- [ ] Copy a few Markdown files from `content/` into `src/content/` to validate the schema
- [ ] Fix any schema validation errors that Astro reports

### Milestone 1.4 — Base Layout
- [ ] Create `src/layouts/BaseLayout.astro` with:
  - `<html>`, `<head>` with meta charset, viewport, title slot
  - `<Header />` component (see next task)
  - `<slot />` for page content
  - `<Footer />` component (see next task)
- [ ] Create `src/components/Header.astro` with:
  - Site logo/name: "Sons To Glory"
  - Nav links: Home, Book, Newsletters, Articles, Videos, Authors, Subscribe
  - Mobile hamburger menu (Tailwind + minimal JS toggle)
- [ ] Create `src/components/Footer.astro` with:
  - Mailing address: Harvest, AL 35749
  - Links: YouTube, Subscribe, RSS
  - Copyright line
- [ ] Add global typography styles in `src/styles/global.css` (import Tailwind directives, set base font size to 18–20px)

### Milestone 1.5 — Homepage
- [ ] Create `src/pages/index.astro`:
  - Hero section: site title, one-sentence mission statement, two CTA buttons (Read the Book, Browse Newsletters)
  - "Latest Newsletters" section: grid of 3 most recent newsletter cards (title, date, short excerpt)
  - "Featured Article" section: one highlighted piece
  - Newsletter signup CTA block (email input + subscribe button — can be a placeholder for now)
- [ ] Pull latest newsletters dynamically from the content collection

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
- [x] Add `public/CNAME` with `sonstoglory.com` for custom domain
- [x] Fixed `package.json`: name → "sonstoglory", engines → ">=18.0.0"
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
- [ ] Move all remaining converted Markdown files into `src/content/`
- [ ] Fix any frontmatter schema errors reported by Astro
- [ ] Verify all 40+ newsletters render correctly at `/newsletters/[slug]`
- [ ] Verify all book chapters render

### Milestone 2.2 — Book Reading Experience
- [ ] Create `src/layouts/BookChapterLayout.astro`:
  - Chapter title and number
  - Table of contents sidebar (links to all chapters)
  - Previous/Next chapter navigation buttons at bottom
  - "Download full book PDF" link
- [ ] Create `src/pages/book/index.astro`: book overview page with chapter listing
- [ ] Create `src/pages/book/[slug].astro`: dynamic route for individual chapters

### Milestone 2.3 — Guest Author Pages
- [ ] Create `src/layouts/AuthorLayout.astro`:
  - Author name, bio, photo placeholder
  - List of their writings/books on the site
- [ ] Create `src/pages/authors/[author]/index.astro`: author profile page
- [ ] Create `src/pages/authors/roland-pletts/index.astro` and populate Roland Pletts' bio and book list
- [ ] Create `src/pages/authors/bonnie-gaunt/index.astro` and populate Bonnie Gaunt's bio

### Milestone 2.4 — Articles & Poems Pages
- [ ] Create `src/pages/articles/index.astro`: list of all standalone articles
- [ ] Create `src/pages/articles/[slug].astro`: single article render
- [ ] Create `src/pages/poems/[slug].astro`: single poem render

### Milestone 2.5 — YouTube Integration
- [ ] Confirm Paul's YouTube channel ID (see Open Questions in README)
- [ ] Write `scripts/fetch-youtube-feed.mjs`:
  1. Fetch `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID`
  2. Parse the XML (use a lightweight XML parser npm package)
  3. Write to `src/data/videos.json` (array of `{ id, title, date, thumbnail }`)
- [ ] Add this script to the Astro build process in `package.json`:
  ```json
  "prebuild": "node scripts/fetch-youtube-feed.mjs"
  ```
- [ ] Create `src/pages/videos.astro`:
  - Reads `src/data/videos.json`
  - Renders a responsive grid of video thumbnails + titles
  - On click, replaces thumbnail with a full `<iframe>` YouTube embed (lite-youtube or native)
- [ ] Add 2 latest videos to the homepage

### Milestone 2.6 — Newsletter Signup
- [ ] Create account on Buttondown (or chosen email service)
- [ ] Import existing email list contacts
- [ ] Get the embed code for the subscribe form
- [ ] Create `src/components/NewsletterSignup.astro` wrapping the embed
- [ ] Add the component to the footer and to a dedicated `src/pages/subscribe.astro` page

### Milestone 2.7 — RSS Feed
- [ ] Install `@astrojs/rss`: `npm install @astrojs/rss`
- [ ] Create `src/pages/rss.xml.ts` that generates an RSS feed from the newsletters content collection
- [ ] Add `<link rel="alternate" type="application/rss+xml">` to BaseLayout head
- [ ] Test the feed URL at `/rss.xml`

### Milestone 2.8 — QA Pass
- [ ] Click through every page on the live Netlify URL
- [ ] Check all 40+ newsletter pages load and display correctly
- [ ] Verify all PDFs are accessible
- [ ] Test on a real mobile device (iOS and Android)
- [ ] Fix any broken links, missing images, or formatting issues found

---

## Phase 3 — Polish & Enhance

**Goal:** Site is production-ready with search, SEO, analytics, and accessibility.
**Prereqs:** Phase 2 complete.

### Milestone 3.1 — Full-Text Search (Pagefind)
- [ ] Install Pagefind: `npm install pagefind`
- [ ] Add Pagefind indexing to the build script (runs after `astro build`)
- [ ] Create `src/components/SearchBar.astro` using the Pagefind UI widget
- [ ] Add search bar to the header
- [ ] Create `src/pages/search.astro` as a dedicated search page
- [ ] Test search for 3–5 different keywords across newsletters and articles

### Milestone 3.2 — SEO Metadata
- [ ] Add to `BaseLayout.astro` head:
  - `<meta name="description">` from frontmatter
  - Open Graph tags: `og:title`, `og:description`, `og:image`, `og:url`
  - Twitter card tags
- [ ] Add JSON-LD structured data (`Article` schema) to ArticleLayout
- [ ] Verify with Google's Rich Results Test tool on a sample page

### Milestone 3.3 — Sitemap
- [ ] Install `@astrojs/sitemap`: `npm install @astrojs/sitemap`
- [ ] Add `sitemap()` to `astro.config.mjs` integrations
- [ ] Set `site` in config to `https://sonstoglory.com`
- [ ] After build, verify `sitemap-index.xml` is generated in `dist/`
- [ ] Submit sitemap to Google Search Console

### Milestone 3.4 — Performance Audit
- [ ] Run Lighthouse audit on the live site (Chrome DevTools → Lighthouse)
- [ ] Identify and fix the top 3 performance issues found
- [ ] Convert large images to WebP format using a script or Astro image integration
- [ ] Add lazy loading (`loading="lazy"`) to all `<img>` tags not in the initial viewport

### Milestone 3.5 — Accessibility Audit
- [ ] Run axe DevTools browser extension on homepage, a newsletter page, and the book page
- [ ] Fix all critical and serious violations found
- [ ] Ensure heading hierarchy is logical (one `<h1>` per page, `<h2>` for sections, etc.)
- [ ] Add `alt` text to all images
- [ ] Verify keyboard navigation works for the nav menu, search, and subscribe form

### Milestone 3.6 — Analytics
- [ ] Create a free account at Plausible.io or set up self-hosted Umami
- [ ] Add the analytics snippet to `BaseLayout.astro`
- [ ] Verify pageview events are being recorded

### Milestone 3.7 — Dark Mode Toggle
- [ ] Add a `data-theme` attribute toggle to `<html>` element
- [ ] Define CSS custom properties for light and dark color schemes in `global.css`
- [ ] Create a toggle button in the Header that flips `data-theme`
- [ ] Persist the user's preference to `localStorage`
- [ ] Test that the preference is remembered on page reload

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
