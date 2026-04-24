---
tags:
  - concepts:architecture
  - infrastructure:kubernetes
  - infrastructure:containers
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Orchestration with Kubernetes

---
## What Is Container Orchestration?

- Automated management of containerized applications at scale
- Handles deployment, scaling, networking, and availability
- Ensures the desired state of the system matches reality
- Required when running dozens or hundreds of containers

---
## Why Kubernetes?

- Open-source, originally developed by Google
- De facto standard for container orchestration
- Runs on any cloud provider and on-premises
- Backed by the `Cloud Native Computing Foundation` (`CNCF`)
- Massive ecosystem of tools and extensions

---
## Kubernetes Architecture

![kubernetes_architecture](svg/courses/architecting/modern-software-architecture/10_orchestration_with_kubernetes/kubernetes_architecture.svg)

---
## K8s Architecture

![k8s_architecture](svg/courses/architecting/modern-software-architecture/10_orchestration_with_kubernetes/k8s_architecture.svg)

---
## Control Plane Components

- `API Server` - the front door to the cluster, handles all REST requests
- `etcd` - distributed key-value store that holds all cluster state
- `Scheduler` - assigns pods to nodes based on resource requirements
- `Controller Manager` - runs control loops that reconcile desired vs actual state

---
## Worker Node Components

- `kubelet` - agent running on each node that manages pods
- `kube-proxy` - maintains network rules for pod communication
- Container Runtime - runs the actual containers (`containerd`, `CRI-O`)
- Each node reports its status to the control plane

---
## Pods

- The smallest deployable unit in Kubernetes
- Contains one or more tightly coupled containers
- Containers in a pod share the same network namespace and storage
- Pods are ephemeral and can be replaced at any time

---
## Pod Definition

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
  labels:
    app: web
spec:
  containers:
    - name: web
      image: myapp:1.0
      ports:
        - containerPort: 8080
      resources:
        requests:
          memory: "128Mi"
          cpu: "250m"
        limits:
          memory: "256Mi"
          cpu: "500m"
```

---
## Multi-Container Pod Patterns

![multi_container_pod_patterns](svg/courses/architecting/modern-software-architecture/10_orchestration_with_kubernetes/multi_container_pod_patterns.svg)

---
## Sidecar Pattern

- A helper container that runs alongside the main container
- Shares the same network and storage as the main container
- Common uses: log shipping, monitoring agents, proxies
- The main container does not need to know about the sidecar

---
## Deployments

- Manages the lifecycle of a set of identical pods
- Defines the desired number of replicas
- Handles rolling updates and rollbacks
- The standard way to run stateless applications

---
## Deployment Definition

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
          image: myapp:1.0
          ports:
            - containerPort: 8080
```

---
## Rolling Update Strategy

![rolling_update_strategy](svg/courses/architecting/modern-software-architecture/10_orchestration_with_kubernetes/rolling_update_strategy.svg)

---
## Deployment Update Configuration

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

- `maxSurge` - how many extra pods can exist during update
- `maxUnavailable` - how many pods can be unavailable during update
- Setting `maxUnavailable: 0` ensures zero downtime

---
## ReplicaSets

- Ensures a specified number of pod replicas are running
- Created and managed automatically by Deployments
- Rarely created directly; use Deployments instead
- Provides self-healing by replacing failed pods

---
## Services

- A stable network endpoint that exposes a set of pods
- Pods are selected by labels
- Provides load balancing across matching pods
- The IP address of a Service remains constant even as pods come and go

---
## Service Types

| Type | Description |
|------|-------------|
| `ClusterIP` | Internal-only IP, default type |
| `NodePort` | Exposes on each node's IP at a static port |
| `LoadBalancer` | Provisions an external load balancer |
| `ExternalName` | Maps to a DNS name |

---
## ClusterIP Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

- Accessible only within the cluster
- Other pods reach it via `web-service.default.svc.cluster.local`

---
## Service Networking Diagram

![service_networking_diagram](svg/courses/architecting/modern-software-architecture/10_orchestration_with_kubernetes/service_networking_diagram.svg)

---
## Ingress

- Manages external HTTP/HTTPS access to services in the cluster
- Provides URL routing, SSL termination, and name-based virtual hosting
- Requires an Ingress Controller (e.g., `NGINX`, `Traefik`, `HAProxy`)
- More flexible than `LoadBalancer` services

---
## Ingress Definition

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

---
## ConfigMaps

- Store non-sensitive configuration data as key-value pairs
- Decouple configuration from container images
- Can be mounted as files or exposed as environment variables
- Changes can be applied without rebuilding images

---
## ConfigMap Definition

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
  config.yaml: |
    database:
      pool_size: 10
      timeout: 30s
```

---
## Using ConfigMaps in Pods

```yaml
spec:
  containers:
    - name: web
      image: myapp:1.0
      envFrom:
        - configMapRef:
            name: app-config
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: app-config
```

---
## Secrets

- Store sensitive data such as passwords, tokens, and certificates
- Base64 encoded by default (not encrypted at rest without extra configuration)
- Should be encrypted at rest using `EncryptionConfiguration` or a KMS provider
- Mounted as files or environment variables, similar to ConfigMaps

---
## Secret Definition

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  username: YWRtaW4=
  password: cGFzc3dvcmQxMjM=
```

- Values are base64 encoded
- Use `kubectl create secret` to avoid manual encoding

---
## Secrets Best Practices

- Enable encryption at rest in `etcd`
- Use external secret managers (`Vault`, `AWS Secrets Manager`)
- Tools like `External Secrets Operator` sync external secrets into Kubernetes
- Limit RBAC access to secrets to only the pods that need them
- Rotate secrets regularly and automate the process

---
## Namespaces

- Virtual clusters within a physical cluster
- Provide isolation for teams, environments, or applications
- Resource quotas can be applied per namespace
- Default namespaces: `default`, `kube-system`, `kube-public`

---
## Health Checks: Liveness Probes

- Determines if a container is running and healthy
- If the liveness probe fails, Kubernetes restarts the container
- Catches situations where the process is alive but unresponsive
- Types: HTTP, TCP, and command-based probes

---
## Liveness Probe Example

```yaml
spec:
  containers:
    - name: web
      image: myapp:1.0
      livenessProbe:
        httpGet:
          path: /healthz
          port: 8080
        initialDelaySeconds: 15
        periodSeconds: 10
        failureThreshold: 3
```

---
## Health Checks: Readiness Probes

- Determines if a container is ready to accept traffic
- If the readiness probe fails, the pod is removed from service endpoints
- The container is not restarted, just removed from load balancing
- Used during startup and when dependencies are temporarily unavailable

---
## Readiness Probe Example

```yaml
spec:
  containers:
    - name: web
      image: myapp:1.0
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5
        failureThreshold: 3
```

---
## Startup Probes

- Used for containers that take a long time to start
- Disables liveness and readiness probes until the startup probe succeeds
- Prevents Kubernetes from killing slow-starting containers
- Only runs during the initial startup phase

---
## Self-Healing Mechanisms

![self_healing_mechanisms](svg/courses/architecting/modern-software-architecture/10_orchestration_with_kubernetes/self_healing_mechanisms.svg)

---
## Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

---
## Resource Management

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "250m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

- `requests` - guaranteed resources for scheduling
- `limits` - maximum resources the container can use
- Pod is evicted if it exceeds memory limits
- Pod is throttled if it exceeds CPU limits

---
## Summary

- Kubernetes automates deployment, scaling, and management of containers
- Pods are the basic unit; Deployments manage their lifecycle
- Services provide stable networking for dynamic pods
- ConfigMaps and Secrets externalize configuration and sensitive data
- Liveness, readiness, and startup probes enable self-healing
- HPA automatically scales based on metrics
- Proper resource management prevents noisy-neighbor problems
