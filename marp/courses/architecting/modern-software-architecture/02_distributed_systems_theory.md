---
tags:
  - concepts:architecture
  - concepts:distributed-systems
  - concepts:cap-theorem
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Distributed Systems Theory

---
## What Is a Distributed System?

![what_is_distributed_system](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/what_is_distributed_system.svg)

---
## Why Distributed Systems?

- Handle more traffic than a single machine can support
- Improve availability through redundancy
- Reduce latency by placing data closer to users
- Enable independent development and deployment of components

---
## Core Challenges

- Network is unreliable and introduces latency
- Clocks on different machines drift apart
- Nodes can fail independently and silently
- Achieving consensus across nodes is fundamentally hard

---
## The CAP Theorem

- Proposed by Eric Brewer in 2000, proven in 2002
- In a distributed data store, you can only guarantee two of three:
    - `Consistency` (C)
    - `Availability` (A)
    - `Partition Tolerance` (P)
- Network partitions are inevitable, so the real choice is C vs A

---
## CAP Theorem Diagram

![cap_theorem_diagram](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/cap_theorem_diagram.svg)

---
## CAP Theorem

![cap_theorem](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/cap_theorem.svg)

---
## Consistency in CAP

- Every read receives the most recent write or an error
- All nodes see the same data at the same time
- Linearizability is the strongest form of consistency
- Requires coordination between nodes on every write

---
## Availability in CAP

- Every request receives a non-error response
- The system continues to operate even when some nodes fail
- No guarantee that the response contains the most recent write
- Measured as the percentage of successful responses

---
## Partition Tolerance in CAP

- The system continues to operate despite network partitions
- Messages between nodes can be lost or delayed arbitrarily
- In real-world networks, partitions will happen
- Therefore partition tolerance is not optional

---
## CP Systems

- Prioritize consistency over availability during partitions
- Refuse to serve requests if they cannot guarantee freshness
- Examples: `ZooKeeper`, `etcd`, `HBase`, `MongoDB` (default config)
- Use cases: financial transactions, configuration management

---
## AP Systems

- Prioritize availability over consistency during partitions
- Continue serving requests even with stale data
- Examples: `Cassandra`, `DynamoDB`, `CouchDB`, `Riak`
- Use cases: social media feeds, product catalogs, caching

---
## The PACELC Theorem

![pacelc_theorem](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/pacelc_theorem.svg)

---
## PACELC Examples

| System | Partition (P) | Else (E) |
|--------|--------------|----------|
| `DynamoDB` | A | L |
| `Cassandra` | A | L |
| `MongoDB` | C | C |
| `PNUTS` | A | C |

---
## Consistency Models Spectrum

![consistency_models_spectrum](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/consistency_models_spectrum.svg)

---
## Consistency Trade-Offs

- Stronger consistency means more coordination overhead
- Weaker consistency means better performance and availability

---
## Eventual Consistency

- If no new updates are made, all replicas will eventually converge
- No guarantee on how long convergence takes
- Reads may return stale data temporarily
- Widely used in `AP` systems for high availability

---
## Strong Consistency

- All reads reflect the most recent write across all nodes
- Requires synchronous coordination protocols
- Higher latency due to cross-node communication
- Necessary when correctness depends on data freshness

---
## The Fallacies of Distributed Computing

- Eight assumptions that developers new to distributed systems wrongly make
- Originally listed by Peter Deutsch and James Gosling at Sun Microsystems
- Each fallacy leads to specific categories of bugs and outages
- Understanding them is essential for building robust systems

---
## Fallacy 1: The Network Is Reliable

- Packets get lost, connections drop, switches fail
- Impact: need retries, timeouts, and idempotent operations
- Design pattern: use message queues for critical communication
- Always expect and handle network failures gracefully

---
## Fallacy 2: Latency Is Zero

- Every network call adds milliseconds or more of delay
- Impact: chatty protocols perform poorly over networks
- Design pattern: batch requests and use coarse-grained APIs
- Measure and account for latency in performance budgets

---
## Fallacy 3: Bandwidth Is Infinite

- Network capacity is limited and shared with other traffic
- Impact: large payloads can saturate links and cause congestion
- Design pattern: compress data, paginate responses, use streaming
- Monitor network utilization and plan for growth

---
## Fallacy 4: The Network Is Secure

- Every network boundary is a potential attack surface
- Impact: data in transit can be intercepted or tampered with
- Design pattern: use `TLS`, mutual authentication, and zero-trust networking
- Never assume internal networks are inherently safe

---
## Fallacy 5: Topology Doesn't Change

- Network paths, servers, and load balancers change frequently
- Impact: hardcoded addresses and routes will break
- Design pattern: use service discovery and DNS-based routing
- Build systems that adapt to topology changes automatically

---
## Fallacy 6: There Is One Administrator

- Modern systems span teams, organizations, and cloud providers
- Impact: no single person controls all the infrastructure
- Design pattern: use well-defined APIs and contracts at boundaries
- Assume limited control over external dependencies

---
## Fallacy 7: Transport Cost Is Zero

- Serialization, deserialization, and network I/O consume resources
- Impact: excessive remote calls waste CPU, memory, and bandwidth
- Design pattern: cache frequently accessed data locally
- Consider the total cost of each network interaction

---
## Fallacy 8: The Network Is Homogeneous

- Systems use different protocols, formats, and versions
- Impact: interoperability issues at service boundaries
- Design pattern: use standard protocols like `HTTP`, `gRPC`, or `AMQP`
- Test against multiple client and server versions

---
## High Availability Defined

- The ability of a system to remain operational for a high percentage of time
- Measured in "nines": 99.9% (three nines) = 8.76 hours downtime per year
- Achieved through redundancy, failover, and fault tolerance
- Requires both technical and operational disciplines

---
## Availability Tiers

| Level | Uptime | Downtime/Year |
|-------|--------|---------------|
| 99% | Two nines | 3.65 days |
| 99.9% | Three nines | 8.76 hours |
| 99.99% | Four nines | 52.6 minutes |
| 99.999% | Five nines | 5.26 minutes |

---
## Redundancy Strategies

- Active-Active: multiple nodes serve traffic simultaneously
- Active-Passive: standby node takes over when primary fails
- N+1 Redundancy: one extra node beyond the minimum required
- Geographic redundancy: replicate across data centers or regions

---
## Active-Active Architecture

![active_active_architecture](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/active_active_architecture.svg)

---
## Active-Passive Architecture

![active_passive_architecture](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/active_passive_architecture.svg)

---
## Fault Tolerance Principles

- Assume every component can and will fail
- Detect failures quickly through health checks and monitoring
- Isolate failures to prevent cascading across the system
- Recover automatically without human intervention when possible

---
## Failure Detection

- Heartbeat mechanisms between nodes
- Health check endpoints probed by load balancers
- Timeouts that trigger failover after a threshold
- Gossip protocols for peer-to-peer failure detection

---
## Failover Strategies

- DNS failover: update DNS records to point to healthy nodes
- Load balancer failover: remove unhealthy nodes from rotation
- Database failover: promote a replica to primary
- Application-level failover: retry on a different service instance

---
## Data Replication

- Synchronous replication: write is acknowledged only after all replicas confirm
    - Strong consistency but higher latency
- Asynchronous replication: write is acknowledged after primary confirms
    - Lower latency but risk of data loss on primary failure
- Semi-synchronous: primary waits for at least one replica to confirm

---
## Replication Topologies

![replication_topologies](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/replication_topologies.svg)

---
## Consensus Algorithms

- Enable multiple nodes to agree on a single value
- Essential for leader election and distributed state machines
- Examples: `Paxos`, `Raft`, `Zab`
- Trade availability for correctness during partitions

---
## Raft Consensus Overview

![raft_consensus_overview](svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/raft_consensus_overview.svg)

---
## Raft Consensus Details

- Leader handles all writes
- Majority acknowledgment required for commit
- New leader elected if current leader fails

---
## Quorum-Based Systems

- A quorum is the minimum number of nodes that must agree
- Write quorum (W) + Read quorum (R) > Total nodes (N) ensures consistency
- Common configuration: N=3, W=2, R=2
- Tuning W and R trades consistency for latency

---
## Idempotency

- An operation that produces the same result when applied multiple times
- Essential for safe retries in unreliable networks
- Assign unique IDs to requests and deduplicate on the server
- `GET`, `PUT`, and `DELETE` are naturally idempotent; `POST` is not

---
## Designing for Partial Failure

- Not all components fail at once; handle degraded states gracefully
- Use circuit breakers to stop cascading failures
- Provide fallback responses when a dependency is unavailable
- Communicate degraded state to users rather than failing silently

---
## Summary

- The `CAP` theorem forces a choice between consistency and availability during partitions
- The `PACELC` theorem extends this to normal operation trade-offs
- The eight fallacies of distributed computing warn against common assumptions
- High availability requires redundancy, failover, and automated recovery
- Consensus algorithms enable coordination but add complexity
- Design every component with the expectation that it will fail

---

## FLP Impossibility

Fischer, Lynch, Paterson (1985):

> No deterministic algorithm can guarantee consensus in an asynchronous system with even one faulty process.

Implications:

- Perfect consensus is impossible in a truly asynchronous model
- Real systems must relax requirements (e.g., use timeouts, partial synchrony)
- Raft and Paxos assume eventual synchrony to make progress

---

## Logical Clocks (Lamport)

Physical clocks disagree; logical clocks give a consistent *partial order* of events:

- Each process has a counter; increment before every local event
- On send, attach counter value to the message
- On receive, set counter to `max(local, received) + 1`

Captures "happens-before" but not concurrency — two unrelated events may have equal timestamps with no causal link.

---

## Vector Clocks

Track causality across *all* nodes. Each process holds a vector `V[i]` of counters, one per node:

- On local event, increment your own slot
- On send, include the full vector
- On receive, element-wise max, then increment own slot

Two events `A` and `B` are concurrent iff `V(A) < V(B)` is false AND `V(B) < V(A)` is false. Used in Dynamo, Riak, version vectors for conflict detection.

---

## Byzantine Fault Tolerance

Crash faults: a node stops. Byzantine faults: a node lies, sends contradicting messages, or is malicious.

- Classical BFT protocols (PBFT) tolerate `f` faults with `3f + 1` total nodes
- Expensive: many message rounds, cryptographic signatures
- Modern use cases: blockchains, financial systems, safety-critical control

Most traditional distributed systems (ZooKeeper, etcd, Cassandra) assume crash-only faults — not Byzantine.

---

## Gossip Protocols

Epidemic-style information spread:

- Each node periodically picks a random peer and exchanges state
- Information propagates exponentially until everyone converges
- Robust to partitions and churn; no single coordinator

Used for: failure detection (SWIM, Cassandra), membership (Consul, Serf), CRDT replication.

---

## Saga Pattern

Long-running distributed transactions implemented as a series of local transactions plus compensations:

1. 1. Step 1: book flight → compensation: cancel flight
1. 1. Step 2: book hotel → compensation: cancel hotel
1. 1. Step 3: charge card → compensation: refund

If any step fails, compensations run in reverse for all completed steps. Two styles:

- **Choreography** — services emit events; each service reacts
- **Orchestration** — a central coordinator drives the saga

No ACID across services — only eventual consistency with explicit compensation.

---

## Split-Brain Problem

A network partition leaves two groups of nodes each believing it is the primary:

- Both accept writes, diverging from each other
- On heal, reconciliation is required — possibly with data loss

Mitigations:

- **Majority quorum** — only the partition with >50% of nodes stays active
- **Fencing tokens** — monotonically increasing tokens; storage rejects older tokens
- **STONITH** / dedicated arbiter nodes in clustering systems

---

## Circuit Breaker Pattern

Prevents cascading failures when a downstream service is struggling:

1. 1. **Closed** — requests pass through; count failures
1. 1. **Open** — once failures exceed threshold, fail fast without calling the downstream service
1. 1. **Half-Open** — after a timeout, let a trickle of requests through; if they succeed, close again

Libraries: Resilience4j (Java), Polly (.NET), Hystrix (deprecated but influential). Prevents the thundering-herd retry storm that often kills already-overloaded services.

---

## Backpressure and Rate Limiting

When producers outrun consumers, you need explicit flow control.

**Backpressure** — consumer signals "slow down" upstream:

- TCP's sliding window is backpressure at the transport layer
- Reactive Streams (`Flow.Subscriber`), RxJava, akka-streams provide it in-process

**Rate limiting** — cap incoming request rate to protect a service:

- **Token bucket** — refills at a fixed rate, bursty up to bucket size
- **Leaky bucket** — constant output rate, smooths bursts
- **Sliding window / fixed window** — count requests over a time interval

---

## Observability: Logs, Metrics, Traces

Three pillars, distinct use cases:

- **Logs** — discrete events with full context (ELK, Loki). Great for forensics.
- **Metrics** — aggregated numeric time-series (Prometheus). Great for dashboards and alerts.
- **Traces** — request-spanning timelines across services (Jaeger, Zipkin, OpenTelemetry). Great for latency root-cause and dependency mapping.

A distributed trace needs a **trace ID** and **span IDs** propagated through every inter-service call. Context propagation is usually via HTTP headers (W3C Trace Context).

---

## Chaos Engineering

Deliberately inject failures into production (or production-like) systems to build confidence:

- **Network partitions** — drop packets between services
- **Node crashes** — kill random instances
- **Latency injection** — add delays to dependency calls
- **Resource exhaustion** — fill disks, saturate CPU
- **Clock skew** — offset node clocks

Tools: Chaos Monkey (Netflix), Gremlin, LitmusChaos, `tc`-based shapers.

Principle: find failures in controlled chaos before they find you in uncontrolled chaos.
