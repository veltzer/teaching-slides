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
