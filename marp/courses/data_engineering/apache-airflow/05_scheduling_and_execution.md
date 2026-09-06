---
tags:
  - data-and-ai:airflow
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Scheduling and Execution

---

## What This Chapter Covers

- Schedules
- Catchup
- Backfills
- Execution date / data interval
- Concurrency
- Pools

---

## Schedule Expressions

- Cron: `'0 12 * * *'`
- Presets: `'@daily'`, `'@hourly'`, `'@once'`
- timedelta: `timedelta(hours=6)`
- None: manually triggered

---

## Scheduling Concepts

![schedule_intervals](svg/courses/data_engineering/apache-airflow/05_scheduling_and_execution/schedule_intervals.svg)

---

## Data Interval

- Each DAG run covers a data interval
- "Run for 2026-05-01" processes data for that day
- Logical date: end of interval
- Different from execution time

---

## Execution Date / Logical Date

- Confusing: NOT when the DAG ran
- It's the logical date the run covers
- Run at 2026-05-02 covers 2026-05-01
- Templated as {{ ds }} = "2026-05-01"

---

## Catchup

- Backfill all intervals since start_date
- Default: True
- Often turned off
- "Run from start_date until now"

---

## Catchup=False

```python
DAG(..., catchup=False)
```

- Only the latest schedule_interval
- Most production DAGs

---

## Backfills

- Manually run DAG for past dates
- `airflow dags backfill ...`
- Useful for: re-runs after fixes
- Rerun only failed: `--rerun-failed-tasks`

---

## Concurrency Limits

- max_active_runs: per DAG
- max_active_tasks: per DAG
- parallelism: cluster-wide
- task_concurrency: per task
- Tune to avoid overwhelming downstream

---

## Pools

- Limit total concurrent tasks of a type
- "Only 5 BigQuery queries at a time"
- Tasks queue in the pool
- Manage external resource constraints

---

## Sample Pool

```python
@task(pool='bigquery_pool')
def heavy_query(): ...
```

- Pool defined in UI or config
- Pool limit set

---

## Time Zones

- DAGs use UTC by default
- Set timezone with pendulum
- Daylight saving time: gotcha
- Best: UTC throughout

---

## Templating Date Values

- {{ ds }}: 2026-05-01
- {{ ds_nodash }}: 20260501
- {{ data_interval_start }}: full timestamp
- {{ macros.ds_add(ds, 7) }}: 2026-05-08

---

## SLAs

- Per-task: time budget from start of DAG
- Alert if exceeded
- For: late-arriving data alerts

---

## Datasets

- Modern feature
- DAG triggered when dataset updated
- Cleaner than schedule + sensor

---

## Common Scheduling Mistakes

- Catchup=True with old start_date (huge backlog)
- Wrong understanding of execution_date
- Pool not configured (overwhelm downstream)
- max_active_runs default (often too low or high)
- Time zone surprises

---

## Choosing an Executor

![executor_types](svg/courses/data_engineering/apache-airflow/05_scheduling_and_execution/executor_types.svg)
