#!/usr/bin/env python

"""
Check SVG files for quality issues.

Checks:
  --size        Flag SVGs that are too small (likely placeholders)
  --elements    Flag SVGs with too few elements (likely stubs)
  --fonts       Flag SVGs with font-size below minimum
  --parse       Flag SVGs with XML parse errors
  --dimensions  Flag SVGs that do not have exactly viewBox="0 0 1280 720"
  --bounds      Flag SVGs with elements drawn below y=640
  --title       Flag SVGs that contain a <title> element
  --colors      Flag SVGs that use colors not in resources/palette.yaml

Usage:
    check_svg_quality.py file1.svg file2.svg ...
    check_svg_quality.py --fonts --size file1.svg file2.svg ...
    check_svg_quality.py --colors file1.svg file2.svg ...
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
import yaml
from pathlib import Path

MIN_FILE_SIZE = 500
MIN_ELEMENTS = 5
MIN_FONT_SIZE = 10
REQUIRED_VIEWBOX = "0 0 1280 720"
MAX_Y_BOUND = 640


def _check_size(path: Path) -> list[str]:
    """Flag SVGs that are too small (likely placeholders)."""
    size = path.stat().st_size
    if size < MIN_FILE_SIZE:
        return [f"too small ({size} bytes, min {MIN_FILE_SIZE})"]
    return []


def _check_parse(path: Path) -> tuple[ET.ElementTree | None, list[str]]:
    """Parse the SVG and return the tree and any errors."""
    try:
        tree = ET.parse(path)
        return tree, []
    except ET.ParseError as e:
        return None, [f"XML parse error: {e}"]


def _check_elements(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs with too few elements (likely stubs)."""
    count = sum(1 for _ in tree.iter())
    if count < MIN_ELEMENTS:
        return [f"too few elements ({count}, min {MIN_ELEMENTS})"]
    return []


def _check_fonts(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs with font-size below minimum."""
    for elem in tree.iter():
        fs = elem.get("font-size")
        if fs is not None:
            try:
                val = float(fs)
                if val < MIN_FONT_SIZE:
                    return [f"font-size {fs} too small (min {MIN_FONT_SIZE})"]
            except ValueError:
                pass
    return []


def _check_dimensions(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs that do not have exactly viewBox="0 0 1280 720"."""
    root = tree.getroot()
    viewbox = root.get("viewBox")
    if viewbox is None:
        return [f"missing viewBox (required: {REQUIRED_VIEWBOX!r})"]
    # Normalise whitespace for comparison
    normalised = " ".join(viewbox.split())
    if normalised != REQUIRED_VIEWBOX:
        return [f"viewBox is {viewbox!r}, must be {REQUIRED_VIEWBOX!r}"]
    return []


def _check_bounds(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs with elements drawn below the maximum Y boundary."""
    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]
        y_max = None
        
        try:
            if tag in ('rect', 'image', 'foreignObject'):
                y = float(elem.get('y', '0').replace('px', ''))
                h = float(elem.get('height', '0').replace('px', ''))
                y_max = y + h
            elif tag in ('text', 'use'):
                y = float(elem.get('y', '0').replace('px', ''))
                y_max = y
            elif tag in ('circle', 'ellipse'):
                cy = float(elem.get('cy', '0').replace('px', ''))
                if tag == 'circle':
                    r = float(elem.get('r', '0').replace('px', ''))
                else:
                    r = float(elem.get('ry', '0').replace('px', ''))
                y_max = cy + r
            elif tag == 'line':
                y1 = float(elem.get('y1', '0').replace('px', ''))
                y2 = float(elem.get('y2', '0').replace('px', ''))
                y_max = max(y1, y2)
        except ValueError:
            pass
            
        if y_max is not None and y_max > MAX_Y_BOUND:
            return [f"element <{tag}> extends below y={MAX_Y_BOUND} (found bottom y={y_max})"]
    return []

_PALETTE_NAMES: set[str] | None = None
_COLOR_ATTRS = {"fill", "stroke", "stop-color", "flood-color"}
_COLOR_RE = re.compile(r'#[0-9a-fA-F]{3,8}')
_VAR_RE = re.compile(r'^var\(--([a-zA-Z0-9_-]+)\)$')
# Values that are not colors — always allowed
_NON_COLOR_VALUES = {"none", "currentcolor", "inherit", "transparent"}
# Tags inside <defs> where raw hex is allowed (gradient stops, marker fills, filter colors)
_DEFS_TAGS = {"stop", "feDropShadow"}


def _load_palette_names() -> set[str]:
    """Load allowed semantic color names from resources/palette.yaml.

    Returns a set of names like {"bg", "primary", "danger-lt", ...}.
    """
    global _PALETTE_NAMES
    if _PALETTE_NAMES is not None:
        return _PALETTE_NAMES

    palette_path = Path("resources/palette.yaml")
    if not palette_path.exists():
        _PALETTE_NAMES = set()
        return _PALETTE_NAMES

    with open(palette_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    names: set[str] = set()
    for group in data.get("colors", {}).values():
        for name in group:
            names.add(name)

    _PALETTE_NAMES = names
    return _PALETTE_NAMES


def _check_colors(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs that use colors not expressed as var(--name) from the palette.

    Color attributes must use var(--semantic-name) where name is defined in
    resources/palette.yaml. Raw hex values and named CSS colors are rejected.

    Exception: elements inside <defs> (gradient stops, marker paths, filter
    params) may use raw hex since CSS var() doesn't work reliably there.
    """
    palette_names = _load_palette_names()
    if not palette_names:
        return ["cannot check colors: resources/palette.yaml not found or empty"]

    errors: list[str] = []
    seen_bad: set[str] = set()

    # Track whether we're inside a <defs> block
    in_defs = False

    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]

        if tag == 'defs':
            in_defs = True
            continue

        for attr in _COLOR_ATTRS:
            val = elem.get(attr, "")
            if not val:
                continue

            stripped = val.strip().lower()

            # Skip non-color values and url() references
            if stripped in _NON_COLOR_VALUES or stripped.startswith("url("):
                continue

            # Inside defs, raw hex is allowed (for gradient stops, marker fills, etc.)
            if in_defs:
                continue

            # Check for var(--name)
            var_m = _VAR_RE.match(stripped)
            if var_m:
                name = var_m.group(1)
                if name not in palette_names and name not in seen_bad:
                    seen_bad.add(name)
                    errors.append(
                        f"var(--{name}) (in <{tag}> {attr}=)"
                        f" — name not in palette"
                    )
                continue

            # Anything else is not allowed
            key = f"{attr}:{stripped}"
            if key not in seen_bad:
                seen_bad.add(key)
                errors.append(
                    f"raw color {val!r} (in <{tag}> {attr}=)"
                    f" — use var(--name) from the palette"
                )

    return errors


def _check_title(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs that contain a <title> element."""
    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]
        if tag == 'title':
            return ["contains a <title> element (headings should be outside SVG)"]
    return []

def main() -> None:
    if not Path(".git").exists():
        print("Error: script must be run from the root of the repository", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Check SVG files for quality issues.'
    )
    parser.add_argument('paths', nargs='*',
                        help='SVG files to check')
    parser.add_argument('--size', action='store_true',
                        help='Flag SVGs that are too small (likely placeholders)')
    parser.add_argument('--elements', action='store_true',
                        help='Flag SVGs with too few elements (likely stubs)')
    parser.add_argument('--fonts', action='store_true',
                        help='Flag SVGs with font-size below minimum')
    parser.add_argument('--parse', action='store_true',
                        help='Flag SVGs with XML parse errors')
    parser.add_argument('--dimensions', action='store_true',
                        help='Flag SVGs that do not have exactly viewBox="0 0 1280 720"')
    parser.add_argument('--bounds', action='store_true',
                        help='Flag SVGs with elements drawn below y=640')
    parser.add_argument('--title', action='store_true',
                        help='Flag SVGs that contain a <title> element')
    parser.add_argument('--colors', action='store_true',
                        help='Flag SVGs that use colors not in resources/palette.yaml (default: on)')
    args = parser.parse_args()

    if not args.paths:
        parser.error("at least one SVG file is required")

    # Default: all checks enabled when no flags are specified
    flags = [args.size, args.elements, args.fonts, args.parse, args.dimensions, args.bounds, args.title, args.colors]
    explicit = any(flags)
    do_size = args.size or not explicit
    do_elements = args.elements or not explicit
    do_fonts = args.fonts or not explicit
    do_parse = args.parse or not explicit
    do_dimensions = args.dimensions or not explicit
    do_bounds = args.bounds or not explicit
    do_title = args.title or not explicit
    do_colors = args.colors or not explicit

    failures = 0
    for path_str in args.paths:
        path = Path(path_str)
        errors: list[str] = []

        if do_size:
            errors.extend(_check_size(path))

        # Parse once, reuse for element, font, and aspect checks
        tree = None
        if do_parse or do_elements or do_fonts or do_dimensions or do_bounds or do_title or do_colors:
            tree, parse_errors = _check_parse(path)
            if do_parse:
                errors.extend(parse_errors)

        if tree is not None:
            if do_elements:
                errors.extend(_check_elements(tree))
            if do_fonts:
                errors.extend(_check_fonts(tree))
            if do_dimensions:
                errors.extend(_check_dimensions(tree))
            if do_bounds:
                errors.extend(_check_bounds(tree))
            if do_title:
                errors.extend(_check_title(tree))
            if do_colors:
                errors.extend(_check_colors(tree))

        for error in errors:
            print(f"{path}: {error}", file=sys.stderr)
            failures += 1

    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
