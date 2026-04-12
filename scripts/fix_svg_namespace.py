#!/usr/bin/env python
"""
Remove the ns0: XML namespace prefix from SVG files.

Some tool chain step rewrote <svg xmlns="..."> as <ns0:svg xmlns:ns0="...">
and prefixed every child element with ns0:. The SVG is still valid XML, but
the palette's CSS variables (defined inside <style> scoped to the "svg"
selector) no longer apply because the selector does not match a namespaced
ns0:svg root element. Result: every fill="var(--primary-pale2)" falls back
to black in Marp/Chromium rendering.

This script strips the prefix everywhere it appears, restoring the default
namespace. Palette references (var(--...)) are untouched.
"""
from pathlib import Path
import sys

SVG_NAMESPACE = 'http://www.w3.org/2000/svg'


def fix_svg(path: Path) -> bool:
    """Return True if file was modified."""
    content = path.read_text(encoding="utf-8")

    if 'xmlns:ns0=' not in content and '<ns0:' not in content:
        return False

    new_content = content
    new_content = new_content.replace(f'xmlns:ns0="{SVG_NAMESPACE}"', f'xmlns="{SVG_NAMESPACE}"')
    new_content = new_content.replace('<ns0:', '<')
    new_content = new_content.replace('</ns0:', '</')

    if new_content == content:
        return False

    path.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    svg_root = repo_root / 'svg'

    fixed = 0
    scanned = 0
    for svg_path in sorted(svg_root.rglob('*.svg')):
        scanned += 1
        if fix_svg(svg_path):
            fixed += 1
            print(f'fixed: {svg_path.relative_to(repo_root)}')

    print(f'\n{fixed} files fixed out of {scanned} scanned')
    return 0


if __name__ == '__main__':
    sys.exit(main())
