# Deployment Patterns

Advanced Kubernetes Course - Day 3, Module 3

---

## Module Overview

- Rolling updates deep dive
- Blue-green deployments
- Canary deployments
- A/B testing
- Feature flags integration
- Progressive delivery with `Argo Rollouts`

---

## Rolling Update Strategy

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  template:
    spec:
      containers:
      - name: web
        image: myapp:v2
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Rolling Update Visualization

![rolling_update_visualization](svg/courses/devops/advanced-kubernetes/13_deployment_patterns/rolling_update_visualization.svg)

---

## Rolling Update Commands

```bash
# Trigger rolling update
kubectl set image deployment/web web=myapp:v3

# Or with apply
kubectl apply -f deployment-v3.yaml

# Watch rollout progress
kubectl rollout status deployment/web

# View rollout history
kubectl rollout history deployment/web
kubectl rollout history deployment/web --revision=2

# Pause rollout (for investigation)
kubectl rollout pause deployment/web

# Resume rollout
kubectl rollout resume deployment/web

# Rollback to previous version
kubectl rollout undo deployment/web

# Rollback to specific revision
kubectl rollout undo deployment/web --to-revision=3
```

---

## Blue-Green Deployment

![blue_green_deployment](svg/courses/devops/advanced-kubernetes/13_deployment_patterns/blue_green_deployment.svg)

---

## Blue-Green Implementation

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      version: blue
  template:
    metadata:
      labels:
        app: web
        version: blue
    spec:
      containers:
      - name: web
        image: myapp:v1
---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      version: green
  template:
    metadata:
      labels:
        app: web
        version: green
    spec:
      containers:
      - name: web
        image: myapp:v2
```

---

## Blue-Green Service Switch

```yaml
# Service pointing to blue (current)
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
    version: blue    # ← Change this to switch
  ports:
  - port: 80
    targetPort: 8080
```

```bash
# Test green before switching
kubectl port-forward svc/web-green-test 8081:80
curl localhost:8081/health

# Switch traffic to green
kubectl patch service web \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback (switch back to blue)
kubectl patch service web \
  -p '{"spec":{"selector":{"version":"blue"}}}'

# Cleanup old version after validation
kubectl delete deployment web-blue
```

---

## Blue-Green Pros and Cons

| Pros | Cons |
|------|------|
| Instant rollback | Double resources needed |
| Full testing before switch | Database migrations tricky |
| Zero downtime | Long-lived connections may break |
| Simple mental model | Cost overhead |

---

## Canary Deployment

![canary_deployment](svg/courses/devops/advanced-kubernetes/13_deployment_patterns/canary_deployment.svg)

---

## Canary with `Istio`

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: web
spec:
  hosts:
  - web
  http:
  - route:
    - destination:
        host: web
        subset: stable
      weight: 95
    - destination:
        host: web
        subset: canary
      weight: 5
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: web
spec:
  host: web
  subsets:
  - name: stable
    labels:
      version: v1
  - name: canary
    labels:
      version: v2
```

---

## Canary Analysis Metrics

Monitor these during canary phase:

```promql
# Error rate comparison
# Canary error rate
sum(rate(http_requests_total{
  version="v2", status=~"5.."}[5m]))
/
sum(rate(http_requests_total{version="v2"}[5m]))

# Stable error rate
sum(rate(http_requests_total{
  version="v1", status=~"5.."}[5m]))
/
sum(rate(http_requests_total{version="v1"}[5m]))

# Latency comparison (p99)
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket{
    version="v2"}[5m]))
```

**Auto-rollback criteria:**
- Error rate > 5% higher than stable
- P99 latency > 2x stable
- Custom business metrics degraded

---

## `Argo Rollouts` - Progressive Delivery

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: web
spec:
  replicas: 10
  strategy:
    canary:
      canaryService: web-canary
      stableService: web-stable
      trafficRouting:
        istio:
          virtualServices:
          - name: web
            routes:
            - primary
      steps:
      - setWeight: 5
      - pause: {duration: 5m}
      - setWeight: 20
      - pause: {duration: 10m}
      - setWeight: 50
      - pause: {duration: 10m}
      - setWeight: 80
      - pause: {duration: 5m}
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 2
        args:
        - name: service-name
          value: web-canary
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:v2
        ports:
        - containerPort: 8080
```

---

## `Argo Rollouts` Analysis Template

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 60s
    count: 5
    successCondition: result[0] >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{
            service="{{args.service-name}}",
            status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total{
            service="{{args.service-name}}"}[5m]))
  - name: latency
    interval: 60s
    count: 5
    successCondition: result[0] < 0.5
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket{
              service="{{args.service-name}}"}[5m]))
```

---

## `Argo Rollouts` Commands

```bash
# Install Argo Rollouts
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f \
  https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# Install kubectl plugin
kubectl argo rollouts version

# Watch rollout
kubectl argo rollouts get rollout web -w

# Promote to next step
kubectl argo rollouts promote web

# Full promote (skip remaining steps)
kubectl argo rollouts promote web --full

# Abort rollout (automatic rollback)
kubectl argo rollouts abort web

# Retry aborted rollout
kubectl argo rollouts retry rollout web

# View dashboard
kubectl argo rollouts dashboard
```

---

## Blue-Green with `Argo Rollouts`

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: web
spec:
  replicas: 5
  strategy:
    blueGreen:
      activeService: web-active
      previewService: web-preview
      autoPromotionEnabled: false
      prePromotionAnalysis:
        templates:
        - templateName: smoke-test
        args:
        - name: service-url
          value: http://web-preview
      postPromotionAnalysis:
        templates:
        - templateName: success-rate
      scaleDownDelaySeconds: 300
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:v2
```

---

## A/B Testing with Header-Based Routing

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: web
spec:
  hosts:
  - web.example.com
  http:
  # A/B test: New checkout for 10% of users
  - match:
    - headers:
        x-user-group:
          exact: experiment-checkout-v2
    route:
    - destination:
        host: web
        subset: v2-checkout
  # Cookie-based sticky routing
  - match:
    - headers:
        cookie:
          regex: ".*ab_group=treatment.*"
    route:
    - destination:
        host: web
        subset: treatment
  # Default
  - route:
    - destination:
        host: web
        subset: control
```

---

## Deployment Strategy Decision Matrix

| Criteria | Rolling | Blue-Green | Canary |
|----------|---------|------------|--------|
| Zero downtime | Yes | Yes | Yes |
| Instant rollback | No | Yes | Yes (with mesh) |
| Resource overhead | Low | 2x | Low-Medium |
| Risk | Medium | Low | Very Low |
| Complexity | Low | Medium | High |
| Traffic control | No | All-or-nothing | Granular |
| Best for | Most apps | Critical apps | High-traffic |

---

## Feature Flags Integration

```yaml
# ConfigMap for feature flags
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  flags.json: |
    {
      "new-checkout": {
        "enabled": true,
        "percentage": 10,
        "allowlist": ["user-123", "user-456"]
      },
      "dark-mode": {
        "enabled": true,
        "percentage": 100
      },
      "ai-recommendations": {
        "enabled": false
      }
    }
```

Combine with deployment patterns for safe feature delivery:
1. Deploy code with feature flag **off**
2. Gradually enable via flag (no redeploy needed)
3. Roll back by disabling flag (instant)

---

## Lab: Deployment Patterns

```bash
# 1. Rolling update
kubectl apply -f rolling-v1.yaml
kubectl set image deployment/web web=myapp:v2
kubectl rollout status deployment/web

# 2. Blue-green deployment
kubectl apply -f blue-deployment.yaml
kubectl apply -f green-deployment.yaml
kubectl patch svc web -p '{"spec":{"selector":{"version":"green"}}}'

# 3. Canary with Argo Rollouts
kubectl apply -f argo-rollout.yaml
kubectl argo rollouts set image web web=myapp:v3
kubectl argo rollouts get rollout web -w

# 4. Automated analysis
kubectl apply -f analysis-template.yaml
# Watch automated promotion/rollback
kubectl argo rollouts get rollout web -w
```
