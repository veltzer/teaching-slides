---
tags:
  - data-and-ai:airflow
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# XComs and Data Passing

---
## XCom Pattern

![xcom_pattern](svg/courses/data_engineering/apache-airflow/06_xcoms_and_data_passing/xcom_pattern.svg)

---
## What This Chapter Covers

- XComs (cross-communication)
- Push / pull
- TaskFlow API
- Custom XCom backends
- Limitations

---
## What XComs Are

- Pass small data between tasks
- Stored in metadata DB
- Accessible by downstream tasks
- "X-com" = cross-communication

---
## Pushing XCom

```python
def push():
    return {"count": 42}  # auto-pushed as 'return_value'

# or explicit:
def push2(**ctx):
    ctx['ti'].xcom_push(key='my_key', value=...)
```

---
## Pulling XCom

```python
def pull(**ctx):
    val = ctx['ti'].xcom_pull(task_ids='upstream', key='my_key')
```

- By task_id
- Optional key (default: return_value)

---
## TaskFlow API XComs

```python
@task
def extract():
    return [1, 2, 3]

@task
def process(data):
    return sum(data)

process(extract())
```

- Auto-XCom; clean syntax
- The modern way

---
## Limitations

- Stored in metadata DB
- Default: pickle / JSON
- Size limit: typically MB-class (max 48KB by default in some setups)
- Don't pass huge data

---
## Custom XCom Backend

- For big data: store elsewhere
- S3 backend: store in S3, return reference
- Custom backend implements get / set
- Configure in airflow.cfg

---
## Anti-Pattern: Big XComs

- Don't pass dataframes
- Don't pass full files
- Pass: paths, IDs, small results
- Big data: in S3 / DB; pass the reference

---
## Branching Via XCom

- Branch operator returns task_id
- Or: BranchPythonOperator with logic

---
## Templating With XComs

```python
BashOperator(
    task_id='use_value',
    bash_command='echo {{ ti.xcom_pull(task_ids="upstream") }}'
)
```

- Jinja template renders XCom value
- Avoids explicit Python wrappers

---
## XCom For Configuration

- Don't pass config via XCom
- Use Airflow Variables or Connections
- XCom: data from one run

---
## XCom Persistence

- Per-DAG-run
- Survives task retries
- Cleared when run cleared

---
## Cross-DAG Data

- XComs are within a DAG run
- Cross-DAG: use Datasets, or external store (S3 + manifest file)

---
## Common XCom Mistakes

- Passing huge data
- Reading XCom in DAG-definition code (not run-time)
- XCom for config (use Variables)
- Forgetting to specify task_ids correctly
- Overusing instead of: writing to a real store
