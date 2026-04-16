#!/usr/bin/env python

"""
Normalize arrow markers across all SVGs.

Every marker-start/mid/end attribute is rewritten to point at one of the
palette's canonical markers:

  arrow          neutral (text-muted)
  arrow-primary  blue / primary
  arrow-ok       green / success
  arrow-warn     orange / warning
  arrow-danger   red / danger
  arrow-info     purple / info
  arrow-white    white (over dark fills)

Custom <marker> definitions outside that set are removed. The mapping from
a custom name to a canonical one uses a name heuristic (looks for
"red"/"danger", "green"/"ok", etc.); if no hint is present the neutral
`arrow` is used.

This replaces the previous size-capping behaviour. The palette markers are
already 10x10 with clean triangles; the old script only resized broken
polygon markers, which didn't help when the polygon was malformed
(e.g. 2-point "triangles" that render as nothing).

Idempotent.

Usage: svg_fix_markers.py [--dry-run] svg/**/*.svg
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

CANONICAL = {"arrow", "arrow-primary", "arrow-ok", "arrow-warn",
             "arrow-danger", "arrow-info", "arrow-white"}

MARKER_DEF_RE = re.compile(
    r'[ \t]*<marker\b[^>]*?id="([^"]+)"[^>]*?>.*?</marker>\n?',
    re.DOTALL,
)
MARKER_REF_RE = re.compile(
    r'\b(marker-(?:start|mid|end))="url\(#([^)]+)\)"'
)


def resolve(name: str) -> str:
    low = name.lower()
    if "white" in low or low.endswith("-bg"):
        return "arrow-white"
    if "red" in low or "danger" in low or "error" in low:
        return "arrow-danger"
    if "green" in low or re.search(r'(^|[^a-z])ok([^a-z]|$)', low) or "success" in low:
        return "arrow-ok"
    if "orange" in low or "warn" in low or "yellow" in low or "amber" in low:
        return "arrow-warn"
    if "blue" in low or "primary" in low or "accent" in low:
        return "arrow-primary"
    if "purple" in low or "info" in low or "mauve" in low:
        return "arrow-info"
    return "arrow"


def transform(text: str) -> tuple[str, int, int]:
    refs_changed = 0
    defs_removed = 0

    def ref_sub(m: re.Match) -> str:
        nonlocal refs_changed
        attr = m.group(1)
        name = m.group(2)
        if name in CANONICAL:
            return m.group(0)
        target = resolve(name)
        refs_changed += 1
        return f'{attr}="url(#{target})"'

    text = MARKER_REF_RE.sub(ref_sub, text)

    def def_sub(m: re.Match) -> str:
        nonlocal defs_removed
        if m.group(1) in CANONICAL:
            return m.group(0)
        defs_removed += 1
        return ""

    text = MARKER_DEF_RE.sub(def_sub, text)
    text = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", text)
    return text, refs_changed, defs_removed


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("paths", nargs="+")
    args = p.parse_args()

    files_changed = 0
    total_refs = 0
    total_defs = 0
    for path_str in args.paths:
        path = pathlib.Path(path_str)
        if not path.is_file() or path.suffix != ".svg":
            continue
        s = path.read_text(encoding="utf-8")
        new, refs, defs = transform(s)
        if refs or defs:
            files_changed += 1
            total_refs += refs
            total_defs += defs
            if not args.dry_run:
                path.write_text(new, encoding="utf-8")

    action = "would update" if args.dry_run else "updated"
    print(f"{action} {files_changed} file(s); rewrote {total_refs} refs, "
          f"removed {total_defs} defs", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
