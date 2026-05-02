---
tags:
  - databases:postgresql
  - databases:partitioning
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Table Partitioning

---
## Strategies

![partition_strategies](svg/courses/databases/postgresql-for-developers/07_table_partitioning/partition_strategies.svg)

---
## What This Chapter Covers

- What partitioning is
- Range, list, hash
- Declarative partitioning
- Pruning
- Maintenance
- When to partition

---
## What Partitioning Is

- Split a table into pieces
- Each piece is a separate table physically
- Logical view: one big table
- Postgres: declarative partitioning since v10

---
## Range Partitioning

```sql
CREATE TABLE events (id BIGINT, occurred_at TIMESTAMPTZ, ...)
PARTITION BY RANGE (occurred_at);

CREATE TABLE events_2026 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

- By date is most common
- Drop old partitions cheaply

---
## List Partitioning

```sql
PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('US');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('EU');
```

- Discrete categories
- Region, status, type

---
## Hash Partitioning

```sql
PARTITION BY HASH (user_id);

CREATE TABLE orders_p0 PARTITION OF orders FOR VALUES WITH (modulus 4, remainder 0);
```

- Even distribution
- Good for: write distribution

---
## Partition Pruning

- Planner skips partitions that can't match WHERE
- Massive speedup for large tables
- Requires WHERE on partition key

---
## Constraint Exclusion

- Older mechanism
- Replaced by declarative partition pruning
- For non-declarative inheritance, still relevant

---
## Adding A Partition

- Each new period: create a new partition
- Automate: pg_partman extension
- Or: cron job to create monthly

---
## Detaching Partitions

- DETACH PARTITION
- Becomes a regular table
- Useful for archiving / dropping old data

---
## Indexes On Partitions

- Index per partition
- Or: partitioned index (Postgres 11+)
- Auto-applied to new partitions

---
## Constraints

- Primary key must include partition key
- Foreign keys with partitioning: limitations
- Plan accordingly

---
## When To Partition

- Tables &gt; 100M rows
- Time-series data
- Multi-tenant by tenant ID
- Need to drop old data fast

---
## When NOT To

- Small tables
- Most queries don't filter by partition key
- Cross-partition queries dominate
- Premature; not free

---
## Common Partitioning Mistakes

- Partitioning small tables
- Missing partition for new data (errors)
- Wrong partition key for query patterns
- No automation; partitions backlog
- Forgetting cross-partition limitations
