#!/usr/bin/env python
"""
Cap the size of custom arrow markers in SVGs.

Many SVGs define per-file arrow markers (id="arrowhead", id="arrowd0_...",
id="ah12b", etc.) with markerWidth/markerHeight values ranging from 11 up to
~36. These render as oversized triangles that overpower the boxes and lines
they attach to.

This script rewrites any marker whose markerWidth > 10 or markerHeight > 10
to the palette standard (10x10, refX=9, refY=5). The marker id, fill, and
shape are preserved so existing marker-end="url(#...)" references still
resolve to the same marker, just smaller.

Rules:
  - Skip markers whose id is in the palette standard set (arrow, arrow-primary,
    arrow-ok, arrow-warn, arrow-danger, arrow-info, arrow-white). These are
    already 10x10.
  - Skip markers with both dimensions <= 10.
  - For markers with a polygon/path child, leave the shape untouched (just
    resize the marker viewport). The shape's coordinates are often in a
    local space compatible with 10x10 once the viewport shrinks.

Idempotent: running twice has no further effect.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PALETTE_MARKER_IDS = {
    "arrow",
    "arrow-primary",
    "arrow-ok",
    "arrow-warn",
    "arrow-danger",
    "arrow-info",
    "arrow-white",
}

# Match a full <marker ...> opening tag (self-closing or with content).
MARKER_OPEN_RE = re.compile(r'<marker\b([^>]*?)>', re.DOTALL)


def _get_attr(attrs: str, name: str) -> str | None:
    m = re.search(rf'\b{name}="([^"]*)"', attrs)
    return m.group(1) if m else None


def _set_attr(attrs: str, name: str, value: str) -> str:
    if re.search(rf'\b{name}="[^"]*"', attrs):
        return re.sub(rf'\b{name}="[^"]*"', f'{name}="{value}"', attrs)
    return attrs.rstrip() + f' {name}="{value}"'


def rewrite_marker_tag(match: re.Match) -> str:
    attrs = match.group(1)
    marker_id = _get_attr(attrs, "id")
    if marker_id in PALETTE_MARKER_IDS:
        return match.group(0)

    width = _get_attr(attrs, "markerWidth")
    height = _get_attr(attrs, "markerHeight")
    if width is None or height is None:
        return match.group(0)
    try:
        w = float(width)
        h = float(height)
    except ValueError:
        return match.group(0)
    if w <= 10 and h <= 10:
        return match.group(0)

    new_attrs = attrs
    new_attrs = _set_attr(new_attrs, "markerWidth", "10")
    new_attrs = _set_attr(new_attrs, "markerHeight", "10")
    new_attrs = _set_attr(new_attrs, "refX", "9")
    new_attrs = _set_attr(new_attrs, "refY", "5")
    return f"<marker{new_attrs}>"


def fix_svg(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    new_content = MARKER_OPEN_RE.sub(rewrite_marker_tag, content)
    if new_content == content:
        return False
    path.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    svg_root = repo_root / "svg"
    fixed = 0
    scanned = 0
    for svg_path in sorted(svg_root.rglob("*.svg")):
        scanned += 1
        if fix_svg(svg_path):
            fixed += 1
            print(f"fixed: {svg_path.relative_to(repo_root)}")
    print(f"\n{fixed} files fixed out of {scanned} scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
