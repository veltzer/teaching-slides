# SVG Improvement Progress

## What "improved" means

An SVG is considered **improved** when it uses the shared palette defs (`grad-accent`).
The palette is defined in `resources/svg_palette.svg` and must be copied verbatim into
every SVG we create or rewrite.

Detection: `grep -rl 'grad-accent' svg/courses/<course>/`

## Palette reference

Colors:
- `#1e88e5` / `#1565c0` — accent (primary blue, gradient top/bottom)
- `#ffffff` / `#f2f2f2` — surface (neutral boxes)
- `#e0e0e0` — border
- `#212121` — primary text
- `#555555` — muted text
- `#9e9e9e` — annotations

Rules (from CLAUDE.md):
- `viewBox="0 0 1280 720"` always
- No title text inside SVG (the `##` slide heading serves as title)
- Content must not go below `y=630`
- Font size ≥ 10
- No unescaped `&`, `<`, `>` in text content
- No `--` inside XML comments

## Progress by course

Format: `course | total SVGs | improved SVGs | % | status`

| Course | Total | Improved | % | Status |
|--------|------:|--------:|--:|--------|
| embedded/effective-real-time-embedded-c-and-c++ | 37 | 37 | 100% | ✅ Done |
| languages/assembly/assembly-programming-using-gas | 5 | 4 | 80% | 🔄 Partial |
| build_systems/make | 5 | 2 | 40% | 🔄 Partial |
| devops/k8s-introduction | 98 | 15 | 15% | 🔄 Partial |
| architecting/modern-software-architecture | 105 | 11 | 10% | 🔄 Partial |
| operating_systems/linux-fundamentals | 95 | 12 | 13% | 🔄 Partial |
| ai/generative-ai-applications | 140 | 8 | 6% | 🔄 Partial |
| build_systems/cmake | 6 | 0 | 0% | ⬜ Not started |
| cloud/introduction-to-azure | 38 | 0 | 0% | ⬜ Not started |
| databases/redis | 116 | 0 | 0% | ⬜ Not started |
| devops/advanced-docker | 23 | 1 | 4% | 🔄 Partial |
| devops/advanced-kubernetes | 49 | 1 | 2% | 🔄 Partial |
| devops/ansible | 12 | 1 | 8% | 🔄 Partial |
| devops/architectural-decisions-in-devops | 141 | 0 | 0% | ⬜ Not started |
| devops/docker-for-developers | 106 | 0 | 0% | ⬜ Not started |
| devops/github-workflows | 8 | 2 | 25% | 🔄 Partial |
| devops/terraform | 36 | 2 | 6% | 🔄 Partial |
| devops/welcome-to-the-world-of-devops | 105 | 0 | 0% | ⬜ Not started |
| ai/advanced-ai-powered-development | 52 | 1 | 2% | 🔄 Partial |
| ai/developing-using-ai | 129 | 0 | 0% | ⬜ Not started |
| ai/developing-using-ai-short | 47 | 1 | 2% | 🔄 Partial |
| architecting/architecting | 122 | 1 | 1% | 🔄 Partial |
| big_data/advanced-spark-with-python | 145 | 2 | 1% | 🔄 Partial |
| big_data/apache-spark-with-python | 14 | 1 | 7% | 🔄 Partial |
| big_data/apache-spark-with-scala | 136 | 0 | 0% | ⬜ Not started |
| databases/elasticsearch-for-developers | 35 | 1 | 3% | 🔄 Partial |
| git/git | 39 | 1 | 3% | 🔄 Partial |
| git/git2 | 125 | 1 | 1% | 🔄 Partial |
| hardware/computer-architecture-fundamentals | 65 | 1 | 2% | 🔄 Partial |
| languages/bash/bash-scripting | 9 | 1 | 11% | 🔄 Partial |
| languages/c/c-refresher | 17 | 1 | 6% | 🔄 Partial |
| languages/c++/c++-design-patterns | 67 | 2 | 3% | 🔄 Partial |
| languages/python/advanced-python | 31 | 3 | 10% | 🔄 Partial |
| languages/rust/advanced-rust | 102 | 3 | 3% | 🔄 Partial |
| languages/rust/rust-programming | (in languages/rust) | 1 | — | 🔄 Partial |
| networking/linux-networking-overview | 44 | 1 | 2% | 🔄 Partial |
| networking/networking-basics | 71 | 0 | 0% | ⬜ Not started |
| operating_systems/advanced-android | 49 | 1 | 2% | 🔄 Partial |
| operating_systems/linux-kernel-advanced-topics | 45 | 1 | 2% | 🔄 Partial |
| operating_systems/linux-system-administration | 28 | 1 | 4% | 🔄 Partial |
| operating_systems/linux-systems-programming | 75 | 2 | 3% | 🔄 Partial |
| operating_systems/qemu-for-kernel-developers | 15 | 0 | 0% | ⬜ Not started |
| operating_systems/yocto | 50 | 1 | 2% | 🔄 Partial |
| security/cyber-attacks-and-vectors | 97 | 1 | 1% | 🔄 Partial |
| security/it-security-policies | 21 | 1 | 5% | 🔄 Partial |
| security/linux-forensics | 28 | 1 | 4% | 🔄 Partial |
| security/web-application-hacking | 64 | 2 | 3% | 🔄 Partial |
| security/working-with-llms-securely | 15 | 1 | 7% | 🔄 Partial |

## Overall totals

| | Count |
|--|------:|
| Total SVGs in repo | 3116 |
| Improved (using our defs) | 129 |
| Not yet improved | 2987 |
| **% complete** | **4%** |

## How to update this file

Run the following to get current counts:

```bash
# Overall
grep -rl 'grad-accent' svg/courses/ | wc -l

# Per course
for course in $(find svg/courses/ -mindepth 2 -maxdepth 2 -type d | sed 's|svg/courses/||' | sort); do
    total=$(find svg/courses/$course -name '*.svg' | wc -l)
    ours=$(grep -rl 'grad-accent' svg/courses/$course 2>/dev/null | wc -l)
    echo "$course | $total | $ours"
done
```

Or use `scripts/find_unused_svgs.py` to check SVG health.
