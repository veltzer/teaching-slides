# Spark Core

## What is Spark Core?

1. Foundation of Spark ecosystem
1. Provides basic functionality
1. Implements RDDs
1. Handles task scheduling
1. Manages memory

---

## Core Components

```mermaid
graph TB
    A[Spark Core] --> B[RDD API]
    A --> C[Task Scheduler]
    A --> D[Memory Manager]
    A --> E[Shuffle System]
    style A fill:#f96
```

---

## RDD Basics

```mermaid
graph LR
    A[RDD] --> B[Resilient]
    A --> C[Distributed]
    A --> D[Dataset]
    B --> E[Fault Tolerant]
    C --> F[Parallel Processing]
    D --> G[Data Collection]
```

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

```mermaid
graph LR
    A[Source RDD] --> B[Transformations]
    B --> C[More Transformations]
    C --> |Triggers| D[Action]
    D --> E[Result]
    B -.-> F[Lazy]
    C -.-> F
```

---

## Transformations Hierarchy

```mermaid
graph TB
    A[Transformations] --> B[Narrow]
    A --> C[Wide]
    B --> D[map]
    B --> E[filter]
    C --> F[groupByKey]
    C --> G[reduceByKey]
```

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

```mermaid
graph TB
    A[Actions] --> B[Value Return]
    A --> C[Data Export]
    B --> D[collect]
    B --> E[count]
    C --> F[save]
    C --> G[foreach]
```

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

```mermaid
graph TB
    A[RDD] --> B[DAG Creation]
    B --> C[Stage Division]
    C --> D[Task Generation]
    D --> E[Task Distribution]
    E --> F[Execution]
```

---

## Data Partitioning

```mermaid
graph LR
    subgraph Partition 1
    A[Data Chunk 1]
    end
    subgraph Partition 2
    B[Data Chunk 2]
    end
    subgraph Partition 3
    C[Data Chunk 3]
    end
    D[Task] --> A
    D --> B
    D --> C
```

[Continue with remaining content and diagrams...]
