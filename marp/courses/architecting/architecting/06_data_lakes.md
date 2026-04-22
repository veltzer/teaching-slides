---
tags:
  - concepts:architecture
  - concepts:data-lakes
  - concepts:big-data
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Data Lakes and Lakehouses
## Modern Architecture Course

---

## Agenda

1. Introduction to Data Lakes
1. Data Lakehouse Architecture
1. Components and Implementation
1. Data Ingestion Patterns
1. Analytics and ML Integration
1. Best Practices

---

## What is a Data Lake

- Repository for raw data in native format
- Supports structured and unstructured data
- Schema-on-read approach
- Unlimited scalability
- Cost-effective storage
- Supports all data types

---

## Data Lake vs Data Warehouse

![data_lake_vs_data_warehouse](svg/courses/architecting/architecting/06_data_lakes/data_lake_vs_data_warehouse.svg)

---

## Data Lake Architecture

![data_lake_architecture](svg/courses/architecting/architecting/06_data_lakes/data_lake_architecture.svg)

---

## Data Formats in Data Lakes

1. Structured
    - Parquet
    - ORC
    - Avro
1. Semi-structured
    - JSON
    - XML
1. Unstructured
    - Text
    - Images
    - Video

---

## Apache Parquet Example

```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Read CSV data
df = pd.read_csv('data.csv')

# Convert to PyArrow Table
table = pa.Table.from_pandas(df)

# Write to Parquet with partitioning
pq.write_table(
    table,
    'data.parquet',
    partition_cols=['year', 'month']
)
```

---

## Evolution to Data Lakehouse

Traditional Problems:
- Data reliability issues
- Lack of ACID transactions
- Performance challenges
- Schema enforcement
- Data quality

Solution: Data Lakehouse Architecture

---

## Data Lakehouse Architecture

![data_lakehouse_architecture](svg/courses/architecting/architecting/06_data_lakes/data_lakehouse_architecture.svg)

---

## Key Lakehouse Features

1. ACID Transactions
1. Schema Enforcement
1. Time Travel
1. Upserts/Deletes
1. Streaming Support
1. BI Support
1. ML Integration

---

## Delta Lake Example

```python
from delta.tables import DeltaTable
from pyspark.sql import SparkSession

# Create Delta Table
DeltaTable.createIfNotExists(spark) \
    .tableName("events") \
    .addColumn("id", "LONG") \
    .addColumn("timestamp", "TIMESTAMP") \
    .addColumn("data", "STRING") \
    .partitionedBy("timestamp") \
    .execute()

# Upsert data
deltaTable = DeltaTable.forName(spark, "events")
deltaTable.merge(
    source = updates_df,
    condition = "events.id = updates.id"
) \
.whenMatched().updateAll() \
.whenNotMatched().insertAll() \
.execute()
```

---

## Apache Iceberg Features

- Schema evolution
- Hidden partitioning
- Time travel
- Snapshot isolation
- Optimistic concurrency

---

## Iceberg Table Example

```sql
-- Create Iceberg table
CREATE TABLE events (
    id bigint,
    timestamp timestamp,
    data string
) USING iceberg
PARTITIONED BY (days(timestamp));

-- Time travel query
SELECT * FROM events
TIMESTAMP AS OF '2024-01-01 00:00:00';

-- Snapshot query
SELECT * FROM events
VERSION AS OF 12345;
```

---

## Data Ingestion Strategies

1. Batch Processing
1. Stream Processing
1. Change Data Capture
1. API Integration
1. File-based Ingestion

---

## Batch Ingestion Example

```python
from pyspark.sql import SparkSession

def batch_ingest():
    spark = SparkSession.builder \
        .appName("BatchIngestion") \
        .getOrCreate()

    # Read from source
    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://db/source") \
        .load()

    # Write to data lake
    df.write \
        .format("delta") \
        .mode("append") \
        .partitionBy("date") \
        .save("/lake/raw/events")
```

---

## Streaming Ingestion

![streaming_ingestion](svg/courses/architecting/architecting/06_data_lakes/streaming_ingestion.svg)

---

## Streaming Example with Kafka

```python
from pyspark.sql.streaming import *

# Create streaming query
streamingDF = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "events") \
    .load()

# Write to Delta Lake
query = streamingDF \
    .writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/checkpoints") \
    .start("/lake/streaming/events")
```

---

## Data Management & Governance

1. Data Catalog
1. Access Control
1. Data Quality
1. Metadata Management
1. Lineage Tracking

---

## Data Catalog Example

```python
from datacatalog import DataCatalog

# Register dataset
catalog = DataCatalog()
catalog.register_dataset(
    name="customer_events",
    path="/lake/events",
    schema=schema,
    owner="data_team",
    tags=["pii", "raw"],
    retention_days=90
)
```

---

## Processing Engines

1. Apache Spark
1. Presto/Trino
1. Apache Flink
1. Databricks
1. Amazon EMR

---

## Spark Processing Example

```python
from pyspark.sql.functions import *

# Read from lake
events = spark.read.format("delta") \
    .load("/lake/raw/events")

# Process data
processed = events \
    .withColumn("date", to_date("timestamp")) \
    .withColumn("hour", hour("timestamp")) \
    .groupBy("date", "hour") \
    .agg(count("*").alias("event_count"))

# Write back to lake
processed.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("date") \
    .save("/lake/processed/hourly_events")
```

---

## ML Pipeline Integration

![ml_pipeline_integration](svg/courses/architecting/architecting/06_data_lakes/ml_pipeline_integration.svg)

---

## Feature Engineering Example

```python
from pyspark.ml.feature import VectorAssembler, StandardScaler

# Create feature pipeline
assembler = VectorAssembler(
    inputCols=["feature1", "feature2", "feature3"],
    outputCol="features"
)

scaler = StandardScaler(
    inputCol="features",
    outputCol="scaled_features"
)

# Transform data
transformed = assembler.transform(raw_data)
scaled = scaler.fit(transformed).transform(transformed)
```

---

## Data Lake Security

1. Authentication
1. Authorization
1. Encryption
1. Auditing
1. Data Masking

---

## Security Implementation

```python
# Example using AWS
import boto3

def setup_security():
    # Enable encryption
    s3 = boto3.client('s3')
    s3.put_bucket_encryption(
        Bucket='data-lake',
        ServerSideEncryptionConfiguration={
            'Rules': [{
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                }
            }]
        }
    )

    # Setup IAM policies
    iam = boto3.client('iam')
    iam.put_role_policy(
        RoleName='DataLakeAccess',
        PolicyName='ReadWrite',
        PolicyDocument={
            'Version': '2012-10-17',
            'Statement': [{
                'Effect': 'Allow',
                'Action': ['s3:GetObject', 's3:PutObject'],
                'Resource': 'arn:aws:s3:::data-lake/*'
            }]
        }
    )
```

---

## Monitoring and Analytics

1. Storage Metrics
1. Processing Metrics
1. Query Performance
1. Data Quality Metrics
1. Usage Analytics

---

## Monitoring Dashboard

![monitoring_dashboard](svg/courses/architecting/architecting/06_data_lakes/monitoring_dashboard.svg)

---

## Implementation Strategies

1. Cloud-based
    - AWS S3 + EMR
    - Azure Data Lake
    - GCP Cloud Storage
1. On-premises
    - Hadoop HDFS
    - MinIO
    - Ceph

---

## Hybrid Architecture

![hybrid_architecture](svg/courses/architecting/architecting/06_data_lakes/hybrid_architecture.svg)

---

## Best Practices

1. Zone-based architecture
1. Data quality checks
1. Proper partitioning
1. Performance optimization
1. Cost management
1. Regular maintenance

---

## Future Trends

1. Automated data quality
1. Real-time processing
1. AI-driven optimization
1. Unified governance
1. Zero-copy cloning
