#!/usr/bin/env python

"""
Generate an HTML SPA for browsing courses and lectures built by rsconstruct's pdfunite processor.

Scans the pdfunite source directory for course/lecture folders containing source files,
counts slides per entry, and generates a self-contained index.html with
filtering, sorting, folder navigation, and PDF download links.

Usage:
    ./scripts/build_index.py [--source-dir DIR] [--lectures-dir DIR] [--output-dir DIR] [--source-ext EXT] [--out FILE]

Defaults match rsconstruct's pdfunite processor defaults:
    --source-dir   marp/courses
    --lectures-dir marp/lectures
    --output-dir   out/pdfunite
    --source-ext   .md
    --out          _site/index.html
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(".")
if not (ROOT / ".git").exists():
    print("Error: script must be run from the root of the repository", file=sys.stderr)
    sys.exit(1)
RESOURCES_DIR = ROOT / "resources"


def find_course_dirs(source_dir: Path, ext: str) -> list[Path]:
    """Recursively find directories containing files with the given extension."""
    result: list[Path] = []
    if not source_dir.exists():
        return result
    _collect(source_dir, ext, result)
    result.sort()
    return result


def _collect(directory: Path, ext: str, result: list[Path]) -> None:
    has_file = False
    subdirs: list[Path] = []
    try:
        entries = sorted(directory.iterdir())
    except OSError:
        return
    for entry in entries:
        if entry.is_dir():
            subdirs.append(entry)
        elif not has_file and entry.is_file() and entry.suffix == ext:
            has_file = True
    if has_file:
        result.append(directory)
    for sub in subdirs:
        _collect(sub, ext, result)


def count_chapters(directory: Path, ext: str) -> int:
    """Count files with the given extension in a directory (non-recursive)."""
    return sum(1 for f in directory.iterdir() if f.is_file() and f.suffix == ext)


def _strip_front_matter(content: str) -> str:
    """Remove YAML front matter (opening --- to closing ---) from content."""
    if not content.startswith("---"):
        return content
    end = content.find("\n---", 3)
    if end == -1:
        return content
    return content[end + 4:]


def count_slides(directory: Path, ext: str) -> int:
    """Count slides in all files with the given extension in a directory (non-recursive).
    Each file contributes 1 slide (the first) plus one for each '---' separator line.
    YAML front matter delimiters are excluded from the count."""
    total = 0
    for f in directory.iterdir():
        if f.is_file() and f.suffix == ext:
            content = f.read_text(encoding="utf-8", errors="replace")
            body = _strip_front_matter(content)
            total += 1 + sum(1 for line in body.splitlines() if line.strip() == "---")
    return total


def folder_label(rel_path: Path) -> str:
    """Convert a relative path to a human-readable label."""
    return " / ".join(
        p.replace("_", " ").replace("-", " ").title() for p in rel_path.parts
    )


def parse_front_matter(directory: Path, ext: str) -> dict[str, Any]:
    """Parse YAML front matter from the first file (alphabetically) in the directory."""
    files = sorted(f for f in directory.iterdir() if f.is_file() and f.suffix == ext)
    if not files:
        return {}
    content = files[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        return {}


def pdf_path_for_course(rel: Path, output_dir: Path, site_dir: Path) -> str | None:
    """Compute the expected merged PDF path for a course directory, relative to site_dir."""
    parent = rel.parent
    leaf = rel.name
    pdf = output_dir / parent / f"{leaf}.pdf"
    if pdf.exists():
        return str(pdf.relative_to(site_dir))
    return None


def build_course_entries(
    source_dir: Path, output_dir: Path, site_dir: Path, ext: str,
) -> list[dict[str, Any]]:
    """Build the list of course entries (directories containing multiple source files)."""
    dirs = find_course_dirs(source_dir, ext)
    entries: list[dict[str, Any]] = []

    for course_dir in dirs:
        rel = course_dir.relative_to(source_dir)
        name = rel.name.replace("_", " ").replace("-", " ").title()
        chapters = count_chapters(course_dir, ext)
        slides = count_slides(course_dir, ext)
        pdf = pdf_path_for_course(rel, output_dir, site_dir)
        prefixed_folder = "courses/" + str(rel)
        parent = str(rel.parent)
        fm = parse_front_matter(course_dir, ext)

        entries.append(
            {
                "name": name,
                "type": "course",
                "chapters": chapters,
                "slides": slides,
                "folder": prefixed_folder,
                "folder_label": folder_label(rel.parent) if parent != "." else "Root",
                "pdf": pdf,
                "level": fm.get("level", ""),
                "category": fm.get("category", ""),
                "duration_hours": fm.get("duration_hours", 0),
                "tags": fm.get("tags", []),
                "audience": fm.get("audience", []),
            }
        )

    return entries


def count_slides_in_file(filepath: Path) -> int:
    """Count slides in a single markdown file.
    Each file has 1 slide (the first) plus one for each '---' separator line.
    YAML front matter delimiters are excluded from the count."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    body = _strip_front_matter(content)
    return 1 + sum(1 for line in body.splitlines() if line.strip() == "---")


def parse_file_front_matter(filepath: Path) -> dict[str, Any]:
    """Parse YAML front matter from a single markdown file."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        return {}


def build_lecture_entries(
    lectures_dir: Path, marp_output_dir: Path, site_dir: Path, ext: str,
) -> list[dict[str, Any]]:
    """Build the list of lecture entries (individual source files in category dirs)."""
    entries: list[dict[str, Any]] = []
    if not lectures_dir.exists():
        return entries

    for md_file in sorted(lectures_dir.rglob(f"*{ext}")):
        rel = md_file.relative_to(lectures_dir)
        stem = md_file.stem
        name = stem.replace("_", " ").replace("-", " ").title()
        slides = count_slides_in_file(md_file)
        folder_parts = rel.parent
        folder = str(folder_parts) if folder_parts != Path(".") else ""
        prefixed_folder = "lectures/" + str(folder_parts / stem) if folder else "lectures/" + stem
        fm = parse_file_front_matter(md_file)

        # Lecture PDFs are produced by the marp processor (single-file PDFs)
        # e.g. marp/lectures/databases/acid.md -> _site/marp/lectures/databases/acid.pdf
        pdf_candidate = marp_output_dir / "lectures" / folder_parts / f"{stem}.pdf"
        pdf = str(pdf_candidate.relative_to(site_dir)) if pdf_candidate.exists() else None

        entries.append(
            {
                "name": name,
                "type": "lecture",
                "chapters": 1,
                "slides": slides,
                "folder": prefixed_folder,
                "folder_label": folder_label(folder_parts) if folder else "Root",
                "pdf": pdf,
                "level": fm.get("level", ""),
                "category": fm.get("category", ""),
                "duration_hours": fm.get("duration_hours", 0),
                "tags": fm.get("tags", []),
                "audience": fm.get("audience", []),
            }
        )

    return entries


def make_options(values: list[str]) -> str:
    """Generate HTML <option> tags from a sorted list of unique values."""
    return "\n".join(f'<option value="{v}">{v}</option>' for v in sorted(set(values)) if v)


def _git(*args: str) -> str:
    """Run git and return stripped output, or '' on failure."""
    try:
        return subprocess.check_output(
            ["git", *args], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def build_info_html() -> str:
    """Render a "built from commit X on date Y (workflow link)" footer line.

    Values come from env vars set by CI (GITHUB_SHA, GITHUB_RUN_ID,
    GITHUB_SERVER_URL, GITHUB_REPOSITORY) and fall back to local `git` for
    developer builds.
    """
    sha = os.environ.get("GITHUB_SHA", "") or _git("rev-parse", "HEAD")
    sha_short = sha[:12] if sha else "unknown"

    build_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    run_id = os.environ.get("GITHUB_RUN_ID", "")
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if run_id and repo:
        run_link = (
            f'<a href="{server}/{repo}/actions/runs/{run_id}" '
            f'rel="noopener">run #{run_id}</a>'
        )
    else:
        run_link = "local build"

    commit_link = sha_short
    if sha and repo:
        commit_link = f'<a href="{server}/{repo}/commit/{sha}" rel="noopener">{sha_short}</a>'

    return (
        f'<p class="build-info">Built from <code>{commit_link}</code> on '
        f'{build_date} &middot; {run_link}</p>'
    )


def generate_index(entries: list[dict[str, Any]]) -> str:
    """Generate the self-contained HTML index page."""
    css = (RESOURCES_DIR / "courses_index.css").read_text(encoding="utf-8")
    js = (RESOURCES_DIR / "courses_index.js").read_text(encoding="utf-8")
    template = (RESOURCES_DIR / "courses_index.html").read_text(encoding="utf-8")

    levels = [e["level"] for e in entries]
    categories = [e["category"] for e in entries]
    types = [e["type"] for e in entries]
    tags = [t for e in entries for t in e["tags"]]
    audiences = [a for e in entries for a in e["audience"]]

    return (
        template.replace("{{CSS}}", css)
        .replace("{{JS}}", js)
        .replace("{{DATA_JSON}}", json.dumps(entries, ensure_ascii=False))
        .replace("{{TOTAL_COUNT}}", str(len(entries)))
        .replace("{{LEVEL_OPTIONS}}", make_options(levels))
        .replace("{{CATEGORY_OPTIONS}}", make_options(categories))
        .replace("{{TYPE_OPTIONS}}", make_options(types))
        .replace("{{TAG_OPTIONS}}", make_options(tags))
        .replace("{{AUDIENCE_OPTIONS}}", make_options(audiences))
        .replace("{{BUILD_INFO}}", build_info_html())
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build an HTML SPA for browsing courses and lectures"
    )
    parser.add_argument(
        "--source-dir",
        default="marp/courses",
        help="Directory containing course subdirectories (default: marp/courses)",
    )
    parser.add_argument(
        "--lectures-dir",
        default="marp/lectures",
        help="Directory containing lecture subdirectories (default: marp/lectures)",
    )
    parser.add_argument(
        "--output-dir",
        default="_site/pdfunite",
        help="Directory containing merged PDFs (default: _site/pdfunite)",
    )
    parser.add_argument(
        "--marp-output-dir",
        default="_site/marp",
        help="Directory containing individual marp PDFs (default: _site/marp)",
    )
    parser.add_argument(
        "--source-ext",
        default=".md",
        help="Source file extension (default: .md)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output HTML file (default: <output-dir>/index.html)",
    )
    args, _ = parser.parse_known_args()

    source_dir = Path(args.source_dir)
    lectures_dir = Path(args.lectures_dir)
    output_dir = Path(args.output_dir)
    marp_output_dir = Path(args.marp_output_dir)
    ext = args.source_ext if args.source_ext.startswith(".") else f".{args.source_ext}"
    site_dir = output_dir.parent
    out_file = Path(args.out) if args.out else site_dir / "index.html"

    if not source_dir.exists():
        print(f"Error: source directory '{source_dir}' does not exist.", file=sys.stderr)
        raise SystemExit(1)

    entries = build_course_entries(source_dir, output_dir, site_dir, ext)
    n_courses = len(entries)

    lecture_entries = build_lecture_entries(lectures_dir, marp_output_dir, site_dir, ext)
    entries.extend(lecture_entries)
    n_lectures = len(lecture_entries)

    html = generate_index(entries)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Index built: {n_courses} courses, {n_lectures} lectures ({len(entries)} total)")
    print(f"Output: {out_file}")


if __name__ == "__main__":
    main()
