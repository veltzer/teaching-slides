---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:architecture
- concepts:microservices
level: intermediate
category: ai
audience:
- audiences:developers
- audiences:architects
- audiences:team-leads

---

# LLMs on Large Codebases
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/llms_large_projects/title.svg)

---

## What This Lecture Covers

1. Why large codebases are hard for LLMs — monoliths and microservices alike
1. The disciplined workflow: scope, locate, plan, change, verify, review
1. Context strategy: getting the right slice of a huge system into the model
1. Durable project knowledge: making every session start informed
1. Monolith-specific and microservice-specific tactics
1. Guardrails: types, tests, CI, and human review
1. Pitfalls, anti-patterns, and good habits

---

## The Problem

- LLMs look magical on demos: small, fresh, self-contained projects
- Your reality is different: millions of lines, years of history, real users
- Naive use on a large system produces confident, plausible, *wrong* changes
- The tool is not broken — the *method* is
- This lecture is about the method

---

## The Core Idea

> On a large project, the LLM is a **power tool**, not a **colleague**.
> You aim it at a small, well-defined piece of work, and you verify everything it produces.

- The larger the system, the smaller each step must be
- The engineer stays responsible for every merged line

---

## Why Scale Breaks Naive Usage

![scale_problem](svg/lectures/ai/llms_large_projects/scale_problem.svg)

---

## The Model Starts Nearly Blind

- A medium codebase is **millions of tokens**; the window holds a fraction
- The model sees only what you (or your agent tooling) load into it
- Everything else, it *guesses* — from patterns learned on other codebases
- Those guesses are plausible, idiomatic, and often wrong for *your* system

---

## What the Code Does Not Say

- Large systems run on **implicit knowledge**:
    - conventions that are followed but written nowhere
    - invariants that must never break, guarded only by habit
    - historical reasons why the "obvious" fix was rejected twice already
- An LLM cannot know any of this unless someone writes it down
- Monolith or microservices — this problem is identical in both

---

## Greenfield vs Brownfield

- Greenfield: no constraints, any consistent answer is acceptable
- Brownfield: the answer must fit an existing web of constraints
- LLMs are trained to produce *typical* code — brownfield needs *conforming* code
- The gap between typical and conforming is where the damage happens
- Closing that gap is *your* job: context, constraints, and verification

---

## The Disciplined Workflow

![workflow](svg/lectures/ai/llms_large_projects/workflow.svg)

---

## Step: Scope the Task

- Cut work into slices that are **small, verifiable, and reversible**
- One behavior change, one refactoring step, one bug — per slice
- If you cannot describe the "done" condition in one sentence, split it
- Big-bang requests ("modernize this module") produce big-bang damage

---

## Step: Locate Before You Generate

- First question is never "write the code" — it is "**where** does this live?"
- Let the model search: grep, glob, code index, call hierarchy
- Have it *show you* the relevant files and explain the current behavior
- Only when the location and behavior are agreed — ask for the change

---

## Step: Plan, Then Change

- Ask for a plan first: files to touch, approach, risks
- Review the plan like you would review a design note
- A wrong plan costs a minute; wrong code costs a review cycle — or an incident
- Then let it implement the *approved* plan, nothing more

---

## Step: Verify and Review

- Run the build, the linters, and the tests — every single iteration
- Read the diff line by line, as if a stranger wrote it — because one did
- Push back: the model revises cheaply and without ego
- Nothing is merged unread; there is no exception for "it looks fine"

---

## Context Strategy

![context_funnel](svg/lectures/ai/llms_large_projects/context_funnel.svg)

---

## Search First, Read Second

- Never let the model "read the repo to get familiar" — it cannot, and it will pretend
- Narrow with search, then read only the surviving files, then only the relevant sections
- Keep the window lean: irrelevant code actively *distracts* the model
- Re-fetch on demand beats hoarding — files do not change mid-task

---

## Ground Every Claim in Real Code

- The model must quote the actual code it is about to change
- "Show me the current implementation before proposing the fix"
- If it references a function, make it open that function
- Ungrounded answers are pattern-completion — treat them as rumors

---

## Subagents and Fresh Sessions

- Exploration burns context fast — delegate it
- A subagent searches with its *own* window and returns only conclusions
- Between unrelated tasks, clear the session; carry over facts via files
- One task, one focused context — never a mega-session for a mega-project

---

## Durable Project Knowledge

![knowledge_base](svg/lectures/ai/llms_large_projects/knowledge_base.svg)

---

## Write the Unwritten Rules

- Project instruction files (e.g. `CLAUDE.md`) load into **every** session
- Put in them what you keep re-explaining:
    - build, test, and run commands
    - coding conventions and forbidden patterns
    - architectural boundaries the model must respect
- Version them in the repo — they are team assets, not personal notes

---

## Documentation the Model Can Use

- ADRs: *why* decisions were made — stops the model re-litigating them
- A code map: what lives where, which module owns what
- Runbooks: how deployment, migrations, and releases actually work
- Every hour spent here pays off in every future session — human or LLM

---

## The Feedback Loop

- Model violates a convention → add the convention to the instructions file
- Model misunderstands a module → improve that module's documentation
- The corrections compound: sessions start smarter every week
- An LLM is a mirror for your documentation debt — use it as one

---

## Working on a Monolith

![monolith](svg/lectures/ai/llms_large_projects/monolith.svg)

---

## Monolith: The Coupling Trap

- Everything can reach everything — a small edit has a large blast radius
- The model cannot see the whole tangle, so it underestimates impact
- Ask explicitly: "who calls this? who depends on this behavior?"
- Make the model enumerate callers *before* approving any signature change

---

## Monolith: Work the Seams

- Find the seam: the smallest boundary that isolates the change
- Characterization tests first — pin current behavior before touching it
- Refactor in steps small enough that tests stay green between them
- The LLM is excellent at *writing* those tests — use it for that first

---

## Working Across Microservices

![microservices](svg/lectures/ai/llms_large_projects/microservices.svg)

---

## Microservices: The Cross-Cutting Trap

- One feature = changes in several repos, owned by several teams
- No session sees all services — the model reasons about each in isolation
- Contracts (APIs, events, schemas) are where LLM changes silently break things
- Never let a model change both sides of a contract in one blind step

---

## Microservices: Tactics

- Work **one service at a time**, with the contract as the fixed reference
- Give the model the API spec, not your memory of it
- Contract tests and schema checks catch what review misses
- For cross-service tracing, feed it logs and traces — not guesses

---

## Guardrails

![guardrails](svg/lectures/ai/llms_large_projects/guardrails.svg)

---

## Machines Check Before Humans Do

- Every LLM change runs the same gauntlet as human code — automatically
- Types, linters, and formatters kill a whole class of errors instantly
- Tests are your specification: the model must make them pass, not delete them
- CI is non-negotiable; a red pipeline stops the merge, no matter who wrote it

---

## The Human Gate

- Review LLM code *more* carefully, not less — it looks deceptively polished
- Watch for: invented APIs, silently changed behavior, deleted edge cases
- Small diffs enable real review; huge diffs get rubber-stamped
- The author of record is **you** — "the AI wrote it" is not a defense

---

## Team Discipline

- Shared instruction files in the repo — not private prompt collections
- Agree on what LLMs may touch: generated code, tests, migrations, docs
- State LLM usage in the PR when it matters for review depth
- Onboard people on *this* workflow — the tool without the method is a hazard

---

## Common Pitfalls

![pitfalls](svg/lectures/ai/llms_large_projects/pitfalls.svg)

---

## Pitfall: The Big-Bang Refactor

- "Migrate the whole module" produces a 5,000-line unreviewable diff
- Somewhere in it, three behaviors changed silently
- **Fix:** slice by seam; each step compiles, passes tests, and gets reviewed

---

## Pitfall: Hallucinated Internals

- The model calls `utils.retry_with_backoff()` — which does not exist in your repo
- It *should* exist in a typical project; yours is not typical
- **Fix:** grounding — the model reads real files, and the build catches the rest

---

## Pitfall: Erosion by a Thousand Merges

- Each LLM change is fine alone; together they drift from your architecture
- Conventions dilute, layers blur, duplication creeps in
- **Fix:** encode the architecture in instructions and lint rules; audit periodically

---

## Pitfall: Trust Creep

- Week 1: you read every line — week 10: you skim and merge
- The model did not get better at *your* system; you got comfortable
- **Fix:** keep diffs small enough that real review stays cheap forever

---

## Good Habits

- One task per session; clear between tasks; files carry the memory
- Locate and plan before generating; ground every claim in real code
- Keep every diff small enough to review honestly
- Let the machines check first; never merge with a red pipeline
- Feed every correction back into the project knowledge files

---

## The Mental Model

![mental_model](svg/lectures/ai/llms_large_projects/mental_model.svg)

---

## A Brilliant Hire, Every Day Is Day One

- The LLM is a superbly skilled engineer with **no memory of your project**
- You would not let such a hire push to a million-line system unsupervised
- You would onboard them: docs, conventions, small first tasks, close review
- Do exactly that — every session, automatically, via files and workflow

---

## Summary

- Large systems break naive LLM use: the model sees fragments and guesses the rest
- Discipline wins: **scope small, locate first, plan, verify, review everything**
- Context is a scarce resource: search, ground, delegate, keep it lean
- Durable knowledge files turn every correction into a permanent upgrade
- Guardrails — types, tests, CI, human review — are what make speed safe

---

## Where to Start

1. Add an instructions file with build commands and your top ten conventions
1. Pick one small, real maintenance task and run the full workflow on it
1. Note every correction you had to make — move each into the project files
1. Only then scale up: more tasks, more people, same discipline

The method is the product: the model is only as good as the system around it.

---

## Questions?

- The model is a power tool: aim it small, verify everything
- Context, knowledge files, and guardrails do the heavy lifting
- Same discipline for monoliths and microservices — only the seams differ

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
