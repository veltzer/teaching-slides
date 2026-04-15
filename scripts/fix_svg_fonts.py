#!/usr/bin/env python

"""
Normalize <text> and <tspan> font-family across every SVG.

Reads resources/palette_diagram.yaml -> typography:
  sans: "Arial, sans-serif"
  mono: "Courier New, monospace"

Rules per element:
  - If existing font-family contains "mono" or "courier" (case-insensitive),
    set it to typography.mono.
  - Otherwise (or if missing), set it to typography.sans.

Idempotent. Run after authoring or to re-skin the typography in one pass.

Usage: fix_svg_fonts.py [--dry-run] svg/**/*.svg
"""

import argparse
import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PALETTE = ROOT / "resources" / "palette_diagram.yaml"

ELEM_RE = re.compile(r'<(text|tspan)\b([^>]*?)(/?)>')
FONT_FAMILY_RE = re.compile(r'\s*font-family="[^"]*"')


def load_typography() -> tuple[str, str]:
    data = yaml.safe_load(PALETTE.read_text(encoding="utf-8"))
    typo = data.get("typography", {})
    return (
        typo.get("sans", "Arial, sans-serif"),
        typo.get("mono", "Courier New, monospace"),
    )


def transform(text: str, sans: str, mono: str) -> tuple[str, int]:
    changed = 0

    def fix(m: re.Match) -> str:
        nonlocal changed
        tag = m.group(1)
        attrs = m.group(2)
        slash = m.group(3)
        existing = re.search(r'font-family="([^"]*)"', attrs)
        current = existing.group(1) if existing else ""
        is_mono = bool(re.search(r'(mono|courier)', current, re.IGNORECASE))
        target = mono if is_mono else sans
        if current == target:
            return m.group(0)
        # Strip any existing font-family attribute(s).
        new_attrs = FONT_FAMILY_RE.sub("", attrs).rstrip()
        new_attrs = (new_attrs + " " if new_attrs and not new_attrs.endswith(" ") else new_attrs)
        new_attrs += f'font-family="{target}"'
        if not new_attrs.startswith(" "):
            new_attrs = " " + new_attrs
        changed += 1
        return f"<{tag}{new_attrs}{slash}>"

    return ELEM_RE.sub(fix, text), changed


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    sans, mono = load_typography()
    print(f"typography: sans={sans!r}  mono={mono!r}", file=sys.stderr)

    files_changed = 0
    total_changes = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file() or path.suffix != ".svg":
            continue
        text = path.read_text(encoding="utf-8")
        new, n = transform(text, sans, mono)
        if n:
            files_changed += 1
            total_changes += n
            if not args.dry_run:
                path.write_text(new, encoding="utf-8")

    action = "would update" if args.dry_run else "updated"
    print(f"{action} {total_changes} element(s) in {files_changed} file(s)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
