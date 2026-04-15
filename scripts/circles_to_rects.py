#!/usr/bin/env python

"""
Convert <circle cx cy r .../> elements to centered rounded <rect/>.

Mapping:
  cx, cy, r  ->  x = cx-r, y = cy-r, width = 2r, height = 2r,
                 rx = min(r, 14)

All other attributes (fill, stroke, stroke-width, opacity, filter, ...)
are preserved verbatim. Skips <circle> elements inside <defs>.

Usage: circles_to_rects.py [--dry-run] svg/**/*.svg
"""

import argparse
import pathlib
import re
import sys

ATTR_RE = re.compile(r'\b([\w-]+)="([^"]*)"')
CIRCLE_RE = re.compile(r'<circle\b([^/>]*)/\s*>')
DEFS_RE = re.compile(r'<defs\b.*?</defs>', re.DOTALL)


def convert_circle(match: re.Match) -> str:
    body = match.group(1)
    attrs = dict(ATTR_RE.findall(body))
    try:
        cx = float(attrs.pop("cx", "0"))
        cy = float(attrs.pop("cy", "0"))
        r = float(attrs.pop("r"))
    except (KeyError, ValueError):
        return match.group(0)

    x = cx - r
    y = cy - r
    w = 2 * r
    rx = min(r, 14.0)

    parts = []
    parts.append(f'x="{x:g}"')
    parts.append(f'y="{y:g}"')
    parts.append(f'width="{w:g}"')
    parts.append(f'height="{w:g}"')
    parts.append(f'rx="{rx:g}"')
    for k, v in attrs.items():
        parts.append(f'{k}="{v}"')
    return "<rect " + " ".join(parts) + "/>"


def process(text: str) -> tuple[str, int]:
    defs_spans = [m.span() for m in DEFS_RE.finditer(text)]

    def in_defs(pos: int) -> bool:
        return any(a <= pos < b for a, b in defs_spans)

    out = []
    last = 0
    n = 0
    for m in CIRCLE_RE.finditer(text):
        out.append(text[last:m.start()])
        if in_defs(m.start()):
            out.append(m.group(0))
        else:
            out.append(convert_circle(m))
            n += 1
        last = m.end()
    out.append(text[last:])
    return "".join(out), n


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    total_circles = 0
    total_files = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file() or path.suffix != ".svg":
            continue
        if path.name == "title.svg":
            continue
        text = path.read_text(encoding="utf-8")
        new, n = process(text)
        if n == 0:
            continue
        total_files += 1
        total_circles += n
        if not args.dry_run:
            path.write_text(new, encoding="utf-8")

    action = "would convert" if args.dry_run else "converted"
    print(f"{action} {total_circles} <circle> in {total_files} file(s)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
