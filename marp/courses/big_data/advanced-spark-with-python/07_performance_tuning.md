# Performance Tuning and Optimization
---
## Chapter Overview
* Spark UI interpretation and DAG visualization
* Shuffle optimization and partition tuning
* Memory management and configuration
* Data skew detection and handling
* Adaptive Query Execution (AQE)
* Caching strategies and storage levels
---
## Learning Objectives
* Read and interpret the Spark Web UI
* Diagnose performance bottlenecks from DAGs and metrics
* Configure memory, shuffle, and partition settings
* Handle data skew with salting and broadcast joins
* Leverage AQE for automatic runtime optimization
* Choose the right caching strategy for each workload
---
## The Spark Web UI
1. Jobs tab: shows all jobs triggered by actions
1. Stages tab: shows stages within each job
1. Storage tab: shows cached/persisted RDDs and DataFrames
1. Environment tab: shows all Spark configuration
1. Executors tab: shows executor memory, GC, shuffle metrics
1. SQL tab: shows query plans and execution statistics
---
## Spark UI: Key Metrics to Watch

| Metric | Where to Find | What it Tells You |
|---|---|---|
| Task Duration | Stages tab | Skew if max >> median |
| Shuffle Read/Write | Stages tab | Excessive data movement |
| GC Time | Executors tab | Memory pressure |
| Spill (Memory/Disk) | Stages tab | Insufficient memory |
| Input Size | Stages tab | Data volume per stage |
| Scheduler Delay | Tasks tab | Cluster overhead |
| Peak Execution Memory | SQL tab | Memory consumption |
---
## Understanding the DAG

![understanding_the_dag](/svg/courses/big_data/advanced-spark-with-python/07_performance_tuning/understanding_the_dag.svg)

---
## Reading Execution Plans

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("ExecutionPlanAnalysis") \
    .getOrCreate()

df = spark.read.parquet("/data/events/")

query = (
    df.filter(F.col("event_type") == "purchase")
    .groupBy("user_id")
    .agg(F.sum("amount").alias("total"))
    .filter(F.col("total") > 1000)
)

# Simple plan (physical only)
query.explain()

# Extended plan (all phases)
query.explain(mode="extended")

# Formatted plan (tree with details)
query.explain(mode="formatted")

# Cost plan (with statistics)
query.explain(mode="cost")

# Codegen plan (generated Java code)
query.explain(mode="codegen")
```

---
## Execution Plan Key Operators

| Operator | Symbol | Meaning |
|---|---|---|
| FileScan | Scan parquet | Reading from storage |
| Filter | Filter | Row-level predicate |
| Project | Project | Column selection |
| Exchange | Exchange hashpartitioning | Shuffle |
| HashAggregate | HashAggregate | Aggregation |
| BroadcastHashJoin | BroadcastHashJoin | Broadcast join |
| SortMergeJoin | SortMergeJoin | Sort-merge join |
| WholeStageCodegen | WholeStageCodegen | Fused code generation |
---
## Shuffle Deep Dive

![shuffle_deep_dive](/svg/courses/big_data/advanced-spark-with-python/07_performance_tuning/shuffle_deep_dive.svg)

---
## Shuffle Configuration

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ShuffleOptimization") \
    .getOrCreate()

# Number of partitions after shuffle (default: 200)
# Too few: large partitions, OOM risk
# Too many: small tasks, scheduling overhead
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Rule of thumb: target 128MB per partition
# If total shuffle data = 50GB:
#   50GB / 128MB = ~400 partitions
spark.conf.set("spark.sql.shuffle.partitions", "400")

# Shuffle compression (always enable)
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.shuffle.spill.compress", "true")

# Shuffle manager
spark.conf.set("spark.shuffle.manager", "sort")

# Shuffle file buffer
spark.conf.set("spark.shuffle.file.buffer", "64k")

# Shuffle fetch settings
spark.conf.set("spark.reducer.maxSizeInFlight", "96m")
spark.conf.set("spark.shuffle.io.maxRetries", "10")
spark.conf.set("spark.shuffle.io.retryWait", "60s")

# External shuffle service (for dynamic allocation)
spark.conf.set("spark.shuffle.service.enabled", "true")
```

---
## Partition Tuning Guide

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("PartitionTuning") \
    .getOrCreate()

df = spark.read.parquet("/data/large_dataset/")

# Check current partitioning
print(f"Number of partitions: {df.rdd.getNumPartitions()}")

# Check partition sizes
partition_sizes = (
    df.withColumn("partition_id", F.spark_partition_id())
    .groupBy("partition_id")
    .agg(F.count("*").alias("row_count"))
)
stats = partition_sizes.agg(
    F.min("row_count").alias("min_rows"),
    F.max("row_count").alias("max_rows"),
    F.avg("row_count").alias("avg_rows"),
    F.stddev("row_count").alias("stddev_rows"),
).collect()[0]

print(f"Min rows/partition:    {stats['min_rows']}")
print(f"Max rows/partition:    {stats['max_rows']}")
print(f"Avg rows/partition:    {stats['avg_rows']:.0f}")
print(f"Stddev rows/partition: {stats['stddev_rows']:.0f}")

# Repartition for balanced parallelism
# Target: 128MB per partition, ~1M rows per partition
target_partitions = max(1, int(df.count() / 1_000_000))
df_balanced = df.repartition(target_partitions)

# Coalesce: reduce partitions without full shuffle
# Use when reducing partition count (e.g., before writing)
df_coalesced = df.coalesce(10)

# Repartition by column: co-locate data for downstream joins
df_by_key = df.repartition(100, "user_id")
```

---
## Partition Size Guidelines

| Partition Size | Status | Action |
|---|---|---|
| < 10 MB | Too small | Coalesce partitions |
| 10 - 50 MB | Small | Consider coalescing |
| 50 - 200 MB | Optimal | No action needed |
| 200 - 500 MB | Large | Consider repartitioning |
| > 500 MB | Too large | Repartition urgently |
| > 2 GB | Critical | Will likely OOM |
---
## Memory Architecture

![memory_architecture](/svg/courses/big_data/advanced-spark-with-python/07_performance_tuning/memory_architecture.svg)

---
## Memory Configuration Guide

```python
# Executor memory (JVM heap)
spark.conf.set("spark.executor.memory", "8g")

# Memory overhead (off-heap, container overhead)
# Default: max(384MB, 0.1 * executor.memory)
# Increase for PySpark (Python processes need memory)
spark.conf.set("spark.executor.memoryOverhead", "2g")

# PySpark memory (Python worker memory)
# Default: 512m; increase for heavy pandas/numpy usage
spark.conf.set("spark.executor.pyspark.memory", "1g")

# Spark memory fraction (of JVM heap)
spark.conf.set("spark.memory.fraction", "0.6")

# Storage fraction (within Spark memory)
# Lower = more for execution, less for caching
spark.conf.set("spark.memory.storageFraction", "0.5")

# Off-heap memory (optional, bypasses GC)
spark.conf.set("spark.memory.offHeap.enabled", "true")
spark.conf.set("spark.memory.offHeap.size", "4g")

# Driver memory
spark.conf.set("spark.driver.memory", "4g")
spark.conf.set("spark.driver.memoryOverhead", "1g")
spark.conf.set("spark.driver.maxResultSize", "2g")
```

---
## Memory Tuning Scenarios

| Symptom | Likely Cause | Fix |
|---|---|---|
| OOM on executor | Partition too large | Increase partitions or memory |
| OOM on driver | collect() too large | Use take() or write to file |
| Excessive GC time | Too much cached data | Reduce cache, increase memory |
| Shuffle spill to disk | Insufficient execution memory | Increase memory fraction |
| Python worker OOM | Heavy pandas/numpy | Increase pyspark.memory |
| Container killed by YARN | Memory overhead too low | Increase memoryOverhead |
---
## Data Skew Detection

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("SkewDetection") \
    .getOrCreate()

df = spark.read.parquet("/data/transactions/")

# Method 1: Check key distribution
key_distribution = (
    df.groupBy("customer_id")
    .count()
    .orderBy("count", ascending=False)
)

# Top 10 heaviest keys
print("Top 10 keys by count:")
key_distribution.show(10)

# Skew statistics
stats = key_distribution.agg(
    F.count("*").alias("num_keys"),
    F.sum("count").alias("total_rows"),
    F.max("count").alias("max_key_count"),
    F.avg("count").alias("avg_key_count"),
    F.percentile_approx("count", 0.5).alias("median_count"),
    F.percentile_approx("count", 0.99).alias("p99_count"),
).collect()[0]

skew_ratio = stats["max_key_count"] / stats["avg_key_count"]
print(f"\nSkew Analysis:")
print(f"  Total keys:     {stats['num_keys']}")
print(f"  Total rows:     {stats['total_rows']}")
print(f"  Max key count:  {stats['max_key_count']}")
print(f"  Avg key count:  {stats['avg_key_count']:.1f}")
print(f"  Median count:   {stats['median_count']}")
print(f"  P99 count:      {stats['p99_count']}")
print(f"  Skew ratio:     {skew_ratio:.1f}x")
print(f"  Skewed?:        {'YES' if skew_ratio > 5 else 'NO'}")

# Method 2: Check partition-level skew
partition_stats = (
    df.withColumn("part_id", F.spark_partition_id())
    .groupBy("part_id")
    .count()
)
partition_stats.describe().show()
```

---
## Data Skew Solutions

```diagram
Solution 1: Salting (for joins)
┌────────────────────────────────────────────┐
│  Original key: "hot_user_123"               │
│  Records: 10,000,000                        │
│                                            │
│  Salted keys (salt_factor = 10):            │
│  "hot_user_123_0" -> 1,000,000 records      │
│  "hot_user_123_1" -> 1,000,000 records      │
│  "hot_user_123_2" -> 1,000,000 records      │
│  ...                                        │
│  "hot_user_123_9" -> 1,000,000 records      │
│                                            │
│  Small table must be exploded with          │
│  all salt values (0-9) to match.            │
└────────────────────────────────────────────┘
```

---
## Full Program: Salted Join for Skewed Data

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("SaltedJoin") \
    .getOrCreate()

SALT_FACTOR = 10

# Large table with skewed key
large_df = spark.read.parquet("/data/transactions/")

# Small dimension table
small_df = spark.read.parquet("/data/customers/")

# Step 1: Add random salt to large table
salted_large = large_df.withColumn(
    "salt", (F.rand() * SALT_FACTOR).cast("int")
).withColumn(
    "salted_key",
    F.concat(F.col("customer_id").cast("string"),
             F.lit("_"), F.col("salt").cast("string"))
)

# Step 2: Explode small table with all salt values
salt_values = spark.range(0, SALT_FACTOR).toDF("salt")
exploded_small = (
    small_df.crossJoin(salt_values)
    .withColumn(
        "salted_key",
        F.concat(F.col("customer_id").cast("string"),
                 F.lit("_"), F.col("salt").cast("string"))
    )
)

# Step 3: Join on salted key (balanced partitions)
result = salted_large.join(
    exploded_small,
    "salted_key",
    "inner"
).drop("salt", "salted_key")

# Verify balanced partitions
result.withColumn("pid", F.spark_partition_id()) \
    .groupBy("pid").count() \
    .agg(F.max("count"), F.min("count"), F.avg("count")) \
    .show()
```

---
## Broadcast Join for Skew Avoidance

```python
from pyspark.sql.functions import broadcast

# If the small table fits in memory, broadcast it
# This completely avoids shuffle on the large table

# Check if broadcast is feasible
small_size_mb = small_df.count() * 100 / (1024 * 1024)  # Rough estimate
print(f"Small table approx size: {small_size_mb:.1f} MB")

if small_size_mb < 500:  # Safe threshold
    result = large_df.join(
        broadcast(small_df),
        "customer_id"
    )
    print("Using broadcast join (no shuffle)")
else:
    # Fall back to salted join
    print("Table too large for broadcast, using salted join")

# Force broadcast even above threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "500m")

# Verify join strategy
result.explain()
```

---
## Adaptive Query Execution (AQE) Configuration

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("AQEConfiguration") \
    .getOrCreate()

# Enable AQE (default: true in Spark 3.2+)
spark.conf.set("spark.sql.adaptive.enabled", "true")

# === Feature 1: Coalesce Shuffle Partitions ===
# Merges small post-shuffle partitions
spark.conf.set(
    "spark.sql.adaptive.coalescePartitions.enabled", "true")
# Target partition size after coalescing
spark.conf.set(
    "spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")
# Minimum partition size to prevent too-small partitions
spark.conf.set(
    "spark.sql.adaptive.coalescePartitions.minPartitionSize", "1MB")
# Initial shuffle partition count (set high, AQE will reduce)
spark.conf.set(
    "spark.sql.adaptive.coalescePartitions.initialPartitionNum", "2000")

# === Feature 2: Skew Join Optimization ===
# Automatically splits skewed partitions during joins
spark.conf.set(
    "spark.sql.adaptive.skewJoin.enabled", "true")
# A partition is skewed if it is N times the median
spark.conf.set(
    "spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
# AND its size exceeds this threshold
spark.conf.set(
    "spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# === Feature 3: Dynamic Join Strategy ===
# Switch to broadcast join at runtime if one side is small
spark.conf.set(
    "spark.sql.adaptive.autoBroadcastJoinThreshold", "10MB")

# === Feature 4: Dynamic Partition Pruning ===
spark.conf.set(
    "spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")
spark.conf.set(
    "spark.sql.optimizer.dynamicPartitionPruning.reuseBroadcastOnly", "true")
```

---
## AQE: How It Works

![aqe_how_it_works](/svg/courses/big_data/advanced-spark-with-python/07_performance_tuning/aqe_how_it_works.svg)

---
## Dynamic Partition Pruning (DPP)

```python
# DPP eliminates partitions at runtime based on join filters

# Scenario: fact table partitioned by date, join with date filter
# on dimension table

# Fact table: partitioned by event_date
fact_df = spark.read.parquet("/data/events/")  # partitioned by event_date

# Dimension table with filter
dim_df = spark.read.parquet("/data/campaigns/")
active_campaigns = dim_df.filter(
    F.col("start_date") >= "2024-01-01"
)

# DPP allows Spark to prune fact table partitions
# based on the dimension filter at runtime
result = fact_df.join(
    active_campaigns,
    fact_df.campaign_id == active_campaigns.campaign_id
)

# Without DPP: scans ALL event_date partitions
# With DPP: scans only partitions matching campaign dates

result.explain()
# Look for "DynamicPruningExpression" in the plan
```

---
## Full Program: Caching Strategy

```python
from pyspark.sql import SparkSession
from pyspark import StorageLevel
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("CachingStrategy") \
    .getOrCreate()

# Scenario: same DataFrame used in multiple downstream queries

# Step 1: Expensive base transformation
base_df = (
    spark.read.parquet("/data/raw_events/")
    .filter(F.col("event_date") >= "2024-01-01")
    .withColumn("hour", F.hour("timestamp"))
    .withColumn("is_weekend",
        F.dayofweek("event_date").isin([1, 7]))
)

# Step 2: Cache since it is used multiple times
base_df.cache()
# Force materialization (lazy otherwise)
print(f"Cached {base_df.count()} rows")

# Step 3: Multiple downstream queries use the cached data
hourly_counts = base_df.groupBy("hour").count()
hourly_counts.show()

weekend_stats = base_df.filter("is_weekend").groupBy("event_type").agg(
    F.count("*").alias("count"),
    F.avg("value").alias("avg_value"),
)
weekend_stats.show()

# Step 4: When done, unpersist to free memory
base_df.unpersist()
```

---
## cache() vs persist() vs checkpoint()

| Method | Storage | Lineage | Recovery | Use Case |
|---|---|---|---|---|
| cache() | MEMORY_AND_DISK | Preserved | Recompute from source | Reusable intermediate |
| persist(level) | Configurable | Preserved | Recompute from source | Control storage level |
| checkpoint() | Disk only | Truncated | Read from checkpoint | Break long lineage |
| localCheckpoint() | Disk (local) | Truncated | Lost if executor dies | Fast, less reliable |
---
## When to Cache and When Not To

```diagram
CACHE when:
┌──────────────────────────────────────────┐
│  * DataFrame used in 2+ actions           │
│  * Computation is expensive (joins, aggs) │
│  * Data fits in memory (or mostly)        │
│  * Iterative algorithms (ML training)     │
│  * Interactive exploration (notebooks)    │
└──────────────────────────────────────────┘

DO NOT CACHE when:
┌──────────────────────────────────────────┐
│  * DataFrame used only once               │
│  * Data is too large for memory           │
│  * Source read is fast (e.g., small file) │
│  * Memory is scarce for execution         │
│  * Data changes between uses              │
└──────────────────────────────────────────┘
```

---
## Storage Level Selection Guide

```python
from pyspark import StorageLevel

# MEMORY_ONLY: fastest, but evicts if not enough memory
df.persist(StorageLevel.MEMORY_ONLY)

# MEMORY_AND_DISK: safe default, spills to disk
df.persist(StorageLevel.MEMORY_AND_DISK)
# Equivalent to df.cache()

# MEMORY_ONLY_SER: serialized, 2-5x less memory, slower access
df.persist(StorageLevel.MEMORY_ONLY_SER)

# MEMORY_AND_DISK_SER: serialized with disk spillover
df.persist(StorageLevel.MEMORY_AND_DISK_SER)

# DISK_ONLY: when memory is scarce, recomputation is expensive
df.persist(StorageLevel.DISK_ONLY)

# _2 variants: replication for fault tolerance
df.persist(StorageLevel.MEMORY_AND_DISK_2)

# Check what is cached
for (rdd_id, rdd) in spark.sparkContext._jsc.sc().getRDDStorageInfo():
    print(f"RDD {rdd_id}: {rdd.memSize()} bytes in memory, "
          f"{rdd.diskSize()} bytes on disk")

# Or use Spark UI -> Storage tab
```

---
## Full Program: Complete Performance Tuning Session

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time

spark = SparkSession.builder \
    .appName("PerformanceTuningSession") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.memoryOverhead", "2g") \
    .config("spark.executor.cores", "4") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.serializer",
            "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()

# Read large dataset
orders = spark.read.parquet("/data/orders/")
customers = spark.read.parquet("/data/customers/")
products = spark.read.parquet("/data/products/")

# ---- Optimization 1: Filter before join ----
start = time.time()
filtered_orders = orders.filter(
    (F.col("order_date") >= "2024-01-01") &
    (F.col("status") == "completed")
)
print(f"Filtered orders: {filtered_orders.count()} "
      f"(from {orders.count()})")
print(f"  Reduced dataset by "
      f"{(1 - filtered_orders.count()/orders.count())*100:.0f}%")

# ---- Optimization 2: Broadcast small table ----
from pyspark.sql.functions import broadcast
products_small = products.select("product_id", "category", "price")
enriched = filtered_orders.join(
    broadcast(products_small), "product_id"
)

# ---- Optimization 3: Select only needed columns ----
projected = enriched.select(
    "order_id", "customer_id", "order_date",
    "category", "price", "quantity"
).withColumn("revenue", F.col("price") * F.col("quantity"))

# ---- Optimization 4: Cache for multiple aggregations ----
projected.cache()
projected.count()

# Aggregation 1: Revenue by category
revenue_by_cat = projected.groupBy("category").agg(
    F.sum("revenue").alias("total_revenue"),
    F.count("*").alias("order_count"),
)
revenue_by_cat.show()

# Aggregation 2: Revenue by customer
revenue_by_cust = projected.groupBy("customer_id").agg(
    F.sum("revenue").alias("total_revenue"),
    F.avg("revenue").alias("avg_order_value"),
)

# Join with customer info
final = revenue_by_cust.join(
    broadcast(customers.select("customer_id", "name", "region")),
    "customer_id"
)

# ---- Optimization 5: Coalesce before write ----
final.coalesce(10).write \
    .mode("overwrite") \
    .parquet("/output/customer_revenue/")

projected.unpersist()
total_time = time.time() - start
print(f"\nTotal pipeline time: {total_time:.2f}s")
```

---
## Performance Tuning Checklist

```diagram
┌──────────────────────────────────────────────┐
│       Performance Tuning Checklist            │
├──────────────────────────────────────────────┤
│                                              │
│  Before Running:                             │
│  [ ] Set appropriate executor memory          │
│  [ ] Set executor cores (2-5 per executor)    │
│  [ ] Enable AQE                              │
│  [ ] Set shuffle partitions                   │
│  [ ] Enable Kryo serialization                │
│                                              │
│  Data Reading:                               │
│  [ ] Use columnar formats (Parquet)           │
│  [ ] Define schema explicitly                 │
│  [ ] Use partition pruning                    │
│  [ ] Push predicates to source                │
│                                              │
│  Transformations:                             │
│  [ ] Filter early, select early               │
│  [ ] Avoid UDFs (use built-in functions)      │
│  [ ] Broadcast small tables in joins          │
│  [ ] Handle data skew                         │
│  [ ] Cache reused DataFrames                  │
│                                              │
│  Writing:                                    │
│  [ ] Coalesce before writing                  │
│  [ ] Partition output by query pattern        │
│  [ ] Use dynamic partition overwrite          │
│  [ ] Choose appropriate compression           │
│                                              │
│  Monitoring:                                 │
│  [ ] Check Spark UI for skew                  │
│  [ ] Check GC time per executor               │
│  [ ] Check shuffle spill metrics              │
│  [ ] Check task duration distribution         │
│                                              │
└──────────────────────────────────────────────┘
```

---
## Common Performance Anti-Patterns

| Anti-Pattern | Impact | Better Approach |
|---|---|---|
| collect() on large DataFrame | Driver OOM | Use take(n) or write to storage |
| groupByKey() on RDDs | Full shuffle of values | reduceByKey() or aggregateByKey() |
| Python UDFs | 10-100x slower | Built-in functions or pandas_udf |
| SELECT * | No column pruning | Select only needed columns |
| count() for existence check | Full scan | take(1) or head(1) |
| Repeated reading same data | Multiple I/O operations | cache() or persist() |
| Too many small files | Slow reads | coalesce or repartition before write |
| Default shuffle partitions | Poor parallelism | Tune to data size |
