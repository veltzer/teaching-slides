#!/usr/bin/env python
"""Find SVG files that are not referenced in any Markdown slide file."""

import re
from pathlib import Path

ROOT = Path(__file__)

svg_dir = ROOT / "svg"
marp_dir = ROOT / "marp"

# Collect all .svg files (relative to ROOT) — from svg/ and jpg/
all_svgs = set()
for search_dir in [svg_dir, ROOT / "jpg"]:
    for path in search_dir.rglob("*.svg"):
        all_svgs.add(path.relative_to(ROOT).as_posix())

# Collect all SVG references from all .md files (skip http/https URLs)
referenced = set()
image_pattern = re.compile(r'!\[.*?\]\(([^)]+\.svg)\)')

for md_path in marp_dir.rglob("*.md"):
    text = md_path.read_text(encoding="utf-8", errors="replace")
    for match in image_pattern.finditer(text):
        ref = match.group(1).strip()
        if not ref.startswith("http"):
            referenced.add(ref)

# Find unreferenced SVGs
unused = sorted(all_svgs - referenced)

if unused:
    print(f"Found {len(unused)} unused SVG(s):\n")
    for svg in unused:
        print(f"  {svg}")
else:
    print("All SVG files are referenced in at least one Markdown file.")

print(f"\nTotal SVGs: {len(all_svgs)}  Referenced: {len(referenced)}  Unused: {len(unused)}")
