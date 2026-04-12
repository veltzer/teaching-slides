#!/usr/bin/env python
"""
Migrate SVGs from appearance-named palette variables (primary-vivid,
ok-pale2, warn-yellow, etc.) to semantic role names (primary-fill,
primary-border, primary-text, primary-accent, etc.).

The mapping is context-aware: the same old variable name maps to different
new roles depending on whether it's used on a fill=, stroke=, or inside a
<text> element. For example:
  <rect fill="var(--primary-dk)"/>      -> var(--primary-accent)
  <line stroke="var(--primary-dk)"/>    -> var(--primary-border)

Safe to re-run (idempotent).

The script:
  1. Walks every SVG under svg/.
  2. For each <rect|circle|ellipse|polygon|polyline|path|line|text|tspan>
     element that has fill="var(--OLD)" or stroke="var(--OLD)", looks up
     the new role based on (element-tag, attr, old-name).
  3. Replaces the <defs>-embedded <style> block using install_palette.py
     rules (that's a separate step; this script only rewrites the drawing
     elements).

After running this, run `scripts/install_palette.py --apply` to push the
new palette <defs> into every SVG, then `rsconstruct build --verbose` to
verify.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Map (context, old_name) -> new_role.
# Context is one of: "fill", "stroke", "text" (element is <text>/<tspan>)
#
# Families: primary, ok, warn, danger, info.
# Each old variant maps to one of:
#   {family}-fill     - the box background fill
#   {family}-border   - matching border / stroke
#   {family}-text     - text drawn on top of the fill
#   {family}-accent   - deeper shade for emphasis

FAMILIES = ("primary", "ok", "warn", "danger", "info")

# Appearance-named variants that describe a SATURATED / MAIN hue.
# When used as fill -> {family}-fill (solid saturated box).
# When used as stroke -> {family}-border.
# When used as text color -> {family}-accent (readable against bg).
SATURATED_SUFFIXES = (
    "",          # bare family name (--primary, --ok, ...)
    "-vivid",
    "-bright",
    "-soft",
    "-mid",
    "-light",
    "-google",
    "-indigo",
    "-orange",
    "-yellow",
    "-amber",
    "-gold",
    "-pink",
)

# Appearance-named variants that describe a PALE / TINT hue.
# When used as fill -> {family}-fill (same destination — we're
#   canonicalizing on vivid, so pale fills become vivid fills).
# When used as stroke -> {family}-border.
# When used as text -> {family}-accent.
PALE_SUFFIXES = (
    "-lt",
    "-tint",
    "-pale",
    "-pale2",
    "-pale3",
    "-pale4",
    "-pale5",
)

# Appearance-named variants that describe a DARK / DEEP hue.
# When used as fill -> {family}-accent (use deep shade for filled emphasis panels).
# When used as stroke -> {family}-border.
# When used as text -> {family}-accent.
DARK_SUFFIXES = (
    "-dk",
    "-deep",
    "-deeper",
    "-strong",
    "-indigo-dk",
)

# Neutrals
NEUTRAL_MAP = {
    # old -> new
    "surface-alt": "surface",
    "surface-light": "surface",
    "surface-dark": "surface",
    "border-strong": "border",
    "border-faint": "border",
    "border-softer": "border",
    "text-dark": "text",
    "text-darker": "text",
    "text-mid": "text-muted",
    "text-lighter": "text-muted",
    "text-faintest": "text-faint",
    "text-disabled": "text-faint",
    "text-placeholder": "text-faint",
    "info-indigo-lt": "info-fill",  # indigo light for intro slides, fold into info-fill
}


def build_context_map() -> dict[tuple[str, str], str]:
    """Return {(context, old_var) -> new_var}."""
    m: dict[tuple[str, str], str] = {}

    for family in FAMILIES:
        # saturated variants: fill/stroke/text -> fill/border/accent
        for suffix in SATURATED_SUFFIXES:
            old = f"{family}{suffix}"
            m[("fill",   old)] = f"{family}-fill"
            m[("stroke", old)] = f"{family}-border"
            m[("text",   old)] = f"{family}-accent"
        # pale variants: fill -> fill (canonicalizing vivid), stroke -> border, text -> accent
        for suffix in PALE_SUFFIXES:
            old = f"{family}{suffix}"
            m[("fill",   old)] = f"{family}-fill"
            m[("stroke", old)] = f"{family}-border"
            m[("text",   old)] = f"{family}-accent"
        # dark variants: fill -> accent, stroke -> border, text -> accent
        for suffix in DARK_SUFFIXES:
            old = f"{family}{suffix}"
            m[("fill",   old)] = f"{family}-accent"
            m[("stroke", old)] = f"{family}-border"
            m[("text",   old)] = f"{family}-accent"

    # Neutrals: remap old names to survivors (context doesn't change them)
    for old, new in NEUTRAL_MAP.items():
        m[("fill",   old)] = new
        m[("stroke", old)] = new
        m[("text",   old)] = new

    return m


CONTEXT_MAP = build_context_map()

# Tags treated as text for var mapping purposes
TEXT_TAGS = {"text", "tspan"}

# Tags treated as drawing shapes (non-text) where fill=solid bg and stroke=border
SHAPE_TAGS = {"rect", "circle", "ellipse", "polygon", "polyline", "path", "line", "g"}

# Element open-tag regex: capture tag name and full attribute string
ELEM_RE = re.compile(r'<(?P<tag>[a-zA-Z][a-zA-Z0-9]*)\b(?P<attrs>[^>]*?)(?P<close>/?)>')

# Attribute regex inside an element
ATTR_RE = re.compile(r'\b(?P<name>fill|stroke)="var\(--(?P<var>[\w-]+)\)"')


def migrate_text(text: str) -> tuple[str, int]:
    """Replace var(--old) with var(--new) in every element outside <defs>.
    Returns (new_text, num_replacements).
    """
    # Split on <defs>...</defs> so we only transform outside parts.
    parts = re.split(r'(<defs\b.*?</defs>)', text, flags=re.DOTALL)
    total = 0
    for i in range(0, len(parts), 2):  # even indices = outside defs
        chunk = parts[i]
        new_chunk, n = _migrate_chunk(chunk)
        parts[i] = new_chunk
        total += n
    return "".join(parts), total


def _migrate_chunk(chunk: str) -> tuple[str, int]:
    count = 0

    def sub_element(m: re.Match) -> str:
        nonlocal count
        tag = m.group("tag")
        attrs = m.group("attrs")
        close = m.group("close")
        is_text = tag in TEXT_TAGS

        def sub_attr(am: re.Match) -> str:
            nonlocal count
            attr = am.group("name")   # "fill" or "stroke"
            old = am.group("var")
            if is_text:
                context = "text"
            else:
                context = attr  # "fill" or "stroke"
            new = CONTEXT_MAP.get((context, old))
            if new is None:
                # Already-semantic name or unmapped; leave alone.
                return am.group(0)
            if new == old:
                return am.group(0)
            count += 1
            return f'{attr}="var(--{new})"'

        new_attrs = ATTR_RE.sub(sub_attr, attrs)
        return f"<{tag}{new_attrs}{close}>"

    new_chunk = ELEM_RE.sub(sub_element, chunk)
    return new_chunk, count


def fix_svg(path: Path) -> int:
    before = path.read_text(encoding="utf-8")
    after, n = migrate_text(before)
    if after != before:
        path.write_text(after, encoding="utf-8")
    return n


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    svg_root = repo_root / "svg"
    total_changes = 0
    files_changed = 0
    scanned = 0
    for svg_path in sorted(svg_root.rglob("*.svg")):
        scanned += 1
        n = fix_svg(svg_path)
        if n > 0:
            files_changed += 1
            total_changes += n
    print(f"{files_changed} files changed, {total_changes} var() replacements across {scanned} SVGs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
