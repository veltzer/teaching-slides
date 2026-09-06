---
tags:
  - data-and-ai:dbt
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Snapshots and Slowly Changing Dimensions

---

## SCD Types

![scd_types](svg/courses/data_engineering/dbt/07_snapshots_and_slowly_changing_dimensions/scd_types.svg)

---

## What This Chapter Covers

- What snapshots are
- Type 2 SCD
- dbt snapshot strategies
- When to use
- Patterns

---

## What Snapshots Are

- Track changes to a source over time
- Append historical versions
- For: "what was the price yesterday?"
- Type 2 Slowly Changing Dimension

---

## Why

- Source systems often overwrite
- "Customer changed address; old address gone"
- Snapshots: keep the history

---

## Sample Snapshot

```sql
{% snapshot orders_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='id',
        strategy='timestamp',
        updated_at='updated_at'
    )
}}

SELECT * FROM {{ source('raw', 'orders') }}
{% endsnapshot %}
```

- One table per snapshot
- dbt manages valid_from / valid_to columns

---

## Strategies

- **timestamp**: row changed if `updated_at` is newer
- **check**: row changed if any of N columns changed
- Pick by source's nature

---

## Check Strategy

```sql
{{
    config(
        strategy='check',
        check_cols=['name', 'address', 'phone']
    )
}}
```

- Compares each column
- Useful when no `updated_at`

---

## Snapshot Output

- Original columns
- `dbt_valid_from`, `dbt_valid_to`
- `dbt_updated_at`
- `dbt_scd_id`

---

## Querying

- Latest version: `WHERE dbt_valid_to IS NULL`
- As-of date: `WHERE date BETWEEN valid_from AND valid_to`

---

## Running

```bash
dbt snapshot
```

- Run on schedule
- Captures new versions of changed rows
- Append-only

---

## When To Use

- Source overwrites; you need history
- Reporting "as of last quarter"
- Audit trail
- Type 2 SCD requirement

---

## When Not To

- Source already has versioning (event log)
- You don't need history
- Source data is immutable

---

## Performance

- Snapshot tables grow
- Only changes captured
- Periodic cleanup if too big

---

## Combine With Models

- Snapshot in snapshots/
- Models reference: `{{ ref('orders_snapshot') }}`
- Fact tables often use snapshots

---

## Common Snapshot Mistakes

- Wrong unique_key (creates duplicates)
- Using timestamp when no reliable updated_at exists
- Capturing too many columns with check (too sensitive)
- Snapshots growing unbounded; no archiving
- Forgetting to schedule snapshot runs
