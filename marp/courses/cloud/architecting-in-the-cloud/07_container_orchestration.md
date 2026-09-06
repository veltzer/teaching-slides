---
tags:
  - infrastructure:cloud
  - infrastructure:containers
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---

# Container Orchestration in the Cloud

---

## Orchestration Choices

![orchestration](svg/courses/cloud/architecting-in-the-cloud/07_container_orchestration/orchestration.svg)

---

## Why Containers?
- Package application with all dependencies
- Consistent across dev, staging, production
- Lightweight (shared OS kernel, no hypervisor)
- Start in seconds
- Standard packaging format (Docker/OCI)

---

## Containers vs Virtual Machines
- VMs: full OS per instance, heavy, slow to start
- Containers: share host OS, lightweight, fast
- VMs: stronger isolation
- Containers: better resource utilization
- Many organizations use both

---

## Why Orchestration?
- Running one container is easy
- Running hundreds or thousands requires orchestration
- Scheduling, scaling, networking, health management
- Kubernetes is the industry standard
- Cloud providers offer managed Kubernetes

---

## Kubernetes Overview
- Open-source container orchestration platform
- Originally from Google (Borg heritage)
- Declarative configuration
- Self-healing, auto-scaling, rolling updates
- Massive ecosystem and community

---

## Managed Kubernetes Services
- AWS EKS (Elastic Kubernetes Service)
- Azure AKS (Azure Kubernetes Service)
- GCP GKE (Google Kubernetes Engine)
- Provider manages the control plane
- You manage the worker nodes (or use managed node groups)

---

## Managed vs Self-Managed Kubernetes
- Managed: control plane handled by provider
- Self-managed: you run everything (kubeadm, kops)
- Managed: less operational burden, faster setup
- Self-managed: full control, more complexity
- For most teams: managed is the right choice

---

## Managed K8s

![managed_k8s](svg/courses/cloud/architecting-in-the-cloud/07_container_orchestration/managed_k8s.svg)

---

## EKS vs AKS vs GKE
- GKE: most mature, fastest updates, best auto-scaling
- EKS: deepest AWS integration, largest customer base
- AKS: best Azure/AD integration, free control plane
- All support the same Kubernetes APIs
- Choice often follows primary cloud provider

---

## Kubernetes Architecture
- Control plane: API server, scheduler, controller manager, etcd
- Worker nodes: run your containers (pods)
- Pods: smallest deployable unit (one or more containers)
- Services: stable networking for pods
- Ingress: external access to services

---

## Key Kubernetes Resources
- Deployment: manages replica sets of pods
- Service: load balancing and discovery
- ConfigMap/Secret: configuration and credentials
- PersistentVolumeClaim: storage
- Namespace: logical isolation within a cluster

---

## Kubernetes Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:v1.2.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
```

---

## Scaling in Kubernetes
- Horizontal Pod Autoscaler (HPA): scale pods based on metrics
- Vertical Pod Autoscaler (VPA): resize pod resources
- Cluster Autoscaler: add/remove nodes
- Karpenter (AWS): fast, efficient node provisioning
- KEDA: event-driven autoscaling

---

## Kubernetes Networking
- Every pod gets an IP address
- Services provide stable endpoints
- Ingress controllers for HTTP routing
- Network policies for segmentation
- Service mesh for advanced traffic management

---

## Container Registries
- Store and distribute container images
- AWS ECR, Azure ACR, GCP Artifact Registry
- Private registries for proprietary images
- Image scanning for vulnerabilities
- Tag images with version, not just "latest"

---

## Service Mesh
- Manage service-to-service communication
- Istio, Linkerd, AWS App Mesh
- Traffic management (canary, blue-green)
- Mutual TLS between services
- Observability (distributed tracing, metrics)

---

## Kubernetes Security
- RBAC for access control
- Pod Security Standards (restricted, baseline)
- Network Policies for pod-to-pod traffic
- Secrets management (external secrets operator)
- Image scanning before deployment

---

## Kubernetes Cost Optimization
- Right-size pod resource requests and limits
- Use Cluster Autoscaler for node management
- Spot/preemptible nodes for non-critical workloads
- Namespace-based resource quotas
- Monitor with Kubecost or native tools

---

## Helm and Package Management
- Helm: package manager for Kubernetes
- Charts: reusable application templates
- Values: customize deployments
- Helm repositories for sharing
- Standard way to deploy complex applications

---

## Helm Install and Upgrade

```bash
# Add a chart repository
helm repo add bitnami https://charts.bitnami.com

# Install a release
helm install my-redis bitnami/redis \
  --set auth.password=secret123

# Upgrade with new values
helm upgrade my-redis bitnami/redis \
  --set replica.replicaCount=3

# Rollback to previous version
helm rollback my-redis 1
```

---

## GitOps for Kubernetes
- Git as the single source of truth for cluster state
- ArgoCD or Flux watches Git, syncs to cluster
- Declarative: desired state in Git
- Audit trail: every change is a Git commit
- Rollback by reverting a commit

---

## Do You Need a Cloud-Portable Application?
- Kubernetes runs on any cloud
- But cloud-native services don't port easily
- True portability has a cost (lowest common denominator)
- Evaluate: will you actually switch clouds?
- Often better to embrace provider services for productivity

---

## Kubernetes vs Serverless
- Kubernetes: more control, more complexity
- Serverless: less control, less management
- Kubernetes: good for complex, long-running services
- Serverless: good for event-driven, short-lived tasks
- Not mutually exclusive: use both where appropriate

---

## Serverless Containers
- AWS Fargate: serverless compute for ECS/EKS
- Azure Container Instances: single container, no orchestration
- GCP Cloud Run: serverless containers from Docker images
- No nodes to manage
- Pay per vCPU/memory per second

---

## Container Observability
- Prometheus for metrics collection
- Grafana for dashboards
- Jaeger/Zipkin for distributed tracing
- Fluentd/Fluent Bit for log aggregation
- OpenTelemetry for unified observability

---

## Multi-Cluster Kubernetes
- Separate clusters per environment (dev, staging, prod)
- Multi-Region clusters for DR
- Fleet management tools (Rancher, Anthos)
- Consistent configuration across clusters
- Adds complexity: use only when needed

---

## Container Orchestration Best Practices
- Use managed Kubernetes unless you have a specific reason not to
- Define resource requests and limits for all pods
- Use namespaces for logical separation
- Implement health checks (liveness, readiness)
- Store configuration in ConfigMaps and Secrets
- Scan images for vulnerabilities
