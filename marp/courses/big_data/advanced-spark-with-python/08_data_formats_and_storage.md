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

<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg">
  <text x="310" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">Parquet File Structure</text>
  <!-- Magic Number -->
  <rect x="50" y="25" width="520" height="25" rx="4" fill="#e1f5fe" stroke="#0277bd" stroke-width="1.5"/>
  <text x="310" y="42" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Magic Number: "PAR1" (4 bytes)</text>
  <!-- Row Group 0 -->
  <rect x="50" y="55" width="520" height="130" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="80" y="75" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">Row Group 0</text>
  <rect x="70" y="85" width="480" height="28" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1"/>
  <text x="310" y="103" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Column Chunk: user_id [Page 0] [Page 1] [Page 2]</text>
  <rect x="70" y="118" width="480" height="28" rx="4" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1"/>
  <text x="310" y="136" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Column Chunk: event_type [Page 0] [Page 1]</text>
  <rect x="70" y="151" width="480" height="28" rx="4" fill="#fce4ec" stroke="#c62828" stroke-width="1"/>
  <text x="310" y="169" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Column Chunk: amount [Page 0] [Page 1]</text>
  <!-- Row Group 1 -->
  <rect x="50" y="195" width="520" height="40" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="310" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Row Group 1 (same structure)</text>
  <!-- Footer -->
  <rect x="50" y="245" width="520" height="70" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="310" y="265" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">Footer</text>
  <text x="310" y="283" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">File metadata (schema, row group info)</text>
  <text x="310" y="298" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Column metadata (encodings, statistics) | Key-value metadata</text>
  <!-- Footer length + magic -->
  <rect x="50" y="320" width="520" height="25" rx="4" fill="#e1f5fe" stroke="#0277bd" stroke-width="1.5"/>
  <text x="310" y="337" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#333">Footer Length (4 bytes) | Magic Number: "PAR1" (4 bytes)</text>
</svg>

---
## Row Groups and Column Chunks

<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg">
  <text x="310" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">Row Group Sizing and Layout</text>
  <rect x="30" y="28" width="560" height="240" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="310" y="50" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">Row Group (default: 128 MB, ~1M rows)</text>
  <text x="310" y="70" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Column Chunks stored contiguously:</text>
  <rect x="60" y="80" width="230" height="35" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="175" y="102" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">col_a data (encoded + compressed)</text>
  <rect x="60" y="120" width="230" height="35" rx="6" fill="#e1f5fe" stroke="#0277bd" stroke-width="1.5"/>
  <text x="175" y="142" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">col_b data</text>
  <rect x="60" y="160" width="230" height="35" rx="6" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="175" y="182" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">col_c data</text>
  <!-- Details -->
  <rect x="320" y="80" width="250" height="115" rx="6" fill="#f5f5f5" stroke="#bdbdbd" stroke-width="1"/>
  <text x="445" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#333">Each column chunk has:</text>
  <text x="445" y="118" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Encoding: PLAIN, DICT, RLE, DELTA</text>
  <text x="445" y="136" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Compression: SNAPPY, GZIP, ZSTD</text>
  <text x="445" y="154" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Statistics: min, max, null_count</text>
  <text x="445" y="172" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Page index: offset, size per page</text>
</svg>

---
## Page-Level Statistics and Column Index

<svg viewBox="0 0 620 300" xmlns="http://www.w3.org/2000/svg">
  <text x="310" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">Page-Level Statistics (Column: "amount")</text>
  <rect x="40" y="30" width="250" height="65" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="165" y="48" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Page 0</text>
  <text x="165" y="65" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">min=10, max=500</text>
  <text x="165" y="82" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">null_count=0, num_values=10000</text>
  <rect x="40" y="105" width="250" height="65" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="165" y="123" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Page 1</text>
  <text x="165" y="140" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">min=501, max=2000</text>
  <text x="165" y="157" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">null_count=3, num_values=9997</text>
  <rect x="40" y="180" width="250" height="65" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="165" y="198" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">Page 2</text>
  <text x="165" y="215" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">min=2001, max=9999</text>
  <text x="165" y="232" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">null_count=1, num_values=9999</text>
  <!-- Query box -->
  <rect x="330" y="30" width="260" height="215" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="460" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">WHERE amount > 5000</text>
  <text x="460" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#2e7d32">SKIP Page 0 (max=500)</text>
  <text x="460" y="130" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#2e7d32">SKIP Page 1 (max=2000)</text>
  <text x="460" y="180" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#c62828" font-weight="bold">READ Page 2 (max=9999)</text>
  <text x="460" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Only 1 of 3 pages read!</text>
</svg>

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

```diagram
Reading a 200-column Parquet table:

Without projection pushdown (SELECT *):
┌───┬───┬───┬───┬───┬───┬───┬───┬─────┬───┐
│c1 │c2 │c3 │c4 │c5 │c6 │c7 │c8 │ ... │c200│
│ R │ R │ R │ R │ R │ R │ R │ R │ R   │ R │
└───┴───┴───┴───┴───┴───┴───┴───┴─────┴───┘
Read: 200 columns = 100% of data

With projection pushdown (SELECT c1, c5):
┌───┬───┬───┬───┬───┬───┬───┬───┬─────┬───┐
│c1 │   │   │   │c5 │   │   │   │     │   │
│ R │ S │ S │ S │ R │ S │ S │ S │ S   │ S │
└───┴───┴───┴───┴───┴───┴───┴───┴─────┴───┘
Read: 2 columns = 1% of data   R=Read, S=Skip
```

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

```diagram
ORC (Optimized Row Columnar):

┌──────────────────────────────────────────────────┐
│  ORC File Structure                               │
│  ┌──────────────────────────────────────────┐    │
│  │  Stripe 0 (similar to Parquet row group)  │    │
│  │  ┌──────────┐                             │    │
│  │  │ Index    │ <- min/max per 10K rows     │    │
│  │  │ Data     │ <- column encoded data      │    │
│  │  │ Footer   │ <- column statistics        │    │
│  │  └──────────┘                             │    │
│  ├──────────────────────────────────────────┤    │
│  │  Stripe 1                                 │    │
│  │  ┌──────────┐                             │    │
│  │  │ Index    │                             │    │
│  │  │ Data     │                             │    │
│  │  │ Footer   │                             │    │
│  │  └──────────┘                             │    │
│  ├──────────────────────────────────────────┤    │
│  │  File Footer (column types, statistics)   │    │
│  │  Postscript (compression, version)        │    │
│  └──────────────────────────────────────────┘    │
└──────────────────────────────────────────────────┘
```

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

<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-fs" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <text x="310" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">Choosing the Right Format</text>
  <!-- Q1: Streaming? -->
  <rect x="30" y="30" width="300" height="30" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="180" y="50" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Streaming / message use case?</text>
  <line x1="330" y1="45" x2="380" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrow-fs)"/>
  <text x="350" y="38" font-family="Arial, sans-serif" font-size="10" fill="#2e7d32">Yes</text>
  <rect x="385" y="30" width="200" height="30" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="485" y="50" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#2e7d32">Use Avro</text>
  <!-- Q2: Analytics? -->
  <line x1="180" y1="60" x2="180" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrow-fs)"/>
  <text x="195" y="75" font-family="Arial, sans-serif" font-size="10" fill="#c62828">No</text>
  <rect x="30" y="85" width="300" height="30" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="180" y="105" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Analytics / OLAP workload?</text>
  <line x1="330" y1="100" x2="380" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow-fs)"/>
  <text x="350" y="93" font-family="Arial, sans-serif" font-size="10" fill="#2e7d32">Yes</text>
  <!-- Sub-question: Hive? -->
  <rect x="385" y="85" width="200" height="30" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="485" y="105" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Hive primary engine?</text>
  <line x1="485" y1="115" x2="440" y2="140" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-fs)"/>
  <text x="440" y="135" font-family="Arial, sans-serif" font-size="9" fill="#2e7d32">Yes</text>
  <rect x="385" y="145" width="90" height="25" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="430" y="162" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#333">Use ORC</text>
  <line x1="485" y1="115" x2="530" y2="140" stroke="#333" stroke-width="1.5" marker-end="url(#arrow-fs)"/>
  <text x="530" y="135" font-family="Arial, sans-serif" font-size="9" fill="#c62828">No</text>
  <rect x="490" y="145" width="105" height="25" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="543" y="162" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#333">Use Parquet</text>
  <!-- Q3: ACID? -->
  <line x1="180" y1="115" x2="180" y2="135" stroke="#333" stroke-width="2" marker-end="url(#arrow-fs)"/>
  <text x="195" y="130" font-family="Arial, sans-serif" font-size="10" fill="#c62828">No</text>
  <rect x="30" y="140" width="300" height="30" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="180" y="160" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Need ACID / time travel / MERGE?</text>
  <line x1="330" y1="155" x2="380" y2="200" stroke="#333" stroke-width="2" marker-end="url(#arrow-fs)"/>
  <text x="345" y="175" font-family="Arial, sans-serif" font-size="10" fill="#2e7d32">Yes</text>
  <rect x="385" y="190" width="200" height="30" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="485" y="210" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#7b1fa2">Use Delta Lake / Iceberg</text>
  <!-- Default -->
  <line x1="180" y1="170" x2="180" y2="200" stroke="#333" stroke-width="2" marker-end="url(#arrow-fs)"/>
  <text x="195" y="190" font-family="Arial, sans-serif" font-size="10" fill="#c62828">No</text>
  <rect x="80" y="205" width="200" height="30" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="180" y="225" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#2e7d32">Use Parquet (safe default)</text>
</svg>

---
## Delta Lake Overview

```diagram
Delta Lake adds ACID transactions on top of Parquet:

┌──────────────────────────────────────────────────┐
│  Delta Table Directory Structure                  │
│                                                  │
│  /data/delta_table/                              │
│  ├── _delta_log/                                 │
│  │   ├── 00000000000000000000.json               │
│  │   ├── 00000000000000000001.json               │
│  │   ├── 00000000000000000002.json               │
│  │   ├── ...                                     │
│  │   └── 00000000000000000010.checkpoint.parquet │
│  ├── part-00000-...snappy.parquet                │
│  ├── part-00001-...snappy.parquet                │
│  ├── part-00002-...snappy.parquet                │
│  └── part-00003-...snappy.parquet                │
│                                                  │
│  Transaction Log (_delta_log):                    │
│  - Each JSON file = one atomic transaction        │
│  - Contains: add/remove file actions              │
│  - Checkpoints every 10 transactions              │
│  - Enables time travel and ACID                   │
└──────────────────────────────────────────────────┘
```

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

```diagram
Without Z-ordering (random distribution):
File 1: user_id=[A,B,C,D,E], date=[01,02,03,04,05]
File 2: user_id=[A,C,E,F,G], date=[01,03,05,06,07]
File 3: user_id=[B,D,F,H,I], date=[02,04,06,08,09]
File 4: user_id=[A,G,H,I,J], date=[01,07,08,09,10]

Query: WHERE user_id = 'A'
-> Must scan: File 1, 2, 4 (3 of 4 files = 75%)

With Z-ordering on user_id:
File 1: user_id=[A,A,A,B,B], date=[01,03,07,02,04]
File 2: user_id=[C,C,D,D,E], date=[03,05,02,04,05]
File 3: user_id=[F,F,G,G,H], date=[06,08,06,07,08]
File 4: user_id=[H,I,I,J,J], date=[09,08,09,09,10]

Query: WHERE user_id = 'A'
-> Must scan: File 1 only (1 of 4 files = 25%)

┌──────────────────────────────────────────┐
│  Z-order creates locality for the        │
│  specified columns within data files,    │
│  making min/max statistics more          │
│  effective at file skipping.             │
└──────────────────────────────────────────┘
```

---
## Apache Iceberg Overview

```diagram
Iceberg Table Structure:

┌──────────────────────────────────────────────────┐
│  Iceberg Catalog                                  │
│  (HMS, Glue, REST, Nessie)                        │
│  ┌──────────────────────────────────────────┐    │
│  │  Points to current metadata file          │    │
│  └─────────────────┬────────────────────────┘    │
│                    v                              │
│  Metadata Layer                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  metadata/v3.metadata.json                │    │
│  │  - Schema (current + history)             │    │
│  │  - Partition spec (current + history)     │    │
│  │  - Snapshot list                          │    │
│  │    -> snap-001.avro (manifest list)       │    │
│  │    -> snap-002.avro (manifest list)       │    │
│  └─────────────────┬────────────────────────┘    │
│                    v                              │
│  Manifest List                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  Points to manifest files                 │    │
│  │  Contains partition summary statistics    │    │
│  └─────────────────┬────────────────────────┘    │
│                    v                              │
│  Manifest Files                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  List of data files with:                 │    │
│  │  - File path, format, size                │    │
│  │  - Partition values                        │    │
│  │  - Column-level min/max/null stats        │    │
│  └─────────────────┬────────────────────────┘    │
│                    v                              │
│  Data Files (Parquet/ORC/Avro)                    │
└──────────────────────────────────────────────────┘
```

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

```diagram
Partitioning types:

1. Range Partitioning (most common):
┌───────────────────────────────────────────┐
│  PARTITIONED BY (event_date)               │
│                                           │
│  /data/events/event_date=2024-01-01/      │
│  /data/events/event_date=2024-01-02/      │
│  /data/events/event_date=2024-01-03/      │
│  ...                                      │
│  Best for: time-series, date-based queries │
└───────────────────────────────────────────┘

2. List Partitioning:
┌───────────────────────────────────────────┐
│  PARTITIONED BY (region)                   │
│                                           │
│  /data/events/region=us-east/             │
│  /data/events/region=us-west/             │
│  /data/events/region=eu-west/             │
│  Best for: categorical, low-cardinality    │
└───────────────────────────────────────────┘

3. Hash Partitioning:
┌───────────────────────────────────────────┐
│  PARTITIONED BY (hash(user_id, 32))        │
│                                           │
│  /data/events/user_hash=0/                │
│  /data/events/user_hash=1/                │
│  ...                                      │
│  /data/events/user_hash=31/               │
│  Best for: even distribution, join keys    │
└───────────────────────────────────────────┘
```

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

```diagram
Partition column selection:

┌──────────────────────────────────────────────────┐
│  Good partition column:                           │
│  [x] Used in WHERE clauses frequently             │
│  [x] Low-to-medium cardinality (10-10,000)        │
│  [x] Even data distribution                       │
│  [x] Each partition > 128 MB                      │
│                                                  │
│  Bad partition column:                            │
│  [ ] High cardinality (user_id with millions)     │
│      -> too many small files                      │
│  [ ] Never filtered on                            │
│      -> no pruning benefit, extra overhead         │
│  [ ] Very skewed (99% in one value)               │
│      -> one giant partition, rest tiny             │
│  [ ] Too few values (boolean: true/false)         │
│      -> only 2 partitions, minimal benefit         │
└──────────────────────────────────────────────────┘

Partition count guidelines:
┌──────────────────────────────────────────────────┐
│  Total data size  │  Target partitions            │
│  ─────────────────┼──────────────────────────────│
│  < 1 GB           │  No partitioning needed       │
│  1 GB - 100 GB    │  10-100 partitions            │
│  100 GB - 10 TB   │  100-10,000 partitions        │
│  > 10 TB          │  1,000-100,000 partitions     │
└──────────────────────────────────────────────────┘
```

---
## Bucketing vs Partitioning

```diagram
Partitioning:
┌───────────────────────────────────────────┐
│  Physically separates data into folders    │
│                                           │
│  /table/date=2024-01-01/                  │
│  /table/date=2024-01-02/                  │
│                                           │
│  Pros: partition pruning, human-readable   │
│  Cons: small files, limited cardinality    │
└───────────────────────────────────────────┘

Bucketing:
┌───────────────────────────────────────────┐
│  Distributes data into fixed-size buckets  │
│  based on hash of column value             │
│                                           │
│  /table/part-00000  (bucket 0)            │
│  /table/part-00001  (bucket 1)            │
│  /table/part-00002  (bucket 2)            │
│  ...                                      │
│  /table/part-00031  (bucket 31)           │
│                                           │
│  Pros: eliminates shuffle in joins,        │
│        works with high cardinality         │
│  Cons: fixed bucket count, write overhead  │
└───────────────────────────────────────────┘
```

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

```diagram
The small file problem:

┌──────────────────────────────────────────────────┐
│  Cause: streaming or frequent appends create      │
│  many tiny files                                  │
│                                                  │
│  /data/events/date=2024-06-15/                   │
│  ├── part-00000.parquet  (2 KB)                  │
│  ├── part-00001.parquet  (3 KB)                  │
│  ├── part-00002.parquet  (1 KB)                  │
│  ├── part-00003.parquet  (4 KB)                  │
│  ├── ... (10,000 tiny files)                     │
│  └── part-09999.parquet  (2 KB)                  │
│                                                  │
│  Problems:                                       │
│  - Slow reads: metadata overhead per file         │
│  - HDFS/S3 listing bottleneck                    │
│  - NameNode memory pressure (HDFS)               │
│  - High API cost (S3)                            │
│  - Poor predicate pushdown (stats per file)       │
│                                                  │
│  Target: files of 128 MB - 1 GB                  │
└──────────────────────────────────────────────────┘
```

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

```diagram
Compaction scheduling:

┌──────────────────────────────────────────────────┐
│  Streaming Pipeline:                              │
│                                                  │
│  Micro-batch writes (every 1 min):               │
│  ┌───┐┌───┐┌───┐┌───┐┌───┐ ... ┌───┐            │
│  │2KB││3KB││1KB││2KB││4KB│     │3KB│            │
│  └───┘└───┘└───┘└───┘└───┘     └───┘            │
│          1440 files per day                      │
│                                                  │
│  Scheduled compaction (daily at 2 AM):            │
│  ┌──────────────────────────────────────┐        │
│  │  Read all files for yesterday's       │        │
│  │  partition, write as fewer files       │        │
│  └──────────────────────────────────────┘        │
│                                                  │
│  After compaction:                               │
│  ┌──────────┐┌──────────┐┌──────────┐            │
│  │  128 MB  ││  128 MB  ││  90 MB   │            │
│  └──────────┘└──────────┘└──────────┘            │
│          3 files per day                         │
└──────────────────────────────────────────────────┘
```

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

```diagram
┌──────────────────────────────────────────────────┐
│  Key Takeaways                                    │
├──────────────────────────────────────────────────┤
│                                                  │
│  Formats:                                        │
│  - Parquet: default for analytics, columnar       │
│  - ORC: alternative for Hive-centric stacks       │
│  - Avro: row-based, streaming, schema evolution   │
│  - Delta/Iceberg: ACID on top of Parquet          │
│                                                  │
│  Optimization:                                   │
│  - Predicate pushdown: filter at storage layer    │
│  - Projection pushdown: read only needed columns  │
│  - Z-ordering: co-locate data for better pruning  │
│  - Compression: ZSTD best overall balance         │
│                                                  │
│  Storage Management:                             │
│  - Partition by query pattern (low cardinality)   │
│  - Bucket by join key (high cardinality)          │
│  - Compact small files regularly                  │
│  - VACUUM old versions periodically               │
│  - Monitor file sizes (target 128 MB - 1 GB)      │
│                                                  │
└──────────────────────────────────────────────────┘
```
