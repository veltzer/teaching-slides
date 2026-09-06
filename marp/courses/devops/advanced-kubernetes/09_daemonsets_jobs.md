---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - practices:devops
  - languages:go
  - concepts:service-mesh
level: advanced
category: devops
audience:
  - audiences:developers

---

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

![daemonsets_one_pod_per_node](svg/courses/devops/advanced-kubernetes/09_daemonsets_jobs/daemonsets_one_pod_per_node.svg)

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
```

---

## `DaemonSet` Specification: Volumes

```yaml
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

![job_patterns](svg/courses/devops/advanced-kubernetes/09_daemonsets_jobs/job_patterns.svg)

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
```

---

## `CronJob` Job Template

```yaml
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

![cronjob_schedule_syntax](svg/courses/devops/advanced-kubernetes/09_daemonsets_jobs/cronjob_schedule_syntax.svg)

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
