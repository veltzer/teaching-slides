# Kubernetes Resources

---

## Resource Overview

1. **Workload**: Pods, Deployments, Jobs
1. **Service**: Services, Ingress, Endpoints
1. **Config**: ConfigMaps, Secrets
1. **Storage**: Volumes, PersistentVolumes
1. **Cluster**: Nodes, Namespaces, Roles

---

## Kubernetes Architecture Review

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Master and Worker Nodes</text>
  <rect x="100" y="80" width="250" height="120" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-weight="bold">Master Node</text>
  <rect x="110" y="120" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="160" y="140" text-anchor="middle" fill="white" font-size="11">API Server</text>
  <rect x="220" y="120" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="270" y="140" text-anchor="middle" fill="white" font-size="11">Scheduler</text>
  <rect x="110" y="160" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="160" y="180" text-anchor="middle" fill="white" font-size="11">Controller</text>
  <rect x="220" y="160" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="270" y="180" text-anchor="middle" fill="white" font-size="11">etcd</text>
  <rect x="450" y="80" width="250" height="120" fill="#e8f5e9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="575" y="105" text-anchor="middle" font-weight="bold">Worker Node</text>
  <rect x="460" y="120" width="100" height="30" fill="#34a853" rx="3"/>
  <text x="510" y="140" text-anchor="middle" fill="white" font-size="11">Kubelet</text>
  <rect x="570" y="120" width="120" height="30" fill="#34a853" rx="3"/>
  <text x="630" y="140" text-anchor="middle" fill="white" font-size="11">Container Runtime</text>
  <rect x="460" y="160" width="100" height="30" fill="#34a853" rx="3"/>
  <text x="510" y="180" text-anchor="middle" fill="white" font-size="11">Kube-proxy</text>
  <rect x="100" y="230" width="600" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="400" y="255" text-anchor="middle" font-weight="bold">Pods (Application Containers)</text>
  <circle cx="200" cy="280" r="20" fill="#fbbc04"/>
  <circle cx="300" cy="280" r="20" fill="#fbbc04"/>
  <circle cx="400" cy="280" r="20" fill="#fbbc04"/>
  <circle cx="500" cy="280" r="20" fill="#fbbc04"/>
  <circle cx="600" cy="280" r="20" fill="#fbbc04"/>
</svg>

---

## Master Node Components

1. **API Server**: Central management point
1. **Scheduler**: Assigns pods to nodes
1. **Controller Manager**: Runs controllers
1. **etcd**: Distributed key-value store
1. **Cloud Controller**: Cloud-specific control

---

## API Server Details

```yaml
# API Server responsibilities
responsibilities:
  - Authentication and authorization
  - API request validation
  - Update etcd
  - Serve REST operations
  - Watch mechanism for changes
```

---

## etcd Details

1. **Distributed** key-value store
1. **Consistent** and highly available
1. **Stores** all cluster data
1. **Backup** critical for disaster recovery
1. **Access** only via API server

---

## Scheduler Details

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Scheduler Decision Process</text>
  <rect x="50" y="60" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="125" y="95" text-anchor="middle" fill="white">1. Filter Nodes</text>
  <rect x="250" y="60" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="325" y="95" text-anchor="middle" fill="white">2. Score Nodes</text>
  <rect x="450" y="60" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="525" y="95" text-anchor="middle" fill="white">3. Select Best</text>
  <rect x="650" y="60" width="120" height="60" fill="#34a853" rx="5"/>
  <text x="710" y="95" text-anchor="middle" fill="white">4. Bind Pod</text>
  <rect x="100" y="160" width="600" height="180" fill="#f0f0f0" rx="5"/>
  <text x="400" y="185" text-anchor="middle" font-weight="bold">Scheduling Factors</text>
  <text x="200" y="210" text-anchor="start" font-size="12">• Resource requirements</text>
  <text x="200" y="235" text-anchor="start" font-size="12">• Hardware/software constraints</text>
  <text x="200" y="260" text-anchor="start" font-size="12">• Affinity and anti-affinity</text>
  <text x="200" y="285" text-anchor="start" font-size="12">• Data locality</text>
  <text x="200" y="310" text-anchor="start" font-size="12">• Workload interference</text>
  <text x="450" y="210" text-anchor="start" font-size="12">• Taints and tolerations</text>
  <text x="450" y="235" text-anchor="start" font-size="12">• Pod priority and preemption</text>
  <text x="450" y="260" text-anchor="start" font-size="12">• Node selectors</text>
  <text x="450" y="285" text-anchor="start" font-size="12">• Resource utilization</text>
  <text x="450" y="310" text-anchor="start" font-size="12">• Custom schedulers</text>
</svg>

---

## Controller Manager

1. **Node Controller**: Monitor node health
1. **Replication Controller**: Maintain pod count
1. **Endpoints Controller**: Populate endpoints
1. **Service Account Controller**: Create accounts
1. **Namespace Controller**: Manage namespaces

---

## Worker Node Components

1. **Kubelet**: Primary node agent
1. **Container Runtime**: Docker/containerd
1. **Kube-proxy**: Network proxy
1. **Pods**: Running containers
1. **Add-ons**: DNS, Dashboard, Monitoring

---

## Kubelet Responsibilities

```yaml
kubelet:
  responsibilities:
    - Register node with API server
    - Watch for pod assignments
    - Mount volumes
    - Download secrets
    - Run containers via runtime
    - Report node and pod status
    - Execute liveness/readiness probes
```

---

## Container Runtime

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Container Runtime Options</text>
  <rect x="100" y="100" width="150" height="80" fill="#0066cc" rx="5"/>
  <text x="175" y="130" text-anchor="middle" fill="white" font-weight="bold">Docker</text>
  <text x="175" y="155" text-anchor="middle" fill="white" font-size="11">Most common</text>
  <rect x="275" y="100" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="350" y="130" text-anchor="middle" fill="white" font-weight="bold">containerd</text>
  <text x="350" y="155" text-anchor="middle" fill="white" font-size="11">Industry standard</text>
  <rect x="450" y="100" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="525" y="130" text-anchor="middle" fill="white" font-weight="bold">CRI-O</text>
  <text x="525" y="155" text-anchor="middle" fill="white" font-size="11">OCI compatible</text>
  <rect x="625" y="100" width="125" height="80" fill="#fbbc04" rx="5"/>
  <text x="687" y="130" text-anchor="middle" font-weight="bold">rkt</text>
  <text x="687" y="155" text-anchor="middle" font-size="11">CoreOS</text>
  <rect x="200" y="220" width="400" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-weight="bold">Container Runtime Interface (CRI)</text>
  <text x="400" y="275" text-anchor="middle" font-size="12">Standard interface for container runtimes</text>
</svg>

---

## Kube-proxy

1. **Network proxy** on each node
1. **Maintains** network rules
1. **Allows** network communication
1. **Load balances** backend pods
1. **Modes**: userspace, iptables, IPVS

---

## Pods - Fundamental Unit

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: myapp
spec:
  containers:
  - name: app-container
    image: nginx:1.21
    ports:
    - containerPort: 80
```

---

## Pod Characteristics

1. **Smallest** deployable unit
1. **One or more** containers
1. **Shared** network namespace
1. **Shared** storage volumes
1. **Ephemeral** - not durable

---

## Multi-Container Pods

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Multi-Container Pod Patterns</text>
  <rect x="100" y="80" width="200" height="120" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="200" y="105" text-anchor="middle" font-weight="bold">Sidecar</text>
  <rect x="120" y="120" width="70" height="50" fill="#4285f4" rx="3"/>
  <text x="155" y="150" text-anchor="middle" fill="white" font-size="10">Main</text>
  <rect x="200" y="120" width="70" height="50" fill="#34a853" rx="3"/>
  <text x="235" y="150" text-anchor="middle" fill="white" font-size="10">Helper</text>
  <text x="200" y="190" text-anchor="middle" font-size="10">Logging, Monitoring</text>
  <rect x="320" y="80" width="200" height="120" fill="#e8f5e9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="420" y="105" text-anchor="middle" font-weight="bold">Ambassador</text>
  <rect x="340" y="120" width="70" height="50" fill="#4285f4" rx="3"/>
  <text x="375" y="150" text-anchor="middle" fill="white" font-size="10">Main</text>
  <rect x="420" y="120" width="70" height="50" fill="#fbbc04" rx="3"/>
  <text x="455" y="150" text-anchor="middle" font-size="10">Proxy</text>
  <text x="420" y="190" text-anchor="middle" font-size="10">Network proxy</text>
  <rect x="540" y="80" width="200" height="120" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="640" y="105" text-anchor="middle" font-weight="bold">Adapter</text>
  <rect x="560" y="120" width="70" height="50" fill="#4285f4" rx="3"/>
  <text x="595" y="150" text-anchor="middle" fill="white" font-size="10">Main</text>
  <rect x="640" y="120" width="70" height="50" fill="#ea4335" rx="3"/>
  <text x="675" y="150" text-anchor="middle" fill="white" font-size="10">Adapter</text>
  <text x="640" y="190" text-anchor="middle" font-size="10">Format conversion</text>
</svg>

---

## Labels and Selectors

```yaml
metadata:
  labels:
    environment: production
    tier: frontend
    app: web
    version: v1.2.3

# Selector examples
selector:
  matchLabels:
    app: web
    tier: frontend
```

---

## Label Selectors

```bash
# Equality-based
kubectl get pods -l environment=production
kubectl get pods -l environment!=production

# Set-based
kubectl get pods -l 'environment in (production, staging)'
kubectl get pods -l 'tier notin (backend)'
kubectl get pods -l 'app'  # Has label
kubectl get pods -l '!app' # Doesn't have label
```

---

## Annotations

```yaml
metadata:
  annotations:
    description: "Production web server"
    contact: "team@example.com"
    documentation: "https://docs.example.com"
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Pod"...}
```

---

## Namespaces Purpose

1. **Resource isolation**: Separate environments
1. **Access control**: RBAC per namespace
1. **Resource quotas**: Limit consumption
1. **Network policies**: Traffic control
1. **Organization**: Logical grouping

---

## Default Namespaces

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Default Kubernetes Namespaces</text>
  <rect x="100" y="80" width="180" height="100" fill="#4285f4" rx="5"/>
  <text x="190" y="110" text-anchor="middle" fill="white" font-weight="bold">default</text>
  <text x="190" y="135" text-anchor="middle" fill="white" font-size="11">User workloads</text>
  <text x="190" y="155" text-anchor="middle" fill="white" font-size="11">No namespace specified</text>
  <rect x="310" y="80" width="180" height="100" fill="#34a853" rx="5"/>
  <text x="400" y="110" text-anchor="middle" fill="white" font-weight="bold">kube-system</text>
  <text x="400" y="135" text-anchor="middle" fill="white" font-size="11">System components</text>
  <text x="400" y="155" text-anchor="middle" fill="white" font-size="11">DNS, proxy, etc.</text>
  <rect x="520" y="80" width="180" height="100" fill="#fbbc04" rx="5"/>
  <text x="610" y="110" text-anchor="middle" font-weight="bold">kube-public</text>
  <text x="610" y="135" text-anchor="middle" font-size="11">Public resources</text>
  <text x="610" y="155" text-anchor="middle" font-size="11">ConfigMaps, etc.</text>
  <rect x="255" y="210" width="290" height="100" fill="#ea4335" rx="5"/>
  <text x="400" y="240" text-anchor="middle" fill="white" font-weight="bold">kube-node-lease</text>
  <text x="400" y="265" text-anchor="middle" fill="white" font-size="11">Node heartbeat data</text>
  <text x="400" y="285" text-anchor="middle" fill="white" font-size="11">Improved node failure detection</text>
</svg>

---

## Working with Namespaces

```bash
# Create namespace
kubectl create namespace development

# Using namespace in commands
kubectl get pods -n development
kubectl apply -f app.yaml -n development

# Set default namespace
kubectl config set-context --current \
  --namespace=development

# Delete namespace (and all resources)
kubectl delete namespace development
```

---

## Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: development
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
    pods: "50"
```

---

## LimitRanges

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-mem-limit
  namespace: development
spec:
  limits:
  - default:
      cpu: "1"
      memory: "1Gi"
    defaultRequest:
      cpu: "0.5"
      memory: "256Mi"
    type: Container
```

---

## Node Resources

```bash
# View nodes
kubectl get nodes

# Node details
kubectl describe node node-name

# Node capacity
kubectl get nodes -o json | \
  jq '.items[].status.capacity'

# Node conditions
kubectl get nodes -o json | \
  jq '.items[].status.conditions'
```

---

## Node Components

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Node Resource Management</text>
  <rect x="100" y="80" width="600" height="60" fill="#4285f4" rx="5"/>
  <text x="400" y="100" text-anchor="middle" fill="white" font-weight="bold">Node Capacity</text>
  <text x="400" y="125" text-anchor="middle" fill="white" font-size="12">CPU: 16 cores | Memory: 64GB | Storage: 500GB</text>
  <rect x="100" y="160" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="175" y="185" text-anchor="middle" fill="white" font-size="11">System Reserved</text>
  <text x="175" y="205" text-anchor="middle" fill="white" font-size="10">CPU: 1 | Mem: 2GB</text>
  <rect x="260" y="160" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="335" y="185" text-anchor="middle" font-size="11">Kubernetes Reserved</text>
  <text x="335" y="205" text-anchor="middle" font-size="10">CPU: 1 | Mem: 2GB</text>
  <rect x="420" y="160" width="150" height="60" fill="#ea4335" rx="5"/>
  <text x="495" y="185" text-anchor="middle" fill="white" font-size="11">Eviction Threshold</text>
  <text x="495" y="205" text-anchor="middle" fill="white" font-size="10">Memory: 100Mi</text>
  <rect x="580" y="160" width="120" height="60" fill="#9c27b0" rx="5"/>
  <text x="640" y="185" text-anchor="middle" fill="white" font-size="11">Allocatable</text>
  <text x="640" y="205" text-anchor="middle" fill="white" font-size="10">User Pods</text>
  <rect x="100" y="250" width="600" height="60" fill="#e8f5e9" rx="5"/>
  <text x="400" y="275" text-anchor="middle" font-weight="bold">Allocatable = Capacity - Reserved - Eviction</text>
  <text x="400" y="295" text-anchor="middle" font-size="12">CPU: 14 cores | Memory: 59.9GB available for pods</text>
</svg>

---

## Taints and Tolerations

```yaml
# Taint a node
kubectl taint nodes node1 key=value:NoSchedule

# Pod with toleration
spec:
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
```

---

## Node Selectors

```yaml
# Label node
kubectl label nodes node1 disktype=ssd

# Pod with node selector
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeSelector:
    disktype: ssd
  containers:
  - name: nginx
    image: nginx
```

---

## Node Affinity

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: zone
            operator: In
            values:
            - zone1
```

---

## Pod Affinity

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
            - cache
        topologyKey: kubernetes.io/hostname
```

---

## Pod Anti-Affinity

```yaml
spec:
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - web
          topologyKey: kubernetes.io/hostname
```

---

## Resource Requests and Limits

```yaml
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

---

## Quality of Service Classes

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">QoS Classes</text>
  <rect x="100" y="80" width="200" height="150" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Guaranteed</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">Requests = Limits</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">For all containers</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">CPU & Memory set</text>
  <text x="200" y="200" text-anchor="middle" fill="white" font-size="10">Highest priority</text>
  <text x="200" y="215" text-anchor="middle" fill="white" font-size="10">Last to be killed</text>
  <rect x="320" y="80" width="200" height="150" fill="#fbbc04" rx="5"/>
  <text x="420" y="110" text-anchor="middle" font-weight="bold">Burstable</text>
  <text x="420" y="135" text-anchor="middle" font-size="11">At least one request</text>
  <text x="420" y="155" text-anchor="middle" font-size="11">or limit set</text>
  <text x="420" y="175" text-anchor="middle" font-size="11">Not Guaranteed</text>
  <text x="420" y="200" text-anchor="middle" font-size="10">Medium priority</text>
  <text x="420" y="215" text-anchor="middle" font-size="10">Killed after BestEffort</text>
  <rect x="540" y="80" width="200" height="150" fill="#ea4335" rx="5"/>
  <text x="640" y="110" text-anchor="middle" fill="white" font-weight="bold">BestEffort</text>
  <text x="640" y="135" text-anchor="middle" fill="white" font-size="11">No requests</text>
  <text x="640" y="155" text-anchor="middle" fill="white" font-size="11">No limits</text>
  <text x="640" y="175" text-anchor="middle" fill="white" font-size="11">Uses available resources</text>
  <text x="640" y="200" text-anchor="middle" fill="white" font-size="10">Lowest priority</text>
  <text x="640" y="215" text-anchor="middle" fill="white" font-size="10">First to be killed</text>
</svg>

---

## Priority Classes

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority class"

---
apiVersion: v1
kind: Pod
spec:
  priorityClassName: high-priority
```

---

## Dashboard Overview

1. **Web-based** UI for Kubernetes
1. **Deploy** containerized applications
1. **Troubleshoot** applications
1. **Manage** cluster resources
1. **View** resource utilization

---

## Installing Dashboard

```bash
# Deploy dashboard
kubectl apply -f https://raw.githubusercontent.com/\
kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Create service account
kubectl create serviceaccount dashboard-admin -n kube-system

# Create cluster role binding
kubectl create clusterrolebinding dashboard-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=kube-system:dashboard-admin

# Get token
kubectl -n kube-system create token dashboard-admin
```

---

## Accessing Dashboard

```bash
# Start proxy
kubectl proxy

# Access URL
http://localhost:8001/api/v1/namespaces/\
kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

# Or use port-forward
kubectl port-forward -n kubernetes-dashboard \
  service/kubernetes-dashboard 8443:443

# Access at https://localhost:8443
```

---

## Dashboard Features

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Dashboard Capabilities</text>
  <rect x="100" y="80" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Overview</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="11">Cluster status</text>
  <text x="175" y="145" text-anchor="middle" fill="white" font-size="11">Resource usage</text>
  <rect x="270" y="80" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">Workloads</text>
  <text x="345" y="130" text-anchor="middle" fill="white" font-size="11">Deployments</text>
  <text x="345" y="145" text-anchor="middle" fill="white" font-size="11">Pods, Jobs</text>
  <rect x="440" y="80" width="150" height="80" fill="#fbbc04" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">Services</text>
  <text x="515" y="130" text-anchor="middle" font-size="11">Discovery</text>
  <text x="515" y="145" text-anchor="middle" font-size="11">Load balancing</text>
  <rect x="610" y="80" width="140" height="80" fill="#ea4335" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">Config</text>
  <text x="680" y="130" text-anchor="middle" fill="white" font-size="11">ConfigMaps</text>
  <text x="680" y="145" text-anchor="middle" fill="white" font-size="11">Secrets</text>
  <rect x="100" y="180" width="150" height="80" fill="#9c27b0" rx="5"/>
  <text x="175" y="210" text-anchor="middle" fill="white" font-weight="bold">Storage</text>
  <text x="175" y="230" text-anchor="middle" fill="white" font-size="11">PVCs</text>
  <text x="175" y="245" text-anchor="middle" fill="white" font-size="11">Storage Classes</text>
  <rect x="270" y="180" width="150" height="80" fill="#607d8b" rx="5"/>
  <text x="345" y="210" text-anchor="middle" fill="white" font-weight="bold">Logs</text>
  <text x="345" y="230" text-anchor="middle" fill="white" font-size="11">Pod logs</text>
  <text x="345" y="245" text-anchor="middle" fill="white" font-size="11">Container logs</text>
  <rect x="440" y="180" width="150" height="80" fill="#ff5722" rx="5"/>
  <text x="515" y="210" text-anchor="middle" fill="white" font-weight="bold">Shell</text>
  <text x="515" y="230" text-anchor="middle" fill="white" font-size="11">Exec into pods</text>
  <text x="515" y="245" text-anchor="middle" fill="white" font-size="11">Debug containers</text>
</svg>

---

## Metrics Server

```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/\
metrics-server/releases/latest/download/components.yaml

# For Minikube
minikube addons enable metrics-server

# View metrics
kubectl top nodes
kubectl top pods
kubectl top pods --containers
```

---

## Resource Monitoring

```bash
# Node metrics
kubectl top nodes
NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
minikube   198m         9%     1582Mi          40%

# Pod metrics
kubectl top pods
NAME                     CPU(cores)   MEMORY(bytes)
nginx-6799fc88d8-x48qf   1m           2Mi

# Container metrics
kubectl top pod nginx-6799fc88d8-x48qf --containers
```

---

## Summary

1. Master components manage cluster state
1. Worker nodes run application workloads
1. Pods are fundamental deployment units
1. Labels enable flexible organization
1. Namespaces provide resource isolation
