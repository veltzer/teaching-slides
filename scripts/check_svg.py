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

Usage:
    check_svg_quality.py file1.svg file2.svg ...
    check_svg_quality.py --fonts --size file1.svg file2.svg ...
"""

import argparse
import sys
import xml.etree.ElementTree as ET
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
    args = parser.parse_args()

    if not args.paths:
        parser.error("at least one SVG file is required")

    # Default: all checks enabled
    flags = [args.size, args.elements, args.fonts, args.parse, args.dimensions, args.bounds, args.title]
    explicit = any(flags)
    do_size = args.size or not explicit
    do_elements = args.elements or not explicit
    do_fonts = args.fonts or not explicit
    do_parse = args.parse or not explicit
    do_dimensions = args.dimensions or not explicit
    do_bounds = args.bounds or not explicit
    do_title = args.title or not explicit

    failures = 0
    for path_str in args.paths:
        path = Path(path_str)
        errors: list[str] = []

        if do_size:
            errors.extend(_check_size(path))

        # Parse once, reuse for element, font, and aspect checks
        tree = None
        if do_parse or do_elements or do_fonts or do_dimensions or do_bounds or do_title:
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

        for error in errors:
            print(f"{path}: {error}", file=sys.stderr)
            failures += 1

    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
