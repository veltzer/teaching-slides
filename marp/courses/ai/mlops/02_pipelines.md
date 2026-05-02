---
tags:
  - data-and-ai:machine-learning
  - practices:devops
level: advanced
category: machine-learning
audience:
  - audiences:data-scientists
  - audiences:devops

---
# ML Pipelines

---
## What This Chapter Covers

- Why pipelines
- Pipeline shape
- Orchestrators
- Data and feature pipelines
- Training pipelines

---
## Why Pipelines

- Reproducible runs
- Recoverable failures
- Auditable history
- Schedulable

---
## Pipeline Anatomy

- Sources
- Tasks
- Dependencies
- Artifacts
- Sinks

---
## DAG Model

- Tasks form a graph
- Edges express dependencies
- Cycles are forbidden
- Failures stop downstream

---
## DAG Visualized

![pipeline_dag](svg/courses/ai/mlops/02_pipelines/pipeline_dag.svg)

---
## Orchestrators

- Airflow: mature, Python, broad
- Kubeflow Pipelines: Kubernetes-native
- Prefect: dynamic flows
- Dagster: typed assets

---
## Data Pipelines

- Ingest from source systems
- Validate schemas
- Normalize and clean
- Land in warehouse or lake

---
## Feature Pipelines

- Transform raw data into features
- Same code for training and serving
- Backfill historical features
- Stream fresh ones online

---
## Training Pipelines

- Pull frozen feature snapshot
- Split train, validation, test
- Train and evaluate
- Register if metrics pass

---
## Inference Pipelines

- Online: low latency, single record
- Batch: throughput, large jobs
- Different infra, same model
- Same preprocessing required

---
## Caching and Idempotency

- Re-run safe
- Skip unchanged tasks
- Hash inputs as cache key
- Saves time and cost

---
## Backfills

- Old data, new pipeline
- Treat as a parameter
- Run in parallel partitions
- Validate before promoting

---
## Failure Handling

- Retries with backoff
- Dead-letter queues
- Alert on stuck pipelines
- Automate the safe recovery

---
## Common Pipeline Mistakes

- Long monolithic tasks
- Hidden state between steps
- No data validation
- Different code for train and serve
- No SLA on freshness
