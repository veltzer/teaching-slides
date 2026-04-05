# Spark SQL and Catalyst Optimizer
---
## Chapter Overview
* Query optimization techniques
* Catalyst optimizer internals
* User-Defined Functions (UDFs)
* Data source integration
* Performance tuning
---
## Why Spark SQL?
<svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="505" y1="150.0" x2="595" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="775" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="820" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">SQL</text></svg>

---
## Spark SQL Architecture
1. SQL Parser
1. Analyzer
1. Optimizer
1. Physical planning
---
## DataFrame vs SQL

```python
# DataFrame API
df.select("name").filter("age > 25")

# SQL
spark.sql("SELECT name FROM table WHERE age > 25")
```

---
## Catalyst Optimizer Phases
<svg viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="180" x2="295.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="300" x2="295.0" y2="420" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="520" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="545" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Unresolved Plan</text></svg>

---
## Logical Plan Analysis
```python
df.explain(mode="extended")
# Shows unresolved and resolved logical plans
```
---
## Query Planning
1. Parse SQL/DataFrame
1. Resolve references
1. Apply optimizations
1. Generate physical plan
---
## Understanding Query Plans
```python
# View the execution plan
df.select("name", "age").groupBy("age").count().explain(True)
```
---
## Plan Optimization Rules
1. Constant folding
1. Predicate pushdown
1. Column pruning
1. Join reordering
---
## Predicate Pushdown
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="220.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="280.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="280" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="305" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Filter</text></svg>

---
## Join Optimization
```python
# Join with broadcast hint
from pyspark.sql.functions import broadcast
df1.join(broadcast(df2), "key")
```
---
## Column Pruning Example
```python
# Before: SELECT * FROM table
# After: SELECT id, name FROM table WHERE age > 25
df.select("id", "name").filter("age > 25")
```
---
## Cost-Based Optimization
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="595" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="640" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Plans</text></svg>

---
## Statistics Collection
```python
# Analyze table to collect statistics
spark.sql("ANALYZE TABLE my_table COMPUTE STATISTICS")
```
---
## Column Statistics
```python
# Collect column-level statistics
spark.sql("ANALYZE TABLE my_table COMPUTE STATISTICS FOR COLUMNS id, name")
```
---
## User-Defined Functions
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def upper_custom(s):
    return s.upper() if s else None
```
---
## UDF Performance
1. Serialization overhead
1. Type conversion costs
1. Limited optimization
1. JVM boundary crossing
---
## Vectorized UDFs
```python
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import StringType

@pandas_udf(StringType())
def upper_vectorized(s):
    return s.str.upper()
```
---
## UDF Best Practices
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="130.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="220.0" y1="60" x2="205.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="370.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145.0" y1="180" x2="130.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="180" x2="280.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="130.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="175.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">UDF Choice</text></svg>

---
## Data Sources API
```python
# Read from external source
df = spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://...")
    .option("table", "users")
    .load()
```
---
## Custom Data Sources
1. Implement BaseRelation
1. Define schema
1. Implement scanning
1. Handle pushdown
---
## Data Source Options
```python
# Parquet with specific options
df.write.format("parquet")
    .option("compression", "snappy")
    .mode("overwrite")
    .save("path")
```
---
## File Format Optimization
<svg viewBox="0 0 540 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="110.0" x2="235" y2="70.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="110.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="190.0" x2="235" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="235" y1="70.0" x2="325" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="90.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="115.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Data Format</text></svg>

---
## Parquet Optimization
1. Predicate pushdown
1. Column pruning
1. Dictionary encoding
1. Run-length encoding
---
## Query Performance
```python
# Cache frequently accessed data
df.cache()
# Set proper partition number
spark.sql.shuffle.partitions=200
```
---
## Memory Management
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="280.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="370.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="130.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="130.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="175.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Memory</text></svg>

---
## External Data Sources
1. JDBC connections
1. Cloud storage
1. NoSQL databases
1. Streaming sources
---
## JDBC Optimization
```python
# Parallel read configuration
properties = {
    "partitionColumn": "id",
    "lowerBound": "1",
    "upperBound": "1000000",
    "numPartitions": "10"
}
```
---
## Schema Handling
```python
# Define explicit schema
from pyspark.sql.types import *
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
```
---
## Schema Evolution
1. Add columns
1. Remove columns
1. Change data types
1. Handle nullability
---
## Query Plan Caching
```python
# Enable query plan caching
spark.catalog.cacheTable("frequently_used")
```
---
## Dynamic Partition Pruning
<svg viewBox="0 0 500 480" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="180" x2="295.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="400" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="425" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Query</text></svg>

---
## Cost Model Tuning
```python
spark.conf.set("spark.sql.cbo.enabled", "true")
spark.conf.set("spark.sql.cbo.joinReorder.enabled", "true")
```
---
## Query Plan Analysis
1. Logical plan inspection
1. Physical plan review
1. Execution statistics
1. Bottleneck identification
---
## Adaptive Query Execution
```python
# Enable adaptive query execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
```
---
## Runtime Statistics
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="325" y1="150.0" x2="415" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="595" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="640" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Execution</text></svg>

---
## Join Strategies
1. Broadcast hash join
1. Sort merge join
1. Shuffle hash join
1. Cartesian join
---
## Window Function Optimization
```python
# Efficient window function
windowSpec = Window.partitionBy("department").orderBy("salary")
df.withColumn("rank", rank().over(windowSpec))
```
---
## Subquery Handling
```python
# Correlated subquery optimization
df1.join(df2, df1.id == df2.id).where(df2.value > df1.value)
```
---
## Data Skew Handling
<svg viewBox="0 0 500 480" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="180" x2="295.0" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="400" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="425" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Skewed Data</text></svg>

---
## Configuration Tuning
1. Memory settings
1. Shuffle parameters
1. Compression options
1. Executor settings
---
## Error Handling
```python
# Handle corrupt records
df = spark.read.option("mode", "PERMISSIVE")
    .option("columnNameOfCorruptRecord", "_corrupt_record")
    .json("path")
```
---
## Monitoring and Debugging
<svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="145" y1="150.0" x2="235" y2="70.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="150.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="145" y1="150.0" x2="235" y2="230.0" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="55" y="130.0" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="100" y="155.0" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Monitoring</text></svg>

---
## Performance Metrics
1. Query execution time
1. Memory usage
1. Shuffle data size
1. Task duration
---
## Best Practices Summary
1. Use appropriate data formats
1. Optimize join operations
1. Leverage statistics
1. Monitor performance
---
## Common Pitfalls
1. Inefficient joins
1. Poor partitioning
1. Memory issues
1. Suboptimal UDFs
---
## Advanced Topics
1. Custom optimizers
1. Extension points
1. Query rewrite rules
1. Cost model tuning
---
## Optimization Checklist
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333" /></marker></defs><line x1="205.0" y1="60" x2="145.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="205.0" y1="60" x2="295.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><line x1="295.0" y1="60" x2="355.0" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/><rect x="205.0" y="40" width="90" height="40" fill="#e8f4f8" stroke="#333" stroke-width="2" rx="5"/><text x="250.0" y="65" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Optimization</text></svg>

---
## Production Deployment
1. Resource allocation
1. Monitoring setup
1. Error handling
1. Performance tuning
---
## Future Directions
1. Enhanced optimization
1. Better statistics
1. Improved adaptivity
1. New features
---
## Additional Resources
* Official documentation
* Research papers
* Community guides
* Performance tuning tips

---

## Full Program: Catalyst Optimizer in Action

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("CatalystOptimizerDemo") \
    .config("spark.sql.cbo.enabled", "true") \
    .config("spark.sql.cbo.joinReorder.enabled", "true") \
    .getOrCreate()

# Create sample tables
orders = spark.range(0, 1_000_000).toDF("order_id") \
    .withColumn("customer_id", (F.col("order_id") % 10000).cast("int")) \
    .withColumn("product_id", (F.col("order_id") % 500).cast("int")) \
    .withColumn("amount", (F.rand() * 1000).cast("decimal(10,2)")) \
    .withColumn("order_date", F.date_add(F.lit("2024-01-01"),
        (F.rand() * 365).cast("int")))

customers = spark.range(0, 10000).toDF("customer_id") \
    .withColumn("name", F.concat(F.lit("Customer_"), F.col("customer_id"))) \
    .withColumn("region", F.when(F.col("customer_id") % 4 == 0, "North")
        .when(F.col("customer_id") % 4 == 1, "South")
        .when(F.col("customer_id") % 4 == 2, "East")
        .otherwise("West"))

products = spark.range(0, 500).toDF("product_id") \
    .withColumn("product_name",
        F.concat(F.lit("Product_"), F.col("product_id"))) \
    .withColumn("category",
        F.when(F.col("product_id") % 5 == 0, "Electronics")
        .when(F.col("product_id") % 5 == 1, "Clothing")
        .when(F.col("product_id") % 5 == 2, "Food")
        .when(F.col("product_id") % 5 == 3, "Books")
        .otherwise("Other"))

# Register as temp views
orders.createOrReplaceTempView("orders")
customers.createOrReplaceTempView("customers")
products.createOrReplaceTempView("products")

# Compute statistics for CBO
spark.sql("ANALYZE TABLE orders COMPUTE STATISTICS")
spark.sql("ANALYZE TABLE customers COMPUTE STATISTICS")
spark.sql("ANALYZE TABLE products COMPUTE STATISTICS")
spark.sql("ANALYZE TABLE orders COMPUTE STATISTICS FOR COLUMNS "
          "customer_id, product_id, amount")
```

---

## Catalyst Optimizer Phases Explained

<svg viewBox="0 0 620 580" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-cat" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <!-- SQL Query -->
  <rect x="110" y="5" width="400" height="40" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="310" y="30" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">SQL Query / DataFrame API</text>
  <line x1="310" y1="45" x2="310" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrow-cat)"/>
  <!-- Phase 1 -->
  <rect x="60" y="65" width="500" height="55" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="310" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">Phase 1: PARSING</text>
  <text x="310" y="105" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">SQL string --> Unresolved Logical Plan (names as strings, no types)</text>
  <line x1="310" y1="120" x2="310" y2="135" stroke="#333" stroke-width="2" marker-end="url(#arrow-cat)"/>
  <!-- Phase 2 -->
  <rect x="60" y="140" width="500" height="55" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="310" y="160" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">Phase 2: ANALYSIS</text>
  <text x="310" y="180" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Resolve columns, tables, functions using Catalog</text>
  <line x1="310" y1="195" x2="310" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow-cat)"/>
  <!-- Phase 3 -->
  <rect x="60" y="215" width="500" height="75" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="310" y="235" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">Phase 3: LOGICAL OPTIMIZATION</text>
  <text x="310" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Predicate pushdown, Column pruning,</text>
  <text x="310" y="272" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Constant folding, Boolean simplification</text>
  <line x1="310" y1="290" x2="310" y2="305" stroke="#333" stroke-width="2" marker-end="url(#arrow-cat)"/>
  <!-- Phase 4 -->
  <rect x="60" y="310" width="500" height="55" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="310" y="330" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">Phase 4: PHYSICAL PLANNING</text>
  <text x="310" y="350" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Generate physical plans; CBO selects cheapest</text>
  <line x1="310" y1="365" x2="310" y2="380" stroke="#333" stroke-width="2" marker-end="url(#arrow-cat)"/>
  <!-- Phase 5 -->
  <rect x="60" y="385" width="500" height="55" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="310" y="405" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">Phase 5: CODE GENERATION (Tungsten)</text>
  <text x="310" y="425" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#555">Whole-stage codegen: Java bytecode for CPU-efficient execution</text>
</svg>

---

## Viewing All Plan Levels

```python
# Complex query to analyze
query = (
    orders
    .join(customers, "customer_id")
    .join(products, "product_id")
    .filter(F.col("region") == "North")
    .filter(F.col("category") == "Electronics")
    .filter(F.col("amount") > 100)
    .groupBy("region", "category")
    .agg(
        F.sum("amount").alias("total_revenue"),
        F.count("*").alias("order_count"),
    )
)

# View all plan levels
query.explain(mode="extended")
# Output shows:
#   == Parsed Logical Plan ==
#   == Analyzed Logical Plan ==
#   == Optimized Logical Plan ==
#   == Physical Plan ==

# View formatted plan (Spark 3.0+)
query.explain(mode="formatted")

# View cost-based plan
query.explain(mode="cost")
```

---

## Predicate Pushdown: Before vs After

```python
# Query: filter after join (what you write)
result = (
    orders.join(customers, "customer_id")
    .filter(F.col("region") == "North")
    .filter(F.col("amount") > 500)
)

# Catalyst optimizes this to push filters before join:
# == Optimized Logical Plan ==
# Aggregate
#   Join (customer_id)
#     Filter (amount > 500)    <-- pushed to orders scan
#       Scan orders
#     Filter (region = North)  <-- pushed to customers scan
#       Scan customers
```

<svg viewBox="0 0 620 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-pp" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <!-- Before Optimization title -->
  <text x="130" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">Before Optimization</text>
  <!-- Filter region=N -->
  <rect x="60" y="30" width="140" height="35" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="130" y="52" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Filter region=N</text>
  <line x1="130" y1="65" x2="130" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <!-- Filter amount>500 -->
  <rect x="60" y="90" width="140" height="35" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="130" y="112" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Filter amount>500</text>
  <line x1="130" y1="125" x2="130" y2="145" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <!-- Join -->
  <rect x="60" y="150" width="140" height="35" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="130" y="172" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Join</text>
  <line x1="95" y1="185" x2="75" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <line x1="165" y1="185" x2="185" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <!-- Scans -->
  <rect x="30" y="215" width="90" height="35" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="75" y="237" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Orders Scan</text>
  <rect x="140" y="215" width="90" height="35" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="185" y="237" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Cust. Scan</text>
  <!-- Arrow between -->
  <text x="310" y="150" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#333">--></text>
  <!-- After Optimization title -->
  <text x="490" y="18" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#333">After Optimization</text>
  <!-- Join (top) -->
  <rect x="420" y="30" width="140" height="35" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="490" y="52" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Join</text>
  <line x1="455" y1="65" x2="420" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <line x1="525" y1="65" x2="560" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <!-- Filter amt>500 -->
  <rect x="350" y="100" width="140" height="35" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="420" y="122" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Filter amt>500</text>
  <line x1="420" y1="135" x2="420" y2="155" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <!-- Filter rgn=North -->
  <rect x="490" y="100" width="140" height="35" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="560" y="122" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Filter rgn=North</text>
  <line x1="560" y1="135" x2="560" y2="155" stroke="#333" stroke-width="2" marker-end="url(#arrow-pp)"/>
  <!-- Scans -->
  <rect x="370" y="160" width="100" height="35" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="420" y="182" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Orders Scan</text>
  <rect x="510" y="160" width="100" height="35" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="560" y="182" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Cust. Scan</text>
</svg>

---

## Full Program: Vectorized UDF Performance

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, pandas_udf, col
from pyspark.sql.types import DoubleType
import time

spark = SparkSession.builder \
    .appName("UDFPerformance") \
    .getOrCreate()

# Create test dataset: 5M rows
df = spark.range(0, 5_000_000).toDF("id") \
    .withColumn("value", (col("id") * 0.001).cast("double"))

# Method 1: Regular Python UDF (slowest)
@udf(returnType=DoubleType())
def python_udf(x):
    import math
    return math.sin(x) * math.cos(x) + math.sqrt(abs(x))

# Method 2: Pandas/Vectorized UDF (faster)
@pandas_udf(DoubleType())
def pandas_udf_func(s):
    import numpy as np
    return np.sin(s) * np.cos(s) + np.sqrt(np.abs(s))

# Method 3: Built-in functions (fastest)
from pyspark.sql import functions as F

# Benchmark all three approaches
start = time.time()
df.withColumn("result", python_udf("value")).count()
python_time = time.time() - start

start = time.time()
df.withColumn("result", pandas_udf_func("value")).count()
pandas_time = time.time() - start

start = time.time()
df.withColumn("result",
    F.sin("value") * F.cos("value") + F.sqrt(F.abs("value"))
).count()
builtin_time = time.time() - start

print(f"Python UDF:    {python_time:.2f}s")
print(f"Pandas UDF:    {pandas_time:.2f}s")
print(f"Built-in:      {builtin_time:.2f}s")
print(f"Speedup (pandas vs python): {python_time/pandas_time:.1f}x")
print(f"Speedup (builtin vs python): {python_time/builtin_time:.1f}x")
```

---

## UDF Performance Comparison

| UDF Type | Serialization | Vectorized | Optimizer | Relative Speed |
|---|---|---|---|---|
| Python UDF | Row-by-row Python<->JVM | No | Opaque | 1x (baseline) |
| Pandas UDF | Arrow batches | Yes | Opaque | 3-100x |
| Built-in Functions | None (JVM native) | Yes | Full optimization | 10-1000x |

---

## UDF Data Flow: Python vs Pandas

<svg viewBox="0 0 620 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-udf" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <!-- Python UDF title -->
  <text x="310" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#c62828">Python UDF (row-by-row)</text>
  <!-- JVM Row -->
  <rect x="30" y="35" width="110" height="40" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="85" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">JVM</text>
  <text x="85" y="68" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">Row 1</text>
  <line x1="140" y1="55" x2="190" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <!-- Serialize -->
  <rect x="195" y="35" width="110" height="40" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="250" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Serialize</text>
  <text x="250" y="68" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">(pickle)</text>
  <line x1="305" y1="55" x2="355" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <!-- Python func -->
  <rect x="360" y="35" width="110" height="40" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="415" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Python func()</text>
  <!-- Return arrow -->
  <line x1="415" y1="75" x2="415" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <rect x="360" y="100" width="110" height="30" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="415" y="120" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Result</text>
  <line x1="360" y1="115" x2="305" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <rect x="195" y="100" width="110" height="30" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="250" y="120" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Deserialize</text>
  <line x1="195" y1="115" x2="140" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <rect x="30" y="100" width="110" height="30" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="85" y="120" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">JVM Result</text>
  <text x="520" y="80" font-family="Arial, sans-serif" font-size="11" fill="#c62828" font-weight="bold">x N rows</text>
  <text x="520" y="95" font-family="Arial, sans-serif" font-size="11" fill="#c62828">(very slow!)</text>
  <!-- Pandas UDF title -->
  <text x="310" y="170" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#2e7d32">Pandas UDF (batch)</text>
  <!-- JVM Batch -->
  <rect x="30" y="185" width="110" height="50" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="85" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">JVM Batch</text>
  <text x="85" y="222" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">(10K rows)</text>
  <line x1="140" y1="210" x2="190" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <!-- Arrow (zero-copy) -->
  <rect x="195" y="185" width="110" height="50" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="250" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Arrow</text>
  <text x="250" y="222" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">(zero-copy)</text>
  <line x1="305" y1="210" x2="355" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <!-- Python pandas -->
  <rect x="360" y="185" width="110" height="50" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="415" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#333">Python pandas</text>
  <text x="415" y="222" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#555">vectorized</text>
  <!-- Return -->
  <line x1="415" y1="235" x2="415" y2="255" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <rect x="360" y="260" width="110" height="30" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="415" y="280" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Result Series</text>
  <line x1="360" y1="275" x2="305" y2="275" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <rect x="195" y="260" width="110" height="30" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="250" y="280" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">Arrow</text>
  <line x1="195" y1="275" x2="140" y2="275" stroke="#333" stroke-width="2" marker-end="url(#arrow-udf)"/>
  <rect x="30" y="260" width="110" height="30" rx="8" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="85" y="280" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#333">JVM Result</text>
  <text x="520" y="240" font-family="Arial, sans-serif" font-size="11" fill="#2e7d32" font-weight="bold">x N/10K batches</text>
  <text x="520" y="255" font-family="Arial, sans-serif" font-size="11" fill="#2e7d32">(much faster!)</text>
</svg>

---

## Full Program: JDBC Parallel Read

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("JDBCParallelRead") \
    .config("spark.jars", "/path/to/postgresql-42.6.0.jar") \
    .getOrCreate()

jdbc_url = "jdbc:postgresql://db-host:5432/mydb"
connection_props = {
    "user": "reader",
    "password": "secret",
    "driver": "org.postgresql.Driver",
}

# ANTI-PATTERN: Single-threaded read
# slow_df = spark.read.jdbc(jdbc_url, "large_table", properties=connection_props)

# BEST PRACTICE: Parallel read with partitioning
# First, get the range for partitioning
bounds = spark.read.jdbc(
    jdbc_url, "(SELECT MIN(id) as min_id, MAX(id) as max_id FROM large_table) t",
    properties=connection_props
).collect()[0]

# Parallel read: 10 concurrent connections
df = spark.read.jdbc(
    url=jdbc_url,
    table="large_table",
    column="id",
    lowerBound=bounds["min_id"],
    upperBound=bounds["max_id"],
    numPartitions=10,
    properties=connection_props,
)

print(f"Partitions: {df.rdd.getNumPartitions()}")
print(f"Row count:  {df.count()}")

# For non-numeric partition columns, use predicates
date_predicates = [
    "order_date >= '2024-01-01' AND order_date < '2024-04-01'",
    "order_date >= '2024-04-01' AND order_date < '2024-07-01'",
    "order_date >= '2024-07-01' AND order_date < '2024-10-01'",
    "order_date >= '2024-10-01' AND order_date < '2025-01-01'",
]

df_by_quarter = spark.read.jdbc(
    url=jdbc_url,
    table="orders",
    predicates=date_predicates,
    properties=connection_props,
)
```

---

## Join Strategy Comparison

| Join Strategy | When Used | Shuffle? | Sort? | Best For |
|---|---|---|---|---|
| Broadcast Hash | One side < 10MB | No | No | Small dim + large fact |
| Sort Merge | Both sides large | Yes | Yes | Large table joins |
| Shuffle Hash | Medium tables | Yes | No | Equi-joins, no sort needed |
| Broadcast Nested Loop | Non-equi join, small table | No | No | Range/theta joins |
| Cartesian | No join condition | Yes | No | Avoid! |

---

## Forcing Join Strategies with Hints

```python
from pyspark.sql import functions as F

# Force broadcast join
result = large_df.join(
    small_df.hint("broadcast"), "key"
)

# Force sort-merge join
result = df1.join(
    df2.hint("merge"), "key"
)

# Force shuffle hash join
result = df1.join(
    df2.hint("shuffle_hash"), "key"
)

# Force shuffle-replicate nested loop join
result = df1.join(
    df2.hint("shuffle_replicate_nl"), df1.x < df2.y
)

# SQL hint syntax
spark.sql("""
    SELECT /*+ BROADCAST(small_table) */
        o.*, c.name
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
""")

# Verify which strategy was chosen
result.explain()
```

---

## AQE (Adaptive Query Execution) Deep Dive

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")

# 1. Coalesce Shuffle Partitions
# Merges small partitions after shuffle
spark.conf.set(
    "spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set(
    "spark.sql.adaptive.coalescePartitions.minPartitionSize", "64MB")
spark.conf.set(
    "spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")

# 2. Skew Join Optimization
# Splits skewed partitions automatically
spark.conf.set(
    "spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set(
    "spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set(
    "spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# 3. Dynamic Join Strategy
# Switches to broadcast join at runtime if data is small enough
spark.conf.set(
    "spark.sql.adaptive.autoBroadcastJoinThreshold", "10MB")
```

---

## AQE: Before vs After

<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-aqe2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker>
  </defs>
  <!-- Without AQE -->
  <text x="310" y="20" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#c62828">Without AQE (200 shuffle partitions)</text>
  <rect x="30" y="30" width="70" height="50" rx="4" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="65" y="52" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">1M</text>
  <text x="65" y="70" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#c62828">skew!</text>
  <rect x="105" y="30" width="70" height="50" rx="4" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="140" y="52" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">1M</text>
  <text x="140" y="70" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#c62828">skew!</text>
  <rect x="180" y="30" width="35" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1"/>
  <text x="198" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#333">5K</text>
  <rect x="220" y="30" width="35" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1"/>
  <text x="238" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#333">5K</text>
  <rect x="260" y="30" width="35" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1"/>
  <text x="278" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#333">5K</text>
  <rect x="300" y="30" width="35" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1"/>
  <text x="318" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#333">5K</text>
  <rect x="340" y="30" width="35" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1"/>
  <text x="358" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#333">5K</text>
  <rect x="380" y="30" width="35" height="50" rx="4" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <text x="398" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" fill="#999">empty</text>
  <rect x="420" y="30" width="35" height="50" rx="4" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
  <text x="438" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" fill="#999">empty</text>
  <text x="480" y="58" font-family="Arial, sans-serif" font-size="14" fill="#999">...</text>
  <text x="310" y="105" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#888">many empty/tiny partitions + skewed partitions</text>
  <!-- Arrow -->
  <line x1="310" y1="115" x2="310" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrow-aqe2)"/>
  <text x="340" y="133" font-family="Arial, sans-serif" font-size="11" fill="#333" font-weight="bold">AQE</text>
  <!-- With AQE -->
  <text x="310" y="160" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#2e7d32">With AQE (optimized partitions)</text>
  <rect x="50" y="170" width="120" height="50" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="110" y="192" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">500K (1_a)</text>
  <text x="110" y="208" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#2e7d32">split skew</text>
  <rect x="180" y="170" width="120" height="50" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="240" y="192" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">500K (1_b)</text>
  <text x="240" y="208" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#2e7d32">split skew</text>
  <rect x="310" y="170" width="130" height="50" rx="4" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="375" y="192" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">50K (merged 2-10)</text>
  <text x="375" y="208" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#0277bd">coalesced</text>
  <rect x="450" y="170" width="130" height="50" rx="4" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="515" y="192" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#333">50K (merged 11-20)</text>
  <text x="515" y="208" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#0277bd">coalesced</text>
</svg>

---

## Full Program: Complex SQL with Window + CTE

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ComplexSQL") \
    .getOrCreate()

# Register tables (assuming data is loaded)
spark.sql("""
    WITH monthly_revenue AS (
        SELECT
            customer_id,
            DATE_TRUNC('month', order_date) AS month,
            SUM(amount) AS monthly_total,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY customer_id, DATE_TRUNC('month', order_date)
    ),
    ranked_customers AS (
        SELECT
            customer_id,
            month,
            monthly_total,
            order_count,
            ROW_NUMBER() OVER (
                PARTITION BY month
                ORDER BY monthly_total DESC
            ) AS rank,
            LAG(monthly_total) OVER (
                PARTITION BY customer_id
                ORDER BY month
            ) AS prev_month_total,
            AVG(monthly_total) OVER (
                PARTITION BY customer_id
                ORDER BY month
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) AS rolling_3m_avg
        FROM monthly_revenue
    )
    SELECT
        r.customer_id,
        c.name,
        c.region,
        r.month,
        r.monthly_total,
        r.rank,
        r.prev_month_total,
        ROUND(
            (r.monthly_total - r.prev_month_total)
            / r.prev_month_total * 100, 2
        ) AS growth_pct,
        ROUND(r.rolling_3m_avg, 2) AS rolling_avg
    FROM ranked_customers r
    JOIN customers c ON r.customer_id = c.customer_id
    WHERE r.rank <= 10
    ORDER BY r.month, r.rank
""").show(20, truncate=False)
```

---

## Common SQL Performance Pitfalls

```python
# PITFALL 1: SELECT * (no column pruning)
# Bad:
spark.sql("SELECT * FROM orders WHERE amount > 100")
# Good:
spark.sql("SELECT order_id, amount FROM orders WHERE amount > 100")

# PITFALL 2: Functions on partition columns prevent pruning
# Bad (scans all partitions):
spark.sql("SELECT * FROM orders WHERE YEAR(order_date) = 2024")
# Good (partition pruning works):
spark.sql("SELECT * FROM orders WHERE order_date >= '2024-01-01' "
          "AND order_date < '2025-01-01'")

# PITFALL 3: Implicit type conversion
# Bad (string comparison, no pushdown):
spark.sql("SELECT * FROM orders WHERE customer_id = '123'")
# Good (matching types):
spark.sql("SELECT * FROM orders WHERE customer_id = 123")

# PITFALL 4: Non-deterministic functions block optimization
# Bad (rand() prevents caching/reuse):
spark.sql("SELECT *, rand() as r FROM orders ORDER BY r LIMIT 100")
# Good:
spark.sql("SELECT * FROM orders TABLESAMPLE (100 ROWS)")
```
