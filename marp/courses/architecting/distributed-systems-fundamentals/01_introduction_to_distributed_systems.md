---
tags:
  - concepts:distributed-systems
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Introduction to Distributed Systems

---
## What This Chapter Covers

- What a distributed system is
- Why we build them
- The 8 fallacies of distributed computing
- Local vs distributed
- Trade-offs
- A short tour of what's ahead

---
## What A Distributed System Is

- Multiple computers cooperating to deliver a service
- They communicate over a network
- No single component is the whole system
- Each may fail independently
- Even "your laptop" + cloud is a distributed system

---
## Why Distribute

- Scale: more capacity than one machine
- Availability: survive a node failure
- Latency: serve users from nearby
- Durability: replicate to survive hardware loss
- Specialisation: different machines for different jobs

---
## The 8 Fallacies

- The network is reliable
- Latency is zero
- Bandwidth is infinite
- The network is secure
- Topology doesn't change
- There is one administrator
- Transport cost is zero
- The network is homogeneous

---
## What The Fallacies Mean

- Each is *false*; designers who assume true build broken systems
- Networks drop packets; latency is variable; bandwidth is finite
- "It works in dev" usually means "I assumed the fallacies"
- Distributed system design is about handling these realities
- Read Peter Deutsch (1994) for the original

---
## Local vs Distributed Calls

- Local function call: nanoseconds; never fails (unless OOM)
- Distributed call: milliseconds-to-seconds; can fail in many ways
- Treating distributed calls as local: classic disaster
- The first lesson: respect the network

---
## Failure Modes

- Network partition (some nodes can't reach others)
- Slow node (alive but unresponsive)
- Crashed node (dead)
- Byzantine node (lying / corrupted)
- Most systems handle the first three; the fourth is exotic

---
## Determinism Goes Out The Window

- Same input + same code &#8594; same output (local)
- Distributed: timing matters; partial state matters
- Tests pass locally; fail in prod
- Fundamentally harder to reason about
- Tools (formal methods, fault injection) help

---
## Trade-Offs

- Strong consistency vs availability (CAP)
- Latency vs throughput
- Simplicity vs scalability
- Complexity always grows
- Pick deliberately; don't drift

---
## When NOT To Distribute

- Your data fits on one big server
- Your traffic fits on one big server
- You don't need cross-region availability
- Your team is small
- "We need microservices" before having a working monolith — usually wrong

---
## A Map Of The Course

- CAP theorem and consistency models
- Consensus algorithms (Paxos, Raft)
- Time and clocks
- CRDTs
- Leader election
- Partitioning and replication
- Failure modes

---
## Vocabulary You'll Need

- **Node**: a participant
- **Replica**: a copy of data on another node
- **Partition**: a network split *or* a data shard (context-dependent)
- **Quorum**: a majority required to commit
- **Eventual consistency**: replicas converge over time

---
## What This Course Won't Cover

- Distributed databases in detail (separate course)
- Specific tools (Kafka, Cassandra, etcd) in depth
- Advanced consensus (Byzantine fault tolerance, blockchain)
- This is the *fundamentals*; build the conceptual framework

---
## Common Beginner Mistakes

- "Just retry" without idempotency
- Assuming clocks are synchronised
- Storing state in memory and not replicating
- Building everything as if it can't fail
- Premature distribution
