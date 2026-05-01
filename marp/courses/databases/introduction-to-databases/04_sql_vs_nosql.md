---
tags:
  - databases:sql
  - databases:nosql
level: beginner
category: databases
audience:
  - audiences:developers

---
# SQL vs NoSQL

---
## What This Chapter Covers

- SQL strengths
- NoSQL flavours
- When each wins
- Hybrid use
- Choosing

---
## SQL Strengths

- Mature: 50 years of optimisation
- Standardised query language
- Strong consistency
- Joins
- Constraints

---
## SQL Weaknesses

- Vertical scaling (mostly)
- Schema migration complexity
- Less flexible for nested data

---
## NoSQL Flavours

- Document (MongoDB, DynamoDB)
- Key-Value (Redis, DynamoDB key-only)
- Wide-Column (Cassandra, HBase)
- Graph (Neo4j)
- Search (Elasticsearch)

---
## Document

- JSON-like documents
- Flexible schema
- Embedded relationships
- Best: hierarchical data

---
## Key-Value

- Simple: key &#8594; value
- Cache, sessions
- Sub-millisecond
- Limited query model

---
## Wide-Column

- Tables with sparse columns
- Massive write throughput
- Schema flexibility per row
- Best: time-series at scale

---
## Graph

- Nodes and edges
- Relationship-heavy data
- Queries traverse: friends-of-friends
- Best: social, fraud, knowledge graphs

---
## Search

- Full-text + analytics
- Inverted index
- Schema-flexible
- Best: search experiences

---
## When SQL Wins

- Complex relations
- Strong consistency
- Reporting / BI
- Tax: most apps fit
- Default choice

---
## When NoSQL Wins

- Specific access patterns (key-only)
- Massive write throughput (Cassandra)
- Flexible schemas (Mongo)
- Domain-specific (graph, search)
- Match to need

---
## Hybrid

- SQL for core data
- Redis for cache / sessions
- Elasticsearch for search
- Most production stacks
- Use the right tool

---
## ACID vs BASE

- ACID: atomic, consistent, isolated, durable (SQL)
- BASE: basically available, soft state, eventually consistent (NoSQL)
- Different consistency models
- Pick by: how much staleness can you tolerate

---
## Common SQL/NoSQL Mistakes

- Choosing NoSQL for hype
- Choosing NoSQL because "we'll need to scale"
- Choosing SQL when document model fits naturally
- Forcing relations into NoSQL with N joins
- Single DB for everything when polyglot would help
