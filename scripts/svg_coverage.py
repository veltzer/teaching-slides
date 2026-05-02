#!/usr/bin/env python
"""Report SVG coverage per course, grouped into tiers.

For each course (a directory under marp/courses/<domain>/<course>/ that contains
*.md files), counts non-title SVG references and total Marp slides, and computes:

    ratio = svgs / slides

Slides are counted by parsing each markdown file: skip the YAML front matter,
then count `---` separators (one slide per separator, plus the first slide).

Prints a tier-summary table; pass --detail for a per-course table.
"""
import argparse
import re
from pathlib import Path

SVG_REF = re.compile(r"svg/(?:courses|lectures)/[^)\s]+\.svg")
TITLE_SVG = re.compile(r"/title\.svg\b")

TIERS = [
    (0.00, 0.05, "<= 0.05", "very low; less than 1 SVG per 20 slides"),
    (0.05, 0.10, "0.05-0.10", "low; about 1 SVG per 10-20 slides"),
    (0.10, 0.20, "0.10-0.20", "moderate; 1 SVG per 5-10 slides"),
    (0.20, 0.33, "0.20-0.33", "good; 1 SVG per 3-5 slides"),
    (0.33, 1.01, ">= 0.33", "rich; 1 SVG per 3 slides or better"),
]


def course_dirs(root: Path):
    """Yield directories that contain at least 2 markdown files (a real course)."""
    for course_dir in sorted(root.glob("courses/*/*/")):
        if not course_dir.is_dir():
            continue
        md_files = list(course_dir.glob("*.md"))
        if len(md_files) >= 2:
            yield course_dir, md_files


def slide_count(md_files):
    """Count Marp slides across the given markdown files.

    Each file contributes (1 + number of `---` separators after front matter).
    """
    total = 0
    for md in md_files:
        content = md.read_text(encoding="utf-8", errors="replace")
        if content.startswith("---"):
            end = content.find("\n---", 3)
            if end != -1:
                content = content[end + 4:]
        total += 1 + sum(1 for line in content.splitlines() if line.strip() == "---")
    return total


def svg_count(md_files):
    """Count non-title SVG references across the given markdown files."""
    n = 0
    for md in md_files:
        for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
            for ref in SVG_REF.findall(line):
                if not TITLE_SVG.search(ref):
                    n += 1
    return n


def tier_for(ratio):
    for lo, hi, label, _desc in TIERS:
        if lo <= ratio < hi:
            return label
    return TIERS[-1][2]


def print_table(headers, rows, aligns=None):
    """Print rows as a fixed-width table. aligns: 'l' or 'r' per column."""
    cols = list(zip(headers, *rows))
    widths = [max(len(str(c)) for c in col) for col in cols]
    if aligns is None:
        aligns = ["l"] * len(headers)

    def fmt(cells):
        return "  ".join(
            (str(c).rjust(w) if a == "r" else str(c).ljust(w))
            for c, w, a in zip(cells, widths, aligns)
        )

    print(fmt(headers))
    print(fmt(["-" * w for w in widths]))
    for row in rows:
        print(fmt(row))


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--detail", action="store_true", help="per-course table")
    p.add_argument("--root", default="marp", help="marp root (default: marp)")
    args = p.parse_args()

    rows = []
    for course_dir, md_files in course_dirs(Path(args.root)):
        slides = slide_count(md_files)
        svgs = svg_count(md_files)
        ratio = svgs / slides if slides else 0.0
        rows.append((ratio, svgs, slides, course_dir))

    rows.sort()

    if args.detail:
        print("Per-course SVG coverage")
        print()
        print("Columns:")
        print("  ratio   - svgs / slides (higher = better illustrated)")
        print("  svgs    - non-title SVG references in the course's markdown")
        print("  slides  - total Marp slides (--- separated, ex front matter)")
        print("  course  - path to the course directory")
        print()
        detail_rows = [
            (f"{r:.2f}", s, sl, str(p)) for r, s, sl, p in rows
        ]
        print_table(
            ["ratio", "svgs", "slides", "course"],
            detail_rows,
            aligns=["r", "r", "r", "l"],
        )
        print()

    counts = {label: 0 for _, _, label, _ in TIERS}
    for ratio, *_ in rows:
        counts[tier_for(ratio)] += 1

    print("Tier summary")
    print()
    print("Columns:")
    print("  tier        - ratio range of svgs / slides")
    print("  count       - number of courses in the range")
    print("  description - what the range means in practice")
    print()
    summary_rows = [(label, counts[label], desc) for _, _, label, desc in TIERS]
    summary_rows.append(("total", len(rows), ""))
    print_table(
        ["tier", "count", "description"],
        summary_rows,
        aligns=["l", "r", "l"],
    )


if __name__ == "__main__":
    main()
