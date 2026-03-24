#!/usr/bin/env python3
"""
inventory.py — Crawl the legacy-mirror and produce content-inventory.csv

Usage:
    python scripts/inventory.py > content-inventory.csv

Columns:
    path         - relative path from sonstoglory.com root (e.g. newsletters/40TheCovenantCircle.htm)
    filename     - bare filename
    title        - from <title> tag
    description  - from <meta name="description">
    type         - inferred: newsletter | book-chapter | article | guest-author | index | unknown
    author       - from <meta name="Author"> or inferred
    newsletter_number - integer if type==newsletter, else blank
    estimated_date - parsed from page body (YYYY-MM-DD or YYYY-MM or YYYY)
    legacy_url   - full legacy URL path (for _redirects generation)
    slug         - suggested new URL slug
"""

import csv
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

MIRROR_ROOT = Path(__file__).parent.parent / "legacy-mirror" / "sonstoglory.com"

# Book chapter filenames (root level, non-newsletter)
BOOK_CHAPTERS = {
    "foreword.htm", "book.htm", "endnotes.htm", "covenantofpeace.htm",
    "spiritualadoption.htm", "spiritualauthority.htm", "spiritualfathersons.htm",
    "sonshipofwomen.htm", "moderndayapostles.htm", "womenapostlesleaders.htm",
}

# Index / nav pages — not standalone content
INDEX_PAGES = {
    "index.htm", "index.html", "newsletters.htm", "messages.htm",
    "aboutsonstoglory.htm", "friends.htm", "pray.htm", "temple.htm",
    "signs.htm", "Finances.htm",
}

# Known month names for date parsing
MONTHS = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12",
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10",
    "nov": "11", "dec": "12",
}


class MetaParser(HTMLParser):
    """Extract <title>, <meta name="description">, <meta name="author"> from HTML."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.author = ""
        self._in_title = False
        self._title_done = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k.lower(): v for k, v in attrs}
        if tag.lower() == "title" and not self._title_done:
            self._in_title = True
        elif tag.lower() == "meta":
            name = attrs_dict.get("name", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.description = content.strip()
            elif name == "author":
                self.author = content.strip()

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False
            self._title_done = True
            self.title = self.title.strip()


def extract_date(text):
    """
    Try to find a publication date in the page body text.
    Returns YYYY-MM-DD, YYYY-MM, or YYYY string, or empty string.
    Looks for patterns like:
      - "April 27, 2021"
      - "Passover - April 27, 2021"
      - "June 2011"
      - "2021"
    """
    # "Month DD, YYYY"
    m = re.search(
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+(\d{1,2}),?\s+(20\d{2}|19\d{2})\b',
        text, re.IGNORECASE
    )
    if m:
        month = MONTHS[m.group(1).lower()]
        day = m.group(2).zfill(2)
        year = m.group(3)
        return f"{year}-{month}-{day}"

    # "Month YYYY"
    m = re.search(
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+(20\d{2}|19\d{2})\b',
        text, re.IGNORECASE
    )
    if m:
        month = MONTHS[m.group(1).lower()]
        year = m.group(2)
        return f"{year}-{month}"

    # Bare year in a plausible range
    m = re.search(r'\b(200[0-9]|201[0-9]|202[0-9])\b', text)
    if m:
        return m.group(1)

    return ""


def infer_type(rel_path, filename, title):
    """Infer content type from path and filename."""
    parts = rel_path.parts

    if parts[0] == "newsletters":
        return "newsletter"
    if parts[0] in ("rolandpletts", "bonniegaunt", "kennymitchell", "milesalbright"):
        return "guest-author"
    if parts[0] == "Jesus":
        return "article"

    # Root-level files
    if filename in INDEX_PAGES:
        return "index"
    if filename in BOOK_CHAPTERS:
        return "book-chapter"

    # Book-request / order pages (not content, just mailing address forms)
    BOOK_REQUEST_PAGES = {
        "bonniegaunt.htm", "kennymitchell.htm", "mileswyliealbright.htm",
        "pauljablonowski.htm", "rolandpletss.htm",
    }
    if filename in BOOK_REQUEST_PAGES:
        return "book-request"

    # Known redirect-only stub (duplicate of 18newmonthcelebrations.htm)
    if filename == "18newmooncelebrations.htm":
        return "redirect-only"

    return "article"


def infer_author(path_parts, meta_author, content_type):
    GUEST_AUTHOR_NAMES = {
        "rolandpletts": "Roland Pletts",
        "bonniegaunt": "Bonnie Gaunt",
        "kennymitchell": "Kenny Mitchell",
        "milesalbright": "Miles Wylie Albright",
    }
    if content_type == "guest-author" and path_parts:
        name = GUEST_AUTHOR_NAMES.get(path_parts[0])
        if name:
            return name
    if meta_author:
        return meta_author
    return "Paul Jablonowski"


def newsletter_number(filename):
    """Extract leading newsletter number from filename like '40TheCovenantCircle.htm'."""
    m = re.match(r'^(\d+)', filename)
    if m:
        return int(m.group(1))
    return ""


def slugify(text):
    """Convert a string to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def suggested_slug(filename, title, content_type, num):
    """Generate a suggested new URL slug."""
    base = os.path.splitext(filename)[0]
    if content_type == "newsletter" and num:
        # Use number + slugified title
        clean_title = re.sub(r'^\s*newsletter\s*#?\d+\s*[-—]*\s*', '', title, flags=re.IGNORECASE)
        clean_title = re.sub(r'\s*sons\s*to\s*glory\s*newsletter.*', '', clean_title, flags=re.IGNORECASE)
        slug = f"{num:02d}-{slugify(clean_title)}" if clean_title else slugify(base)
        return slug
    return slugify(base)


def process_file(html_path):
    """Return a dict of inventory fields for one HTML file."""
    rel = html_path.relative_to(MIRROR_ROOT)
    filename = html_path.name

    try:
        raw = html_path.read_bytes()
        # Try UTF-8, fall back to latin-1 (Dreamweaver-era pages)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")
    except Exception as e:
        return None

    parser = MetaParser()
    try:
        parser.feed(text)
    except Exception:
        pass

    content_type = infer_type(rel, filename, parser.title)
    num = newsletter_number(filename) if content_type == "newsletter" else ""
    author = infer_author(rel.parts[:-1] if len(rel.parts) > 1 else [], parser.author, content_type)
    date = extract_date(text[:3000])  # Search first 3000 chars where dates usually appear
    slug = suggested_slug(filename, parser.title, content_type, num)
    legacy_url = "/" + str(rel).replace("\\", "/")

    return {
        "path": str(rel).replace("\\", "/"),
        "filename": filename,
        "title": parser.title,
        "description": parser.description,
        "type": content_type,
        "author": author,
        "newsletter_number": num,
        "estimated_date": date,
        "legacy_url": legacy_url,
        "slug": slug,
    }


def main():
    html_files = sorted(
        MIRROR_ROOT.rglob("*.htm"),
        key=lambda p: (len(p.parts), str(p))
    )
    html_files += sorted(MIRROR_ROOT.rglob("*.html"), key=lambda p: (len(p.parts), str(p)))

    fieldnames = [
        "path", "filename", "title", "description", "type", "author",
        "newsletter_number", "estimated_date", "legacy_url", "slug",
    ]

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()

    for html_path in html_files:
        row = process_file(html_path)
        if row:
            writer.writerow(row)


if __name__ == "__main__":
    main()
