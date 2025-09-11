# Introduction to Kubernetes

---

## Welcome to Kubernetes

1. Industry standard for container orchestration
1. Also known as `k8s`
1. Manages containerized applications at scale
1. Open-source platform originally from Google

---

## Course Overview

1. From zero to beginner level
1. Hands-on with real systems
1. Real cluster orchestration
1. 40 hours / 5 days

---

## What We'll Cover

1. `Docker` fundamentals
1. `Kubernetes` architecture
1. Pods and controllers
1. Services and volumes
1. Cluster administration

---

## Who Should Take This Course

1. Developers deploying applications
1. Architects designing systems
1. DevOps engineers expanding skills
1. Cloud practitioners evaluating options

---

## Prerequisites

1. Tech environment experience (required)
1. Web application understanding (required)
1. DevOps experience (helpful)
1. System administration (helpful)
1. Cloud platform familiarity (helpful)

---

## What is Container Orchestration?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold">Container Orchestration</text>
  <rect x="100" y="100" width="120" height="80" fill="#4285f4" rx="5"/>
  <text x="160" y="145" text-anchor="middle" fill="white">Container 1</text>
  <rect x="250" y="100" width="120" height="80" fill="#4285f4" rx="5"/>
  <text x="310" y="145" text-anchor="middle" fill="white">Container 2</text>
  <rect x="400" y="100" width="120" height="80" fill="#4285f4" rx="5"/>
  <text x="460" y="145" text-anchor="middle" fill="white">Container 3</text>
  <rect x="550" y="100" width="120" height="80" fill="#4285f4" rx="5"/>
  <text x="610" y="145" text-anchor="middle" fill="white">Container 4</text>
  <rect x="300" y="230" width="200" height="60" fill="#34a853" rx="5"/>
  <text x="400" y="265" text-anchor="middle" fill="white" font-weight="bold">Orchestrator</text>
</svg>

---

## Why Containers?

1. Lightweight virtualization
1. Consistent environments
1. Fast deployment
1. Resource efficiency
1. Portable across platforms

---

## Container vs Virtual Machine

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <g id="vm">
    <rect x="50" y="50" width="300" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
    <text x="200" y="30" text-anchor="middle" font-weight="bold">Virtual Machines</text>
    <rect x="60" y="280" width="280" height="60" fill="#666"/>
    <text x="200" y="315" text-anchor="middle" fill="white">Hardware</text>
    <rect x="60" y="210" width="280" height="60" fill="#888"/>
    <text x="200" y="245" text-anchor="middle" fill="white">Hypervisor</text>
    <rect x="70" y="80" width="80" height="120" fill="#4285f4"/>
    <text x="110" y="100" text-anchor="middle" fill="white" font-size="12">Guest OS</text>
    <text x="110" y="140" text-anchor="middle" fill="white" font-size="12">App</text>
    <rect x="160" y="80" width="80" height="120" fill="#4285f4"/>
    <text x="200" y="100" text-anchor="middle" fill="white" font-size="12">Guest OS</text>
    <text x="200" y="140" text-anchor="middle" fill="white" font-size="12">App</text>
    <rect x="250" y="80" width="80" height="120" fill="#4285f4"/>
    <text x="290" y="100" text-anchor="middle" fill="white" font-size="12">Guest OS</text>
    <text x="290" y="140" text-anchor="middle" fill="white" font-size="12">App</text>
  </g>
  <g id="container">
    <rect x="450" y="50" width="300" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
    <text x="600" y="30" text-anchor="middle" font-weight="bold">Containers</text>
    <rect x="460" y="280" width="280" height="60" fill="#666"/>
    <text x="600" y="315" text-anchor="middle" fill="white">Hardware</text>
    <rect x="460" y="210" width="280" height="60" fill="#888"/>
    <text x="600" y="245" text-anchor="middle" fill="white">Host OS</text>
    <rect x="460" y="140" width="280" height="60" fill="#34a853"/>
    <text x="600" y="175" text-anchor="middle" fill="white">Container Runtime</text>
    <rect x="470" y="80" width="80" height="50" fill="#4285f4"/>
    <text x="510" y="110" text-anchor="middle" fill="white">App</text>
    <rect x="560" y="80" width="80" height="50" fill="#4285f4"/>
    <text x="600" y="110" text-anchor="middle" fill="white">App</text>
    <rect x="650" y="80" width="80" height="50" fill="#4285f4"/>
    <text x="690" y="110" text-anchor="middle" fill="white">App</text>
  </g>
</svg>

---

## The Container Challenge

1. Running hundreds of containers
1. Ensuring high availability
1. Scaling on demand
1. Load balancing traffic
1. Managing updates

---

## Enter Kubernetes

1. Automates container deployment
1. Manages scaling and failover
1. Provides service discovery
1. Handles storage orchestration
1. Manages secrets and configuration

---

## Kubernetes History

1. **2003-2004**: Google's Borg system begins
1. **2014**: Kubernetes open-sourced by Google
1. **2015**: v1.0 released, CNCF founded
1. **2016**: Becomes CNCF graduated project
1. **Today**: Industry standard

---

## Why "K8s"?

1. `Kubernetes`
1. 8 letters between K and s
1. Common abbreviation pattern
1. Easier to type and say
1. Community adopted term

---

## Core Concepts

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold">Kubernetes Cluster</text>
  <rect x="150" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="250" y="110" text-anchor="middle" fill="white" font-weight="bold">Control Plane</text>
  <text x="250" y="130" text-anchor="middle" fill="white" font-size="12">API Server</text>
  <text x="250" y="150" text-anchor="middle" fill="white" font-size="12">Scheduler</text>
  <text x="250" y="170" text-anchor="middle" fill="white" font-size="12">Controller</text>
  <rect x="450" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="550" y="110" text-anchor="middle" fill="white" font-weight="bold">Worker Nodes</text>
  <text x="550" y="130" text-anchor="middle" fill="white" font-size="12">Kubelet</text>
  <text x="550" y="150" text-anchor="middle" fill="white" font-size="12">Container Runtime</text>
  <text x="550" y="170" text-anchor="middle" fill="white" font-size="12">Kube-proxy</text>
  <rect x="200" y="220" width="100" height="80" fill="#fbbc04" rx="5"/>
  <text x="250" y="265" text-anchor="middle">Pod</text>
  <rect x="350" y="220" width="100" height="80" fill="#fbbc04" rx="5"/>
  <text x="400" y="265" text-anchor="middle">Pod</text>
  <rect x="500" y="220" width="100" height="80" fill="#fbbc04" rx="5"/>
  <text x="550" y="265" text-anchor="middle">Pod</text>
</svg>

---

## What is a Pod?

1. Smallest deployable unit
1. One or more containers
1. Shared network and storage
1. Ephemeral by design
1. Has unique IP address

---

## What is a Node?

1. Physical or virtual machine
1. Runs container runtime
1. Managed by control plane
1. Contains multiple pods
1. Has CPU and memory resources

---

## Control Plane Components

1. **API Server**: Frontend to Kubernetes
1. **etcd**: Key-value store for cluster data
1. **Scheduler**: Assigns pods to nodes
1. **Controller Manager**: Runs controllers
1. **Cloud Controller**: Cloud-specific logic

---

## Node Components

1. **Kubelet**: Ensures containers running
1. **Container Runtime**: Runs containers
1. **Kube-proxy**: Network proxy
1. **Pods**: Your applications

---

## Kubernetes Architecture

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="400" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Kubernetes Architecture</text>
  <rect x="100" y="80" width="250" height="150" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-weight="bold">Control Plane</text>
  <rect x="110" y="120" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="160" y="140" text-anchor="middle" fill="white" font-size="12">API Server</text>
  <rect x="220" y="120" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="270" y="140" text-anchor="middle" fill="white" font-size="12">Scheduler</text>
  <rect x="110" y="160" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="160" y="180" text-anchor="middle" fill="white" font-size="12">Controller</text>
  <rect x="220" y="160" width="100" height="30" fill="#4285f4" rx="3"/>
  <text x="270" y="180" text-anchor="middle" fill="white" font-size="12">etcd</text>
  <rect x="450" y="80" width="250" height="150" fill="#e8f5e9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="575" y="105" text-anchor="middle" font-weight="bold">Worker Node</text>
  <rect x="460" y="120" width="100" height="30" fill="#34a853" rx="3"/>
  <text x="510" y="140" text-anchor="middle" fill="white" font-size="12">Kubelet</text>
  <rect x="570" y="120" width="120" height="30" fill="#34a853" rx="3"/>
  <text x="630" y="140" text-anchor="middle" fill="white" font-size="12">Container Runtime</text>
  <rect x="460" y="160" width="100" height="30" fill="#34a853" rx="3"/>
  <text x="510" y="180" text-anchor="middle" fill="white" font-size="12">Kube-proxy</text>
  <rect x="100" y="280" width="600" height="120" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="400" y="305" text-anchor="middle" font-weight="bold">Application Pods</text>
  <circle cx="200" cy="350" r="30" fill="#fbbc04"/>
  <text x="200" y="355" text-anchor="middle">Pod</text>
  <circle cx="300" cy="350" r="30" fill="#fbbc04"/>
  <text x="300" y="355" text-anchor="middle">Pod</text>
  <circle cx="400" cy="350" r="30" fill="#fbbc04"/>
  <text x="400" y="355" text-anchor="middle">Pod</text>
  <circle cx="500" cy="350" r="30" fill="#fbbc04"/>
  <text x="500" y="355" text-anchor="middle">Pod</text>
  <circle cx="600" cy="350" r="30" fill="#fbbc04"/>
  <text x="600" y="355" text-anchor="middle">Pod</text>
</svg>

---

## Key Kubernetes Objects

1. **Pods**: Basic execution unit
1. **Services**: Network abstraction
1. **Deployments**: Manage replicas
1. **ConfigMaps**: Configuration data
1. **Secrets**: Sensitive data

---

## Declarative vs Imperative

## Imperative
```bash
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
kubectl expose deployment nginx --port=80
```

## Declarative
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
```

---

## YAML Configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: web
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
```

---

## Benefits of Kubernetes

1. **Automatic scaling**: Based on load
1. **Self-healing**: Restarts failed containers
1. **Load balancing**: Distributes traffic
1. **Rolling updates**: Zero downtime
1. **Secret management**: Secure credentials

---

## Common Use Cases

1. Microservices architecture
1. CI/CD pipelines
1. Big data processing
1. Machine learning workloads
1. Web applications

---

## Kubernetes Ecosystem

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="200" r="60" fill="#326ce5"/>
  <text x="400" y="210" text-anchor="middle" fill="white" font-weight="bold">K8s</text>
  <circle cx="250" cy="120" r="40" fill="#4285f4"/>
  <text x="250" y="125" text-anchor="middle" fill="white" font-size="12">Helm</text>
  <circle cx="550" cy="120" r="40" fill="#4285f4"/>
  <text x="550" y="125" text-anchor="middle" fill="white" font-size="12">Istio</text>
  <circle cx="250" cy="280" r="40" fill="#34a853"/>
  <text x="250" y="285" text-anchor="middle" fill="white" font-size="12">Prometheus</text>
  <circle cx="550" cy="280" r="40" fill="#34a853"/>
  <text x="550" y="285" text-anchor="middle" fill="white" font-size="12">Grafana</text>
  <circle cx="150" cy="200" r="40" fill="#fbbc04"/>
  <text x="150" y="205" text-anchor="middle" font-size="12">ArgoCD</text>
  <circle cx="650" cy="200" r="40" fill="#fbbc04"/>
  <text x="650" y="205" text-anchor="middle" font-size="12">Flux</text>
  <line x1="190" y1="200" x2="340" y2="200" stroke="#666" stroke-width="2"/>
  <line x1="460" y1="200" x2="610" y2="200" stroke="#666" stroke-width="2"/>
  <line x1="280" y1="150" x2="360" y2="170" stroke="#666" stroke-width="2"/>
  <line x1="520" y1="150" x2="440" y2="170" stroke="#666" stroke-width="2"/>
  <line x1="280" y1="250" x2="360" y2="230" stroke="#666" stroke-width="2"/>
  <line x1="520" y1="250" x2="440" y2="230" stroke="#666" stroke-width="2"/>
</svg>

---

## Cloud Provider Support

1. **AWS**: EKS (Elastic Kubernetes Service)
1. **Google Cloud**: GKE (Google Kubernetes Engine)
1. **Azure**: AKS (Azure Kubernetes Service)
1. **IBM**: IKS (IBM Kubernetes Service)
1. **On-premise**: OpenShift, Rancher

---

## Local Development Options

1. **Minikube**: Single-node cluster
1. **Kind**: Kubernetes in Docker
1. **K3s**: Lightweight Kubernetes
1. **Docker Desktop**: Built-in Kubernetes
1. **MicroK8s**: Canonical's solution

---

## kubectl - The CLI Tool

1. Command-line interface for Kubernetes
1. Manages cluster resources
1. Deploys applications
1. Inspects and debugs
1. Updates configurations

---

## Basic kubectl Commands

```bash
# Get cluster info
kubectl cluster-info

# List all pods
kubectl get pods

# Describe a pod
kubectl describe pod my-pod

# View logs
kubectl logs my-pod
```

---

## Resource Types

1. **Workloads**: Deployments, StatefulSets, DaemonSets
1. **Services**: ClusterIP, NodePort, LoadBalancer
1. **Storage**: PersistentVolumes, PersistentVolumeClaims
1. **Configuration**: ConfigMaps, Secrets
1. **Security**: ServiceAccounts, Roles, RoleBindings

---

## Namespaces

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Kubernetes Namespaces</text>
  <rect x="150" y="80" width="150" height="230" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-weight="bold">development</text>
  <rect x="160" y="120" width="130" height="40" fill="#4285f4" rx="3"/>
  <text x="225" y="145" text-anchor="middle" fill="white">App Pods</text>
  <rect x="160" y="170" width="130" height="40" fill="#4285f4" rx="3"/>
  <text x="225" y="195" text-anchor="middle" fill="white">Services</text>
  <rect x="325" y="80" width="150" height="230" fill="#e8f5e9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-weight="bold">staging</text>
  <rect x="335" y="120" width="130" height="40" fill="#34a853" rx="3"/>
  <text x="400" y="145" text-anchor="middle" fill="white">App Pods</text>
  <rect x="335" y="170" width="130" height="40" fill="#34a853" rx="3"/>
  <text x="400" y="195" text-anchor="middle" fill="white">Services</text>
  <rect x="500" y="80" width="150" height="230" fill="#ffebee" stroke="#d32f2f" stroke-width="2" rx="5"/>
  <text x="575" y="105" text-anchor="middle" font-weight="bold">production</text>
  <rect x="510" y="120" width="130" height="40" fill="#ea4335" rx="3"/>
  <text x="575" y="145" text-anchor="middle" fill="white">App Pods</text>
  <rect x="510" y="170" width="130" height="40" fill="#ea4335" rx="3"/>
  <text x="575" y="195" text-anchor="middle" fill="white">Services</text>
</svg>

---

## Labels and Selectors

```yaml
metadata:
  labels:
    app: frontend
    environment: production
    version: v1.2.3
```

1. Key-value pairs
1. Organize resources
1. Enable selection
1. Support queries

---

## Service Discovery

1. **DNS**: Internal cluster DNS
1. **Environment Variables**: Service info
1. **Service Types**: Different exposure levels
1. **Endpoints**: Backend pod IPs
1. **Load Balancing**: Traffic distribution

---

## Storage in Kubernetes

1. **Volumes**: Pod-level storage
1. **PersistentVolumes**: Cluster resources
1. **PersistentVolumeClaims**: Storage requests
1. **StorageClasses**: Dynamic provisioning
1. **CSI**: Container Storage Interface

---

## Scaling Applications

## Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
```

---

## Health Checks

1. **Liveness Probe**: Is container running?
1. **Readiness Probe**: Ready for traffic?
1. **Startup Probe**: Has container started?

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

## Rolling Updates

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Rolling Update Process</text>
  <g id="step1">
    <text x="100" y="60" text-anchor="middle" font-size="12">Step 1</text>
    <rect x="50" y="80" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="100" y="105" text-anchor="middle" fill="white">v1</text>
    <rect x="50" y="130" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="100" y="155" text-anchor="middle" fill="white">v1</text>
    <rect x="50" y="180" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="100" y="205" text-anchor="middle" fill="white">v1</text>
  </g>
  <g id="step2">
    <text x="250" y="60" text-anchor="middle" font-size="12">Step 2</text>
    <rect x="200" y="80" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="250" y="105" text-anchor="middle" fill="white">v2</text>
    <rect x="200" y="130" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="250" y="155" text-anchor="middle" fill="white">v1</text>
    <rect x="200" y="180" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="250" y="205" text-anchor="middle" fill="white">v1</text>
  </g>
  <g id="step3">
    <text x="400" y="60" text-anchor="middle" font-size="12">Step 3</text>
    <rect x="350" y="80" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="400" y="105" text-anchor="middle" fill="white">v2</text>
    <rect x="350" y="130" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="400" y="155" text-anchor="middle" fill="white">v2</text>
    <rect x="350" y="180" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="400" y="205" text-anchor="middle" fill="white">v1</text>
  </g>
  <g id="step4">
    <text x="550" y="60" text-anchor="middle" font-size="12">Step 4</text>
    <rect x="500" y="80" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="550" y="105" text-anchor="middle" fill="white">v2</text>
    <rect x="500" y="130" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="550" y="155" text-anchor="middle" fill="white">v2</text>
    <rect x="500" y="180" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="550" y="205" text-anchor="middle" fill="white">v2</text>
  </g>
  <path d="M 160 150 L 190 150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 310 150 L 340 150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 460 150 L 490 150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

---

## Security Best Practices

1. **RBAC**: Role-Based Access Control
1. **Network Policies**: Traffic rules
1. **Pod Security**: Security contexts
1. **Secrets Management**: Encrypted storage
1. **Image Scanning**: Vulnerability checks

---

## Monitoring and Logging

1. **Metrics Server**: Resource metrics
1. **Prometheus**: Time-series data
1. **Grafana**: Visualization
1. **ELK Stack**: Log aggregation
1. **Jaeger**: Distributed tracing

---

## Course Journey Ahead

1. **Day 1**: Docker and basics
1. **Day 2**: Core Kubernetes concepts
1. **Day 3**: Services and networking
1. **Day 4**: Storage and configuration
1. **Day 5**: Production practices

---

## Getting Started Checklist

1. ✓ Ubuntu 24.04 machine ready
1. ✓ 8 GB RAM available
1. ✓ Internet access configured
1. ✓ Sudo privileges confirmed
1. ✓ Ready to learn!

---

## Summary

1. Kubernetes orchestrates containers at scale
1. Declarative configuration approach
1. Rich ecosystem of tools
1. Industry standard platform
1. Essential for modern DevOps

---

## Next Steps

1. Install Docker
1. Set up Minikube
1. Deploy first application
1. Explore `kubectl` commands
1. Build confidence with hands-on practice
