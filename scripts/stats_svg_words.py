#!/usr/bin/env python
"""
Report word-count statistics for SVG diagrams.

Counts words from <text> and <tspan> elements outside <defs>.
Useful to decide the word-count limit for the check_svg.py enforcer.

Usage:
    scripts/stats_svg_words.py             # histogram + top 20 offenders
    scripts/stats_svg_words.py --list 50   # list top 50 by word count
    scripts/stats_svg_words.py --over 30   # list every SVG with > 30 words
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_TEXT_RE = re.compile(r'<(?:text|tspan)[^>]*?>(.*?)</(?:text|tspan)>', re.DOTALL)
_DEFS_RE = re.compile(r'<defs\b.*?</defs>', re.DOTALL)
_TAG_RE = re.compile(r'<[^>]+>')
_WORD_RE = re.compile(r"[A-Za-z0-9_.@#+\-/()'\"]+")


def count_words(path: Path) -> int:
    content = path.read_text(encoding="utf-8", errors="replace")
    outside = _DEFS_RE.sub('', content)
    total = 0
    for m in _TEXT_RE.finditer(outside):
        plain = _TAG_RE.sub(' ', m.group(1))
        total += len(_WORD_RE.findall(plain))
    return total


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--list", type=int, default=20, help="show top N by word count")
    p.add_argument("--over", type=int, default=None, help="list every SVG with > N words")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    svg_root = repo_root / "svg"

    counts: list[tuple[int, Path]] = []
    for path in sorted(svg_root.rglob("*.svg")):
        n = count_words(path)
        counts.append((n, path))

    counts.sort(reverse=True)
    total_svgs = len(counts)
    if total_svgs == 0:
        print("no svgs found")
        return 0

    nums = [n for n, _ in counts]
    nums_sorted = sorted(nums)
    mean = sum(nums) / total_svgs
    median = nums_sorted[total_svgs // 2]
    p90 = nums_sorted[int(total_svgs * 0.90)]
    p95 = nums_sorted[int(total_svgs * 0.95)]
    p99 = nums_sorted[int(total_svgs * 0.99)]

    print(f"total SVGs: {total_svgs}")
    print(f"word count — mean: {mean:.1f}  median: {median}  p90: {p90}  p95: {p95}  p99: {p99}  max: {nums[0]}")
    print()

    # Histogram
    buckets = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 60), (60, 80), (80, 120), (120, 200), (200, 10**9)]
    print("Histogram of words per SVG:")
    for lo, hi in buckets:
        hi_label = "inf" if hi > 10**6 else str(hi)
        count = sum(1 for n in nums if lo <= n < hi)
        pct = 100 * count / total_svgs
        bar = "#" * int(pct)
        print(f"  [{lo:4d}..{hi_label:>4}): {count:5d}  {pct:5.1f}%  {bar}")
    print()

    if args.over is not None:
        over = [(n, path) for n, path in counts if n > args.over]
        print(f"SVGs with > {args.over} words: {len(over)}")
        for n, path in over[:200]:
            print(f"  {n:4d}  {path.relative_to(repo_root)}")
        if len(over) > 200:
            print(f"  ... {len(over) - 200} more")
    else:
        print(f"Top {args.list} by word count:")
        for n, path in counts[:args.list]:
            print(f"  {n:4d}  {path.relative_to(repo_root)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
