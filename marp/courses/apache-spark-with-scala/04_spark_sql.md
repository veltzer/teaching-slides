# Spark SQL

## Introduction to Spark SQL

1. High-level API for structured data
1. DataFrame abstraction
1. SQL query support
1. Schema inference
1. Optimized execution

---

## Spark SQL Architecture

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Spark SQL</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Data Sources

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Spark SQL</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Source</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">SQL Query</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Query</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Data Types</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Spark SQL</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Window Spec</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">UDF</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Join Types</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

[Continue with remaining content, adding diagrams for:]

## Performance Optimization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Optimization</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

[Continue until approximately 40 slides...]
