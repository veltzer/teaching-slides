# Spark Core Training

---

## What is Apache Spark

- Unified analytics engine for large-scale data processing
- Up to 100x faster than Hadoop MapReduce in memory
- Supports multiple programming languages (Java, Scala, Python, R)
- Built around speed, ease of use, and sophisticated analytics
- Runs everywhere: Hadoop, Mesos, Kubernetes, standalone, or in the cloud

---

## Spark Architecture

![spark_architecture](/svg/courses/big_data/apache-spark-with-python/02_core/spark_architecture.svg)

---

## Key Components

| Component | Description |
|-----------|-------------|
| Driver Program | Contains application's main function; Creates SparkContext |
| Spark Context | Coordinates and manages job execution on the cluster |
| Cluster Manager | Allocates resources across applications |
| Worker Node | Compute node in the Spark cluster |
| Executor | Process launched for an application on a worker node |

---

## RDD Basics

- RDD = Resilient Distributed Dataset
- Fundamental data structure of Spark
- Immutable, partitioned collection of elements
- Can be operated on in parallel

---

## RDD Characteristics

1. **Resilient**: Fault-tolerant with lineage graph
1. **Distributed**: Data split across nodes
1. **Dataset**: Collection of partitioned data
1. **Immutable**: Cannot be modified after creation
1. **Lazy Evaluation**: Transformations are not executed until an action is triggered

---

## Creating RDDs

```python
# From a Python collection
numbers = sc.parallelize([1, 2, 3, 4, 5])

# From a text file
logs = sc.textFile("logs.txt")

# From another RDD
filtered = numbers.filter(lambda x: x > 2)
```

---

## RDD Operations Types

![rdd_operations_types](/svg/courses/big_data/apache-spark-with-python/02_core/rdd_operations_types.svg)

---

## Transformations

- Create new RDD from existing one
- Lazy evaluation
- Examples:
    - `map()`
    - `filter()`
    - `flatMap()`
    - `union()`
    - `distinct()`

---

## Common Transformations Example

```python
# Original RDD
data = sc.parallelize([1, 2, 3, 4, 5])

# map transformation
squared = data.map(lambda x: x * x)

# filter transformation
evens = data.filter(lambda x: x % 2 == 0)

# flatMap transformation
words = sc.parallelize(["Hello World", "Hi There"])
letters = words.flatMap(lambda x: x.split())
```

---

## Actions

- Return values to driver program
- Trigger computation
- Examples:
    - `collect()`
    - `count()`
    - `first()`
    - `take(n)`
    - `reduce()`

---

## Common Actions Example

```python
# Create RDD
numbers = sc.parallelize([1, 2, 3, 4, 5])

# count action
total = numbers.count()  # Returns: 5

# collect action
all_nums = numbers.collect()  # Returns: [1,2,3,4,5]

# reduce action
sum = numbers.reduce(lambda a, b: a + b)  # Returns: 15
```

---

## Chaining Transformations

```python
# Complex data processing chain
result = sc.textFile("data.txt") \
    .map(lambda x: x.split()) \
    .filter(lambda x: len(x) > 0) \
    .flatMap(lambda x: x) \
    .map(lambda x: (x, 1)) \
    .reduceByKey(lambda a, b: a + b)
```

---

## Lambda Functions in Spark

- Anonymous functions
- Used for simple operations
- Common in transformations and actions

```python
# Lambda function examples
square = lambda x: x * x
add = lambda x, y: x + y
first_elem = lambda x: x[0]
```

---

## Map Reduce Concept

![map_reduce_concept](/svg/courses/big_data/apache-spark-with-python/02_core/map_reduce_concept.svg)

---

## Shuffle Operations

- Redistributes data across partitions
- Network-intensive operation
- Examples:
    - `groupByKey()`
    - `reduceByKey()`
    - `join()`
    - `repartition()`

---

## Shuffle Impact

| Operation | Shuffle Required? | Performance Impact |
|-----------|------------------|-------------------|
| map() | No | Fast |
| filter() | No | Fast |
| reduceByKey() | Yes | Medium |
| groupByKey() | Yes | Slow |
| join() | Yes | Slow |

---

## Caching in Spark

- Persists RDD in memory/disk
- Speeds up iterative algorithms
- Different storage levels available

---

## Storage Levels

| Level | Memory | Disk | Description |
|-------|---------|------|-------------|
| MEMORY_ONLY | Yes | No | Default, pure memory |
| MEMORY_AND_DISK | Yes | Yes | Spill to disk if needed |
| DISK_ONLY | No | Yes | Only disk storage |
| OFF_HEAP | No | No | Off-heap memory storage |

---

## Caching Example

```python
# Cache RDD in memory
rdd.cache()

# Persist with specific storage level
from pyspark import StorageLevel
rdd.persist(StorageLevel.MEMORY_AND_DISK)
```

---

## Web Monitoring Example

```python
# Real-time log analysis
logs = sc.textFile("access_logs.txt")

# Parse logs and count errors
errors = logs.filter(lambda line: "ERROR" in line) \
    .map(lambda line: (line.split()[0], 1)) \
    .reduceByKey(lambda a, b: a + b)
```

---

## Common Use Cases

1. Log Analysis
1. ETL Operations
1. Machine Learning
1. Real-time Processing
1. Data Warehousing

---

## Serialization

- Process of converting objects to byte stream
- Important for distributed processing
- Python uses pickle by default
- Custom serializers possible

---

## Serialization Best Practices

1. Use simple data types when possible
1. Implement custom serialization for complex objects
1. Avoid serializing large objects
1. Consider using Kryo serialization
1. Monitor serialization overhead

---

## Performance Optimization

![performance_optimization](/svg/courses/big_data/apache-spark-with-python/02_core/performance_optimization.svg)

---

## Troubleshooting Common Issues

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Out of Memory | Large data/poor caching | Adjust partition size |
| Slow Performance | Poor parallelization | Optimize partitioning |
| Serialization Errors | Complex objects | Simplify data structures |
| Job Failures | Resource constraints | Monitor resource usage |

---

## Spark UI

- Web interface for monitoring
- Shows application details
- Tracks job progress
- Debugging tool
- Performance metrics

---

## Best Practices

1. Use appropriate number of partitions
1. Minimize shuffling operations
1. Cache wisely
1. Monitor through Spark UI
1. Use broadcast variables for lookups

---

## Wrap Up

- Spark Core fundamentals
- RDD operations and management
- Performance optimization
- Troubleshooting strategies
- Best practices
