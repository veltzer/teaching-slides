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

<svg xmlns="http://www.w3.org/2000/svg" width="614" height="220"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><text x="20" y="26" font-family="sans-serif" font-size="14" fill="#222" text-anchor="start" font-weight="bold">Reading a 200-column Parquet table</text><text x="20" y="56" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start">Without projection pushdown (SELECT *):</text><rect x="20" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="22" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c1</text><text x="34" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="74" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="76" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c2</text><text x="88" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="128" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="130" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c3</text><text x="142" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="182" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="184" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c4</text><text x="196" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="236" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="238" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c5</text><text x="250" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="290" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="292" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c6</text><text x="304" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="344" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="346" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c7</text><text x="358" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="398" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="400" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c8</text><text x="412" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="452" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="454" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">...</text><text x="466" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><rect x="506" y="66" width="52" height="34" fill="#fde0dc" stroke="#333" stroke-width="1.5" rx="4"/><text x="508" y="80" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c200</text><text x="520" y="94" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="start" font-weight="bold">R</text><text x="20" y="116" font-family="sans-serif" font-size="12" fill="#555" text-anchor="start">Read: 200 columns = 100% of data</text><text x="20" y="140" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start">With projection pushdown (SELECT c1, c5):</text><rect x="20" y="150" width="52" height="34" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="22" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c1</text><text x="34" y="178" font-family="sans-serif" font-size="11" fill="#1b5e20" text-anchor="start" font-weight="bold">R</text><rect x="74" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="76" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c2</text><text x="88" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><rect x="128" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="130" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c3</text><text x="142" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><rect x="182" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="184" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c4</text><text x="196" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><rect x="236" y="150" width="52" height="34" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="238" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c5</text><text x="250" y="178" font-family="sans-serif" font-size="11" fill="#1b5e20" text-anchor="start" font-weight="bold">R</text><rect x="290" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="292" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c6</text><text x="304" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><rect x="344" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="346" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c7</text><text x="358" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><rect x="398" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="400" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c8</text><text x="412" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><rect x="452" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="454" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">...</text><text x="466" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><rect x="506" y="150" width="52" height="34" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="508" y="164" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">c200</text><text x="520" y="178" font-family="sans-serif" font-size="11" fill="#9e9e9e" text-anchor="start" font-weight="bold">S</text><text x="20" y="202" font-family="sans-serif" font-size="12" fill="#555" text-anchor="start">Read: 2 columns = 1% of data     R = Read,  S = Skip</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="330"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="620" height="310" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="32" font-family="sans-serif" font-size="14" fill="#222" text-anchor="start" font-weight="bold">ORC File Structure</text><rect x="30" y="50" width="580" height="105" fill="#fff" stroke="#333" stroke-width="1.5" rx="4"/><text x="40" y="66" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">Stripe 0</text><rect x="40" y="74" width="90" height="18" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="46" y="87" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Index</text><text x="140" y="87" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start">← min/max per 10K rows</text><rect x="40" y="96" width="90" height="18" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="46" y="109" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Data</text><text x="140" y="109" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start">← column encoded data</text><rect x="40" y="118" width="90" height="18" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="46" y="131" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Footer</text><text x="140" y="131" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start">← column statistics</text><rect x="30" y="170" width="580" height="105" fill="#fff" stroke="#333" stroke-width="1.5" rx="4"/><text x="40" y="186" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">Stripe 1</text><rect x="40" y="194" width="90" height="18" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="46" y="207" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Index</text><text x="140" y="207" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start"></text><rect x="40" y="216" width="90" height="18" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="46" y="229" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Data</text><text x="140" y="229" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start"></text><rect x="40" y="238" width="90" height="18" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="46" y="251" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Footer</text><text x="140" y="251" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start"></text><rect x="30" y="285" width="580" height="22" fill="#bbdefb" stroke="#333" stroke-width="1.5" rx="4"/><text x="40" y="300" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">File Footer (column types, statistics)   |   Postscript (compression, version)</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="330"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="640" height="310" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="32" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">Delta Lake adds ACID transactions on top of Parquet</text><text x="20" y="52" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">Delta Table Directory Structure</text><text x="28" y="72" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">/data/delta_table/</text><text x="28" y="89" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── _delta_log/</text><text x="28" y="106" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">│   ├── 00000000000000000000.json</text><text x="28" y="123" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">│   ├── 00000000000000000001.json</text><text x="28" y="140" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">│   ├── 00000000000000000002.json</text><text x="28" y="157" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">│   ├── ...</text><text x="28" y="174" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">│   └── 00000000000000000010.checkpoint.parquet</text><text x="28" y="191" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── part-00000-...snappy.parquet</text><text x="28" y="208" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── part-00001-...snappy.parquet</text><text x="28" y="225" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── part-00002-...snappy.parquet</text><text x="28" y="242" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">└── part-00003-...snappy.parquet</text><rect x="20" y="265" width="620" height="64" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="28" y="281" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start" font-weight="bold">Transaction Log (_delta_log):</text><text x="28" y="297" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Each JSON file = one atomic transaction   • Contains: add/remove file actions</text><text x="28" y="313" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Checkpoints every 10 transactions         • Enables time travel and ACID</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="290"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><text x="20" y="22" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">Without Z-ordering (random distribution):</text><rect x="20" y="30" width="155" height="46" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="26" y="45" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start" font-weight="bold">File 1</text><text x="26" y="59" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[A,B,C,D,E]</text><text x="26" y="72" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[01,02,03,04,05]</text><rect x="182" y="30" width="155" height="46" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="188" y="45" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start" font-weight="bold">File 2</text><text x="188" y="59" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[A,C,E,F,G]</text><text x="188" y="72" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[01,03,05,06,07]</text><rect x="344" y="30" width="155" height="46" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="350" y="45" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start" font-weight="bold">File 3</text><text x="350" y="59" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[B,D,F,H,I]</text><text x="350" y="72" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[02,04,06,08,09]</text><rect x="506" y="30" width="155" height="46" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="512" y="45" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start" font-weight="bold">File 4</text><text x="512" y="59" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[A,G,H,I,J]</text><text x="512" y="72" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[01,07,08,09,10]</text><text x="20" y="95" font-family="sans-serif" font-size="12" fill="#c62828" text-anchor="start">Query: WHERE user_id = 'A'  →  Must scan File 1, 2, 4  (3/4 files = 75%)</text><text x="20" y="120" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">With Z-ordering on user_id:</text><rect x="20" y="128" width="155" height="46" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="26" y="143" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start" font-weight="bold">File 1</text><text x="26" y="157" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[A,A,A,B,B]</text><text x="26" y="170" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[01,03,07,02,04]</text><rect x="182" y="128" width="155" height="46" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="188" y="143" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start" font-weight="bold">File 2</text><text x="188" y="157" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[C,C,D,D,E]</text><text x="188" y="170" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[03,05,02,04,05]</text><rect x="344" y="128" width="155" height="46" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="350" y="143" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start" font-weight="bold">File 3</text><text x="350" y="157" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[F,F,G,G,H]</text><text x="350" y="170" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[06,08,06,07,08]</text><rect x="506" y="128" width="155" height="46" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="512" y="143" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start" font-weight="bold">File 4</text><text x="512" y="157" font-family="sans-serif" font-size="10" fill="#333" text-anchor="start">user_id=[H,I,I,J,J]</text><text x="512" y="170" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">date=[09,08,09,09,10]</text><text x="20" y="193" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start">Query: WHERE user_id = 'A'  →  Must scan File 1 only  (1/4 files = 25%)</text><rect x="20" y="208" width="660" height="68" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="226" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Z-order creates locality for the specified columns within data files,</text><text x="30" y="244" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">making min/max statistics more effective at file skipping.</text><text x="30" y="262" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Result: 75% → 25% files scanned in this example.</text></svg>

---
## Apache Iceberg Overview

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="520"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="20" y="70" width="620" height="48" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="88" font-family="sans-serif" font-size="13" fill="#1565c0" text-anchor="start" font-weight="bold">Iceberg Catalog  (HMS, Glue, REST, Nessie)</text><text x="30" y="104" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Points to current metadata file</text><line x1="330" y1="118" x2="330" y2="134" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="20" y="160" width="620" height="90" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="178" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">Metadata Layer</text><text x="30" y="194" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">metadata/v3.metadata.json</text><text x="30" y="208" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">- Schema (current + history)</text><text x="30" y="222" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">- Partition spec (current + history)</text><text x="30" y="236" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">- Snapshot list → snap-001.avro, snap-002.avro</text><line x1="330" y1="250" x2="330" y2="266" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="20" y="280" width="620" height="62" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="298" font-family="sans-serif" font-size="13" fill="#e65100" text-anchor="start" font-weight="bold">Manifest List</text><text x="30" y="314" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Points to manifest files</text><text x="30" y="328" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Contains partition summary statistics</text><line x1="330" y1="342" x2="330" y2="358" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="20" y="360" width="620" height="76" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="378" font-family="sans-serif" font-size="13" fill="#880e4f" text-anchor="start" font-weight="bold">Manifest Files</text><text x="30" y="394" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">List of data files with:</text><text x="30" y="408" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">- File path, format, size   - Partition values</text><text x="30" y="422" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">- Column-level min/max/null stats</text><line x1="330" y1="436" x2="330" y2="452" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="20" y="460" width="620" height="48" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="478" font-family="sans-serif" font-size="13" fill="#4a148c" text-anchor="start" font-weight="bold">Data Files  (Parquet / ORC / Avro)</text><text x="30" y="494" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Actual columnar data storage</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="430"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="20" y="10" width="620" height="118" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="28" font-family="sans-serif" font-size="13" fill="#1565c0" text-anchor="start" font-weight="bold">1. Range Partitioning (most common)</text><text x="30" y="42" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">PARTITIONED BY (event_date)</text><text x="30" y="56" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/event_date=2024-01-01/</text><text x="30" y="70" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/event_date=2024-01-02/</text><text x="30" y="84" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/event_date=2024-01-03/</text><text x="30" y="98" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">...</text><text x="30" y="112" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Best for: time-series, date-based queries</text><rect x="20" y="155" width="620" height="104" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="173" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">2. List Partitioning</text><text x="30" y="187" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">PARTITIONED BY (region)</text><text x="30" y="201" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/region=us-east/</text><text x="30" y="215" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/region=us-west/</text><text x="30" y="229" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/region=eu-west/</text><text x="30" y="243" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Best for: categorical, low-cardinality</text><rect x="20" y="290" width="620" height="118" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="30" y="308" font-family="sans-serif" font-size="13" fill="#e65100" text-anchor="start" font-weight="bold">3. Hash Partitioning</text><text x="30" y="322" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">PARTITIONED BY (hash(user_id, 32))</text><text x="30" y="336" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/user_hash=0/</text><text x="30" y="350" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/user_hash=1/</text><text x="30" y="364" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">...</text><text x="30" y="378" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">/data/events/user_hash=31/</text><text x="30" y="392" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Best for: even distribution, join keys</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="460"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="120" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="28" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">Good partition column:</text><text x="20" y="46" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start">[✓] Used in WHERE clauses frequently</text><text x="20" y="63" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start">[✓] Low-to-medium cardinality (10 – 10,000)</text><text x="20" y="80" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start">[✓] Even data distribution</text><text x="20" y="97" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start">[✓] Each partition > 128 MB</text><rect x="10" y="140" width="660" height="160" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="158" font-family="sans-serif" font-size="13" fill="#c62828" text-anchor="start" font-weight="bold">Bad partition column:</text><text x="20" y="176" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start">[✗] High cardinality (user_id with millions) → too many small files</text><text x="20" y="193" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start">[✗] Never filtered on → no pruning benefit, extra overhead</text><text x="20" y="210" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start">[✗] Very skewed (99% in one value) → one giant partition, rest tiny</text><text x="20" y="227" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start">[✗] Too few values (boolean: true/false) → only 2 partitions, minimal benefit</text><text x="10" y="320" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">Partition count guidelines:</text><rect x="10" y="334" width="660" height="22" fill="#bbdefb" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="349" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start" font-weight="bold">Total data size</text><text x="245" y="349" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start" font-weight="bold">Target partitions</text><line x1="235" y1="334" x2="235" y2="444" stroke="#333" stroke-width="1"/><rect x="10" y="356" width="660" height="22" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="371" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">< 1 GB</text><text x="245" y="371" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">No partitioning needed</text><rect x="10" y="378" width="660" height="22" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="393" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">1 GB – 100 GB</text><text x="245" y="393" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">10 – 100 partitions</text><rect x="10" y="400" width="660" height="22" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="415" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">100 GB – 10 TB</text><text x="245" y="415" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">100 – 10,000 partitions</text><rect x="10" y="422" width="660" height="22" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="437" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">> 10 TB</text><text x="245" y="437" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">1,000 – 100,000 partitions</text></svg>

---
## Bucketing vs Partitioning

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="320"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="140" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="28" font-family="sans-serif" font-size="14" fill="#1565c0" text-anchor="start" font-weight="bold">Partitioning</text><text x="20" y="46" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">Physically separates data into folders</text><text x="20" y="66" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">/table/date=2024-01-01/   /table/date=2024-01-02/</text><text x="20" y="86" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">Pros: partition pruning, human-readable</text><text x="20" y="106" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">Cons: small files, limited cardinality</text><rect x="10" y="160" width="660" height="150" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="178" font-family="sans-serif" font-size="14" fill="#2e7d32" text-anchor="start" font-weight="bold">Bucketing</text><text x="20" y="196" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">Distributes data into fixed-size buckets based on hash of column value</text><text x="20" y="216" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">/table/part-00000 (bucket 0)   /table/part-00001 (bucket 1)</text><text x="20" y="236" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">/table/part-00002 (bucket 2)   ...   /table/part-00031 (bucket 31)</text><text x="20" y="256" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">Pros: eliminates shuffle in joins, works with high cardinality</text><text x="20" y="276" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">Cons: fixed bucket count, write overhead</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="360"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="340" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="14" fill="#e65100" text-anchor="start" font-weight="bold">The small file problem</text><text x="20" y="50" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Cause: streaming or frequent appends create many tiny files</text><text x="28" y="68" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">/data/events/date=2024-06-15/</text><text x="28" y="85" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── part-00000.parquet  (2 KB)</text><text x="28" y="102" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── part-00001.parquet  (3 KB)</text><text x="28" y="119" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── part-00002.parquet  (1 KB)</text><text x="28" y="136" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── part-00003.parquet  (4 KB)</text><text x="28" y="153" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">├── ... (10,000 tiny files)</text><text x="28" y="170" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">└── part-09999.parquet  (2 KB)</text><text x="20" y="200" font-family="sans-serif" font-size="12" fill="#e65100" text-anchor="start" font-weight="bold">Problems:</text><text x="28" y="218" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">• Slow reads: metadata overhead per file</text><text x="28" y="235" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">• HDFS/S3 listing bottleneck</text><text x="28" y="252" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">• NameNode memory pressure (HDFS)</text><text x="28" y="269" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">• High API cost (S3)</text><text x="28" y="286" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">• Poor predicate pushdown (stats per file)</text><text x="20" y="328" font-family="sans-serif" font-size="12" fill="#bf360c" text-anchor="start" font-weight="bold">Target: files of 128 MB – 1 GB</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="340"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="320" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="14" fill="#4a148c" text-anchor="start" font-weight="bold">Compaction Scheduling</text><text x="20" y="50" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Micro-batch writes (every 1 min) → 1440 files/day:</text><rect x="28" y="60" width="50" height="28" fill="#e1bee7" stroke="#333" stroke-width="1.5" rx="4"/><text x="36" y="79" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">2KB</text><rect x="82" y="60" width="50" height="28" fill="#e1bee7" stroke="#333" stroke-width="1.5" rx="4"/><text x="90" y="79" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">3KB</text><rect x="136" y="60" width="50" height="28" fill="#e1bee7" stroke="#333" stroke-width="1.5" rx="4"/><text x="144" y="79" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">1KB</text><rect x="190" y="60" width="50" height="28" fill="#e1bee7" stroke="#333" stroke-width="1.5" rx="4"/><text x="198" y="79" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">2KB</text><rect x="244" y="60" width="50" height="28" fill="#e1bee7" stroke="#333" stroke-width="1.5" rx="4"/><text x="252" y="79" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">4KB</text><rect x="298" y="60" width="60" height="28" fill="#e1bee7" stroke="#333" stroke-width="1.5" rx="4"/><text x="306" y="79" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">...</text><rect x="362" y="60" width="50" height="28" fill="#e1bee7" stroke="#333" stroke-width="1.5" rx="4"/><text x="370" y="79" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">3KB</text><line x1="340" y1="100" x2="340" y2="130" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><text x="348" y="120" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start">Scheduled compaction (daily at 2 AM)</text><rect x="30" y="135" width="620" height="38" fill="#ce93d8" stroke="#333" stroke-width="1.5" rx="4"/><text x="40" y="151" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Read all files for yesterday's partition, write as fewer larger files</text><line x1="340" y1="175" x2="340" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><text x="20" y="230" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start" font-weight="bold">After compaction:</text><rect x="28" y="240" width="180" height="40" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="78" y="265" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">128 MB</text><rect x="228" y="240" width="180" height="40" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="278" y="265" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">128 MB</text><rect x="428" y="240" width="180" height="40" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="478" y="265" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">90 MB</text><text x="20" y="300" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="start">3 files per day  (vs 1440)</text></svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="370"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="350" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="15" fill="#0d47a1" text-anchor="start" font-weight="bold">Key Takeaways</text><text x="20" y="66" font-family="sans-serif" font-size="13" fill="#1565c0" text-anchor="start" font-weight="bold">Formats:</text><text x="28" y="84" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Parquet: default for analytics, columnar</text><text x="28" y="101" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• ORC: alternative for Hive-centric stacks</text><text x="28" y="118" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Avro: row-based, streaming, schema evolution</text><text x="28" y="135" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Delta / Iceberg: ACID on top of Parquet</text><text x="20" y="160" font-family="sans-serif" font-size="13" fill="#1565c0" text-anchor="start" font-weight="bold">Optimization:</text><text x="28" y="178" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Predicate pushdown: filter at storage layer</text><text x="28" y="195" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Projection pushdown: read only needed columns</text><text x="28" y="212" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Z-ordering: co-locate data for better pruning</text><text x="28" y="229" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Compression: ZSTD best overall balance</text><text x="20" y="254" font-family="sans-serif" font-size="13" fill="#1565c0" text-anchor="start" font-weight="bold">Storage Management:</text><text x="28" y="272" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Partition by query pattern (low cardinality)</text><text x="28" y="289" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Bucket by join key (high cardinality)</text><text x="28" y="306" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Compact small files regularly</text><text x="28" y="323" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• VACUUM old versions periodically</text><text x="28" y="340" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Monitor file sizes (target 128 MB – 1 GB)</text></svg>
