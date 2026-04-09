# Use Cases, Best Practices & Real-Life Examples

Advanced Kubernetes Course - Day 3, Module 2

---

## Module Overview

- Production-ready `Kubernetes` patterns
- Microservices architecture on `Kubernetes`
- Multi-tenancy
- Cost optimization
- Security hardening
- Disaster recovery

---

## Production Checklist

```misc
□ Resource requests and limits on all containers
□ Liveness and readiness probes configured
□ PodDisruptionBudgets for critical workloads
□ Anti-affinity rules for high availability
□ NetworkPolicies restricting traffic
□ RBAC with least-privilege access
□ Secrets encrypted at rest
□ Container images scanned and signed
□ Pod Security Standards enforced
□ Monitoring and alerting configured
□ Backup and disaster recovery tested
□ Resource quotas per namespace
□ Horizontal Pod Autoscaler configured
□ Ingress with TLS termination
□ Log aggregation operational
```

---

## Microservices on `Kubernetes`

![microservices_on_kubernetes](svg/courses/devops/advanced-kubernetes/12_use_cases_best_practices/microservices_on_kubernetes.svg)

---

## Namespace Strategy

```yaml
# Namespace per environment
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# Namespace per team
apiVersion: v1
kind: Namespace
metadata:
  name: team-payments
  labels:
    team: payments
    cost-center: "CC-1234"
```

| Strategy | Pros | Cons |
|----------|------|------|
| Per environment | Simple, clear | Teams share namespace |
| Per team | Team isolation | Env separation lost |
| Per service | Maximum isolation | Overhead, many namespaces |
| Hybrid (team+env) | Best of both | Complexity |

---

## Multi-Tenancy Patterns

**Namespace-based isolation:**
```yaml
# ResourceQuota per tenant
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-alpha-quota
  namespace: tenant-alpha
spec:
  hard:
    requests.cpu: "8"
    requests.memory: "16Gi"
    limits.cpu: "16"
    limits.memory: "32Gi"
    pods: "50"
    services: "20"

---
# NetworkPolicy isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-cross-tenant
  namespace: tenant-alpha
spec:
  podSelector: {}
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector: {}
```

---

## Pod Security Standards

```yaml
# Enforce restricted security on namespace
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
```

**Restricted pod example:**
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:v2
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop: ["ALL"]
```

---

## Image Security

```yaml
# Only allow images from trusted registries
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: image-policy
webhooks:
- name: images.policy.example.com
  rules:
  - apiGroups: [""]
    apiVersions: ["v1"]
    operations: ["CREATE", "UPDATE"]
    resources: ["pods"]
  # webhook validates image source
```

```bash
# Scan images with trivy
trivy image myapp:v2

# Sign images with cosign
cosign sign --key cosign.key registry.example.com/myapp:v2

# Verify signatures
cosign verify --key cosign.pub registry.example.com/myapp:v2
```

---

## Cost Optimization Strategies

![cost_optimization_strategies](svg/courses/devops/advanced-kubernetes/12_use_cases_best_practices/cost_optimization_strategies.svg)

---

## Spot Instance Usage

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
spec:
  replicas: 10
  template:
    spec:
      nodeSelector:
        node.kubernetes.io/instance-type: spot
      tolerations:
      - key: "kubernetes.io/spot"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"
      terminationGracePeriodSeconds: 30
      containers:
      - name: processor
        image: batch:v1
        lifecycle:
          preStop:
            exec:
              command:
              - /bin/sh
              - -c
              - |
                # Save checkpoint before eviction
                curl -X POST http://localhost:8080/checkpoint
                sleep 5
```

---

## Health Check Endpoint Pattern

```go
package main

import (
    "database/sql"
    "encoding/json"
    "net/http"
    "sync/atomic"
)

var ready int32

type HealthResponse struct {
    Status  string            `json:"status"`
    Checks  map[string]string `json:"checks"`
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("ok"))
}

func readyHandler(db *sql.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        resp := HealthResponse{
            Status: "ok",
            Checks: make(map[string]string),
        }

        // Check database
        if err := db.Ping(); err != nil {
            resp.Status = "degraded"
            resp.Checks["database"] = err.Error()
        } else {
            resp.Checks["database"] = "ok"
        }

        // Check if ready
        if atomic.LoadInt32(&ready) == 0 {
            resp.Status = "not_ready"
            w.WriteHeader(http.StatusServiceUnavailable)
        }

        json.NewEncoder(w).Encode(resp)
    }
}
```

---

## Graceful Shutdown Pattern

```go
func main() {
    srv := &http.Server{Addr: ":8080"}

    // Start server
    go func() {
        if err := srv.ListenAndServe(); err != nil &&
            err != http.ErrServerClosed {
            log.Fatalf("listen: %s\n", err)
        }
    }()

    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    log.Println("Shutting down server...")

    // Mark as not ready (readiness probe fails)
    atomic.StoreInt32(&ready, 0)

    // Wait for load balancer to remove us
    time.Sleep(5 * time.Second)

    // Graceful shutdown with timeout
    ctx, cancel := context.WithTimeout(
        context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }

    log.Println("Server exited properly")
}
```

---

## Disaster Recovery Strategy

![disaster_recovery_strategy](svg/courses/devops/advanced-kubernetes/12_use_cases_best_practices/disaster_recovery_strategy.svg)

---

## `Velero` Backup and Restore

```bash
# Install Velero
velero install \
  --provider aws \
  --bucket velero-backups \
  --secret-file ./credentials \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1

# Create backup
velero backup create prod-backup \
  --include-namespaces production \
  --include-resources deployments,services,configmaps,secrets,pvc

# Schedule regular backups
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces production \
  --ttl 720h

# Restore
velero restore create --from-backup prod-backup \
  --namespace-mappings production:production-restored
```

---

## Monitoring Best Practices

```yaml
# Golden signals alerting
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: golden-signals
spec:
  groups:
  - name: golden-signals
    rules:
    # Latency
    - alert: HighLatency
      expr: |
        histogram_quantile(0.99,
          rate(http_request_duration_seconds_bucket[5m])
        ) > 1
      for: 5m
      labels: {severity: warning}

    # Traffic drop
    - alert: TrafficDrop
      expr: |
        sum(rate(http_requests_total[5m]))
        < sum(rate(http_requests_total[5m] offset 1h)) * 0.5
      for: 10m
      labels: {severity: critical}

    # Saturation
    - alert: HighMemoryUsage
      expr: |
        container_memory_working_set_bytes
        / container_spec_memory_limit_bytes > 0.9
      for: 5m
      labels: {severity: warning}
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Better Approach |
|-------------|----------------|
| Running as root | `runAsNonRoot: true` |
| No resource limits | Always set requests + limits |
| `latest` image tag | Pin specific versions |
| Storing secrets in `ConfigMaps` | Use `Secrets` + encryption |
| Single replica in prod | 3+ replicas with PDB |
| No health probes | Liveness + readiness + startup |
| Hardcoded configs | `ConfigMaps` + `Secrets` |
| No `NetworkPolicies` | Deny-all, then allow specific |
| Manual deployments | GitOps with `ArgoCD`/`Flux` |
| No backup strategy | `Velero` + `etcd` backups |

---

## Lab: Production Readiness Review

```bash
# 1. Deploy a "bad" application
kubectl apply -f bad-app.yaml

# 2. Identify issues using:
kubectl get pods -o wide
kubectl describe pod <pod>
kubectl top pods
kubectl get events --sort-by=.lastTimestamp

# 3. Fix each issue:
# - Add resource limits
# - Add probes
# - Add PDB
# - Add NetworkPolicy
# - Fix security context
# - Add anti-affinity

# 4. Apply fixes
kubectl apply -f good-app.yaml

# 5. Verify all checks pass
kubectl get pods,pdb,networkpolicy
```
