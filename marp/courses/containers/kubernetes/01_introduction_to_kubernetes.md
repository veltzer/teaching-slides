---
tags:
  - infrastructure:kubernetes
level: intermediate
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Introduction to Kubernetes

---
## What This Chapter Covers

- What Kubernetes is
- Why orchestration
- Architecture: control plane and nodes
- Concepts: pod, service, deployment
- A short tour

---
## What Kubernetes Is

- Container orchestration platform
- Schedules containers across many machines
- Self-healing, auto-scaling
- Industry standard since ~2018
- Originally from Google (Borg-inspired)

---
## Why Orchestration

- One container: easy
- 1000 containers across 50 machines: needs orchestration
- Restarts, scheduling, networking, storage
- K8s automates all of this

---
## Architecture

- Control plane: API server, scheduler, controller, etcd
- Nodes: kubelet (agent), kube-proxy, container runtime
- One control plane manages many nodes
- HA: multiple control plane replicas

---
## Pod

- The smallest deployable unit
- One or more containers sharing network/storage
- Ephemeral; replaced when failed
- Most pods have one container

---
## Service

- Stable network endpoint
- Routes traffic to pods
- Pods come and go; service name stays
- ClusterIP, NodePort, LoadBalancer

---
## Deployment

- Manages pod replicas
- Rolling updates
- Scale up/down
- The standard way to run pods

---
## Namespace

- Logical separation within a cluster
- "default", "kube-system", custom
- Per-team, per-env

---
## kubectl

- The CLI
- "kubectl get pods"
- "kubectl apply -f manifest.yaml"
- The daily workflow

---
## YAML Manifests

- Declarative configuration
- Describe desired state
- K8s reconciles to match
- Versioned in git

---
## Kubernetes Distributions

- Vanilla: kubeadm
- Cloud: EKS (AWS), GKE (GCP), AKS (Azure)
- Local: minikube, kind, k3s
- Pick by deployment target

---
## When K8s Wins

- Many services, many machines
- Need HA, auto-scaling
- Multi-team platform
- Polyglot stacks

---
## When K8s Is Overkill

- One service
- A small team
- Simple stateful workloads
- Fargate / Cloud Run might do

---
## Common Misconceptions

- "K8s is just Docker but bigger" — way more complex
- "We need K8s to scale" — only past a threshold
- "K8s solves networking" — adds its own complexity
- "Easy migration to K8s" — multi-month projects typical
