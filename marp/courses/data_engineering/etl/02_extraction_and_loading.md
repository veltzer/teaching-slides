---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Extraction and Loading

---

## What This Chapter Covers

- Source types
- Full vs incremental
- Change data capture
- Loading strategies
- Idempotency

---

## Database Sources

- JDBC and ODBC
- Bulk export
- Logical replication
- Change feeds

---

## File Sources

- Local
- Network shares
- Object storage
- FTP, SFTP

---

## API Sources

- REST and GraphQL
- Pagination required
- Rate limits
- Authentication churn

---

## Stream Sources

- Kafka and friends
- Continuous flow
- Offsets must be tracked
- Idempotent writers required

---

## Full Extract

- Re-read everything
- Simple, expensive
- Useful for small tables
- Captures hard deletes

---

## Incremental Extract

- Only new and changed rows
- Watermark column needed
- Misses hard deletes
- Cheaper at scale

---

## Change Data Capture

- Source emits changes
- Captures inserts, updates, deletes
- Requires source support
- Latency in seconds

---

## CDC Flow

![cdc_flow](svg/courses/data_engineering/etl/02_extraction_and_loading/cdc_flow.svg)

---

## Loading Modes

- Append
- Overwrite
- Merge
- Truncate and reload

---

## Modes Compared

![load_modes](svg/courses/data_engineering/etl/02_extraction_and_loading/load_modes.svg)

---

## Bulk Loading

- Use the warehouse loader
- Stage files first
- Load in parallel
- Avoid row-by-row inserts

---

## Idempotency

- Re-running yields same result
- Use natural keys
- Or stage and merge
- Required for safe retries

---

## Backfills

- Reload old data
- Often partitioned by time
- Resumable
- Validate after

---

## Late-Arriving Data

- Out-of-order rows
- Update past partitions
- Use merge logic
- Track lateness metrics

---

## Common Loading Mistakes

- Row-by-row inserts at scale
- No watermark for incremental
- Missing hard-delete handling
- Backfill without partition strategy
- No idempotency
