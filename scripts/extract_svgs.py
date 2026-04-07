#!/usr/bin/env python

"""
Extract inline SVGs from marp markdown files into separate .svg files
under an svg/ directory mirroring the marp/ structure, and replace
them with markdown image references.

Idempotent: if no inline SVGs remain, prints nothing and exits 0.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARP_DIR = ROOT / 'marp'
SVG_DIR = ROOT / 'svg'

# Match complete <svg ...>...</svg> blocks (possibly multiline)
SVG_RE = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL)

# Match marp slide headings
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


def find_heading_for_position(text: str, pos: int) -> str:
    """Find the nearest heading before the given position."""
    best = None
    for m in HEADING_RE.finditer(text):
        if m.start() <= pos:
            best = m.group(1)
        else:
            break
    return best or 'diagram'


def process_file(md_path: Path) -> int:
    """Extract SVGs from one file, replace with image refs. Returns count."""
    text = md_path.read_text(encoding='utf-8')
    matches = list(SVG_RE.finditer(text))
    if not matches:
        return 0

    rel = md_path.relative_to(MARP_DIR)
    out_dir = SVG_DIR / rel.parent / rel.stem
    abs_prefix = 'svg/' + str(rel.parent / rel.stem)

    # First pass: compute names, detect collisions
    slug_counts: dict[str, int] = {}
    entries = []
    for m in matches:
        heading = find_heading_for_position(text, m.start())
        slug = slugify(heading)
        slug_counts[slug] = slug_counts.get(slug, 0) + 1
        entries.append((slug, m))

    # Second pass: assign unique names
    final_counts = dict(slug_counts)
    seen: dict[str, int] = {}
    named: list[tuple[str, re.Match]] = []
    for slug, m in entries:
        if final_counts[slug] == 1:
            name = slug
        else:
            seen[slug] = seen.get(slug, 0) + 1
            name = f'{slug}_{seen[slug]}'
        named.append((name, m))

    # Write SVG files
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, m in named:
        svg_path = out_dir / f'{name}.svg'
        svg_path.write_text(m.group(0) + '\n', encoding='utf-8')

    # Replace inline SVGs with image references (work backwards to preserve positions)
    for name, m in reversed(named):
        img_ref = f'![{name}]({abs_prefix}/{name}.svg)'
        text = text[:m.start()] + img_ref + text[m.end():]

    md_path.write_text(text, encoding='utf-8')
    return len(named)


def main() -> None:
    total = 0
    for md_path in sorted(MARP_DIR.rglob('*.md')):
        total += process_file(md_path)

    print(f'Extracted {total} SVGs')


if __name__ == '__main__':
    main()
