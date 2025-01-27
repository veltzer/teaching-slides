# Spark Streaming

## Introduction to Streaming

1. Real-time processing
1. Stream sources
1. Window operations
1. State management
1. Fault tolerance

---

## Streaming Architecture

![0](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/0.png)

---

## Processing Models

![1](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/1.png)

---

## DStream Basics

```scala
import org.apache.spark.streaming._
val conf = new SparkConf().setAppName("StreamingApp")
val ssc = new StreamingContext(conf, Seconds(1))
```

---

## Stream Sources

![2](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/2.png)

---

## Kafka Integration Flow

![3](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/3.png)

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

![4](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/4.png)

---

## Windowing Types

![5](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/5.png)

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

![6](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/6.png)

---

## State Implementation

```scala
val words = lines.flatMap(_.split(" "))
val pairs = words.map(word => (word, 1))
val wordCounts = pairs.updateStateByKey(updateFunction)
```

---

## Checkpointing

![7](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/7.png)

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

![8](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/8.png)

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

![9](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/9.png)

---

## Error Handling

![10](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/10.png)

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

![11](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/11.png)

---

## Monitoring Architecture

![12](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/12.png)

---

## Monitoring Implementation

1. Streaming tab in UI
1. Processing time
1. Scheduling delay
1. Total delay
1. Input rate

---

## Backpressure

![13](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/13.png)

---

## Best Practices

![14](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/14.png)

---

## Production Deployment

![15](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/15.png)

---

## Use Cases

1. Log Processing
1. IoT Data Analysis
1. Social Media Analysis
1. Financial Data Processing
1. Real-time Analytics

---

## Advanced Features

![16](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/16.png)
