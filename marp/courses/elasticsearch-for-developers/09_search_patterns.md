# Search Patterns and Features

## Building User-Friendly Search Experiences

---

## Common Search Patterns

1. Pagination strategies
1. Faceted search
1. Autocomplete
1. Search-as-you-type
1. Geo-based search

---

## Pagination Overview

<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="50" fill="#4CAF50" rx="5"/>
  <text x="100" y="80" text-anchor="middle" fill="white">from/size</text>
  <text x="100" y="120" text-anchor="middle" font-size="12">Simple</text>
  <rect x="180" y="50" width="100" height="50" fill="#2196F3" rx="5"/>
  <text x="230" y="80" text-anchor="middle" fill="white">search_after</text>
  <text x="230" y="120" text-anchor="middle" font-size="12">Deep paging</text>
  <rect x="310" y="50" width="70" height="50" fill="#FF9800" rx="5"/>
  <text x="345" y="80" text-anchor="middle" fill="white">PIT</text>
  <text x="345" y="120" text-anchor="middle" font-size="12">Consistent</text>
</svg>

---

## From/Size Pagination

```json
GET /products/_search
{
  "from": 20,
  "size": 10,
  "query": {
    "match_all": {}
  }
}
```

Page 3 with 10 results per page

---

## From/Size Limitations

1. Max window: 10,000 results (default)
1. Performance degrades with depth
1. Memory usage increases
1. Not suitable for deep pagination

---

## Increasing Max Window

```json
PUT /products/_settings
{
  "index.max_result_window": 50000
}
```

⚠️ Use with caution!

---

## Search After

```json
GET /products/_search
{
  "size": 10,
  "sort": [
    {"price": "asc"},
    {"_id": "asc"}
  ],
  "search_after": [29.99, "product_123"]
}
```

Efficient deep pagination

---

## Search After Workflow

1. First request with sort
1. Get last document's sort values
1. Use values in `search_after`
1. Repeat for next page

---

## Point in Time (PIT)

```json
POST /products/_pit?keep_alive=1m

GET /_search
{
  "size": 10,
  "pit": {
    "id": "46ToAwMDaWR5BXV...",
    "keep_alive": "1m"
  }
}
```

Consistent pagination snapshot

---

## PIT with Search After

```json
{
  "size": 10,
  "pit": {
    "id": "46ToAwMDaWR5BXV..."
  },
  "sort": [{"_shard_doc": "asc"}],
  "search_after": [12345]
}
```

Best practice for pagination

---

## Scroll API (Deprecated)

```json
POST /products/_search?scroll=1m
{
  "size": 100,
  "query": {"match_all": {}}
}

POST /_search/scroll
{
  "scroll": "1m",
  "scroll_id": "DnF1ZXJ..."
}
```

Use PIT instead!

---

## Sorting Results

```json
{
  "sort": [
    {"price": {"order": "asc"}},
    {"_score": {"order": "desc"}},
    {"name.keyword": {"order": "asc"}}
  ]
}
```

Multi-level sorting

---

## Sort with Missing Values

```json
{
  "sort": [
    {
      "price": {
        "order": "asc",
        "missing": "_last"
      }
    }
  ]
}
```

Options: `_first`, `_last`, or custom value

---

## Geo Distance Sorting

```json
{
  "sort": [
    {
      "_geo_distance": {
        "location": {"lat": 40.7, "lon": -74.0},
        "order": "asc",
        "unit": "km"
      }
    }
  ]
}
```

---

## Script-based Sorting

```json
{
  "sort": {
    "_script": {
      "type": "number",
      "script": {
        "source": "doc['price'].value * doc['rating'].value"
      },
      "order": "desc"
    }
  }
}
```

---

## Faceted Search

<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="80" height="100" fill="#f0f0f0" stroke="#333" rx="5"/>
  <text x="90" y="75" text-anchor="middle" font-weight="bold">Filters</text>
  <text x="90" y="95" text-anchor="middle" font-size="12">□ Brand</text>
  <text x="90" y="115" text-anchor="middle" font-size="12">□ Price</text>
  <text x="90" y="135" text-anchor="middle" font-size="12">□ Color</text>
  <rect x="160" y="50" width="200" height="100" fill="#e8f5e9" stroke="#4CAF50" rx="5"/>
  <text x="260" y="75" text-anchor="middle" font-weight="bold">Results</text>
  <text x="260" y="100" text-anchor="middle">Filtered products</text>
  <text x="260" y="120" text-anchor="middle">with counts</text>
</svg>

---

## Building Facets

```json
{
  "aggs": {
    "brands": {
      "terms": {
        "field": "brand.keyword",
        "size": 10
      }
    },
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          {"to": 50},
          {"from": 50, "to": 200},
          {"from": 200}
        ]
      }
    }
  }
}
```

---

## Post Filter

```json
{
  "query": {
    "match": {"description": "laptop"}
  },
  "post_filter": {
    "term": {"brand": "dell"}
  },
  "aggs": {
    "all_brands": {
      "terms": {"field": "brand.keyword"}
    }
  }
}
```

Filter results, not aggregations

---

## Multi-Select Facets

```json
{
  "aggs": {
    "all_brands": {
      "global": {},
      "aggs": {
        "brands": {
          "terms": {"field": "brand.keyword"}
        }
      }
    },
    "filtered_brands": {
      "filter": {
        "bool": {
          "must": [
            {"term": {"category": "electronics"}}
          ]
        }
      },
      "aggs": {
        "brands": {
          "terms": {"field": "brand.keyword"}
        }
      }
    }
  }
}
```

---

## Filter Breadcrumbs

```json
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"category": "electronics"}},
        {"term": {"brand": "apple"}},
        {"range": {"price": {"lte": 1000}}}
      ]
    }
  }
}
```

Build from selected facets

---

## Autocomplete with Prefix

```json
{
  "query": {
    "prefix": {
      "name": {
        "value": "lap"
      }
    }
  }
}
```

Simple but limited

---

## Edge N-gram Mapping

```json
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "autocomplete": {
            "type": "text",
            "analyzer": "edge_ngram_analyzer"
          }
        }
      }
    }
  }
}
```

---

## Edge N-gram Analyzer

```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "edge_ngram_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase", "edge_ngram_filter"]
        }
      },
      "filter": {
        "edge_ngram_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 10
        }
      }
    }
  }
}
```

---

## Completion Suggester Setup

```json
{
  "mappings": {
    "properties": {
      "suggest": {
        "type": "completion",
        "analyzer": "simple",
        "preserve_separators": true,
        "preserve_position_increments": true,
        "max_input_length": 50
      }
    }
  }
}
```

---

## Index Completion Data

```json
PUT /products/_doc/1
{
  "name": "Apple MacBook Pro",
  "suggest": {
    "input": [
      "Apple MacBook Pro",
      "MacBook",
      "Apple laptop"
    ],
    "weight": 10
  }
}
```

---

## Query Completion

```json
{
  "_source": false,
  "suggest": {
    "product_suggest": {
      "prefix": "mac",
      "completion": {
        "field": "suggest",
        "size": 5,
        "skip_duplicates": true
      }
    }
  }
}
```

---

## Search As You Type Field

```json
{
  "mappings": {
    "properties": {
      "title": {
        "type": "search_as_you_type",
        "max_shingle_size": 3
      }
    }
  }
}
```

Built-in autocomplete support

---

## Query Search As You Type

```json
{
  "query": {
    "multi_match": {
      "query": "quick bro",
      "type": "bool_prefix",
      "fields": [
        "title",
        "title._2gram",
        "title._3gram"
      ]
    }
  }
}
```

---

## Fuzzy Autocomplete

```json
{
  "suggest": {
    "fuzzy_suggest": {
      "prefix": "appl",
      "completion": {
        "field": "suggest",
        "fuzzy": {
          "fuzziness": 2
        }
      }
    }
  }
}
```

Handle typos

---

## Context Suggester

```json
{
  "mappings": {
    "properties": {
      "suggest": {
        "type": "completion",
        "contexts": [
          {
            "name": "category",
            "type": "category"
          }
        ]
      }
    }
  }
}
```

Category-aware suggestions

---

## Index with Context

```json
PUT /products/_doc/1
{
  "name": "iPhone",
  "suggest": {
    "input": "iPhone",
    "contexts": {
      "category": ["electronics", "mobile"]
    }
  }
}
```

---

## Query with Context

```json
{
  "suggest": {
    "product_suggest": {
      "prefix": "iph",
      "completion": {
        "field": "suggest",
        "contexts": {
          "category": ["mobile"]
        }
      }
    }
  }
}
```

---

## Highlight Search Terms

```json
{
  "query": {
    "match": {"description": "wireless mouse"}
  },
  "highlight": {
    "fields": {
      "description": {
        "pre_tags": ["<mark>"],
        "post_tags": ["</mark>"],
        "fragment_size": 150
      }
    }
  }
}
```

---

## Search State Management

Track in application:
1. Current query
1. Active filters
1. Sort order
1. Page number
1. Results per page

---

## Performance Patterns

1. Cache frequent queries
1. Use filter context for facets
1. Limit aggregation cardinality
1. Implement result caching
1. Consider async search for slow queries

---

## Testing Search Quality

1. Collect search analytics
1. Track zero-result queries
1. Monitor click-through rates
1. A/B test variations
1. Gather user feedback

---

## Common Anti-patterns

1. Deep pagination with from/size
1. Wildcard queries on large fields
1. Not using filter context
1. Over-fetching with `size`
1. Ignoring query performance
