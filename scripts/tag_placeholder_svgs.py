#!/usr/bin/env python
"""
Scan svg/ for placeholder SVGs and tag them with a PLACEHOLDERSVG comment
so they can be found and rewritten later.

A placeholder is identified by having >=3 <text> elements whose content is
a single uppercase letter ("A", "B", "C", ...) — the signature of a
scaffolded SVG where real labels were never filled in.

Adds `<!-- PLACEHOLDERSVG -->` as the first child of the root <svg> if the
file is a placeholder AND doesn't already contain the marker.

Idempotent. Safe to re-run.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TEXT_RE = re.compile(r'<text[^>]*?>(.*?)</text>', re.DOTALL)
PLACEHOLDER_LABELS = set("ABCDEFGHIJ")
MARKER = "PLACEHOLDERSVG"


def is_placeholder(content: str) -> bool:
    stripped = re.sub(r'<defs\b.*?</defs>', '', content, flags=re.DOTALL)
    texts = [re.sub(r'<[^>]+>', '', t).strip() for t in TEXT_RE.findall(stripped)]
    texts = [t for t in texts if t]
    if len(texts) < 3:
        return False
    placeholder_count = sum(1 for t in texts if t in PLACEHOLDER_LABELS)
    return placeholder_count >= 3 and placeholder_count / len(texts) >= 0.4


def tag_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    if MARKER in content:
        return False
    if not is_placeholder(content):
        return False
    # Insert marker right after the opening <svg ...> tag
    new = re.sub(
        r'(<svg\b[^>]*>)',
        r'\1\n  <!-- PLACEHOLDERSVG — scaffolded diagram, needs real content -->',
        content,
        count=1,
    )
    if new == content:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    svg_root = repo_root / "svg"
    tagged = 0
    for p in sorted(svg_root.rglob("*.svg")):
        if tag_file(p):
            tagged += 1
            print(f"tagged: {p.relative_to(repo_root)}")
    print(f"\n{tagged} placeholder SVGs tagged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
