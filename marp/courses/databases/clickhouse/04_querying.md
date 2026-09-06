---
tags:
  - databases:clickhouse
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---

# Querying

---

## What This Chapter Covers

- SQL dialect notes
- Aggregations
- Joins
- Skip indexes
- Optimization

---

## SQL Dialect

- Mostly familiar
- Many extensions
- Array and map functions powerful
- Lambdas inline

---

## Query Patterns

![query_patterns](svg/courses/databases/clickhouse/04_querying/query_patterns.svg)

---

## Aggregations

- Standard sum, count, avg
- Cardinality functions
- Approximate where exact is too costly
- Aggregate states for materialized views

---

## Approximate Functions

- Sketch-based unique counters
- Sketch-based quantiles
- Trade exact for cheap
- Document tolerance

---

## Joins

- Hash join default
- Sort-merge for big-vs-big
- Distributed needs locality plan
- Mind memory cost

---

## Distributed Joins

- Subquery push-down works
- Joins between shards expensive
- Replicate small tables
- Or denormalize at write

---

## Array Join

- Expand array column to rows
- Like a lateral join elsewhere
- Powerful for events with sub-records
- Watch row blowup

---

## Window Functions

- Standard SQL syntax
- Useful for session analysis
- Watch memory on big partitions
- Combine with sort key for streams

---

## Skip Indexes

- Min-max, set, n-gram, token bloom
- Skip granules at scan time
- Cheaper than full secondary index
- Define per filter pattern

---

## Pruning Visualized

![skip_indexes](svg/courses/databases/clickhouse/04_querying/skip_indexes.svg)

---

## Settings

- Per-query overrides
- Memory limits
- Max threads
- Timeout

---

## Plan Inspection

- Explain syntax variants
- System logs capture everything
- Profile to find hot operators
- Iterate

---

## Common Optimization Steps

- Add sort-key columns to filter
- Convert string columns to low-cardinality types
- Use materialized view for hot pre-aggregations
- Avoid star-select

---

## Pitfalls

- Hash join blowing memory
- The final modifier in latency-sensitive paths
- Functions cast on filter columns
- Sorting huge result sets

---

## Common Querying Mistakes

- Star-select in dashboards
- Function calls on filter columns
- Joins where denormalize would do
- No skip indexes for common filters
- Ignoring query log
