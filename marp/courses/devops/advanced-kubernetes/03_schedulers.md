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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="420" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <text x="330" y="28" text-anchor="middle" font-size="13" fill="#222">New Pod Created (spec.nodeName is empty)</text>
  <line x1="330" y1="33" x2="330" y2="58" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="220" y="58" width="220" height="56" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="81" text-anchor="middle" font-size="14" fill="#222">Scheduling Queue</text>
  <text x="330" y="98" text-anchor="middle" font-size="12" fill="#555"></text>
  <line x1="330" y1="114" x2="330" y2="140" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="120" y="140" width="190" height="56" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="215" y="164" text-anchor="middle" font-size="14" fill="#222">Filter Phase</text>
  <text x="215" y="181" text-anchor="middle" font-size="11" fill="#555">(Predicates)</text>
  <line x1="310" y1="168" x2="355" y2="168" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="355" y="140" width="195" height="56" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="452" y="164" text-anchor="middle" font-size="14" fill="#222">Feasible Nodes</text>
  <text x="452" y="181" text-anchor="middle" font-size="11" fill="#555">(candidates)</text>
  <line x1="452" y1="196" x2="452" y2="222" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="355" y="222" width="195" height="56" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="452" y="246" text-anchor="middle" font-size="14" fill="#222">Score Phase</text>
  <text x="452" y="263" text-anchor="middle" font-size="11" fill="#555">(Priorities)</text>
  <line x1="452" y1="278" x2="452" y2="304" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="355" y="304" width="195" height="56" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="452" y="328" text-anchor="middle" font-size="14" fill="#222">Bind Phase</text>
  <text x="452" y="345" text-anchor="middle" font-size="11" fill="#555">(Assign Node)</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="180" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="20" y="20" width="260" height="110" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="150" y="14" text-anchor="middle" font-size="12" fill="#555">Node 1</text>
  <rect x="40" y="40" width="80" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="80" y="70" text-anchor="middle" font-size="13" fill="#222">Redis</text>
  <rect x="150" y="40" width="100" height="50" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="200" y="70" text-anchor="middle" font-size="13" fill="#222">Web App</text>
  <rect x="360" y="20" width="260" height="110" rx="4" fill="#f5f5f5" stroke="#333" stroke-width="1.5"/>
  <text x="490" y="14" text-anchor="middle" font-size="12" fill="#555">Node 2</text>
  <text x="490" y="80" text-anchor="middle" font-size="13" fill="#aaa">(empty)</text>
  <text x="320" y="158" text-anchor="middle" font-size="12" fill="#444">Web App has podAffinity to Redis → scheduled to same node</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="160" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="20" y="20" width="195" height="95" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="117" y="14" text-anchor="middle" font-size="12" fill="#555">Node 1</text>
  <rect x="50" y="38" width="130" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="115" y="68" text-anchor="middle" font-size="13" fill="#222">Web-1</text>
  <rect x="235" y="20" width="195" height="95" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="332" y="14" text-anchor="middle" font-size="12" fill="#555">Node 2</text>
  <rect x="265" y="38" width="130" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="68" text-anchor="middle" font-size="13" fill="#222">Web-2</text>
  <rect x="450" y="20" width="195" height="95" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="547" y="14" text-anchor="middle" font-size="12" fill="#555">Node 3</text>
  <rect x="480" y="38" width="130" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="545" y="68" text-anchor="middle" font-size="13" fill="#222">Web-3</text>
  <text x="330" y="140" text-anchor="middle" font-size="12" fill="#444">One web pod per node (anti-affinity on hostname)</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="310" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <text x="330" y="22" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">maxSkew: 1, topologyKey: zone</text>
  <rect x="30" y="35" width="175" height="130" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="117" y="28" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">Zone A</text>
  <rect x="50" y="50" width="135" height="40" rx="4" fill="#fff" stroke="#777" stroke-width="1.5"/>
  <text x="117" y="75" text-anchor="middle" font-size="13" fill="#222">web-1</text>
  <rect x="50" y="102" width="135" height="40" rx="4" fill="#fff" stroke="#777" stroke-width="1.5"/>
  <text x="117" y="127" text-anchor="middle" font-size="13" fill="#222">web-4</text>
  <text x="117" y="185" text-anchor="middle" font-size="12" fill="#555">2 pods</text>
  <rect x="235" y="35" width="175" height="130" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="322" y="28" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">Zone B</text>
  <rect x="255" y="50" width="135" height="40" rx="4" fill="#fff" stroke="#777" stroke-width="1.5"/>
  <text x="322" y="75" text-anchor="middle" font-size="13" fill="#222">web-2</text>
  <rect x="255" y="102" width="135" height="40" rx="4" fill="#fff" stroke="#777" stroke-width="1.5"/>
  <text x="322" y="127" text-anchor="middle" font-size="13" fill="#222">web-5</text>
  <text x="322" y="185" text-anchor="middle" font-size="12" fill="#555">2 pods</text>
  <rect x="440" y="35" width="175" height="130" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="527" y="28" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">Zone C</text>
  <rect x="460" y="50" width="135" height="40" rx="4" fill="#fff" stroke="#777" stroke-width="1.5"/>
  <text x="527" y="75" text-anchor="middle" font-size="13" fill="#222">web-3</text>
  <rect x="460" y="102" width="135" height="40" rx="4" fill="#fff" stroke="#777" stroke-width="1.5"/>
  <text x="527" y="127" text-anchor="middle" font-size="13" fill="#222">web-6</text>
  <text x="527" y="185" text-anchor="middle" font-size="12" fill="#555">2 pods</text>
  <text x="330" y="218" text-anchor="middle" font-size="12" fill="#333">Balanced! maxSkew=1 means difference between any two zones ≤ 1.</text>
  <rect x="80" y="232" width="490" height="58" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="1.5"/>
  <text x="325" y="253" text-anchor="middle" font-size="12" fill="#b71c1c">Violation example: Zone A = 2 pods, Zone C = 0 pods</text>
  <text x="325" y="272" text-anchor="middle" font-size="12" fill="#b71c1c">skew = 2 − 0 = 2 > maxSkew(1) → VIOLATION</text>
</svg>

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
1. **Use pod anti-affinity** to spread replicas across nodes
1. **Use taints** to dedicate nodes for specific workloads
1. **Set priorities** for critical workloads
1. **Avoid over-constraining** - leave room for the scheduler

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
