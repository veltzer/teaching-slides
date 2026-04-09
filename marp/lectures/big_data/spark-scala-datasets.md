# Spark Datasets and DataFrames in Scala
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/big_data/spark-scala-datasets/title.svg)

## Core Concepts
1. Datasets: Typed distributed collections
1. DataFrames: Untyped distributed collections
1. Type safety and runtime checks
1. Performance considerations
---
## Dataset Definition
```scala
case class Person(name: String, age: Int)
val ds: Dataset[Person] = spark.read
  .json("people.json")
  .as[Person]
```
---
## DataFrame Definition
```scala
val df: DataFrame = spark.read
  .json("people.json")
```
---
## Type Safety
![type_safety](svg/lectures/big_data/spark-scala-datasets/type_safety.svg)

---
## Basic Transformations
```scala
// Dataset
personDS.filter(_.age > 21)

// DataFrame
personDF.filter($"age" > 21)
```
---
## Schema Definition
```scala
// Dataset implicit schema from case class
case class Person(name: String, age: Int)

// DataFrame explicit schema
val schema = StructType(Array(
  StructField("name", StringType),
  StructField("age", IntegerType)
))
```
---
## Dataset Type Safety Example
```scala
case class Person(name: String, age: Int)
val ds = spark.read.json("people.json").as[Person]

// Compile error if wrong type
ds.map(p => p.age.substring(1))
```
---
## DataFrame Runtime Checks
```scala
val df = spark.read.json("people.json")

// Runtime error if wrong type
df.select($"age".cast("string").substring(1))
```
---
## Performance Characteristics
![performance_characteristics](svg/lectures/big_data/spark-scala-datasets/performance_characteristics.svg)

---
## Memory Usage
1. Datasets: Object creation overhead
1. DataFrames: Optimized internal format
1. Memory management considerations
1. Garbage collection impact
---
## Converting Between Types
```scala
// DataFrame to Dataset
case class Person(name: String, age: Int)
val ds = df.as[Person]

// Dataset to DataFrame
val df = ds.toDF()
```
---
## SQL Operations
```scala
// Register temporary view
ds.createOrReplaceTempView("people")

// SQL query
spark.sql("SELECT * FROM people WHERE age > 21")
```
---
## Catalyst Optimizer
![catalyst_optimizer](svg/lectures/big_data/spark-scala-datasets/catalyst_optimizer.svg)

---
## Encoder Operations
1. Serialization
1. Deserialization
1. Schema generation
1. Code generation
---
## Dataset Advantages
1. Type safety
1. Object-oriented interface
1. IDE support
1. Compile-time errors
---
## DataFrame Advantages
1. Better performance
1. Dynamic typing
1. SQL-like operations
1. Simpler API
---
## When to Use Datasets
1. Complex domain objects
1. Type safety requirement
1. Java/Scala codebase
1. Compile-time verification
---
## When to Use DataFrames
1. Simple operations
1. Best performance needed
1. Dynamic typing preferred
1. SQL-like operations
---
## Common Operations
```scala
// Dataset
ds.filter(_.age > 21)
  .map(_.name)
  .groupByKey(_.length)
  .count()

// DataFrame
df.filter($"age" > 21)
  .select($"name")
  .groupBy(length($"name"))
  .count()
```
---
## Aggregations
```scala
// Dataset
ds.groupByKey(_.age)
  .agg(count("*").as[Long])

// DataFrame
df.groupBy($"age")
  .agg(count("*"))
```
---
## Join Operations
```scala
case class Order(id: Int, personId: Int)
val orders: Dataset[Order] = ...

persons.joinWith(orders,
  persons("id") === orders("personId"))
```
---
## Performance Tuning
1. Caching strategies
1. Partition management
1. Memory configuration
1. Execution plans
---
## Debugging Tools
```scala
// View execution plan
ds.explain()

// View logical plan
ds.explain(true)
```
---
## Error Handling
```scala
// Dataset - compile-time error
ds.map(_.nonexistentField) // Won't compile

// DataFrame - runtime error
df.select($"nonexistentField") // Runtime error
```
---
## Schema Evolution
1. Adding columns
1. Removing columns
1. Type changes
1. Compatibility checks
---
## Data Sources
```scala
// Read parquet
val ds = spark.read.parquet("data.parquet").as[Person]

// Write parquet
ds.write.parquet("output.parquet")
```
---
## Custom Encoders
```scala
// Custom encoder for complex type
implicit val encoder = Encoders.kryo[CustomType]
val ds: Dataset[CustomType] = ...
```
---
## Serialization
![serialization](svg/lectures/big_data/spark-scala-datasets/serialization.svg)

---
## Best Practices
1. Use appropriate types
1. Consider performance impact
1. Handle schema evolution
1. Implement proper error handling
---
## Dataset APIs
1. Transformation operations
1. Action operations
1. Aggregation functions
1. Window functions
---
## DataFrame APIs
1. Column operations
1. SQL functions
1. Window expressions
1. UDFs
---
## Real-world Usage
```scala
case class SalesRecord(
  id: Long,
  date: java.sql.Date,
  amount: Double
)

val sales: Dataset[SalesRecord] = ...
sales.groupByKey(_.date)
  .agg(sum($"amount").as[Double])
```
---
## Performance Monitoring
1. Spark UI metrics
1. Memory usage
1. Execution time
1. Resource utilization
---
## Common Pitfalls
1. Excessive object creation
1. Inefficient serialization
1. Memory leaks
1. Poor partitioning
---
## Future Considerations
1. Scala 3 support
1. Performance improvements
1. API enhancements
1. Integration features
