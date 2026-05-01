---
tags:
  - databases:design
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Introduction to Database Design Principles

---
## What This Chapter Covers

- Why design matters
- Goals: integrity, performance, evolution
- The conceptual / logical / physical model
- Common pitfalls

---
## Why Design Matters

- Schema lives longer than the code
- Bad design: hard to fix later
- Good design: scales, evolves, performs
- The single most important DB skill

---
## Goals

- Data integrity
- Performance
- Evolvability
- Clarity for developers

---
## Three Models

- Conceptual: ER diagrams; "what entities exist"
- Logical: tables, columns, FKs (no DBMS specifics)
- Physical: indexes, partitions, types (DBMS-specific)
- Each builds on the last

---
## Conceptual Modelling

- Entities: User, Order, Product
- Relationships: User has many Orders
- Cardinality: 1:1, 1:N, M:N
- High-level; for stakeholders

---
## Logical Design

- Convert to tables
- Primary keys, foreign keys
- Normalisation
- Independent of database vendor

---
## Physical Design

- Storage decisions
- Indexes for queries
- Partitioning for scale
- Vendor-specific features

---
## Iterating

- First pass: get it correct
- Second: optimise for performance
- Don't over-optimise upfront
- Measure before adding indexes

---
## Conventions

- Plural table names: users, orders
- snake_case columns
- Primary key: id
- Foreign keys: user_id, order_id
- Consistency saves debate

---
## Common Pitfalls

- Designing tables before understanding the queries
- Ignoring future growth
- Premature denormalisation
- "We'll add indexes later"
- Not documenting decisions
