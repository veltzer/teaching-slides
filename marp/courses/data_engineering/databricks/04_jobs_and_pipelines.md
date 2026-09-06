---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Jobs and Pipelines

---

## What This Chapter Covers

- Jobs in depth
- Workflows
- Declarative pipelines
- Triggering
- CI/CD

---

## Why Jobs

- Production scheduling
- Retries and alerts
- Tracked history
- Source of truth for runs

---

## Job Anatomy

- Tasks
- Cluster per task
- Dependencies
- Schedule or trigger

---

## Job Anatomy Diagram

![job_anatomy](svg/courses/data_engineering/databricks/04_jobs_and_pipelines/job_anatomy.svg)

---

## Task Types

- Notebook
- Python script
- SQL
- JAR
- Pipeline

---

## Cluster Reuse

- Same cluster across tasks
- Faster startup
- Cheaper compute
- Trade-off vs isolation

---

## Notifications

- On success, failure, duration
- Email or webhook
- Integrate with on-call tools
- Document runbooks

---

## Retries

- Per-task setting
- Exponential backoff
- Cap to prevent loops
- Idempotent code required

---

## Workflows

- Multi-task DAGs
- Dependencies and triggers
- Parallel branches
- Conditional logic

---

## Workflow DAG

![workflow_dag](svg/courses/data_engineering/databricks/04_jobs_and_pipelines/workflow_dag.svg)

---

## Declarative Pipelines

- Define datasets, not steps
- Engine plans incrementally
- Built-in quality expectations
- Monitoring included

---

## Expectations

- Declarative data quality
- Block, drop, or warn
- Visible in pipeline metrics
- Reduces hand-rolled checks

---

## Triggering

- Cron schedule
- File arrival
- API trigger
- Continuous

---

## CI/CD

- Code in git
- Bundles for deploy
- Test in lower env
- Promote with approval

---

## Secrets

- Secrets API
- Reference by scope and key
- Never inline credentials
- Rotate regularly

---

## Common Job Mistakes

- All-purpose clusters for jobs
- No retries
- No alert on failure
- Notebooks edited in production
- Hand-rolled orchestration over jobs
