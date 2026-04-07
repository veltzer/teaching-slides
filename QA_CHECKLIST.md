# QA Checklist — Visual Pipeline Verification

Open each PDF in `_site/marp/` and verify that all images render correctly.

## SVG diagrams (hand-drawn)

- [ ] `_site/marp/courses/operating_systems/linux-fundamentals/01_intro.pdf`
  — Has history_of_unix, process_lifecycle, security model diagrams + JPG photos
- [ ] `_site/marp/courses/operating_systems/linux-fundamentals/10_networking_basics.pdf`
  — Multiple networking SVGs

## SVG diagrams (many per file)

- [ ] `_site/marp/courses/big_data/apache-spark-with-scala/08_optimization_tuning.pdf`
  — 24 SVG diagrams, good stress test

## Mermaid-generated SVGs

- [ ] `_site/marp/courses/architecting/modern-software-architecture/05_microservices_design_patterns.pdf`
  — 13 mermaid diagrams (saga, CQRS, service discovery, etc.)
- [ ] `_site/marp/courses/architecting/modern-software-architecture/11_devops_and_cicd_for_architects.pdf`
  — 12 mermaid diagrams (CI/CD, deployment strategies, GitOps)

## JPG photos

- [ ] `_site/marp/courses/operating_systems/linux-systems-programming/00_title.pdf`
  — Linus Torvalds photo
- [ ] `_site/marp/courses/languages/python/python-programming/01_introduction_to_python.pdf`
  — Guido van Rossum photo
- [ ] `_site/marp/courses/languages/c/c-refresher/01_c_programming_review.pdf`
  — Dennis Ritchie photo

## Mixed content

- [ ] `_site/marp/courses/languages/python/advanced-python/17_porting_2_to_3.pdf`
  — Had many placeholder icons removed; verify no broken images remain
- [ ] `_site/marp/lectures/iouring.pdf`
  — Has mermaid diagrams + regular SVGs
