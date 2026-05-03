---
tags:
  - databases:migrations
  - practices:migration
level: intermediate
category: databases
audience:
  - audiences:dba
  - audiences:architects

---
# Schema Migrations

---
## What This Chapter Covers

- Online vs offline
- Locking
- Add and drop columns
- Index creation
- Tools

---
## Online vs Offline

- Online: traffic continues
- Offline: maintenance window
- Most modern engines support online for many operations
- Some operations still lock heavily

---
## Online Phases

![online_phases](svg/courses/databases/database-migration-strategies/02_schema_migrations/online_phases.svg)

---
## Locking Levels

- Exclusive: blocks reads and writes
- Shared: allows reads
- Metadata locks block schema changes too
- Inspect before running

---
## Change Safety

![safe_changes](svg/courses/databases/database-migration-strategies/02_schema_migrations/safe_changes.svg)

---
## Adding a Column

- Default null is fast
- Default with value can be slow
- Modern engines optimize this
- Always test on a clone

---
## Removing a Column

- Two-step approach safer
- Stop reading, deploy, then drop
- Drop with care
- Track who reads what

---
## Renaming a Column

- Atomic in some engines, not others
- Application must be ready
- Two-name window often easier
- Avoid renames if you can

---
## Type Changes

- Often rewrite the table
- Long lock or long time
- Add new column, backfill, swap
- Then drop old

---
## Index Creation

- Online builders in modern engines
- Lock-free or near it
- Slow but safe
- Plan during low traffic

---
## Long-Running Migrations

- Track progress
- Resumable preferred
- Watch replication lag
- Cancel safely if needed

---
## Tooling

- Rails migrations
- Flyway, Liquibase
- ghost, gh-ost for MySQL
- Native commands where adequate

---
## Idempotency

- IF NOT EXISTS guards
- Repeatable across environments
- Track applied versions
- Skip if already there

---
## Reviewing Migrations

- DBA review for risky ones
- Lint for known traps
- Run on staging with traffic
- Time the operation

---
## CI Pipelines

- Run migrations on test DB
- Verify forward and rollback
- Block PRs on failure
- Provide a dry-run

---
## Common Schema Mistakes

- ADD COLUMN with default on huge table
- Renaming without planning
- Lock-heavy changes during peak
- No CI for migrations
- No rollback path
