# NoSQL Databases Fundamentals

---

## What Are NoSQL Databases?

- Not Only SQL databases
- Designed for specific data models
- Flexible schemas or schema-less
- Horizontally scalable by design
- Optimized for specific access patterns

---

## Why NoSQL Emerged

- Massive data volumes (Big Data)
- Need for horizontal scaling
- Flexible, evolving data structures
- High-performance requirements
- Geographic distribution needs

---

## The Fundamental Shift

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="200" height="150" fill="#e3f2fd" stroke="#2196f3" stroke-width="2"/>
  <rect x="350" y="50" width="200" height="150" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="150" y="30" text-anchor="middle" font-size="14" font-weight="bold">RDBMS</text>
  <text x="450" y="30" text-anchor="middle" font-size="14" font-weight="bold">NoSQL</text>
  <text x="150" y="100" text-anchor="middle" font-size="12">ACID</text>
  <text x="150" y="120" text-anchor="middle" font-size="12">Vertical Scaling</text>
  <text x="150" y="140" text-anchor="middle" font-size="12">Fixed Schema</text>
  <text x="450" y="100" text-anchor="middle" font-size="12">BASE</text>
  <text x="450" y="120" text-anchor="middle" font-size="12">Horizontal Scaling</text>
  <text x="450" y="140" text-anchor="middle" font-size="12">Flexible Schema</text>
</svg>

---

## Core NoSQL Categories

1. Document Stores
1. Key-Value Stores
1. Column-Family Stores
1. Graph Databases

---

## Document Stores: Core Concepts

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="400" height="120" fill="#fff" stroke="#333" stroke-width="2"/>
  <text x="300" y="80" text-anchor="middle" font-size="14" font-weight="bold">Document</text>
  <text x="120" y="110" font-size="12">{ "id": "123",</text>
  <text x="120" y="130" font-size="12">  "name": "John",</text>
  <text x="120" y="150" font-size="12">  "address": { "city": "NYC" } }</text>
</svg>

Self-contained data units with nested structures

---

## Document Stores: How They Work

- Store data as documents (JSON, BSON, XML)
- Each document has unique identifier
- Documents can contain nested structures
- No predefined schema required
- Query by document contents

---

## Document Stores: Storage Strategy

- Documents grouped in collections
- Collections analogous to tables
- But no enforced structure
- Indexes on any field
- Secondary indexes supported

---

## Key-Value Stores: Core Model

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="40" fill="#ffd43b" stroke="#333" stroke-width="2"/>
  <rect x="350" y="50" width="150" height="40" fill="#51cf66" stroke="#333" stroke-width="2"/>
  <text x="175" y="75" text-anchor="middle" font-size="14">Key: "user:123"</text>
  <text x="425" y="75" text-anchor="middle" font-size="14">Value: {data}</text>
  <line x1="250" y1="70" x2="350" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Simplest NoSQL model - pure associative arrays

---

## Key-Value Stores: Operations

Basic operations:
- `PUT(key, value)` - Store value
- `GET(key)` - Retrieve value
- `DELETE(key)` - Remove value

That's essentially it - simplicity is the strength

---

## Key-Value: Distribution Strategy

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="13" font-weight="bold">Key-Value Distribution via Consistent Hashing</text>
  <rect x="30" y="30" width="100" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="3"/>
  <text x="80" y="47" text-anchor="middle" font-size="10" font-weight="bold">Hash(key)</text>
  <text x="80" y="62" text-anchor="middle" font-size="9" fill="#666">0 - 2^32</text>
  <line x1="130" y1="50" x2="160" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowkv)"/>
  <rect x="160" y="30" width="100" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="3"/>
  <text x="210" y="47" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">Partition A</text>
  <text x="210" y="62" text-anchor="middle" font-size="9" fill="#666">Keys 0-99</text>
  <rect x="280" y="30" width="100" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="3"/>
  <text x="330" y="47" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">Partition B</text>
  <text x="330" y="62" text-anchor="middle" font-size="9" fill="#666">Keys 100-199</text>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="3"/>
  <text x="450" y="47" text-anchor="middle" font-size="10" font-weight="bold" fill="#7b1fa2">Partition C</text>
  <text x="450" y="62" text-anchor="middle" font-size="9" fill="#666">Keys 200-299</text>
  <rect x="520" y="30" width="60" height="40" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="550" y="55" text-anchor="middle" font-size="9">...</text>
  <rect x="160" y="90" width="100" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="210" y="112" text-anchor="middle" font-size="10">Server 1</text>
  <rect x="280" y="90" width="100" height="35" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="330" y="112" text-anchor="middle" font-size="10">Server 2</text>
  <rect x="400" y="90" width="100" height="35" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="3"/>
  <text x="450" y="112" text-anchor="middle" font-size="10">Server 3</text>
  <line x1="210" y1="70" x2="210" y2="88" stroke="#2e7d32" stroke-width="1.5"/>
  <line x1="330" y1="70" x2="330" y2="88" stroke="#e65100" stroke-width="1.5"/>
  <line x1="450" y1="70" x2="450" y2="88" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="300" y="150" text-anchor="middle" font-size="10" fill="#666">Adding/removing a server only remaps nearby keys</text>
  <rect x="120" y="160" width="360" height="30" fill="#e3f2fd" stroke="#1565c0" stroke-width="1" rx="3"/>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#1565c0">Minimal redistribution = high availability during scaling</text>
  <defs>
    <marker id="arrowkv" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Column-Family Stores: Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="150" y="50" width="120" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <rect x="270" y="50" width="120" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <rect x="390" y="50" width="120" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="100" y="70" text-anchor="middle" font-size="12">Row Key</text>
  <text x="210" y="70" text-anchor="middle" font-size="12">Col Family 1</text>
  <text x="330" y="70" text-anchor="middle" font-size="12">Col Family 2</text>
  <text x="450" y="70" text-anchor="middle" font-size="12">Col Family 3</text>
  <rect x="50" y="80" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="150" y="80" width="120" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <rect x="270" y="80" width="120" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="100" y="100" text-anchor="middle" font-size="11">user:001</text>
</svg>

---

## Column-Family: How It Works

- Data stored in column families
- Each row has a unique row key
- Columns grouped into families
- Sparse storage - only store what exists
- Optimized for write-heavy workloads

---

## Graph Databases: Core Model

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="100" r="30" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="100" r="30" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <circle cx="450" cy="100" r="30" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <circle cx="225" cy="200" r="30" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <line x1="180" y1="100" x2="270" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="330" y1="100" x2="420" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="165" y1="125" x2="210" y2="175" stroke="#333" stroke-width="2"/>
  <line x1="240" y1="175" x2="285" y2="125" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="12">Node</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node</text>
  <text x="450" y="105" text-anchor="middle" font-size="12">Node</text>
  <text x="225" y="205" text-anchor="middle" font-size="12">Node</text>
  <text x="225" y="85" text-anchor="middle" font-size="10">Edge</text>
</svg>

---

## Graph Databases: Operations

- Store nodes (entities)
- Store edges (relationships)
- Properties on both nodes and edges
- Traverse relationships efficiently
- Pattern matching queries

---

## The CAP Theorem

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <circle cx="200" cy="150" r="120" fill="#ff6b6b" opacity="0.3" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="150" r="120" fill="#51cf66" opacity="0.3" stroke="#333" stroke-width="2"/>
  <circle cx="250" cy="230" r="120" fill="#4c9aff" opacity="0.3" stroke="#333" stroke-width="2"/>
  <text x="200" y="100" text-anchor="middle" font-size="14" font-weight="bold">Consistency</text>
  <text x="300" y="100" text-anchor="middle" font-size="14" font-weight="bold">Availability</text>
  <text x="250" y="290" text-anchor="middle" font-size="14" font-weight="bold">Partition Tolerance</text>
</svg>

Pick two (but you must pick P in distributed systems)

---

## CAP: Consistency

All nodes see the same data at the same time

- Every read receives the most recent write
- Or returns an error
- Linearizability guarantee
- Strong consistency model

---

## CAP: Availability

System remains operational

- Every request receives a response
- No error due to system state
- May not contain most recent write
- System stays up despite failures

---

## CAP: Partition Tolerance

System continues despite network failures

- Network can lose messages
- Nodes can be isolated
- Split-brain scenarios
- Must handle network partitions

---

## Why You Must Choose P

In distributed systems:
- Networks fail (it's not if, it's when)
- Partitions are inevitable
- Can't sacrifice P in practice
- Real choice is between C and A

---

## CP Systems

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="400" height="100" fill="#ffe0e0" stroke="#ff6b6b" stroke-width="2"/>
  <text x="300" y="90" text-anchor="middle" font-size="14" font-weight="bold">Consistency + Partition Tolerance</text>
  <text x="300" y="120" text-anchor="middle" font-size="12">May refuse requests to maintain consistency</text>
</svg>

Example behaviors: Banking systems, inventory management

---

## AP Systems

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="400" height="100" fill="#e0ffe0" stroke="#51cf66" stroke-width="2"/>
  <text x="300" y="90" text-anchor="middle" font-size="14" font-weight="bold">Availability + Partition Tolerance</text>
  <text x="300" y="120" text-anchor="middle" font-size="12">Always responds, may serve stale data</text>
</svg>

Example behaviors: Social media feeds, caching systems

---

## Consistency Models Spectrum

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="500" height="40" fill="linear-gradient(to right, #ff6b6b, #51cf66)" stroke="#333" stroke-width="2"/>
  <text x="50" y="110" text-anchor="start" font-size="12">Strong</text>
  <text x="300" y="110" text-anchor="middle" font-size="12">Eventual</text>
  <text x="550" y="110" text-anchor="end" font-size="12">Weak</text>
  <text x="300" y="30" text-anchor="middle" font-size="14" font-weight="bold">Consistency Guarantees</text>
</svg>

---

## Strong Consistency

- All nodes agree on data order
- Synchronous replication
- Higher latency
- Lower availability
- Easier to reason about

---

## Eventual Consistency

- Nodes will eventually converge
- Asynchronous replication
- Lower latency
- Higher availability
- Requires conflict resolution

---

## Weak Consistency

- No guarantees about convergence
- Best effort delivery
- Lowest latency
- Highest availability
- Application handles inconsistency

---

## BASE Properties

Alternative to ACID for distributed systems:

- Basically Available
- Soft state
- Eventual consistency

---

## Basically Available

- System appears to work most of the time
- Partial failures allowed
- Degraded performance acceptable
- Some data might be unavailable

---

## Soft State

- Data may change without input
- System state evolves over time
- Replicas may diverge temporarily
- No guaranteed consistency

---

## Eventual Consistency Details

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <line x1="100" y1="50" x2="100" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#333" stroke-width="2"/>
  <circle cx="100" cy="80" r="5" fill="#ff6b6b"/>
  <circle cx="300" cy="100" r="5" fill="#ff6b6b"/>
  <circle cx="500" cy="120" r="5" fill="#ff6b6b"/>
  <text x="100" y="40" text-anchor="middle" font-size="12">Node A</text>
  <text x="300" y="40" text-anchor="middle" font-size="12">Node B</text>
  <text x="500" y="40" text-anchor="middle" font-size="12">Node C</text>
  <text x="300" y="180" text-anchor="middle" font-size="12">Updates propagate asynchronously</text>
</svg>

---

## Replication Strategies

**Single-Master Replication:**
- One node handles writes
- Replicas handle reads
- Simple consistency model

**Multi-Master Replication:**
- Any node can handle writes
- Conflict resolution required
- Higher availability

---

## Conflict Resolution

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="60" fill="#ffe0e0" stroke="#333" stroke-width="2"/>
  <rect x="350" y="50" width="150" height="60" fill="#e0e0ff" stroke="#333" stroke-width="2"/>
  <text x="175" y="85" text-anchor="middle" font-size="12">Write A: X=5</text>
  <text x="425" y="85" text-anchor="middle" font-size="12">Write B: X=7</text>
  <text x="300" y="150" text-anchor="middle" font-size="14" font-weight="bold">Conflict!</text>
  <text x="300" y="180" text-anchor="middle" font-size="12">Resolution Strategies:</text>
  <text x="300" y="200" text-anchor="middle" font-size="11">Last-Write-Wins | Version Vectors | CRDTs</text>
</svg>

---

## Sharding (Partitioning)

Splitting data across multiple nodes:

- Horizontal partitioning
- Each shard holds subset of data
- Distribution by key range or hash
- Enables horizontal scaling

---

## Sharding Strategies

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="225" y="50" width="150" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="400" y="50" width="150" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="125" y="75" text-anchor="middle" font-size="12">A-H</text>
  <text x="300" y="75" text-anchor="middle" font-size="12">I-P</text>
  <text x="475" y="75" text-anchor="middle" font-size="12">Q-Z</text>
  <text x="300" y="120" text-anchor="middle" font-size="12" font-weight="bold">Range Sharding</text>
  <rect x="50" y="150" width="150" height="40" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <rect x="225" y="150" width="150" height="40" fill="#fce4ec" stroke="#333" stroke-width="2"/>
  <rect x="400" y="150" width="150" height="40" fill="#e0f2f1" stroke="#333" stroke-width="2"/>
  <text x="125" y="175" text-anchor="middle" font-size="12">Hash%3=0</text>
  <text x="300" y="175" text-anchor="middle" font-size="12">Hash%3=1</text>
  <text x="475" y="175" text-anchor="middle" font-size="12">Hash%3=2</text>
  <text x="300" y="220" text-anchor="middle" font-size="12" font-weight="bold">Hash Sharding</text>
</svg>

---

## Consistent Hashing

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <circle cx="300" cy="125" r="100" fill="none" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="25" r="8" fill="#ff6b6b"/>
  <circle cx="380" cy="80" r="8" fill="#51cf66"/>
  <circle cx="350" cy="180" r="8" fill="#4c9aff"/>
  <circle cx="220" cy="180" r="8" fill="#ffd43b"/>
  <circle cx="200" cy="80" r="8" fill="#9c27b0"/>
  <text x="300" y="10" text-anchor="middle" font-size="10">Node A</text>
  <text x="400" y="80" text-anchor="start" font-size="10">Node B</text>
  <text x="350" y="200" text-anchor="middle" font-size="10">Node C</text>
  <text x="300" y="260" text-anchor="middle" font-size="12">Keys assigned to next node clockwise</text>
</svg>

---

## Write Concerns

Control durability vs performance:

- **W=1**: Write to one node (fast)
- **W=Majority**: Write to majority (balanced)
- **W=All**: Write to all nodes (slow, consistent)

---

## Read Concerns

Control consistency vs performance:

- **R=1**: Read from one node (fast, maybe stale)
- **R=Majority**: Read from majority (quorum)
- **R=All**: Read from all nodes (slow, consistent)

---

## Quorum Consistency

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold">Quorum: W + R > N = Strong Consistency</text>
  <rect x="40" y="35" width="150" height="70" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="3"/>
  <text x="115" y="55" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Write Quorum (W=2)</text>
  <text x="115" y="72" text-anchor="middle" font-size="10" fill="#2e7d32">Replica A: Written</text>
  <text x="115" y="87" text-anchor="middle" font-size="10" fill="#2e7d32">Replica B: Written</text>
  <text x="115" y="100" text-anchor="middle" font-size="10" fill="#999">Replica C: Pending</text>
  <rect x="225" y="35" width="150" height="70" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="3"/>
  <text x="300" y="55" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">Read Quorum (R=2)</text>
  <text x="300" y="72" text-anchor="middle" font-size="10" fill="#1565c0">Replica A: v2</text>
  <text x="300" y="87" text-anchor="middle" font-size="10" fill="#1565c0">Replica C: v1 (stale)</text>
  <text x="300" y="100" text-anchor="middle" font-size="10" fill="#1565c0">Pick latest: v2</text>
  <rect x="410" y="35" width="170" height="70" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="3"/>
  <text x="495" y="55" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">Overlap Guarantee</text>
  <text x="495" y="72" text-anchor="middle" font-size="10">W + R = 2 + 2 = 4</text>
  <text x="495" y="87" text-anchor="middle" font-size="10">N = 3 replicas</text>
  <text x="495" y="100" text-anchor="middle" font-size="10" fill="#2e7d32">4 > 3: Overlap exists</text>
  <rect x="100" y="120" width="400" height="30" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="3"/>
  <text x="300" y="140" text-anchor="middle" font-size="10" fill="#7b1fa2">At least one node in Read set saw the latest Write = consistency guaranteed</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#666">Tuning W and R: higher W+R = stronger consistency, lower = faster but weaker</text>
  <text x="300" y="192" text-anchor="middle" font-size="10" fill="#666">Common configs: W=1,R=N (fast writes) | W=N,R=1 (fast reads) | W=R=majority (balanced)</text>
</svg>

---

## Vector Clocks

Track causality in distributed systems:

```txt
Node A: [A:1, B:0, C:0] writes X=5
Node B: [A:1, B:1, C:0] writes X=7
Node C: [A:1, B:1, C:1] can determine order
```

Enables detection of concurrent updates

---

## CRDTs

Conflict-free Replicated Data Types:

- Automatically merge concurrent updates
- No conflicts possible
- Examples: Counters, Sets, Maps
- Trade-off: Limited operations

---

## NoSQL Performance Patterns

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <line x1="50" y1="150" x2="550" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="50" y1="150" x2="50" y2="50" stroke="#333" stroke-width="2"/>
  <path d="M 50 150 Q 200 140, 300 100, 400 60, 550 50" stroke="#ff6b6b" stroke-width="2" fill="none"/>
  <text x="300" y="180" text-anchor="middle" font-size="12">Data Size</text>
  <text x="30" y="100" text-anchor="middle" font-size="12" transform="rotate(-90 30 100)">Latency</text>
  <text x="300" y="30" text-anchor="middle" font-size="14" font-weight="bold">NoSQL scales linearly</text>
</svg>

---

## Data Modeling Differences

**RDBMS:**
- Normalize to avoid redundancy
- JOIN at query time
- Schema first

**NoSQL:**
- Denormalize for performance
- Pre-compute JOINs
- Access patterns first

---

## Denormalization Strategy

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="200" height="100" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="150" y="80" text-anchor="middle" font-size="12" font-weight="bold">User Document</text>
  <text x="150" y="100" text-anchor="middle" font-size="10">{ id, name,</text>
  <text x="150" y="115" text-anchor="middle" font-size="10">  orders: [...],</text>
  <text x="150" y="130" text-anchor="middle" font-size="10">  addresses: [...] }</text>
  <text x="400" y="100" text-anchor="middle" font-size="12">Everything in one place</text>
  <text x="400" y="120" text-anchor="middle" font-size="12">Single read operation</text>
</svg>

---

## Query Patterns Drive Design

- Know your access patterns upfront
- Design data model around queries
- Duplicate data if needed
- Trade storage for performance

---

## Secondary Indexing

Most NoSQL databases offer:
- Local secondary indexes (per partition)
- Global secondary indexes (across partitions)
- Trade-off: Consistency vs Performance
- Index maintenance overhead

---

## Transactions in NoSQL

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="180" height="60" fill="#ffe0e0" stroke="#333" stroke-width="2"/>
  <rect x="320" y="50" width="180" height="60" fill="#e0ffe0" stroke="#333" stroke-width="2"/>
  <text x="190" y="85" text-anchor="middle" font-size="12">Single Document</text>
  <text x="410" y="85" text-anchor="middle" font-size="12">Multi-Document</text>
  <text x="190" y="130" text-anchor="middle" font-size="11">Atomic</text>
  <text x="410" y="130" text-anchor="middle" font-size="11">Limited/Complex</text>
</svg>

---

## Choosing NoSQL Type

**Key-Value:**
- Simple lookups
- Session storage
- Caching

**Document:**
- Flexible schemas
- Content management
- Catalogs

---

## Choosing NoSQL Type (cont.)

**Column-Family:**
- Time-series data
- Write-heavy workloads
- Analytics

**Graph:**
- Social networks
- Recommendations
- Fraud detection

---

## Polyglot Persistence

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="120" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="200" y="50" width="120" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="350" y="50" width="120" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="110" y="85" text-anchor="middle" font-size="11">User Data</text>
  <text x="110" y="100" text-anchor="middle" font-size="10">RDBMS</text>
  <text x="260" y="85" text-anchor="middle" font-size="11">Sessions</text>
  <text x="260" y="100" text-anchor="middle" font-size="10">Key-Value</text>
  <text x="410" y="85" text-anchor="middle" font-size="11">Products</text>
  <text x="410" y="100" text-anchor="middle" font-size="10">Document</text>
  <text x="300" y="150" text-anchor="middle" font-size="14" font-weight="bold">Use the right tool for each job</text>
</svg>

---

## Key Takeaways

- NoSQL trades consistency for scale
- CAP theorem forces trade-offs
- Design for your access patterns
- Denormalization is normal
- Choose the right tool for your data
