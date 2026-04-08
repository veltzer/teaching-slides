#!/usr/bin/env python

"""
Extract ```diagram code blocks from Marp markdown files and list them
with their context (heading, file, content) for conversion to SVG.

Usage:
    ./scripts/extract_diagrams.py          # list all diagram blocks
    ./scripts/extract_diagrams.py --json   # output as JSON for automation
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARP_DIR = ROOT / 'marp'
SVG_DIR = ROOT / 'svg'

DIAGRAM_RE = re.compile(r'```diagram\s*\n(.*?)```', re.DOTALL)
HEADING_RE = re.compile(r'^#{1,3}\s+(.+)', re.MULTILINE)


def slugify(text: str) -> str:
    """Convert heading text to a filesystem-safe snake_case slug."""
    text = text.strip().lower()
    text = re.sub(r'[*_`~\[\]()]', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = text.strip('_')
    if len(text) > 60:
        text = text[:60].rstrip('_')
    return text or 'diagram'


def find_heading(text: str, pos: int) -> str:
    best = None
    for m in HEADING_RE.finditer(text):
        if m.start() <= pos:
            best = m.group(1)
        else:
            break
    return best or 'diagram'


def extract_all():
    results = []
    for md_path in sorted(MARP_DIR.rglob('*.md')):
        text = md_path.read_text(encoding='utf-8')
        matches = list(DIAGRAM_RE.finditer(text))
        if not matches:
            continue

        rel = md_path.relative_to(MARP_DIR)
        slug_counts = {}
        entries = []

        for m in matches:
            heading = find_heading(text, m.start())
            slug = slugify(heading)
            slug_counts[slug] = slug_counts.get(slug, 0) + 1
            entries.append((slug, m))

        final_counts = dict(slug_counts)
        seen = {}
        for slug, m in entries:
            if final_counts[slug] == 1:
                name = slug
            else:
                seen[slug] = seen.get(slug, 0) + 1
                name = f'{slug}_{seen[slug]}'

            svg_rel = f'svg/{rel.parent}/{rel.stem}/{name}.svg'
            results.append({
                'md_file': str(md_path.relative_to(ROOT)),
                'svg_path': svg_rel,
                'name': name,
                'heading': heading,
                'content': m.group(1).rstrip(),
            })
    return results


def main():
    results = extract_all()
    if '--json' in sys.argv:
        json.dump(results, sys.stdout, indent=2)
    else:
        for r in results:
            print(f"{r['md_file']}: {r['name']} ({r['heading']})")
        print(f"\nTotal: {len(results)} diagram blocks in {len(set(r['md_file'] for r in results))} files")


if __name__ == '__main__':
    main()
