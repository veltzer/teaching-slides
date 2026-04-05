# `DaemonSets`, `Jobs`, and `CronJobs`

Advanced Kubernetes Course - Day 2, Module 4

---

## Module Overview

- `DaemonSets` for node-level workloads
- `Jobs` for batch processing
- `CronJobs` for scheduled tasks
- Patterns and best practices
- Indexed jobs and job queues

---

## `DaemonSets` - One Pod Per Node

```text
┌─── Node 1 ───┐  ┌─── Node 2 ───┐  ┌─── Node 3 ───┐
│ ┌──────────┐  │  │ ┌──────────┐  │  │ ┌──────────┐  │
│ │ App Pods │  │  │ │ App Pods │  │  │ │ App Pods │  │
│ └──────────┘  │  │ └──────────┘  │  │ └──────────┘  │
│               │  │               │  │               │
│ ┌──────────┐  │  │ ┌──────────┐  │  │ ┌──────────┐  │
│ │DaemonSet │  │  │ │DaemonSet │  │  │ │DaemonSet │  │
│ │  Pod     │  │  │ │  Pod     │  │  │ │  Pod     │  │
│ └──────────┘  │  │ └──────────┘  │  │ └──────────┘  │
└───────────────┘  └───────────────┘  └───────────────┘

Exactly one DaemonSet pod per node.
New node added → DaemonSet pod auto-created.
```

---

## `DaemonSet` Specification

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentbit
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentbit
  template:
    metadata:
      labels:
        app: fluentbit
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      containers:
      - name: fluentbit
        image: fluent/fluent-bit:3.0
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
          readOnly: true
        - name: containers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: containers
        hostPath:
          path: /var/lib/docker/containers
```

---

## `DaemonSet` Use Cases

| Use Case | Example |
|----------|---------|
| Log collection | `Fluent Bit`, `Filebeat`, `Fluentd` |
| Monitoring agent | `Prometheus` Node Exporter, `Datadog` Agent |
| Network plugin | `Calico`, `Cilium`, `Weave` |
| Storage plugin | `CSI` node drivers |
| Security agent | `Falco`, `Twistlock` |
| Service mesh proxy | `Envoy` (in some configs) |

---

## `DaemonSet` Update Strategies

**RollingUpdate** (default):
```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 0
```

**OnDelete** (manual control):
```yaml
spec:
  updateStrategy:
    type: OnDelete
```

```bash
# Check rollout status
kubectl rollout status daemonset fluentbit -n logging

# View rollout history
kubectl rollout history daemonset fluentbit -n logging
```

---

## Targeting Specific Nodes

```yaml
spec:
  template:
    spec:
      nodeSelector:
        node-type: gpu
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/os
                operator: In
                values: [linux]
              - key: gpu-type
                operator: In
                values: [nvidia-a100, nvidia-v100]
```

This `DaemonSet` only runs on Linux GPU nodes.

---

## `Jobs` - Run to Completion

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration
spec:
  backoffLimit: 3
  activeDeadlineSeconds: 3600
  ttlSecondsAfterFinished: 86400
  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - name: migrate
        image: myapp/migrate:v2
        command: ["python", "migrate.py"]
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
```

---

## Parallel `Jobs`

**Fixed completion count:**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: render-frames
spec:
  completions: 100
  parallelism: 10
  completionMode: Indexed
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: render
        image: blender:latest
        command:
        - /bin/sh
        - -c
        - |
          FRAME=$JOB_COMPLETION_INDEX
          blender -b scene.blend -f $FRAME \
            -o /output/frame_
        env:
        - name: JOB_COMPLETION_INDEX
          valueFrom:
            fieldRef:
              fieldPath: metadata.annotations['batch.kubernetes.io/job-completion-index']
```

---

## `Job` Patterns

```text
Non-parallel Job (completions=1, parallelism=1):
┌──────┐
│Task 1│ → Done
└──────┘

Parallel with fixed completions (completions=6, parallelism=3):
┌──────┐ ┌──────┐ ┌──────┐
│Task 1│ │Task 2│ │Task 3│ → wave 1
└──────┘ └──────┘ └──────┘
┌──────┐ ┌──────┐ ┌──────┐
│Task 4│ │Task 5│ │Task 6│ → wave 2
└──────┘ └──────┘ └──────┘

Work queue (completions=null, parallelism=5):
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ W-1  │ │ W-2  │ │ W-3  │ │ W-4  │ │ W-5  │
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘
   │        │        │        │        │
   └────────┴────────┼────────┴────────┘
                     │
              ┌──────┴──────┐
              │ Work Queue  │
              │ (external)  │
              └─────────────┘
```

---

## `Job` Configuration Options

| Field | Description | Default |
|-------|-------------|---------|
| `completions` | Number of completions needed | 1 |
| `parallelism` | Max parallel pods | 1 |
| `backoffLimit` | Retries before marking failed | 6 |
| `activeDeadlineSeconds` | Max total runtime | none |
| `ttlSecondsAfterFinished` | Cleanup after completion | none |
| `completionMode` | `NonIndexed` or `Indexed` | `NonIndexed` |
| `suspend` | Pause/resume job | false |

---

## `CronJobs`

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: production
spec:
  schedule: "0 2 * * *"
  timeZone: "America/New_York"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  startingDeadlineSeconds: 300
  jobTemplate:
    spec:
      backoffLimit: 2
      activeDeadlineSeconds: 1800
      template:
        spec:
          restartPolicy: OnFailure
          serviceAccountName: backup-sa
          containers:
          - name: backup
            image: postgres:16
            command:
            - /bin/sh
            - -c
            - |
              TIMESTAMP=$(date +%Y%m%d_%H%M%S)
              pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | \
                gzip > /backup/db_${TIMESTAMP}.sql.gz
              aws s3 cp /backup/db_${TIMESTAMP}.sql.gz \
                s3://backups/postgres/
            envFrom:
            - secretRef:
                name: db-credentials
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            emptyDir:
              sizeLimit: 10Gi
```

---

## `CronJob` Schedule Syntax

```text
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6, Sun=0)
│ │ │ │ │
* * * * *

Examples:
"0 * * * *"      Every hour
"*/15 * * * *"   Every 15 minutes
"0 2 * * *"      Daily at 2 AM
"0 0 * * 0"      Weekly on Sunday
"0 0 1 * *"      Monthly on the 1st
"0 0 1 1 *"      Yearly on Jan 1
```

---

## Concurrency Policies

| Policy | Behavior |
|--------|----------|
| `Allow` | Multiple jobs can run simultaneously |
| `Forbid` | Skip new run if previous still running |
| `Replace` | Cancel running job, start new one |

```yaml
spec:
  concurrencyPolicy: Forbid
```

```bash
# Monitor CronJobs
kubectl get cronjobs
kubectl get jobs --sort-by=.metadata.creationTimestamp

# Manual trigger
kubectl create job --from=cronjob/database-backup manual-backup

# Suspend a CronJob
kubectl patch cronjob database-backup -p '{"spec":{"suspend":true}}'
```

---

## `Job` with Sidecar Pattern

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: etl-pipeline
spec:
  template:
    spec:
      restartPolicy: Never
      initContainers:
      - name: download-data
        image: aws-cli:latest
        command: ['aws', 's3', 'cp',
          's3://data/input.csv', '/data/input.csv']
        volumeMounts:
        - name: data
          mountPath: /data
      containers:
      - name: transform
        image: python:3.12
        command: ['python', '/scripts/transform.py',
          '--input', '/data/input.csv',
          '--output', '/data/output.csv']
        volumeMounts:
        - name: data
          mountPath: /data
        - name: scripts
          mountPath: /scripts
      volumes:
      - name: data
        emptyDir: {}
      - name: scripts
        configMap:
          name: etl-scripts
```

---

## Monitoring `Jobs` and `CronJobs`

```bash
# List all jobs
kubectl get jobs -o wide

# Watch job pod status
kubectl get pods -l job-name=data-migration -w

# View job logs
kubectl logs job/data-migration

# Check CronJob last schedule
kubectl get cronjob database-backup \
  -o jsonpath='{.status.lastScheduleTime}'

# Alert on failed jobs (PrometheusRule)
```

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: job-alerts
spec:
  groups:
  - name: job.rules
    rules:
    - alert: CronJobFailed
      expr: |
        kube_job_status_failed{
          namespace="production"} > 0
      for: 5m
      labels:
        severity: warning
```

---

## Lab: Batch Processing Pipeline

```bash
# 1. Create a DaemonSet for log collection
kubectl apply -f fluentbit-daemonset.yaml

# 2. Create a parallel Job
kubectl apply -f parallel-job.yaml
kubectl get pods -l job-name=parallel-job -w

# 3. Create a CronJob for backups
kubectl apply -f backup-cronjob.yaml

# 4. Manually trigger the CronJob
kubectl create job --from=cronjob/backup manual-test

# 5. Check results
kubectl get jobs
kubectl logs job/manual-test
```
