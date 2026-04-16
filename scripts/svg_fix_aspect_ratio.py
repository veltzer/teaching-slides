#!/usr/bin/env python
"""
Fix all SVG files to have exactly viewBox="0 0 1280 720" and no width/height
attributes on the root <svg> element. This enforces the 16:9 1280x720 standard
matching Marp slide dimensions.
"""
import re
import sys
from pathlib import Path

TARGET_VIEWBOX = 'viewBox="0 0 1280 720"'


def fix_svg(path: Path) -> bool:
    """Return True if file was modified."""
    content = path.read_text(encoding="utf-8")

    # Work only on the opening <svg ...> tag
    svg_tag_match = re.search(r'<svg\b[^>]*>', content, re.DOTALL)
    if not svg_tag_match:
        return False

    original_tag = svg_tag_match.group(0)
    tag = original_tag

    # Remove width and height attributes
    tag = re.sub(r'\s+width="[^"]*"', '', tag)
    tag = re.sub(r'\s+height="[^"]*"', '', tag)

    # Replace or insert viewBox
    if re.search(r'viewBox="', tag):
        tag = re.sub(r'viewBox="[^"]*"', TARGET_VIEWBOX, tag)
    else:
        # Insert viewBox after <svg
        tag = tag.replace('<svg', f'<svg {TARGET_VIEWBOX}', 1)

    if tag == original_tag:
        return False

    new_content = content.replace(original_tag, tag, 1)
    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    svg_root = Path("svg")
    if not svg_root.exists():
        print("ERROR: run from project root (svg/ directory not found)", file=sys.stderr)
        sys.exit(1)

    files = sorted(svg_root.rglob("*.svg"))
    modified = 0
    skipped = 0
    for f in files:
        if fix_svg(f):
            modified += 1
            print(f"fixed: {f}")
        else:
            skipped += 1

    print(f"\nDone: {modified} fixed, {skipped} already correct or unchanged.")


if __name__ == "__main__":
    main()
