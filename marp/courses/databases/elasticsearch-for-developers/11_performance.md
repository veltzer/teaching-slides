# Performance Optimization for Developers

## Maximizing Elasticsearch Performance

---

## Performance Areas

<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="60" fill="#4CAF50" rx="5"/>
  <text x="100" y="85" text-anchor="middle" fill="white">Query</text>
  <rect x="180" y="50" width="100" height="60" fill="#2196F3" rx="5"/>
  <text x="230" y="85" text-anchor="middle" fill="white">Indexing</text>
  <rect x="50" y="140" width="100" height="60" fill="#FF9800" rx="5"/>
  <text x="100" y="175" text-anchor="middle" fill="white">Data Model</text>
  <rect x="180" y="140" width="100" height="60" fill="#9C27B0" rx="5"/>
  <text x="230" y="175" text-anchor="middle" fill="white">Hardware</text>
  <circle cx="320" cy="125" r="40" fill="#F44336"/>
  <text x="320" y="130" text-anchor="middle" fill="white">Cache</text>
</svg>

---

## Query Performance

Key principles:
1. Filter instead of query when possible
1. Use query context only for scoring
1. Cache frequently used filters
1. Avoid expensive queries
1. Profile slow queries

---

## Filter vs Query Context

```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"title": "laptop"}}  // Scores
      ],
      "filter": [  // No scoring, cached
        {"term": {"status": "active"}},
        {"range": {"price": {"lte": 1000}}}
      ]
    }
  }
}
```

---

## Query Caching

Elasticsearch caches:
1. Filter context queries
1. Aggregation results
1. Not cached: Query context
1. Cache key: Query structure + data

---

## Cache Settings

```json
PUT /products/_settings
{
  "index.queries.cache.enabled": true,
  "index.requests.cache.enable": true
}
```

Monitor cache usage:
```console
GET /_nodes/stats/indices/query_cache
```

---

## Expensive Query Types

Avoid or optimize:
1. **Wildcard**: `*pattern*`
1. **Regexp**: Complex patterns
1. **Fuzzy**: High edit distance
1. **Script queries**: Compute-intensive
1. **Deep pagination**: Large `from` values

---

## Query Optimization

```json
// Bad: Wildcard at beginning
{"wildcard": {"email": "*@example.com"}}

// Better: Use prefix
{"prefix": {"email_domain": "example.com"}}

// Best: Use keyword field
{"term": {"email_domain.keyword": "example.com"}}
```

---

## Profile API

```json
GET /products/_search
{
  "profile": true,
  "query": {
    "match": {"description": "wireless mouse"}
  }
}
```

Shows time breakdown per query component

---

## Profile Output

```json
{
  "profile": {
    "shards": [{
      "searches": [{
        "query": [{
          "type": "TermQuery",
          "time_in_nanos": 123456,
          "breakdown": {
            "score": 45678,
            "build_scorer": 12345
          }
        }]
      }]
    }]
  }
}
```

---

## Indexing Performance

Key factors:
1. Bulk size optimization
1. Refresh interval tuning
1. Replica configuration
1. Document routing
1. Thread pool settings

---

## Bulk Indexing Best Practices

```python
def optimal_bulk_index(docs):
    batch = []
    batch_size = 0

    for doc in docs:
        batch.append(doc)
        batch_size += len(json.dumps(doc))

        if len(batch) >= 1000 or batch_size >= 5_000_000:
            es.bulk(batch)
            batch = []
            batch_size = 0
```

---

## Refresh Interval

```json
PUT /products/_settings
{
  "index.refresh_interval": "30s"
}

// Disable during bulk indexing
PUT /products/_settings
{
  "index.refresh_interval": "-1"
}
```

Default: 1 second

---

## Replica Strategy

```json
// During bulk indexing
PUT /products/_settings
{
  "number_of_replicas": 0
}

// After indexing
PUT /products/_settings
{
  "number_of_replicas": 1
}
```

---

## Indexing Buffer

```json
PUT /_cluster/settings
{
  "persistent": {
    "indices.memory.index_buffer_size": "20%"
  }
}
```

More buffer = better bulk performance

---

## Thread Pool Tuning

```yaml
# elasticsearch.yml
thread_pool:
  write:
    size: 8
    queue_size: 500
  search:
    size: 13
    queue_size: 1000
```

---

## Data Modeling Performance

<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-weight="bold">Query Performance Impact</text>
  <rect x="50" y="50" width="80" height="40" fill="#4CAF50" rx="5"/>
  <text x="90" y="75" text-anchor="middle" fill="white" font-size="12">Denorm</text>
  <rect x="150" y="50" width="80" height="60" fill="#FFC107" rx="5"/>
  <text x="190" y="85" text-anchor="middle" fill="black" font-size="12">Parent-Child</text>
  <rect x="250" y="50" width="80" height="80" fill="#F44336" rx="5"/>
  <text x="290" y="95" text-anchor="middle" fill="white" font-size="12">Nested</text>
  <text x="200" y="160" text-anchor="middle">Fast → Slow</text>
</svg>

---

## Denormalization Benefits

```json
// Instead of joins, duplicate data
{
  "product_id": "123",
  "product_name": "Laptop",
  "category": {
    "id": "electronics",
    "name": "Electronics",
    "parent": "Technology"
  }
}
```

Trade storage for speed

---

## Field Data Types Impact

```json
{
  "mappings": {
    "properties": {
      "exact_match": {"type": "keyword"},  // Fast
      "full_text": {"type": "text"},       // Slower
      "number": {"type": "long"},          // Fast
      "nested": {"type": "nested"}         // Slowest
    }
  }
}
```

---

## Doc Values Optimization

```json
{
  "mappings": {
    "properties": {
      "never_aggregate": {
        "type": "text",
        "doc_values": false  // Save memory
      },
      "always_aggregate": {
        "type": "keyword",
        "doc_values": true   // Default
      }
    }
  }
}
```

---

## Norms Optimization

```json
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "norms": true  // Need scoring
      },
      "description": {
        "type": "text",
        "norms": false  // No scoring needed
      }
    }
  }
}
```

---

## Field Limitation

```json
PUT /products/_settings
{
  "index.mapping.total_fields.limit": 500,
  "index.mapping.depth.limit": 10,
  "index.mapping.nested_fields.limit": 25
}
```

Prevent mapping explosion

---

## Search Optimization Patterns

```json
// Use terminate_after for exists checks
{
  "query": {"match": {"category": "electronics"}},
  "terminate_after": 1,
  "size": 0
}
```

Stop after finding N matches

---

## Request Breaker

```json
{
  "query": {"match_all": {}},
  "timeout": "1s"
}
```

Prevent long-running queries

---

## Pagination Performance

```json
// Bad: Deep pagination
{"from": 10000, "size": 10}

// Good: Search after
{
  "search_after": [1234, "id"],
  "sort": [{"_id": "asc"}]
}
```

---

## Aggregation Optimization

```json
{
  "aggs": {
    "sampled": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_terms": {
            "field": "text"
          }
        }
      }
    }
  }
}
```

Sample for expensive aggregations

---

## Shard Size Impact

Optimal shard size:
1. Target: 10-50 GB per shard
1. No more than 20 shards per GB heap
1. Fewer large shards > many small shards
1. Consider future growth

---

## Force Merge

```json
POST /products/_forcemerge?max_num_segments=1
```

Use for read-only indices:
1. Reduces segment count
1. Improves query performance
1. Removes deleted documents
1. CPU intensive operation

---

## Routing Strategy

```json
PUT /products/_doc/1?routing=electronics
{
  "name": "Laptop",
  "category": "electronics"
}

GET /products/_search?routing=electronics
{
  "query": {"match_all": {}}
}
```

Query fewer shards

---

## Preference Parameter

```json
GET /products/_search?preference=_local
{
  "query": {"match_all": {}}
}
```

Options: `_local`, `_prefer_nodes`, `_shards`, custom

---

## Monitoring Performance

Key metrics:
1. Query latency
1. Indexing rate
1. Cache hit rates
1. GC frequency
1. Thread pool rejections

---

## Slow Log Configuration

```json
PUT /products/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.fetch.warn": "1s",
  "index.indexing.slowlog.threshold.index.warn": "10s"
}
```

---

## Hot Threads API

```bash
GET /_nodes/hot_threads
```

Identifies CPU-intensive operations

---

## Memory Management

```yaml
# jvm.options
-Xms16g
-Xmx16g  # 50% of RAM, max 32GB
```

Heap recommendations:
1. Same min and max heap
1. No more than 50% of RAM
1. Leave RAM for OS cache

---

## Circuit Breakers

```json
PUT /_cluster/settings
{
  "persistent": {
    "indices.breaker.total.limit": "70%",
    "indices.breaker.request.limit": "60%",
    "indices.breaker.fielddata.limit": "60%"
  }
}
```

Prevent OutOfMemory errors

---

## Client-side Optimizations

1. Connection pooling
1. Retry with backoff
1. Bulk request batching
1. Async operations
1. Response streaming

---

## Performance Testing

```python
def benchmark_query(query, iterations=100):
    times = []
    for _ in range(iterations):
        start = time.time()
        es.search(index="products", body=query)
        times.append(time.time() - start)

    return {
        "avg": statistics.mean(times),
        "p95": statistics.quantiles(times, n=20)[18]
    }
```

---

## Common Performance Issues

1. Deep pagination with from/size
1. Wildcard queries on large fields
1. Scripts in hot code paths
1. Parent-child with many children
1. Not using filters

---

## Performance Checklist

1. ✓ Use filters for non-scoring queries
1. ✓ Optimize bulk size (5-15MB)
1. ✓ Tune refresh interval
1. ✓ Monitor slow logs
1. ✓ Profile expensive queries

---

## Next Steps

1. Client Libraries and Integration
1. Connection management
1. Error handling
1. Integration patterns
