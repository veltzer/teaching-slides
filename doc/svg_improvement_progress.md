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

| Course | Total | Improved | Status |
|--------|------:|--------:|--------|
| big_data/apache-spark-with-python | 14 | 14 | ✅ Done |
| build_systems/make | 5 | 5 | ✅ Done |
| devops/advanced-docker | 23 | 23 | ✅ Done |
| devops/ansible | 12 | 12 | ✅ Done |
| devops/github-workflows | 8 | 8 | ✅ Done |
| embedded/effective-real-time-embedded-c-and-c++ | 37 | 37 | ✅ Done |
| languages/assembly | 5 | 5 | ✅ Done |
| languages/bash | 9 | 9 | ✅ Done |
| languages/c | 17 | 17 | ✅ Done |
| security/it-security-policies | 21 | 21 | ✅ Done |
| security/working-with-llms-securely | 15 | 15 | ✅ Done |
| architecting/modern-software-architecture | 105 | 11 | 🔄 10% |
| operating_systems/linux-fundamentals | 95 | 12 | 🔄 12% |
| devops/k8s-introduction | 98 | 15 | 🔄 15% |
| ai/generative-ai-applications | 140 | 8 | 🔄 5% |
| devops/terraform | 36 | 2 | 🔄 5% |
| languages/python | 31 | 3 | 🔄 9% |
| languages/c++ | 67 | 2 | 🔄 2% |
| languages/rust | 102 | 3 | 🔄 2% |
| operating_systems/linux-systems-programming | 75 | 2 | 🔄 2% |
| databases/elasticsearch-for-developers | 35 | 1 | 🔄 2% |
| devops/advanced-kubernetes | 49 | 1 | 🔄 2% |
| ai/developing-using-ai-short | 47 | 1 | 🔄 2% |
| ai/advanced-ai-powered-development | 52 | 1 | 🔄 1% |
| architecting/architecting | 122 | 1 | 🔄 0% |
| big_data/advanced-spark-with-python | 145 | 2 | 🔄 1% |
| git/git | 39 | 1 | 🔄 2% |
| git/git2 | 125 | 1 | 🔄 0% |
| hardware/computer-architecture-fundamentals | 65 | 1 | 🔄 1% |
| networking/linux-networking-overview | 44 | 1 | 🔄 2% |
| operating_systems/advanced-android-application-development | 49 | 1 | 🔄 2% |
| operating_systems/embedded-linux-platform-development-with-yocto | 50 | 1 | 🔄 2% |
| operating_systems/linux-kernel-advanced-topics | 45 | 1 | 🔄 2% |
| operating_systems/linux-system-administration | 28 | 1 | 🔄 3% |
| security/cyber-attacks-and-vectors | 97 | 1 | 🔄 1% |
| security/linux-forensics | 28 | 1 | 🔄 3% |
| security/web-application-hacking | 64 | 2 | 🔄 3% |
| ai/developing-using-ai | 129 | 0 | ⬜ Not started |
| big_data/apache-spark-with-scala | 136 | 0 | ⬜ Not started |
| build_systems/cmake | 6 | 0 | ⬜ Not started |
| cloud/introduction-to-azure | 38 | 0 | ⬜ Not started |
| databases/redis | 116 | 0 | ⬜ Not started |
| devops/architectural-decisions-in-devops | 141 | 0 | ⬜ Not started |
| devops/docker-for-developers | 106 | 0 | ⬜ Not started |
| devops/welcome-to-the-world-of-devops | 105 | 0 | ⬜ Not started |
| networking/networking-basics | 71 | 0 | ⬜ Not started |
| operating_systems/qemu-for-kernel-developers | 15 | 0 | ⬜ Not started |

## Overall totals

| | Count |
|--|------:|
| Total SVGs in repo | 3116 |
| Improved (using our defs) | 243 |
| Not yet improved | 2873 |
| **% complete** | **7.8%** |

## Next up (partial courses, sorted by remaining work)

| Course | Remaining | Priority |
|--------|----------:|---------|
| architecting/modern-software-architecture | 94 | next |
| devops/k8s-introduction | 83 | next |
| operating_systems/linux-fundamentals | 83 | next |
| ai/generative-ai-applications | 132 | next |
| languages/rust | 99 | next |
| languages/c++ | 65 | next |
| operating_systems/linux-systems-programming | 73 | next |
| devops/terraform | 34 | next |

## How to update this file

```bash
# Overall
grep -rl 'grad-accent' svg/courses/ | wc -l

# Per course
for course in $(find svg/courses/ -mindepth 2 -maxdepth 2 -type d | sed 's|svg\/courses\///||' | sort); do
    total=$(find svg/courses/$course -name '*.svg' | wc -l)
    ours=$(grep -rl 'grad-accent' svg/courses/$course 2>/dev/null | wc -l)
    echo "$course | $total | $ours"
done
```
