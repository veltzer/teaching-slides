# SQL Databases Fundamentals

---

## What Are SQL Databases?

- Relational Database Management Systems (RDBMS)
- Structured data in tables with rows and columns
- Relationships between tables
- SQL as standard query language
- ACID compliance as core principle

---

## The Relational Model

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="200" height="150" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="350" y="50" width="200" height="150" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="30" text-anchor="middle" font-size="14" font-weight="bold">Users Table</text>
  <text x="450" y="30" text-anchor="middle" font-size="14" font-weight="bold">Orders Table</text>
  <line x1="60" y1="80" x2="240" y2="80" stroke="#333" stroke-width="1"/>
  <text x="80" y="100" font-size="11">ID | Name | Email</text>
  <text x="80" y="120" font-size="11">1  | John | j@ex.com</text>
  <text x="80" y="140" font-size="11">2  | Jane | jane@ex</text>
  <line x1="360" y1="80" x2="540" y2="80" stroke="#333" stroke-width="1"/>
  <text x="380" y="100" font-size="11">ID | UserID | Total</text>
  <text x="380" y="120" font-size="11">101 | 1     | $50</text>
  <text x="380" y="140" font-size="11">102 | 2     | $75</text>
  <path d="M 250 110 Q 300 110 350 110" stroke="#ff6b6b" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#ff6b6b"/>
    </marker>
  </defs>
</svg>

---

## ACID Properties

The foundation of SQL database guarantees:

- Atomicity
- Consistency
- Isolation
- Durability

---

## Atomicity

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="100" fill="#e8f5e9" stroke="#4caf50" stroke-width="2"/>
  <rect x="350" y="50" width="150" height="100" fill="#ffebee" stroke="#f44336" stroke-width="2"/>
  <text x="175" y="90" text-anchor="middle" font-size="12" font-weight="bold">All Succeed</text>
  <text x="175" y="110" text-anchor="middle" font-size="11">Debit: -$100</text>
  <text x="175" y="130" text-anchor="middle" font-size="11">Credit: +$100</text>
  <text x="425" y="90" text-anchor="middle" font-size="12" font-weight="bold">All Fail</text>
  <text x="425" y="110" text-anchor="middle" font-size="11">Debit: Rollback</text>
  <text x="425" y="130" text-anchor="middle" font-size="11">Credit: Never happens</text>
</svg>

All or nothing - no partial transactions

---

## Consistency

Database remains valid after every transaction:

- Constraints are enforced
- Triggers execute
- Foreign keys maintained
- Data integrity preserved
- Business rules respected

---

## Isolation

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="180" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="100" y="110" width="180" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="190" y="75" text-anchor="middle" font-size="12">Transaction A</text>
  <text x="190" y="135" text-anchor="middle" font-size="12">Transaction B</text>
  <line x1="320" y1="50" x2="320" y2="150" stroke="#ff6b6b" stroke-width="3"/>
  <text x="320" y="180" text-anchor="middle" font-size="12">Isolation Barrier</text>
  <text x="420" y="100" text-anchor="middle" font-size="11">Cannot see each</text>
  <text x="420" y="120" text-anchor="middle" font-size="11">other's changes</text>
</svg>

---

## Durability

Once committed, data survives:

- Written to persistent storage
- Survives system crashes
- Transaction logs maintained
- Point-in-time recovery possible
- Backup and restore capabilities

---

## SQL Database Architecture

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="30" width="200" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="200" y="90" width="200" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="200" y="150" width="200" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <rect x="200" y="210" width="200" height="40" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-size="12">Query Parser</text>
  <text x="300" y="115" text-anchor="middle" font-size="12">Query Optimizer</text>
  <text x="300" y="175" text-anchor="middle" font-size="12">Execution Engine</text>
  <text x="300" y="235" text-anchor="middle" font-size="12">Storage Engine</text>
</svg>

---

## Query Processing Pipeline

1. Parse SQL into abstract syntax tree
1. Validate against schema
1. Generate execution plans
1. Choose optimal plan
1. Execute plan
1. Return results

---

## Query Optimization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="40" fill="#ffe0e0" stroke="#333" stroke-width="2"/>
  <rect x="50" y="100" width="150" height="40" fill="#e0ffe0" stroke="#333" stroke-width="2"/>
  <rect x="50" y="150" width="150" height="40" fill="#e0e0ff" stroke="#333" stroke-width="2"/>
  <text x="125" y="75" text-anchor="middle" font-size="11">Plan A: Nested Loop</text>
  <text x="125" y="125" text-anchor="middle" font-size="11">Plan B: Hash Join</text>
  <text x="125" y="175" text-anchor="middle" font-size="11">Plan C: Merge Join</text>
  <text x="350" y="75" text-anchor="middle" font-size="12">Cost: 1000</text>
  <text x="350" y="125" text-anchor="middle" font-size="12" font-weight="bold">Cost: 100 ✓</text>
  <text x="350" y="175" text-anchor="middle" font-size="12">Cost: 500</text>
</svg>

---

## Indexing Strategies

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="400" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="100" y="80" width="400" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <rect x="100" y="110" width="400" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <rect x="100" y="140" width="400" height="30" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="300" y="70" text-anchor="middle" font-size="12">Table Data</text>
  <path d="M 50 200 L 100 200 L 75 170 Z" fill="#ff6b6b"/>
  <text x="75" y="220" text-anchor="middle" font-size="10">Index</text>
  <line x1="75" y1="170" x2="100" y2="95" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,5"/>
  <line x1="75" y1="170" x2="100" y2="125" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="300" y="30" text-anchor="middle" font-size="14" font-weight="bold">Direct Access via Index</text>
</svg>

---

## B-Tree Index Structure

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="30" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="150" y="90" width="80" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="370" y="90" width="80" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="50" y="150" width="60" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="120" y="150" width="60" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="190" y="150" width="60" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="260" y="150" width="60" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="330" y="150" width="60" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="400" y="150" width="60" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="470" y="150" width="60" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="300" y="50" text-anchor="middle" font-size="11">50</text>
  <text x="190" y="110" text-anchor="middle" font-size="11">20</text>
  <text x="410" y="110" text-anchor="middle" font-size="11">70</text>
  <line x1="300" y1="60" x2="190" y2="90" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="60" x2="410" y2="90" stroke="#333" stroke-width="1"/>
  <text x="300" y="210" text-anchor="middle" font-size="12">Balanced tree for O(log n) operations</text>
</svg>

---

## Transaction Isolation Levels

1. **Read Uncommitted** - Dirty reads possible
1. **Read Committed** - No dirty reads
1. **Repeatable Read** - No phantom reads
1. **Serializable** - Full isolation

Trade-off: Performance vs Consistency

---

## Concurrency Control

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="180" height="100" fill="#ffe0e0" stroke="#333" stroke-width="2"/>
  <rect x="320" y="50" width="180" height="100" fill="#e0ffe0" stroke="#333" stroke-width="2"/>
  <text x="190" y="30" text-anchor="middle" font-size="12" font-weight="bold">Pessimistic</text>
  <text x="410" y="30" text-anchor="middle" font-size="12" font-weight="bold">Optimistic</text>
  <text x="190" y="90" text-anchor="middle" font-size="11">Lock first</text>
  <text x="190" y="110" text-anchor="middle" font-size="11">Then modify</text>
  <text x="190" y="130" text-anchor="middle" font-size="11">Prevents conflicts</text>
  <text x="410" y="90" text-anchor="middle" font-size="11">Modify freely</text>
  <text x="410" y="110" text-anchor="middle" font-size="11">Check at commit</text>
  <text x="410" y="130" text-anchor="middle" font-size="11">Retry if conflict</text>
</svg>

---

## Locking Mechanisms

**Row-level locks:**
- Fine granularity
- Higher concurrency
- More overhead

**Table-level locks:**
- Coarse granularity
- Lower concurrency
- Less overhead

---

## MVCC (Multi-Version Concurrency Control)

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="400" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="300" y="70" text-anchor="middle" font-size="12">Row: ID=1, Value=100, Version=T1</text>
  <rect x="100" y="90" width="400" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="300" y="110" text-anchor="middle" font-size="12">Row: ID=1, Value=150, Version=T2</text>
  <rect x="100" y="130" width="400" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="300" y="150" text-anchor="middle" font-size="12">Row: ID=1, Value=200, Version=T3</text>
  <text x="300" y="180" text-anchor="middle" font-size="11">Readers see consistent snapshot</text>
</svg>

---

## SQL Databases and CAP Theorem

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <circle cx="200" cy="150" r="120" fill="#ff6b6b" opacity="0.3" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="150" r="120" fill="#51cf66" opacity="0.3" stroke="#333" stroke-width="2"/>
  <circle cx="250" cy="230" r="120" fill="#4c9aff" opacity="0.3" stroke="#333" stroke-width="2"/>
  <text x="200" y="100" text-anchor="middle" font-size="14" font-weight="bold">C</text>
  <text x="300" y="100" text-anchor="middle" font-size="14" font-weight="bold">A</text>
  <text x="250" y="290" text-anchor="middle" font-size="14" font-weight="bold">P</text>
  <circle cx="250" cy="150" r="8" fill="#333"/>
  <text x="250" y="140" text-anchor="middle" font-size="11">Traditional</text>
  <text x="250" y="125" text-anchor="middle" font-size="11">SQL</text>
</svg>

Traditional SQL: CA systems (single node)

---

## Single-Node SQL: CA System

**Consistency:** ACID guarantees
**Availability:** Up when server is up
**Partition Tolerance:** Not applicable (single node)

No network partitions in single-node systems!

---

## The Scale Challenge

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="120" height="100" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="110" y="100" text-anchor="middle" font-size="12">Single SQL</text>
  <text x="110" y="120" text-anchor="middle" font-size="11">Server</text>
  <line x1="200" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="225" y="90" text-anchor="middle" font-size="10">Scale?</text>
  <rect x="300" y="30" width="80" height="60" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <rect x="300" y="110" width="80" height="60" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <rect x="400" y="30" width="80" height="60" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <rect x="400" y="110" width="80" height="60" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="390" y="190" text-anchor="middle" font-size="11">Distributed SQL</text>
</svg>

---

## Vertical Scaling (Scale-Up)

Traditional SQL approach:

- Add more CPU
- Add more RAM
- Faster disks (SSD/NVMe)
- Hardware limits exist
- Expensive at scale

---

## Horizontal Scaling Challenges

Why SQL databases struggle with distribution:

- ACID requires coordination
- JOINs across network
- Foreign key constraints
- Distributed transactions
- Two-phase commit overhead

---

## Master-Slave Replication

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="30" width="100" height="60" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <rect x="100" y="150" width="100" height="60" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <rect x="250" y="150" width="100" height="60" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <rect x="400" y="150" width="100" height="60" fill="#4c9aff" stroke="#333" stroke-width="2"/>
  <text x="300" y="65" text-anchor="middle" font-size="12">Master</text>
  <text x="150" y="185" text-anchor="middle" font-size="12">Slave 1</text>
  <text x="300" y="185" text-anchor="middle" font-size="12">Slave 2</text>
  <text x="450" y="185" text-anchor="middle" font-size="12">Slave 3</text>
  <line x1="300" y1="90" x2="150" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="300" y1="90" x2="300" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="300" y1="90" x2="450" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Writes to master, reads from slaves

---

## Replication and CAP

**Synchronous Replication:**
- Choose CP
- Wait for all replicas
- Strong consistency
- Lower availability

**Asynchronous Replication:**
- Choose AP
- Don't wait for replicas
- Eventual consistency
- Higher availability

---

## Read/Write Splitting

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="150" cy="100" rx="80" ry="60" fill="#ffe0e0" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="100" rx="80" ry="60" fill="#e0ffe0" stroke="#333" stroke-width="2"/>
  <text x="150" y="90" text-anchor="middle" font-size="12" font-weight="bold">Write Path</text>
  <text x="150" y="110" text-anchor="middle" font-size="11">Master only</text>
  <text x="150" y="130" text-anchor="middle" font-size="11">Consistent</text>
  <text x="450" y="90" text-anchor="middle" font-size="12" font-weight="bold">Read Path</text>
  <text x="450" y="110" text-anchor="middle" font-size="11">Any replica</text>
  <text x="450" y="130" text-anchor="middle" font-size="11">May lag</text>
</svg>

---

## Multi-Master Replication

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="50" width="100" height="60" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <rect x="350" y="50" width="100" height="60" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <rect x="150" y="150" width="100" height="60" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <rect x="350" y="150" width="100" height="60" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <text x="200" y="85" text-anchor="middle" font-size="12">Master 1</text>
  <text x="400" y="85" text-anchor="middle" font-size="12">Master 2</text>
  <text x="200" y="185" text-anchor="middle" font-size="12">Master 3</text>
  <text x="400" y="185" text-anchor="middle" font-size="12">Master 4</text>
  <line x1="250" y1="80" x2="350" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="110" x2="200" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="110" x2="400" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="180" x2="350" y2="180" stroke="#333" stroke-width="2"/>
</svg>

Conflict resolution required

---

## Sharding SQL Databases

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="400" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="300" y="75" text-anchor="middle" font-size="12">Users Table (1M rows)</text>
  <rect x="100" y="130" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <rect x="240" y="130" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <rect x="380" y="130" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="160" y="155" text-anchor="middle" font-size="11">Shard 1: A-H</text>
  <text x="300" y="155" text-anchor="middle" font-size="11">Shard 2: I-P</text>
  <text x="440" y="155" text-anchor="middle" font-size="11">Shard 3: Q-Z</text>
</svg>

---

## Sharding Challenges

- No cross-shard JOINs
- No foreign keys across shards
- Distributed transactions complex
- Rebalancing is difficult
- Application-level sharding logic

---

## Distributed SQL Architectures

Modern approaches to distributed SQL:

- Shared-nothing architecture
- Consensus protocols (Raft/Paxos)
- Distributed transaction coordinators
- Global secondary indexes

---

## Two-Phase Commit (2PC)

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Two-Phase Commit Protocol (2PC)</text>
  <rect x="230" y="25" width="140" height="35" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="3"/>
  <text x="300" y="47" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Coordinator</text>
  <rect x="30" y="90" width="120" height="35" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="3"/>
  <text x="90" y="112" text-anchor="middle" font-size="10" fill="#1565c0">Participant A</text>
  <rect x="240" y="90" width="120" height="35" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="3"/>
  <text x="300" y="112" text-anchor="middle" font-size="10" fill="#1565c0">Participant B</text>
  <rect x="450" y="90" width="120" height="35" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="3"/>
  <text x="510" y="112" text-anchor="middle" font-size="10" fill="#1565c0">Participant C</text>
  <line x1="270" y1="60" x2="90" y2="88" stroke="#e65100" stroke-width="1.5" marker-end="url(#arrow2pc)"/>
  <line x1="300" y1="60" x2="300" y2="88" stroke="#e65100" stroke-width="1.5" marker-end="url(#arrow2pc)"/>
  <line x1="330" y1="60" x2="510" y2="88" stroke="#e65100" stroke-width="1.5" marker-end="url(#arrow2pc)"/>
  <text x="150" y="75" text-anchor="middle" font-size="9" fill="#e65100">PREPARE?</text>
  <text x="450" y="75" text-anchor="middle" font-size="9" fill="#e65100">PREPARE?</text>
  <rect x="30" y="135" width="170" height="55" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="115" y="152" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">Phase 1: Prepare</text>
  <text x="115" y="167" text-anchor="middle" font-size="9">Each node votes YES/NO</text>
  <text x="115" y="182" text-anchor="middle" font-size="9">Locks resources, writes log</text>
  <rect x="230" y="135" width="170" height="55" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="315" y="152" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">Phase 2: Commit</text>
  <text x="315" y="167" text-anchor="middle" font-size="9">All YES: COMMIT</text>
  <text x="315" y="182" text-anchor="middle" font-size="9">Any NO: ROLLBACK all</text>
  <rect x="430" y="135" width="160" height="55" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="3"/>
  <text x="510" y="152" text-anchor="middle" font-size="10" font-weight="bold" fill="#7b1fa2">Trade-off</text>
  <text x="510" y="167" text-anchor="middle" font-size="9">Strong consistency</text>
  <text x="510" y="182" text-anchor="middle" font-size="9">But: blocking protocol</text>
  <defs>
    <marker id="arrow2pc" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#e65100"/>
    </marker>
  </defs>
</svg>

---

## 2PC and CAP Trade-offs

**During normal operation:** CP system
**During coordinator failure:** Unavailable
**Blocking protocol:** Reduces availability

Trade availability for consistency

---

## Consensus Protocols

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Raft Consensus: Leader-Based Replication</text>
  <rect x="210" y="25" width="100" height="40" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="20"/>
  <text x="260" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Leader</text>
  <text x="260" y="57" text-anchor="middle" font-size="9">Handles writes</text>
  <rect x="50" y="90" width="100" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="20"/>
  <text x="100" y="107" text-anchor="middle" font-size="11" fill="#1565c0">Follower A</text>
  <text x="100" y="122" text-anchor="middle" font-size="9" fill="#666">Replicates log</text>
  <rect x="210" y="90" width="100" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="20"/>
  <text x="260" y="107" text-anchor="middle" font-size="11" fill="#1565c0">Follower B</text>
  <text x="260" y="122" text-anchor="middle" font-size="9" fill="#666">Replicates log</text>
  <rect x="370" y="90" width="100" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="20"/>
  <text x="420" y="107" text-anchor="middle" font-size="11" fill="#1565c0">Follower C</text>
  <text x="420" y="122" text-anchor="middle" font-size="9" fill="#666">Replicates log</text>
  <line x1="230" y1="65" x2="120" y2="88" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowraft)"/>
  <line x1="260" y1="65" x2="260" y2="88" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowraft)"/>
  <line x1="290" y1="65" x2="400" y2="88" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowraft)"/>
  <text x="170" y="78" font-size="9" fill="#2e7d32">AppendEntries</text>
  <rect x="100" y="145" width="320" height="20" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="260" y="159" text-anchor="middle" font-size="10" fill="#2e7d32">Majority ACK (2/3) required to commit entry</text>
  <rect x="100" y="170" width="320" height="20" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="260" y="184" text-anchor="middle" font-size="10" fill="#e65100">Leader fails? Election selects new leader with latest log</text>
  <defs>
    <marker id="arrowraft" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#2e7d32"/>
    </marker>
  </defs>
</svg>

---

## NewSQL Movement

Attempting to get best of both worlds:

- SQL interface and ACID
- Horizontal scalability
- Distributed by design
- Modern architectures
- Cloud-native

---

## NewSQL and CAP

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <circle cx="200" cy="125" r="100" fill="#ff6b6b" opacity="0.3" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="125" r="100" fill="#51cf66" opacity="0.3" stroke="#333" stroke-width="2"/>
  <circle cx="250" cy="200" r="100" fill="#4c9aff" opacity="0.3" stroke="#333" stroke-width="2"/>
  <text x="200" y="75" text-anchor="middle" font-size="12" font-weight="bold">C</text>
  <text x="300" y="75" text-anchor="middle" font-size="12" font-weight="bold">A</text>
  <text x="250" y="260" text-anchor="middle" font-size="12" font-weight="bold">P</text>
  <ellipse cx="225" cy="160" rx="30" ry="20" fill="#333" opacity="0.5"/>
  <text x="225" y="165" text-anchor="middle" font-size="10" fill="white">NewSQL</text>
</svg>

Usually CP with high availability

---

## SQL Database Optimization Strategies

For CAP considerations:

- Read replicas for availability
- Caching layers
- Connection pooling
- Query optimization
- Denormalization when needed

---

## Caching Strategies

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="80" width="100" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="250" y="80" width="100" height="60" fill="#ffd43b" stroke="#333" stroke-width="2"/>
  <rect x="450" y="80" width="100" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="100" y="115" text-anchor="middle" font-size="12">Client</text>
  <text x="300" y="115" text-anchor="middle" font-size="12">Cache</text>
  <text x="500" y="115" text-anchor="middle" font-size="12">Database</text>
  <line x1="150" y1="110" x2="250" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="350" y1="110" x2="450" y2="110" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrow4)"/>
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="160" text-anchor="middle" font-size="11">Hit = High Availability</text>
</svg>

---

## Connection Pooling

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="60" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="50" y="90" width="60" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="50" y="130" width="60" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="250" y="70" width="100" height="80" fill="#ffd43b" stroke="#333" stroke-width="2"/>
  <rect x="450" y="80" width="100" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="80" y="70" text-anchor="middle" font-size="10">App 1</text>
  <text x="80" y="110" text-anchor="middle" font-size="10">App 2</text>
  <text x="80" y="150" text-anchor="middle" font-size="10">App 3</text>
  <text x="300" y="115" text-anchor="middle" font-size="12">Pool</text>
  <text x="500" y="115" text-anchor="middle" font-size="12">Database</text>
  <line x1="110" y1="65" x2="250" y2="90" stroke="#333" stroke-width="1"/>
  <line x1="110" y1="105" x2="250" y2="110" stroke="#333" stroke-width="1"/>
  <line x1="110" y1="145" x2="250" y2="130" stroke="#333" stroke-width="1"/>
  <line x1="350" y1="110" x2="450" y2="110" stroke="#333" stroke-width="2"/>
</svg>

Reduces connection overhead

---

## Partitioning Strategies for SQL

**Vertical Partitioning:**
- Split tables by columns
- Different tables on different servers
- Maintain relationships carefully

**Horizontal Partitioning:**
- Split tables by rows
- Same schema, different data
- Sharding key crucial

---

## Federation Pattern

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="30" width="100" height="40" fill="#333" stroke="#333" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-size="12" fill="white">Router</text>
  <rect x="100" y="130" width="100" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="250" y="130" width="100" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="400" y="130" width="100" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="150" y="165" text-anchor="middle" font-size="11">Users DB</text>
  <text x="300" y="165" text-anchor="middle" font-size="11">Orders DB</text>
  <text x="450" y="165" text-anchor="middle" font-size="11">Products DB</text>
  <line x1="275" y1="70" x2="175" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="70" x2="300" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="325" y1="70" x2="425" y2="130" stroke="#333" stroke-width="2"/>
</svg>

Split by functional areas

---

## SQL in Microservices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="100" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="350" y="50" width="150" height="100" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="175" y="80" text-anchor="middle" font-size="11">Service A</text>
  <rect x="125" y="95" width="100" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="175" y="120" text-anchor="middle" font-size="10">SQL DB A</text>
  <text x="425" y="80" text-anchor="middle" font-size="11">Service B</text>
  <rect x="375" y="95" width="100" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="425" y="120" text-anchor="middle" font-size="10">SQL DB B</text>
  <text x="300" y="180" text-anchor="middle" font-size="12">Database per service pattern</text>
</svg>

---

## Event Sourcing with SQL

Store events, not state:

- Append-only writes (no conflicts)
- Complete audit trail
- Replay to any point
- CQRS pattern compatible
- Eventually consistent projections

---

## CQRS Pattern

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="80" width="100" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="230" y="50" width="100" height="40" fill="#ffe0e0" stroke="#333" stroke-width="2"/>
  <rect x="230" y="110" width="100" height="40" fill="#e0ffe0" stroke="#333" stroke-width="2"/>
  <rect x="410" y="50" width="100" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <rect x="410" y="110" width="100" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="100" y="115" text-anchor="middle" font-size="12">Client</text>
  <text x="280" y="75" text-anchor="middle" font-size="11">Commands</text>
  <text x="280" y="135" text-anchor="middle" font-size="11">Queries</text>
  <text x="460" y="75" text-anchor="middle" font-size="11">Write DB</text>
  <text x="460" y="135" text-anchor="middle" font-size="11">Read DB</text>
  <line x1="150" y1="100" x2="230" y2="70" stroke="#333" stroke-width="2"/>
  <line x1="150" y1="120" x2="230" y2="130" stroke="#333" stroke-width="2"/>
</svg>

---

## Comparing SQL Scaling Approaches

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <text x="100" y="30" font-size="12" font-weight="bold">Approach</text>
  <text x="250" y="30" font-size="12" font-weight="bold">CAP Choice</text>
  <text anch="400" y="30" font-size="12" font-weight="bold">Trade-off</text>
  <line x1="50" y1="40" x2="550" y2="40" stroke="#333" stroke-width="1"/>
  <text x="100" y="60" font-size="11">Single Node</text>
  <text x="250" y="60" font-size="11">CA</text>
  <text x="400" y="60" font-size="11">No distribution</text>
  <text x="100" y="90" font-size="11">Master-Slave</text>
  <text x="250" y="90" font-size="11">CP/AP</text>
  <text x="400" y="90" font-size="11">Replication lag</text>
  <text x="100" y="120" font-size="11">Sharding</text>
  <text x="250" y="120" font-size="11">CP</text>
  <text x="400" y="120" font-size="11">No cross-shard ops</text>
  <text x="100" y="150" font-size="11">NewSQL</text>
  <text x="250" y="150" font-size="11">CP</text>
  <text x="400" y="150" font-size="11">Complexity</text>
</svg>

---

## SQL Database Evolution

From CA to distributed CP:

1. Single-node ACID (CA)
1. Replication for reads (CP/AP)
1. Sharding for scale (CP)
1. Distributed SQL (CP)
1. Hybrid approaches

---

## Key Takeaways

- Traditional SQL databases are CA systems
- Distribution forces CAP trade-offs
- Replication introduces consistency challenges
- Modern SQL embraces distribution
- Different strategies for different needs
