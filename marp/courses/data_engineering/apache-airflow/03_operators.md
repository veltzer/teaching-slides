---
tags:
  - data-and-ai:airflow
  - data-and-ai:operators
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Operators

---
## What This Chapter Covers

- What operators are
- Common operators
- Custom operators
- Provider packages
- Hooks vs operators

---
## What An Operator Is

- A class representing a task
- "Run a Python function", "Copy to S3", "Run a SQL query"
- Each operator is one task type

---
## Operator Kinds

![operator_kinds](svg/courses/data_engineering/apache-airflow/03_operators/operator_kinds.svg)

---
## PythonOperator

```python
PythonOperator(
    task_id='process',
    python_callable=process_func,
    op_kwargs={'date': '{{ ds }}'}
)
```

- Run Python code
- Most common for custom logic

---
## BashOperator

```python
BashOperator(
    task_id='run_script',
    bash_command='python /scripts/foo.py'
)
```

- Run shell command
- Ad-hoc operations

---
## Database Operators

- PostgresOperator: run Postgres SQL
- SnowflakeOperator
- BigQueryOperator
- Each: provider-specific
- Cleaner than custom Python

---
## File Transfer Operators

- S3CopyObjectOperator
- GCSToBigQueryOperator
- LocalFilesystemToS3Operator
- Common ETL patterns

---
## Provider Packages

- Apache Airflow Providers: per-service packages
- Postgres provider, AWS provider, Google provider, etc.
- Install: `pip install apache-airflow-providers-postgres`
- Hundreds available

---
## Hooks

- Lower-level: connect to a service
- Operators usually use hooks underneath
- "I want to call this in a Python function"
- PostgresHook, S3Hook, etc.

---
## Custom Operators

```python
class MyOperator(BaseOperator):
    def execute(self, context):
        # ... logic ...
        return result
```

- Subclass BaseOperator
- Implement execute method
- For repeated patterns

---
## Custom Hooks

- Subclass BaseHook
- Provide connection / API methods
- Use in operators

---
## Operator Templating

- Many parameters Jinja-templated
- `{{ ds }}`: execution date
- Templates rendered at run time

---
## Templated Fields

- Operators declare which fields are templated
- `template_fields = ('sql', 'output_path')`
- Custom operators: declare your own

---
## TaskFlow Decorators

- `@task` works with most operators
- `@task.bash` for bash
- `@task.docker` for Docker container
- More Pythonic than constructing operators

---
## Common Operator Mistakes

- Building shell pipelines in BashOperator (use Python)
- Not using provider operators (NIH)
- Custom operators for one-off tasks
- Forgetting templating
- Not checking provider docs for existing operators
