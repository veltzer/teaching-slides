---
tags:
  - data-and-ai:dashboards
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---

# Dashboards

---

## What This Chapter Covers

- Dashboard design principles
- Selecting key performance indicators
- Layout and visual hierarchy
- Interactive elements
- Building dashboards in Tableau and Excel
- Maintenance and refresh

---

## What a Dashboard Is

- A *single view* of the most important metrics for a purpose
- Designed to be *consumed*, not built (each time)
- Updated regularly without manual intervention
- Aimed at a specific audience and a specific decision
- Not a report, not a one-off chart

---

## Design Pattern

![dashboard_design](svg/courses/data_science/data-analyst-fundamentals/11_dashboards/dashboard_design.svg)

---

## Why Dashboards Often Fail

- Built without a clear consumer in mind
- 30 charts, no priority
- Stale data nobody trusts
- Three teams have three different "active user" definitions
- Reviewed in meetings where no decisions are made
- Many companies have hundreds; few have value-generating ones

---

## Start From the Decision

- What decision will this dashboard support?
- Who will make that decision?
- How often?
- Without these answers: don't build the dashboard
- The decision dictates the metrics, the metrics dictate the layout

---

## Choosing KPIs

- Few, important, actionable
- Each KPI ties to a decision
- 5-7 metrics maximum on the main view
- Add depth with linked drill-down dashboards
- "If this metric were red, what would we do?" — every metric should have an answer

---

## Lagging vs Leading

- **Lagging**: revenue, churn, NPS — outcomes
- **Leading**: signups, time-on-site, support tickets — predictors
- A balanced dashboard has both
- Leading indicators give you time to act before the lagging ones move
- Don't track only what already happened

---

## Layout Principles

- Most-important top-left (eye lands here first)
- Grouping by topic, not random placement
- Consistent chart sizing within a row
- Whitespace is your friend
- Mobile preview if relevant

---

## Information Layers

![dashboard_layers](svg/courses/data_science/data-analyst-fundamentals/11_dashboards/dashboard_layers.svg)

---

## Visual Hierarchy

- Big numbers for headline metrics
- Charts for trends and comparisons
- Smaller details below
- Color highlights what's outside expected range
- Most data should be muted; the exceptional should stand out

---

## Interactive Elements

- **Filters**: date range, segment, region — global to the dashboard
- **Slicers**: clickable filter buttons
- **Drill-down**: click a metric to see detail dashboard
- **Tooltips**: hover for context
- Make interactive only what users will *actually* use

---

## Dashboards in Tableau

- Build worksheets first; combine on a dashboard
- Add filter actions: clicking a chart filters another
- Use floating layouts sparingly
- Set fixed dashboard size for predictable rendering
- Publish to server; subscribe stakeholders

---

## Dashboards in Excel

- Pivot tables + slicers + pivot charts on a separate sheet
- Hide or protect the data sheets
- Clean layout: title, KPIs, charts, filters
- For Excel Online: shared, refreshable
- Lower polish than Tableau but free if you have Office

---

## Dashboards in Power BI

- Similar to Tableau in capability
- Cheaper if you have Microsoft 365
- DAX language for advanced calculations (steep learning curve)
- Tight integration with Excel and Teams
- Common in Microsoft-shops

---

## Real-Time vs Refresh

- Real-time: streaming updates as data changes
- Periodic refresh (every 5 min, hourly, nightly): more common
- Real-time costs more, complicates more, used less than people think
- Match refresh cadence to *decision* cadence
- Daily decisions don't need second-by-second updates

---

## Maintaining Dashboards

- Source data changes &#8594; dashboards break
- Schema migrations &#8594; queries fail
- Definitions drift &#8594; numbers diverge from other sources
- Owner per dashboard; check-in cadence
- Without maintenance, dashboards rot

---

## Killing Dashboards

- Most dashboards aren't viewed after week 2
- Audit usage; retire the unused
- Each kept dashboard has an ongoing cost
- Less is more — 5 actively-used dashboards beats 50 stale ones
- Track this; report it; act on it

---

## Sharing Permissions

- Public, internal, restricted
- Some metrics are sensitive; not everyone should see
- Tableau Server / Power BI / Looker all support row-level security
- Don't give everyone admin access "just in case"
- Audit access periodically

---

## Common Mistakes

- Pretty dashboards with no consumer
- 30 charts on one page
- Static screenshots emailed weekly instead of a live dashboard
- Inconsistent metric definitions across dashboards
- "We need a dashboard for that" without a decision in mind
