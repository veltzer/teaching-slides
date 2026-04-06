#!/usr/bin/env python3
"""
check_code_labels.py — lint code-block language labels in markdown files.

For every fenced code block (```label ... ```) found in the given files or
directories, verifies that the label is listed in config/code_labels.py.
Exits with code 1 if any violations are found.

Usage:
    python scripts/check_code_labels.py [paths...] [--quiet]
    python scripts/check_code_labels.py marp/          # scan a directory
    python scripts/check_code_labels.py marp/foo.md    # scan a single file
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Iterator
from config.code_labels import VALID  # noqa: E402

# Locate the project root (one level up from this script's directory) and
# import the labels module from config/.
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))


# Matches the opening fence of a fenced code block, capturing the label.
# Handles optional leading spaces (up to 3) per the CommonMark spec.
_FENCE_RE = re.compile(r'^[ \t]{0,3}```(\w+)', re.MULTILINE)


def iter_labels(text: str) -> Iterator[tuple[str, int]]:
    """Yield (label, line_number) for every opening code fence in *text*."""
    for m in _FENCE_RE.finditer(text):
        line_no = text.count('\n', 0, m.start()) + 1
        yield m.group(1), line_no


def check_file(path: Path) -> list[tuple[int, str]]:
    """
    Return a list of (line_number, label) pairs for every invalid label found
    in *path*.
    """
    text = path.read_text(encoding='utf-8')
    return [
        (line_no, label)
        for label, line_no in iter_labels(text)
        if label not in VALID
    ]


def check_path(path: Path) -> dict[Path, list[tuple[int, str]]]:
    """Recursively check a file or directory; return {path: violations}."""
    if path.is_file():
        return {path: check_file(path)}
    return {
        md: check_file(md)
        for md in sorted(path.rglob('*.md'))
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Check fenced code-block labels against the allowed list.'
    )
    parser.add_argument(
        'paths',
        nargs='*',
        default=['.'],
        help='Markdown files or directories to scan (default: current directory)',
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress the summary line; only print violations',
    )
    args = parser.parse_args()

    all_violations: dict[Path, list[tuple[int, str]]] = {}
    for p in args.paths:
        path = Path(p)
        if not path.exists():
            print(f'error: path not found: {path}', file=sys.stderr)
            sys.exit(1)
        all_violations.update(check_path(path))

    total_files = len(all_violations)
    total_violations = sum(len(v) for v in all_violations.values())

    for file_path, violations in all_violations.items():
        for line_no, label in violations:
            print(f'{file_path}:{line_no}: invalid label `{label}`')

    if not args.quiet:
        files_with_issues = sum(1 for v in all_violations.values() if v)
        print(
            f'\n{total_violations} violation(s) in '
            f'{files_with_issues}/{total_files} file(s).',
            file=sys.stderr if total_violations else sys.stdout,
        )

    sys.exit(1 if total_violations else 0)


if __name__ == '__main__':
    main()
