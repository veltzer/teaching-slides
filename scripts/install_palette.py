#!/usr/bin/env python
# IMPORTANT: This script MUST be idempotent. Running it twice on the same
# file must produce identical output. If you modify this script, verify
# idempotency by running it on the full repo twice and confirming zero
# files change on the second run.

"""
Install the canonical palette into every SVG under svg/.

Each SVG declares its type via a <metadata><type> element:

    <metadata>
      <type>regular</type>    — uses palette_diagram.yaml (default)
    </metadata>

    <metadata>
      <type>title</type>      — uses palette_intro.yaml
    </metadata>

The type determines which palette YAML is used to build the <defs> block.
If no <metadata><type> element is present, the SVG defaults to "regular".

For each SVG:
  1. Reads <metadata><type> to select the palette
  2. Rebuilds the <defs> block from the selected palette YAML (via svg_lib)
  3. Converts raw hex color values in attributes to var(--name) references
  4. Renames old gradient/marker IDs to canonical ones
  5. Ensures xmlns, viewBox, and background style on root

Uses svg_lib.SvgFile for tree operations + deterministic serialization.

Usage:
    scripts/install_palette.py                  # dry-run
    scripts/install_palette.py --apply          # apply to all SVGs
    scripts/install_palette.py --apply FILE...  # apply to specific files
"""

import argparse
import re
import sys
from pathlib import Path

from svg_lib import SvgFile, load_palette, PALETTES

SVG_ROOT = Path("svg")

# Old ID -> canonical ID renames.
ID_RENAMES: dict[str, str] = {
    "arrowhead-green": "arrow-ok",
    "arrowhead-gray": "arrow",
    "arrowhead-grey": "arrow",
    "arrowhead-red": "arrow-danger",
    "arrowhead-dash": "arrow",
    "arrowhead": "arrow",
    "arrowgreen": "arrow-ok",
    "arrowred": "arrow-danger",
    "arrowdash": "arrow",
    "arrow-accent": "arrow-primary",
    "arrow-blue": "arrow-primary",
    "arrow-green": "arrow-ok",
    "arrow-red": "arrow-danger",
    "arrow-orange": "arrow-warn",
    "arrow1": "arrow",
    "arrow2": "arrow",
    "arrow3": "arrow",
    "arrow4": "arrow",
    "arrow5": "arrow",
    "grad-accent": "grad-primary",
    "grad-green": "grad-ok",
    "grad-orange": "grad-warn",
    "grad-red": "grad-danger",
    "grad-purple": "grad-info",
}

# Named CSS colors -> palette semantic name.
CSS_TO_PALETTE: dict[str, str] = {
    "white": "bg",
    "black": "black",
    "red": "danger",
    "green": "ok",
    "blue": "primary",
    "gray": "text-faint",
    "grey": "text-faint",
}

# Color attributes to convert.
COLOR_ATTRS = {"fill", "stroke", "stop-color", "flood-color"}

_HEX_RE = re.compile(r"^#[0-9a-fA-F]{3,8}$")


def _build_hex_to_name(data: dict) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for group in data["colors"].values():
        for name, hexval in group.items():
            h = hexval.strip().lower().lstrip("#")
            if len(h) == 3:
                h = "".join(ch * 2 for ch in h)
            mapping[f"#{h}"] = name
    return mapping


def _apply_renames(svg: SvgFile) -> None:
    """Rename old marker/gradient IDs in references and definitions."""
    marker_ref_re = re.compile(r"url\(#([^)]+)\)")
    for elem, _parent in svg.content_elements():
        # Rename marker references
        for attr in ("marker-start", "marker-mid", "marker-end"):
            val = elem.get(attr, "")
            m = marker_ref_re.match(val)
            if m and m.group(1) in ID_RENAMES:
                elem.set(attr, f"url(#{ID_RENAMES[m.group(1)]})")
                svg.changed = True
        # Rename fill/filter gradient references
        for attr in ("fill", "filter"):
            val = elem.get(attr, "")
            m = marker_ref_re.match(val)
            if m and m.group(1) in ID_RENAMES:
                elem.set(attr, f"url(#{ID_RENAMES[m.group(1)]})")
                svg.changed = True


def _convert_colors(svg: SvgFile, hex_to_name: dict[str, str]) -> None:
    """Convert raw hex and named CSS colors to var(--name) on content elements."""
    for elem, _parent in svg.content_elements():
        for attr in COLOR_ATTRS:
            val = (elem.get(attr) or "").strip()
            if not val:
                continue
            # Skip non-color values
            if val.lower() in ("none", "currentcolor", "inherit", "transparent"):
                continue
            if val.startswith("url(") or val.startswith("var("):
                continue
            # Named CSS color
            if val.lower() in CSS_TO_PALETTE:
                elem.set(attr, f"var(--{CSS_TO_PALETTE[val.lower()]})")
                svg.changed = True
                continue
            # Hex color
            if _HEX_RE.match(val):
                h = val.lower().lstrip("#")
                if len(h) == 3:
                    h = "".join(ch * 2 for ch in h)
                normalized = f"#{h}"
                if normalized in hex_to_name:
                    elem.set(attr, f"var(--{hex_to_name[normalized]})")
                    svg.changed = True


def process_file(path: Path, hex_to_name_map: dict[str, dict[str, str]],
                 apply: bool) -> bool:
    """Process one SVG. Returns True if the file changed."""
    svg = SvgFile.load(path)
    hex_to_name = hex_to_name_map.get(svg.svg_type, hex_to_name_map["regular"])
    _apply_renames(svg)
    _convert_colors(svg, hex_to_name)

    if apply:
        return svg.save_if_changed()
    else:
        new = svg.serialize()
        return new != svg._original_text


def main() -> None:
    if not Path(".git").exists():
        print("Error: run from the repository root", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*",
                        help="SVG files (default: all under svg/)")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes (default is dry-run)")
    args = parser.parse_args()

    # Build hex-to-name mapping for each palette type
    hex_to_name_map: dict[str, dict[str, str]] = {}
    for svg_type, palette_path in PALETTES.items():
        if not palette_path.exists():
            print(f"Error: {palette_path} not found", file=sys.stderr)
            sys.exit(1)
        data = load_palette(palette_path)
        hex_to_name_map[svg_type] = _build_hex_to_name(data)

    svg_files = ([Path(p) for p in args.paths] if args.paths
                 else sorted(SVG_ROOT.rglob("*.svg")))

    changed: list[Path] = []
    errors: list[tuple[Path, Exception]] = []

    for path in svg_files:
        try:
            if process_file(path, hex_to_name_map, args.apply):
                changed.append(path)
        except Exception as exc:
            errors.append((path, exc))

    action = "Updated" if args.apply else "Would update"
    for p in changed:
        print(f"{action}: {p}")
    for p, exc in errors:
        print(f"ERROR: {p}: {exc}", file=sys.stderr)

    print(f"\n{action} {len(changed)} file(s). {len(errors)} error(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
