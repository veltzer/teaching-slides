---
tags:
  - practices:sre
  - practices:incident-management
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:sres
---
# Incident Management and Postmortems

---

## What an incident is

- An unplanned event that degrades or threatens service
- Not every page is an incident; not every incident pages
- Severity levels (varies by org):
  - **SEV1** — major outage, customer impact, exec attention
  - **SEV2** — significant degradation, contained scope
  - **SEV3** — partial outage, workaround available
  - **SEV4** — internal-only, low impact

Declare loudly and early. It is far cheaper to downgrade a SEV2 to SEV3 than to upgrade a SEV3 mid-fire.

---

## The incident command structure

Three roles, even on small teams:

- **Incident Commander (IC)** — coordinates, makes calls, doesn't fix
- **Communications Lead** — updates stakeholders, customers, status page
- **Operations Lead** — actually debugs and applies fixes

For small incidents one person can wear two hats. **Never** the same person doing all three — context-switching kills response time.

Inspired by the Incident Command System used by fire departments and FEMA.

---

## ![w:50](svg/courses/architecting/site-reliability-engineering/06_incidents/incident_flow.svg)

---

![](svg/courses/architecting/site-reliability-engineering/06_incidents/incident_flow.svg)

---

## Communication during incidents

- **Internal channel** — single Slack/Teams channel, dedicated to this incident
- **Public status page** — updated every 15-30 minutes during SEV1
- **Stakeholder updates** — written summaries, not raw chat
- **Customer comms** — drafted by the Communications Lead, reviewed by IC

Bad: silent on-call engineer alone in a chat with five managers.
Good: IC posts hourly summaries; engineers debug in a separate thread.

---

## Tools that help

- **PagerDuty / Opsgenie / Splunk On-Call** — paging and rotation
- **Slack/Teams** — incident channel, automation bots
- **Status page** — Statuspage.io, Better Uptime, custom
- **War room video bridge** — Zoom/Meet ready in seconds
- **Document templates** — incident timeline, comms updates

The single most useful incident tool is a Slack bot that creates the channel + Zoom + status page entry on `/incident`.

---

## The blameless postmortem

> "We assume that every employee meant to do the right thing." — Etsy postmortem template

- The goal is to learn, not to assign fault
- Humans make errors because of the system around them
- Punishing humans for system-level failures creates fear and hiding
- Fear creates worse incidents next time

Blameless does not mean accountabilityless. It means: focus on the system that allowed the error, not the human who made it.

---

## Postmortem structure

Every postmortem documents:

```
1. Summary — one-paragraph user-facing description
2. Impact — duration, customers affected, revenue
3. Timeline — UTC timestamps of every event
4. Detection — how did we find out?
5. Response — what did we do?
6. Root cause — why did this happen, technically
7. What went well
8. What went wrong
9. Action items — owned, dated, tracked
10. Lessons learned
```

The action items are the only part with teeth. Track them like normal work.

---

## Root cause analysis

- "5 Whys" — keep asking why until you hit a system-level cause
- "Cause map" — multiple contributing factors, not one root cause
- The honest answer is usually "many things had to align"
- Resist the urge to stop at human error — that is a symptom, not a cause

```
Outage → DB overloaded
  Why? → Bad query in shipping
    Why? → No load test for this query
      Why? → Load testing isn't part of the workflow
        Why? → No tooling makes it easy
          Why? → No one prioritised building it
```

The fix is at the bottom, not the top.

---

## Action items that matter

Bad action item: "Be more careful when deploying"
Good action item: "Add automated check that blocks deploy if X is true"

- Specific
- Owned by a named person
- Has a deadline
- Reduces likelihood OR reduces impact of recurrence
- Tracked in the same system as feature work

If your postmortem produces 30 action items, half won't get done. Prioritise 3-5 high-leverage ones.

---

## Reading postmortems publicly

- Postmortems are valuable beyond the team that wrote them
- Internal database of postmortems = institutional memory
- Reading recent postmortems is part of on-call onboarding
- Public postmortems (Cloudflare, GitHub, AWS) educate the entire industry

The cost of an incident is paid; capture the value.

---

## Common incident anti-patterns

- **Silent on-call** — engineer fixes alone, no IC, no comms
- **Heroes** — one person does everything; doesn't scale, leads to burnout
- **Postmortem theatre** — written but never read; action items never done
- **Blame** — incident felt like a punishment; people hide problems next time
- **No declaration** — outage debated for hours before anyone calls it
- **Tool soup** — incident in 5 channels, 3 docs, no single source of truth

Drill these as a team — chaos engineering, game days, on-call simulations.

---

## Maturing the practice

| Stage | Look like |
|---|---|
| Reactive | "What just broke?" |
| Aware | Pages exist, but no IC structure |
| Defined | IC role assigned; postmortems written |
| Measured | Incident metrics tracked over time |
| Optimised | Postmortems drive systemic improvement |

Move up by adding one practice at a time. Skip steps and the team rejects them.
