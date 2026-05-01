---
tags:
  - observability:prometheus
  - observability:grafana
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Alerting and Production

---
## What This Chapter Covers

- Alerting rules
- Alertmanager
- Routing and silences
- SLOs
- Production patterns

---
## Alerting Rules

```yaml
groups:
  - name: alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) > 1
        for: 10m
        annotations:
          summary: "High error rate"
```

- PromQL expression
- Fires after `for` duration

---
## Alertmanager

- Receives alerts from Prometheus
- Groups, deduplicates, routes
- Sends to PagerDuty, Slack, email

---
## Routing

- By labels: team, severity
- Different receivers per route
- Catch-all default
- Inhibit rules: silence one when another fires

---
## Silences

- Mute alerts during maintenance
- Time-bound
- Match by label

---
## Templates

- Format alert messages
- Use labels and annotations
- Consistent format across alerts

---
## SLOs and SLIs

- SLI: indicator (latency, availability)
- SLO: target (99.9% requests under 200ms)
- Error budget: 1 - SLO
- Use to gate releases

---
## Burn Rate Alerts

- Alert when burning budget too fast
- Multi-window: 5m and 1h
- Standard SRE pattern
- Better than threshold alerts

---
## Alert Fatigue

- Too many alerts: ignored
- Page only on user-impacting issues
- Tune ruthlessly
- Run blameless reviews

---
## Recording Rules in Production

- Pre-aggregate hot queries
- Reduce dashboard load
- Lower percentile latency on dashboards

---
## Federation

- Scale Prometheus across regions
- Aggregate locally; federate selected
- Or: use Thanos / Cortex / Mimir

---
## Long-Term Storage

- Prometheus: weeks of local data
- Thanos / Cortex / Mimir: years
- Object storage backend

---
## High Availability

- Two Prometheus servers, same config
- Both scrape, both alert
- Alertmanager dedupes
- No single point of failure

---
## Capacity Planning

- Memory: ~3 KB per series
- Disk: ~1-2 bytes per sample
- Scrape impact on targets
- Plan for growth

---
## Migration Path

- Start: single Prometheus
- Grow: HA pair
- Scale: Thanos / Mimir
- Each step adds complexity

---
## Common Production Mistakes

- No HA; single point of failure
- Alerts on symptoms, not user impact
- No SLOs; ad-hoc thresholds
- Short retention; can't investigate after 24h
- Alertmanager not tested; pages don't fire
