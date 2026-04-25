---
tags:
  - concepts:architecture
  - concepts:big-data
  - infrastructure:cloud
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Architecting Systems for Big Data

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

![big_data_architecture_overview](svg/courses/architecting/architecture-patterns/15_big_data/big_data_architecture_overview.svg)

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

## Lambda Architecture Overview

- Combines batch and stream processing methods
- Designed to handle massive quantities of data
- Provides comprehensive and accurate views of batch data
- Offers real-time views of online data
- Aims to balance latency, throughput, and fault-tolerance

---

## Lambda Architecture Diagram

![lambda_architecture](svg/courses/architecting/architecture-patterns/15_big_data/lambda_architecture.svg)

---

## Lambda Pros and Cons

Pros:
- Handles both real-time and batch processing
- Provides fault tolerance and scalability
- Allows reprocessing of data in batch layer
- Supports complex analytics on large datasets
- Enables correction of errors in real-time layer through batch processing

Cons:
- Increased complexity in system architecture
- Requires maintaining two separate systems for batch and speed layers
- May lead to increased operational and development costs
- Potential for data inconsistency between batch and speed layers
- Batch processing introduces latency in data availability

---

## Lambda When to Use

- For systems requiring both batch and real-time data processing
- When dealing with large-scale data that needs both historical and real-time analysis
- In scenarios where data accuracy is crucial, but low-latency views are also needed
- For applications that can tolerate some degree of eventual consistency
- When building systems that need to handle both incremental and reprocessing computations
- In use cases where you need to balance between accuracy (batch layer) and speed (real-time layer)

---

## Kappa Architecture Overview

- Simplifies Lambda Architecture by treating all data as streams
- Uses a single processing engine for both real-time and batch processing
- Relies on replayable logs or event sourcing for data storage
- Eliminates the need for separate batch and speed layers
- Aims to reduce complexity while maintaining scalability and fault-tolerance

---

## Kappa Architecture Diagram

![kappa_architecture](svg/courses/architecting/architecture-patterns/15_big_data/kappa_architecture.svg)

---

## Kappa Pros and Cons

Pros:
- Simplifies architecture by using a single processing path
- Reduces code duplication and maintenance overhead
- Allows easy reprocessing of data by replaying the event stream
- Provides consistency between "batch" and "real-time" results
- Typically easier to reason about and debug

Cons:
- May require more storage for maintaining a long-term log
- Can be less efficient for certain types of batch processing
- Relies heavily on the scalability of the stream processing system
- May not be suitable for all types of data or processing requirements
- Can be challenging to implement for systems not designed with event sourcing in mind

---

## Kappa When to Use

- When your data can be naturally represented as a series of events or changes
- In systems where the distinction between batch and real-time processing is blurred
- When you need to frequently reprocess historical data
- For applications built around event sourcing and CQRS principles
- When you want to simplify your architecture and reduce maintenance overhead
- In scenarios where consistency between historical and real-time views is crucial
- When your use case allows for incremental processing of all data

---

## Data Lakes in Big Data Stacks

- Both Lambda and Kappa typically land raw data in a data lake before processing
- Schema-on-read; cheap object storage; partition by ingest time
- Architecture, lakehouse evolution, and governance: see ch 14 (Data Lakes)
- This chapter focuses on the processing layer above the lake

---

## Storage Systems

1. HDFS
1. Object Storage
1. NoSQL Databases
1. Data Warehouses
1. Data Lakes

---

## HDFS Architecture

![hdfs_architecture](svg/courses/architecting/architecture-patterns/15_big_data/hdfs_architecture.svg)

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

![spark_architecture](svg/courses/architecting/architecture-patterns/15_big_data/spark_architecture.svg)

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

![machine_learning_pipeline](svg/courses/architecting/architecture-patterns/15_big_data/machine_learning_pipeline.svg)

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

![monitoring_dashboard](svg/courses/architecting/architecture-patterns/15_big_data/monitoring_dashboard.svg)

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

![real_time_processing](svg/courses/architecting/architecture-patterns/15_big_data/real_time_processing.svg)

---

## Batch Processing

![batch_processing](svg/courses/architecting/architecture-patterns/15_big_data/batch_processing.svg)

---

## Hybrid Processing

![hybrid_processing](svg/courses/architecting/architecture-patterns/15_big_data/hybrid_processing.svg)

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
