---
marp: true
theme: default
paginate: true
---

# Deploying Resilient Applications in `Kubernetes`

Advanced Kubernetes Course - Day 1, Module 1

---

## Module Overview

- Understanding `ReplicaSets` in depth
- `StatefulSets` for stateful workloads
- Resource requests and limits
- Liveness, readiness, and startup probes
- Designing for failure

---

## What Makes an App Resilient?

- **Self-healing**: Automatically recovers from failures
- **Scalable**: Handles varying load gracefully
- **Observable**: Exposes health and metrics
- **Redundant**: No single point of failure

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Pod A-1   │    │   Pod A-2   │    │   Pod A-3   │
│  (healthy)  │    │  (healthy)  │    │  (healthy)  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                    ┌─────┴─────┐
                    │  Service  │
                    └───────────┘
```

---

## `ReplicaSets` Deep Dive

A `ReplicaSet` ensures a specified number of pod replicas are running at any given time.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: web-frontend
  labels:
    app: web
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      tier: frontend
  template:
    metadata:
      labels:
        app: web
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
```

---

## `ReplicaSet` Label Selectors

Two types of selectors:

**Equality-based:**
```yaml
selector:
  matchLabels:
    app: web
    environment: production
```

**Set-based:**
```yaml
selector:
  matchExpressions:
  - key: app
    operator: In
    values: [web, api]
  - key: environment
    operator: NotIn
    values: [dev]
```

---

## `ReplicaSet` vs `Deployment`

| Feature | `ReplicaSet` | `Deployment` |
|---------|-------------|-------------|
| Pod management | Yes | Yes (via `ReplicaSet`) |
| Rolling updates | No | Yes |
| Rollback | No | Yes |
| Revision history | No | Yes |
| Declarative updates | No | Yes |

> **Best Practice**: Always use `Deployments` instead of bare `ReplicaSets`

---

## How `ReplicaSets` Handle Failures

```
Time T0: 3 replicas running
┌────┐  ┌────┐  ┌────┐
│Pod1│  │Pod2│  │Pod3│
└────┘  └────┘  └────┘

Time T1: Pod2 crashes
┌────┐  ┌────┐  ┌────┐
│Pod1│  │ XX │  │Pod3│
└────┘  └────┘  └────┘

Time T2: ReplicaSet controller creates Pod4
┌────┐  ┌────┐  ┌────┐
│Pod1│  │Pod4│  │Pod3│
└────┘  └────┘  └────┘
```

The reconciliation loop runs continuously.

---

## Scaling `ReplicaSets`

**Imperative:**
```bash
kubectl scale replicaset web-frontend --replicas=5
```

**Declarative:**
```bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: web-frontend
spec:
  replicas: 5
EOF
```

**Verify:**
```bash
kubectl get rs web-frontend
kubectl describe rs web-frontend
```

---

## `ReplicaSet` Owner References

When a `ReplicaSet` creates a pod, it sets an owner reference:

```bash
kubectl get pod web-frontend-abc12 -o yaml
```

```yaml
metadata:
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: web-frontend
    uid: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

Orphan pods (no owner) can be adopted by a matching `ReplicaSet`.

---

## `StatefulSets` - Why They Exist

Stateless apps are easy. But what about:

- **Databases** (`PostgreSQL`, `MySQL`, `MongoDB`)
- **Message queues** (`Kafka`, `RabbitMQ`)
- **Distributed caches** (`Redis` cluster, `Memcached`)
- **Search engines** (`Elasticsearch`)

These need:
- Stable network identity
- Stable persistent storage
- Ordered deployment and scaling

---

## `StatefulSet` Specification

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-headless
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 10Gi
```

---

## `StatefulSet` Naming and Identity

Pods get predictable names:

```
postgres-0    (first, leader)
postgres-1    (second, replica)
postgres-2    (third, replica)
```

Each pod gets a stable DNS name:

```
postgres-0.postgres-headless.default.svc.cluster.local
postgres-1.postgres-headless.default.svc.cluster.local
postgres-2.postgres-headless.default.svc.cluster.local
```

---

## Headless Service for `StatefulSets`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

Setting `clusterIP: None` makes it headless - DNS returns individual pod IPs instead of a virtual IP.

---

## `StatefulSet` Ordering Guarantees

**OrderedReady** (default):
```
Deploy:  postgres-0 → postgres-1 → postgres-2
Scale down: postgres-2 → postgres-1 → postgres-0
```

**Parallel** (for apps that don't need ordering):
```yaml
spec:
  podManagementPolicy: Parallel
```

```
Deploy:  postgres-0, postgres-1, postgres-2 (simultaneously)
```

---

## `StatefulSet` Update Strategies

**RollingUpdate** (default):
```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 1
```

With `partition: 1`, only pods with ordinal >= 1 are updated. Great for **canary testing**.

**OnDelete:**
```yaml
spec:
  updateStrategy:
    type: OnDelete
```

Pods only update when manually deleted.

---

## Resource Requests and Limits

```yaml
spec:
  containers:
  - name: app
    image: myapp:v2
    resources:
      requests:
        cpu: "250m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
```

| | Requests | Limits |
|---|----------|--------|
| Purpose | Scheduling guarantee | Maximum allowed |
| CPU exceeded | N/A | Throttled |
| Memory exceeded | N/A | OOMKilled |

---

## Understanding CPU Units

```
1 CPU = 1000m (millicores)

"100m"  = 0.1 CPU  (10% of one core)
"250m"  = 0.25 CPU (25% of one core)
"1"     = 1 CPU    (one full core)
"1500m" = 1.5 CPU  (one and a half cores)
```

```
┌─────────────────────────────────┐
│          Node (4 CPU)           │
│                                 │
│  ┌──────┐ ┌──────┐ ┌────────┐  │
│  │250m  │ │500m  │ │1000m   │  │
│  │Pod A │ │Pod B │ │Pod C   │  │
│  └──────┘ └──────┘ └────────┘  │
│                                 │
│  Remaining: 2250m allocatable   │
└─────────────────────────────────┘
```

---

## Understanding Memory Units

```
"128Mi" = 128 Mebibytes = 134,217,728 bytes
"256Mi" = 256 Mebibytes
"1Gi"   = 1 Gibibyte = 1,073,741,824 bytes
"2Gi"   = 2 Gibibytes

Note: Mi (Mebibyte) ≠ M (Megabyte)
      Gi (Gibibyte) ≠ G (Gigabyte)
```

> **Best Practice**: Always set memory limits. Without them, a memory leak can take down the entire node.

---

## `QoS` Classes

`Kubernetes` assigns Quality of Service classes automatically:

| `QoS` Class | Condition | Eviction Priority |
|-----------|-----------|-------------------|
| **Guaranteed** | requests == limits for all containers | Last (lowest) |
| **Burstable** | requests < limits for at least one | Middle |
| **BestEffort** | No requests or limits set | First (highest) |

```bash
kubectl get pod myapp -o jsonpath='{.status.qosClass}'
```

---

## `LimitRange` - Namespace Defaults

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "256Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "2Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
    type: Container
```

---

## `ResourceQuota` - Namespace Totals

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "50"
    persistentvolumeclaims: "10"
    services.loadbalancers: "2"
```

```bash
kubectl describe quota production-quota -n production
```

---

## Liveness Probes

Determines if a container is **running**. If it fails, `kubelet` kills the container.

```yaml
spec:
  containers:
  - name: app
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 15
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 3
      successThreshold: 1
```

---

## Readiness Probes

Determines if a container is **ready to receive traffic**. If it fails, the pod is removed from `Service` endpoints.

```yaml
spec:
  containers:
  - name: app
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
      timeoutSeconds: 2
      failureThreshold: 3
```

```
Pod with failing readiness probe:
Service ──X──> Pod (removed from endpoints)
```

---

## Startup Probes

For slow-starting containers. Disables liveness and readiness probes until it succeeds.

```yaml
spec:
  containers:
  - name: legacy-app
    startupProbe:
      httpGet:
        path: /healthz
        port: 8080
      failureThreshold: 30
      periodSeconds: 10
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      periodSeconds: 10
```

Maximum startup time: `failureThreshold * periodSeconds` = 300 seconds

---

## Probe Types Compared

**HTTP GET:**
```yaml
httpGet:
  path: /healthz
  port: 8080
  httpHeaders:
  - name: X-Custom-Header
    value: Awesome
```

**TCP Socket:**
```yaml
tcpSocket:
  port: 3306
```

**Exec Command:**
```yaml
exec:
  command:
  - /bin/sh
  - -c
  - pg_isready -U postgres
```

**gRPC:**
```yaml
grpc:
  port: 50051
  service: my.health.v1.Health
```

---

## Probe Decision Tree

```
Is the container running?
│
├─ YES → Liveness Probe passes
│        │
│        ├─ Is it ready for traffic?
│        │  │
│        │  ├─ YES → Readiness Probe passes
│        │  │        Pod receives traffic ✓
│        │  │
│        │  └─ NO → Readiness Probe fails
│        │          Pod removed from Service endpoints
│        │
│        └─ Liveness Probe fails →
│           Container is killed and restarted
│
└─ NO → Container is starting
        │
        ├─ Startup Probe passes → Enable liveness/readiness
        └─ Startup Probe fails  → Container is killed
```

---

## `PodDisruptionBudget`

Protect availability during voluntary disruptions (node drain, cluster upgrade):

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web
```

Or use `maxUnavailable`:
```yaml
spec:
  maxUnavailable: 1
```

Or percentage:
```yaml
spec:
  minAvailable: "75%"
```

---

## Resilience Patterns Summary

```
┌──────────────────────────────────────────────┐
│            Resilient Application              │
│                                              │
│  ┌────────────┐  ┌────────────────────────┐  │
│  │ ReplicaSet │  │ Resource Management    │  │
│  │ (3+ pods)  │  │ requests + limits      │  │
│  └────────────┘  └────────────────────────┘  │
│                                              │
│  ┌────────────┐  ┌────────────────────────┐  │
│  │ Probes     │  │ PodDisruptionBudget    │  │
│  │ L + R + S  │  │ minAvailable: 2        │  │
│  └────────────┘  └────────────────────────┘  │
│                                              │
│  ┌────────────┐  ┌────────────────────────┐  │
│  │ Anti-      │  │ Topology Spread        │  │
│  │ Affinity   │  │ Constraints            │  │
│  └────────────┘  └────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## Lab Exercise: Build a Resilient App

1. Create a `Deployment` with 3 replicas
2. Add resource requests and limits
3. Configure liveness and readiness probes
4. Create a `PodDisruptionBudget`
5. Simulate a node failure and observe recovery

```bash
# Deploy the application
kubectl apply -f resilient-app.yaml

# Watch pod status
kubectl get pods -w

# Simulate failure
kubectl delete pod <pod-name>

# Verify PDB
kubectl get pdb
```
