---
tags:
  - practices:sre
  - practices:monitoring
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops
---
# Monitoring and Alerting

---

## The monitoring philosophy

- **Symptoms over causes** — alert when users hurt, not when CPU is high
- **Actionable over informative** — every page must require a human action
- **SLO-driven** — alerts derive from SLOs, not from individual metrics
- **Few and trusted** — alert fatigue kills response capability

The goal of monitoring is not to know everything; it is to know exactly what matters when it matters.

---

## Three signals, three uses

| Type | Used for | Example |
|---|---|---|
| **Alerts** | Wake someone up | latency over budget burn rate |
| **Tickets** | Action this week | disk filling up at current rate |
| **Logs** | Investigate later | full request traces |

Most things are not alerts. Most things are not tickets either. Logs and dashboards exist for the case-by-case questions.

---

## Four Golden Signals

![golden_signals](svg/courses/architecting/site-reliability-engineering/05_monitoring/golden_signals.svg)

---

## The four golden signals

For every user-facing service, monitor:

- **Latency** — how long requests take (split: success vs error)
- **Traffic** — how much demand (RPS, concurrent users, bytes/sec)
- **Errors** — rate of failed requests
- **Saturation** — how full the service is (CPU, memory, queue depth)

If you only get four metrics per service, these are the four. Everything else is supporting context.

---

## USE for resources

For machines and components — the **USE** method:

- **Utilization** — % of time the resource is busy
- **Saturation** — degree to which it has extra work queued
- **Errors** — count of error events

A widely used systems framework. Apply to: CPU, memory, disk, network, GPU, file descriptors. Quick way to find the bottleneck in any system.

---

## RED for services

For request-driven services — the **RED** method:

- **Rate** — requests per second
- **Errors** — failed requests per second
- **Duration** — distribution of request times

A microservices-oriented framework. Closely related to golden signals but framed for HTTP services. Trivial to compute from any reverse-proxy or service mesh.

---

## Designing alerts

```output
For each SLO:
  - One page-on-call alert: "burning fast or budget exhausted"
  - One ticket alert: "burning slowly, look this week"
  - Zero info alerts (use dashboards instead)
```

Each alert needs:

- A **runbook link** — what to do when this fires
- A **clear failure description** — what is broken from the user's view
- A **deep link to dashboard** — context for the on-call

Pages without runbooks are mistakes.

---

## Multi-burn-rate alerting

Page when fast burn AND slow burn both fire:

```output
fast burn  : 14.4× burn over 1h    → would deplete budget in 2 days
slow burn  : 6× burn over 6h       → would deplete budget in 4 days
```

- Fast burn alone catches outages
- Slow burn alone catches degradation
- Requiring both reduces flapping
- Documented in the Google SRE workbook chapter on alerting

---

## Dashboard design

- One **overview** dashboard per service: 4 golden signals + SLO status
- Drill-down dashboards for components, dependencies, queues
- Resist the dashboard sprawl — every dashboard needs an owner
- Annotate deploys, incidents, config changes on the timeline
- Dashboards rot — review them quarterly, delete what no one looks at

A dashboard nobody reads is worse than no dashboard — it pretends to be observability.

---

## Distributed system observability

Three pillars:

- **Metrics** — aggregate, low-cardinality numbers
- **Logs** — discrete event records
- **Traces** — causally-linked request paths across services

Modern stacks (OpenTelemetry, Prometheus, Grafana, Loki, Tempo) unify these. Each pillar answers different questions; you need all three to debug serious incidents.

---

## Alert fatigue

- Most teams page far too often when starting out
- Alert that fires often and has no action = noise — delete or downgrade
- Alert that fires once a year — probably needs better testing, not better alerting
- Page-to-action ratio: should be ≥80% — if lower, your alerts are wrong

Track every page. After every on-call shift: which pages were valuable? Which were noise? Tune relentlessly.

---

## Tools landscape

- **Prometheus + Grafana + Alertmanager** — open-source default
- **Datadog, New Relic, Splunk** — commercial; faster to start with
- **OpenTelemetry** — vendor-neutral instrumentation; emit once, route anywhere
- **Cloud-native** — CloudWatch, GCP Monitoring, Azure Monitor
- **Honeycomb** — observability platform with high-cardinality querying

The tool matters less than the discipline of SLO-driven alerting.
