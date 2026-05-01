---
tags:
  - databases:postgresql
  - languages:plpgsql
level: intermediate
category: databases
audience:
  - audiences:developers

---
# PL/pgSQL Programming

---
## What This Chapter Covers

- What PL/pgSQL is
- Functions
- Procedures
- Control flow
- Triggers
- When to use; when not

---
## What PL/pgSQL Is

- Postgres's procedural language
- SQL embedded in procedural code
- Stored functions and procedures
- Compiled and cached
- "Server-side scripting"

---
## A Simple Function

```sql
CREATE FUNCTION add_one(n INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN n + 1;
END;
$$ LANGUAGE plpgsql;

SELECT add_one(42); -- 43
```

---
## Variables

```sql
CREATE FUNCTION compute() RETURNS INTEGER AS $$
DECLARE
    total INTEGER := 0;
    row_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO row_count FROM users;
    total := row_count * 10;
    RETURN total;
END;
$$ LANGUAGE plpgsql;
```

---
## Control Flow

- IF / THEN / ELSE
- LOOP, WHILE, FOR
- CASE
- RAISE EXCEPTION

---
## Procedures

- Postgres 11+
- Like functions but can COMMIT / ROLLBACK
- Called with CALL not SELECT
- For multi-statement transactions inside

---
## Triggers

```sql
CREATE FUNCTION update_modified()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_modified();
```

- Automatic: on INSERT, UPDATE, DELETE

---
## When To Use Functions

- Complex queries that benefit from procedural logic
- Reused logic across queries
- Constraint enforcement
- Audit triggers

---
## When NOT To

- Business logic better in app code
- Hard to test
- Hard to version-control
- Hard to debug

---
## Performance

- Functions cached (parsed plan)
- Subsequent calls fast
- Long functions: harder to optimise
- INTO for single-value SELECT

---
## Error Handling

```sql
BEGIN
    -- ...
EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'Duplicate; skipping';
    WHEN OTHERS THEN
        RAISE;
END;
```

- Catch specific exceptions
- Or all (OTHERS)

---
## Returning Sets

```sql
CREATE FUNCTION top_users(n INTEGER)
RETURNS TABLE(id INTEGER, name TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name FROM users ORDER BY score DESC LIMIT n;
END;
$$ LANGUAGE plpgsql;
```

- Like a view function
- Reuse in queries

---
## Other PL Languages

- PL/Python: Python in DB
- PL/V8: JavaScript
- PL/R: R for statistics
- Not in Postgres core; extensions
- Similar shape

---
## Common PL/pgSQL Mistakes

- Heavy business logic in DB
- No tests
- Triggers that hide important logic
- Recursive triggers (loops!)
- Forgetting `LANGUAGE plpgsql`
