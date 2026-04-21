---
tags:
  - tools:spark
  - languages:python
  - data-and-ai:big-data
  - concepts:data-formats
level: advanced
category: big-data
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Data Formats and Storage

---
## Chapter Overview
* Parquet deep dive: row groups, column chunks, page-level statistics
* Predicate pushdown and projection pushdown
* ORC comparison and Avro for streaming
* Delta Lake operations and time travel
* Apache Iceberg overview
* Partitioning strategies, bucketing, and file compaction

---
## Learning Objectives
* Understand Parquet internal structure and optimization mechanisms
* Compare columnar vs row-based formats for different workloads
* Perform Delta Lake operations including MERGE, time travel, and VACUUM
* Design effective partitioning and bucketing strategies
* Diagnose and resolve the small file problem
* Choose the right storage format for each use case

---
## Parquet File Format Overview

![parquet_file_format_overview](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/parquet_file_format_overview.svg)

---
## Row Groups and Column Chunks

![row_groups_and_column_chunks](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/row_groups_and_column_chunks.svg)

---
## Page-Level Statistics and Column Index

![page_level_statistics_and_column_index](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/page_level_statistics_and_column_index.svg)

---
## Predicate Pushdown

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("PredicatePushdown") \
    .getOrCreate()

# Predicate pushdown pushes filters to the storage layer
# Parquet uses row group and page statistics to skip data

# Example: read with filter
df = (
    spark.read.parquet("/data/events/")
    .filter(F.col("event_date") == "2024-06-15")
    .filter(F.col("amount") > 1000)
)

# Check physical plan for pushed filters
df.explain(mode="formatted")
# Look for: PushedFilters: [IsNotNull(event_date),
#   EqualTo(event_date,2024-06-15), GreaterThan(amount,1000)]

# Predicates that CAN be pushed down:
# - =, <, >, <=, >=, !=
# - IS NULL, IS NOT NULL
# - IN (value_list)
# - AND, OR combinations of the above

# Predicates that CANNOT be pushed down:
# - UDF-based filters
# - LIKE with leading wildcard
# - Complex expressions (CASE WHEN in filter)

# Configuration
spark.conf.set(
    "spark.sql.parquet.filterPushdown", "true")  # default: true
spark.conf.set(
    "spark.sql.parquet.filterPushdown.statistics", "true")
```

---
## Projection Pushdown

```python
# Projection pushdown reads only requested columns
# Parquet stores data column-by-column, so skipping
# unrequested columns is very efficient

# BAD: reads all columns from disk
df_all = spark.read.parquet("/data/wide_table/")  # 200 columns
result = df_all.filter(F.col("status") == "active").select("user_id")

# GOOD: Spark optimizes this automatically via Catalyst
# Only user_id and status columns are read from Parquet
# Even though we wrote it as above, the physical plan
# shows only needed columns in FileScan

# Verify with explain
result.explain()
# FileScan parquet [user_id#0, status#5]
#   ReadSchema: struct<user_id:string,status:string>
#   (only 2 of 200 columns read)

# Nested column pushdown (Spark 3.0+)
spark.conf.set(
    "spark.sql.optimizer.nestedSchemaPruning.enabled", "true")

# With nested structs
df = spark.read.parquet("/data/nested/")
# Only reads address.city from the nested struct
df.select("user_id", "address.city").explain()
```

---
## Projection Pushdown Savings

![projection_pushdown_savings](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/projection_pushdown_savings.svg)

---
## Writing Parquet with PySpark

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, \
    StringType, IntegerType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("ParquetWriting") \
    .getOrCreate()

df = spark.read.parquet("/data/raw_events/")

# Basic write
df.write.parquet("/output/events/")

# Write with compression
df.write \
    .option("compression", "snappy") \
    .parquet("/output/events_snappy/")

# Write with partitioning
df.write \
    .partitionBy("event_date", "region") \
    .option("compression", "zstd") \
    .mode("overwrite") \
    .parquet("/output/events_partitioned/")

# Control row group size
spark.conf.set("spark.sql.parquet.rowGroupSize",
               str(128 * 1024 * 1024))  # 128 MB

# Control page size
spark.conf.set("spark.sql.parquet.pageSize",
               str(1024 * 1024))  # 1 MB

# Enable dictionary encoding (default: true)
spark.conf.set("spark.sql.parquet.enableDictionary", "true")

# Enable page-level column index
spark.conf.set(
    "spark.sql.parquet.columnIndex.enabled", "true")
```

---
## Compression Comparison

| Codec | Ratio | Write Speed | Read Speed | Splittable | Use Case |
|---|---|---|---|---|---|
| Snappy | ~2x | Very fast | Very fast | Yes | Default, balanced |
| GZIP | ~4x | Slow | Medium | Yes | Storage-optimized |
| ZSTD | ~3.5x | Fast | Fast | Yes | Best overall |
| LZ4 | ~2x | Very fast | Very fast | Yes | Speed-optimized |
| Uncompressed | 1x | Fastest | Fastest | Yes | Debug/testing |

---
## ORC Format Comparison

![orc_format_comparison](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/orc_format_comparison.svg)

---
## Parquet vs ORC Comparison

| Feature | Parquet | ORC |
|---|---|---|
| Origin | Twitter + Cloudera | Facebook (Hive) |
| Ecosystem fit | Spark, Impala, Dremio | Hive, Presto |
| Nested types | Excellent | Good |
| ACID support | Via Delta/Iceberg | Built-in (Hive) |
| Bloom filters | Yes (column index) | Yes (built-in) |
| Predicate pushdown | Row group + page | Stripe + row index |
| Default in Spark | Yes | No |
| Compression | Snappy/ZSTD/GZIP | ZLIB/Snappy/ZSTD |
| Schema evolution | Append columns | Append columns |
| Typical compression | Slightly better | Slightly better for Hive |
| Recommendation | Use with Spark | Use with Hive-heavy stacks |

---
## Reading and Writing ORC with PySpark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ORCExample") \
    .getOrCreate()

# Read ORC
df = spark.read.orc("/data/hive_warehouse/events/")

# Write ORC
df.write \
    .option("compression", "zstd") \
    .mode("overwrite") \
    .orc("/output/events_orc/")

# Write ORC with partitioning
df.write \
    .partitionBy("event_date") \
    .option("compression", "snappy") \
    .orc("/output/events_orc_partitioned/")

# Read ORC as table
spark.sql("""
    CREATE TABLE IF NOT EXISTS events_orc (
        user_id STRING,
        event_type STRING,
        amount DOUBLE,
        event_date STRING
    )
    STORED AS ORC
    LOCATION '/output/events_orc/'
""")

result = spark.sql("SELECT * FROM events_orc WHERE amount > 100")
result.show()
```

---
## Avro for Streaming

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("AvroStreaming") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-avro_2.12:3.5.0") \
    .getOrCreate()

# Avro: row-based format, ideal for:
# - Record-at-a-time writes (streaming)
# - Schema evolution with full/transitive compatibility
# - Kafka message serialization
# - Write-heavy workloads

# Read Avro files
df = spark.read.format("avro").load("/data/avro_events/")

# Write Avro
df.write.format("avro") \
    .option("avroSchema", open("event.avsc").read()) \
    .mode("overwrite") \
    .save("/output/events_avro/")

# Streaming with Avro from Kafka
streaming_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "events")
    .load()
)

# Deserialize Avro messages
from pyspark.sql.avro.functions import from_avro
schema_registry_url = "http://schema-registry:8081"
avro_schema = open("event.avsc").read()

parsed = streaming_df.select(
    from_avro(F.col("value"), avro_schema).alias("event")
).select("event.*")

# Write stream as Parquet (Avro in, Parquet out is common)
query = (
    parsed.writeStream
    .format("parquet")
    .option("checkpointLocation", "/checkpoints/events/")
    .option("path", "/output/streaming_events/")
    .trigger(processingTime="1 minute")
    .start()
)
```

---
## Format Selection Guide

![format_selection_guide](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/format_selection_guide.svg)

---
## Delta Lake Overview

![delta_lake_overview](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/delta_lake_overview.svg)

---
## Delta Lake: Basic Operations

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder \
    .appName("DeltaLakeBasics") \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Write as Delta
df = spark.read.parquet("/data/raw_events/")
df.write.format("delta") \
    .mode("overwrite") \
    .save("/data/delta/events/")

# Read Delta
delta_df = spark.read.format("delta").load("/data/delta/events/")

# Append new data
new_data = spark.read.parquet("/data/new_events/")
new_data.write.format("delta") \
    .mode("append") \
    .save("/data/delta/events/")

# Overwrite with replaceWhere (partial overwrite)
daily_data = spark.read.parquet("/data/daily/2024-06-15/")
daily_data.write.format("delta") \
    .mode("overwrite") \
    .option("replaceWhere", "event_date = '2024-06-15'") \
    .save("/data/delta/events/")

# Register as SQL table
spark.sql("""
    CREATE TABLE IF NOT EXISTS events
    USING DELTA
    LOCATION '/data/delta/events/'
""")
```

---
## Delta Lake: MERGE INTO

```python
from delta.tables import DeltaTable

spark = configure_spark_with_delta_pip(
    SparkSession.builder.appName("DeltaMerge")
).getOrCreate()

# Target: existing Delta table
target = DeltaTable.forPath(spark, "/data/delta/customers/")

# Source: incoming updates
updates = spark.read.parquet("/data/customer_updates/")

# MERGE: upsert pattern
target.alias("target").merge(
    updates.alias("source"),
    "target.customer_id = source.customer_id"
).whenMatchedUpdate(
    set={
        "name": "source.name",
        "email": "source.email",
        "updated_at": "source.updated_at",
    }
).whenNotMatchedInsert(
    values={
        "customer_id": "source.customer_id",
        "name": "source.name",
        "email": "source.email",
        "created_at": "source.updated_at",
        "updated_at": "source.updated_at",
    }
).execute()

# MERGE with delete condition
target.alias("t").merge(
    updates.alias("s"),
    "t.customer_id = s.customer_id"
).whenMatchedUpdate(
    condition="s.is_deleted = false",
    set={"name": "s.name", "email": "s.email"}
).whenMatchedDelete(
    condition="s.is_deleted = true"
).whenNotMatchedInsert(
    condition="s.is_deleted = false",
    values={
        "customer_id": "s.customer_id",
        "name": "s.name",
        "email": "s.email",
    }
).execute()
```

---
## Delta Lake: MERGE with SQL

```python
# SQL syntax for MERGE
spark.sql("""
    MERGE INTO customers AS target
    USING customer_updates AS source
    ON target.customer_id = source.customer_id

    WHEN MATCHED AND source.is_deleted = true THEN
        DELETE

    WHEN MATCHED THEN UPDATE SET
        target.name = source.name,
        target.email = source.email,
        target.updated_at = source.updated_at

    WHEN NOT MATCHED THEN INSERT (
        customer_id, name, email, created_at, updated_at
    ) VALUES (
        source.customer_id,
        source.name,
        source.email,
        source.updated_at,
        source.updated_at
    )
""")

# Check merge metrics
history = spark.sql("DESCRIBE HISTORY customers LIMIT 1")
history.select(
    "version", "timestamp", "operation",
    "operationMetrics"
).show(truncate=False)
```

---
## Delta Lake: Time Travel

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DeltaTimeTravel") \
    .getOrCreate()

# Read a specific version
df_v0 = (
    spark.read.format("delta")
    .option("versionAsOf", 0)
    .load("/data/delta/events/")
)

# Read at a specific timestamp
df_ts = (
    spark.read.format("delta")
    .option("timestampAsOf", "2024-06-01T00:00:00Z")
    .load("/data/delta/events/")
)

# SQL syntax
spark.sql("""
    SELECT * FROM events VERSION AS OF 5
""")

spark.sql("""
    SELECT * FROM events TIMESTAMP AS OF '2024-06-01'
""")

# Compare two versions (audit / debugging)
df_old = spark.read.format("delta") \
    .option("versionAsOf", 10).load("/data/delta/events/")
df_new = spark.read.format("delta") \
    .option("versionAsOf", 15).load("/data/delta/events/")

print(f"Version 10 count: {df_old.count()}")
print(f"Version 15 count: {df_new.count()}")
print(f"Rows added: {df_new.count() - df_old.count()}")

# View table history
history = spark.sql("DESCRIBE HISTORY events")
history.select(
    "version", "timestamp", "operation",
    "operationParameters"
).show(20, truncate=False)
```

---
## Delta Lake: VACUUM and Maintenance

```python
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("DeltaMaintenance") \
    .getOrCreate()

delta_table = DeltaTable.forPath(spark, "/data/delta/events/")

# VACUUM: remove old files no longer referenced
# Default retention: 7 days (168 hours)
delta_table.vacuum(168)  # hours

# WARNING: shorter retention breaks time travel
# Only reduce if you understand the implications
spark.conf.set(
    "spark.databricks.delta.retentionDurationCheck.enabled",
    "false")
delta_table.vacuum(24)  # 24 hours - careful!

# SQL syntax
spark.sql("VACUUM events RETAIN 168 HOURS")

# OPTIMIZE: compact small files
spark.sql("OPTIMIZE events")

# OPTIMIZE with Z-ordering
# Z-ordering co-locates related data for filter efficiency
spark.sql("""
    OPTIMIZE events
    ZORDER BY (user_id, event_date)
""")

# Z-ordering effect on query performance:
# Before Z-ORDER: filter reads 80% of files
# After Z-ORDER:  filter reads 10% of files

# Check table details
spark.sql("DESCRIBE DETAIL events").show(truncate=False)

# Restore a previous version
delta_table.restoreToVersion(5)
# Or by timestamp
delta_table.restoreToTimestamp("2024-06-01")
```

---
## Z-Ordering Visualization

![z_ordering_visualization](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/z_ordering_visualization.svg)

---
## Apache Iceberg Overview

![apache_iceberg_overview](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/apache_iceberg_overview.svg)

---
## Iceberg vs Delta Lake

| Feature | Delta Lake | Apache Iceberg |
|---|---|---|
| Origin | Databricks | Netflix |
| License | Apache 2.0 | Apache 2.0 |
| ACID transactions | Yes | Yes |
| Time travel | Yes | Yes |
| Schema evolution | Yes | Yes (richer) |
| Partition evolution | No (rewrite) | Yes (in-place) |
| Hidden partitioning | No | Yes |
| Engine support | Spark (best), others | Spark, Flink, Trino, Presto |
| Catalog support | Unity Catalog | HMS, Glue, REST, Nessie |
| File formats | Parquet only | Parquet, ORC, Avro |
| Merge-on-read | Yes | Yes |
| Copy-on-write | Yes | Yes |
| Vendor lock-in | Low-medium | Low |

---
## Iceberg with PySpark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IcebergExample") \
    .config("spark.sql.extensions",
            "org.apache.iceberg.spark.extensions."
            "IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.my_catalog",
            "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.my_catalog.type", "hadoop") \
    .config("spark.sql.catalog.my_catalog.warehouse",
            "/data/iceberg/warehouse") \
    .getOrCreate()

# Create table
spark.sql("""
    CREATE TABLE my_catalog.db.events (
        event_id STRING,
        user_id STRING,
        event_type STRING,
        amount DOUBLE,
        event_ts TIMESTAMP
    )
    USING iceberg
    PARTITIONED BY (days(event_ts))
""")

# Note: days(event_ts) is "hidden partitioning"
# Users query by event_ts, Iceberg handles partition mapping

# Insert data
spark.sql("""
    INSERT INTO my_catalog.db.events
    SELECT * FROM raw_events
""")

# Time travel
spark.sql("""
    SELECT * FROM my_catalog.db.events
    VERSION AS OF 2
""")

# Partition evolution (change partitioning without rewrite)
spark.sql("""
    ALTER TABLE my_catalog.db.events
    ADD PARTITION FIELD hours(event_ts)
""")
```

---
## Partitioning Strategies

![partitioning_strategies](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/partitioning_strategies.svg)

---
## Partitioning Implementation

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("PartitioningStrategies") \
    .getOrCreate()

df = spark.read.parquet("/data/raw_events/")

# Range partitioning by date
df.write \
    .partitionBy("event_date") \
    .mode("overwrite") \
    .parquet("/output/events_by_date/")

# Multi-level partitioning
df.write \
    .partitionBy("event_date", "region") \
    .mode("overwrite") \
    .parquet("/output/events_by_date_region/")

# Hash partitioning (manual)
num_buckets = 32
df_hashed = df.withColumn(
    "user_bucket",
    F.abs(F.hash(F.col("user_id"))) % num_buckets
)
df_hashed.write \
    .partitionBy("user_bucket") \
    .mode("overwrite") \
    .parquet("/output/events_hashed/")

# Dynamic partition overwrite (only overwrite touched partitions)
spark.conf.set(
    "spark.sql.sources.partitionOverwriteMode", "dynamic")
df.write \
    .partitionBy("event_date") \
    .mode("overwrite") \
    .parquet("/output/events_by_date/")
```

---
## Partitioning Best Practices

![partitioning_best_practices](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/partitioning_best_practices.svg)

---
## Bucketing vs Partitioning

![bucketing_vs_partitioning](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/bucketing_vs_partitioning.svg)

---
## Bucketing Implementation

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BucketingExample") \
    .getOrCreate()

orders = spark.read.parquet("/data/orders/")
customers = spark.read.parquet("/data/customers/")

# Write bucketed tables
orders.write \
    .bucketBy(32, "customer_id") \
    .sortBy("customer_id") \
    .mode("overwrite") \
    .saveAsTable("orders_bucketed")

customers.write \
    .bucketBy(32, "customer_id") \
    .sortBy("customer_id") \
    .mode("overwrite") \
    .saveAsTable("customers_bucketed")

# Join on bucketed tables: NO SHUFFLE needed
# Both tables have same bucket count and key
result = spark.sql("""
    SELECT o.*, c.name, c.region
    FROM orders_bucketed o
    JOIN customers_bucketed c
    ON o.customer_id = c.customer_id
""")

# Verify no exchange (shuffle) in the plan
result.explain()
# Should show: SortMergeJoin without Exchange

# Combined: partition by date, bucket by user
orders.write \
    .partitionBy("order_date") \
    .bucketBy(32, "customer_id") \
    .sortBy("customer_id") \
    .mode("overwrite") \
    .saveAsTable("orders_part_bucketed")
```

---
## The Small File Problem

**Cause**: streaming or frequent appends create many tiny files

```tree
/data/events/date=2024-06-15/
├── part-00000.parquet  (2 KB)
├── part-00001.parquet  (3 KB)
├── part-00002.parquet  (1 KB)
├── part-00003.parquet  (4 KB)
├── ... (10,000 tiny files)
└── part-09999.parquet  (2 KB)
```

**Problems:**
* Slow reads: metadata overhead per file
* HDFS/S3 listing bottleneck
* NameNode memory pressure (HDFS)
* High API cost (S3)
* Poor predicate pushdown (stats per file)

---
## Solving the Small File Problem

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("FileCompaction") \
    .getOrCreate()

# Method 1: Coalesce before writing
df = spark.read.parquet("/data/small_files/")
target_size_mb = 128
total_size_mb = 5000  # estimated
target_files = max(1, total_size_mb // target_size_mb)

df.coalesce(target_files) \
    .write.mode("overwrite") \
    .parquet("/data/compacted/")

# Method 2: Repartition for even distribution
df.repartition(target_files) \
    .write.mode("overwrite") \
    .parquet("/data/compacted/")

# Method 3: Delta Lake OPTIMIZE (best approach)
spark.sql("OPTIMIZE events")

# Method 4: Auto-compaction (Delta Lake)
spark.conf.set(
    "spark.databricks.delta.autoCompact.enabled", "true")
spark.conf.set(
    "spark.databricks.delta.autoCompact.minNumFiles", "50")

# Method 5: Optimized writes (Delta Lake)
spark.conf.set(
    "spark.databricks.delta.optimizeWrite.enabled", "true")

# Method 6: Compaction job (scheduled)
def compact_partition(table_path, partition_col, partition_val):
    """Compact a single partition of a Parquet table."""
    partition_path = (
        f"{table_path}/{partition_col}={partition_val}")
    df = spark.read.parquet(partition_path)
    row_count = df.count()
    target_files = max(1, row_count // 1_000_000)

    df.coalesce(target_files) \
        .write.mode("overwrite") \
        .parquet(f"/tmp/compacted/{partition_val}")

    # Move compacted files back
    # (use hadoop fs -mv in production)
    return target_files

# Compact yesterday's partition
compact_partition("/data/events", "event_date", "2024-06-14")
```

---
## File Compaction Strategy

![file_compaction_strategy](svg/courses/big_data/advanced-spark-with-python/08_data_formats_and_storage/file_compaction_strategy.svg)

---
## Full Program: Data Format Pipeline

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, \
    StringType, DoubleType, TimestampType
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("DataFormatPipeline") \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.parquet.columnIndex.enabled", "true") \
    .config("spark.sql.parquet.filterPushdown", "true") \
    .getOrCreate()

# Stage 1: Ingest raw data (CSV/JSON to Parquet)
schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("user_id", StringType(), False),
    StructField("event_type", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("event_ts", TimestampType(), True),
])

raw = spark.read.schema(schema).json("/data/raw/events/")
raw = raw.withColumn(
    "event_date", F.to_date("event_ts"))

# Stage 2: Write as Delta with partitioning
raw.write.format("delta") \
    .partitionBy("event_date") \
    .option("compression", "zstd") \
    .mode("append") \
    .save("/data/delta/events/")

# Stage 3: MERGE incremental updates
target = DeltaTable.forPath(spark, "/data/delta/events/")
updates = spark.read.schema(schema).json(
    "/data/raw/event_updates/")
updates = updates.withColumn(
    "event_date", F.to_date("event_ts"))

target.alias("t").merge(
    updates.alias("s"),
    "t.event_id = s.event_id AND "
    "t.event_date = s.event_date"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

# Stage 4: Optimize storage
spark.sql("""
    OPTIMIZE delta.`/data/delta/events/`
    ZORDER BY (user_id)
""")

# Stage 5: Clean up old versions
target.vacuum(168)  # retain 7 days

# Stage 6: Verify table health
detail = spark.sql("""
    DESCRIBE DETAIL delta.`/data/delta/events/`
""").collect()[0]

print(f"Table size: {detail['sizeInBytes'] / 1e9:.2f} GB")
print(f"Num files: {detail['numFiles']}")
print(f"Avg file size: "
      f"{detail['sizeInBytes']/detail['numFiles']/1e6:.1f} MB")

history = spark.sql("""
    DESCRIBE HISTORY delta.`/data/delta/events/`
    LIMIT 5
""")
history.select(
    "version", "timestamp", "operation"
).show()
```

---
## Summary: Data Formats and Storage

**Formats:**
* Parquet: default for analytics, columnar
* ORC: alternative for Hive-centric stacks
* Avro: row-based, streaming, schema evolution
* Delta / Iceberg: ACID on top of Parquet

**Optimization:**
* Predicate pushdown: filter at storage layer
* Projection pushdown: read only needed columns
* Z-ordering: co-locate data for better pruning
* Compression: ZSTD best overall balance

**Storage Management:**
* Partition by query pattern (low cardinality)
* Bucket by join key (high cardinality)
* Compact small files regularly
