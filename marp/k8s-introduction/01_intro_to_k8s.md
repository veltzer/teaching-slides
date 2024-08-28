# Introduction to Kubernetes
---
## What is Kubernetes?

- Kubernetes (K8s) is an open-source container orchestration platform
- Developed by Google, now maintained by the Cloud Native Computing Foundation (CNCF)
- Automates deployment, scaling, and management of containerized applications
- Provides a framework to run distributed systems resiliently
---
## Why Kubernetes?

- Enables high availability and scalability
- Facilitates declarative configuration and automation
- Supports microservices architecture
- Provides platform-agnostic deployment (cloud, on-premise, hybrid)
- Extensive ecosystem and community support
---
## Key Concepts in Kubernetes

1. **Containers**: Lightweight, portable units of software
2. **Pods**: Smallest deployable units in Kubernetes
3. **Nodes**: Worker machines in a Kubernetes cluster
4. **Clusters**: Set of nodes that run containerized applications
5. **Control Plane**: Manages the cluster state and desired configuration
---
## Kubernetes Architecture

![Kubernetes Architecture](https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec0f54ddc1d92aa8d4c87c96b/e7c81/images/docs/components-of-kubernetes.svg)
---
## Core Kubernetes Objects

- **Pods**: One or more containers that are scheduled together
- **Services**: Expose pods to network traffic
- **ConfigMaps & Secrets**: Store configuration data
- **Deployments**: Manage replica sets and provide declarative updates
- **StatefulSets**: Manage stateful applications
- **DaemonSets**: Ensure specific pods run on all (or some) nodes
---
## Kubernetes in Action

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```
---
## Course Outline

1. Kubernetes Fundamentals
2. Setting up a Kubernetes Cluster
3. Deploying Applications on Kubernetes
4. Kubernetes Networking
5. Storage and Persistence
6. Resource Management and Scaling
7. Security in Kubernetes
8. Monitoring and Logging
9. Continuous Integration/Continuous Deployment (CI/CD) with Kubernetes
10. Advanced Kubernetes Concepts
---
## Learning Resources

* Official Kubernetes Documentation: kubernetes.io
* Kubernetes: Up and Running (Book) by Kelsey Hightower, Brendan Burns, and Joe Beda
* Kubernetes the Hard Way by Kelsey Hightower
* CNCF Kubernetes Certification (CKA, CKAD)
