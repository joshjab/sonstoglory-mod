# Sons To Glory — Site Modernization Plan

> **Prepared for:** Paul Jablonowski  
> **Prepared by:** Josh Jablonowski + Claude  
> **Date:** March 24, 2026  
> **Status:** Discovery & Planning

---

## 1. Current Site Audit

### 1.1 Domain Inventory

| Domain | Role | Tech | Status |
|---|---|---|---|
| `pauljab.com` | Personal landing page | Static HTML (Dreamweaver) | Live — mostly redirects to sonstoglory.com |
| `pauljab.net` | Mirror / alias | Redirects to pauljab.com | Live |
| `sonstoglory.com` | Primary content site | Static HTML (Dreamweaver), PDFs | Live |

### 1.2 Current Site Structure — sonstoglory.com

The site is built entirely in static HTML with no JavaScript, no CMS, and no database. All content was authored in Macromedia/Adobe Dreamweaver circa early 2000s. The site uses HTML table-based layouts (pre-CSS Grid/Flexbox era).

```
sonstoglory.com/
├── index.htm                    # Homepage — "Sons To Glory books | Everlasting Kingdom of Jesus"
├── book.htm                     # "Sons To Glory" book — Table of Contents
├── messages.htm                 # Messages index page
├── newsletters.htm              # Newsletter index page (40+ newsletters)
├── SonsToGloryBook.pdf          # Full book as downloadable PDF
│
├── newsletters/                 # Individual newsletter HTML pages
│   ├── 12worshipwarfare.htm         # #12 — Worship Warfare (June 2011)
│   ├── 13feastoftabernacles.htm     # #13 — Tabernacles (Oct 2011)
│   ├── 14christianpassoverhaggadah.htm  # #14 — Passover (Apr 2012)
│   ├── 16Hallelujah.htm             # #16 — Hallelujah (Oct 2012)
│   ├── 18newmooncelebrations.htm    # #18 — New Moon (May 2013)
│   ├── 21pauljab.htm                # #21 — Work Profile/Bio (Jul 2014)
│   ├── 24number33and13.htm          # #24 — Numbers 33 and 13 (Sep 2015)
│   ├── 31sonshipovercomers.htm      # #31 — Birthing Overcomers (Jun 2018)
│   ├── 33heartofdavid.htm           # #33 — He Has Exalted the Lowly (Dec 2018)
│   ├── 37OrderofMelchiZedek.htm     # #37 — Melchizedek Order (Apr 2020)
│   ├── 40TheCovenantCircle.htm      # #40 — The Covenant Circle (Apr 2021)
│   └── ... (newsletters #1–#40, possibly more)
│
├── rolandpletts/                # Guest author: Roland Pletts
│   ├── index.htm                    # Roland Pletts landing page
│   ├── about.htm                    # About Roland Pletts bio
│   └── books.htm                    # Roland Pletts books index (8+ books)
│
├── bonniegaunt/                 # Guest author: Bonnie Gaunt (1929–2012)
│   └── about.htm                    # About Bonnie Gaunt
│
├── Jesus/                       # Standalone articles / resources
│   ├── henrygruvervision.htm        # Henry Gruver's vision (1969)
│   └── Rulers of Evil book report by Paul Jablonowski.pdf
│
├── worshipJesusfeastssaved.htm  # "Worship in Spirit and Truth"
├── JesusSecondComing.htm        # Roland Pletts — "Shekinah Glory of Christ"
├── ChristComingBook.pdf         # Roland Pletts book as PDF
├── JudgeRoyMoore10commandments.htm  # Ten Commandments article (2003)
├── starJesusbirth.htm           # Star of Bethlehem article
├── manchildBirth.htm            # "Birth of a Manchild" poem
├── mileswyliealbright.htm       # Miles Albright book request page
└── ... (additional articles and resources)
```

### 1.3 Content Inventory Summary

| Content Type | Estimated Count | Format | Notes |
|---|---|---|---|
| **Newsletters** | 40+ | Individual `.htm` files | Dated 2011–2021, by Paul Jablonowski |
| **Book — "Sons To Glory"** | 1 (multi-chapter) | HTML chapters + PDF download | Free distribution, also on Amazon |
| **Standalone Articles** | 10–15+ | `.htm` files | Topics: worship, feasts, prophecy, testimonies |
| **Guest Author: Roland Pletts** | 8+ books | HTML + PDF | UK-based author, prophecy/covenant theology |
| **Guest Author: Bonnie Gaunt** | Studies + book list | HTML | Passed away 2012; memorial content |
| **Book Reports / PDFs** | 2–3+ | PDF in `/Jesus/` dir | Academic-style theological analysis |
| **Poems** | 1+ | HTML | "Birth of a Manchild" |
| **Messages** | Unknown count | HTML index | Referenced at messages.htm |
| **Email List** | Active | Unknown platform | Manual/Dreamweaver-era management |

### 1.4 Key Themes & Taxonomy (for future tagging/categories)

- **Biblical Feasts:** Passover, Pentecost, Tabernacles, Trumpets, Atonement, New Moon
- **Kingdom Theology:** Sonship, maturity, overcomers, the Bride Body
- **The Cross & Redemption:** Covenant, sacrifice, the Melchizedek Order
- **Prophecy & End Times:** Second Coming, Shekinah Glory, Daniel, Revelation
- **Worship & Intercession:** Worship warfare, spiritual authority, prayer
- **Personal Testimony:** Paul's work profile, family, spiritual journey
- **Guest Authors:** Roland Pletts (prophecy/covenant), Bonnie Gaunt (Biblical numerics)

### 1.5 Current Features

- ✅ Free book distribution (HTML + PDF + paperback)
- ✅ Newsletter archive (40+ issues)
- ✅ Guest author hosting
- ✅ Email list for updates
- ✅ Mailing address published (Harvest, AL 35749)
- ❌ No mobile responsiveness
- ❌ No search functionality
- ❌ No YouTube integration
- ❌ No RSS feed
- ❌ No analytics
- ❌ No HTTPS (mixed http/https references found)
- ❌ No SEO metadata
- ❌ Table-based layout (Dreamweaver-era)
- ❌ No sitemap.xml or robots.txt (likely)

---

## 2. Modernization Goals

### 2.1 Non-Negotiables (Preserve)

1. **All existing written content** — every newsletter, article, chapter, and PDF must migrate
2. **Free book distribution model** — the content is freely given, not monetized
3. **Guest author sections** — Roland Pletts and Bonnie Gaunt content stays intact
4. **Mailing list capability** — readers must still be able to subscribe for updates
5. **Existing URLs** — old links should redirect or still resolve (SEO + bookmarks)

### 2.2 New Features

| Feature | Priority | Description |
|---|---|---|
| **YouTube Integration** | 🔴 High | Embed or auto-sync Paul's YouTube videos; video page/feed |
| **Modern Email/Newsletter** | 🔴 High | Replace manual list with Buttondown, Mailchimp, or Substack-style integration |
| **Responsive Design** | 🔴 High | Mobile-first layout that works on phones and tablets |
| **Search** | 🟡 Medium | Full-text search across all writings and newsletters |
| **RSS Feed** | 🟡 Medium | Auto-generated feed for newsletters and new content |
| **Reading Experience** | 🟡 Medium | Clean typography, table of contents nav, estimated read times |
| **Content Tagging** | 🟡 Medium | Categorize by theme (feasts, prophecy, worship, etc.) |
| **Analytics** | 🟢 Low | Privacy-respecting visitor analytics (Plausible, Umami, or similar) |
| **Dark Mode** | 🟢 Low | Reader preference toggle |
| **PDF Generation** | 🟢 Low | Auto-generate printer-friendly PDFs from markdown content |

---

## 3. Recommended Architecture

### 3.1 Tech Stack Recommendation

| Layer | Choice | Rationale |
|---|---|---|
| **Static Site Generator** | **Astro** or **Hugo** | Fast, markdown-native, zero JS by default (matches Paul's static HTML philosophy), great for content-heavy sites |
| **Content Format** | **Markdown (.md)** | Easy to edit, version-controlled, portable, converts to HTML/PDF |
| **Styling** | **Tailwind CSS** | Utility-first, responsive out of the box, small bundle |
| **Hosting** | **GitHub Pages**, **Netlify**, or **Cloudflare Pages** | Free, auto-deploys from git, HTTPS included, CDN |
| **Email/Newsletter** | **Buttondown** or **Mailchimp Free** | Modern subscribe forms, email campaigns, archive page |
| **YouTube Sync** | **YouTube Data API v3** or **RSS feed embed** | Pull latest videos at build time |
| **Search** | **Pagefind** (static search) | Zero-cost, builds a search index at deploy time, no server needed |
| **Analytics** | **Plausible** or **Umami** (self-hosted) | Privacy-first, lightweight, no cookies |
| **Domain** | Keep `sonstoglory.com` as primary | `pauljab.com` redirects to it |

### 3.2 Why a Static Site Generator (Not WordPress)

Paul's current site is static HTML — it's fast and simple. The goal is to keep that simplicity while adding modern features. A static site generator (SSG) like Astro or Hugo:

- Generates plain HTML/CSS at build time (no server, no database, no PHP)
- Content lives as markdown files in a git repo (easy to edit, backup, and version)
- Deploys for free to GitHub Pages / Netlify / Cloudflare
- Near-zero maintenance — no WordPress updates, no plugin vulnerabilities, no hosting fees
- Paul can still write in a simple text editor if he wants; Josh can manage the tech side

### 3.3 Proposed Directory Structure (Git Repository)

```
sonstoglory/
├── README.md                        # This plan document
├── ROADMAP.md                       # Implementation tracking
├── astro.config.mjs                 # (or hugo.toml) — site config
├── package.json
│
├── src/
│   ├── layouts/
│   │   ├── BaseLayout.astro         # HTML shell, nav, footer
│   │   ├── ArticleLayout.astro      # Single writing/newsletter template
│   │   ├── BookChapterLayout.astro  # Book chapter reading template
│   │   └── AuthorLayout.astro       # Guest author profile template
│   │
│   ├── pages/
│   │   ├── index.astro              # Homepage
│   │   ├── about.astro              # About Paul
│   │   ├── videos.astro             # YouTube integration page
│   │   ├── subscribe.astro          # Newsletter signup
│   │   └── search.astro             # Full-text search page
│   │
│   ├── components/
│   │   ├── Header.astro             # Site navigation
│   │   ├── Footer.astro             # Footer with mailing address, links
│   │   ├── NewsletterSignup.astro   # Email subscribe widget
│   │   ├── YouTubeEmbed.astro       # Responsive video embed
│   │   ├── YouTubeFeed.astro        # Latest videos grid
│   │   ├── ReadingProgress.astro    # Progress bar for long articles
│   │   ├── TableOfContents.astro    # Auto-generated from headings
│   │   ├── TagCloud.astro           # Topic/category navigation
│   │   └── SearchBar.astro          # Pagefind search widget
│   │
│   └── styles/
│       └── global.css               # Tailwind + custom typography
│
├── content/                         # ALL CONTENT LIVES HERE AS MARKDOWN
│   ├── newsletters/
│   │   ├── 01-first-newsletter.md
│   │   ├── ...
│   │   └── 40-the-covenant-circle.md
│   │
│   ├── book/                        # "Sons To Glory" book chapters
│   │   ├── _index.md                # Book intro / table of contents
│   │   ├── 01-how-to-worship.md
│   │   ├── 02-thinking-like-sons.md
│   │   └── ...
│   │
│   ├── articles/                    # Standalone writings
│   │   ├── worship-in-spirit-and-truth.md
│   │   ├── judge-roy-moore-ten-commandments.md
│   │   ├── star-of-bethlehem.md
│   │   └── ...
│   │
│   ├── authors/                     # Guest author profiles + content
│   │   ├── roland-pletts/
│   │   │   ├── _index.md            # Bio and book listing
│   │   │   ├── shekinah-glory.md
│   │   │   └── ...
│   │   └── bonnie-gaunt/
│   │       └── _index.md
│   │
│   └── poems/
│       └── birth-of-a-manchild.md
│
├── public/                          # Static assets (copied as-is)
│   ├── pdfs/
│   │   ├── SonsToGloryBook.pdf
│   │   ├── ChristComingBook.pdf
│   │   └── ...
│   ├── images/
│   ├── favicon.ico
│   ├── robots.txt
│   └── _redirects                   # Old URL → new URL mapping
│
└── scripts/
    ├── migrate-html-to-md.py        # One-time migration script
    ├── fetch-youtube-feed.js        # Build-time YouTube data fetch
    └── generate-redirects.py        # Generate redirect map from old URLs
```

### 3.4 Markdown Frontmatter Schema

Every content file uses YAML frontmatter for metadata:

```yaml
---
title: "The Covenant Circle"
author: "Paul Jablonowski"
date: 2021-04-27
type: newsletter          # newsletter | book-chapter | article | poem | guest-author
number: 40                # newsletter number (if applicable)
tags:
  - cross
  - covenant
  - redemption
  - sacrifice
description: "The cross is the power of God and the wisdom of God; and the cross of Christ is central to the Gospel of the Kingdom."
pdf: /pdfs/newsletter-40.pdf   # optional PDF version
legacy_url: /newsletters/40TheCovenantCircle.htm   # for redirect mapping
---

Content body in markdown here...
```

---

## 4. Implementation Roadmap

### Phase 0 — Content Extraction & Migration (Foundation)
> **Goal:** Get all existing content out of static HTML and into markdown files  
> **Estimated effort:** 2–3 days  
> **Depends on:** Nothing — start here

| Step | Task | Details |
|---|---|---|
| 0.1 | **Mirror the existing site** | Use `wget --mirror` or `httrack` to download a complete copy of sonstoglory.com and pauljab.com. This is the source-of-truth backup. |
| 0.2 | **Inventory all pages** | Crawl the mirror, catalog every `.htm`, `.html`, `.pdf`, and image file. Produce a master spreadsheet/CSV of all URLs and their titles. |
| 0.3 | **Convert HTML → Markdown** | Write/run `migrate-html-to-md.py` using `pandoc` or `html2text`. Strip Dreamweaver table layout markup, preserve the actual text content. |
| 0.4 | **Add frontmatter to each file** | Populate title, date, author, type, tags, legacy_url for every piece of content. |
| 0.5 | **Organize into content directories** | Sort markdown files into `newsletters/`, `book/`, `articles/`, `authors/`, `poems/`. |
| 0.6 | **Copy static assets** | Move all PDFs and images to `public/pdfs/` and `public/images/`. |
| 0.7 | **Generate redirect map** | Create `_redirects` file mapping every old URL to its new path. |
| 0.8 | **QA pass** | Manually spot-check 5–10 converted files against the originals for content accuracy. |

### Phase 1 — Scaffold & Deploy (Get Something Live)
> **Goal:** Working site skeleton deployed with a few pieces of real content  
> **Estimated effort:** 1–2 days  
> **Depends on:** Phase 0

| Step | Task | Details |
|---|---|---|
| 1.1 | **Init git repo** | `git init sonstoglory`, add `.gitignore`, push to GitHub. |
| 1.2 | **Init Astro project** | `npm create astro@latest`, configure with Tailwind, markdown support. |
| 1.3 | **Create BaseLayout** | Responsive shell: header nav, footer with mailing address, mobile hamburger menu. |
| 1.4 | **Create homepage** | Hero section with mission statement, latest content cards, newsletter signup CTA. |
| 1.5 | **Create ArticleLayout** | Clean reading template: title, date, author, body, tag links, prev/next navigation. |
| 1.6 | **Import 3–5 newsletters** | Validate the markdown → rendered HTML pipeline with real content. |
| 1.7 | **Set up deployment** | Connect repo to Netlify or Cloudflare Pages. Configure custom domain (`sonstoglory.com`). |
| 1.8 | **Verify HTTPS & redirects** | Ensure old URLs resolve. Test on mobile. |

### Phase 2 — Full Content & Core Features
> **Goal:** All content migrated, newsletter + YouTube features working  
> **Estimated effort:** 3–5 days  
> **Depends on:** Phase 1

| Step | Task | Details |
|---|---|---|
| 2.1 | **Import ALL remaining content** | Complete newsletter archive, all book chapters, all articles, all guest author pages. |
| 2.2 | **Build newsletter index page** | Paginated archive listing, sortable by date, filterable by tag. |
| 2.3 | **Build book reading experience** | Table of contents, chapter nav (prev/next), progress indicator. |
| 2.4 | **Build guest author sections** | Author bio pages with their content listed below. |
| 2.5 | **YouTube integration** | Build `videos.astro` page. Fetch Paul's YouTube channel feed at build time. Display video grid with thumbnails and titles. Responsive embed on click. |
| 2.6 | **Newsletter signup** | Integrate Buttondown or Mailchimp. Embed subscribe form in footer and dedicated page. Migrate existing email list. |
| 2.7 | **RSS feed** | Auto-generate `/feed.xml` from content collection. |
| 2.8 | **Full QA pass** | Check every migrated page. Fix broken links, formatting issues, missing images. |

### Phase 3 — Polish & Enhance
> **Goal:** Search, SEO, performance, and quality-of-life features  
> **Estimated effort:** 2–3 days  
> **Depends on:** Phase 2

| Step | Task | Details |
|---|---|---|
| 3.1 | **Pagefind search** | Add static search indexing at build time. Search bar in header. |
| 3.2 | **SEO metadata** | OpenGraph tags, Twitter cards, structured data (JSON-LD for articles). |
| 3.3 | **Sitemap generation** | Auto-generate `sitemap.xml` for Google indexing. |
| 3.4 | **Performance audit** | Lighthouse score check. Optimize images (WebP conversion). Lazy-load videos. |
| 3.5 | **Accessibility audit** | Semantic HTML, proper heading hierarchy, alt text, keyboard nav, color contrast. |
| 3.6 | **Analytics** | Add Plausible or Umami snippet (privacy-first, no cookies). |
| 3.7 | **Dark mode toggle** | CSS custom properties + localStorage preference. |
| 3.8 | **Print stylesheet** | Clean print-friendly layout for articles. |

### Phase 4 — Future Enhancements (Optional / Ongoing)
> **Goal:** Nice-to-haves for when the core is solid

| Feature | Description |
|---|---|
| **Auto PDF generation** | Generate downloadable PDFs from markdown at build time |
| **Audio versions** | Text-to-speech or recorded readings of newsletters |
| **Content calendar** | Tie newsletters to the Biblical feast calendar |
| **Comment system** | Giscus (GitHub-based) or Disqus alternative |
| **Multi-language** | If there's international readership interest |
| **Substack cross-post** | Publish newsletters to Substack simultaneously for broader reach |

---

## 5. Email List Modernization

### Current State
Paul manages an email list manually (likely BCC'd emails or a basic mailing list tool from the Dreamweaver era).

### Recommended Alternatives

| Service | Free Tier | Why Consider |
|---|---|---|
| **Buttondown** | Up to 100 subscribers | Markdown-native, minimal, newsletter-focused, great for writers |
| **Mailchimp** | Up to 500 contacts | Well-known, easy embeds, automation, landing pages |
| **Substack** | Free (takes % on paid) | Built-in audience, newsletter + web archive, but locks you into their platform |
| **ConvertKit (Kit)** | Up to 10,000 subscribers | Creator-focused, tagging, automation, landing pages |

### Recommendation
**Buttondown** for its simplicity and markdown-native approach — aligns well with the content philosophy. It provides a hosted archive page, simple subscribe embeds, and Paul can draft in plain text. If the list is large (500+), **Kit (ConvertKit)** is the better choice for its generous free tier.

### Migration Steps
1. Export current email list (whatever format it's in)
2. Import contacts to chosen platform
3. Set up subscribe form on new site
4. Send a "we've moved" announcement from old system
5. Sunset old system

---

## 6. YouTube Integration Strategy

### Approach: Build-Time RSS Fetch (No API Key Needed)

YouTube channels have a public RSS feed at:
```
https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID
```

At build time, the site fetches this feed and generates a static videos page. This means:
- No API key management
- No client-side JavaScript
- Videos page updates on every deploy (can be triggered by a cron-based rebuild, e.g., daily via Netlify build hook or GitHub Actions)

### Implementation
```javascript
// scripts/fetch-youtube-feed.js (runs at build time)
// 1. Fetch RSS XML from YouTube channel
// 2. Parse video titles, thumbnails, dates, IDs
// 3. Write to src/data/videos.json
// 4. videos.astro reads videos.json and renders grid
```

### Video Display
- Grid of video thumbnails + titles on `/videos` page
- Clicking opens a responsive YouTube embed (no iframe until click — performance)
- Latest 1–2 videos featured on the homepage
- Optional: embed relevant videos inline within newsletter/article pages

### TODO: Identify Paul's YouTube Channel
- [ ] Get Paul's YouTube channel URL or channel ID
- [ ] Verify RSS feed is accessible
- [ ] Determine if videos should be categorized/tagged to match written content

---

## 7. URL Redirect Strategy

Old visitors and search engines will have bookmarked the legacy URLs. A `_redirects` file handles this:

```
# Legacy → New URL mapping
/newsletters/40TheCovenantCircle.htm    /newsletters/40-the-covenant-circle/    301
/newsletters/37OrderofMelchiZedek.htm   /newsletters/37-order-of-melchizedek/   301
/newsletters/31sonshipovercomers.htm    /newsletters/31-birthing-overcomers/     301
/newsletters/21pauljab.htm              /newsletters/21-work-profile/            301
/book.htm                               /book/                                   301
/messages.htm                           /messages/                               301
/newsletters.htm                        /newsletters/                            301
/worshipJesusfeastssaved.htm            /articles/worship-in-spirit-and-truth/   301
/JesusSecondComing.htm                  /authors/roland-pletts/shekinah-glory/   301
/rolandpletts/index.htm                 /authors/roland-pletts/                  301
/bonniegaunt/about.htm                  /authors/bonnie-gaunt/                   301
/manchildBirth.htm                      /poems/birth-of-a-manchild/             301
/JudgeRoyMoore10commandments.htm        /articles/judge-roy-moore/              301
/starJesusbirth.htm                     /articles/star-of-bethlehem/            301
/mileswyliealbright.htm                 /miles-wylie-albright/                  301
```

Plus a catch-all for `pauljab.com`:
```
# pauljab.com → sonstoglory.com
/*    https://sonstoglory.com/:splat    301
```

---

## 8. Design Direction

### Guiding Principles
1. **Readability first** — This is a text-heavy site. Typography and whitespace matter more than flashy design.
2. **Warm and inviting** — Reflect the generous spirit of freely-given content.
3. **Uncluttered** — Let the writing breathe. No sidebar ads, no pop-ups, no visual noise.
4. **Accessible** — Large readable fonts, good contrast, works for older eyes.

### Typography
- **Headings:** Serif font (e.g., Merriweather, Lora, or Playfair Display) — conveys warmth, tradition, and authority for theological writing
- **Body:** Clean serif or sans-serif (e.g., Source Serif Pro, Inter, or system fonts) — optimized for long-form reading
- **Base size:** 18–20px body text (larger than typical — this audience skews older)

### Color Palette (Suggested)
- **Primary:** Deep navy or forest green — grounded, trustworthy
- **Accent:** Gold or warm amber — evokes light, glory, Kingdom themes
- **Background:** Warm off-white (#FAFAF5 or similar) — easier on eyes than pure white
- **Text:** Near-black (#1A1A2E) — strong contrast without harsh pure black

### Layout
- Single-column reading layout for articles (max-width ~700px for body text)
- Two-column grid for index/listing pages (cards with title, date, excerpt)
- Sticky header with logo + minimal nav
- Footer: mailing address, subscribe link, social links (YouTube)

---

## 9. Claude Code Session Checklist

When you sit down to build this with Claude Code, here's the order of operations:

### Session 1: Migration
```bash
# 1. Mirror the old site
wget --mirror --convert-links --adjust-extension --page-requisites \
     --no-parent https://sonstoglory.com/

# 2. Run the migration script (Claude Code can write this)
python scripts/migrate-html-to-md.py ./sonstoglory.com/ ./content/

# 3. Review and fix frontmatter
# 4. Commit the raw content to git
```

### Session 2: Scaffold
```bash
# 1. Init Astro project
npm create astro@latest -- --template minimal

# 2. Add Tailwind
npx astro add tailwind

# 3. Build layouts and components
# 4. Import content collection config
# 5. Deploy to Netlify/Cloudflare
```

### Session 3: Features
```bash
# 1. YouTube feed integration
# 2. Newsletter signup embed
# 3. Pagefind search
# 4. RSS feed
# 5. Redirects
```

### Session 4: Polish
```bash
# 1. SEO + sitemap
# 2. Performance audit
# 3. Accessibility pass
# 4. Analytics
# 5. Final QA
```

---

## 10. Open Questions

- [ ] What is Paul's YouTube channel URL?
- [ ] How many subscribers are on the current email list, and in what format is it stored?
- [ ] Does Paul want to continue publishing new newsletters? Or shift to video only?
- [ ] Are there any unpublished writings that should be added during migration?
- [ ] Domain registrar access — who controls DNS for sonstoglory.com and pauljab.com?
- [ ] Is there any content on the site that should be retired / not migrated?
- [ ] Does Paul have a preference between Astro (more flexible) and Hugo (faster builds, Go-based)?
- [ ] Budget for hosting/services? (Can be $0 with free tiers, but custom domain email or analytics may cost)

---

*This document is intended to live at the root of the git repository as `README.md` and evolve as the project progresses.*
