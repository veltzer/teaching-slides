# Workflow Orchestration and Data Pipelines
## Modern Architecture Course

---

## Agenda

1. Introduction to Workflow Orchestration
1. DAGs and Workflows
1. Major Orchestration Tools
1. Data Pipeline Patterns
1. Implementation Strategies
1. Monitoring and Observability
1. Best Practices

---

## What is Workflow Orchestration

- Automation of complex processes
- Dependency management
- Error handling and recovery
- Scheduling and triggers
- Resource management
- Monitoring and logging

---

## Key Workflow Concepts

![0](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/0.png)

---

## Directed Acyclic Graphs (DAGs)

- No cyclic dependencies
- Clear execution order
- Task dependencies
- Parallel execution
- Error propagation

---

## DAG Example

![1](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/1.png)

---

## Popular Orchestration Tools

1. Apache Airflow
1. Prefect
1. Dagster
1. Netflix Conductor
1. Argo Workflows
1. Luigi

---

## Apache Airflow Architecture

![2](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/2.png)

---

## Airflow DAG Example

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_workflow',
    default_args=default_args,
    schedule_interval='@daily'
)

def extract():
    # Extract data
    pass

def transform():
    # Transform data
    pass

def load():
    # Load data
    pass

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag
)

extract_task >> transform_task >> load_task
```

---

## Prefect Architecture

![3](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/3.png)

---

## Prefect Flow Example

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def extract_data():
    # Extract data
    return data

@task
def transform_data(data):
    # Transform data
    return transformed_data

@task
def load_data(data):
    # Load data
    pass

@flow(name="ETL Pipeline")
def etl_pipeline():
    raw_data = extract_data()
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)

if __name__ == "__main__":
    etl_pipeline()
```

---

## Dagster Architecture

![4](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/4.png)

---

## Dagster Job Example

```python
from dagster import job, op, In, Out

@op
def extract():
    return extract_data()

@op
def transform(data):
    return transform_data(data)

@op
def load(data):
    load_data(data)

@job
def etl_pipeline():
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)

if __name__ == "__main__":
    result = etl_pipeline.execute_in_process()
```

---

## Netflix Conductor Architecture

![5](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/5.png)

---

## Conductor Workflow Example

```json
{
  "name": "etl_workflow",
  "version": 1,
  "tasks": [
    {
      "name": "extract",
      "taskReferenceName": "extract_ref",
      "type": "SIMPLE",
      "inputParameters": {
        "source": "${workflow.input.source}"
      }
    },
    {
      "name": "transform",
      "taskReferenceName": "transform_ref",
      "type": "SIMPLE",
      "inputParameters": {
        "data": "${extract_ref.output.data}"
      }
    },
    {
      "name": "load",
      "taskReferenceName": "load_ref",
      "type": "SIMPLE",
      "inputParameters": {
        "data": "${transform_ref.output.data}"
      }
    }
  ]
}
```

---

## Common Pipeline Patterns

1. ETL/ELT
1. Fan-out/Fan-in
1. Branch and Merge
1. Retry with Backoff
1. Circuit Breaker

---

## ETL Pattern

![6](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/6.png)

---

## Fan-out/Fan-in Pattern

![7](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/7.png)

---

## Branch and Merge Example

```python
from dagster import job, op, Out

@op(out={"success": Out(), "failure": Out()})
def validate(data):
    if is_valid(data):
        return {"success": data}
    else:
        return {"failure": data}

@op
def process_valid(data):
    return process_success(data)

@op
def process_invalid(data):
    return process_failure(data)

@op
def merge_results(success_data, failure_data):
    return merge(success_data, failure_data)

@job
def branching_pipeline():
    data = extract()
    valid, invalid = validate(data)
    success = process_valid(valid)
    failure = process_invalid(invalid)
    merge_results(success, failure)
```

---

## Retry Pattern Implementation

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def fetch_data():
    try:
        return external_api.get_data()
    except ApiError as e:
        logger.error(f"API Error: {e}")
        raise
```

---

## Circuit Breaker Pattern

```python
from circuitbreaker import circuit

@circuit(
    failure_threshold=5,
    recovery_timeout=60,
    expected_exception=ServiceUnavailable
)
def process_data():
    try:
        return service.process()
    except Exception as e:
        logger.error(f"Service Error: {e}")
        raise ServiceUnavailable()
```

---

## Error Handling Strategies

1. Retry Logic
1. Dead Letter Queues
1. Fallback Actions
1. Alert Notifications
1. Recovery Workflows

---

## Error Handling Example

```python
@task(
    retries=3,
    retry_delay=timedelta(minutes=5),
    on_failure_callback=notify_team
)
def process_data():
    try:
        data = fetch_data()
        process(data)
    except FetchError:
        # Handle fetch errors
        send_to_dlq()
    except ProcessError:
        # Handle process errors
        trigger_recovery_workflow()
```

---

## Monitoring and Observability

1. Task Status
1. Duration Metrics
1. Error Rates
1. Resource Usage
1. Data Quality

---

## Monitoring Dashboard

![8](../../../out/mermaid/marp/courses/architecting/XX_workflows.md/8.png)

---

## Metrics Collection Example

```python
from prometheus_client import Counter, Histogram
import time

task_counter = Counter('task_runs_total', 'Total task runs')
task_duration = Histogram('task_duration_seconds', 'Task duration')

@task
def monitored_task():
    task_counter.inc()
    with task_duration.time():
        # Task execution
        process_data()
```

---

## Data Quality Checks

```python
from great_expectations.core import ExpectationSuite
from great_expectations.dataset import PandasDataset

def validate_data(df):
    dataset = PandasDataset(df)
    dataset.expect_column_values_to_not_be_null('id')
    dataset.expect_column_values_to_be_unique('email')
    dataset.expect_column_values_to_be_between('age', 0, 120)

    validation_result = dataset.validate()
    if not validation_result.success:
        raise DataQualityError(validation_result)
```

---

## Resource Management

1. CPU Allocation
1. Memory Limits
1. Concurrency Control
1. Queue Management
1. Worker Scaling

---

## Resource Configuration Example

```yaml
resources:
  cpu: 2
  memory: 4Gi

concurrency:
  task_concurrency: 3
  dag_concurrency: 16

pools:
  - name: heavy_process
    slots: 2
  - name: api_calls
    slots: 5
```

---

## Scalability Patterns

1. Horizontal Scaling
1. Queue-based Distribution
1. Partition-based Processing
1. Dynamic Worker Allocation

---

## Horizontal Scaling Example

```python
from kubernetes import client, config

def scale_workers(replicas):
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    # Scale deployment
    apps_v1.patch_namespaced_deployment_scale(
        name="airflow-worker",
        namespace="airflow",
        body={"spec": {"replicas": replicas}}
    )
```

---

## Security Considerations

1. Authentication
1. Authorization
1. Encryption
1. Audit Logging
1. Secret Management

---

## Security Implementation

```python
from airflow.models import Connection
from airflow.contrib.hooks.aws_hook import AwsHook

def get_secure_connection():
    conn = Connection(
        conn_id='secure_conn',
        conn_type='aws',
        login='access_key',
        password='secret_key'
    )

    hook = AwsHook(conn.conn_id)
    return hook.get_client('s3')
```

---

## Workflow Testing

1. Unit Testing
1. Integration Testing
1. End-to-End Testing
1. Dry Runs
1. Mocking

---

## Testing Example

```python
import pytest
from unittest.mock import Mock

def test_etl_workflow():
    # Mock dependencies
    extract_mock = Mock(return_value={'data': 'test'})
    transform_mock = Mock(return_value={'processed': 'test'})
    load_mock = Mock()

    # Create workflow
    workflow = ETLWorkflow(
        extract=extract_mock,
        transform=transform_mock,
        load=load_mock
    )

    # Execute
    workflow.run()

    # Verify
    extract_mock.assert_called_once()
    transform_mock.assert_called_once_with({'data': 'test'})
    load_mock.assert_called_once_with({'processed': 'test'})
```

---

## Best Practices

1. Idempotent Tasks
1. Clear Dependencies
1. Proper Error Handling
1. Comprehensive Monitoring
1. Regular Testing
1. Documentation
1. Version Control

---

## Future Trends

1. Serverless Workflows
1. AI/ML Integration
1. Real-time Processing
1. Multi-cloud Orchestration
1. Enhanced Automation
