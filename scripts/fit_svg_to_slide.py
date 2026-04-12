#!/usr/bin/env python
"""
Stretch SVG drawing content to fill the usable slide area exactly.

Every SVG ends up with its content occupying the same rectangle:
x in [40, 1240], y in [40, 620]. Aspect ratio is NOT preserved — the
content is stretched independently on x and y so every diagram fills the
same real estate.

viewBox stays at 1280x720 (we only transform the drawing elements).

Steps for each SVG:
  1. Compute the axis-aligned bounding box of all drawing elements.
  2. Compute sx = target_w / bbox_w, sy = target_h / bbox_h (independent).
  3. Translate the bbox to the origin, apply (sx, sy), then translate to
     the usable-area origin.
  4. Apply that affine transform to every drawing element's coordinates and
     sizes. Font-size scales by the geometric mean of sx and sy.

Circles: SVG <circle> has a single radius. We scale it by the geometric
mean of sx and sy — imperfect but reasonable. Authors should use <ellipse>
if they need true independent radii.

Elements handled: rect, circle, ellipse, line, text, tspan, polygon, polyline,
path (with the d= attribute parsed).

Elements inside <defs> are skipped.

Idempotent: re-running on a fitted SVG is a no-op (bbox already matches the
target rectangle).
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

USABLE_X0 = 40.0
USABLE_Y0 = 40.0
USABLE_X1 = 1240.0
USABLE_Y1 = 620.0
USABLE_W = USABLE_X1 - USABLE_X0  # 1200
USABLE_H = USABLE_Y1 - USABLE_Y0  # 580


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
        # Underestimate the y-extent of circles so that the fit doesn't
        # try to stretch huge circles vertically — the fit preserves circle
        # shape (geometric-mean radius), so a vertical stretch that doesn't
        # enlarge the circle would leave it overflowing. Using a smaller
        # bbox here lets the fit compute a reasonable sy that doesn't break
        # idempotency on subsequent runs.
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
        # A <tspan> without its own x/y inherits its parent <text>'s
        # position. Treating it as a point at (0, 0) would pull the bbox
        # minimum to the origin incorrectly. If no coordinates are given,
        # the element contributes nothing to the bbox.
        x_attr = attrs.get("x")
        y_attr = attrs.get("y")
        if x_attr is None and y_attr is None:
            return None
        x = _parse_num(x_attr) if x_attr is not None else 0
        y = _parse_num(y_attr) if y_attr is not None else 0
        if x is None or y is None:
            return None
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


_G_OPEN_RE = re.compile(r'<g\b([^>]*?)(/?)>', re.DOTALL)
_G_CLOSE_RE = re.compile(r'</g\s*>')
_TRANSLATE_RE = re.compile(r'translate\s*\(\s*(-?[\d.]+)\s*[,\s]\s*(-?[\d.]+)?\s*\)')
_ANY_TRANSFORM_FN = re.compile(r'\b(translate|matrix|scale|rotate|skewX|skewY)\s*\(')


def _is_non_translate_transform(transform: str) -> bool:
    """True if the transform string contains any function other than translate()."""
    for m in _ANY_TRANSFORM_FN.finditer(transform):
        if m.group(1) != "translate":
            return True
    return False


def _translate_offset(transform_attr: str) -> tuple[float, float]:
    """Extract the (dx, dy) of the first translate() in a transform attribute.
    Other transform functions (rotate, scale, matrix) are ignored — we only
    handle the common case of a plain translate() on a <g>."""
    if not transform_attr:
        return (0.0, 0.0)
    m = _TRANSLATE_RE.search(transform_attr)
    if not m:
        return (0.0, 0.0)
    dx = float(m.group(1))
    dy = float(m.group(2)) if m.group(2) is not None else 0.0
    return (dx, dy)


def compute_bbox(outside_defs: str) -> tuple[float, float, float, float] | None:
    """Return (x0, y0, x1, y1) of all drawing elements in the chunk.

    Walks tags in order. Maintains a stack of accumulated translate() offsets
    from enclosing <g transform="translate(...)"> elements. Elements with
    other transform types (rotate, scale, matrix) contribute their untransformed
    bbox — approximate but good enough for fit/center decisions.
    """
    # Combined token stream: <g openings, </g closes, and drawing elements.
    combined = re.compile(
        r'<g\b([^>]*?)(/?)>|</g\s*>|'
        r'<(rect|circle|ellipse|line|text|tspan|polygon|polyline|path)\b([^>]*?)(/?)>',
        re.DOTALL,
    )

    # Stack holds cumulative (dx, dy) after each open <g>
    stack: list[tuple[float, float]] = [(0.0, 0.0)]
    mins_x: list[float] = []
    mins_y: list[float] = []
    maxs_x: list[float] = []
    maxs_y: list[float] = []

    for m in combined.finditer(outside_defs):
        whole = m.group(0)
        if whole.startswith('<g'):
            g_attrs = m.group(1) or ""
            self_close = m.group(2)
            # Find transform attribute
            tm = re.search(r'\btransform="([^"]*)"', g_attrs)
            dx, dy = _translate_offset(tm.group(1)) if tm else (0.0, 0.0)
            cur_x, cur_y = stack[-1]
            new_offset = (cur_x + dx, cur_y + dy)
            if self_close:
                # <g .../> — no children, don't push
                continue
            stack.append(new_offset)
        elif whole.startswith('</g'):
            if len(stack) > 1:
                stack.pop()
        else:
            # Drawing element
            tag = m.group(3)
            attrs_str = m.group(4) or ""
            attrs = {am.group("name"): am.group("val") for am in _ATTR_RE.finditer(attrs_str)}
            # If the element has a non-trivial transform (anything other than
            # a pure translate()), skip it. Re-positioning without
            # understanding the transform corrupts the rendering.
            tm = re.search(r'\btransform="([^"]*)"', attrs_str)
            if tm is not None:
                t = tm.group(1).strip()
                if _is_non_translate_transform(t):
                    continue
                elem_dx, elem_dy = _translate_offset(t)
            else:
                elem_dx, elem_dy = 0.0, 0.0
            box = _element_bbox(tag, attrs)
            if box is None:
                continue
            x0, y0, x1, y1 = box
            off_x, off_y = stack[-1]
            off_x += elem_dx
            off_y += elem_dy
            mins_x.append(x0 + off_x)
            mins_y.append(y0 + off_y)
            maxs_x.append(x1 + off_x)
            maxs_y.append(y1 + off_y)

    if not mins_x:
        return None
    return (min(mins_x), min(mins_y), max(maxs_x), max(maxs_y))


# ------------------- Transform application -------------------

def _transform_point(x: float, y: float, sx: float, sy: float, tx: float, ty: float) -> tuple[float, float]:
    return (x * sx + tx, y * sy + ty)


def _transform_element(tag: str, attrs_str: str, sx: float, sy: float, tx: float, ty: float) -> str:
    tag = tag.lower()

    # If this element has a non-trivial own transform (scale/rotate/matrix/
    # skew), leave it alone — rewriting its coordinates without understanding
    # the transform corrupts its final position.
    tm = re.search(r'\btransform="([^"]*)"', attrs_str)
    if tm is not None and _is_non_translate_transform(tm.group(1)):
        return attrs_str

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

    # Geometric mean of sx and sy, for scalars that have no direction
    s_mean = math.sqrt(sx * sy) if sx > 0 and sy > 0 else max(sx, sy)

    def ensure_and_rewrite(name: str, default: float, transform_fn):
        """Like rewrite, but inserts the attribute with `default` transformed
        if it was missing. Matters for rect/line/circle/etc. where missing
        x/y means implicit 0."""
        nonlocal attrs_str
        m = re.search(rf'\b{re.escape(name)}="([^"]*)"', attrs_str)
        if m is None:
            attrs_str = attrs_str.rstrip() + f' {name}="{_fmt_num(transform_fn(default))}"'
            return
        val = _parse_num(m.group(1))
        if val is None:
            return
        attrs_str = re.sub(
            rf'\b{re.escape(name)}="[^"]*"',
            f'{name}="{_fmt_num(transform_fn(val))}"',
            attrs_str,
            count=1,
        )

    if tag == "rect":
        ensure_and_rewrite("x", 0.0, lambda v: v * sx + tx)
        ensure_and_rewrite("y", 0.0, lambda v: v * sy + ty)
        rewrite("width", lambda v: v * sx)
        rewrite("height", lambda v: v * sy)
        rewrite("rx", lambda v: v * s_mean)
        rewrite("ry", lambda v: v * s_mean)
    elif tag == "circle":
        rewrite("cx", lambda v: v * sx + tx)
        rewrite("cy", lambda v: v * sy + ty)
        rewrite("r", lambda v: v * s_mean)
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
        m = re.search(r'\bfont-size="([^"]*)"', attrs_str)
        if m:
            fs = _parse_num(m.group(1))
            if fs is not None and fs > 0:
                attrs_str = re.sub(
                    r'\bfont-size="[^"]*"',
                    f'font-size="{_fmt_num(max(10, fs * s_mean))}"',
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

    # Stretch to fill: independent x and y scales.
    sx = USABLE_W / bbox_w
    sy = USABLE_H / bbox_h
    # If the aspect-ratio stretch would be severe (>50% difference), fall
    # back to uniform scaling and center. Heavy stretching distorts circles
    # badly (SVG <circle> has only one radius) and breaks idempotency on
    # circle-heavy diagrams.
    ratio = max(sx, sy) / min(sx, sy) if min(sx, sy) > 0 else 1
    if ratio > 1.5:
        s = min(sx, sy)
        sx = s
        sy = s
    # Translate so scaled bbox lands in the usable area. When uniform, center
    # the content on the unused axis.
    new_w = bbox_w * sx
    new_h = bbox_h * sy
    tx = USABLE_X0 + (USABLE_W - new_w) / 2 - x0 * sx
    ty = USABLE_Y0 + (USABLE_H - new_h) / 2 - y0 * sy

    # Skip if the SVG is within 5% of a perfect fit in scale AND within
    # 2px in translation. Path bbox approximation can produce a few
    # pixels of scale drift even on well-fitted files, but translation
    # drift is a real off-center problem the user can see. The scale
    # tolerance keeps idempotency; the tight translation tolerance keeps
    # content centered.
    if abs(sx - 1.0) < 0.05 and abs(sy - 1.0) < 0.05 and abs(tx) < 2.0 and abs(ty) < 2.0:
        return content, {"skipped": "already exactly fitted"}

    info = {
        "bbox": bbox,
        "scale": (sx, sy),
        "translate": (tx, ty),
    }

    new_segments = []
    for tag, chunk in segments:
        if tag == "defs":
            new_segments.append(chunk)
            continue

        def sub(m: re.Match) -> str:
            inner_tag = m.group(1)
            attrs_str = m.group(2)
            self_close = m.group(3)
            new_attrs = _transform_element(inner_tag, attrs_str, sx, sy, tx, ty)
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
        sx, sy = info["scale"]
        if args.dry_run:
            print(f"would fit: {rel} sx={sx:.2f} sy={sy:.2f}")
        else:
            sp.write_text(new, encoding="utf-8")
            print(f"fitted:    {rel} sx={sx:.2f} sy={sy:.2f}")
        changed += 1

    print(f"\n{changed} fitted, {skipped} skipped, {len(svg_paths)} total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
