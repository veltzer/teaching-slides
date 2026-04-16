#!/usr/bin/env python

"""
Normalize <rect> family fills between solid color and gradient per palette.

Reads resources/palette_diagram.yaml -> effects.rect-fill.style:
  solid:    family-fill rects MUST use fill="var(--{family}-fill)"
  gradient: family-fill rects MUST use fill="url(#grad-{family})"

Family names are discovered from the palette: every group except
"neutrals" defines a {name}-fill role. Neutral rect fills (--bg,
--surface, none) are not touched.

Idempotent.

Usage: svg_fix_gradients.py [--dry-run] svg/**/*.svg
"""

import argparse
import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PALETTE = ROOT / "resources" / "palette_diagram.yaml"

RECT_RE = re.compile(r'<rect\b([^/>]*)/\s*>')
DEFS_RE = re.compile(r'<defs\b.*?</defs>', re.DOTALL)
FILL_RE = re.compile(r'\bfill="([^"]*)"')


def load_policy() -> tuple[str, list[str]]:
    data = yaml.safe_load(PALETTE.read_text(encoding="utf-8"))
    style = data.get("effects", {}).get("rect-fill", {}).get("style", "solid")
    families: list[str] = []
    for group_name, group in data.get("colors", {}).items():
        if group_name == "neutrals":
            continue
        for name in group:
            if name.endswith("-fill"):
                families.append(name[:-len("-fill")])
    return style, families


def transform(text: str, style: str, families: list[str]) -> tuple[str, int]:
    defs_spans = [m.span() for m in DEFS_RE.finditer(text)]

    def in_defs(pos: int) -> bool:
        return any(a <= pos < b for a, b in defs_spans)

    solid_for = {f: f"var(--{f}-fill)" for f in families}
    grad_for = {f: f"url(#grad-{f})" for f in families}
    if style == "gradient":
        from_to = {solid_for[f]: grad_for[f] for f in families}
    elif style == "solid":
        from_to = {grad_for[f]: solid_for[f] for f in families}
    else:
        return text, 0

    out: list[str] = []
    last = 0
    n = 0
    for m in RECT_RE.finditer(text):
        out.append(text[last:m.start()])
        last = m.end()
        if in_defs(m.start()):
            out.append(m.group(0))
            continue
        body = m.group(1)
        fm = FILL_RE.search(body)
        if not fm:
            out.append(m.group(0))
            continue
        fill = fm.group(1).strip()
        target = from_to.get(fill)
        if target is None:
            out.append(m.group(0))
            continue
        new_body = body[:fm.start()] + f'fill="{target}"' + body[fm.end():]
        out.append(f"<rect{new_body}/>")
        n += 1
    out.append(text[last:])
    return "".join(out), n


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    style, families = load_policy()
    print(f"policy: rect-fill.style={style}", file=sys.stderr)

    files_changed = 0
    total = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file() or path.suffix != ".svg":
            continue
        text = path.read_text(encoding="utf-8")
        new, n = transform(text, style, families)
        if n:
            files_changed += 1
            total += n
            if not args.dry_run:
                path.write_text(new, encoding="utf-8")

    action = "would convert" if args.dry_run else "converted"
    print(f"{action} {total} <rect> fill(s) in {files_changed} file(s)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
