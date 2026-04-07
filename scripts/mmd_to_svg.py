#!/usr/bin/env python

"""
Convert Mermaid (.mmd) files to SVG using mmdc (mermaid CLI).

Usage (batch mode, called by rsconstruct):
    mmd_to_svg.py source1.mmd source2.mmd ...

Output SVGs are written under out/mermaid/ mirroring the mermaid/ structure.

Also supports explicit source/target pairs:
    mmd_to_svg.py source1.mmd target1.svg source2.mmd target2.svg ...
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MERMAID_DIR = ROOT / 'mermaid'
OUT_DIR = ROOT / 'out' / 'mermaid'
PUPPETEER_CONFIG = {"args": ["--no-sandbox"]}


def convert(mmd_path: str, svg_path: str, puppeteer_cfg: str) -> None:
    """Convert one .mmd file to .svg."""
    Path(svg_path).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["mmdc", "-i", mmd_path, "-o", svg_path, "-b", "transparent",
         "-p", puppeteer_cfg],
        capture_output=True,
        text=True,
        check=True,
    )


def compute_output(mmd_path: str) -> str:
    """Compute output SVG path from input .mmd path."""
    p = Path(mmd_path).resolve()
    rel = p.relative_to(MERMAID_DIR)
    return str(OUT_DIR / rel.with_suffix('.svg'))


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 0:
        raise SystemExit(
            "usage: mmd_to_svg.py source1.mmd [source2.mmd ...]"
        )

    # Detect mode: if all args end with .mmd, compute outputs automatically.
    # If args alternate .mmd/.svg, treat as explicit pairs.
    all_mmd = all(a.endswith('.mmd') for a in args)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as cfg:
        json.dump(PUPPETEER_CONFIG, cfg)
        cfg.flush()
        if all_mmd:
            for mmd in args:
                convert(mmd, compute_output(mmd), cfg.name)
        else:
            if len(args) % 2 != 0:
                raise SystemExit(
                    f"expected even number of arguments (source/target pairs), got {len(args)}"
                )
            for i in range(0, len(args), 2):
                convert(args[i], args[i + 1], cfg.name)


if __name__ == '__main__':
    main()
