# CLAUDE.md — Sons To Glory Site Modernization

This file gives Claude Code the context needed to resume work on this project in any session.

---

## Project Overview

We are rebuilding [sonstoglory.com](https://sonstoglory.com) — a theological newsletter and writing site by Paul Jablonowski — from legacy static Dreamweaver HTML into a modern Astro-based static site.

**Repo:** `/home/joshjab/Documents/sonstoglory-mod`
**People:** Paul Jablonowski (content author, not technical), Josh Jablonowski (developer, running these sessions)

---

## Key Documents

| File | What it is |
|---|---|
| `doc/ROADMAP.md` | The master task list. **Check off tasks as you complete them.** |
| `doc/ARCH.md` | Architecture decisions and rationale. Update when decisions change. |
| `doc/CLAUDEPLAN.md` | Original discovery/planning document. Historical reference, do not modify. |
| `README.md` | Public-facing project description. Keep up to date as the project evolves. |

---

## Architecture Decisions (Summary)

- **SSG:** Astro (not Hugo)
- **Styling:** Tailwind CSS
- **Hosting:** GitHub Pages → AWS Lightsail if limits are hit
- **CMS:** Decap CMS with Cloudflare Worker OAuth proxy (free tier)
- **Email:** ConvertKit free tier (~500 subscribers)
- **Search:** Pagefind (build-time, zero cost)
- **Analytics:** Self-hosted Umami
- **YouTube:** Build-time RSS fetch from `@coolpixstargazer`
- **Budget:** Zero / free tiers only. No paid services without explicit approval.

Full details in `doc/ARCH.md`.

---

## Current Project Phase

**Phase 1 — Scaffold & Deploy** (in progress as of 2026-03-24)

### Phase 0 — COMPLETE
- [x] Legacy mirror (464 files, 2.1 GB)
- [x] Inventory script + content-inventory.csv (116 pages catalogued)
- [x] HTML → Markdown migration (101 files, scripts/migrate.py)
- [x] Frontmatter injected, content organized into src/content/
- [x] Static assets copied: 46 PDFs → public/pdfs/, 282 images → public/images/
- [x] Audio/video excluded from git (too large); stay on legacy server for now
- [x] 106 URL redirect rules → public/_redirects (scripts/generate_redirects.py)
- [x] Asset paths rewritten to absolute /images/ and /pdfs/ URLs (scripts/fix_asset_paths.py)

### Phase 1 — In Progress
- [x] GitHub repo: https://github.com/joshjab/sonstoglory-mod
- [x] Astro 4.16.19 + Tailwind CSS 3 scaffolded (Node 20, Astro 4 — NOT 5/6, requires Node 22)
- [x] src/content/config.ts — Zod schemas for newsletters, book, articles, authors
- [x] src/layouts/BaseLayout.astro — header, footer, mobile nav
- [x] src/pages/index.astro — homepage with hero, latest newsletters, book CTA
- [x] src/styles/global.css — Lora + Source Serif 4 fonts, brand palette
- [x] src/layouts/ArticleLayout.astro — title, author, date, reading time, prev/next nav
- [x] src/pages/newsletters/index.astro — full listing sorted by number desc
- [x] src/pages/newsletters/[slug].astro — dynamic detail route (41 pages, clean build)
- [ ] **Next: Milestone 1.7** — Deploy to GitHub Pages (.github/workflows/deploy.yml)
- [ ] Milestone 1.8 — Verify HTTPS + redirects on live site

### Key findings from Phase 0
- 41 newsletters (#1–#41, 2008–2021), all dated
- 4 guest authors: Roland Pletts, Bonnie Gaunt, Kenny Mitchell, Miles Wylie Albright
- Newsletter #41 was Paul's last — site is now an archive (videos continue on YouTube)
- Audio (MP3s) and video (MP4s) not in git — reference legacy server URLs for now
- `18newmooncelebrations.htm` is a redirect-only stub → canonical `18newmonthcelebrations.htm`

Check `doc/ROADMAP.md` for the full task list and current completion state.

---

## How We Work Together

### Task Tracking
- Work through `doc/ROADMAP.md` in order.
- **Check off each task (`- [x]`) immediately when it is complete.** Do not batch.
- When a phase or milestone is fully complete, note it in this file under "Current Project Phase."

### Code Quality
- **Write failing tests first, then implement.** This applies to all non-trivial code (Astro components, scripts with logic, utility functions). It does NOT apply to one-off migration scripts or config files.
- Keep code simple. Do not add abstractions, error handling, or features beyond what the current task requires.

### Evaluation Pauses
- At natural checkpoints (end of a milestone, before a major phase transition, after deploying something new), **pause and tell Josh what to test or verify** before proceeding. Be specific: URL to visit, thing to click, expected output.

### Pull Requests / Commits
- Do not push or create PRs without Josh explicitly asking.
- Prefer small, focused commits with clear messages.

### Open Questions
- One open question remains for Paul: **Are there any unpublished writings to include during migration?** Ask when starting Phase 0.3.

---

## Codebase Layout (Once Built)

```
sonstoglory-mod/
├── legacy-mirror/          # wget mirror of old site — DO NOT MODIFY
├── scripts/                # Migration and build-time scripts (Python + Node)
│   ├── inventory.py
│   ├── migrate.py
│   ├── add_frontmatter.py
│   ├── generate_redirects.py
│   └── fetch-youtube-feed.mjs
├── src/
│   ├── content/            # All Markdown content files
│   ├── layouts/            # Astro layout components
│   ├── pages/              # Astro page routes
│   ├── components/         # Reusable Astro components
│   ├── data/               # Build-time generated data (e.g. videos.json)
│   └── styles/
├── public/                 # Static assets (PDFs, images, _redirects)
├── doc/                    # Planning docs
├── CLAUDE.md               # This file
└── README.md
```

---

## YouTube Channel

Paul's channel handle: `@coolpixstargazer`
URL: `https://youtube.com/@coolpixstargazer`
Channel ID: TBD — extract from channel page source when implementing Phase 2.5.

---

## Important Technical Notes

- **Node version**: Must use Node 20 (system). Astro 4 was chosen because Astro 5/6 requires Node 22.
- **Dev server**: Run `npm run dev -- --host` to expose on local network (user remotes in from another machine).
- **Build**: `npm run build` — clean, no warnings as of last commit.
- **Cloudflare Worker for Decap CMS OAuth** confirmed free (100k req/day). Implement in Milestone 2.5.1.
- **Audio/video not in git**: MP4s (1.9GB) and MP3s (217MB) excluded from git. `public/video/` and `public/audio/` in .gitignore. Files exist locally but need a media hosting decision before launch.
- **Legacy mirror**: Read-only source at `legacy-mirror/sonstoglory.com/`. pauljab.com mirror has only 5 files — it's just a landing page.
- **package.json name** is still "astro-scaffold" — worth renaming to "sonstoglory" in a future cleanup pass.
