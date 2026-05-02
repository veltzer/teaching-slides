---
tags:
  - data-and-ai:dbt
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Introduction to dbt and the Modern Data Stack

---
## What This Chapter Covers

- What dbt is
- The modern data stack
- ELT vs ETL
- Core dbt features
- Use cases

---
## What dbt Is

- "Data Build Tool"
- Transform data within your warehouse
- SQL + Jinja templating
- Version-controlled transformations
- Open source + dbt Cloud

---
## ELT Position

![elt_position](svg/courses/data_engineering/dbt/01_introduction_to_dbt_and_the_modern_data_stack/elt_position.svg)

---
## Modern Data Stack

- Source &#8594; Loader (Fivetran, Airbyte) &#8594; Warehouse (Snowflake, BigQuery)
- &#8594; dbt transforms &#8594; BI tools (Looker, Tableau)
- Each best-of-breed
- Replaced monolithic ETL

---
## ELT vs ETL

- ETL: transform before load (legacy)
- ELT: load raw; transform in warehouse (modern)
- Warehouse compute is cheap
- dbt is the T in ELT

---
## Core Features

- Models: SQL transformations
- Tests: data quality checks
- Documentation: auto-generated
- Lineage: dependency graph
- Reusable macros

---
## Why dbt

- SQL-first; analysts can use it
- Git-friendly
- Tests built in
- Lineage visualisation
- Standard in modern stacks

---
## dbt Core vs dbt Cloud

- Core: open-source CLI
- Cloud: hosted; IDE, scheduling, RBAC
- Most teams: Core + own scheduler
- Cloud: easier; pricier

---
## Supported Warehouses

- Snowflake, BigQuery, Redshift
- Databricks, Postgres
- Many more via adapters
- Same dbt code; different SQL backends

---
## A Sample Model

```sql
-- models/staging/stg_orders.sql
SELECT
    id,
    customer_id,
    total::numeric AS total_usd,
    created_at::date AS order_date
FROM {{ source('raw', 'orders') }}
WHERE total > 0
```

---
## ref() and source()

- `{{ source(...) }}`: raw data table
- `{{ ref('model_name') }}`: another model
- dbt resolves dependencies
- Build order automatic

---
## Materialisations

- view (default for staging)
- table (full rebuild)
- incremental (append only changed rows)
- ephemeral (CTE; not materialised)
- Pick by use case

---
## When To Use dbt

- Anywhere you transform data in a warehouse
- Replaces SQL scripts
- Standard for analytics engineering teams

---
## When Not To

- Streaming transformations
- Operational data (use ETL with Airflow)
- One-off ad-hoc queries

---
## Common Misconceptions

- "dbt loads data" — no, it transforms
- "dbt requires dbt Cloud" — Core is free
- "dbt is for data engineers" — for analysts too
- "dbt replaces Airflow" — they complement (Airflow runs dbt)

---
## What's Next

- Models, materialisations
- Jinja templating
- Tests, documentation
- Sources, seeds, snapshots
- Macros
- Production deployment
