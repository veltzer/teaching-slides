#!/usr/bin/env python

"""
Shared SVG parsing, manipulation, and serialization library.

Uses lxml for tree operations (preserves comments, attribute order, blank
lines) and string-based defs replacement (deterministic formatting).

All SVG-editing scripts in this project MUST use this module. It ensures:

  1. Byte-identical output for the same logical content (idempotency).
  2. The <defs> block is always rebuilt from the palette YAML.
  3. Comments, blank lines, and attribute order are preserved.
  4. Files are only written when the output actually differs.

Typical usage:

    from svg_lib import SvgFile

    svg = SvgFile.load(path)
    for elem, parent in svg.content_elements("rect"):
        if needs_fix(elem):
            elem.set("fill", "url(#grad-primary)")
            svg.changed = True
    svg.save_if_changed()
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import yaml
from lxml import etree

SVG_NS = "http://www.w3.org/2000/svg"

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PALETTE = ROOT_DIR / "resources" / "palette_diagram.yaml"
INTRO_PALETTE = ROOT_DIR / "resources" / "palette_intro.yaml"

PALETTES: dict[str, Path] = {
    "regular": DEFAULT_PALETTE,
    "title": INTRO_PALETTE,
}

# Regex to match the full <defs>...</defs> block including surrounding whitespace.
_DEFS_BLOCK_RE = re.compile(
    r"[ \t]*<defs\b[^>]*>.*?</defs>[ \t]*\n?", re.DOTALL
)
_SVG_OPEN_RE = re.compile(r"(<svg\b[^>]*>)\n?")
_METADATA_BLOCK_RE = re.compile(
    r"[ \t]*<metadata\b[^>]*>.*?</metadata>[ \t]*\n?", re.DOTALL
)


# ── Palette loading ──

_palette_cache: dict[str, dict] = {}


def load_palette(palette_path: Path = DEFAULT_PALETTE) -> dict:
    key = str(palette_path)
    if key not in _palette_cache:
        _palette_cache[key] = yaml.safe_load(
            palette_path.read_text(encoding="utf-8")
        )
    return _palette_cache[key]


# ── Canonical defs string ──

def build_defs_string(palette_path: Path = DEFAULT_PALETTE) -> str:
    """Build the canonical <defs>...</defs> string from the palette YAML.

    This is the SINGLE SOURCE OF TRUTH for the defs block format.
    """
    data = load_palette(palette_path)
    lines: list[str] = []
    lines.append("  <defs>")

    lines.append('    <style id="palette-vars">')
    lines.append("      :root, svg {")
    for group in data.get("colors", {}).values():
        for name, hexval in group.items():
            lines.append(f"        --{name}: {hexval};")
    lines.append("      }")
    lines.append("    </style>")

    gradients = data.get("gradients", {})
    if gradients:
        lines.append("    <!-- Gradients -->")
        first = True
        for gid, gdata in gradients.items():
            if not first:
                lines.append("")
            first = False
            lines.append(
                f'    <linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            )
            for stop in gdata.get("stops", []):
                lines.append(
                    f'      <stop offset="{stop["offset"]}"'
                    f' stop-color="{stop["color"]}"/>'
                )
            lines.append("    </linearGradient>")

    filters = data.get("filters", {})
    if filters:
        lines.append("")
        lines.append("    <!-- Drop shadow -->")
        for fid, fdata in filters.items():
            lines.append(
                f'    <filter id="{fid}" x="-4%" y="-8%"'
                f' width="108%" height="124%">'
            )
            lines.append(
                f'      <feDropShadow dx="{fdata.get("dx", 0)}"'
                f' dy="{fdata.get("dy", 2)}"'
                f' stdDeviation="{fdata.get("stdDeviation", 3)}"'
                f' flood-color="{fdata.get("flood-color", "#00000022")}"/>'
            )
            lines.append("    </filter>")

    markers = data.get("markers", {})
    if markers:
        lines.append("")
        lines.append("    <!-- Arrow markers -->")
        for mid, mdata in markers.items():
            lines.append(
                f'    <marker id="{mid}"'
                f' markerWidth="{mdata.get("markerWidth", 10)}"'
                f' markerHeight="{mdata.get("markerHeight", 10)}"'
                f' refX="9" refY="5" orient="auto">'
            )
            lines.append(
                f'      <path d="M1,2 L9,5 L1,8 Z" fill="{mdata["fill"]}"/>'
            )
            lines.append("    </marker>")

    lines.append("  </defs>")
    return "\n".join(lines)


def build_metadata_string(svg_type: str = "regular") -> str:
    """Build the canonical <metadata> block declaring the SVG type."""
    return f"  <metadata>\n    <type>{svg_type}</type>\n  </metadata>"


def svg_type_from_tree(root) -> str:
    """Read <metadata><type> from an lxml tree. Returns 'regular' if absent."""
    ns = f"{{{SVG_NS}}}"
    for meta in root.iter(f"{ns}metadata", "metadata"):
        for child in meta:
            t = child.tag
            local = t.split("}", 1)[1] if "}" in t else t
            if local == "type" and child.text:
                return child.text.strip()
    return "regular"


def palette_for_type(svg_type: str) -> Path:
    """Return the palette path for a given SVG type."""
    return PALETTES.get(svg_type, DEFAULT_PALETTE)


# ── Helpers ──

def tag(elem) -> str:
    """Return local tag name, stripping namespace."""
    if callable(elem.tag):
        return ""  # comment
    t = elem.tag
    return t.split("}", 1)[1] if "}" in t else t


def is_comment(elem) -> bool:
    return callable(elem.tag)


# ── SvgFile ──

class SvgFile:
    """SVG file with lxml tree for element manipulation.

    Approach:
      - lxml parses the file and provides tree access for element queries
        and modifications (content_elements, set attrs, add/remove elements).
      - On serialize(), the tree is serialized by lxml (preserving comments,
        attribute order, whitespace), then the <defs> block is replaced with
        the canonical string version via regex.
      - This hybrid gives us: tree-level operations + deterministic defs +
        preserved formatting.
    """

    def __init__(self, path: Path, root: etree._Element,
                 original_text: str,
                 palette_path: Path = DEFAULT_PALETTE):
        self.path = path
        self.root = root
        self.changed = False
        self._original_text = original_text
        self._palette_path = palette_path
        self.svg_type = svg_type_from_tree(root)

    @classmethod
    def load(cls, path: Path,
             palette_path: Path | None = None) -> "SvgFile":
        text = path.read_text(encoding="utf-8")
        parser = etree.XMLParser(remove_blank_text=False)
        root = etree.fromstring(text.encode(), parser)
        if palette_path is None:
            palette_path = palette_for_type(svg_type_from_tree(root))
        return cls(path, root, text, palette_path)

    def content_elements(self, elem_tag: str | None = None):
        """Iterate (element, parent) pairs outside <defs>."""
        defs_set: set = set()
        for elem in self.root.iter():
            if is_comment(elem):
                continue
            if tag(elem) == "defs":
                for child in elem.iter():
                    defs_set.add(child)

        parent_map: dict = {}
        for parent in self.root.iter():
            if is_comment(parent):
                continue
            for child in parent:
                parent_map[child] = parent

        for elem in self.root.iter():
            if is_comment(elem):
                continue
            if elem in defs_set or elem is self.root:
                continue
            if elem_tag is None or tag(elem) == elem_tag:
                yield elem, parent_map.get(elem)

    def serialize(self) -> str:
        """Serialize the tree, then splice canonical metadata + defs.

        1. lxml serializes the tree (preserves content formatting).
        2. The <metadata> block is replaced/inserted with the canonical type.
        3. The <defs> block is replaced with the canonical string.
        4. Any legacy palette comment is removed.
        5. Root attrs (xmlns, viewBox, style) are ensured.
        """
        # Ensure root attributes on the tree before serialization
        vb = self.root.get("viewBox")
        if vb is None or " ".join(vb.split()) != "0 0 1280 720":
            self.root.set("viewBox", "0 0 1280 720")
        for attr in ("width", "height"):
            if attr in self.root.attrib:
                del self.root.attrib[attr]
        style = self.root.get("style", "")
        if "background" not in style:
            if style:
                self.root.set("style", f"background:var(--bg);{style}")
            else:
                self.root.set("style", "background:var(--bg)")

        # Serialize via lxml
        text = etree.tostring(
            self.root, pretty_print=True,
            xml_declaration=False, encoding="unicode",
        )
        if not text.endswith("\n"):
            text += "\n"

        # Splice canonical metadata
        meta_str = build_metadata_string(self.svg_type)

        if _METADATA_BLOCK_RE.search(text):
            text = _METADATA_BLOCK_RE.sub(meta_str + "\n", text, count=1)
        else:
            # Insert metadata after <svg> opening tag
            text = _SVG_OPEN_RE.sub(r"\1\n" + meta_str + "\n", text, count=1)

        # Splice canonical defs
        defs_str = build_defs_string(self._palette_path)

        if _DEFS_BLOCK_RE.search(text):
            text = _DEFS_BLOCK_RE.sub(defs_str + "\n", text, count=1)
        else:
            # Insert defs after metadata
            text = text.replace(
                meta_str + "\n",
                meta_str + "\n" + defs_str + "\n",
                1,
            )

        return text

    def save_if_changed(self) -> bool:
        new_text = self.serialize()
        if new_text == self._original_text:
            return False
        self.path.write_text(new_text, encoding="utf-8")
        self._original_text = new_text
        return True

    def save(self) -> None:
        new_text = self.serialize()
        self.path.write_text(new_text, encoding="utf-8")
        self._original_text = new_text


# ── Fit-to-slide logic (moved from fit_svg_to_slide.py) ──

USABLE_X0 = 40.0
USABLE_Y0 = 40.0
USABLE_X1 = 1240.0
USABLE_Y1 = 620.0
USABLE_W = USABLE_X1 - USABLE_X0  # 1200
USABLE_H = USABLE_Y1 - USABLE_Y0  # 580

_FLOAT_RE = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?')
_FIT_ELEM_RE = re.compile(
    r'<(rect|circle|ellipse|line|text|tspan|polygon|polyline|path)\b([^>]*?)(/?)>',
    re.IGNORECASE,
)
_FIT_DEFS_RE = re.compile(r'<defs\b.*?</defs>', re.DOTALL)
_FIT_ATTR_RE = re.compile(r'\b(?P<name>[\w-]+)="(?P<val>[^"]*)"')
_TRANSLATE_RE = re.compile(
    r'translate\s*\(\s*(-?[\d.]+)\s*[,\s]\s*(-?[\d.]+)?\s*\)'
)
_ANY_TRANSFORM_FN = re.compile(
    r'\b(translate|matrix|scale|rotate|skewX|skewY)\s*\('
)


def _parse_num(val: str | None) -> float | None:
    if val is None:
        return None
    m = _FLOAT_RE.match(val.strip())
    return float(m.group(0)) if m else None


def _fmt_num(v: float) -> str:
    if v != v:
        return "0"
    out = f"{v:.12f}".rstrip("0").rstrip(".")
    return out if out else "0"


def _element_bbox(
    elem_tag: str, attrs: dict[str, str]
) -> tuple[float, float, float, float] | None:
    elem_tag = elem_tag.lower()

    def num(name):
        return _parse_num(attrs.get(name))

    if elem_tag == "rect":
        x, y = num("x") or 0, num("y") or 0
        w, h = num("width") or 0, num("height") or 0
        return (x, y, x + w, y + h) if w > 0 and h > 0 else None
    if elem_tag == "circle":
        cx, cy, r = num("cx") or 0, num("cy") or 0, num("r") or 0
        return (cx - r, cy - r, cx + r, cy + r)
    if elem_tag == "ellipse":
        cx, cy = num("cx") or 0, num("cy") or 0
        rx, ry = num("rx") or 0, num("ry") or 0
        return (cx - rx, cy - ry, cx + rx, cy + ry)
    if elem_tag == "line":
        x1, y1 = num("x1") or 0, num("y1") or 0
        x2, y2 = num("x2") or 0, num("y2") or 0
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    if elem_tag in ("text", "tspan"):
        xa, ya = attrs.get("x"), attrs.get("y")
        if xa is None and ya is None:
            return None
        x = _parse_num(xa) if xa else 0
        y = _parse_num(ya) if ya else 0
        return (x, y, x, y) if x is not None and y is not None else None
    if elem_tag in ("polygon", "polyline"):
        nums = [float(m.group(0)) for m in _FLOAT_RE.finditer(attrs.get("points", ""))]
        if len(nums) < 2:
            return None
        return (min(nums[0::2]), min(nums[1::2]), max(nums[0::2]), max(nums[1::2]))
    if elem_tag == "path":
        nums = [float(m.group(0)) for m in _FLOAT_RE.finditer(attrs.get("d", ""))]
        if len(nums) < 2:
            return None
        return (min(nums[0::2]), min(nums[1::2]), max(nums[0::2]), max(nums[1::2]))
    return None


def _is_non_translate_transform(transform: str) -> bool:
    for m in _ANY_TRANSFORM_FN.finditer(transform):
        if m.group(1) != "translate":
            return True
    return False


def _translate_offset(transform_attr: str) -> tuple[float, float]:
    if not transform_attr:
        return (0.0, 0.0)
    m = _TRANSLATE_RE.search(transform_attr)
    if not m:
        return (0.0, 0.0)
    return (float(m.group(1)), float(m.group(2)) if m.group(2) else 0.0)


def compute_bbox(
    outside_defs: str,
) -> tuple[float, float, float, float] | None:
    """Compute axis-aligned bounding box of all drawing elements."""
    combined = re.compile(
        r'<g\b([^>]*?)(/?)>|</g\s*>|'
        r'<(rect|circle|ellipse|line|text|tspan|polygon|polyline|path)\b([^>]*?)(/?)>',
        re.DOTALL,
    )
    stack: list[tuple[float, float]] = [(0.0, 0.0)]
    mins_x, mins_y, maxs_x, maxs_y = [], [], [], []

    for m in combined.finditer(outside_defs):
        whole = m.group(0)
        if whole.startswith("<g"):
            g_attrs = m.group(1) or ""
            if m.group(2):
                continue
            tm = re.search(r'\btransform="([^"]*)"', g_attrs)
            dx, dy = _translate_offset(tm.group(1)) if tm else (0.0, 0.0)
            cx, cy = stack[-1]
            stack.append((cx + dx, cy + dy))
        elif whole.startswith("</g"):
            if len(stack) > 1:
                stack.pop()
        else:
            t = m.group(3)
            a_str = m.group(4) or ""
            attrs = {am.group("name"): am.group("val") for am in _FIT_ATTR_RE.finditer(a_str)}
            tm = re.search(r'\btransform="([^"]*)"', a_str)
            if tm and _is_non_translate_transform(tm.group(1)):
                continue
            edx, edy = _translate_offset(tm.group(1)) if tm else (0.0, 0.0)
            box = _element_bbox(t, attrs)
            if box is None:
                continue
            ox, oy = stack[-1]
            ox += edx
            oy += edy
            mins_x.append(box[0] + ox)
            mins_y.append(box[1] + oy)
            maxs_x.append(box[2] + ox)
            maxs_y.append(box[3] + oy)

    if not mins_x:
        return None

    def _snap(v: float) -> float:
        r = round(v)
        return float(r) if abs(v - r) < 1e-9 else v

    return (_snap(min(mins_x)), _snap(min(mins_y)),
            _snap(max(maxs_x)), _snap(max(maxs_y)))


def _transform_element(
    elem_tag: str, attrs_str: str,
    sx: float, sy: float, tx: float, ty: float,
) -> str:
    elem_tag = elem_tag.lower()
    tm = re.search(r'\btransform="([^"]*)"', attrs_str)
    if tm and _is_non_translate_transform(tm.group(1)):
        return attrs_str
    s_mean = math.sqrt(sx * sy) if sx > 0 and sy > 0 else max(sx, sy)

    def rewrite(name, fn):
        nonlocal attrs_str
        m = re.search(rf'\b{re.escape(name)}="([^"]*)"', attrs_str)
        if not m:
            return
        val = _parse_num(m.group(1))
        if val is None:
            return
        attrs_str = re.sub(rf'\b{re.escape(name)}="[^"]*"',
                           f'{name}="{_fmt_num(fn(val))}"', attrs_str, count=1)

    def ensure(name, default, fn):
        nonlocal attrs_str
        m = re.search(rf'\b{re.escape(name)}="([^"]*)"', attrs_str)
        if m is None:
            attrs_str = attrs_str.rstrip() + f' {name}="{_fmt_num(fn(default))}"'
            return
        val = _parse_num(m.group(1))
        if val is None:
            return
        attrs_str = re.sub(rf'\b{re.escape(name)}="[^"]*"',
                           f'{name}="{_fmt_num(fn(val))}"', attrs_str, count=1)

    if elem_tag == "rect":
        ensure("x", 0.0, lambda v: v * sx + tx)
        ensure("y", 0.0, lambda v: v * sy + ty)
        rewrite("width", lambda v: v * sx)
        rewrite("height", lambda v: v * sy)
        rewrite("rx", lambda v: v * s_mean)
        rewrite("ry", lambda v: v * s_mean)
    elif elem_tag == "circle":
        rewrite("cx", lambda v: v * sx + tx)
        rewrite("cy", lambda v: v * sy + ty)
        rewrite("r", lambda v: v * s_mean)
    elif elem_tag == "ellipse":
        rewrite("cx", lambda v: v * sx + tx)
        rewrite("cy", lambda v: v * sy + ty)
        rewrite("rx", lambda v: v * sx)
        rewrite("ry", lambda v: v * sy)
    elif elem_tag == "line":
        rewrite("x1", lambda v: v * sx + tx)
        rewrite("y1", lambda v: v * sy + ty)
        rewrite("x2", lambda v: v * sx + tx)
        rewrite("y2", lambda v: v * sy + ty)
    elif elem_tag in ("text", "tspan"):
        rewrite("x", lambda v: v * sx + tx)
        rewrite("y", lambda v: v * sy + ty)
        m = re.search(r'\bfont-size="([^"]*)"', attrs_str)
        if m:
            fs = _parse_num(m.group(1))
            if fs and fs > 0:
                attrs_str = re.sub(r'\bfont-size="[^"]*"',
                                   f'font-size="{_fmt_num(max(10, fs * s_mean))}"',
                                   attrs_str, count=1)
    elif elem_tag in ("polygon", "polyline"):
        m = re.search(r'\bpoints="([^"]*)"', attrs_str)
        if m:
            nums = [float(mm.group(0)) for mm in _FLOAT_RE.finditer(m.group(1))]
            new = []
            for i in range(0, len(nums) - 1, 2):
                new.extend([nums[i] * sx + tx, nums[i + 1] * sy + ty])
            pts = " ".join(f"{_fmt_num(a)},{_fmt_num(b)}" for a, b in zip(new[0::2], new[1::2]))
            attrs_str = re.sub(r'\bpoints="[^"]*"', f'points="{pts}"', attrs_str, count=1)
    elif elem_tag == "path":
        m = re.search(r'\bd="([^"]*)"', attrs_str)
        if m:
            tokens = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?', m.group(1))
            new_tokens = []
            is_x = True
            for t in tokens:
                if re.match(r'^[A-Za-z]$', t):
                    new_tokens.append(t)
                else:
                    v = float(t)
                    new_tokens.append(_fmt_num(v * sx + tx if is_x else v * sy + ty))
                    is_x = not is_x
            attrs_str = re.sub(r'\bd="[^"]*"', f'd="{" ".join(new_tokens)}"', attrs_str, count=1)
    return attrs_str


def _apply_fit_transform(
    segments: list[tuple[str, str]],
    sx: float, sy: float, tx: float, ty: float,
) -> list[tuple[str, str]]:
    out = []
    for seg_tag, chunk in segments:
        if seg_tag == "defs":
            out.append((seg_tag, chunk))
            continue

        def sub(m):
            return f"<{m.group(1)}{_transform_element(m.group(1), m.group(2), sx, sy, tx, ty)}{m.group(3)}>"

        out.append((seg_tag, _FIT_ELEM_RE.sub(sub, chunk)))
    return out


def fit_svg(content: str) -> tuple[str, dict]:
    """Fit SVG content to the usable area [40,1240]x[40,620].

    Returns (new_content, info_dict). If info contains "skipped", no
    modification was needed.
    """
    defs_matches = list(_FIT_DEFS_RE.finditer(content))
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

    outside_full = "".join(s for t, s in segments if t == "outside")
    bbox = compute_bbox(outside_full)
    if bbox is None:
        return content, {"skipped": "no drawing elements"}

    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0, y1 - y0
    if bw <= 0 or bh <= 0:
        return content, {"skipped": "zero-size bbox"}

    sx_ideal = USABLE_W / bw
    sy_ideal = USABLE_H / bh
    ratio = max(sx_ideal, sy_ideal) / min(sx_ideal, sy_ideal) if min(sx_ideal, sy_ideal) > 0 else 1
    has_circles = "<circle" in outside_full
    uniform = ratio > 1.5 and has_circles
    if uniform:
        s = min(sx_ideal, sy_ideal)
        tw, th = bw * s, bh * s
    else:
        tw, th = float(USABLE_W), float(USABLE_H)

    tx0 = USABLE_X0 + (USABLE_W - tw) / 2.0
    ty0 = USABLE_Y0 + (USABLE_H - th) / 2.0

    if x0 == tx0 and y0 == ty0 and bw == tw and bh == th:
        return content, {"skipped": "already exactly fitted"}

    cur = segments
    cx0, cy0, cw, ch = x0, y0, bw, bh
    first_sx = first_sy = None

    for _ in range(20):
        sx = tw / cw if cw else 1.0
        sy = th / ch if ch else 1.0
        if uniform:
            sx = sy = min(sx, sy)
        ttx = tx0 - cx0 * sx
        tty = ty0 - cy0 * sy
        if first_sx is None:
            first_sx, first_sy = sx, sy
        if abs(sx - 1) < 1e-15 and abs(sy - 1) < 1e-15 and abs(ttx) < 1e-15 and abs(tty) < 1e-15:
            break
        cur = _apply_fit_transform(cur, sx, sy, ttx, tty)
        new_out = "".join(s for t, s in cur if t == "outside")
        nb = compute_bbox(new_out)
        if nb is None:
            break
        cx0, cy0, nx1, ny1 = nb
        cw, ch = nx1 - cx0, ny1 - cy0
        if cx0 == tx0 and cy0 == ty0 and cw == tw and ch == th:
            break

    return "".join(s for _, s in cur), {
        "scale": (first_sx, first_sy),
        "final_bbox": (cx0, cy0, cx0 + cw, cy0 + ch),
    }
