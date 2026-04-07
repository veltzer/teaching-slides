# Spark Streaming

## Introduction to Streaming

1. Real-time processing
1. Stream sources
1. Window operations
1. State management
1. Fault tolerance

---

## Streaming Architecture

![streaming_architecture](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/streaming_architecture.svg)

---

## Processing Models

![processing_models](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/processing_models.svg)

---

## DStream Basics

```scala
import org.apache.spark.streaming._
val conf = new SparkConf().setAppName("StreamingApp")
val ssc = new StreamingContext(conf, Seconds(1))
```

---

## Stream Sources

![stream_sources](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/stream_sources.svg)

---

## Kafka Integration Flow

![kafka_integration_flow](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/kafka_integration_flow.svg)

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

![window_operations](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/window_operations.svg)

---

## Windowing Types

![windowing_types](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/windowing_types.svg)

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

![stateful_operations](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/stateful_operations.svg)

---

## State Implementation

```scala
val words = lines.flatMap(_.split(" "))
val pairs = words.map(word => (word, 1))
val wordCounts = pairs.updateStateByKey(updateFunction)
```

---

## Checkpointing

![checkpointing](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/checkpointing.svg)

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

![output_operations](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/output_operations.svg)

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

![transformation_types](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/transformation_types.svg)

---

## Error Handling

![error_handling](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/error_handling.svg)

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

![performance_tuning](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/performance_tuning.svg)

---

## Monitoring Architecture

![monitoring_architecture](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/monitoring_architecture.svg)

---

## Monitoring Implementation

1. Streaming tab in UI
1. Processing time
1. Scheduling delay
1. Total delay
1. Input rate

---

## Backpressure

![backpressure](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/backpressure.svg)

---

## Best Practices

![best_practices](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/best_practices.svg)

---

## Production Deployment

![production_deployment](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/production_deployment.svg)

---

## Use Cases

1. Log Processing
1. IoT Data Analysis
1. Social Media Analysis
1. Financial Data Processing
1. Real-time Analytics

---

## Advanced Features

![advanced_features](/svg/courses/big_data/apache-spark-with-scala/06_spark_streaming/advanced_features.svg)
