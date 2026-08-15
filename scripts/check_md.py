#!/usr/bin/env python

"""
Unified markdown checker for Marp slide files.

Checks:
  --links       Validate that local links point to existing files
  --labels      Validate fenced code block language labels against text_labels.yaml
  --fences      Check for unclosed code fences (odd number of ``` lines)
  --urls        Check for external URLs in image references (should be local)
  --whitespace  Check for trailing whitespace and consecutive blank lines
  --slides      Check for empty slides (consecutive --- separators)
  --dead-slides Check for dead slides (heading only, no body content)
  --images      Check that image references point to existing local files
  --numbering   Check for sequential numbered lists (should use 1. 1. 1.)
  --svg-content Check that slides with SVG images have no other content on the same slide
  --inline-svg  Flag inline <svg>...</svg> elements in markdown (forbidden — SVGs must be external files)
  --title-svg   Check that every 00_title.md has a corresponding svg/.../title.svg
  --title-count Enforce "one title per unit": each course has exactly one 00_title.md with one H1; each lecture has exactly one H1; non-title chapters have no H1
  --table-width Flag markdown tables with more than MAX_TABLE_COLUMNS columns
  --slide-length Flag slides with more than MAX_SLIDE_LINES non-blank body lines

Usage:
    check_md.py --links --labels file1.md file2.md ...
    check_md.py --links marp/                          # scan a directory
    check_md.py --labels marp/courses/foo.md           # single check on one file
"""

import argparse
import os
import re
import sys
from collections.abc import Iterator
from pathlib import Path

import yaml

_ROOT = Path(".")
if not (_ROOT / ".git").exists():
    print("Error: script must be run from the root of the repository", file=sys.stderr)
    sys.exit(1)


# ── Regexes ──

_LINK_RE = re.compile(r'^\[([^\]]+)\]\(([^)]+)\)')
_FENCE_RE = re.compile(r'^[ \t]{0,3}```(\w+)', re.MULTILINE)
_FENCE_LINE_RE = re.compile(r'^[ \t]{0,3}```', re.MULTILINE)
_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
_SVG_IMAGE_RE = re.compile(r'!\[.*?\]\(.*?\.svg\)')
_HEADING_RE = re.compile(r'^#{1,6}\s')
_NUMBERED_LIST_RE = re.compile(r'^(\s*)([2-9]\d*)\. ')

MAX_TABLE_COLUMNS = 6
MAX_SLIDE_LINES = 40


# ── Helpers ──

def _is_local_link(link: str) -> bool:
    return not link.startswith(('http://', 'https://', 'ftp://', 'mailto:'))


def _remove_code_blocks(content: str) -> str:
    return re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)


def _load_labels() -> frozenset:
    labels_file = _ROOT / 'text_labels.yaml'
    with open(labels_file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return frozenset(
        entry['label']
        for category in data.values()
        for entry in category
    )


_VALID_LABELS = _load_labels()


# ── Per-check functions (accept pre-loaded text/lines) ──

def _check_links(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for m in _LINK_RE.finditer(text_no_code):
        link_text, link = m.groups()
        if not _is_local_link(link):
            continue
        clean = link.split('#')[0]
        if not clean:
            continue
        if os.path.isabs(clean):
            target = Path(clean)
        else:
            target = (path.parent / clean).resolve()
        if not target.exists():
            errors.append(f"{path}: broken link [{link_text}]({link})")
    return errors


def _iter_labels(text: str) -> Iterator[tuple[str, int]]:
    for m in _FENCE_RE.finditer(text):
        line_no = text.count('\n', 0, m.start()) + 1
        yield m.group(1), line_no


def _check_labels(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for label, line_no in _iter_labels(text):
        if label not in _VALID_LABELS:
            errors.append(f"{path}:{line_no}: invalid label `{label}`")
    return errors


def _check_fences(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    fence_count = len(_FENCE_LINE_RE.findall(text))
    if fence_count % 2 != 0:
        return [f"{path}: unclosed code fence ({fence_count} fence lines, expected even)"]
    return []


def _check_urls(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for line_no, line in enumerate(text_no_code.splitlines(), 1):
        for m in _IMAGE_RE.finditer(line):
            url = m.group(2)
            if url.startswith(('http://', 'https://')):
                errors.append(f"{path}:{line_no}: external image URL: {url}")
    return errors


def _check_whitespace(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    prev_blank = False
    for line_no, line in enumerate(lines, 1):
        if line != line.rstrip():
            errors.append(f"{path}:{line_no}: trailing whitespace")
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            errors.append(f"{path}:{line_no}: consecutive blank lines")
        prev_blank = is_blank
    return errors


def _check_slides(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    last_separator = None
    only_blanks = True
    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == '---':
            if last_separator is not None and only_blanks:
                errors.append(f"{path}:{line_no}: empty slide (no content between --- separators)")
            last_separator = line_no
            only_blanks = True
        elif stripped != '':
            only_blanks = False
    return errors


def _split_slides(lines: list[str]) -> list[tuple[int, list[str]]]:
    """Split lines into (start_line_1based, slide_lines) pairs.

    Handles YAML front matter (two leading --- fences) by skipping past it.
    Slide separators are bare `---` lines between slides.
    """
    i = 0
    # Skip YAML front matter if present
    if lines and lines[0].strip() == '---':
        i = 1
        while i < len(lines) and lines[i].strip() != '---':
            i += 1
        i += 1  # past closing ---
    slides: list[tuple[int, list[str]]] = []
    cur: list[str] = []
    cur_start = i + 1  # 1-based line number of first line of current slide
    for j in range(i, len(lines)):
        if lines[j].strip() == '---':
            slides.append((cur_start, cur))
            cur = []
            cur_start = j + 2
        else:
            cur.append(lines[j])
    if cur:
        slides.append((cur_start, cur))
    return slides


def _check_dead_slides(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    """Flag `## `-titled slides with no body content (heading only).

    Skips:
      - Slides whose only heading is level-1 (`# `). These are legitimate
        chapter-title divider slides per the course convention.
      - The first slide of 00_title.md (the title slide with author/email).
    """
    errors: list[str] = []
    is_title_file = path.name == '00_title.md'
    slides = _split_slides(lines)
    for idx, (start, slide_lines) in enumerate(slides):
        if is_title_file and idx == 0:
            continue
        has_h1 = False      # slide contains a `# ` level-1 heading
        h2_line_no = None   # line of first `## ` heading
        has_body = False
        in_fence = False
        for offset, ln in enumerate(slide_lines):
            stripped = ln.strip()
            if _FENCE_OPEN_RE.match(ln):
                in_fence = not in_fence
                has_body = True
                continue
            if in_fence:
                has_body = True
                continue
            if not stripped:
                continue
            if stripped.startswith('<!--') and stripped.endswith('-->'):
                continue
            if stripped.startswith('# '):
                has_h1 = True
                continue
            if stripped.startswith('## '):
                if h2_line_no is None:
                    h2_line_no = start + offset
                    continue
                has_body = True
                continue
            if _HEADING_RE.match(ln):
                # h3+ heading acts as body
                has_body = True
                continue
            has_body = True
        # Only flag slides that have a `## ` but no `# ` and no body — the
        # pattern `# Chapter / ## Subtitle` is a legitimate divider slide.
        if h2_line_no is not None and not has_body and not has_h1:
            errors.append(
                f"{path}:{h2_line_no}: dead slide (heading only, no body content)"
            )
    return errors


def _check_images(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    for line_no, line in enumerate(text_no_code.splitlines(), 1):
        for m in _IMAGE_RE.finditer(line):
            target = m.group(2)
            if target.startswith(('http://', 'https://')):
                continue
            clean = target.strip()
            if ' ' in clean:
                clean = clean.rsplit(' ', 1)[-1]
            resolved = _ROOT / clean
            if not resolved.exists():
                resolved_rel = path.parent / clean
                if not resolved_rel.exists():
                    errors.append(f"{path}:{line_no}: broken image reference: {clean}")
    return errors


def _check_numbering(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    in_code = False
    for line_no, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code = not in_code
        if not in_code:
            m = _NUMBERED_LIST_RE.match(line)
            if m:
                errors.append(f"{path}:{line_no}: sequential numbering (use 1. not {m.group(2)}.)")
    return errors


def _check_slide_length(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    """Flag slides with more than MAX_SLIDE_LINES non-blank body lines.

    Body excludes blank lines and heading lines (#..). Code-fence content counts
    toward the limit since it still renders and consumes vertical space.
    """
    errors: list[str] = []
    slides = _split_slides(lines)
    for start, slide_lines in slides:
        in_fence = False
        count = 0
        heading_line_no = None
        for offset, ln in enumerate(slide_lines):
            stripped = ln.strip()
            if re.match(r'^[ \t]{0,3}```', ln):
                in_fence = not in_fence
                count += 1
                continue
            if in_fence:
                count += 1
                continue
            if not stripped:
                continue
            if stripped.startswith('#'):
                if heading_line_no is None:
                    heading_line_no = start + offset
                continue
            count += 1
        if count > MAX_SLIDE_LINES:
            report_line = heading_line_no if heading_line_no is not None else start
            errors.append(
                f"{path}:{report_line}: slide has {count} body lines "
                f"(max {MAX_SLIDE_LINES}) — split into smaller slides"
            )
    return errors


def _check_table_width(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    """Flag markdown tables whose header row has more than MAX_TABLE_COLUMNS columns."""
    errors: list[str] = []
    in_code = False
    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        # A table header line starts and ends with `|` and the NEXT non-blank
        # non-code line is the `---` separator. Detect header via the separator
        # below: a line like `|---|---|---|`.
        if not (stripped.startswith('|') and stripped.endswith('|')):
            continue
        # Look at the next line to see if it's a separator
        if line_no >= len(lines):
            continue
        next_line = lines[line_no].strip() if line_no < len(lines) else ''
        if not re.match(r'^\|[\s:|-]+\|$', next_line):
            continue
        # Count columns: split on unescaped pipes, drop leading/trailing empties.
        cells = [c for c in stripped.strip('|').split('|')]
        if len(cells) > MAX_TABLE_COLUMNS:
            errors.append(
                f"{path}:{line_no}: table has {len(cells)} columns "
                f"(max {MAX_TABLE_COLUMNS})"
            )
    return errors


def _check_svg_content(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    errors = []
    raw_slides = re.split(r'\n---\n', text)
    line_cursor = 1
    for slide in raw_slides:
        slide_lines = slide.split('\n')
        numbered = list(enumerate(slide_lines, line_cursor))
        has_svg = any(_SVG_IMAGE_RE.search(ln.strip()) for _, ln in numbered)
        if has_svg:
            headings = [(i, ln) for i, ln in numbered if ln.strip() and _HEADING_RE.match(ln)]
            non_heading_non_svg = [
                (i, ln) for i, ln in numbered
                if ln.strip()
                and not _HEADING_RE.match(ln)
                and not _SVG_IMAGE_RE.search(ln.strip())
            ]
            # More than one heading on an SVG slide is not allowed
            if len(headings) > 1:
                first_lineno, first_line = headings[1]
                errors.append(
                    f"{path}:{first_lineno}: slide with SVG image has multiple headings: {first_line.strip()!r}"
                )
            # Any non-heading, non-SVG content is not allowed
            if non_heading_non_svg:
                first_lineno, first_line = non_heading_non_svg[0]
                errors.append(
                    f"{path}:{first_lineno}: slide with SVG image contains other content: {first_line.strip()!r}"
                )
        line_cursor += len(slide_lines) + 1
    return errors


_INLINE_SVG_RE = re.compile(r'<svg\b[^>]*>', re.IGNORECASE)
_FENCE_OPEN_RE = re.compile(r'^[ \t]{0,3}```')


def _check_inline_svg(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    """Flag inline <svg>…</svg> blocks in markdown that sit OUTSIDE fenced
    code blocks. Fenced examples (e.g. XSS payloads in a ```html block) are
    legitimate teaching content and are skipped.

    SVGs meant as diagrams must live in svg/ and be referenced with ![...](...svg).
    """
    errors: list[str] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if _FENCE_OPEN_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if _INLINE_SVG_RE.search(line):
            errors.append(
                f"{path}:{i}: inline <svg> element in markdown — "
                f"SVGs must live in svg/ and be referenced with ![](...)"
            )
    return errors


def _check_title_count(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    """Enforce "one title per unit":
      - Every course must have exactly one 00_title.md.
      - Every course 00_title.md must contain exactly one `# Title` H1.
      - Every lecture file must have exactly one `# Title` H1 at its top (inside
        the first slide, before the first `---` separator).

    Chapter-divider slides (`# Chapter`) inside non-title chapters are permitted
    (they are a legitimate pattern for section breaks).

    Code-fence contents are stripped so `# comment` in shell code doesn't count.
    """
    parts = path.parts
    if len(parts) < 3 or parts[0] != "marp":
        return []

    errors: list[str] = []

    # Strip YAML frontmatter (starts with --- on first line, ends with --- alone)
    body = text_no_code
    if body.startswith(('---\n', '---\r\n')):
        m = re.match(r'^---\s*\n.*?\n---\s*\n', body, re.DOTALL)
        if m:
            body = body[m.end():]

    # First-slide H1: find H1s before the first `---` separator (slide break)
    first_slide = re.split(r'^---\s*$', body, maxsplit=1, flags=re.MULTILINE)[0]
    first_slide_h1_count = len(re.findall(r'^# [^#\n]', first_slide, re.MULTILINE))

    # Course 00_title.md
    if parts[1] == "courses" and path.name == "00_title.md":
        if first_slide_h1_count != 1:
            errors.append(
                f"{path}: 00_title.md first slide must have exactly 1 H1, "
                f"found {first_slide_h1_count}"
            )
        course_dir = path.parent
        titles = list(course_dir.glob('00_title*.md'))
        if len(titles) != 1:
            errors.append(f"{course_dir}: expected exactly 1 00_title*.md file, "
                          f"found {len(titles)}")
        return errors

    # Lecture file: first slide needs exactly one H1
    if parts[1] == "lectures" and path.suffix == ".md":
        if first_slide_h1_count != 1:
            errors.append(
                f"{path}: lecture first slide must have exactly 1 H1 title, "
                f"found {first_slide_h1_count}"
            )
        return errors

    return errors


def _check_title_svg(path: Path, text: str, text_no_code: str, lines: list[str]) -> list[str]:
    """Check that every course/lecture has a title.svg AND that the markdown references it.

    Courses: marp/courses/DOMAIN/COURSE/00_title.md -> svg/courses/DOMAIN/COURSE/title.svg
    Lectures: marp/lectures/DOMAIN/LECTURE.md -> svg/lectures/DOMAIN/LECTURE/title.svg
    """
    parts = path.parts
    if len(parts) < 3 or parts[0] != "marp":
        return []

    errors: list[str] = []
    expected_ref: str | None = None
    svg_path: Path | None = None

    # Course title slides: marp/courses/DOMAIN/COURSE/00_title.md
    if parts[1] == "courses" and path.name == "00_title.md" and len(parts) >= 5:
        svg_path = _ROOT / "svg" / Path(*parts[1:-1]) / "title.svg"
        expected_ref = "svg/" + "/".join(parts[1:-1]) + "/title.svg"

    # Lecture slides: marp/lectures/DOMAIN/LECTURE.md (single file per lecture)
    elif parts[1] == "lectures" and path.suffix == ".md" and len(parts) == 4:
        lecture_name = path.stem
        svg_path = _ROOT / "svg" / "lectures" / parts[2] / lecture_name / "title.svg"
        expected_ref = f"svg/lectures/{parts[2]}/{lecture_name}/title.svg"

    if svg_path is None:
        return []

    if not svg_path.exists():
        errors.append(f"{path}: missing title SVG: {svg_path}")
        return errors

    if expected_ref not in text:
        errors.append(f"{path}: title SVG exists but is not referenced in the markdown "
                      f"(expected to find `{expected_ref}` in the file)")

    return errors


# ── Main ──

def _collect_files(paths: list[str]) -> list[Path]:
    result = []
    for p_str in paths:
        p = Path(p_str)
        if p.is_file():
            result.append(p)
        elif p.is_dir():
            result.extend(sorted(p.rglob('*.md')))
        else:
            print(f"error: path not found: {p}", file=sys.stderr)
            sys.exit(1)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Unified markdown checker for Marp slides.'
    )
    parser.add_argument('paths', nargs='+',
                        help='Markdown files or directories to check (required)')
    parser.add_argument('--links', action='store_true',
                        help='Check that local links point to existing files')
    parser.add_argument('--labels', action='store_true',
                        help='Check fenced code block labels against text_labels.yaml')
    parser.add_argument('--fences', action='store_true',
                        help='Check for unclosed code fences')
    parser.add_argument('--urls', action='store_true',
                        help='Check for external URLs in image references')
    parser.add_argument('--whitespace', action='store_true',
                        help='Check for trailing whitespace and consecutive blank lines')
    parser.add_argument('--slides', action='store_true',
                        help='Check for empty slides (consecutive --- separators)')
    parser.add_argument('--dead-slides', action='store_true', dest='dead_slides',
                        help='Check for dead slides (heading only, no body content)')
    parser.add_argument('--images', action='store_true',
                        help='Check that image references point to existing local files')
    parser.add_argument('--numbering', action='store_true',
                        help='Check for sequential numbered lists (should use 1. 1. 1.)')
    parser.add_argument('--svg-content', action='store_true',
                        help='Check that slides with SVG images have no other content')
    parser.add_argument('--inline-svg', action='store_true', dest='inline_svg',
                        help='Flag inline <svg>...</svg> elements in markdown (SVGs must be external files)')
    parser.add_argument('--title-svg', action='store_true', dest='title_svg',
                        help='Check that every 00_title.md has a corresponding svg/.../title.svg')
    parser.add_argument('--title-count', action='store_true', dest='title_count',
                        help='Check "one title per unit": each 00_title.md and each lecture has exactly one `# Title`; non-title chapters have none')
    parser.add_argument('--table-width', action='store_true', dest='table_width',
                        help=f'Flag tables with more than {MAX_TABLE_COLUMNS} columns')
    parser.add_argument('--slide-length', action='store_true', dest='slide_length',
                        help=f'Flag slides with more than {MAX_SLIDE_LINES} body lines')
    args = parser.parse_args()

    # Default: all checks enabled
    flags = [args.links, args.labels, args.fences, args.urls,
             args.whitespace, args.slides, args.dead_slides,
             args.images, args.numbering,
             args.svg_content, args.inline_svg, args.title_svg,
             args.title_count, args.table_width, args.slide_length]
    explicit = any(flags)
    checks = []
    if args.links or not explicit:
        checks.append(_check_links)
    if args.labels or not explicit:
        checks.append(_check_labels)
    if args.fences or not explicit:
        checks.append(_check_fences)
    if args.urls or not explicit:
        checks.append(_check_urls)
    if args.whitespace or not explicit:
        checks.append(_check_whitespace)
    if args.slides or not explicit:
        checks.append(_check_slides)
    if args.dead_slides or not explicit:
        checks.append(_check_dead_slides)
    if args.images or not explicit:
        checks.append(_check_images)
    if args.numbering or not explicit:
        checks.append(_check_numbering)
    if args.svg_content or not explicit:
        checks.append(_check_svg_content)
    if args.inline_svg or not explicit:
        checks.append(_check_inline_svg)
    if args.title_svg or not explicit:
        checks.append(_check_title_svg)
    if args.title_count or not explicit:
        checks.append(_check_title_count)
    if args.table_width or not explicit:
        checks.append(_check_table_width)
    if args.slide_length or not explicit:
        checks.append(_check_slide_length)

    files = _collect_files(args.paths)
    all_errors: list[str] = []

    for path in files:
        text = path.read_text(encoding='utf-8')
        text_no_code = _remove_code_blocks(text)
        lines = text.splitlines()
        for check in checks:
            all_errors.extend(check(path, text, text_no_code, lines))

    for err in all_errors:
        print(err, file=sys.stderr)

    sys.exit(1 if all_errors else 0)


if __name__ == '__main__':
    main()
