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

Usage:
    md_checks.py --links --labels file1.md file2.md ...
    md_checks.py --links marp/                          # scan a directory
    md_checks.py --labels marp/courses/foo.md           # single check on one file
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


# ── Link checking ──

_LINK_RE = re.compile(r'^\[([^\]]+)\]\(([^)]+)\)')


def _is_local_link(link: str) -> bool:
    return not (link.startswith('http://') or
                link.startswith('https://') or
                link.startswith('ftp://') or
                link.startswith('mailto:'))


def _remove_code_blocks(content: str) -> str:
    return re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)


def _check_links(path: Path) -> list[str]:
    """Return list of error messages for broken local links."""
    content = path.read_text(encoding='utf-8')
    content = _remove_code_blocks(content)
    errors = []
    for m in _LINK_RE.finditer(content):
        text, link = m.groups()
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
            errors.append(f"{path}: broken link [{text}]({link})")
    return errors


# ── Label checking ──

_FENCE_RE = re.compile(r'^[ \t]{0,3}```(\w+)', re.MULTILINE)
def _load_labels() -> frozenset:
    labels_file = _ROOT / 'text_labels.yaml'
    with open(labels_file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return frozenset(
        entry['label']
        for category in data.values()
        for entry in category
    )


def _iter_labels(text: str) -> Iterator[tuple[str, int]]:
    for m in _FENCE_RE.finditer(text):
        line_no = text.count('\n', 0, m.start()) + 1
        yield m.group(1), line_no


_VALID_LABELS = _load_labels()


def _check_labels(path: Path) -> list[str]:
    """Return list of error messages for invalid code block labels."""
    valid = _VALID_LABELS
    text = path.read_text(encoding='utf-8')
    errors = []
    for label, line_no in _iter_labels(text):
        if label not in valid:
            errors.append(f"{path}:{line_no}: invalid label `{label}`")
    return errors


# ── Fence checking ──

_FENCE_LINE_RE = re.compile(r'^[ \t]{0,3}```', re.MULTILINE)


def _check_fences(path: Path) -> list[str]:
    """Return list of error messages if code fences are unclosed."""
    text = path.read_text(encoding='utf-8')
    fence_count = len(_FENCE_LINE_RE.findall(text))
    if fence_count % 2 != 0:
        return [f"{path}: unclosed code fence ({fence_count} fence lines, expected even)"]
    return []


# ── External URL checking ──

_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def _check_urls(path: Path) -> list[str]:
    """Return list of error messages for external URLs in image references."""
    text = path.read_text(encoding='utf-8')
    # Remove code blocks to avoid false positives
    text = _remove_code_blocks(text)
    errors = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in _IMAGE_RE.finditer(line):
            url = m.group(2)
            if url.startswith('http://') or url.startswith('https://'):
                errors.append(f"{path}:{line_no}: external image URL: {url}")
    return errors


# ── Whitespace checking ──


def _check_whitespace(path: Path) -> list[str]:
    """Check for trailing whitespace and consecutive blank lines."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
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


# ── Empty slides checking ──


def _check_slides(path: Path) -> list[str]:
    """Check for empty slides (--- immediately followed by --- with only blank lines between)."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    errors = []
    # Track: after seeing a ---, if we see only blank lines then another ---, it's empty
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


# ── Image reference checking ──


def _check_images(path: Path) -> list[str]:
    """Check that image references point to existing local files."""
    text = path.read_text(encoding='utf-8')
    text_no_code = _remove_code_blocks(text)
    errors = []
    for line_no, line in enumerate(text_no_code.splitlines(), 1):
        for m in _IMAGE_RE.finditer(line):
            target = m.group(2)
            # Skip external URLs and marp bg directives with URLs
            if target.startswith('http://') or target.startswith('https://'):
                continue
            # Strip marp-specific prefixes like "bg right:40% 80%"
            # The actual path is the last space-separated token
            clean = target.strip()
            if ' ' in clean:
                clean = clean.rsplit(' ', 1)[-1]
            # Resolve relative to the repo root (marp uses baseUrl)
            resolved = _ROOT / clean
            if not resolved.exists():
                # Also try relative to the file
                resolved_rel = path.parent / clean
                if not resolved_rel.exists():
                    errors.append(f"{path}:{line_no}: broken image reference: {clean}")
    return errors


# ── Numbered list checking ──

_NUMBERED_LIST_RE = re.compile(r'^(\s*)([2-9]\d*)\. ')


def _check_numbering(path: Path) -> list[str]:
    """Check for sequential numbered lists (should always use 1. 1. 1.)."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    errors = []
    in_code = False
    for line_no, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code = not in_code
        if not in_code and _NUMBERED_LIST_RE.match(line):
            errors.append(f"{path}:{line_no}: sequential numbering (use 1. not {_NUMBERED_LIST_RE.match(line).group(2)}.)")
    return errors


# ── Main ──

def _collect_files(paths: list[str]) -> list[Path]:
    """Expand paths: files are kept, directories are recursively scanned for .md."""
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
    args = parser.parse_args()

    # Default: all checks enabled
    flags = [args.links, args.labels, args.fences, args.urls,
             args.whitespace, args.slides, args.images, args.numbering]
    explicit = any(flags)
    do_links = args.links or not explicit
    do_labels = args.labels or not explicit
    do_fences = args.fences or not explicit
    do_urls = args.urls or not explicit
    do_whitespace = args.whitespace or not explicit
    do_slides = args.slides or not explicit
    do_images = args.images or not explicit
    do_numbering = args.numbering or not explicit

    files = _collect_files(args.paths)
    all_errors: list[str] = []

    for path in files:
        if do_links:
            all_errors.extend(_check_links(path))
        if do_labels:
            all_errors.extend(_check_labels(path))
        if do_fences:
            all_errors.extend(_check_fences(path))
        if do_urls:
            all_errors.extend(_check_urls(path))
        if do_whitespace:
            all_errors.extend(_check_whitespace(path))
        if do_slides:
            all_errors.extend(_check_slides(path))
        if do_images:
            all_errors.extend(_check_images(path))
        if do_numbering:
            all_errors.extend(_check_numbering(path))

    for err in all_errors:
        print(err, file=sys.stderr)

    sys.exit(1 if all_errors else 0)


if __name__ == '__main__':
    main()
