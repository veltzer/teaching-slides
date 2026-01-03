# Workflow Orchestration and Data Pipelines
## Modern Architecture Course

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

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

<div class="mermaid">
graph TB
    subgraph "Workflow Components"
        T[Tasks/Jobs]
        D[Dependencies]
        S[Schedule]
        R[Resources]
    end

    subgraph "Execution"
        E[Executor]
        W[Workers]
        Q[Queue]
    end

    subgraph "Monitoring"
        M[Metrics]
        L[Logs]
        A[Alerts]
    end

    T --> E
    D --> E
    S --> E
    E --> W
    E --> Q
    W --> M
    W --> L
    M --> A

    style T fill:#e3f2fd
    style E fill:#f3e5f5
    style M fill:#e8f5e9
</div>

---

## Directed Acyclic Graphs (DAGs)

- No cyclic dependencies
- Clear execution order
- Task dependencies
- Parallel execution
- Error propagation

---

## DAG Example

<div class="mermaid">
graph LR
    Start[Start] --> Extract[Extract Data]
    Extract --> Clean[Clean Data]
    Extract --> Validate[Validate Data]

    Clean --> Transform[Transform]
    Validate --> Transform

    Transform --> Load1[Load to DB]
    Transform --> Load2[Load to S3]

    Load1 --> Report[Generate Report]
    Load2 --> Report

    Report --> End[End]

    style Start fill:#e3f2fd
    style Transform fill:#f3e5f5
    style Report fill:#e8f5e9
</div>

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

<div class="mermaid">
graph TB
    subgraph "Airflow Components"
        WS[Web Server]
        SCH[Scheduler]
        EX[Executor]
        MD[Metadata DB]
    end

    subgraph "Workers"
        W1[Worker 1]
        W2[Worker 2]
        W3[Worker N]
    end

    subgraph "DAGs"
        D1[DAG 1]
        D2[DAG 2]
        D3[DAG N]
    end

    WS --> MD
    SCH --> MD
    SCH --> EX
    EX --> W1
    EX --> W2
    EX --> W3

    D1 --> SCH
    D2 --> SCH
    D3 --> SCH

    style WS fill:#e3f2fd
    style SCH fill:#f3e5f5
    style W1 fill:#e8f5e9
</div>

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

<div class="mermaid">
graph TB
    subgraph "Prefect Core"
        F[Flows]
        T[Tasks]
        S[State Management]
    end

    subgraph "Prefect Server"
        API[API Server]
        UI[UI Dashboard]
        DB[PostgreSQL]
    end

    subgraph "Agents"
        A1[Agent 1]
        A2[Agent 2]
        A3[Agent N]
    end

    F --> T
    T --> S
    S --> API
    API --> DB
    API --> UI

    A1 --> API
    A2 --> API
    A3 --> API

    style F fill:#e3f2fd
    style API fill:#f3e5f5
    style A1 fill:#e8f5e9
</div>

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

<div class="mermaid">
graph TB
    subgraph "Dagster Core"
        J[Jobs]
        O[Ops/Assets]
        R[Resources]
        IO[IO Managers]
    end

    subgraph "Dagster Instance"
        D[Dagit UI]
        DM[Daemon]
        RS[Run Storage]
        ES[Event Storage]
    end

    subgraph "Execution"
        EX[Executors]
        RQ[Run Queue]
        RL[Run Launcher]
    end

    J --> O
    O --> R
    O --> IO

    D --> RS
    DM --> ES
    DM --> RQ
    RQ --> RL
    RL --> EX

    style J fill:#e3f2fd
    style D fill:#f3e5f5
    style EX fill:#e8f5e9
</div>

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

<div class="mermaid">
graph TB
    subgraph "Conductor Server"
        WE[Workflow Engine]
        TQ[Task Queues]
        MS[Metadata Store]
    end

    subgraph "Workers"
        W1[Worker Pool 1]
        W2[Worker Pool 2]
        W3[Worker Pool N]
    end

    subgraph "Storage"
        ES[Elasticsearch]
        DB[Database]
    end

    C[Client API] --> WE
    WE --> TQ
    TQ --> W1
    TQ --> W2
    TQ --> W3

    WE --> MS
    MS --> ES
    MS --> DB

    style C fill:#e3f2fd
    style WE fill:#f3e5f5
    style W1 fill:#e8f5e9
</div>

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

<div class="mermaid">
graph LR
    subgraph "Extract"
        E1[Database]
        E2[API]
        E3[Files]
    end

    subgraph "Transform"
        T1[Clean]
        T2[Validate]
        T3[Enrich]
        T4[Aggregate]
    end

    subgraph "Load"
        L1[Data Warehouse]
        L2[Data Lake]
        L3[Analytics DB]
    end

    E1 --> T1
    E2 --> T1
    E3 --> T1

    T1 --> T2
    T2 --> T3
    T3 --> T4

    T4 --> L1
    T4 --> L2
    T4 --> L3

    style E1 fill:#e3f2fd
    style T1 fill:#f3e5f5
    style L1 fill:#e8f5e9
</div>

---

## Fan-out/Fan-in Pattern

<div class="mermaid">
graph TB
    S[Split Data]

    subgraph "Parallel Processing"
        P1[Process Chunk 1]
        P2[Process Chunk 2]
        P3[Process Chunk 3]
        P4[Process Chunk N]
    end

    M[Merge Results]

    S --> P1
    S --> P2
    S --> P3
    S --> P4

    P1 --> M
    P2 --> M
    P3 --> M
    P4 --> M

    M --> R[Final Result]

    style S fill:#e3f2fd
    style M fill:#f3e5f5
    style R fill:#e8f5e9
</div>

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

<div class="mermaid">
graph TB
    subgraph "Workflow Metrics"
        WM1[Success Rate]
        WM2[Failure Rate]
        WM3[Average Duration]
        WM4[Task Queue Depth]
    end

    subgraph "System Metrics"
        SM1[CPU Usage]
        SM2[Memory Usage]
        SM3[Worker Status]
    end

    subgraph "Alerts"
        A1[Failed Jobs]
        A2[Long Running Tasks]
        A3[Resource Limits]
    end

    WM1 --> D[Dashboard]
    WM2 --> D
    WM3 --> D
    WM4 --> D

    SM1 --> D
    SM2 --> D
    SM3 --> D

    D --> A1
    D --> A2
    D --> A3

    style WM1 fill:#e3f2fd
    style D fill:#f3e5f5
    style A1 fill:#ffcdd2
</div>

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
