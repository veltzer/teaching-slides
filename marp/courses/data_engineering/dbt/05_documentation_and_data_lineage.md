---
tags:
  - data-and-ai:dbt
  - practices:documentation
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Documentation and Data Lineage

---
## Lineage Graph

![lineage_graph](svg/courses/data_engineering/dbt/05_documentation_and_data_lineage/lineage_graph.svg)

---
## What This Chapter Covers

- Model and column descriptions
- Doc blocks
- dbt docs serve
- Lineage graph
- Exposures
- Sharing with stakeholders

---
## Why Document

- Analysts need to know what columns mean
- Stakeholders need to understand where numbers come from
- New hires need a map
- Documentation drift = trust loss

---
## Documentation Artifacts

![doc_artifacts](svg/courses/data_engineering/dbt/05_documentation_and_data_lineage/doc_artifacts.svg)

---
## Model Descriptions

```yaml
models:
  - name: fct_orders
    description: "One row per completed order. Partitioned by order_date."
    columns:
      - name: order_id
        description: "Primary key. Source: raw.orders.id"
```

- YAML alongside model file

---
## Doc Blocks

```jinja
{% docs order_status %}

Status of the order. Possible values:
- pending: order created
- shipped: tracking number assigned
- delivered: confirmed receipt

{% enddocs %}
```

- Defined in `*.md` files
- Reusable across models
- For long descriptions

---
## Referencing Doc Blocks

```yaml
- name: status
  description: '{{ doc("order_status") }}'
```

- Multiple models can reference

---
## dbt docs

```bash
dbt docs generate
dbt docs serve
```

- Generates HTML docs site
- Browse models, columns, lineage
- Host at /docs URL

---
## Lineage Graph

- Visualises model dependencies
- Click to navigate
- See upstreams, downstreams
- Built-in to dbt docs

---
## Exposures

```yaml
exposures:
  - name: weekly_sales_dashboard
    type: dashboard
    description: "Used by sales team weekly review"
    depends_on:
      - ref('fct_orders')
    owner:
      email: sales@example.com
```

- Document downstream consumers
- BI dashboards, ML models, reports
- "Where does this data go?"

---
## Sources

```yaml
sources:
  - name: raw
    description: "Raw data from production via Fivetran"
    tables:
      - name: orders
        description: "Orders from the e-commerce app"
        columns:
          - name: id
            description: "..."
```

- Document raw data too
- The whole graph is documented

---
## Sharing With Stakeholders

- Host dbt docs
- Or: Confluence, Notion summaries
- Stakeholders want: which dashboard? Where's the data from?
- Documentation answers both

---
## Catalogue Tools

- Atlan, Alation, DataHub
- Pull dbt metadata
- Richer than dbt docs alone
- For: many teams, many sources

---
## Documentation As Code

- All docs in YAML / Markdown
- Versioned with models
- Reviewed in PRs
- No drift

---
## Search

- dbt docs has basic search
- For more: Atlan, Datafold
- Find: "where is revenue calculated?"

---
## Common Documentation Mistakes

- Empty descriptions (auto-generated stubs)
- Stale docs after schema changes
- Documenting what (column type) instead of why
- No exposures (downstream invisible)
- Documentation only in Confluence; not in code
