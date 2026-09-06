---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:azure
  - infrastructure:gcp
  - concepts:architecture
level: advanced
category: cloud
audience:
  - audiences:architects
  - audiences:managers

---

# Kubernetes as Cloud Abstraction

---

## Why Kubernetes for Multi-Cloud?
- Standard API across all providers
- Workloads defined in portable YAML
- Large ecosystem of cloud-agnostic tools
- Managed offerings on every major cloud
- De facto standard for container orchestration

---

## Managed Kubernetes Services
- AWS: EKS (Elastic Kubernetes Service)
- Azure: AKS (Azure Kubernetes Service)
- GCP: GKE (Google Kubernetes Engine)
- All run upstream Kubernetes with provider-specific integrations
- GKE is generally considered the most mature

---

## Kubernetes Across Clouds

![k8s](svg/courses/cloud/multi-cloud-strategy/05_kubernetes/k8s_across_clouds.svg)

---

## What Kubernetes Standardizes
- Container scheduling and orchestration
- Service discovery and load balancing
- Rolling deployments and rollbacks
- Configuration and secret management
- Health checks and self-healing

---

## What Kubernetes Does NOT Standardize
- Ingress controller implementations
- Storage classes and provisioners
- Load balancer annotations
- Node auto-scaling behavior
- Networking CNI plugins

---

## Portable Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
        - name: web
          image: myregistry.io/web-app:1.2.3
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

---

## This Deployment Works Identically On
- EKS (AWS)
- AKS (Azure)
- GKE (GCP)
- Self-managed Kubernetes on bare metal
- k3s, kind, minikube (local development)
- This is the power of Kubernetes as abstraction

---

## Provider-Specific: Ingress Annotations

```yaml
# AWS ALB Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip

# GKE Ingress
# metadata:
#   annotations:
#     kubernetes.io/ingress.class: gce
#     kubernetes.io/ingress.global-static-ip-name: web-ip
```

---

## Kustomize for Multi-Cloud Overlays

```tree
k8s/
  base/
    deployment.yaml
    service.yaml
    kustomization.yaml
  overlays/
    aws/
      kustomization.yaml
      ingress-patch.yaml
    azure/
      kustomization.yaml
      ingress-patch.yaml
    gcp/
      kustomization.yaml
      ingress-patch.yaml
```

---

## Kustomize Base

```yaml
# k8s/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
```

---

## Kustomize AWS Overlay

```yaml
# k8s/overlays/aws/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
  - ingress.yaml
patches:
  - target:
      kind: Deployment
      name: web-app
    patch: |-
      - op: add
        path: /spec/template/metadata/annotations
        value:
          iam.amazonaws.com/role: web-app-role
```

---

## kubectl: Universal Interface

```bash
# These commands work identically on EKS, AKS, GKE
kubectl get nodes
kubectl get pods -n production
kubectl apply -f deployment.yaml
kubectl rollout status deployment/web-app
kubectl scale deployment/web-app --replicas=5
kubectl logs deployment/web-app --tail=100
kubectl exec -it pod/web-app-abc123 -- /bin/sh
```

---

## Platform Engineering with Kubernetes
- Build an internal developer platform on top of Kubernetes
- Standardize deployment patterns across clouds
- Provide self-service capabilities through custom resources
- Abstract cloud differences behind platform APIs
- Teams deploy to "the platform," not to a specific cloud

---

## Limitations of Kubernetes as Abstraction
- Storage: PersistentVolume provisioners are cloud-specific
- Networking: CNI plugins and policies vary
- Autoscaling: cluster autoscaler configuration differs
- Cost: managed Kubernetes has per-cluster fees ($73/mo EKS, free AKS control plane)
- Not all workloads belong in Kubernetes

---

## Portability Layers

![layers](svg/courses/cloud/multi-cloud-strategy/05_kubernetes/portability_layers.svg)
