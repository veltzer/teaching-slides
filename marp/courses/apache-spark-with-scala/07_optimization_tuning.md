# Spark Optimization and Tuning

## Performance Overview

1. Memory Management
1. CPU Utilization
1. I/O Operations
1. Network Usage
1. Resource Allocation

## Memory Architecture

![0](../../../out/mermaid/marp/courses/apache-spark-with-scala/07_optimization_tuning.md/0.png)

## Memory Configuration

```scala
spark.conf.set("spark.memory.fraction", 0.75)
spark.conf.set("spark.memory.storageFraction", 0.5)
spark.conf.set("spark.driver.memory", "4g")
spark.conf.set("spark.executor.memory", "4g")
```

## Data Serialization

1. Java Serialization
1. Kryo Serialization
1. Custom Serializers
1. Compression Settings
1. Schema Optimization

## Execution Tuning

![1](../../../out/mermaid/marp/courses/apache-spark-with-scala/07_optimization_tuning.md/1.png)

## Partitioning Strategy

```scala
// Repartition data
df.repartition(numPartitions)
// Partition by column
df.repartitionByRange(col("timestamp"))
// Coalesce for reducing partitions
df.coalesce(numPartitions)
```

## Shuffle Operations

1. Reduce Shuffling
1. Partition Tuning
1. Memory Settings
1. Disk Spill
1. Network Transfer

## Caching Strategies

```scala
// Memory only
df.cache()
// Memory and disk
df.persist(StorageLevel.MEMORY_AND_DISK)
// Memory and disk serialized
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
```

## Resource Management

![2](../../../out/mermaid/marp/courses/apache-spark-with-scala/07_optimization_tuning.md/2.png)

## SQL Optimization

1. Predicate Pushdown
1. Column Pruning
1. Join Optimization
1. Broadcast Hints
1. Query Plan Analysis

## Broadcast Joins

```scala
import org.apache.spark.sql.functions.broadcast
val joinedDF = largeDF.join(
  broadcast(smallDF),
  Seq("key")
)
```

## Data Skew Handling

```scala
// Add random prefix
val saltedDF = df.withColumn(
  "salt",
  rand() * numPartitions
)
// Join with salt
val joinedDF = saltedDF.join(
  otherDF,
  Seq("key", "salt")
)
```

## Monitoring Tools

1. Spark UI
1. Metrics System
1. JVM Profiling
1. Ganglia Integration
1. Custom Metrics

## Configuration Best Practices

![3](../../../out/mermaid/marp/courses/apache-spark-with-scala/07_optimization_tuning.md/3.png)

## Performance Checklist

1. Memory Configuration
1. Partition Sizing
1. Shuffle Management
1. Cache Strategy
1. Resource Allocation
