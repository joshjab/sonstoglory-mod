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

**Phase 0 — Content Migration** (in progress as of 2026-03-24)

- [x] Git repo initialized
- [x] `doc/ROADMAP.md`, `doc/ARCH.md`, `CLAUDE.md`, `README.md` created
- [x] sonstoglory.com mirror complete — 464 files, 2.1 GB (`legacy-mirror/sonstoglory.com/`)
- [x] pauljab.com mirror complete — 5 files, landing page only (`legacy-mirror/pauljab.com/`)
- [x] Inventory script written (`scripts/inventory.py`) and run → `content-inventory.csv` (116 rows)
- [ ] **Next:** Milestone 0.3 — HTML → Markdown conversion (`scripts/migrate.py`)

### Inventory findings (important for next session)
- 41 newsletters (#1–#41, 2008–2021), all dated
- **4 guest authors** (not 2 as originally planned): Roland Pletts, Bonnie Gaunt, Kenny Mitchell, Miles Wylie Albright
- 39 articles, 10 book-chapters, 5 book-request pages, 10 index/nav pages
- `18newmooncelebrations.htm` is a redirect-only stub (canonical is `18newmonthcelebrations.htm`)
- 14 MP3s + 4 MP4s in the mirror — copy to `public/audio/` and `public/video/`
- `temple.htm` has an empty title — needs manual check during migration

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

## Notes for Future Sessions

- The Cloudflare Worker for Decap CMS OAuth is confirmed as the approach. It is genuinely free (100k req/day). Implement in Milestone 2.5.1.
- The `--wait=1 --random-wait` flags were used during mirroring to avoid hammering the server. The mirror lives in `legacy-mirror/` and should be treated as read-only source material.
- pauljab.com is essentially just a landing page that redirects to sonstoglory.com — only 5 files downloaded. The real content is all on sonstoglory.com.
