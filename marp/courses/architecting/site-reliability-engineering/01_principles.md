---
tags:
  - practices:sre
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:sres
---
# SRE Principles

---

## What is SRE

Ben Treynor's definition (Google):

> "SRE is what happens when you ask a software engineer to design an operations team."

- A discipline that applies software engineering to operations problems
- Born at Google in 2003; principles published in 2016 in the SRE Book
- Now widespread: Netflix, Microsoft, Amazon, every cloud team
- Different teams adopt parts; the philosophy matters more than the title

---

## The core idea

Operations problems are software problems. If you treat them that way:

- You write code instead of running checklists
- You instrument before incidents, not after
- You measure reliability with numbers, not feelings
- You set explicit reliability targets and hold yourself to them
- You stop the work when the targets are missed

This is fundamentally different from "ops as a separate team that gets paged when devs break things."

---

## Five core tenets

1. **Embrace risk** — 100% reliability is the wrong target
1. 1. **Service Level Objectives** — define what reliable means, in numbers
1. 1. **Eliminate toil** — automate repetitive operational work
1. 1. **Monitor everything** — alert on symptoms, not causes
1. 1. **Automate this year's job away** — engineering, not babysitting

These compose: SLOs measure risk you took, error budgets translate risk into velocity, toil reduction frees time to do the engineering.

---

## The 50% rule

- Google's SRE charter: at most 50% of an SRE's time on operations
- The other 50% must go to engineering work — automation, tooling, building reliability
- If ops work creeps over 50%, push work back to dev teams
- This is what stops SRE from becoming "ops with extra steps"

The 50% isn't aspirational — it's enforced. Without it, you have no SRE, just operations.

---

## ![w:50](svg/courses/architecting/site-reliability-engineering/01_principles/sre_vs_ops.svg)

---

![](svg/courses/architecting/site-reliability-engineering/01_principles/sre_vs_ops.svg)

---

## Embracing risk

- A service with 99.999% uptime needs 100x more engineering than 99.9%
- Each "nine" costs exponentially more
- Most users cannot tell the difference between 99.9% and 99.99%
- Most users will quit using your service if features stop shipping
- So: pick a reliability target that matches user need, not engineer pride

The goal is not to be as reliable as possible. The goal is to be exactly as reliable as you need to be, leaving everything else for shipping features.

---

## SRE vs DevOps

| | DevOps | SRE |
|---|---|---|
| Origin | Cultural movement | Specific Google practice |
| Scope | Dev + ops collaboration | Reliability engineering specifically |
| Metrics | Loose (DORA, etc.) | Strict (SLOs, error budgets) |
| Ops cap | None enforced | 50% of time |
| Title | Often a label | Often a role |

> "Class SRE implements interface DevOps" — they are not in opposition.

---

## What SRE is NOT

- Not 100% uptime — that target wastes resources and blocks shipping
- Not a renamed ops team — without engineering culture, it is just ops
- Not a silver bullet — culture and management support are required
- Not free — SREs cost more than ops engineers
- Not for everything — small services may not need SRE

A team called "SRE" that does only ops work is a team called "SRE" that does only ops work. Names are not magic.

---

## Where to start

- Pick **one critical service** and define SLOs for it
- Stand up dashboards from existing metrics — don't build new infra
- Run **one blameless postmortem** for the next significant incident
- Track toil for one rotation; automate the worst item
- Measure: did the team's reliability or velocity change?

Big-bang SRE rollouts fail. Incremental adoption with measured outcomes succeeds.
