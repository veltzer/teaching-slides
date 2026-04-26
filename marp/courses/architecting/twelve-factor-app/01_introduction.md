---
tags:
  - concepts:architecture
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Introduction to the Twelve-Factor Methodology

---
## Origins

- Published in 2011 by engineers at Heroku
- Adam Wiggins and the Heroku platform team
- Distilled from running thousands of customer apps
- Originally targeted at SaaS apps deployed to PaaS platforms
- Now a baseline for cloud-native software in general

---
## The Problem It Solves

- Apps depended on details of the machine where they ran
- "Works on my laptop" was a permanent state
- Configuration was hand-edited in production
- Deploys were ceremonies, not automation
- Scaling out required redesign

---
## The Twelve Factors at a Glance

1. Codebase — one codebase, many deploys
1. Dependencies — declare and isolate
1. Config — store in environment
1. Backing services — treat as attached resources
1. Build, release, run — strictly separate
1. Processes — execute as stateless processes
1. Port binding — export services via port binding
1. Concurrency — scale via the process model
1. Disposability — fast startup, graceful shutdown
1. Dev/prod parity — keep environments similar
1. Logs — treat as event streams
1. Admin processes — run as one-off tasks

---
## Twelve-Factor and Cloud-Native

- "Cloud-native" was coined later but builds on the twelve factors
- Containers, Kubernetes, microservices all assume twelve-factor practices
- An app that violates the factors is harder to run anywhere automated
- The factors are the contract between developer and platform

---
## Twelve-Factor and Microservices

- Each microservice should follow the twelve factors independently
- Multiple twelve-factor services compose into a system
- The factors make a service portable across environments
- They don't tell you how to split a system into services — that's a separate concern

---
## What This Course Covers

- One chapter per factor, with rationale, examples, and anti-patterns
- A chapter on what's missing from the original twelve (telemetry, security)
- A chapter mapping each factor to Docker and Kubernetes practices
- The goal: be able to recognize and fix violations in real codebases

---
## How to Read the Factors

- Each factor is a constraint that pays back later
- Some are obvious; some are counterintuitive
- They reinforce each other — violating one tends to lead to violating others
- A "twelve-factor app" is shorthand for a system that takes them all seriously

---
## A Common Misconception

- Twelve-factor is **not** about a specific technology
- You can have a twelve-factor app in any language, on any platform
- You can violate every factor while using "cloud-native" tools
- The discipline is in the design, not the toolset

---
## Summary

- Twelve factors emerged from running real apps at scale
- They make apps portable, automatable, and operable
- Cloud-native and microservices both assume them
- Violating them works — until the team needs to scale or migrate
- Each factor is a small commitment with a large payoff
