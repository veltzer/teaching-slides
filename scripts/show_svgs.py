#!/usr/bin/env python

"""
Show all SVGs from svg/ in a browser as a scrollable grid.

  show_svgs.py            # all SVGs
  show_svgs.py --sample N # random sample of N SVGs

Generates /tmp/show_svgs.html and opens it.
"""

import argparse
import html
import pathlib
import random
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "svg"
OUT = pathlib.Path("/tmp/show_svgs.html")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sample", type=int, default=None,
                   help="show only N random SVGs")
    p.add_argument("--seed", type=int, default=None,
                   help="seed for --sample (reproducible)")
    args = p.parse_args()

    paths = sorted(SVG_DIR.rglob("*.svg"))
    if not paths:
        print("no SVGs found", file=sys.stderr)
        sys.exit(1)

    if args.sample:
        if args.seed is not None:
            random.seed(args.seed)
        paths = random.sample(paths, min(args.sample, len(paths)))
        paths.sort()

    parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        f"<title>SVG gallery ({len(paths)} slides)</title>",
        "<style>",
        "body{margin:0;padding:16px;background:#222;color:#eee;",
        "font-family:system-ui,sans-serif}",
        ".grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}",
        ".cell{background:#fff;border-radius:6px;overflow:hidden;",
        "display:flex;flex-direction:column}",
        ".cell img{width:100%;height:auto;display:block}",
        ".cell .cap{padding:8px 12px;background:#333;color:#ddd;",
        "font-size:12px;font-family:monospace;word-break:break-all}",
        "h1{font-size:18px;margin:0 0 12px}",
        "</style></head><body>",
        f"<h1>{len(paths)} slides — {SVG_DIR}</h1>",
        "<div class='grid'>",
    ]
    for p in paths:
        rel = p.relative_to(ROOT)
        src = "file://" + str(p)
        parts.append(
            f"<div class='cell'><img src='{html.escape(src)}' "
            f"loading='lazy'><div class='cap'>{html.escape(str(rel))}"
            f"</div></div>"
        )
    parts.append("</div></body></html>")

    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {OUT} ({len(paths)} slides)", file=sys.stderr)
    subprocess.Popen(["xdg-open", str(OUT)],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
