---
tags:
  - data-and-ai:dbt
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Sources and Seeds

---
## What This Chapter Covers

- Sources: raw data definitions
- Source freshness
- Seeds: CSV data
- When to use each
- Patterns

---
## Sources

- Declared raw tables
- Outside of dbt's control (loaded by Fivetran, Airbyte, etc.)
- Reference: `{{ source('group', 'table') }}`
- Documentation lives here

---
## Defining Sources

```yaml
sources:
  - name: raw
    database: my_db
    schema: raw
    tables:
      - name: orders
      - name: customers
```

---
## Source Freshness

```yaml
sources:
  - name: raw
    tables:
      - name: orders
        loaded_at_field: ingested_at
        freshness:
          warn_after: { count: 6, period: hour }
          error_after: { count: 24, period: hour }
```

- Test that source data is recent
- Catches upstream pipeline failures

---
## Running Freshness Checks

```bash
dbt source freshness
```

- Run before or alongside dbt run
- Alert on failures

---
## Seeds

- CSV files committed to repo
- Loaded as tables
- For: small reference data, mappings

---
## Sample Seed

```csv
# seeds/country_mapping.csv
country_code,country_name
US,United States
CA,Canada
UK,United Kingdom
```

```bash
dbt seed
```

- Loads into warehouse
- Reference: `{{ ref('country_mapping') }}`

---
## When To Use Seeds

- Mapping tables (small)
- Lookup tables
- Test fixtures
- "Static" reference data

---
## When Not To

- Large datasets (use sources instead)
- Frequently changing (sources or external loader)
- Sensitive data (don't put in git)

---
## Seed Configuration

```yaml
seeds:
  my_project:
    +schema: reference
    country_mapping:
      +column_types:
        country_code: varchar(2)
```

- Per-seed config

---
## External Tables

- Sources can be external tables (S3, GCS)
- Snowflake external tables, BigQuery external
- Useful for: data lakes, infrequent access

---
## Source Patterns

- One source group per upstream system
- "fivetran_postgres", "fivetran_salesforce"
- Document each table
- Test freshness on critical ones

---
## Layered Approach

- Sources &#8594; staging models (clean) &#8594; intermediate &#8594; marts
- Each layer has clearer expectations
- Standard dbt pattern

---
## Common Source/Seed Mistakes

- No source documentation
- Source freshness configured but not run
- Big seeds (slow to load every run)
- Using seeds for anything non-trivial
- Hardcoded source paths in models (use source())
