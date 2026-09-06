---
tags:
  - databases:mongodb
  - architecture:patterns
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Application Patterns

---

## What This Chapter Covers

- Embed vs reference revisited
- Outlier pattern
- Bucket pattern
- Computed pattern
- Subset pattern
- Schema versioning

---

## Common Patterns

![app_patterns](svg/courses/databases/mongodb-for-developers/13_application_patterns/app_patterns.svg)

---

## Embed Pattern

- Related data inside parent document
- Atomic updates
- One read fetches all
- "User and addresses"

---

## Reference Pattern

- ID pointer to another document
- Use $lookup or app-side join
- "Order references Product by id"

---

## Outlier Pattern

- Most documents fit one shape
- Some have unusual data
- Store outliers separately
- Avoid: fitting one big schema for the worst case

---

## Bucket Pattern

- Time-series; group readings into buckets
- One doc per hour with array of readings
- Reduces document count
- Faster queries on time ranges

---

## Computed Pattern

- Pre-compute expensive aggregates
- Store as a field
- Update on relevant writes
- Trade write complexity for read speed

---

## Subset Pattern

- Most docs need a subset of related data
- Embed the subset
- Keep full data in another collection
- "User has top 3 reviews embedded; full reviews elsewhere"

---

## Extended Reference

- Reference + duplicate frequently-needed fields
- "Order has product_id and product_name"
- Avoid: needing to look up name on every order
- Sync challenges if name changes

---

## Schema Versioning

- `schema_version` field
- App handles each version
- Migrate lazily
- Avoids: massive rewrite migrations

---

## Polymorphic Schema

- One collection; multiple shapes
- `type` field discriminates
- Index on `type`
- Common in events, messages

---

## Tree Patterns

- Parent reference: `parent_id`
- Materialised path: `path: "/root/branch/"`
- Children array: `children: [...ids]`
- Each: trade-offs in query / update

---

## Approximate Pattern

- Counter approximations
- Don't increment on every event
- Sample 1 of N; multiply
- Trade precision for write throughput

---

## Tree Of Categories

- Often: materialised path for fast ancestor queries
- Or: separate ancestor table
- Updates on move are expensive
- Read-heavy &#8594; simpler patterns work

---

## Multi-Tenant

- Per-tenant database vs per-tenant field
- Per-tenant DB: isolation; harder to operate
- Per-tenant field: easier; share queries
- Pick based on isolation requirements

---

## Common Pattern Mistakes

- One pattern for everything
- Embedding unbounded arrays
- Reference where embedded would do
- Polymorphic without `type` index
- Schema-of-the-week
