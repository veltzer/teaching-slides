# SQL Databases Fundamentals
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/databases/sql-database-fundamentals/title.svg)

## What Are SQL Databases?

- Relational Database Management Systems (RDBMS)
- Structured data in tables with rows and columns
- Relationships between tables
- SQL as standard query language
- ACID compliance as core principle

---

## The Relational Model

![the_relational_model](svg/lectures/databases/sql-database-fundamentals/the_relational_model.svg)

---

## ACID Properties

The foundation of SQL database guarantees:

- Atomicity
- Consistency
- Isolation
- Durability

---

## Atomicity

![atomicity](svg/lectures/databases/sql-database-fundamentals/atomicity.svg)

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

![isolation](svg/lectures/databases/sql-database-fundamentals/isolation.svg)

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

![sql_database_architecture](svg/lectures/databases/sql-database-fundamentals/sql_database_architecture.svg)

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

![query_optimization](svg/lectures/databases/sql-database-fundamentals/query_optimization.svg)

---

## Indexing Strategies

![indexing_strategies](svg/lectures/databases/sql-database-fundamentals/indexing_strategies.svg)

---

## B-Tree Index Structure

![b_tree_index_structure](svg/lectures/databases/sql-database-fundamentals/b_tree_index_structure.svg)

---

## Transaction Isolation Levels

1. **Read Uncommitted** - Dirty reads possible
1. **Read Committed** - No dirty reads
1. **Repeatable Read** - No phantom reads
1. **Serializable** - Full isolation

Trade-off: Performance vs Consistency

---

## Concurrency Control

![concurrency_control](svg/lectures/databases/sql-database-fundamentals/concurrency_control.svg)

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

![mvcc_multi_version_concurrency_control](svg/lectures/databases/sql-database-fundamentals/mvcc_multi_version_concurrency_control.svg)

---

## SQL Databases and CAP Theorem

![sql_databases_and_cap_theorem](svg/lectures/databases/sql-database-fundamentals/sql_databases_and_cap_theorem.svg)

Traditional SQL: CA systems (single node)

---

## Single-Node SQL: CA System

**Consistency:** ACID guarantees
**Availability:** Up when server is up
**Partition Tolerance:** Not applicable (single node)

No network partitions in single-node systems!

---

## The Scale Challenge

![the_scale_challenge](svg/lectures/databases/sql-database-fundamentals/the_scale_challenge.svg)

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

![master_slave_replication](svg/lectures/databases/sql-database-fundamentals/master_slave_replication.svg)

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

![read_write_splitting](svg/lectures/databases/sql-database-fundamentals/read_write_splitting.svg)

---

## Multi-Master Replication

![multi_master_replication](svg/lectures/databases/sql-database-fundamentals/multi_master_replication.svg)

Conflict resolution required

---

## Sharding SQL Databases

![sharding_sql_databases](svg/lectures/databases/sql-database-fundamentals/sharding_sql_databases.svg)

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

![two_phase_commit_2pc](svg/lectures/databases/sql-database-fundamentals/two_phase_commit_2pc.svg)

---

## 2PC and CAP Trade-offs

**During normal operation:** CP system
**During coordinator failure:** Unavailable
**Blocking protocol:** Reduces availability

Trade availability for consistency

---

## Consensus Protocols

![consensus_protocols](svg/lectures/databases/sql-database-fundamentals/consensus_protocols.svg)

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

![newsql_and_cap](svg/lectures/databases/sql-database-fundamentals/newsql_and_cap.svg)

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

![caching_strategies](svg/lectures/databases/sql-database-fundamentals/caching_strategies.svg)

---

## Connection Pooling

![connection_pooling](svg/lectures/databases/sql-database-fundamentals/connection_pooling.svg)

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

![federation_pattern](svg/lectures/databases/sql-database-fundamentals/federation_pattern.svg)

Split by functional areas

---

## SQL in Microservices

![sql_in_microservices](svg/lectures/databases/sql-database-fundamentals/sql_in_microservices.svg)

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

![cqrs_pattern](svg/lectures/databases/sql-database-fundamentals/cqrs_pattern.svg)

---

## Comparing SQL Scaling Approaches

![comparing_sql_scaling_approaches](svg/lectures/databases/sql-database-fundamentals/comparing_sql_scaling_approaches.svg)

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
