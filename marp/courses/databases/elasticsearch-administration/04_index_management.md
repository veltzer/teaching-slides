---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# Index Management

---
## What This Chapter Covers

- Index creation and configuration
- Mappings and field types
- Dynamic vs explicit mapping
- Index settings and analysis
- Aliases and data streams
- Index templates and component templates
- Rollover and shrink operations
- Force merge and refresh

---
## Creating an Index

- Create an index with settings and mappings in one request
- Choose primary shards at creation; replicas can change later

```bash
PUT products
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  }
}
```

---
## Inspecting an Index

- View settings, mappings, and stats with the REST API

```bash
GET products
GET products/_settings
GET products/_mapping
GET products/_stats
```

---
## Mappings Overview

- A mapping defines the fields in an index and their types
- Controls how fields are stored, indexed, and analyzed
- Field types cannot be changed once data is indexed
- Plan mappings carefully; reindex to change types
- Mappings can be extended by adding new fields

---
## Core Field Types

- text: full-text, analyzed into terms for search
- keyword: exact-value strings for filtering, sorting, aggregation
- numeric: long, integer, short, byte, double, float, scaled_float
- date: dates with configurable formats
- boolean: true/false values
- object / nested: structured and array-of-object data

---
## text vs keyword

- text is analyzed: tokenized and lowercased for full-text search
- keyword is not analyzed: stored as a single exact term
- Use text for search-as-you-type and relevance matching
- Use keyword for exact filters, sorting, and aggregations
- Strings are often mapped as both via multi-fields

```json
"city": { "type": "text", "fields": { "raw": { "type": "keyword" } } }
```

---
## Object and Nested Types

- object: JSON objects flattened into dotted field paths
- Arrays of objects lose per-object relationships when flattened
- nested: indexes each object independently to preserve relationships
- Use nested when you must match conditions within the same sub-object
- Nested queries are more expensive than object queries

```json
"tags": { "type": "nested" }
```

---
## Explicit Mapping

- Define field types up front for predictable behavior
- Recommended for production indices

```bash
PUT products
{
  "mappings": {
    "properties": {
      "name":   { "type": "text" },
      "sku":    { "type": "keyword" },
      "price":  { "type": "scaled_float", "scaling_factor": 100 },
      "created":{ "type": "date" }
    }
  }
}
```

---
## Dynamic Mapping

- Elasticsearch can infer field types from incoming documents
- Convenient for prototyping and unknown schemas
- Risk: type guesses and field explosion in production
- Control behavior with `dynamic`: true, false, or strict
- `strict` rejects documents with unmapped fields

```json
"mappings": { "dynamic": "strict", "properties": { } }
```

---
## Adding Fields to a Mapping

- New fields can be added to an existing mapping
- Existing field types cannot be modified in place

```bash
PUT products/_mapping
{
  "properties": {
    "in_stock": { "type": "boolean" }
  }
}
```

---
## Index Settings: Shards and Replicas

- `number_of_shards` is fixed at creation time
- `number_of_replicas` is dynamic and can change anytime
- More primaries increase write/parallelism but add overhead
- More replicas increase read throughput and resilience

```bash
PUT products/_settings
{ "index.number_of_replicas": 2 }
```

---
## Analysis: Analyzers and Tokenizers

- An analyzer turns text into searchable terms
- Composed of character filters, a tokenizer, and token filters
- Tokenizer splits text into tokens (e.g. standard, whitespace)
- Token filters transform tokens (lowercase, stop, stemming)
- Custom analyzers are defined in index settings

---
## Defining a Custom Analyzer

- Combine a tokenizer with token filters in settings

```bash
PUT articles
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_en": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [ "lowercase", "stop", "porter_stem" ]
        }
      }
    }
  }
}
```

---
## Testing an Analyzer

- Use the _analyze API to see produced tokens

```bash
POST articles/_analyze
{
  "analyzer": "my_en",
  "text": "The Quick Brown Foxes"
}
```

---
## Aliases

- An alias is a pointer to one or more indices
- Provides a stable name while the underlying index changes
- Enables zero-downtime reindex and atomic index swaps
- Can carry filters and routing

```bash
POST _aliases
{
  "actions": [
    { "remove": { "index": "products_v1", "alias": "products" } },
    { "add":    { "index": "products_v2", "alias": "products" } }
  ]
}
```

---
## Data Streams

- Append-only abstraction for time-series data (logs, metrics)
- Backed by a sequence of hidden backing indices
- Writes go to the current write index; rollover creates new ones
- Require a matching index template with data stream enabled
- Documents must include a `@timestamp` field

```bash
PUT _data_stream/logs-app-default
```

---
## Index Templates

- Templates apply settings and mappings to new matching indices
- Match indices by name pattern via `index_patterns`
- Composable templates can reference component templates

```bash
PUT _index_template/logs-template
{
  "index_patterns": [ "logs-*" ],
  "data_stream": { },
  "composed_of": [ "logs-settings", "logs-mappings" ]
}
```

---
## Component Templates

- Reusable building blocks of settings, mappings, or aliases
- Composed together by index templates with `composed_of`
- Promote consistency and reuse across many indices

```bash
PUT _component_template/logs-settings
{
  "template": {
    "settings": { "number_of_shards": 1, "number_of_replicas": 1 }
  }
}
```

---
## Rollover

- Rolls writing over to a new index when conditions are met
- Common conditions: max age, max docs, max primary size
- Data streams roll over automatically; aliases roll over via API
- Keeps individual indices/shards at a manageable size

```bash
POST logs-write/_rollover
{
  "conditions": { "max_age": "7d", "max_primary_shard_size": "50gb" }
}
```

---
## Shrink

- Reduces the number of primary shards of an index
- Useful after rollover to consolidate small shards
- Source index must be read-only and allocated to one node
- Target shard count must divide the source shard count

```bash
PUT logs-2026.05/_settings
{ "index.blocks.write": true }

POST logs-2026.05/_shrink/logs-2026.05-shrunk
```

---
## Force Merge

- Merges Lucene segments to reduce their count
- Reclaims space from deleted documents
- Run only on read-only / no-longer-written indices
- Expensive in I/O; schedule during low-traffic windows

```bash
POST logs-2026.05/_forcemerge?max_num_segments=1
```

---
## Refresh

- Refresh makes newly indexed documents searchable
- Default refresh interval is 1 second per index
- Increase the interval for bulk loads to boost throughput
- Manual refresh forces immediate visibility (use sparingly)

```bash
PUT logs/_settings
{ "index.refresh_interval": "30s" }

POST logs/_refresh
```

---
## Index Management Best Practices

- Use explicit mappings for production indices
- Use templates and component templates for consistency
- Use data streams for time-series data
- Roll over to keep shards in the 10–50 GB range
- Force merge and set read-only on completed indices
- Reindex behind an alias for zero-downtime mapping changes
