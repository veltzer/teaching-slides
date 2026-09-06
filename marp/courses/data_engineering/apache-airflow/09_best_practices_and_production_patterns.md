---
tags:
  - data-and-ai:airflow
  - practices:production
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Best Practices and Production Patterns

---

## Patterns

![best_practices](svg/courses/data_engineering/apache-airflow/09_best_practices_and_production_patterns/best_practices.svg)

---

## What This Chapter Covers

- DAG design
- Idempotency
- Code organisation
- Testing
- Deployment
- Anti-patterns

---

## DAG Design

- Each DAG: one logical pipeline
- Tasks: small, focused
- Avoid: 1000-task monsters
- Multiple smaller DAGs better than one giant

---

## Idempotency

- Same task with same data interval &#8594; same result
- Crucial for retries and backfills
- Use {{ ds }} in queries, not "today"
- Output: deterministic per interval

---

## Atomic Writes

- Write to staging; rename to final
- Or: write to temp; commit at end
- Avoids: partial data in target

---

## Code Organisation

- DAGs in dags/ folder
- Helpers in plugins/ or installed package
- Operators in operators/
- Don't pollute the dag folder

---

## DAG File Structure

- One DAG per file (mostly)
- Top-level code minimal
- DAG definition function for testability
- Imports at top

---

## Avoid In DAG Definition

- DB queries
- Network calls
- Heavy computation
- Random values
- These run every parse (every minute by default)

---

## Testing

- Unit test custom operators
- DAG validation: import + minimal sanity
- Integration: run on test cluster
- pytest-airflow helps

---

## DAG Validation Test

```python
def test_dag_loads():
    from airflow.models import DagBag
    db = DagBag(include_examples=False)
    assert len(db.import_errors) == 0
```

---

## Deployment

- DAGs from git
- Deploy via: git sync, S3 sync, GitOps
- CI: validate before deploy
- Standard ops practice

---

## CI for DAGs

- pytest for unit tests
- DAG validation
- Lint / format
- On merge: deploy

---

## Versioning

- DAG behaviour can change
- Version tag if behaviour-impacting
- Or: rename DAG for major changes
- Don't surprise consumers

---

## Anti-Patterns

- DAGs that import heavy libraries
- DAGs with random / time-based logic in definition
- One mega-DAG
- Tasks that don't fit in workers
- Synchronous chains where parallel would work

---

## When To Use Airflow

- Batch pipelines
- Complex dependencies
- Need scheduling + retries + alerts
- Team familiar with Python

---

## When Not To

- Real-time / streaming
- Single-script jobs (cron is fine)
- Workflows that change on the fly
- Tight latency requirements

---

## Course Wrap-Up

- Airflow: workflow orchestration in Python
- DAGs of tasks; dependencies; schedule
- Operators for what to run; sensors for waiting
- XComs for small inter-task data; external stores for big
- Production: idempotency, monitoring, secrets
- The standard for batch data pipelines

---

## DAG Anti-Patterns

![dag_anti_patterns](svg/courses/data_engineering/apache-airflow/09_best_practices_and_production_patterns/dag_anti_patterns.svg)
