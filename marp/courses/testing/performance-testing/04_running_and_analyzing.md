---
tags:
  - testing:performance
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Running and Analyzing

---
## What This Chapter Covers

- Pre-flight checks
- During-run observation
- Analyzing results
- Bottlenecks
- Reporting

---
## Pre-Flight

- Environment ready
- Monitors active
- Generators sized
- Stakeholders informed

---
## Warm-Up

- Run at low rate first
- Caches fill
- Just-in-time compilers warm
- Discard early data

---
## Steady State

- Hold target rate
- Watch for stability
- Check for drift
- Length matters

---
## During-Run Observation

- Live latency
- Live error rate
- Resource use across tiers
- Do not just wait for results

---
## Aborting

- Customer impact in shared env
- Errors run away
- Resource exhaustion on the wrong tier
- Have a kill switch

---
## Result Capture

- Generator metrics
- Application metrics
- Infrastructure metrics
- Logs sampled

---
## Latency Distribution

- Histogram, not just averages
- Compare percentiles run to run
- Look for changing tail shape
- Plot side by side

---
## Throughput

- Requests per second by endpoint
- Steady or drifting
- Match expected mix
- Compare with capacity target

---
## Errors

- Rate
- Status code mix
- New errors during run
- Reproduce in lower environment

---
## Bottleneck Hunt

- Highest-utilized component
- Saturation signs: queue length, CPU, latency at component
- Profile that component
- Iterate

---
## Bottleneck Categories

- CPU
- Memory and GC
- I/O
- Locks and contention
- Downstream calls

---
## Reporting

- Hypothesis
- Setup
- Numbers
- Bottleneck
- Action items

---
## Comparisons

- Versus baseline
- Versus prior release
- Versus capacity target
- Trend over time

---
## Action Items

- Owner per item
- Deadline
- Re-test after fix
- Track regressions

---
## Common Run Mistakes

- No baseline
- Average reporting only
- One run, no repeats
- No live observation
- Reports without action items
