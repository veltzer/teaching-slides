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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Pod Lifecycle Phases</text>
  <circle cx="150" cy="200" r="40" fill="#888"/>
  <text x="150" y="205" text-anchor="middle" fill="white">Pending</text>
  <circle cx="300" cy="200" r="40" fill="#4285f4"/>
  <text x="300" y="205" text-anchor="middle" fill="white">Running</text>
  <circle cx="450" cy="200" r="40" fill="#34a853"/>
  <text x="450" y="205" text-anchor="middle" fill="white">Succeeded</text>
  <circle cx="600" cy="200" r="40" fill="#ea4335"/>
  <text x="600" y="205" text-anchor="middle" fill="white">Failed</text>
  <circle cx="375" cy="320" r="40" fill="#fbbc04"/>
  <text x="375" y="325" text-anchor="middle">Unknown</text>
  <path d="M 190 200 L 260 200" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 340 200 L 410 200" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 340 200 L 560 200" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 300 240 L 375 280" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="225" y="190" text-anchor="middle" font-size="10">Scheduled</text>
  <text x="375" y="190" text-anchor="middle" font-size="10">Complete</text>
  <text x="450" y="190" text-anchor="middle" font-size="10">Error</text>
  <text x="320" y="265" text-anchor="middle" font-size="10">Lost</text>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Container States</text>
  <rect x="100" y="100" width="200" height="120" fill="#4285f4" rx="5"/>
  <text x="200" y="130" text-anchor="middle" fill="white" font-weight="bold">Waiting</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">Not yet running</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">Pulling image</text>
  <text x="200" y="195" text-anchor="middle" fill="white" font-size="11">Creating container</text>
  <rect x="320" y="100" width="200" height="120" fill="#34a853" rx="5"/>
  <text x="420" y="130" text-anchor="middle" fill="white" font-weight="bold">Running</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">Executing normally</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">Started at: timestamp</text>
  <text x="420" y="195" text-anchor="middle" fill="white" font-size="11">Process active</text>
  <rect x="540" y="100" width="200" height="120" fill="#ea4335" rx="5"/>
  <text x="640" y="130" text-anchor="middle" fill="white" font-weight="bold">Terminated</text>
  <text x="640" y="155" text-anchor="middle" fill="white" font-size="11">Execution completed</text>
  <text x="640" y="175" text-anchor="middle" fill="white" font-size="11">Exit code: 0 or error</text>
  <text x="640" y="195" text-anchor="middle" fill="white" font-size="11">Reason: OOMKilled, Error</text>
  <path d="M 300 160 L 315 160" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 520 160 L 535 160" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 640 220 Q 420 260 200 220" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="420" y="255" text-anchor="middle" font-size="10">Restart Policy</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Init Container Execution</text>
  <rect x="50" y="80" width="120" height="60" fill="#888" rx="5"/>
  <text x="110" y="115" text-anchor="middle" fill="white">Pod Created</text>
  <rect x="200" y="80" width="120" height="60" fill="#4285f4" rx="5"/>
  <text x="260" y="105" text-anchor="middle" fill="white" font-size="11">Init Container 1</text>
  <text x="260" y="125" text-anchor="middle" fill="white" font-size="10">Check DB</text>
  <rect x="350" y="80" width="120" height="60" fill="#4285f4" rx="5"/>
  <text x="410" y="105" text-anchor="middle" fill="white" font-size="11">Init Container 2</text>
  <text x="410" y="125" text-anchor="middle" fill="white" font-size="10">Setup Config</text>
  <rect x="500" y="80" width="120" height="60" fill="#4285f4" rx="5"/>
  <text x="560" y="105" text-anchor="middle" fill="white" font-size="11">Init Container 3</text>
  <text x="560" y="125" text-anchor="middle" fill="white" font-size="10">Load Data</text>
  <rect x="650" y="80" width="120" height="60" fill="#34a853" rx="5"/>
  <text x="710" y="105" text-anchor="middle" fill="white">Main Container</text>
  <text x="710" y="125" text-anchor="middle" fill="white" font-size="10">App Running</text>
  <path d="M 170 110 L 195 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 320 110 L 345 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 470 110 L 495 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 620 110 L 645 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="200" y="180" width="400" height="80" fill="#fff3e0" rx="5"/>
  <text x="400" y="205" text-anchor="middle" font-weight="bold">Sequential Execution</text>
  <text x="400" y="225" text-anchor="middle" font-size="12">• Each init container must complete successfully</text>
  <text x="400" y="245" text-anchor="middle" font-size="12">• Main containers start only after all init containers finish</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Liveness Probe Types</text>
  <rect x="100" y="80" width="200" height="120" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">HTTP GET</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">GET request to path</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">200-399 = healthy</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">Other = unhealthy</text>
  <rect x="320" y="80" width="200" height="120" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">TCP Socket</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="11">TCP connection</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">Connect = healthy</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">Fail = unhealthy</text>
  <rect x="540" y="80" width="200" height="120" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">Exec Command</text>
  <text x="640" y="135" text-anchor="middle" font-size="11">Run command in container</text>
  <text x="640" y="155" text-anchor="middle" font-size="11">Exit 0 = healthy</text>
  <text x="640" y="175" text-anchor="middle" font-size="11">Non-zero = unhealthy</text>
  <rect x="200" y="230" width="400" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="255" text-anchor="middle" font-weight="bold">Action on Failure</text>
  <text x="400" y="280" text-anchor="middle" font-size="12">Container is killed and restarted based on restart policy</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Readiness vs Liveness Probes</text>
  <rect x="100" y="80" width="300" height="120" fill="#4285f4" rx="5"/>
  <text x="250" y="110" text-anchor="middle" fill="white" font-weight="bold">Readiness Probe</text>
  <text x="250" y="135" text-anchor="middle" fill="white" font-size="11">• Removes from service endpoints</text>
  <text x="250" y="155" text-anchor="middle" fill="white" font-size="11">• Traffic stops routing to pod</text>
  <text x="250" y="175" text-anchor="middle" fill="white" font-size="11">• Container keeps running</text>
  <rect x="420" y="80" width="300" height="120" fill="#34a853" rx="5"/>
  <text x="570" y="110" text-anchor="middle" fill="white" font-weight="bold">Liveness Probe</text>
  <text x="570" y="135" text-anchor="middle" fill="white" font-size="11">• Restarts container</text>
  <text x="570" y="155" text-anchor="middle" fill="white" font-size="11">• Kills unhealthy container</text>
  <text x="570" y="175" text-anchor="middle" fill="white" font-size="11">• Based on restart policy</text>
  <rect x="100" y="230" width="620" height="80" fill="#fff3e0" rx="5"/>
  <text x="410" y="255" text-anchor="middle" font-weight="bold">Best Practice</text>
  <text x="410" y="275" text-anchor="middle" font-size="12">Use both probes with different endpoints</text>
  <text x="410" y="295" text-anchor="middle" font-size="12">Readiness: /ready (dependencies check) | Liveness: /health (app health)</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Probe Execution Timeline</text>
  <line x1="100" y1="100" x2="700" y2="100" stroke="#333" stroke-width="2"/>
  <text x="100" y="90" text-anchor="start" font-size="12">Container Start</text>
  <circle cx="100" cy="100" r="5" fill="#333"/>
  <rect x="100" y="120" width="150" height="40" fill="#888" rx="3"/>
  <text x="175" y="145" text-anchor="middle" fill="white" font-size="11">Initial Delay (30s)</text>
  <circle cx="250" cy="100" r="5" fill="#4285f4"/>
  <text x="250" y="85" text-anchor="middle" font-size="10">Probe 1</text>
  <rect x="250" y="120" width="60" height="30" fill="#4285f4" rx="3"/>
  <text x="280" y="140" text-anchor="middle" fill="white" font-size="10">Period</text>
  <circle cx="310" cy="100" r="5" fill="#4285f4"/>
  <text x="310" y="85" text-anchor="middle" font-size="10">Probe 2</text>
  <rect x="310" y="120" width="60" height="30" fill="#4285f4" rx="3"/>
  <text x="340" y="140" text-anchor="middle" fill="white" font-size="10">Period</text>
  <circle cx="370" cy="100" r="5" fill="#ea4335"/>
  <text x="370" y="85" text-anchor="middle" font-size="10">Fail 1</text>
  <circle cx="430" cy="100" r="5" fill="#ea4335"/>
  <text x="430" y="85" text-anchor="middle" font-size="10">Fail 2</text>
  <circle cx="490" cy="100" r="5" fill="#ea4335"/>
  <text x="490" y="85" text-anchor="middle" font-size="10">Fail 3</text>
  <rect x="490" y="120" width="100" height="40" fill="#ea4335" rx="3"/>
  <text x="540" y="145" text-anchor="middle" fill="white" font-size="11">Action Taken</text>
  <text x="400" y="200" text-anchor="middle" font-size="12">Timeline: Initial Delay → Periodic Checks → Failure Threshold → Action</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Pod Disruption Budget</text>
  <rect x="100" y="80" width="600" height="60" fill="#e8f5e9" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-weight="bold">Current State: 5 Pods Running</text>
  <text x="400" y="125" text-anchor="middle" font-size="12">PDB: minAvailable = 3</text>
  <circle cx="200" cy="200" r="30" fill="#34a853"/>
  <text x="200" y="205" text-anchor="middle" fill="white">Pod 1</text>
  <circle cx="300" cy="200" r="30" fill="#34a853"/>
  <text x="300" y="205" text-anchor="middle" fill="white">Pod 2</text>
  <circle cx="400" cy="200" r="30" fill="#34a853"/>
  <text x="400" y="205" text-anchor="middle" fill="white">Pod 3</text>
  <circle cx="500" cy="200" r="30" fill="#34a853"/>
  <text x="500" y="205" text-anchor="middle" fill="white">Pod 4</text>
  <circle cx="600" cy="200" r="30" fill="#34a853"/>
  <text x="600" y="205" text-anchor="middle" fill="white">Pod 5</text>
  <rect x="250" y="260" width="300" height="60" fill="#fff3e0" rx="5"/>
  <text x="400" y="285" text-anchor="middle" font-weight="bold">Voluntary Disruption</text>
  <text x="400" y="305" text-anchor="middle" font-size="12">Max 2 pods can be evicted (5 - 3 = 2)</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Lifecycle Hook Timing</text>
  <rect x="100" y="80" width="150" height="60" fill="#888" rx="5"/>
  <text x="175" y="115" text-anchor="middle" fill="white">Container Created</text>
  <rect x="280" y="80" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="355" y="105" text-anchor="middle" fill="white">PostStart Hook</text>
  <text x="355" y="125" text-anchor="middle" fill="white" font-size="10">Runs immediately</text>
  <rect x="460" y="80" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="535" y="115" text-anchor="middle" fill="white">Container Running</text>
  <rect x="280" y="180" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="355" y="205" text-anchor="middle">PreStop Hook</text>
  <text x="355" y="225" text-anchor="middle" font-size="10">Before termination</text>
  <rect x="460" y="180" width="150" height="60" fill="#ea4335" rx="5"/>
  <text x="535" y="215" text-anchor="middle" fill="white">Container Terminated</text>
  <path d="M 250 110 L 275 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 430 110 L 455 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 535 140 L 355 175" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 430 210 L 455 210" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
</svg>

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
