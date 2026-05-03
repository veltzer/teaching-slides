---
tags:
  - concepts:crdt
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# CRDTs: Conflict-Free Replicated Data Types

---
## What This Chapter Covers

- The problem CRDTs solve
- State-based vs op-based CRDTs
- Common CRDTs: counters, sets, registers
- Use cases
- Limitations
- A short tour

---
## The Problem

- Multiple replicas accept writes
- They reconcile later
- Without coordination, what's the merged state?
- Naive merge can lose data or pick "wrong" winners
- CRDTs provide deterministic merges

---
## Common CRDT Types

![crdt_kinds](svg/courses/architecting/distributed-systems-fundamentals/06_crdts_conflict_free_replicated_data_types/crdt_kinds.svg)

---
## CRDT Use Cases

![crdt_use_cases](svg/courses/architecting/distributed-systems-fundamentals/06_crdts_conflict_free_replicated_data_types/crdt_use_cases.svg)

---
## What "Conflict-Free" Means

- Concurrent updates merge to a deterministic result
- All replicas converge to the same state
- No conflict resolution needed
- Replicas can operate independently
- Strong eventual consistency

---
## State-Based CRDTs

- Each replica has a state
- Periodically: send full state to peers
- Peers merge by taking the *join* of states
- Join must be commutative, associative, idempotent
- Examples: G-Counter, OR-Set

---
## Op-Based CRDTs

- Each replica broadcasts operations
- Peers apply operations
- Operations must commute (if delivered in any order, same result)
- Reliable broadcast required
- Smaller messages than state-based

---
## G-Counter

- "Grow-only counter"
- Each replica increments only its own counter
- Total = sum of all replicas' counters
- Merge: max of each replica's value
- Used for: page views, votes that only increase

---
## PN-Counter

- Two G-Counters: increments and decrements
- Total = increments - decrements
- Supports both add and subtract
- Used for: distributed counters with both directions

---
## OR-Set

- "Observed-Remove Set"
- Add: include with a unique tag
- Remove: only the (element, tag) pairs you've seen
- Concurrent add and remove of same element: add wins
- Used for: shared collections

---
## LWW-Register

- "Last-Write-Wins"
- Each value has a timestamp
- Highest timestamp wins on merge
- Simple; loses concurrent writes
- Common in eventual-consistency stores

---
## CRDT Use Cases

- Collaborative editing (Google Docs, Figma)
- Distributed counters
- Shared shopping carts
- Replicated graphs (DAGs)
- Session state across regions

---
## CRDTs in Practice

- Riak: built on CRDTs
- Redis CRDTs (in Redis Enterprise)
- Yjs and Automerge: collaborative editing libraries
- DynamoDB Streams + CRDTs in application code
- Firebase Realtime DB

---
## Tradeoffs

- Pro: no coordination needed; high availability
- Pro: deterministic merges
- Con: more storage (vector clocks, tombstones)
- Con: not all data structures are easy to make CRDT
- Con: operations are restricted (no "delete unconditionally")

---
## Tombstones

- Removed elements need to be tracked, not just deleted
- Otherwise: late-arriving "add" might re-add removed elements
- Tombstones grow over time; periodic GC
- A real cost of OR-Sets and similar

---
## CRDTs vs Coordination

- Coordination (consensus): strong consistency, slow, less available
- CRDTs: eventually consistent, fast, always available
- Different trade-offs; different use cases
- Mix: CRDTs for high-volume; consensus for control plane

---
## When To Use CRDTs

- Collaborative apps (multiple users editing simultaneously)
- Multi-region writes
- Edge computing
- Mobile apps with offline support
- High-availability over strict consistency

---
## When NOT To

- Strong consistency required (financial)
- Simple single-region apps
- Operations not naturally commutative
- Lots of metadata adds storage / network cost
- Domain doesn't fit existing CRDT types

---
## Common CRDT Mistakes

- Custom CRDTs without proving correctness (wrong merges)
- LWW-Register where you needed multi-value (data lost)
- Tombstone garbage collection bugs
- Vector clocks growing unbounded
- Treating CRDTs as a magic solution; they have constraints
