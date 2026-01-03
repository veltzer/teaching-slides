# Architecting Systems for Big Data
## Modern Architecture Course

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---

## Agenda

1. Introduction to Big Data
1. Big Data Architecture
1. Data Processing Frameworks
1. Storage Solutions
1. Processing Patterns
1. Analytics & ML Integration
1. Security & Governance

---

## The 3 V's of Big Data

- Volume: Scale of data
- Velocity: Speed of data generation
- Variety: Different forms of data

Additional V's:
- Veracity: Data quality
- Value: Business impact

---

## Big Data Architecture Overview

<div class="mermaid">
graph LR
    DS[Data Sources] --> I[Ingestion Layer]
    I --> S[Storage Layer]
    S --> P[Processing Layer]
    P --> A[Analytics Layer]
    A --> V[Visualization Layer]
    S -.->|Metadata| C[Catalog]
    P -.->|Monitoring| M[Metrics]
</div>

---

## Data Sources

1. Structured Data
    - Databases
    - CSV files
1. Semi-structured
    - JSON
    - XML
1. Unstructured
    - Text
    - Images
    - Videos

---

## Lambda Architecture

<div class="mermaid">
graph TB
    D[Data Stream] --> B[Batch Layer]
    D --> S[Speed Layer]
    B --> BV[Batch Views]
    S --> RV[Real-time Views]
    BV --> SL[Serving Layer]
    RV --> SL
    SL --> Q[Queries]
    B -.->|Master Dataset| MD[(Master Data)]
</div>

---

## Kappa Architecture

<div class="mermaid">
graph LR
    D[Data Stream] --> K[Kafka/Event Log]
    K --> SP[Stream Processing]
    SP --> V[Views]
    V --> Q[Queries]
    K -.->|Replay| RP[Reprocessing]
    RP --> SP
</div>

---

## Data Lake Architecture

<div class="mermaid">
graph TB
    subgraph "Data Lake Zones"
        RZ[Raw Zone]
        CZ[Curated Zone]
        PZ[Production Zone]
    end
    DS[Data Sources] --> RZ
    RZ --> T[Transform]
    T --> CZ
    CZ --> P[Process]
    P --> PZ
    PZ --> A[Analytics/ML]
    RZ -.->|Catalog| DC[Data Catalog]
</div>

---

## Storage Systems

1. HDFS
1. Object Storage
1. NoSQL Databases
1. Data Warehouses
1. Data Lakes

---

## HDFS Architecture

<div class="mermaid">
graph TB
    C[Client] --> NN[NameNode]
    NN --> M[Metadata]
    C --> DN1[DataNode 1]
    C --> DN2[DataNode 2]
    C --> DN3[DataNode 3]
    DN1 -.->|Replication| DN2
    DN2 -.->|Replication| DN3
    DN3 -.->|Replication| DN1
    NN -.->|Heartbeat| DN1
    NN -.->|Heartbeat| DN2
    NN -.->|Heartbeat| DN3
</div>

---

## Object Storage Example (S3)

```python
import boto3

def store_data(data, bucket, key):
    s3 = boto3.client('s3')

    # Store with lifecycle policy
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=data,
        StorageClass='INTELLIGENT_TIERING',
        Metadata={
            'source': 'sensors',
            'timestamp': datetime.now().isoformat()
        }
    )
```

---

## Processing Frameworks

1. Apache Hadoop
1. Apache Spark
1. Apache Flink
1. Apache Beam
1. Dask

---

## Spark Architecture

<div class="mermaid">
graph LR
    D[Driver] --> E1[Executor 1]
    D --> E2[Executor 2]
    D --> E3[Executor 3]
    E1 -.->|Tasks| W1[Workers]
    E2 -.->|Tasks| W2[Workers]
    E3 -.->|Tasks| W3[Workers]
    D -.->|Coordinates| CM[Cluster Manager]
</div>

---

## Spark Processing Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("BigDataProcessing") \
    .config("spark.executor.memory", "8g") \
    .getOrCreate()

# Read data
df = spark.read.parquet("s3://data/events/")

# Process
result = df.groupBy("event_type") \
    .agg(
        count("*").alias("count"),
        avg("duration").alias("avg_duration")
    ) \
    .where(col("count") > 1000)

# Write results
result.write \
    .partitionBy("event_type") \
    .mode("overwrite") \
    .parquet("s3://data/aggregated/")
```

---

## Stream Processing

1. Real-time Analytics
1. Event Processing
1. Continuous Computation
1. Window Operations
1. State Management

---

## Streaming Example (Flink)

```java
StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<Event> events = env
    .addSource(new KafkaSource<>())
    .keyBy(Event::getType)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CustomAggregator());

events.addSink(new ElasticsearchSink<>());

env.execute("Streaming Pipeline");
```

---

## Data Warehousing

1. Schema Design
1. Partitioning
1. Data Modeling
1. Query Optimization
1. Performance Tuning

---

## SQL Query Engines

1. Apache Hive
1. Presto/Trino
1. Amazon Athena
1. Apache Drill
1. Snowflake

---

## Presto Query Example

```sql
WITH daily_stats AS (
  SELECT
    date_trunc('day', timestamp) as day,
    user_id,
    count(*) as events,
    sum(amount) as total_amount
  FROM events
  WHERE date >= date_add('day', -30, current_date)
  GROUP BY 1, 2
)
SELECT
  day,
  count(distinct user_id) as users,
  sum(events) as total_events,
  avg(total_amount) as avg_amount
FROM daily_stats
GROUP BY 1
ORDER BY 1 DESC
```

---

## Machine Learning Pipeline

<div class="mermaid">
graph LR
    D[Data Ingestion] --> P[Preprocessing]
    P --> FE[Feature Engineering]
    FE --> T[Training]
    T --> E[Evaluation]
    E --> D2[Deployment]
    T -.->|Model| MS[Model Store]
    E -.->|Metrics| M[Monitoring]
</div>

---

## ML Pipeline Example

```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Create pipeline
pipeline = Pipeline(stages=[
    VectorAssembler(
        inputCols=feature_cols,
        outputCol="features"
    ),
    RandomForestClassifier(
        labelCol="label",
        featuresCol="features"
    )
])

# Train
model = pipeline.fit(training_data)

# Save
model.write().overwrite().save("s3://models/latest")
```

---

## Data Quality

1. Schema Validation
1. Data Profiling
1. Quality Checks
1. Anomaly Detection
1. Data Lineage

---

## Data Quality Example

```python
from great_expectations.dataset import SparkDFDataset

def validate_dataset(df):
    data = SparkDFDataset(df)

    # Add expectations
    data.expect_column_values_to_not_be_null("user_id")
    data.expect_column_values_to_be_between("amount", 0, 1000000)
    data.expect_column_values_to_match_regex("email", r"[^@]+@[^@]+\.[^@]+")

    # Validate
    results = data.validate()

    if not results["success"]:
        raise DataQualityException(results)
```

---

## Monitoring Systems

1. Cluster Metrics
1. Job Statistics
1. Data Quality
1. Resource Usage
1. Performance Metrics

---

## Monitoring Dashboard

<div class="mermaid">
graph TB
    subgraph "Monitoring Stack"
        M[Metrics Collection] --> P[Prometheus]
        L[Log Collection] --> E[Elasticsearch]
        T[Traces] --> J[Jaeger]
    end
    P --> G[Grafana Dashboard]
    E --> K[Kibana]
    J --> G
    G --> A[Alerts]
    K --> A
</div>

---

## Resource Management

```yaml
resources:
  driver:
    cores: 4
    memory: "16g"
  executor:
    cores: 8
    memory: "32g"
    instances: 10

dynamic:
  minExecutors: 2
  maxExecutors: 20
  targetCPUUtilization: 0.7
```

---

## Security Implementation

```python
def secure_data_access():
    # Enable encryption
    spark.conf.set("spark.hadoop.fs.s3a.encryption.enabled", "true")

    # Set up authentication
    spark.conf.set("spark.hadoop.fs.s3a.aws.credentials.provider",
                  "com.amazonaws.auth.WebIdentityTokenCredentialsProvider")

    # Enable audit logging
    spark.conf.set("spark.hadoop.fs.s3a.audit.enabled", "true")
```

---

## Data Governance

1. Access Control
1. Data Catalog
1. Metadata Management
1. Compliance
1. Audit Trails

---

## Data Catalog Example

```python
from datacatalog import DataCatalog

catalog = DataCatalog()

# Register dataset
catalog.register_dataset(
    name="user_events",
    location="s3://data/events/",
    schema=schema,
    owner="data_team",
    tags=["pii", "raw"],
    retention_days=90,
    sensitivity="high"
)
```

---

## Cost Optimization

1. Storage Tiering
1. Compute Scaling
1. Caching Strategy
1. Query Optimization
1. Resource Planning

---

## Cost Optimization Example

```python
def optimize_storage():
    # Move cold data to cheaper storage
    s3.copy_object(
        Bucket="archive-bucket",
        Key=f"archive/{date}/data.parquet",
        CopySource={
            "Bucket": "hot-bucket",
            "Key": f"data/{date}/data.parquet"
        },
        StorageClass="GLACIER"
    )

    # Delete from hot storage
    s3.delete_object(
        Bucket="hot-bucket",
        Key=f"data/{date}/data.parquet"
    )
```

---

## Disaster Recovery

1. Backup Strategy
1. Recovery Plans
1. Data Replication
1. Failover Process
1. Testing Procedures

---

## Performance Optimization

1. Partitioning Strategy
1. Indexing
1. Caching
1. Query Optimization
1. Resource Allocation

---

## Partitioning Example

```python
def optimize_partitioning(df):
    # Repartition for optimal file size
    df = df.repartition(
        num_partitions=calculate_optimal_partitions(df),
        partitionBy=["year", "month", "day"]
    )

    # Write with optimization
    df.write \
        .option("maxRecordsPerFile", 1000000) \
        .partitionBy("year", "month", "day") \
        .format("parquet") \
        .save(output_path)
```

---

## Real-time Processing

<div class="mermaid">
graph LR
    S[Stream Source] --> K[Kafka]
    K --> SP[Stream Processor]
    SP --> RT[Real-time Analytics]
    SP --> DB[(State Store)]
    RT --> D[Dashboard]
    RT --> AL[Alerts]
    SP -.->|Checkpoint| CP[Checkpoints]
</div>

---

## Batch Processing

<div class="mermaid">
graph LR
    DS[(Data Source)] --> I[Ingestion]
    I --> S[(Storage/Data Lake)]
    S --> B[Batch Jobs]
    B --> T[Transform]
    T --> A[Aggregate]
    A --> DW[(Data Warehouse)]
    DW --> R[Reports]
    B -.->|Schedule| SC[Scheduler]
</div>

---

## Hybrid Processing

<div class="mermaid">
graph TB
    D[Data Sources] --> RT[Real-time Stream]
    D --> BT[Batch Data]
    RT --> SP[Stream Processing]
    BT --> BP[Batch Processing]
    SP --> SV[(Speed Views)]
    BP --> BV[(Batch Views)]
    SV --> SL[Serving Layer]
    BV --> SL
    SL --> API[API/Query Layer]
    API --> U[Users]
</div>

---

## Future Trends

1. Serverless Analytics
1. AI-Driven Optimization
1. Multi-cloud Architecture
1. Real-time Everything
1. Automated Governance

---

## Best Practices

1. Data Quality First
1. Proper Partitioning
1. Resource Planning
1. Security by Design
1. Cost Optimization
1. Regular Monitoring
1. Documentation
