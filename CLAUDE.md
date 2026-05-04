# Project Rules

## General
- All project rules must be stored in this file (CLAUDE.md), not only in Claude memory. Memory is not shared with collaborators and can be erased.
- Be strict. Never pass errors silently. Never forgive validation failures. All checks must fail loudly on any error. A script that opens a missing file, parses an empty config, or finds zero results from an expected source must raise — not return an empty result and continue.
- Always prefer project-root-relative includes over file-relative ones (e.g., `svg/courses/...` not `../../../../svg/...`). Marp resolves these via `baseUrl` in `.marprc.mjs`.
- Always build with `rsconstruct build --verbose -j10`.
- **NEVER make semantic content changes with a script.** Do not write or run a script that mass-edits the *meaning* of slides, SVG text, prose, copy, diagram labels, or any human-authored content. This includes: trimming `<text>` elements to fit a word count, dropping bullets, shortening paragraphs, rewriting prose, removing "summary" blocks, deduplicating ideas, or any other content edit. Mechanical/structural changes (e.g., `svg_fix.py --fit` rescaling coordinates, `svg_fix.py --fonts` normalizing font-family) are fine because they preserve meaning. If the build complains about content (too many words, too long, etc.), edit each file by hand, one at a time, with judgment. No exceptions, no "just this once."

## Python
- Use `#!/usr/bin/env python` in shebang lines, never `#!/usr/bin/env python3`. python3 is the default on all systems now.
- All scripts must be executable (`chmod +x`). Run them directly (`./scripts/foo.py`), never via `python scripts/foo.py`.

## Writing presentations or slides
- File naming: `NN_name.md` (e.g., `00_introduction.md`)
- File location: `marp/courses/<domain>/<course-name>/` or `marp/lectures/<domain>/`
- Every file needs YAML front matter: `tags`, `level`, `category`, `audience`
- Title slide (slide 1): only `# Title`, `## Author`, `## Email` — no content, no images
- No empty slides (two consecutive `---` with nothing between them)
- Always close code fences before starting a new slide (`---`)
- Use `1. 1. 1.` for ordered lists, not `1. 2. 3.` — the renderer numbers automatically
- Never number "parts" in slide headings (e.g., `## Part 3: Foo`, `## Part II: Foo`). Reordering slides breaks the numbering. Just use the descriptive title.
- Indent sub-items with 4 spaces: `    - item`
- No mermaid diagrams — prefer SVG (no fast mermaid tool available yet)
- Always use the project SVG color palette: `resources/palette_diagram.yaml`
- No external image URLs — all images must be in `svg/` or `jpg/` directories
- SVG font size must be ≥ 10 (enforced by `scripts/check_svg.py --fonts`)
- All SVG files must use `viewBox="0 0 1280 720"` (16:9, matches Marp slide dimensions). Use `scripts/svg_fix.py --aspect-ratio` to fix existing SVGs.
- A slide with an SVG must contain ONLY the `##` heading and the image line. Any other content (bullets, text, code) must be moved to a separate slide before or after.
- SVG diagrams must NOT include a title inside the SVG. The `##` slide heading serves as the title.
- SVG content must not extend below y=630. Marp renders the `##` heading above the image, so the image is scaled to ~640px tall. Keep viewBox at 1280x720 but treat y=630 as the effective bottom boundary.
- SVG drawing content must be exactly fitted to the usable area [40,1240]x[40,620] (enforced by `scripts/check_svg.py --fit`). Run `scripts/svg_fix.py --fit` to fix.

## Validation
- Check markdown: `scripts/check_md.py` (run via `rsconstruct build --verbose -j10`)
- Check SVGs: `scripts/check_svg.py --dimensions --fonts`
- Verify image refs exist: `scripts/check_md.py --images`
