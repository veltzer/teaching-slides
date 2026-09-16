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

# SDD on a Real Team

## Overview
- Brownfield reality: specifying inside a codebase that has no specs
- Specs in the team workflow: review, living documentation, ownership
- Pitfalls: drift, ceremony creep, the spec nobody reads
- When not to use `SDD`, and the honest cost-benefit line
- Adopting `SDD` incrementally, with a checklist for the first month

---

## Brownfield Reality

![brownfield_baseline_spec](svg/courses/ai/spec-driven-development-with-ai/05_sdd_on_a_real_team/brownfield_baseline_spec.svg)

---

## Reverse-Engineering a Baseline Spec

- Do not specify the whole legacy system; specify the part the feature touches

```markdown
Read src/audit/ and its tests. Write docs/specs/000-audit-baseline.md
describing what the module does today: inputs, outputs, error behavior,
limits, and every quirk you notice. Use EARS sentences. Mark anything
you cannot determine from the code as UNKNOWN. Do not suggest changes.
```

- Review the baseline with someone who remembers the history: bug or contract?
- Pin the behaviors you keep with characterization tests before changing anything
- The feature spec is then written as a delta: keep, change, add
- The baseline becomes the first documentation the module ever had

---

## Specs in the Team Workflow

- **Spec review as a pull request**: the spec lands in a branch before code
    - Product approves requirements, an architect the plan; comments here are cheap
- **Specs as living documentation**: `docs/specs/` answers "why does it work this way?"
    - New joiners read the last five specs and understand the system; the agent reads them too
- **Ownership**: every spec names an owner in its header
    - The owner updates it when behavior changes and archives it when the feature dies
    - Orphaned specs are deleted, not kept; a wrong spec is worse than none

---

## Pitfalls

- **Spec drift**: code moved on, spec did not
    - Cause: fixes made directly in code, hot-fixes under pressure
    - Guard: the audit prompt in CI on every pull request, a hook that flags touched modules
- **Ceremony creep**: a three-file spec for a one-line fix
    - Guard: a size rule, for example "spec required above half a day of work"
    - Small fixes still cite the criterion they restore
- **The spec nobody reads because it is too long**
    - Guard: word budgets per section, one screen for requirements
    - If the agent needs a summary to use it, so do the humans

---

## When Not to Use SDD

- Exploration and spikes: you do not yet know what to specify; write the spec *after* the spike
- Throwaway prototypes and demos that will not be maintained
- Trivial changes where the ticket already is the spec
- Work where the cost is in discovering the requirement, not in implementing it
- Rule of thumb: if you could not write an acceptance criterion, you are not ready for `SDD` yet
- A spike that succeeds becomes the input to a spec, never the shipped code

---

## The Honest Cost-Benefit Line

| Situation | Spec cost | Payoff |
|---|---|---|
| One-hour fix, one developer | High relative | None |
| One-day feature, one developer | Moderate | Fewer re-prompts, reviewable PR |
| Multi-day feature, parallel agents | Low relative | Large: shared contract |
| Feature in a legacy module | High | Large: baseline plus safety net |
| Handover to another team | Low | Large: the spec is the handover |

- The cost is roughly fixed per feature; the payoff scales with size, risk and headcount
- Track re-prompts and review rounds before and after; that is the metric that convinces skeptics

---

## Adopting SDD Incrementally

![adoption_roadmap](svg/courses/ai/spec-driven-development-with-ai/05_sdd_on_a_real_team/adoption_roadmap.svg)

---

## A Checklist for the First Month

- Week 1
    - One volunteer, one feature, one template copied into `docs/specs/`
    - Spec reviewed as a pull request before any code
- Week 2
    - Plan and task review added; implementation one task per run
- Week 3
    - Second-agent audit before merge; spec becomes the PR description
    - First amendment made through the spec, not around it
- Week 4
    - Constitution written from what the reviews kept repeating
    - Retro: keep, drop or change the template; decide whether to widen
