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

All SVGs share a single color palette defined in `resources/palette_diagram.yaml`
(and `resources/palette_intro.yaml` for title slides). The palette uses
**semantic role names only** — never appearance-based names like "vivid",
"pale", "bright", or "soft". Role names describe WHAT a color is used for,
not what it LOOKS LIKE. This lets us retune the whole visual theme by
editing hex values in one YAML file; every SVG follows automatically.

### The role set

Five semantic families: `primary`, `ok`, `warn`, `danger`, `info`. Each
family has four roles:

- `--{family}-fill` — the box background fill
- `--{family}-border` — matching border / stroke
- `--{family}-text` — text drawn on top of the fill (always readable)
- `--{family}-accent` — deeper shade for emphasis, lines, marker heads

Plus neutrals: `--bg`, `--surface`, `--border`, `--text`, `--text-muted`,
`--text-faint`, `--code-bg`, `--shadow`, `--black`.

### Usage

**Always** use palette variables, not raw hex:

```xml
<rect fill="var(--primary-fill)" stroke="var(--primary-border)"/>
<text fill="var(--primary-text)">label on fill</text>
<line stroke="var(--primary-accent)" marker-end="url(#arrow-primary)"/>
```

NOT:

```xml
<rect fill="#2196f3" stroke="#1565c0"/>
```

AND NOT appearance-named variants (which no longer exist):

```xml
<rect fill="var(--primary-pale2)" stroke="var(--primary-bright)"/>
```

The `check_svg.py --colors` check validates every fill/stroke/color
attribute against the palette YAML. Use `scripts/install_palette.py` to
push the canonical `<defs>` block into every SVG.

## Shape primitives: one canonical way to draw

Colors aren't the only thing that must be uniform. Every rect, circle, and
line in every SVG must share the same visual primitives. Use `scripts/
normalize_svg_style.py` to enforce these; it's idempotent and safe to re-run.

### Rects (boxes)

- **Corner radius:** always `rx="6"`. No sharp boxes, no extra-round boxes.
- **Family-filled box** (fill is `var(--{family}-fill)`):
  - `stroke="var(--{family}-border)"` — matches family
  - `stroke-width="2"`
- **Neutral box** (fill is `var(--surface)`, `var(--bg)`, `none`, or missing):
  - `stroke="var(--border)"` — standard neutral divider
  - `stroke-width="1"`
- Never use gradient fills. `url(#grad-primary)` etc. are flattened to
  `var(--primary-fill)` by the normalizer.

### Lines (connectors)

- Standard connector: `stroke="var(--text-muted)" stroke-width="2"
  marker-end="url(#arrow)"`.
- Emphasis line: `stroke="var(--text)" stroke-width="3"`. Use sparingly.
- `stroke-width` capped at 2 by the normalizer unless explicitly overridden.

### Arrow markers

- Use only the palette markers: `url(#arrow)`, `url(#arrow-primary)`,
  `url(#arrow-ok)`, `url(#arrow-warn)`, `url(#arrow-danger)`,
  `url(#arrow-info)`, `url(#arrow-white)`.
- All palette markers are 10x10. No oversized arrowheads — don't define
  per-file `<marker>` elements with larger dimensions.
  `scripts/fix_svg_markers.py` caps any stray custom markers.

## Placeholders

If you scaffold an SVG before its real content exists (e.g. dropping in
generic "A / B / C / D" boxes so a slide has something to reference), the
SVG must contain the literal string **`PLACEHOLDERSVG`** somewhere inside
it — in a comment or a text element. This makes placeholders trivially
greppable so they can be found and finished later instead of being
shipped by accident.

```xml
<!-- PLACEHOLDERSVG — replace with real diagram -->
```

or

```xml
<text x="40" y="40" fill="var(--text-faint)" font-size="12">PLACEHOLDERSVG</text>
```

Find all placeholders in the repo:

```
grep -rl PLACEHOLDERSVG svg/
```

Never commit a placeholder without the marker. If you see an SVG that
looks placeholder-like but doesn't have the marker, add it.

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
