#!/usr/bin/env python

"""
Check SVG files for placeholder or trivially small content.

Flags SVGs that are likely decorative icons or placeholders rather than
real diagrams. Checks file size and element count.

Usage:
    check_svg_quality.py file1.svg file2.svg ...
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MIN_FILE_SIZE = 500
MIN_ELEMENTS = 5
MIN_FONT_SIZE = 10


def check_file(path: Path) -> list[str]:
    """Return a list of error messages for the SVG, empty if OK."""
    errors: list[str] = []
    size = path.stat().st_size
    if size < MIN_FILE_SIZE:
        errors.append(f"too small ({size} bytes, min {MIN_FILE_SIZE})")
        return errors

    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        errors.append(f"XML parse error: {e}")
        return errors

    count = sum(1 for _ in tree.iter())
    if count < MIN_ELEMENTS:
        errors.append(f"too few elements ({count}, min {MIN_ELEMENTS})")

    # Check for small font sizes in attributes
    for elem in tree.iter():
        fs = elem.get("font-size")
        if fs is not None:
            try:
                val = float(fs)
                if val < MIN_FONT_SIZE:
                    errors.append(f"font-size {fs} too small (min {MIN_FONT_SIZE})")
                    break  # one error per file is enough
            except ValueError:
                pass

    return errors


def main() -> None:
    if not Path(".git").exists():
        print("Error: script must be run from the root of the repository", file=sys.stderr)
        sys.exit(1)
    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: check_svg_quality.py file1.svg [file2.svg ...]")

    failures = 0
    for path_str in args:
        path = Path(path_str)
        errors = check_file(path)
        for error in errors:
            print(f"{path}: {error}", file=sys.stderr)
            failures += 1

    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
