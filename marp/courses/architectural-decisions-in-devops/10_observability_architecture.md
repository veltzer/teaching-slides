# Observability Architecture

---

## What is Observability?

- The ability to understand a system's internal state from its external outputs
- Goes beyond traditional monitoring: not just "is it up?"
- Enables answering novel questions about production systems
- Critical for operating distributed, microservice-based architectures

---

## The Three Pillars of Observability

<svg width="700" height="380" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="50" y="60" width="180" height="120" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="140" y="95" text-anchor="middle" font-size="16" font-weight="bold" fill="#1565c0">Metrics</text>
  <text x="140" y="120" text-anchor="middle" font-size="12">Numeric aggregates</text>
  <text x="140" y="140" text-anchor="middle" font-size="12">over time</text>
  <text x="140" y="160" text-anchor="middle" font-size="12">CPU, latency, errors</text>
  <rect x="260" y="60" width="180" height="120" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="350" y="95" text-anchor="middle" font-size="16" font-weight="bold" fill="#2e7d32">Logs</text>
  <text x="350" y="120" text-anchor="middle" font-size="12">Discrete events</text>
  <text x="350" y="140" text-anchor="middle" font-size="12">with context</text>
  <text x="350" y="160" text-anchor="middle" font-size="12">Errors, audit, debug</text>
  <rect x="470" y="60" width="180" height="120" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="8"/>
  <text x="560" y="95" text-anchor="middle" font-size="16" font-weight="bold" fill="#f9a825">Traces</text>
  <text x="560" y="120" text-anchor="middle" font-size="12">Request flow across</text>
  <text x="560" y="140" text-anchor="middle" font-size="12">services</text>
  <text x="560" y="160" text-anchor="middle" font-size="12">Latency, dependencies</text>
  <line x1="230" y1="180" x2="260" y2="180" stroke="#555" stroke-width="2" stroke-dasharray="5,3"/>
  <line x1="440" y1="180" x2="470" y2="180" stroke="#555" stroke-width="2" stroke-dasharray="5,3"/>
  <rect x="180" y="240" width="340" height="60" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="8"/>
  <text x="350" y="275" text-anchor="middle" font-size="16" font-weight="bold" fill="#7b1fa2">Correlation Layer</text>
  <line x1="140" y1="180" x2="270" y2="240" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="350" y1="180" x2="350" y2="240" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="560" y1="180" x2="430" y2="240" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="350" y="340" text-anchor="middle" font-size="13" fill="#555">Each pillar answers different questions about system behavior</text>
</svg>

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

<svg width="700" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <text x="175" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#1565c0">Pull Model</text>
  <rect x="100" y="50" width="150" height="50" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="175" y="80" text-anchor="middle" font-size="14">Prometheus</text>
  <rect x="30" y="150" width="120" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="1" rx="4"/>
  <text x="90" y="175" text-anchor="middle" font-size="12">Service A</text>
  <rect x="170" y="150" width="120" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="1" rx="4"/>
  <text x="230" y="175" text-anchor="middle" font-size="12">Service B</text>
  <path d="M 150 100 L 90 150" stroke="#1565c0" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 200 100 L 230 150" stroke="#1565c0" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="70" y="130" font-size="10" fill="#1565c0">scrape</text>
  <text x="230" y="130" font-size="10" fill="#1565c0">scrape</text>
  <text x="525" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#2e7d32">Push Model</text>
  <rect x="450" y="50" width="150" height="50" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="525" y="80" text-anchor="middle" font-size="14">Collector</text>
  <rect x="380" y="150" width="120" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="4"/>
  <text x="440" y="175" text-anchor="middle" font-size="12">Service A</text>
  <rect x="520" y="150" width="120" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="4"/>
  <text x="580" y="175" text-anchor="middle" font-size="12">Service B</text>
  <path d="M 440 150 L 490 100" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 580 150 L 560 100" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="440" y="130" font-size="10" fill="#2e7d32">push</text>
  <text x="580" y="130" font-size="10" fill="#2e7d32">push</text>
  <line x1="350" y1="20" x2="350" y2="260" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="175" y="230" text-anchor="middle" font-size="11" fill="#555">Server controls scrape rate</text>
  <text x="525" y="230" text-anchor="middle" font-size="11" fill="#555">Agents push to collector</text>
</svg>

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

<svg width="700" height="320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="40" width="130" height="50" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="85" y="70" text-anchor="middle" font-size="13" font-weight="bold">Metrics</text>
  <rect x="180" y="40" width="130" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="6"/>
  <text x="245" y="70" text-anchor="middle" font-size="13" font-weight="bold">Alert Rules</text>
  <rect x="340" y="40" width="130" height="50" fill="#ffccbc" stroke="#e64a19" stroke-width="2" rx="6"/>
  <text x="405" y="70" text-anchor="middle" font-size="13" font-weight="bold">Alert Manager</text>
  <rect x="340" y="120" width="130" height="35" fill="#e8eaf6" stroke="#3949ab" stroke-width="1" rx="4"/>
  <text x="405" y="143" text-anchor="middle" font-size="11">Grouping</text>
  <rect x="340" y="165" width="130" height="35" fill="#e8eaf6" stroke="#3949ab" stroke-width="1" rx="4"/>
  <text x="405" y="188" text-anchor="middle" font-size="11">Deduplication</text>
  <rect x="340" y="210" width="130" height="35" fill="#e8eaf6" stroke="#3949ab" stroke-width="1" rx="4"/>
  <text x="405" y="233" text-anchor="middle" font-size="11">Silencing</text>
  <rect x="540" y="90" width="130" height="35" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="605" y="113" text-anchor="middle" font-size="12">Slack / Email</text>
  <rect x="540" y="145" width="130" height="35" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="6"/>
  <text x="605" y="168" text-anchor="middle" font-size="12">PagerDuty</text>
  <rect x="540" y="200" width="130" height="35" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="6"/>
  <text x="605" y="223" text-anchor="middle" font-size="12">Webhook</text>
  <line x1="150" y1="65" x2="180" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="310" y1="65" x2="340" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="405" y1="90" x2="405" y2="120" stroke="#3949ab" stroke-width="1" marker-end="url(#arrow3)"/>
  <line x1="470" y1="137" x2="540" y2="107" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="470" y1="182" x2="540" y2="162" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="470" y1="227" x2="540" y2="217" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="350" y="290" text-anchor="middle" font-size="12" fill="#555">Alerts flow from metrics through rules, processing, then routing</text>
</svg>

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

<svg width="700" height="340" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="200" y="20" width="300" height="55" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="8"/>
  <text x="350" y="42" text-anchor="middle" font-size="14" font-weight="bold" fill="#c62828">SLA (Service Level Agreement)</text>
  <text x="350" y="62" text-anchor="middle" font-size="11" fill="#555">Contract with customers, financial penalties</text>
  <rect x="200" y="100" width="300" height="55" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="8"/>
  <text x="350" y="122" text-anchor="middle" font-size="14" font-weight="bold" fill="#f9a825">SLO (Service Level Objective)</text>
  <text x="350" y="142" text-anchor="middle" font-size="11" fill="#555">Internal target, tighter than SLA</text>
  <rect x="200" y="180" width="300" height="55" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="350" y="202" text-anchor="middle" font-size="14" font-weight="bold" fill="#2e7d32">SLI (Service Level Indicator)</text>
  <text x="350" y="222" text-anchor="middle" font-size="11" fill="#555">The actual metric being measured</text>
  <line x1="350" y1="75" x2="350" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="350" y1="155" x2="350" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="560" y="45" font-size="11" fill="#c62828">99.9% availability/month</text>
  <text x="560" y="125" font-size="11" fill="#f9a825">99.95% availability/month</text>
  <text x="560" y="205" font-size="11" fill="#2e7d32">successful_requests / total</text>
  <rect x="200" y="260" width="300" height="55" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="350" y="282" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565c0">Error Budget</text>
  <text x="350" y="302" text-anchor="middle" font-size="11" fill="#555">Allowed failures = 1 - SLO target</text>
  <line x1="350" y1="235" x2="350" y2="260" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
</svg>

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

<svg width="700" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="50" y="30" width="160" height="50" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="6"/>
  <text x="130" y="60" text-anchor="middle" font-size="14" font-weight="bold">Alert Fires</text>
  <rect x="50" y="120" width="160" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="6"/>
  <text x="130" y="140" text-anchor="middle" font-size="13" font-weight="bold">Primary On-Call</text>
  <text x="130" y="158" text-anchor="middle" font-size="11">Ack within 5 min</text>
  <rect x="270" y="120" width="160" height="50" fill="#ffe0b2" stroke="#e65100" stroke-width="2" rx="6"/>
  <text x="350" y="140" text-anchor="middle" font-size="13" font-weight="bold">Secondary On-Call</text>
  <text x="350" y="158" text-anchor="middle" font-size="11">Ack within 10 min</text>
  <rect x="490" y="120" width="160" height="50" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="6"/>
  <text x="570" y="140" text-anchor="middle" font-size="13" font-weight="bold">Engineering Lead</text>
  <text x="570" y="158" text-anchor="middle" font-size="11">Ack within 15 min</text>
  <line x1="130" y1="80" x2="130" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="210" y1="145" x2="270" y2="145" stroke="#e65100" stroke-width="2" marker-end="url(#arrow5)"/>
  <text x="240" y="138" font-size="10" fill="#e65100">no ack</text>
  <line x1="430" y1="145" x2="490" y2="145" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrow5)"/>
  <text x="460" y="138" font-size="10" fill="#7b1fa2">no ack</text>
  <rect x="50" y="210" width="600" height="50" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="350" y="230" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">Incident Response</text>
  <text x="350" y="248" text-anchor="middle" font-size="11" fill="#555">Follow runbook, communicate status, resolve or escalate</text>
  <line x1="130" y1="170" x2="130" y2="210" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow5)"/>
  <text x="145" y="195" font-size="10" fill="#2e7d32">ack</text>
</svg>

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

<svg width="700" height="260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow6" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="50" width="100" height="60" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="70" y="75" text-anchor="middle" font-size="11" font-weight="bold">Applications</text>
  <text x="70" y="95" text-anchor="middle" font-size="10">SDK / Agent</text>
  <rect x="160" y="50" width="120" height="60" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="6"/>
  <text x="220" y="75" text-anchor="middle" font-size="11" font-weight="bold">Collector</text>
  <text x="220" y="95" text-anchor="middle" font-size="10">OTel Collector</text>
  <rect x="320" y="20" width="120" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="1" rx="4"/>
  <text x="380" y="45" text-anchor="middle" font-size="11">Filter / Enrich</text>
  <rect x="320" y="80" width="120" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="1" rx="4"/>
  <text x="380" y="105" text-anchor="middle" font-size="11">Sample / Batch</text>
  <rect x="490" y="15" width="100" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="540" y="40" text-anchor="middle" font-size="11" font-weight="bold">Metrics DB</text>
  <rect x="490" y="65" width="100" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="540" y="90" text-anchor="middle" font-size="11" font-weight="bold">Log Store</text>
  <rect x="490" y="115" width="100" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="540" y="140" text-anchor="middle" font-size="11" font-weight="bold">Trace Store</text>
  <rect x="630" y="65" width="55" height="40" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="6"/>
  <text x="658" y="90" text-anchor="middle" font-size="11" font-weight="bold">UI</text>
  <line x1="120" y1="80" x2="160" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrow6)"/>
  <line x1="280" y1="80" x2="320" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrow6)"/>
  <line x1="440" y1="40" x2="490" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arrow6)"/>
  <line x1="440" y1="80" x2="490" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow6)"/>
  <line x1="440" y1="100" x2="490" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arrow6)"/>
  <line x1="590" y1="85" x2="630" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow6)"/>
  <text x="350" y="200" text-anchor="middle" font-size="12" fill="#555">Collectors process data before it reaches storage backends</text>
</svg>

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
