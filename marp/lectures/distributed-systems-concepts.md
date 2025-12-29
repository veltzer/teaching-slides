# Distributed Systems Concepts

---

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="250" y="50" width="100" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="450" y="50" width="100" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="85" text-anchor="middle" font-size="12">Node A</text>
  <text x="300" y="85" text-anchor="middle" font-size="12">Node B</text>
  <text x="500" y="85" text-anchor="middle" font-size="12">Node C</text>
  <line x1="150" y1="80" x2="250" y2="80" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,5"/>
  <line x1="350" y1="80" x2="450" y2="80" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="300" y="150" text-anchor="middle" font-size="14" font-weight="bold">Networks are unreliable</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="12">Sender</text>
  <text x="450" y="105" text-anchor="middle" font-size="12">Receiver</text>
  <path d="M 190 100 L 290 100" stroke="#51cf66" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 310 100 L 410 100" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="300" y="90" text-anchor="middle" font-size="10">Message</text>
  <text x="300" y="130" text-anchor="middle" font-size="11">✓ Sent</text>
  <text x="300" y="145" text-anchor="middle" font-size="11">✗ Lost</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#51cf66"/>
    </marker>
  </defs>
</svg>

Messages can be lost, duplicated, or reordered

---

## Fallacy 2: Latency Is Zero

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="100" y="50" font-size="12">Local Call:</text>
  <rect x="100" y="60" width="50" height="20" fill="#51cf66"/>
  <text x="100" y="100" font-size="12">Network Call:</text>
  <rect x="100" y="110" width="400" height="20" fill="#ff6b6b"/>
  <text x="300" y="160" text-anchor="middle" font-size="11">~0.0001ms vs ~100ms</text>
  <text x="300" y="180" text-anchor="middle" font-size="11">Million times slower!</text>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="100" r="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="40" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <circle cx="225" cy="200" r="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="11">OK</text>
  <text x="300" y="105" text-anchor="middle" font-size="11">OK</text>
  <text x="450" y="105" text-anchor="middle" font-size="11">Failed</text>
  <text x="225" y="205" text-anchor="middle" font-size="11">OK</text>
  <text x="300" y="30" text-anchor="middle" font-size="14" font-weight="bold">System partially operational</text>
</svg>

---

## Time and Ordering

In distributed systems, there's no global clock

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <line x1="100" y1="50" x2="100" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#333" stroke-width="2"/>
  <circle cx="100" cy="80" r="5" fill="#ff6b6b"/>
  <circle cx="300" cy="100" r="5" fill="#51cf66"/>
  <circle cx="500" cy="70" r="5" fill="#4c9aff"/>
  <text x="100" y="40" text-anchor="middle" font-size="11">Node A</text>
  <text x="300" y="40" text-anchor="middle" font-size="11">Node B</text>
  <text x="500" y="40" text-anchor="middle" font-size="11">Node C</text>
  <text x="50" y="80" font-size="10">Event 1</text>
  <text x="250" y="100" font-size="10">Event 2</text>
  <text x="450" y="70" font-size="10">Event 3</text>
  <text x="300" y="180" text-anchor="middle" font-size="12">Which happened first?</text>
</svg>

---

## Logical Clocks

Lamport timestamps establish partial ordering:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <line x1="100" y1="50" x2="100" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="50" x2="400" y2="150" stroke="#333" stroke-width="2"/>
  <circle cx="100" cy="70" r="5" fill="#ff6b6b"/>
  <circle cx="100" cy="110" r="5" fill="#ff6b6b"/>
  <circle cx="400" cy="90" r="5" fill="#4c9aff"/>
  <circle cx="400" cy="130" r="5" fill="#4c9aff"/>
  <path d="M 105 75 Q 250 80 395 90" stroke="#333" stroke-width="1" marker-end="url(#arrow2)"/>
  <path d="M 405 135 Q 250 140 105 115" stroke="#333" stroke-width="1" marker-end="url(#arrow2)"/>
  <text x="50" y="70" font-size="10">T:1</text>
  <text x="50" y="110" font-size="10">T:4</text>
  <text x="450" y="90" font-size="10">T:2</text>
  <text x="450" y="130" font-size="10">T:3</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Vector Clocks

Track causality across all nodes:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="100" y="50" font-size="12">Node A: [1,0,0]</text>
  <text x="100" y="80" font-size="12">Node A: [2,0,0]</text>
  <text x="100" y="110" font-size="12">Node A: [3,1,0]</text>
  <text x="300" y="50" font-size="12">Node B: [0,1,0]</text>
  <text x="300" y="80" font-size="12">Node B: [2,2,0]</text>
  <text x="300" y="110" font-size="12">Node B: [2,3,0]</text>
  <text x="300" y="150" text-anchor="middle" font-size="11">Can determine: concurrent vs causal</text>
</svg>

---

## Consensus Problem

Getting distributed nodes to agree on a value

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="100" r="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="150" y="100" text-anchor="middle" font-size="11">Value: ?</text>
  <text x="300" y="100" text-anchor="middle" font-size="11">Value: ?</text>
  <text x="450" y="100" text-anchor="middle" font-size="11">Value: ?</text>
  <text x="300" y="160" text-anchor="middle" font-size="14" font-weight="bold">Must agree on same value</text>
  <text x="300" y="180" text-anchor="middle" font-size="11">Even with failures!</text>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="30" width="100" height="60" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <rect x="100" y="150" width="100" height="60" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <rect x="250" y="150" width="100" height="60" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <rect x="400" y="150" width="100" height="60" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <text x="300" y="65" text-anchor="middle" font-size="12">Leader</text>
  <text x="150" y="185" text-anchor="middle" font-size="12">Follower</text>
  <text x="300" y="185" text-anchor="middle" font-size="12">Follower</text>
  <text x="450" y="185" text-anchor="middle" font-size="12">Follower</text>
  <line x1="300" y1="90" x2="150" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="300" y1="90" x2="300" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="300" y1="90" x2="450" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Byzantine Fault Tolerance

When nodes can be malicious:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="100" r="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="40" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="11">Honest</text>
  <text x="300" y="105" text-anchor="middle" font-size="11">Honest</text>
  <text x="450" y="105" text-anchor="middle" font-size="11">Byzantine</text>
  <text x="300" y="150" text-anchor="middle" font-size="12">Need 3f+1 nodes to tolerate f failures</text>
</svg>

---

## Replication Strategies

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="175" y="75" text-anchor="middle" font-size="12">Primary</text>
  <rect x="50" y="130" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <rect x="170" y="130" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <rect x="290" y="130" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="100" y="155" text-anchor="middle" font-size="11">Replica 1</text>
  <text x="220" y="155" text-anchor="middle" font-size="11">Replica 2</text>
  <text x="340" y="155" text-anchor="middle" font-size="11">Replica 3</text>
  <text x="220" y="200" text-anchor="middle" font-size="11">Synchronous or Asynchronous?</text>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="30" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="100" r="30" fill="#ffd43b" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="30" fill="#e0e0e0" stroke="#333" stroke-width="2"/>
  <circle cx="150" cy="200" r="30" fill="#e0e0e0" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="200" r="30" fill="#e0e0e0" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="200" r="30" fill="#e0e0e0" stroke="#333" stroke-width="2"/>
  <path d="M 180 100 L 270 100" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <path d="M 330 100 L 420 100" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="300" y="30" text-anchor="middle" font-size="12">Information spreads exponentially</text>
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Eventual Consistency

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <line x1="50" y1="100" x2="550" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <text x="300" y="90" text-anchor="middle" font-size="12">Time</text>
  <rect x="100" y="120" width="60" height="30" fill="#ff6b6b" stroke="#333" stroke-width="1"/>
  <rect x="180" y="120" width="60" height="30" fill="#ffd43b" stroke="#333" stroke-width="1"/>
  <rect x="260" y="120" width="60" height="30" fill="#51cf66" stroke="#333" stroke-width="1"/>
  <rect x="340" y="120" width="60" height="30" fill="#51cf66" stroke="#333" stroke-width="1"/>
  <rect x="420" y="120" width="60" height="30" fill="#51cf66" stroke="#333" stroke-width="1"/>
  <text x="130" y="140" text-anchor="middle" font-size="10">Inconsistent</text>
  <text x="450" y="140" text-anchor="middle" font-size="10">Converged</text>
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Quorum Systems

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="30" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <circle cx="250" cy="100" r="30" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <circle cx="350" cy="100" r="30" fill="#e0e0e0" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="30" fill="#e0e0e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="50" text-anchor="middle" font-size="12">N=4, W=2, R=3</text>
  <text x="300" y="150" text-anchor="middle" font-size="11">W + R > N ensures consistency</text>
  <text x="300" y="170" text-anchor="middle" font-size="11">2 + 3 > 4 ✓</text>
</svg>

---

## Split Brain Problem

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="180" cy="125" rx="100" ry="80" fill="#ffe0e0" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,5"/>
  <ellipse cx="420" cy="125" rx="100" ry="80" fill="#e0e0ff" stroke="#4c9aff" stroke-width="2" stroke-dasharray="5,5"/>
  <circle cx="150" cy="100" r="25" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <circle cx="210" cy="150" r="25" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <circle cx="390" cy="100" r="25" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="150" r="25" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <text x="180" y="220" text-anchor="middle" font-size="11">Partition A</text>
  <text x="420" y="220" text-anchor="middle" font-size="11">Partition B</text>
  <text x="300" y="30" text-anchor="middle" font-size="14" font-weight="bold">Both think they're primary!</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="100" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="250" y="50" width="100" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="400" y="50" width="100" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="150" y="85" text-anchor="middle" font-size="11">Service A</text>
  <text x="300" y="85" text-anchor="middle" font-size="11">Service B</text>
  <text x="450" y="85" text-anchor="middle" font-size="11">Service C</text>
  <text x="300" y="140" text-anchor="middle" font-size="12">All must commit or all must abort</text>
</svg>

---

## Saga Pattern

Long-running transactions as series of local transactions:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="80" width="80" height="40" fill="#51cf66" stroke="#333" stroke-width="1"/>
  <rect x="150" y="80" width="80" height="40" fill="#51cf66" stroke="#333" stroke-width="1"/>
  <rect x="250" y="80" width="80" height="40" fill="#ff6b6b" stroke="#333" stroke-width="1"/>
  <rect x="350" y="80" width="80" height="40" fill="#ffd43b" stroke="#333" stroke-width="1"/>
  <rect x="450" y="80" width="80" height="40" fill="#ffd43b" stroke="#333" stroke-width="1"/>
  <text x="90" y="103" text-anchor="middle" font-size="10">T1</text>
  <text x="190" y="103" text-anchor="middle" font-size="10">T2</text>
  <text x="290" y="103" text-anchor="middle" font-size="10">T3 fail</text>
  <text x="390" y="103" text-anchor="middle" font-size="10">C2</text>
  <text x="490" y="103" text-anchor="middle" font-size="10">C1</text>
  <text x="290" y="150" text-anchor="middle" font-size="11">Forward recovery or compensating transactions</text>
</svg>

---

## Idempotency

Operations that can be applied multiple times:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <text x="175" y="75" text-anchor="middle" font-size="12">SET X = 5</text>
  <text x="175" y="110" text-anchor="middle" font-size="11">✓ Idempotent</text>
  <rect x="350" y="50" width="150" height="40" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <text x="425" y="75" text-anchor="middle" font-size="12">X = X + 1</text>
  <text x="425" y="110" text-anchor="middle" font-size="11">✗ Not idempotent</text>
  <text x="300" y="150" text-anchor="middle" font-size="11">Critical for handling retries</text>
</svg>

---

## Distributed Caching

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="100" width="80" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="200" y="50" width="80" height="40" fill="#ffd43b" stroke="#333" stroke-width="1"/>
  <rect x="200" y="110" width="80" height="40" fill="#ffd43b" stroke="#333" stroke-width="1"/>
  <rect x="200" y="170" width="80" height="40" fill="#ffd43b" stroke="#333" stroke-width="1"/>
  <rect x="350" y="100" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="90" y="130" text-anchor="middle" font-size="11">Client</text>
  <text x="240" y="75" text-anchor="middle" font-size="10">Cache 1</text>
  <text x="240" y="135" text-anchor="middle" font-size="10">Cache 2</text>
  <text x="240" y="195" text-anchor="middle" font-size="10">Cache 3</text>
  <text x="400" y="130" text-anchor="middle" font-size="11">Database</text>
  <line x1="130" y1="125" x2="200" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="280" y1="125" x2="350" y2="125" stroke="#333" stroke-width="2" stroke-dasharray="5,5"/>
</svg>

Cache invalidation is hard!

---

## Load Balancing Strategies

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="30" width="100" height="40" fill="#333" stroke="#333" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-size="12" fill="white">LB</text>
  <rect x="100" y="120" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="210" y="120" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="320" y="120" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="430" y="120" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="140" y="145" text-anchor="middle" font-size="10">Server 1</text>
  <text x="250" y="145" text-anchor="middle" font-size="10">Server 2</text>
  <text x="360" y="145" text-anchor="middle" font-size="10">Server 3</text>
  <text x="470" y="145" text-anchor="middle" font-size="10">Server 4</text>
  <text x="300" y="190" text-anchor="middle" font-size="11">Round-robin, Least connections, Consistent hashing</text>
</svg>

---

## Service Discovery

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="30" width="100" height="50" fill="#ffd43b" stroke="#333" stroke-width="2"/>
  <text x="300" y="60" text-anchor="middle" font-size="12">Registry</text>
  <rect x="100" y="150" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="420" y="150" width="80" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="140" y="175" text-anchor="middle" font-size="11">Service A</text>
  <text x="460" y="175" text-anchor="middle" font-size="11">Service B</text>
  <path d="M 140 150 L 280 80" stroke="#51cf66" stroke-width="2" marker-end="url(#arrow6)"/>
  <path d="M 140 170 L 320 80" stroke="#ff6b6b" stroke-width="2" marker-end="url(#arrow6)" stroke-dasharray="5,5"/>
  <text x="80" y="130" font-size="10">Register</text>
  <text x="80" y="210" font-size="10">Discover</text>
  <defs>
    <marker id="arrow6" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#51cf66"/>
    </marker>
  </defs>
</svg>

---

## Circuit Breaker Pattern

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="100" r="40" fill="#ffd43b" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="40" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="11">Closed</text>
  <text x="300" y="105" text-anchor="middle" font-size="11">Half-Open</text>
  <text x="450" y="105" text-anchor="middle" font-size="11">Open</text>
  <path d="M 190 100 L 260 100" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <path d="M 340 100 L 410 100" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <text x="225" y="90" font-size="9">Failures</text>
  <text x="375" y="90" font-size="9">Timeout</text>
  <defs>
    <marker id="arrow7" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Prevent cascading failures

---

## Backpressure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="80" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="250" y="60" width="100" height="80" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <rect x="450" y="80" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="100" y="105" text-anchor="middle" font-size="11">Producer</text>
  <text x="300" y="105" text-anchor="middle" font-size="11">Queue Full</text>
  <text x="500" y="105" text-anchor="middle" font-size="11">Consumer</text>
  <path d="M 150 100 L 250 100" stroke="#333" stroke-width="3"/>
  <path d="M 350 100 L 450 100" stroke="#333" stroke-width="1"/>
  <path d="M 250 90 L 150 90" stroke="#ff6b6b" stroke-width="2" marker-end="url(#arrow8)" stroke-dasharray="5,5"/>
  <text x="200" y="80" text-anchor="middle" font-size="10">Slow down!</text>
  <defs>
    <marker id="arrow8" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#ff6b6b"/>
    </marker>
  </defs>
</svg>

---

## Rate Limiting

Control request flow:

- **Token Bucket** - Fixed capacity, refills at constant rate
- **Leaky Bucket** - Smooth output rate
- **Sliding Window** - Track requests in time window
- **Fixed Window** - Reset counter at intervals

---

## Distributed Tracing

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="500" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="100" y="100" width="200" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <rect x="150" y="140" width="100" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="350" y="100" width="150" height="25" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="300" y="70" text-anchor="middle" font-size="11">Request Trace</text>
  <text x="200" y="117" text-anchor="middle" font-size="10">Service A</text>
  <text x="200" y="157" text-anchor="middle" font-size="10">DB Query</text>
  <text x="425" y="117" text-anchor="middle" font-size="10">Service B</text>
  <text x="300" y="200" text-anchor="middle" font-size="11">Trace ID: abc-123</text>
</svg>

---

## Observability Pillars

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="60" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="100" r="60" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="60" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="12">Logs</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Metrics</text>
  <text x="450" y="105" text-anchor="middle" font-size="12">Traces</text>
  <text x="300" y="180" text-anchor="middle" font-size="11">Complete system visibility</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <line x1="100" y1="150" x2="500" y2="50" stroke="#ff6b6b" stroke-width="2"/>
  <line x1="100" y1="50" x2="500" y2="150" stroke="#51cf66" stroke-width="2"/>
  <text x="100" y="40" font-size="12">Consistency</text>
  <text x="420" y="40" font-size="12">Availability</text>
  <text x="100" y="170" font-size="12">Latency</text>
  <text x="420" y="170" font-size="12">Throughput</text>
  <text x="300" y="190" text-anchor="middle" font-size="11">You can't have everything</text>
</svg>

---

## Key Takeaways

- Embrace failure as normal
- No global state or time
- Consensus is expensive
- Eventual consistency is often enough
- Design for partition tolerance
- Monitor and trace everything
