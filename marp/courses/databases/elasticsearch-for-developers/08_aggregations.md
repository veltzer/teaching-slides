---
tags:
  - databases:elasticsearch
  - databases:aggregations
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Aggregations

---

## Aggregation Kinds

![aggregation_kinds](svg/courses/databases/elasticsearch-for-developers/08_aggregations/aggregation_kinds.svg)

---

## What This Chapter Covers

- Bucket aggregations
- Metric aggregations
- Pipeline aggregations
- Sub-aggregations
- Performance

---

## Aggregation Families

![agg_types](svg/courses/databases/elasticsearch-for-developers/08_aggregations/agg_types.svg)

---

## Aggregation Overview

![agg_overview](svg/courses/databases/elasticsearch-for-developers/08_aggregations/agg_overview.svg)

---

## Bucket Aggregations

- Group documents into buckets
- terms, date_histogram, range, filter

---

## Terms Aggregation

```json
{
  "aggs": {
    "by_status": {
      "terms": { "field": "status.keyword", "size": 10 }
    }
  }
}
```

---

## Date Histogram

```json
{
  "aggs": {
    "per_day": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "day"
      }
    }
  }
}
```

---

## Range Aggregation

```json
{
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 50 },
          { "from": 50, "to": 200 },
          { "from": 200 }
        ]
      }
    }
  }
}
```

---

## Metric Aggregations

- sum, avg, min, max, percentiles, cardinality
- Often nested inside buckets

---

## Sub-Aggregations

```json
{
  "aggs": {
    "by_status": {
      "terms": { "field": "status.keyword" },
      "aggs": {
        "avg_total": { "avg": { "field": "total" } }
      }
    }
  }
}
```

---

## Cardinality

- Distinct count
- Approximate (HyperLogLog)
- Cheaper than exact

---

## Percentiles

```json
{ "percentiles": { "field": "latency_ms", "percents": [50, 95, 99] } }
```

- For SLA reporting

---

## Pipeline Aggregations

- Operate on results of other aggregations
- Moving average, derivative, cumulative sum
- Run after the buckets are computed

---

## Filter Aggregation

```json
{ "aggs": {
    "errors": {
      "filter": { "term": { "level": "ERROR" } },
      "aggs": { "count": { "value_count": { "field": "_id" } } }
    }
}}
```

- Pre-filter then aggregate

---

## Composite Aggregation

- For pagination through many buckets
- "All distinct user_id values"
- Page through with composite

---

## Performance

- Aggregations are heavy
- Use filter context to narrow first
- Field type matters: doc_values for fast aggregations
- Cardinality precision_threshold trade-off

---

## Common Aggregation Mistakes

- terms on text field (analysed; weird groups)
- date_histogram with wrong calendar_interval
- Heavy aggregations on huge indexes without filter
- Sub-aggregating to deep depths
- Forgetting to filter first
