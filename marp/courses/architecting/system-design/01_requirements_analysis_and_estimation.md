---
tags:
  - architecture:system-design
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Requirements Analysis and Estimation

---
## What This Chapter Covers

- Functional vs non-functional requirements
- Capacity estimation
- Latency and throughput targets
- The back-of-the-envelope mindset
- Common estimation traps

---
## Back-of-Envelope

![back_of_envelope](svg/courses/architecting/system-design/01_requirements_analysis_and_estimation/back_of_envelope.svg)

---
## Capacity Estimation

![capacity_estimation](svg/courses/architecting/system-design/01_requirements_analysis_and_estimation/capacity_estimation.svg)

---
## Functional Requirements

- What the system *does*
- Use cases, user stories
- "User can post a tweet"
- The base of any design
- Often well-known up-front

---
## Non-Functional Requirements

- How well it does it
- Latency, throughput, availability
- "Users see their feed in under 200ms"
- Often the hard part
- Drives architecture decisions

---
## Capacity Estimation

- "How big does this need to be?"
- Users, requests/sec, data size, bandwidth
- Twitter: 500M tweets/day, ~6K/sec average, 50K/sec peak
- Each number drives a design choice
- Estimate before designing

---
## Back-of-the-Envelope

- 1ns: CPU cycle
- 100ns: RAM access
- 1us: SSD random read
- 10ms: disk seek
- 100ms: cross-DC round trip
- Memorise; use to estimate latency

---
## Bytes and Powers of Ten

- KB: 10^3, MB: 10^6, GB: 10^9, TB: 10^12, PB: 10^15
- 1 ASCII char: 1 byte
- 1 image: 100KB-1MB
- 1 minute video (HD): 100MB
- 1 day's tweets: ~5 GB

---
## Throughput Math

- 1B users * 10 actions/day = 10B actions/day
- 10B / 86400s = ~115K actions/sec average
- Peak: usually 2-5x average
- Account for headroom (50% spare)
- Actual capacity: ~500K/sec

---
## Latency Targets

- User-facing API: 100-200ms p95
- Internal RPC: 10-50ms
- Database query: 1-10ms
- Cache hit: <1ms
- Each layer has a budget

---
## Storage Estimation

- Users x data per user x retention
- 1B users x 1MB profile = 1PB
- Plus indexes (~30% extra)
- Plus replication (3x)
- Plus headroom (50%)
- Real total: 5-6PB

---
## Read vs Write Ratios

- Twitter: 100:1 reads to writes
- Banks: closer to 1:1
- Read-heavy &#8594; replicas, caching
- Write-heavy &#8594; partitioning, async
- Different optimisation paths

---
## SLAs

- 99.9% = 8.7 hours down/year
- 99.99% = 52 minutes down/year
- 99.999% = 5 minutes down/year
- Each 9 is ~10x harder than the last
- Don't promise more than you can deliver

---
## Common Estimation Mistakes

- Forgetting peak vs average
- No headroom
- Underestimating bandwidth (forgot images?)
- Confusing reads and writes
- "Round numbers" that hide order of magnitude

---
## A Practical Approach

- State the requirements out loud
- Estimate users, traffic, data
- Sanity-check with known systems
- Pick technologies that fit
- Reserve 50% headroom; you'll need it
