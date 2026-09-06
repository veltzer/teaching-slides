---
tags:
  - data-and-ai:airflow
  - practices:monitoring
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Monitoring, Logging, and Troubleshooting

---

## What This Chapter Covers

- Task logs
- Web UI dashboards
- Metrics
- Alerts
- Common failures
- Debugging

---

## Task Logs

- Each task instance logs to a file
- View in UI or on disk
- Forward to S3 / cloud storage for persistence
- Or: ELK / Loki stack

---

## Logs and Monitoring

![log_pipeline](svg/courses/data_engineering/apache-airflow/08_monitoring_logging_and_troubleshooting/log_pipeline.svg)

---

## Log Backend Configuration

```ini
[logging]
remote_logging = True
remote_base_log_folder = s3://airflow-logs
remote_log_conn_id = s3_default
```

- Logs survive worker restarts
- Centralised access

---

## Web UI

- DAG view: all DAGs, status
- Tree view: task history per DAG
- Graph view: DAG topology
- Gantt: timing per task

---

## Metrics: StatsD

- Built-in StatsD support
- Forward to Prometheus
- Or: cloud monitoring
- Track: task duration, queue depth, success rate

---

## OpenTelemetry

- Modern alternative
- Traces, metrics, logs unified
- Newer Airflow versions
- The future direction

---

## Alerting

- email_on_failure: simple
- on_failure_callback: custom code
- SLA misses
- Forward to PagerDuty / Slack

---

## Common Failures

- DAG parse error: see scheduler log
- Task timeout: increase or fix code
- Connection failure: check connections
- Out-of-memory: increase worker resources

---

## Debugging

- View task logs in UI
- Re-run individual task
- Check: XCom values, Variables, connections
- Use `airflow tasks test` for ad-hoc

---

## airflow tasks test

```bash
airflow tasks test my_dag my_task 2026-05-01
```

- Run a single task locally
- For dev / debug
- No DAG run created

---

## Scheduler Health

- Heartbeat: scheduler must report regularly
- Slow scheduler: queue grows
- Scheduler restart: tasks paused briefly
- Monitor scheduler latency

---

## Worker Health

- Workers must reach metadata DB
- Celery: monitor queue length
- Kubernetes: pod health
- Auto-scale workers if needed

---

## Metadata DB

- Performance critical
- Vacuum regularly
- Old DAG runs: archive
- Postgres common

---

## Cleaning Up

- Old DAG runs: cleanup task
- `airflow db clean`
- Configure retention
- Otherwise: DB grows unbounded

---

## Common Monitoring Mistakes

- No alerts on DAG failure
- Logs not retained beyond worker
- No view into Celery queue depth
- Metadata DB never cleaned
- Forgetting to monitor the scheduler itself
