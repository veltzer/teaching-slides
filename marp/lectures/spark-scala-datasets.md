# Spark Datasets and DataFrames in Scala
---
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
    </marker>
  </defs>
  <rect x="50" y="30" width="100" height="40" rx="5" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Dataset</text>

  <rect x="200" y="30" width="150" height="40" rx="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="275" y="55" text-anchor="middle" fill="#333" font-family="Arial" font-size="12">Compile-time Type Safety</text>

  <line x1="150" y1="50" x2="200" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <rect x="50" y="130" width="100" height="40" rx="5" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">DataFrame</text>

  <rect x="200" y="130" width="150" height="40" rx="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="275" y="155" text-anchor="middle" fill="#333" font-family="Arial" font-size="12">Runtime Type Safety</text>

  <line x1="150" y1="150" x2="200" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 150">
  <defs>
    <marker id="arrowhead2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
    </marker>
  </defs>
  <rect x="30" y="55" width="80" height="40" rx="5" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="70" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Input</text>

  <rect x="160" y="55" width="80" height="40" rx="5" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="200" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Encoder</text>

  <rect x="290" y="55" width="80" height="40" rx="5" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="330" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Processing</text>

  <rect x="420" y="55" width="80" height="40" rx="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="460" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Results</text>

  <line x1="110" y1="75" x2="160" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowhead2)"/>
  <line x1="240" y1="75" x2="290" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowhead2)"/>
  <line x1="370" y1="75" x2="420" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowhead2)"/>
</svg>

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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 150">
  <defs>
    <marker id="arrowhead3" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
    </marker>
  </defs>
  <rect x="30" y="55" width="80" height="40" rx="5" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="70" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Query</text>

  <rect x="160" y="55" width="80" height="40" rx="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="200" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Analysis</text>

  <rect x="290" y="55" width="100" height="40" rx="5" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <text x="340" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Logical Plan</text>

  <rect x="440" y="55" width="100" height="40" rx="5" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="490" y="80" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Physical Plan</text>

  <line x1="110" y1="75" x2="160" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowhead3)"/>
  <line x1="240" y1="75" x2="290" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowhead3)"/>
  <line x1="390" y1="75" x2="440" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowhead3)"/>
</svg>

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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 250">
  <defs>
    <marker id="arrowhead4" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
    </marker>
  </defs>
  <rect x="125" y="20" width="150" height="40" rx="5" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="200" y="45" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">JVM Object</text>

  <rect x="125" y="90" width="150" height="40" rx="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="200" y="115" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Internal Format</text>

  <rect x="125" y="160" width="150" height="40" rx="5" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="200" y="185" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Network Transfer</text>

  <rect x="125" y="230" width="150" height="40" rx="5" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="200" y="255" text-anchor="middle" fill="#333" font-family="Arial" font-size="14">Storage</text>

  <line x1="200" y1="60" x2="200" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowhead4)"/>
  <line x1="200" y1="130" x2="200" y2="160" stroke="#333" stroke-width="2" marker-end="url(#arrowhead4)"/>
  <line x1="200" y1="200" x2="200" y2="230" stroke="#333" stroke-width="2" marker-end="url(#arrowhead4)"/>
</svg>

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
