---
tags:
  - testing:api
level: intermediate
category: testing
audience:
  - audiences:qa
  - audiences:developers

---

# Introduction to API Testing

---

## What This Chapter Covers

- What API testing is
- Levels of testing
- Why test APIs
- Tooling landscape
- Roles

---

## What API Testing Is

- Validating APIs at the integration level
- Below UI; above unit
- Tests contracts and behaviour
- Automatable

---

## Why Test APIs

- APIs are public surface for clients
- Many integrations depend on them
- Faster than UI tests
- Catch contract breakage early

---

## Levels of Testing

- Unit: code units
- Integration: with dependencies
- API: through HTTP
- E2E: full system
- API tests sit in the middle

---

## Pyramid

- Many unit tests
- Fewer integration / API tests
- Few E2E tests
- Inversion is a smell

---

## Where API Tests Sit

![api_testing_pyramid](svg/courses/testing/api-testing/01_introduction/api_testing_pyramid.svg)

---

## What to Test

- Happy paths: 200 responses, correct shape
- Error paths: 4xx and 5xx
- Edge cases: empty, large, malformed
- Auth, permissions
- Rate limits, idempotency

---

## Functional vs Non-Functional

- Functional: does it do the right thing
- Non-functional: performance, security, reliability
- Both need coverage

---

## Manual vs Automated

- Manual: exploration, ad-hoc
- Automated: regression, CI
- Both have a place; favor automated

---

## Tools

- Postman, Insomnia: manual + scripted
- REST-assured, supertest: code-first
- Karate, Schemathesis: spec-driven
- k6, JMeter, Locust: load

---

## Roles

- QA: defines and runs tests
- Devs: write tests alongside code
- Both: review failures
- Shared ownership

---

## Where Tests Live

- Same repo as code (preferred)
- Separate repo for E2E across services
- CI runs on every change

---

## Course Plan

- Tools, contract testing
- Test design
- Auth, performance, security
- CI integration

---

## Common Introduction Mistakes

- Treating API tests as a UI substitute
- All testing through E2E; slow
- No ownership; tests rot
- Manual-only; no regression net
- Testing implementation, not behaviour
