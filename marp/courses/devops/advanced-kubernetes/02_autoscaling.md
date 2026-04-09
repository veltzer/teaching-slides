# Autoscaling in `Kubernetes`

Advanced Kubernetes Course - Day 1, Module 2

---

## Module Overview

- `HorizontalPodAutoscaler` (`HPA`)
- `VerticalPodAutoscaler` (`VPA`)
- `Cluster Autoscaler`
- `KEDA` - Event-driven autoscaling
- Scaling strategies and best practices

---

## Autoscaling Dimensions

![autoscaling_dimensions](svg/courses/devops/advanced-kubernetes/02_autoscaling/autoscaling_dimensions.svg)

---

## `HorizontalPodAutoscaler` v2

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## `HPA` Scaling Algorithm

The desired replica count is calculated as:

```misc
desiredReplicas = ceil[currentReplicas * (currentMetric / desiredMetric)]
```

**Example:**
- Current replicas: 3
- Current CPU utilization: 90%
- Target CPU utilization: 70%

```misc
desiredReplicas = ceil[3 * (90 / 70)]
                = ceil[3 * 1.286]
                = ceil[3.857]
                = 4
```

---

## `HPA` with Custom Metrics

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  - type: Object
    object:
      describedObject:
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        name: api-ingress
      metric:
        name: requests_per_second
      target:
        type: Value
        value: "5000"
```

---

## `HPA` Scaling Behavior

Control the speed of scaling up and down:

```yaml
spec:
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      selectPolicy: Min
```

> Scale up aggressively, scale down conservatively.

---

## `HPA` Monitoring Commands

```bash
# View HPA status
kubectl get hpa web-hpa

# Detailed view with events
kubectl describe hpa web-hpa

# Watch scaling in real time
kubectl get hpa -w

# Check metrics availability
kubectl top pods
kubectl top nodes
```

Example output:
```misc
NAME      REFERENCE        TARGETS         MINPODS   MAXPODS   REPLICAS
web-hpa   Deployment/web   65%/70%, 45%/80%   2        20        4
```

---

## `Metrics Server` - Prerequisite for `HPA`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-server
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: metrics-server
  template:
    spec:
      containers:
      - name: metrics-server
        image: registry.k8s.io/metrics-server/metrics-server:v0.7.0
        args:
        - --cert-dir=/tmp
        - --secure-port=10250
        - --kubelet-preferred-address-types=InternalIP
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
```

```bash
# Install via Helm
helm install metrics-server metrics-server/metrics-server \
  -n kube-system
```

---

## `VerticalPodAutoscaler`

Automatically adjusts CPU and memory requests:

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: web
      minAllowed:
        cpu: "100m"
        memory: "128Mi"
      maxAllowed:
        cpu: "2"
        memory: "4Gi"
      controlledResources: ["cpu", "memory"]
```

---

## `VPA` Modes

| Mode | Description |
|------|-------------|
| `Off` | Only provides recommendations, no changes |
| `Initial` | Sets resources only at pod creation |
| `Auto` | Updates running pods (may restart them) |
| `Recreate` | Same as Auto in current implementation |

```bash
# View recommendations
kubectl describe vpa web-vpa
```

```misc
Recommendation:
  Container Recommendations:
    Container Name: web
    Lower Bound:    Cpu: 100m, Memory: 128Mi
    Target:         Cpu: 250m, Memory: 256Mi
    Upper Bound:    Cpu: 500m, Memory: 512Mi
```

---

## `HPA` vs `VPA` - When to Use

| Scenario | Use |
|----------|-----|
| Stateless web apps | `HPA` |
| Batch processing | `HPA` |
| Database pods | `VPA` |
| Unknown resource needs | `VPA` (Off mode first) |
| High traffic variance | `HPA` + `VPA` (careful!) |

> **Warning**: Do not use `HPA` and `VPA` on the same metric (e.g., both on CPU). They will fight each other.

---

## `Cluster Autoscaler`

Automatically adjusts the number of nodes in a cluster:

---

## `Cluster Autoscaler`

![cluster_autoscaler](svg/courses/devops/advanced-kubernetes/02_autoscaling/cluster_autoscaler.svg)

---

## `Cluster Autoscaler` Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - name: cluster-autoscaler
        image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.29.0
        command:
        - ./cluster-autoscaler
        - --v=4
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
        - --scale-down-delay-after-add=10m
        - --scale-down-unneeded-time=10m
        - --scale-down-utilization-threshold=0.5
```

---

## `Cluster Autoscaler` Expander Strategies

| Strategy | Description |
|----------|-------------|
| `random` | Picks a random node group |
| `most-pods` | Schedules the most pending pods |
| `least-waste` | Minimizes idle resources after scaling |
| `price` | Selects cheapest option (cloud-specific) |
| `priority` | Uses user-defined priorities |

```yaml
# Priority expander config
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-priority-expander
  namespace: kube-system
data:
  priorities: |-
    10:
      - .*spot.*
    50:
      - .*on-demand.*
```

---

## Scale-Down Behavior

The `Cluster Autoscaler` removes nodes when:

1. All pods can be moved to other nodes
1. Node utilization is below threshold (default 50%)
1. No pods with `PodDisruptionBudget` violations
1. No pods with local storage (unless configured)
1. No system pods without controller

```bash
# Prevent a node from being scaled down
kubectl annotate node node-1 \
  cluster-autoscaler.kubernetes.io/scale-down-disabled=true
```

---

## `KEDA` - Event-Driven Autoscaling

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: rabbitmq-consumer
spec:
  scaleTargetRef:
    name: consumer-deployment
  minReplicaCount: 0
  maxReplicaCount: 30
  pollingInterval: 15
  cooldownPeriod: 300
  triggers:
  - type: rabbitmq
    metadata:
      queueName: orders
      host: amqp://rabbitmq.default.svc.cluster.local
      queueLength: "50"
```

`KEDA` can scale to zero - true event-driven scaling.

---

## `KEDA` Scalers

`KEDA` supports 60+ event sources:

| Category | Scalers |
|----------|---------|
| Message Queues | `Kafka`, `RabbitMQ`, `NATS`, `SQS` |
| Databases | `PostgreSQL`, `MySQL`, `MongoDB` |
| Cloud | `AWS CloudWatch`, `Azure Monitor` |
| HTTP | `Prometheus`, `Datadog`, `Graphite` |
| Custom | `External`, `Metrics API`, `Cron` |

```yaml
triggers:
- type: kafka
  metadata:
    bootstrapServers: kafka:9092
    consumerGroup: my-group
    topic: orders
    lagThreshold: "100"
```

---

## Combining Autoscalers

![combining_autoscalers](svg/courses/devops/advanced-kubernetes/02_autoscaling/combining_autoscalers.svg)

---

## Autoscaling Best Practices

1. **Always set resource requests** - `HPA` needs them for CPU-based scaling
1. **Use stabilization windows** - Prevent flapping
1. **Scale down slowly** - Avoid thrashing
1. **Monitor scaling events** - Alert on max replicas reached
1. **Test scaling behavior** - Use load testing tools
1. **Set appropriate min/max** - Safety boundaries

```bash
# Load test with hey
hey -z 5m -q 100 -c 50 http://web-service/api

# Watch scaling
watch kubectl get hpa,pods
```

---

## Lab: Autoscaling Pipeline

```bash
# 1. Deploy an app with HPA
kubectl apply -f app-with-hpa.yaml

# 2. Generate load
kubectl run load-generator --image=busybox --restart=Never \
  -- /bin/sh -c "while true; do wget -q -O- http://web; done"

# 3. Observe HPA scaling
kubectl get hpa -w

# 4. Stop load and observe scale-down
kubectl delete pod load-generator

# 5. Verify cluster autoscaler logs
kubectl logs -n kube-system -l app=cluster-autoscaler
```
