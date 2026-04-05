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

<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Driver Program -->
  <rect x="320" y="30" width="160" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="400" y="65" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Driver Program</text>

  <!-- Spark Context -->
  <rect x="320" y="130" width="160" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="400" y="165" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Spark Context</text>

  <!-- Cluster Manager -->
  <rect x="320" y="230" width="160" height="60" rx="5" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="2"/>
  <text x="400" y="265" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Cluster Manager</text>

  <!-- Worker Nodes -->
  <rect x="80" y="350" width="140" height="60" rx="5" fill="#d1f2eb" stroke="#55a3a0" stroke-width="2"/>
  <text x="150" y="385" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Worker Node 1</text>

  <rect x="330" y="350" width="140" height="60" rx="5" fill="#d1f2eb" stroke="#55a3a0" stroke-width="2"/>
  <text x="400" y="385" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Worker Node 2</text>

  <rect x="580" y="350" width="140" height="60" rx="5" fill="#d1f2eb" stroke="#55a3a0" stroke-width="2"/>
  <text x="650" y="385" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Worker Node n</text>

  <!-- Executors -->
  <rect x="85" y="460" width="130" height="50" rx="5" fill="#ffefd5" stroke="#ffa500" stroke-width="2"/>
  <text x="150" y="490" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Executor 1</text>

  <rect x="335" y="460" width="130" height="50" rx="5" fill="#ffefd5" stroke="#ffa500" stroke-width="2"/>
  <text x="400" y="490" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Executor 2</text>

  <rect x="585" y="460" width="130" height="50" rx="5" fill="#ffefd5" stroke="#ffa500" stroke-width="2"/>
  <text x="650" y="490" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Executor n</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Driver to Spark Context -->
  <line x1="400" y1="90" x2="400" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Spark Context to Cluster Manager -->
  <line x1="400" y1="190" x2="400" y2="230" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Cluster Manager to Worker Nodes -->
  <line x1="360" y1="290" x2="180" y2="350" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="400" y1="290" x2="400" y2="350" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="440" y1="290" x2="620" y2="350" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Worker Nodes to Executors -->
  <line x1="150" y1="410" x2="150" y2="460" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="400" y1="410" x2="400" y2="460" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="650" y1="410" x2="650" y2="460" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Main RDD Operations node -->
  <rect x="50" y="170" width="150" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="125" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">RDD Operations</text>

  <!-- Transformations branch -->
  <rect x="280" y="80" width="150" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="355" y="115" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Transformations</text>

  <!-- Actions branch -->
  <rect x="280" y="260" width="150" height="60" rx="5" fill="#f8d7da" stroke="#dc3545" stroke-width="2"/>
  <text x="355" y="295" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Actions</text>

  <!-- Transformation operations -->
  <rect x="510" y="30" width="180" height="50" rx="5" fill="#e7f5e7" stroke="#5cb85c" stroke-width="2"/>
  <text x="600" y="60" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">map, filter, flatMap</text>

  <rect x="510" y="100" width="180" height="50" rx="5" fill="#e7f5e7" stroke="#5cb85c" stroke-width="2"/>
  <text x="600" y="130" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">union, intersection</text>

  <!-- Action operations -->
  <rect x="510" y="210" width="180" height="50" rx="5" fill="#fde7e7" stroke="#f5c6cb" stroke-width="2"/>
  <text x="600" y="240" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">reduce, collect, count</text>

  <rect x="510" y="280" width="180" height="50" rx="5" fill="#fde7e7" stroke="#f5c6cb" stroke-width="2"/>
  <text x="600" y="310" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">take, saveAsTextFile</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Main to Transformations -->
  <line x1="200" y1="180" x2="280" y2="120" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Main to Actions -->
  <line x1="200" y1="220" x2="280" y2="280" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Transformations to operations -->
  <line x1="430" y1="100" x2="510" y2="55" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="430" y1="120" x2="510" y2="125" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Actions to operations -->
  <line x1="430" y1="280" x2="510" y2="235" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="430" y1="300" x2="510" y2="305" stroke="#666" stroke-width="2" marker-end="url(#arrow2)"/>
</svg>

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

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Input Data -->
  <rect x="50" y="120" width="120" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="110" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Input Data</text>

  <!-- Map Phase -->
  <rect x="230" y="120" width="120" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="290" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Map Phase</text>

  <!-- Shuffle -->
  <rect x="410" y="120" width="120" height="60" rx="5" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
  <text x="470" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Shuffle</text>

  <!-- Reduce Phase -->
  <rect x="590" y="120" width="120" height="60" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="650" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Reduce Phase</text>

  <!-- Final Result -->
  <rect x="770" y="120" width="120" height="60" rx="5" fill="#f8d7da" stroke="#dc3545" stroke-width="2"/>
  <text x="830" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Final Result</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Connect the phases -->
  <line x1="170" y1="150" x2="230" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="350" y1="150" x2="410" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="530" y1="150" x2="590" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="710" y1="150" x2="770" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow3)"/>
</svg>

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

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Performance Optimization (root) -->
  <rect x="300" y="30" width="200" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="400" y="65" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Performance Optimization</text>

  <!-- Caching -->
  <rect x="80" y="180" width="120" height="50" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="140" y="210" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Caching</text>

  <!-- Partitioning -->
  <rect x="240" y="180" width="120" height="50" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="300" y="210" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Partitioning</text>

  <!-- Serialization -->
  <rect x="400" y="180" width="120" height="50" rx="5" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
  <text x="460" y="210" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Serialization</text>

  <!-- Memory Management -->
  <rect x="180" y="300" width="160" height="50" rx="5" fill="#f8d7da" stroke="#dc3545" stroke-width="2"/>
  <text x="260" y="330" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Memory Management</text>

  <!-- Shuffle Optimization -->
  <rect x="380" y="300" width="160" height="50" rx="5" fill="#e2d5f1" stroke="#6f42c1" stroke-width="2"/>
  <text x="460" y="330" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Shuffle Optimization</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- From root to branches -->
  <line x1="350" y1="90" x2="160" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="380" y1="90" x2="300" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="420" y1="90" x2="460" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="370" y1="90" x2="260" y2="300" stroke="#666" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="430" y1="90" x2="460" y2="300" stroke="#666" stroke-width="2" marker-end="url(#arrow4)"/>
</svg>

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
