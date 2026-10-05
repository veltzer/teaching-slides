# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `scripts/count_slides.py:13` - slide counting treats every `---` line as a slide separator, including the 121 `---` lines that sit inside fenced code blocks across `marp/` (e.g. `marp/courses/ai/generative-ai-applications/06_prompt_engineering.md:254`), which Marp does not split on. The README slide total (rendered through `tera.snippets/main.md.tera:6`) is inflated as a result. The same faulty logic is copied into `scripts/build_index.py:86` and `:170` (site index counts), `scripts/course_tree.py:20` and `scripts/svg_coverage.py:40`. The fix is to skip fenced blocks when counting, written once in a shared helper (e.g. in `scripts/svg_lib.py` or a new module) that all four scripts import.

## Medium

- `pyproject.toml:14` - `mypy` and `pytest` are declared dev dependencies, but nothing runs them: `rsconstruct.toml` has no mypy or pytest processor and the repo has no tests. Running mypy on `scripts/` gives 11 errors in 4 files (e.g. `scripts/check_svg.py:66`, `:128`, `scripts/check_marp_md.py:490`, plus missing `lxml` stubs for `scripts/svg_lib.py:35` and `scripts/svg_fix.py:42`). The fix is to add a `[processor.mypy]` on `scripts`, add `lxml-stubs` to the dev group and fix the errors. Also drop `pytest` unless tests are added.
- `rsconstruct.toml:97` - `[processor.terms]` is configured but `enabled = false`, with no comment saying why (git history only shows "no commit message given"). The fix is to enable it and fix what it reports, or remove the section along with the `shared/shared-terms` submodule (`.gitmodules:1`) if the check is abandoned.
- `scripts/check_svg.py:237` - `_svg_type_from_file` catches `Exception` and returns `"regular"`, so an unreadable or malformed SVG gets checked against the wrong palette without any warning. This breaks the CLAUDE.md "never pass errors silently" rule (`CLAUDE.md:5`). The fix is to let it raise, or to report the error through the parse check.
- `doc/HowToWriteSlides.txt:28` - tells the reader to add mermaid through an external CDN `<script>` (lines 28-47). That contradicts its own line 11, `CLAUDE.md:24` (no mermaid) and `CLAUDE.md:26` (no external URLs). The fix is to delete the block.

- `scripts/check_marp_md.py:48` - `_LINK_RE` is anchored with `^` but compiled without `re.MULTILINE` and applied to the whole file with `finditer` (line 88), so `--links` (on by default here, since `rsconstruct.toml` passes no args) only ever looks at the very first characters of a file and never reports a broken link; add `re.MULTILINE` (or drop the anchor). The script is shared byte-identical with demos-lang-marp (rsmultigit check `marp-check-md`), so fix it in both.

## Low

- `tera.snippets/main.md.tera:6` - runs `python3 scripts/count_slides.py`. `CLAUDE.md:12` requires running scripts directly (`scripts/count_slides.py`). The snippet also has no leading blank line, so the generated `README.md:20-21` puts `## Slide numbers` right under the build badge. Add a blank first line to the snippet.
- `scripts/build_index.py:254` - `_git` returns `""` on any git failure, so the site footer silently loses its commit info. Per `CLAUDE.md:5` it should raise when no `GITHUB_SHA` is set and git fails.
- `scripts/svg_gallery.py:50` - corrupt lines in the queue file are skipped silently. Report them instead.
- `CLAUDE.md:31` - says SVG content must stay above y=630, but `scripts/check_svg.py:44` enforces `MAX_Y_BOUND = 640` and `--fit` enforces 620 (`CLAUDE.md:32`). Pick one number and make the docs and the code agree.
- `doc/HowToWriteSlides.txt:63` - points to `doc/HowToWriteSVG.txt`. The file is `doc/HowToWriteSVG.md`.
- `doc/QA_CHECKLIST.md:7` - lists PDFs under `_site/marp/courses/...` and `_site/marp/lectures/iouring.pdf` (line 37). Course chapters now render to `out/chapters/courses` and are united into `_site/pdfunite` (`rsconstruct.toml:31`, `:63`), and the lecture is at `marp/lectures/operating_systems/iouring.md`. Update the paths or delete the checklist.
- `doc/HowToWriteSVG.md:10` - example path `.../advanced-python/03_memory/python_memory_management_levels.svg` does not exist. The real directory is `03_memory_and_garbage_collector/`.
- `doc/svg_known_issues.md:67` - path `svg/courses/big_data/advanced-spark-ecosystem-and-best-practice-scala/authorization_with_ranger_sentry.svg` does not exist. The file is now `svg/courses/big_data/apache-spark-with-scala/09_advanced_ecosystem/authorization_with_ranger_sentry.svg`.
- `doc/TODO.txt:7` - stale items: a makefile (line 7), odp slides (lines 9, 16), "make this repo public" (line 11, it is public), `txt/syllabi` (line 15), a gh-pages site (line 22, Pages now exists). Prune them. `doc/TODO_old.txt` (last touched 2020) can be merged in or deleted.
- `svg/` - 75 SVGs are not referenced by any `marp/` file, 60 of them by no file at all outside `svg/` (e.g. `svg/courses/architecting/architecture-patterns/11_queues/rabbitmq_architecture.svg`). Reference them from slides or delete them, and consider adding an orphan check to `scripts/check_svg.py`.
- `resources/palette_diagram_v1.yaml` - nothing in the repo references it (scripts use `palette_diagram.yaml` and `palette_intro.yaml`). Delete it.
- `to_integrate/drawings/jsx/python-frameworks-comparison.jsx` and `to_integrate/cf-vs-k8s.pdf` - staging leftovers that no processor checks, and the SVGs in `to_integrate/drawings/svg/` skip `check_svg`. Move them into `svg/` and `marp/`, or remove them.
- `config/project.lua:6` - keywords `powerpoint`, `openoffice`, `odp` are stale. The repo has no odp or ppt files.
- Fleet-wide shared file: `.oxlintrc.json:7` - `$schema` points to `./node_modules/oxlint/configuration_schema.json`, but oxlint is installed as a Rust binary and that path does not exist (here or elsewhere).
