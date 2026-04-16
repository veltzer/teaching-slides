#!/usr/bin/env python
"""
Fix Marp slide files so that every slide containing an SVG image has ONLY
the ## heading and the image line — no other real content on the same slide.

"Real content" means non-blank, non-heading lines.

For each violating slide:
- Content BEFORE the image (after the heading) -> moved to a new slide BEFORE the image slide
- Content AFTER the image -> moved to a new slide AFTER the image slide

The heading is duplicated on each split slide.
"""
import re
import sys
from pathlib import Path

IMG_RE = re.compile(r'!\[.*?\]\(.*?\.svg\)')
HEADING_RE = re.compile(r'^#{1,6}\s')


def is_real_content(line: str) -> bool:
    """True if line has actual content (not blank, not a heading, not the image itself)."""
    stripped = line.strip()
    if not stripped:
        return False
    if HEADING_RE.match(line):
        return False
    if IMG_RE.match(stripped):
        return False
    return True


def fix_slide(slide: str) -> str:
    """
    Given raw slide text (without the surrounding --- separators),
    return fixed slide text (may contain multiple slides joined by ---).
    """
    lines = slide.split('\n')

    # Find image line index
    img_idx = None
    for i, line in enumerate(lines):
        if IMG_RE.search(line.strip()):
            img_idx = i
            break

    if img_idx is None:
        return slide  # no SVG

    # Find heading line
    heading_idx = None
    heading_line = ''
    for i, line in enumerate(lines):
        if HEADING_RE.match(line):
            heading_idx = i
            heading_line = line
            break

    # Lines before image (after heading): check for real content
    pre_start = (heading_idx + 1) if heading_idx is not None else 0
    pre_lines = lines[pre_start:img_idx]
    pre_content = [line for line in pre_lines if is_real_content(line)]

    # Lines after image: check for real content
    post_lines = lines[img_idx + 1:]
    post_content = [line for line in post_lines if is_real_content(line)]

    if not pre_content and not post_content:
        return slide  # already compliant

    # Build replacement slides
    result_parts = []

    # If pre-content exists, create a slide before the image slide
    if pre_content:
        pre_slide_lines = []
        if heading_line:
            pre_slide_lines.append(heading_line)
        pre_slide_lines.append('')
        for ln in pre_lines:
            if is_real_content(ln) or ln.strip() == '':
                pre_slide_lines.append(ln)
        # Strip trailing blanks
        while pre_slide_lines and not pre_slide_lines[-1].strip():
            pre_slide_lines.pop()
        result_parts.append('\n'.join(pre_slide_lines))

    # The image-only slide
    img_slide_lines = []
    if heading_line:
        img_slide_lines.append(heading_line)
        img_slide_lines.append('')
    img_slide_lines.append(lines[img_idx].strip())
    result_parts.append('\n'.join(img_slide_lines))

    # If post-content exists, create a slide after the image slide
    if post_content:
        post_slide_lines = []
        if heading_line:
            post_slide_lines.append(heading_line)
            post_slide_lines.append('')
        # Add post lines, skip leading blanks
        started = False
        for ln in post_lines:
            if not started and not ln.strip():
                continue
            started = True
            post_slide_lines.append(ln)
        # Strip trailing blanks
        while post_slide_lines and not post_slide_lines[-1].strip():
            post_slide_lines.pop()
        result_parts.append('\n'.join(post_slide_lines))

    return '\n\n---\n\n'.join(result_parts)


def fix_file(path: Path) -> bool:
    """Return True if file was modified."""
    text = path.read_text(encoding='utf-8')

    # Split on --- slide separators
    raw_slides = re.split(r'\n---\n', text)

    new_slides = []
    modified = False
    for slide in raw_slides:
        fixed = fix_slide(slide)
        if fixed != slide:
            modified = True
        new_slides.append(fixed)

    if not modified:
        return False

    result = '\n---\n'.join(new_slides)
    # Ensure single trailing newline
    result = result.rstrip('\n') + '\n'
    path.write_text(result, encoding='utf-8')
    return True


def main():
    root = Path('marp')
    if not root.exists():
        print('ERROR: run from project root', file=sys.stderr)
        sys.exit(1)

    files = sorted(root.rglob('*.md'))
    modified = 0
    for f in files:
        if fix_file(f):
            modified += 1
            print(f'fixed: {f}')

    print(f'\nDone: {modified} files modified.')


if __name__ == '__main__':
    main()
