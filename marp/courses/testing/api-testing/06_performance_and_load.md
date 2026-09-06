---
tags:
  - testing:api
  - practices:performance
level: intermediate
category: testing
audience:
  - audiences:qa

---

# Performance and Load Testing

---

## What This Chapter Covers

- Load test types
- Tools
- Scenarios
- Metrics
- Test design
- Production-like environments

---

## Load Test Types

- Smoke: baseline
- Load: expected traffic
- Stress: above expected
- Spike: sudden surge
- Soak: sustained, long duration

---

## Load Test Shapes

![load_shapes](svg/courses/testing/api-testing/06_performance_and_load/load_shapes.svg)

---

## Tools

- k6: modern, JS scripts
- JMeter: mature, GUI
- Locust: Python, distributed
- Gatling: Scala, code-first

---

## k6 Sample (Pseudo)

- Define VUs and duration
- HTTP requests in default function
- Thresholds for SLOs
- Run in CI

---

## Scenarios

- Single endpoint
- User journey: login then browse then buy
- Multi-endpoint at proportions
- Realistic traffic shapes

---

## Metrics To Watch

- Latency: p50, p95, p99
- Throughput: req/sec
- Error rate
- Resource: CPU, memory, DB

---

## Defining Success

- SLOs: e.g., 95% under 200ms at 1000 rps
- Test fails if SLO not met
- Automate gates

---

## Test Environment

- As prod-like as possible
- Same DB, similar size data
- Own infra (don't load test prod)

---

## Production Load Tests

- Carefully, with feature flag and small fraction
- Or: shadow traffic
- Risk: real impact

---

## Data Volume

- Empty DB: misleading fast
- Realistic data sizes change profile
- Seed before tests

---

## Caching Effects

- First run: cold cache
- Steady state after warm-up
- Both interesting; report separately

---

## Distributed Generators

- Single machine: limited rps
- Distribute load generators
- k6 cloud, JMeter slaves

---

## Continuous Performance Testing

- Run on every release
- Compare against baseline
- Catch regressions early

---

## Profiling Bottlenecks

- Slow endpoint identified
- Profile: CPU, DB, network
- Fix and re-test

---

## Common Bottleneck Patterns

![bottleneck_patterns](svg/courses/testing/api-testing/06_performance_and_load/bottleneck_patterns.svg)

---

## Common Performance-Testing Mistakes

- Test environment too small
- Missing realistic data volume
- Looking only at average latency
- Ignoring tail (p99) latency
- Load tests only before release; never in CI
