#!/usr/bin/env python

"""
Generate an HTML SPA for browsing courses built by rsconstruct's pdfunite processor.

Scans the pdfunite source directory for course folders containing source files,
counts slides per course, and generates a self-contained index.html with
filtering, sorting, folder navigation, and PDF download links.

Usage:
    ./scripts/build_courses_index.py [--source-dir DIR] [--output-dir DIR] [--source-ext EXT] [--out FILE]

Defaults match rsconstruct's pdfunite processor defaults:
    --source-dir  marp/courses
    --output-dir  out/pdfunite
    --source-ext  .md
    --out         _site/index.html
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
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


def count_slides(directory: Path, ext: str) -> int:
    """Count slides in all files with the given extension in a directory (non-recursive).
    Each file contributes 1 slide (the first) plus one for each '---' separator line."""
    total = 0
    for f in directory.iterdir():
        if f.is_file() and f.suffix == ext:
            content = f.read_text(encoding="utf-8", errors="replace")
            total += 1 + sum(1 for line in content.splitlines() if line.strip() == "---")
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


def build_entries(
    source_dir: Path, output_dir: Path, site_dir: Path, ext: str
) -> list[dict[str, Any]]:
    """Build the list of course entries."""
    dirs = find_course_dirs(source_dir, ext)
    entries: list[dict[str, Any]] = []

    for course_dir in dirs:
        rel = course_dir.relative_to(source_dir)
        name = rel.name.replace("_", " ").replace("-", " ").title()
        chapters = count_chapters(course_dir, ext)
        slides = count_slides(course_dir, ext)
        pdf = pdf_path_for_course(rel, output_dir, site_dir)
        folder = str(rel.parent) if rel.parent != Path(".") else ""
        fm = parse_front_matter(course_dir, ext)

        entries.append(
            {
                "name": name,
                "chapters": chapters,
                "slides": slides,
                "folder": str(rel),
                "folder_label": folder_label(rel.parent) if folder else "Root",
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


def generate_index(entries: list[dict[str, Any]]) -> str:
    """Generate the self-contained HTML index page."""
    css = (RESOURCES_DIR / "courses_index.css").read_text(encoding="utf-8")
    js = (RESOURCES_DIR / "courses_index.js").read_text(encoding="utf-8")
    template = (RESOURCES_DIR / "courses_index.html").read_text(encoding="utf-8")

    levels = [e["level"] for e in entries]
    categories = [e["category"] for e in entries]
    tags = [t for e in entries for t in e["tags"]]
    audiences = [a for e in entries for a in e["audience"]]

    return (
        template.replace("{{CSS}}", css)
        .replace("{{JS}}", js)
        .replace("{{DATA_JSON}}", json.dumps(entries, ensure_ascii=False))
        .replace("{{TOTAL_COUNT}}", str(len(entries)))
        .replace("{{LEVEL_OPTIONS}}", make_options(levels))
        .replace("{{CATEGORY_OPTIONS}}", make_options(categories))
        .replace("{{TAG_OPTIONS}}", make_options(tags))
        .replace("{{AUDIENCE_OPTIONS}}", make_options(audiences))
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build an HTML SPA for browsing courses"
    )
    parser.add_argument(
        "--source-dir",
        default="marp/courses",
        help="Directory containing course subdirectories (default: marp/courses)",
    )
    parser.add_argument(
        "--output-dir",
        default="_site/pdfunite",
        help="Directory containing merged PDFs (default: _site/pdfunite)",
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
    output_dir = Path(args.output_dir)
    ext = args.source_ext if args.source_ext.startswith(".") else f".{args.source_ext}"
    site_dir = output_dir.parent
    out_file = Path(args.out) if args.out else site_dir / "index.html"

    if not source_dir.exists():
        print(f"Error: source directory '{source_dir}' does not exist.", file=sys.stderr)
        raise SystemExit(1)

    entries = build_entries(source_dir, output_dir, site_dir, ext)
    html = generate_index(entries)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Course index built: {len(entries)} courses found")
    print(f"Output: {out_file}")


if __name__ == "__main__":
    main()
