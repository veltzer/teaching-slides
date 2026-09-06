---
tags:
  - practices:devops
  - concepts:architecture
  - practices:ci-cd
  - infrastructure:infrastructure-as-code
level: advanced
category: devops
audience:
  - audiences:architects
  - audiences:devops
  - audiences:managers

---

# Observability Architecture

---

## What is Observability?

- The ability to understand a system's internal state from its external outputs
- Goes beyond traditional monitoring: not just "is it up?"
- Enables answering novel questions about production systems
- Critical for operating distributed, microservice-based architectures

---

## The Three Pillars of Observability

![the_three_pillars_of_observability](svg/courses/devops/architectural-decisions-in-devops/11_observability_architecture/the_three_pillars_of_observability.svg)

---

## Metrics: Overview

- Numeric measurements collected at regular intervals
- Stored as time-series data: `(timestamp, value, labels)`
- Types: counters, gauges, histograms, summaries
- Low storage cost per data point
- Ideal for dashboards, trend analysis, and alerting

---

## Metrics: When to Use

- Tracking system health: `cpu_usage`, `memory_free`, `disk_io`
- Measuring application behavior: `request_rate`, `error_rate`, `latency_p99`
- Business KPIs: `orders_per_minute`, `active_users`
- Capacity planning and forecasting
- Triggering alerts based on thresholds or anomalies

---

## Metrics: Cost and Storage

- Very compact: a single data point is roughly 1-2 bytes compressed
- Well-suited for long retention (months or years)
- Cardinality is the main cost driver
    - Each unique combination of labels creates a new time series
    - `{method="GET", path="/api/users", status="200"}` is one series
- Avoid high-cardinality labels like `user_id` or `request_id`

---

## Logs: Overview

- Immutable, timestamped records of discrete events
- Can be structured (`JSON`) or unstructured (plain text)
- Contain rich context: stack traces, request payloads, user IDs
- The most detailed signal type
- Essential for debugging specific incidents

---

## Logs: When to Use and Cost

- When to use:
    - Diagnosing specific errors or failures
    - Audit trails and compliance requirements
    - Debugging edge cases that metrics cannot capture
    - Forensic analysis after security incidents
- Cost controls:
    - Log levels: `ERROR` always, `DEBUG` only when needed
    - Sampling: log 1 in N requests at `INFO` level
    - Retention policies: hot logs for days, archive for months

---

## Traces: Overview

- Records of a request's journey through distributed services
- Composed of `spans`: individual units of work with timing data
- Each span has a `trace_id`, `span_id`, `parent_span_id`
- Show causality and dependencies between services
- Measure latency contribution per service

---

## Traces: When to Use and Cost

- When to use:
    - Debugging latency in multi-service architectures
    - Understanding request flow and service dependencies
    - Root cause analysis: which service caused the failure?
- Cost controls:
    - Head-based sampling: decide at entry whether to trace (simpler)
    - Tail-based sampling: decide after completion (captures errors)
    - Typical sampling rate of 1-10% in high-traffic systems
    - Typical retention: 7-30 days for raw traces

---

## Signal Comparison Table

| Aspect | Metrics | Logs | Traces |
|--------|---------|------|--------|
| Data type | Numeric aggregates | Text events | Request spans |
| Storage cost | Low | High | Medium |
| Cardinality | Labels-limited | Unbounded | Bounded by sampling |
| Best for | Trends, alerts | Debugging, audit | Latency, dependencies |
| Retention | Months/years | Days/weeks | Days/weeks |
| Query speed | Fast | Slower | Moderate |

---

## Correlating Across Signal Types

- The real power comes from connecting all three signals
- Common correlation keys:
    - `trace_id` embedded in log lines
    - `trace_id` as an exemplar on metric data points
    - Shared labels: `service`, `environment`, `version`
- Workflow: metric alert -> exemplar trace -> correlated logs

```yaml
# Structured log with trace context
{
  "level": "ERROR",
  "service": "payment-api",
  "trace_id": "abc123def456",
  "message": "Payment processing failed"
}
```

---

## Push vs Pull Collection Models

![push_vs_pull_collection_models](svg/courses/devops/architectural-decisions-in-devops/11_observability_architecture/push_vs_pull_collection_models.svg)

---

## Pull Model: Prometheus

- `Prometheus` server scrapes HTTP endpoints (`/metrics`) at configured intervals
- Targets are discovered via service discovery or static config
- The server controls collection frequency and timeout

```yaml
scrape_configs:
  - job_name: "my-service"
    scrape_interval: 15s
    static_configs:
      - targets: ["svc-a:8080", "svc-b:8080"]
```

---

## Pull Model: Pros and Cons

- Advantages:
    - Central control over what gets collected and how often
    - Easy to detect if a target is down (scrape fails)
    - Targets are stateless: they just expose current values
    - Natural fit for `Kubernetes` service discovery
- Disadvantages:
    - Requires network access from server to every target
    - Difficult across firewalls, NATs, or multi-cloud
    - Does not work well for short-lived jobs or batch processes

---

## Push Model: Agent-Based Collection

- Agents (`Telegraf`, `Fluentd`, `OTel Collector`) run alongside services
- Services push data to a local agent or directly to a backend
- The agent buffers, batches, and forwards data
- Advantages:
    - Works across network boundaries
    - Supports short-lived processes and serverless functions
    - Better for event-driven data like logs and traces
- Disadvantages:
    - Risk of overwhelming the backend during spikes
    - Harder to detect silent failures
    - Agent deployment adds operational overhead

---

## Scalability: Pull vs Push

| Factor | Pull | Push |
|--------|------|------|
| 10s of targets | Easy | Easy |
| 1000s of targets | Federation needed | Load-balance collectors |
| Short-lived jobs | `Pushgateway` workaround | Native support |
| Cross-network | VPN or proxy needed | Works natively |
| Backpressure | Built-in (scrape interval) | Must be implemented |
| Failure detection | Scrape failure alerts | Heartbeat checks needed |

---

## Hybrid Approach: OpenTelemetry

- `OpenTelemetry` (`OTel`) provides a vendor-neutral standard
- Supports both push and pull collection
- Unified SDK for metrics, logs, and traces
- `OTel Collector` receives, processes, and exports data
- Decouples instrumentation from backend choice

```yaml
receivers:
  otlp:
    protocols:
      grpc: { endpoint: "0.0.0.0:4317" }
processors:
  batch: { timeout: 5s }
exporters:
  otlp: { endpoint: "backend:4317" }
service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
```

---

## Centralized Observability

- All teams send data to a single observability platform
- One set of dashboards, one query language, one alert pipeline
- Often called "single pane of glass"
- Advantages:
    - Consistent tooling across the organization
    - Easier to correlate data across teams and services
    - Economies of scale in licensing and infrastructure
- Disadvantages:
    - Platform team becomes a bottleneck
    - Blast radius: platform outage blinds the entire organization
    - Scaling to handle all teams can be expensive

---

## Distributed (Team-Owned) Observability

- Each team operates their own observability stack
- Teams choose tools that fit their specific needs
- Federated queries provide cross-team visibility when needed
- Advantages:
    - Teams move independently
    - Blast radius limited to a single team
    - Faster iteration on dashboards and alerts
- Disadvantages:
    - Duplicated effort across teams
    - Difficult to correlate signals across boundaries
    - Higher total cost due to lack of shared infrastructure

---

## Build vs Buy: Decision Framework

| Factor | Build (Open Source) | Buy (SaaS) |
|--------|-------------------|-------------|
| Up-front cost | Low (free software) | Subscription fees |
| Operational cost | High (team maintains) | Low (vendor manages) |
| Customization | Full control | Limited to vendor features |
| Scale | You manage scaling | Vendor handles scaling |
| Vendor lock-in | Low | High |
| Time to value | Weeks/months | Days |

---

## Common Build Stack

- Metrics: `Prometheus` + `Thanos` or `Mimir` for long-term storage
- Logs: `Loki` or `Elasticsearch`
- Traces: `Jaeger` or `Tempo`
- Visualization: `Grafana`
- Collection: `OpenTelemetry Collector`
- Requires a dedicated platform engineering team

---

## Common Buy Options

- `Datadog`: all-in-one, strong integrations, per-host pricing
- `New Relic`: unified platform, per-GB ingest pricing
- `Splunk`: strong log analytics, enterprise-focused
- `Honeycomb`: trace-first, high-cardinality exploration
- `Grafana Cloud`: managed open-source stack
- Evaluate based on data volume, retention needs, and team size

---

## Alerting Strategy Overview

![alerting_strategy_overview](svg/courses/devops/architectural-decisions-in-devops/11_observability_architecture/alerting_strategy_overview.svg)

---

## Alert Fatigue: The Problem

- Too many alerts desensitize responders
- Symptoms of alert fatigue:
    - On-call engineers ignore or snooze alerts
    - Critical alerts buried in noise
    - High alert-to-incident ratio (most alerts are non-actionable)
- Teams with more than 5 alerts per on-call shift lose effectiveness
- Root cause: monitoring everything "just in case"

---

## Reducing Alert Noise

- Every alert must be actionable: if no one needs to act, delete it
- Group related alerts to reduce volume
- Use inhibition: suppress downstream alerts when root cause fires
- Set appropriate severity levels:
    - `critical`: page immediately, customer impact
    - `warning`: review next business day
    - `info`: dashboard only, never page
- Alerts without runbooks or clear ownership must be fixed or removed

---

## Threshold-Based Alerting

- Traditional approach: set a static threshold, alert when crossed

```yaml
groups:
  - name: infra
    rules:
      - alert: HighCPU
        expr: node_cpu_usage_percent > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU above 90%"
```

- Limitations: does not adapt to changing baselines
- Seasonal patterns cause false positives
- Requires constant tuning as workloads evolve

---

## SLO-Based Alerting

- Define Service Level Objectives (`SLOs`) based on user experience
- Alert on error budget consumption rate, not raw metrics
- Example: "99.9% of requests succeed within 300ms over 30 days"
- Error budget = 0.1% = 43.2 minutes of allowed downtime per 30 days
- Focuses on what users actually experience

---

## SLO Hierarchy

![slo_hierarchy](svg/courses/devops/architectural-decisions-in-devops/11_observability_architecture/slo_hierarchy.svg)

---

## Error Budget Burn Rate

- Burn rate = how fast the error budget is being consumed
- A burn rate of 1x means the budget is exactly exhausted in the window

| Burn rate | Budget consumed in | Urgency |
|-----------|--------------------|---------|
| 14.4x | 1 hour (over 30-day window) | Page immediately |
| 6x | 5 hours | Page |
| 1x | 30 days | Ticket |
| 0.5x | Never exhausted | No action |

---

## Multi-Window Burn Rate Alerts

```yaml
- alert: ErrorBudgetFastBurn
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h]))
      / sum(rate(http_requests_total[1h]))
    ) > 14.4 * 0.001
    AND
    (
      sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m]))
    ) > 14.4 * 0.001
  labels:
    severity: critical
```

- Short window confirms the alert is not a brief spike

---

## SLO-Based vs Threshold-Based

| Aspect | Threshold-Based | SLO-Based |
|--------|----------------|-----------|
| What it measures | Raw metric values | User impact |
| Adaptability | Static, needs tuning | Self-adjusting via budget |
| False positives | Common | Fewer |
| Actionability | Often unclear | Clear: budget at risk |
| Complexity | Simple to set up | Requires SLO definition |
| Business alignment | Low | High |

---

## Defining Good SLIs

- Choose SLIs that reflect user experience:
    - Availability: proportion of successful requests
    - Latency: proportion of requests faster than threshold
    - Correctness: proportion of correct responses
- Measure at the boundary closest to the user
    - Load balancer metrics are better than database metrics
- Use ratios, not averages: `good_events / total_events`

---

## On-Call Architecture

- On-call is the operational backbone of reliability
- Key design decisions:
    - Rotation structure: weekly, daily, follow-the-sun
    - Escalation tiers: primary, secondary, incident commander
    - Tools: `PagerDuty`, `OpsGenie`, `Grafana OnCall`
    - Compensation and burnout prevention

---

## Escalation Flow

![escalation_flow](svg/courses/devops/architectural-decisions-in-devops/11_observability_architecture/escalation_flow.svg)

---

## On-Call Best Practices

- Target maximum 1 page per on-call shift on average
- Every page must have a runbook with:
    - What the alert means and likely causes
    - Diagnostic steps and remediation actions
    - Escalation criteria and dashboard links
- Conduct blameless post-incident reviews
- Track: pages per shift, time to acknowledge, time to resolve

```yaml
annotations:
  runbook_url: "https://wiki.internal/runbooks/high-error-rate"
  dashboard_url: "https://grafana.internal/d/abc123"
```

---

## Observability Data Pipeline

![observability_data_pipeline](svg/courses/devops/architectural-decisions-in-devops/11_observability_architecture/observability_data_pipeline.svg)

---

## Instrumentation Best Practices

- Use standard libraries: `OpenTelemetry` SDKs, `Prometheus` client libs
- Instrument at service boundaries: incoming and outgoing requests
- Include context: `service.name`, `service.version`, `environment`

```python
from opentelemetry import trace

tracer = trace.get_tracer("payment-service")

with tracer.start_as_current_span("process_payment") as span:
    span.set_attribute("payment.method", "credit_card")
    span.set_attribute("payment.amount", 99.99)
    result = charge_card(card_info)
```

---

## RED and USE Methods

- `RED` method (for request-driven services):
    - **R**ate: requests per second
    - **E**rrors: failed requests per second
    - **D**uration: latency distribution
- `USE` method (for infrastructure resources):
    - **U**tilization: percentage of resource busy
    - **S**aturation: queue depth or wait time
    - **E**rrors: error count
- Use `RED` for microservices, `USE` for nodes, disks, and networks

---

## Dashboard Design Principles

- Start with the user journey, not the infrastructure
- Layer dashboards:
    - Level 1: business health (revenue, user activity)
    - Level 2: service health (latency, errors, throughput)
    - Level 3: infrastructure health (CPU, memory, disk)
- Use consistent color coding:
    - Green = healthy, Yellow = warning, Red = critical
- Avoid vanity metrics that do not drive decisions

---

## Observability in Kubernetes

- `Kubernetes` adds unique observability challenges:
    - Pods are ephemeral: logs disappear when pods restart
    - Service mesh (`Istio`, `Linkerd`) provides automatic tracing
    - Node-level metrics vs pod-level metrics
- Common stack:
    - `kube-state-metrics` for cluster state
    - `node-exporter` for node hardware metrics
    - `DaemonSet`-deployed log collectors (`Fluent Bit`)
    - `OTel Collector` as a sidecar or `DaemonSet`

---

## Cost Management

- Observability costs can grow faster than infrastructure costs
- Key levers for cost control:
    - Reduce log verbosity in production
    - Sample traces instead of collecting 100%
    - Drop unused metrics at the collector level
    - Set retention tiers: hot (fast queries), warm, cold (archive)
    - Use `OpenTelemetry` processors to filter before export

---

## Anti-Patterns to Avoid

- Collecting everything without a plan (data hoarding)
- Alerting on metrics nobody looks at
- Using averages instead of percentiles for latency
- No correlation between metrics, logs, and traces
- Building dashboards after incidents instead of before
- Treating observability as an afterthought rather than a design concern

---

## Maturity Model

| Level | Characteristics |
|-------|----------------|
| 1. Reactive | Basic infrastructure monitoring, manual log checking |
| 2. Proactive | Structured logging, basic dashboards, threshold alerts |
| 3. Integrated | Correlated signals, SLO-based alerts, runbooks |
| 4. Advanced | Distributed tracing, error budgets, automated remediation |
| 5. Optimized | AIOps, predictive scaling, continuous SLO refinement |

---

## Key Takeaways

- Use all three signal types: metrics for trends, logs for details, traces for flow
- Correlate signals with shared identifiers like `trace_id`
- Choose push vs pull based on your network topology and workload types
- Centralize for consistency; distribute for autonomy
- Alert on user impact (`SLOs`), not raw metrics
- Treat on-call health as seriously as system health
- Observability is a continuous investment, not a one-time project
