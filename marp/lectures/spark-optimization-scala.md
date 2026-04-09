# Spark Optimization
## Understanding Data Skew and Memory Pressure
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/spark-optimization-scala/title.svg)

## Understanding Data Skew 🔄

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
```scala
// Skewed user activity data
df.groupBy("user_id").count()  // Some users very active

// Geographic data concentration
df.groupBy("city").agg(count("*").as("count"))  // Major cities dominate
```

---

## Repartitioning Strategy ⚖️

**Default Configuration**:
```scala
val df = dataFrame.repartition(200)
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

```scala
// Single column partitioning
val df = dataFrame.repartition(200, col("user_id"))

// Multiple column partitioning
val df = dataFrame.repartition(200, col("date"), col("region"))

// Range partitioning
val df = dataFrame.repartitionByRange(200, col("timestamp"))
```

**Best Practices**:
- Target partition size: 100MB-1GB
- Monitor sizes: `df.rdd.glom().map(_.length).collect()`

---

## Memory Management Overview 🧠

**Key Components**:
- Execution memory (computations)
- Storage memory (caching)
- User memory (data structures)
- Reserved memory (internal ops)

---

## Memory Fraction Configuration ⚙️

```scala
spark.conf.set("spark.memory.fraction", "0.8")
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

```scala
spark.conf.set("spark.memory.storageFraction", "0.3")
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
```scala
// Enable detailed metrics
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

```scala
// Comprehensive configuration
spark.conf.set("spark.memory.fraction", "0.8")
spark.conf.set("spark.memory.storageFraction", "0.3")

// Skew handling
val df = dataFrame.repartition(200)
  .persist(StorageLevel.MEMORY_AND_DISK)

// Broadcast optimization
val broadcast_threshold = 100 * 1024 * 1024  // 100MB
spark.conf.set("spark.sql.autoBroadcastJoinThreshold",
               broadcast_threshold.toString)

// Enable adaptive execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
```
