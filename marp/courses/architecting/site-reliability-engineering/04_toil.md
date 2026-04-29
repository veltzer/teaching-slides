---
tags:
  - practices:sre
  - practices:automation
level: intermediate
category: architecture
audience:
  - audiences:sres
  - audiences:devops
---
# Toil and Automation

---

## What counts as toil

Google's checklist — toil is work that is:

- **Manual** — needs a human to do it
- **Repetitive** — same actions repeated identically
- **Automatable** — could be replaced by code
- **Tactical** — interrupt-driven, not strategic
- **Devoid of long-term value** — produces nothing reusable
- **Scaling linearly with service growth** — twice the load = twice the work

If a task hits ≥3 of these, it is toil.

---

## Toil is not the same as "stuff I dislike"

- Architectural decisions feel tedious; not toil — produces value
- Code review feels repetitive; not toil — produces value (catches bugs)
- Filing tickets feels manual; some of it is toil, some of it is necessary
- "Operational overhead" includes toil but also genuine sysadmin judgment

The point of the checklist is to be honest. Not everything you dislike is toil.

---

## ![w:50](svg/courses/architecting/site-reliability-engineering/04_toil/toil_examples.svg)

---

![](svg/courses/architecting/site-reliability-engineering/04_toil/toil_examples.svg)

---

## Why toil is dangerous

- **Career stagnation** — engineers doing only toil don't grow
- **Burnout** — repetitive interrupt-driven work exhausts people
- **Hiring problems** — people quit; new hires inherit the toil
- **Compounding** — toil scales with service growth; you cannot grow out of it
- **Engineering capacity loss** — toil time is time not spent reducing future toil

A team buried in toil cannot stop being buried in toil. Someone has to drag them out.

---

## Measuring toil

```
toil_fraction = toil_hours / total_hours

Track per engineer per quarter:
- on-call hours (mostly toil)
- ticket queue time
- manual deploy/rollback time
- repetitive config changes
- "interrupt-driven" task hours
```

Google's target: toil ≤ 50% of an SRE's time. If higher, push work back to dev or hire more SREs.

---

## The toil reduction loop

1. **Track** — quarterly survey or time tracking
1. 1. **Rank** — top 5 toil sources by hours consumed
1. 1. **Pick one** — the worst, or the easiest to fix
1. 1. **Engineer** — write code, build tooling, automate
1. 1. **Measure** — did the toil go down?
1. 1. **Repeat** — next quarter, next item

This is engineering work. It belongs in the 50% engineering half of an SRE's time.

---

## Common toil sources and fixes

| Toil | Fix |
|---|---|
| Manual production deploys | CI/CD pipeline |
| Approving routine alerts | Auto-remediation, alert tuning |
| Provisioning new resources | Self-service portal, IaC |
| Rotating credentials | Secret manager with auto-rotation |
| Triaging tickets | Better routing, runbooks for common issues |
| Capacity expansion | Autoscaling |
| Rebooting flaky hosts | Health checks + auto-replacement |

The pattern: a person doing the same decision tree repeatedly is a script waiting to be written.

---

## The automation hierarchy

1. **No automation** — humans do everything
1. 1. **System-specific automation** — bash scripts per box
1. 1. **Externalised automation** — config files, central scripts
1. 1. **Internal automation** — system manages itself with operator approval
1. 1. **Autonomous automation** — system manages itself, alerts on anomalies
1. 1. **Self-healing** — system detects and fixes problems automatically

Most teams sit at level 2-3. The ROI on moving up the ladder is huge.

---

## When NOT to automate

- One-off tasks — you spend more building automation than you save
- Tasks done less than a few times a year — code rots between uses
- Tasks requiring human judgment — automating bad judgment makes it bigger
- Tasks where failure is silent and dangerous — keep a human in the loop

xkcd #1205: "Is It Worth The Time?" — the calculation matters. Automating things you do once a year is its own form of toil.

---

## Self-service as toil reduction

- Best toil reduction is shifting work to the people who need it
- Dev teams provisioning their own staging environments via portal
- Approval workflows that don't need an SRE in the loop
- Runbooks that any on-call engineer can execute
- Documentation that answers questions before they reach you

If SRE is the bottleneck for routine actions, the dev teams are slowed down too. Self-service helps everyone.

---

## Tracking toil over time

- Quarterly survey: each engineer estimates toil %
- Year-over-year comparison: is automation reducing toil per engineer?
- Per-service toil ranking: which services drain the most time?
- Per-incident toil: postmortems include a "manual fix steps" count

If toil is going up, your SRE program is failing. Stop adding services until automation catches up.
