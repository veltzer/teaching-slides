#!/usr/bin/env python

"""
Convert relative SVG image references in Marp markdown files to project-root paths.

Replaces patterns like:
  ![name](../../../../svg/courses/foo/bar/name.svg)
  ![name](../../svg/lectures/baz/name.svg)
with:
  ![name](svg/courses/foo/bar/name.svg)
  ![name](svg/lectures/baz/name.svg)
"""

import re
import sys
from pathlib import Path

ROOT = Path(".")
if not (ROOT / ".git").exists():
    print("Error: script must be run from the root of the repository", file=sys.stderr)
    sys.exit(1)
MARP_DIR = ROOT / 'marp'

# Match image references with relative SVG paths
REL_SVG_RE = re.compile(r'(!\[[^\]]*\]\()(\.\./)+svg/', re.MULTILINE)


def fix_file(md_path: Path) -> int:
    """Fix relative SVG paths in one file. Returns number of replacements."""
    text = md_path.read_text(encoding='utf-8')
    new_text = REL_SVG_RE.sub(r'\1svg/', text)
    if new_text == text:
        return 0
    count = len(REL_SVG_RE.findall(text))
    md_path.write_text(new_text, encoding='utf-8')
    return count


def main() -> None:
    total = 0
    for md_path in sorted(MARP_DIR.rglob('*.md')):
        count = fix_file(md_path)
        if count:
            print(f'  {md_path.relative_to(ROOT)}: {count} paths fixed')
            total += count
    print(f'Fixed {total} SVG paths')


if __name__ == '__main__':
    main()
