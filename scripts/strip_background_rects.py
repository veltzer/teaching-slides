#!/usr/bin/env python

"""
Strip full-slide background rects from SVGs.

A background rect is identified by:
  - x <= 60, y <= 60
  - width >= 1000, height >= 500
  - fill is one of: var(--bg), var(--surface), none

Content-colored full-slide rects (primary-fill, text, warn-fill, etc.)
are left alone — they are typically intentional hero/alert backgrounds.

Usage: strip_background_rects.py [--dry-run] [--list] svg/**/*.svg
"""

import argparse
import pathlib
import re
import sys

NEUTRAL_FILLS = {"var(--bg)", "var(--surface)", "none"}
RECT_RE = re.compile(r'<rect\b[^/>]*/>')
ATTR_RE = re.compile(r'\b(\w[\w-]*)="([^"]*)"')


def is_background_rect(tag: str) -> bool:
    attrs = dict(ATTR_RE.findall(tag))
    try:
        x = float(attrs.get("x", "0"))
        y = float(attrs.get("y", "0"))
        w = float(attrs["width"])
        h = float(attrs["height"])
    except (KeyError, ValueError):
        return False
    if not (x <= 60 and y <= 60 and w >= 1000 and h >= 500):
        return False
    fill = attrs.get("fill", "").strip()
    return fill in NEUTRAL_FILLS


def strip_one(path: pathlib.Path, dry_run: bool) -> bool:
    if path.name == "title.svg":
        return False
    s = path.read_text(encoding="utf-8")
    m = RECT_RE.search(s)
    if not m or not is_background_rect(m.group(0)):
        return False
    start, end = m.span()
    before = s[:start]
    after = s[end:]
    stripped = before.rstrip() + "\n" + after.lstrip("\n")
    stripped = re.sub(r"\n{3,}", "\n\n", stripped)
    if not dry_run:
        path.write_text(stripped, encoding="utf-8")
    return True


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--list", action="store_true", help="print affected paths")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    changed = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file():
            continue
        if strip_one(path, dry_run=args.dry_run):
            changed += 1
            if args.list:
                print(path)

    action = "would strip" if args.dry_run else "stripped"
    print(f"{action} background rect from {changed} file(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
