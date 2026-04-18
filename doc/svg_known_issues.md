# SVG Known Issues

Tracking issues found while reviewing rendered SVG diagrams. Ordered from
highest to lowest severity. Append new findings as we discover them.

## Fixed

- **ns0: namespace prefix on root element.** 2,031 SVGs had their root
  rewritten as `<ns0:svg xmlns:ns0="...">`, which broke CSS variable
  resolution (the `<style>` block targets `svg`, not `ns0:svg`). Everything
  using `fill="var(--palette-color)"` rendered as solid black. Fixed via a
  bulk rewrite; `check_svg.py --namespace` now rejects any future
  regression. See `doc/HowToWriteSVG.md` for prevention.

- **ElementTree-based scripts would reintroduce the ns0 bug.** The old
  `auto_fix_bounds.py` / `auto_fix_fonts.py` scripts used
  `xml.etree.ElementTree` without calling
  `ET.register_namespace("", "http://www.w3.org/2000/svg")` before writing,
  which is almost certainly how the original ns0 damage happened. Those
  scripts have been retired; modern replacements (`svg_fix.py --fit`,
  `svg_fix.py --fonts`) either avoid ElementTree or register the namespace.

- **Content below y=630.** Historical: one-off rescale run fixed 15 files.
  Ongoing enforcement is via `check_svg.py --bounds` + `svg_fix.py --fit`.

- **Oversized custom arrow markers.** 1,228 SVGs used per-file-named
  markers (`id="arrowhead"`, `id="ah12b"`, `id="arrowd0_..."`, etc.) with
  dimensions ranging from 11x11 up to 21x36, rendering as oversized
  triangles. Fixed by `scripts/svg_fix.py --markers` which caps any non-
  palette marker to 10x10 / refX=9 / refY=5 while leaving the marker id,
  fill color, and polygon/path shape untouched. Idempotent.

## Open

### Placeholder / empty diagrams

Some SVGs were apparently scaffolded and never filled in. They render as
a handful of labeled-A/B/C/D boxes with no real content.

- `svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/monitoring_architecture.svg`
  — five rects labeled "Metrics, B, C, D, E" connected by arrows. No actual
  monitoring architecture. **Referenced by**
  `marp/courses/big_data/apache-spark-with-scala/06_spark_streaming.md:197`.
  Needs a human to author real content — do NOT delete, the slide depends
  on it.
- `svg/courses/cloud/introduction-to-azure/09_management/monitoring_architecture.svg`
  — also scaffolded. Needs real content. Referenced by
  `marp/courses/cloud/introduction-to-azure/09_management.md:35`.

**How to find more:** grep for suspicious single-letter or sequential
labels (`>B<`, `>C<`, `>D<` near each other inside `<text>` elements), or
check for SVGs with unusually few unique text strings. A script like
`scripts/find_placeholder_svgs.py` could flag any SVG where ≥80% of
`<text>` elements are single letters or contain only "A/B/C/D/E".

### Inconsistent color styling across diagrams

The palette system works, but the visual look still varies because
different SVGs choose different palette tones, different border weights,
different backgrounds. Some examples:

- Most diagrams use pastel fills (`--primary-pale2`, `--ok-pale2`) with
  matching mid-tone borders — this is the dominant visual style.
- `svg/lectures/devops/logstash/logstash_architecture.svg` uses bright
  saturated fills (vivid green/orange/blue) with no pastel — looks like a
  different diagram system entirely.
- `svg/courses/big_data/advanced-spark-ecosystem-and-best-practice-scala/authorization_with_ranger_sentry.svg`
  uses saturated orange fills with white text — again not the repo's
  dominant pastel look.
- `svg/courses/ai/developing-using-ai/03_chats/performance_optimization.svg`
  uses a dark (code-bg) background. Valid for terminal/code-style diagrams
  but stylistically an outlier.

**What to decide:** pick one default visual style (pastel fill + mid-tone
border) and treat dark-bg and saturated-fill as explicit opt-in variants
with clear rules about when each is appropriate. Then audit and convert.

### Undersized content (not filling the 1280x720 viewBox)

Several diagrams use a small fraction of the available slide area — the
content is clustered in a corner or fills only 30-40% of the frame. Seen in:

- `svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/monitoring_architecture.svg`
  (also a placeholder, above)
- `svg/courses/databases/redis/04_pubsub/pub_sub_use_case_cache_invalidation.svg`
- `svg/courses/security/web-application-hacking/17_server_hardening/why_hardening_matters.svg`
- `svg/courses/big_data/apache-spark-with-python/06_yarn/core_components.svg`
- `svg/courses/ai/generative-ai-applications/02_overview_of_generative_ai/tokenization_methods.svg`
  (content is sized well horizontally but heavy top-loaded; lower half empty)

**Suggested fix:** rescale coordinates so content fills the usable area
(roughly x: 40..1240, y: 40..620). `scripts/svg_fix.py --fit` handles
this; it now produces exactly-fitted output.
