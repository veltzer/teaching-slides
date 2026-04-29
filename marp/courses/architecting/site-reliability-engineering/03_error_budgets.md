---
tags:
  - practices:sre
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:sres
---
# Error Budgets

---

## The error budget concept

If your SLO says 99.9% over 28 days, you are explicitly allowing 0.1% failure.

```
Error budget = (1 − SLO) × time
99.9% over 28 days = 43.2 minutes of downtime allowed
```

This is the **error budget**. It is not a target to hit; it is a budget to spend on whatever you want — risky deploys, experiments, refactors, planned maintenance.

---

## Why error budgets matter

- They turn reliability from a vague concern into a quantitative resource
- They give engineers permission to take risks (the budget covers it)
- They give SREs leverage to slow shipping when the budget is exhausted
- They align dev and ops on the same metric — reliability is no longer an "ops problem"

Before error budgets, dev pushes for velocity, ops pushes for stability, neither side trusts the other. With them, both sides argue about the same number.

---

## ![w:50](svg/courses/architecting/site-reliability-engineering/03_error_budgets/burn.svg)

---

![](svg/courses/architecting/site-reliability-engineering/03_error_budgets/burn.svg)

---

## Spending the budget

Things that consume your budget:

- Real outages
- Bad deploys
- Slow degradation (P95 latency creeping up)
- Dependency failures
- Bugs in error-handling that surface to users
- Overly aggressive load-shedding

Things that **save** budget:

- Canary deploys catching issues
- Better testing (fewer regressions)
- Circuit breakers (degrade gracefully, count fewer errors)
- Faster rollbacks (less downtime per incident)

---

## The error budget policy

Document what happens when the budget is exhausted:

```
If error budget is consumed:
  - All new feature deploys to production are paused
  - Only reliability work and rollbacks ship
  - The on-call team gets dedicated time on the top reliability bug
  - We resume feature deploys when budget recovers
```

The policy must be agreed by dev and SRE leadership in advance. Negotiating during a budget crunch is too late.

---

## Burn rates

Burn rate = how fast you are spending the budget right now

| Burn | Meaning | Action |
|---|---|---|
| 1× | spending at the SLO target rate | sustainable |
| 2× | will burn 28-day budget in 14 days | investigate |
| 10× | will burn 28-day budget in 2.8 days | page on-call |
| 100× | will burn 28-day budget in 7 hours | wake people up |

Multi-window, multi-burn-rate alerts (Google's MWMBR pattern) catch both fast outages and slow degradation.

---

## A worked example

```
SLO: 99.9% availability over 28 days
Total requests in 28 days: 100,000,000
Allowed bad requests: 0.1% × 100M = 100,000
Budget: 100,000 errors

Day 5: 12,000 errors served (12% of budget)
Day 10: 35,000 errors (35%)
Day 15: 88,000 errors (88%) — within 5 days will exhaust
Day 16: 105,000 errors — budget gone, freeze deploys
```

The team now spends a sprint on reliability. The budget refills as the rolling window moves.

---

## Common error budget anti-patterns

- **Vanity SLOs** — 99.99% on a service that does not need it; budget always tight
- **Pet SLOs** — every team picks the same number without thought
- **Heroic recovery** — manually fixing every blip to "save the budget"
- **No policy** — exhausted budget triggers nothing; budget is decoration
- **Budget hoarding** — never spending; team has lost the courage to ship

The budget is meant to be spent. A team with no incidents is over-engineering.

---

## Error budgets and incidents

- A 30-min outage on a 99.9%/28d service eats 70% of the budget
- After exhaustion, the freeze gives ops time to fix root causes
- Postmortems quantify "how much budget did this incident cost?"
- Over time, you can see which incident classes hurt most and prioritise mitigations

The budget makes incident impact comparable. "Bad outage" becomes "consumed 0.6 budgets" — measurable across teams and quarters.

---

## Budget policies in practice

- **Google** — formal policy; budget exhaustion freezes feature deploys
- **Spotify** — burn-rate alerts; manager signs off on freezes
- **Netflix** — chaos engineering deliberately spends budget to prove resilience
- **Smaller teams** — informal; the policy is "we slow down a little"

The exact mechanism matters less than having one. No policy = no error budget, just a number.
