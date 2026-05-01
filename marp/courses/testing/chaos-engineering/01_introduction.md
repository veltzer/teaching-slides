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
# Introduction to Chaos Engineering

---
## What This Chapter Covers

- What chaos engineering is
- Why it works
- Principles
- Maturity model
- Course outline

---
## What It Is

- Inject controlled failure
- Observe how systems behave
- Find weaknesses before customers do
- Build confidence in resilience

---
## Why Now

- Systems are distributed
- Failures are constant
- Production looks different from staging
- Test there, carefully

---
## Origins

- Born at Netflix
- Chaos Monkey killed instances
- Spread to other teams
- Now a recognized discipline

---
## Principles

- Hypothesize about steady state
- Vary real-world events
- Run experiments in production
- Minimize blast radius

---
## Steady State

- Define what healthy looks like
- Latency, error rate, throughput
- Business metrics matter most
- Measured before, during, after

---
## Hypothesis

- "If we kill a node, latency stays under X"
- "If a region goes down, traffic shifts within Y minutes"
- Falsifiable
- Tied to a metric

---
## Blast Radius

- Limit who is affected
- Pick safe time windows
- Have an abort plan
- Start small

---
## When To Stop

- Hypothesis disproved
- Customer impact detected
- Metrics off track
- Have a kill switch

---
## Maturity Model

- Manual game days
- Scheduled experiments
- Continuous chaos
- Automated chaos in CI

---
## Tools Landscape

- Open source frameworks
- Vendor platforms
- Cloud-provider built-ins
- Custom in-house tools

---
## Where To Run

- Lower environments first
- Then production with safeguards
- Some experiments only run in production
- Plan accordingly

---
## Course Outline

- Designing experiments
- Common failure injections
- Running game days
- Tooling
- Operationalizing

---
## Common Beginner Mistakes

- No hypothesis
- No blast-radius limit
- No abort plan
- Skipping post-experiment review
- One chaos event then never again
