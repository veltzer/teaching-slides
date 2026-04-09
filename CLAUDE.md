# Project Rules

## General
- All project rules must be stored in this file (CLAUDE.md), not only in Claude memory. Memory is not shared with collaborators and can be erased.
- Always prefer project-root-relative includes over file-relative ones (e.g., `svg/courses/...` not `../../../../svg/...`). Marp resolves these via `baseUrl` in `.marprc.mjs`.
- Always build with `rsconstruct build --verbose -j10`.

## Python
- Use `#!/usr/bin/env python` in shebang lines, never `#!/usr/bin/env python3`. python3 is the default on all systems now.
- All scripts must be executable (`chmod +x`). Run them directly (`./scripts/foo.py`), never via `python scripts/foo.py`.

## Writing presentations or slides
- read "doc/HowToWriteSlides.txt"
- All SVG files must use `viewBox="0 0 1280 720"` (16:9, matches Marp slide dimensions). Use `scripts/fix_svg_aspect_ratio.py` to fix existing SVGs.
- A slide with an SVG must contain ONLY the `##` heading and the image line. Any other content (bullets, text, code) must be moved to a separate slide before or after.
