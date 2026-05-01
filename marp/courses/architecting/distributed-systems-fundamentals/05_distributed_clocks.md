---
tags:
  - concepts:distributed-clocks
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Distributed Clocks

---
## What This Chapter Covers

- Why clocks are hard in distributed systems
- Wall clocks and their limitations
- NTP and clock skew
- Logical clocks (Lamport)
- Vector clocks
- Hybrid clocks (TrueTime)
- Practical guidance

---
## Why Clocks Matter

- "Did A happen before B?"
- Crucial for: ordering events, causality, conflict resolution
- Across machines: tricky
- Wrong clock answers cause subtle bugs
- A perennial source of distributed-system pain

---
## Wall Clocks

- Each machine has its own clock
- Drifts: ~10ms per day on consumer hardware
- Can jump (NTP corrections, manual changes)
- Different machines disagree
- Don't compare wall-clock times across machines

---
## NTP

- Network Time Protocol; synchronises clocks
- Public NTP servers; corporate ones too
- Typical accuracy: 1-50ms
- Better with PTP (sub-millisecond)
- Doesn't make clocks identical, just close

---
## Clock Skew

- The difference between two clocks at the same instant
- Always non-zero
- Bounded with NTP; unbounded without
- Code that assumes clock skew == 0 will fail
- Worst case: leap seconds, NTP outages

---
## Monotonic Clocks

- Don't go backwards
- Don't track real time
- For measuring durations: ideal
- POSIX: `CLOCK_MONOTONIC`
- Use these for timeouts, latency

---
## Logical Clocks (Lamport)

- A counter incremented on each event
- Send `(time, value)`; receiver sets its time to `max(local, received) + 1`
- Captures causality: if A &#8594; B then time(A) < time(B)
- Doesn't capture absence of causality
- Lamport's foundational work (1978)

---
## Lamport Clocks Limitation

- A < B in Lamport time may not mean A happened before B
- Could be: concurrent events with arbitrary numbers
- "If A &#8594; B then time(A) < time(B)" — implication, not equivalence
- Useful for ordering; insufficient for causality detection

---
## Vector Clocks

- Each node has a vector of counters (one per node)
- On event: increment own slot
- On send: include the vector
- On receive: take element-wise max + own increment
- Captures causality fully

---
## Vector Clock Comparison

- Two vectors V, W are *concurrent* if neither V &le; W nor W &le; V
- V &lt; W if V[i] &le; W[i] for all i, with strict inequality somewhere
- Lets you detect: causally dependent vs concurrent
- Used in: Dynamo, Riak, version vectors

---
## Vector Clock Cost

- Size grows with number of nodes
- For systems with many short-lived clients: prohibitive
- "Dotted version vectors" mitigate
- Practical for fixed-size clusters

---
## Hybrid Logical Clocks

- Combine wall clock + counter
- "Time" is `(physical, logical)`
- Tightly coupled to physical time but with monotonicity guarantees
- Used in: CockroachDB
- Sweet spot for some systems

---
## TrueTime (Google Spanner)

- Spanner has dedicated GPS / atomic clocks in every datacenter
- API returns `(earliest, latest)` instead of "now"
- Uses bounded uncertainty for global ordering
- Required for Spanner's external consistency
- Hardware investment most companies don't make

---
## Practical Guidance

- Don't compare wall clocks across machines for correctness
- Use NTP; alert on huge skews
- Use monotonic clocks for durations
- Use logical clocks for ordering
- Use vector clocks when you need to detect concurrency

---
## Common Clock Mistakes

- "We're using NTP, so clocks are fine" — wrong by 10s of ms easily
- Comparing timestamps from two services as if they're synchronised
- Storing wall-clock time in a distributed system as authoritative ordering
- Ignoring leap seconds (rare but real)
- Trusting JVM clocks across containers (subtler than you'd think)

---
## What To Do

- For ordering: logical or vector clocks
- For physical time: NTP-synchronised wall clock
- For uniqueness: UUIDs or monotonic IDs from a single source
- For consensus on order: a leader (Raft), not clocks
- The clock is one input; not the truth
