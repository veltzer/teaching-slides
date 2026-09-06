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

# Engine Migrations

---

## What This Chapter Covers

- Why change engines
- Compatibility surface
- Replication-based moves
- Dual writes
- Cutover

---

## Why Change

- Cost
- Scale
- Features
- Cloud strategy

---

## Compatibility Surface

- SQL dialect differences
- Function and operator gaps
- Behavior differences (collation, time)
- Driver and ORM behavior

---

## Pre-Migration Audit

- Inventory queries
- Identify incompatibilities
- Estimate change required
- Catalog stored procedures and triggers

---

## Replication-Based

- Source streams to target
- Logical replication preferred
- Initial snapshot plus changes
- Cutover when caught up

---

## Cutover Steps

![cutover_steps](svg/courses/databases/database-migration-strategies/04_engine_migrations/cutover_steps.svg)

---

## Cutover Flow

![replication_cutover](svg/courses/databases/database-migration-strategies/04_engine_migrations/replication_cutover.svg)

---

## Tools

- Built-in logical replication
- Source-specific connectors
- Cloud database migration services
- Custom for unsupported pairs

---

## Dual Writes

- App writes both
- Verify equality
- Reads still source
- Flip when stable

---

## Shadow Reads

- Read both sources
- Compare results
- Alert on divergence
- Useful before full cutover

---

## Behavioral Differences

- Implicit conversions
- Sort order under collation
- NULL semantics
- Date and time arithmetic

---

## Performance Reset

- Old indexes may not fit new engine
- Statistics fresh on target
- Profile real workload
- Tune before cutover

---

## Cutover Plan

- Freeze schema window
- Final delta replication
- Switch app config
- Monitor closely

---

## Rollback Plan

- Keep source running
- Reverse replication if possible
- Cap rollback window
- Document the trigger

---

## Decommission

- Old engine kept warm for weeks
- Then read-only
- Then archived
- Then shut down

---

## Cost and Effort

- Engine moves are months not weeks
- Engineering cost dominates
- Test environments multiply
- Plan accordingly

---

## Common Engine Migration Mistakes

- No pre-audit
- Underestimating SQL differences
- One big bang cutover
- No rollback plan
- Skipping shadow reads
