# Data Lakes and Lakehouses
## Modern Architecture Course

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

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

<div class="mermaid">
graph LR
subgraph "Data Lake"
A[Raw Data<br/>All Formats] --> B[Schema on Read]
B --> C[Low Cost Storage]
end

subgraph "Data Warehouse"
D[Structured Data] --> E[Schema on Write]
E --> F[Optimized for BI]
end

A -.->|ETL Process| D
C -->|Analytics| G[Data Scientists]
F -->|Reports| H[Business Users]

style A fill:#e3f2fd
style D fill:#f3e5f5
style G fill:#e8f5e9
style H fill:#fff3e0
</div>

---

## Data Lake Architecture

<div class="mermaid">
graph TB
subgraph "Data Sources"
S1[Databases]
S2[APIs]
S3[Files]
S4[Streams]
end
subgraph "Ingestion Layer"
I1[Batch Processing]
I2[Stream Processing]
end
subgraph "Storage Layer"
ST1[Raw Zone]
ST2[Processed Zone]
ST3[Curated Zone]
end
subgraph "Processing Layer"
P1[ETL/ELT]
P2[Analytics]
P3[ML Pipelines]
end
S1 --> I1
S2 --> I1
S3 --> I1
S4 --> I2
I1 --> ST1
I2 --> ST1
ST1 --> P1
P1 --> ST2
ST2 --> P2
ST2 --> P3
P2 --> ST3
P3 --> ST3
style ST1 fill:#e3f2fd
style ST2 fill:#f3e5f5
style ST3 fill:#e8f5e9
</div>

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

<div class="mermaid">
graph TB
subgraph "Lakehouse Platform"
L1[Object Storage<br/>Parquet/ORC/Avro]
L2[Metadata Layer<br/>Delta/Iceberg/Hudi]
L3[Transaction Layer<br/>ACID Support]
L4[Query Engine<br/>SQL/DataFrame API]
end
subgraph "Workloads"
W1[BI & Analytics]
W2[Data Science]
W3[Machine Learning]
W4[Real-time Analytics]
end
L1 --> L2
L2 --> L3
L3 --> L4
L4 --> W1
L4 --> W2
L4 --> W3
L4 --> W4
style L1 fill:#e3f2fd
style L2 fill:#f3e5f5
style L3 fill:#e8f5e9
style L4 fill:#fff3e0
</div>

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

<div class="mermaid">
graph LR
subgraph "Stream Sources"
K[Kafka]
KN[Kinesis]
EH[Event Hub]
end
subgraph "Stream Processing"
SP[Spark Streaming]
FL[Flink]
KS[Kafka Streams]
end
subgraph "Data Lake"
R[Raw Events]
P[Processed Events]
A[Aggregated Data]
end
K --> SP
KN --> SP
EH --> FL
SP --> R
FL --> R
KS --> P
R --> P
P --> A
style K fill:#e3f2fd
style SP fill:#f3e5f5
style R fill:#e8f5e9
</div>

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

<div class="mermaid">
graph LR
subgraph "Data Lake"
DL1[Raw Data]
DL2[Feature Store]
DL3[Model Registry]
end

subgraph "ML Pipeline"
ML1[Data Prep]
ML2[Feature Engineering]
ML3[Model Training]
ML4[Model Evaluation]
end

subgraph "Deployment"
D1[Model Serving]
D2[Predictions]
end

DL1 --> ML1
ML1 --> ML2
ML2 --> DL2
DL2 --> ML3
ML3 --> ML4
ML4 --> DL3
DL3 --> D1
D1 --> D2
D2 -.->|Feedback| DL1

style DL1 fill:#e3f2fd
style ML3 fill:#f3e5f5
style D1 fill:#e8f5e9
</div>

---

## Feature Engineering Example

```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.preprocessing import StandardScaler

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

<div class="mermaid">
graph TB
subgraph "Data Lake Metrics"
M1[Storage Usage]
M2[Processing Jobs]
M3[Query Performance]
M4[Data Quality]
M5[Cost Metrics]
end

subgraph "Monitoring Tools"
T1[CloudWatch/Azure Monitor]
T2[Datadog]
T3[Grafana]
end

subgraph "Alerts & Actions"
A1[Threshold Alerts]
A2[Auto-scaling]
A3[Notifications]
end

M1 --> T1
M2 --> T2
M3 --> T3
M4 --> T2
M5 --> T1

T1 --> A1
T2 --> A2
T3 --> A3

style M1 fill:#e3f2fd
style T2 fill:#f3e5f5
style A1 fill:#e8f5e9
</div>

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

<div class="mermaid">
graph TB
subgraph "On-Premises"
OP1[Legacy Systems]
OP2[Sensitive Data]
OP3[Edge Processing]
end

subgraph "Hybrid Layer"
H1[Data Gateway]
H2[Sync Service]
H3[Security Layer]
end

subgraph "Cloud Data Lake"
C1[Object Storage]
C2[Compute Services]
C3[Analytics Tools]
end

OP1 --> H1
OP2 --> H3
OP3 --> H2

H1 --> C1
H2 --> C1
H3 --> C1

C1 --> C2
C2 --> C3

style OP2 fill:#e3f2fd
style H3 fill:#f3e5f5
style C1 fill:#e8f5e9
</div>

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
