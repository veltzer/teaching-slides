# Serverless with `Knative`

Advanced Kubernetes Course - Day 3, Module 5

---

## Module Overview

- Serverless concepts on `Kubernetes`
- `Knative Serving`
- `Knative Eventing`
- Scale to zero
- Traffic management
- Event-driven architectures

---

## Why Serverless on `Kubernetes`?

```text
Traditional Kubernetes:
  Pods always running → costs even when idle

Serverless (Knative):
  Scale to zero → pay only for actual usage

┌─────────────────────────────────────────┐
│  Request Rate Over Time                 │
│                                         │
│  ▲                                      │
│  │    ╱╲      ╱╲                        │
│  │   ╱  ╲    ╱  ╲    ╱╲                │
│  │  ╱    ╲  ╱    ╲  ╱  ╲               │
│  │ ╱      ╲╱      ╲╱    ╲──────        │
│  │╱                                     │
│  └──────────────────────────────── ▶    │
│                                         │
│  Traditional: ████████████████████ $$$  │
│  Serverless:  ██  ██  ██  ██  █   $    │
└─────────────────────────────────────────┘
```

---

## `Knative` Architecture

```text
┌──────────────────────────────────────────────┐
│                  Knative                      │
│                                              │
│  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Knative Serving │  │ Knative Eventing │  │
│  │                  │  │                  │  │
│  │  • Request-driven│  │  • Event-driven  │  │
│  │  • Auto-scaling  │  │  • Pub/Sub       │  │
│  │  • Scale to zero │  │  • Sources       │  │
│  │  • Revisions     │  │  • Brokers       │  │
│  │  • Traffic split │  │  • Triggers      │  │
│  └──────────────────┘  └──────────────────┘  │
│                                              │
│  ┌──────────────────────────────────────────┐ │
│  │        Kubernetes Cluster                │ │
│  │  + Networking (Istio/Kourier/Contour)    │ │
│  └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

---

## Installing `Knative`

```bash
# Install Knative Serving CRDs
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.13.0/serving-crds.yaml

# Install Knative Serving core
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.13.0/serving-core.yaml

# Install networking layer (Kourier - lightweight)
kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.13.0/kourier.yaml

# Configure Knative to use Kourier
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'

# Configure DNS (Magic DNS for development)
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.13.0/serving-default-domain.yaml

# Verify
kubectl get pods -n knative-serving
```

---

## `Knative Service` - Basic Example

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: hello
  namespace: default
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/min-scale: "0"
        autoscaling.knative.dev/max-scale: "10"
    spec:
      containers:
      - image: gcr.io/knative-samples/helloworld-go
        ports:
        - containerPort: 8080
        env:
        - name: TARGET
          value: "Advanced Kubernetes"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
```

```bash
kubectl apply -f hello-service.yaml
```

---

## `Knative` Concepts

```text
┌──────── Knative Service ────────────────────┐
│                                             │
│  ┌─── Configuration ────────────────────┐   │
│  │                                      │   │
│  │  ┌── Revision 1 ──┐  ┌── Rev 2 ──┐  │   │
│  │  │ image: v1      │  │ image: v2  │  │   │
│  │  │ env: ...       │  │ env: ...   │  │   │
│  │  └────────────────┘  └────────────┘  │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌─── Route ────────────────────────────┐   │
│  │  Traffic:                            │   │
│  │    90% → Revision 1                  │   │
│  │    10% → Revision 2                  │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

- **Configuration**: Desired state of the workload
- **Revision**: Immutable snapshot (like a git commit)
- **Route**: Maps traffic to revisions

---

## Scale to Zero

```text
Request arrives
      │
      ▼
┌──────────────┐
│  Activator   │  (Knative component, always running)
│  buffers     │
│  request     │
└──────┬───────┘
       │
       ▼
  Pod exists?
  ├─ YES → Forward request
  └─ NO  → Create pod
           Wait for ready
           Forward buffered request

No requests for scale-to-zero-grace-period (default: 30s)
  → Scale to 0 pods
  → No compute costs!
```

---

## Autoscaling Configuration

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: api
spec:
  template:
    metadata:
      annotations:
        # Knative Pod Autoscaler (KPA)
        autoscaling.knative.dev/class: kpa.autoscaling.knative.dev
        autoscaling.knative.dev/metric: concurrency
        autoscaling.knative.dev/target: "100"

        # Scale boundaries
        autoscaling.knative.dev/min-scale: "0"
        autoscaling.knative.dev/max-scale: "50"

        # Scale to zero timing
        autoscaling.knative.dev/scale-to-zero-pod-retention-period: "1m"

        # Initial scale on creation
        autoscaling.knative.dev/initial-scale: "3"

        # Scale down delay
        autoscaling.knative.dev/scale-down-delay: "15s"
    spec:
      containerConcurrency: 0
      containers:
      - image: myapi:v1
```

---

## Autoscaling Metrics

| Metric | Description | Default Target |
|--------|-------------|----------------|
| `concurrency` | Requests in flight per pod | 100 |
| `rps` | Requests per second per pod | 200 |

```yaml
# Scale based on RPS
annotations:
  autoscaling.knative.dev/metric: rps
  autoscaling.knative.dev/target: "200"
```

```yaml
# Use HPA instead of KPA (no scale-to-zero)
annotations:
  autoscaling.knative.dev/class: hpa.autoscaling.knative.dev
  autoscaling.knative.dev/metric: cpu
  autoscaling.knative.dev/target: "70"
```

---

## Traffic Splitting Between Revisions

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: api
spec:
  template:
    metadata:
      name: api-v2
    spec:
      containers:
      - image: myapi:v2
  traffic:
  - revisionName: api-v1
    percent: 80
    tag: stable
  - revisionName: api-v2
    percent: 20
    tag: canary
  - latestRevision: true
    percent: 0
    tag: latest
```

Each tag gets its own URL:
- `https://stable-api.default.example.com`
- `https://canary-api.default.example.com`
- `https://latest-api.default.example.com`

---

## `Knative` CLI (`kn`)

```bash
# Create a service
kn service create hello \
  --image gcr.io/knative-samples/helloworld-go \
  --env TARGET="World"

# Update (creates new revision)
kn service update hello \
  --env TARGET="Kubernetes" \
  --traffic @latest=10 \
  --traffic hello-v1=90

# List services
kn service list

# List revisions
kn revision list

# Describe service
kn service describe hello

# Delete service
kn service delete hello

# Get route info
kn route list
```

---

## `Knative Eventing` - Event Sources

```yaml
apiVersion: sources.knative.dev/v1
kind: ApiServerSource
metadata:
  name: pod-events
spec:
  serviceAccountName: events-sa
  mode: Resource
  resources:
  - apiVersion: v1
    kind: Pod
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-processor
---
apiVersion: sources.knative.dev/v1beta1
kind: KafkaSource
metadata:
  name: kafka-orders
spec:
  bootstrapServers:
  - kafka:9092
  topics:
  - orders
  consumerGroup: knative-group
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: order-processor
```

---

## `Knative Eventing` - Broker and Trigger

```yaml
apiVersion: eventing.knative.dev/v1
kind: Broker
metadata:
  name: default
  namespace: production
---
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: order-created
spec:
  broker: default
  filter:
    attributes:
      type: com.example.order.created
      source: /api/orders
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: order-fulfillment
---
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: order-notification
spec:
  broker: default
  filter:
    attributes:
      type: com.example.order.created
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: notification-sender
```

---

## Event-Driven Architecture

```text
┌──────────┐    ┌────────────────────────────────────┐
│ API      │───▶│           Broker                   │
│ Gateway  │    │  (receives CloudEvents)            │
└──────────┘    └─────┬──────────┬──────────┬────────┘
                      │          │          │
              ┌───────▼───┐ ┌───▼────┐ ┌───▼────────┐
              │ Trigger:  │ │Trigger:│ │ Trigger:   │
              │ order.*   │ │payment.│ │ *.created  │
              └─────┬─────┘ └───┬────┘ └─────┬──────┘
                    │           │             │
              ┌─────▼─────┐ ┌──▼─────┐ ┌─────▼──────┐
              │ Order     │ │Payment │ │ Analytics  │
              │ Service   │ │Service │ │ Service    │
              │ (scale 0) │ │(scale 0│ │ (scale 0)  │
              └───────────┘ └────────┘ └────────────┘
```

All services scale to zero when no events are flowing.

---

## Sending `CloudEvents`

```go
package main

import (
    "context"
    "log"

    cloudevents "github.com/cloudevents/sdk-go/v2"
)

type OrderCreated struct {
    OrderID   string  `json:"orderId"`
    Customer  string  `json:"customer"`
    Total     float64 `json:"total"`
}

func main() {
    c, err := cloudevents.NewClientHTTP()
    if err != nil {
        log.Fatal(err)
    }

    event := cloudevents.NewEvent()
    event.SetSource("/api/orders")
    event.SetType("com.example.order.created")
    event.SetData(cloudevents.ApplicationJSON,
        OrderCreated{
            OrderID:  "ORD-12345",
            Customer: "Alice",
            Total:    99.99,
        })

    ctx := cloudevents.ContextWithTarget(context.Background(),
        "http://broker-ingress.knative-eventing/production/default")

    if result := c.Send(ctx, event); !cloudevents.IsACK(result) {
        log.Fatalf("failed to send: %v", result)
    }
}
```

---

## Receiving `CloudEvents`

```go
package main

import (
    "context"
    "fmt"
    "log"

    cloudevents "github.com/cloudevents/sdk-go/v2"
)

type OrderCreated struct {
    OrderID  string  `json:"orderId"`
    Customer string  `json:"customer"`
    Total    float64 `json:"total"`
}

func handleEvent(ctx context.Context,
    event cloudevents.Event) error {

    var order OrderCreated
    if err := event.DataAs(&order); err != nil {
        return err
    }

    fmt.Printf("Processing order %s for %s ($%.2f)\n",
        order.OrderID, order.Customer, order.Total)

    // Process the order...
    return nil
}

func main() {
    c, err := cloudevents.NewClientHTTP()
    if err != nil {
        log.Fatal(err)
    }
    log.Fatal(c.StartReceiver(context.Background(),
        handleEvent))
}
```

---

## `Knative` Serving with Private Networking

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: internal-api
  labels:
    networking.knative.dev/visibility: cluster-local
spec:
  template:
    spec:
      containers:
      - image: myapi:v1
        ports:
        - containerPort: 8080
```

```bash
# Only accessible within the cluster:
# http://internal-api.default.svc.cluster.local
```

---

## Custom Domain Mapping

```yaml
apiVersion: serving.knative.dev/v1beta1
kind: DomainMapping
metadata:
  name: api.mycompany.com
spec:
  ref:
    name: api
    kind: Service
    apiVersion: serving.knative.dev/v1
---
# Configure TLS
apiVersion: serving.knative.dev/v1beta1
kind: DomainMapping
metadata:
  name: api.mycompany.com
  annotations:
    networking.knative.dev/certificate-class: cert-manager.io
spec:
  ref:
    name: api
    kind: Service
    apiVersion: serving.knative.dev/v1
```

---

## `Knative` vs Other Serverless

| Feature | `Knative` | AWS Lambda | `OpenFaaS` |
|---------|---------|------------|----------|
| Platform | `Kubernetes` | AWS | `Kubernetes` |
| Scale to zero | Yes | Yes | Yes |
| Container support | Any | Custom runtime | Any |
| Vendor lock-in | No | Yes | No |
| Event sources | CloudEvents | AWS events | Various |
| Cold start | Depends | ~100ms-1s | Depends |
| Max duration | Unlimited | 15 min | Configurable |

---

## Performance: Cold Start Mitigation

```yaml
spec:
  template:
    metadata:
      annotations:
        # Keep minimum 1 pod always warm
        autoscaling.knative.dev/min-scale: "1"

        # Pre-warm: Initial scale for new revisions
        autoscaling.knative.dev/initial-scale: "3"

        # Use faster networking
        autoscaling.knative.dev/activation-scale: "2"
    spec:
      containers:
      - image: myapi:v1
        # Fast startup
        startupProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 1
          periodSeconds: 1
          failureThreshold: 10
```

---

## `Knative` Monitoring

```bash
# Check service status
kn service list
NAME    URL                                    LATEST    READY
hello   http://hello.default.example.com       hello-2   True

# View revisions and traffic split
kn revision list
NAME      SERVICE   TRAFFIC   TAGS     GENERATION   AGE
hello-2   hello     80%       current  2            1h
hello-1   hello     20%       prev     1            2h

# Check autoscaler metrics
kubectl get pods -l serving.knative.dev/service=hello -w

# View autoscaler logs
kubectl logs -n knative-serving \
  -l app=autoscaler -c autoscaler
```

---

## Lab: Serverless Application

```bash
# 1. Install Knative
kubectl apply -f knative-serving.yaml
kubectl apply -f knative-eventing.yaml

# 2. Deploy a Knative service
kn service create hello \
  --image gcr.io/knative-samples/helloworld-go \
  --env TARGET="World"

# 3. Test scale-to-zero
curl http://hello.default.example.com
# Wait 30 seconds, observe pod count
kubectl get pods -w

# 4. Load test and observe autoscaling
hey -z 60s -q 100 http://hello.default.example.com

# 5. Traffic splitting
kn service update hello --env TARGET="v2"
kn service update hello --traffic hello-v1=50 --traffic @latest=50

# 6. Set up event-driven architecture
kubectl apply -f broker.yaml
kubectl apply -f triggers.yaml
kubectl apply -f event-source.yaml
```

---

## Course Summary - Day 3

Key takeaways:

1. **Declarative config** with `Kustomize`, `Helm`, and GitOps
1. **Production patterns**: checklists, security, cost optimization
1. **Deployment strategies**: rolling, blue-green, canary with `Argo Rollouts`
1. **`RBAC`**: Least privilege, `ServiceAccounts`, audit logging
1. **Serverless**: `Knative` for scale-to-zero and event-driven workloads

---

## Course Wrap-Up

```text
Day 1: Deploying Resilient Apps & Extending Kubernetes
  ✓ ReplicaSets, StatefulSets, Resources, Probes
  ✓ HPA, Cluster Autoscaler, KEDA
  ✓ Schedulers, Controllers, Operators
  ✓ Init Containers, CRDs

Day 2: Cluster Provisioning, Observability & Service Mesh
  ✓ kubeadm, Cluster API
  ✓ Prometheus, OpenTelemetry
  ✓ Istio, NetworkPolicies
  ✓ DaemonSets, Jobs, CronJobs
  ✓ Volumes, ConfigMaps, Secrets

Day 3: Advanced Admin, RBAC & Serverless
  ✓ Declarative config, Kustomize, Helm
  ✓ Best practices, deployment patterns
  ✓ RBAC deep dive
  ✓ Knative Serving & Eventing
```

> Thank you!
