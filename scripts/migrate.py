#!/usr/bin/env python3
"""
migrate.py — Convert legacy HTML pages to Markdown with YAML frontmatter.

Reads content-inventory.csv, processes each migratable page:
  1. Parses HTML, strips Dreamweaver layout wrapper (outer nav table)
  2. Extracts the content body
  3. Converts to Markdown via pandoc
  4. Prepends YAML frontmatter from inventory data
  5. Writes to content/<type>/<slug>.md

Usage:
    python3 scripts/migrate.py              # migrate all
    python3 scripts/migrate.py --file newsletters/40TheCovenantCircle.htm
    python3 scripts/migrate.py --dry-run    # print paths without writing

Skips types: index, book-request, redirect-only
"""

import argparse
import csv
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MIRROR_ROOT = REPO_ROOT / "legacy-mirror" / "sonstoglory.com"
CONTENT_ROOT = REPO_ROOT / "src" / "content"
INVENTORY_CSV = REPO_ROOT / "content-inventory.csv"

SKIP_TYPES = {"index", "book-request", "redirect-only"}

TYPE_TO_DIR = {
    "newsletter": "newsletters",
    "book-chapter": "book",
    "article": "articles",
    "guest-author": "authors",
    "poem": "poems",
}

# Dreamweaver comment markers used in templates
DW_COMMENT_RE = re.compile(r'<!--\s*#(?:Begin|End)\w+.*?-->', re.IGNORECASE | re.DOTALL)


class TableStripper(HTMLParser):
    """
    Strip the outermost layout <table> from Dreamweaver pages.

    Dreamweaver pages use a single top-level <table> as a layout shell:
      <body>
        <table>           ← layout wrapper (nav header, content, nav footer rows)
          <tr><td>nav</td></tr>
          <tr><td>CONTENT</td></tr>   ← we want this
          <tr><td>nav</td></tr>
        </table>
      </body>

    Strategy: find the outermost <table>, collect all <td> content,
    discard the first row (site nav) and last row (site nav footer),
    return the inner HTML of the remaining rows joined together.

    Falls back to full <body> content if no wrapping table is found.
    """

    def __init__(self):
        super().__init__()
        self.depth = 0               # overall tag nesting depth
        self.table_depth = 0         # <table> nesting depth
        self.in_outer_table = False
        self.outer_table_found = False
        self.rows = []               # list of HTML strings, one per <tr>
        self._current_row = []       # buffer for current <tr>
        self._in_row = False
        self._row_depth = 0
        self._body_content = []      # fallback: everything inside <body>
        self._in_body = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        raw = self._rebuild_tag(tag, attrs)

        if tag == "body":
            self._in_body = True
            return

        if self._in_body:
            self._body_content.append(raw)

        if tag == "table":
            self.table_depth += 1
            if self.table_depth == 1:
                self.in_outer_table = True
                self.outer_table_found = True
                return   # don't include the outer <table> tag itself

        if self.in_outer_table and self.table_depth == 1:
            if tag == "tr":
                self._in_row = True
                self._row_depth = 0
                self._current_row = []
                return
            if tag in ("td", "th") and self._in_row:
                self._row_depth += 1

        if self._in_row:
            self._current_row.append(raw)

        self.depth += 1

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == "body":
            self._in_body = False
            return

        if self._in_body and not (self.in_outer_table and self.table_depth >= 1):
            self._body_content.append(f"</{tag}>")

        if tag == "table":
            if self.table_depth == 1:
                self.in_outer_table = False
            self.table_depth -= 1
            if self.table_depth == 0:
                return

        if self.in_outer_table and self.table_depth == 1 and tag == "tr" and self._in_row:
            self.rows.append("".join(self._current_row))
            self._current_row = []
            self._in_row = False
            return

        if self._in_row:
            self._current_row.append(f"</{tag}>")

        if self.depth > 0:
            self.depth -= 1

    def handle_data(self, data):
        if self._in_body:
            if self._in_row:
                self._current_row.append(data)
            elif not self.in_outer_table:
                self._body_content.append(data)

    def handle_entityref(self, name):
        ref = f"&{name};"
        if self._in_row:
            self._current_row.append(ref)
        elif self._in_body:
            self._body_content.append(ref)

    def handle_charref(self, name):
        ref = f"&#{name};"
        if self._in_row:
            self._current_row.append(ref)
        elif self._in_body:
            self._body_content.append(ref)

    @staticmethod
    def _rebuild_tag(tag, attrs):
        if not attrs:
            return f"<{tag}>"
        attr_str = ""
        for k, v in attrs:
            if v is None:
                attr_str += f" {k}"
            else:
                v_escaped = v.replace('"', "&quot;")
                attr_str += f' {k}="{v_escaped}"'
        return f"<{tag}{attr_str}>"

    def get_content_html(self):
        """Return the inner HTML of the content rows (strip first and last nav rows)."""
        if not self.outer_table_found or len(self.rows) < 2:
            # Fallback: return full body content
            return "".join(self._body_content)

        # The outer layout table typically has:
        #   row 0: site nav header
        #   row 1..N-2: actual content
        #   row N-1: site nav footer
        # For pages with exactly 2 rows, take row 1 (skip row 0 nav header).
        if len(self.rows) == 2:
            content_rows = self.rows[1:]
        else:
            content_rows = self.rows[1:-1]

        return "".join(content_rows)


def clean_html(raw_bytes):
    """Decode, strip Dreamweaver artifacts, extract content HTML."""
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = raw_bytes.decode("latin-1")

    # Strip the non-standard custom tag at top/bottom of every page
    text = re.sub(r'<Jesus[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</Jesus[^>]*>', '', text, flags=re.IGNORECASE)

    # Strip Dreamweaver template comments
    text = DW_COMMENT_RE.sub('', text)

    parser = TableStripper()
    try:
        parser.feed(text)
    except Exception:
        pass

    return parser.get_content_html()


def html_to_markdown(html_content):
    """Run pandoc to convert HTML string to Markdown."""
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w",
                                     encoding="utf-8", delete=False) as f:
        f.write(f"<html><body>{html_content}</body></html>")
        tmp_path = f.name

    try:
        result = subprocess.run(
            [
                "pandoc",
                tmp_path,
                "--from=html",
                "--to=markdown_strict",
                "--wrap=none",
                "--no-highlight",
                "--strip-comments",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"pandoc error: {result.stderr}")
        return result.stdout
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def clean_markdown(md):
    """Post-process pandoc output: collapse excessive blank lines, trim noise."""
    # Collapse 3+ consecutive blank lines to 2
    md = re.sub(r'\n{4,}', '\n\n\n', md)
    # Remove trailing whitespace on each line
    md = "\n".join(line.rstrip() for line in md.splitlines())
    # Remove lines that are just &nbsp; artifacts
    md = re.sub(r'^\s*\\\s*$', '', md, flags=re.MULTILINE)
    # Collapse again after cleanup
    md = re.sub(r'\n{4,}', '\n\n\n', md)
    return md.strip()


def build_frontmatter(row):
    """Build YAML frontmatter string from a CSV inventory row."""
    title = row["title"].replace('"', '\\"')
    description = row["description"].replace('"', '\\"')
    author = row["author"].replace('"', '\\"')
    date = row["estimated_date"] or ""
    tags = []  # Tags to be filled in manually post-migration
    legacy_url = row["legacy_url"]
    content_type = row["type"]
    number = row["newsletter_number"]

    lines = ['---']
    lines.append(f'title: "{title}"')
    lines.append(f'author: "{author}"')
    if date:
        lines.append(f'date: "{date}"')
    lines.append(f'type: {content_type}')
    if number:
        lines.append(f'number: {number}')
    lines.append(f'description: "{description}"')
    lines.append('tags: []')
    lines.append(f'legacy_url: "{legacy_url}"')
    lines.append('---')
    return "\n".join(lines)


def output_path(row):
    """Determine the output .md file path for a row."""
    content_type = row["type"]
    slug = row["slug"]
    path = row["path"]

    dir_name = TYPE_TO_DIR.get(content_type, "articles")

    if content_type == "guest-author":
        # e.g. rolandpletts/about.htm → authors/roland-pletts/about.md
        parts = Path(path).parts
        author_folder = parts[0].replace("rolandpletts", "roland-pletts") \
                                 .replace("bonniegaunt", "bonnie-gaunt") \
                                 .replace("kennymitchell", "kenny-mitchell") \
                                 .replace("milesalbright", "miles-albright")
        filename = slug + ".md"
        return CONTENT_ROOT / dir_name / author_folder / filename

    return CONTENT_ROOT / dir_name / (slug + ".md")


def migrate_row(row, dry_run=False):
    """Process a single inventory row. Returns (output_path, status_str)."""
    content_type = row["type"]
    if content_type in SKIP_TYPES:
        return None, "skip"

    src = MIRROR_ROOT / row["path"]
    if not src.exists():
        return None, f"missing: {src}"

    out = output_path(row)

    if dry_run:
        return out, "dry-run"

    raw = src.read_bytes()
    content_html = clean_html(raw)
    md = html_to_markdown(content_html)
    md = clean_markdown(md)
    frontmatter = build_frontmatter(row)
    final = frontmatter + "\n\n" + md + "\n"

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(final, encoding="utf-8")
    return out, "ok"


def main():
    parser = argparse.ArgumentParser(description="Migrate legacy HTML to Markdown")
    parser.add_argument("--file", help="Migrate only this legacy path (relative to sonstoglory.com/)")
    parser.add_argument("--dry-run", action="store_true", help="Print output paths without writing")
    args = parser.parse_args()

    rows = list(csv.DictReader(INVENTORY_CSV.open()))

    if args.file:
        rows = [r for r in rows if r["path"] == args.file]
        if not rows:
            print(f"ERROR: '{args.file}' not found in inventory", file=sys.stderr)
            sys.exit(1)

    ok = skip = errors = 0
    for row in rows:
        out, status = migrate_row(row, dry_run=args.dry_run)
        if status == "skip":
            skip += 1
        elif status in ("ok", "dry-run"):
            label = "DRY" if args.dry_run else " OK"
            print(f"[{label}] {row['path']}\n      → {out}")
            ok += 1
        else:
            print(f"[ERR] {row['path']} — {status}", file=sys.stderr)
            errors += 1

    print(f"\nDone: {ok} converted, {skip} skipped, {errors} errors")


if __name__ == "__main__":
    main()
