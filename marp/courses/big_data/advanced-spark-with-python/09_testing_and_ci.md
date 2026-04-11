---
tags:
  - tools:spark
  - languages:python
  - data-and-ai:big-data
  - practices:testing
level: advanced
category: big-data
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Testing and CI/CD for PySpark

---
## Chapter Overview
* Unit testing PySpark with pytest
* Creating test SparkSessions and fixtures
* DataFrame assertions and comparison libraries
* Testing UDFs and complex transformations
* Integration testing patterns
* CI/CD pipeline setup for Spark jobs
* Code quality tools: pylint, mypy, black

---
## Learning Objectives
* Write effective unit tests for PySpark transformations
* Set up reusable test fixtures with conftest.py
* Use chispa for DataFrame equality assertions
* Mock external data sources for isolated testing
* Design integration tests for end-to-end pipelines
* Configure GitHub Actions CI for Spark projects
* Enforce code quality with linting and type checking

---
## Spark Testing Pyramid

![spark_testing_pyramid](svg/courses/big_data/advanced-spark-with-python/09_testing_and_ci/spark_testing_pyramid.svg)

---
## Testing Architecture

![testing_architecture](svg/courses/big_data/advanced-spark-with-python/09_testing_and_ci/testing_architecture.svg)

---
## Project Structure for Testable Spark Code

```tree
my_spark_project/
├── src/
│   ├── __init__.py
│   ├── transformations/
│   │   ├── __init__.py
│   │   ├── cleaning.py
│   │   ├── enrichment.py
│   │   └── aggregation.py
│   ├── udfs/
│   │   ├── __init__.py
│   │   └── custom_functions.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   └── daily_etl.py
│   └── utils/
│       ├── __init__.py
│       └── spark_session.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          <- shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_cleaning.py
│   │   ├── test_enrichment.py
│   │   └── test_udfs.py
│   └── integration/
│       ├── __init__.py
│       └── test_daily_etl.py
├── pyproject.toml
└── .github/
    └── workflows/
        └── ci.yml
```

---
## Creating a Test SparkSession

```python
# tests/conftest.py
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    """Create a SparkSession for the entire test session."""
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("unit-tests")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "2")
        .config("spark.sql.warehouse.dir", "/tmp/spark-wh")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()

@pytest.fixture(autouse=True)
def reset_spark_context(spark):
    """Reset any cached tables between tests."""
    spark.catalog.clearCache()
    for table in spark.catalog.listTables():
        spark.catalog.dropTempView(table.name)
```

---
## Why These SparkSession Settings

| Setting | Value | Reason |
|---|---|---|
| master | local[2] | 2 threads catches parallelism bugs |
| shuffle.partitions | 2 | Faster than default 200 for small data |
| default.parallelism | 2 | Match local[2] thread count |
| spark.ui.enabled | false | No web UI needed in tests |
| driver.bindAddress | 127.0.0.1 | Avoid network issues in CI |

---
## Writing Your First PySpark Test

```python
# src/transformations/cleaning.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def remove_duplicates(df: DataFrame, key_cols: list) -> DataFrame:
    """Remove duplicate rows based on key columns."""
    return df.dropDuplicates(key_cols)

def fill_missing_amounts(df: DataFrame,
                         default: float = 0.0) -> DataFrame:
    """Fill null amounts with a default value."""
    return df.fillna({"amount": default})

def normalize_email(df: DataFrame) -> DataFrame:
    """Lowercase and trim email addresses."""
    return df.withColumn(
        "email",
        F.lower(F.trim(F.col("email")))
    )
```

---
## Test for Cleaning Functions

```python
# tests/unit/test_cleaning.py
from pyspark.sql import Row
from src.transformations.cleaning import (
    remove_duplicates,
    fill_missing_amounts,
    normalize_email,
)

def test_remove_duplicates(spark):
    data = [
        Row(id=1, name="Alice"),
        Row(id=1, name="Alice"),
        Row(id=2, name="Bob"),
    ]
    df = spark.createDataFrame(data)
    result = remove_duplicates(df, ["id"])
    assert result.count() == 2

def test_fill_missing_amounts(spark):
    data = [
        Row(id=1, amount=100.0),
        Row(id=2, amount=None),
        Row(id=3, amount=50.0),
    ]
    df = spark.createDataFrame(data)
    result = fill_missing_amounts(df, default=0.0)

    null_count = result.filter("amount IS NULL").count()
    assert null_count == 0

    row = result.filter("id = 2").collect()[0]
    assert row["amount"] == 0.0

def test_normalize_email(spark):
    data = [
        Row(id=1, email="  Alice@EXAMPLE.COM  "),
        Row(id=2, email="BOB@test.com"),
    ]
    df = spark.createDataFrame(data)
    result = normalize_email(df)

    emails = [r["email"] for r in result.collect()]
    assert "alice@example.com" in emails
    assert "bob@test.com" in emails
```

---
## DataFrame Assertions Without Libraries

```python
# tests/unit/test_manual_assertions.py
from pyspark.sql import Row
from pyspark.sql import functions as F

def assert_dataframe_equal(df1, df2, order_by=None):
    """Compare two DataFrames for equality."""
    # Check schemas match
    assert df1.schema == df2.schema, (
        f"Schema mismatch:\n"
        f"  Left:  {df1.schema}\n"
        f"  Right: {df2.schema}"
    )

    # Check row counts match
    count1, count2 = df1.count(), df2.count()
    assert count1 == count2, (
        f"Row count mismatch: {count1} vs {count2}"
    )

    # Sort both DataFrames for deterministic comparison
    if order_by:
        df1 = df1.orderBy(order_by)
        df2 = df2.orderBy(order_by)
    else:
        cols = df1.columns
        df1 = df1.orderBy(cols)
        df2 = df2.orderBy(cols)

    # Compare row by row
    rows1 = df1.collect()
    rows2 = df2.collect()
    for i, (r1, r2) in enumerate(zip(rows1, rows2)):
        assert r1 == r2, (
            f"Row {i} mismatch:\n"
            f"  Left:  {r1}\n"
            f"  Right: {r2}"
        )

def test_transformation_output(spark):
    input_data = [Row(x=1, y=2), Row(x=3, y=4)]
    expected_data = [Row(x=1, y=2, z=3), Row(x=3, y=4, z=7)]

    df = spark.createDataFrame(input_data)
    result = df.withColumn("z", F.col("x") + F.col("y"))
    expected = spark.createDataFrame(expected_data)

    assert_dataframe_equal(result, expected, order_by="x")
```

---
## Using chispa for DataFrame Equality

```python
# pip install chispa

# tests/unit/test_with_chispa.py
from chispa.dataframe_comparer import assert_df_equality
from chispa.column_comparer import assert_column_equality
from pyspark.sql import Row
from pyspark.sql import functions as F

def test_exact_equality(spark):
    data1 = [Row(id=1, value=10.0), Row(id=2, value=20.0)]
    data2 = [Row(id=1, value=10.0), Row(id=2, value=20.0)]
    df1 = spark.createDataFrame(data1)
    df2 = spark.createDataFrame(data2)

    # Exact match (order-independent)
    assert_df_equality(df1, df2, ignore_row_order=True)

def test_approximate_equality(spark):
    data1 = [Row(id=1, value=10.0001)]
    data2 = [Row(id=1, value=10.0002)]
    df1 = spark.createDataFrame(data1)
    df2 = spark.createDataFrame(data2)

    # Allow small float differences
    assert_df_equality(
        df1, df2,
        ignore_row_order=True,
        precision=0.001,
    )

def test_ignore_nullable(spark):
    """Schema nullable flags often differ; ignore them."""
    data = [Row(id=1, name="Alice")]
    df1 = spark.createDataFrame(data)
    df2 = spark.createDataFrame(data)

    assert_df_equality(
        df1, df2,
        ignore_nullable=True,
    )

def test_column_equality(spark):
    data = [Row(id=1, first="Alice", computed="Alice")]
    df = spark.createDataFrame(data)
    assert_column_equality(df, "first", "computed")
```

---
## chispa Error Messages

![chispa_error_messages](svg/courses/big_data/advanced-spark-with-python/09_testing_and_ci/chispa_error_messages.svg)

---
## Test Fixtures with conftest.py

```python
# tests/conftest.py
import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from datetime import date

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("unit-tests")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()

@pytest.fixture
def sample_orders(spark):
    """Reusable sample orders DataFrame."""
    data = [
        Row(order_id=1, customer_id=101,
            amount=50.0, order_date=date(2024, 1, 15)),
        Row(order_id=2, customer_id=102,
            amount=75.0, order_date=date(2024, 1, 16)),
        Row(order_id=3, customer_id=101,
            amount=120.0, order_date=date(2024, 2, 1)),
        Row(order_id=4, customer_id=103,
            amount=200.0, order_date=date(2024, 2, 10)),
        Row(order_id=5, customer_id=102,
            amount=30.0, order_date=date(2024, 2, 15)),
    ]
    return spark.createDataFrame(data)

@pytest.fixture
def sample_customers(spark):
    """Reusable sample customers DataFrame."""
    data = [
        Row(customer_id=101, name="Alice", region="US"),
        Row(customer_id=102, name="Bob", region="EU"),
        Row(customer_id=103, name="Charlie", region="US"),
    ]
    return spark.createDataFrame(data)

@pytest.fixture
def empty_orders(spark):
    """Empty DataFrame with the orders schema."""
    from pyspark.sql.types import StructType, StructField, \
        IntegerType, DoubleType, DateType
    schema = StructType([
        StructField("order_id", IntegerType(), False),
        StructField("customer_id", IntegerType(), False),
        StructField("amount", DoubleType(), True),
        StructField("order_date", DateType(), True),
    ])
    return spark.createDataFrame([], schema)
```

---
## Testing UDFs

```python
# src/udfs/custom_functions.py
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, DoubleType
import re

def classify_amount_logic(amount):
    """Pure Python logic for testability."""
    if amount is None:
        return "unknown"
    if amount < 50:
        return "small"
    if amount < 200:
        return "medium"
    return "large"

classify_amount_udf = F.udf(classify_amount_logic, StringType())

def clean_phone_logic(phone):
    """Pure Python logic for testability."""
    if phone is None:
        return None
    digits = re.sub(r"[^\d]", "", phone)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    if len(digits) == 11 and digits[0] == "1":
        return (f"({digits[1:4]}) "
                f"{digits[4:7]}-{digits[7:]}")
    return None

clean_phone_udf = F.udf(clean_phone_logic, StringType())
```

---
## Testing UDFs: Pure Python and Spark

```python
# tests/unit/test_udfs.py
import pytest
from pyspark.sql import Row
from src.udfs.custom_functions import (
    classify_amount_logic,
    classify_amount_udf,
    clean_phone_logic,
    clean_phone_udf,
)

# ---- Test pure Python logic (fast, no Spark needed) ----

class TestClassifyAmountLogic:
    def test_small(self):
        assert classify_amount_logic(10) == "small"

    def test_medium(self):
        assert classify_amount_logic(100) == "medium"

    def test_large(self):
        assert classify_amount_logic(500) == "large"

    def test_boundary_50(self):
        assert classify_amount_logic(50) == "medium"

    def test_boundary_200(self):
        assert classify_amount_logic(200) == "large"

    def test_none(self):
        assert classify_amount_logic(None) == "unknown"

class TestCleanPhoneLogic:
    def test_ten_digits(self):
        assert clean_phone_logic("5551234567") == \
            "(555) 123-4567"

    def test_with_dashes(self):
        assert clean_phone_logic("555-123-4567") == \
            "(555) 123-4567"

    def test_with_country_code(self):
        assert clean_phone_logic("15551234567") == \
            "(555) 123-4567"

    def test_invalid(self):
        assert clean_phone_logic("123") is None

    def test_none(self):
        assert clean_phone_logic(None) is None

# ---- Test UDFs within Spark (verify serialization) ----

def test_classify_amount_udf_in_spark(spark):
    data = [
        Row(id=1, amount=10.0),
        Row(id=2, amount=100.0),
        Row(id=3, amount=500.0),
        Row(id=4, amount=None),
    ]
    df = spark.createDataFrame(data)
    result = df.withColumn(
        "category", classify_amount_udf("amount"))

    rows = {r["id"]: r["category"]
            for r in result.collect()}
    assert rows[1] == "small"
    assert rows[2] == "medium"
    assert rows[3] == "large"
    assert rows[4] == "unknown"

def test_clean_phone_udf_in_spark(spark):
    data = [
        Row(id=1, phone="555-123-4567"),
        Row(id=2, phone="123"),
    ]
    df = spark.createDataFrame(data)
    result = df.withColumn(
        "clean", clean_phone_udf("phone"))

    rows = {r["id"]: r["clean"]
            for r in result.collect()}
    assert rows[1] == "(555) 123-4567"
    assert rows[2] is None
```

---
## Mocking External Data Sources

```python
# tests/unit/test_with_mocks.py
import pytest
from unittest.mock import patch, MagicMock
from pyspark.sql import Row

# src/pipelines/daily_etl.py (the code under test)
# def run_daily_etl(spark, input_path, output_path):
#     df = spark.read.parquet(input_path)
#     result = df.filter("amount > 0").groupBy("region").sum()
#     result.write.mode("overwrite").parquet(output_path)

def test_etl_with_mock_io(spark, tmp_path):
    """Use tmp_path to simulate file I/O."""
    # Create test input data
    input_data = [
        Row(region="US", amount=100.0),
        Row(region="US", amount=-50.0),
        Row(region="EU", amount=200.0),
    ]
    input_path = str(tmp_path / "input")
    output_path = str(tmp_path / "output")

    # Write test input
    spark.createDataFrame(input_data) \
        .write.parquet(input_path)

    # Run the ETL
    from src.pipelines.daily_etl import run_daily_etl
    run_daily_etl(spark, input_path, output_path)

    # Verify output
    result = spark.read.parquet(output_path)
    assert result.count() == 2  # US and EU

    us_row = result.filter("region = 'US'").collect()[0]
    assert us_row["sum(amount)"] == 100.0

def test_etl_with_mocked_reader(spark):
    """Mock spark.read to avoid filesystem access."""
    test_data = [
        Row(region="US", amount=100.0),
        Row(region="EU", amount=200.0),
    ]
    test_df = spark.createDataFrame(test_data)

    # Patch the read path
    mock_reader = MagicMock()
    mock_reader.parquet.return_value = test_df

    with patch.object(spark, "read", mock_reader):
        df = spark.read.parquet("/fake/path")
        result = df.filter("amount > 0") \
            .groupBy("region").sum("amount")
        assert result.count() == 2
```

---
## Integration Testing Patterns

```python
# tests/integration/test_daily_etl.py
import pytest
import os
from datetime import date
from pyspark.sql import Row

@pytest.fixture
def etl_dirs(tmp_path):
    """Create directory structure for ETL test."""
    dirs = {
        "raw": str(tmp_path / "raw"),
        "staging": str(tmp_path / "staging"),
        "output": str(tmp_path / "output"),
        "checkpoint": str(tmp_path / "checkpoints"),
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    return dirs

def test_full_daily_pipeline(spark, etl_dirs):
    """Integration test: run the full daily pipeline."""
    # Arrange: create realistic test data
    orders = [
        Row(order_id=1, customer_id=101,
            amount=50.0, order_date=date(2024, 6, 15)),
        Row(order_id=2, customer_id=102,
            amount=75.0, order_date=date(2024, 6, 15)),
        Row(order_id=3, customer_id=101,
            amount=120.0, order_date=date(2024, 6, 15)),
    ]
    customers = [
        Row(customer_id=101, name="Alice", region="US"),
        Row(customer_id=102, name="Bob", region="EU"),
    ]

    spark.createDataFrame(orders) \
        .write.parquet(f"{etl_dirs['raw']}/orders")
    spark.createDataFrame(customers) \
        .write.parquet(f"{etl_dirs['raw']}/customers")

    # Act: run the pipeline
    from src.pipelines.daily_etl import DailyETL
    etl = DailyETL(spark, etl_dirs)
    etl.run(process_date="2024-06-15")

    # Assert: verify output
    result = spark.read.parquet(
        f"{etl_dirs['output']}/customer_summary")

    assert result.count() == 2

    alice = result.filter("name = 'Alice'").collect()[0]
    assert alice["total_amount"] == 170.0
    assert alice["order_count"] == 2

    bob = result.filter("name = 'Bob'").collect()[0]
    assert bob["total_amount"] == 75.0
    assert bob["order_count"] == 1

def test_pipeline_idempotent(spark, etl_dirs):
    """Running the pipeline twice produces same result."""
    orders = [
        Row(order_id=1, customer_id=101,
            amount=50.0, order_date=date(2024, 6, 15)),
    ]
    customers = [
        Row(customer_id=101, name="Alice", region="US"),
    ]

    spark.createDataFrame(orders) \
        .write.parquet(f"{etl_dirs['raw']}/orders")
    spark.createDataFrame(customers) \
        .write.parquet(f"{etl_dirs['raw']}/customers")

    from src.pipelines.daily_etl import DailyETL
    etl = DailyETL(spark, etl_dirs)

    # Run twice
    etl.run(process_date="2024-06-15")
    etl.run(process_date="2024-06-15")

    result = spark.read.parquet(
        f"{etl_dirs['output']}/customer_summary")
    assert result.count() == 1  # No duplicates
```

---
## Testing Edge Cases

```python
# tests/unit/test_edge_cases.py
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, \
    StringType, DoubleType
from src.transformations.cleaning import (
    remove_duplicates,
    fill_missing_amounts,
)

def test_empty_dataframe(spark, empty_orders):
    """Transformations should handle empty DataFrames."""
    result = remove_duplicates(empty_orders, ["order_id"])
    assert result.count() == 0
    assert result.schema == empty_orders.schema

def test_all_nulls(spark):
    data = [
        Row(id=1, amount=None),
        Row(id=2, amount=None),
    ]
    df = spark.createDataFrame(data)
    result = fill_missing_amounts(df, default=0.0)

    amounts = [r["amount"] for r in result.collect()]
    assert all(a == 0.0 for a in amounts)

def test_single_row(spark):
    data = [Row(id=1, name="Alice")]
    df = spark.createDataFrame(data)
    result = remove_duplicates(df, ["id"])
    assert result.count() == 1

def test_special_characters(spark):
    data = [
        Row(id=1, name="O'Brien"),
        Row(id=2, name='Say "hello"'),
        Row(id=3, name="Line\nBreak"),
        Row(id=4, name="Tab\there"),
        Row(id=5, name=""),
    ]
    df = spark.createDataFrame(data)
    assert df.count() == 5

    # Verify roundtrip through parquet
    import tempfile, os
    path = os.path.join(tempfile.mkdtemp(), "test.parquet")
    df.write.parquet(path)
    reloaded = spark.read.parquet(path)
    assert reloaded.count() == 5

def test_large_values(spark):
    data = [
        Row(id=1, amount=float("inf")),
        Row(id=2, amount=float("-inf")),
        Row(id=3, amount=1e308),
    ]
    df = spark.createDataFrame(data)
    result = df.filter("amount > 0")
    assert result.count() == 2
```

---
## Running Tests with pytest

```bash
# Install dependencies
pip install pytest chispa pyspark

# Run all tests
pytest tests/ -v

# Run only unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_cleaning.py -v

# Run specific test
pytest tests/unit/test_cleaning.py::test_remove_duplicates -v

# Run with coverage
pip install pytest-cov
pytest tests/ -v --cov=src --cov-report=html

# Run with parallel execution (careful with Spark)
pip install pytest-xdist
pytest tests/ -v -n 2  # 2 workers

# Show test durations (find slow tests)
pytest tests/ -v --durations=10

# Stop on first failure
pytest tests/ -v -x
```

---
## pytest Configuration

```python
# pyproject.toml
# [tool.pytest.ini_options]
# testpaths = ["tests"]
# python_files = ["test_*.py"]
# python_functions = ["test_*"]
# addopts = "-v --tb=short --strict-markers"
# markers = [
#     "slow: marks tests as slow (deselect with '-m \"not slow\"')",
#     "integration: marks integration tests",
# ]
# filterwarnings = [
#     "ignore::DeprecationWarning",
#     "ignore::FutureWarning",
# ]

# Usage with markers:
# @pytest.mark.slow
# def test_large_dataset(spark):
#     ...
#
# @pytest.mark.integration
# def test_full_pipeline(spark, etl_dirs):
#     ...
#
# Run excluding slow tests:
#   pytest -m "not slow"
#
# Run only integration tests:
#   pytest -m integration
```

---
## CI/CD Pipeline: GitHub Actions

```yaml
# .github/workflows/ci.yml
name: PySpark CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          java-version: "11"
          distribution: "temurin"

      - name: Cache pip packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ matrix.python-version }}-${{ hashFiles('pyproject.toml') }}

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint with pylint
        run: pylint src/ --fail-under=8.0

      - name: Check formatting with black
        run: black --check src/ tests/

      - name: Type check with mypy
        run: mypy src/ --ignore-missing-imports

      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml

      - name: Run integration tests
        run: pytest tests/integration/ -v -m integration

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

---
## CI Pipeline Visualization

![ci_pipeline_visualization](svg/courses/big_data/advanced-spark-with-python/09_testing_and_ci/ci_pipeline_visualization.svg)

---
## Code Quality: pylint Configuration

```python
# pyproject.toml
# [tool.pylint.master]
# load-plugins = []
# jobs = 2
#
# [tool.pylint.messages_control]
# disable = [
#     "missing-module-docstring",
#     "too-few-public-methods",
#     "import-error",        # PySpark stubs may be missing
# ]
#
# [tool.pylint.format]
# max-line-length = 88     # match black
#
# [tool.pylint.design]
# max-args = 8

# Common pylint issues with PySpark:
# - F.col("name") triggers no-member warnings
# - Dynamic DataFrame columns not recognized
# - Spark SQL strings not validated

# Run pylint
# pylint src/ --fail-under=8.0
# pylint src/transformations/ --disable=C0114
```

---
## Code Quality: mypy with PySpark Stubs

```python
# Install PySpark type stubs
# pip install pyspark-stubs  (for Spark < 3.4)
# Spark 3.4+ includes inline type hints

# pyproject.toml
# [tool.mypy]
# python_version = "3.10"
# warn_return_any = true
# warn_unused_configs = true
# ignore_missing_imports = true
#
# [[tool.mypy.overrides]]
# module = "pyspark.*"
# ignore_missing_imports = true

# Type-annotated transformation:
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from typing import List, Optional

def aggregate_by_columns(
    df: DataFrame,
    group_cols: List[str],
    agg_col: str,
    alias: Optional[str] = None,
) -> DataFrame:
    """Aggregate a column by specified grouping columns."""
    result_alias = alias or f"sum_{agg_col}"
    return (
        df.groupBy(*group_cols)
        .agg(F.sum(agg_col).alias(result_alias))
    )

# Run mypy
# mypy src/ --ignore-missing-imports
```

---
## Code Quality: black Formatting

```python
# pyproject.toml
# [tool.black]
# line-length = 88
# target-version = ["py310"]
# include = '\.pyi?$'

# Before black:
def process_data(spark,input_path,output_path,process_date,max_records=None):
    df=spark.read.parquet(input_path).filter(F.col("date")==process_date)
    if max_records:df=df.limit(max_records)
    df.write.mode("overwrite").parquet(output_path)

# After black:
def process_data(
    spark,
    input_path,
    output_path,
    process_date,
    max_records=None,
):
    df = spark.read.parquet(input_path).filter(
        F.col("date") == process_date
    )
    if max_records:
        df = df.limit(max_records)
    df.write.mode("overwrite").parquet(output_path)

# Run black
# black src/ tests/           # format in place
# black --check src/ tests/   # check only (for CI)
# black --diff src/ tests/    # show diff
```

---
## Full Program: Complete Test Suite

```python
# tests/conftest.py
import pytest
from pyspark.sql import SparkSession, Row
from datetime import date

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("unit-tests")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()

@pytest.fixture
def sample_events(spark):
    return spark.createDataFrame([
        Row(event_id="e1", user_id="u1",
            event_type="click", amount=10.0,
            event_date=date(2024, 6, 15)),
        Row(event_id="e2", user_id="u2",
            event_type="purchase", amount=99.0,
            event_date=date(2024, 6, 15)),
        Row(event_id="e3", user_id="u1",
            event_type="purchase", amount=250.0,
            event_date=date(2024, 6, 16)),
        Row(event_id="e4", user_id="u3",
            event_type="click", amount=5.0,
            event_date=date(2024, 6, 16)),
    ])
```

---
## Full Program: Complete Test Suite (continued)

```python
# tests/unit/test_event_transformations.py
import pytest
from chispa.dataframe_comparer import assert_df_equality
from pyspark.sql import Row, functions as F
from datetime import date

def filter_purchases(df):
    return df.filter(F.col("event_type") == "purchase")

def compute_user_totals(df):
    return (
        df.groupBy("user_id")
        .agg(
            F.sum("amount").alias("total_amount"),
            F.count("*").alias("event_count"),
        )
    )

def test_filter_purchases(spark, sample_events):
    result = filter_purchases(sample_events)
    assert result.count() == 2
    types = [r["event_type"] for r in result.collect()]
    assert all(t == "purchase" for t in types)

def test_filter_purchases_no_matches(spark):
    data = [Row(event_id="e1", user_id="u1",
                event_type="click", amount=10.0,
                event_date=date(2024, 6, 15))]
    df = spark.createDataFrame(data)
    result = filter_purchases(df)
    assert result.count() == 0

def test_compute_user_totals(spark, sample_events):
    result = compute_user_totals(sample_events)
    expected = spark.createDataFrame([
        Row(user_id="u1", total_amount=260.0, event_count=2),
        Row(user_id="u2", total_amount=99.0, event_count=1),
        Row(user_id="u3", total_amount=5.0, event_count=1),
    ])
    assert_df_equality(
        result, expected,
        ignore_row_order=True,
        ignore_nullable=True,
    )

def test_compute_user_totals_single_user(spark):
    data = [
        Row(event_id="e1", user_id="u1",
            event_type="click", amount=10.0,
            event_date=date(2024, 6, 15)),
        Row(event_id="e2", user_id="u1",
            event_type="click", amount=20.0,
            event_date=date(2024, 6, 16)),
    ]
    df = spark.createDataFrame(data)
    result = compute_user_totals(df)

    assert result.count() == 1
    row = result.collect()[0]
    assert row["total_amount"] == 30.0
    assert row["event_count"] == 2
```

---
## Summary: Testing and CI/CD

![summary_testing_and_ci_cd](svg/courses/big_data/advanced-spark-with-python/09_testing_and_ci/summary_testing_and_ci_cd.svg)
