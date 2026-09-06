---
tags:
- data-and-ai:nosql
- concepts:databases
- concepts:data-modeling
level: intermediate
category: database
audience:
- audiences:developers
- audiences:data-engineers

---

# NoSQL Databases Fundamentals
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What Are NoSQL Databases?

![title](svg/lectures/databases/nosql-database-fundamentals/title.svg)

---

## What Are NoSQL Databases?: Details

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

![the_fundamental_shift](svg/lectures/databases/nosql-database-fundamentals/the_fundamental_shift.svg)

---

## Core NoSQL Categories

1. Document Stores
1. Key-Value Stores
1. Column-Family Stores
1. Graph Databases

---

## Document Stores: Core Concepts

![document_stores_core_concepts](svg/lectures/databases/nosql-database-fundamentals/document_stores_core_concepts.svg)

---

## Document Stores: Core Concepts: Overview

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

![key_value_stores_core_model](svg/lectures/databases/nosql-database-fundamentals/key_value_stores_core_model.svg)

---

## Key-Value Stores: Core Model: Overview

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

![key_value_distribution_strategy](svg/lectures/databases/nosql-database-fundamentals/key_value_distribution_strategy.svg)

---

## Column-Family Stores: Structure

![column_family_stores_structure](svg/lectures/databases/nosql-database-fundamentals/column_family_stores_structure.svg)

---

## Column-Family: How It Works

- Data stored in column families
- Each row has a unique row key
- Columns grouped into families
- Sparse storage - only store what exists
- Optimized for write-heavy workloads

---

## Graph Databases: Core Model

![graph_databases_core_model](svg/lectures/databases/nosql-database-fundamentals/graph_databases_core_model.svg)

---

## Graph Databases: Operations

- Store nodes (entities)
- Store edges (relationships)
- Properties on both nodes and edges
- Traverse relationships efficiently
- Pattern matching queries

---

## The CAP Theorem

![the_cap_theorem](svg/lectures/databases/nosql-database-fundamentals/the_cap_theorem.svg)

---

## The CAP Theorem: Overview

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

![cp_systems](svg/lectures/databases/nosql-database-fundamentals/cp_systems.svg)

---

## CP Systems: Overview

Example behaviors: Banking systems, inventory management

---

## AP Systems

![ap_systems](svg/lectures/databases/nosql-database-fundamentals/ap_systems.svg)

---

## AP Systems: Overview

Example behaviors: Social media feeds, caching systems

---

## Consistency Models Spectrum

![consistency_models_spectrum](svg/lectures/databases/nosql-database-fundamentals/consistency_models_spectrum.svg)

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

![eventual_consistency_details](svg/lectures/databases/nosql-database-fundamentals/eventual_consistency_details.svg)

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

![conflict_resolution](svg/lectures/databases/nosql-database-fundamentals/conflict_resolution.svg)

---

## Sharding (Partitioning)

Splitting data across multiple nodes:

- Horizontal partitioning
- Each shard holds subset of data
- Distribution by key range or hash
- Enables horizontal scaling

---

## Sharding Strategies

![sharding_strategies](svg/lectures/databases/nosql-database-fundamentals/sharding_strategies.svg)

---

## Consistent Hashing

![consistent_hashing](svg/lectures/databases/nosql-database-fundamentals/consistent_hashing.svg)

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

![quorum_consistency](svg/lectures/databases/nosql-database-fundamentals/quorum_consistency.svg)

---

## Vector Clocks

Track causality in distributed systems:

```output
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

![nosql_performance_patterns](svg/lectures/databases/nosql-database-fundamentals/nosql_performance_patterns.svg)

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

![denormalization_strategy](svg/lectures/databases/nosql-database-fundamentals/denormalization_strategy.svg)

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

![transactions_in_nosql](svg/lectures/databases/nosql-database-fundamentals/transactions_in_nosql.svg)

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

![polyglot_persistence](svg/lectures/databases/nosql-database-fundamentals/polyglot_persistence.svg)

---

## Key Takeaways

- NoSQL trades consistency for scale
- CAP theorem forces trade-offs
- Design for your access patterns
- Denormalization is normal
- Choose the right tool for your data
