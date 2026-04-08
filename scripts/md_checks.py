#!/usr/bin/env python

"""
Unified markdown checker for Marp slide files.

Checks:
  --links       Validate that local links point to existing files
  --labels      Validate fenced code block language labels against text_labels.yaml

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

_ROOT = Path(__file__).resolve().parent.parent


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
    args = parser.parse_args()

    # Default: all checks enabled
    run_all = not args.links and not args.labels
    do_links = args.links or run_all
    do_labels = args.labels or run_all

    files = _collect_files(args.paths)
    all_errors: list[str] = []

    for path in files:
        if do_links:
            all_errors.extend(_check_links(path))
        if do_labels:
            all_errors.extend(_check_labels(path))

    for err in all_errors:
        print(err, file=sys.stderr)

    sys.exit(1 if all_errors else 0)


if __name__ == '__main__':
    main()
