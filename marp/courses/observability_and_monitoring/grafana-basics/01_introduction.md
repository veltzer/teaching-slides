---
tags:
  - observability:grafana
level: beginner
category: observability
audience:
  - audiences:devops

---

# Introduction to Grafana

---

## What This Chapter Covers

- What Grafana is
- Why use it
- Core concepts
- Architecture
- Course outline

---

## What Grafana Is

- Open-source dashboard tool
- Visualize metrics, logs, traces
- Many data source plugins
- Self-hosted or hosted

---

## What It Is And Is Not

![grafana_pieces](svg/courses/observability_and_monitoring/grafana-basics/01_introduction/grafana_pieces.svg)

---

## Why Use It

- Single UI across many backends
- Friendly for engineers
- Powerful query and panel options
- Active community

---

## Core Concepts

- Data source
- Dashboard
- Panel
- Query
- Alert

---

## Data Source

- Connection to a backend
- One per system: metrics store, log store
- Configurable per workspace
- Reused across dashboards

---

## Dashboard

- Collection of panels
- Shared time range
- Variables for filtering
- Versioned over time

---

## Panel

- One visualization
- Time series, table, stat, gauge
- Pulls from one or more queries
- Configured per visualization

---

## Query

- Asks the data source for data
- Per panel
- Variables substituted at runtime
- Templated for reuse

---

## Alerts

- Watch a query
- Trigger on threshold
- Send to channels
- Track history

---

## Variables

- Dropdowns at top of dashboard
- Filter all panels
- Templated queries
- Improves reusability

---

## Architecture

- Server backend
- Web frontend
- Plugin system for data sources
- Database for state

---

## Sources to Dashboards

![grafana_arch](svg/courses/observability_and_monitoring/grafana-basics/01_introduction/grafana_arch.svg)

---

## Hosting Options

- Self-hosted Grafana
- Grafana Cloud
- Embedded in vendor products
- Pick by team and budget

---

## Course Outline

- Data sources
- Building panels
- Building dashboards
- Alerts
- Operations

---

## Common Beginner Mistakes

- Too many panels per dashboard
- No variables
- Hardcoded time range
- No naming convention
- No backups of dashboards
