---
tags:
  - concepts:consistency
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Consistency Models

---
## Spectrum

![consistency_spectrum](svg/courses/architecting/distributed-systems-fundamentals/03_consistency_models/consistency_spectrum.svg)

---
## What This Chapter Covers

- A spectrum of consistency
- Strong consistency
- Linearisability
- Sequential consistency
- Causal consistency
- Eventual consistency
- Picking a model

---
## Why Consistency Models

- "Consistent" alone is too vague
- Different models give different guarantees
- Different costs (latency, complexity)
- Choose the *weakest* model that satisfies your needs
- Stronger costs more

---
## Linearisability

- The strongest single-object model
- Each operation appears to take effect at some instant
- All operations have a single global order
- "Looks like one node from the client's perspective"
- Required for: locks, leader election, counters

---
## Sequential Consistency

- All clients see operations in the same order
- That order may not match real-time order
- Cheaper than linearisability
- Less common as a primary target
- Often confused with linearisability

---
## Causal Consistency

- If A happened-before B, all clients see A before B
- Concurrent operations: any order
- Captures user-perceivable order without global coordination
- Used in chat apps, social networks
- A sweet spot between strong and eventual

---
## Eventual Consistency

- Replicas eventually converge if no new writes
- "Eventually" is vague; quantify it
- Cheapest model; most available
- Application sees stale reads
- Standard for AP systems

---
## Strong Eventual Consistency

- Eventual consistency + same end state regardless of operation order
- Achieved by CRDTs
- Available as eventual; converges as strong
- Best of both, where applicable

---
## Read-Your-Writes

- Client always sees its own writes
- Useful: post a comment, see it immediately
- Achievable with sticky sessions or write-through caches
- Subset of consistency; client-centric

---
## Monotonic Reads

- A client doesn't see *older* data than it has seen before
- Useful: don't show order with status "shipped" then "pending"
- Sticky sessions; read-from-leader
- Easy to violate without thought

---
## Bounded Staleness

- Reads see data at most N seconds old
- Quantifies eventual consistency
- Common in cloud DBs: "data may be up to 5 seconds stale"
- Easier to reason about than pure eventual

---
## Snapshot Isolation

- Each transaction sees a consistent snapshot
- Can serve concurrent transactions
- Read skew possible; write skew possible
- Common in DBs (Postgres, Oracle)
- Different from serialisability

---
## Serialisability

- Concurrent transactions equivalent to *some* serial order
- Strongest standard isolation level
- More expensive than snapshot isolation
- Rare in distributed DBs
- Required for some financial workflows

---
## A Spectrum

- Strict / Linearisable
- Sequential
- Causal
- Read-Your-Writes
- Eventual
- Each weaker; cheaper; more available
- Pick the weakest that works

---
## Mixing Models

- Different operations, different models
- "Account balance: strong; activity feed: eventual"
- Per-operation tuning common in modern DBs
- Document which is which

---
## Common Consistency Mistakes

- Assuming strong consistency without checking
- Choosing eventual without understanding the staleness window
- Building a UX that requires read-your-writes without it
- Trusting documentation that says "eventually consistent" without bounds
- Designing for one model; deploying with another (config drift)
