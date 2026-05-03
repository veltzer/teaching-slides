---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Code Review Goals

---

## Goal Dimensions

![goal_dimensions](svg/courses/development_methodologies/code-review-best-practices/02_code_review_goals/goal_dimensions.svg)

---
## What This Chapter Covers

- The goals of a code review
- Correctness, readability, maintainability
- Knowledge sharing
- Trade-offs between thoroughness and speed
- A goals checklist
- When goals conflict

---
## A Code Review Has Goals

- Without goals, reviews drift to bikeshedding
- Each review should know which goals matter most
- Different changes &#8594; different priorities
- A documented set of goals aligns the team
- "Why are we doing this?" should always have an answer

---
## Goals at a Glance

![review_goals](svg/courses/development_methodologies/code-review-best-practices/02_code_review_goals/review_goals.svg)

---
## Goal: Correctness

- Does the code do what it says?
- Does it handle the obvious edge cases?
- Are there logic errors or off-by-ones?
- Is concurrency handled (if relevant)?
- The most important goal — but not always sufficient

---
## Goal: Readability

- Will another developer understand this in 6 months?
- Are names meaningful?
- Is the structure clear?
- Could a junior developer maintain it?
- Code is read 10x more than written; readability compounds

---
## Goal: Maintainability

- Can this change be safely modified later?
- Are there tests?
- Are the abstractions reasonable?
- Does it fit the existing patterns?
- Trade-off: heavy abstractions vs simple code

---
## Goal: Knowledge Sharing

- Does the reviewer learn something?
- Does the author?
- Are there opportunities to mentor?
- Does the change document a decision?
- A side benefit; should not be the *only* benefit

---
## Goal: Style and Consistency

- Does it follow the project's conventions?
- Most of this should be automated (linters, formatters)
- Reviews catch what tools can't: naming, structure, idiom
- Style should not dominate; substance does
- Comment "nit:" prefix for style nitpicks

---
## Goal: Security

- Does it introduce vulnerabilities?
- SQL injection, XSS, auth flaws
- Secret in source code?
- Third-party deps with known CVEs?
- Reviews catch some of this; specialists catch the rest

---
## Goal: Performance

- Will this scale?
- Are there obvious inefficiencies (N+1 queries, etc.)?
- Profile before assuming
- Premature optimisation is the bigger risk
- Block on performance only when it's clear and measurable

---
## Thoroughness vs Speed

- Thorough review catches more, costs more time
- Fast review preserves momentum, may miss issues
- Match thoroughness to risk: critical code &#8594; thorough; trivial &#8594; quick
- Don't apply the same rigour everywhere
- Reviews waiting for days are themselves a cost

---
## When Goals Conflict

- Readable code may be less performant
- Strict typing may slow development
- Comprehensive tests may delay shipping
- Reviewers should articulate the trade-off, not just push their preference
- Authors and reviewers negotiate; team norms guide

---
## Setting Goals Per PR

- A bug fix: correctness first; small change; quick review
- A new feature: design + correctness + tests
- A refactor: behaviour preserved; tests unchanged
- A doc change: clarity; little risk
- A perf change: numbers, not vibes

---
## Documenting Team Goals

- A short doc: "what we look for in PRs"
- Linked from the PR template
- Reviewed quarterly
- Saves the same arguments happening repeatedly
- Onboarding new developers faster

---
## Goals by Maturity

- Junior dev's PR: focus on learning + correctness
- Senior dev's PR: focus on design + maintainability
- Cross-team PR: focus on integration + agreement
- Match feedback intensity to context
- Reviews aren't one-size-fits-all

---
## Common Mistakes

- No stated goals &#8594; bikeshedding
- "Be thorough" applied to every PR &#8594; reviews stack up
- Treating reviews as a quality gate only &#8594; missing the learning side
- Ignoring small PRs &#8594; the smallest changes break production
- Treating goals as immutable &#8594; teams evolve, goals should too
