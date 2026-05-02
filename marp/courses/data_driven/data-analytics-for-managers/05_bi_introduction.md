---
tags:
  - data-and-ai:business-intelligence
level: beginner
category: data-driven
audience:
  - audiences:managers

---
# BI Introduction

---
## Modern BI Stack

![bi_stack](svg/courses/data_driven/data-analytics-for-managers/05_bi_introduction/bi_stack.svg)

---
## What This Chapter Covers

- What Business Intelligence is
- BI platforms and what they offer
- Data visualisation principles
- Dashboard design for managers
- Common measurement frameworks: Balanced Scorecard, Six Sigma
- When BI helps; when it gets in the way

---
## What BI Is

- Tools and processes for *consuming* data, mostly via dashboards
- Built on top of data warehouses or OLAP cubes
- Designed for *non-engineer* business users
- Self-service queries, scheduled reports, alerts
- Where most "data work" lands at most companies

---
## BI vs Data Engineering vs Data Science

- **Data engineering**: builds the pipelines; data lands clean and queryable
- **BI**: consumes the data; reports, dashboards, queries
- **Data science**: builds models that predict or recommend
- A healthy data org has all three
- Confusing the roles is the #1 reason hires don't work out

---
## Common BI Platforms

- **Tableau**: best-in-class visualisation; expensive
- **Power BI**: dominant in Microsoft shops; cheaper
- **Looker** (now Looker Studio + Looker): semantic layer + dashboards
- **Metabase / Superset**: open source; capable for most needs
- **Mode / Hex**: SQL + notebooks for analyst workflows

---
## What BI Tools Provide

- Connectors to common data sources (DB, warehouse, files, APIs)
- Visual query builder for non-SQL users
- Charting: bars, lines, pies, heatmaps, geos
- Dashboards combining many charts
- Scheduling, sharing, alerting
- Permissions: who sees what

---
## Visualisation Principles

- Match the chart to the *question* — not your aesthetic preferences
- Bar / column: comparing categories
- Line: change over time
- Scatter: relationship between two variables
- Pie: parts of a whole — and only when there are 2-5 slices
- Most data needs a bar or a line; the rest are special-purpose

---
## Visualisation Anti-Patterns

- 3D pie charts that distort the message
- Truncated y-axes that exaggerate small differences
- 14-slice pie charts — unreadable
- Rainbow gradients on categorical data
- Charts with 10+ colours — pick a smaller palette
- Dual y-axes without a strong reason

---
## Dashboard Design

- One dashboard, one purpose
- Most-important metric at top-left (eye lands there first)
- Group related metrics together
- 5-7 charts maximum per dashboard
- "Drill-down" links to detail dashboards
- Test by handing it to someone unfamiliar with the data

---
## Self-Service vs Curated

- **Curated**: data team builds and owns dashboards; users consume
- **Self-service**: business users build their own, on a semantic layer
- Curated: more reliable, less flexible, lower throughput
- Self-service: more flexible, more inconsistent, higher governance burden
- Most teams blend: curated executive dashboards, self-service exploration

---
## Balanced Scorecard

- A framework that tracks *four* perspectives:
    - **Financial**: revenue, costs, margin
    - **Customer**: satisfaction, retention
    - **Internal**: operational efficiency
    - **Learning**: capability growth
- Forces you not to optimise one perspective at the cost of others
- Common in large organisations and government

---
## Six Sigma

- Quality-improvement methodology born at Motorola
- DMAIC cycle: Define, Measure, Analyse, Improve, Control
- Heavy on statistics: process variability, defects per million
- Best fit for repetitive, well-defined processes (manufacturing, fulfilment)
- Less useful for creative or research work

---
## Other Frameworks Worth Knowing

- **OKRs**: covered earlier; goal-setting
- **KPIs**: Key Performance Indicators — the headline numbers
- **NPS**: Net Promoter Score — single-question loyalty metric
- **CSAT**: Customer Satisfaction — short surveys
- **DORA metrics**: deployment frequency, lead time, MTTR, change failure rate (engineering)

---
## Real-Time vs Batch BI

- **Batch**: refreshed nightly or hourly; "yesterday's numbers"
- **Real-time**: streaming updates; "right now"
- Real-time is harder, more expensive, often unnecessary
- Most managers act on weekly trends, not minute-to-minute changes
- Be honest: do you *act* on real-time data, or just stare at it?

---
## Cost of BI

- Tool licences (per-user, per-dashboard, per-query)
- Data warehouse compute (query pricing)
- Maintenance: dashboards rot if not curated
- Training: tools that look easy aren't, in practice
- ROI tracking still rarely done; budgets often ungoverned

---
## When BI Hurts

- Dashboard sprawl: 200 dashboards, no one knows which is right
- Conflicting numbers — every team has its own definition of "active user"
- Ritualistic dashboard reviews where no decisions are made
- Tools that don't match the team's literacy
- Treating BI as a substitute for thinking

---
## Common Mistakes

- Building dashboards before defining decisions they support
- Letting "metric definitions" drift across teams
- Dashboards that look impressive but never get acted on
- Buying every BI tool the salesperson recommends
- Not investing in training for the consumer audience
