# Spark SQL & DataFrames

---
## Introduction to Spark SQL

### Overview
- High-level API for structured data processing
- Seamless integration with SQL and DataFrame operations
- Optimized execution through Catalyst optimizer
- Schema inference and type safety

---
## Architecture
![0](../../../out/mermaid/marp/courses/apache-spark-with-python/03_sql.md/0.png)

---
## Key Components
1. DataFrame API
1. Dataset API
1. Catalyst Optimizer
1. Tungsten Execution Engine

---
## Working with DataFrames

### Creating DataFrames

```python
# From RDD
rdd = sc.parallelize([
    (1, "John", 25),
    (2, "Alice", 30),
    (3, "Bob", 35)
])
df = spark.createDataFrame(rdd, ["id", "name", "age"])

# From CSV
df = spark.read.csv("people.csv", header=True, inferSchema=True)

# From JSON
df = spark.read.json("people.json")

# From Parquet
df = spark.read.parquet("people.parquet")
```

---
### Basic Operations

```python
# Select columns
df.select("name", "age")
df.select(df.name, df.age + 1)

# Filter rows
df.filter(df.age > 30)
df.where(df.age > 30)

# Add columns
df.withColumn("age_doubled", df.age * 2)

# Rename columns
df.withColumnRenamed("name", "full_name")

# Drop columns
df.drop("age")
```

---
### Aggregations and Grouping

```python
from pyspark.sql.functions import avg, count, sum

# Basic aggregations
df.groupBy("department").agg(
    avg("salary").alias("avg_salary"),
    count("*").alias("employee_count"),
    sum("salary").alias("total_salary")
)

# Window functions
from pyspark.sql.window import Window
window_spec = Window.partitionBy("department").orderBy("salary")
df.withColumn("rank", rank().over(window_spec))
```

---
## SQL Queries

### Running SQL

```python
# Register temporary view
df.createOrReplaceTempView("employees")

# Run SQL query
result = spark.sql("""
    SELECT department,
           AVG(salary) as avg_salary,
           COUNT(*) as employee_count
    FROM employees
    GROUP BY department
    HAVING AVG(salary) > 50000
""")
```

---
### Complex SQL Operations

```python
# Joins
result = spark.sql("""
    SELECT e.name, d.department_name, e.salary
    FROM employees e
    JOIN departments d ON e.dept_id = d.id
    WHERE e.salary > (
        SELECT AVG(salary)
        FROM employees
        WHERE dept_id = e.dept_id
    )
""")
```

---
### Complex SQL Operations

```python
# Window Functions
result = spark.sql("""
    SELECT name,
           salary,
           department,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
    FROM employees
""")
```

---
## Integration with Different Data Sources

### Supported Formats

```python
# Reading different formats
json_df = spark.read.json("data.json")
csv_df = spark.read.csv("data.csv")
parquet_df = spark.read.parquet("data.parquet")
orc_df = spark.read.orc("data.orc")
avro_df = spark.read.format("avro").load("data.avro")

# Writing to different formats
df.write.json("output.json")
df.write.parquet("output.parquet")
df.write.csv("output.csv")
```

---
### JDBC Connections

```python
# Reading from database
jdbc_df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "schema.tablename") \
    .option("user", "username") \
    .option("password", "password") \
    .load()

# Writing to database
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "schema.tablename") \
    .mode("append") \
    .save()
```

---
## Integration with Hive

### Hive Configuration

```python
# Create HiveContext
from pyspark.sql import HiveContext
hive_context = HiveContext(sc)

# Configure Hive warehouse
spark.sql("SET hive.metastore.warehouse.dir=/path/to/warehouse")
```

---
### Hive Operations

```python
# Create Hive table
spark.sql("""
    CREATE TABLE hive_table (
        id INT,
        name STRING,
        age INT
    )
    STORED AS PARQUET
""")

# Load data into Hive
df.write.saveAsTable("hive_table")

# Query Hive table
result = spark.sql("SELECT * FROM hive_table")
```

---
## Performance Optimization

### Catalyst Optimizer
![1](../../../out/mermaid/marp/courses/apache-spark-with-python/03_sql.md/1.png)

---
### Caching Strategies

```python
# Cache DataFrame
df.cache()

# Cache with specific storage level
from pyspark.storagelevel import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)

# Uncache
df.unpersist()
```

---
### Query Optimization Tips
1. Predicate Pushdown

```python
# Good - pushes filter to data source
df.filter("age > 30").select("name")

# Bad - reads all data first
df.select("name").filter("age > 30")
```

1. Partition Pruning

```python
# Create partitioned table
df.write.partitionBy("date").saveAsTable("events")

# Query specific partition
spark.sql("SELECT * FROM events WHERE date = '2024-01-01'")
```

---
## Advanced Features

### User-Defined Functions (UDFs)

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Define UDF
@udf(StringType())
def upper_case(s):
    return s.upper() if s else None

# Use UDF
df.select(upper_case("name").alias("upper_name"))
```

---
### Custom Aggregations

```python
from pyspark.sql.expressions import UserDefinedAggregateFunction

class CustomAverage(UserDefinedAggregateFunction):
    def inputSchema(self): ...
    def bufferSchema(self): ...
    def dataType(self): ...
    def deterministic(self): ...
    def initialize(self): ...
    def update(self): ...
    def merge(self): ...
    def evaluate(self): ...
```

---
### Structured Streaming

```python
# Create streaming DataFrame
streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:port") \
    .option("subscribe", "topic") \
    .load()

# Process stream
query = streaming_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
```

---
## Best Practices

### Schema Management

```python
# Define schema explicitly
from pyspark.sql.types import *
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", DoubleType(), True)
])

# Read with schema
df = spark.read.schema(schema).csv("data.csv")
```

---
### Memory Management
1. Broadcast joins for small tables

```python
from pyspark.sql.functions import broadcast
result = df1.join(broadcast(df2), "key")
```

1. Repartitioning for better distribution

```python
# Repartition by key
df = df.repartition("key")

# Repartition by size
df = df.repartition(10)
```

---
## Summary
- Spark SQL provides unified data access
- DataFrames offer type-safe, structured operations
- Multiple data source integration
- Advanced optimization through Catalyst
- Rich ecosystem integration
