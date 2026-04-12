# How to Write SVG in This Project

This document covers everything about authoring and maintaining SVG diagrams
used in our Marp-rendered slides.

## File layout

- All SVGs live in `svg/` (organized as `svg/courses/...` or `svg/lectures/...`).
- Reference them from slides using project-root-relative paths, e.g.
  `![](svg/courses/languages/python/advanced-python/03_memory/python_memory_management_levels.svg)`.
  Marp resolves these via `baseUrl` in `.marprc.mjs`. Do NOT use
  `../../../../svg/...`.
- Do NOT reference external images via `http://` or `https://` URLs. All
  images must be local files in `svg/` or `jpg/`.
- Do NOT use inline SVG in markdown. Always write the SVG as an external file
  and reference it. This broken pattern is NOT allowed:

  ```marp
  <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <circle cx="100" cy="100" r="80" fill="#f0f0f0" stroke="#333"/>
  </svg>
  ```

## Dimensions and bounds

- Every SVG must use exactly `viewBox="0 0 1280 720"` (16:9, matches Marp
  slide dimensions). Do NOT use 1280x640 — that 2:1 aspect ratio makes Marp
  distort or mis-center the image. Use `scripts/fix_svg_aspect_ratio.py` to
  convert existing SVGs. The `check_svg.py --dimensions` check enforces this.
- SVG content must not extend below **y=630**. Marp renders the slide's `##`
  heading at the top of the page, pushing the image down; the bottom ~80px
  becomes a buffer. Keep the viewBox at 1280x720 but treat y=630 as the
  effective bottom boundary.
- Background rects should use `height=640` (not 720) for the same reason.
- Do NOT put a title element inside the SVG. The slide's `##` heading IS the
  title. Duplicating it wastes vertical space.

## Slide composition rules

- A slide that contains an SVG must have ONLY the `##` heading and the image
  reference. No bullets, no paragraphs, no code before or after the image.
  If you have commentary, put it on a separate slide before or after.
- If a slide has text AND an SVG (uncommon — prefer splitting), the SVG may
  have at most ONE line of text above OR below it, not both.

## Colors: use the palette, always

All SVGs share a single color palette defined in `resources/svg_palette.svg`.
The palette declares CSS custom properties (CSS variables) for every semantic
role: `--primary`, `--ok`, `--warn`, `--danger`, `--info`, plus neutrals and
many tonal variants. See `resources/svg_palette.svg` for the complete list
and hex mappings.

**Always** use palette variables for color, not raw hex:

```xml
<rect fill="var(--primary-pale2)" stroke="var(--primary-bright)"/>
<text fill="var(--text-muted)">label</text>
```

NOT:

```xml
<rect fill="#e8f4f8" stroke="#4a90e2"/>
```

This keeps the look consistent across every diagram and lets us retune the
palette in one place. Use `scripts/install_palette.py` to push the canonical
`<defs>` block into every SVG.

## Fonts and readability

- SVG diagrams must use `font-size` ≥ 10. Smaller is unreadable when
  projected. The `check_svg.py --fonts` check enforces this.

## File format rules

- SVGs must be properly formatted multi-line XML. Never generate single-line
  SVGs or truncated stubs. Each SVG should have at least 5 XML elements.
- No duplicate XML attributes.
- **Do NOT use XML namespace prefixes on the root `<svg>` element or its
  children.** See "The ns0: trap" below — this has broken us before.

## The ns0: trap (what NOT to do)

Some XML processing tools will rewrite a clean SVG like this:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect fill="var(--primary-pale2)"/>
</svg>
```

Into this:

```xml
<ns0:svg xmlns:ns0="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <ns0:rect fill="var(--primary-pale2)"/>
</ns0:svg>
```

Both are technically valid XML and look the same to XML parsers. **But they
do not render the same.**

The palette defines CSS variables inside a `<style>` block scoped to the
`svg` and `:root` selectors:

```xml
<defs>
  <style>
    :root, svg {
      --primary-pale2: #e8f4f8;
      /* ... */
    }
  </style>
</defs>
```

The CSS selector `svg` does NOT match the element `ns0:svg` — it's the wrong
namespace. So the CSS custom properties are never defined on the element,
every `fill="var(--primary-pale2)"` resolves to nothing, and the browser
falls back to the default paint: **solid black**.

Symptom: your diagrams render as black boxes on a black background in the
actual Marp output. This affected 2,031 files (61% of all SVGs) before it
was caught in April 2026.

**Fix:** run `scripts/fix_svg_namespace.py`. It strips the `ns0:` prefix
from every affected SVG (root declaration and all child elements) while
leaving all palette references intact. The script is idempotent and safe to
re-run.

**Prevention:** when generating or editing SVGs programmatically, configure
the XML serializer to use the default namespace, not a prefixed one. After
any bulk transform, sanity-check at least one file by opening it in a
browser or rendering a Marp deck — black-box regressions are obvious once
you look.

## General guidance

- Look at existing SVGs near the one you're writing — match their style,
  typography, and palette usage.
- Prefer SVG to Mermaid diagrams. Avoid ASCII-art diagrams entirely.

## Validation commands

- `scripts/check_svg.py --dimensions --fonts` — enforce viewBox and font-size
- `scripts/check_svg.py --colors` — enforce palette compliance
- `scripts/check_md.py --images` — verify all image references resolve
- `scripts/find_unused_svgs.py` — list SVGs no slide references
- `scripts/fix_svg_aspect_ratio.py` — normalize viewBox to 1280x720
- `scripts/fix_svg_namespace.py` — strip ns0: prefix (see above)
- `scripts/install_palette.py` — push canonical palette defs into every SVG
- `rsconstruct build --verbose -j10` — full build (runs `check_md.py`)
