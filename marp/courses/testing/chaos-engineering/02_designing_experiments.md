---
tags:
  - testing:chaos
  - practices:reliability
level: advanced
category: testing
audience:
  - audiences:devops
  - audiences:developers

---

# Designing Experiments

---

## What This Chapter Covers

- Picking targets
- Hypothesis
- Variables
- Safety
- Documentation

---

## Picking A Target

- Critical user paths first
- Where you have least confidence
- Where rollback is cheap
- Recently changed systems

---

## Hypothesis Form

- Steady state X
- Inject Y
- Predict Z
- Measure to verify

---

## Experiment Flow

![chaos_flow](svg/courses/testing/chaos-engineering/02_designing_experiments/chaos_flow.svg)

---

## Independent Variables

- What you change
- One at a time
- Easy to attribute results
- Avoid confounding

---

## Dependent Variables

- What you measure
- Customer-facing first
- Then technical proxies
- Multiple per experiment

---

## Pre-Conditions

- System healthy
- Steady state verified
- On-call notified
- Maintenance window if needed

---

## Experiment Anatomy

![experiment_anatomy](svg/courses/testing/chaos-engineering/02_designing_experiments/experiment_anatomy.svg)

---

## Abort Conditions

- Customer impact threshold
- Business metric drop
- Security event
- Manual override

---

## Time Window

- Off-peak first
- Wide enough to see effect
- Short enough to limit damage
- Consistent across runs

---

## Cohorts

- Small percentage of users
- Or single internal team
- Expand if results good
- Document cohort criteria

---

## Communication

- On-call team aware
- Customer support aware
- Stakeholders informed
- Status page if needed

---

## Reporting

- What you tested
- What happened
- Action items
- Owners and deadlines

---

## Action Items

- Bugs filed
- Runbook updates
- Monitoring gaps fixed
- Re-test scheduled

---

## Repetition

- Same experiment over time
- Confirms fixes hold
- Detects regressions
- Cheap to run again

---

## Common Design Mistakes

- Vague hypothesis
- No abort condition
- Multiple changes at once
- No customer-facing metric
- Skipping the report
