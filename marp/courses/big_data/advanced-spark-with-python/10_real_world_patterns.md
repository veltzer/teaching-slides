---
tags:
  - tools:spark
  - languages:python
  - data-and-ai:big-data
  - practices:design-patterns
level: advanced
category: big-data
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Real-World Patterns

---

## Chapter Overview
* ETL pipeline design patterns
* Slowly Changing Dimensions (SCD Type 1/2/3)
* Data quality checks and validation
* Idempotent writes and exactly-once semantics
* Change Data Capture (CDC) with Debezium
* Schema evolution handling
* Monitoring, alerting, and cost optimization

---

## Learning Objectives
* Design robust ETL pipelines with clear separation of concerns
* Implement SCD Type 1, 2, and 3 with Delta Lake MERGE
* Build data quality checks using Great Expectations and custom rules
* Write idempotent pipelines that are safe to re-run
* Implement CDC ingestion from operational databases
* Handle schema evolution gracefully with mergeSchema
* Monitor Spark jobs and optimize cloud costs

---

## ETL Pipeline Architecture

![etl_pipeline_architecture](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/etl_pipeline_architecture.svg)

---

## ETL Pipeline Design Pattern

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from abc import ABC, abstractmethod
from datetime import date
import logging

logger = logging.getLogger(__name__)

class PipelineStep(ABC):
    """Base class for pipeline steps."""

    def __init__(self, spark: SparkSession):
        self.spark = spark

    @abstractmethod
    def extract(self) -> DataFrame:
        pass

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def load(self, df: DataFrame) -> None:
        pass

    def run(self) -> None:
        logger.info(f"Starting {self.__class__.__name__}")
        df = self.extract()
        row_count = df.count()
        logger.info(f"Extracted {row_count} rows")

        df = self.transform(df)
        transformed_count = df.count()
        logger.info(f"Transformed to {transformed_count} rows")

        self.load(df)
        logger.info(f"Loaded {self.__class__.__name__}")
```

---

## ETL Pipeline: Extract

```python
class BronzeToSilverOrders(PipelineStep):
    def __init__(self, spark, process_date: str):
        super().__init__(spark)
        self.process_date = process_date

    def extract(self) -> DataFrame:
        return (
            self.spark.read.format("delta")
            .load("/data/bronze/orders/")
            .filter(F.col("ingestion_date") == self.process_date)
        )
```

---

## ETL Pipeline: Transform

```python
    def transform(self, df: DataFrame) -> DataFrame:
        return (
            df
            .withColumn(
                "row_num",
                F.row_number().over(
                    Window.partitionBy("order_id")
                    .orderBy(F.col("ingestion_ts").desc())
                )
            )
            .filter(F.col("row_num") == 1)
            .drop("row_num")
            .filter(F.col("order_id").isNotNull())
            .filter(F.col("amount") > 0)
            .withColumn("amount",
                        F.col("amount").cast("decimal(18,2)"))
            .withColumn("order_date",
                        F.to_date("order_date_str", "yyyy-MM-dd"))
            .withColumn("processed_at", F.current_timestamp())
            .withColumn("process_date",
                        F.lit(self.process_date))
        )
```

---

## ETL Pipeline: Load and Run

```python
    def load(self, df: DataFrame) -> None:
        (
            df.write.format("delta")
            .mode("overwrite")
            .option("replaceWhere",
                    f"process_date = '{self.process_date}'")
            .save("/data/silver/orders/")
        )

from pyspark.sql import Window

spark = SparkSession.builder \
    .appName("BronzeToSilver") \
    .getOrCreate()

pipeline = BronzeToSilverOrders(spark, "2024-06-15")
pipeline.run()
```

---

## Slowly Changing Dimensions: Overview

![slowly_changing_dimensions_overview](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/slowly_changing_dimensions_overview.svg)

---

## SCD Type 1: Overwrite with MERGE

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("SCDType1") \
    .getOrCreate()

# Target: current customer dimension
target = DeltaTable.forPath(spark, "/data/gold/dim_customer/")

# Source: incoming changes
updates = spark.read.format("delta") \
    .load("/data/silver/customer_updates/")

# SCD Type 1: simply overwrite changed fields
target.alias("t").merge(
    updates.alias("s"),
    "t.customer_id = s.customer_id"
).whenMatchedUpdate(
    set={
        "name": "s.name",
        "email": "s.email",
        "city": "s.city",
        "phone": "s.phone",
        "updated_at": F.current_timestamp(),
    }
).whenNotMatchedInsert(
    values={
        "customer_id": "s.customer_id",
        "name": "s.name",
        "email": "s.email",
        "city": "s.city",
        "phone": "s.phone",
        "created_at": F.current_timestamp(),
        "updated_at": F.current_timestamp(),
    }
).execute()
```

---

## SCD Type 2: Setup and Identify Changes

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("SCDType2") \
    .getOrCreate()

target = DeltaTable.forPath(spark, "/data/gold/dim_customer/")
updates = spark.read.format("delta") \
    .load("/data/silver/customer_updates/")

current = target.toDF().filter("is_current = true")
changes = updates.alias("s").join(
    current.alias("t"),
    "customer_id",
    "inner"
).filter(
    (F.col("s.name") != F.col("t.name")) |
    (F.col("s.city") != F.col("t.city")) |
    (F.col("s.email") != F.col("t.email"))
).select("s.*")
```

---

## SCD Type 2: Expire and Insert

```python
if changes.count() > 0:
    target.alias("t").merge(
        changes.alias("s"),
        "t.customer_id = s.customer_id "
        "AND t.is_current = true"
    ).whenMatchedUpdate(
        set={
            "is_current": F.lit(False),
            "end_date": F.current_date(),
        }
    ).execute()

    new_records = changes.select(
        F.col("customer_id"),
        F.col("name"),
        F.col("email"),
        F.col("city"),
        F.current_date().alias("start_date"),
        F.lit(None).cast("date").alias("end_date"),
        F.lit(True).alias("is_current"),
        F.monotonically_increasing_id().alias("surrogate_key"),
    )
    new_records.write.format("delta") \
        .mode("append") \
        .save("/data/gold/dim_customer/")
```

---

## SCD Type 2: Insert New Customers

```python
target.alias("t").merge(
    updates.alias("s"),
    "t.customer_id = s.customer_id"
).whenNotMatchedInsert(
    values={
        "customer_id": "s.customer_id",
        "name": "s.name",
        "email": "s.email",
        "city": "s.city",
        "start_date": F.current_date(),
        "end_date": F.lit(None).cast("date"),
        "is_current": F.lit(True),
        "surrogate_key": F.monotonically_increasing_id(),
    }
).execute()
```

---

## SCD Type 3: Setup and Merge

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("SCDType3") \
    .getOrCreate()

target = DeltaTable.forPath(spark, "/data/gold/dim_customer/")
updates = spark.read.format("delta") \
    .load("/data/silver/customer_updates/")

target.alias("t").merge(
    updates.alias("s"),
    "t.customer_id = s.customer_id"
).whenMatchedUpdate(
    condition="t.city != s.city",
    set={
        "prev_city": "t.city",
        "city": "s.city",
        "city_changed_date": F.current_date(),
        "name": "s.name",
        "email": "s.email",
        "updated_at": F.current_timestamp(),
    }
```

---

## SCD Type 3: Other Branches and Query

```python
).whenMatchedUpdate(
    set={
        "name": "s.name",
        "email": "s.email",
        "updated_at": F.current_timestamp(),
    }
).whenNotMatchedInsert(
    values={
        "customer_id": "s.customer_id",
        "name": "s.name",
        "email": "s.email",
        "city": "s.city",
        "prev_city": F.lit(None).cast("string"),
        "city_changed_date": F.lit(None).cast("date"),
        "created_at": F.current_timestamp(),
        "updated_at": F.current_timestamp(),
    }
).execute()

moved = spark.sql("""
    SELECT customer_id, name, city, prev_city,
           city_changed_date
    FROM dim_customer
    WHERE prev_city IS NOT NULL
    ORDER BY city_changed_date DESC
""")
moved.show()
```

---

## SCD Type Comparison

| Feature | Type 1 | Type 2 | Type 3 |
|---|---|---|---|
| History preserved | No | Full history | Previous value only |
| Storage growth | Constant | Grows with changes | Constant |
| Query complexity | Simple | Needs is_current filter | Simple |
| Surrogate keys | Not needed | Required | Not needed |
| Slowly changing | Any frequency | Any frequency | Infrequent changes |
| Reporting at point-in-time | No | Yes | Limited |
| Implementation complexity | Low | High | Medium |

---

## Data Quality: Validation Types

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from dataclasses import dataclass
from typing import List
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    check_name: str
    passed: bool
    details: str

def check_not_null(df: DataFrame,
                   columns: List[str]) -> List[ValidationResult]:
    results = []
    for col in columns:
        null_count = df.filter(F.col(col).isNull()).count()
        results.append(ValidationResult(
            check_name=f"not_null_{col}",
            passed=null_count == 0,
            details=f"{null_count} null values in {col}",
        ))
    return results
```

---

## Data Quality: Unique and Range

```python
def check_unique(df: DataFrame,
                 columns: List[str]) -> ValidationResult:
    total = df.count()
    distinct = df.select(columns).distinct().count()
    return ValidationResult(
        check_name=f"unique_{'_'.join(columns)}",
        passed=total == distinct,
        details=f"{total - distinct} duplicate rows",
    )

def check_range(df: DataFrame, column: str,
                min_val: float,
                max_val: float) -> ValidationResult:
    out_of_range = df.filter(
        (F.col(column) < min_val) |
        (F.col(column) > max_val)
    ).count()
    return ValidationResult(
        check_name=f"range_{column}",
        passed=out_of_range == 0,
        details=f"{out_of_range} values outside "
                f"[{min_val}, {max_val}]",
    )

def check_referential_integrity(
    df: DataFrame,
    ref_df: DataFrame,
    column: str,
) -> ValidationResult:
    orphans = df.join(ref_df, column, "left_anti").count()
    return ValidationResult(
        check_name=f"ref_integrity_{column}",
        passed=orphans == 0,
        details=f"{orphans} orphaned records",
    )
```

---

## Data Quality: Running Checks

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("DataQualityChecks") \
    .getOrCreate()

orders = spark.read.format("delta") \
    .load("/data/silver/orders/")
customers = spark.read.format("delta") \
    .load("/data/silver/customers/")

results = []
results.extend(
    check_not_null(orders, ["order_id", "customer_id", "amount"])
)
results.append(
    check_unique(orders, ["order_id"])
)
results.append(
    check_range(orders, "amount", min_val=0.01, max_val=1_000_000)
)
results.append(
    check_referential_integrity(
        orders, customers, "customer_id")
)
```

---

## Data Quality: Reporting

```python
passed = sum(1 for r in results if r.passed)
failed = sum(1 for r in results if not r.passed)
print(f"\nData Quality Report:")
print(f"  Passed: {passed}")
print(f"  Failed: {failed}")
print(f"  Total:  {len(results)}")

for r in results:
    status = "PASS" if r.passed else "FAIL"
    print(f"  [{status}] {r.check_name}: {r.details}")

critical_failures = [r for r in results if not r.passed]
if critical_failures:
    raise ValueError(
        f"{len(critical_failures)} quality checks failed: "
        + ", ".join(r.check_name for r in critical_failures)
    )
```

---

## Great Expectations: Context Setup

```python
from pyspark.sql import SparkSession
import great_expectations as gx

spark = SparkSession.builder \
    .appName("GreatExpectations") \
    .getOrCreate()

df = spark.read.format("delta").load("/data/silver/orders/")

context = gx.get_context()

datasource = context.data_sources.add_spark("spark_source")
data_asset = datasource.add_dataframe_asset("orders")
batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "orders_batch"
)
batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)
```

---

## Great Expectations: Define Expectations

```python
expectations = context.suites.add(
    gx.ExpectationSuite(name="orders_suite")
)
expectations.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="order_id"
    )
)
expectations.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="order_id"
    )
)
expectations.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount", min_value=0.01, max_value=1000000
    )
)
expectations.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        column="email", regex=r"^[a-zA-Z0-9+_.'-]+@.+\..+$"
    )
)
```

---

## Great Expectations: Validate and Check

```python
validation_definition = context.validation_definitions.add(
    gx.ValidationDefinition(
        name="orders_validation",
        data=batch_definition,
        suite=expectations,
    )
)
result = validation_definition.run()

if not result.success:
    for r in result.results:
        if not r.success:
            print(f"FAILED: {r.expectation_config}")
    raise ValueError("Data quality validation failed")
```

---

## Idempotent Writes: Dynamic Overwrite

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("IdempotentWrites") \
    .getOrCreate()

spark.conf.set(
    "spark.sql.sources.partitionOverwriteMode", "dynamic")

df = spark.read.parquet("/data/staging/orders/")
df.write \
    .partitionBy("order_date") \
    .mode("overwrite") \
    .parquet("/data/silver/orders/")
```

---

## Idempotent Writes: `replaceWhere` and DELETE

```python
process_date = "2024-06-15"
df = spark.read.parquet(f"/data/staging/{process_date}/")
df = df.withColumn("process_date", F.lit(process_date))

df.write.format("delta") \
    .mode("overwrite") \
    .option("replaceWhere",
            f"process_date = '{process_date}'") \
    .save("/data/silver/orders/")

spark.sql(f"""
    DELETE FROM silver_orders
    WHERE process_date = '{process_date}'
""")
df.write.format("delta") \
    .mode("append") \
    .save("/data/silver/orders/")
```

---

## Idempotent Write Comparison

![idempotent_write_comparison](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/idempotent_write_comparison.svg)

---

## Exactly-Once: Read and Parse

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("ExactlyOnceStreaming") \
    .getOrCreate()

stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "events")
    .option("startingOffsets", "earliest")
    .load()
)

parsed = (
    stream
    .select(
        F.col("key").cast("string"),
        F.from_json(
            F.col("value").cast("string"),
            "event_id STRING, user_id STRING, "
            "event_type STRING, amount DOUBLE, "
            "event_ts TIMESTAMP"
        ).alias("data"),
    )
    .select("data.*")
    .withColumn("event_date", F.to_date("event_ts"))
)
```

---

## Exactly-Once: Write Stream

```python
query = (
    parsed.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation",
            "/checkpoints/events_stream/")
    .option("mergeSchema", "true")
    .partitionBy("event_date")
    .trigger(processingTime="1 minute")
    .start("/data/bronze/events/")
)
```

---

## Checkpointing Architecture

![checkpointing_architecture](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/checkpointing_architecture.svg)

---

## Change Data Capture (CDC) with Debezium

![change_data_capture_cdc_with_debezium](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/change_data_capture_cdc_with_debezium.svg)

---

## CDC: Read Kafka and Parse

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("CDCProcessing") \
    .getOrCreate()

cdc_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "dbserver1.public.customers")
    .load()
)

cdc_schema = """
    op STRING,
    before STRUCT<customer_id: INT, name: STRING,
                  email: STRING, city: STRING>,
    after STRUCT<customer_id: INT, name: STRING,
                 email: STRING, city: STRING>,
    ts_ms BIGINT
"""

parsed = cdc_stream.select(
    F.from_json(
        F.col("value").cast("string"), cdc_schema
    ).alias("cdc")
).select("cdc.*")
```

---

## CDC: Batch Handler

```python
def apply_cdc_batch(batch_df, batch_id):
    if batch_df.count() == 0:
        return

    latest = (
        batch_df
        .withColumn("row_num", F.row_number().over(
            Window.partitionBy(
                F.coalesce("after.customer_id",
                            "before.customer_id")
            ).orderBy(F.col("ts_ms").desc())
        ))
        .filter("row_num = 1")
    )

    target = DeltaTable.forPath(
        spark, "/data/bronze/customers/")

    upserts = latest.filter("op IN ('c', 'u', 'r')") \
        .select("after.*")
    deletes = latest.filter("op = 'd'") \
        .select("before.customer_id")
```

---

## CDC: Merge Upserts and Deletes

```python
    if upserts.count() > 0:
        target.alias("t").merge(
            upserts.alias("s"),
            "t.customer_id = s.customer_id"
        ).whenMatchedUpdateAll() \
         .whenNotMatchedInsertAll() \
         .execute()

    if deletes.count() > 0:
        target.alias("t").merge(
            deletes.alias("s"),
            "t.customer_id = s.customer_id"
        ).whenMatchedDelete().execute()

from pyspark.sql import Window

query = (
    parsed.writeStream
    .foreachBatch(apply_cdc_batch)
    .option("checkpointLocation",
            "/checkpoints/cdc_customers/")
    .trigger(processingTime="30 seconds")
    .start()
)
```

---

## Schema Evolution: mergeSchema

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("SchemaEvolution") \
    .getOrCreate()

new_data = spark.read.parquet("/data/new_batch/")
new_data.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/data/delta/customers/")

spark.conf.set(
    "spark.databricks.delta.schema.autoMerge.enabled",
    "true")
```

---

## Schema Evolution: Overwrite and ALTER

```python
new_data.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save("/data/delta/customers/")

spark.sql("""
    ALTER TABLE customers
    ADD COLUMNS (
        phone STRING COMMENT 'Phone number',
        address STRING COMMENT 'Mailing address'
    )
""")

spark.read.format("delta") \
    .load("/data/delta/customers/") \
    .printSchema()
```

---

## Schema Evolution Strategy

![schema_evolution_strategy](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/schema_evolution_strategy.svg)

---

## Monitoring: Metrics Listener

```python
from pyspark.sql import SparkSession
from pyspark import SparkContext
import json
import time

class PipelineMetricsListener:
    def __init__(self):
        self.metrics = {
            "jobs": [],
            "stages": [],
            "start_time": time.time(),
        }

    def on_job_end(self, job_id, status, stages):
        self.metrics["jobs"].append({
            "job_id": job_id,
            "status": status,
            "num_stages": stages,
        })

spark = SparkSession.builder \
    .appName("Monitoring") \
    .config("spark.metrics.conf.*.sink.prometheusServlet"
            ".class",
            "org.apache.spark.metrics.sink."
            "PrometheusServlet") \
    .config("spark.metrics.conf.*.sink.prometheusServlet"
            ".path", "/metrics/prometheus") \
    .config("spark.ui.prometheus.enabled", "true") \
    .getOrCreate()
```

---

## Monitoring: Inspect Metrics

```python
df = spark.read.parquet("/data/events/")
result = df.groupBy("event_type").count()
result.show()

status_store = spark.sparkContext.statusTracker
active_jobs = status_store.getActiveJobIds()
print(f"Active jobs: {active_jobs}")

for job_id in status_store.getJobIdsForGroup():
    job_info = status_store.getJobInfo(job_id)
    if job_info:
        print(f"Job {job_id}: status={job_info.status}")
```

---

## Monitoring: `PipelineMonitor` Class

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time
import json
import logging

logger = logging.getLogger(__name__)

class PipelineMonitor:
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.start_time = None
        self.metrics = {}

    def start(self):
        self.start_time = time.time()
        logger.info(f"Pipeline {self.pipeline_name} started")

    def record_metric(self, name: str, value):
        self.metrics[name] = value
        logger.info(f"Metric {name}: {value}")

    def finish(self):
        duration = time.time() - self.start_time
        self.metrics["duration_seconds"] = duration
        logger.info(
            f"Pipeline {self.pipeline_name} finished "
            f"in {duration:.2f}s"
        )
        return self.metrics
```

---

## Monitoring: Freshness Check

```python
    def check_data_freshness(self, df, ts_column,
                              max_delay_hours=6):
        max_ts = df.agg(
            F.max(ts_column).alias("max_ts")
        ).collect()[0]["max_ts"]

        if max_ts is None:
            logger.error("No data found!")
            return False

        from datetime import datetime, timedelta
        threshold = datetime.now() - timedelta(
            hours=max_delay_hours)
        if max_ts < threshold:
            logger.error(
                f"Data stale! Latest: {max_ts}, "
                f"threshold: {threshold}"
            )
            return False

        logger.info(f"Data fresh. Latest: {max_ts}")
        return True
```

---

## Monitoring: Row Count Check and Usage

```python
    def check_row_count(self, df, min_expected,
                         max_expected=None):
        count = df.count()
        self.record_metric("row_count", count)

        if count < min_expected:
            logger.error(
                f"Row count {count} below minimum "
                f"{min_expected}")
            return False
        if max_expected and count > max_expected:
            logger.error(
                f"Row count {count} above maximum "
                f"{max_expected}")
            return False
        return True

spark = SparkSession.builder \
    .appName("MonitoredPipeline") \
    .getOrCreate()

monitor = PipelineMonitor("daily_orders")
monitor.start()

df = spark.read.format("delta").load("/data/silver/orders/")
monitor.check_data_freshness(df, "order_date",
                              max_delay_hours=24)
monitor.check_row_count(df, min_expected=1000,
                         max_expected=10_000_000)

result = df.groupBy("region").agg(
    F.sum("amount").alias("total"))
monitor.record_metric("regions_processed",
                       result.count())

metrics = monitor.finish()
print(json.dumps(metrics, indent=2, default=str))
```

---

## Prometheus Metrics Configuration

![prometheus_metrics_configuration](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/prometheus_metrics_configuration.svg)

---

## Cost Optimization Strategies

![cost_optimization_strategies](svg/courses/big_data/advanced-spark-with-python/10_real_world_patterns/cost_optimization_strategies.svg)

---

## Cost Optimization: Dynamic Allocation

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CostOptimized") \
    .config("spark.dynamicAllocation.enabled", "true") \
    .config("spark.dynamicAllocation"
            ".minExecutors", "2") \
    .config("spark.dynamicAllocation"
            ".maxExecutors", "50") \
    .config("spark.dynamicAllocation"
            ".executorIdleTimeout", "60s") \
    .config("spark.dynamicAllocation"
            ".schedulerBacklogTimeout", "5s") \
    .config("spark.shuffle.service.enabled", "true") \
    .getOrCreate()
```

---

## Cost Optimization: AQE and Compression

```python
spark = SparkSession.builder \
    .appName("CostOptimized") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive"
            ".coalescePartitions.enabled", "true") \
    .config("spark.serializer",
            "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.parquet.compression.codec", "zstd") \
    .config("spark.network.timeout", "600s") \
    .getOrCreate()
```

---

## Full Program: Session and Bronze Ingest

```python
from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from delta.tables import DeltaTable
import logging
import time
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("production_etl")

def create_spark_session():
    return (
        SparkSession.builder
        .appName("ProductionETL")
        .config("spark.sql.extensions",
                "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog."
                "DeltaCatalog")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.shuffle.partitions", "200")
        .getOrCreate()
    )
```

---

## Full Program: Bronze Ingestion

```python
def ingest_bronze(spark, process_date):
    logger.info(f"Ingesting bronze for {process_date}")
    raw = spark.read.json(f"/data/raw/{process_date}/")
    raw = raw.withColumn("ingestion_ts",
                         F.current_timestamp())
    raw = raw.withColumn("ingestion_date",
                         F.lit(process_date))

    raw.write.format("delta") \
        .mode("overwrite") \
        .option("replaceWhere",
                f"ingestion_date = '{process_date}'") \
        .partitionBy("ingestion_date") \
        .save("/data/bronze/orders/")

    count = raw.count()
    logger.info(f"Bronze: ingested {count} rows")
    return count
```

---

## Full Program: Silver Transform

```python
def transform_silver(spark, process_date):
    logger.info(f"Transforming silver for {process_date}")
    bronze = (
        spark.read.format("delta")
        .load("/data/bronze/orders/")
        .filter(F.col("ingestion_date") == process_date)
    )

    silver = (
        bronze
        .withColumn("rn", F.row_number().over(
            Window.partitionBy("order_id")
            .orderBy(F.col("ingestion_ts").desc())
        ))
        .filter("rn = 1").drop("rn")
        .filter(F.col("order_id").isNotNull())
        .filter(F.col("amount") > 0)
        .withColumn("amount",
                    F.col("amount").cast("decimal(18,2)"))
        .withColumn("order_date",
                    F.to_date("order_date_str"))
        .withColumn("process_date", F.lit(process_date))
    )

    silver.write.format("delta") \
        .mode("overwrite") \
        .option("replaceWhere",
                f"process_date = '{process_date}'") \
        .save("/data/silver/orders/")

    count = silver.count()
    logger.info(f"Silver: wrote {count} rows")
    return count
```

---

## Full Program: Build Gold

```python
def build_gold(spark, process_date):
    logger.info(f"Building gold for {process_date}")
    silver = (
        spark.read.format("delta")
        .load("/data/silver/orders/")
        .filter(F.col("process_date") == process_date)
    )
    customers = spark.read.format("delta") \
        .load("/data/silver/customers/")

    gold = (
        silver.groupBy("customer_id", "order_date")
        .agg(
            F.sum("amount").alias("daily_total"),
            F.count("*").alias("order_count"),
            F.avg("amount").alias("avg_order_value"),
        )
        .join(
            F.broadcast(customers.select(
                "customer_id", "name", "region")),
            "customer_id",
            "left",
        )
        .withColumn("process_date", F.lit(process_date))
    )

    gold.write.format("delta") \
        .mode("overwrite") \
        .option("replaceWhere",
                f"process_date = '{process_date}'") \
        .save("/data/gold/daily_summary/")

    count = gold.count()
    logger.info(f"Gold: wrote {count} rows")
    return count
```

---

## Full Program: Validate

```python
def validate(spark, process_date):
    gold = (
        spark.read.format("delta")
        .load("/data/gold/daily_summary/")
        .filter(F.col("process_date") == process_date)
    )

    count = gold.count()
    if count == 0:
        raise ValueError("Gold table is empty!")

    null_customers = gold.filter(
        "customer_id IS NULL").count()
    if null_customers > 0:
        raise ValueError(
            f"{null_customers} null customer_ids!")

    negative = gold.filter("daily_total < 0").count()
    if negative > 0:
        logger.warning(f"{negative} negative totals")

    logger.info(f"Validation passed: {count} rows OK")
```

---

## Full Program: Main

```python
def main():
    process_date = sys.argv[1] if len(sys.argv) > 1 \
        else "2024-06-15"

    spark = create_spark_session()
    start = time.time()

    try:
        bronze_count = ingest_bronze(spark, process_date)
        silver_count = transform_silver(spark, process_date)
        gold_count = build_gold(spark, process_date)
        validate(spark, process_date)

        duration = time.time() - start
        logger.info(
            f"Pipeline complete: "
            f"bronze={bronze_count}, "
            f"silver={silver_count}, "
            f"gold={gold_count}, "
            f"duration={duration:.1f}s"
        )
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

---

## Summary: Real-World Patterns

**Pipeline Design:**
* Use Bronze/Silver/Gold layered architecture
* Separate extract, transform, load concerns
* Make every step idempotent (safe to re-run)

**Data Management:**
* SCD Type 1 for simple overwrites
* SCD Type 2 for full history tracking
* Use Delta Lake `MERGE` for all upsert patterns
* Handle schema evolution with `mergeSchema`

**Data Quality:**
* Validate at each layer boundary
* Check nulls, ranges, uniqueness, referential
* Fail fast on critical violations
* Use Great Expectations for complex rules
