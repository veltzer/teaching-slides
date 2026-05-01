---
tags:
  - databases:neo4j
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Modeling

---
## What This Chapter Covers

- Node vs property
- Relationship types
- Hyper-edges
- Time and versioning
- Indexing

---
## When To Make A Node

- Has its own identity
- Has its own relationships
- Could exist independently
- Likely to be queried directly

---
## When To Make A Property

- Adjective of a node
- Not queried alone
- Stable in cardinality
- Tied to one node

---
## Relationship Types

- Use specific types not generic
- Direction matters
- Properties on relationships are fine
- Avoid one type for all edges

---
## Direction

- Most relationships have a natural direction
- Cypher patterns follow direction
- Can match in either direction with -[r]-
- Pick a convention and document

---
## Hyper-Edges

- Relationships connecting more than two
- Modeled as a node with edges out
- Common for events, transactions
- Not as elegant but works

---
## Time And Versions

- Add a node for the event
- Connect to participants
- Properties hold timestamps
- Powerful for histories

---
## Indexes

- B-tree indexes on properties
- Required for fast lookups
- Composite indexes possible
- Run usage stats

---
## Constraints

- Uniqueness
- Existence (Enterprise)
- Property type (Enterprise)
- Drive MERGE correctness

---
## Avoid Property Explosion

- Hundreds of properties on a node hurts
- Move some into related nodes
- Or sub-type with labels
- Profile before optimizing

---
## Labels

- Multi-label allowed
- Use sparingly
- Each label is an index dimension
- Consistent naming convention

---
## Naming Conventions

- Labels CamelCase
- Relationships UPPER_SNAKE_CASE
- Properties camelCase
- Apply across the codebase

---
## Polymorphic Patterns

- Inheritance via labels
- Or via separate types and shared interface
- Choose by query patterns
- Test with realistic data

---
## Common Modeling Mistakes

- Generic relationship type
- Properties for things that are nodes
- Missing unique constraints
- No indexes on lookup keys
- Ignoring growth in degree distribution
