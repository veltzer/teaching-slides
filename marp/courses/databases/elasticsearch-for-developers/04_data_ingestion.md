---
tags:
  - tools:elasticsearch
  - data-and-ai:search
  - concepts:data-pipelines
level: intermediate
category: database
audience:
  - audiences:developers

---
# Data Ingestion and Pipelines

## Getting Data Into Elasticsearch

---

## Ingestion Overview

![ingestion_overview](svg/courses/databases/elasticsearch-for-developers/04_data_ingestion/ingestion_overview.svg)

---

## Bulk API Basics

```json
POST /_bulk
{"index": {"_index": "products"}}
{"name": "Product A", "price": 29.99}
{"index": {"_index": "products"}}
{"name": "Product B", "price": 39.99}
```

NDJSON format - newline delimited

---

## Bulk Actions

1. **index**: Insert or replace
1. **create**: Insert if not exists
1. **update**: Partial update
1. **delete**: Remove document

---

## Bulk Index Example

```json
POST /products/_bulk
{"index": {"_id": "1"}}
{"name": "Laptop", "price": 999}
{"index": {"_id": "2"}}
{"name": "Mouse", "price": 29}
{"index": {"_id": "3"}}
{"name": "Keyboard", "price": 79}
```

---

## Bulk Update Example

```json
POST /_bulk
{"update": {"_index": "products", "_id": "1"}}
{"doc": {"price": 899}, "doc_as_upsert": true}
{"update": {"_index": "products", "_id": "2"}}
{"script": {"source": "ctx._source.price *= 0.9"}}
```

---

## Bulk Delete Example

```json
POST /_bulk
{"delete": {"_index": "products", "_id": "old-1"}}
{"delete": {"_index": "products", "_id": "old-2"}}
{"delete": {"_index": "products", "_id": "old-3"}}
```

No document body for deletes

---

## Optimal Batch Size

![optimal_batch_size](svg/courses/databases/elasticsearch-for-developers/04_data_ingestion/optimal_batch_size.svg)

---

## Bulk Performance Tips

1. Batch size: 5-15 MB
1. Document count: 1000-5000 per batch
1. Use compression when possible
1. Monitor rejection rates
1. Implement retry logic

---

## Error Handling

```json
{
  "took": 30,
  "errors": true,
  "items": [{
    "index": {
      "_index": "products",
      "_id": "1",
      "status": 200
    }
  }, {
    "index": {
      "_index": "products",
      "_id": "2",
      "status": 400,
      "error": {
        "type": "mapper_parsing_exception"
      }
    }
  }]
}
```

---

## Bulk Retry Strategy

```python
def bulk_with_retry(actions, max_retries=3):
    for attempt in range(max_retries):
        response = es.bulk(actions)
        if not response['errors']:
            return response
        # Extract failed actions
        actions = get_failed_actions(response)
        time.sleep(2 ** attempt)
```

---

## Ingest Pipelines

```json
PUT /_ingest/pipeline/product_pipeline
{
  "description": "Process product data",
  "processors": [{
    "set": {
      "field": "timestamp",
      "value": "{{_ingest.timestamp}}"
    }
  }]
}
```

---

## Pipeline Architecture

![pipeline_architecture](svg/courses/databases/elasticsearch-for-developers/04_data_ingestion/pipeline_architecture.svg)

---

## Common Processors

1. **set**: Add/update fields
1. **remove**: Delete fields
1. **rename**: Rename fields
1. **convert**: Change types
1. **date**: Parse dates

---

## Set Processor

```json
{
  "set": {
    "field": "category",
    "value": "electronics",
    "override": false
  }
}
```

Add or update field values

---

## Remove Processor

```json
{
  "remove": {
    "field": ["temp_field", "debug_info"],
    "ignore_missing": true
  }
}
```

Clean up unwanted fields

---

## Rename Processor

```json
{
  "rename": {
    "field": "product_name",
    "target_field": "name",
    "ignore_missing": false
  }
}
```

Standardize field names

---

## Convert Processor

```json
{
  "convert": {
    "field": "price",
    "type": "float",
    "ignore_missing": false
  }
}
```

Types: `integer`, `long`, `float`, `double`, `string`, `boolean`

---

## Date Processor

```json
{
  "date": {
    "field": "date_string",
    "target_field": "@timestamp",
    "formats": ["dd/MM/yyyy", "ISO8601"],
    "timezone": "UTC"
  }
}
```

Parse various date formats

---

## Grok Processor

```json
{
  "grok": {
    "field": "message",
    "patterns": [
      "%{IP:client_ip} - - \\[%{HTTPDATE:timestamp}\\] \"%{WORD:method} %{URIPATHPARAM:request}\""
    ]
  }
}
```

Parse unstructured text

---

## Dissect Processor

```json
{
  "dissect": {
    "field": "message",
    "pattern": "%{client_ip} - - [%{timestamp}] \"%{method} %{request}\""
  }
}
```

Faster than Grok for fixed formats

---

## Script Processor

```json
{
  "script": {
    "lang": "painless",
    "source": """
      ctx.total = ctx.price * ctx.quantity;
      ctx.discounted = ctx.total * 0.9;
    """
  }
}
```

Custom transformations

---

## Enrich Processor

```json
{
  "enrich": {
    "policy_name": "user_lookup",
    "field": "user_id",
    "target_field": "user",
    "max_matches": "1"
  }
}
```

Join with reference data

---

## Creating Enrich Policy

```json
PUT /_enrich/policy/user_lookup
{
  "match": {
    "indices": "users",
    "match_field": "user_id",
    "enrich_fields": ["name", "email", "department"]
  }
}

POST /_enrich/policy/user_lookup/_execute
```

---

## Conditional Processing

```json
{
  "set": {
    "field": "discount_tier",
    "value": "gold",
    "if": "ctx.total_purchases > 1000"
  }
}
```

Apply processors conditionally

---

## Pipeline Error Handling

```json
{
  "date": {
    "field": "date_field",
    "formats": ["ISO8601"],
    "on_failure": [{
      "set": {
        "field": "date_parse_error",
        "value": "true"
      }
    }]
  }
}
```

---

## Testing Pipelines

```json
POST /_ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [{
      "lowercase": {
        "field": "name"
      }
    }]
  },
  "docs": [{
    "_source": {
      "name": "PRODUCT NAME"
    }
  }]
}
```

---

## CSV Data Ingestion

```json
{
  "csv": {
    "field": "csv_line",
    "target_fields": ["name", "price", "category"],
    "separator": ",",
    "quote": "\"",
    "ignore_missing": false
  }
}
```

---

## JSON Parsing

```json
{
  "json": {
    "field": "json_string",
    "target_field": "parsed_data",
    "add_to_root": true
  }
}
```

Parse JSON strings in fields

---

## Log File Processing

```json
PUT /_ingest/pipeline/apache_logs
{
  "processors": [{
    "grok": {
      "field": "message",
      "patterns": ["%{COMBINEDAPACHELOG}"]
    }
  }, {
    "date": {
      "field": "timestamp",
      "formats": ["dd/MMM/yyyy:HH:mm:ss Z"]
    }
  }]
}
```

---

## Update Strategies

1. **Full replace**: PUT with complete document
1. **Partial update**: POST with `_update`
1. **Scripted update**: Dynamic modifications
1. **Update by query**: Bulk updates

---

## Update by Query

```json
POST /products/_update_by_query
{
  "script": {
    "source": "ctx._source.price *= params.factor",
    "params": {
      "factor": 1.1
    }
  },
  "query": {
    "term": {
      "category": "electronics"
    }
  }
}
```

---

## Optimistic Concurrency

```json
POST /products/_update/1?if_seq_no=5&if_primary_term=1
{
  "doc": {
    "stock": 45
  }
}
```

Prevent lost updates

---

## Version Conflicts

```json
POST /products/_update_by_query?conflicts=proceed
{
  "query": {
    "match_all": {}
  }
}
```

Options: `abort` (default) or `proceed`

---

## Performance Monitoring

```json
GET /_nodes/stats/ingest

GET /_stats/indexing
```

Track ingestion metrics

---

## Refresh Control

```json
POST /products/_bulk?refresh=wait_for
{"index": {"_id": "1"}}
{"name": "Product", "price": 100}
```

Options: `false`, `true`, `wait_for`

---

## Threading and Throttling

```json
POST /products/_update_by_query?slices=auto&scroll_size=1000
{
  "query": {
    "match_all": {}
  }
}
```

Parallel processing with slices

---

## Best Practices

1. Use bulk API for multiple documents
1. Implement retry logic
1. Monitor pipeline performance
1. Test pipelines before production
1. Control refresh intervals

---

## Common Issues

1. Pipeline bottlenecks
1. Memory pressure from large batches
1. Processor failures
1. Version conflicts
