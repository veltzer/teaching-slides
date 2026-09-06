---
tags:
  - data-and-ai:pivot-tables
  - data-and-ai:excel
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---

# Pivot Tables

---

## What This Chapter Covers

- What a pivot table is
- Building one
- Configuring rows, columns, values, filters
- Calculated fields
- Pivot charts
- Cross-tabulation analysis
- When pivot tables are the right tool (and when they aren't)

---

## What a Pivot Table Is

- A *cross-tabulation* of one or more rows by one or more columns
- Aggregates a third value (sum, count, average) at each intersection
- Built into Excel, Google Sheets, and most analytics tools
- Same idea as `GROUP BY` in SQL or `pivot_table` in pandas
- The most-used spreadsheet feature for analysis

---

## Anatomy

![pivot_anatomy](svg/courses/data_science/data-analyst-fundamentals/10_pivot_tables/pivot_anatomy.svg)

---

## A Concrete Example

- Source: orders table with `country`, `month`, `amount`
- Pivot: countries as rows, months as columns, sum of amount in cells
- Result: a quick view of "where and when revenue happened"
- Same data could be viewed many ways — that's the power
- One source, many views, no data duplication

---

## Building One in Excel

- Select your data
- Insert &#8594; PivotTable
- Drag fields into:
    - **Rows**: dimensions (categories along the side)
    - **Columns**: dimensions (categories along the top)
    - **Values**: numeric to aggregate
    - **Filters**: dimensions you want to filter on

---

## Building One in Google Sheets

- Data &#8594; Pivot table
- Same idea, slightly different UI
- Data updates: refresh manually or use a fresh range
- Free, collaborative, lower performance than Excel on big data

---

## Aggregation Functions

- Sum (default for numeric)
- Count
- Average
- Min, Max
- Count Distinct
- Custom: by formula
- Click the field in Values &#8594; Value Field Settings &#8594; Summarize by

---

## Showing Values As

- Raw value: the aggregate
- Percentage of total: each cell as % of grand total
- Percentage of row: each cell as % of its row
- Percentage of column: each cell as % of its column
- Difference from another column: e.g., this month vs last
- Right-click a value &#8594; Show Values As

---

## Sorting and Filtering

- Sort rows by a value column (descending revenue per country)
- Filter to top-N within a dimension
- Slicers: clickable filter buttons on top of the pivot
- Slicer + chart = a dashboard prototype
- Especially powerful in Excel Online and Power BI

---

## Calculated Fields

- Compute a new metric in the pivot, not the source
- Insert &#8594; Calculated Field (Excel) or "Formula" (Sheets)
- `Profit Margin = Profit / Revenue`
- The new field can then be aggregated like any other
- Centralises logic; multiple pivots can reuse

---

## Calculated Items

- Combine pivot row/column values
- Example: combine "Q1" and "Q2" into "H1"
- Less common; usually a calculated field is enough
- Can confuse downstream consumers — use sparingly

---

## Pivot Charts

- Insert a chart linked to the pivot
- Chart updates as the pivot updates
- Filter the pivot &#8594; chart filters too
- Bar / column / line charts work best
- Pie charts: same warnings as elsewhere

---

## Cross-Tabulation

- Two categorical dimensions vs each other
- Useful for: "users by country and plan type"
- Heatmap formatting reveals patterns
- Combined with calculated percentages: powerful diagnostics
- Shows up in surveys, demographics, support analysis

---

## Drill-Down

- Double-click a pivot value
- Excel creates a new sheet with the underlying rows
- Verifies your aggregations
- Spot-check stakeholder questions: "show me which orders contributed"
- Audit trail in one click

---

## Refreshing Pivot Data

- Source data changes &#8594; right-click pivot &#8594; Refresh
- Set "refresh on open" if data is in a sheet
- Pivots from external sources: configure refresh schedule
- A pivot that doesn't reflect current data is worse than no pivot

---

## When To Use Pivot Tables

- Quick exploration with non-technical stakeholders
- Aggregate views of medium-sized data
- Building a dashboard prototype
- Cross-tabulation analysis
- Any time someone asks "can you slice this by X?"

---

## When NOT to Use Them

- Datasets over a few hundred thousand rows (gets slow)
- Operations requiring complex joins (use SQL)
- Reproducible production reporting (use a notebook or BI tool)
- Multi-analyst collaboration on logic (version control issues)
- Pivot tables don't replace SQL or pandas — they complement

---

## Common Mistakes

- Building elaborate pivots on data that won't be refreshed
- Copy-pasting pivot output and losing the underlying logic
- Ignoring stale data — pivots show what was, not what is
- Trying to do everything in one massive pivot
- Forgetting to refresh after data changes
