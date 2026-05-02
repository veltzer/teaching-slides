---
tags:
  - data-and-ai:tableau
  - data-and-ai:visualization
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# Tableau for Data Visualization

---
## What This Chapter Covers

- The Tableau interface
- Connecting to data
- Building worksheets
- Calculated fields and parameters
- Interactive filters and actions
- Publishing and sharing

---
## What Tableau Is

- A drag-and-drop visualisation tool
- Connects to many data sources directly
- Build charts without writing code
- Combine charts into dashboards
- Industry standard in many large organisations

---
## Quick Tour

![tableau_basics](svg/courses/data_science/data-analyst-fundamentals/07_tableau_for_data_visualization/tableau_basics.svg)

---
## Tableau Editions

- **Tableau Desktop**: build worksheets, dashboards (the analyst's tool)
- **Tableau Server**: enterprise hosting (on-prem)
- **Tableau Cloud**: hosted by Tableau
- **Tableau Public**: free, all your work is public
- **Tableau Reader**: free, view-only

---
## The Interface

- **Data pane** (left): your fields, dimensions, measures
- **Shelves** (top): rows, columns, filters, marks
- **View** (centre): the actual chart
- **Marks card**: control color, size, label, tooltip per mark
- **Pages, Filters, Cards**: more controls on the right

---
## Connecting to Data

- File: CSV, Excel, JSON, PDF, spatial files
- Database: Postgres, MySQL, SQL Server, Snowflake, BigQuery, Redshift
- Cloud: Google Sheets, Salesforce, Marketo
- Live connection vs Extract:
    - Live: queries the source on every interaction
    - Extract: cached snapshot, faster, schedulable refresh

---
## Dimensions vs Measures

- **Dimensions**: categorical fields (country, product, date)
- **Measures**: numeric fields you aggregate (sales, revenue, count)
- Tableau auto-classifies on import; you can override
- Drag a measure into the view &#8594; auto-aggregated (SUM by default)
- Right-click the field on a shelf to change the aggregation

---
## Building a First Worksheet

- Connect data &#8594; new worksheet
- Drag `Order Date` (dimension) to Columns
- Drag `Sales` (measure) to Rows
- Tableau picks line chart for date vs measure
- Add `Region` to Color in the Marks card &#8594; multiple lines

---
## Show Me Panel

- Tableau suggests chart types based on what's on the shelves
- Greys out incompatible types
- Useful while learning; later you'll know what you want
- Custom charts: drag fields into specific shelves, override defaults

---
## Calculated Fields

```misc
Profit Margin = SUM([Profit]) / SUM([Sales])
```

- Right-click in Data pane &#8594; Create Calculated Field
- Use them like any other field
- Aggregations, conditional logic (`IF / THEN`), date functions
- Centralise calculations; don't redo them in every worksheet

---
## Parameters

- A user-controllable value (number, string, date)
- Examples: "show top N customers", "as of date", "metric to display"
- Drop a parameter into a calculated field
- Right-click the parameter &#8594; Show Parameter Control
- The dashboard becomes interactive

---
## Filters

- Drag a field to the Filters shelf
- Filter on dimensions: include / exclude values
- Filter on measures: range
- Filter on dates: relative date, range, individual dates
- "Show Filter" makes it interactive on a dashboard

---
## Sets and Groups

- **Set**: subset of dimension values
- "Top 10 customers by revenue" is a set
- **Group**: combine values into one bucket
- Combine "USA", "U.S.A.", "United States" into one group
- Both are reusable across the workbook

---
## Dashboards

- Combine worksheets into one view
- Drag worksheets onto the dashboard canvas
- Add filters, action filters, parameter controls
- Layout: tiled or floating
- Resize for the target screen size

---
## Actions

- **Filter actions**: clicking a chart filters another
- **Highlight actions**: clicking highlights related data
- **URL actions**: clicking opens an external link
- The mechanism that makes a Tableau dashboard *feel* alive
- Configure under Dashboard &#8594; Actions

---
## Publishing

- Tableau Server / Cloud: upload, share with permissions
- Public: free but everything is public
- Embed in web pages, Confluence, Salesforce, etc.
- Schedule extract refreshes
- Subscriptions: email a snapshot on a schedule

---
## Performance Tips

- Use extracts for large data sources, live for small / fast ones
- Filter at the data source if possible
- Avoid `INCLUDE` / `EXCLUDE` LODs over huge data
- Hide unused fields to reduce extract size
- "Performance Recording" finds bottlenecks

---
## Common Mistakes

- Live-connecting to a slow source and shipping a slow dashboard
- One giant dashboard with 30 charts &#8594; nobody reads any of them
- Calculated fields rebuilt in every workbook
- Using too many colours
- Treating Tableau as a replacement for thinking
