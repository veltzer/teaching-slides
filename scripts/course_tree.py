#!/usr/bin/env python
"""Print a tree of all courses with slide and drawing counts.

Layout:
    domain/
    ├── course (slides=N, drawings=M)
    └── ...

Slides are counted from `marp/courses/<domain>/<course>/*.md` (one slide per
file plus one for every `---` separator outside the YAML front matter).
Drawings are SVG files under `svg/courses/<domain>/<course>/`.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARP_COURSES = ROOT / "marp" / "courses"
SVG_COURSES = ROOT / "svg" / "courses"


def count_slides_in_file(path: Path) -> int:
    content = path.read_text(encoding="utf-8", errors="replace")
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            content = content[end + 4:]
    return 1 + sum(1 for line in content.splitlines() if line.strip() == "---")


def slide_count(course_dir: Path) -> int:
    return sum(count_slides_in_file(f) for f in course_dir.glob("*.md"))


def drawing_count(domain: str, course: str) -> int:
    course_svg = SVG_COURSES / domain / course
    if not course_svg.is_dir():
        return 0
    return sum(1 for _ in course_svg.rglob("*.svg"))


def main() -> None:
    domains = sorted(d for d in MARP_COURSES.iterdir() if d.is_dir())
    total_slides = 0
    total_drawings = 0
    total_courses = 0
    for i, domain in enumerate(domains):
        is_last_domain = i == len(domains) - 1
        print(f"{domain.name}/")
        courses = sorted(c for c in domain.iterdir() if c.is_dir())
        for j, course in enumerate(courses):
            is_last = j == len(courses) - 1
            connector = "└──" if is_last else "├──"
            slides = slide_count(course)
            drawings = drawing_count(domain.name, course.name)
            total_slides += slides
            total_drawings += drawings
            total_courses += 1
            print(f"{connector} {course.name} (slides={slides}, drawings={drawings})")
        if not is_last_domain:
            print()
    print()
    print(f"Total: {total_courses} courses, {total_slides} slides, {total_drawings} drawings")


if __name__ == "__main__":
    main()
