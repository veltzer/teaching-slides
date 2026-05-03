---
tags:
  - observability:grafana
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Grafana and Dashboards

---
## What This Chapter Covers

- Grafana basics
- Data sources
- Panels
- Variables
- Dashboards as code
- Best practices

---
## What Grafana Is

- Open-source visualisation
- Multi-source: Prometheus, Loki, Postgres, ...
- Dashboards, alerts, exploration
- Most-used UI for Prometheus

---
## Dashboard Anatomy

![dashboard_anatomy](svg/courses/observability_and_monitoring/prometheus-and-grafana/05_grafana_and_dashboards/dashboard_anatomy.svg)

---
## Design Principles

![dashboard_principles](svg/courses/observability_and_monitoring/prometheus-and-grafana/05_grafana_and_dashboards/dashboard_principles.svg)

---
## Data Sources

- Prometheus: most common
- Loki: logs
- Tempo: traces
- Many SQL DBs
- Configure once, use everywhere

---
## Panels

- One visualisation
- Driven by a query
- Time series, gauge, table, stat
- Many types

---
## Time Series Panel

- The classic
- Shows metric over time
- Multiple series
- Most dashboards built around this

---
## Sample Panel Query

```promql
sum by (status) (rate(http_requests_total[5m]))
```

- Stacked area or line
- Per-status breakdown

---
## Variables

- Template dashboards
- $service, $instance, $env
- Dropdown at top
- One dashboard for many services

---
## Defining a Variable

- Type: query, custom, interval
- Query type: PromQL `label_values(...)`
- Refresh on dashboard load or interval

---
## Annotations

- Mark events on graphs
- Deployments, incidents
- From query or manual

---
## Linking Panels

- Drill-down across dashboards
- Click panel: jump to detail
- Pass variables across

---
## Dashboards as Code

- JSON definition
- Store in git
- Apply via API or provisioning
- Reproducible

---
## Provisioning

- Files describe data sources, dashboards
- Loaded on Grafana startup
- No clicking around for setup

---
## Sharing

- Public / private snapshots
- Embed in wikis
- Export JSON

---
## Best Practices

- Start with the four golden signals
- One dashboard per service
- Don't over-pack panels
- Use variables for reuse

---
## Common Dashboard Mistakes

- Too many panels; nobody scrolls
- No variables; one dashboard per service per env
- Panels with no titles or units
- Stacking when sum doesn't make sense
- Dashboards built once, never updated
