# Content Review Progress

Review every course and lecture for content: fix wrong info, add where useful, improve slides, prune stale content. Build after each change. Start date: 2026-04-22.

## Review guidelines

- Pass: read every chapter file; flag factual errors, outdated info, dead examples.
- Edit: fix small/medium issues directly. For larger rewrites, note and continue.
- Build: run `rsconstruct build --verbose -j10` after each unit; fix any failure before marking complete.
- Unchanged units are still marked `[x]` if a full read confirmed no issues.

## Calibration (from user, 2026-04-22)

1. **Do a good review. Find typos too.** Full-depth review including prose polish (typos, apostrophes, capitalization, asterisk balance, heading consistency).
2. **All units are in priority.** Work through the list in order; no cherry-picking.
3. **Leave the user's opinions alone.** Provocative lines ("Fire them!", "Stop using MS-Windows", strong stances on tools/practices) are the user's voice — do not soften, hedge, or remove.
4. **Free to add or remove content.** If a topic needs a missing slide, add it. If a slide is redundant or wrong beyond repair, remove it. Same latitude for SVG drawings: add where needed, drop where stale. Use judgment; stay within the user's voice.

## Legend

- `[ ]` not started
- `[~]` in progress (opened but not finished)
- `[x]` reviewed (read fully + build green)

## Courses (53)

- [ ] ai/advanced-ai-powered-development (12 files)
- [ ] ai/developing-using-ai (15 files)
- [ ] ai/generative-ai-applications (21 files)
- [ ] architecting/architecting (14 files)
- [ ] architecting/modern-software-architecture (12 files)
- [ ] big_data/advanced-spark-with-python (11 files)
- [ ] big_data/apache-spark-with-python (8 files)
- [ ] big_data/apache-spark-with-scala (9 files)
- [ ] build_systems/cmake (9 files)
- [ ] build_systems/make (6 files)
- [ ] cloud/architecting-in-the-cloud (14 files)
- [ ] cloud/finops (9 files)
- [ ] cloud/introduction-to-aws (9 files)
- [ ] cloud/introduction-to-azure (11 files)
- [ ] cloud/introduction-to-cloud-computing (14 files)
- [ ] cloud/multi-cloud-strategy (14 files)
- [ ] databases/elasticsearch-for-developers (18 files)
- [ ] databases/redis (10 files)
- [ ] devops/advanced-docker (7 files)
- [ ] devops/advanced-kubernetes (16 files)
- [ ] devops/ansible (18 files)
- [ ] devops/architectural-decisions-in-devops (16 files)
- [ ] devops/docker-for-developers (14 files)
- [ ] devops/github-workflows (9 files)
- [ ] devops/k8s-introduction (16 files)
- [ ] devops/terraform (16 files)
- [ ] devops/welcome-to-the-world-of-devops (14 files)
- [ ] embedded/effective-real-time-embedded-c-and-c++ (20 files)
- [ ] git/git (22 files)
- [ ] hardware/computer-architecture-fundamentals (7 files)
- [ ] languages/assembly/assembly-programming-using-gas (21 files)
- [ ] languages/bash/bash-scripting (26 files)
- [ ] languages/c++/c++-design-patterns (26 files)
- [ ] languages/c++/modern-c++-for-c-programmers (19 files)
- [ ] languages/c/c-refresher (16 files)
- [ ] languages/python/advanced-python (21 files)
- [ ] languages/python/python-programming (15 files)
- [ ] languages/rust/advanced-rust (10 files)
- [ ] languages/rust/rust-programming (12 files)
- [ ] networking/linux-networking-overview (11 files)
- [ ] networking/networking-basics (9 files)
- [ ] operating_systems/advanced-android-application-development (16 files)
- [ ] operating_systems/embedded-linux-platform-development-with-yocto (12 files)
- [ ] operating_systems/linux-fundamentals (13 files)
- [ ] operating_systems/linux-kernel-advanced-topics (12 files)
- [ ] operating_systems/linux-system-administration (15 files)
- [ ] operating_systems/linux-systems-programming (24 files)
- [ ] operating_systems/qemu-for-kernel-developers (10 files)
- [ ] security/cyber-attacks-and-vectors (29 files)
- [ ] security/it-security-policies (8 files)
- [ ] security/linux-forensics (14 files)
- [ ] security/web-application-hacking (22 files)
- [ ] security/working-with-llms-securely (12 files)

## Lectures (34)

- [ ] architecting/distributed-systems-concepts.md
- [ ] architecting/idempotency.md
- [x] architecting/senior-level-development.md
- [ ] architecting/solid.md
- [ ] big_data/advanced-spark-ecosystem-and-best-practice-python.md
- [ ] big_data/advanced-spark-ecosystem-and-best-practice-scala.md
- [ ] big_data/spark-internals.md
- [ ] big_data/spark-notebooks.md
- [ ] big_data/spark-optimization-python.md
- [ ] big_data/spark-optimization-scala.md
- [ ] big_data/spark-reports.md
- [ ] big_data/spark-scala-datasets.md
- [ ] big_data/spark-sql-optimization-python.md
- [ ] big_data/spark-ui.md
- [ ] build_systems/gcc-optimizations.md
- [ ] cloud/azure-boards.md
- [ ] databases/acid.md
- [ ] databases/data_formats.md
- [ ] databases/nosql-database-fundamentals.md
- [ ] databases/sql-database-fundamentals.md
- [ ] devops/devops-slides.md
- [ ] devops/eks.md
- [ ] devops/logstash.md
- [ ] embedded/microcontroller-bootloader.md
- [ ] git/git-workflows.md
- [ ] languages/c++17.md
- [ ] languages/scala-basics.md
- [ ] operating_systems/iouring.md
- [ ] operating_systems/isolation-in-computing.md
- [ ] operating_systems/linux-io.md
- [ ] operating_systems/linux-kernel-and-interrupts.md
- [ ] operating_systems/virtio.md
- [ ] operating_systems/writing-netfilter-modules.md
- [ ] operating_systems/zero-copy-linux.md

## Notes per unit

### architecting/senior-level-development.md (2026-04-22)
Fixed: asterisk-mismatch on microservices bullet (`*Independently Testable**` → `**...**`); `codes` → `code's`; `Micro-services` → `Microservices` for consistency; lowercase `windows` → `Windows`; `it's` → `its`; converted visible `[comment:]` lines at the end into a proper HTML comment TODO block.

