---
tags:
  - data-and-ai:dbt
  - practices:testing
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Testing and Data Quality

---
## Test Types

![test_types](svg/courses/data_engineering/dbt/04_testing_and_data_quality/test_types.svg)

---
## What This Chapter Covers

- dbt tests
- Generic tests
- Custom tests
- Test severity
- Data quality patterns
- Production testing

---
## Why Test

- Data is wrong silently
- Stakeholders trust your numbers
- Tests = early warning
- Standard part of dbt

---
## Generic Tests

- Built-in: not_null, unique, accepted_values, relationships
- Configured in YAML

---
## Sample Tests

```yaml
models:
  - name: stg_users
    columns:
      - name: id
        tests:
          - not_null
          - unique
      - name: country
        tests:
          - accepted_values:
              values: ['US', 'CA', 'UK']
```

---
## Relationships

```yaml
- name: order_id
  tests:
    - relationships:
        to: ref('orders')
        field: id
```

- Foreign key test
- Catches orphan rows

---
## Singular Tests

- A custom SELECT in tests/ folder
- Returns rows for failures
- More flexible than generic

---
## Singular Test Example

```sql
-- tests/total_must_be_positive.sql
SELECT * FROM {{ ref('orders') }} WHERE total < 0
```

- Returns rows where condition violated
- Test fails if rows returned

---
## Custom Generic Tests

- Write reusable tests as macros
- "All values in column X must match regex"
- Test = macro returning a SELECT

---
## Test Severity

- error (default): fails the run
- warn: log; continue
- Configure per test
- Useful: warn for new tests, error after stable

---
## Running Tests

- `dbt test`: all tests
- `dbt test --select model_name`: specific
- Run after `dbt run`
- Standard CI step

---
## Schema Yml

- Tests live in YAML files alongside models
- `schema.yml` or `*_models.yml`
- Co-located with model

---
## dbt Source Tests

- Test source data freshness
- "If raw.orders is more than 6 hours stale, alert"
- Catches upstream pipeline issues

---
## Data Quality Patterns

- not_null on all primary keys
- unique on natural keys
- accepted_values on enums
- relationships on foreign keys
- Custom: business rules

---
## Custom Quality Tests

- Volume: row count within expected range
- Distribution: percentiles match historical
- Anomaly: sudden spikes
- Tools: dbt-expectations package

---
## Production Testing

- Run tests after every dbt run
- Alert on failures
- Block downstream consumers (DAG dependency)
- Trust without tests is misplaced

---
## Common Testing Mistakes

- Tests as warnings only (never act)
- Only generic tests; no business logic tests
- Tests that flake (timezone, etc.)
- Many warnings; nobody reads them
- Adding tests after data has been wrong for months

---
## Test Severity and Configuration

![test_severity](svg/courses/data_engineering/dbt/04_testing_and_data_quality/test_severity.svg)
