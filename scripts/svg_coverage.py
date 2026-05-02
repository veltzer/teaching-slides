#!/usr/bin/env python
"""Report SVG coverage per course, grouped into tiers.

For each course (a directory under marp/courses/<domain>/<course>/ that contains
*.md files), counts non-title SVG references in the markdown and computes the
ratio: svg_refs / md_files. Prints a tier-summary table and optionally per-course
detail with --detail.
"""
import argparse
import re
from pathlib import Path

SVG_REF = re.compile(r"svg/(?:courses|lectures)/[^)\s]+\.svg")
TITLE_SVG = re.compile(r"/title\.svg\b")

TIERS = [
    (0.00, 0.25, "<= 0.25", "under-illustrated; 1 SVG every 4+ slides"),
    (0.25, 0.30, "0.25-0.30", "low; could use more"),
    (0.30, 0.50, "0.30-0.50", "acceptable; could improve"),
    (0.50, 0.83, "0.50-0.83", "solid"),
    (0.83, 1.01, ">= 0.83", "feature-complete"),
]


def course_dirs(root: Path):
    """Yield directories that contain at least 2 markdown files (a real course)."""
    for course_dir in sorted(root.glob("courses/*/*/")):
        if not course_dir.is_dir():
            continue
        md_files = list(course_dir.glob("*.md"))
        if len(md_files) >= 2:
            yield course_dir, md_files


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


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--detail", action="store_true", help="list each course")
    p.add_argument("--root", default="marp", help="marp root (default: marp)")
    args = p.parse_args()

    rows = []
    for course_dir, md_files in course_dirs(Path(args.root)):
        md_count = len(md_files)
        svg_refs = svg_count(md_files)
        ratio = svg_refs / md_count
        rows.append((ratio, svg_refs, md_count, course_dir))

    rows.sort()

    if args.detail:
        for ratio, svgs, mds, path in rows:
            print(f"{ratio:.2f}  {svgs:3d}/{mds:<3d}  {path}")
        print()

    counts = {label: 0 for _, _, label, _ in TIERS}
    for ratio, *_ in rows:
        counts[tier_for(ratio)] += 1

    total = len(rows)
    print(f"{'Tier':<12} {'Count':>6}  Description")
    print(f"{'-' * 12} {'-' * 6}  {'-' * 40}")
    for _, _, label, desc in TIERS:
        print(f"{label:<12} {counts[label]:>6}  {desc}")
    print(f"{'-' * 12} {'-' * 6}")
    print(f"{'total':<12} {total:>6}")


if __name__ == "__main__":
    main()
