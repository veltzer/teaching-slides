---
tags:
  - testing:performance
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Tools and Environments

---
## What This Chapter Covers

- Tool families
- Picking a tool
- Test environments
- Production-likeness
- Networks and topology

---
## Tool Families

- Open-source script-based
- Open-source GUI-based
- Hosted load test platforms
- Cloud provider services

---
## Script-Based

- JavaScript or Lua test scripts
- Reproducible
- Source-controlled
- Common in modern stacks

---
## GUI-Based

- Drag and drop scenarios
- Easier for testers without coding
- Harder to version
- Still in use for legacy

---
## Hosted Platforms

- Distributed load generators
- High target rates
- Pay per test
- Good for occasional spikes

---
## Picking A Tool

- Skill set of team
- Target rate needed
- Protocol support
- Integration with CI

---
## Test Environment

- As production-like as possible
- Same software versions
- Same data shape
- Similar topology

---
## Likeness Spectrum

![env_likeness](svg/courses/testing/performance-testing/02_tools_and_environments/env_likeness.svg)

---
## Why Production-Likeness

- Different config breaks results
- Caches behave differently
- Latency profiles change
- Conclusions invalid otherwise

---
## Sampling Production Data

- Cleanse for PII
- Preserve distributions
- Match volume scale
- Document what you changed

---
## Synthetic Data

- Fast to generate
- Less realistic
- Useful for stress tests
- Validate against real data later

---
## Load Generator Placement

- Cloud region near or far
- Effects realistic latency
- Avoid co-located noise
- Scale generators with target

---
## Network Conditions

- Add latency
- Add packet loss
- Test bad networks
- Realistic for mobile users

---
## Observability During Tests

- Same monitoring as production
- Plus load-generator metrics
- Trace samples saved
- Logs aggregated

---
## CI Integration

- Smoke perf tests on PRs
- Full perf tests nightly
- Block on regression
- Trends tracked over time

---
## Common Environment Mistakes

- Smaller environment than production
- Different software versions
- No network shaping
- One generator for huge load
- Tests in shared environments
