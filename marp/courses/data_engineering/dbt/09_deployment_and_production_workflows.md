---
tags:
  - data-and-ai:dbt
  - practices:production
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Deployment and Production Workflows

---

## What This Chapter Covers

- dbt Cloud vs self-managed
- Scheduling
- CI / CD
- Environments
- Selecting models
- Monitoring

---

## Environments and Schedules

![dbt_envs](svg/courses/data_engineering/dbt/09_deployment_and_production_workflows/dbt_envs.svg)

---

## dbt Cloud

- Hosted IDE + scheduler
- Run dbt jobs on schedule
- Web UI for logs, lineage
- Commercial; per-user pricing

---

## Self-Managed

- Use dbt Core CLI
- Schedule with Airflow, GitHub Actions, cron
- Free; ops burden
- Common in data platform teams

---

## Airflow + dbt

- Most common pattern
- Airflow DAG calls `dbt run`, `dbt test`
- Per-task dbt commands
- Depends-on for ordering

---

## Environments

- target: dev, staging, prod
- Different schemas / databases per env
- Configured in profiles.yml

---

## profiles.yml

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      schema: dev_user_alice
    prod:
      type: snowflake
      schema: prod
```

---

## Selecting Models

- `dbt run --select model_name`
- `dbt run --select tag:daily`
- `dbt run --select +model_name`: model and downstream
- `dbt run --select model_name+`: model and upstream
- For incremental runs

---

## Slim CI

- On PR: only run / test changed models
- `dbt run --select state:modified+ --defer ...`
- Saves CI time
- Standard for production projects

---

## CI Pipeline

- PR opened: spin up CI environment
- `dbt run` on changed models
- `dbt test`
- Comment status on PR
- Block merge if tests fail

---

## CD Pipeline

- Merge to main: deploy to prod
- Run on schedule (Airflow / Cloud)
- Alert on failures
- Promote dev artifacts to prod

---

## Source Control

- All dbt code in git
- Reviewed via PRs
- Branch per change
- Standard software practice

---

## Monitoring

- dbt Cloud: built-in
- Self-managed: log to S3 / cloud logs
- Track: run duration, failures, freshness
- Alert on regressions

---

## Documentation Hosting

- `dbt docs generate` produces HTML
- Host on S3, GitHub Pages, Atlas
- Embed in internal portals
- Re-generate after each prod run

---

## Best Practices

- Tests as merge-gate
- Slim CI
- Per-developer dev schemas
- Prod runs on schedule (not ad-hoc)

---

## Snapshots Scheduling

- Run with regular dbt run
- Or: separate schedule
- Critical: don't miss snapshots; data history breaks

---

## Common Production Mistakes

- Manual prod runs (drift from CI)
- No environment separation
- Slim CI not configured (slow PRs)
- Ignoring test failures (silently bad data)
- No alerting on failed runs

---

## Course Wrap-Up

- dbt: SQL transformations, version-controlled
- Materialisations match use case
- Tests are first-class
- Documentation is a feature
- Macros and packages for reusability
- Production: CI / CD / scheduling / alerting

---

## CI/CD Pipeline Steps

![cicd_steps](svg/courses/data_engineering/dbt/09_deployment_and_production_workflows/cicd_steps.svg)
