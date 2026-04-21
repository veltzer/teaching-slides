---
tags:
- tools:spark
- languages:python
- data-and-ai:big-data
- concepts:performance
level: advanced
category: big-data
audience:
- audiences:developers
- audiences:data-engineers

---
# Spark Optimization
## Understanding Data Skew and Memory Pressure
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Understanding Data Skew 🔄

![title](svg/lectures/big_data/spark-optimization-python/title.svg)

---

## Understanding Data Skew 🔄: Details

- **Definition**: Uneven distribution of data across partitions
- **Symptoms**:
    - Few executors doing most work
    - Significant task duration variance
    - "Straggler" tasks in stage view
- **Impact**: Reduces parallel processing efficiency

---

## Common Causes of Data Skew 🎯

- Hot keys in join operations
- Imbalanced key distribution in groupBy
- Non-uniform data distribution

**Real-world examples**:
```python
// Skewed user activity data
df.groupBy("user_id").count()  // Some users very active

// Geographic data concentration
df.groupBy("city").count()     // Major cities dominate
```

---

## Repartitioning Strategy ⚖️

**Default Configuration**:
```python
df = df.repartition(200)
```

**When to Increase Partitions (>200)**:
- Large dataset (>1TB)
- Many concurrent operations
- High-memory computations

**When to Decrease Partitions (<200)**:
- Small dataset (<100GB)
- Simple transformations
- Limited cluster resources

---

## Advanced Repartitioning Techniques 🛠️

```python
# Single column partitioning
df.repartition(200, "user_id")

# Multiple column partitioning
df.repartition(200, "date", "region")

# Range partitioning
df.repartitionByRange(200, "timestamp")
```

**Best Practices**:
- Target partition size: 100MB-1GB
- Monitor sizes: `df.rdd.glom().map(len).collect()`

---

## Memory Management Overview 🧠

**Key Components**:
- Execution memory (computations)
- Storage memory (caching)
- User memory (data structures)
- Reserved memory (internal ops)

---

## Memory Fraction Configuration ⚙️

```python
spark.conf.set("spark.memory.fraction", 0.8)
```

**When to Increase (>0.8)**:
- Heavy computational workloads
- Large shuffle operations
- Complex joins

**When to Decrease (<0.8)**:
- More user-defined structures needed
- External service integration
- Off-heap operations

---

## Storage Fraction Settings 💾

```python
spark.conf.set("spark.memory.storageFraction", 0.3)
```

**Increase (>0.3) when**:
- Heavy caching needs
- Frequent data reuse
- Many broadcast joins

**Decrease (<0.3) when**:
- Need more execution memory
- Limited data reuse
- Memory-intensive compute

---

## Monitoring and Tuning 📊

**Essential Metrics**:
- Storage tab: Cache usage
- Executors tab: Memory consumption
- Stages tab: Spill metrics

**External Monitoring**:
```python
# Enable detailed metrics
spark.conf.set("spark.eventLog.enabled", "true")
spark.conf.set("spark.eventLog.dir", "/path/to/logs")
```

---

## Best Practices Checklist ✅

1. **Start Default**:
    - Begin with standard settings
    - Establish baseline metrics
1. **Monitor**:
    - Track memory patterns
    - Observe GC behavior
    - Check spill metrics
1. **Tune Incrementally**:
    - One parameter at a time
    - Document changes
    - Validate improvements

---

## Advanced Optimization Techniques 🚀

```python
# Comprehensive configuration
spark.conf.set("spark.memory.fraction", 0.8)
spark.conf.set("spark.memory.storageFraction", 0.3)

# Skew handling
df = df.repartition(200)\
       .persist(StorageLevel.MEMORY_AND_DISK)

# Broadcast optimization
broadcast_threshold = 100 * 1024 * 1024  # 100MB
spark.conf.set("spark.sql.autoBroadcastJoinThreshold",
               broadcast_threshold)

# Enable adaptive execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
```
