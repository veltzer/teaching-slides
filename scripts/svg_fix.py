#!/usr/bin/env python
# IMPORTANT: This script MUST be idempotent. Running it twice on the same
# file must produce identical output. If you modify this script, verify
# idempotency by running it on the full repo twice and confirming zero
# files change on the second run.

"""
Unified SVG fixer.  Replaces all individual svg_fix_*.py scripts.

Every fix operates on the lxml element tree via svg_lib.SvgFile.
The tree is serialized deterministically and written only if the output
differs from the original file.

Fixes:
  --fonts          Normalize font-family on <text>/<tspan>
  --gradients      Switch family-fill rects between solid/gradient per palette
  --shadows        Add/strip filter="url(#shadow)" per palette policy
  --markers        Rewrite custom arrow markers to canonical palette markers
  --no-circles     Convert <circle> to centered rounded <rect>
  --no-background  Strip full-slide background rects
  --root-bg        Ensure root <svg> has style="background:var(--bg)"
  --aspect-ratio   Ensure viewBox="0 0 1280 720", strip width/height
  --text-fill      Ensure every <text>/<tspan> has an explicit fill
  --tag-placeholders  Mark placeholder SVGs with PLACEHOLDERSVG comment
  --fit            Fit content to [40,1240]x[40,620] usable area

Running with no flags applies ALL fixes.

Usage:
    svg_fix.py svg/**/*.svg              # all fixes on all SVGs
    svg_fix.py --fonts --shadows FILE    # specific fixes
    svg_fix.py --dry-run svg/**/*.svg    # report what would change
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lxml import etree

from svg_lib import (
    SvgFile, load_palette, tag, is_comment, fit_svg,
)

_palette_cache: dict | None = None


def _palette() -> dict:
    global _palette_cache
    if _palette_cache is None:
        _palette_cache = load_palette()
    return _palette_cache


# ── Fix: fonts ──

def fix_fonts(svg: SvgFile) -> None:
    data = _palette()
    typo = data.get("typography", {})
    sans = typo.get("sans", "Arial, sans-serif")
    mono = typo.get("mono", "Courier New, monospace")
    for elem, _ in svg.content_elements():
        if tag(elem) not in ("text", "tspan"):
            continue
        current = elem.get("font-family", "")
        is_mono = bool(re.search(r"(mono|courier)", current, re.IGNORECASE))
        target = mono if is_mono else sans
        if current != target:
            elem.set("font-family", target)
            svg.changed = True


# ── Fix: gradients ──

def fix_gradients(svg: SvgFile) -> None:
    data = _palette()
    style = data.get("effects", {}).get("rect-fill", {}).get("style", "solid")
    families = []
    for gname, group in data.get("colors", {}).items():
        if gname == "neutrals":
            continue
        for name in group:
            if name.endswith("-fill"):
                families.append(name[:-len("-fill")])
    solid_for = {f: f"var(--{f}-fill)" for f in families}
    grad_for = {f: f"url(#grad-{f})" for f in families}
    if style == "gradient":
        from_to = {solid_for[f]: grad_for[f] for f in families}
    elif style == "solid":
        from_to = {grad_for[f]: solid_for[f] for f in families}
    else:
        return
    for elem, _ in svg.content_elements("rect"):
        fill = (elem.get("fill") or "").strip()
        target = from_to.get(fill)
        if target:
            elem.set("fill", target)
            svg.changed = True


# ── Fix: shadows ──

def fix_shadows(svg: SvgFile) -> None:
    data = _palette()
    eff = data.get("effects", {}).get("rect-shadow", {})
    enabled = bool(eff.get("enabled", False))
    apply_to = eff.get("apply-to", "none") if enabled else "none"
    family_fills: set[str] = set()
    for gname, group in data.get("colors", {}).items():
        if gname == "neutrals":
            continue
        for name in group:
            if name.endswith("-fill"):
                family_fills.add(f"var(--{name})")
                family_fills.add(f"url(#grad-{name[:-len('-fill')]})")

    for elem, _ in svg.content_elements("rect"):
        fill = (elem.get("fill") or "").strip()
        has = elem.get("filter") == "url(#shadow)"
        if apply_to == "none":
            want = False
        elif apply_to == "all":
            want = True
        else:
            want = fill in family_fills
        if want and not has:
            if "filter" in elem.attrib:
                del elem.attrib["filter"]
            elem.set("filter", "url(#shadow)")
            svg.changed = True
        elif has and not want:
            del elem.attrib["filter"]
            svg.changed = True


# ── Fix: markers ──

_CANONICAL_MARKERS = {
    "arrow", "arrow-primary", "arrow-ok", "arrow-warn",
    "arrow-danger", "arrow-info", "arrow-white",
}
_MARKER_URL_RE = re.compile(r"url\(#([^)]+)\)")


def _resolve_marker(name: str) -> str:
    low = name.lower()
    if "white" in low:
        return "arrow-white"
    if "red" in low or "danger" in low:
        return "arrow-danger"
    if "green" in low or "success" in low:
        return "arrow-ok"
    if "orange" in low or "warn" in low:
        return "arrow-warn"
    if "blue" in low or "primary" in low or "accent" in low:
        return "arrow-primary"
    if "purple" in low or "info" in low:
        return "arrow-info"
    return "arrow"


def fix_markers(svg: SvgFile) -> None:
    # Rewrite references
    for elem, _ in svg.content_elements():
        for attr in ("marker-start", "marker-mid", "marker-end"):
            val = elem.get(attr, "")
            m = _MARKER_URL_RE.match(val)
            if not m:
                continue
            name = m.group(1)
            if name in _CANONICAL_MARKERS:
                continue
            elem.set(attr, f"url(#{_resolve_marker(name)})")
            svg.changed = True

    # Remove custom marker defs
    for child in list(svg.root.iter()):
        if tag(child) != "defs":
            continue
        for marker in list(child):
            if is_comment(marker):
                continue
            if tag(marker) == "marker" and marker.get("id") not in _CANONICAL_MARKERS:
                child.remove(marker)
                svg.changed = True


# ── Fix: no-circles ──

def fix_no_circles(svg: SvgFile) -> None:
    if svg.path.name == "title.svg":
        return
    replacements = []
    for elem, parent in svg.content_elements("circle"):
        if parent is None:
            continue
        try:
            cx = float(elem.get("cx", "0"))
            cy = float(elem.get("cy", "0"))
            r = float(elem.get("r", "0"))
        except ValueError:
            continue
        rect = etree.Element("rect")
        rect.set("x", str(cx - r))
        rect.set("y", str(cy - r))
        rect.set("width", str(2 * r))
        rect.set("height", str(2 * r))
        rect.set("rx", str(min(r, 14.0)))
        for k, v in elem.attrib.items():
            if k not in ("cx", "cy", "r"):
                rect.set(k, v)
        rect.tail = elem.tail
        replacements.append((parent, elem, rect))

    for parent, old, new in replacements:
        idx = list(parent).index(old)
        parent.remove(old)
        parent.insert(idx, new)
        svg.changed = True


# ── Fix: no-background ──

_NEUTRAL_FILLS = {"var(--bg)", "var(--surface)", "none"}


def fix_no_background(svg: SvgFile) -> None:
    if svg.path.name == "title.svg":
        return
    for elem in list(svg.root):
        if is_comment(elem) or tag(elem) != "rect":
            continue
        try:
            x = float(elem.get("x", "0"))
            y = float(elem.get("y", "0"))
            w = float(elem.get("width", "0"))
            h = float(elem.get("height", "0"))
        except ValueError:
            continue
        if x <= 60 and y <= 60 and w >= 1000 and h >= 500:
            fill = (elem.get("fill") or "").strip()
            if fill in _NEUTRAL_FILLS:
                svg.root.remove(elem)
                svg.changed = True


# ── Fix: text-fill ──

def fix_text_fill(svg: SvgFile) -> None:
    FAMILY_NAMES = ["primary", "ok", "warn", "danger", "info"]
    family_fills = set()
    for f in FAMILY_NAMES:
        family_fills.add(f"var(--{f}-fill)")
        family_fills.add(f"url(#grad-{f})")

    rects: list[tuple[float, float, float, float, str]] = []
    for elem, _ in svg.content_elements("rect"):
        fill = (elem.get("fill") or "").strip()
        fam = None
        for f in FAMILY_NAMES:
            if fill in (f"var(--{f}-fill)", f"url(#grad-{f})"):
                fam = f
                break
        if fam is None:
            continue
        try:
            rects.append((
                float(elem.get("x", "0")), float(elem.get("y", "0")),
                float(elem.get("width", "0")), float(elem.get("height", "0")),
                fam,
            ))
        except ValueError:
            pass

    def containing_family(px: float, py: float) -> str | None:
        best, best_area = None, None
        for x, y, w, h, fam in rects:
            if x <= px <= x + w and y <= py <= y + h:
                area = w * h
                if best_area is None or area < best_area:
                    best, best_area = fam, area
        return best

    for elem, _ in svg.content_elements():
        if tag(elem) not in ("text", "tspan"):
            continue
        if elem.get("fill"):
            continue
        try:
            px = float(elem.get("x", "0"))
            py = float(elem.get("y", "0"))
        except ValueError:
            px, py = 0.0, 0.0
        fam = containing_family(px, py)
        elem.set("fill", f"var(--{fam}-text)" if fam else "var(--text)")
        svg.changed = True


# ── Fix: tag-placeholders ──

_PH_RE = re.compile(r"^[A-Z]$|^(Box|Item|Node|Label)\s*\d*$")


def fix_tag_placeholders(svg: SvgFile) -> None:
    # Check if already tagged
    for child in svg.root:
        if is_comment(child) and "PLACEHOLDERSVG" in (child.text or ""):
            return
    # Count placeholder-ish text
    ph_count = total = 0
    for elem, _ in svg.content_elements():
        if tag(elem) not in ("text", "tspan"):
            continue
        text = (elem.text or "").strip()
        if not text:
            continue
        total += 1
        if _PH_RE.match(text):
            ph_count += 1
    if total >= 3 and ph_count >= 3:
        comment = etree.Comment(" PLACEHOLDERSVG — replace with real diagram ")
        comment.tail = "\n"
        svg.root.insert(0, comment)
        svg.changed = True


# ── CLI ──

ALL_FIXES = [
    "fonts", "gradients", "shadows", "markers", "no_circles",
    "no_background", "root_bg", "aspect_ratio", "text_fill",
    "tag_placeholders", "fit",
]

FIX_MAP = {
    "fonts": fix_fonts,
    "gradients": fix_gradients,
    "shadows": fix_shadows,
    "markers": fix_markers,
    "no_circles": fix_no_circles,
    "no_background": fix_no_background,
    "text_fill": fix_text_fill,
    "tag_placeholders": fix_tag_placeholders,
}

# root_bg and aspect_ratio are handled by SvgFile.serialize() automatically.
# They're included as fix names for CLI completeness but don't need
# separate functions — SvgFile always ensures them.


def process_file(path: Path, fixes: set[str], dry_run: bool) -> bool:
    try:
        svg = SvgFile.load(path)
    except Exception:
        print(f"  SKIP (parse error): {path}", file=sys.stderr)
        return False

    for name in ALL_FIXES:
        if name not in fixes:
            continue
        fn = FIX_MAP.get(name)
        if fn:
            fn(svg)

    # Serialize (applies tree fixes + canonical defs)
    new_text = svg.serialize()

    # Apply fit on the serialized text (operates on coordinates via regex)
    if "fit" in fixes:
        fitted, info = fit_svg(new_text)
        if "skipped" not in info:
            new_text = fitted

    if new_text == svg._original_text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    if not Path(".git").exists():
        print("Error: run from the repository root", file=sys.stderr)
        sys.exit(1)

    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("paths", nargs="*",
                   help="SVG files (default: all under svg/)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--fonts", action="store_true")
    p.add_argument("--gradients", action="store_true")
    p.add_argument("--shadows", action="store_true")
    p.add_argument("--markers", action="store_true")
    p.add_argument("--no-circles", action="store_true", dest="no_circles")
    p.add_argument("--no-background", action="store_true", dest="no_background")
    p.add_argument("--root-bg", action="store_true", dest="root_bg")
    p.add_argument("--aspect-ratio", action="store_true", dest="aspect_ratio")
    p.add_argument("--text-fill", action="store_true", dest="text_fill")
    p.add_argument("--tag-placeholders", action="store_true",
                   dest="tag_placeholders")
    p.add_argument("--fit", action="store_true",
                   help="Fit content to [40,1240]x[40,620] usable area")
    args = p.parse_args()

    explicit = any(getattr(args, f) for f in ALL_FIXES)
    fixes = {f for f in ALL_FIXES if getattr(args, f) or not explicit}

    paths = ([Path(x) for x in args.paths] if args.paths
             else sorted(Path("svg").rglob("*.svg")))

    changed = 0
    total = 0
    for path in paths:
        if not path.is_file() or path.suffix != ".svg":
            continue
        total += 1
        if process_file(path, fixes, args.dry_run):
            changed += 1

    action = "would change" if args.dry_run else "changed"
    print(f"{action} {changed}/{total} file(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
