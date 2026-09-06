---
tags:
  - data-and-ai:airflow
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Introduction to Apache Airflow

---

## What This Chapter Covers

- What Airflow is
- Use cases
- Architecture
- Components
- Why workflow orchestration

---

## What Airflow Is

- Workflow orchestration for batch data pipelines
- Define workflows as Python code
- Schedule and monitor
- Originally from Airbnb (2015)
- Apache top-level since 2019

---

## Architecture

![airflow_arch](svg/courses/data_engineering/apache-airflow/01_introduction_to_apache_airflow/airflow_arch.svg)

---

## Use Cases

- ETL / ELT pipelines
- ML training pipelines
- Data quality checks
- Report generation
- Backfilling historical data

---

## Architecture

- Webserver: UI
- Scheduler: triggers tasks
- Worker (executor): runs tasks
- Metadata DB: state
- Components scale independently

---

## Executors

- Sequential: dev only
- Local: single machine
- Celery: distributed via queue
- Kubernetes: per-task pods
- Pick by scale

---

## DAGs

- Directed Acyclic Graph
- Each node: a task
- Edges: dependencies
- Define in Python

---

## Why Airflow

- Code as workflow (versioned, reviewed)
- Rich UI for monitoring
- Retries, alerts, backfills
- Huge ecosystem of providers

---

## Alternatives

- Prefect: more modern API
- Dagster: asset-oriented
- Argo Workflows: Kubernetes-native
- Airflow: most-deployed
- Pick by team / stack

---

## A Simple DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG('my_dag', start_date=datetime(2026, 1, 1), schedule='@daily') as dag:
    task = PythonOperator(
        task_id='hello',
        python_callable=lambda: print("hi")
    )
```

---

## Web UI

- View DAGs, runs, logs
- Trigger manually
- Pause / unpause
- Visualise dependencies

---

## When To Use

- Many interdependent batch jobs
- Need scheduling + retries + monitoring
- Team familiar with Python
- Most ETL / data pipeline work

---

## When Not To

- Simple cron jobs
- Real-time / streaming (use Kafka Streams, Flink)
- Lightweight glue (just write a script)

---

## Common Misconceptions

- "Airflow is for streaming" — no, batch
- "Airflow runs the work" — usually delegates to other systems
- "DAG file = the work" — DAG defines orchestration; tasks delegate

---

## What's Next

- DAGs and dependencies
- Operators
- Sensors
- Scheduling
- XComs
- Connections
- Production patterns

---

## Where Airflow Fits

![airflow_use_cases](svg/courses/data_engineering/apache-airflow/01_introduction_to_apache_airflow/airflow_use_cases.svg)
