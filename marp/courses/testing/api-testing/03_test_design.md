---
tags:
  - testing:api
  - practices:design
level: intermediate
category: testing
audience:
  - audiences:qa

---
# Test Design

---
## What This Chapter Covers

- Test cases
- Arrange-Act-Assert
- Data setup
- Independence
- Edge cases
- Negative tests

---
## A Good Test

- Clear name
- Tests one thing
- Independent
- Fast
- Deterministic

---
## Arrange-Act-Assert

- Arrange: setup data and state
- Act: call the API
- Assert: verify response and side effects

---
## Sample Test (Pseudo)

- Arrange: create user
- Act: GET /users/{id}
- Assert: 200 + correct body

---
## What to Assert

- Status code
- Response body shape and values
- Headers (Content-Type, custom)
- Side effects (DB row created, event published)

---
## Schema Assertions

- Validate against JSON Schema or OpenAPI
- Catches structural changes
- Stronger than ad-hoc assertions

---
## Test Data

- Fixed: known test users
- Dynamic: created per test
- Reset between runs (transactions, cleanup)

---
## Independence

- Tests don't depend on each other
- Run in any order
- Parallelisable

---
## Setup and Teardown

- Per-test or per-suite
- Database seed / cleanup
- Idempotent

---
## Negative Tests

- 400 on bad input
- 401 without auth
- 403 with wrong role
- 404 on missing resource
- 409 on duplicate

---
## Edge Cases

- Empty arrays / objects
- Maximum sizes
- Special characters in strings
- Unicode
- Timezone boundaries

---
## Boundary Values

- Just below, at, and just above limits
- e.g., page size 0, 1, max-1, max, max+1

---
## Idempotency Tests

- Repeat same call: same result
- For idempotent endpoints (GET, PUT, DELETE)
- POST with idempotency key

---
## Concurrency

- Two clients hit same endpoint
- Verify locking, race-condition behaviour
- Hard but valuable

---
## Common Test Design Mistakes

- Testing implementation (DB rows) instead of behaviour
- Tests dependent on each other
- Hardcoded ids; brittle
- No negative tests; only happy path
- Asserting on too much (snapshot comparison) or too little
