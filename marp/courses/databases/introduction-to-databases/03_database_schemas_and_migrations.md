---
tags:
  - databases:schemas
  - databases:migrations
level: beginner
category: databases
audience:
  - audiences:developers

---
# Database Schemas and Migrations

---
## Migration Workflow

![migration_workflow](svg/courses/databases/introduction-to-databases/03_database_schemas_and_migrations/migration_workflow.svg)

---
## What This Chapter Covers

- Schema definition
- DDL vs DML
- Migrations
- Schema evolution
- Tools: Flyway, Liquibase, Alembic, Knex
- Best practices

---
## Schema Definition

- DDL: CREATE TABLE, ALTER TABLE, DROP TABLE
- Defines structure
- Database stores it as metadata

---
## DDL vs DML

- **DDL**: structure (CREATE, ALTER, DROP)
- **DML**: data (SELECT, INSERT, UPDATE, DELETE)
- Different permissions, different concerns

---
## Schema Migrations

- Versioned changes to the schema
- Track which migrations have been applied
- Forward (up) and reverse (down) where possible
- Standard for app deployment

---
## A Migration Tool

- Flyway (Java), Liquibase (multi-language)
- Alembic (Python)
- Knex / Sequelize migrations (Node)
- Each: similar shape

---
## A Sample Migration

```sql
-- 001_create_users.sql (up)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 001_create_users.down.sql
DROP TABLE users;
```

---
## Migration Order

- Each migration has a unique ID / timestamp
- Tool tracks applied ones
- Applies in order
- Idempotent: re-running is safe

---
## Schema Evolution

- Add column: usually safe (with default)
- Remove column: deploy in two phases
- Rename: deploy in three phases (add, copy, remove)
- Type change: case-by-case

---
## Two-Phase Deploy For Removal

- Phase 1: deploy code that doesn't use the column
- Phase 2: drop the column
- Avoids: app breaks because column gone

---
## Online Migrations

- Big tables: ALTER TABLE blocks
- Tools: pt-online-schema-change, gh-ost
- Or: build a new table; migrate; swap
- Critical for prod systems

---
## Expand-Backfill-Switch-Contract

![online_migration_steps](svg/courses/databases/introduction-to-databases/03_database_schemas_and_migrations/online_migration.svg)

---
## CI / CD

- Migrations run on deploy
- Or: as a separate pre-deploy step
- Test on staging first
- Rollback strategy: forward fix usually beats down migration

---
## Schema In Code

- Migrations live in source repo
- Reviewed in PRs
- Applied automatically by deployment
- Source of truth for schema

---
## Versioning

- Each migration: numbered or timestamped
- Most tools: track in a migrations table
- "schema_migrations": table with applied IDs

---
## Common Migration Mistakes

- Manual changes in production (drift)
- No down migration; can't rollback
- Long-running migrations during peak traffic
- No tests before applying
- One huge migration; should be many small ones
