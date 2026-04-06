# Observability in `Kubernetes`

Advanced Kubernetes Course - Day 2, Module 2

---

## Module Overview

- The three pillars of observability
- `Prometheus` monitoring stack
- `Grafana` dashboards
- `OpenTelemetry` and distributed tracing
- Log aggregation
- Alerting strategies

---

## Three Pillars of Observability

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="220" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="630" height="200" rx="4" fill="#f8f9fa" stroke="#333" stroke-width="1.5"/>
  <text x="325" y="34" text-anchor="middle" font-size="16" fill="#222" font-weight="bold">Observability</text>
  <rect x="30" y="50" width="175" height="140" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="117" y="76" text-anchor="middle" font-size="15" fill="#222" font-weight="bold">Metrics</text>
  <text x="117" y="100" text-anchor="middle" font-size="11" fill="#444">Numbers over time</text>
  <text x="117" y="162" text-anchor="middle" font-size="11" fill="#666">Prometheus / Datadog</text>
  <rect x="230" y="50" width="175" height="140" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="317" y="76" text-anchor="middle" font-size="15" fill="#222" font-weight="bold">Logs</text>
  <text x="317" y="100" text-anchor="middle" font-size="11" fill="#444">Events with context</text>
  <text x="317" y="162" text-anchor="middle" font-size="11" fill="#666">Loki / EFK</text>
  <rect x="430" y="50" width="175" height="140" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="517" y="76" text-anchor="middle" font-size="15" fill="#222" font-weight="bold">Traces</text>
  <text x="517" y="100" text-anchor="middle" font-size="11" fill="#444">Request flow across services</text>
  <text x="517" y="162" text-anchor="middle" font-size="11" fill="#666">Jaeger / Tempo</text>
</svg>

---

## `Prometheus` Architecture

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="380" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="20" y="20" width="155" height="65" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="97" y="47" text-anchor="middle" font-size="13" fill="#222">App Pod</text>
  <text x="97" y="66" text-anchor="middle" font-size="11" fill="#555">/metrics</text>
  <rect x="240" y="20" width="155" height="65" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="317" y="47" text-anchor="middle" font-size="13" fill="#222">Node Exporter</text>
  <line x1="240" y1="52" x2="175" y2="52" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="97" y1="85" x2="97" y2="155" stroke="#555" stroke-width="1.5"/>
  <line x1="317" y1="85" x2="317" y2="155" stroke="#555" stroke-width="1.5"/>
  <line x1="97" y1="155" x2="220" y2="155" stroke="#555" stroke-width="1.5"/>
  <line x1="317" y1="155" x2="220" y2="155" stroke="#555" stroke-width="1.5"/>
  <line x1="220" y1="155" x2="220" y2="160" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="120" y="160" width="195" height="100" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="217" y="185" text-anchor="middle" font-size="13" fill="#222">Prometheus Server</text>
  <rect x="140" y="195" width="155" height="40" rx="4" fill="#fff" stroke="#777" stroke-width="1.5"/>
  <text x="217" y="220" text-anchor="middle" font-size="11" fill="#444">TSDB (Time Series DB)</text>
  <line x1="315" y1="210" x2="355" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="355" y="160" width="175" height="100" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="442" y="185" text-anchor="middle" font-size="13" fill="#222">Alertmanager</text>
  <text x="442" y="208" text-anchor="middle" font-size="11" fill="#555">→ Slack</text>
  <text x="442" y="224" text-anchor="middle" font-size="11" fill="#555">→ PagerDuty</text>
  <text x="442" y="240" text-anchor="middle" font-size="11" fill="#555">→ Email</text>
  <line x1="217" y1="260" x2="217" y2="295" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="120" y="295" width="195" height="65" rx="4" fill="#ede7f6" stroke="#333" stroke-width="1.5"/>
  <text x="217" y="322" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Grafana</text>
  <text x="217" y="342" text-anchor="middle" font-size="11" fill="#555">(Dashboards)</text>
</svg>

---

## Installing `Prometheus` Stack

```bash
# Add Helm repo
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

# Install kube-prometheus-stack
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
  --set grafana.adminPassword=admin123

# Verify installation
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

---

## `ServiceMonitor` - Declarative Scrape Config

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-server-monitor
  namespace: monitoring
  labels:
    release: monitoring
spec:
  namespaceSelector:
    matchNames:
    - production
  selector:
    matchLabels:
      app: api-server
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
    scheme: http
    tlsConfig:
      insecureSkipVerify: false
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: pod
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'go_gc_.*'
      action: drop
```

---

## `PodMonitor` - Direct Pod Scraping

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: envoy-metrics
  namespace: monitoring
spec:
  namespaceSelector:
    any: true
  selector:
    matchLabels:
      app.kubernetes.io/part-of: istio
  podMetricsEndpoints:
  - port: http-envoy-prom
    interval: 15s
    path: /stats/prometheus
```

---

## Exposing Application Metrics

```go
package main

import (
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )

    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request latency",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestsTotal)
    prometheus.MustRegister(httpRequestDuration)
}

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.HandleFunc("/api/orders", instrumentHandler(
        "GET", "/api/orders", ordersHandler))
    http.ListenAndServe(":8080", nil)
}
```

---

## `PromQL` - Essential Queries

```promql
# Request rate per second (last 5 minutes)
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket[5m]))

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m])) * 100

# Pod CPU usage
sum(rate(container_cpu_usage_seconds_total{
  namespace="production"}[5m])) by (pod)

# Pod memory usage in MB
sum(container_memory_working_set_bytes{
  namespace="production"}) by (pod) / 1024 / 1024

# Node disk usage percentage
100 - (node_filesystem_avail_bytes{mountpoint="/"}
/ node_filesystem_size_bytes{mountpoint="/"} * 100)
```

---

## `PrometheusRule` - Alerting Rules

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: app-alerts
  namespace: monitoring
  labels:
    release: monitoring
spec:
  groups:
  - name: application.rules
    rules:
    - alert: HighErrorRate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m])) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ $value | humanizePercentage }}"
    - alert: PodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total[15m])
        * 60 * 5 > 0
      for: 15m
      labels:
        severity: warning
      annotations:
        summary: "Pod {{ $labels.pod }} is crash looping"
```

---

## `Alertmanager` Configuration

```yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: alert-routing
  namespace: monitoring
spec:
  route:
    groupBy: ['alertname', 'namespace']
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 4h
    receiver: slack-notifications
    routes:
    - match:
        severity: critical
      receiver: pagerduty
    - match:
        severity: warning
      receiver: slack-notifications
  receivers:
  - name: slack-notifications
    slackConfigs:
    - channel: '#k8s-alerts'
      apiURL:
        name: slack-webhook
        key: url
      title: '[{{ .Status }}] {{ .CommonLabels.alertname }}'
      text: '{{ .CommonAnnotations.description }}'
  - name: pagerduty
    pagerdutyConfigs:
    - serviceKey:
        name: pagerduty-key
        key: service-key
```

---

## `OpenTelemetry` in `Kubernetes`

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-collector
  namespace: monitoring
spec:
  mode: daemonset
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      prometheus:
        config:
          scrape_configs:
          - job_name: 'kubernetes-pods'
            kubernetes_sd_configs:
            - role: pod
    processors:
      batch:
        timeout: 5s
        send_batch_size: 1000
      memory_limiter:
        limit_mib: 512
    exporters:
      otlp:
        endpoint: jaeger:4317
        tls:
          insecure: true
      prometheus:
        endpoint: 0.0.0.0:8889
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [otlp]
        metrics:
          receivers: [otlp, prometheus]
          processors: [memory_limiter, batch]
          exporters: [prometheus]
```

---

## Distributed Tracing with `OpenTelemetry`

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
)

func initTracer() (*sdktrace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(context.Background(),
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("order-service"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func handleOrder(w http.ResponseWriter, r *http.Request) {
    ctx, span := otel.Tracer("order-service").
        Start(r.Context(), "handleOrder")
    defer span.End()

    // Call downstream service with context propagation
    processPayment(ctx, orderID)
}
```

---

## Trace Visualization

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="300" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="150" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="80" y="34" text-anchor="middle" font-size="12" fill="#222">Order Service</text>
  <rect x="220" y="10" width="150" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="290" y="34" text-anchor="middle" font-size="12" fill="#222">Payment Service</text>
  <rect x="440" y="10" width="150" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="510" y="34" text-anchor="middle" font-size="12" fill="#222">Inventory Service</text>
  <line x1="80" y1="50" x2="80" y2="270" stroke="#bbb" stroke-width="1.5"/>
  <line x1="290" y1="50" x2="290" y2="270" stroke="#bbb" stroke-width="1.5"/>
  <line x1="510" y1="50" x2="510" y2="270" stroke="#bbb" stroke-width="1.5"/>
  <rect x="75" y="60" width="215" height="30" rx="4" fill="#e8f5e9" stroke="#4caf50" stroke-width="1.5"/>
  <text x="130" y="79" text-anchor="middle" font-size="11" fill="#2e7d32">handleOrder (12ms)</text>
  <rect x="285" y="100" width="230" height="30" rx="4" fill="#fff3e0" stroke="#ff9800" stroke-width="1.5"/>
  <text x="350" y="119" text-anchor="middle" font-size="11" fill="#e65100">processPayment (45ms)</text>
  <rect x="505" y="140" width="100" height="28" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
  <text x="555" y="159" text-anchor="middle" font-size="11" fill="#1565c0">checkStock (8ms)</text>
  <rect x="505" y="175" width="100" height="28" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
  <text x="555" y="194" text-anchor="middle" font-size="11" fill="#1565c0">reserve (15ms)</text>
  <rect x="15" y="218" width="160" height="40" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="95" y="242" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">Total: 80ms</text>
</svg>

---

## Grafana Dashboards via `ConfigMap`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-app
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  app-dashboard.json: |
    {
      "dashboard": {
        "title": "Application Overview",
        "panels": [
          {
            "title": "Request Rate",
            "type": "timeseries",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total[5m])) by (service)",
                "legendFormat": "{{service}}"
              }
            ]
          },
          {
            "title": "Error Rate",
            "type": "stat",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
              }
            ]
          }
        ]
      }
    }
```

---

## Key `Kubernetes` Metrics to Monitor

| Category | Metrics |
|----------|---------|
| **Cluster** | Node count, CPU/memory capacity |
| **Node** | CPU%, memory%, disk%, network |
| **Pod** | Restarts, CPU/memory usage, OOMKills |
| **Container** | Resource utilization vs requests |
| **Application** | Request rate, error rate, latency (RED) |
| **`API` Server** | Request latency, `etcd` latency |

```promql
# RED Method queries
# Rate
sum(rate(http_requests_total[5m]))
# Errors
sum(rate(http_requests_total{status=~"5.."}[5m]))
# Duration
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

---

## SLOs and Error Budgets

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="210" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <text x="310" y="24" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">SLA: 99.9% availability (43.8 min downtime/month)</text>
  <text x="310" y="46" text-anchor="middle" font-size="13" fill="#555">Error Budget = 1 − SLO = 0.1%</text>
  <rect x="20" y="58" width="580" height="130" rx="4" fill="#f8f9fa" stroke="#333" stroke-width="1.5"/>
  <text x="60" y="86" text-anchor="start" font-size="12" fill="#333">Month Progress</text>
  <rect x="200" y="72" width="300" height="22" rx="3" fill="#e0e0e0" stroke="#999" stroke-width="1.5"/>
  <rect x="200" y="72" width="225" height="22" rx="3" fill="#1976d2" stroke="#1976d2" stroke-width="1.5"/>
  <text x="510" y="88" text-anchor="start" font-size="12" fill="#1976d2">75%</text>
  <text x="60" y="120" text-anchor="start" font-size="12" fill="#333">Error Budget Used</text>
  <rect x="200" y="106" width="300" height="22" rx="3" fill="#e0e0e0" stroke="#999" stroke-width="1.5"/>
  <rect x="200" y="106" width="90" height="22" rx="3" fill="#4caf50" stroke="#4caf50" stroke-width="1.5"/>
  <text x="510" y="122" text-anchor="start" font-size="12" fill="#4caf50">30%</text>
  <text x="310" y="158" text-anchor="middle" font-size="13" fill="#2e7d32">Budget Remaining: 70%  ≈  13.1 minutes of downtime left</text>
</svg>

```promql
# SLO: 99.9% of requests succeed within 500ms
1 - (
  sum(rate(http_requests_total{status=~"5.."}[30d]))
  +
  sum(rate(http_request_duration_seconds_bucket{le="0.5"}[30d]))
) / sum(rate(http_requests_total[30d]))
```

---

## Lab: Set Up Observability Stack

```bash
# 1. Install Prometheus stack
helm install monitoring \
  prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace

# 2. Deploy a sample app with metrics
kubectl apply -f instrumented-app.yaml

# 3. Create ServiceMonitor
kubectl apply -f service-monitor.yaml

# 4. Access Grafana
kubectl port-forward -n monitoring \
  svc/monitoring-grafana 3000:80

# 5. Create alerting rules
kubectl apply -f prometheus-rules.yaml

# 6. Generate load and observe dashboards
hey -z 5m -q 50 http://app-service/api
```
