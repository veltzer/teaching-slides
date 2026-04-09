---
tags:
- concepts:distributed-systems
- concepts:architecture
- concepts:scalability
level: intermediate
category: architecture
audience:
- audiences:developers
- audiences:architects
---
# Distributed Systems Concepts
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/architecting/distributed-systems-concepts/title.svg)

## What Is a Distributed System?

A collection of independent computers that appears to users as a single coherent system

- Multiple autonomous computers
- Connected through a network
- Coordinating to achieve a common goal
- Transparent to end users

---

## Why Distributed Systems?

- **Scalability** - Handle more load
- **Reliability** - No single point of failure
- **Performance** - Parallelism and locality
- **Geographic Distribution** - Global presence
- **Cost Efficiency** - Commodity hardware

---

## The Fundamental Challenge

![the_fundamental_challenge](svg/lectures/architecting/distributed-systems-concepts/the_fundamental_challenge.svg)

---

## The Eight Fallacies

1. The network is reliable
1. Latency is zero
1. Bandwidth is infinite
1. The network is secure
1. Topology doesn't change
1. There is one administrator
1. Transport cost is zero
1. The network is homogeneous

---

## Fallacy 1: Network Reliability

![fallacy_1_network_reliability](svg/lectures/architecting/distributed-systems-concepts/fallacy_1_network_reliability.svg)

Messages can be lost, duplicated, or reordered

---

## Fallacy 2: Latency Is Zero

![fallacy_2_latency_is_zero](svg/lectures/architecting/distributed-systems-concepts/fallacy_2_latency_is_zero.svg)

---

## Types of Failures

**Crash Failures:**
- Node stops responding
- Detectable (eventually)

**Byzantine Failures:**
- Node sends incorrect/malicious messages
- Hardest to handle

**Network Partitions:**
- Groups of nodes isolated
- Split-brain scenarios

---

## Partial Failures

![partial_failures](svg/lectures/architecting/distributed-systems-concepts/partial_failures.svg)

---

## Time and Ordering

In distributed systems, there's no global clock

![time_and_ordering](svg/lectures/architecting/distributed-systems-concepts/time_and_ordering.svg)

---

## Logical Clocks

Lamport timestamps establish partial ordering:

![logical_clocks](svg/lectures/architecting/distributed-systems-concepts/logical_clocks.svg)

---

## Vector Clocks

Track causality across all nodes:

![vector_clocks](svg/lectures/architecting/distributed-systems-concepts/vector_clocks.svg)

---

## Consensus Problem

Getting distributed nodes to agree on a value

![consensus_problem](svg/lectures/architecting/distributed-systems-concepts/consensus_problem.svg)

---

## FLP Impossibility

Fischer, Lynch, Paterson (1985):

### No deterministic algorithm can guarantee consensus in an asynchronous system with even one faulty process

Implications:
- Perfect consensus is impossible
- Must relax requirements
- Use timeouts (not truly async)

---

## Consensus Algorithms

**Paxos:**
- Mathematically proven
- Complex to implement
- Foundation for many systems

**Raft:**
- Designed for understandability
- Leader-based approach
- Widely adopted

---

## Raft Leader Election

![raft_leader_election](svg/lectures/architecting/distributed-systems-concepts/raft_leader_election.svg)

---

## Byzantine Fault Tolerance

When nodes can be malicious:

![byzantine_fault_tolerance](svg/lectures/architecting/distributed-systems-concepts/byzantine_fault_tolerance.svg)

---

## Replication Strategies

![replication_strategies](svg/lectures/architecting/distributed-systems-concepts/replication_strategies.svg)

---

## State Machine Replication

All replicas execute same operations in same order:

1. Client sends request to leader
1. Leader assigns sequence number
1. Leader replicates to followers
1. Majority acknowledgment
1. Apply to state machine
1. Respond to client

---

## Gossip Protocols

![gossip_protocols](svg/lectures/architecting/distributed-systems-concepts/gossip_protocols.svg)

---

## Eventual Consistency

![eventual_consistency](svg/lectures/architecting/distributed-systems-concepts/eventual_consistency.svg)

---

## Quorum Systems

![quorum_systems](svg/lectures/architecting/distributed-systems-concepts/quorum_systems.svg)

---

## Split Brain Problem

![split_brain_problem](svg/lectures/architecting/distributed-systems-concepts/split_brain_problem.svg)

---

## Handling Split Brain

**Majority Quorum:**
- Only partition with >50% nodes stays active
- Minority partition becomes read-only or unavailable

**Fencing Tokens:**
- Monotonically increasing tokens
- Storage rejects older tokens

---

## Distributed Transactions

![distributed_transactions](svg/lectures/architecting/distributed-systems-concepts/distributed_transactions.svg)

---

## Saga Pattern

Long-running transactions as series of local transactions:

![saga_pattern](svg/lectures/architecting/distributed-systems-concepts/saga_pattern.svg)

---

## Idempotency

Operations that can be applied multiple times:

![idempotency](svg/lectures/architecting/distributed-systems-concepts/idempotency.svg)

---

## Distributed Caching

![distributed_caching](svg/lectures/architecting/distributed-systems-concepts/distributed_caching.svg)

Cache invalidation is hard!

---

## Load Balancing Strategies

![load_balancing_strategies](svg/lectures/architecting/distributed-systems-concepts/load_balancing_strategies.svg)

---

## Service Discovery

![service_discovery](svg/lectures/architecting/distributed-systems-concepts/service_discovery.svg)

---

## Circuit Breaker Pattern

![circuit_breaker_pattern](svg/lectures/architecting/distributed-systems-concepts/circuit_breaker_pattern.svg)

Prevent cascading failures

---

## Backpressure

![backpressure](svg/lectures/architecting/distributed-systems-concepts/backpressure.svg)

---

## Rate Limiting

Control request flow:

- **Token Bucket** - Fixed capacity, refills at constant rate
- **Leaky Bucket** - Smooth output rate
- **Sliding Window** - Track requests in time window
- **Fixed Window** - Reset counter at intervals

---

## Distributed Tracing

![distributed_tracing](svg/lectures/architecting/distributed-systems-concepts/distributed_tracing.svg)

---

## Observability Pillars

![observability_pillars](svg/lectures/architecting/distributed-systems-concepts/observability_pillars.svg)

---

## Chaos Engineering

Intentionally inject failures:

- Network partitions
- Node crashes
- Latency injection
- Resource exhaustion
- Clock skew

Learn how system behaves under stress

---

## Distributed System Patterns

**Leader Election** - Single coordinator
**Gossip Protocol** - Epidemic information spread
**Consistent Hashing** - Distributed hash tables
**Vector Clocks** - Causality tracking
**Quorum** - Majority agreement
**Saga** - Distributed transactions
**Circuit Breaker** - Fault isolation

---

## Trade-offs Everywhere

![trade_offs_everywhere](svg/lectures/architecting/distributed-systems-concepts/trade_offs_everywhere.svg)

---

## Key Takeaways

- Embrace failure as normal
- No global state or time
- Consensus is expensive
- Eventual consistency is often enough
- Design for partition tolerance
- Monitor and trace everything
