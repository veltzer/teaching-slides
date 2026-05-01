---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Transformation

---
## What This Chapter Covers

- Transform tooling
- Modeling approaches
- Slowly changing dimensions
- Reusability
- Testing

---
## Where to Transform

- In the source: pre-load
- In flight: streaming
- In the warehouse: post-load
- ELT pattern: warehouse wins

---
## SQL-Based Transformation

- Familiar to analysts
- Expressive enough for most cases
- Optimizable by warehouses
- Hard to test without tooling

---
## Code-Based Transformation

- Spark or Pandas or similar engines
- Better for complex logic
- More test-friendly
- Heavier infrastructure

---
## Modeling Approaches

- Star schema
- Snowflake schema
- Wide tables
- Medallion (bronze, silver, gold)

---
## Star Schema

- Fact table at center
- Dimension tables around
- Fewer joins for analysts
- Classic warehouse design

---
## Wide Tables

- Denormalize for query speed
- Simpler analytics
- More storage, more update cost
- Common in lakehouse

---
## Slowly Changing Dimensions

- Type 1: overwrite
- Type 2: history rows
- Type 3: limited history
- Pick by audit needs

---
## Idempotent Transforms

- Re-runnable
- Keyed by partition or version
- Use MERGE patterns
- Required for backfills

---
## Reusability

- Macros and shared models
- Layered builds
- Avoid copy-paste SQL
- Test the shared layer hard

---
## Tests

- Not-null
- Uniqueness
- Referential integrity
- Domain ranges

---
## Documentation

- Column descriptions
- Lineage
- Owners
- Auto-generated where possible

---
## Performance

- Push down to warehouse
- Cluster on filter columns
- Materialize hot models
- Profile slow queries

---
## Common Transformation Mistakes

- One big query
- No layering
- Untested critical paths
- Models without owners
- No documentation
