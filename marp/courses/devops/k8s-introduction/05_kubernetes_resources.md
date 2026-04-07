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

![kubernetes_architecture_review](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/kubernetes_architecture_review.svg)

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

![scheduler_details](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/scheduler_details.svg)

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

![container_runtime](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/container_runtime.svg)

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

![multi_container_pods](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/multi_container_pods.svg)

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

![default_namespaces](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/default_namespaces.svg)

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

![node_components](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/node_components.svg)

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

![quality_of_service_classes](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/quality_of_service_classes.svg)

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

![dashboard_features](/svg/courses/devops/k8s-introduction/05_kubernetes_resources/dashboard_features.svg)

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
