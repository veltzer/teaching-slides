---
tags:
  - infrastructure:kubernetes
level: intermediate
category: containers
audience:
  - audiences:developers

---
# ReplicaSets and Deployments

---
## What This Chapter Covers

- ReplicaSet
- Deployment
- Rolling updates
- Rollback
- Scaling
- StatefulSet briefly

---
## Deployment Hierarchy

![deployment_hierarchy](svg/courses/containers/kubernetes/03_replicasets_and_deployments/deployment_hierarchy.svg)

---
## ReplicaSet

- Ensures N pod replicas running
- If pod dies: spawn another
- You rarely use directly
- Behind the scenes of Deployment

---
## Deployment

- Manages a ReplicaSet
- Rolling updates
- Rollback history
- The default way to run stateless apps

---
## Sample Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
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
        image: nginx:1.27
```

---
## Rolling Update

- Default strategy
- Replace pods one at a time
- maxSurge, maxUnavailable
- Zero-downtime deploys (mostly)

---
## maxSurge / maxUnavailable

- maxSurge: extra pods during update (default 25%)
- maxUnavailable: pods that can be down (default 25%)
- Tune for your latency / capacity needs

---
## Recreate Strategy

- Stop all old; start new
- Downtime; simpler
- For apps that can't run two versions concurrently

---
## Strategy Compared

![rollout_strategies](svg/courses/containers/kubernetes/03_replicasets_and_deployments/rollout_strategies.svg)

---
## Rollback

- `kubectl rollout undo deployment/web`
- Reverts to previous ReplicaSet
- History limit configurable
- Standard practice

---
## Scaling

```bash
kubectl scale deployment/web --replicas=5
```

- Manual scale
- Or: HorizontalPodAutoscaler (HPA)
- Based on CPU / memory / custom metrics

---
## HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web
spec:
  scaleTargetRef:
    name: web
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---
## VPA (Vertical Pod Autoscaler)

- Adjusts resource requests / limits
- Based on actual usage
- Less commonly used
- Conflicts with HPA on same metric

---
## StatefulSet

- For stateful apps (DBs, message queues)
- Stable network identity
- Stable storage
- Ordered deployment / scaling
- Different from Deployment

---
## DaemonSet

- One pod per node
- For: node agents (logging, monitoring)
- Auto-deployed to new nodes

---
## Job / CronJob

- Run-once or scheduled work
- "Run this tomorrow at 2am"
- Different shape from long-running services

---
## Common Deployment Mistakes

- No rolling update strategy specified
- Replica count of 1 (no HA during deploy)
- No resource requests (HPA can't decide)
- Forgetting to retain history (can't rollback far)
- Mixing labels; selector matches wrong pods
