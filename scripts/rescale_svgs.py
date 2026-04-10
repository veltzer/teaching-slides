#!/usr/bin/env python

"""
Rescale all SVG files to natively use viewBox="0 0 1280 720".

For each SVG:
1. Reads the original file from git HEAD to get the original dimensions.
2. Computes sx = 1280/orig_w, sy = 720/orig_h.
3. Rewrites all coordinate/size attributes in every element so the content
   fills 1280x720 natively — no transform wrappers.

Attributes scaled by sx (horizontal): x, cx, x1, x2, width, refX, markerWidth
Attributes scaled by sy (vertical):   y, cy, y1, y2, height, refY, markerHeight
Attributes scaled by min(sx,sy):       r, rx, ry, font-size, stroke-width
Path data (d) and points: each coordinate pair scaled by (sx, sy).
"""

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TARGET_W = 1280
TARGET_H = 720

# Attributes scaled only horizontally
X_ATTRS = {"x", "cx", "x1", "x2", "refX", "markerWidth"}
# Attributes scaled only vertically
Y_ATTRS = {"y", "cy", "y1", "y2", "refY", "markerHeight"}
# Attributes scaled by min(sx, sy) — uniform scale
U_ATTRS = {"r", "rx", "ry", "font-size", "stroke-width", "stroke-dasharray",
           "markerUnits"}


def get_original_dims(path: Path) -> tuple[float, float] | None:
    """Return (width, height) from git HEAD version of the file."""
    try:
        original = subprocess.check_output(
            ["git", "show", f"HEAD:{path}"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8", errors="replace")
    except subprocess.CalledProcessError:
        return None

    # Try viewBox first
    m = re.search(r'viewBox="(-?[\d.]+)\s+(-?[\d.]+)\s+([\d.]+)\s+([\d.]+)"', original)
    if m:
        return float(m.group(3)), float(m.group(4))

    # Fall back to width/height attributes
    mw = re.search(r'\bwidth="([\d.]+)"', original)
    mh = re.search(r'\bheight="([\d.]+)"', original)
    if mw and mh:
        return float(mw.group(1)), float(mh.group(1))

    return None


def scale_number(val: str, factor: float) -> str:
    """Scale a numeric string by factor, preserving units if present."""
    val = val.strip()
    # Handle px/pt/em suffix
    m = re.match(r'^(-?[\d.]+)(px|pt|em|%)?$', val)
    if not m:
        return val
    unit = m.group(2) or ""
    if unit == '%':
        return val
    num = float(m.group(1)) * factor
    # Format cleanly
    if num == int(num):
        return f"{int(num)}{unit}"
    return f"{num:.4f}".rstrip("0").rstrip(".") + unit


def scale_dasharray(val: str, factor: float) -> str:
    """Scale a stroke-dasharray value (space or comma separated numbers)."""
    parts = re.split(r'[\s,]+', val.strip())
    scaled = []
    for p in parts:
        try:
            scaled.append(scale_number(p, factor))
        except Exception:
            scaled.append(p)
    return " ".join(scaled)


def scale_points(val: str, sx: float, sy: float) -> str:
    """Scale SVG points attribute: 'x1,y1 x2,y2 ...'"""
    result = []
    for pair in re.finditer(r'(-?[\d.]+)\s*,\s*(-?[\d.]+)', val):
        nx = float(pair.group(1)) * sx
        ny = float(pair.group(2)) * sy
        nx_s = f"{int(nx)}" if nx == int(nx) else f"{nx:.4f}".rstrip("0").rstrip(".")
        ny_s = f"{int(ny)}" if ny == int(ny) else f"{ny:.4f}".rstrip("0").rstrip(".")
        result.append(f"{nx_s},{ny_s}")
    return " ".join(result)


def scale_path_d(val: str, sx: float, sy: float) -> str:
    """Scale SVG path d attribute coordinate values."""
    # Tokenise the path into commands and numbers
    tokens = re.findall(r'[MmZzLlHhVvCcSsQqTtAa]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', val)

    result = []
    cmd = None
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if re.match(r'^[MmZzLlHhVvCcSsQqTtAa]$', t):
            cmd = t
            result.append(t)
            i += 1
            continue

        # Number — scale based on current command context
        if cmd in ('H', 'h'):
            result.append(scale_number(t, sx))
        elif cmd in ('V', 'v'):
            result.append(scale_number(t, sy))
        elif cmd in ('Z', 'z'):
            result.append(t)
        elif cmd in ('A', 'a'):
            # arc: rx ry x-rotation large-arc-flag sweep-flag x y (7 params)
            # rx, ry: uniform; x-rotation, flags: unchanged; x: sx, y: sy
            arc_params = [t]
            while len(arc_params) < 7 and i + 1 < len(tokens) and not re.match(r'^[MmZzLlHhVvCcSsQqTtAa]$', tokens[i+1]):
                i += 1
                arc_params.append(tokens[i])
            if len(arc_params) == 7:
                su = min(sx, sy)
                scaled_arc = [
                    scale_number(arc_params[0], su),   # rx
                    scale_number(arc_params[1], su),   # ry
                    arc_params[2],                      # x-rotation (angle)
                    arc_params[3],                      # large-arc-flag
                    arc_params[4],                      # sweep-flag
                    scale_number(arc_params[5], sx),   # x
                    scale_number(arc_params[6], sy),   # y
                ]
                result.extend(scaled_arc)
            else:
                result.extend(arc_params)
            i += 1
            continue
        else:
            # Default: alternate x/y scaling
            # Simple heuristic: track index within current command
            if not hasattr(scale_path_d, '_cmd_count'):
                scale_path_d._cmd_count = 0
            # Just alternate sx/sy
            if scale_path_d._cmd_count % 2 == 0:
                result.append(scale_number(t, sx))
            else:
                result.append(scale_number(t, sy))
            scale_path_d._cmd_count += 1
            i += 1
            continue
        i += 1

    return " ".join(result)


def scale_element(elem: ET.Element, sx: float, sy: float, su: float) -> None:
    """Scale all coordinate/size attributes of one element."""
    tag = elem.tag.split("}")[-1]
    if tag in ("linearGradient", "radialGradient", "filter", "marker"):
        # Attributes in these are typically objectBoundingBox relative or percentages
        # Markers might need scaling but usually they are relative to stroke width
        # Let's be safe and not scale them unless they use userSpaceOnUse.
        # But wait, markerWidth/Height on <marker> might need scaling?
        # Let's just exclude gradients and filters
        pass
    if tag in ("linearGradient", "radialGradient", "filter"):
        # We should NOT scale x1, y1, x2, y2, cx, cy, r on gradients
        # as they are relative to bounding box.
        return
        
    for attr, val in list(elem.attrib.items()):
        local = attr.split("}")[-1]  # strip namespace

        if local in X_ATTRS:
            elem.set(attr, scale_number(val, sx))
        elif local in Y_ATTRS:
            elem.set(attr, scale_number(val, sy))
        elif local == "font-size" or local == "stroke-width":
            elem.set(attr, scale_number(val, su))
        elif local == "stroke-dasharray":
            elem.set(attr, scale_dasharray(val, su))
        elif local in {"r", "rx", "ry"}:
            elem.set(attr, scale_number(val, su))
        elif local == "points":
            elem.set(attr, scale_points(val, sx, sy))
        elif local == "d":
            scale_path_d._cmd_count = 0
            elem.set(attr, scale_path_d(val, sx, sy))
        elif local == "width":
            # width on root svg is handled separately; on others scale
            elem.set(attr, scale_number(val, sx))
        elif local == "height":
            elem.set(attr, scale_number(val, sy))

    # Also handle style attribute for font-size and stroke-width
    style = elem.get("style", "")
    if style:
        def scale_style_prop(m):
            prop = m.group(1)
            val = m.group(2)
            if prop in ("font-size", "stroke-width"):
                return f"{prop}:{scale_number(val, su)}"
            return m.group(0)
        new_style = re.sub(r'(font-size|stroke-width):\s*([\d.]+(?:px|pt|em)?)', scale_style_prop, style)
        elem.set("style", new_style)


def walk_and_scale(elem: ET.Element, sx: float, sy: float, su: float) -> None:
    tag = elem.tag.split("}")[-1]
    if tag in ("linearGradient", "radialGradient", "filter", "marker", "pattern"):
        return
    scale_element(elem, sx, sy, su)
    for child in elem:
        walk_and_scale(child, sx, sy, su)

def rescale_svg(path: Path, orig_w: float, orig_h: float) -> bool:
    """Rescale SVG content to 1280x720 natively. Return True if modified."""
    if orig_w == 0 or orig_h == 0:
        return False

    sx = TARGET_W / orig_w
    sy = TARGET_H / orig_h
    su = min(sx, sy)

    # Check if already at target (no scaling needed)
    if abs(sx - 1.0) < 0.001 and abs(sy - 1.0) < 0.001:
        return False

    content = path.read_text(encoding="utf-8")

    # Register all namespaces to avoid ns0: prefixes
    namespaces = dict(re.findall(r'xmlns(?::(\w+))?="([^"]+)"', content))
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix or "", uri)

    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return False

    root = tree.getroot()

    # Set the target viewBox on root, remove width/height attrs
    root.set("viewBox", f"0 0 {TARGET_W} {TARGET_H}")
    root.attrib.pop("width", None)
    root.attrib.pop("height", None)

    # Scale all elements recursively, skipping defs
    for child in root:
        walk_and_scale(child, sx, sy, su)
        
    # Scale root itself (excluding viewBox, handled in scale_element safely)
    for attr in list(root.attrib):
        local = attr.split("}")[-1]
        if local not in ("viewBox", "xmlns", "width", "height") and not local.startswith("xmlns"):
            # A bit hacky but we just temporarily swap attributes to scale them on root
            pass # Actually, it's safer to just run scale_element on root
    scale_element(root, sx, sy, su)

    # Write back preserving declaration
    ET.indent(tree, space="  ")
    tree.write(str(path), encoding="unicode", xml_declaration=False)

    # Restore <?xml ...?> if it was there and ensure svg xmlns
    new_content = path.read_text(encoding="utf-8")
    if not new_content.startswith("<svg") and not new_content.startswith("<?"):
        pass
    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    if not Path(".git").exists():
        print("ERROR: run from project root", file=sys.stderr)
        sys.exit(1)

    svg_root = Path("svg")
    files = sorted(svg_root.rglob("*.svg"))

    modified = 0
    skipped = 0
    errors = 0

    for f in files:
        dims = get_original_dims(f)
        if dims is None:
            print(f"SKIP (no original dims): {f}")
            skipped += 1
            continue

        orig_w, orig_h = dims
        if orig_w == TARGET_W and orig_h == TARGET_H:
            skipped += 1
            continue

        try:
            if rescale_svg(f, orig_w, orig_h):
                modified += 1
                print(f"scaled ({orig_w}x{orig_h} -> {TARGET_W}x{TARGET_H}): {f}")
            else:
                skipped += 1
        except Exception as e:
            print(f"ERROR {f}: {e}", file=sys.stderr)
            errors += 1

    print(f"\nDone: {modified} rescaled, {skipped} skipped, {errors} errors.")


if __name__ == "__main__":
    main()
