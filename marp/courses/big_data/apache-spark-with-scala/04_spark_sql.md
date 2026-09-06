---
tags:
  - tools:spark
  - languages:scala
  - data-and-ai:big-data
  - languages:sql
level: intermediate
category: big-data
audience:
  - audiences:developers

---

# Spark SQL

---

## Introduction to Spark SQL

1. High-level API for structured data
1. DataFrame abstraction
1. SQL query support
1. Schema inference
1. Optimized execution

---

## Spark SQL Architecture

![spark_sql_architecture](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/spark_sql_architecture.svg)

---

## Data Sources

![data_sources](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/data_sources.svg)

---

## DataFrame Creation

```scala
// From RDD
case class Person(name: String, age: Int)
val people = sc.parallelize(List(
  Person("Alice", 25),
  Person("Bob", 30)
)).toDF()

// From CSV
val df = spark.read
  .option("header", "true")
  .csv("people.csv")

// From JSON
val jsonDF = spark.read.json("data.json")
```

---

## DataFrame Operations Flow

![dataframe_operations_flow](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/dataframe_operations_flow.svg)

---

## DataFrame Operations

```scala
// Select columns
df.select("name", "age")

// Filter rows
df.filter($"age" > 25)

// Group and aggregate
df.groupBy("department")
  .agg(avg("salary"), max("age"))
```

---

## Query Optimization

![query_optimization](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/query_optimization.svg)

---

## SQL Queries

```scala
// Register temp view
df.createOrReplaceTempView("people")

// Run SQL query
val results = spark.sql("""
  SELECT department,
         AVG(salary) as avg_salary
  FROM people
  GROUP BY department
  HAVING AVG(salary) > 50000
""")
```

---

## Catalyst Optimizer

![catalyst_optimizer](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/catalyst_optimizer.svg)

---

## Working with Parquet

```scala
// Write Parquet
df.write.parquet("data.parquet")

// Read Parquet
val parquetDF = spark.read.parquet("data.parquet")

// Partition by column
df.write
  .partitionBy("year", "month")
  .parquet("partitioned_data")
```

---

## Data Types

![data_types](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/data_types.svg)

---

## Schema Management

```scala
// Define schema
import org.apache.spark.sql.types._

val schema = StructType(Array(
  StructField("name", StringType, false),
  StructField("age", IntegerType, true),
  StructField("salary", DoubleType, true)
))

// Apply schema
val df = spark.read
  .schema(schema)
  .csv("data.csv")
```

---

## Hive Integration

![hive_integration](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/hive_integration.svg)

---

## Hive Operations

```scala
// Enable Hive support
val spark = SparkSession.builder()
  .enableHiveSupport()
  .getOrCreate()

// Create Hive table
spark.sql("CREATE TABLE IF NOT EXISTS users ...")

// Query Hive table
val results = spark.sql("SELECT * FROM users")
```

---

## Window Functions

![window_functions](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/window_functions.svg)

---

## Window Implementation

```scala
import org.apache.spark.sql.expressions.Window

val windowSpec = Window
  .partitionBy("department")
  .orderBy("salary")
  .rowsBetween(Window.unboundedPreceding,
               Window.currentRow)

df.withColumn("running_total",
  sum("salary").over(windowSpec))
```

---

## UDF Registration

![udf_registration](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/udf_registration.svg)

---

## User-Defined Functions

```scala
// Register UDF
spark.udf.register("myUpper",
  (input: String) => input.toUpperCase)

// Use in SQL
spark.sql("SELECT myUpper(name) FROM users")

// Use in DataFrame API
import org.apache.spark.sql.functions.udf
val upperUDF = udf((input: String) => input.toUpperCase)
df.select(upperUDF($"name"))
```

---

## Join Operations

![join_operations](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/join_operations.svg)

---

## Join Examples

```scala
// Inner join
df1.join(df2, "key")

// Left outer join
df1.join(df2, Seq("key"), "left_outer")

// Cross join
df1.crossJoin(df2)
```

---

## Performance Optimization

![performance_optimization](svg/courses/big_data/apache-spark-with-scala/04_spark_sql/performance_optimization.svg)
