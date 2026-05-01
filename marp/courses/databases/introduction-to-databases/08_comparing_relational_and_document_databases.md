---
tags:
  - databases:relational
  - databases:document
level: beginner
category: databases
audience:
  - audiences:developers

---
# Comparing Relational and Document Databases

---
## What This Chapter Covers

- Modeling differences
- Query differences
- Performance trade-offs
- Operational differences
- A practical comparison

---
## Modeling

- Relational: separate tables; foreign keys
- Document: embed related data
- Same problem; different shape
- "Customer with orders" looks very different

---
## Relational Example

```sql
CREATE TABLE customers (id INT, name TEXT);
CREATE TABLE orders (id INT, customer_id INT, total NUMERIC);
```

- Two tables; join when needed

---
## Document Example

```json
{
    "_id": 1,
    "name": "Alice",
    "orders": [
        { "id": 100, "total": 99 },
        { "id": 101, "total": 49 }
    ]
}
```

- One document; orders embedded

---
## Querying

- Relational: SQL JOINs
- Document: $lookup or denormalised
- For joins: relational simpler
- For "fetch one entity with all data": document simpler

---
## Schema

- Relational: schema-on-write; rigid
- Document: schema-on-read; flexible
- Trade-off: integrity vs evolution

---
## Performance

- Read one entity: document wins (no join)
- Aggregations: relational often wins
- Writes: depends on shape
- Profile your workload

---
## Transactions

- Relational: full ACID
- Document: single-doc ACID; multi-doc with care
- Heavy multi-entity transactions: relational

---
## Scaling

- Relational: vertical mostly; sharding hard
- Document: horizontal natural
- For massive scale: document often easier

---
## Tooling

- Relational: BI tools, ORMs everywhere
- Document: smaller ecosystem
- Reporting: relational has more options

---
## Operations

- Relational: well-understood; many DBAs
- Document: less mature ops; growing
- Backup, monitoring: both have tools

---
## When Relational Wins

- Complex relations
- Reporting / BI
- ACID across many entities
- Most apps fit here

---
## When Document Wins

- Hierarchical data
- Flexible / evolving schemas
- Embedded sub-objects
- Per-record schema variation

---
## Hybrid Approach

- Many companies use both
- Relational for transactional core
- Document for catalogs, content, sessions
- Polyglot persistence

---
## Common Comparison Mistakes

- "MongoDB is web-scale" without measuring
- "Postgres can't handle my JSON" — Postgres has JSONB
- Choosing by familiarity over fit
- One DB for everything when two would be cleaner
- Migrating without measuring the actual problem
