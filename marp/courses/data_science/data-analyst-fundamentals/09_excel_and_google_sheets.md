---
tags:
  - data-and-ai:excel
  - data-and-ai:spreadsheets
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# Excel and Google Sheets

---
## What This Chapter Covers

- Why analysts can't escape spreadsheets
- Essential formulas and functions
- VLOOKUP and the modern alternatives
- Conditional formatting and data validation
- Charts and sparklines
- Power Query for data transformation

---
## The Spreadsheet Reality

- Every analyst uses spreadsheets, every day
- Stakeholders speak Excel, not Python
- Reports get exported to Excel; meetings happen on Excel
- The skill isn't avoiding spreadsheets — it's using them well
- Master a few patterns; they cover 90% of work

---
## Power Features

![sheets_features](svg/courses/data_science/data-analyst-fundamentals/09_excel_and_google_sheets/sheets_features.svg)

---
## When to Use a Spreadsheet

- Small datasets (under ~100K rows)
- Quick one-off analysis
- Sharing with non-technical stakeholders
- Iterating on a calculation interactively
- *Not* for: production pipelines, version-controlled work, anything reproducible

---
## When NOT to Use a Spreadsheet

- Datasets over 1M rows (Excel can't handle them)
- Anything you'll re-run with different data
- Work that needs to be reviewed with diffs
- Multi-analyst collaboration on logic
- That's where SQL + Python come in

---
## Essential Functions

- `SUM`, `AVERAGE`, `COUNT`, `MIN`, `MAX`
- `IF`, `IFS`, `AND`, `OR`, `NOT`
- `COUNTIF`, `SUMIF`, `AVERAGEIF` (and `*IFS` versions)
- `LEFT`, `RIGHT`, `MID`, `LEN`, `TRIM`, `LOWER`, `UPPER`
- `DATE`, `YEAR`, `MONTH`, `DAY`, `EDATE`, `EOMONTH`

---
## VLOOKUP

```misc
=VLOOKUP(lookup_value, table_array, col_index, [exact_match])
```

- Find a row by key in a table; return a column from that row
- The most-known and most-misused function
- Limitations: only looks right; column index breaks on insert
- Use exact match (`FALSE` or `0`) almost always
- Slow on large datasets

---
## INDEX + MATCH

```misc
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
```

- More flexible than VLOOKUP
- Look in either direction (left or right)
- Doesn't break on inserted columns
- The pre-2019 Excel power user's preference

---
## XLOOKUP (Modern)

```misc
=XLOOKUP(lookup_value, lookup_range, return_range)
```

- Excel 2019+ and Google Sheets
- Replaces both VLOOKUP and INDEX+MATCH
- Easier syntax; more capable
- Defaults to exact match
- The new standard — use it where available

---
## Conditional Logic

```misc
=IF(A2 > 100, "High", "Normal")
=IFS(A2 > 100, "High", A2 > 50, "Medium", TRUE, "Low")
=IFERROR(VLOOKUP(...), "Not found")
```

- `IF` for one condition
- `IFS` for many conditions (cleaner than nested IFs)
- `IFERROR` to handle lookup misses gracefully
- Don't nest IFs more than 3 deep — use a lookup table instead

---
## Conditional Formatting

- Highlight cells based on rules
- Top 10, above average, color scales, data bars
- Useful for spotting outliers visually
- Tooltip-like value labels
- Don't overuse — too much colour distracts

---
## Data Validation

- Restrict what users can enter in a cell
- Dropdowns from a list (`Allow: List`)
- Number ranges
- Custom formulas
- Prevents bad data at entry; cheaper than fixing later

---
## Charts

- Insert &#8594; Chart, pick type
- Match the chart type to the data shape (same rules as everywhere)
- Edit chart title, axes, colors via the Chart Editor
- For dashboards: link chart data to a model sheet, output to a clean sheet

---
## Sparklines

- Tiny chart inside a single cell
- `=SPARKLINE(B2:M2)` (Google Sheets) or Excel's Sparkline insert
- Show trends in a table without taking up space
- Great for KPI tables — one row per metric, sparkline for trend
- Variants: line, column, win/loss

---
## Pivot Tables

```misc
Insert &#8594; PivotTable
Drag fields to Rows, Columns, Values, Filters
```

- The single most powerful spreadsheet feature
- Aggregate, group, filter without writing formulas
- Values can be sum, count, average, %, etc.
- Slicers: clickable filter buttons
- Earns its own chapter, next

---
## Power Query (Excel) / Sheets Importrange

- Excel's Power Query: ETL inside Excel
- Connect to databases, files, web; transform; load into a sheet
- Repeatable: re-run on refreshed source
- A bridge from one-off Excel to reproducible analysis
- For Google Sheets: `IMPORTRANGE`, `QUERY` functions provide some of the same

---
## Common Spreadsheet Anti-Patterns

- Magic numbers hardcoded in formulas
- Manual formatting that breaks with new data
- "I'll just sort it" &#8594; rows get misaligned, data corrupted
- Multiple "version 3 final FINAL.xlsx" files
- Spreadsheets as production data stores

---
## Common Mistakes

- Using Excel where SQL would be faster and reproducible
- Massive workbooks that crash on open
- Hidden sheets and ranges nobody knows about
- Sharing one xlsx via email, getting 5 conflicting versions back
- Not using version control for important spreadsheet logic
