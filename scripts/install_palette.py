#!/usr/bin/env python

"""
Install the canonical palette into every SVG under svg/.

Each SVG is stamped with a <!-- palette: path/to/palette.yaml --> comment
so that check_svg.py knows which palette to validate against.

For each SVG:
  1. Stamps a <!-- palette: ... --> comment (or updates an existing one)
  2. Injects a <style> block with CSS custom properties (--bg, --primary, etc.)
  3. Injects gradient, filter, and marker <defs> entries
  4. Converts raw hex color values in attributes to var(--name) references
  5. Converts named CSS colors (white, black, red, etc.) to var(--name)
  6. Renames old gradient/marker IDs to canonical ones

The <style> block and defs entries are placed inside a <defs> block
at the top of the SVG. Custom SVG-specific defs are preserved.

Usage:
    scripts/install_palette.py                                    # dry-run, diagram palette
    scripts/install_palette.py --apply                            # apply diagram palette to all
    scripts/install_palette.py --palette resources/palette_intro.yaml --apply svg/courses/**/title.svg
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

DEFAULT_PALETTE = Path("resources/palette_diagram.yaml")
SVG_ROOT = Path("svg")

# Regex to find/replace the palette comment stamped into SVGs
_PALETTE_COMMENT_RE = re.compile(r'<!--\s*palette:\s*(\S+)\s*-->')

# Canonical IDs that the palette owns
PALETTE_IDS: set[str] = {
    "grad-primary", "grad-surface", "grad-ok", "grad-warn", "grad-danger", "grad-info",
    "shadow",
    "arrow", "arrow-primary", "arrow-ok", "arrow-warn", "arrow-danger", "arrow-info", "arrow-white",
    "palette-vars",
}

# Old ID -> canonical ID renames (longer/more-specific first).
ID_RENAMES: list[tuple[str, str]] = [
    ("arrowhead-green",  "arrow-ok"),
    ("arrowhead-gray",   "arrow"),
    ("arrowhead-grey",   "arrow"),
    ("arrowhead-red",    "arrow-danger"),
    ("arrowhead-dash",   "arrow"),
    ("arrowhead",        "arrow"),
    ("arrowgreen",       "arrow-ok"),
    ("arrowred",         "arrow-danger"),
    ("arrowdash",        "arrow"),
    ("arrow-accent",     "arrow-primary"),
    ("arrow-blue",       "arrow-primary"),
    ("arrow-green",      "arrow-ok"),
    ("arrow-red",        "arrow-danger"),
    ("arrow-orange",     "arrow-warn"),
    ("arrow1",           "arrow"),
    ("arrow2",           "arrow"),
    ("arrow3",           "arrow"),
    ("arrow4",           "arrow"),
    ("arrow5",           "arrow"),
    ("grad-accent",      "grad-primary"),
    ("grad-green",       "grad-ok"),
    ("grad-orange",      "grad-warn"),
    ("grad-red",         "grad-danger"),
    ("grad-purple",      "grad-info"),
]

# Color attributes to convert from hex to var()
_COLOR_ATTRS = {"fill", "stroke", "stop-color", "flood-color"}

# Named CSS colors -> palette semantic name (direct mapping)
_CSS_TO_PALETTE_NAME: dict[str, str] = {
    "white": "bg",
    "black": "black",
    "red": "danger",
    "green": "ok",
    "blue": "primary",
    "yellow": "warn-yellow",
    "orange": "warn-orange",
    "gray": "text-faint",
    "grey": "text-faint",
    "lightblue": "primary-lt",
    "lightgreen": "ok-lt",
    "lightcoral": "danger-lt",
    "lightyellow": "warn-pale",
    "lightpink": "danger-pale3",
}

# Regex patterns
_DEFS_OPEN_RE  = re.compile(r'<(?:[a-zA-Z0-9_]+:)?defs(?:\s[^>]*)?>')
_DEFS_CLOSE_RE = re.compile(r'</(?:[a-zA-Z0-9_]+:)?defs>')
_SVG_OPEN_RE = re.compile(r'(<(?:[a-zA-Z0-9_]+:)?svg\b[^>]*>)')
_ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')
_COLOR_RE = re.compile(r'#[0-9a-fA-F]{3,8}')
_STYLE_BLOCK_RE = re.compile(
    r'<style\b[^>]*id="palette-vars"[^>]*>.*?</style>',
    re.DOTALL,
)


def _load_palette(path: Path) -> dict:
    """Load and return the palette data from YAML."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_hex_to_name(data: dict) -> dict[str, str]:
    """Build a mapping from normalized hex -> semantic name."""
    mapping: dict[str, str] = {}
    for group in data["colors"].values():
        for name, hexval in group.items():
            h = hexval.strip().lower()
            # Normalize 3-digit to 6-digit
            digits = h.lstrip('#')
            if len(digits) == 3:
                digits = ''.join(ch * 2 for ch in digits)
                h = '#' + digits
            if h not in mapping:
                mapping[h] = name
    return mapping


def _generate_style_block(data: dict) -> str:
    """Generate a <style> block with CSS custom properties."""
    lines = ['    <style id="palette-vars">']
    lines.append('      :root, svg {')
    for group_name, group in data["colors"].items():
        for name, hexval in group.items():
            lines.append(f'        --{name}: {hexval};')
    lines.append('      }')
    lines.append('    </style>')
    return '\n'.join(lines)


def _generate_defs_content(data: dict) -> str:
    """Generate the gradient, filter, and marker defs from YAML."""
    lines = []

    # Gradients
    lines.append('    <!-- Gradients -->')
    for gid, gdata in data.get("gradients", {}).items():
        lines.append(f'    <linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">')
        for stop in gdata["stops"]:
            lines.append(f'      <stop offset="{stop["offset"]}" stop-color="{stop["color"]}"/>')
        lines.append('    </linearGradient>')
        lines.append('')

    # Filters
    lines.append('    <!-- Drop shadow -->')
    for fid, fdata in data.get("filters", {}).items():
        lines.append(
            f'    <filter id="{fid}" x="-4%" y="-8%" width="108%" height="124%">'
        )
        lines.append(
            f'      <feDropShadow dx="{fdata["dx"]}" dy="{fdata["dy"]}"'
            f' stdDeviation="{fdata["stdDeviation"]}"'
            f' flood-color="{fdata["flood-color"]}"/>'
        )
        lines.append('    </filter>')
        lines.append('')

    # Markers
    lines.append('    <!-- Arrow markers -->')
    for mid, mdata in data.get("markers", {}).items():
        lines.append(
            f'    <marker id="{mid}" markerWidth="10" markerHeight="10"'
            f' refX="9" refY="5" orient="auto">'
        )
        lines.append(f'      <path d="M1,2 L9,5 L1,8 Z" fill="{mdata["fill"]}"/>')
        lines.append('    </marker>')

    return '\n'.join(lines)


def _apply_renames(text: str) -> str:
    """Replace old gradient/marker IDs with canonical ones throughout text."""
    for old, new in ID_RENAMES:
        text = re.sub(
            rf'(?<!["\w-]){re.escape(old)}(?!["\w-])',
            new,
            text,
        )
    return text


def _convert_colors_to_vars(text: str, hex_to_name: dict[str, str]) -> str:
    """Convert raw hex colors and named CSS colors in color attributes to var(--name).

    Only converts colors in fill/stroke/stop-color/flood-color attributes.
    Does NOT convert colors inside <defs> blocks (gradients, markers, filters
    need raw hex for their stop-color/fill values).
    """
    # Find defs region to exclude it from conversion
    defs_open = _DEFS_OPEN_RE.search(text)
    defs_close = _DEFS_CLOSE_RE.search(text)
    defs_start = defs_open.start() if defs_open else -1
    defs_end = defs_close.end() if defs_close else -1

    def _in_defs(pos: int) -> bool:
        return defs_start <= pos <= defs_end if defs_start >= 0 else False

    # Build regex for color attributes
    # Matches: fill="..." stroke="..." stop-color="..." flood-color="..."
    attr_re = re.compile(
        r'(?P<attr>(?:fill|stroke|stop-color|flood-color))\s*=\s*"(?P<val>[^"]*)"'
    )

    def _replace_attr(m: re.Match) -> str:
        if _in_defs(m.start()):
            return m.group()

        attr_name = m.group('attr')
        val = m.group('val').strip()
        val_lower = val.lower()

        # Skip non-color values and url() references and var() references
        if val_lower in ('none', 'currentcolor', 'inherit', 'transparent'):
            return m.group()
        if val_lower.startswith('url(') or val_lower.startswith('var('):
            return m.group()

        # Handle named CSS colors
        if val_lower in _CSS_TO_PALETTE_NAME:
            return f'{attr_name}="var(--{_CSS_TO_PALETTE_NAME[val_lower]})"'

        # Handle hex colors
        new_val = val
        for hex_m in reversed(list(_COLOR_RE.finditer(val))):
            raw = hex_m.group().lower()
            h = raw.lstrip('#')
            if len(h) == 3:
                h = ''.join(ch * 2 for ch in h)
            if len(h) == 6:
                normalized = '#' + h
                if normalized in hex_to_name:
                    start, end = hex_m.span()
                    new_val = new_val[:start] + f'var(--{hex_to_name[normalized]})' + new_val[end:]
            elif len(h) == 8:
                # Alpha hex: convert base color, keep alpha
                base = '#' + h[:6]
                if base in hex_to_name:
                    start, end = hex_m.span()
                    # Can't easily use var() with alpha, leave as-is
                    pass

        return f'{attr_name}="{new_val}"'

    return attr_re.sub(_replace_attr, text)


# Comments injected by the palette that should be stripped on re-install
_PALETTE_COMMENTS = {
    '<!-- Gradients -->',
    '<!-- Drop shadow -->',
    '<!-- Arrow markers -->',
}


def _strip_palette_elements(inner_text: str) -> str:
    """Remove palette-managed elements from a defs block."""
    lines = inner_text.split('\n')
    result = []
    skip_until_close: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if skip_until_close:
            if skip_until_close in line:
                skip_until_close = None
            i += 1
            continue
        id_m = _ID_ATTR_RE.search(line)
        if id_m and id_m.group(1) in PALETTE_IDS:
            if '/>' in line:
                i += 1
                continue
            tag_m = re.match(r'\s*<([A-Za-z0-9_:]+)', line)
            if tag_m:
                skip_until_close = f'</{tag_m.group(1)}>'
            i += 1
            continue
        # Strip <style id="palette-vars"> blocks
        if 'id="palette-vars"' in line:
            if '</style>' in line:
                i += 1
                continue
            skip_until_close = '</style>'
            i += 1
            continue
        # Strip palette-injected comments
        stripped = line.strip()
        if stripped in _PALETTE_COMMENTS:
            i += 1
            continue
        result.append(line)
        i += 1
    # Collapse runs of blank lines into at most one
    collapsed = []
    prev_blank = False
    for line in result:
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            continue
        collapsed.append(line)
        prev_blank = is_blank
    return '\n'.join(collapsed)


def _merge_defs(svg_text: str, palette_block: str) -> str:
    """Merge palette defs (style + gradients + markers) into the SVG."""
    open_m = _DEFS_OPEN_RE.search(svg_text)
    close_m = _DEFS_CLOSE_RE.search(svg_text)

    if open_m and close_m and open_m.start() < close_m.start():
        defs_start = open_m.start()
        defs_end   = close_m.end()
        open_tag   = open_m.group()
        close_tag  = close_m.group()

        cleaned_inner = _strip_palette_elements(
            svg_text[open_m.end():close_m.start()]
        )

        new_defs = open_tag + '\n' + palette_block + '\n' + cleaned_inner + close_tag
        svg_text = svg_text[:defs_start] + new_defs + svg_text[defs_end:]
    else:
        new_defs_block = '\n  <defs>\n' + palette_block + '\n  </defs>'
        svg_text = _SVG_OPEN_RE.sub(r'\1' + new_defs_block, svg_text, count=1)

    return svg_text


def _stamp_palette_comment(text: str, palette_path: Path) -> str:
    """Insert or update the <!-- palette: path --> comment after the <svg> tag."""
    comment = f'<!-- palette: {palette_path} -->'
    existing = _PALETTE_COMMENT_RE.search(text)
    if existing:
        return text[:existing.start()] + comment + text[existing.end():]
    # Insert right after the opening <svg ...> tag
    svg_m = _SVG_OPEN_RE.search(text)
    if svg_m:
        return text[:svg_m.end()] + '\n  ' + comment + text[svg_m.end():]
    return text


def process_file(
    path: Path,
    palette_path: Path,
    palette_block: str,
    hex_to_name: dict[str, str],
    apply: bool,
) -> bool:
    """Process one SVG. Returns True if the file would/did change."""
    original = path.read_text(encoding="utf-8")

    # Step 1: stamp palette comment
    updated = _stamp_palette_comment(original, palette_path)

    # Step 2: rename old IDs
    updated = _apply_renames(updated)

    # Step 3: convert hex colors to var() references
    updated = _convert_colors_to_vars(updated, hex_to_name)

    # Step 4: merge palette defs (style block + gradients + markers)
    updated = _merge_defs(updated, palette_block)

    if updated == original:
        return False

    if apply:
        path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    if not Path(".git").exists():
        print("Error: run from the repository root", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*",
                        help="SVG files to process (default: all under svg/)")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes to disk (default is dry-run)")
    parser.add_argument("--palette", type=Path, default=DEFAULT_PALETTE,
                        help=f"Palette YAML to install (default: {DEFAULT_PALETTE})")
    args = parser.parse_args()

    palette_path = args.palette
    if not palette_path.exists():
        print(f"Error: {palette_path} not found", file=sys.stderr)
        sys.exit(1)

    data = _load_palette(palette_path)
    hex_to_name = _build_hex_to_name(data)
    style_block = _generate_style_block(data)
    defs_content = _generate_defs_content(data)
    palette_block = style_block + '\n' + defs_content

    svg_files = [Path(p) for p in args.paths] if args.paths \
        else sorted(SVG_ROOT.rglob("*.svg"))

    changed: list[Path] = []
    errors: list[tuple[Path, Exception]] = []

    for path in svg_files:
        try:
            if process_file(path, palette_path, palette_block, hex_to_name, args.apply):
                changed.append(path)
        except Exception as exc:
            errors.append((path, exc))

    action = "Updated" if args.apply else "Would update"
    for p in changed:
        print(f"{action}: {p}")
    for p, exc in errors:
        print(f"ERROR: {p}: {exc}", file=sys.stderr)

    print(f"\n{action} {len(changed)} file(s). {len(errors)} error(s).")
    if not args.apply and changed:
        print("Re-run with --apply to write changes.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
