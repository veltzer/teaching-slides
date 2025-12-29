# Advanced Spark Ecosystem and Best Practices
---

## Agenda

- Spark on Kubernetes and Cloud Platforms
- Integration with Delta Lake for ACID Transactions
- Monitoring and Debugging Spark Applications
- Best Practices for Production Deployment
- Security Considerations in Spark Applications

---
## Part 1: Spark on Kubernetes and Cloud Platforms
---

## Evolution of Spark Deployment

- **Traditional deployment**: YARN, Mesos, Standalone
- **Modern deployment**: Kubernetes, Cloud-native services
- **Benefits**: Flexibility, scalability, resource isolation

---

## Why Kubernetes for Spark?

- Container orchestration with dynamic scaling
- Resource efficiency and isolation
- Consistent deployment across environments
- Self-healing capabilities
- Integrated with modern CI/CD pipelines

---

## Spark on Kubernetes Architecture

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" style="height: 400px; display: block; margin: auto;">
  <rect width="800" height="400" fill="#f8f9fa"/>

  <!-- Kubernetes Cluster Box -->
  <rect x="50" y="30" width="700" height="340" fill="none" stroke="#326ce5" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="400" y="20" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#326ce5">Kubernetes Cluster</text>

  <!-- API Server -->
  <rect x="100" y="60" width="120" height="50" fill="#326ce5" rx="5"/>
  <text x="160" y="90" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">API Server</text>

  <!-- Driver Pod -->
  <g transform="translate(300, 120)">
    <rect x="0" y="0" width="200" height="80" fill="#ff6b6b" rx="5"/>
    <text x="100" y="25" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white" font-weight="bold">Driver Pod</text>
    <rect x="10" y="35" width="180" height="35" fill="#ff5252" rx="3"/>
    <text x="100" y="58" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white">Spark Driver</text>
  </g>

  <!-- Executor Pods -->
  <g transform="translate(100, 240)">
    <rect x="0" y="0" width="150" height="80" fill="#4ecdc4" rx="5"/>
    <text x="75" y="25" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white" font-weight="bold">Executor Pod 1</text>
    <rect x="10" y="35" width="130" height="35" fill="#45b7aa" rx="3"/>
    <text x="75" y="58" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white">Spark Executor</text>
  </g>

  <g transform="translate(275, 240)">
    <rect x="0" y="0" width="150" height="80" fill="#4ecdc4" rx="5"/>
    <text x="75" y="25" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white" font-weight="bold">Executor Pod 2</text>
    <rect x="10" y="35" width="130" height="35" fill="#45b7aa" rx="3"/>
    <text x="75" y="58" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white">Spark Executor</text>
  </g>

  <g transform="translate(450, 240)">
    <rect x="0" y="0" width="150" height="80" fill="#4ecdc4" rx="5"/>
    <text x="75" y="25" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white" font-weight="bold">Executor Pod N</text>
    <rect x="10" y="35" width="130" height="35" fill="#45b7aa" rx="3"/>
    <text x="75" y="58" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white">Spark Executor</text>
  </g>

  <!-- Arrows showing communication -->
  <path d="M 220 85 L 300 140" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 400 200 L 175 240" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 400 200 L 350 240" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 400 200 L 525 240" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>

  <!-- Labels -->
  <text x="250" y="110" font-family="Arial, sans-serif" font-size="11" fill="#666">Submit</text>
  <text x="320" y="225" font-family="Arial, sans-serif" font-size="11" fill="#666">Schedule</text>
</svg>

---

## Setting Up Spark on Kubernetes

```yaml
# Example spark-submit for Kubernetes
spark-submit \
  --master k8s://https://kubernetes-api-server:443 \
  --deploy-mode cluster \
  --name spark-pi \
  --class org.apache.spark.examples.SparkPi \
  --conf spark.kubernetes.container.image=spark:v3.4.0 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/examples/jars/spark-examples_2.12-3.4.0.jar
```

---

## Key Kubernetes Configuration Options

- `spark.kubernetes.namespace`
- `spark.kubernetes.container.image.pullPolicy`
- `spark.kubernetes.authenticate.driver.serviceAccountName`
- `spark.kubernetes.driver.request.cores`/`spark.kubernetes.executor.request.cores`
- `spark.kubernetes.driver.limit.cores`/`spark.kubernetes.executor.limit.cores`

---

## Spark on AWS

- **EMR**: Managed Spark cluster service
- **EMR on EKS**: Combines EMR with Kubernetes
- **AWS Glue**: Serverless Spark ETL service

---

## Spark on Azure

- **Azure Databricks**: Optimized Spark platform
- **Azure Synapse Analytics**: Integrated analytics service
- **Azure HDInsight**: Managed Hadoop/Spark service

---

## Spark on Google Cloud Platform

- **Dataproc**: Managed Spark/Hadoop service
- **Dataproc Serverless**: Spark without cluster management
- **Google Kubernetes Engine (GKE)**: For custom Spark on K8s

---

## Cloud-Native Spark Optimization

- Use cloud storage (S3, ADLS, GCS)
- Leverage instance-store for shuffle
- Right-size instances for workloads
- Utilize spot/preemptible instances
- Monitor cloud costs

---
## Part 2: Integration with Delta Lake for ACID Transactions
---

## What is Delta Lake?

- Open-source storage layer for Spark
- Brings ACID transactions to Spark
- Enables reliable data lakes
- Developed by Databricks, now open source

<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" style="position: absolute; right: 5%; top: 50%; transform: translateY(-50%); width: 40%; max-width: 300px;">
  <!-- Delta symbol -->
  <g transform="translate(150, 150)">
    <!-- Triangle (Delta) -->
    <path d="M 0,-80 L 70,60 L -70,60 Z" fill="#00b4d8" stroke="#0077b6" stroke-width="3"/>
    <!-- Inner highlight -->
    <path d="M 0,-50 L 45,40 L -45,40 Z" fill="#90e0ef" opacity="0.3"/>
    <!-- Lake waves -->
    <path d="M -50,20 Q -25,10 0,20 T 50,20" stroke="#0077b6" stroke-width="2" fill="none"/>
    <path d="M -50,35 Q -25,25 0,35 T 50,35" stroke="#0077b6" stroke-width="2" fill="none"/>
  </g>
  <!-- Text -->
  <text x="150" y="250" font-family="Arial, sans-serif" font-size="28" font-weight="bold" text-anchor="middle" fill="#0077b6">DELTA LAKE</text>
</svg>

---

## Delta Lake Key Features

- ACID transactions
- Schema enforcement and evolution
- Time travel (data versioning)
- Audit history
- Efficient upserts and deletes
- Optimized for batch and streaming

---

## Delta Lake Architecture

<svg viewBox="0 0 900 450" xmlns="http://www.w3.org/2000/svg" style="height: 450px; display: block; margin: auto;">
  <rect width="900" height="450" fill="#f8f9fa"/>

  <!-- Bronze Layer -->
  <g transform="translate(50, 50)">
    <rect x="0" y="0" width="200" height="350" fill="#cd7f32" opacity="0.2" rx="10"/>
    <text x="100" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#8b4513">Bronze Layer</text>
    <text x="100" y="55" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#666">(Raw Data)</text>
    <!-- Data Sources -->
    <rect x="20" y="80" width="160" height="40" fill="#cd7f32" rx="5"/>
    <text x="100" y="105" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Streaming Data</text>
    <rect x="20" y="140" width="160" height="40" fill="#cd7f32" rx="5"/>
    <text x="100" y="165" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Batch Files</text>
    <rect x="20" y="200" width="160" height="40" fill="#cd7f32" rx="5"/>
    <text x="100" y="225" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">IoT Sensors</text>
    <rect x="20" y="260" width="160" height="40" fill="#cd7f32" rx="5"/>
    <text x="100" y="285" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">External APIs</text>
  </g>
  <!-- Silver Layer -->
  <g transform="translate(350, 50)">
    <rect x="0" y="0" width="200" height="350" fill="#c0c0c0" opacity="0.2" rx="10"/>
    <text x="100" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#696969">Silver Layer</text>
    <text x="100" y="55" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#666">(Refined Data)</text>
    <!-- Processing -->
    <rect x="20" y="80" width="160" height="40" fill="#9e9e9e" rx="5"/>
    <text x="100" y="105" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Data Validation</text>
    <rect x="20" y="140" width="160" height="40" fill="#9e9e9e" rx="5"/>
    <text x="100" y="165" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Deduplication</text>
    <rect x="20" y="200" width="160" height="40" fill="#9e9e9e" rx="5"/>
    <text x="100" y="225" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Schema Enforcement</text>
    <rect x="20" y="260" width="160" height="40" fill="#9e9e9e" rx="5"/>
    <text x="100" y="285" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Data Cleaning</text>
  </g>
  <!-- Gold Layer -->
  <g transform="translate(650, 50)">
    <rect x="0" y="0" width="200" height="350" fill="#ffd700" opacity="0.2" rx="10"/>
    <text x="100" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#b8860b">Gold Layer</text>
    <text x="100" y="55" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#666">(Business Data)</text>
    <!-- Business Views -->
    <rect x="20" y="80" width="160" height="40" fill="#ffb300" rx="5"/>
    <text x="100" y="105" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Analytics Tables</text>
    <rect x="20" y="140" width="160" height="40" fill="#ffb300" rx="5"/>
    <text x="100" y="165" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">ML Features</text>
    <rect x="20" y="200" width="160" height="40" fill="#ffb300" rx="5"/>
    <text x="100" y="225" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Reports</text>
    <rect x="20" y="260" width="160" height="40" fill="#ffb300" rx="5"/>
    <text x="100" y="285" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Dashboards</text>
  </g>
  <!-- Arrows -->
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Flow arrows -->
  <path d="M 250 150 L 350 150" stroke="#333" stroke-width="3" marker-end="url(#arrow)"/>
  <path d="M 250 230 L 350 230" stroke="#333" stroke-width="3" marker-end="url(#arrow)"/>
  <path d="M 550 150 L 650 150" stroke="#333" stroke-width="3" marker-end="url(#arrow)"/>
  <path d="M 550 230 L 650 230" stroke="#333" stroke-width="3" marker-end="url(#arrow)"/>
  <!-- Labels on arrows -->
  <text x="300" y="145" font-family="Arial, sans-serif" font-size="11" fill="#666">ETL</text>
  <text x="300" y="225" font-family="Arial, sans-serif" font-size="11" fill="#666">Stream</text>
  <text x="600" y="145" font-family="Arial, sans-serif" font-size="11" fill="#666">Aggregate</text>
  <text x="600" y="225" font-family="Arial, sans-serif" font-size="11" fill="#666">Transform</text>
  <!-- Delta Lake label at bottom -->
  <text x="450" y="430" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#0077b6">Delta Lake Multi-Hop Architecture</text>
</svg>

---

## Setting Up Delta Lake with Spark

```python
# Adding Delta Lake to Spark
spark.sql("CREATE DATABASE IF NOT EXISTS delta_db")

# Creating a Delta table
spark.sql("""
  CREATE TABLE delta_db.customer_data (
    id LONG,
    name STRING,
    email STRING,
    update_timestamp TIMESTAMP
  ) USING DELTA
""")
```

---

## Writing to Delta Tables

```python
# Batch write
dataFrame.write.format("delta") \
  .mode("overwrite") \
  .save("/path/to/delta/table")

# Streaming write
streamingDF.writeStream \
  .format("delta") \
  .outputMode("append") \
  .option("checkpointLocation", "/path/to/checkpoint") \
  .start("/path/to/delta/table")
```

---

## ACID Transactions with Delta Lake

```python
# Atomic operations
spark.sql("""
  MERGE INTO customers t
  USING updates s
  ON t.id = s.id
  WHEN MATCHED THEN UPDATE SET *
  WHEN NOT MATCHED THEN INSERT *
""")
```

---

## Time Travel with Delta Lake

```python
# Query by version
spark.read.format("delta") \
  .option("versionAsOf", 5) \
  .load("/path/to/delta/table")

# Query by timestamp
spark.read.format("delta") \
  .option("timestampAsOf", "2025-01-15 00:00:00") \
  .load("/path/to/delta/table")
```

---

## Schema Evolution with Delta Lake

```python
# Add new column with schema evolution
from pyspark.sql.functions import lit

spark.read.format("delta") \
  .load("/path/to/delta/table") \
  .withColumn("new_column", lit(None)) \
  .write.format("delta") \
  .mode("overwrite") \
  .option("mergeSchema", "true") \
  .save("/path/to/delta/table")
```

---

## Delta Lake Optimization Commands

```python
# Compact small files
spark.sql("OPTIMIZE delta_db.customer_data")

# Z-order clustering
spark.sql("""
  OPTIMIZE delta_db.customer_data
  ZORDER BY (date, region)
""")

# Vacuum old file versions
spark.sql("VACUUM delta_db.customer_data RETAIN 168 HOURS")
```

---
## Part 3: Monitoring and Debugging Spark Applications
---

## Spark Monitoring Metrics

Key metrics to track:
- **Executor/driver memory usage**
- **CPU utilization**
- **Shuffle read/write size**
- **GC time/overhead**
- **Task completion rates**
- **I/O throughput**

---

## Spark Web UI

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" style="height: 400px; display: block; margin: auto;">
  <rect width="800" height="400" fill="#f5f5f5"/>

  <!-- Header -->
  <rect x="0" y="0" width="800" height="50" fill="#e15a0d"/>
  <text x="20" y="32" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="white">Spark Application UI</text>
  <text x="680" y="32" font-family="Arial, sans-serif" font-size="14" fill="white">app-20250129</text>

  <!-- Navigation tabs -->
  <rect x="0" y="50" width="800" height="40" fill="#333"/>
  <rect x="10" y="55" width="80" height="30" fill="#e15a0d" rx="3"/>
  <text x="50" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white">Jobs</text>
  <rect x="100" y="55" width="80" height="30" fill="transparent" stroke="#666" stroke-width="1" rx="3"/>
  <text x="140" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#ccc">Stages</text>
  <rect x="190" y="55" width="80" height="30" fill="transparent" stroke="#666" stroke-width="1" rx="3"/>
  <text x="230" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#ccc">Storage</text>
  <rect x="280" y="55" width="90" height="30" fill="transparent" stroke="#666" stroke-width="1" rx="3"/>
  <text x="325" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#ccc">Executors</text>
  <rect x="380" y="55" width="80" height="30" fill="transparent" stroke="#666" stroke-width="1" rx="3"/>
  <text x="420" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#ccc">SQL</text>

  <!-- Job List -->
  <text x="20" y="120" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#333">Active Jobs (2)</text>

  <!-- Job 1 -->
  <rect x="20" y="135" width="760" height="80" fill="white" stroke="#ddd" stroke-width="1" rx="5"/>
  <text x="30" y="155" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">Job 0: collect at DataProcessor.py:142</text>
  <text x="30" y="175" font-family="Arial, sans-serif" font-size="12" fill="#666">Duration: 2.3 min | Stages: 3/5</text>

  <!-- Progress bar -->
  <rect x="30" y="185" width="300" height="20" fill="#e0e0e0" rx="3"/>
  <rect x="30" y="185" width="180" height="20" fill="#4caf50" rx="3"/>
  <text x="180" y="199" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">60%</text>

  <!-- Job 2 -->
  <rect x="20" y="225" width="760" height="80" fill="white" stroke="#ddd" stroke-width="1" rx="5"/>
  <text x="30" y="245" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">Job 1: saveAsTable at ETLPipeline.py:87</text>
  <text x="30" y="265" font-family="Arial, sans-serif" font-size="12" fill="#666">Duration: 45 sec | Stages: 2/4</text>

  <!-- Progress bar -->
  <rect x="30" y="275" width="300" height="20" fill="#e0e0e0" rx="3"/>
  <rect x="30" y="275" width="150" height="20" fill="#2196f3" rx="3"/>
  <text x="180" y="289" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">50%</text>

  <!-- Summary Stats -->
  <rect x="20" y="320" width="180" height="60" fill="white" stroke="#ddd" stroke-width="1" rx="5"/>
  <text x="30" y="340" font-family="Arial, sans-serif" font-size="12" fill="#666">Total Tasks:</text>
  <text x="120" y="340" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">2,456</text>
  <text x="30" y="360" font-family="Arial, sans-serif" font-size="12" fill="#666">Completed:</text>
  <text x="120" y="360" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#4caf50">1,842</text>

  <rect x="210" y="320" width="180" height="60" fill="white" stroke="#ddd" stroke-width="1" rx="5"/>
  <text x="220" y="340" font-family="Arial, sans-serif" font-size="12" fill="#666">Shuffle Read:</text>
  <text x="310" y="340" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">3.2 GB</text>
  <text x="220" y="360" font-family="Arial, sans-serif" font-size="12" fill="#666">Shuffle Write:</text>
  <text x="310" y="360" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">2.8 GB</text>

  <rect x="400" y="320" width="180" height="60" fill="white" stroke="#ddd" stroke-width="1" rx="5"/>
  <text x="410" y="340" font-family="Arial, sans-serif" font-size="12" fill="#666">Storage Memory:</text>
  <text x="510" y="340" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">8.5/16 GB</text>
  <text x="410" y="360" font-family="Arial, sans-serif" font-size="12" fill="#666">Execution Memory:</text>
  <text x="510" y="360" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">12.3/32 GB</text>
</svg>

---

## Key Spark UI Tabs

- **Jobs**: Overview of job execution and stages
- **Stages**: Detailed DAG visualization and metrics
- **Storage**: RDD/DataFrame persistence info
- **Executors**: Resource utilization per executor
- **SQL**: Execution plans for SQL queries
- **Environment**: Configuration settings

---

## Spark History Server

```bash
# Start history server
./sbin/start-history-server.sh

# Configure application for history server
spark.eventLog.enabled true
spark.eventLog.dir hdfs://namenode:8021/spark-logs
spark.history.fs.logDirectory hdfs://namenode:8021/spark-logs
```

---

## Integrating Spark with Prometheus & Grafana

```properties
# In spark-defaults.conf
spark.metrics.conf=/path/to/metrics.properties

# In metrics.properties
*.sink.prometheus.class=org.apache.spark.metrics.sink.PrometheusSink
*.sink.prometheus.period=10
*.sink.prometheus.port=8091
```

![bg right:30% 80%](https://grafana.com/static/img/grafana_logo.svg)

---

## Custom Spark Metrics

```python
from py4j.java_gateway import java_import
from pyspark import SparkContext

# Get Java imports
sc = SparkContext.getOrCreate()
java_import(sc._jvm, "org.apache.spark.metrics.source.Source")
java_import(sc._jvm, "com.codahale.metrics.MetricRegistry")
java_import(sc._jvm, "com.codahale.metrics.Gauge")

# Define a Python class that implements the Java interface
class CustomMetricsSource(object):
    def __init__(self):
        self.registry = sc._jvm.com.codahale.metrics.MetricRegistry()

        # Define a gauge
        class LongGauge(sc._jvm.com.codahale.metrics.Gauge):
            def getValue(self):
                # Return custom value
                return 100

        self.registry.register("custom_metric", LongGauge())

    def getSourceName(self):
        return "CustomMetrics"

    def getMetricRegistry(self):
        return self.registry
```

---

## Common Spark Performance Issues

- **Data skew**: Uneven partition distribution
- **Small file problem**: Excessive file handles/metadata
- **Memory pressure**: OOM errors, excessive GC
- **Insufficient parallelism**: Underutilized cluster
- **Inefficient joins**: Cartesian products, broadcast threshold issues
- **Resource contention**: CPU/memory/network bottlenecks

---

## Debugging Data Skew

```python
# Check partition sizes
partition_sizes = df.rdd.glom().map(lambda x: len(x)).collect()
sorted_sizes = sorted(partition_sizes)
print(sorted_sizes)

# Repartition by hash to balance data
from pyspark.sql.functions import col
df_balanced = df.repartition(200, col("skewed_column"))

# Use salting technique for skewed joins
from pyspark.sql.functions import rand, col
salt_factor = 10
salted_df = skewed_df.withColumn("salt",
  (rand() * salt_factor).cast("int"))
```

---

## Debugging Memory Issues

```python
# Check executor memory breakdown
sc.getExecutorMemoryStatus()

# Get RDD storage details
spark.sparkContext.getRDDStorageInfo()

# Find storage fraction
sc.getConf().get("spark.memory.fraction")
sc.getConf().get("spark.memory.storageFraction")
```

---

## Debugging with Spark Logs

- **Driver logs**: Application-level issues
- **Executor logs**: Task-specific failures
- **Event logs**: Detailed execution timeline
- **GC logs**: Memory management issues

```bash
# Enable GC logs
--conf spark.executor.extraJavaOptions="-verbose:gc -XX:+PrintGCDetails"
```

---
## Part 4: Best Practices for Production Deployment
---

## Spark Application Configuration Best Practices

### Memory Configuration

```properties
spark.driver.memory=16g
spark.executor.memory=32g
spark.executor.memoryOverhead=6g
spark.memory.fraction=0.8
spark.memory.storageFraction=0.3
```

### CPU Configuration

```properties
spark.driver.cores=4
spark.executor.cores=8
spark.task.cpus=1
```

---

## Dynamic Resource Allocation

```properties
spark.dynamicAllocation.enabled=true
spark.dynamicAllocation.minExecutors=5
spark.dynamicAllocation.maxExecutors=100
spark.dynamicAllocation.executorIdleTimeout=60s
spark.dynamicAllocation.schedulerBacklogTimeout=1s
spark.shuffle.service.enabled=true
```

Benefits:
- Automatically adjusts resources
- Improves cluster utilization
- Reduces costs in cloud environments

---

## Spark Job Scheduling

### Fair Scheduler Configuration

```xml
<allocations>
  <pool name="production">
    <schedulingMode>FAIR</schedulingMode>
    <weight>10</weight>
    <minShare>5</minShare>
  </pool>
  <pool name="development">
    <schedulingMode>FIFO</schedulingMode>
    <weight>1</weight>
    <minShare>2</minShare>
  </pool>
</allocations>
```

---

## Input/Output Optimization

- **Input partitioning**: Match with HDFS block size
- **Output partitioning**: Control file sizes
- **File formats**: Use Parquet/ORC for analytics
- **Compression**: Balance between CPU and I/O
- **Predicate pushdown**: Filter early

```python
from pyspark.sql.functions import col

spark.read \
  .option("mergeSchema", "true") \
  .parquet("/data/path") \
  .filter(col("date") > "2025-01-01") \
  .repartition(200) \
  .write \
  .partitionBy("year", "month") \
  .option("compression", "snappy") \
  .parquet("/output/path")
```

---

## Data Pipeline Design Patterns

- **Bronze-Silver-Gold** architecture
    - Bronze: Raw ingestion layer
    - Silver: Cleaned, validated data
    - Gold: Business-level aggregates

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg" style="height: 300px; display: block; margin: auto;">
  <rect width="800" height="300" fill="#f8f9fa"/>

  <!-- Bronze Section -->
  <g transform="translate(50, 50)">
    <circle cx="100" cy="100" r="80" fill="#cd7f32" opacity="0.8"/>
    <text x="100" y="95" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="white">BRONZE</text>
    <text x="100" y="115" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white">Raw Data</text>
    <text x="100" y="210" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Ingestion</text>
    <text x="100" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Historical</text>
    <text x="100" y="240" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Unvalidated</text>
  </g>

  <!-- Silver Section -->
  <g transform="translate(300, 50)">
    <circle cx="100" cy="100" r="80" fill="#c0c0c0" opacity="0.8"/>
    <text x="100" y="95" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="white">SILVER</text>
    <text x="100" y="115" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white">Refined Data</text>
    <text x="100" y="210" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Cleaned</text>
    <text x="100" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Deduplicated</text>
    <text x="100" y="240" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Validated</text>
  </g>

  <!-- Gold Section -->
  <g transform="translate(550, 50)">
    <circle cx="100" cy="100" r="80" fill="#ffd700" opacity="0.8"/>
    <text x="100" y="95" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="white">GOLD</text>
    <text x="100" y="115" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white">Business Data</text>
    <text x="100" y="210" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Aggregated</text>
    <text x="100" y="225" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Features</text>
    <text x="100" y="240" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">• Analytics</text>
  </g>

  <!-- Flow Arrows -->
  <defs>
    <marker id="arrowBSG" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>

  <path d="M 230 150 L 370 150" stroke="#333" stroke-width="3" marker-end="url(#arrowBSG)"/>
  <path d="M 480 150 L 620 150" stroke="#333" stroke-width="3" marker-end="url(#arrowBSG)"/>

  <!-- Flow Labels -->
  <text x="300" y="145" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">Clean & Validate</text>
  <text x="550" y="145" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">Aggregate</text>

  <!-- Title -->
  <text x="400" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#333">Delta Lake Medallion Architecture</text>
</svg>

---

## CI/CD for Spark Applications

- **Unit testing**: ScalaTest, JUnit, pytest
- **Integration testing**: spark-testing-base
- **Containerization**: Package dependencies
- **Version control**: Git-based workflows
- **Infrastructure as Code**: Terraform, CloudFormation
- **CI platforms**: Jenkins, GitHub Actions, GitLab CI

---

## Production Job Monitoring

- **SLAs and alerts**: Define critical thresholds
- **Business metrics**: Track domain KPIs
- **Operational metrics**: Cluster health
- **Cost metrics**: Resource utilization
- **Automated recovery**: Implement retry logic

---

## Checkpoint and State Management

```python
# For streaming applications
streaming_query = df_stream.writeStream \
  .fo
```

---

## Disaster Recovery Strategies

- **Multi-region deployment**: Geographic redundancy
- **Backup and restore**: Regular state preservation
- **High availability**: No single point of failure
- **Data replication**: Synchronous/asynchronous copies
- **Chaos engineering**: Proactive failure testing

---
## Part 5: Security Considerations in Spark Applications
---

## Spark Security Framework

Key security domains:
- **Authentication**: Identity verification
- **Authorization**: Access control
- **Encryption**: Data protection
- **Auditing**: Activity monitoring
- **Compliance**: Regulatory requirements

---

## Authentication in Spark

```properties
# Kerberos authentication
spark.authenticate=true
spark.network.crypto.enabled=true
spark.authenticate.enableSaslEncryption=true

# Auth provider
spark.hadoop.hadoop.security.authentication=kerberos
spark.kerberos.keytab=/path/to/keytab
spark.kerberos.principal=spark@EXAMPLE.COM
```

---

## Authorization with Ranger/Sentry

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" style="height: 400px; display: block; margin: auto;">
  <rect width="800" height="400" fill="#f8f9fa"/>

  <!-- Title -->
  <text x="400" y="25" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#333">Apache Ranger Security Architecture</text>

  <!-- Admin Portal -->
  <rect x="320" y="50" width="160" height="60" fill="#2e7d32" rx="5"/>
  <text x="400" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white" font-weight="bold">Ranger Admin</text>
  <text x="400" y="95" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">Policy Manager</text>

  <!-- Policy Database -->
  <rect x="550" y="50" width="120" height="60" fill="#1565c0" rx="5"/>
  <text x="610" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white" font-weight="bold">Policy DB</text>
  <text x="610" y="95" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">MySQL/Postgres</text>

  <!-- Audit Database -->
  <rect x="130" y="50" width="120" height="60" fill="#6a1b9a" rx="5"/>
  <text x="190" y="75" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="white" font-weight="bold">Audit Store</text>
  <text x="190" y="95" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">Solr/ES</text>

  <!-- Plugin Components -->
  <g transform="translate(0, 180)">
    <!-- HDFS Plugin -->
    <rect x="50" y="0" width="120" height="80" fill="#ff6f00" rx="5"/>
    <text x="110" y="20" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white" font-weight="bold">HDFS</text>
    <rect x="60" y="30" width="100" height="35" fill="#ff8f00" rx="3"/>
    <text x="110" y="52" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">Ranger Plugin</text>
    <!-- Hive Plugin -->
    <rect x="190" y="0" width="120" height="80" fill="#ff6f00" rx="5"/>
    <text x="250" y="20" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white" font-weight="bold">Hive</text>
    <rect x="200" y="30" width="100" height="35" fill="#ff8f00" rx="3"/>
    <text x="250" y="52" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">Ranger Plugin</text>
    <!-- Spark Plugin -->
    <rect x="330" y="0" width="120" height="80" fill="#ff6f00" rx="5"/>
    <text x="390" y="20" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white" font-weight="bold">Spark</text>
    <rect x="340" y="30" width="100" height="35" fill="#ff8f00" rx="3"/>
    <text x="390" y="52" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">Ranger Plugin</text>
    <!-- Kafka Plugin -->
    <rect x="470" y="0" width="120" height="80" fill="#ff6f00" rx="5"/>
    <text x="530" y="20" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white" font-weight="bold">Kafka</text>
    <rect x="480" y="30" width="100" height="35" fill="#ff8f00" rx="3"/>
    <text x="530" y="52" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">Ranger Plugin</text>
    <!-- HBase Plugin -->
    <rect x="610" y="0" width="120" height="80" fill="#ff6f00" rx="5"/>
    <text x="670" y="20" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="white" font-weight="bold">HBase</text>
    <rect x="620" y="30" width="100" height="35" fill="#ff8f00" rx="3"/>
    <text x="670" y="52" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="white">Ranger Plugin</text>
  </g>
  <!-- User/Client Layer -->
  <rect x="250" y="320" width="300" height="50" fill="#e0e0e0" rx="5"/>
  <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333" font-weight="bold">Users / Applications / Services</text>
  <!-- Connection Arrows -->
  <defs>
    <marker id="arrowRanger" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="#666"/>
    </marker>
  </defs>
  <!-- Policy sync arrows -->
  <path d="M 400 110 L 110 180" stroke="#666" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <path d="M 400 110 L 250 180" stroke="#666" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <path d="M 400 110 L 390 180" stroke="#666" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <path d="M 400 110 L 530 180" stroke="#666" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <path d="M 400 110 L 670 180" stroke="#666" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <!-- Audit arrows -->
  <path d="M 110 260 L 190 110" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowRanger)" stroke-dasharray="5,3"/>
  <path d="M 250 260 L 190 110" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowRanger)" stroke-dasharray="5,3"/>
  <!-- Admin to Policy DB -->
  <path d="M 480 80 L 550 80" stroke="#1976d2" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <!-- User access arrows -->
  <path d="M 350 320 L 250 260" stroke="#333" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <path d="M 400 320 L 390 260" stroke="#333" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <path d="M 450 320 L 530 260" stroke="#333" stroke-width="2" marker-end="url(#arrowRanger)"/>
  <!-- Labels -->
  <text x="300" y="140" font-family="Arial, sans-serif" font-size="10" fill="#666">Policy Sync</text>
  <text x="150" y="170" font-family="Arial, sans-serif" font-size="10" fill="#9c27b0">Audit</text>
  <text x="515" y="75" font-family="Arial, sans-serif" font-size="10" fill="#1976d2">Store</text>
  <text x="320" y="295" font-family="Arial, sans-serif" font-size="10" fill="#333">Access Request</text>
</svg>

---

## Fine-Grained Access Control

- **Table-level access**: Read/write permissions
- **Column-level security**: Mask sensitive data
- **Row-level security**: Filter by user context
- **Dynamic data masking**: Hide PII in real-time

```sql
-- Example of column masking policy
CREATE MASK email_mask ON TABLE customers
FOR COLUMN email
RETURN
  CASE WHEN current_user() IN ('analyst_role')
    THEN regexp_replace(email, '(.).*@', '$1***@')
    ELSE email
  END
ENABLE;
```

---

## Network Encryption in Spark

```properties
# Wire encryption
spark.network.crypto.enabled=true
spark.io.encryption.enabled=true
spark.io.encryption.keySizeBits=256
spark.io.encryption.keygen.algorithm=HmacSHA1

# SSL configuration
spark.ssl.enabled=true
spark.ssl.keyStore=/path/to/keystore
spark.ssl.keyStorePassword=${KEYSTORE_PASSWORD}
spark.ssl.trustStore=/path/to/truststore
spark.ssl.trustStorePassword=${TRUSTSTORE_PASSWORD}
```

---

## Data Encryption

- **At-rest encryption**: HDFS encryption, cloud storage encryption
- **In-transit encryption**: SSL/TLS
- **HDFS transparent encryption**:
  ```bash
  hdfs crypto -createZone -keyName sparkKey -path /data/secure
  ```
- **Client-side encryption**: Custom encryption utilities

---

## Secrets Management

**Bad practice:**
```scala
val jdbcUsername = "admin"  // Hardcoded credentials
val jdbcPassword = "P@ssw0rd123"

// DO NOT DO THIS
```

**Better approach:**
```scala
// Using secret management services
val secret = spark.sparkContext.hadoopConfiguration
  .get("fs.azure.account.key.storage.dfs.core.windows.net")

// Or environment variables
val password = sys.env.getOrElse("DB_PASSWORD",
  throw new Exception("DB password not set"))
```

---

## Audit Logging

```properties
# Enable audit logs
spark.eventLog.enabled=true
spark.eventLog.dir=hdfs://namenode:8021/spark-logs
spark.history.fs.logDirectory=hdfs://namenode:8021/spark-logs

# Integrate with enterprise logging
spark.driver.extraJavaOptions=-Dlog4j.configuration=log4j-audit.properties
```

Key events to audit:
- Authentication attempts
- Authorization decisions
- Data access patterns
- Configuration changes

---

## Secure Coding Practices

- **Input validation**: Prevent SQL injection
- **Output encoding**: Escape special characters
- **Dependency management**: Regular updates
- **Least privilege**: Minimal permissions
- **Code review**: Security-focused reviews

---

## Compliance Considerations

- **GDPR**: Data protection for EU citizens
- **HIPAA**: Healthcare data protection (US)
- **PCI DSS**: Payment card security
- **SOX**: Financial reporting controls
- **CCPA**: California privacy law

---

## Security Testing

- **Vulnerability scanning**: Regular assessment
- **Penetration testing**: Simulated attacks
- **Configuration analysis**: Hardening verification
- **Dependency checking**: CVE monitoring
- **Data leakage prevention**: Exfiltration testing

---
## Conclusion and Next Steps
---

## Key Takeaways

- Kubernetes provides flexible, scalable Spark deployment
- Delta Lake enables reliable data lakes with ACID properties
- Comprehensive monitoring is essential for production
- Follow deployment best practices for reliability
- Implement security at all layers

---

## Recommended Resources

- [Spark on Kubernetes Documentation](https://spark.apache.org/docs/latest/running-on-kubernetes.html)
- [Delta Lake Documentation](https://docs.delta.io/latest/index.html)
- [Databricks Academy](https://academy.databricks.com/)
- [The Definitive Guide to Apache Spark](https://databricks.com/p/ebook/definitive-guide-to-apache-spark)
- [Learning Spark, 2nd Edition](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/)

---

## Q&A

Thank you!

Contact: spark-admin@example.com

<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="position: absolute; right: 5%; top: 50%; transform: translateY(-50%); width: 30%; max-width: 200px;">
  <!-- Spark Logo -->
  <g transform="translate(100, 100)">
    <!-- Outer circle -->
    <circle cx="0" cy="0" r="80" fill="#e15a0d"/>
    <!-- Lightning bolt -->
    <path d="M -30,-40 L 10,-40 L -10,0 L 20,0 L -20,50 L 0,10 L -30,10 Z" fill="white"/>
    <!-- Spark text -->
    <text x="0" y="60" font-family="Arial, sans-serif" font-size="20" font-weight="bold" text-anchor="middle" fill="white">SPARK</text>
  </g>
  <!-- Apache text -->
  <text x="100" y="20" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">Apache</text>
</svg>
