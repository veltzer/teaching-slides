#!/usr/bin/env python
"""
Fix Marp slide files so that every slide containing an SVG image has at most
one line of non-heading content above the SVG (the ## heading itself counts
as the one allowed line).

Rule: on any slide that contains an ![...](....svg) reference, all content
lines that appear BEFORE the image line (excluding the ## heading) are removed.
Content that appears AFTER the image is left untouched.
"""
import re
import sys
from pathlib import Path


def fix_file(path: Path) -> bool:
    """Return True if file was modified."""
    text = path.read_text(encoding="utf-8")

    # Split into slides on --- separator (keeping the ---)
    # We process each slide independently
    raw_slides = re.split(r'^---$', text, flags=re.MULTILINE)

    new_slides = []
    modified = False

    for slide in raw_slides:
        new_slide = fix_slide(slide)
        if new_slide != slide:
            modified = True
        new_slides.append(new_slide)

    if not modified:
        return False

    path.write_text("---".join(new_slides), encoding="utf-8")
    return True


def fix_slide(slide: str) -> str:
    """
    If this slide contains an SVG image reference, ensure there is at most
    one line of content above it (the ## heading line). Remove any extra
    content lines between the heading and the image.
    """
    lines = slide.split("\n")

    # Find the image line index
    img_idx = None
    for i, line in enumerate(lines):
        if re.match(r'!\[.*\]\(.*\.svg\)', line.strip()):
            img_idx = i
            break

    if img_idx is None:
        return slide  # no SVG in this slide

    # Find the heading line (## ...)
    heading_idx = None
    for i, line in enumerate(lines):
        if re.match(r'^#{1,6}\s', line):
            heading_idx = i
            break

    if heading_idx is None:
        return slide  # no heading, leave alone

    # Lines between heading and image (exclusive of both)
    between_start = heading_idx + 1
    between_end = img_idx

    # Collect the lines between heading and image, ignoring blank lines
    between_lines = [l for l in lines[between_start:between_end] if l.strip()]

    if not between_lines:
        return slide  # nothing between heading and image, already correct

    # Remove all non-blank content lines between heading and image
    # Keep blank lines structure: just heading, blank, image
    new_lines = (
        lines[:between_start]           # heading and before
        + [""]                           # one blank line
        + lines[img_idx:]               # image and after
    )

    return "\n".join(new_lines)


def main():
    root = Path("marp")
    if not root.exists():
        print("ERROR: run from project root", file=sys.stderr)
        sys.exit(1)

    files = sorted(root.rglob("*.md"))
    modified = 0
    for f in files:
        if fix_file(f):
            modified += 1
            print(f"fixed: {f}")

    print(f"\nDone: {modified} files modified.")


if __name__ == "__main__":
    main()
