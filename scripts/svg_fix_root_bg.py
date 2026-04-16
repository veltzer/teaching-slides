#!/usr/bin/env python

"""
Ensure every SVG's root <svg> element carries style="background:var(--bg)"
so the slide background is white (or whatever the palette says) regardless
of the surrounding viewer.

Idempotent. If a style attribute already exists with a background declaration
it is left alone. If style exists without background, the background is
prepended. If style is absent it is added.

Usage: svg_fix_root_bg.py [--dry-run] svg/**/*.svg
"""

import argparse
import pathlib
import re
import sys

SVG_OPEN_RE = re.compile(r'<svg\b([^>]*)>')
STYLE_RE = re.compile(r'\bstyle="([^"]*)"')
BG_DECL = "background:var(--bg)"


def transform(text: str) -> tuple[str, bool]:
    m = SVG_OPEN_RE.search(text)
    if not m:
        return text, False
    body = m.group(1)
    sm = STYLE_RE.search(body)
    if sm:
        style_val = sm.group(1)
        if "background" in style_val:
            return text, False
        new_style = f"{BG_DECL};{style_val.strip()}"
        new_body = body[:sm.start()] + f'style="{new_style}"' + body[sm.end():]
    else:
        new_body = body.rstrip() + f' style="{BG_DECL}"'
    new_text = text[:m.start()] + f"<svg{new_body}>" + text[m.end():]
    return new_text, True


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    changed = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file() or path.suffix != ".svg":
            continue
        text = path.read_text(encoding="utf-8")
        new, did = transform(text)
        if did:
            changed += 1
            if not args.dry_run:
                path.write_text(new, encoding="utf-8")

    action = "would update" if args.dry_run else "updated"
    print(f"{action} {changed} file(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
