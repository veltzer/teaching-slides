# Syllabi → Materials Tracker

Tracks the work of writing slide materials for syllabi in `../teaching-syllabi/` that don't yet have corresponding course material in `marp/courses/`.

## Source of truth

- Syllabi: `../teaching-syllabi/syllabi/courses/<domain>/<course>.md`
- Materials: `marp/courses/<domain>/<course-with-dashes>/`

The diff at session start: 549 syllabi, 50 with material, **529 without material**.

## Status legend
- [ ] not started
- [~] in progress
- [x] done (all chapters written, builds clean)
- [-] decided not to write (out of scope, deprecated, etc.)

## Process per course

For each course:
1. Read the syllabus to extract chapters and durations.
2. Create `marp/courses/<domain>/<course-with-dashes>/` directory.
3. Write `00_title.md` plus one `NN_<chapter>.md` per syllabus chapter.
4. Add `title.svg` and any per-chapter SVGs the material references.
5. Run `rsconstruct build --verbose -j10` and resolve all errors.
6. Mark the entry below `[x]` and commit (user commits, not me).

## In progress

_(none — pick a new course from the backlog)_

## Done

- [x] **architecting/cqrs_and_event_sourcing** — 9 chapters + title; 16h advanced course; 33 SVGs; build clean

## Backlog

The full list of 529 missing courses lives in the repo as `/tmp/missing_courses.txt` at session start (regenerable). The high-priority near-term subset is below; remaining courses are tracked by domain and re-prioritized when this section empties.

### ai
- [ ] ai_agents_development
- [ ] prompt_engineering
- [ ] rag_applications
- [ ] mlops
- [ ] nlp_with_python
- [ ] computer_vision_with_python
- [ ] llm_fine_tuning_and_prompt_engineering
- [ ] reinforcement_learning
- [ ] ai_ethics_and_responsible_ai
- [ ] explainable_ai
- [ ] federated_learning
- [ ] rag_deep_dive
- [ ] using_ai_when_developing_applications

### architecting
- [ ] introduction_to_architecting
- [ ] domain_driven_design
- [ ] microservices_architecture
- [ ] event_driven_architecture
- [x] cqrs_and_event_sourcing
- [ ] saga_pattern
- [ ] api_design_best_practices
- [ ] api_first_development
- [ ] api_gateway_patterns
- [ ] clean_and_hexagonal_architecture
- [ ] data_mesh
- [ ] disaster_recovery
- [ ] distributed_systems_fundamentals
- [ ] enterprise_architecture
- [ ] event_driven_architecture_with_kafka
- [ ] large_scale_architecting
- [ ] legacy_modernization
- [ ] message_queues
- [ ] modern_software_architecture
- [ ] serverless_architecture
- [ ] site_reliability_engineering
- [ ] sre_practices
- [ ] system_design
- [ ] twelve_factor_app
- [ ] uml
- [ ] web_architecture_and_scaling
- [ ] cloud_monolith_microservices_cloudnative_servicmesh

(Other 22 domains tracked in `/tmp/missing_courses.txt`. Pull into this file as work progresses.)

## Notes

- Each course is roughly 8-15 chapters × ~700-1500 lines of well-written content + per-chapter SVGs. Writing one course end-to-end is several hours of focused work; this is a long-running task.
- Default style follows existing courses (e.g. `marp/courses/ai/developing-using-ai/`): plain headings (no "Part N:"), `1. 1. 1.` ordered lists, dash bullets, project-root-relative SVG paths, palette-compliant SVGs.
- Skip syllabi that overlap heavily with already-written courses unless the syllabus introduces meaningfully different angle/depth.
