#!/usr/bin/env python

import xml.etree.ElementTree as ET
from pathlib import Path
import re

# Register the SVG namespace as the default (unprefixed) namespace before any
# parse/write. Without this, ElementTree serializes the root as <ns0:svg ...>,
# which breaks the palette's CSS variable resolution (selectors target "svg",
# not "ns0:svg"). See doc/HowToWriteSVG.md, section "The ns0: trap".
ET.register_namespace("", "http://www.w3.org/2000/svg")

def fix_fonts(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return False
        
    modified = False
    for elem in tree.iter():
        fs = elem.get('font-size')
        if fs:
            try:
                # Handle '12px' or '10.5'
                m = re.match(r'^(-?[\d.]+)(px|pt|em|%)?$', fs.strip())
                if m:
                    val = float(m.group(1))
                    unit = m.group(2) or ''
                    if val < 10:
                        elem.set('font-size', f"10{unit}")
                        modified = True
            except ValueError:
                pass
                
        style = elem.get('style', '')
        if style and 'font-size' in style:
            def fix_style_prop(m):
                nonlocal modified
                val = float(m.group(2))
                unit = m.group(3) or ''
                if val < 10:
                    modified = True
                    return f"font-size:10{unit}"
                return m.group(0)
            new_style = re.sub(r'font-size:\s*([\d.]+)(px|pt|em|%)?', fix_style_prop, style)
            if new_style != style:
                elem.set('style', new_style)
                modified = True
                
    if modified:
        ET.indent(tree, space="  ")
        tree.write(str(path), encoding="unicode", xml_declaration=False)
        return True
    return False

def main():
    svg_root = Path("svg")
    files = sorted(svg_root.rglob("*.svg"))
    modified = 0
    for f in files:
        if fix_fonts(f):
            modified += 1
            print(f"Fixed fonts in {f}")
    print(f"Fixed fonts in {modified} files")

if __name__ == '__main__':
    main()
