#!/usr/bin/env python

"""
Extract inline Mermaid diagrams from Marp markdown files into separate .mmd
files under a mermaid/ directory mirroring the marp/ structure, and replace
them with markdown image references using absolute paths.

Also removes the Mermaid.js <script> tags since they are no longer needed.

Idempotent: if no inline Mermaid blocks remain, prints nothing and exits 0.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARP_DIR = ROOT / 'marp'
MERMAID_DIR = ROOT / 'mermaid'

# Match <div class="mermaid">...</div> blocks (multiline)
MERMAID_RE = re.compile(
    r'<div\s+class\s*=\s*"mermaid"\s*>\s*\n(.*?)</div>',
    re.DOTALL,
)

# Match the mermaid script block (comment + script tags)
SCRIPT_RE = re.compile(
    r'(?:<!-- Add Mermaid\.js support -->\n)?'
    r'<script src="https://cdn\.jsdelivr\.net/npm/mermaid@\d+/dist/mermaid\.min\.js"></script>\n'
    r'<script>\n'
    r'\s*mermaid\.initialize\(\{[^}]*\}\);\n'
    r'</script>\n',
    re.DOTALL,
)

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
    """Extract Mermaid blocks from one file. Returns count."""
    text = md_path.read_text(encoding='utf-8')
    matches = list(MERMAID_RE.finditer(text))
    if not matches:
        return 0

    rel = md_path.relative_to(MARP_DIR)
    out_dir = MERMAID_DIR / rel.parent / rel.stem
    abs_prefix = 'out/mermaid/' + str(rel.parent / rel.stem)

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

    # Write Mermaid files
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, m in named:
        mmd_path = out_dir / f'{name}.mmd'
        content = m.group(1).rstrip() + '\n'
        mmd_path.write_text(content, encoding='utf-8')

    # Replace inline Mermaid blocks with references (work backwards)
    for name, m in reversed(named):
        ref = f'![{name}]({abs_prefix}/{name}.mmd)'
        text = text[:m.start()] + ref + text[m.end():]

    # Remove mermaid script tags
    text = SCRIPT_RE.sub('', text)

    md_path.write_text(text, encoding='utf-8')
    return len(named)


def main() -> None:
    total = 0
    for md_path in sorted(MARP_DIR.rglob('*.md')):
        count = process_file(md_path)
        if count:
            print(f'  {md_path.relative_to(ROOT)}: {count} extracted')
            total += count
    print(f'Extracted {total} Mermaid diagrams')


if __name__ == '__main__':
    main()
