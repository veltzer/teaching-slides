---
tags:
  - databases:elasticsearch
  - databases:mappings
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Data Modeling and Mappings

---
## What This Chapter Covers

- Field types
- Text vs keyword
- Date types
- Nested vs object
- Multi-fields
- Dynamic mapping
- Best practices

---
## Field Types

- Text, keyword
- Numeric: long, integer, short, byte, double, float
- Date: date, date_nanos
- Boolean
- Binary
- Range, IP, geo

---
## Text Vs Keyword

- **text**: analysed; broken into tokens; for full-text search
- **keyword**: stored as-is; for exact match, sort, aggregation
- Use both: multi-field
- Common: name as text + name.keyword

---
## Multi-Field

```json
"name": {
    "type": "text",
    "fields": {
        "keyword": { "type": "keyword" }
    }
}
```

- Search: name (analysed)
- Sort / aggregate: name.keyword (raw)

---
## text vs keyword

![text_vs_keyword](svg/courses/databases/elasticsearch-for-developers/03_data_modeling_and_mappings/text_vs_keyword.svg)

---
## Date Type

- ISO 8601 strings
- Or Unix timestamps
- Range queries work; date math
- Time zones: store UTC; render in UI

---
## Nested

- Array of objects
- Preserves relationship between fields within an object
- Slower; richer queries
- Use when sub-objects need internal queries

---
## Object

- Default for nested objects
- Flattens; loses inner-object relations
- "Faster but query-limited"
- Most apps: object is fine

---
## Dynamic Mapping

- ES auto-detects field types on first ingest
- Convenience; risk
- Wrong inferences: dates as text, ints as keyword
- Define explicitly for important fields

---
## Strict Mapping

```json
"dynamic": "strict"
```

- Reject unknown fields
- Catches typos / drifted data
- Recommended for production

---
## Index Settings

- number_of_shards
- number_of_replicas
- refresh_interval
- analysis (analyzers, tokenisers, filters)

---
## Analyzers

- How text is tokenised
- Standard, whitespace, language-specific
- Custom: combine tokeniser + filters
- Shape full-text behaviour

---
## Custom Analyzer

```json
{
  "settings": { "analysis": {
    "analyzer": {
      "my": {
        "tokenizer": "standard",
        "filter": ["lowercase", "asciifolding", "stop"]
      }
    }
  }}
}
```

---
## Index Templates

- Apply mapping to many indexes
- "All indexes named logs-* get this mapping"
- Standard for time-based indexes

---
## Reindexing

- Mappings can't change in-place
- Create new index; copy data; alias swap
- Use Reindex API or Logstash
- Plan for it; not "edit the mapping"

---
## Common Mapping Mistakes

- Letting ES auto-map text as keyword (or vice versa)
- Using nested when object would do (slow queries)
- Same name field with different types across indexes
- No multi-field; can't sort or aggregate text fields
- Reindexing as a manual emergency rather than a planned process
