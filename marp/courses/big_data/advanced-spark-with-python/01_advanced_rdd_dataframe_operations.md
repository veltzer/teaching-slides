# Advanced Spark with Python
---
## Advanced RDD and DataFrame Operations
---
## Chapter topics
* Advanced transformations and actions
* Custom partitioning strategies
* Broadcast variables and accumulators
* Performance optimization techniques
* Real-world applications and patterns
---
## Learning Objectives
* Master complex RDD transformations
* Implement custom partitioning
* Optimize memory usage with broadcast variables
* Design efficient data processing pipelines
* Apply performance tuning techniques
---
## Prerequisites Check
* Basic Python programming
* Spark fundamentals
* DataFrame operations
* SQL knowledge
---
## Complex Transformations
* Beyond basic operations
* Chaining transformations
* Optimization opportunities
* Performance considerations
---
## Key Transformation Types
```python
# mapPartitions example
def process_partition(iterator):
    results = []
    for x in iterator:
        results.append(x * 2)
    return iter(results)
```
---
## MapPartitions vs Map
<svg viewBox="0 0 540 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="110.0" x2="235" y2="110.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="190.0" x2="235" y2="190.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="110.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="90.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="115.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Input RDD</text></svg>

---
## Aggregate Operations
```python
# Complex aggregation
result = rdd.aggregate(
    0,
    lambda acc, value: acc + value,
    lambda acc1, acc2: acc1 + acc2
)
```
---
## Cogroup Operations
```python
rdd1 = sc.parallelize([("a", 1), ("b", 2)])
rdd2 = sc.parallelize([("a", 3), ("a", 4)])
grouped = rdd1.cogroup(rdd2)
```
---
## Understanding Partitioning
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="130.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="220.0" y1="60" x2="205.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="370.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145.0" y1="180" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="180" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="130.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="175.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Data</text></svg>

---
## Custom Partitioner Implementation

```python
class DatePartitioner(Partitioner):
    def __init__(self, partitions):
        self.partitions = partitions

    def numPartitions(self):
        return self.partitions
```

---
## Partition Distribution
<svg viewBox="0 0 540 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="110.0" x2="235" y2="70.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="110.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="190.0" x2="235" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="235" y1="70.0" x2="325" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="235" y1="150.0" x2="325" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="90.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="115.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Data</text></svg>

---
## Partitioning Strategies
1. Key-based partitioning
1. Range-based partitioning
1. Custom logic partitioning
1. Hybrid approaches
---
## Data Skew Handling
```python
def balance_partitions(rdd):
    counts = rdd.countByKey()
    threshold = max(counts.values()) * 0.75
    return rdd.partitionBy(100, lambda k: hash(k))
```
---
## Memory Management
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="130.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="280.0" y1="60" x2="370.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="220.0" y1="180" x2="205.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="130.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="175.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Memory</text></svg>

---
## Broadcast Variables Basics
```python
lookup_table = {"key1": "value1", "key2": "value2"}
broadcast_lookup = sc.broadcast(lookup_table)
```
---
## Broadcast Variable Usage
```python
def process_with_lookup(record):
    return broadcast_lookup.value.get(record, "default")

result = rdd.map(process_with_lookup)
```
---
## Broadcast Best Practices
1. Use for static reference data
1. Monitor memory usage
1. Consider update frequency
1. Optimize serialization
---
## Accumulators Introduction
```python
error_count = sc.accumulator(0)
warning_count = sc.accumulator(0)
```
---
## Custom Accumulator

```python
class SetAccumulator(AccumulatorParam):
    def zero(self, initialValue):
        return set([initialValue])

    def addInPlace(self, v1, v2):
        return v1.union(v2)
```

---
## Accumulator Applications
<svg viewBox="0 0 540 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="70.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="415" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="460" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Tasks</text></svg>

---
## Window Function Basics
```python
from pyspark.sql.window import Window
window_spec = Window.partitionBy("department")
```
---
## Window Function Types
1. Ranking functions
1. Analytic functions
1. Aggregate functions
1. Value functions
---
## Advanced Window Operations
```python
window_spec = (Window
    .partitionBy("department")
    .orderBy("salary")
    .rowsBetween(-2, 2))
```
---
## Complex Window Example
```python
from pyspark.sql import functions as F
df = df.withColumn(
    "moving_avg",
    F.avg("value").over(window_spec)
)
```
---
## Performance Optimization
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Performance</text></svg>

---
## Memory Tuning
```python
spark.conf.set("spark.memory.fraction", 0.8)
spark.conf.set("spark.memory.storageFraction", 0.3)
```
---
## CPU Optimization
1. Partition sizing
1. Task scheduling
1. Resource allocation
1. Serialization
---
## Network Optimization
```python
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.rdd.compress", "true")
```
---
## Storage Strategies
<svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="110.0" x2="235" y2="70.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="190.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="190.0" x2="235" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="90.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="115.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Storage</text></svg>

---
## Caching Levels
1. MEMORY_ONLY
1. MEMORY_AND_DISK
1. MEMORY_ONLY_SER
1. DISK_ONLY
---
## When to Cache
```python
# Expensive computation
complex_rdd = rdd.map(expensive_function).cache()
```
---
## Persistence Options
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="130.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="280.0" y1="60" x2="370.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="220.0" y1="180" x2="205.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="130.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="175.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Data</text></svg>

---
## Join Optimization
```python
# Broadcast join example
small_df = spark.table("small_table")
large_df = spark.table("large_table")
joined = large_df.join(broadcast(small_df), "key")
```
---
## Shuffle Optimization
1. Reduce shuffle partitions
1. Use broadcast joins
1. Partition data properly
1. Monitor shuffle spill
---
## Data Serialization
```python
spark.conf.set("spark.serializer",
    "org.apache.spark.serializer.KryoSerializer")
```
---
## Monitoring Tools
<svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="70.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Monitoring</text></svg>

---
## Performance Metrics
1. Execution time
1. Memory usage
1. Shuffle read/write
1. GC time
---
## Resource Management
```python
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.cores", "4")
```
---
## Common Anti-patterns
1. Unnecessary shuffling
1. Poor partitioning
1. Memory leaks
1. Inefficient UDFs
---
## Debugging Techniques
```python
def debug_function(partition):
    for record in partition:
        print(f"Processing: {record}")
    return partition

debug_rdd = rdd.mapPartitions(debug_function)
```
---
## Data Skew Solutions
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="130.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="280.0" y1="60" x2="370.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="220.0" y1="180" x2="280.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="130.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="175.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Skewed Data</text></svg>

---
## Advanced UDF Usage
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def complex_transformation(value):
    return process(value)
```
---
## Pipeline Optimization
1. Stage optimization
1. Task combining
1. Memory management
1. I/O optimization
---
## Best Practices Summary
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Best Practices</text></svg>

---
## Performance Checklist
1. Monitor memory usage
1. Optimize shuffling
1. Use appropriate partitioning
1. Implement caching strategy
---
## Advanced Configurations
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```
---
## Production Deployment
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="595" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="640" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Development</text></svg>

---
## Security Considerations
1. Authentication
1. Authorization
1. Encryption
1. Audit logging
---
## Future Learning Path
1. Streaming processing
1. Machine learning
1. Graph processing
1. Deep learning
---
## Chapter Summary
1. Complex transformations
1. Custom partitioning
1. Memory optimization
1. Performance tuning
---
## Practice Exercises
1. Implement custom partitioner
1. Optimize join operations
1. Debug performance issues
1. Design efficient pipelines

---

## Full Program: MapPartitions with DB Connection

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MapPartitionsDemo") \
    .getOrCreate()

sc = spark.sparkContext

# Create sample RDD with 1M records
rdd = sc.parallelize(range(1_000_000), numPartitions=100)

def process_partition_with_connection(iterator):
    """Open one DB connection per partition instead of per record."""
    import sqlite3
    conn = sqlite3.connect("/tmp/cache.db")
    cursor = conn.cursor()
    results = []
    for record in iterator:
        cursor.execute("SELECT value FROM cache WHERE key=?", (record,))
        row = cursor.fetchone()
        results.append((record, row[0] if row else None))
    conn.close()
    return iter(results)

# mapPartitions: 100 connections (one per partition)
# map: 1,000,000 connections (one per record) -- ANTI-PATTERN
result_rdd = rdd.mapPartitions(process_partition_with_connection)
print(f"Processed {result_rdd.count()} records")
```

---

## mapPartitions vs map: Performance Comparison

| Aspect | map() | mapPartitions() |
|---|---|---|
| Function calls | Once per element | Once per partition |
| Resource init | Per element (slow) | Per partition (fast) |
| Memory usage | Low per call | Entire partition in memory |
| Use case | Simple transforms | DB/network I/O |
| Overhead | High for I/O ops | Low for I/O ops |
| GC pressure | Higher | Lower |

---

## Data Flow: mapPartitions

<svg viewBox="0 0 600 420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-mp" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <!-- Driver Program -->
  <rect x="100" y="10" width="400" height="50" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="300" y="30" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">Driver Program</text>
  <text x="300" y="48" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#555">rdd.mapPartitions(process_partition)</text>
  <!-- Arrows from driver to partitions -->
  <line x1="200" y1="60" x2="120" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <line x1="300" y1="60" x2="300" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <line x1="400" y1="60" x2="480" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <!-- Partitions -->
  <rect x="60" y="95" width="120" height="45" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="120" y="114" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">Part 0</text>
  <text x="120" y="130" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">[0..999]</text>
  <rect x="240" y="95" width="120" height="45" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="300" y="114" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">Part 1</text>
  <text x="300" y="130" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">[1k..2k]</text>
  <rect x="420" y="95" width="120" height="45" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="480" y="114" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#333">Part 2</text>
  <text x="480" y="130" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">[2k..3k]</text>
  <!-- open conn labels + arrows -->
  <line x1="120" y1="140" x2="120" y2="190" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <text x="145" y="170" font-family="Arial, sans-serif" font-size="10" fill="#888">open conn</text>
  <line x1="300" y1="140" x2="300" y2="190" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <text x="325" y="170" font-family="Arial, sans-serif" font-size="10" fill="#888">open conn</text>
  <line x1="480" y1="140" x2="480" y2="190" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <text x="505" y="170" font-family="Arial, sans-serif" font-size="10" fill="#888">open conn</text>
  <!-- Process batch -->
  <rect x="60" y="195" width="120" height="40" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="120" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Process batch</text>
  <rect x="240" y="195" width="120" height="40" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="300" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Process batch</text>
  <rect x="420" y="195" width="120" height="40" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="480" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Process batch</text>
  <!-- close conn labels + arrows -->
  <line x1="120" y1="235" x2="120" y2="290" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <text x="145" y="268" font-family="Arial, sans-serif" font-size="10" fill="#888">close conn</text>
  <line x1="300" y1="235" x2="300" y2="290" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <text x="325" y="268" font-family="Arial, sans-serif" font-size="10" fill="#888">close conn</text>
  <line x1="480" y1="235" x2="480" y2="290" stroke="#333" stroke-width="2" marker-end="url(#arrow-mp)"/>
  <text x="505" y="268" font-family="Arial, sans-serif" font-size="10" fill="#888">close conn</text>
  <!-- Results -->
  <rect x="60" y="295" width="120" height="40" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="120" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Results</text>
  <rect x="240" y="295" width="120" height="40" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="300" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Results</text>
  <rect x="420" y="295" width="120" height="40" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="480" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Results</text>
</svg>

---

## Full Program: Custom Partitioner for Time Series

```python
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
import random

spark = SparkSession.builder \
    .appName("CustomPartitioner") \
    .getOrCreate()
sc = spark.sparkContext

# Generate time-series data: (date_string, value)
base_date = datetime(2024, 1, 1)
data = []
for i in range(100_000):
    day_offset = random.randint(0, 364)
    date = base_date + timedelta(days=day_offset)
    data.append((date.strftime("%Y-%m"), random.random()))

rdd = sc.parallelize(data)

# Partition by month: 12 partitions for 12 months
def month_partitioner(key):
    """Partition by month number (0-11)."""
    month = int(key.split("-")[1])
    return month - 1

partitioned_rdd = rdd.partitionBy(12, month_partitioner)

# Verify partition distribution
def count_partition(index, iterator):
    count = sum(1 for _ in iterator)
    return iter([(index, count)])

distribution = partitioned_rdd.mapPartitionsWithIndex(
    count_partition
).collect()

for part_id, count in sorted(distribution):
    print(f"  Partition {part_id:2d}: {count:6d} records")
```

---

## Partition Skew Detection and Rebalancing

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("SkewDetection") \
    .getOrCreate()

# Create a skewed dataset
data = [(k, v) for k in range(100) for v in range(k * 10)]
df = spark.createDataFrame(data, ["key", "value"])

# Detect skew: check partition sizes
partition_sizes = (
    df.withColumn("partition_id", F.spark_partition_id())
    .groupBy("partition_id")
    .count()
    .orderBy("count", ascending=False)
)
partition_sizes.show(5)

# Compute skew ratio
stats = partition_sizes.agg(
    F.max("count").alias("max_size"),
    F.avg("count").alias("avg_size"),
    F.min("count").alias("min_size")
).collect()[0]

skew_ratio = stats["max_size"] / stats["avg_size"]
print(f"Skew ratio: {skew_ratio:.2f}")
print(f"Ratio > 3.0 indicates significant skew")

# Fix: Repartition with salting
from pyspark.sql.functions import concat, lit, rand

salt_factor = 10
salted_df = df.withColumn(
    "salted_key",
    concat(F.col("key"), lit("_"), (rand() * salt_factor).cast("int"))
)
rebalanced_df = salted_df.repartition(200, "salted_key")
```

---

## Salting Technique for Skewed Joins

```text
Before Salting (skewed):
┌──────────────────────────────┐
│  Partition 0: key=1 (5M rows)│  <-- HOT PARTITION
├──────────────────────────────┤
│  Partition 1: key=2 (100 rows)│
├──────────────────────────────┤
│  Partition 2: key=3 (200 rows)│
└──────────────────────────────┘

After Salting (balanced):
┌──────────────────────────────┐
│  Partition 0: key=1_0 (500K) │
├──────────────────────────────┤
│  Partition 1: key=1_1 (500K) │
├──────────────────────────────┤
│  ...                         │
├──────────────────────────────┤
│  Partition 9: key=1_9 (500K) │
├──────────────────────────────┤
│  Partition 10: key=2 (100)   │
├──────────────────────────────┤
│  Partition 11: key=3 (200)   │
└──────────────────────────────┘
```

---

## Full Program: Broadcast Variable with Lookup

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BroadcastLookup") \
    .getOrCreate()
sc = spark.sparkContext

# Large reference table (e.g., country codes -> names)
country_lookup = {
    "US": "United States", "GB": "United Kingdom",
    "DE": "Germany", "FR": "France", "JP": "Japan",
    "CN": "China", "IN": "India", "BR": "Brazil",
    "CA": "Canada", "AU": "Australia",
}

# Broadcast the lookup table (sent once to each executor)
bc_countries = sc.broadcast(country_lookup)

# Transaction data: (transaction_id, country_code, amount)
transactions = sc.parallelize([
    (1, "US", 100.0), (2, "GB", 200.0),
    (3, "DE", 150.0), (4, "US", 300.0),
    (5, "JP", 250.0), (6, "FR", 175.0),
], numPartitions=3)

# Enrich with country names using broadcast
def enrich_transaction(record):
    txn_id, code, amount = record
    country_name = bc_countries.value.get(code, "Unknown")
    return (txn_id, code, country_name, amount)

enriched = transactions.map(enrich_transaction)
for row in enriched.collect():
    print(f"  Txn {row[0]}: {row[2]} - ${row[3]:.2f}")

# Clean up broadcast variable when done
bc_countries.unpersist()
```

---

## Broadcast Variable Data Flow

```text
┌─────────────────────────────────────────┐
│           Driver Program                 │
│  bc = sc.broadcast(country_lookup)       │
│  Size: 1 KB (sent once per executor)     │
└──────────┬──────────────────────────────┘
           │ broadcast (once)
     ┌─────┼─────────┐
     v     v         v
┌────────┐ ┌────────┐ ┌────────┐
│Executor│ │Executor│ │Executor│
│   0    │ │   1    │ │   2    │
│        │ │        │ │        │
│ lookup │ │ lookup │ │ lookup │
│ (copy) │ │ (copy) │ │ (copy) │
│        │ │        │ │        │
│ Task 0 │ │ Task 1 │ │ Task 2 │
│ Task 3 │ │ Task 4 │ │ Task 5 │
└────────┘ └────────┘ └────────┘

Without broadcast: lookup sent with EVERY task
With broadcast: lookup sent ONCE per executor
```

---

## Accumulator: Complete Error Tracking Example

```python
from pyspark.sql import SparkSession
from pyspark import AccumulatorParam

spark = SparkSession.builder \
    .appName("AccumulatorDemo") \
    .getOrCreate()
sc = spark.sparkContext

# Built-in numeric accumulators
total_records = sc.accumulator(0)
error_count = sc.accumulator(0)
null_count = sc.accumulator(0)

# Custom accumulator for collecting error types
class DictAccumulator(AccumulatorParam):
    def zero(self, initialValue):
        return {}

    def addInPlace(self, v1, v2):
        for key, val in v2.items():
            v1[key] = v1.get(key, 0) + val
        return v1

error_types = sc.accumulator({}, DictAccumulator())

# Process records and track errors
raw_data = sc.parallelize([
    '{"name": "Alice", "age": 30}',
    '{"name": "Bob", "age": null}',
    'CORRUPT_RECORD',
    '{"name": "Charlie", "age": -5}',
    '{"name": "", "age": 25}',
], numPartitions=2)

import json

def validate_and_process(record):
    total_records.add(1)
    try:
        data = json.loads(record)
        if data.get("age") is None:
            null_count.add(1)
            error_types.add({"null_field": 1})
            return None
        if data.get("age", 0) < 0:
            error_count.add(1)
            error_types.add({"negative_age": 1})
            return None
        if not data.get("name"):
            error_count.add(1)
            error_types.add({"empty_name": 1})
            return None
        return data
    except json.JSONDecodeError:
        error_count.add(1)
        error_types.add({"json_parse_error": 1})
        return None

results = raw_data.map(validate_and_process).filter(lambda x: x is not None)
valid_count = results.count()

print(f"Total records:  {total_records.value}")
print(f"Valid records:  {valid_count}")
print(f"Error records:  {error_count.value}")
print(f"Null fields:    {null_count.value}")
print(f"Error breakdown: {error_types.value}")
```

---

## Full Program: Advanced Window Functions

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("WindowFunctions") \
    .getOrCreate()

# Employee salary data
data = [
    ("Engineering", "Alice", 95000, "2020-01-15"),
    ("Engineering", "Bob", 110000, "2019-03-20"),
    ("Engineering", "Charlie", 85000, "2021-06-01"),
    ("Engineering", "Diana", 120000, "2018-11-10"),
    ("Sales", "Eve", 75000, "2020-05-22"),
    ("Sales", "Frank", 82000, "2019-08-14"),
    ("Sales", "Grace", 91000, "2021-02-28"),
    ("Marketing", "Hank", 78000, "2020-09-01"),
    ("Marketing", "Ivy", 88000, "2019-12-15"),
    ("Marketing", "Jack", 72000, "2022-01-10"),
]

df = spark.createDataFrame(
    data, ["department", "name", "salary", "hire_date"]
)

# Window specs
dept_window = Window.partitionBy("department").orderBy("salary")
dept_rows = Window.partitionBy("department") \
    .orderBy("salary") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

# Multiple window functions in one query
result = df.select(
    "department", "name", "salary",
    F.rank().over(dept_window).alias("rank"),
    F.dense_rank().over(dept_window).alias("dense_rank"),
    F.percent_rank().over(dept_window).alias("pct_rank"),
    F.ntile(3).over(dept_window).alias("quartile"),
    F.lag("salary", 1).over(dept_window).alias("prev_salary"),
    F.lead("salary", 1).over(dept_window).alias("next_salary"),
    F.sum("salary").over(dept_rows).alias("running_total"),
    F.avg("salary").over(
        Window.partitionBy("department")
    ).alias("dept_avg"),
)

result.show(truncate=False)
```

---

## Window Function Types Reference

| Category | Functions | Use Case |
|---|---|---|
| Ranking | rank(), dense_rank(), row_number() | Top-N, deduplication |
| Analytic | lag(), lead(), first(), last() | Comparisons, gaps |
| Aggregate | sum(), avg(), min(), max(), count() | Running totals |
| Distribution | percent_rank(), cume_dist(), ntile() | Percentiles |

---

## Full Program: Optimized Join Strategies

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col
import time

spark = SparkSession.builder \
    .appName("JoinOptimization") \
    .config("spark.sql.autoBroadcastJoinThreshold", 10 * 1024 * 1024) \
    .getOrCreate()

# Large fact table: 10M rows
large_df = spark.range(0, 10_000_000).toDF("id") \
    .withColumn("category_id", (col("id") % 1000).cast("int")) \
    .withColumn("amount", (col("id") * 0.01))

# Small dimension table: 1000 rows
small_df = spark.range(0, 1000).toDF("category_id") \
    .withColumn("category_name", col("category_id").cast("string"))

# Strategy 1: Broadcast join (small table fits in memory)
start = time.time()
broadcast_join = large_df.join(
    broadcast(small_df), "category_id"
)
broadcast_join.count()
broadcast_time = time.time() - start
print(f"Broadcast join: {broadcast_time:.2f}s")

# Strategy 2: Sort-merge join (default for large tables)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
start = time.time()
sort_merge_join = large_df.join(small_df, "category_id")
sort_merge_join.count()
sort_merge_time = time.time() - start
print(f"Sort-merge join: {sort_merge_time:.2f}s")

# Verify the plan
broadcast_join.explain()
sort_merge_join.explain()
```

---

## Join Strategy Decision Flow

```text
                    ┌──────────────┐
                    │ Join Request │
                    └──────┬───────┘
                           │
                    ┌──────v───────┐
                    │ Table size?  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              v            v            v
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │ < 10 MB  │ │ 10MB-1GB │ │  > 1 GB  │
       └────┬─────┘ └────┬─────┘ └────┬─────┘
            v            v            v
     ┌────────────┐┌───────────┐┌───────────┐
     │ Broadcast  ││Shuffle    ││Sort-Merge  │
     │ Hash Join  ││Hash Join  ││Join        │
     └────────────┘└───────────┘└───────────┘
     No shuffle     Shuffle      Shuffle+Sort
     O(n)           O(n+m)       O(nlogn)
```

---

## Anti-Patterns and Fixes

| Anti-Pattern | Problem | Fix |
|---|---|---|
| collect() in UDF | OOM on driver | Use broadcast variable |
| groupByKey() | Shuffles all data | Use reduceByKey() |
| repartition(1) | Single partition bottleneck | Use coalesce() for reduction |
| No persistence | Recomputation on reuse | cache() or persist() |
| Python UDFs | Serialization overhead | Use pandas_udf or built-in functions |
| cartesian joins | Exploding data | Add join condition |

---

## Full Program: Efficient Data Pipeline

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("EfficientPipeline") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .getOrCreate()

# Define schema upfront (avoid schema inference)
schema = StructType([
    StructField("user_id", LongType(), False),
    StructField("event_type", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("properties", StringType(), True),
])

# Read with explicit schema
events = spark.read.schema(schema).parquet("/data/events/")

# Filter early (predicate pushdown)
filtered = events.filter(
    (F.col("event_type") == "purchase") &
    (F.col("timestamp") >= "2024-01-01")
)

# Select only needed columns (column pruning)
projected = filtered.select(
    "user_id", "timestamp",
    F.get_json_object("properties", "$.amount").cast("double").alias("amount"),
    F.get_json_object("properties", "$.product_id").alias("product_id"),
)

# Cache intermediate result used multiple times
projected.cache()

# Aggregation 1: Revenue per user
revenue_per_user = projected.groupBy("user_id").agg(
    F.sum("amount").alias("total_revenue"),
    F.count("*").alias("purchase_count"),
    F.avg("amount").alias("avg_order_value"),
)

# Aggregation 2: Revenue per product
revenue_per_product = projected.groupBy("product_id").agg(
    F.sum("amount").alias("product_revenue"),
    F.countDistinct("user_id").alias("unique_buyers"),
)

# Write results
revenue_per_user.write.mode("overwrite").parquet("/output/user_revenue/")
revenue_per_product.write.mode("overwrite").parquet("/output/product_revenue/")

# Clean up
projected.unpersist()
```

---

## Pipeline Optimization Checklist

```text
┌─────────────────────────────────────────────┐
│          Pipeline Optimization               │
├─────────────────────────────────────────────┤
│                                              │
│  1. Schema Definition                        │
│     [ ] Explicit schema (no inference)       │
│     [ ] Appropriate data types               │
│     [ ] Nullable flags set correctly         │
│                                              │
│  2. Predicate Pushdown                       │
│     [ ] Filter as early as possible          │
│     [ ] Use partition columns in filters     │
│     [ ] Avoid UDFs in filter conditions      │
│                                              │
│  3. Column Pruning                           │
│     [ ] Select only needed columns           │
│     [ ] Drop columns before joins            │
│     [ ] Avoid SELECT *                       │
│                                              │
│  4. Join Optimization                        │
│     [ ] Broadcast small tables               │
│     [ ] Filter before joining                │
│     [ ] Avoid cartesian products             │
│                                              │
│  5. Caching                                  │
│     [ ] Cache reused DataFrames              │
│     [ ] Unpersist when done                  │
│     [ ] Choose appropriate storage level     │
│                                              │
│  6. Shuffle Management                       │
│     [ ] Tune shuffle partitions              │
│     [ ] Coalesce before writing              │
│     [ ] Enable AQE                           │
│                                              │
└─────────────────────────────────────────────┘
```

---

## Configuration Tuning: Key Parameters

```python
# Memory configuration
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.executor.memoryOverhead", "2g")
spark.conf.set("spark.memory.fraction", 0.8)
spark.conf.set("spark.memory.storageFraction", 0.3)

# Shuffle configuration
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.shuffle.spill.compress", "true")

# Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")

# Serialization
spark.conf.set("spark.serializer",
    "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.kryoserializer.buffer.max", "1024m")

# Dynamic allocation
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "100")
```

---

## Storage Level Comparison

| Storage Level | Space | CPU | In Memory | On Disk | Replicated |
|---|---|---|---|---|---|
| MEMORY_ONLY | High | Low | Yes | No | No |
| MEMORY_AND_DISK | High | Medium | Partial | Partial | No |
| MEMORY_ONLY_SER | Low | High | Yes | No | No |
| MEMORY_AND_DISK_SER | Low | High | Partial | Partial | No |
| DISK_ONLY | Low | High | No | Yes | No |
| MEMORY_ONLY_2 | High | Low | Yes | No | Yes |

---

## When to Use Each Storage Level

```python
from pyspark import StorageLevel

# Default: fits in memory, fast access needed
df.cache()  # equivalent to MEMORY_AND_DISK

# Large dataset, memory constrained
df.persist(StorageLevel.MEMORY_AND_DISK_SER)

# Recomputation is cheap, memory is scarce
df.persist(StorageLevel.DISK_ONLY)

# Critical data, must not be lost
df.persist(StorageLevel.MEMORY_AND_DISK_2)

# Check if cached
print(f"Is cached: {df.is_cached}")

# Check storage level
print(f"Storage level: {df.storageLevel}")

# Unpersist when done
df.unpersist()
```
