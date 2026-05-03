---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Orchestration

---
## What This Chapter Covers

- Why orchestration
- DAGs
- Scheduling
- Retries and recovery
- Lineage

---
## Why Orchestration

- Coordinate extract, load, transform
- Dependencies across tasks
- Recoverable failures
- Auditable runs

---
## DAGs

- Tasks form a graph
- Edges express order
- No cycles
- Failure stops downstream

---
## DAG Visualized

![dag_dependencies](svg/courses/data_engineering/etl/04_orchestration/dag_dependencies.svg)

---
## Static vs Dynamic DAGs

- Static: shape known up front
- Dynamic: shape from data
- Dynamic is powerful but harder to test
- Static covers most cases

---
## Scheduling

- Cron for fixed times
- Event-based for arrivals
- Sensors poll for readiness
- Beware sensor backlogs

---
## Orchestrator Choices

![scheduler_choices](svg/courses/data_engineering/etl/04_orchestration/scheduler_choices.svg)

---
## SLAs

- Latest acceptable arrival
- Alert on breach
- Document the cause
- Drive engineering priorities

---
## Retries

- Per-task setting
- Exponential backoff
- Cap to avoid loops
- Idempotency required

---
## Recovery

- Restart from failed task
- Requires per-task state
- Skip already-done tasks
- Or rerun from scratch

---
## Backfills

- Run for past partitions
- Parallelize where independent
- Watch for downstream load
- Track progress

---
## Parameterization

- Date partitions
- Environment
- Source endpoints
- Avoid hardcoded values

---
## Lineage in Orchestrators

- Capture task to dataset
- Visualize dependencies
- Aid impact analysis
- Required for governance

---
## Cost Visibility

- Tag jobs by team or dataset
- Track compute per run
- Find regressions
- Drive optimization

---
## Tooling Options

- Workflow engines: Airflow, Prefect, Dagster
- Cloud-native: Step Functions, Cloud Composer
- Built-in: Databricks Workflows
- Pick by team and stack

---
## Common Orchestration Mistakes

- Long monolithic tasks
- Hidden dependencies
- No SLA
- No retries
- Hardcoded environments
