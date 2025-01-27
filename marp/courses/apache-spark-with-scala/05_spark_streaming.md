# Spark Streaming

## Introduction to Streaming

1. Real-time processing
1. Stream sources
1. Window operations
1. State management
1. Fault tolerance

## Streaming Architecture

![0](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/0.png)

## DStream Basics

```scala
import org.apache.spark.streaming._
val conf = new SparkConf().setAppName("StreamingApp")
val ssc = new StreamingContext(conf, Seconds(1))
```

## Data Sources

1. Kafka
1. Flume
1. Kinesis
1. Socket
1. Files

## Kafka Integration

```scala
import org.apache.spark.streaming.kafka010._
val kafkaParams = Map(
  "bootstrap.servers" -> "localhost:9092",
  "key.deserializer" -> classOf[StringDeserializer],
  "value.deserializer" -> classOf[StringDeserializer],
  "group.id" -> "spark_streaming_group"
)
```

## Window Operations

![1](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/1.png)

## Stateful Operations

```scala
val words = lines.flatMap(_.split(" "))
val pairs = words.map(word => (word, 1))
val wordCounts = pairs.updateStateByKey(updateFunction)
```

## Checkpointing

```scala
ssc.checkpoint("checkpoint_directory")
def functionToCreateContext(): StreamingContext = {
  val ssc = new StreamingContext(...)
  ssc.checkpoint("checkpoint_directory")
  ssc
}
```

## Output Operations

1. print()
1. saveAsTextFiles()
1. saveAsObjectFiles()
1. foreachRDD()
1. saveAsHadoopFiles()

## Transformation Types

![2](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/2.png)

## Performance Tuning

1. Batch interval
1. Partition count
1. Memory allocation
1. Backpressure
1. Receiver rate

## Error Handling

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

## Monitoring

1. Streaming tab in UI
1. Processing time
1. Scheduling delay
1. Total delay
1. Input rate

## Best Practices

![3](../../../out/mermaid/marp/courses/apache-spark-with-scala/05_spark_streaming.md/3.png)

## Use Cases

1. Log Processing
1. IoT Data Analysis
1. Social Media Analysis
1. Financial Data Processing
1. Real-time Analytics
