#!/usr/bin/env python3
"""
fix_asset_paths.py — Rewrite relative asset paths in converted Markdown files.

Each Markdown file has a legacy_url in its frontmatter (e.g. /newsletters/40TheCovenantCircle.htm).
Relative image/PDF/audio/video paths in the body are resolved against that legacy URL's directory,
then rewritten to absolute paths under /images/, /pdfs/, /audio/, /video/.

Usage:
    python3 scripts/fix_asset_paths.py           # rewrite all files in-place
    python3 scripts/fix_asset_paths.py --dry-run  # print changes without writing
"""

import argparse
import re
import sys
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).parent.parent
CONTENT_ROOT = REPO_ROOT / "src" / "content"
PUBLIC_ROOT = REPO_ROOT / "public"

# Extensions and where they live under public/
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".ico", ".JPG", ".JPEG", ".PNG", ".GIF"}
PDF_EXTS   = {".pdf", ".PDF"}
AUDIO_EXTS = {".mp3", ".m4a", ".MP3"}
VIDEO_EXTS = {".mp4", ".MP4"}

# Where images were copied: rsync'd mirror root → public/images/
# So sonstoglory.com/newsletters/pictures/foo.jpg → /images/newsletters/pictures/foo.jpg

# PDFs were copied to a simplified structure — build a lookup from filename → public path
def build_pdf_index():
    index = {}
    for p in PUBLIC_ROOT.rglob("*.pdf"):
        index[p.name.lower()] = "/" + str(p.relative_to(PUBLIC_ROOT)).replace("\\", "/")
    for p in PUBLIC_ROOT.rglob("*.PDF"):
        index[p.name.lower()] = "/" + str(p.relative_to(PUBLIC_ROOT)).replace("\\", "/")
    return index

def build_image_index():
    """Map filename (lowercased) → list of /images/... paths (may have duplicates)."""
    index = {}
    for p in PUBLIC_ROOT.rglob("*"):
        if p.suffix in IMAGE_EXTS and p.is_file():
            key = p.name.lower()
            path_str = "/" + str(p.relative_to(PUBLIC_ROOT)).replace("\\", "/")
            index.setdefault(key, []).append(path_str)
    return index


def resolve_asset_url(rel_path: str, legacy_base: str, pdf_index: dict, image_index: dict) -> str | None:
    """
    Given a relative asset path and the legacy base dir (e.g. /newsletters/),
    return the new absolute public URL, or None if we can't resolve it.
    """
    if rel_path.startswith("http://") or rel_path.startswith("https://"):
        return None  # external, leave as-is

    # Resolve against legacy base — manually handle ../ traversal
    base = PurePosixPath(legacy_base)
    parts = []
    for part in (base / rel_path).parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part != ".":
            parts.append(part)
    resolved_str = "/".join(parts).lstrip("/")
    # resolved_str is now relative to site root, e.g. "newsletters/pictures/foo.jpg"

    p = PurePosixPath(resolved_str)
    ext = p.suffix.lower()
    filename = p.name

    if ext in {s.lower() for s in PDF_EXTS}:
        hit = pdf_index.get(filename.lower())
        if hit:
            return hit
        return f"/pdfs/{filename}"  # best guess

    if ext in {s.lower() for s in IMAGE_EXTS}:
        # First try: exact path match under public/images/
        candidate = PUBLIC_ROOT / "images" / resolved_str
        if candidate.exists():
            return f"/images/{resolved_str}"

        # Second try: look up by filename in index
        hits = image_index.get(filename.lower(), [])
        if len(hits) == 1:
            return hits[0]
        elif len(hits) > 1:
            # Pick the hit whose path contains the most path components in common
            best = max(hits, key=lambda h: len(set(h.split("/")) & set(resolved_str.split("/"))))
            return best

        return f"/images/{resolved_str}"  # fallback

    if ext in {s.lower() for s in AUDIO_EXTS}:
        # Audio not in git — keep pointing to legacy server path for now
        return None

    if ext in {s.lower() for s in VIDEO_EXTS}:
        # Video not in git — keep pointing to legacy server path for now
        return None

    return None


FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)
LEGACY_URL_RE  = re.compile(r'^legacy_url:\s*"([^"]+)"', re.MULTILINE)

# Match src="..." and href="..." for asset files
ASSET_ATTR_RE  = re.compile(
    r'(src|href)="([^"]*\.(jpg|jpeg|png|gif|ico|pdf|PDF|mp3|m4a|mp4|JPG|JPEG|PNG|GIF))"',
    re.IGNORECASE
)


def process_file(md_path: Path, pdf_index: dict, image_index: dict, dry_run: bool) -> int:
    text = md_path.read_text(encoding="utf-8")

    m = LEGACY_URL_RE.search(text)
    if not m:
        return 0
    legacy_url = m.group(1)  # e.g. /newsletters/40TheCovenantCircle.htm
    legacy_base = str(PurePosixPath(legacy_url).parent)  # e.g. /newsletters

    changes = 0

    def replacer(match):
        nonlocal changes
        attr, path, ext = match.group(1), match.group(2), match.group(3)
        new_path = resolve_asset_url(path, legacy_base, pdf_index, image_index)
        if new_path and new_path != path:
            changes += 1
            if dry_run:
                print(f"  {path}\n    → {new_path}")
            return f'{attr}="{new_path}"'
        return match.group(0)

    new_text = ASSET_ATTR_RE.sub(replacer, text)

    if changes and not dry_run:
        md_path.write_text(new_text, encoding="utf-8")

    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    pdf_index   = build_pdf_index()
    image_index = build_image_index()

    total_files = total_changes = 0
    for md_path in sorted(CONTENT_ROOT.rglob("*.md")):
        n = process_file(md_path, pdf_index, image_index, args.dry_run)
        if n:
            if args.dry_run:
                print(f"[{md_path.relative_to(CONTENT_ROOT)}] {n} changes")
            total_files += 1
            total_changes += n

    print(f"\n{'Would update' if args.dry_run else 'Updated'}: {total_files} files, {total_changes} asset references")


if __name__ == "__main__":
    main()
