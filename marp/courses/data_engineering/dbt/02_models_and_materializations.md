---
tags:
  - data-and-ai:dbt
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Models and Materialisations

---
## What This Chapter Covers

- Model files
- Materialisations: view, table, incremental, ephemeral
- Configuring materialisations
- Incremental strategies
- Folder structure

---
## Materialisations

![materialisations](svg/courses/data_engineering/dbt/02_models_and_materializations/materializations.svg)

---
## Model Files

- One SQL file per model
- File name = model name (without extension)
- SELECT statement (no INSERT, etc.)
- dbt wraps in CREATE / INSERT

---
## Materialisations

- **view**: SQL view; recomputed on each query
- **table**: full rebuild on dbt run
- **incremental**: append/upsert changed rows
- **ephemeral**: CTE; inlined in dependents

---
## View

```sql
{{ config(materialized='view') }}
SELECT * FROM {{ source('raw', 'users') }}
```

- Cheap to materialise
- Slow to query (always recomputes)
- Default for staging

---
## Table

```sql
{{ config(materialized='table') }}
SELECT ...
```

- Full rebuild every run
- Fast queries
- For: small / medium models

---
## Incremental

```sql
{{ config(materialized='incremental', unique_key='id') }}
SELECT * FROM {{ source('raw', 'events') }}
{% if is_incremental() %}
    WHERE timestamp > (SELECT MAX(timestamp) FROM {{ this }})
{% endif %}
```

- Only process new rows
- For big tables; saves compute

---
## Incremental Strategies

- append: just insert new rows
- merge: upsert by unique_key
- delete+insert: replace partition
- Pick by deduplication needs

---
## Ephemeral

```sql
{{ config(materialized='ephemeral') }}
SELECT ...
```

- Inlined into downstream models as a CTE
- No persistent table
- For: simple intermediate logic

---
## Configuring

- Per-model in the model file
- Or in dbt_project.yml for groups
- Inheritance: dbt_project.yml &#8594; model file
- Cleaner: project-level defaults

---
## Folder Structure

```misc
models/
├── staging/      (views: clean and rename)
├── intermediate/ (ephemeral or views: business logic)
└── marts/        (tables: analytical layer)
```

- Standard pattern
- Each layer narrows / aggregates

---
## Naming Conventions

- stg_: staging
- int_: intermediate
- fct_: fact
- dim_: dimension
- Consistent across team

---
## ref()

- Reference another model: `{{ ref('stg_users') }}`
- dbt builds dependency graph
- Order of execution automatic

---
## Schema

- `{{ this }}`: current model's table reference
- Includes schema and database
- Useful in incremental logic

---
## Common Materialisation Mistakes

- Table when view would do (wasteful)
- View on huge tables that get queried often (slow)
- Incremental without considering late-arriving data
- Ephemeral that should be a real table (queries duplicate work)
- Same materialisation everywhere (one size doesn't fit all)
