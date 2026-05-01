---
tags:
  - observability:grafana
level: beginner
category: observability
audience:
  - audiences:devops

---
# Panels and Queries

---
## What This Chapter Covers

- Panel types
- Writing queries
- Transformations
- Field options
- Annotations

---
## Time Series Panel

- Default for metrics
- Plot value over time
- Multiple series in one
- Most-used panel type

---
## Stat Panel

- Single big number
- Trend sparkline
- Useful for KPIs
- Pick units carefully

---
## Gauge

- Bounded scalar
- Thresholds for color
- Useful for utilization
- Less precise than time series

---
## Table

- Rows and columns of data
- Useful for status views
- Conditional formatting
- Sortable

---
## Bar Gauge

- Compare values across rows
- Good for top-N
- Logical scale options
- Compact display

---
## Logs Panel

- Stream of log lines
- Filter and search
- Linked to traces
- Time-aligned with metrics

---
## Heatmap

- Distribution over time
- Useful for latency histograms
- Y-axis as bucket
- Color as count

---
## Writing Queries

- Per-source query language
- Helpers in UI
- Preview before saving
- Save with descriptive name

---
## Variables In Queries

- Dollar-sign substitution
- Multi-value supported
- Cascading variables
- Test all combinations

---
## Transformations

- Post-process query results
- Join, filter, calculate
- Done in browser
- Avoid for huge datasets

---
## Field Options

- Units, decimals
- Min and max
- Color thresholds
- Override per series

---
## Annotations

- Mark events on time series
- Releases, incidents
- Pulled from a query
- Useful for context

---
## Tooltip

- On hover
- Multi-series mode
- Shared across panels
- Easier debugging

---
## Common Panel Mistakes

- Wrong unit
- Default time range
- Too many series in one panel
- No description on panels
- Hardcoded filters
