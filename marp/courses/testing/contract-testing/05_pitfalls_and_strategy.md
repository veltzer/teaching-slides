---
tags:
  - testing:contract
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---

# Pitfalls and Strategy

---

## What This Chapter Covers

- Common pitfalls
- When not to use
- Mixing with other tests
- Async messaging
- Adoption strategy

---

## Brittle Contracts

- Match exact values that change
- Fail on every release
- Use loose matching
- Test only what you depend on

---

## Over-Specification

- Listing every field
- Coupling to provider details
- Tests every change anyway
- Specify only what you read

---

## Under-Specification

- Skipping fields you depend on
- Provider can rename and break you
- Find the balance
- Cover error responses too

---

## When Not To Use

- Single-team monolith
- One service for the whole product
- No independent deploys
- Tests do not pay back the effort

---

## End-To-End Still Matters

- Smoke tests for critical journeys
- Per environment
- Cover wiring contract tests cannot
- Run sparingly

---

## Mixing With Schema Validation

- Schemas catch shape drift
- Contracts catch behavior drift
- Combine for full coverage
- Tools support both

---

## Async Messaging

- Topics and queues
- Producer-consumer contracts
- Schema registry helps
- Message tools have contract support

---

## Event Schemas

- Backward compatibility rules
- Tag events with version
- Migrate consumers before producer breaks
- Same disciplines as HTTP

---

## Documentation Bonus

- Contracts double as examples
- Easier onboarding
- Living documentation
- Free side benefit

---

## Adoption Strategy

- Pilot one boundary
- Measure incident reduction
- Expand to neighboring services
- Standardize tooling

---

## Adoption Path

![adoption_path](svg/courses/testing/contract-testing/05_pitfalls_and_strategy/adoption_path.svg)

---

## Team Buy-In

- Provider teams must verify
- Consumer teams must specify
- Both need training
- Leadership backs the discipline

---

## Maintenance

- Stale contracts removed
- Branch hygiene
- Broker housekeeping
- Document the process

---

## Metrics That Matter

- Verification pass rate
- Time to fix verification failures
- Production incidents from interface drift
- Deploys gated by can-i-deploy

---

## Common Strategy Mistakes

- Tooling without discipline
- Discipline without tooling
- One side adopts, other does not
- No rollout plan
- No sunset for old contracts
