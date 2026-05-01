---
tags:
  - architecting:patterns
level: intermediate
category: architecting
audience:
  - audiences:architects

---
# Data Migration

---
## What This Chapter Covers

- Why data is the hardest part
- Migration patterns
- Dual writes
- Backfills
- Cutover

---
## Why Data Is Hardest

- Cannot be re-deployed
- Wrong data is corruption
- Volumes can be huge
- Schemas drift over time

---
## Inventory First

- Sources, sinks, owners
- Schemas and constraints
- Volumes and growth rates
- Sensitivity tags

---
## Patterns

- Big bang
- Trickle
- Dual write
- Read replica then promote

---
## Big Bang

- Stop, copy, start
- Predictable outage
- Rollback is restore
- Acceptable for small systems only

---
## Trickle

- Continuous flow old to new
- Long coexistence
- Lower risk per step
- More moving parts

---
## Dual Write

- Application writes both
- Reads from one
- Verify equality
- Flip reads when ready

---
## Read Replica Promotion

- Replicate from old to new
- Promote new when caught up
- Cutover by config
- Common with database upgrades

---
## Backfill

- Historical rows copied
- Often partitioned by time
- Resumable
- Track progress

---
## Reconciliation

- Compare old vs new
- By count, by hash, by sample
- Diff drives fixes
- Required before cutover

---
## Schema Differences

- Map fields explicitly
- Handle defaults and nulls
- Coerce types carefully
- Test edge cases

---
## Encoding and Time Zones

- Character encodings differ
- Time zones cause silent corruption
- Normalize early
- Add tests for known offenders

---
## Cutover Window

- Plan the freeze
- Final delta migration
- Verify before flip
- Communicate to users

---
## Common Data Migration Mistakes

- No reconciliation
- No backfill plan
- Schema mismatch found late
- Untested rollback
- No data freeze plan
