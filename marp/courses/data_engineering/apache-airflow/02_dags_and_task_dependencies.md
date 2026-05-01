---
tags:
  - data-and-ai:airflow
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# DAGs and Task Dependencies

---
## What This Chapter Covers

- DAG structure
- Defining tasks
- Dependencies
- Task groups
- Branching
- TaskFlow API

---
## DAG Structure

- DAG: container of tasks + dependencies
- start_date, schedule, catchup
- Tasks defined as operators

---
## Task Dependencies

```python
task_a >> task_b >> task_c
task_a >> [task_b, task_c]
```

- `>>` operator
- Or: set_upstream / set_downstream

---
## Task Groups

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup('extract') as extract:
    e1 = ...
    e2 = ...

with TaskGroup('transform') as transform:
    t1 = ...

extract >> transform
```

- Visual grouping
- Reuse common pipelines

---
## Branching

```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**ctx):
    return 'task_a' if condition else 'task_b'

branch = BranchPythonOperator(task_id='branch', python_callable=choose_branch)
```

- Conditional execution
- Skip non-chosen tasks

---
## Trigger Rules

- all_success (default)
- one_success
- all_failed
- one_failed
- none_failed
- always
- Configure per task

---
## TaskFlow API

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2026, 1, 1), schedule='@daily')
def my_pipeline():
    @task
    def extract():
        return [1, 2, 3]

    @task
    def transform(x):
        return x * 2

    @task
    def load(items):
        print(items)

    load(transform(extract()))

dag = my_pipeline()
```

- Modern, Pythonic
- Auto-handles XComs

---
## Dynamic Task Mapping

```python
@task
def double(n): return n * 2

double.expand(n=[1, 2, 3, 4, 5])
```

- Generates tasks at runtime
- Like map / parallel for-each

---
## SubDAGs

- Older nesting mechanism
- Performance issues
- Replaced by TaskGroups
- Don't use new ones

---
## DAG Versioning

- DAG ID: stays the same; treat as immutable
- Major changes: rename DAG
- Or: version the DAG file (modern feature)

---
## SLA

- Time budget per task
- Alert if exceeded
- For: SLA monitoring

---
## Default Args

```python
default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}
```

- Apply to all tasks unless overridden

---
## Common DAG Mistakes

- Top-level code that runs every DAG parse (Airflow parses every minute)
- Cyclic dependencies
- DAGs that span days of execution time
- Heavy work in DAG definition (parsing slows)
- No retries on flaky tasks
