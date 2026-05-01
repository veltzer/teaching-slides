---
tags:
  - databases:postgresql
  - databases:jsonb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# JSONB and Semi-Structured Data

---
## What This Chapter Covers

- JSONB vs JSON
- Operators
- Querying nested data
- Indexing JSONB
- When to use it
- When NOT to

---
## JSONB

- Binary JSON
- Indexable
- Faster to read
- Slightly slower to write than text
- The default for JSON in modern Postgres

---
## JSON Operators

- `->`: get JSON object field
- `->>`: get field as text
- `#>`: nested path; returns JSON
- `#>>`: nested path; returns text
- `@>`: contains
- `?`: key exists

---
## Examples

```sql
SELECT data->'address'->>'city' FROM users;
SELECT * FROM events WHERE data @> '{"type": "click"}';
SELECT * FROM users WHERE data ? 'verified';
```

- Read fields out
- Filter by JSON content
- Check key existence

---
## GIN Index For JSONB

```sql
CREATE INDEX idx_data ON events USING GIN (data);
```

- Index entire JSON
- Containment queries (`@>`) fast
- Larger than B-tree

---
## Path-Specific Index

```sql
CREATE INDEX idx_data_type ON events ((data->>'type'));
```

- Index a specific field
- Smaller than full GIN
- Only that field's queries benefit

---
## When To Use JSONB

- Schemaless / heterogeneous data
- Don't know fields up front
- Many sparse fields
- Storing third-party API responses
- Flexible audit / event payloads

---
## When NOT To

- Well-structured, predictable schema
- Frequent queries on individual fields
- Joins between fields
- Postgres can do; relational columns are usually better

---
## Updates In JSONB

- `jsonb_set(data, '{key}', '"value"')`
- Whole JSONB rewritten on update
- Frequent partial updates: expensive
- Consider relational columns for hot fields

---
## JSONB In Tables

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    data JSONB NOT NULL
);
```

- One JSONB column among others
- Common pattern

---
## Hybrid Schema

- Common fields as columns
- Rare / variable fields in JSONB
- Best of both worlds
- Most pragmatic

---
## Validation

- Postgres doesn't validate schema of JSONB by default
- CHECK constraints can validate
- Or: app-level validation
- JSON Schema extensions exist

---
## Performance Tips

- Index only what you query
- Avoid `jsonb_set` in hot paths if possible
- Use generated columns for frequent extractions
- Profile JSONB query plans

---
## Common JSONB Mistakes

- Schemaless when relational would do
- No validation; junk accumulates
- `jsonb_set` in tight loops
- Over-indexing JSONB (huge GIN indexes)
- Querying by deep nested keys without path indexes
