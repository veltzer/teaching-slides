#!/usr/bin/env python

"""
Add or strip filter="url(#shadow)" on <rect> elements per palette policy.

Reads resources/palette_diagram.yaml -> effects.rect-shadow:
  enabled: bool
  apply-to: family-only | all | none

Family-fill colors (those that should be shadowed under family-only) are
discovered from the palette: any color name ending in "-fill" that lives
in a non-neutral group.

Rects inside <defs> are ignored. The script is idempotent.

Usage: fix_svg_shadows.py [--dry-run] svg/**/*.svg
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
ATTR_RE = re.compile(r'\b([\w-]+)="([^"]*)"')
FILTER_ATTR_RE = re.compile(r'\s*filter="[^"]*"')
FILTER_DEF = (
    '<filter id="shadow" x="-4%" y="-8%" width="108%" height="124%">'
    '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#00000022"/>'
    '</filter>'
)


def load_policy() -> tuple[bool, str, set[str]]:
    data = yaml.safe_load(PALETTE.read_text(encoding="utf-8"))
    eff = data.get("effects", {}).get("rect-shadow", {})
    enabled = bool(eff.get("enabled", False))
    apply_to = eff.get("apply-to", "none")
    if not enabled:
        apply_to = "none"

    family_fills: set[str] = set()
    for group_name, group in data.get("colors", {}).items():
        if group_name == "neutrals":
            continue
        for name in group:
            if name.endswith("-fill"):
                family_fills.add(f"var(--{name})")
    return enabled, apply_to, family_fills


def needs_shadow(rect_attrs: dict[str, str], apply_to: str,
                 family_fills: set[str]) -> bool:
    if apply_to == "none":
        return False
    if apply_to == "all":
        return True
    if apply_to == "family-only":
        return rect_attrs.get("fill", "").strip() in family_fills
    return False


def transform(text: str, apply_to: str, family_fills: set[str]) -> tuple[str, int, int]:
    defs_spans = [m.span() for m in DEFS_RE.finditer(text)]

    def in_defs(pos: int) -> bool:
        return any(a <= pos < b for a, b in defs_spans)

    out: list[str] = []
    last = 0
    added = 0
    removed = 0
    for m in RECT_RE.finditer(text):
        out.append(text[last:m.start()])
        last = m.end()
        if in_defs(m.start()):
            out.append(m.group(0))
            continue
        body = m.group(1)
        attrs = dict(ATTR_RE.findall(body))
        has_filter = "filter" in attrs and "url(#shadow)" in attrs["filter"]
        want = needs_shadow(attrs, apply_to, family_fills)

        if want and not has_filter:
            new_body = body.rstrip()
            new_body += ' filter="url(#shadow)"'
            out.append(f"<rect{new_body}/>")
            added += 1
        elif has_filter and not want:
            new_body = FILTER_ATTR_RE.sub("", body)
            new_body = re.sub(r"\s+/\s*$", "", new_body)
            out.append(f"<rect{new_body}/>")
            removed += 1
        else:
            out.append(m.group(0))

    out.append(text[last:])
    return "".join(out), added, removed


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    enabled, apply_to, family_fills = load_policy()
    print(f"policy: enabled={enabled} apply-to={apply_to}", file=sys.stderr)

    files_changed = 0
    total_added = 0
    total_removed = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file() or path.suffix != ".svg":
            continue
        text = path.read_text(encoding="utf-8")
        new, added, removed = transform(text, apply_to, family_fills)
        # If we added shadows but the filter def is missing, inject it.
        if added and 'id="shadow"' not in new:
            if "<defs>" in new:
                new = new.replace("<defs>", "<defs>\n    " + FILTER_DEF, 1)
            elif "<defs " in new:
                new = re.sub(r"(<defs\b[^>]*>)",
                             r"\1\n    " + FILTER_DEF, new, count=1)
            else:
                # No <defs> at all — inject one right after the opening <svg ...>
                new = re.sub(
                    r"(<svg\b[^>]*>)",
                    r"\1\n  <defs>\n    " + FILTER_DEF + "\n  </defs>",
                    new, count=1,
                )
        if added or removed:
            files_changed += 1
            total_added += added
            total_removed += removed
            if not args.dry_run:
                path.write_text(new, encoding="utf-8")

    action = "would change" if args.dry_run else "changed"
    print(f"{action} {files_changed} file(s); +{total_added} shadows, "
          f"-{total_removed} shadows", file=sys.stderr)


if __name__ == "__main__":
    main()
