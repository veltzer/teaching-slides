# Controllers

---

## Controller Overview

1. **Watch** desired state
1. **Monitor** current state
1. **Reconcile** differences
1. **Continuous** loop
1. **Self-healing** system

---

## Controller Pattern

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Controller Loop</text>
  <rect x="100" y="80" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="175" y="115" text-anchor="middle" fill="white">Observe</text>
  <rect x="325" y="80" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="400" y="115" text-anchor="middle" fill="white">Analyze</text>
  <rect x="550" y="80" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="625" y="115" text-anchor="middle">Act</text>
  <path d="M 250 110 L 320 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 475 110 L 545 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 625 140 Q 400 200 175 140" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="200" y="230" width="400" height="100" fill="#e8f5e9" rx="5"/>
  <text x="400" y="260" text-anchor="middle" font-weight="bold">Reconciliation Loop</text>
  <text x="400" y="285" text-anchor="middle" font-size="12">1. Watch for changes in resources</text>
  <text x="400" y="305" text-anchor="middle" font-size="12">2. Compare desired vs current state</text>
  <text x="400" y="325" text-anchor="middle" font-size="12">3. Take action to match desired state</text>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

---

## Deployment Controller

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
        image: nginx:1.21
        ports:
        - containerPort: 80
```

---

## Deployment Features

1. **Declarative** updates
1. **Rolling** updates
1. **Rollback** capability
1. **Scaling** up/down
1. **Self-healing** pods

---

## Deployment Strategy

```yaml
spec:
  strategy:
    type: RollingUpdate  # or Recreate
    rollingUpdate:
      maxSurge: 1        # Extra pods during update
      maxUnavailable: 1  # Pods that can be down
  revisionHistoryLimit: 10
  progressDeadlineSeconds: 600
```

---

## Rolling Update Process

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Rolling Update Stages</text>
  <g id="stage1">
    <text x="100" y="60" text-anchor="middle" font-size="12">Initial</text>
    <rect x="50" y="80" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="100" y="105" text-anchor="middle" fill="white">v1</text>
    <rect x="50" y="130" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="100" y="155" text-anchor="middle" fill="white">v1</text>
    <rect x="50" y="180" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="100" y="205" text-anchor="middle" fill="white">v1</text>
  </g>
  <g id="stage2">
    <text x="250" y="60" text-anchor="middle" font-size="12">Updating</text>
    <rect x="200" y="80" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="250" y="105" text-anchor="middle" fill="white">v2</text>
    <rect x="200" y="130" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="250" y="155" text-anchor="middle" fill="white">v1</text>
    <rect x="200" y="180" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="250" y="205" text-anchor="middle" fill="white">v1</text>
    <rect x="200" y="230" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="250" y="255" text-anchor="middle" fill="white">v2</text>
  </g>
  <g id="stage3">
    <text x="400" y="60" text-anchor="middle" font-size="12">Progressing</text>
    <rect x="350" y="80" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="400" y="105" text-anchor="middle" fill="white">v2</text>
    <rect x="350" y="130" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="400" y="155" text-anchor="middle" fill="white">v2</text>
    <rect x="350" y="180" width="100" height="40" fill="#4285f4" rx="3"/>
    <text x="400" y="205" text-anchor="middle" fill="white">v1</text>
  </g>
  <g id="stage4">
    <text x="550" y="60" text-anchor="middle" font-size="12">Complete</text>
    <rect x="500" y="80" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="550" y="105" text-anchor="middle" fill="white">v2</text>
    <rect x="500" y="130" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="550" y="155" text-anchor="middle" fill="white">v2</text>
    <rect x="500" y="180" width="100" height="40" fill="#34a853" rx="3"/>
    <text x="550" y="205" text-anchor="middle" fill="white">v2</text>
  </g>
</svg>

---

## ReplicaSet

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicaset
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
        image: nginx:1.21
```

---

## Deployment vs ReplicaSet

1. **Deployment** manages ReplicaSets
1. **ReplicaSet** manages Pods
1. **Deployment** provides updates
1. **ReplicaSet** maintains count
1. **Use** Deployment in practice

---

## StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
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
        image: nginx
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

---

## StatefulSet Features

1. **Stable** network identities
1. **Ordered** deployment
1. **Ordered** scaling
1. **Persistent** storage
1. **Ordered** rolling updates

---

## StatefulSet Pod Identity

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">StatefulSet Pod Names</text>
  <rect x="100" y="100" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="130" text-anchor="middle" fill="white" font-weight="bold">web-0</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="11">First pod</text>
  <text x="175" y="170" text-anchor="middle" fill="white" font-size="11">PVC: www-web-0</text>
  <rect x="275" y="100" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="350" y="130" text-anchor="middle" fill="white" font-weight="bold">web-1</text>
  <text x="350" y="150" text-anchor="middle" fill="white" font-size="11">Second pod</text>
  <text x="350" y="170" text-anchor="middle" fill="white" font-size="11">PVC: www-web-1</text>
  <rect x="450" y="100" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="525" y="130" text-anchor="middle" fill="white" font-weight="bold">web-2</text>
  <text x="525" y="150" text-anchor="middle" fill="white" font-size="11">Third pod</text>
  <text x="525" y="170" text-anchor="middle" fill="white" font-size="11">PVC: www-web-2</text>
  <rect x="625" y="100" width="125" height="80" fill="#888" rx="5"/>
  <text x="687" y="140" text-anchor="middle" fill="white">web-N</text>
  <rect x="200" y="220" width="400" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-weight="bold">Properties</text>
  <text x="400" y="270" text-anchor="middle" font-size="12">• Predictable pod names: $(statefulset)-$(ordinal)</text>
  <text x="400" y="290" text-anchor="middle" font-size="12">• Stable network ID: web-0.nginx.default.svc.cluster.local</text>
</svg>

---

## DaemonSet

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      containers:
      - name: node-exporter
        image: prom/node-exporter
        ports:
        - containerPort: 9100
```

---

## DaemonSet Use Cases

1. **Node monitoring** agents
1. **Log collection** daemons
1. **Storage** daemons
1. **Network** plugins
1. **Security** agents

---

## Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-process
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 4
  template:
    spec:
      containers:
      - name: processor
        image: myapp:process
        command: ["python", "process.py"]
      restartPolicy: Never
```

---

## Job Types

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Job Patterns</text>
  <rect x="100" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Single Job</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">completions: 1</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">parallelism: 1</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">One task</text>
  <rect x="320" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">Parallel Fixed</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="11">completions: 10</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">parallelism: 3</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">Multiple tasks</text>
  <rect x="540" y="80" width="200" height="100" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">Work Queue</text>
  <text x="640" y="135" text-anchor="middle" font-size="11">completions: null</text>
  <text x="640" y="155" text-anchor="middle" font-size="11">parallelism: 3</text>
  <text x="640" y="175" text-anchor="middle" font-size="11">Process queue</text>
</svg>

---

## CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: myapp:backup
            command: ["/bin/sh", "-c", "backup.sh"]
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

---

## Cron Schedule Format

```bash
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6)
# │ │ │ │ │
# * * * * *

Examples:
"0 * * * *"     # Every hour
"*/15 * * * *"  # Every 15 minutes
"0 0 * * 0"     # Weekly on Sunday
"0 0 1 * *"     # Monthly on the 1st
```

---

## Controller Comparison

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Controller Types</text>
  <rect x="80" y="80" width="130" height="250" fill="#4285f4" rx="5"/>
  <text x="145" y="105" text-anchor="middle" fill="white" font-weight="bold">Deployment</text>
  <text x="145" y="125" text-anchor="middle" fill="white" font-size="10">Stateless apps</text>
  <text x="145" y="145" text-anchor="middle" fill="white" font-size="10">Rolling updates</text>
  <rect x="220" y="80" width="130" height="250" fill="#34a853" rx="5"/>
  <text x="285" y="105" text-anchor="middle" fill="white" font-weight="bold">StatefulSet</text>
  <text x="285" y="125" text-anchor="middle" fill="white" font-size="10">Stateful apps</text>
  <text x="285" y="145" text-anchor="middle" fill="white" font-size="10">Ordered</text>
  <rect x="360" y="80" width="130" height="250" fill="#fbbc04" rx="5"/>
  <text x="425" y="105" text-anchor="middle" font-weight="bold">DaemonSet</text>
  <text x="425" y="125" text-anchor="middle" font-size="10">Node agents</text>
  <text x="425" y="145" text-anchor="middle" font-size="10">One per node</text>
  <rect x="500" y="80" width="130" height="250" fill="#ea4335" rx="5"/>
  <text x="565" y="105" text-anchor="middle" fill="white" font-weight="bold">Job</text>
  <text x="565" y="125" text-anchor="middle" fill="white" font-size="10">Batch tasks</text>
  <text x="565" y="145" text-anchor="middle" fill="white" font-size="10">Run to completion</text>
  <rect x="640" y="80" width="110" height="250" fill="#9c27b0" rx="5"/>
  <text x="695" y="105" text-anchor="middle" fill="white" font-weight="bold">CronJob</text>
  <text x="695" y="125" text-anchor="middle" fill="white" font-size="10">Scheduled</text>
  <text x="695" y="145" text-anchor="middle" fill="white" font-size="10">Recurring</text>
</svg>

---

## HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## Scaling Behavior

```yaml
spec:
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

---

## VerticalPodAutoscaler

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  updatePolicy:
    updateMode: "Auto"  # or "Off" or "Initial"
  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: 100m
        memory: 50Mi
      maxAllowed:
        cpu: 1
        memory: 500Mi
```

---

## Managing Controllers

```bash
# Create deployment
kubectl create deployment nginx --image=nginx

# Scale deployment
kubectl scale deployment nginx --replicas=5

# Update image
kubectl set image deployment/nginx nginx=nginx:1.21

# Check rollout status
kubectl rollout status deployment/nginx

# Rollback
kubectl rollout undo deployment/nginx
```

---

## Deployment Strategies

1. **Recreate**: Stop all, then start new
1. **RollingUpdate**: Gradual replacement
1. **Blue/Green**: Switch traffic
1. **Canary**: Gradual traffic shift
1. **A/B Testing**: Split traffic

---

## Blue/Green Deployment

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Blue/Green Deployment</text>
  <rect x="100" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="200" y="120" text-anchor="middle" fill="white" font-weight="bold">Blue (Current)</text>
  <text x="200" y="145" text-anchor="middle" fill="white">Version 1.0</text>
  <text x="200" y="165" text-anchor="middle" fill="white">Active Traffic</text>
  <rect x="350" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="450" y="120" text-anchor="middle" fill="white" font-weight="bold">Green (New)</text>
  <text x="450" y="145" text-anchor="middle" fill="white">Version 2.0</text>
  <text x="450" y="165" text-anchor="middle" fill="white">Testing</text>
  <rect x="600" y="80" width="150" height="100" fill="#fbbc04" rx="5"/>
  <text x="675" y="120" text-anchor="middle" font-weight="bold">Service</text>
  <text x="675" y="145" text-anchor="middle">Selector: blue</text>
  <text x="675" y="165" text-anchor="middle">→ Switch to green</text>
  <path d="M 200 180 L 675 180" stroke="#4285f4" stroke-width="3"/>
  <path d="M 450 180 L 675 220" stroke="#34a853" stroke-width="2" stroke-dasharray="5,5"/>
</svg>

---

## Canary Deployment

```yaml
# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
spec:
  replicas: 1  # 1 out of 10 total
  selector:
    matchLabels:
      app: myapp
      version: canary
---
# Stable deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-stable
spec:
  replicas: 9  # 9 out of 10 total
  selector:
    matchLabels:
      app: myapp
      version: stable
```

---

## Controller Events

```bash
# View deployment events
kubectl describe deployment nginx

# Watch events
kubectl get events --watch

# Filter by object
kubectl get events --field-selector involvedObject.name=nginx

# Check controller logs
kubectl logs -n kube-system deployment/kube-controller-manager
```

---

## Troubleshooting Controllers

1. **Pods not starting**: Check image, resources
1. **Rollout stuck**: Check deployment conditions
1. **Scaling issues**: Check HPA metrics
1. **Job failures**: Check backoffLimit
1. **CronJob not running**: Check schedule, timezone

---

## Best Practices

1. **Use** Deployments for stateless apps
1. **Set** resource requests/limits
1. **Configure** health checks
1. **Use** PodDisruptionBudgets
1. **Test** rollback procedures

---

## Summary

1. Controllers maintain desired state
1. Deployments manage stateless apps
1. StatefulSets for stateful apps
1. DaemonSets run on every node
1. Jobs and CronJobs for batch processing
