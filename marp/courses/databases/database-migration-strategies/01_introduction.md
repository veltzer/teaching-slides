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
# Introduction to Database Migrations

---
## What This Chapter Covers

- What database migration is
- Schema vs data
- Why it is risky
- Common patterns
- Course outline

---
## What Migration Means

- Changing schema
- Moving data
- Changing engines
- Often all three at once

---
## Schema Migration

- Adding, removing, altering columns
- Adding indexes
- Renaming tables
- Online or offline

---
## Data Migration

- Moving rows from old to new
- Reformatting fields
- Backfilling computed columns
- Across engines too

---
## Engine Migration

- Switching database product
- Mostly data plus schema
- Application changes too
- Hardest of the three

---
## Why It Is Risky

- Data is the canonical source
- Can corrupt silently
- Downtime impacts revenue
- Harder than re-deploying code

---
## Categories of Pain

- Type changes
- Constraint changes
- Long-running locks
- Compatibility breaks

---
## Strategy Spectrum

- Big bang
- Online schema change
- Dual writes
- Replication-based

---
## Strategy Spectrum Visualized

![migration_spectrum](svg/courses/databases/database-migration-strategies/01_introduction/migration_spectrum.svg)

---
## Big Bang

- Stop, change, start
- Predictable outage
- Simple to plan
- Bad for tier-1

---
## Online Migrations

- Application keeps running
- Schema changes incrementally
- Tools assist
- Default for production

---
## Dual Writes

- Application writes both
- Verify equality
- Flip reads when ready
- For engine changes mainly

---
## Tools

- Rails-style migrations
- Flyway, Liquibase
- pt-online-schema-change for MySQL
- Native online DDL in modern engines

---
## Course Outline

- Schema migrations
- Data migrations
- Engine migrations
- Rollout
- Verification

---
## Common Misconceptions

- "It is just a column add"
- "Backups are enough rollback"
- "We can migrate during a meeting"
- "We do not need a freeze"
- "The application will not notice"
