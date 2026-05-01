---
tags:
  - concepts:failure-modes
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Failure Modes

---
## What This Chapter Covers

- Common distributed-system failures
- Network failures
- Node failures
- Slow nodes (the hardest case)
- Cascading failures
- Detection and recovery
- Chaos engineering

---
## Catalogue of Failures

- Node crashes
- Network partitions
- Network packet loss
- Slow nodes
- Disk full
- Clock skew
- Byzantine (malicious / corrupted)
- All happen; design for each

---
## Network Failures

- Packet loss: TCP retransmits; latency spikes
- Partitions: nodes can't reach each other
- High latency: looks like everything else's slowness
- Partial: some links work, others don't
- The most common failure

---
## Node Failures

- Hardware: disk, RAM, CPU, power
- OS crash, kernel panic
- Process crash (OOM killer, bug)
- Hard to distinguish from network failure remotely
- Frequency: anything mechanical eventually fails

---
## Slow Nodes

- Alive but very slow
- Worse than crashed: heartbeats may still arrive
- Causes: GC pause, disk I/O contention, network congestion
- Detection: tail latency monitoring
- Mitigation: hedged requests, load shedding

---
## The Slow Node Problem

- A timeout-based system can't tell a slow node from a dead one
- Wait too long: app hangs
- Wait too short: false positives, retries
- This is *the* hard problem
- Practical solution: hedged requests + circuit breakers

---
## Cascading Failures

- One node fails &#8594; load shifts to others &#8594; they fail too
- Common cause: insufficient capacity headroom
- Common cause: synchronous calls that pile up on slow services
- Mitigation: bulkheads, circuit breakers, load shedding
- The way most outages happen

---
## Bulkheads

- Isolate resources by type / consumer
- One slow tenant doesn't affect others
- Per-service connection pools
- Per-tenant quotas
- Inspired by ship design: a hole in one section doesn't sink the ship

---
## Circuit Breakers

- Track recent failures
- After N failures: "open" the circuit; reject calls without trying
- After a timeout: try one call ("half-open")
- On success: close; on failure: stay open
- Prevents pile-up on a failing dependency

---
## Retries

- Almost always: try again
- Beware: amplifies load on the failing service
- Exponential backoff: reduce pressure
- Jitter: avoid thundering herds
- Don't retry non-idempotent operations without an idempotency key

---
## Load Shedding

- When overwhelmed: refuse some requests
- Better: 50% of users get 200; some get 503
- Worse: everyone gets 30s timeouts, all fail
- Fail fast; preserve capacity for what you can serve
- The tail of resilient systems

---
## Timeouts

- *Always* set timeouts
- Defaults: often "infinity" — disastrous
- Tune to: 95th percentile latency * 2
- Different per operation
- The most common cause of cascading failure: missing timeouts

---
## Idempotency For Retries

- Retried operations must be safe
- Idempotency keys for non-idempotent operations (POST, financial)
- Server dedupes by the key
- Without it: a retry causes duplicate orders
- Built into your APIs from day one

---
## Fault Injection

- Deliberately introduce failures in test
- Tools: chaos-monkey, toxiproxy
- Validates: timeouts, retries, fallbacks all work
- Without injection: untested fail paths
- Standard practice at high-availability shops

---
## Chaos Engineering

- Run fault injection in *production*
- Sounds scary; in mature orgs, the routine
- Catches: untested failure modes, misconfigurations
- Netflix's Simian Army popularised
- Build the muscle; don't wait for real outage

---
## The "Game Day"

- Plan a failure exercise: "switch fails at 2pm"
- Team practices the response
- Reveals: missing runbooks, slow alerts, knowledge gaps
- Periodic; before they're for real
- Sports teams practice; engineering teams should too

---
## Detection

- Health checks: liveness + readiness
- Liveness: am I alive?
- Readiness: am I ready to serve?
- External monitoring beats self-monitoring
- Multiple signals: one alone misleads

---
## Common Failure-Mode Mistakes

- No timeouts (cascading failures)
- Retries without idempotency (duplicate effects)
- No circuit breakers (pile-up on failing dependency)
- Health checks that don't catch real problems
- "It worked in test" — and prod has different failure modes

---
## Course Wrap-Up

- Distributed systems are *systems of failure modes*
- Embrace: failures will happen; design for them
- CAP, consensus, clocks, replication: each a tool
- Test failure scenarios deliberately
- "It works on the happy path" is the easy half
