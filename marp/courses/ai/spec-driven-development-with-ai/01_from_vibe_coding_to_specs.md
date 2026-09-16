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

# From Vibe Coding to Specs

## Overview
- Why prompt-by-prompt development stops working once a task spans more than one sitting
- The core idea of Spec-Driven Development (`SDD`): the specification is the source of truth
- How `SDD` relates to `TDD`, `BDD` and `DDD`, and why it is not waterfall in disguise
- Where the spec lives in a sprint, who writes it and who reviews it

---

## How Prompt-by-Prompt Development Fails

![prompt_by_prompt_decay](svg/courses/ai/spec-driven-development-with-ai/01_from_vibe_coding_to_specs/prompt_by_prompt_decay.svg)

---

## Three Failure Modes at Scale

- **Decisions made in chat and lost forever**
    - "Use 15 minute expiry" lives in message 12 of a 90 message thread
    - Nobody can find it a week later, including the agent
- **The agent that forgets what you agreed on**
    - Context windows are finite and compaction is lossy
    - Every new session starts from the code, not from the intent
- **Code that matches the last prompt, not the goal**
    - "Fix the failing test" is obeyed literally
    - The fix may undo a constraint you stated three prompts earlier
- Small tasks survive this; a two-day feature does not

---

## The Core Idea of SDD

![spec_as_source_of_truth](svg/courses/ai/spec-driven-development-with-ai/01_from_vibe_coding_to_specs/spec_as_source_of_truth.svg)

---

## Iterating on the Spec Instead of Re-Prompting

- In vibe coding the prompt is disposable; in `SDD` the spec is versioned
- When the agent produces the wrong thing, ask: *what in the spec allowed that?*
    - Missing constraint: add it to the spec, re-run
    - Ambiguous wording: sharpen it, re-run
    - The spec was right: the agent violated it, reject the diff
- The fix goes into the document, so the next run and the next developer inherit it

```markdown
<!-- before -->
Exports should be fast.

<!-- after -->
When a user requests an export of up to 100,000 rows,
the system shall return the file within 30 seconds.
```

---

## Reviewing Code Against a Written Contract

- Without a spec, review asks "does this look reasonable?"
- With a spec, review asks "does this diff satisfy criteria 3, 4 and 7?"
- Concrete review questions the spec makes possible:
    - Which acceptance criterion does this change serve?
    - Which edge case in the spec is not covered by a test?
    - Did the agent change anything the spec does not mention?
- The reviewer no longer needs to reconstruct the intent from the diff
- `AI` reviewers benefit even more: they read the spec and the diff in one context

---

## SDD and Its Relatives

![sdd_and_its_relatives](svg/courses/ai/spec-driven-development-with-ai/01_from_vibe_coding_to_specs/sdd_and_its_relatives.svg)

---

## Why SDD Is Not Big Design Up Front

- The waterfall fear: months of documents, then code that ignores them
- `SDD` differs on every axis that made waterfall fail

| Waterfall spec | `SDD` spec |
|---|---|
| Whole system | One feature |
| Months before code | Hours before code |
| Frozen after sign-off | Amended when reality wins |
| Read by humans once | Read by the agent on every run |
| Separate from the code | Committed next to the code |

- `TDD` gives you tests as spec; `BDD` gives you Gherkin precision; `DDD` gives you the vocabulary
- `SDD` combines them into prose the agent can act on and the reviewer can check

---

## Where SDD Fits in a Sprint

- A user story is the *input* to a spec, not the spec itself
    - Story: "As an admin I want to export audit logs"
    - Spec: stories plus acceptance criteria, limits, errors, non-goals, plan, tasks
- Who writes what:
    - The developer taking the story drafts the requirements, often with the agent
    - Product or the story author reviews the requirements
    - An architect or senior reviews the technical plan
    - The implementer owns the task list
- Timing: spec review happens in the first hours of the story, before any code
- Definition of ready for an `SDD` team: the requirements document is approved
