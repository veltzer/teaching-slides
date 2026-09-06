---
tags:
  - concepts:microservices
  - practices:testing
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Testing Microservices

---

## Why Testing Is Different

- A monolith: one process to test
- Microservices: many processes, network in between
- Test pyramid still applies but the layers are different
- End-to-end across all services is expensive and brittle

---

## The Test Pyramid for Microservices

- Many: unit tests within each service
- Some: integration tests against the service's dependencies (mocked or real)
- Few: contract tests between services
- Fewer: end-to-end tests across the system

---

## Testing Layers

![microservice_testing](svg/courses/architecting/microservices-architecture/11_testing/microservice_testing.svg)

---

## Unit Tests

- Same as for any code
- Fast; no network, no database
- High count; the foundation of the pyramid
- Run on every commit

---

## Integration Tests

- Test the service in isolation, but with its real dependencies (or close)
- Real database (in a container), real cache
- Mocked external services (other microservices)
- Slower than unit tests; check that the service works correctly with its store

---

## Component Tests

- Test a service from outside its API
- Real implementation inside; mocked or stubbed external services
- Fast enough to run in CI; thorough enough to catch most bugs
- Often the sweet spot for microservices testing

---

## Contract Tests

- Verify that consumer and producer agree on the API
- Consumer-driven: the consumer specifies what it expects
- Producer's CI verifies it satisfies all consumer contracts
- Tools: Pact, Spring Cloud Contract

---

## Why Contract Tests Matter

- A producer changes the API; consumers fail in production
- With contract tests, the producer's CI catches it before deploy
- The consumer doesn't need to be deployed for the test
- Solves the "producer broke us" class of bugs

---

## End-to-End Tests

- Test a user-visible flow across multiple services
- Slow, expensive, brittle
- Use sparingly: a few critical flows, run on a schedule
- Not a replacement for unit, integration, or contract tests

---

## Testing in Production

- Some bugs only show up under real load and real data
- Canary deploys; feature flags; A/B tests
- Synthetic monitoring: scheduled requests that test critical flows
- Chaos engineering: deliberate failures to verify resilience

---

## Test Data Strategies

- Each test starts from a known state
- Database snapshots, fixtures, factories
- Don't share test data across tests — flaky tests result
- Per-service test data is easier than shared

---

## Mocking External Services

- For integration tests, mock the other services
- Tools: WireMock, MockServer, in-process stubs
- The mock must match the producer's contract (use contract tests to verify)
- Mocks are convenient but introduce drift risk

---

## Local Development

- Run a service locally; mock its dependencies
- Or: run the full stack with docker-compose
- The trade-off: speed vs. realism
- Most teams use both at different times

---

## Anti-Patterns

- Only end-to-end tests, no contract tests (slow, brittle, expensive)
- Mocks that drift from the real producer's contract
- Tests that depend on a specific test database state
- Long test runs that discourage frequent commits
- "Test in staging" without test discipline

---

## Summary

- Unit and integration tests at each service
- Contract tests across service boundaries
- End-to-end tests sparingly
- Test in production via canaries, feature flags, synthetic monitoring
- Contracts are the cheap insurance against producer-consumer breakage
