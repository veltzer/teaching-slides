#!/usr/bin/env python
"""
Fit SVG drawing content to fill the usable slide area.

Usable area: x in [40, 1240], y in [40, 620] — 1200 x 580 pixels.
viewBox stays at 1280x720 (we only transform the drawing elements).

For each SVG:
  1. Compute the axis-aligned bounding box of all drawing elements.
  2. If the bounding box already fills >= 80% of the usable area, skip.
  3. Otherwise compute a uniform scale = min(target_w / bbox_w, target_h / bbox_h),
     capped at MAX_SCALE to avoid wildly blowing up small icons.
  4. Translate the bbox to the origin, scale, then translate to center the
     result in the usable area.
  5. Apply that affine transform to every drawing element's coordinates and
     sizes, and scale font-size proportionally.

Elements handled: rect, circle, ellipse, line, text, tspan, polygon, polyline,
path (with the d= attribute parsed).

Elements inside <defs> are skipped.

Idempotent in practice (re-running on a fitted SVG is a near-no-op since it
already fills >=80% of usable area).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

USABLE_X0 = 40.0
USABLE_Y0 = 40.0
USABLE_X1 = 1240.0
USABLE_Y1 = 620.0
USABLE_W = USABLE_X1 - USABLE_X0  # 1200
USABLE_H = USABLE_Y1 - USABLE_Y0  # 580
MARGIN = 40.0
SKIP_FILL_RATIO = 0.80
MAX_SCALE = 2.0
MIN_SCALE = 1.0   # never shrink; only grow


# ------------------- Attribute helpers -------------------

_FLOAT_RE = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?')


def _parse_num(val: str | None) -> float | None:
    if val is None:
        return None
    m = _FLOAT_RE.match(val.strip())
    if not m:
        return None
    try:
        return float(m.group(0))
    except ValueError:
        return None


def _fmt_num(v: float) -> str:
    """Format without exponent notation, trim trailing zeros."""
    if v != v:  # NaN
        return "0"
    out = f"{v:.4f}".rstrip("0").rstrip(".")
    return out if out else "0"


# ------------------- Bounding box -------------------

_ELEM_RE = re.compile(
    r'<(rect|circle|ellipse|line|text|tspan|polygon|polyline|path)\b([^>]*?)(/?)>',
    re.IGNORECASE,
)
_DEFS_RE = re.compile(r'<defs\b.*?</defs>', re.DOTALL)
_ATTR_RE = re.compile(r'\b(?P<name>[\w-]+)="(?P<val>[^"]*)"')


def _element_bbox(tag: str, attrs: dict[str, str]) -> tuple[float, float, float, float] | None:
    """Return (x0, y0, x1, y1) for this element, or None if indeterminate."""
    tag = tag.lower()

    def num(name):
        return _parse_num(attrs.get(name))

    if tag == "rect":
        x = num("x") or 0
        y = num("y") or 0
        w = num("width") or 0
        h = num("height") or 0
        if w <= 0 or h <= 0:
            return None
        return (x, y, x + w, y + h)

    if tag in ("circle",):
        cx = num("cx") or 0
        cy = num("cy") or 0
        r = num("r") or 0
        return (cx - r, cy - r, cx + r, cy + r)

    if tag == "ellipse":
        cx = num("cx") or 0
        cy = num("cy") or 0
        rx = num("rx") or 0
        ry = num("ry") or 0
        return (cx - rx, cy - ry, cx + rx, cy + ry)

    if tag == "line":
        x1 = num("x1") or 0
        y1 = num("y1") or 0
        x2 = num("x2") or 0
        y2 = num("y2") or 0
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    if tag in ("text", "tspan"):
        x = num("x") or 0
        y = num("y") or 0
        # Approximate text extent is unknown from attrs; treat as a point.
        return (x, y, x, y)

    if tag in ("polygon", "polyline"):
        pts = attrs.get("points", "")
        nums = [float(m.group(0)) for m in _FLOAT_RE.finditer(pts)]
        if len(nums) < 2:
            return None
        xs = nums[0::2]
        ys = nums[1::2]
        if not xs or not ys:
            return None
        return (min(xs), min(ys), max(xs), max(ys))

    if tag == "path":
        d = attrs.get("d", "")
        nums = [float(m.group(0)) for m in _FLOAT_RE.finditer(d)]
        if len(nums) < 2:
            return None
        # Crude: treat every (n, n+1) as a coordinate pair. Works for paths
        # that use absolute Mx,y Lx,y etc. Over-estimates bbox for arcs/Bezier
        # control points, which is fine for fitting.
        xs = nums[0::2]
        ys = nums[1::2]
        return (min(xs), min(ys), max(xs), max(ys))

    return None


def compute_bbox(outside_defs: str) -> tuple[float, float, float, float] | None:
    mins_x = []
    mins_y = []
    maxs_x = []
    maxs_y = []
    for m in _ELEM_RE.finditer(outside_defs):
        tag = m.group(1)
        attrs_str = m.group(2)
        attrs = {am.group("name"): am.group("val") for am in _ATTR_RE.finditer(attrs_str)}
        box = _element_bbox(tag, attrs)
        if box is None:
            continue
        x0, y0, x1, y1 = box
        mins_x.append(x0)
        mins_y.append(y0)
        maxs_x.append(x1)
        maxs_y.append(y1)
    if not mins_x:
        return None
    return (min(mins_x), min(mins_y), max(maxs_x), max(maxs_y))


# ------------------- Transform application -------------------

def _transform_point(x: float, y: float, sx: float, sy: float, tx: float, ty: float) -> tuple[float, float]:
    return (x * sx + tx, y * sy + ty)


def _transform_element(tag: str, attrs_str: str, sx: float, sy: float, tx: float, ty: float) -> str:
    tag = tag.lower()

    def rewrite(name: str, transform_fn):
        nonlocal attrs_str
        m = re.search(rf'\b{re.escape(name)}="([^"]*)"', attrs_str)
        if not m:
            return
        val = _parse_num(m.group(1))
        if val is None:
            return
        new_val = transform_fn(val)
        attrs_str = re.sub(
            rf'\b{re.escape(name)}="[^"]*"',
            f'{name}="{_fmt_num(new_val)}"',
            attrs_str,
            count=1,
        )

    if tag == "rect":
        rewrite("x", lambda v: v * sx + tx)
        rewrite("y", lambda v: v * sy + ty)
        rewrite("width", lambda v: v * sx)
        rewrite("height", lambda v: v * sy)
        rewrite("rx", lambda v: v * sx)
        rewrite("ry", lambda v: v * sy)
    elif tag == "circle":
        rewrite("cx", lambda v: v * sx + tx)
        rewrite("cy", lambda v: v * sy + ty)
        rewrite("r", lambda v: v * sx)   # uniform sx == sy since we use same scale
    elif tag == "ellipse":
        rewrite("cx", lambda v: v * sx + tx)
        rewrite("cy", lambda v: v * sy + ty)
        rewrite("rx", lambda v: v * sx)
        rewrite("ry", lambda v: v * sy)
    elif tag == "line":
        rewrite("x1", lambda v: v * sx + tx)
        rewrite("y1", lambda v: v * sy + ty)
        rewrite("x2", lambda v: v * sx + tx)
        rewrite("y2", lambda v: v * sy + ty)
    elif tag in ("text", "tspan"):
        rewrite("x", lambda v: v * sx + tx)
        rewrite("y", lambda v: v * sy + ty)
        # Scale font-size
        m = re.search(r'\bfont-size="([^"]*)"', attrs_str)
        if m:
            fs = _parse_num(m.group(1))
            if fs is not None and fs > 0:
                attrs_str = re.sub(
                    r'\bfont-size="[^"]*"',
                    f'font-size="{_fmt_num(max(10, fs * sx))}"',
                    attrs_str,
                    count=1,
                )
    elif tag in ("polygon", "polyline"):
        m = re.search(r'\bpoints="([^"]*)"', attrs_str)
        if m:
            pts_str = m.group(1)
            nums = [float(mm.group(0)) for mm in _FLOAT_RE.finditer(pts_str)]
            new_nums = []
            for i in range(0, len(nums) - 1, 2):
                x, y = _transform_point(nums[i], nums[i + 1], sx, sy, tx, ty)
                new_nums.extend([x, y])
            new_pts = " ".join(f"{_fmt_num(a)},{_fmt_num(b)}" for a, b in zip(new_nums[0::2], new_nums[1::2]))
            attrs_str = re.sub(r'\bpoints="[^"]*"', f'points="{new_pts}"', attrs_str, count=1)
    elif tag == "path":
        m = re.search(r'\bd="([^"]*)"', attrs_str)
        if m:
            d = m.group(1)
            # Walk through: preserve command letters, transform number pairs
            # by alternating x/y. Approximate for H/V/A commands but usually
            # close enough since we only use this to rescale, not to parse
            # paths semantically.
            tokens = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?', d)
            new_tokens = []
            is_x = True
            for t in tokens:
                if re.match(r'^[MmLlHhVvCcSsQqTtAaZz]$', t):
                    new_tokens.append(t)
                    # After a relative command, still alternate — this is crude
                else:
                    v = float(t)
                    if is_x:
                        new_tokens.append(_fmt_num(v * sx + tx))
                    else:
                        new_tokens.append(_fmt_num(v * sy + ty))
                    is_x = not is_x
            # Reassemble with spaces
            attrs_str = re.sub(r'\bd="[^"]*"', f'd="{" ".join(new_tokens)}"', attrs_str, count=1)

    return attrs_str


# ------------------- Main fitting logic -------------------

def fit_svg(content: str) -> tuple[str, dict]:
    """Return (new_content, info)."""
    defs_matches = list(_DEFS_RE.finditer(content))
    if defs_matches:
        segments = []
        last = 0
        for m in defs_matches:
            segments.append(("outside", content[last:m.start()]))
            segments.append(("defs", content[m.start():m.end()]))
            last = m.end()
        segments.append(("outside", content[last:]))
    else:
        segments = [("outside", content)]

    # Compute bbox across all outside-defs chunks
    outside_full = "".join(s for tag, s in segments if tag == "outside")
    bbox = compute_bbox(outside_full)
    if bbox is None:
        return content, {"skipped": "no drawing elements"}

    x0, y0, x1, y1 = bbox
    bbox_w = x1 - x0
    bbox_h = y1 - y0
    if bbox_w <= 0 or bbox_h <= 0:
        return content, {"skipped": "zero-size bbox"}

    fill_ratio = (bbox_w * bbox_h) / (USABLE_W * USABLE_H)
    if fill_ratio >= SKIP_FILL_RATIO:
        return content, {"skipped": f"already fills {fill_ratio:.0%}"}

    target_w = USABLE_W - 2 * MARGIN
    target_h = USABLE_H - 2 * MARGIN
    scale = min(target_w / bbox_w, target_h / bbox_h)
    if scale < MIN_SCALE:
        return content, {"skipped": f"scale {scale:.2f} below min"}
    scale = min(scale, MAX_SCALE)

    # After scaling, bbox has size (bbox_w*scale, bbox_h*scale). Center in usable area.
    new_w = bbox_w * scale
    new_h = bbox_h * scale
    # The scaled bbox starts at (x0*scale, y0*scale). Translate so it starts at
    # (USABLE_X0 + (USABLE_W - new_w)/2, ...).
    center_x = USABLE_X0 + (USABLE_W - new_w) / 2
    center_y = USABLE_Y0 + (USABLE_H - new_h) / 2
    tx = center_x - x0 * scale
    ty = center_y - y0 * scale

    info = {
        "bbox": bbox,
        "scale": scale,
        "translate": (tx, ty),
        "fill_ratio": fill_ratio,
    }

    # Rewrite every element in outside segments
    new_segments = []
    for tag, chunk in segments:
        if tag == "defs":
            new_segments.append(chunk)
            continue

        def sub(m: re.Match) -> str:
            inner_tag = m.group(1)
            attrs_str = m.group(2)
            self_close = m.group(3)
            new_attrs = _transform_element(inner_tag, attrs_str, scale, scale, tx, ty)
            return f"<{inner_tag}{new_attrs}{self_close}>"

        new_segments.append(_ELEM_RE.sub(sub, chunk))

    return "".join(new_segments), info


def fit_file(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    new, info = fit_svg(content)
    if "skipped" in info:
        return info
    path.write_text(new, encoding="utf-8")
    return info


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="*", help="Files or directories")
    p.add_argument("--dry-run", action="store_true", help="Show what would change, don't write")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    if not args.paths:
        svg_paths = sorted((repo_root / "svg").rglob("*.svg"))
    else:
        svg_paths = []
        for p in args.paths:
            pp = Path(p)
            if pp.is_dir():
                svg_paths.extend(sorted(pp.rglob("*.svg")))
            else:
                svg_paths.append(pp)

    changed = 0
    skipped = 0
    for sp in svg_paths:
        content = sp.read_text(encoding="utf-8")
        new, info = fit_svg(content)
        if "skipped" in info:
            skipped += 1
            continue
        try:
            rel = sp.relative_to(repo_root)
        except ValueError:
            rel = sp
        if args.dry_run:
            print(f"would fit: {rel} scale={info['scale']:.2f}")
        else:
            sp.write_text(new, encoding="utf-8")
            print(f"fitted:    {rel} scale={info['scale']:.2f}")
        changed += 1

    print(f"\n{changed} fitted, {skipped} skipped, {len(svg_paths)} total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
