---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - data-and-ai:agents
  - concepts:code-generation
  - practices:methodology
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:team-leads
  - audiences:architects

---

# Anatomy of an AI-Consumable Spec

## Overview
- The three artifacts: requirements, technical plan, task list
- Writing requirements the agent cannot misread: stories, `EARS`, edge cases, open questions
- Writing the technical plan: constraints, interfaces, decisions
- The project constitution and what belongs in it
- Calibrating detail: under-specification, over-specification, and what to leave to the agent

---

## The Three Artifacts

![the_three_artifacts](svg/courses/ai/spec-driven-development-with-ai/02_anatomy_of_an_ai_consumable_spec/the_three_artifacts.svg)

---

## The Requirements Document: What and Why

- Answers *what* the feature does and *why* it exists; says nothing about *how*
- Sections that earn their place:
    - Goal in two sentences, plus the non-goals
    - User stories, each with acceptance criteria
    - Edge cases, error behavior, limits and quotas
    - Open questions, marked as such
- Written in the language of the domain, not of the framework
- Test for a good requirement: a stranger could tell whether the finished feature meets it
- The agent reads this document on every run, so it must be short enough to be read whole

---

## The Technical Plan: How and With What

- Answers *how* the requirements will be met inside this codebase
- Contents:
    - Constraints: stack, libraries, architecture rules, conventions
    - Interfaces: endpoints, function signatures, events
    - Data model changes and migrations
    - Decisions taken and alternatives rejected
    - Explicit non-goals, so the agent does not "helpfully" expand scope
- Usually drafted by the agent from the requirements, then corrected by a human
- Every requirement should be traceable to something in the plan

---

## The Task List: Implementation in Reviewable Steps

- Breaks the plan into steps the agent can finish in one focused run
- Each task states:
    - What to change, and where
    - Which requirement or plan item it serves
    - How to verify it is done, usually a test
- Ordered so every task leaves the codebase working

```markdown
- [ ] T3: Add `ExportJob` table and migration (plan section 2.1)
      Done when: migration applies cleanly, model test passes
- [ ] T4: Implement `POST /exports` returning 202 with a job id (REQ-2)
      Done when: contract test for REQ-2 passes
```

- Tasks are the unit of review: one task, one diff, one decision

---

## User Stories With Acceptance Criteria

- A story without criteria is a wish; the criteria are what the agent implements

```markdown
### Story 2: Export audit logs
As an admin, I want to export audit logs for a date range
so that I can hand them to an external auditor.

Acceptance criteria:
- AC-2.1 The export covers exactly the selected date range, inclusive
- AC-2.2 The file is CSV with a header row and UTF-8 encoding
- AC-2.3 Exports larger than 100,000 rows run as a background job
- AC-2.4 A non-admin user receives 403 and no file
```

- Number the criteria: tasks, tests and reviews will refer to them by id
- Each criterion is observable from outside the system

---

## The EARS Notation

![ears_requirement_patterns](svg/courses/ai/spec-driven-development-with-ai/02_anatomy_of_an_ai_consumable_spec/ears_requirement_patterns.svg)

---

## EARS in Practice

- Easy Approach to Requirements Syntax: five sentence shapes, one keyword each
- The shapes force you to name the trigger, the state, or the failure condition
- Rewriting a vague requirement:

```markdown
Vague:   The system should handle big exports gracefully.

EARS:    When an export request exceeds 100,000 rows,
         the system shall queue it as a background job
         and shall return 202 with a job id.

         If the queue is unavailable,
         then the system shall return 503 with a retry hint.
```

- `LLMs` handle the fixed shapes well: each sentence maps to one test and one branch
- `Kiro` generates `EARS` criteria by default; with other tools you ask for the format

---

## Making the Implicit Explicit

- The agent fills every gap with the most typical answer, which is rarely yours
- Walk each requirement through a checklist:
    - **Edge cases**: empty input, maximum size, duplicates, concurrent requests
    - **Errors**: what the user sees, what is logged, what is retried
    - **Limits**: sizes, rates, timeouts, retention
    - **Permissions**: who may, who may not, what they see instead
    - **Compatibility**: existing clients, existing data, feature flags
- Write down the boring answers too: "no pagination" is a decision, silence is not
- A short table of inputs and expected outcomes often beats paragraphs

---

## Marking Open Questions Instead of Hiding Them

- Unresolved questions are normal; unmarked ones are how the agent invents policy
- Keep an explicit section and keep it visible until empty

```markdown
## Open questions
- OQ-1: Should exports include soft-deleted records? (owner: product, due: Tue)
- OQ-2: Retention of generated files: 24 hours or 7 days? (owner: security)
```

- Instruct the agent: "if a task touches an open question, stop and ask"
- Resolving a question moves the answer into a requirement and deletes the question
- Review rule: a spec with open questions may be approved for planning, not for implementation

---

## Writing the Technical Plan: Constraints

- Constraints are the cheapest words in the spec; each one prevents a class of rewrites

```markdown
## Constraints
- Python 3.12, FastAPI, SQLAlchemy 2.x; no new dependencies without approval
- Follow the repository layout in docs/architecture.md
- All new endpoints are versioned under /api/v2
- No synchronous work longer than 2 seconds in request handlers
- Non-goals: no UI changes, no changes to the auth module
```

- Include what the agent cannot discover: team conventions, political boundaries, deprecations
- Point at existing code to imitate: "model after `reports/service.py`"

---

## Interfaces and Data Models Before Code

- Fix the boundaries first; the agent then fills in the inside

```python
class ExportRequest(BaseModel):
    start: date
    end: date            # inclusive, must be >= start
    format: Literal["csv"] = "csv"

class ExportJob(BaseModel):
    id: UUID
    status: Literal["queued", "running", "done", "failed"]
    download_url: str | None
```

- Interfaces are what other tasks, other agents and other teams depend on
- A reviewed interface lets tasks run in parallel without merge surprises
- Data model changes deserve their own review: migrations are the hardest thing to undo

---

## Recording Decisions and Rejected Alternatives

- The agent will re-propose every rejected idea unless the rejection is written down

```markdown
## Decisions
- D-1: Background jobs use the existing Celery queue.
  Rejected: a new worker service (operational cost), threads (no retries).
- D-2: Files are stored in S3 with a 24 hour pre-signed URL.
  Rejected: streaming responses (timeouts on large exports).
```

- One line per decision, one line per rejected option, one reason each
- These entries become the seed of the team's architecture decision records
- When a decision changes, edit the entry; do not append a contradiction

---

## The Project Constitution

![constitution_vs_feature_spec](svg/courses/ai/spec-driven-development-with-ai/02_anatomy_of_an_ai_consumable_spec/constitution_vs_feature_spec.svg)

---

## A Constitution Example

```markdown
# Constitution
1. Every behavior change ships with a test that fails without it.
1. Public interfaces are typed and documented before implementation.
1. No secrets, credentials or customer data in the repository or in prompts.
1. Errors are never swallowed; every failure path is logged with context.
1. A task is done only when lint, type check and the full test suite pass.
1. The agent never edits spec.md; it proposes amendments in the PR.
```

- Short enough to be included in every agent run
- Changes go through the same review as a code change, and rarely
- What does not belong: feature details, tool-specific commands, opinions without consequences

---

## Calibrating the Level of Detail

![level_of_detail_spectrum](svg/courses/ai/spec-driven-development-with-ai/02_anatomy_of_an_ai_consumable_spec/level_of_detail_spectrum.svg)

---

## Hands-On: Repair a Spec

- You receive a one-page requirements document for a "notification preferences" feature
- Work in pairs, 25 minutes, with your own agent

1. Rewrite every acceptance criterion in `EARS` form
1. Add the edge cases, errors and limits the document is silent about
1. Move any sentence that describes *how* into a draft technical plan
1. Mark at least two open questions with an owner
1. Ask the agent to list what it would still have to guess; fix what it finds

- Debrief: which gaps did the agent find that you missed, and which did it invent?
