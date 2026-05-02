---
tags:
  - testing:performance
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Designing Tests

---
## What This Chapter Covers

- Workload modeling
- Scenarios
- Pacing
- Think time
- Data variety

---
## Workload Modeling

- Match real user behavior
- Mix of endpoints
- Realistic ratios
- Realistic burst patterns

---
## Workload Visualized

![workload_model](svg/courses/testing/performance-testing/03_designing_tests/workload_model.svg)

---
## Sources Of Truth

- Production logs
- Analytics tools
- Customer support insight
- Sampling tools

---
## Scenarios

- Sign-up
- Browse
- Search
- Checkout
- Settings

---
## Mix

- Common scenarios at production rates
- Rare scenarios sampled
- Cover happy and sad paths
- Document the mix

---
## Pacing

- Time between requests per user
- Models human delays
- Drives concurrency vs throughput
- Tune to match real users

---
## Open Vs Closed Models

- Open: arrival rate independent of response
- Closed: fixed users repeat
- Open mirrors web traffic
- Closed mirrors fixed-thread workers

---
## Think Time

- Pause between user actions
- Reflects reading, deciding
- Without it, results are unrealistic
- Vary across users

---
## Data Variety

- Many user IDs
- Many item IDs
- Many search terms
- Avoid cache-only paths

---
## Cache Warming

- Realistic warm-up before measurement
- Or skip caches and test cold path
- Document the choice
- Compare warm and cold runs

---
## Authentication

- Realistic logins per session
- Reuse tokens
- Roll fresh users to avoid coupling
- Watch for auth-server bottleneck

---
## Rate Ramps

- Step up gradually
- Find first breakage point
- Plateau at target
- Cool-down phase

---
## Repeatability

- Same script, same data
- Same environment
- Same time of day
- Compare runs apples to apples

---
## Test Length

- Long enough to flush warm-up
- Long enough to catch GC pauses
- Long enough for autoscaling
- Pretty long, in practice

---
## Common Design Mistakes

- One endpoint at a time
- No think time
- One user ID
- Closed model for web traffic
- Too short test runs
