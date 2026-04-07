# Pods and Health Checks

---

## Pod Overview

1. **Smallest** deployable unit in Kubernetes
1. **One or more** containers
1. **Shared** network and storage
1. **Ephemeral** by design
1. **Unique** IP address

---

## Pod Lifecycle

![pod_lifecycle](/svg/courses/devops/k8s-introduction/06_pods_and_health/pod_lifecycle.svg)

---

## Pod Phases Explained

1. **Pending**: Accepted but not running
1. **Running**: Bound to node, containers created
1. **Succeeded**: All containers terminated successfully
1. **Failed**: At least one container failed
1. **Unknown**: Pod state cannot be determined

---

## Pod Status Conditions

```yaml
status:
  conditions:
  - type: Initialized
    status: "True"
  - type: Ready
    status: "True"
  - type: ContainersReady
    status: "True"
  - type: PodScheduled
    status: "True"
```

---

## Container States

![container_states](/svg/courses/devops/k8s-introduction/06_pods_and_health/container_states.svg)

---

## Restart Policies

```yaml
apiVersion: v1
kind: Pod
spec:
  restartPolicy: Always  # Default
  # Options:
  # Always - Always restart
  # OnFailure - Restart only on failure
  # Never - Never restart
```

---

## Init Containers

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  initContainers:
  - name: init-db
    image: busybox
    command: ['sh', '-c', 'until nc -z db-service 3306; do sleep 1; done']
  - name: init-cache
    image: busybox
    command: ['sh', '-c', 'until nc -z cache-service 6379; do sleep 1; done']
  containers:
  - name: app
    image: myapp:latest
```

---

## Init Container Flow

![init_container_flow](/svg/courses/devops/k8s-introduction/06_pods_and_health/init_container_flow.svg)

---

## Health Checks Overview

1. **Liveness Probe**: Is container running?
1. **Readiness Probe**: Ready to serve traffic?
1. **Startup Probe**: Has application started?

---

## Why Health Checks?

1. **Detect failures** automatically
1. **Restart** unhealthy containers
1. **Remove** from service endpoints
1. **Handle** slow-starting containers
1. **Ensure** high availability

---

## Liveness Probe

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
```

---

## Liveness Probe Types

![liveness_probe_types](/svg/courses/devops/k8s-introduction/06_pods_and_health/liveness_probe_types.svg)

---

## HTTP Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
    httpHeaders:
    - name: Custom-Header
      value: Awesome
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

## TCP Liveness Probe

```yaml
livenessProbe:
  tcpSocket:
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 20
  failureThreshold: 3
  successThreshold: 1
```

---

## Exec Liveness Probe

```yaml
livenessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 1
  failureThreshold: 3
```

---

## Readiness Probe

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 5
      successThreshold: 1
      failureThreshold: 3
```

---

## Readiness vs Liveness

![readiness_vs_liveness](/svg/courses/devops/k8s-introduction/06_pods_and_health/readiness_vs_liveness.svg)

---

## Startup Probe

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    startupProbe:
      httpGet:
        path: /startup
        port: 8080
      periodSeconds: 10
      failureThreshold: 30  # 30 * 10 = 300s max startup time
```

---

## Startup Probe Purpose

1. **Slow-starting** containers
1. **Legacy** applications
1. **Disables** other probes until success
1. **Prevents** premature kills
1. **One-time** check at startup

---

## Probe Configuration Parameters

```yaml
probeConfig:
  initialDelaySeconds: 30  # Delay before first probe
  periodSeconds: 10        # How often to probe
  timeoutSeconds: 5        # Probe timeout
  successThreshold: 1      # Successes to be healthy
  failureThreshold: 3      # Failures to be unhealthy
```

---

## Probe Timeline

![probe_timeline](/svg/courses/devops/k8s-introduction/06_pods_and_health/probe_timeline.svg)

---

## Common Probe Patterns

```yaml
# Database dependency check
readinessProbe:
  exec:
    command:
    - sh
    - -c
    - "pg_isready -U postgres"

# Application warmup check
startupProbe:
  httpGet:
    path: /initialized
    port: 8080
  failureThreshold: 60  # Long startup time
```

---

## Pod Disruption Budgets

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  # OR
  # maxUnavailable: 1
  selector:
    matchLabels:
      app: web
```

---

## PDB Protection

![pdb_protection](/svg/courses/devops/k8s-introduction/06_pods_and_health/pdb_protection.svg)

---

## Pod Priority and Preemption

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false

---
apiVersion: v1
kind: Pod
spec:
  priorityClassName: high-priority
  containers:
  - name: app
    image: myapp
```

---

## Pod Lifecycle Hooks

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "echo Starting > /tmp/message"]
      preStop:
        exec:
          command: ["/bin/sh", "-c", "nginx -s quit; sleep 15"]
```

---

## Hook Execution

![hook_execution](/svg/courses/devops/k8s-introduction/06_pods_and_health/hook_execution.svg)

---

## Container Resources

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "256Mi"
        cpu: "500m"
```

---

## Resource Units

1. **CPU**: Measured in cores
    - `1` = 1 CPU core
    - `1000m` = 1 CPU core
    - `250m` = 0.25 CPU core
1. **Memory**: Measured in bytes
    - `128Mi` = 128 mebibytes
    - `1Gi` = 1 gibibyte

---

## Ephemeral Containers

```bash
# Add debug container to running pod
kubectl debug my-pod -it --image=busybox

# Add debug container with shared namespaces
kubectl debug my-pod -it --image=nicolaka/netshoot \
  --target=app-container

# Create debug pod copy
kubectl debug my-pod -it --image=busybox \
  --copy-to=my-pod-debug
```

---

## Pod Security Context

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: app
    image: myapp
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
```

---

## Pod Scheduling

```yaml
apiVersion: v1
kind: Pod
spec:
  schedulerName: default-scheduler
  nodeSelector:
    disktype: ssd
  tolerations:
  - key: "key1"
    operator: "Equal"
    value: "value1"
    effect: "NoSchedule"
```

---

## Pod Topology Spread

```yaml
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: web
```

---

## Debugging Failed Pods

```bash
# Check pod status
kubectl get pod my-pod -o wide

# Describe pod for events
kubectl describe pod my-pod

# Check logs
kubectl logs my-pod
kubectl logs my-pod --previous

# Check events
kubectl get events --field-selector involvedObject.name=my-pod
```

---

## Common Pod Issues

1. **ImagePullBackOff**: Can't pull image
1. **CrashLoopBackOff**: Container keeps crashing
1. **Pending**: Can't be scheduled
1. **OOMKilled**: Out of memory
1. **Evicted**: Node pressure

---

## Troubleshooting Health Checks

```bash
# Test probe endpoint manually
kubectl exec -it my-pod -- curl localhost:8080/health

# Check probe configuration
kubectl get pod my-pod -o yaml | grep -A 10 livenessProbe

# View probe events
kubectl describe pod my-pod | grep -A 5 "Liveness:"
kubectl describe pod my-pod | grep -A 5 "Readiness:"
```

---

## Health Check Best Practices

1. **Different endpoints** for liveness/readiness
1. **Appropriate timeouts** for your application
1. **Startup probe** for slow-starting apps
1. **Simple checks** that don't consume resources
1. **Avoid cascading** failures

---

## Pod Best Practices

1. **One process** per container
1. **Use init containers** for setup
1. **Set resource** requests and limits
1. **Configure** health checks
1. **Use security** contexts

---

## Summary

1. Pods have defined lifecycle phases
1. Health checks ensure reliability
1. Liveness restarts unhealthy containers
1. Readiness controls traffic routing
1. Proper configuration prevents issues
