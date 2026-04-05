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

<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-dag" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <text x="310" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">DAG: Join + Aggregation</text>
  <!-- Stage 0 -->
  <rect x="20" y="30" width="570" height="70" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="50" y="48" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#0277bd">Stage 0: Scan Table A</text>
  <rect x="40" y="55" width="100" height="35" rx="6" fill="#fff" stroke="#0277bd" stroke-width="1.5"/>
  <text x="90" y="70" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">FileScan</text>
  <text x="90" y="82" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">Parquet</text>
  <line x1="140" y1="72" x2="180" y2="72" stroke="#333" stroke-width="2" marker-end="url(#arrow-dag)"/>
  <rect x="185" y="55" width="120" height="35" rx="6" fill="#fff" stroke="#0277bd" stroke-width="1.5"/>
  <text x="245" y="70" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Filter</text>
  <text x="245" y="82" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">(pushdown)</text>
  <line x1="305" y1="72" x2="345" y2="72" stroke="#333" stroke-width="2" marker-end="url(#arrow-dag)"/>
  <rect x="350" y="55" width="120" height="35" rx="6" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="410" y="77" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">ShuffleWrite</text>
  <!-- Stage 1 -->
  <rect x="20" y="115" width="570" height="70" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="50" y="133" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#2e7d32">Stage 1: Scan Table B</text>
  <rect x="40" y="140" width="100" height="35" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="90" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">FileScan</text>
  <text x="90" y="167" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">Parquet</text>
  <line x1="140" y1="157" x2="180" y2="157" stroke="#333" stroke-width="2" marker-end="url(#arrow-dag)"/>
  <rect x="185" y="140" width="100" height="35" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="235" y="162" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Select</text>
  <line x1="285" y1="157" x2="345" y2="157" stroke="#333" stroke-width="2" marker-end="url(#arrow-dag)"/>
  <rect x="350" y="140" width="120" height="35" rx="6" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="410" y="162" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">ShuffleWrite</text>
  <!-- Stage 2 -->
  <rect x="20" y="200" width="570" height="70" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="50" y="218" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#7b1fa2">Stage 2: Join + Aggregate</text>
  <rect x="40" y="225" width="120" height="35" rx="6" fill="#fff" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="100" y="240" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">ShuffleRead</text>
  <text x="100" y="252" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">(both sides)</text>
  <line x1="160" y1="242" x2="200" y2="242" stroke="#333" stroke-width="2" marker-end="url(#arrow-dag)"/>
  <rect x="205" y="225" width="100" height="35" rx="6" fill="#fff" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="255" y="247" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Join</text>
  <line x1="305" y1="242" x2="345" y2="242" stroke="#333" stroke-width="2" marker-end="url(#arrow-dag)"/>
  <rect x="350" y="225" width="120" height="35" rx="6" fill="#fff" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="410" y="247" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Aggregate</text>
</svg>

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

<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-sh" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <text x="310" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0277bd">Writer Side (Map stage)</text>
  <rect x="30" y="25" width="560" height="150" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="50" y="42" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Executor</text>
  <rect x="50" y="50" width="110" height="35" rx="6" fill="#fff" stroke="#0277bd" stroke-width="1.5"/>
  <text x="105" y="72" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Task (process)</text>
  <line x1="160" y1="67" x2="200" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrow-sh)"/>
  <rect x="205" y="50" width="200" height="35" rx="6" fill="#fff" stroke="#0277bd" stroke-width="1.5"/>
  <text x="305" y="65" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Sort by partition key</text>
  <text x="305" y="78" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">+ spill to disk</text>
  <line x1="250" y1="85" x2="130" y2="115" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-sh)"/>
  <line x1="305" y1="85" x2="305" y2="115" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-sh)"/>
  <line x1="360" y1="85" x2="480" y2="115" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-sh)"/>
  <rect x="70" y="120" width="120" height="35" rx="6" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="130" y="142" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Part 0 file</text>
  <rect x="245" y="120" width="120" height="35" rx="6" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="305" y="142" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Part 1 file</text>
  <rect x="420" y="120" width="120" height="35" rx="6" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="480" y="142" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Part 2 file</text>
  <text x="310" y="200" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#2e7d32">Reader Side (Reduce stage)</text>
  <rect x="30" y="210" width="560" height="155" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="50" y="228" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Executor (for Partition 0)</text>
  <text x="310" y="248" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Fetch Part 0 from all map executors</text>
  <rect x="80" y="258" width="110" height="35" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="135" y="273" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Exec 0 Part 0</text>
  <rect x="220" y="258" width="110" height="35" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="275" y="273" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Exec 1 Part 0</text>
  <rect x="360" y="258" width="110" height="35" rx="6" fill="#fff" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="415" y="273" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Exec 2 Part 0</text>
  <line x1="135" y1="293" x2="275" y2="320" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-sh)"/>
  <line x1="275" y1="293" x2="275" y2="320" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-sh)"/>
  <line x1="415" y1="293" x2="275" y2="320" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-sh)"/>
  <rect x="200" y="325" width="150" height="30" rx="6" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="275" y="345" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Merge + Sort</text>
</svg>

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

<svg viewBox="0 0 620 360" xmlns="http://www.w3.org/2000/svg">
  <text x="310" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">Executor Memory Layout (spark.executor.memory = 8g)</text>
  <!-- Total Container -->
  <rect x="20" y="25" width="580" height="320" rx="8" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="310" y="45" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Total Container: 8g + max(384m, 0.1*8g) = 8.8 GB</text>
  <!-- JVM Heap -->
  <rect x="40" y="55" width="540" height="240" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="310" y="75" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0277bd">JVM Heap (8 GB)</text>
  <!-- Reserved -->
  <rect x="60" y="85" width="500" height="25" rx="4" fill="#fce4ec" stroke="#c62828" stroke-width="1.5"/>
  <text x="310" y="102" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Reserved Memory (300 MB)</text>
  <!-- Spark Memory -->
  <rect x="60" y="118" width="500" height="100" rx="6" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="310" y="136" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Spark Memory (0.6 * 8g = 4.8 GB)</text>
  <rect x="80" y="145" width="230" height="60" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="195" y="165" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Execution (60%)</text>
  <text x="195" y="180" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">Shuffles, sorts, joins, aggs</text>
  <text x="195" y="195" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">2.88 GB</text>
  <rect x="320" y="145" width="230" height="60" rx="6" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="435" y="165" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Storage (40%)</text>
  <text x="435" y="180" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">Cached data, broadcast vars</text>
  <text x="435" y="195" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#555">1.92 GB</text>
  <!-- User Memory -->
  <rect x="60" y="225" width="500" height="55" rx="6" fill="#e1f5fe" stroke="#0277bd" stroke-width="1"/>
  <text x="310" y="248" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">User Memory (0.4 * 8g = 3.2 GB)</text>
  <text x="310" y="268" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">UDF data, internal metadata</text>
  <!-- Off-Heap -->
  <rect x="40" y="300" width="540" height="35" rx="6" fill="#fce4ec" stroke="#c62828" stroke-width="1.5"/>
  <text x="310" y="322" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Off-Heap / Overhead (800 MB) - OS overhead, Python processes</text>
</svg>

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

```text
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

<svg viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-aqe7" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <!-- Without AQE -->
  <rect x="20" y="5" width="580" height="140" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="310" y="25" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#c62828">Without AQE (static planning)</text>
  <text x="310" y="45" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">shuffle.partitions = 200 (fixed), Join strategy decided upfront</text>
  <text x="310" y="65" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#888">Result: 200 partitions, many empty/tiny</text>
  <rect x="40" y="75" width="55" height="30" rx="3" fill="#fce4ec" stroke="#c62828" stroke-width="1.5"/>
  <text x="68" y="94" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#333">5</text>
  <rect x="100" y="75" width="30" height="30" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <rect x="135" y="75" width="30" height="30" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <rect x="170" y="75" width="80" height="30" rx="3" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="210" y="94" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#c62828">9M skew!</text>
  <rect x="255" y="75" width="30" height="30" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <rect x="290" y="75" width="30" height="30" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <rect x="325" y="75" width="30" height="30" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <rect x="360" y="75" width="30" height="30" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <text x="420" y="94" font-family="Arial, sans-serif" font-size="14" fill="#999">...</text>
  <text x="310" y="125" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#c62828">many empty partitions + skewed data</text>
  <!-- Arrow -->
  <line x1="310" y1="148" x2="310" y2="175" stroke="#333" stroke-width="2" marker-end="url(#arrow-aqe7)"/>
  <text x="345" y="167" font-family="Arial, sans-serif" font-size="12" fill="#333" font-weight="bold">AQE optimizes</text>
  <!-- With AQE -->
  <rect x="20" y="180" width="580" height="145" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="310" y="200" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#2e7d32">With AQE (runtime optimization)</text>
  <text x="310" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Step 1: Run map stages, collect statistics | Step 2: Re-optimize | Step 3: Coalesce | Step 4: Split skew</text>
  <text x="310" y="240" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#888">Result: balanced partitions</text>
  <rect x="50" y="250" width="120" height="35" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="110" y="265" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#333">3M (sk1)</text>
  <text x="110" y="278" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" fill="#2e7d32">split skew</text>
  <rect x="180" y="250" width="120" height="35" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="240" y="265" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#333">3M (sk2)</text>
  <text x="240" y="278" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" fill="#2e7d32">split skew</text>
  <rect x="310" y="250" width="120" height="35" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="370" y="265" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#333">3M (sk3)</text>
  <text x="370" y="278" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" fill="#2e7d32">split skew</text>
  <rect x="440" y="250" width="70" height="35" rx="4" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="475" y="265" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#333">1M</text>
  <text x="475" y="278" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" fill="#0277bd">coalesced</text>
  <rect x="515" y="250" width="70" height="35" rx="4" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="550" y="265" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#333">1M</text>
  <text x="550" y="278" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" fill="#0277bd">coalesced</text>
</svg>

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

```text
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

```text
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
