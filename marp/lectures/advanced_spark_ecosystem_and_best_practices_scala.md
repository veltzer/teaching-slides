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

![height:400px](https://spark.apache.org/docs/latest/img/k8s-cluster-mode.png)

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

![bg right:40% 70%](https://docs.delta.io/latest/_static/delta-lake-logo.png)

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

![height:450px](https://docs.delta.io/latest/_static/delta-lake-multi-hop-architecture.png)

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

![height:400px](https://databricks.com/wp-content/uploads/2015/06/Screen-Shot-2015-06-10-at-10.30.32-AM-1024x522.png)

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
sc.getExecutorM
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

```scala
spark.read
  .option("mergeSchema", "true")
  .parquet("/data/path")
  .filter($"date" > "2025-01-01")
  .repartition(200)
  .write
  .partitionBy("year", "month")
  .option("compression", "snappy")
  .parquet("/output/path")
```

---

## Data Pipeline Design Patterns

- **Bronze-Silver-Gold** architecture
    - Bronze: Raw ingestion layer
    - Silver: Cleaned, validated data
    - Gold: Business-level aggregates

![height:300px](https://databricks.com/wp-content/uploads/2019/08/image5-2.png)

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

```scala
// For streaming applications
streamingQuery.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", "s3a://bucket/checkpoints/job1")
  .start()

// For batch recovery
sc.setCheckpointDir("s3a://bucket/checkpoints/batch1")
rdd.checkpoint()
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

![height:400px](https://ranger.apache.org/assets/images/architecture.png)

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

![bg right:30% 80%](https://www.apache.org/logos/res/spark/default.png)
