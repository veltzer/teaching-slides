# Advanced Spark Ecosystem and Best Practices
---
## Ecosystem Overview
* Kubernetes integration
* Cloud platforms
* Delta Lake
* MLflow integration
---
## Modern Architecture
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Spark</text></svg>

---
## Deployment Options
1. Standalone cluster
1. YARN deployment
1. Kubernetes deployment
1. Cloud services
---
## Kubernetes Integration
```python
# Kubernetes configuration
spark.kubernetes.container.image=spark:v3.0
spark.kubernetes.namespace=spark
```
---
## Resource Management
<svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="70.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Resources</text></svg>

---
## Cloud Integration
1. AWS EMR
1. Azure Synapse
1. Google Dataproc
1. Custom deployment
---
## Cloud Configuration
```python
# AWS EMR configuration
spark.conf.set(
    "spark.hadoop.fs.s3a.access.key",
    "key"
)
```
---
## Storage Integration
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Storage</text></svg>

---
## Delta Lake Overview
1. ACID transactions
1. Schema enforcement
1. Time travel
1. Optimization
---
## Delta Lake Operations
```python
# Write to Delta Lake
df.write.format("delta") \
    .mode("overwrite") \
    .save("/path/to/table")
```
---
## Version Control
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="595" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="640" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Versions</text></svg>

---
## Time Travel
```python
# Read specific version
df = spark.read.format("delta") \
    .option("versionAsOf", "1") \
    .load("/path/to/table")
```
---
## Schema Evolution
1. Add columns
1. Remove columns
1. Change types
1. Merge schema
---
## Delta Operations
```python
from delta.tables import *
deltaTable = DeltaTable.forPath(
    spark, "/path/to/table"
)
```
---
## Optimization Methods
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="280.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Optimize</text></svg>

---
## Performance Tuning
1. File sizing
1. Partitioning
1. Caching
1. Indexing
---
## Monitoring Setup
```python
# Configure monitoring
spark.conf.set(
    "spark.metrics.conf.*.sink.graphite.class",
    "org.apache.spark.metrics.sink.GraphiteSink"
)
```
---
## Metrics Collection
<svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="110.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="190.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Metrics</text></svg>

---
## Security Framework
1. Authentication
1. Authorization
1. Encryption
1. Auditing
---
## Authentication Setup
```python
# Kerberos configuration
spark.conf.set(
    "spark.kerberos.keytab",
    "/path/to/keytab"
)
```
---
## Authorization Model
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="280.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Access</text></svg>

---
## Data Governance
1. Lineage tracking
1. Audit logging
1. Policy enforcement
1. Compliance
---
## Backup Strategies
```python
# Backup configuration
def backup_data():
    snapshot = create_snapshot()
    replicate(snapshot)
```
---
## Disaster Recovery
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="595" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="640" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Disaster</text></svg>

---
## CI/CD Pipeline
1. Build process
1. Testing
1. Deployment
1. Monitoring
---
## Testing Framework
```python
# Unit test example
def test_transformation():
    result = transform_data(input_df)
    assert validate_result(result)
```
---
## Quality Assurance
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="280.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">QA</text></svg>

---
## Cost Optimization
1. Resource sizing
1. Spot instances
1. Storage tiers
1. Caching strategy
---
## Resource Planning
```python
# Resource configuration
spark.conf.set(
    "spark.executor.instances",
    "auto"
)
```
---
## Capacity Planning
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="595" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="640" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Capacity</text></svg>

---
## MLflow Integration
1. Experiment tracking
1. Model registry
1. Deployment
1. Monitoring
---
## Production Pipeline
```python
# Pipeline configuration
pipeline = create_pipeline()
mlflow.spark.log_model(pipeline, "model")
```
---
## Workflow Management
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="280.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Workflow</text></svg>

---
## Best Practices
1. Code organization
1. Documentation
1. Testing
1. Monitoring
---
## Code Standards
```python
# Example structure
class SparkJob:
    def __init__(self):
        self.spark = create_spark_session()
```
---
## Documentation
<svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="110.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="190.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Docs</text></svg>

---
## Troubleshooting
1. Log analysis
1. Metrics review
1. Performance audit
1. Error tracking
---
## Common Issues
```python
# Memory issues
spark.conf.set(
    "spark.memory.offHeap.enabled",
    "true"
)
```
---
## Error Handling
<svg viewBox="0 0 500 480" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="180" x2="295.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="400" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="425" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Error</text></svg>

---
## Maintenance
1. Updates
1. Patches
1. Optimization
1. Cleanup
---
## Version Management
```python
# Version compatibility
spark.conf.set(
    "spark.jars.packages",
    "org.apache.spark:spark-avro_2.12:3.0.0"
)
```
---
## Future Planning
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="595" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="640" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Plan</text></svg>

---
## Migration Strategies
1. Version upgrade
1. Platform migration
1. Data migration
1. Service migration
---
## Cost Management
```python
# Cost optimization
def optimize_resources():
    analyze_usage()
    adjust_resources()
```
---
## Scaling Strategies
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="280.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Scale</text></svg>

---
## Advanced Features
1. Custom extensions
1. Plugins
1. Integrations
1. Tools
---
## Community Resources
* Documentation
* Forums
* Blogs
* Research papers

---

## Full Program: Kubernetes Deployment

```python
# spark-submit configuration for Kubernetes
# spark-submit \
#   --master k8s://https://k8s-api-server:6443 \
#   --deploy-mode cluster \
#   --name spark-etl-job \
#   --conf spark.kubernetes.container.image=myrepo/spark:3.5 \
#   --conf spark.kubernetes.namespace=spark-jobs \
#   --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
#   --conf spark.executor.instances=10 \
#   --conf spark.executor.memory=8g \
#   --conf spark.executor.cores=4 \
#   --conf spark.driver.memory=4g \
#   --conf spark.kubernetes.executor.request.cores=4 \
#   --conf spark.kubernetes.executor.limit.cores=4 \
#   --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.data.mount.path=/data \
#   --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.data.options.claimName=spark-data-pvc \
#   local:///opt/spark/jobs/etl_pipeline.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("K8sETLJob") \
    .config("spark.kubernetes.container.image.pullPolicy", "Always") \
    .config("spark.kubernetes.executor.podTemplateFile",
            "/opt/spark/conf/executor-pod-template.yaml") \
    .config("spark.kubernetes.node.selector.workload", "spark") \
    .getOrCreate()

# Pod template for executor customization
# executor-pod-template.yaml:
# apiVersion: v1
# kind: Pod
# spec:
#   containers:
#   - name: spark-executor
#     resources:
#       requests:
#         memory: "8Gi"
#         cpu: "4"
#       limits:
#         memory: "10Gi"
#         cpu: "4"
#     volumeMounts:
#     - name: scratch-volume
#       mountPath: /tmp/spark
#   volumes:
#   - name: scratch-volume
#     emptyDir:
#       sizeLimit: "50Gi"
```

---

## Kubernetes vs YARN Deployment

| Aspect | YARN | Kubernetes |
|---|---|---|
| Resource isolation | Container-based | Pod-based (stronger) |
| Scaling | Static/Dynamic | Dynamic (autoscaler) |
| Multi-tenancy | Queue-based | Namespace-based |
| Docker support | Limited | Native |
| Cloud-native | No | Yes |
| Setup complexity | Hadoop ecosystem | K8s cluster |
| Monitoring | YARN UI | K8s dashboard + Prometheus |
| Cost | Fixed cluster | Pay-per-use (spot/preemptible) |

---

## Full Program: AWS EMR with S3

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("EMRS3Pipeline") \
    .config("spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.InstanceProfileCredentialsProvider") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.us-east-1.amazonaws.com") \
    .config("spark.sql.parquet.compression.codec", "snappy") \
    .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
    .getOrCreate()

# Read from S3 with partition discovery
raw_events = spark.read.parquet(
    "s3a://my-data-lake/raw/events/"
)

# S3-optimized write with committer
spark.conf.set("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version",
               "2")
spark.conf.set("spark.sql.parquet.output.committer.class",
    "org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter")
spark.conf.set("spark.hadoop.fs.s3a.committer.name", "magic")

# Process and write partitioned data
processed = (
    raw_events
    .withColumn("event_date", F.to_date("timestamp"))
    .withColumn("event_hour", F.hour("timestamp"))
    .filter(F.col("event_date") == "2024-06-15")
)

# Write with dynamic partition overwrite
processed.write \
    .mode("overwrite") \
    .partitionBy("event_date", "event_hour") \
    .parquet("s3a://my-data-lake/processed/events/")

# S3 Select pushdown (read only needed data from S3)
spark.conf.set("spark.hadoop.fs.s3a.select.enabled", "true")
csv_with_select = spark.read \
    .option("header", "true") \
    .csv("s3a://my-data-lake/raw/csv/large_file.csv") \
    .filter(F.col("status") == "active")
```

---

## Cloud Platform Comparison

| Feature | AWS EMR | Azure Synapse | Google Dataproc |
|---|---|---|---|
| Storage | S3 | ADLS Gen2 | GCS |
| Auto-scaling | Yes (managed) | Yes (serverless) | Yes |
| Spot/Preemptible | Spot instances | Low-priority | Preemptible VMs |
| Notebook | EMR Studio | Synapse Notebooks | Jupyter on Dataproc |
| Delta Lake | Yes | Native | Yes |
| Serverless | EMR Serverless | Serverless pools | Dataproc Serverless |
| GPU support | Yes | Yes | Yes |
| Min cost/hour | ~$0.10 | ~$0.15 | ~$0.10 |

---

## Full Program: Delta Lake MERGE Operation

```python
from pyspark.sql import SparkSession
from delta.tables import DeltaTable
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("DeltaLakeMerge") \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Create initial Delta table
initial_data = spark.createDataFrame([
    (1, "Alice", "alice@example.com", "active", "2024-01-01"),
    (2, "Bob", "bob@example.com", "active", "2024-01-01"),
    (3, "Charlie", "charlie@example.com", "active", "2024-01-01"),
], ["id", "name", "email", "status", "updated_at"])

initial_data.write.format("delta").mode("overwrite") \
    .save("/data/delta/customers/")

# Incoming updates (CDC events)
updates = spark.createDataFrame([
    (2, "Bob Smith", "bob.smith@example.com", "active", "2024-06-15"),
    (3, "Charlie", "charlie@example.com", "inactive", "2024-06-15"),
    (4, "Diana", "diana@example.com", "active", "2024-06-15"),
], ["id", "name", "email", "status", "updated_at"])

# MERGE operation (upsert)
delta_table = DeltaTable.forPath(spark, "/data/delta/customers/")

delta_table.alias("target").merge(
    updates.alias("source"),
    "target.id = source.id"
).whenMatchedUpdate(
    condition="source.updated_at > target.updated_at",
    set={
        "name": "source.name",
        "email": "source.email",
        "status": "source.status",
        "updated_at": "source.updated_at",
    }
).whenNotMatchedInsert(
    values={
        "id": "source.id",
        "name": "source.name",
        "email": "source.email",
        "status": "source.status",
        "updated_at": "source.updated_at",
    }
).execute()

# Verify results
spark.read.format("delta").load("/data/delta/customers/").show()

# Time travel: see previous version
previous = spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .load("/data/delta/customers/")
print("Before merge:")
previous.show()

# View table history
delta_table.history().select(
    "version", "timestamp", "operation", "operationMetrics"
).show(truncate=False)
```

---

## Delta Lake Operations Summary

```diagram
┌──────────────────────────────────────────────┐
│            Delta Lake Operations              │
├──────────────────────────────────────────────┤
│                                              │
│  WRITE Operations                            │
│  ├── INSERT (append)                         │
│  ├── UPDATE (in-place modify)                │
│  ├── DELETE (remove rows)                    │
│  ├── MERGE (upsert: insert + update)         │
│  └── OVERWRITE (replace data)                │
│                                              │
│  READ Operations                             │
│  ├── Current version (default)               │
│  ├── Time travel (versionAsOf, timestampAsOf)│
│  └── Change Data Feed (readChangeFeed)       │
│                                              │
│  MAINTENANCE Operations                      │
│  ├── OPTIMIZE (compact small files)          │
│  ├── VACUUM (delete old versions)            │
│  ├── Z-ORDER (co-locate data for queries)    │
│  └── DESCRIBE HISTORY (audit log)            │
│                                              │
│  SCHEMA Operations                           │
│  ├── Schema enforcement (reject bad data)    │
│  ├── Schema evolution (mergeSchema)          │
│  └── Column mapping                          │
│                                              │
└──────────────────────────────────────────────┘
```

---

## Full Program: MLflow Model Registry Pipeline

```python
import mlflow
from mlflow.tracking import MlflowClient
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MLflowPipeline") \
    .getOrCreate()

mlflow.set_tracking_uri("http://mlflow-server:5000")
client = MlflowClient()

# Register a model
model_name = "revenue_predictor"

# Create registered model if it doesn't exist
try:
    client.create_registered_model(model_name)
except Exception:
    pass  # Already exists

# Promote model through stages
# Stage 1: None (just registered)
# Stage 2: Staging (testing)
# Stage 3: Production (serving)

# Find the latest run with best metrics
experiment = mlflow.get_experiment_by_name("revenue_prediction")
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="metrics.rmse < 100",
    order_by=["metrics.rmse ASC"],
    max_results=1
)

if len(runs) > 0:
    best_run_id = runs.iloc[0]["run_id"]

    # Register the model version
    model_version = mlflow.register_model(
        f"runs:/{best_run_id}/model",
        model_name
    )

    # Transition to Staging
    client.transition_model_version_stage(
        name=model_name,
        version=model_version.version,
        stage="Staging"
    )

    # Run validation tests
    staging_model = mlflow.spark.load_model(
        f"models:/{model_name}/Staging"
    )
    test_data = spark.read.parquet("/data/test/revenue/")
    predictions = staging_model.transform(test_data)

    # If validation passes, promote to Production
    from pyspark.ml.evaluation import RegressionEvaluator
    evaluator = RegressionEvaluator(
        labelCol="revenue", predictionCol="prediction",
        metricName="rmse"
    )
    rmse = evaluator.evaluate(predictions)

    if rmse < 150:
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Production"
        )
        print(f"Model v{model_version.version} promoted "
              f"to Production (RMSE={rmse:.2f})")
    else:
        print(f"Model validation failed (RMSE={rmse:.2f})")
```

---

## Full Program: Spark Application Monitoring

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("MonitoredApplication") \
    .config("spark.metrics.conf.*.sink.graphite.class",
            "org.apache.spark.metrics.sink.GraphiteSink") \
    .config("spark.metrics.conf.*.sink.graphite.host", "graphite:2003") \
    .config("spark.metrics.conf.*.sink.graphite.period", "10") \
    .config("spark.metrics.conf.*.sink.graphite.unit", "seconds") \
    .config("spark.ui.prometheus.enabled", "true") \
    .config("spark.eventLog.enabled", "true") \
    .config("spark.eventLog.dir", "hdfs:///spark-events/") \
    .getOrCreate()

# Custom Spark listener for job-level monitoring
class JobMonitor:
    def __init__(self, spark):
        self.spark = spark
        self.sc = spark.sparkContext

    def get_executor_metrics(self):
        """Get current executor metrics."""
        status = self.sc.statusTracker()
        executor_ids = status.getExecutorInfos()
        metrics = []
        for info in executor_ids:
            metrics.append({
                "host": info.host(),
                "port": info.port(),
                "total_cores": info.totalCores(),
                "active_tasks": len(info.activeTasks()),
            })
        return metrics

    def log_query_plan(self, df, query_name):
        """Log the physical plan for a DataFrame."""
        plan = df._jdf.queryExecution().executedPlan().toString()
        print(f"[{query_name}] Physical Plan:")
        print(plan[:500])

    def monitor_job(self, func, job_name):
        """Wrapper to monitor a Spark job."""
        import time
        start = time.time()
        self.sc.setJobDescription(job_name)
        try:
            result = func()
            duration = time.time() - start
            print(f"[{job_name}] Completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            print(f"[{job_name}] Failed after {duration:.2f}s: {e}")
            raise

monitor = JobMonitor(spark)

# Use monitoring wrapper
def my_etl_job():
    df = spark.read.parquet("/data/events/")
    result = df.groupBy("event_type").count()
    result.write.mode("overwrite").parquet("/output/event_counts/")
    return result

monitor.monitor_job(my_etl_job, "daily_event_aggregation")
```

---

## Production Spark Application Structure

```python
"""
Recommended project structure for production Spark applications:

my_spark_project/
├── pyproject.toml           # Project metadata, dependencies
├── src/
│   └── my_spark_project/
│       ├── __init__.py
│       ├── main.py          # Entry point
│       ├── config.py        # Configuration management
│       ├── jobs/
│       │   ├── __init__.py
│       │   ├── base_job.py  # Abstract base class
│       │   ├── etl_job.py   # ETL pipeline
│       │   └── ml_job.py    # ML pipeline
│       ├── transformations/
│       │   ├── __init__.py
│       │   ├── cleaning.py  # Data cleaning functions
│       │   └── features.py  # Feature engineering
│       └── utils/
│           ├── __init__.py
│           ├── io.py        # Read/write helpers
│           └── logging.py   # Logging configuration
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── test_cleaning.py
│   └── test_features.py
├── config/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── prod.yaml
└── Dockerfile
"""

# Example base job class
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

class BaseSparkJob(ABC):
    def __init__(self, app_name, config_path):
        self.config = self._load_config(config_path)
        self.spark = self._create_session(app_name)

    def _create_session(self, app_name):
        builder = SparkSession.builder.appName(app_name)
        for key, value in self.config.get("spark", {}).items():
            builder = builder.config(key, value)
        return builder.getOrCreate()

    def _load_config(self, path):
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, df):
        pass

    @abstractmethod
    def load(self, df):
        pass

    def run(self):
        raw = self.extract()
        transformed = self.transform(raw)
        self.load(transformed)
        self.spark.stop()
```

---

## Security Best Practices

```python
# Authentication: Kerberos for Hadoop
spark.conf.set("spark.kerberos.keytab", "/etc/spark/spark.keytab")
spark.conf.set("spark.kerberos.principal", "spark/host@REALM.COM")

# Encryption: In-transit
spark.conf.set("spark.ssl.enabled", "true")
spark.conf.set("spark.ssl.keyStore", "/etc/spark/keystore.jks")
spark.conf.set("spark.ssl.keyStorePassword", "password")
spark.conf.set("spark.ssl.trustStore", "/etc/spark/truststore.jks")

# Encryption: Shuffle and RPC
spark.conf.set("spark.authenticate", "true")
spark.conf.set("spark.authenticate.secret", "secret-key")
spark.conf.set("spark.network.crypto.enabled", "true")
spark.conf.set("spark.io.encryption.enabled", "true")

# Fine-grained access control (with Apache Ranger)
# Configured at cluster level, not in Spark code

# Secret management (never hardcode credentials!)
# Use environment variables or secret managers
import os
aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Or use IAM roles (preferred on cloud)
spark.conf.set(
    "spark.hadoop.fs.s3a.aws.credentials.provider",
    "com.amazonaws.auth.InstanceProfileCredentialsProvider"
)
```
