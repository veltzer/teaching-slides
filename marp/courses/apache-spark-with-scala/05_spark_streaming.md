# Spark Streaming

## Introduction to Streaming

1. Real-time processing
1. Stream sources
1. Window operations
1. State management
1. Fault tolerance

---

## Streaming Architecture

```mermaid
graph LR
    A[Data Sources] --> B[Receivers]
    B --> C[DStreams]
    C --> D[Processing]
    D --> E[Output]
    style C fill:#f96
```

---

## Processing Models

```mermaid
graph TB
    A[Processing] --> B[Micro-batch]
    A --> C[Continuous]
    B --> D[DStream]
    C --> E[Structured Streaming]
    style A fill:#f96
```

---

## DStream Basics

```scala
import org.apache.spark.streaming._
val conf = new SparkConf().setAppName("StreamingApp")
val ssc = new StreamingContext(conf, Seconds(1))
```

---

## Stream Sources

```mermaid
graph TB
    A[Sources] --> B[Kafka]
    A --> C[Flume]
    A --> D[Kinesis]
    A --> E[Socket]
    A --> F[Files]
    style A fill:#f96
```

---

## Kafka Integration Flow

```mermaid
graph LR
    A[Kafka] --> B[Consumer]
    B --> C[DStream]
    C --> D[Processing]
    D --> E[Results]
    E --> F[Storage]
```

---

## Kafka Setup

```scala
import org.apache.spark.streaming.kafka010._
val kafkaParams = Map(
  "bootstrap.servers" -> "localhost:9092",
  "key.deserializer" -> classOf[StringDeserializer],
  "value.deserializer" -> classOf[StringDeserializer],
  "group.id" -> "spark_streaming_group"
)
```

---

## Window Operations

```mermaid
graph LR
    subgraph Window 1
    A[Batch 1] --> B[Batch 2]
    end
    subgraph Window 2
    B --> C[Batch 3]
    end
    subgraph Window 3
    C --> D[Batch 4]
    end
```

---

## Windowing Types

```mermaid
graph TB
    A[Windows] --> B[Sliding]
    A --> C[Tumbling]
    B --> D[Overlap]
    C --> E[No Overlap]
    style A fill:#f96
```

---

## Window Configuration

```scala
// Window duration
val windowLength = Seconds(30)
// Sliding interval
val slidingInterval = Seconds(10)
// Apply window
val windowedStream = stream.window(
  windowLength,
  slidingInterval
)
```

---

## Stateful Operations

```mermaid
graph TB
    A[State] --> B[Initialize]
    B --> C[Update]
    C --> D[Cleanup]
    D --> B
    style C fill:#f96
```

---

## State Implementation

```scala
val words = lines.flatMap(_.split(" "))
val pairs = words.map(word => (word, 1))
val wordCounts = pairs.updateStateByKey(updateFunction)
```

---

## Checkpointing

```mermaid
graph LR
    A[Stream] --> B[Process]
    B --> C[Checkpoint]
    C --> D[Recovery]
    D -.-> A
    style C fill:#f96
```

---

## Checkpoint Setup

```scala
ssc.checkpoint("checkpoint_directory")
def functionToCreateContext(): StreamingContext = {
  val ssc = new StreamingContext(...)
  ssc.checkpoint("checkpoint_directory")
  ssc
}
```

---

## Output Operations

```mermaid
graph TB
    A[Output] --> B[print]
    A --> C[saveAsFiles]
    A --> D[foreachRDD]
    B --> E[Debug]
    C --> F[Storage]
    D --> G[Custom]
```

---

## Output Implementation

```scala
// Print output
stream.print()
// Save as text files
stream.saveAsTextFiles("prefix", "suffix")
// Custom output
stream.foreachRDD { rdd =>
  rdd.foreach { record =>
    // Process each record
  }
}
```

---

## Transformation Types

```mermaid
graph TB
    A[Transformations] --> B[Stateless]
    A --> C[Stateful]
    B --> D[map/filter]
    C --> E[updateStateByKey]
    style A fill:#f96
```

---

## Error Handling

```mermaid
graph LR
    A[Error] --> B[Detect]
    B --> C[Retry]
    C --> D[Recover]
    D --> E[Continue]
    C --> F[Fail]
```

---

## Error Implementation

```scala
stream.foreachRDD { rdd =>
  rdd.foreachPartition { partition =>
    try {
      // Process partition
    } catch {
      case e: Exception =>
        // Handle error
    }
  }
}
```

---

## Performance Tuning

```mermaid
graph TB
    A[Performance] --> B[Batch Size]
    A --> C[Parallelism]
    A --> D[Memory]
    B --> E[Optimization]
    C --> E
    D --> E
```

---

## Monitoring Architecture

```mermaid
graph LR
    A[Metrics] --> B[Processing Time]
    A --> C[Scheduling Delay]
    A --> D[Total Delay]
    A --> E[Input Rate]
    style A fill:#f96
```

---

## Monitoring Implementation

1. Streaming tab in UI
1. Processing time
1. Scheduling delay
1. Total delay
1. Input rate

---

## Backpressure

```mermaid
graph TB
    A[Input] --> B[Rate Control]
    B --> C[Processing]
    C --> |Feedback| B
    style B fill:#f96
```

---

## Best Practices

```mermaid
graph LR
    A[Best Practices] --> B[Batch Size]
    A --> C[Memory Tuning]
    A --> D[Error Handling]
    A --> E[Monitoring]
    style A fill:#f96
```

---

## Production Deployment

```mermaid
graph TB
    A[Deploy] --> B[Configure]
    B --> C[Monitor]
    C --> D[Optimize]
    D --> E[Scale]
    style A fill:#f96
```

---

## Use Cases

1. Log Processing
1. IoT Data Analysis
1. Social Media Analysis
1. Financial Data Processing
1. Real-time Analytics

---

## Advanced Features

```mermaid
graph TB
    A[Advanced] --> B[Custom Receivers]
    A --> C[Dynamic Scaling]
    A --> D[Custom Storage]
    B --> E[Implementation]
    C --> E
    D --> E
```
