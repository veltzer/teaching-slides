---
tags:
  - practices:sre
  - practices:on-call
level: intermediate
category: architecture
audience:
  - audiences:sres
  - audiences:managers
---
# On-Call and SRE Organisation

---

## Sustainable on-call

The on-call rotation is the single biggest cause of SRE burnout. Get this right or lose your team.

- **Min 6 people per rotation** — fewer means too-frequent shifts
- **One week on, five weeks off** — typical pattern at Google
- **Follow-the-sun** — distribute across time zones to avoid 3am pages
- **Pages cap** — ≤2 pages per shift; if more, page volume is the bug

If on-call is a punishment, the team will not survive long-term.

---

## On-call compensation

- Pay for the hours, not just the pages
- Time off in lieu after a busy shift
- Recognise the load in performance reviews
- Provide tools (good laptop, mobile data, secondary monitor) for the role

> "We expect you to be available 24/7 for free during your on-call week" → engineers leave

The math: a ruined sleep night costs more than fair on-call pay.

---

## ![w:50](svg/courses/architecting/site-reliability-engineering/08_oncall_org/team_models.svg)

---

![](svg/courses/architecting/site-reliability-engineering/08_oncall_org/team_models.svg)

---

## Runbooks and playbooks

Every alert needs a runbook:

```
Alert: High error rate on Checkout API
Severity: SEV2

What this means: 5xx errors >2% of requests for 5 minutes
User impact: checkout failing intermittently

Investigation:
1. Check the deploy timeline — recent changes?
2. Check downstream dependencies (payment, inventory)
3. Look at error_log_query

Mitigations:
- Rollback if recent deploy
- Toggle feature flag X to fall back to legacy
- Scale checkout-api to 2× replicas
```

Runbooks are the difference between a 10-minute incident and a 2-hour incident.

---

## Escalation policy

Define explicitly:

```
1. Primary on-call (1st page)
2. If no ack in 5 min → secondary
3. If no ack in 5 min → manager
4. If no resolution in 30 min → leadership escalation
5. SEV1 → wake up the VP regardless of time
```

Don't make this up during an incident. The escalation path lives in PagerDuty config and the team wiki.

---

## Training new on-call engineers

- **Shadow** — observe the senior on-call for 2-4 weeks
- **Reverse shadow** — handle pages with senior watching
- **Game days** — practice with simulated incidents
- **Postmortem reading** — last 6 months of incidents
- **Solo with safety net** — on-call but with senior backup

Throwing a new engineer into solo on-call after one week is a known anti-pattern. Build the ramp.

---

## SRE team models

| Model | Description | When |
|---|---|---|
| **Embedded** | SRE inside product team | Small org, single product |
| **Centralised** | SRE team supports many services | Many services, shared expertise |
| **Consulting** | SRE advises, dev teams own ops | Dev-led culture |
| **Platform** | SRE builds tools dev teams use | Many teams, similar problems |

Most large orgs use a mix. Google itself uses a centralised model with embedded engagements.

---

## When to hire your first SRE

Signals that the time has come:

- Service has paying customers and an SLA
- The on-call burden on dev team is hurting feature velocity
- Incidents are repetitive — pattern recognition would help
- The org has 50+ engineers but no dedicated reliability function
- You can name 3 reliability projects waiting in the backlog

Hiring an SRE is hiring a software engineer. They write code, build tools, and have opinions. Treat them like one.

---

## SRE career development

- SRE is software engineering with operational specialty
- Career progression mirrors SWE (engineer → senior → staff → principal)
- Skills: distributed systems, performance, debugging, automation
- Side roads: platform engineering, security, observability tools
- Beware: "SRE manager" who hasn't engineered in 5 years tends to drift

Treat SRE as a parallel track to product engineering, not a step down.

---

## Common org anti-patterns

- **SRE as ops team** — no engineering work, just toil; team burns out
- **No SLOs** — reliability is vibes-based; no leverage for SRE to push back
- **No error budget policy** — exhaustion triggers nothing; SLOs are decoration
- **SRE owns code without authority** — fix the breakage, can't change the design
- **One SRE per ten services** — spread too thin; nothing improves
- **Hero culture** — one engineer carries on-call; quits, takes knowledge

Each of these is a organisational failure mode that no amount of personal heroism will fix.

---

## Building executive support

- Tie SLOs to **business outcomes** (uptime → revenue, NPS, churn)
- Show **incident cost** in dollars (engineer hours + revenue lost)
- Demonstrate **error budget velocity** wins (more reliable + faster shipping)
- Bring **postmortem learnings** to leadership; show systemic fixes
- Quantify **toil reduction** (engineer-hours saved per quarter)

If executives think SRE is "ops", they will resource it like ops. Reframe in their language.

---

## Final survival rules for SRE teams

1. Defend the 50% engineering time — every quarter
1. 1. Define SLOs, document them, review them
1. 1. Write the error budget policy — get it signed by leadership
1. 1. Make on-call sustainable; pay for it
1. 1. Blameless postmortems; track action items to completion
1. 1. Automate the worst toil item every quarter
1. 1. Hire engineers, not "operators"
1. 1. Read the SRE Book and Workbook (free online from Google)

The discipline matters more than any single practice.
