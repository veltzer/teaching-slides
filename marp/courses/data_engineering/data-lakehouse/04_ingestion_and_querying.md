---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers
  - audiences:architects

---
# Ingestion and Querying

---
## What This Chapter Covers

- Batch ingestion
- Streaming ingestion
- Change data capture
- Query engines
- Optimization

---
## Batch Ingestion

- Periodic copy from source
- Full snapshots or incremental
- Simple and reliable
- Latency in hours

---
## Streaming Ingestion

- Continuous from source
- Latency in seconds
- More complex to operate
- Requires idempotent writers

---
## Change Data Capture

- Source database emits changes
- Captured to a stream
- Applied to lakehouse table
- Mirrors source within seconds

---
## Bronze, Silver, Gold

- Bronze: raw landing
- Silver: cleaned and conformed
- Gold: business-ready
- Each with own SLA

---
## Bronze Properties

- Append-only
- Lineage to source
- Minimal transformation
- Immutable history

---
## Silver Properties

- Schema enforced
- Quality checked
- Joined with reference data
- Consumer-friendly

---
## Gold Properties

- Aggregated for BI
- Domain models
- Tuned for query speed
- Often materialized

---
## Query Engines

- Spark
- Trino, Presto
- Athena, BigQuery, Snowflake on open tables
- Choose by workload

---
## SQL on Files

- Engines push predicates to storage
- Columnar pruning
- Partition pruning
- Statistics drive plans

---
## Optimization

- Compaction
- Z-ordering or clustering
- Materialized views
- Cache hot scans

---
## Cost Awareness

- Compute is metered
- Storage is metered
- Egress is metered
- Tag and chargeback

---
## Federated Queries

- Join lakehouse with external sources
- Useful for late-binding integration
- Watch for performance cliffs
- Push compute down

---
## Common Ingestion Mistakes

- No backfill plan
- Streaming without idempotency
- One layer instead of bronze-silver-gold
- No data quality checks
- Treating ingest as one-time
