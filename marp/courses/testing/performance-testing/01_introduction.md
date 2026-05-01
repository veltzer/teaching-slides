---
tags:
  - testing:performance
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Introduction to Performance Testing

---
## What This Chapter Covers

- What performance testing is
- Types of tests
- When to run
- Key metrics
- Course outline

---
## What It Is

- Measuring system behavior under load
- Latency, throughput, errors
- Compared to targets
- Repeatable

---
## Why It Matters

- Slow systems lose users
- Outages happen first under load
- Capacity planning needs data
- SLAs need evidence

---
## Test Types

- Load test
- Stress test
- Spike test
- Soak test
- Capacity test

---
## Test Types Visualized

![perf_test_types](svg/courses/testing/performance-testing/01_introduction/perf_test_types.svg)

---
## Load Test

- Expected production traffic
- Verify SLA holds
- Run regularly
- Baseline for comparisons

---
## Stress Test

- Push beyond expected
- Find the breaking point
- Observe failure modes
- Inform autoscaling

---
## Spike Test

- Sudden traffic burst
- Verify autoscaling reacts
- Verify queues absorb
- Verify nothing collapses

---
## Soak Test

- Sustained moderate load for hours
- Find leaks and drift
- Find resource exhaustion
- Often run nightly

---
## Capacity Test

- Increase load until SLA breaks
- Find max sustainable rate
- Drives capacity planning
- Run on each major release

---
## Key Metrics

- Throughput
- Latency p50, p95, p99
- Error rate
- Resource use

---
## Latency Distributions

- Mean is misleading
- Tail dominates user experience
- Track p99 and p99.9
- Plot the histogram

---
## SLOs And SLAs

- SLO: internal target
- SLA: external commitment
- Performance tests verify both
- Document and align

---
## When To Run

- Before launch
- Before peak season
- After architecture changes
- On a schedule

---
## Course Outline

- Tools
- Designing tests
- Running tests
- Analyzing results
- Continuous performance

---
## Common Beginner Mistakes

- One run is enough
- Production-scale only on launch
- Average latency reporting
- No warm-up
- No baseline
