---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Loading and Unloading

---
## What This Chapter Covers

- Stages
- COPY INTO
- File formats
- Snowpipe
- Unloading

---
## Stages

- Pointers to files
- Internal or external
- Used by COPY commands
- Permissions per stage

---
## Internal Stages

- Snowflake-managed
- Per-table, per-user, named
- PUT command uploads files
- Handy for ad-hoc loads

---
## External Stages

- Point at object storage
- Reuse existing data lake
- Authentication via IAM or keys
- Common in production

---
## File Formats

- CSV, JSON, Parquet, Avro, ORC
- Format object stores parsing rules
- Reuse across loads
- Test formats before bulk runs

---
## COPY INTO

- Bulk load command
- Reads from stage to table
- Parallel by file
- Tracks loaded files

---
## Load Validation

- VALIDATION_MODE for dry run
- Error counts per file
- Bad files quarantined
- Track in load history

---
## Idempotent Loads

- Same file loaded twice is skipped by default
- Override with FORCE if needed
- Hashes track files
- Important for retries

---
## Snowpipe

- Continuous loading
- Triggered by file arrival
- Serverless compute
- Per-file billing

---
## Snowpipe Flow

![snowpipe_flow](svg/courses/data_engineering/snowflake/03_loading_and_unloading/snowpipe_flow.svg)

---
## Snowpipe Streaming

- API-based ingest
- Lower latency than file-based
- Suits event streams
- Watches connection health

---
## Unloading

- COPY INTO stage
- Files written to object storage
- Use for archival or sharing
- File format chosen at unload

---
## Performance Tips

- Many medium files beat few huge ones
- Compress with ZSTD or GZIP
- Match format to source
- Pre-sort for cluster-friendly loads

---
## Permissions

- USAGE on stage
- INSERT on table
- Use roles for groups of pipelines
- Avoid raw user privileges

---
## Common Loading Mistakes

- Single huge file
- No format reuse
- No load history checks
- FORCE to bypass dedup
- Mixing file formats per stage
