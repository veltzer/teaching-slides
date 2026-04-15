#!/usr/bin/env python

"""
Check SVG files for quality issues.

Checks:
  --size        Flag SVGs that are too small (likely placeholders)
  --elements    Flag SVGs with too few elements (likely stubs)
  --fonts       Flag SVGs with font-size below minimum
  --parse       Flag SVGs with XML parse errors
  --dimensions  Flag SVGs that do not have exactly viewBox="0 0 1280 720"
  --namespace   Flag SVGs whose root <svg> lacks xmlns="http://www.w3.org/2000/svg"
  --bounds      Flag SVGs with elements drawn below y=640
  --title       Flag SVGs that contain a <title> element
  --colors      Flag SVGs against their <!-- palette: path --> comment
  --words       Flag SVGs whose <text>/<tspan> content exceeds MAX_WORD_COUNT
  --fill        Flag SVGs whose bbox fills < MIN_FILL_PCT of the usable area
  --fit         Flag SVGs whose content bbox is not exactly fitted to [40,1240]x[40,620]
  --no-circles  Flag SVGs that contain <circle> elements (use <rect>/<ellipse> instead)
  --shadows     Validate <rect> shadow filter usage against palette effects.rect-shadow
  --typography  Validate <text>/<tspan> font-family against palette typography
  --gradients   Validate <rect> family fills (solid vs gradient) against palette effects.rect-fill

Usage:
    check_svg.py file1.svg file2.svg ...
    check_svg.py --fonts --size file1.svg file2.svg ...
    check_svg.py --colors file1.svg file2.svg ...
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
import yaml
from pathlib import Path

MIN_FILE_SIZE = 500
MIN_ELEMENTS = 5
MIN_FONT_SIZE = 10
REQUIRED_VIEWBOX = "0 0 1280 720"
MAX_Y_BOUND = 640
MAX_WORD_COUNT = 100
MIN_FILL_PCT = 40.0
USABLE_W = 1200.0
USABLE_H = 580.0
USABLE_X0 = 40.0
USABLE_Y0 = 40.0
FIT_TOL = 0.0  # px — bbox must match target exactly


def _check_size(path: Path) -> list[str]:
    """Flag SVGs that are too small (likely placeholders)."""
    size = path.stat().st_size
    if size < MIN_FILE_SIZE:
        return [f"too small ({size} bytes, min {MIN_FILE_SIZE})"]
    return []


def _check_parse(path: Path) -> tuple[ET.ElementTree | None, list[str]]:
    """Parse the SVG and return the tree and any errors."""
    try:
        tree = ET.parse(path)
        return tree, []
    except ET.ParseError as e:
        return None, [f"XML parse error: {e}"]


def _check_elements(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs with too few elements (likely stubs)."""
    count = sum(1 for _ in tree.iter())
    if count < MIN_ELEMENTS:
        return [f"too few elements ({count}, min {MIN_ELEMENTS})"]
    return []


_WORDS_TEXT_RE = re.compile(r'<(?:text|tspan)[^>]*?>(.*?)</(?:text|tspan)>', re.DOTALL)
_WORDS_DEFS_RE = re.compile(r'<defs\b.*?</defs>', re.DOTALL)
_WORDS_TAG_RE = re.compile(r'<[^>]+>')
_WORDS_WORD_RE = re.compile(r"[A-Za-z0-9_.@#+\-/()'\"]+")


def _check_words(path: Path) -> list[str]:
    """Flag SVGs whose total visible text exceeds MAX_WORD_COUNT.

    Counts words across <text>/<tspan> elements outside <defs>. Heavy-text
    diagrams belong in prose slides or speaker notes, not inside a diagram.
    """
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return []
    outside = _WORDS_DEFS_RE.sub('', content)
    total = 0
    for m in _WORDS_TEXT_RE.finditer(outside):
        plain = _WORDS_TAG_RE.sub(' ', m.group(1))
        total += len(_WORDS_WORD_RE.findall(plain))
    if total > MAX_WORD_COUNT:
        return [f"too many words in text elements ({total}, max {MAX_WORD_COUNT}) — move prose to speaker notes or a separate slide"]
    return []


def _check_fonts(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs with font-size below minimum."""
    for elem in tree.iter():
        fs = elem.get("font-size")
        if fs is not None:
            try:
                val = float(fs)
                if val < MIN_FONT_SIZE:
                    return [f"font-size {fs} too small (min {MIN_FONT_SIZE})"]
            except ValueError:
                pass
    return []


SVG_NS = "http://www.w3.org/2000/svg"


def _check_namespace(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs whose root <svg> lacks xmlns="http://www.w3.org/2000/svg".

    Without the SVG namespace the browser treats the file as generic XML
    and renders nothing — the slide appears blank. ElementTree parses such
    files fine (they are valid XML), which is why every earlier check
    passed. This check exists to catch that specific failure mode."""
    root = tree.getroot()
    tag = root.tag
    if tag.startswith("{"):
        ns = tag[1:].split("}", 1)[0]
        if ns != SVG_NS:
            return [f"root element in namespace {ns!r}, must be {SVG_NS!r}"]
        return []
    return [f'root <svg> missing xmlns="{SVG_NS}"']


def _check_dimensions(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs that do not have exactly viewBox="0 0 1280 720"."""
    root = tree.getroot()
    viewbox = root.get("viewBox")
    if viewbox is None:
        return [f"missing viewBox (required: {REQUIRED_VIEWBOX!r})"]
    normalised = " ".join(viewbox.split())
    if normalised != REQUIRED_VIEWBOX:
        return [f"viewBox is {viewbox!r}, must be {REQUIRED_VIEWBOX!r}"]
    return []


def _check_bounds(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs with elements drawn below the maximum Y boundary."""
    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]
        y_max = None
        
        try:
            if tag in ('rect', 'image', 'foreignObject'):
                y = float(elem.get('y', '0').replace('px', ''))
                h = float(elem.get('height', '0').replace('px', ''))
                y_max = y + h
            elif tag in ('text', 'use'):
                y = float(elem.get('y', '0').replace('px', ''))
                y_max = y
            elif tag in ('circle', 'ellipse'):
                cy = float(elem.get('cy', '0').replace('px', ''))
                if tag == 'circle':
                    r = float(elem.get('r', '0').replace('px', ''))
                else:
                    r = float(elem.get('ry', '0').replace('px', ''))
                y_max = cy + r
            elif tag == 'line':
                y1 = float(elem.get('y1', '0').replace('px', ''))
                y2 = float(elem.get('y2', '0').replace('px', ''))
                y_max = max(y1, y2)
        except ValueError:
            pass
            
        if y_max is not None and y_max > MAX_Y_BOUND:
            return [f"element <{tag}> extends below y={MAX_Y_BOUND} (found bottom y={y_max})"]
    return []

_PALETTE_CACHE: dict[str, set[str]] = {}
_COLOR_ATTRS = {"fill", "stroke", "stop-color", "flood-color"}
_COLOR_RE = re.compile(r'#[0-9a-fA-F]{3,8}')
_VAR_RE = re.compile(r'^var\(--([a-zA-Z0-9_-]+)\)$')
# Values that are not colors — always allowed
_NON_COLOR_VALUES = {"none", "currentcolor", "inherit", "transparent"}
# Tags inside <defs> where raw hex is allowed (gradient stops, marker fills, filter colors)
_DEFS_TAGS = {"stop", "feDropShadow"}

_DEFAULT_PALETTE = Path("resources/palette_diagram.yaml")
_PALETTE_COMMENT_RE = re.compile(r'<!--\s*palette:\s*(\S+)\s*-->')


def _load_palette_names(palette_path: Path) -> set[str]:
    """Load allowed semantic color names from a palette YAML file.

    Returns a set of names like {"bg", "primary", "danger-lt", ...}.
    """
    key = str(palette_path)
    if key in _PALETTE_CACHE:
        return _PALETTE_CACHE[key]

    if not palette_path.exists():
        _PALETTE_CACHE[key] = set()
        return _PALETTE_CACHE[key]

    with open(palette_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    names: set[str] = set()
    for group in data.get("colors", {}).values():
        for name in group:
            names.add(name)

    _PALETTE_CACHE[key] = names
    return _PALETTE_CACHE[key]


def _palette_for_svg(svg_path: Path) -> Path:
    """Return the palette file for an SVG by reading its <!-- palette: ... --> comment.

    Falls back to the default diagram palette if no comment is found.
    """
    try:
        text = svg_path.read_text(encoding="utf-8")
        m = _PALETTE_COMMENT_RE.search(text)
        if m:
            return Path(m.group(1))
    except OSError:
        pass
    return _DEFAULT_PALETTE


def _check_colors(tree: ET.ElementTree, svg_path: Path | None = None) -> list[str]:
    """Flag SVGs that use colors not expressed as var(--name) from the palette.

    Reads the <!-- palette: path --> comment inside the SVG to determine
    which palette YAML to validate against. Falls back to palette_diagram.yaml
    if no comment is present.
    Raw hex values and named CSS colors are rejected.

    Exception: elements inside <defs> (gradient stops, marker paths, filter
    params) may use raw hex since CSS var() doesn't work reliably there.
    """
    palette_path = _palette_for_svg(svg_path) if svg_path else _DEFAULT_PALETTE
    palette_names = _load_palette_names(palette_path)
    if not palette_names:
        return [f"cannot check colors: {palette_path} not found or empty"]

    errors: list[str] = []
    seen_bad: set[str] = set()

    # Collect all elements that are descendants of <defs>
    defs_children: set[ET.Element] = set()
    root = tree.getroot()
    for defs_elem in root.iter():
        if defs_elem.tag.split('}')[-1] == 'defs':
            for child in defs_elem.iter():
                defs_children.add(child)

    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]

        # Skip defs elements themselves and their children
        if elem in defs_children or tag == 'defs':
            continue

        for attr in _COLOR_ATTRS:
            val = elem.get(attr, "")
            if not val:
                continue

            stripped = val.strip().lower()

            # Skip non-color values and url() references
            if stripped in _NON_COLOR_VALUES or stripped.startswith("url("):
                continue

            # Check for var(--name)
            var_m = _VAR_RE.match(stripped)
            if var_m:
                name = var_m.group(1)
                if name not in palette_names and name not in seen_bad:
                    seen_bad.add(name)
                    errors.append(
                        f"var(--{name}) (in <{tag}> {attr}=)"
                        f" — name not in palette"
                    )
                continue

            # Anything else is not allowed
            key = f"{attr}:{stripped}"
            if key not in seen_bad:
                seen_bad.add(key)
                errors.append(
                    f"raw color {val!r} (in <{tag}> {attr}=)"
                    f" — use var(--name) from the palette"
                )

    return errors


def _check_fill(path: Path) -> list[str]:
    """Flag SVGs whose drawing bbox fills less than MIN_FILL_PCT of the
    usable area (1200x580). Under-filled SVGs waste slide space; most end
    up that way through a broken prior edit, not by design."""
    # Lazy-import to avoid paying the cost when --fill isn't used.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "fit_svg_to_slide",
        Path(__file__).resolve().parent / "fit_svg_to_slide.py",
    )
    fit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fit)
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    outside = re.sub(r'<defs\b.*?</defs>', '', content, flags=re.DOTALL)
    bbox = fit.compute_bbox(outside)
    if bbox is None:
        return ["no drawable content (bbox is empty)"]
    x0, y0, x1, y1 = bbox
    w = max(0.0, x1 - x0)
    h = max(0.0, y1 - y0)
    fill_pct = 100 * (w * h) / (USABLE_W * USABLE_H)
    if fill_pct < MIN_FILL_PCT:
        return [
            f"fill ratio {fill_pct:.1f}% < {MIN_FILL_PCT:.0f}% "
            f"(bbox {w:.0f}x{h:.0f}) — expand content to fill 1200x580"
        ]
    return []


def _check_fit(path: Path) -> list[str]:
    """Flag SVGs whose content bbox is not exactly fitted to [40,1240]x[40,620].

    Run scripts/fit_svg_to_slide.py to fix."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "fit_svg_to_slide",
        Path(__file__).resolve().parent / "fit_svg_to_slide.py",
    )
    fit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fit)
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    outside = re.sub(r'<defs\b.*?</defs>', '', content, flags=re.DOTALL)
    bbox = fit.compute_bbox(outside)
    if bbox is None:
        return []  # no drawable content — let _check_fill handle it
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0
    target_x0 = USABLE_X0
    target_y0 = USABLE_Y0
    target_w = USABLE_W
    target_h = USABLE_H
    if (abs(x0 - target_x0) > FIT_TOL or abs(y0 - target_y0) > FIT_TOL
            or abs(w - target_w) > FIT_TOL or abs(h - target_h) > FIT_TOL):
        return [
            f"content not fitted: bbox ({x0:.1f},{y0:.1f})+{w:.1f}x{h:.1f}"
            f" != target ({target_x0:.0f},{target_y0:.0f})+{target_w:.0f}x{target_h:.0f}"
            f" — run scripts/fit_svg_to_slide.py"
        ]
    return []


_SHADOW_POLICY: tuple[bool, str, set[str]] | None = None


def _shadow_policy() -> tuple[bool, str, set[str]]:
    global _SHADOW_POLICY
    if _SHADOW_POLICY is not None:
        return _SHADOW_POLICY
    palette_path = _DEFAULT_PALETTE
    if not palette_path.exists():
        _SHADOW_POLICY = (False, "none", set())
        return _SHADOW_POLICY
    data = yaml.safe_load(palette_path.read_text(encoding="utf-8"))
    eff = data.get("effects", {}).get("rect-shadow", {})
    enabled = bool(eff.get("enabled", False))
    apply_to = eff.get("apply-to", "none") if enabled else "none"
    family_fills: set[str] = set()
    for group_name, group in data.get("colors", {}).items():
        if group_name == "neutrals":
            continue
        for name in group:
            if name.endswith("-fill"):
                family_fills.add(f"var(--{name})")
                family_fills.add(f"url(#grad-{name[:-len('-fill')]})")
    _SHADOW_POLICY = (enabled, apply_to, family_fills)
    return _SHADOW_POLICY


def _check_shadows(tree: ET.ElementTree) -> list[str]:
    """Validate <rect> shadow usage against palette effects.rect-shadow."""
    enabled, apply_to, family_fills = _shadow_policy()
    errors: list[str] = []
    defs_children: set[ET.Element] = set()
    root = tree.getroot()
    for elem in root.iter():
        if elem.tag.split('}')[-1] == 'defs':
            for child in elem.iter():
                defs_children.add(child)
    for elem in tree.iter():
        if elem in defs_children:
            continue
        if elem.tag.split('}')[-1] != 'rect':
            continue
        fill = (elem.get('fill') or '').strip()
        has = 'url(#shadow)' in (elem.get('filter') or '')
        if apply_to == 'none':
            want = False
        elif apply_to == 'all':
            want = True
        else:  # family-only
            want = fill in family_fills
        if want and not has:
            errors.append(f"<rect fill={fill!r}> missing filter=\"url(#shadow)\"")
        elif has and not want:
            errors.append(f"<rect fill={fill!r}> has filter=\"url(#shadow)\" but policy forbids it")
    return errors


_TYPOGRAPHY: tuple[str, str] | None = None


def _typography() -> tuple[str, str]:
    global _TYPOGRAPHY
    if _TYPOGRAPHY is not None:
        return _TYPOGRAPHY
    if not _DEFAULT_PALETTE.exists():
        _TYPOGRAPHY = ("Arial, sans-serif", "Courier New, monospace")
        return _TYPOGRAPHY
    data = yaml.safe_load(_DEFAULT_PALETTE.read_text(encoding="utf-8"))
    typo = data.get("typography", {})
    _TYPOGRAPHY = (
        typo.get("sans", "Arial, sans-serif"),
        typo.get("mono", "Courier New, monospace"),
    )
    return _TYPOGRAPHY


_RECT_FILL_POLICY: tuple[str, list[str]] | None = None


def _rect_fill_policy() -> tuple[str, list[str]]:
    global _RECT_FILL_POLICY
    if _RECT_FILL_POLICY is not None:
        return _RECT_FILL_POLICY
    if not _DEFAULT_PALETTE.exists():
        _RECT_FILL_POLICY = ("solid", [])
        return _RECT_FILL_POLICY
    data = yaml.safe_load(_DEFAULT_PALETTE.read_text(encoding="utf-8"))
    style = data.get("effects", {}).get("rect-fill", {}).get("style", "solid")
    fams = []
    for group_name, group in data.get("colors", {}).items():
        if group_name == "neutrals":
            continue
        for name in group:
            if name.endswith("-fill"):
                fams.append(name[:-len("-fill")])
    _RECT_FILL_POLICY = (style, fams)
    return _RECT_FILL_POLICY


def _check_gradients(tree: ET.ElementTree) -> list[str]:
    """Validate <rect> family fills against palette effects.rect-fill.style."""
    style, families = _rect_fill_policy()
    errors: list[str] = []
    defs_children: set[ET.Element] = set()
    root = tree.getroot()
    for elem in root.iter():
        if elem.tag.split('}')[-1] == 'defs':
            for child in elem.iter():
                defs_children.add(child)
    solid_fills = {f"var(--{f}-fill)": f for f in families}
    grad_fills = {f"url(#grad-{f})": f for f in families}
    for elem in tree.iter():
        if elem in defs_children:
            continue
        if elem.tag.split('}')[-1] != 'rect':
            continue
        fill = (elem.get('fill') or '').strip()
        if style == 'gradient' and fill in solid_fills:
            fam = solid_fills[fill]
            errors.append(
                f"<rect fill={fill!r}> should be url(#grad-{fam}) "
                f"per rect-fill.style=gradient"
            )
        elif style == 'solid' and fill in grad_fills:
            fam = grad_fills[fill]
            errors.append(
                f"<rect fill={fill!r}> should be var(--{fam}-fill) "
                f"per rect-fill.style=solid"
            )
    return errors


def _check_typography(tree: ET.ElementTree) -> list[str]:
    """Validate font-family on every <text>/<tspan> against palette typography."""
    sans, mono = _typography()
    allowed = {sans, mono}
    errors: list[str] = []
    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]
        if tag not in ('text', 'tspan'):
            continue
        ff = elem.get('font-family')
        if ff is None:
            errors.append(f"<{tag}> missing font-family")
            continue
        if ff not in allowed:
            errors.append(f"<{tag}> font-family={ff!r} not in palette typography")
    return errors


def _check_no_circles(tree: ET.ElementTree, path: Path) -> list[str]:
    """Flag SVGs that contain <circle> elements.

    Circles are locked to a 1:1 aspect ratio and don't stretch correctly
    under the fit-to-slide pass. Use <rect> (with rx for rounded corners)
    or <ellipse> instead. Title slides (title.svg) are exempt — they are
    decorative and often use circles intentionally."""
    if path.name == 'title.svg':
        return []
    count = 0
    for elem in tree.iter():
        if elem.tag.split('}')[-1] == 'circle':
            count += 1
    if count:
        return [f"contains {count} <circle> element(s) — use <rect> or <ellipse> instead"]
    return []


def _check_title(tree: ET.ElementTree) -> list[str]:
    """Flag SVGs that contain a <title> element."""
    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]
        if tag == 'title':
            return ["contains a <title> element (headings should be outside SVG)"]
    return []

def main() -> None:
    if not Path(".git").exists():
        print("Error: script must be run from the root of the repository", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Check SVG files for quality issues.'
    )
    parser.add_argument('paths', nargs='*',
                        help='SVG files to check')
    parser.add_argument('--size', action='store_true',
                        help='Flag SVGs that are too small (likely placeholders)')
    parser.add_argument('--elements', action='store_true',
                        help='Flag SVGs with too few elements (likely stubs)')
    parser.add_argument('--fonts', action='store_true',
                        help='Flag SVGs with font-size below minimum')
    parser.add_argument('--parse', action='store_true',
                        help='Flag SVGs with XML parse errors')
    parser.add_argument('--dimensions', action='store_true',
                        help='Flag SVGs that do not have exactly viewBox="0 0 1280 720"')
    parser.add_argument('--namespace', action='store_true',
                        help='Flag SVGs whose root <svg> lacks xmlns="http://www.w3.org/2000/svg"')
    parser.add_argument('--bounds', action='store_true',
                        help='Flag SVGs with elements drawn below y=640')
    parser.add_argument('--title', action='store_true',
                        help='Flag SVGs that contain a <title> element')
    parser.add_argument('--colors', action='store_true',
                        help='Flag SVGs against their <!-- palette: path --> comment (default: palette_diagram)')
    parser.add_argument('--words', action='store_true',
                        help=f'Flag SVGs whose <text>/<tspan> content exceeds {MAX_WORD_COUNT} words total')
    parser.add_argument('--fill', action='store_true',
                        help=f'Flag SVGs whose content bbox fills less than {MIN_FILL_PCT:.0f}% of the 1200x580 usable area')
    parser.add_argument('--fit', action='store_true',
                        help='Flag SVGs whose content bbox is not exactly fitted to [40,1240]x[40,620]')
    parser.add_argument('--no-circles', action='store_true', dest='no_circles',
                        help='Flag SVGs that contain <circle> elements (use <rect>/<ellipse> instead)')
    parser.add_argument('--shadows', action='store_true',
                        help='Validate <rect> shadow filter usage against palette effects.rect-shadow')
    parser.add_argument('--typography', action='store_true',
                        help='Validate <text>/<tspan> font-family against palette typography')
    parser.add_argument('--gradients', action='store_true',
                        help='Validate <rect> family fills (solid vs gradient) against palette effects.rect-fill')
    args = parser.parse_args()

    if not args.paths:
        parser.error("at least one SVG file is required")

    # Default: all checks enabled when no flags are specified
    flags = [args.size, args.elements, args.fonts, args.parse, args.dimensions,
            args.namespace, args.bounds, args.title, args.colors, args.words,
            args.fill, args.fit, args.no_circles, args.shadows, args.typography,
            args.gradients]
    explicit = any(flags)
    do_size = args.size or not explicit
    do_elements = args.elements or not explicit
    do_fonts = args.fonts or not explicit
    do_parse = args.parse or not explicit
    do_dimensions = args.dimensions or not explicit
    do_namespace = args.namespace or not explicit
    do_bounds = args.bounds or not explicit
    do_title = args.title or not explicit
    do_colors = args.colors or not explicit
    do_words = args.words or not explicit
    do_fill = args.fill or not explicit
    do_fit = args.fit or not explicit
    do_no_circles = args.no_circles or not explicit
    do_shadows = args.shadows or not explicit
    do_typography = args.typography or not explicit
    do_gradients = args.gradients or not explicit

    failures = 0
    for path_str in args.paths:
        path = Path(path_str)
        errors: list[str] = []

        if do_size:
            errors.extend(_check_size(path))

        if do_words:
            errors.extend(_check_words(path))

        if do_fill:
            errors.extend(_check_fill(path))

        if do_fit:
            errors.extend(_check_fit(path))

        # Parse once, reuse for element, font, and aspect checks
        tree = None
        if do_parse or do_elements or do_fonts or do_dimensions or do_namespace or do_bounds or do_title or do_colors or do_no_circles or do_shadows or do_typography or do_gradients:
            tree, parse_errors = _check_parse(path)
            if do_parse:
                errors.extend(parse_errors)

        if tree is not None:
            if do_elements:
                errors.extend(_check_elements(tree))
            if do_fonts:
                errors.extend(_check_fonts(tree))
            if do_dimensions:
                errors.extend(_check_dimensions(tree))
            if do_namespace:
                errors.extend(_check_namespace(tree))
            if do_bounds:
                errors.extend(_check_bounds(tree))
            if do_title:
                errors.extend(_check_title(tree))
            if do_colors:
                errors.extend(_check_colors(tree, svg_path=path))
            if do_no_circles:
                errors.extend(_check_no_circles(tree, path))
            if do_shadows:
                errors.extend(_check_shadows(tree))
            if do_typography:
                errors.extend(_check_typography(tree))
            if do_gradients:
                errors.extend(_check_gradients(tree))

        for error in errors:
            print(f"{path}: {error}", file=sys.stderr)
            failures += 1

    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
