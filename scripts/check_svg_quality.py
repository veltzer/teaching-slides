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

MIN_FILE_SIZE = 450
MIN_ELEMENTS = 5


def check_file(path: Path) -> str | None:
    """Return an error message if the SVG looks like a placeholder, else None."""
    size = path.stat().st_size
    if size < MIN_FILE_SIZE:
        return f"too small ({size} bytes, min {MIN_FILE_SIZE})"

    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return f"XML parse error: {e}"

    count = sum(1 for _ in tree.iter())
    if count < MIN_ELEMENTS:
        return f"too few elements ({count}, min {MIN_ELEMENTS})"

    return None


def main() -> None:
    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: check_svg_quality.py file1.svg [file2.svg ...]")

    failures = 0
    for path_str in args:
        path = Path(path_str)
        error = check_file(path)
        if error:
            print(f"{path}: {error}", file=sys.stderr)
            failures += 1

    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
