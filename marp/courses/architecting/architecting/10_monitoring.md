# Monitoring and Observability
## Modern Architecture Course

---
## Agenda
1. Introduction to Observability
1. The Three Pillars
1. Logging Strategies
1. Metrics Collection
1. Tracing Implementation
1. Alerting Systems
1. Dashboard Design
1. Best Practices
---
## What is Observability?
- Ability to understand internal state from external outputs
- Beyond traditional monitoring
- Debug problems you haven't predicted
- Understand system behavior
- Make data-driven decisions
---
## The Three Pillars of Observability

![the_three_pillars_of_observability](/out/mermaid/courses/architecting/architecting/10_monitoring/the_three_pillars_of_observability.svg)

---

## Logs vs Metrics vs Traces

| Type | Format | Cardinality | Use Case |
|------|---------|------------|-----------|
| Logs | Text | High | Debugging |
| Metrics | Numbers | Low | Patterns/Alerts |
| Traces | Graphs | Medium | Performance |

---

## Logging Levels

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.debug("Detailed information")
logger.info("General information")
logger.warning("Warning messages")
logger.error("Error messages")
logger.critical("Critical failures")
```

---

## Structured Logging

```python
import structlog

logger = structlog.get_logger()

logger.info("order_processed",
    order_id="12345",
    customer_id="CUS789",
    amount=99.99,
    status="completed",
    processing_time_ms=150
)
```

---

## ELK Stack Architecture

![elk_stack_architecture](/out/mermaid/courses/architecting/architecting/10_monitoring/elk_stack_architecture.svg)

---

## Elasticsearch Template

```json
{
  "template": "logs-*",
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "service": { "type": "keyword" },
      "level": { "type": "keyword" },
      "message": { "type": "text" },
      "trace_id": { "type": "keyword" },
      "duration_ms": { "type": "long" }
    }
  }
}
```

---

## Metrics Collection

1. System Metrics
   - CPU, Memory, Disk, Network
1. Application Metrics
   - Response time, Error rates
1. Business Metrics
   - Transactions, Users, Revenue

---

## Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, start_http_server

# Counter for total requests
requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

# Histogram for response time
response_time = Histogram(
    'http_response_time_seconds',
    'Response time in seconds',
    ['endpoint']
)

@response_time.time()
def process_request():
    requests_total.labels(
        method='POST',
        endpoint='/api/orders'
    ).inc()
    # Process request...
```

---

## Distributed Tracing

![distributed_tracing](/out/mermaid/courses/architecting/architecting/10_monitoring/distributed_tracing.svg)

---

## OpenTelemetry Example

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("process_order")
def process_order(order_id):
    with tracer.start_span("validate_order") as span:
        span.set_attribute("order_id", order_id)
        # Validation logic

    with tracer.start_span("payment_processing") as span:
        try:
            process_payment()
            span.set_status(Status(StatusCode.OK))
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
```

---

## Alert Definition

```yaml
alert: HighErrorRate
expr: |
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
  > 0.01
for: 5m
labels:
  severity: critical
  team: backend
annotations:
  summary: High error rate detected
  description: Error rate above 1% for 5 minutes
```

---

## Alert Routing

![alert_routing](/out/mermaid/courses/architecting/architecting/10_monitoring/alert_routing.svg)

---

## Anomaly Detection

```python
from sklearn.ensemble import IsolationForest

def detect_anomalies(metrics_df):
    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    predictions = model.fit_predict(metrics_df)
    anomalies = metrics_df[predictions == -1]

    alert_on_anomalies(anomalies)
```

---

## Dashboard Design Principles

1. Purpose-driven layout
1. Clear hierarchy
1. Consistent metrics
1. Interactive elements
1. Responsive design

---

## Grafana Dashboard Example

```javascript
{
  "dashboard": {
    "title": "Service Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [{
          "expr": "rate(http_requests_total[5m])"
        }]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [{
          "expr": "rate(http_errors_total[5m])"
        }]
      }
    ]
  }
}
```

---

## SLI/SLO Implementation

```python
def calculate_sli():
    # Get metrics from Prometheus
    success_rate = prom.query("""
        sum(rate(http_requests_total{status=~"2.."}[1h]))
        /
        sum(rate(http_requests_total[1h]))
    """)

    latency_p95 = prom.query("""
        histogram_quantile(0.95,
            sum(rate(http_latency_bucket[1h]))
            by (le)
        )
    """)

    return {
        "availability": success_rate,
        "latency_p95": latency_p95
    }
```

---

## Error Budget Tracking

```python
class ErrorBudget:
    def __init__(self, slo_target, time_window):
        self.slo_target = slo_target
        self.time_window = time_window

    def calculate_remaining(self):
        current_availability = get_availability()
        error_budget = 1 - self.slo_target
        used_budget = 1 - current_availability

        return max(0, error_budget - used_budget)
```

---

## Monitoring as Code

```terraform
resource "grafana_dashboard" "service_overview" {
  config_json = jsonencode({
    title = "Service Overview"
    panels = [
      {
        title = "Request Rate"
        type  = "graph"
        datasource = "Prometheus"
      },
      {
        title = "Error Rate"
        type  = "graph"
        datasource = "Prometheus"
      }
    ]
  })
}
```

---

## Incident Response Integration

```python
def handle_alert(alert):
    # Create incident
    incident = create_pagerduty_incident(alert)

    # Gather context
    context = {
        "logs": fetch_relevant_logs(alert.timeframe),
        "metrics": fetch_related_metrics(alert.timeframe),
        "traces": fetch_related_traces(alert.trace_id)
    }

    # Update incident
    update_incident(incident.id, context)
```

---

## Cost of Monitoring

![cost_of_monitoring](/out/mermaid/courses/architecting/architecting/10_monitoring/cost_of_monitoring.svg)

---

## Retention Policies

```yaml
retention:
  logs:
    hot: 7d
    warm: 30d
    cold: 90d
  metrics:
    raw: 15d
    aggregated: 365d
  traces:
    sampled: 7d
    errors: 30d
```

---

## System Health Score

```python
def calculate_health_score():
    metrics = {
        "availability": get_availability_score(),
        "latency": get_latency_score(),
        "error_rate": get_error_score(),
        "saturation": get_saturation_score()
    }

    weights = {
        "availability": 0.4,
        "latency": 0.3,
        "error_rate": 0.2,
        "saturation": 0.1
    }

    return sum(score * weights[metric]
              for metric, score in metrics.items())
```

---

## Best Practices

1. Start with business objectives
1. Use structured logging
1. Implement proper sampling
1. Set meaningful alerts
1. Automate responses
1. Regular review and updates
1. Documentation

---

## Future Trends

1. AI-powered analysis
1. Automated remediation
1. Chaos engineering integration
1. Real-time visualization
1. Predictive monitoring
