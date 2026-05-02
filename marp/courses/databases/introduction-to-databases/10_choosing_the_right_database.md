---
tags:
  - databases:choosing
level: beginner
category: databases
audience:
  - audiences:developers
  - audiences:architects

---
# Choosing the Right Database

---
## Decision Tree

![decision_tree](svg/courses/databases/introduction-to-databases/10_choosing_the_right_database/decision_tree.svg)

---
## What This Chapter Covers

- A decision framework
- Workload characteristics
- Cloud vs self-hosted
- Cost
- Lock-in
- Polyglot persistence

---
## Start With The Workload

- Read-heavy or write-heavy?
- Strict consistency or eventual?
- Relational structure or hierarchical?
- Scale (data size, throughput)?
- Latency requirements?

---
## Workload Patterns

- OLTP: transactional; high concurrency; small queries
- OLAP: analytical; few queries; big aggregations
- Time-series: append-mostly; time-based queries
- Search: full-text relevance
- Graph: relationship traversal

---
## Default: Postgres

- Capable for 90% of OLTP workloads
- JSON support for semi-structured
- Strong ecosystem
- Easy to find DBAs / docs

---
## When Not Default

- Specific access pattern (key-value, time-series)
- Massive scale (Cassandra, ScyllaDB)
- Document-heavy (MongoDB)
- Search-first (Elasticsearch)
- Graph-first (Neo4j)

---
## Cloud Hosted

- AWS RDS, Aurora
- GCP Cloud SQL, AlloyDB
- Azure Database
- Atlas (MongoDB)
- Confluent Cloud (Kafka)
- Less ops; more cost

---
## Self-Hosted

- Cheaper at scale
- Full control
- More operational burden
- Ops team required

---
## Cost Considerations

- Storage
- Compute
- Network egress
- Backup retention
- Hosted markup
- Forecast year 1 and year 3

---
## Vendor Lock-In

- Proprietary features = lock-in
- Standard features = portable
- Document trade-off when adopting
- Multi-cloud is usually a fantasy; just pick one

---
## Polyglot Persistence

- Multiple DBs for different needs
- Postgres for transactional core
- Redis for cache
- Elasticsearch for search
- Common in modern stacks

---
## Hidden Costs

- Operational complexity
- Sync between stores (CDC, ETL)
- Multiple expertise needed
- Pick polyglot deliberately

---
## When To Switch DBs

- Workload outgrew current DB
- Specific feature needed
- Cost / ops drives change
- Migration: months of work

---
## A Decision Framework

- Identify the workload
- Default to Postgres unless reason to differ
- Add specialised stores when justified
- Hosted unless cost / control demands
- Forecast cost; check lock-in

---
## Course Wrap-Up

- Databases store and query data persistently
- Relational and NoSQL: different trade-offs
- SQL is the lingua franca; learn it well
- Migrations are how schemas evolve
- ORMs help; understand what they generate
- Match the database to the workload, not to hype
