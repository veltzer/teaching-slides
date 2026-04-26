---
tags:
  - concepts:architecture
  - infrastructure:kubernetes
  - infrastructure:containers
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Practical Application With Containers and Kubernetes

---
## Why This Chapter

- Kubernetes wasn't around when twelve-factor was written
- But every factor maps onto Kubernetes primitives
- Understanding the mapping makes the factors concrete
- And makes Kubernetes deployment straightforward

---
## Factor I: Codebase

- One codebase → one container image
- Image versioning = release tagging
- Many deploys = many running pods of that image
- Helm chart or Kustomize tracks the deployment configuration

---
## Factor II: Dependencies

- The Dockerfile declares OS and runtime dependencies
- The application's package manager (pip, npm, etc.) declares app dependencies
- The image is the lock — once built, it's frozen
- Multi-stage builds keep the image small and explicit

---
## Factor III: Config

- ConfigMap for non-sensitive config
- Secret for sensitive values
- Both injected as environment variables (or mounted files)
- Per-environment ConfigMap/Secret = per-environment deploy

---
## Factor IV: Backing Services

- Service objects abstract internal services (DNS-based)
- ExternalName services for cloud-managed databases
- Connection strings come from ConfigMap/Secret
- The pod doesn't know if Postgres is in-cluster or in RDS

---
## Factor V: Build, Release, Run

- Build: CI builds the image, pushes to a registry
- Release: a Deployment manifest with the image tag plus ConfigMap/Secret
- Run: kubectl apply, the Deployment creates pods
- Rollback: change the image tag, apply again

---
## Factor VI: Processes

- Each pod is a stateless process
- StatefulSet exists, but most workloads use Deployment
- Pods are ephemeral; storage goes to PersistentVolume (a backing service)
- A pod dying is not a problem; the Deployment replaces it

---
## Factor VII: Port Binding

- The container listens on a port (declared in the Dockerfile)
- A Service object exposes the port to other pods
- An Ingress exposes it to the outside world
- The app reads `$PORT` from the container's env

---
## Factor VIII: Concurrency

- A Deployment has a `replicas` field — that's the process count
- Different process types = different Deployments
- HPA (Horizontal Pod Autoscaler) auto-scales based on CPU/memory/custom metrics
- Each Deployment scales independently

---
## Factor IX: Disposability

- Liveness probe: is the pod still alive? (restart if not)
- Readiness probe: is the pod ready to serve? (don't route traffic until ready)
- `terminationGracePeriodSeconds`: how long to drain before SIGKILL
- preStop hook: cleanup actions before SIGTERM

---
## Probe Configuration Sketch

```yaml
livenessProbe:
  httpGet: { path: /healthz, port: 8080 }
  initialDelaySeconds: 10
  periodSeconds: 10
readinessProbe:
  httpGet: { path: /ready, port: 8080 }
  periodSeconds: 5
terminationGracePeriodSeconds: 30
```

- Tunable per service
- Operators see "not ready" pods removed from the load balancer

---
## Factor X: Dev/Prod Parity

- Same image in dev, staging, prod
- Local kind/minikube clusters mirror prod topology
- docker-compose for backing services in dev
- Helm value files differ per environment, not the image

---
## Factor XI: Logs

- The app writes to stdout
- The container runtime captures stdout
- A DaemonSet (Fluent Bit, Promtail) ships logs to an aggregator
- The app does nothing log-management-related

---
## Factor XII: Admin Processes

- Kubernetes Job runs a one-off task
- Same image as the app, different command
- For migrations: a Job runs before the Deployment rolls out
- Cron tasks: CronJob (also a one-off, on a schedule)

---
## A Migration Job Sketch

```yaml
apiVersion: batch/v1
kind: Job
metadata: { name: migrate-app }
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: registry/app:v123
        command: ["python", "manage.py", "migrate"]
        envFrom:
        - configMapRef: { name: app-config }
        - secretRef: { name: app-secrets }
      restartPolicy: OnFailure
```

- Same image, same config, different command — that's factor XII

---
## Putting It Together: A Twelve-Factor App in Kubernetes

- A Deployment for `web`, with HPA, probes, and a Service
- A Deployment for `worker`, scaled by queue depth
- A CronJob for scheduled tasks
- ConfigMap + Secret for config
- Persistent backing services (Postgres, Redis) accessed by URL
- All built from one image; deployed by a Helm chart or Kustomize overlay

---
## What This Chapter Doesn't Cover

- Service mesh, mTLS, network policies — security extensions
- Multi-cluster deployments — beyond the basics
- Operator patterns — for stateful applications
- These build **on** twelve-factor, not against it

---
## Course Recap

- Each factor: a small commitment with a large payoff
- Together: a contract between the app and the platform
- Kubernetes assumes the factors; violating them fights the platform
- Modern extensions (telemetry, security, API-first) build on the foundation

---
## Where to Apply This Tomorrow

- Audit one service against the twelve factors
- Identify the violations
- Pick the cheapest one to fix first
- Repeat
- A team that internalizes the factors ships faster and operates with less drama

---
## Summary

- Every factor maps to Kubernetes primitives cleanly
- The factors aren't Kubernetes-specific, but they fit it perfectly
- Following them makes Kubernetes deployment straightforward
- Violating them makes Kubernetes painful
