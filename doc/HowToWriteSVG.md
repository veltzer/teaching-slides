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
  distort or mis-center the image. Use `scripts/svg_fix.py --aspect-ratio` to
  convert existing SVGs. The `check_svg.py --dimensions` check enforces this.
- SVG content must not extend below **y=630**. Marp renders the slide's `##`
  heading at the top of the page, pushing the image down; the bottom ~80px
  becomes a buffer. Keep the viewBox at 1280x720 but treat y=630 as the
  effective bottom boundary.
- **Do not use background rects.** SVGs should have no full-slide
  background rectangle — the slide itself provides the background. A
  background rect adds visual weight (a framed card inside the slide),
  wastes edge pixels, and duplicates what Marp already draws. Content
  should sit directly on the transparent canvas.
- *(Out of date — superseded by the rule above.)* ~~Background rects
  should use `height=640` (not 720) for the same reason.~~
- Do NOT put a title element inside the SVG. The slide's `##` heading IS the
  title. Duplicating it wastes vertical space.

## Fill the usable area

Every SVG's drawing content should fill the usable area — the rectangle
`x ∈ [40, 1240], y ∈ [40, 620]` (1200×580). A diagram that only occupies a
thin band in the middle of the slide wastes screen real estate and looks
amateurish next to its well-filled neighbours.

- **Design the content to fill the full 1200×580** from the start. Use a
  layout that matches the topic (4-column comparison, flow with arrows,
  left/right split, 2×2 grid, etc.) and stretch it to the edges.
- **Do not rely on svg_fix.py --fit to rescue a tiny diagram.** The fit
  script stretches content to fit, but extreme scale ratios (>1.5×) trigger
  a uniform-scale fallback that leaves letterbox space — see "Why circles
  don't stretch like rects" below.
- **The fill ratio** is `content bbox area / (1200 × 580)`. Aim for ≥ 90%.
  Below 40% is a failure and the build will reject it. Values in the
  40–70% band are acceptable but worth improving.
- `scripts/svg_fix.py --fit` is idempotent and exact: it centers content
  on integer pixels and re-runs are no-ops. Run after authoring an SVG.
- `scripts/check_svg.py --fill` enforces the minimum fill ratio.

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

Colors aren't the only thing that must be uniform. Every rect and line in
every SVG must share the same visual primitives. The individual `svg_fix.py`
scripts enforce these (shadows, gradients, fonts, markers, etc.).

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
  `scripts/svg_fix.py --markers` caps any stray custom markers.

## Do not use circles in drawings

Circles are locked to a 1:1 aspect ratio — a `<circle>` has only `r`, so it
cannot stretch independently on x and y. Rectangles have `width` and
`height` and scale freely on each axis. This makes circles brittle under
the fit-to-slide pass (see below) and awkward to compose into layouts.

**Rule:** do not introduce `<circle>` elements in new SVGs. Use `<rect>`
(with `rx` for rounded corners) or `<ellipse>` if a round shape is truly
necessary. Existing circles may remain until rewritten.

**Exception:** title slides (`title.svg`) are decorative rather than
informational and may use circles freely. `check_svg.py --no-circles`
skips files named `title.svg`.

## Why circles don't stretch like rects

When you run `scripts/svg_fix.py --fit`, every diagram gets stretched so
its content bounding box fills the usable area exactly (`x ∈ [40, 1240]`,
`y ∈ [40, 620]`). That works beautifully for diagrams built from rectangles
and text. But **circles don't stretch correctly under non-uniform scaling**,
and this is why the fit script has a fallback to uniform scale for
circle-heavy diagrams.

### The root cause

An SVG `<rect>` has two independent dimensions — `width` and `height`. Scale
the rect by `(sx=2, sy=0.8)` and it becomes 2× wider and 0.8× taller. Each
axis is controlled separately. A 100×100 rect becomes 200×80. Clean.

An SVG `<circle>` has only one dimension — `r`. A circle is "all points at
distance r from (cx, cy)." There's no way to tell a `<circle>` to be twice
as wide as it is tall; that shape is an **ellipse**, which is a different
element (`<ellipse>` with `rx` and `ry`).

So when the fit script encounters a `<circle>` under non-uniform scale, it
has three bad options:

1. **Average the two scales** (what the script does by default, using the
   geometric mean). The circle stays a circle but ends up the wrong size on
   both axes. If the original bbox had `sx=2, sy=0.8`, the circle scales by
   `√(2 × 0.8) ≈ 1.26` — too small horizontally, too big vertically.
2. **Use sx for radius** — circle is the right horizontal size but wrong
   vertical size.
3. **Use sy for radius** — mirror problem.

All three leave the circle in a position where the next run of the fit
script computes a different bbox (because the circle's contribution to the
bbox changed), producing a different scale, oscillating forever. The fit
script is not idempotent on circle-heavy diagrams under heavy stretch.

### The fallback

If the required stretch is severe (ratio of `sx` to `sy` exceeds 1.5×), the
fit script falls back to **uniform scale**: it picks the smaller of `sx`
and `sy` and uses it for both axes. The content is scaled uniformly and
centered in the usable area, letterboxed on the axis it doesn't fill.
Circles stay circles. Idempotent.

The trade-off: circle-heavy diagrams don't fill the slide edge-to-edge the
way rect-based diagrams do. If your diagram's content naturally has an
extreme aspect ratio (e.g. a tall concentric-rings diagram), it will fit
centered rather than stretched.

### How to avoid letterboxing

- Use `<ellipse>` instead of `<circle>` if you actually want the shape to
  deform under non-uniform scaling.
- Design diagrams with a moderate aspect ratio (wider than they are tall,
  ideally close to 16:9) so the fit produces reasonable `sx`/`sy` values
  without triggering the fallback.
- Avoid making a single giant circle the dominant element — its radius
  forces the bbox aspect ratio.

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

## Word count: diagrams are not paragraphs

A diagram is a picture, not a document. Audiences read a slide in seconds;
they listen to the speaker for the rest. If a diagram contains more prose
than a few labels and short phrases, the prose belongs in speaker notes
or on a separate text-only slide.

**Limit: 60 words** across all `<text>` and `<tspan>` content in an SVG.
Enforced by `scripts/check_svg.py --words`.

- Aim much lower when you can — the median diagram in this repo is around
  30 words. Under 30 is ideal; under 15 is great.
- Enforced by `scripts/check_svg.py --words` (on by default, max 100).

### What to cut

- **Long explanatory panels** ("Key ideas", "How it works", "Watch-outs"
  blocks at the bottom). These are a paragraph pretending to be a diagram.
  Move them to the slide's speaker notes or a separate text-only slide.
- **Sentences inside boxes.** A box label should be 1 header + 1–2 short
  lines (≤ 4 words each), not a sentence.
- **Every parenthetical you could drop.** "(optional)", "(default 10MB)",
  "(runs once per row)" — usually unnecessary in a diagram.
- **Redundant labels.** If an arrow is obvious from context, don't label it.
  If the box color already encodes the category, the box doesn't need a
  category label too.

### What to keep

- Short labels: node names, function names, state names.
- Single-line formulas or code fragments when they are the point of the
  diagram.
- A one-line caption / title at the top if the slide heading alone doesn't
  convey what the picture shows.

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

**Fix:** the repo was scrubbed of `ns0:` prefixes in April 2026, and
`check_svg.py --namespace` now rejects any SVG whose root is missing
`xmlns="http://www.w3.org/2000/svg"` or lives in a non-SVG namespace — so
the bug cannot reappear silently.

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
- `scripts/svg_fix.py --aspect-ratio` — normalize viewBox to 1280x720
- `scripts/install_palette.py` — push canonical palette defs into every SVG
- `rsconstruct build --verbose -j10` — full build (runs `check_md.py`)
