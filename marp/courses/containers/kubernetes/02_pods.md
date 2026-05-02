---
tags:
  - infrastructure:kubernetes
level: intermediate
category: containers
audience:
  - audiences:developers

---
# Pods

---
## What This Chapter Covers

- The pod abstraction
- Single vs multi-container
- Pod lifecycle
- Resource requests / limits
- Probes
- Init containers

---
## Pod Anatomy

![pod_anatomy](svg/courses/containers/kubernetes/02_pods/pod_anatomy.svg)

---
## What A Pod Is

- One or more containers; shared network and storage
- Smallest scheduled unit in K8s
- Ephemeral
- "Like a logical host"

---
## Single-Container Pod

- 99% of pods
- One app per pod
- Replicated via Deployment

---
## Multi-Container Pod

- Sidecar pattern: app + helper
- Examples: log shipper, proxy, init
- Share localhost network
- Less common; specific use cases

---
## A Simple Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.27
    ports:
    - containerPort: 80
```

---
## Pod Lifecycle

- Pending: scheduled but not started
- Running: at least one container running
- Succeeded: all containers exited 0
- Failed: at least one exited non-zero
- Unknown: lost contact

---
## Resource Requests

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

- Requests: what's reserved
- Limits: max
- Scheduling uses requests

---
## Liveness Probe

- "Is the container alive?"
- HTTP, TCP, or exec
- Failed: kill and restart
- For: detecting deadlocks, hangs

---
## Readiness Probe

- "Is the container ready to serve?"
- Failed: removed from service endpoints
- For: warm-up, dependency checks

---
## Startup Probe

- "Has it finished starting?"
- For slow-start apps (Java)
- Disables liveness during startup
- Avoids: false-positive kills

---
## Init Containers

- Run before main containers
- Setup tasks
- Each must complete before next starts
- Then main containers run

---
## Restart Policy

- Always (default)
- OnFailure
- Never
- Affects pod-level behaviour

---
## Pod Anti-Affinity

- Spread pods across nodes
- "Don't put all replicas on one node"
- For HA

---
## Common Pod Mistakes

- No resource requests (scheduler can't plan)
- No liveness probe (hangs forever)
- Same liveness and readiness (defeats purpose)
- Privileged containers (security risk)
- Cramming many processes into one container
