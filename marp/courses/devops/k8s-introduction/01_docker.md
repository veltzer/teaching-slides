---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - infrastructure:orchestration
  - practices:devops
  - tools:docker
level: beginner
category: devops
audience:
  - audiences:developers
  - audiences:devops
  - audiences:sysadmins

---
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

![what_is_container_orchestration](svg/courses/devops/k8s-introduction/01_docker/what_is_container_orchestration.svg)

---

## Why Containers?

1. Lightweight virtualization
1. Consistent environments
1. Fast deployment
1. Resource efficiency
1. Portable across platforms

---

## Container Image Layers

![container_image_layers](svg/courses/devops/k8s-introduction/01_docker/container_image_layers.svg)

---

## Container vs Virtual Machine

![container_vs_virtual_machine](svg/courses/devops/k8s-introduction/01_docker/container_vs_virtual_machine.svg)

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

![core_concepts](svg/courses/devops/k8s-introduction/01_docker/core_concepts.svg)

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

![kubernetes_architecture](svg/courses/devops/k8s-introduction/01_docker/kubernetes_architecture.svg)

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

![kubernetes_ecosystem](svg/courses/devops/k8s-introduction/01_docker/kubernetes_ecosystem.svg)

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

![namespaces](svg/courses/devops/k8s-introduction/01_docker/namespaces.svg)

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

![rolling_updates](svg/courses/devops/k8s-introduction/01_docker/rolling_updates.svg)

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
