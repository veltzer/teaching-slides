---
tags:
  - databases:elasticsearch
  - databases:esql
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Elasticsearch Query Language (ES|QL)

---

## Elasticsearch Query Language Capabilities

![esql_capabilities](svg/courses/databases/elasticsearch-for-developers/07_elasticsearch_query_language_es_ql/esql_capabilities.svg)

---
## What This Chapter Covers

- What ES|QL is
- Pipe-based syntax
- Common commands
- Aggregations
- ES|QL vs Query DSL
- When to use it

---
## What ES|QL Is

- A new query language for Elasticsearch
- Pipe-based; SQL-inspired
- Released in 8.11+
- Aimed at: easier complex queries
- Complements (doesn't replace) Query DSL

---
## Pipe Syntax

```misc
FROM logs
| WHERE status == "error"
| STATS count = COUNT(*) BY service
| SORT count DESC
| LIMIT 10
```

- Each `|` is a step
- Output of step is input of next
- Like Unix pipes

---
## FROM

- Source index or pattern
- `FROM logs-*` for date-based indexes

---
## WHERE

- Filter rows
- `WHERE status == "error"`
- `WHERE timestamp > NOW() - 1h`

---
## STATS

- Aggregations
- `STATS count = COUNT(*) BY service`
- BY: grouping
- Multiple aggregations possible

---
## EVAL

- Add computed fields
- `EVAL duration_seconds = duration / 1000`

---
## SORT, LIMIT

- Like SQL
- After STATS or alone

---
## DROP, KEEP

- Project columns
- `KEEP name, status`
- `DROP internal_field`

---
## ENRICH

- Join with another dataset
- Pre-loaded enrich indexes
- Useful for: geoip, user-agent parsing

---
## Comparison With Query DSL

- DSL: full-text relevance, scoring, complex bool logic
- ES|QL: tabular analytics, aggregations, computed fields
- ES|QL doesn't replace DSL for relevance search
- Use both for different needs

---
## When To Use ES|QL

- Log analysis
- Tabular reports
- Computed columns
- Easier to read for SQL-trained users
- Quick ad-hoc queries

---
## When To Stick With DSL

- Full-text search with relevance
- Complex bool queries
- Standard search-engine workloads

---
## Limitations

- Newer; some operations missing
- Performance varies by query
- Not all Lucene features exposed
- Maturing rapidly

---
## Common ES|QL Mistakes

- Using for full-text where DSL is better
- Forgetting that aggregations after pipe
- No LIMIT on huge indexes
- Overusing EVAL when better at index-time
- Comparing performance to DSL incorrectly
