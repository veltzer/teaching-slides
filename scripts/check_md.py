#!/usr/bin/env python

"""
Unified markdown checker for Marp slide files.

Checks:
  --links       Validate that local links point to existing files
  --labels      Validate fenced code block language labels against text_labels.yaml
  --fences      Check for unclosed code fences (odd number of ``` lines)
  --urls        Check for external URLs in image references (should be local)
  --whitespace  Check for trailing whitespace and consecutive blank lines
  --slides      Check for empty slides (consecutive --- separators)
  --images      Check that image references point to existing local files
  --numbering   Check for sequential numbered lists (should use 1. 1. 1.)
  --svg-content Check that slides with SVG images have no other content on the same slide

Usage:
    check_md.py --links --labels file1.md file2.md ...
    check_md.py --links marp/                          # scan a directory
    check_md.py --labels marp/courses/foo.md           # single check on one file
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Iterator

import yaml

_ROOT = Path(".")
if not (_ROOT / ".git").exists():
    print("Error: script must be run from the root of the repository", file=sys.stderr)
    sys.exit(1)


# ── Regexes ──

_LINK_RE = re.compile(r'^\[([^\]]+)\]\(([^)]+)\)')
_FENCE_RE = re.compile(r'^[ \t]{0,3}```(\w+)', re.MULTILINE)
_FENCE_LINE_RE = re.compile(r'^[ \t]{0,3}```', re.MULTILINE)
_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
_SVG_IMAGE_RE = re.compile(r'!\[.*?\]\(.*?\.svg\)')
_HEADING_RE = re.compile(r'^#{1,6}\s')
_NUMBERED_LIST_RE = re.compile(r'^(\s*)([2-9]\d*)\. ')


# ── Helpers ──

def _is_local_link(link: str) -> bool:
    return not (link.startswith('http://') or
                link.startswith('https://') or
                link.startswith('ftp://') or
                link.startswith('mailto:'))


def _remove_code_blocks(content: str) -> str:
    return re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)


def _load_labels() -> frozenset:
    labels_file = _ROOT / 'text_labels.yaml'
    with open(labels_file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return frozenset(
        entry['label']
        for category in data.values()
        for entry in category
    )


_VALID_LABELS = _load_labels()


# ── Per-check functions (accept pre-loaded text/lines) ──

def _check_links(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for m in _LINK_RE.finditer(text_no_code):
        link_text, link = m.groups()
        if not _is_local_link(link):
            continue
        clean = link.split('#')[0]
        if not clean:
            continue
        if os.path.isabs(clean):
            target = Path(clean)
        else:
            target = (path.parent / clean).resolve()
        if not target.exists():
            errors.append(f"{path}: broken link [{link_text}]({link})")
    return errors


def _iter_labels(text: str) -> Iterator[tuple[str, int]]:
    for m in _FENCE_RE.finditer(text):
        line_no = text.count('\n', 0, m.start()) + 1
        yield m.group(1), line_no


def _check_labels(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for label, line_no in _iter_labels(text):
        if label not in _VALID_LABELS:
            errors.append(f"{path}:{line_no}: invalid label `{label}`")
    return errors


def _check_fences(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    fence_count = len(_FENCE_LINE_RE.findall(text))
    if fence_count % 2 != 0:
        return [f"{path}: unclosed code fence ({fence_count} fence lines, expected even)"]
    return []


def _check_urls(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for line_no, line in enumerate(text_no_code.splitlines(), 1):
        for m in _IMAGE_RE.finditer(line):
            url = m.group(2)
            if url.startswith('http://') or url.startswith('https://'):
                errors.append(f"{path}:{line_no}: external image URL: {url}")
    return errors


def _check_whitespace(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    prev_blank = False
    for line_no, line in enumerate(lines, 1):
        if line != line.rstrip():
            errors.append(f"{path}:{line_no}: trailing whitespace")
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            errors.append(f"{path}:{line_no}: consecutive blank lines")
        prev_blank = is_blank
    return errors


def _check_slides(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    last_separator = None
    only_blanks = True
    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == '---':
            if last_separator is not None and only_blanks:
                errors.append(f"{path}:{line_no}: empty slide (no content between --- separators)")
            last_separator = line_no
            only_blanks = True
        elif stripped != '':
            only_blanks = False
    return errors


def _check_images(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for line_no, line in enumerate(text_no_code.splitlines(), 1):
        for m in _IMAGE_RE.finditer(line):
            target = m.group(2)
            if target.startswith('http://') or target.startswith('https://'):
                continue
            clean = target.strip()
            if ' ' in clean:
                clean = clean.rsplit(' ', 1)[-1]
            resolved = _ROOT / clean
            if not resolved.exists():
                resolved_rel = path.parent / clean
                if not resolved_rel.exists():
                    errors.append(f"{path}:{line_no}: broken image reference: {clean}")
    return errors


def _check_numbering(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    in_code = False
    for line_no, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code = not in_code
        if not in_code:
            m = _NUMBERED_LIST_RE.match(line)
            if m:
                errors.append(f"{path}:{line_no}: sequential numbering (use 1. not {m.group(2)}.)")
    return errors


def _check_svg_content(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    raw_slides = re.split(r'\n---\n', text)
    line_cursor = 1
    for slide in raw_slides:
        slide_lines = slide.split('\n')
        numbered = list(enumerate(slide_lines, line_cursor))
        has_svg = any(_SVG_IMAGE_RE.search(ln.strip()) for _, ln in numbered)
        if has_svg:
            headings = [(i, ln) for i, ln in numbered if ln.strip() and _HEADING_RE.match(ln)]
            non_heading_non_svg = [
                (i, ln) for i, ln in numbered
                if ln.strip()
                and not _HEADING_RE.match(ln)
                and not _SVG_IMAGE_RE.search(ln.strip())
            ]
            # More than one heading on an SVG slide is not allowed
            if len(headings) > 1:
                first_lineno, first_line = headings[1]
                errors.append(
                    f"{path}:{first_lineno}: slide with SVG image has multiple headings: {first_line.strip()!r}"
                )
            # Any non-heading, non-SVG content is not allowed
            if non_heading_non_svg:
                first_lineno, first_line = non_heading_non_svg[0]
                errors.append(
                    f"{path}:{first_lineno}: slide with SVG image contains other content: {first_line.strip()!r}"
                )
        line_cursor += len(slide_lines) + 1
    return errors


# ── Main ──

def _collect_files(paths: list[str]) -> list[Path]:
    result = []
    for p_str in paths:
        p = Path(p_str)
        if p.is_file():
            result.append(p)
        elif p.is_dir():
            result.extend(sorted(p.rglob('*.md')))
        else:
            print(f"error: path not found: {p}", file=sys.stderr)
            sys.exit(1)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Unified markdown checker for Marp slides.'
    )
    parser.add_argument('paths', nargs='*', default=['.'],
                        help='Markdown files or directories to check')
    parser.add_argument('--links', action='store_true',
                        help='Check that local links point to existing files')
    parser.add_argument('--labels', action='store_true',
                        help='Check fenced code block labels against text_labels.yaml')
    parser.add_argument('--fences', action='store_true',
                        help='Check for unclosed code fences')
    parser.add_argument('--urls', action='store_true',
                        help='Check for external URLs in image references')
    parser.add_argument('--whitespace', action='store_true',
                        help='Check for trailing whitespace and consecutive blank lines')
    parser.add_argument('--slides', action='store_true',
                        help='Check for empty slides (consecutive --- separators)')
    parser.add_argument('--images', action='store_true',
                        help='Check that image references point to existing local files')
    parser.add_argument('--numbering', action='store_true',
                        help='Check for sequential numbered lists (should use 1. 1. 1.)')
    parser.add_argument('--svg-content', action='store_true',
                        help='Check that slides with SVG images have no other content')
    args = parser.parse_args()

    # Default: all checks enabled
    flags = [args.links, args.labels, args.fences, args.urls,
             args.whitespace, args.slides, args.images, args.numbering,
             args.svg_content]
    explicit = any(flags)
    checks = []
    if args.links or not explicit:
        checks.append(_check_links)
    if args.labels or not explicit:
        checks.append(_check_labels)
    if args.fences or not explicit:
        checks.append(_check_fences)
    if args.urls or not explicit:
        checks.append(_check_urls)
    if args.whitespace or not explicit:
        checks.append(_check_whitespace)
    if args.slides or not explicit:
        checks.append(_check_slides)
    if args.images or not explicit:
        checks.append(_check_images)
    if args.numbering or not explicit:
        checks.append(_check_numbering)
    if args.svg_content or not explicit:
        checks.append(_check_svg_content)

    files = _collect_files(args.paths)
    all_errors: list[str] = []

    for path in files:
        text = path.read_text(encoding='utf-8')
        text_no_code = _remove_code_blocks(text)
        lines = text.splitlines()
        for check in checks:
            all_errors.extend(check(path, text, text_no_code, lines))

    for err in all_errors:
        print(err, file=sys.stderr)

    sys.exit(1 if all_errors else 0)


if __name__ == '__main__':
    main()
