---
tags:
  - concepts:cap-theorem
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# CAP Theorem

---
## What This Chapter Covers

- The CAP theorem precisely stated
- C, A, and P meanings
- Why P is non-negotiable
- CP vs AP systems
- The PACELC extension
- Misuses of CAP

---
## CAP Triangle

![cap_triangle](svg/courses/architecting/distributed-systems-fundamentals/02_cap_theorem/cap_triangle.svg)

---
## CAP Stated

- A distributed data store cannot simultaneously provide more than two of:
- **Consistency**: all reads see the latest write
- **Availability**: every request gets a response
- **Partition tolerance**: continues to operate despite network partitions

---
## What Partitions Are

- Some nodes can't communicate with others
- Not "downtime"; the nodes are alive
- They just can't see each other
- Common: switch failure, datacenter loss, transient network blip
- Real; happens regularly

---
## Why P Is Non-Negotiable

- Real networks partition
- You can't pretend they don't
- The choice is: when partitioned, do we favour C or A?
- Every distributed system makes this trade-off
- "CA only" is a marketing fantasy

---
## CP Systems

- During partition: refuse some requests to keep consistent
- Examples: ZooKeeper, etcd, Consul
- The minority side stops accepting writes
- Used for: configuration, leader election, locks
- Strict consistency at the cost of availability

---
## AP Systems

- During partition: accept all requests; reconcile later
- Examples: Cassandra, DynamoDB, CouchDB
- Both sides accept writes
- Conflicts resolved at read time or via CRDTs
- Eventual consistency at the cost of immediate consistency

---
## CP vs AP By Example

- Bank transaction: CP (you can't have two valid balances)
- Shopping cart: AP (let user add items; merge later)
- Match the system to the data's tolerance for staleness
- Some systems mix per-operation

---
## Misuses Of CAP

- "Pick two": misleading; you always have P
- "Cassandra is AP": yes, but tunable consistency exists
- "Consistent ALWAYS": only outside partitions
- Read the original Brewer/Lynch papers; the nuances matter

---
## PACELC Extension

- **Partition** &#8594; **Availability or Consistency**
- **Else** (no partition) &#8594; **Latency or Consistency**
- Even without partitions, there's a trade-off
- More complete picture than CAP alone

---
## Latency vs Consistency

- Strong consistency requires coordination
- Coordination requires extra round trips
- More latency for stronger guarantees
- Most systems trade some consistency for sub-100ms latency

---
## Tunable Consistency

- Per-operation consistency choice
- DynamoDB: "strongly consistent read" (slower) or "eventually consistent" (faster)
- Cassandra: read/write consistency levels (ONE, QUORUM, ALL)
- Different operations have different needs
- A pragmatic compromise

---
## Real Decisions

- Will users notice 5 seconds of staleness? AP often fine
- Will users notice an inconsistent balance? CP required
- Most "we need CP" turns out to need bounded staleness
- Most "we're fine with AP" actually wants conflict-free updates

---
## Misunderstandings

- "Consistent" doesn't mean ACID
- "Available" doesn't mean "fast"
- "Partition tolerant" doesn't mean "no downtime"
- Each term has a precise CAP meaning; not the everyday meaning
- Read the literature; vocabulary trips many engineers

---
## Beyond CAP

- CRDTs: conflict-free; eventually consistent without coordination
- CALM theorem: monotonic computations don't need coordination
- Modern systems exploit these to avoid the CAP trade-off where possible
- Active research area

---
## Common CAP Mistakes

- Treating CAP as a marketing slogan
- Ignoring partition tolerance ("our network is fine")
- Choosing CP without understanding the availability cost
- Choosing AP without designing for conflict resolution
- Not testing partition behaviour explicitly
