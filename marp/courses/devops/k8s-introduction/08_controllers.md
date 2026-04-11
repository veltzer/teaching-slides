---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - infrastructure:orchestration
  - practices:devops
  - tools:docker
level: beginner
category: devops
audience:
  - audiences:developers
  - audiences:devops
  - audiences:sysadmins

---
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

![controller_pattern](svg/courses/devops/k8s-introduction/08_controllers/controller_pattern.svg)

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

![rolling_update_process](svg/courses/devops/k8s-introduction/08_controllers/rolling_update_process.svg)

---

## Deployment Rolling Update

![deployment_rollout](svg/courses/devops/k8s-introduction/08_controllers/deployment_rollout.svg)

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

![statefulset_pod_identity](svg/courses/devops/k8s-introduction/08_controllers/statefulset_pod_identity.svg)

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

![job_types](svg/courses/devops/k8s-introduction/08_controllers/job_types.svg)

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

![controller_comparison](svg/courses/devops/k8s-introduction/08_controllers/controller_comparison.svg)

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

![blue_green_deployment](svg/courses/devops/k8s-introduction/08_controllers/blue_green_deployment.svg)

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
