#!/usr/bin/env python

"""
Extract diagram content from Marp markdown files.

Supports two modes:
1. --diagrams: List ```diagram blocks (for conversion to SVG)
2. --svgs: Extract inline <svg> tags to files and replace with image references

Usage:
    ./scripts/extract.py --diagrams [--json]
    ./scripts/extract.py --svgs
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(".")
if not (ROOT / ".git").exists():
    print("Error: script must be run from the root of the repository", file=sys.stderr)
    sys.exit(1)

MARP_DIR = ROOT / 'marp'
SVG_DIR = ROOT / 'svg'

# Regular expressions
DIAGRAM_RE = re.compile(r'```diagram\s*\n(.*?)```', re.DOTALL)
SVG_RE = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL)
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
    """Find the nearest heading before the given position."""
    best = None
    for m in HEADING_RE.finditer(text):
        if m.start() <= pos:
            best = m.group(1)
        else:
            break
    return best or 'diagram'


def get_unique_names(text: str, matches: list[re.Match]) -> list[str]:
    """Assign unique slug-based names to each match."""
    slug_counts = {}
    entries = []
    for m in matches:
        heading = find_heading(text, m.start())
        slug = slugify(heading)
        slug_counts[slug] = slug_counts.get(slug, 0) + 1
        entries.append(slug)

    final_counts = dict(slug_counts)
    seen = {}
    names = []
    for slug in entries:
        if final_counts[slug] == 1:
            name = slug
        else:
            seen[slug] = seen.get(slug, 0) + 1
            name = f'{slug}_{seen[slug]}'
        names.append(name)
    return names


def handle_diagrams(as_json: bool):
    """List all ```diagram blocks."""
    results = []
    for md_path in sorted(MARP_DIR.rglob('*.md')):
        text = md_path.read_text(encoding='utf-8')
        matches = list(DIAGRAM_RE.finditer(text))
        if not matches:
            continue

        rel = md_path.relative_to(MARP_DIR)
        names = get_unique_names(text, matches)

        for name, m in zip(names, matches):
            heading = find_heading(text, m.start())
            svg_rel = f'svg/{rel.parent}/{rel.stem}/{name}.svg'
            results.append({
                'md_file': str(md_path.relative_to(ROOT)),
                'svg_path': svg_rel,
                'name': name,
                'heading': heading,
                'content': m.group(1).rstrip(),
            })

    if as_json:
        json.dump(results, sys.stdout, indent=2)
    else:
        for r in results:
            print(f"{r['md_file']}: {r['name']} ({r['heading']})")
        print(f"\nTotal: {len(results)} diagram blocks in {len(set(r['md_file'] for r in results))} files")


def handle_svgs():
    """Extract inline SVGs to files and replace with image references."""
    total = 0
    for md_path in sorted(MARP_DIR.rglob('*.md')):
        text = md_path.read_text(encoding='utf-8')
        matches = list(SVG_RE.finditer(text))
        if not matches:
            continue

        rel = md_path.relative_to(MARP_DIR)
        out_dir = SVG_DIR / rel.parent / rel.stem
        abs_prefix = 'svg/' + str(rel.parent / rel.stem)
        names = get_unique_names(text, matches)

        # Write SVG files
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, m in zip(names, matches):
            svg_path = out_dir / f'{name}.svg'
            svg_path.write_text(m.group(0) + '\n', encoding='utf-8')

        # Replace inline SVGs (work backwards to preserve positions)
        for name, m in reversed(list(zip(names, matches))):
            img_ref = f'![{name}]({abs_prefix}/{name}.svg)'
            text = text[:m.start()] + img_ref + text[m.end():]

        md_path.write_text(text, encoding='utf-8')
        total += len(matches)

    print(f'Extracted {total} SVGs')


def main():
    if '--diagrams' in sys.argv:
        handle_diagrams(as_json='--json' in sys.argv)
    elif '--svgs' in sys.argv:
        handle_svgs()
    else:
        print("Usage: scripts/extract.py [--diagrams [--json] | --svgs]", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
