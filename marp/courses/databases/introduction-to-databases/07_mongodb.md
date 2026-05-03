---
tags:
  - databases:mongodb
level: beginner
category: databases
audience:
  - audiences:developers

---
# MongoDB

---
## What This Chapter Covers

- MongoDB at a glance
- Document model
- CRUD basics
- Schema flexibility
- When to choose
- Comparison with relational

---
## What MongoDB Is

- Document-oriented NoSQL
- BSON storage
- Distributed
- Most-deployed document DB

---
## Document

```json
{
    "_id": "...",
    "name": "Alice",
    "addresses": [
        { "type": "home", "city": "Boston" },
        { "type": "work", "city": "NYC" }
    ]
}
```

---
## Collections

- Group of documents
- No fixed schema (by default)
- Schema validation optional
- Per-database

---
## CRUD

```python
db.users.insert_one({"name": "Alice"})
db.users.find_one({"name": "Alice"})
db.users.update_one({"_id": 1}, {"$set": {"name": "Alice S"}})
db.users.delete_one({"_id": 1})
```

---
## Embed vs Reference

- Embed: nested document; atomic; fast read
- Reference: ID pointer; avoid duplication
- Pick by query patterns

---
## Modelling Choice

![embed_vs_reference](svg/courses/databases/introduction-to-databases/07_mongodb/embed_vs_reference.svg)

---
## Aggregation

- Pipeline: $match, $group, $project, $lookup
- Like a series of transformations
- Powerful for analytics

---
## Indexes

- Same as relational (B-tree, multi-key, text, geo)
- _id always indexed
- Per-collection

---
## Transactions

- Multi-document since 4.0
- Slower than single-doc ops
- Use for: ACID across collections

---
## Schema Flexibility

- Each document can have different fields
- Useful for: evolving schemas
- Risk: junk accumulates without validation

---
## When MongoDB Wins

- Hierarchical data
- Schema flexibility
- Read-heavy with embedded relations
- Geospatial

---
## When MongoDB Loses

- Multi-document ACID at scale
- Reporting / SQL-style analytics
- Heavy joins

---
## Atlas

- Hosted MongoDB
- Free tier
- Multi-cloud
- Default for most teams

---
## Common MongoDB Mistakes

- Modeling like SQL (separate collections everywhere)
- Embedding unbounded arrays
- No schema validation
- Treating MongoDB as a primary store without backup discipline
- ACID expectations from a single-doc-atomic system
