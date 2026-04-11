#!/usr/bin/env python
"""Count total Marp slides across all markdown files, excluding YAML front matter."""
from pathlib import Path


def count():
    total = 0
    for f in Path("marp").rglob("*.md"):
        content = f.read_text(encoding="utf-8", errors="replace")
        if content.startswith("---"):
            end = content.find("\n---", 3)
            if end != -1:
                content = content[end + 4:]
        total += 1 + sum(1 for line in content.splitlines() if line.strip() == "---")
    print(total)


if __name__ == "__main__":
    count()
