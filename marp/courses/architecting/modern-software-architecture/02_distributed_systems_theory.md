# Distributed Systems Theory

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---
## What Is a Distributed System?

- A collection of independent computers that appear as a single system to users
- Components communicate and coordinate actions by passing messages
- No shared memory or clock between nodes
- Examples: cloud applications, microservices, databases clusters

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

![cap_theorem_diagram](../../../../svg/courses/architecting/modern-software-architecture/02_distributed_systems_theory/cap_theorem_diagram.svg)

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

- An extension of CAP that addresses normal operation
- If there is a Partition: choose Availability or Consistency
- Else (normal operation): choose Latency or Consistency
- Captures the trade-off that exists even without partitions

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

<div class="mermaid">
graph LR
    A[Strong Consistency] --> B[Sequential Consistency]
    B --> C[Causal Consistency]
    C --> D[Read-Your-Writes]
    D --> E[Eventual Consistency]
    style A fill:#e74c3c,color:white
    style E fill:#27ae60,color:white
</div>

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

<div class="mermaid">
graph TD
    LB[Load Balancer] --> N1[Node 1 - Active]
    LB --> N2[Node 2 - Active]
    LB --> N3[Node 3 - Active]
    N1 --> DB1[(DB Primary)]
    N2 --> DB1
    N3 --> DB1
    DB1 -->|Replication| DB2[(DB Replica)]
</div>

---
## Active-Passive Architecture

<div class="mermaid">
graph TD
    LB[Load Balancer] --> N1[Node 1 - Active]
    N2[Node 2 - Standby]
    N1 --> DB1[(DB Primary)]
    DB1 -->|Replication| DB2[(DB Standby)]
    N1 -.->|Heartbeat| N2
    N2 -.->|Failover| LB
</div>

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

<div class="mermaid">
graph TD
    subgraph Single Leader
        P1[Primary] --> R1[Replica 1]
        P1 --> R2[Replica 2]
    end
    subgraph Multi Leader
        L1[Leader 1] <--> L2[Leader 2]
        L1 --> R3[Replica]
        L2 --> R4[Replica]
    end
</div>

---
## Consensus Algorithms

- Enable multiple nodes to agree on a single value
- Essential for leader election and distributed state machines
- Examples: `Paxos`, `Raft`, `Zab`
- Trade availability for correctness during partitions

---
## Raft Consensus Overview

<div class="mermaid">
graph TD
    L[Leader] -->|AppendEntries| F1[Follower 1]
    L -->|AppendEntries| F2[Follower 2]
    L -->|AppendEntries| F3[Follower 3]
    L -->|AppendEntries| F4[Follower 4]
    F1 -->|Acknowledge| L
    F2 -->|Acknowledge| L
    F3 -->|Acknowledge| L
    F4 -->|Acknowledge| L
</div>

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
