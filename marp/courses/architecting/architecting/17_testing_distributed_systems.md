---
tags:
  - concepts:architecture
  - concepts:testing
  - concepts:distributed-systems
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Testing Distributed Systems

---

## Why Distributed Testing Is Different

- Unit tests catch logic bugs; they don't catch integration bugs
- Integration bugs dominate production incidents in microservice systems
- Every network hop is a new failure mode to test
- Traditional end-to-end pyramids break down when you have dozens of services

---

## The Testing Pyramid (Revised)

- **Unit** — fast, many, inside a single process
- **Component** — one service with its real dependencies mocked out
- **Contract** — each service against the promises made by and to its neighbors
- **Integration** — a small subset of services running together
- **End-to-end** — the whole system; slowest, flakiest, fewest

In microservices, the pyramid flattens at the top and bulges at contract.

---

## Unit Tests

- Fast, deterministic, no I/O
- Test pure business logic and data structures
- Mocks and stubs for collaborators
- Thousands of tests in under a minute
- Run on every commit, on every branch

---

## Component Tests

- A single service spun up in isolation
- Real database (often Testcontainers); fake external services
- Exercises HTTP handlers, database schemas, message consumers
- Slow enough to run minutes, not seconds; run on every PR

---

## The End-to-End Problem

- E2E tests become flakier linearly with the number of services
- A test that fails 1% per service touches 20 services → 18% flake rate
- Flaky tests erode trust, then get ignored, then hide real bugs
- Keep E2E tests few, critical-path, and well-isolated

---

## Contract Testing

- Each consumer states the shape of requests and responses it expects
- Each provider runs all consumer contracts as part of its own CI
- Failures surface at the provider's build, not in staging after merge
- Scales linearly with the number of dependencies, not quadratically

---

## Pact Flow

- Consumer test generates a contract file
- Contract is uploaded to a **Pact Broker**
- Provider CI fetches the broker's contracts
- Provider runs every contract against a real instance
- Any breaking change fails the provider's build

---

## Consumer-Driven vs Provider-Driven

- **Consumer-driven** — consumers write contracts; providers comply
- **Provider-driven (schema-first)** — provider publishes an OpenAPI/AsyncAPI spec; consumers validate against it
- Consumer-driven catches more bugs; provider-driven is easier to adopt organization-wide
- Can and often should coexist

---

## Integration Testing Done Right

- Pick the smallest meaningful subset of services
- Use real databases and real message brokers; fake external paid services
- Spin up with `docker-compose` or `Testcontainers`
- Tear down completely between runs — no shared state across tests

---

## Synthetic Monitoring

- Continuously run a small set of E2E scenarios against production
- Treats your own system as a black box
- Detects real-world failures before users notice
- Tools: `Datadog Synthetic`, `Grafana k6 Cloud`, custom probes
- Keep it cheap and fast — it's a monitor, not a regression suite

---

## Load and Performance Testing

- Load tests confirm the system handles expected traffic
- Stress tests push beyond expected load to find breaking points
- Soak tests run at moderate load for hours to catch leaks
- Spike tests simulate sudden traffic bursts
- Tools: `k6`, `Gatling`, `Locust`, `wrk`, `JMeter`

---

## Shadow Traffic

- Mirror real production requests to a candidate system in parallel
- Production path serves the user; candidate is compared silently
- Perfect for validating rewrites and optimizations
- Uncovers load patterns you cannot synthesize

---

## Dark Launches

- Deploy the new code behind a feature flag disabled for all users
- Exercise it internally or for a small cohort
- Observe under real production conditions
- Enable broadly only after it has been silently correct for days

---

## Testing in Production (Responsibly)

- Modern services are too complex to fully replicate in staging
- Canary analysis, synthetic probes, and feature flags let you test safely in prod
- Requires: observability, feature flags, instant rollback, blast-radius limits
- Not a license to skip pre-prod tests — a complement, not a replacement

---

## Chaos Testing

- Deliberately inject failures in test or staging clusters
- Validates that resiliency patterns (retries, circuit breakers) actually work
- Types:
    - **Latency injection** — make calls slower
    - **Error injection** — return 500s from dependencies
    - **Resource exhaustion** — fill disk, pin CPU
    - **Pod/node kills** — Chaos Mesh, LitmusChaos
- Start small, scheduled, with a kill switch

---

## Game Days

- A scheduled exercise: a team simulates a failure, others respond
- Reveals gaps in runbooks, monitoring, and on-call procedures
- Humans are part of the system — they need to be tested too
- Output: action items to close identified gaps

---

## Flaky Test Discipline

- Flaky tests are worse than no tests — they train teams to ignore failures
- Quarantine flaky tests the day they are detected
- Fix or delete within an owner-SLA (1 week typical)
- Track flake rate as a first-class quality metric

---

## Test Data Management

- **Anonymized production snapshots** — realistic, privacy-safe
- **Seed data in migrations** — predictable, versioned
- **Factories / builders** — small, composable test data in code
- **Resettable stores** — every test starts from a known state
- Avoid: hand-crafted dev databases passed around on USB sticks

---

## Observability for Tests

- Every test environment emits the same metrics, logs, and traces as production
- Failed tests should be triageable from the same tools you use on-call
- Test IDs propagate into traces so you can find the span that failed
- Log aggregation for test runs — not just prod

---

## Test Environment Strategy

- **Ephemeral per-PR environment** — best fidelity, requires infrastructure investment
- **Shared long-lived staging** — cheap but collisions and drift
- **Namespace-per-developer** — good middle ground in Kubernetes clusters
- **Production-like data volumes** — matters more than most teams admit

---

## Progressive Rollout as Test

- Every canary is a test against real traffic
- Automate analysis: compare canary vs baseline metrics
- Roll back on any significant regression
- Shifts testing burden from pre-prod to early post-prod — cheaper and more realistic

---

## Architectural Fitness Functions

- Automated tests that validate architectural properties
- Examples:
    - "No service imports another service's private packages"
    - "p99 latency never exceeds 200ms"
    - "No new service adds more than two inbound dependencies"
- Run in CI; fail the build on violation

---

## Common Anti-Patterns

- **Mocking what you should integration-test** — happy mock tests, unhappy prod
- **Integration-testing what you should unit-test** — slow, flaky, expensive
- **No contract tests** — every breaking change becomes a staging incident
- **Staging treated as an afterthought** — drift from prod erodes confidence
- **Chaos tests without observability** — you break things but can't tell what broke

---

## Summary

- The testing pyramid for microservices flattens at the top; contract tests fill the middle
- Contract testing (Pact) scales where end-to-end cannot
- Synthetic monitoring extends testing into production safely
- Shadow traffic and dark launches validate rewrites with real load
- Chaos testing proves resiliency patterns actually work
- Flaky tests are a quality metric, not an acceptable reality
- Observability turns every test environment into a diagnosable system
