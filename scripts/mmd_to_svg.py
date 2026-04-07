#!/usr/bin/env python

"""
Convert Mermaid (.mmd) files to SVG using mmdc (mermaid CLI).

Usage (batch mode):
    mmd_to_svg.py source1.mmd target1.svg source2.mmd target2.svg ...

Each source/target pair: reads the Mermaid definition and converts
it to SVG using mmdc, writing the result to the target path.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

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


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 0:
        raise SystemExit(
            "usage: mmd_to_svg.py source1.mmd target1.svg [source2.mmd target2.svg ...]"
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
