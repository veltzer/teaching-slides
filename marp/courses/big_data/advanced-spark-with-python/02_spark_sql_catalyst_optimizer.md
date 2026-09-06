---
tags:
  - tools:spark
  - languages:python
  - data-and-ai:big-data
  - practices:performance
level: advanced
category: big-data
audience:
  - audiences:developers
  - audiences:data-scientists

---

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
![why_spark_sql](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/why_spark_sql.svg)

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
![catalyst_optimizer_phases](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/catalyst_optimizer_phases.svg)

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
![predicate_pushdown](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/predicate_pushdown.svg)

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
![cost_based_optimization](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/cost_based_optimization.svg)

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
![udf_best_practices](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/udf_best_practices.svg)

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
![file_format_optimization](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/file_format_optimization.svg)

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
![memory_management](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/memory_management.svg)

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
![dynamic_partition_pruning](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/dynamic_partition_pruning.svg)

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
![runtime_statistics](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/runtime_statistics.svg)

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
![data_skew_handling](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/data_skew_handling.svg)

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
![monitoring_and_debugging](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/monitoring_and_debugging.svg)

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
![optimization_checklist](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/optimization_checklist.svg)

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
```

---

## Catalyst Demo: Products, Views, and Stats

```python
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

![catalyst_optimizer_phases_explained](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/catalyst_optimizer_phases_explained.svg)

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

## Predicate Pushdown: Before vs After: Example

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

---

## Predicate Pushdown: Before vs After

![scan_customers](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/scan_customers.svg)

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
```

---

## Vectorized UDF: Benchmark and Results

```python
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

![udf_data_flow_python_vs_pandas](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/udf_data_flow_python_vs_pandas.svg)

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
```

---

## JDBC: Partitioning by Date Predicates

```python
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
```

---

## AQE: Skew Join and Dynamic Strategy

```python
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

![aqe_before_vs_after](svg/courses/big_data/advanced-spark-with-python/02_spark_sql_catalyst_optimizer/aqe_before_vs_after.svg)

---

## Full Program: Complex SQL with Window + CTE

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ComplexSQL") \
    .getOrCreate()
```

Defines the CTE with monthly revenue and ranked customers:

```sql
WITH monthly_revenue AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount) AS monthly_total,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id, DATE_TRUNC('month', order_date)
),
```

---

## Complex SQL: ranked_customers CTE

```sql
ranked_customers AS (
    SELECT
        customer_id, month, monthly_total, order_count,
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
```

---

## Complex SQL: Final SELECT

```sql
SELECT
    r.customer_id, c.name, c.region,
    r.month, r.monthly_total, r.rank,
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
```

Run via `spark.sql(query).show(20, truncate=False)`.

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

---

## Bucketing

Pre-shuffle data to skip exchange on joins and aggregations:

```python
# Create a bucketed table (Hive-compatible, Parquet-backed)
spark.sql("""
    CREATE TABLE sales_bucketed
    USING parquet
    CLUSTERED BY (customer_id) INTO 8 BUCKETS
    AS SELECT * FROM sales
""")

# Joining two tables bucketed on the same key and count avoids a shuffle:
result = spark.sql("""
    SELECT * FROM sales_bucketed s
    JOIN customers_bucketed c ON s.customer_id = c.id
""")
```

Bucket count must match on both tables for the optimizer to skip the shuffle. Bucketing requires `saveAsTable`/managed tables; it does not work for raw DataFrame writes.
