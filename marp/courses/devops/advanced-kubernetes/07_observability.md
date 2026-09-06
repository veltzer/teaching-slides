---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - practices:devops
  - languages:go
  - concepts:service-mesh
level: advanced
category: devops
audience:
  - audiences:developers

---

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

![three_pillars_of_observability](svg/courses/devops/advanced-kubernetes/07_observability/three_pillars_of_observability.svg)

---

## `Prometheus` Architecture

![prometheus_architecture](svg/courses/devops/advanced-kubernetes/07_observability/prometheus_architecture.svg)

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
```

---

## `OpenTelemetry` Collector: Exporters and Pipelines

```yaml
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

![trace_visualization](svg/courses/devops/advanced-kubernetes/07_observability/trace_visualization.svg)

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

![slos_and_error_budgets](svg/courses/devops/advanced-kubernetes/07_observability/slos_and_error_budgets.svg)

---

## SLOs and Error Budgets: Example

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
