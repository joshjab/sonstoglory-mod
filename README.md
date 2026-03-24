# Sons To Glory — Site Modernization

Modernizing [sonstoglory.com](https://sonstoglory.com) — a theological writing and newsletter site authored by Paul Jablonowski — from a static Dreamweaver-era HTML site into a modern, mobile-responsive static site with a proper publishing workflow.

## What This Repo Is

This is the **build repository** for the new sonstoglory.com. It contains:

- Migrated content (Markdown files converted from legacy HTML)
- The new Astro-based static site
- Migration and build scripts
- A legacy mirror of the original site (for reference and migration)
- Architecture and planning documentation

The site is published via GitHub Pages and rebuilt automatically on every commit to `main`, as well as on a daily schedule to pull in new YouTube videos.

## Site Features

- Mobile-responsive reading experience for 40+ newsletters, a multi-chapter book, standalone articles, and poems
- YouTube video feed (auto-updated daily from Paul's channel)
- Newsletter signup via ConvertKit
- Full-text search via Pagefind (build-time, zero cost)
- RSS feed
- URL redirects preserving all legacy links
- Privacy-first analytics via self-hosted Umami
- Dark mode toggle
- Web-based CMS (Decap CMS) so Paul can publish new newsletters without touching code

## Tech Stack

| Layer | Tool |
|---|---|
| Static site generator | [Astro](https://astro.build) |
| Styling | [Tailwind CSS](https://tailwindcss.com) |
| Content | Markdown with YAML frontmatter |
| Hosting | GitHub Pages |
| CMS | [Decap CMS](https://decapcms.org) + Cloudflare Worker (OAuth proxy) |
| Email | ConvertKit (free tier) |
| Search | [Pagefind](https://pagefind.app) |
| Analytics | Self-hosted [Umami](https://umami.is) |
| YouTube | Build-time RSS fetch (`@coolpixstargazer`) |

## Project Status

Currently in **Phase 0 — Content Migration**. The legacy site is being mirrored locally; HTML-to-Markdown conversion and Astro scaffold come next.

See [`doc/ROADMAP.md`](doc/ROADMAP.md) for the full implementation plan with task-level detail.

## Documentation

| File | Purpose |
|---|---|
| [`doc/ROADMAP.md`](doc/ROADMAP.md) | Phase-by-phase implementation plan with checkable tasks |
| [`doc/ARCH.md`](doc/ARCH.md) | Architecture decision record — stack choices and rationale |
| [`doc/CLAUDEPLAN.md`](doc/CLAUDEPLAN.md) | Original discovery & planning document (historical reference) |

## Repository Layout

```
sonstoglory-mod/
├── legacy-mirror/          # wget mirror of original sonstoglory.com and pauljab.com
├── scripts/                # Migration and build-time utility scripts
├── src/                    # Astro site source (layouts, pages, components, content)
├── public/                 # Static assets (PDFs, images, _redirects)
├── doc/                    # Planning and architecture docs
├── CLAUDE.md               # AI session context and working conventions
└── README.md               # This file
```

## Development

```bash
npm install
npm run dev        # Start dev server at localhost:4321
npm run build      # Full production build (includes YouTube fetch + Pagefind index)
npm run preview    # Preview the production build locally
```

## Contributing

This is a personal family project. Paul Jablonowski authors the content; Josh Jablonowski manages the technical side.
