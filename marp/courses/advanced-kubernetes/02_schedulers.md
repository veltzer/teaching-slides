---
marp: true
theme: default
paginate: true
---

# `Kubernetes` Schedulers

Advanced Kubernetes Course - Day 1, Module 3

---

## Module Overview

- How the default scheduler works
- Node affinity and anti-affinity
- Pod affinity and anti-affinity
- Taints and tolerations
- Topology spread constraints
- Custom schedulers

---

## The Scheduling Pipeline

```text
New Pod Created (spec.nodeName is empty)
         │
         ▼
┌─────────────────┐
│   Scheduling    │
│     Queue       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  Filter Phase   │────▶│  Feasible Nodes  │
│  (Predicates)   │     │  (candidates)    │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Score Phase     │
                        │  (Priorities)    │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Bind Phase      │
                        │  (Assign Node)   │
                        └──────────────────┘
```

---

## Filter Plugins (Predicates)

| Plugin | Purpose |
|--------|---------|
| `NodeResourcesFit` | Node has enough CPU/memory |
| `NodePorts` | Requested ports are available |
| `NodeAffinity` | Node matches affinity rules |
| `TaintToleration` | Pod tolerates node taints |
| `PodTopologySpread` | Topology constraints met |
| `VolumeBinding` | Volume requirements satisfied |
| `InterPodAffinity` | Pod affinity rules met |

---

## Score Plugins (Priorities)

| Plugin | Purpose |
|--------|---------|
| `NodeResourcesBalancedAllocation` | Balance CPU/memory usage |
| `ImageLocality` | Prefer nodes with container images |
| `InterPodAffinity` | Score based on pod affinity |
| `TaintToleration` | Prefer nodes with fewer taints |
| `NodeAffinity` | Score based on node affinity |

Each plugin returns a score 0-100. Final score is weighted sum.

---

## `nodeSelector` - Simple Placement

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  nodeSelector:
    gpu-type: nvidia-a100
    disk-type: ssd
  containers:
  - name: ml-training
    image: pytorch:latest
    resources:
      limits:
        nvidia.com/gpu: 2
```

```bash
# Label a node
kubectl label node worker-3 gpu-type=nvidia-a100
kubectl label node worker-3 disk-type=ssd

# View node labels
kubectl get nodes --show-labels
```

---

## Node Affinity - Advanced Placement

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-east-1a
            - us-east-1b
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 80
        preference:
          matchExpressions:
          - key: node-type
            operator: In
            values:
            - high-memory
      - weight: 20
        preference:
          matchExpressions:
          - key: cost
            operator: In
            values:
            - spot
```

---

## Node Affinity Operators

| Operator | Meaning |
|----------|---------|
| `In` | Label value is in the set |
| `NotIn` | Label value is not in the set |
| `Exists` | Label key exists (any value) |
| `DoesNotExist` | Label key does not exist |
| `Gt` | Label value is greater than |
| `Lt` | Label value is less than |

```yaml
matchExpressions:
- key: gpu-count
  operator: Gt
  values: ["3"]
```

---

## Pod Affinity - Co-locate Pods

Place pods near related pods:

```yaml
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - redis-cache
        topologyKey: kubernetes.io/hostname
```

```text
┌────── Node 1 ──────┐    ┌────── Node 2 ──────┐
│ ┌─────┐  ┌───────┐ │    │                     │
│ │Redis│  │Web App│ │    │     (empty)         │
│ └─────┘  └───────┘ │    │                     │
└─────────────────────┘    └─────────────────────┘

Web App has podAffinity to Redis → same node
```

---

## Pod Anti-Affinity - Spread Pods

Keep pods away from each other:

```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - web
        topologyKey: kubernetes.io/hostname
```

```text
┌── Node 1 ──┐  ┌── Node 2 ──┐  ┌── Node 3 ──┐
│  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │
│  │Web-1  │  │  │  │Web-2  │  │  │  │Web-3  │  │
│  └───────┘  │  │  └───────┘  │  │  └───────┘  │
└─────────────┘  └─────────────┘  └─────────────┘
One web pod per node (anti-affinity on hostname)
```

---

## Taints and Tolerations

**Taint a node** (repel pods):
```bash
kubectl taint nodes gpu-node-1 gpu=nvidia:NoSchedule
kubectl taint nodes maintenance-node key=value:NoExecute
```

**Tolerate the taint** (pod-level):
```yaml
spec:
  tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "nvidia"
    effect: "NoSchedule"
  - key: "maintenance"
    operator: "Exists"
    effect: "NoExecute"
    tolerationSeconds: 3600
```

---

## Taint Effects

| Effect | Behavior |
|--------|----------|
| `NoSchedule` | New pods without toleration won't be scheduled |
| `PreferNoSchedule` | Scheduler tries to avoid, but not guaranteed |
| `NoExecute` | Evicts existing pods without toleration |

```bash
# View node taints
kubectl describe node worker-1 | grep -A5 Taints

# Remove a taint (note the trailing dash)
kubectl taint nodes gpu-node-1 gpu=nvidia:NoSchedule-
```

---

## Built-in Taints

`Kubernetes` automatically adds these taints:

| Taint | Condition |
|-------|-----------|
| `node.kubernetes.io/not-ready` | Node is not ready |
| `node.kubernetes.io/unreachable` | Node is unreachable |
| `node.kubernetes.io/memory-pressure` | Node has memory pressure |
| `node.kubernetes.io/disk-pressure` | Node has disk pressure |
| `node.kubernetes.io/pid-pressure` | Too many processes |
| `node.kubernetes.io/unschedulable` | Node is cordoned |

---

## Topology Spread Constraints

Distribute pods evenly across zones/nodes:

```yaml
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: web
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: web
```

---

## Topology Spread Visualization

```text
maxSkew: 1, topologyKey: zone

Zone A          Zone B          Zone C
┌─────────┐    ┌─────────┐    ┌─────────┐
│ web-1   │    │ web-2   │    │ web-3   │
│ web-4   │    │ web-5   │    │ web-6   │
└─────────┘    └─────────┘    └─────────┘
  2 pods         2 pods         2 pods

Balanced! maxSkew=1 means difference between
any two zones is at most 1.

If Zone C had 0 pods and A had 2:
  skew = 2 - 0 = 2 > maxSkew(1) → VIOLATION
```

---

## Custom Scheduler

Create a scheduler profile in `KubeSchedulerConfiguration`:

```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: gpu-scheduler
  plugins:
    filter:
      enabled:
      - name: NodeResourcesFit
      - name: TaintToleration
      disabled:
      - name: "*"
    score:
      enabled:
      - name: NodeResourcesBalancedAllocation
        weight: 1
      disabled:
      - name: "*"
```

---

## Using a Custom Scheduler

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ml-workload
spec:
  schedulerName: gpu-scheduler
  containers:
  - name: training
    image: tensorflow:latest
```

```bash
# Check which scheduler handled the pod
kubectl get events --field-selector \
  involvedObject.name=ml-workload | grep Scheduled
```

---

## Priority and Preemption

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical-production
value: 1000000
globalDefault: false
preemptionPolicy: PreemptLowerPriority
description: "For critical production workloads"
---
apiVersion: v1
kind: Pod
metadata:
  name: critical-app
spec:
  priorityClassName: critical-production
  containers:
  - name: app
    image: critical-app:v1
```

Higher priority pods can **preempt** (evict) lower priority pods.

---

## Scheduling Best Practices

1. **Use topology spread** for high availability across zones
2. **Use pod anti-affinity** to spread replicas across nodes
3. **Use taints** to dedicate nodes for specific workloads
4. **Set priorities** for critical workloads
5. **Avoid over-constraining** - leave room for the scheduler

```yaml
# Good: Spread across zones, prefer specific nodes
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 50
        preference:
          matchExpressions:
          - key: node-type
            operator: In
            values: [compute-optimized]
```

---

## Lab: Advanced Scheduling

```bash
# 1. Label nodes by zone
kubectl label node worker-1 zone=a
kubectl label node worker-2 zone=b
kubectl label node worker-3 zone=c

# 2. Deploy with topology spread
kubectl apply -f topology-spread-deploy.yaml

# 3. Verify distribution
kubectl get pods -o wide

# 4. Taint a node and observe eviction
kubectl taint nodes worker-1 maintenance=true:NoExecute

# 5. Check pod redistribution
kubectl get pods -o wide -w
```
