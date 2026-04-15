#!/usr/bin/env python

"""
Ensure every <text> and <tspan> has an explicit fill attribute.

Elements without fill render in the browser/renderer default (usually
black), which is invisible on dark/gradient family-fill rects. This
script infers the correct fill:

  - If the text's (x,y) falls inside a family-fill rect (fill is
    var(--primary-fill), var(--ok-fill), etc. — solid or gradient),
    the text is given var(--{family}-text).
  - Otherwise it gets var(--text) (dark body text).

Idempotent — skips elements that already have a fill attribute.

Usage: fix_svg_text_fill.py [--dry-run] svg/**/*.svg
"""

import argparse
import pathlib
import re
import sys

FAMILY_NAMES = ["primary", "ok", "warn", "danger", "info"]
FAMILY_FILL_TOKENS = {
    f"var(--{f}-fill)": f for f in FAMILY_NAMES
} | {
    f"url(#grad-{f})": f for f in FAMILY_NAMES
}

RECT_RE = re.compile(
    r'<rect\b[^/>]*?\bx="([\d.]+)"[^/>]*?\by="([\d.]+)"[^/>]*?'
    r'\bwidth="([\d.]+)"[^/>]*?\bheight="([\d.]+)"[^/>]*?'
    r'\bfill="([^"]+)"[^/>]*?/\s*>',
    re.DOTALL,
)
# Also handle alternate attribute ordering
RECT_RE_LOOSE = re.compile(r'<rect\b([^/>]*)/\s*>')
ATTR_RE = re.compile(r'\b([\w-]+)="([^"]*)"')
TEXT_RE = re.compile(r'<(text|tspan)\b([^>]*)>')


def rect_family(rect_attrs_str: str) -> tuple[float, float, float, float, str] | None:
    attrs = dict(ATTR_RE.findall(rect_attrs_str))
    try:
        x = float(attrs.get("x", "0"))
        y = float(attrs.get("y", "0"))
        w = float(attrs["width"])
        h = float(attrs["height"])
    except (KeyError, ValueError):
        return None
    fill = attrs.get("fill", "").strip()
    fam = FAMILY_FILL_TOKENS.get(fill)
    if fam is None:
        return None
    return (x, y, w, h, fam)


def find_family_rects(text: str) -> list[tuple[float, float, float, float, str]]:
    rects = []
    for m in RECT_RE_LOOSE.finditer(text):
        r = rect_family(m.group(1))
        if r is not None:
            rects.append(r)
    return rects


def containing_family(px: float, py: float,
                      rects: list[tuple[float, float, float, float, str]]) -> str | None:
    """Pick the innermost (smallest-area) rect whose box contains (px, py)."""
    best = None
    best_area = None
    for (x, y, w, h, fam) in rects:
        if x <= px <= x + w and y <= py <= y + h:
            area = w * h
            if best_area is None or area < best_area:
                best = fam
                best_area = area
    return best


def transform(text: str) -> tuple[str, int]:
    rects = find_family_rects(text)
    changed = 0

    def fix(m: re.Match) -> str:
        nonlocal changed
        tag = m.group(1)
        body = m.group(2)
        if 'fill=' in body:
            return m.group(0)
        # Extract x, y (fallbacks to 0,0)
        xm = re.search(r'\bx="([\d.\-]+)"', body)
        ym = re.search(r'\by="([\d.\-]+)"', body)
        try:
            px = float(xm.group(1)) if xm else 0.0
            py = float(ym.group(1)) if ym else 0.0
        except ValueError:
            px, py = 0.0, 0.0
        fam = containing_family(px, py, rects)
        fill_val = f"var(--{fam}-text)" if fam else "var(--text)"
        new_body = body.rstrip() + f' fill="{fill_val}"'
        if not new_body.startswith(" "):
            new_body = " " + new_body
        changed += 1
        return f"<{tag}{new_body}>"

    return TEXT_RE.sub(fix, text), changed


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    files_changed = 0
    total = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file() or path.suffix != ".svg":
            continue
        s = path.read_text(encoding="utf-8")
        new, n = transform(s)
        if n:
            files_changed += 1
            total += n
            if not args.dry_run:
                path.write_text(new, encoding="utf-8")

    action = "would update" if args.dry_run else "updated"
    print(f"{action} {total} element(s) in {files_changed} file(s)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
