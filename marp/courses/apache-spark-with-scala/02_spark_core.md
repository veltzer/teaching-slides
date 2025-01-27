# Spark Core

## What is Spark Core?

1. Foundation of Spark ecosystem
1. Provides basic functionality
1. Implements RDDs
1. Handles task scheduling
1. Manages memory

---

## Core Components

![0](../../../out/mermaid/marp/courses/apache-spark-with-scala/02_spark_core.md/0.png)

---

## RDD Basics

![1](../../../out/mermaid/marp/courses/apache-spark-with-scala/02_spark_core.md/1.png)

---

## RDD Characteristics

1. Immutable
1. Partitioned
1. Lazy evaluation
1. Fault-tolerant
1. Type-safe

---

## Creating RDDs

```scala
// From a collection
val data = Array(1, 2, 3, 4, 5)
val rdd = sc.parallelize(data)

// From a file
val textFile = sc.textFile("data.txt")

// From another RDD
val mappedRDD = rdd.map(_ * 2)
```

---

## RDD Operations Flow

![2](../../../out/mermaid/marp/courses/apache-spark-with-scala/02_spark_core.md/2.png)

---

## Transformations Hierarchy

![3](../../../out/mermaid/marp/courses/apache-spark-with-scala/02_spark_core.md/3.png)

---

## Transformation Examples

```scala
// Map transformation
val numbers = sc.parallelize(1 to 10)
val doubled = numbers.map(_ * 2)

// Filter transformation
val evens = numbers.filter(_ % 2 == 0)

// FlatMap transformation
val lines = sc.parallelize(List("hello world", "hi there"))
val words = lines.flatMap(_.split(" "))
```

---

## Action Types

![4](../../../out/mermaid/marp/courses/apache-spark-with-scala/02_spark_core.md/4.png)

---

## Action Examples

```scala
// Collect action
val result = doubled.collect()

// Count action
val total = evens.count()

// Reduce action
val sum = numbers.reduce(_ + _)
```

---

[Continue with remaining slides, adding mermaid diagrams for concepts like:]

## Execution Model

![5](../../../out/mermaid/marp/courses/apache-spark-with-scala/02_spark_core.md/5.png)

---

## Data Partitioning

![6](../../../out/mermaid/marp/courses/apache-spark-with-scala/02_spark_core.md/6.png)

[Continue with remaining content and diagrams...]
