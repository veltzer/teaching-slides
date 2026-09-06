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

# Data Migrations

---

## What This Chapter Covers

- Backfills
- Live transformations
- Dual writes
- Reconciliation
- Late-arriving data

---

## Backfill

- Populate new structure with old data
- Often partitioned by id or time
- Resumable
- Idempotent

---

## Backfill Strategy

- Small batches
- Throttled by time or rows
- Watch replica lag
- Pause on errors

---

## Backfill Modes

![backfill_modes](svg/courses/databases/database-migration-strategies/03_data_migrations/backfill_modes.svg)

---

## Live Transformation

- Application writes new format
- Old format also kept until cutover
- Or trigger maintains parity
- Pick by safety needs

---

## Triggers For Parity

- Database trigger updates new column
- Logical equivalent in app code
- App code is easier to deploy
- Triggers cost performance

---

## Dual Writes

- App writes both old and new
- Reads still old
- Flip when ready
- Common for engine moves

---

## Reconciliation

- Compare old and new
- By count
- By hash
- By sample

---

## Backfill and Reconciliation

![backfill_recon](svg/courses/databases/database-migration-strategies/03_data_migrations/backfill_recon.svg)

---

## Inconsistencies

- Find differences
- Investigate causes
- Fix application path or migration code
- Repeat until clean

---

## Late-Arriving Data

- Old code paths still write old format
- Migration must catch up
- Run reconciliation regularly
- Cut over only when caught up

---

## Partition-By-Time Backfill

- Process oldest first
- Or newest first
- Track watermark
- Easy to resume

---

## Throughput Control

- Rows per second cap
- Pauses on lag
- Off-peak preferred
- Auto-throttle on errors

---

## Failure Recovery

- Treat backfill as a job
- Retry on transient errors
- Stop on persistent
- Resume from last checkpoint

---

## Verification Before Cutover

- Reconciliation must pass
- Consumers tested on new format
- Read traffic switched gradually
- Rollback documented

---

## Common Data Migration Mistakes

- One huge batch
- No throttling
- No reconciliation
- Skipping late-arriving cases
- Dropping old data too early
