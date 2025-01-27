# Introduction to Apache Spark

## Overview of Big Data

1. Volume - Scale of data
1. Velocity - Speed of data generation
1. Variety - Different types of data
1. Veracity - Uncertainty of data
1. Value - Business impact

## Big Data Challenges

1. Data Storage
1. Data Processing
1. Data Analysis
1. Real-time Processing
1. Resource Management

## Evolution of Big Data Technologies

1. Traditional Databases
1. MapReduce & Hadoop
1. Apache Spark
1. Modern Data Lake Architecture

## Traditional vs Big Data Processing

```mermaid
graph LR
    A[Traditional] --> B[Single Machine]
    A --> C[Vertical Scaling]
    A --> D[RDBMS]
    E[Big Data] --> F[Distributed Systems]
    E --> G[Horizontal Scaling]
    E --> H[NoSQL/Distributed Storage]
```

## Apache Spark Overview

1. Open-source unified analytics engine
1. In-memory computation
1. Fault tolerance
1. Lazy evaluation
1. Multiple language support

## Spark vs Hadoop MapReduce

```mermaid
graph TB
    subgraph MapReduce
    A[Disk-Based] --> B[Batch Processing]
    B --> C[Complex Implementation]
    end
    subgraph Spark
    D[In-Memory] --> E[Interactive & Streaming]
    E --> F[Simple APIs]
    end
```

## Spark Components

```mermaid
graph TB
    A[Spark Core] --> B[Spark SQL]
    A --> C[Spark Streaming]
    A --> D[MLlib]
    A --> E[GraphX]
    style A fill:#f9f,stroke:#333
```

## Spark Architecture

```mermaid
graph TB
    A[Driver Program] --> B[Cluster Manager]
    B --> C[Worker Node 1]
    B --> D[Worker Node 2]
    B --> E[Worker Node N]
    C --> F[Executor 1]
    D --> G[Executor 2]
    E --> H[Executor N]
```

## Driver Program

1. Contains application's main function
1. Creates SparkContext
1. Declares transformations and actions
1. Coordinates work distribution

## Spark Context

```scala
// Creating Spark Context
import org.apache.spark.{SparkConf, SparkContext}

val conf = new SparkConf()
  .setAppName("MySparkApp")
  .setMaster("local[*]")

val sc = new SparkContext(conf)
```

## Executors

1. Run on worker nodes
1. Execute tasks
1. Store data in memory or disk
1. Return results to driver

## Cluster Manager Types

1. Standalone
1. YARN
1. Mesos
1. Kubernetes

## Cluster Manager Responsibilities

```mermaid
graph LR
    A[Cluster Manager] --> B[Resource Allocation]
    A --> C[Node Management]
    A --> D[Job Scheduling]
    A --> E[Fault Recovery]
```

## DAG - Directed Acyclic Graph

```mermaid
graph LR
    A[Read Data] --> B[Filter]
    B --> C[Map]
    C --> D[Group]
    D --> E[Aggregate]
    E --> F[Save]
```

## Stages in Spark

1. DAG scheduler breaks job into stages
1. Each stage contains multiple tasks
1. Stages are separated by shuffle operations

## Task Execution

```mermaid
graph TB
    A[Task] --> B[Read Input]
    B --> C[Process Data]
    C --> D[Write Output]
    D --> E[Return Status]
```

## Memory Management

1. Execution Memory
1. Storage Memory
1. User Memory
1. Reserved Memory

## Performance Considerations

1. Data serialization
1. Memory allocation
1. Shuffle operations
1. Data locality

## Best Practices

1. Proper partition sizing
1. Cache reused data
1. Minimize shuffling
1. Use appropriate data formats

## Local vs Cluster Mode

```mermaid
graph TB
    subgraph Local
    A[Single JVM] --> B[All Components]
    end
    subgraph Cluster
    C[Distributed] --> D[Multiple JVMs]
    D --> E[Multiple Machines]
    end
```

## Spark Web UI

1. Application monitoring
1. Job progress tracking
1. Memory usage
1. Executor information
1. Stage details

## Data Lineage

```mermaid
graph LR
    A[Source] --> B[Transform 1]
    B --> C[Transform 2]
    C --> D[Action]
    style D fill:#f96
```

## Fault Tolerance

1. RDD lineage tracking
1. Executor failure handling
1. Task retry mechanism
1. Checkpoint support
