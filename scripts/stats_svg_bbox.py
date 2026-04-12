#!/usr/bin/env python
"""
Report bounding-box and centering statistics for every SVG under svg/.

For each SVG the script computes the axis-aligned bbox of its drawing
elements (using the same logic as fit_svg_to_slide.py) and reports:

  - bbox width and height
  - fill ratio: how much of the 1200x580 usable area the content occupies
  - horizontal centering: signed offset of content center from viewBox
    horizontal center (x=640). Negative = shifted LEFT, positive = RIGHT.
  - vertical centering: signed offset from y=360. Negative = UP, positive = DOWN.

Summary output: histograms and top offenders.

Usage:
    scripts/stats_svg_bbox.py                # summary only
    scripts/stats_svg_bbox.py --all          # per-file rows + summary
    scripts/stats_svg_bbox.py --off-h 5      # list files with horizontal asym > 5px
    scripts/stats_svg_bbox.py --off-v 5      # list files with vertical asym > 5px
    scripts/stats_svg_bbox.py --fill-below 50  # list files whose content fills < 50% of slide
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fit_svg_to_slide as fit  # noqa: E402

USABLE_W = 1200.0
USABLE_H = 580.0
USABLE_AREA = USABLE_W * USABLE_H
# "Center" = center of the USABLE area (where fit_svg_to_slide targets),
# not the center of the raw viewBox. The usable area is x=[40, 1240],
# y=[40, 620] → center = (640, 330). Measuring against the viewBox center
# (640, 360) would show a spurious ~30px vertical offset on every SVG.
CENTER_X = 640.0
CENTER_Y = 330.0


def analyze(path: Path) -> dict | None:
    content = path.read_text(encoding="utf-8", errors="replace")
    outside = re.sub(r'<defs\b.*?</defs>', '', content, flags=re.DOTALL)
    bbox = fit.compute_bbox(outside)
    if bbox is None:
        return None
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0
    area = max(0.0, w) * max(0.0, h)
    fill_pct = 100 * area / USABLE_AREA
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    return {
        "path": path,
        "bbox": bbox,
        "w": w,
        "h": h,
        "fill_pct": fill_pct,
        "dx": cx - CENTER_X,
        "dy": cy - CENTER_Y,
    }


def histogram(values: list[float], buckets: list[tuple[float, float]], label_fmt) -> None:
    total = len(values)
    if total == 0:
        return
    for lo, hi in buckets:
        n = sum(1 for v in values if lo <= v < hi)
        pct = 100 * n / total
        bar = "#" * int(pct * 0.5)
        lbl = label_fmt(lo, hi)
        print(f"  {lbl:22s}: {n:5d}  {pct:5.1f}%  {bar}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    ap.add_argument("--all", action="store_true", help="list every SVG")
    ap.add_argument("--off-h", type=float, default=None,
                    help="list files where horizontal offset > N px")
    ap.add_argument("--off-v", type=float, default=None,
                    help="list files where vertical offset > N px")
    ap.add_argument("--fill-below", type=float, default=None,
                    help="list files whose content fills < N%% of usable area")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    svg_root = repo_root / "svg"

    results: list[dict] = []
    no_bbox = 0
    for p in sorted(svg_root.rglob("*.svg")):
        r = analyze(p)
        if r is None:
            no_bbox += 1
            continue
        results.append(r)

    total = len(results)
    if total == 0:
        print("no SVGs analyzed")
        return 0

    widths = [r["w"] for r in results]
    heights = [r["h"] for r in results]
    fills = [r["fill_pct"] for r in results]
    dx_abs = [abs(r["dx"]) for r in results]
    dy_abs = [abs(r["dy"]) for r in results]

    def pct(xs: list[float], p: float) -> float:
        xs = sorted(xs)
        return xs[min(len(xs) - 1, int(len(xs) * p))]

    print(f"Analyzed {total} SVGs  ({no_bbox} had no bbox)")
    print()
    print(f"Bbox width  — mean: {sum(widths) / total:7.1f}  median: {pct(widths, 0.5):7.1f}  p95: {pct(widths, 0.95):7.1f}  max: {max(widths):7.1f}")
    print(f"Bbox height — mean: {sum(heights) / total:7.1f}  median: {pct(heights, 0.5):7.1f}  p95: {pct(heights, 0.95):7.1f}  max: {max(heights):7.1f}")
    print(f"Fill %      — mean: {sum(fills) / total:6.1f}%  median: {pct(fills, 0.5):6.1f}%  p10: {pct(fills, 0.10):6.1f}%  min: {min(fills):6.1f}%")
    print(f"|dx|        — mean: {sum(dx_abs) / total:6.2f}  median: {pct(dx_abs, 0.5):6.2f}  p95: {pct(dx_abs, 0.95):6.2f}  max: {max(dx_abs):6.2f}")
    print(f"|dy|        — mean: {sum(dy_abs) / total:6.2f}  median: {pct(dy_abs, 0.5):6.2f}  p95: {pct(dy_abs, 0.95):6.2f}  max: {max(dy_abs):6.2f}")
    print()

    print(f"Horizontal centering (|dx| from usable-area center x={int(CENTER_X)}):")
    histogram(dx_abs,
              [(0, 2), (2, 10), (10, 30), (30, 100), (100, 10**9)],
              lambda lo, hi: f"|dx| [{int(lo):3d}..{('inf' if hi > 1e6 else str(int(hi))):>3s})")
    print()
    print(f"Vertical centering (|dy| from usable-area center y={int(CENTER_Y)}):")
    histogram(dy_abs,
              [(0, 2), (2, 10), (10, 30), (30, 100), (100, 10**9)],
              lambda lo, hi: f"|dy| [{int(lo):3d}..{('inf' if hi > 1e6 else str(int(hi))):>3s})")
    print()
    print("Fill ratio (content area / 1200x580 usable area):")
    histogram(fills,
              [(0, 10), (10, 25), (25, 50), (50, 75), (75, 90), (90, 101)],
              lambda lo, hi: f"fill [{int(lo):3d}..{int(hi):3d}%)")
    print()

    def show(rows: list[dict], label: str) -> None:
        print(f"{label} ({len(rows)}):")
        for r in rows[:30]:
            rel = r["path"].relative_to(repo_root)
            print(f"  dx={r['dx']:+7.1f}  dy={r['dy']:+7.1f}  fill={r['fill_pct']:5.1f}%  {rel}")
        if len(rows) > 30:
            print(f"  ... {len(rows) - 30} more")
        print()

    if args.off_h is not None:
        rows = sorted((r for r in results if abs(r["dx"]) > args.off_h),
                      key=lambda r: -abs(r["dx"]))
        show(rows, f"Horizontal offset > {args.off_h}px")

    if args.off_v is not None:
        rows = sorted((r for r in results if abs(r["dy"]) > args.off_v),
                      key=lambda r: -abs(r["dy"]))
        show(rows, f"Vertical offset > {args.off_v}px")

    if args.fill_below is not None:
        rows = sorted((r for r in results if r["fill_pct"] < args.fill_below),
                      key=lambda r: r["fill_pct"])
        show(rows, f"Fill < {args.fill_below}%")

    if args.all:
        print("All SVGs:")
        for r in sorted(results, key=lambda r: str(r["path"])):
            rel = r["path"].relative_to(repo_root)
            print(f"  w={r['w']:6.1f} h={r['h']:6.1f} fill={r['fill_pct']:5.1f}% dx={r['dx']:+6.1f} dy={r['dy']:+6.1f}  {rel}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
