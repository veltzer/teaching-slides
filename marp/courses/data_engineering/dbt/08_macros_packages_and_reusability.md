---
tags:
  - data-and-ai:dbt
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Macros, Packages, and Reusability

---
## What This Chapter Covers

- Macros
- Common patterns
- Packages
- dbt_utils
- Custom packages

---
## Package Ecosystem

![package_ecosystem](svg/courses/data_engineering/dbt/08_macros_packages_and_reusability/package_ecosystem.svg)

---
## Macros

- Reusable Jinja code
- Like functions
- Live in macros/

---
## Sample Macro

```jinja
-- macros/clean_email.sql
{% macro clean_email(col) %}
    LOWER(TRIM({{ col }}))
{% endmacro %}
```

- Use in models: `SELECT {{ clean_email('email') }}`

---
## Macros Generating SQL

```jinja
{% macro pivot_by(col, values) %}
{% for v in values %}
    SUM(CASE WHEN {{ col }} = '{{ v }}' THEN 1 ELSE 0 END) AS {{ v }}_count
    {%- if not loop.last -%},{% endif %}
{% endfor %}
{% endmacro %}
```

- Build repetitive SQL
- DRY across models

---
## Materialisation Macros

- Custom materialisations
- For non-standard table types
- Rarely needed

---
## Packages

- Reusable dbt code (macros + models)
- packages.yml: declare dependencies
- `dbt deps` installs

---
## Sample packages.yml

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.1
```

---
## dbt_utils

- Most popular package
- Macros: surrogate_key, pivot, date_spine, etc.
- Install; use in your models
- Standard

---
## dbt_expectations

- Inspired by Great Expectations
- More test types
- Distribution checks, type checks
- Good for: data quality

---
## fivetran utils

- Helpers for Fivetran-loaded data
- Source models for popular SaaS apps
- Saves boilerplate

---
## Internal Packages

- Your own reusable code
- Across multiple dbt projects
- Versioned, distributed
- For: monorepos with many projects

---
## Standardising Across Teams

- Shared macros for common transformations
- One source of truth
- Update once; benefit everywhere

---
## adapter Dispatch

```jinja
{% macro days_between(start, end) %}
    {{ adapter.dispatch('days_between')(start, end) }}
{% endmacro %}

{% macro default__days_between(start, end) %}
    DATEDIFF(day, {{ start }}, {{ end }})
{% endmacro %}

{% macro snowflake__days_between(start, end) %}
    DATEDIFF('day', {{ start }}, {{ end }})
{% endmacro %}
```

- Per-warehouse implementations
- Code portable across DBs

---
## When To Macro

- Same SQL pattern in 3+ models
- Non-trivial logic
- Cross-team reusability

---
## When Not To

- One-off code
- Simple expressions (just inline)
- Macros that obscure simple SQL

---
## Common Macro Mistakes

- Over-abstraction (macro hides simple SQL)
- Macros without tests (broken silently)
- Reinventing dbt_utils
- Macros with side effects
- Not version-pinning packages

---
## Macro Patterns

![macro_examples](svg/courses/data_engineering/dbt/08_macros_packages_and_reusability/macro_examples.svg)
