---
tags:
  - testing:api
  - practices:ci-cd
level: intermediate
category: testing
audience:
  - audiences:qa
  - audiences:developers

---

# CI and Practices

---

## API Test CI Pipeline

![ci_pipeline](svg/courses/testing/api-testing/07_ci_and_practices/ci_pipeline.svg)

---

## What This Chapter Covers

- CI integration
- Test environments
- Flakiness
- Reporting
- Ownership
- Wrap-up

---

## CI Integration

- Tests run on every PR
- Block merge on failures
- Fast tests in PR; long tests nightly

---

## Test Tiers

- Unit: every commit, seconds
- API integration: every PR, minutes
- E2E: nightly, longer
- Performance: scheduled

---

## Test Environments

- Ephemeral per PR (preview env)
- Shared staging for nightly
- Production: smoke tests post-deploy

---

## Test Environment Tiers

![test_environments](svg/courses/testing/api-testing/07_ci_and_practices/test_environments.svg)

---

## Ephemeral Environments

- Spin up on PR open
- Run tests
- Tear down on close
- Preview-deploy services

---

## Flakiness

- Tests fail intermittently
- Erodes trust
- Quarantine and fix
- Don't ignore

---

## Causes of Flakiness

- Shared state
- Timing (sleeps, races)
- External dependencies
- Random data with bugs

---

## Reducing Flakiness

- Test isolation
- Wait on conditions, not sleeps
- Mock external services
- Stable test data

---

## Reporting

- JUnit XML standard
- HTML reports
- Trend charts: pass rate over time
- Failure categorisation

---

## Test Owners

- Each test has a team owner
- Failures route to owner
- Stale tests removed

---

## Code Review for Tests

- Tests reviewed like code
- Same standards: clarity, isolation, speed
- Catch flakiness before merge

---

## Documentation

- README per test suite
- How to run locally
- How to debug failures
- Critical for adoption

---

## Test Data Management

- Versioned fixtures
- Per-environment seeders
- Reset between runs
- Avoid hardcoded data

---

## Smoke Tests in Production

- Tiny set of critical paths
- Run post-deploy
- Page if fail
- Fast feedback on bad releases

---

## Wrap-Up

- API testing: integration sweet spot
- Pyramid: many small, few big
- Tools across the spectrum
- Auth, perf, security: each its own discipline
- Contract tests for cross-team APIs
- CI integration: non-negotiable

---

## Common CI Mistakes

- Tests in CI but not blocking
- Long suites in PR; slow merges
- Flaky tests retried until green
- No ownership; failures pile up
- No nightly E2E; gaps appear
