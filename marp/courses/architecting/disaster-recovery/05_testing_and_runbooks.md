---
tags:
  - architecting:patterns
  - practices:reliability
level: intermediate
category: architecting
audience:
  - audiences:architects
  - audiences:devops

---
# Testing and Runbooks

---
## What This Chapter Covers

- DR testing levels
- Game days
- Runbooks
- Communication plan
- Post-incident review

---
## Why Test

- Untested DR is theoretical DR
- Configurations drift
- People forget
- Tools change

---
## Testing Levels

- Walkthrough
- Tabletop exercise
- Failover drill
- Full failover

---
## Drill Levels

![drill_levels](svg/courses/architecting/disaster-recovery/05_testing_and_runbooks/drill_levels.svg)

---
## Walkthrough

- Read the runbook with the team
- No systems touched
- Spot gaps quickly
- Cheap to run often

---
## Tabletop Exercise

- Scenario-driven discussion
- Roles played
- Decisions made out loud
- Find missing inputs

---
## Failover Drill

- Real failover in lower environment
- Or partial in production
- Measure RTO and RPO
- Identify automation gaps

---
## Full Failover

- Production traffic moved
- Validate steady state on secondary
- Fail back as a separate exercise
- Highest fidelity

---
## Game Days

- Inject realistic faults
- Cross-team participation
- Time-bounded
- Document learnings

---
## Runbook Anatomy

- Trigger conditions
- Roles
- Step-by-step actions
- Validation checks
- Rollback steps

---
## Runbook Sections

![runbook_anatomy](svg/courses/architecting/disaster-recovery/05_testing_and_runbooks/runbook_anatomy.svg)

---
## Runbook Quality

- Linkable from alerts
- Current for the live environment
- Idempotent steps
- Versioned with code

---
## Communication Plan

- Internal status updates
- External customer comms
- Regulatory notifications
- Pre-approved templates

---
## Decision Authority

- Who can declare disaster
- Who can authorize failover
- Who can talk to press
- Documented and on-call

---
## Post-Incident Review

- Blameless culture
- Timeline reconstruction
- Action items with owners
- Update runbooks afterward

---
## Common Testing Mistakes

- Annual-only drill
- Lower environment only
- No metrics on RTO
- Runbook ignored on the day
- No follow-through on action items
