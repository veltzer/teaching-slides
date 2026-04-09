# Spark SQL Optimization Techniques
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/big_data/spark-sql-optimization-python/title.svg)

## Understanding the Catalyst Optimizer
Catalyst is Spark's query optimization framework that transforms queries into efficient execution plans
![understanding_the_catalyst_optimizer](svg/lectures/big_data/spark-sql-optimization-python/understanding_the_catalyst_optimizer.svg)

---
## Query Plan Components
Every Spark SQL query goes through multiple plan stages:
1. Parsed Logical Plan
1. Analyzed Logical Plan
1. Optimized Logical Plan
1. Physical Plan
---
## Caching Tables
Cache frequently accessed tables in memory
```python
# Cache table
spark.sql("CACHE TABLE employees")
# Lazy caching
spark.sql("CACHE LAZY TABLE departments")
# Remove from cache
spark.sql("UNCACHE TABLE employees")
# Clear all cached tables
spark.catalog.clearCache()
```
---
## Table Statistics
Accurate statistics help the optimizer make better decisions
```python
# Compute table statistics
spark.sql("ANALYZE TABLE employees COMPUTE STATISTICS")
# Compute column statistics
spark.sql("""
    ANALYZE TABLE employees
    COMPUTE STATISTICS FOR COLUMNS salary, department
""")
# View table statistics
spark.sql("DESCRIBE EXTENDED employees").show()
```
---
## Partition Pruning
Create and query partitioned tables for better performance
```python
# Create partitioned table
spark.sql("""
    CREATE TABLE events (
        id LONG,
        data STRING
    ) PARTITIONED BY (date STRING)
""")
# Query with partition filter
result = spark.sql("""
    SELECT * FROM events
    WHERE date = '2024-02-12'
    AND id > 1000
""")
```
---
## Join Optimizations - Broadcast
Small tables can be broadcasted using hints
```python
# Using broadcast hint
result = spark.sql("""
    SELECT /*+ BROADCAST(dept) */ emp.name, dept.name
    FROM employees emp
    JOIN departments dept ON emp.dept_id = dept.id
""")
# Configure broadcast threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10485760)
```
---
## Join Optimizations - Sort Merge
Optimize large table joins with sort-merge
```python
# Using sort merge hint
result = spark.sql("""
    SELECT /*+ MERGE(sales, customers) */
        s.id, c.name, s.amount
    FROM sales s
    JOIN customers c ON s.customer_id = c.id
""")
# View join execution plan
result.explain()
```
---
## Join Optimizations - Shuffle Hash
Control shuffle partitions for better distribution
```python
# Using shuffle hash hint
result = spark.sql("""
    SELECT /*+ SHUFFLE_HASH(orders) */ *
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
""")
# Configure shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", 200)
```
---
## Skew Join Handling
Handle skewed data in joins
```python
# Enable skew join optimization
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# Query with skew hint
result = spark.sql("""
    SELECT /*+ SKEW('orders') */ *
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
""")
```
---
## Common Table Expressions (CTEs)
Use CTEs for better readability and optimization
```python
result = spark.sql("""
    WITH ranked_sales AS (
        SELECT *,
               RANK() OVER (PARTITION BY region
                           ORDER BY amount DESC) as rank
        FROM sales
    ),
    top_sales AS (
        SELECT * FROM ranked_sales WHERE rank <= 10
    )
    SELECT * FROM top_sales
""")
```
---
## Column Pruning
Select only needed columns for better I/O
```python
# Bad practice
result = spark.sql("SELECT * FROM large_table")
# Good practice
result = spark.sql("""
    SELECT id, name, date
    FROM large_table
    WHERE date > '2024-01-01'
""")
result.explain()  # Verify column pruning
```
---
## Predicate Pushdown
Write queries that allow predicate pushdown
```python
# Enables pushdown
result = spark.sql("""
    SELECT name, age
    FROM employees
    WHERE age > 25 AND department = 'Sales'
""")
# View pushdown details
result.explain(mode="extended")
```
---
## Window Functions Optimization
Optimize window function performance
```python
result = spark.sql("""
    SELECT department,
           salary,
           AVG(salary) OVER (
               PARTITION BY department
               ORDER BY salary
               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
           ) as moving_avg
    FROM employees
""")
```
---
## Bucketing
Create and query bucketed tables
```python
# Create bucketed table
spark.sql("""
    CREATE TABLE sales_bucketed
    USING parquet
    CLUSTERED BY (customer_id) INTO 8 BUCKETS
    AS SELECT * FROM sales
""")
# Query bucketed table
result = spark.sql("""
    SELECT * FROM sales_bucketed s
    JOIN customers c ON s.customer_id = c.id
""")
```
---
## Materialized Views
Create and maintain materialized views
```python
# Create materialized view
spark.sql("""
    CREATE MATERIALIZED VIEW daily_sales
    AS SELECT date, SUM(amount) as total
    FROM sales
    GROUP BY date
""")
# Refresh view
spark.sql("REFRESH MATERIALIZED VIEW daily_sales")
```
---
## AQE Configuration
Configure Adaptive Query Execution
```python
# Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")
# Configure AQE features
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# Test AQE query
result = spark.sql("""
    SELECT d.name, COUNT(e.id) as emp_count
    FROM departments d
    JOIN employees e ON d.id = e.dept_id
    GROUP BY d.name
""")
```
---
## Query Cost Analysis
Analyze query execution cost
```python
# Get full explain plan with cost
query = """
    SELECT d.name, COUNT(e.id) as emp_count
    FROM departments d
    LEFT JOIN employees e ON d.id = e.dept_id
    GROUP BY d.name
"""
# Show explain plan
spark.sql(f"EXPLAIN COST {query}").show(truncate=False)
```
---
## Memory Configuration
Configure memory settings for SQL operations
```python
# Set memory fraction
spark.conf.set("spark.memory.fraction", "0.8")
# Configure storage fraction
spark.conf.set("spark.memory.storageFraction", "0.3")
# Monitor with explain
result = spark.sql("""
    SELECT department, AVG(salary)
    FROM employees
    GROUP BY department
""")
result.explain("cost")
```
---
## Query Plan Analysis
View and analyze execution plans
```python
# Complex query for analysis
query = """
    SELECT e.department,
           AVG(e.salary) as avg_salary,
           COUNT(*) as emp_count
    FROM employees e
    JOIN departments d ON e.dept_id = d.id
    WHERE e.salary > 50000
    GROUP BY e.department
    HAVING AVG(e.salary) > 60000
"""
# View different explain modes
spark.sql(f"EXPLAIN FORMATTED {query}").show(truncate=False)
spark.sql(f"EXPLAIN EXTENDED {query}").show(truncate=False)
```
---
## Statistics-Based Optimization
Enable and configure statistics collection
```python
# Enable histogram statistics
spark.conf.set("spark.sql.statistics.histogram.enabled", "true")
# Compute statistics
spark.sql("""
    ANALYZE TABLE employees COMPUTE STATISTICS
    FOR COLUMNS department, salary
""")
# View statistics
spark.sql("DESCRIBE EXTENDED employees").show()
```
---
## Performance Monitoring
Monitor query performance
```python
# Enable detailed logging
spark.conf.set("spark.sql.execution.logLevel", "TRACE")
# Analyze query performance
result = spark.sql("""
    SELECT /*+ BROADCAST(d) */
        e.department,
        d.location,
        AVG(e.salary) as avg_salary
    FROM employees e
    JOIN departments d ON e.dept_id = d.id
    GROUP BY e.department, d.location
""")
# Get execution details
result.explain(mode="formatted")
```
