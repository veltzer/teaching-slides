#!/usr/bin/env python

"""
Convert Mermaid (.mmd) files to SVG using mmdc (mermaid CLI).

Usage:
    # Single file (output computed automatically under out/mermaid/):
    ./scripts/mmd_to_svg.py mermaid/courses/foo/bar/diagram.mmd

    # Batch mode:
    ./scripts/mmd_to_svg.py mermaid/a.mmd mermaid/b.mmd ...

    # Explicit input/output pairs:
    ./scripts/mmd_to_svg.py -o input.mmd output.svg input2.mmd output2.svg ...
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


def convert(mmd_path: str, svg_path: str, puppeteer_cfg: str) -> bool:
    """Convert one .mmd file to .svg. Returns True on success."""
    out = Path(svg_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["mmdc", "-i", mmd_path, "-o", svg_path, "-b", "transparent",
         "-p", puppeteer_cfg],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"FAIL: {mmd_path}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False
    return True


def compute_output(mmd_path: str) -> str:
    """Compute output SVG path from input .mmd path."""
    p = Path(mmd_path).resolve()
    rel = p.relative_to(MERMAID_DIR)
    return str(OUT_DIR / rel.with_suffix('.svg'))


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(f"Usage: {sys.argv[0]} file.mmd [file2.mmd ...]", file=sys.stderr)
        sys.exit(1)

    # Explicit pairs mode: -o input output input output ...
    if args[0] == '-o':
        pairs = args[1:]
        if len(pairs) < 2 or len(pairs) % 2 != 0:
            print(f"Usage: {sys.argv[0]} -o input.mmd output.svg [...]",
                  file=sys.stderr)
            sys.exit(1)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as cfg:
            json.dump(PUPPETEER_CONFIG, cfg)
            cfg.flush()
            failures = sum(
                0 if convert(pairs[i], pairs[i + 1], cfg.name) else 1
                for i in range(0, len(pairs), 2)
            )
        sys.exit(1 if failures else 0)

    # Auto mode: compute output paths from input paths
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as cfg:
        json.dump(PUPPETEER_CONFIG, cfg)
        cfg.flush()
        failures = sum(
            0 if convert(mmd, compute_output(mmd), cfg.name) else 1
            for mmd in args
        )
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
