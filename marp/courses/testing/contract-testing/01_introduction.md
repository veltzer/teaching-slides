---
tags:
  - testing:contract
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---

# Introduction to Contract Testing

---

## What This Chapter Covers

- What contract testing is
- The integration test problem
- Consumer vs provider
- When it pays off
- Course outline

---

## What It Is

- Verify the boundary between services
- Without spinning up both
- Driven by an explicit contract
- Run in isolation

---

## Why Now

- Microservices multiply boundaries
- End-to-end tests are flaky
- Slow feedback hurts
- Need a faster check

---

## The Integration Test Problem

- Spinning up many services is expensive
- Flakiness compounds
- Slow to debug
- Slow to run in CI

---

## Contract Tests vs E2E

![contract_vs_e2e](svg/courses/testing/contract-testing/01_introduction/contract_vs_e2e.svg)

---

## End-To-End Has Its Place

- Smoke tests for critical journeys
- A few, not many
- Per environment, not per PR
- Combine with contract tests

---

## The Contract

- Promise from provider to consumer
- Includes request shape
- Includes response shape
- Includes status codes and headers

---

## Consumer Tests

- Define expected interactions
- Run against a mock provider
- Generate a contract artifact
- Cheap and fast

---

## Provider Verification

- Replay the contract against the real provider
- Confirms provider still meets it
- Run in provider CI
- Fast feedback to provider team

---

## Pact Style

- Consumer-driven contracts
- Broker stores contracts
- Notify provider of changes
- Industry-standard tools

---

## End-to-End Flow

![contract_flow](svg/courses/testing/contract-testing/01_introduction/contract_flow.svg)

---

## OpenAPI Style

- Spec-driven contracts
- Schema and examples in spec
- Both sides validate against spec
- Less detail than Pact

---

## When It Pays Off

- Many small services
- Independent teams
- Different release cadences
- High cost of integration regressions

---

## When It Does Not

- Monolithic apps
- One team, one release
- Few stable boundaries
- Small system overall

---

## Course Outline

- Contracts and tools
- Writing consumer tests
- Verifying providers
- Brokers and CI
- Pitfalls

---

## Common Misconceptions

- "Contract testing replaces integration tests"
- "Contracts replace API design"
- "OpenAPI is enough"
- "Contracts are just schemas"
- "We do not need them since we have one team"
