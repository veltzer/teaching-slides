---
tags:
  - infrastructure:kubernetes
  - practices:observability
level: intermediate
category: containers
audience:
  - audiences:developers
  - audiences:devops

---

# Observability

---

## What This Chapter Covers

- Logs
- Metrics
- Tracing
- The PLG / ELK stacks
- Cluster monitoring
- Application monitoring

---

## The Three Pillars

- Logs: what happened
- Metrics: how often, how fast
- Tracing: per-request paths
- Together: full picture

---

## Cluster Signals

![four_signals](svg/courses/containers/kubernetes/10_observability/four_signals.svg)

---

## Logging

- Apps log to stdout / stderr
- Container runtime captures
- Log shipper forwards to backend
- Don't write to files inside the pod

---

## Log Shippers

- Fluent Bit: lightweight
- Fluentd: more features
- Vector: modern alternative
- Filebeat: from Elastic

---

## Centralised Log Storage

- Loki: cheap, log-only
- Elasticsearch: search + analytics
- Cloud logging: CloudWatch, Stackdriver
- Pick: cost vs features

---

## Metrics: Prometheus

- Pull-based
- Each pod exposes /metrics
- Prometheus scrapes
- Stores time-series

---

## Service Monitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-metrics
spec:
  selector:
    matchLabels:
      app: api
  endpoints:
  - port: metrics
```

- Tells Prometheus to scrape

---

## Grafana

- Dashboards over Prometheus, Loki, etc.
- Ubiquitous
- Pre-built dashboards for K8s
- Build your own per-service

---

## Tracing: OpenTelemetry

- Standard for tracing
- SDKs in every major language
- Traces, metrics, logs unified
- Forward to: Jaeger, Tempo, vendor backends

---

## Cluster Monitoring

- Metrics-server: basic CPU / memory
- kube-state-metrics: cluster state
- node-exporter: node-level metrics
- All Prometheus-compatible

---

## Application Monitoring

- Per-service /metrics endpoint
- RED method: rate, errors, duration
- USE for resources
- Custom business metrics

---

## Alerting

- Prometheus Alertmanager
- Alerts on: high error rate, latency, low resources
- Routes to: Slack, PagerDuty, email
- Tune to avoid alert fatigue

---

## SLO-Based Alerting

- Service Level Objectives: targets (99.9% uptime)
- Burn rate alerts: alert when SLO budget burning fast
- More signal; less noise
- Modern best practice

---

## Distributed Tracing

- Trace request across services
- Span per service call
- Find: slow dependencies, error sources
- Sample (don't trace 100%)

---

## Cost Considerations

- Logs: $$$ at scale
- Metrics: cheap (low cardinality)
- Traces: $ to $$$ depending on sampling
- Sample logs / traces; keep all metrics

---

## Common Observability Mistakes

- Logging request bodies (cost; PII)
- High-cardinality labels in Prometheus (memory)
- No alerts on cluster health
- Alerts that fire constantly (ignored)
- Logs without trace context (can't correlate)

---

## Course Wrap-Up

- K8s orchestrates containers across machines
- Pods, Services, Deployments: the daily abstractions
- ConfigMaps and Secrets for config
- Networking and Ingress for traffic
- RBAC for permissions
- Helm for packaging
- Observability: pillars of operations
