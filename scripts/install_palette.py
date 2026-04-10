#!/usr/bin/env python

"""
Install the canonical palette defs block into every SVG under svg/.

What it does:
  1. Reads the <defs> block from resources/svg_palette.svg.
  2. For each SVG file under svg/:
     a. Renames old palette gradient / marker IDs to their canonical
        equivalents throughout the file (e.g. grad-accent -> grad-primary).
     b. Removes any palette-managed entries that are already present in
        the SVG's <defs> block (to avoid duplicates).
     c. Inserts the canonical palette entries at the top of the SVG's
        existing <defs> block, or creates a new <defs> block if none exists.
     Custom SVG-specific entries (unique gradients, custom markers, etc.)
     are left untouched.

ID renames applied:
  grad-accent   -> grad-primary
  grad-green    -> grad-ok
  grad-orange   -> grad-warn
  grad-red      -> grad-danger
  grad-purple   -> grad-info
  arrow-accent  -> arrow-primary
  arrow-blue    -> arrow-primary
  arrow-green   -> arrow-ok
  arrow-red     -> arrow-danger
  arrow-orange  -> arrow-warn
  arrowhead     -> arrow        (and numbered / colour variants)

Usage:
    scripts/install_palette.py                  # dry-run: report what would change
    scripts/install_palette.py --apply          # write changes to disk
    scripts/install_palette.py --apply svg/...  # apply to specific files only
"""

import argparse
import re
import sys
from pathlib import Path

PALETTE_PATH = Path("resources/svg_palette.svg")
SVG_ROOT = Path("svg")

# Canonical IDs that the palette owns — anything with one of these IDs in an
# existing <defs> block will be removed and re-inserted from the palette.
PALETTE_IDS: set[str] = {
    "grad-primary", "grad-surface", "grad-ok", "grad-warn", "grad-danger", "grad-info",
    "shadow",
    "arrow", "arrow-primary", "arrow-ok", "arrow-warn", "arrow-danger", "arrow-info", "arrow-white",
}

# Old ID -> canonical ID renames (longer/more-specific first).
ID_RENAMES: list[tuple[str, str]] = [
    ("arrowhead-green",  "arrow-ok"),
    ("arrowhead-gray",   "arrow"),
    ("arrowhead-grey",   "arrow"),
    ("arrowhead-red",    "arrow-danger"),
    ("arrowhead-dash",   "arrow"),
    ("arrowhead",        "arrow"),
    ("arrowgreen",       "arrow-ok"),
    ("arrowred",         "arrow-danger"),
    ("arrowdash",        "arrow"),
    ("arrow-accent",     "arrow-primary"),
    ("arrow-blue",       "arrow-primary"),
    ("arrow-green",      "arrow-ok"),
    ("arrow-red",        "arrow-danger"),
    ("arrow-orange",     "arrow-warn"),
    ("arrow1",           "arrow"),
    ("arrow2",           "arrow"),
    ("arrow3",           "arrow"),
    ("arrow4",           "arrow"),
    ("arrow5",           "arrow"),
    ("grad-accent",      "grad-primary"),
    ("grad-green",       "grad-ok"),
    ("grad-orange",      "grad-warn"),
    ("grad-red",         "grad-danger"),
    ("grad-purple",      "grad-info"),
]

# Matches any namespace-prefixed or plain defs block
_DEFS_OPEN_RE  = re.compile(r'<(?:[a-zA-Z0-9_]+:)?defs(?:\s[^>]*)?>')
_DEFS_CLOSE_RE = re.compile(r'</(?:[a-zA-Z0-9_]+:)?defs>')

# Opening <svg …> tag
_SVG_OPEN_RE = re.compile(r'(<(?:[a-zA-Z0-9_]+:)?svg\b[^>]*>)')

# One XML element (non-recursive, for top-level defs children)
_ELEMENT_RE = re.compile(r'<[^>]+(?:/>|>.*?</[^>]+>)', re.DOTALL)

# id="..." anywhere
_ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')


def _extract_palette_defs_block(palette_text: str) -> str:
    """Return the indented content between <defs> and </defs> in the palette."""
    m = re.search(r'<defs>(.*?)</defs>', palette_text, re.DOTALL)
    if not m:
        raise RuntimeError(f"No <defs> block found in {PALETTE_PATH}")
    return m.group(1)   # the inner content, not the tags themselves


def _apply_renames(text: str) -> str:
    """Replace old gradient/marker IDs with canonical ones throughout text."""
    for old, new in ID_RENAMES:
        text = re.sub(
            rf'(?<!["\w-]){re.escape(old)}(?!["\w-])',
            new,
            text,
        )
    return text


def _merge_defs(svg_text: str, palette_inner: str) -> str:
    """Merge palette entries into the SVG's <defs> block.

    - If the SVG has a <defs> block: remove any existing palette-owned entries
      (by id) and prepend the canonical palette content.
    - If no <defs> block: insert a new one right after the opening <svg> tag.
    """
    open_m = _DEFS_OPEN_RE.search(svg_text)
    close_m = _DEFS_CLOSE_RE.search(svg_text)

    if open_m and close_m and open_m.start() < close_m.start():
        # There is an existing <defs> block.
        defs_start = open_m.start()
        defs_end   = close_m.end()
        open_tag   = open_m.group()      # e.g. <defs> or <ns0:defs>
        close_tag  = close_m.group()     # e.g. </defs> or </ns0:defs>
        inner      = svg_text[open_m.end():close_m.start()]

        # Remove any element whose id= is a palette-managed ID
        def _strip_palette_elements(inner_text: str) -> str:
            # Walk through removing top-level elements with palette IDs.
            # We do this line-by-line on the raw text to avoid re-parsing.
            lines = inner_text.split('\n')
            result = []
            skip_until_close: str | None = None
            i = 0
            while i < len(lines):
                line = lines[i]
                if skip_until_close:
                    if skip_until_close in line:
                        skip_until_close = None
                    i += 1
                    continue
                # Check if this line opens an element with a palette ID
                id_m = _ID_ATTR_RE.search(line)
                if id_m and id_m.group(1) in PALETTE_IDS:
                    # Self-closing or multi-line?
                    if '/>' in line:
                        i += 1
                        continue   # skip just this line
                    # Find the closing tag
                    tag_m = re.match(r'\s*<([A-Za-z0-9_:]+)', line)
                    if tag_m:
                        tag_name = tag_m.group(1)
                        skip_until_close = f'</{tag_name}>'
                    i += 1
                    continue
                result.append(line)
                i += 1
            return '\n'.join(result)

        cleaned_inner = _strip_palette_elements(inner)

        new_defs = open_tag + '\n' + palette_inner + cleaned_inner + close_tag
        svg_text = svg_text[:defs_start] + new_defs + svg_text[defs_end:]
    else:
        # No <defs> block — insert one after the opening <svg> tag.
        new_defs_block = '\n  <defs>\n' + palette_inner + '  </defs>'
        svg_text = _SVG_OPEN_RE.sub(r'\1' + new_defs_block, svg_text, count=1)

    return svg_text


def process_file(path: Path, palette_inner: str, apply: bool) -> bool:
    """Process one SVG. Returns True if the file would/did change."""
    original = path.read_text(encoding="utf-8")

    # Step 1: rename old IDs
    updated = _apply_renames(original)

    # Step 2: merge palette defs
    updated = _merge_defs(updated, palette_inner)

    if updated == original:
        return False

    if apply:
        path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    if not Path(".git").exists():
        print("Error: run from the repository root", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*",
                        help="SVG files to process (default: all under svg/)")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes to disk (default is dry-run)")
    args = parser.parse_args()

    if not PALETTE_PATH.exists():
        print(f"Error: {PALETTE_PATH} not found", file=sys.stderr)
        sys.exit(1)

    palette_text = PALETTE_PATH.read_text(encoding="utf-8")
    palette_inner = _extract_palette_defs_block(palette_text)

    svg_files = [Path(p) for p in args.paths] if args.paths \
        else sorted(SVG_ROOT.rglob("*.svg"))

    changed: list[Path] = []
    errors: list[tuple[Path, Exception]] = []

    for path in svg_files:
        try:
            if process_file(path, palette_inner, args.apply):
                changed.append(path)
        except Exception as exc:
            errors.append((path, exc))

    action = "Updated" if args.apply else "Would update"
    for p in changed:
        print(f"{action}: {p}")
    for p, exc in errors:
        print(f"ERROR: {p}: {exc}", file=sys.stderr)

    print(f"\n{action} {len(changed)} file(s). {len(errors)} error(s).")
    if not args.apply and changed:
        print("Re-run with --apply to write changes.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
