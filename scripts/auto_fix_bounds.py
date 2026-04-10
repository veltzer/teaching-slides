#!/usr/bin/env python

import re
import xml.etree.ElementTree as ET
from pathlib import Path

# Import scaling logic from rescale_svgs
import rescale_svgs

def get_actual_bounds(tree):
    max_x, max_y = 0, 0
    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]
        x_max = 0
        y_max = 0
        try:
            if tag in ('rect', 'image', 'foreignObject'):
                x = float(elem.get('x', '0').replace('px', ''))
                w = float(elem.get('width', '0').replace('px', ''))
                x_max = x + w
                
                y = float(elem.get('y', '0').replace('px', ''))
                h = float(elem.get('height', '0').replace('px', ''))
                y_max = y + h
            elif tag in ('text', 'use'):
                x = float(elem.get('x', '0').replace('px', ''))
                x_max = x
                y = float(elem.get('y', '0').replace('px', ''))
                y_max = y
            elif tag in ('circle', 'ellipse'):
                cx = float(elem.get('cx', '0').replace('px', ''))
                cy = float(elem.get('cy', '0').replace('px', ''))
                if tag == 'circle':
                    r = float(elem.get('r', '0').replace('px', ''))
                    x_max = cx + r
                    y_max = cy + r
                else:
                    rx = float(elem.get('rx', '0').replace('px', ''))
                    ry = float(elem.get('ry', '0').replace('px', ''))
                    x_max = cx + rx
                    y_max = cy + ry
            elif tag == 'line':
                x1 = float(elem.get('x1', '0').replace('px', ''))
                x2 = float(elem.get('x2', '0').replace('px', ''))
                y1 = float(elem.get('y1', '0').replace('px', ''))
                y2 = float(elem.get('y2', '0').replace('px', ''))
                x_max = max(x1, x2)
                y_max = max(y1, y2)
            elif tag == 'path':
                # very crude, just parse all numbers
                d = elem.get('d', '')
                nums = [float(n) for n in re.findall(r'[-+]?(?:\d+\.?\d*|\.\d+)', d)]
                if nums:
                    x_max = max(nums)
                    y_max = max(nums) # Crude but safeish if they are interleaved
        except ValueError:
            pass
        
        max_x = max(max_x, x_max)
        max_y = max(max_y, y_max)
        
    return max_x, max_y

def main():
    svg_root = Path("svg")
    files = sorted(svg_root.rglob("*.svg"))
    
    modified = 0
    for f in files:
        try:
            tree = ET.parse(f)
        except ET.ParseError:
            continue
            
        root = tree.getroot()
        max_x, max_y = get_actual_bounds(tree)
        
        if max_y > 640 or max_x > 1280:
            scale_y = 640 / max_y if max_y > 640 else 1.0
            scale_x = 1280 / max_x if max_x > 1280 else 1.0
            s = min(scale_x, scale_y)
            
            print(f"Fixing {f}: max_y={max_y}, max_x={max_x}, scaling by {s}")
            
            # Now scale all elements
            for child in root:
                rescale_svgs.walk_and_scale(child, s, s, s)
            rescale_svgs.scale_element(root, s, s, s)
                
            ET.indent(tree, space="  ")
            tree.write(str(f), encoding="unicode", xml_declaration=False)
            
            # Restore <?xml ...?> if needed
            content = f.read_text(encoding="utf-8")
            if not content.startswith("<svg") and not content.startswith("<?"):
                pass
            
            modified += 1
            
    print(f"Fixed {modified} files")

if __name__ == '__main__':
    main()
