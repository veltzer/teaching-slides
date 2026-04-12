#!/usr/bin/env python
"""
Normalize visual primitives across every SVG:

  - rects get rx="6" (canonical corner radius)
  - rects with family fills (var(--primary-fill) etc.) get matching
    family borders and stroke-width="2"
  - rects with neutral fills (--surface, --bg, none) get --border stroke
    and stroke-width="1"
  - gradient fills (url(#grad-primary) etc.) are flattened to var(--*-fill)
  - lines get stroke-width="2" (cap, no larger)

Outside-<defs> only; palette <defs> block is left untouched.

Idempotent. Safe to re-run. Uses regex — no XML parsing, no ns0 risk.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

FAMILIES = ("primary", "ok", "warn", "danger", "info")

GRAD_TO_FILL = {
    "grad-primary": "primary-fill",
    "grad-ok":      "ok-fill",
    "grad-warn":    "warn-fill",
    "grad-danger":  "danger-fill",
    "grad-info":    "info-fill",
    "grad-surface": None,
}

FILL_TO_BORDER = {f"{fam}-fill": f"{fam}-border" for fam in FAMILIES}

_VAR_RE = re.compile(r'var\(--([\w-]+)\)')
_URL_REF_RE = re.compile(r'url\(#([\w-]+)\)')
_RECT_RE = re.compile(r'<rect\b([^>]*?)(/?)>', re.DOTALL)
_LINE_RE = re.compile(r'<line\b([^>]*?)(/?)>', re.DOTALL)


def _extract_var(val: str) -> str | None:
    m = _VAR_RE.fullmatch(val.strip())
    return m.group(1) if m else None


def _extract_url(val: str) -> str | None:
    m = _URL_REF_RE.fullmatch(val.strip())
    return m.group(1) if m else None


def _get_attr(attrs: str, name: str) -> str | None:
    m = re.search(rf'\b{re.escape(name)}="([^"]*)"', attrs)
    return m.group(1) if m else None


def _set_attr(attrs: str, name: str, value: str) -> str:
    pattern = rf'\b{re.escape(name)}="[^"]*"'
    if re.search(pattern, attrs):
        return re.sub(pattern, f'{name}="{value}"', attrs)
    sep = "" if attrs.endswith(" ") or attrs == "" else " "
    return attrs + sep + f'{name}="{value}"'


def _del_attr(attrs: str, name: str) -> str:
    pattern = rf'\s*\b{re.escape(name)}="[^"]*"'
    return re.sub(pattern, "", attrs)


def _normalize_fill_value(fill: str | None) -> str | None:
    if fill is None:
        return None
    ref = _extract_url(fill)
    if ref is not None and ref in GRAD_TO_FILL:
        target = GRAD_TO_FILL[ref]
        if target is None:
            return "var(--surface)"
        return f"var(--{target})"
    return fill


def _rewrite_rect(attrs: str) -> str:
    fill = _get_attr(attrs, "fill")
    new_fill = _normalize_fill_value(fill)
    if new_fill != fill and new_fill is not None:
        attrs = _set_attr(attrs, "fill", new_fill)
        fill = new_fill

    fill_var = _extract_var(fill) if fill else None
    is_family_fill = fill_var in FILL_TO_BORDER
    is_surface = fill_var == "surface" or fill == "none" or fill is None

    attrs = _set_attr(attrs, "rx", "6")
    attrs = _del_attr(attrs, "ry")

    if is_family_fill:
        border = FILL_TO_BORDER[fill_var]
        attrs = _set_attr(attrs, "stroke", f"var(--{border})")
        attrs = _set_attr(attrs, "stroke-width", "2")
    elif is_surface:
        existing_stroke = _get_attr(attrs, "stroke")
        if existing_stroke is not None:
            attrs = _set_attr(attrs, "stroke", "var(--border)")
            attrs = _set_attr(attrs, "stroke-width", "1")

    return attrs


def _rewrite_line(attrs: str) -> str:
    stroke = _get_attr(attrs, "stroke")
    new_stroke = _normalize_fill_value(stroke)
    if new_stroke != stroke and new_stroke is not None:
        attrs = _set_attr(attrs, "stroke", new_stroke)

    sw = _get_attr(attrs, "stroke-width")
    if sw is not None:
        try:
            val = float(sw)
            if val > 2:
                attrs = _set_attr(attrs, "stroke-width", "2")
        except ValueError:
            pass
    return attrs


def _split_defs(content: str) -> list[str]:
    return re.split(r'(<defs\b.*?</defs>)', content, flags=re.DOTALL)


def normalize_content(content: str) -> str:
    parts = _split_defs(content)
    for i in range(0, len(parts), 2):
        chunk = parts[i]
        chunk = _RECT_RE.sub(
            lambda m: f'<rect{_rewrite_rect(m.group(1))}{m.group(2)}>',
            chunk,
        )
        chunk = _LINE_RE.sub(
            lambda m: f'<line{_rewrite_line(m.group(1))}{m.group(2)}>',
            chunk,
        )
        parts[i] = chunk
    return "".join(parts)


def fix_svg(path: Path) -> bool:
    before = path.read_text(encoding="utf-8")
    after = normalize_content(before)
    if after == before:
        return False
    path.write_text(after, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    svg_root = repo_root / "svg"
    changed = 0
    scanned = 0
    for p in sorted(svg_root.rglob("*.svg")):
        scanned += 1
        if fix_svg(p):
            changed += 1
    print(f"{changed} files changed out of {scanned} scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
