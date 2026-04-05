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
