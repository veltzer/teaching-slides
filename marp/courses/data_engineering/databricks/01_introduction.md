---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Introduction to Databricks

---
## What This Chapter Covers

- What Databricks is
- Workspace concepts
- Clusters
- Notebooks and jobs
- Course outline

---
## What Databricks Is

- Cloud platform for data and AI
- Built around Apache Spark
- Ships the Delta table format
- Unified for SQL, Python, Scala, R

---
## Why Use It

- Managed Spark with autoscaling
- One platform for batch and stream
- Notebooks plus jobs plus pipelines
- Strong on ML workflows

---
## Workspace

- Top-level container
- Users, groups, roles
- Notebooks, jobs, models
- Per-region deployment

---
## Workspace Components

![databricks_arch](svg/courses/data_engineering/databricks/01_introduction/databricks_arch.svg)

---
## Repos and Notebooks

- Notebooks: interactive cells
- Repos: git-backed code
- Multi-language in one notebook
- Source of truth lives in git

---
## Clusters

- Compute on demand
- Driver plus workers
- Autoscale by workload
- Terminate to save cost

---
## All-Purpose vs Job Clusters

- All-purpose: shared, interactive
- Job: spawned per job, terminated after
- Job clusters cost less per job
- Production prefers job clusters

---
## Runtime

- Bundle of Spark plus libraries
- Versioned
- ML runtime adds frameworks
- Pin in production

---
## Notebooks

- Cell-based execution
- Visualizations inline
- Schedulable as jobs
- Comments and lineage

---
## Jobs

- Scheduled or triggered
- Tasks form a DAG
- Retries and notifications
- Source of production runs

---
## Workflows

- Multi-task jobs
- Dependencies across tasks
- Different languages per task
- Replaces external orchestrators for many

---
## Catalog

- Unity Catalog for governance
- Three-level namespace
- Permissions per object
- Lineage tracked

---
## Pricing Model

- Compute units per second
- Tied to instance size
- Idle clusters bleed money
- Tag for chargeback

---
## Course Outline

- Spark on Databricks
- Delta tables
- Jobs and pipelines
- ML workflows
- Operations

---
## Common Beginner Mistakes

- Long-lived all-purpose clusters
- Notebooks as production code
- No git
- One workspace for everything
- Ignoring auto-termination
