---
tags:
  - databases:mongodb
  - databases:design
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Document Model and Schema Design

---

## What This Chapter Covers

- Embed vs reference
- Schema patterns
- Anti-patterns
- Schema versioning
- Validation
- Practical guidance

---

## Embed vs Reference

- Embed: nested document
- Reference: ID pointing to another collection
- Embed: simpler reads, atomic updates
- Reference: avoid duplication

---

## Schema Patterns

![schema_patterns](svg/courses/databases/mongodb-for-developers/03_document_model_and_schema_design/schema_patterns.svg)

---

## When To Embed

- One-to-few (3-100)
- Read-mostly
- Updates atomic per document
- Bounded growth

---

## When To Reference

- One-to-many (thousands+)
- Documents shared across many
- Updated independently
- Avoid: 16MB document limit

---

## Embed vs Reference

![embed_vs_reference](svg/courses/databases/mongodb-for-developers/03_document_model_and_schema_design/embed_vs_reference.svg)

---

## Schema Design Decisions

![schema_decisions](svg/courses/databases/mongodb-for-developers/03_document_model_and_schema_design/schema_decisions.svg)

---

## Document Size

- Max: 16MB per document
- Practically: 1MB or less
- Beyond: split or use GridFS
- Watch unbounded arrays

---

## Common Patterns

- **Embedded subdocs**: addresses inside user
- **References**: orders point to user_id
- **Hybrid**: embed common fields, reference details
- **Bucket**: group time-series by hour
- **Outlier**: separate large entries

---

## Schema Versioning

- Add `schema_version` field
- App reads version; handles each
- Migrations: lazy (on read) or batch
- Avoid: "all-or-nothing" migrations on huge collections

---

## Schema Validation

```javascript
db.createCollection("users", {
    validator: {
        $jsonSchema: {
            required: ["email"],
            properties: {
                email: { bsonType: "string" }
            }
        }
    }
});
```

- JSON Schema-based
- Per-collection
- Catches: bad inserts; not catches all bugs

---

## Anti-Patterns

- Massive embedded arrays (unbounded)
- Many references mimicking SQL JOINs
- Same data duplicated everywhere
- Document grows on every write
- Schema-on-read with no app-side checks

---

## Polymorphic Collections

- Different shapes in one collection
- Use a `type` field
- Common in: events, audit logs
- Schema validation harder; deal with it

---

## Time-Series Pattern

- Bucket by time period
- One doc per hour with array of measurements
- Reduces document count; faster queries
- MongoDB 5+: native time-series collections

---

## Polymorphic Documents

- One collection; many shapes
- Filter by `type` field
- Index on `type` for performance
- Common in: events, analytics

---

## Practical Guidance

- Start with embedded; reference when needed
- Document the schema (even if not enforced)
- Plan for evolution (schema_version)
- Watch document size
- Profile query patterns; design for them

---

## Common Schema Mistakes

- Modeling like SQL (separate collections everywhere)
- Embedding unbounded arrays
- No validation; junk accumulates
- Schema-of-the-week (not versioned)
- Designing without knowing query patterns
