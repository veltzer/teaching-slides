---
tags:
  - data-and-ai:dbt
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Jinja and Advanced Transformations

---
## What This Chapter Covers

- Jinja basics
- Templating in models
- Variables
- Loops
- Conditionals
- Common patterns

---
## Jinja In dbt

- Templating layer over SQL
- `{{ ... }}`: expression
- `{% ... %}`: statement
- Compiles to plain SQL

---
## Jinja, ref, Macros

![jinja_macros](svg/courses/data_engineering/dbt/03_jinja_and_advanced_transformations/jinja_macros.svg)

---
## Variables

```sql
{% set ages = [18, 25, 35, 50] %}
SELECT
{% for age in ages %}
    SUM(CASE WHEN age >= {{ age }} THEN 1 ELSE 0 END) AS users_{{ age }}{% if not loop.last %},{% endif %}
{% endfor %}
FROM users
```

---
## ref() And source()

- `{{ ref('model') }}`: reference another model
- `{{ source('group', 'table') }}`: raw source
- dbt resolves at compile time

---
## Conditionals

```sql
SELECT
    name,
    {% if target.name == 'prod' %}
        email AS email
    {% else %}
        '***' AS email
    {% endif %}
FROM users
```

- Different SQL per environment

---
## Loops

```sql
SELECT
    {% for col in ['a', 'b', 'c'] %}
        SUM(CASE WHEN type = '{{ col }}' THEN 1 END) AS {{ col }}_count{% if not loop.last %},{% endif %}
    {% endfor %}
FROM events
```

- Generate repetitive SQL

---
## Built-In Variables

- `{{ target.name }}`: env name (dev, prod)
- `{{ run_started_at }}`: timestamp
- `{{ this }}`: current model's reference
- `{{ env_var('VAR') }}`: env variable

---
## var()

- Custom variables in dbt_project.yml
- `{{ var('my_var') }}`
- Per-environment overrides

---
## Macros

- Reusable Jinja code
- Like functions
- Defined in macros/ folder
- Covered in detail later

---
## Compile vs Run

- `dbt compile`: render Jinja; produce SQL
- `dbt run`: execute SQL
- Always check compiled SQL when debugging

---
## Pre-Hooks / Post-Hooks

- Run before / after a model
- "GRANT SELECT ON {{ this }} TO analyst"
- Common for: permissions, auditing

---
## adapter Macros

- `{{ adapter.dispatch(...) }}`: warehouse-specific impl
- Write once; works on Snowflake, BigQuery, etc.

---
## dbt_utils

- Popular package: macros for common patterns
- `dbt_utils.surrogate_key`, `dbt_utils.pivot`, etc.
- Install via packages.yml
- Standard

---
## Examples Of Useful Macros

- Generate dim/fact joins
- Pivot tables
- Date spines
- All in dbt_utils or fivetran-utils

---
## Common Jinja Mistakes

- Heavy logic in Jinja (hard to read)
- Forgetting `loop.last` (trailing commas)
- Variables that should be config
- Compile errors hidden in runtime errors
- Treating Jinja as a programming language

---
## Jinja Features in dbt

![jinja_features](svg/courses/data_engineering/dbt/03_jinja_and_advanced_transformations/jinja_features.svg)
