---
tags:
  - concepts:consensus
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Consensus Algorithms

---
## What This Chapter Covers

- Why consensus
- Two Generals Problem
- Paxos
- Raft
- Byzantine fault tolerance
- Practical consensus systems
- Limits

---
## Why Consensus

- A group of nodes must agree on a value
- "Who is the leader?", "What's the next entry?"
- Despite failures, network delays
- The hardest problem in distributed computing
- Foundation for many other guarantees

---
## Two Generals Problem

- Two armies, separated by a valley
- Must agree to attack at the same time
- Messengers can be captured
- Provably impossible to guarantee agreement
- The intuition: there's no way to be *certain* the other side received the message

---
## What Consensus Solves

- Many participants; want to agree on one value
- Tolerates: process crashes, message loss, message delay
- Doesn't tolerate (in normal consensus): malicious participants
- Ensures: all surviving participants agree
- The basis of distributed databases, locks, leader election

---
## FLP Impossibility

- Fischer, Lynch, Paterson (1985)
- "Consensus is impossible in an asynchronous system with even one crash"
- Strict reading: no algorithm always terminates
- Practice: with timeouts and stable networks, we get "good enough"
- All real consensus algorithms work around FLP

---
## Paxos

- Leslie Lamport, 1989 (published 1998)
- Provably correct; notoriously hard to understand
- Basic Paxos: agree on one value
- Multi-Paxos: a sequence of values
- Used in: Google Chubby, Spanner

---
## How Paxos Works (Sketch)

- **Prepare**: a proposer asks acceptors to promise to ignore older proposals
- **Promise**: acceptors respond with their last promise
- **Accept**: proposer sends a value; acceptors accept
- **Learn**: a value is chosen when a quorum accepts
- Quorum: majority

---
## Why Paxos Is Hard

- Many roles (proposer, acceptor, learner)
- Many edge cases
- Lamport's original paper is famously dense
- Practical implementations diverge in details
- Prefer Raft for new work

---
## Raft

- Stanford, 2014
- Designed to be *understandable*
- Provably equivalent to Paxos in safety
- Three sub-problems: leader election, log replication, safety
- Adopted in: etcd, Consul, CockroachDB, RethinkDB

---
## Raft Leader Election

- Each follower has a random election timeout (150-300ms)
- On timeout: become a candidate; request votes
- Win majority &#8594; become leader
- Leader sends heartbeats to suppress new elections
- Simple, robust

---
## Raft Log Replication

- Clients send commands to leader
- Leader appends to its log
- Leader sends to followers
- Once a majority commits, the leader applies and replies
- Each entry has a term number; monotonically increasing

---
## Quorum

- Majority: more than half
- 3 nodes: 2 must agree
- 5 nodes: 3 must agree
- Can survive `(n-1)/2` failures
- Odd numbers preferred

---
## Byzantine Fault Tolerance

- Tolerates *malicious* participants
- Requires `3f+1` nodes to tolerate `f` Byzantine faults
- More expensive than crash-fault tolerance
- Used in: blockchains, high-stakes systems
- BFT-Paxos, PBFT, Tendermint

---
## Practical Consensus Systems

- **etcd**: Raft; used by Kubernetes
- **Consul**: Raft; service discovery + config
- **ZooKeeper**: ZAB (similar to Paxos); Hadoop ecosystem
- **Spanner**: Paxos at huge scale
- All implement consensus for the control plane

---
## Limits Of Consensus

- Latency: requires multiple round trips
- Throughput: limited by leader
- Doesn't scale linearly with nodes
- Use sparingly: only for state that must be agreed on
- Most data should not go through consensus

---
## Common Consensus Mistakes

- Putting too much through consensus (slow)
- Using consensus where eventual consistency would do
- Not understanding the safety conditions
- Choosing nodes < 3 (no fault tolerance)
- Even number of nodes (no clear majority)

---
## When To Reach For Consensus

- Configuration that must be the same everywhere
- Leader election
- Distributed locks
- Membership / cluster state
- Transaction commit (when truly needed)

---
## When NOT To

- High-volume data writes
- User session state
- Any data where eventual consistency suffices
- "Just put everything in etcd" — slow and expensive
- Use the right tool for the right scale
