---
tags:
  - observability:grafana
level: beginner
category: observability
audience:
  - audiences:devops

---
# Dashboards and Alerts

---
## What This Chapter Covers

- Dashboard layout
- Variables
- Templating
- Alerts
- Notification channels

---
## Dashboard Layout

- Top: KPIs at a glance
- Middle: time series details
- Bottom: tables and logs
- Reading order matches investigation flow

---
## Sizing Panels

- Width by importance
- Smaller for context
- Larger for the metric you watch
- Avoid horizontal scrolling

---
## Time Range

- Default to last 1 hour
- Quick ranges in picker
- Auto-refresh interval set per dashboard
- Snap to current time

---
## Variables

- Drop-downs at top
- Multi-select supported
- Substitute into queries
- Refresh policy chosen

---
## Variables Visualized

![variables](svg/courses/observability_and_monitoring/grafana-basics/04_dashboards_and_alerts/variables_drilldown.svg)

---
## Templating

- One dashboard, many environments
- Variables for environment, region, service
- Saves duplication
- Encourages consistency

---
## Linking

- Click panel to drill down
- Link to another dashboard
- Pre-fill variables
- Keeps investigation flow

---
## Versioning

- Dashboards as code
- Stored as JSON
- Reviewed via PR
- Provisioned to Grafana

---
## Alert Rules

- Tied to a query
- Threshold or expression
- For-duration to avoid flapping
- Severity levels matter

---
## Alert Routing

- Send by labels
- Per team or service
- Avoid cross-team noise
- Document each rule

---
## Notification Channels

- Email
- Chat tools
- Pager systems
- Webhooks

---
## Pager Hygiene

- Each page should require action
- Each page should have a runbook
- Tune until it does
- Otherwise it gets ignored

---
## Silences

- Pause noisy alerts during deploys
- Time-bounded
- Document the reason
- Audit silences

---
## Inhibition

- Suppress less important alerts
- When higher-level rule fires
- Reduces noise during incidents
- Configure per environment

---
## Common Dashboard Mistakes

- One huge dashboard
- No variables
- Static time range
- Alerts without runbooks
- Notification channels for many small things
