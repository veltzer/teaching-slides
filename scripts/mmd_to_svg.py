#!/usr/bin/env python

"""
Convert Mermaid (.mmd) files to SVG using mmdc (mermaid CLI).

Usage (batch mode):
    mmd_to_svg.py source1.mmd target1 source2.mmd target2 ...

Called by rsconstruct generator processor. The target path from rsconstruct
is used as a stamp file. The actual SVG output mirrors the mermaid/ structure
under out/mermaid/ with .svg extension.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MERMAID_DIR = ROOT / 'mermaid'
SVG_OUT_DIR = ROOT / 'out' / 'mermaid'
PUPPETEER_CONFIG = {"args": ["--no-sandbox"]}


def compute_svg_path(mmd_path: str) -> str:
    """Compute output SVG path from input .mmd path."""
    p = Path(mmd_path).resolve()
    rel = p.relative_to(MERMAID_DIR)
    return str(SVG_OUT_DIR / rel.with_suffix('.svg'))


def convert(mmd_path: str, stamp_path: str, puppeteer_cfg: str) -> None:
    """Convert one .mmd file to .svg and touch the stamp file."""
    svg_path = compute_svg_path(mmd_path)
    Path(svg_path).parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["mmdc", "-i", mmd_path, "-o", svg_path, "-b", "transparent",
         "-p", puppeteer_cfg],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"mmdc failed for {mmd_path}:\n{result.stderr}"
        )
    # Touch the stamp file so rsconstruct knows this target is done
    stamp = Path(stamp_path)
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text("")


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 0:
        raise SystemExit(
            "usage: mmd_to_svg.py source1.mmd target1 [source2.mmd target2 ...]"
        )
    if len(args) % 2 != 0:
        raise SystemExit(
            f"expected even number of arguments (source/target pairs), got {len(args)}"
        )

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as cfg:
        json.dump(PUPPETEER_CONFIG, cfg)
        cfg.flush()
        for i in range(0, len(args), 2):
            convert(args[i], args[i + 1], cfg.name)


if __name__ == '__main__':
    main()
