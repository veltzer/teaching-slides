---
tags:
  - observability:prometheus
level: intermediate
category: observability
audience:
  - audiences:devops

---

# PromQL

---

## PromQL Building Blocks

![promql_examples](svg/courses/observability_and_monitoring/prometheus-and-grafana/03_promql/promql_examples.svg)

---

## What This Chapter Covers

- Selectors
- Operators
- Functions
- Aggregations
- Common patterns

---

## Instant vs Range Vectors

- Instant: one value per series at a moment
- Range: values over a time window
- Functions need one or the other

---

## Selectors

```promql
http_requests_total
http_requests_total{method="GET"}
http_requests_total{method!="POST"}
http_requests_total{path=~"/api/.*"}
```

- =, !=, =~, !~
- Filter by labels

---

## Range Vector

```promql
http_requests_total[5m]
```

- Last 5 minutes of values
- Input to rate, increase, etc.

---

## rate()

```promql
rate(http_requests_total[5m])
```

- Per-second rate
- Standard for counters
- Range vector input; instant output

---

## increase()

- Total increase over range
- Less common than rate
- Watch for resets

---

## PromQL Function Families

![promql_functions](svg/courses/observability_and_monitoring/prometheus-and-grafana/03_promql/promql_functions.svg)

---

## Aggregations

```promql
sum(rate(http_requests_total[5m]))
sum by (status) (rate(http_requests_total[5m]))
```

- sum, avg, min, max, count
- Group by labels with `by`

---

## Histograms and Quantiles

```promql
histogram_quantile(0.95,
    sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```

- Compute percentiles from buckets
- Common for SLOs

---

## Math Operators

```promql
node_memory_used_bytes / node_memory_total_bytes
```

- Match by labels
- Useful for ratios

---

## Comparison

```promql
node_cpu_seconds_total > 100
```

- Filter to series above threshold
- Used in alerts

---

## offset

```promql
http_requests_total offset 1h
```

- Look at past data
- Compare now vs an hour ago

---

## Recording Rules

- Pre-compute expensive queries
- Run on interval
- Reduce dashboard load

---

## Sample Recording Rule

```yaml
groups:
  - name: app
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))
```

- Defined in rules file
- Loaded by Prometheus

---

## Common PromQL Mistakes

- avg() on counters without rate first
- Wrong window for rate (too short, noisy; too long, lagging)
- Mixing histogram_quantile with avg
- Forgetting `by` for proper grouping
- Recording-rule names that don't reflect their content
