# Advanced Developer Features

## Scripting, Pipelines, and Advanced Capabilities

---

## Advanced Features Overview

![advanced_features_overview](svg/courses/databases/elasticsearch-for-developers/14_advanced_features/advanced_features_overview.svg)

---

## Painless Scripting Language

Why Painless?
1. Secure by design
1. Fast execution
1. Java-like syntax
1. Built for Elasticsearch
1. Sandboxed environment

---

## Painless Basics

```json
{
  "script": {
    "lang": "painless",
    "source": """
      int total = 0;
      for (int i = 0; i < params.values.length; i++) {
        total += params.values[i];
      }
      return total;
    """,
    "params": {
      "values": [1, 2, 3, 4, 5]
    }
  }
}
```

---

## Script Fields

```json
GET /orders/_search
{
  "script_fields": {
    "total_with_tax": {
      "script": {
        "source": "doc['price'].value * doc['quantity'].value * 1.2"
      }
    },
    "discount_amount": {
      "script": {
        "source": """
          double price = doc['price'].value;
          double discount = doc['discount_percent'].value / 100;
          return price * discount;
        """
      }
    }
  }
}
```

---

## Script Queries

```json
{
  "query": {
    "bool": {
      "filter": {
        "script": {
          "script": {
            "source": """
              doc['stock'].value > 0 &&
              doc['price'].value < params.max_price
            """,
            "params": {
              "max_price": 100
            }
          }
        }
      }
    }
  }
}
```

---

## Script Scoring

```json
{
  "query": {
    "function_score": {
      "query": {"match": {"title": "laptop"}},
      "script_score": {
        "script": {
          "source": """
            double boost = 1.0;
            if (doc['featured'].value) boost *= 2;
            if (doc['in_stock'].value) boost *= 1.5;
            return _score * boost *
                   Math.log(2 + doc['popularity'].value);
          """
        }
      }
    }
  }
}
```

---

## Update Scripts

```json
POST /products/_update/1
{
  "script": {
    "source": """
      if (ctx._source.views == null) {
        ctx._source.views = 1;
      } else {
        ctx._source.views++;
      }

      if (ctx._source.views > 1000) {
        ctx._source.trending = true;
      }
    """
  }
}
```

---

## Bulk Update by Query

```json
POST /products/_update_by_query
{
  "script": {
    "source": """
      ctx._source.sale_price = ctx._source.price * 0.8;
      ctx._source.on_sale = true;
      ctx._source.sale_ends = params.end_date;
    """,
    "params": {
      "end_date": "2024-12-31"
    }
  },
  "query": {
    "term": {"category": "electronics"}
  }
}
```

---

## Script Aggregations

```json
{
  "aggs": {
    "profit_margin": {
      "avg": {
        "script": {
          "source": """
            (doc['price'].value - doc['cost'].value) /
            doc['price'].value * 100
          """
        }
      }
    },
    "custom_buckets": {
      "terms": {
        "script": {
          "source": """
            if (doc['price'].value < 50) return 'budget';
            else if (doc['price'].value < 200) return 'mid';
            else return 'premium';
          """
        }
      }
    }
  }
}
```

---

## Stored Scripts

```json
PUT _scripts/calculate_discount
{
  "script": {
    "lang": "painless",
    "source": """
      double price = doc['price'].value;
      double discount = params.discount_percent;
      return price * (1 - discount / 100);
    """
  }
}

GET /products/_search
{
  "script_fields": {
    "discounted_price": {
      "script": {
        "id": "calculate_discount",
        "params": {"discount_percent": 20}
      }
    }
  }
}
```

---

## Painless Context Variables

Available in different contexts:
1. **doc**: Access document fields
1. **_source**: Original document
1. **ctx**: Update context
1. **_score**: Query score
1. **params**: Script parameters

---

## Complex Pipeline Example

```json
PUT _ingest/pipeline/process_logs
{
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["%{COMBINEDAPACHELOG}"]
      }
    },
    {
      "date": {
        "field": "timestamp",
        "formats": ["dd/MMM/yyyy:HH:mm:ss Z"]
      }
    },
    {
      "geoip": {
        "field": "clientip",
        "target_field": "geo"
      }
    },
    {
      "user_agent": {
        "field": "agent",
        "target_field": "user_agent"
      }
    },
    {
      "script": {
        "source": """
          if (ctx.response != null) {
            int code = Integer.parseInt(ctx.response);
            ctx.status_category = code < 400 ? 'success' : 'error';
          }
        """
      }
    }
  ]
}
```

---

## Pipeline Composition

```json
PUT _ingest/pipeline/main_pipeline
{
  "processors": [
    {
      "pipeline": {
        "if": "ctx.type == 'access_log'",
        "name": "process_access_logs"
      }
    },
    {
      "pipeline": {
        "if": "ctx.type == 'error_log'",
        "name": "process_error_logs"
      }
    },
    {
      "set": {
        "field": "processed_at",
        "value": "{{_ingest.timestamp}}"
      }
    }
  ]
}
```

---

## Conditional Processing

```json
{
  "processors": [
    {
      "set": {
        "if": "ctx.price != null && ctx.price > 1000",
        "field": "category",
        "value": "premium"
      }
    },
    {
      "remove": {
        "if": """
          ctx.debug != null &&
          ctx.environment == 'production'
        """,
        "field": ["debug", "trace"]
      }
    }
  ]
}
```

---

## Error Handling in Pipelines

```json
{
  "processors": [
    {
      "convert": {
        "field": "price",
        "type": "float",
        "on_failure": [
          {
            "set": {
              "field": "price_error",
              "value": "Invalid price format"
            }
          },
          {
            "set": {
              "field": "price",
              "value": 0
            }
          }
        ]
      }
    }
  ]
}
```

---

## Pipeline Debugging

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "lowercase": {
          "field": "category"
        }
      }
    ]
  },
  "docs": [
    {
      "_source": {
        "category": "ELECTRONICS"
      }
    }
  ]
}
```

---

## Percolator Overview

Reverse search pattern:
1. Store queries instead of documents
1. Match documents against stored queries
1. Use cases: Alerts, classification, routing

---

## Percolator Mapping

```json
PUT /alerts
{
  "mappings": {
    "properties": {
      "query": {
        "type": "percolator"
      },
      "alert_name": {
        "type": "keyword"
      },
      "user_id": {
        "type": "keyword"
      },
      "threshold": {
        "type": "float"
      }
    }
  }
}
```

---

## Store Percolator Queries

```json
PUT /alerts/_doc/price_alert_1
{
  "alert_name": "Price Drop Alert",
  "user_id": "user123",
  "query": {
    "bool": {
      "must": [
        {"term": {"category": "electronics"}},
        {"range": {"price": {"lte": 500}}}
      ]
    }
  }
}
```

---

## Percolate Documents

```json
POST /alerts/_search
{
  "query": {
    "percolate": {
      "field": "query",
      "document": {
        "name": "Laptop Sale",
        "category": "electronics",
        "price": 450
      }
    }
  }
}
```

Returns matching alerts

---

## Percolator with Existing Docs

```json
{
  "query": {
    "percolate": {
      "field": "query",
      "index": "products",
      "id": "product_123"
    }
  }
}
```

---

## Data Streams

Time series data management:
```json
PUT _index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "data_stream": {},
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {"type": "date"},
        "message": {"type": "text"}
      }
    }
  }
}

PUT _data_stream/logs-app
```

---

## Data Stream Operations

```json
// Write to data stream
POST /logs-app/_doc
{
  "@timestamp": "2024-01-15T10:00:00Z",
  "message": "Application started"
}

// Search across stream
GET /logs-app/_search

// Roll over to new index
POST /logs-app/_rollover
```

---

## Index Lifecycle Management

```json
PUT _ilm/policy/logs_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "7d",
            "max_size": "50GB"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {"number_of_shards": 1},
          "forcemerge": {"max_num_segments": 1}
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {"delete": {}}
      }
    }
  }
}
```

---

## Apply ILM Policy

```json
PUT _index_template/logs_ilm
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "index.lifecycle.name": "logs_policy",
      "index.lifecycle.rollover_alias": "logs"
    }
  }
}
```

---

## Transform Jobs

```json
PUT _transform/sales_summary
{
  "source": {
    "index": ["sales-*"]
  },
  "dest": {
    "index": "sales_summary"
  },
  "pivot": {
    "group_by": {
      "customer": {"terms": {"field": "customer_id"}},
      "month": {"date_histogram": {"field": "date", "calendar_interval": "month"}}
    },
    "aggregations": {
      "total_spent": {"sum": {"field": "amount"}},
      "order_count": {"value_count": {"field": "order_id"}}
    }
  }
}
```

---

## Continuous Transforms

```json
PUT _transform/real_time_summary
{
  "source": {
    "index": ["orders"]
  },
  "dest": {
    "index": "order_summary"
  },
  "sync": {
    "time": {
      "field": "timestamp",
      "delay": "60s"
    }
  },
  "pivot": {
    "group_by": {
      "product": {"terms": {"field": "product_id"}}
    },
    "aggregations": {
      "sales": {"sum": {"field": "quantity"}}
    }
  }
}
```

---

## Watcher Alerts

```json
PUT _watcher/watch/error_alert
{
  "trigger": {
    "schedule": {"interval": "5m"}
  },
  "input": {
    "search": {
      "request": {
        "indices": ["logs-*"],
        "body": {
          "query": {
            "bool": {
              "filter": [
                {"term": {"level": "ERROR"}},
                {"range": {"@timestamp": {"gte": "now-5m"}}}
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {"ctx.payload.hits.total": {"gt": 10}}
  },
  "actions": {
    "send_email": {
      "email": {
        "to": "admin@example.com",
        "subject": "High Error Rate Alert"
      }
    }
  }
}
```

---

## Runtime Fields

```json
PUT /products/_mapping
{
  "runtime": {
    "profit_margin": {
      "type": "double",
      "script": {
        "source": """
          if (doc['cost'].size() > 0 && doc['price'].size() > 0) {
            emit((doc['price'].value - doc['cost'].value) /
                 doc['price'].value * 100);
          }
        """
      }
    }
  }
}
```

---

## Search with Runtime Fields

```json
GET /products/_search
{
  "runtime_mappings": {
    "day_of_week": {
      "type": "keyword",
      "script": {
        "source": """
          ZonedDateTime date = doc['timestamp'].value;
          emit(date.getDayOfWeek().toString());
        """
      }
    }
  },
  "query": {
    "term": {"day_of_week": "MONDAY"}
  }
}
```

---

## Snapshot and Restore

```json
PUT _snapshot/backup_repo
{
  "type": "fs",
  "settings": {
    "location": "/backup/elasticsearch"
  }
}

PUT _snapshot/backup_repo/snapshot_1?wait_for_completion=true
{
  "indices": "products,orders",
  "include_global_state": false
}

POST _snapshot/backup_repo/snapshot_1/_restore
{
  "indices": "products"
}
```

---

## Cross-Cluster Search

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.remote": {
      "cluster_two": {
        "seeds": ["node1.cluster2:9300"]
      }
    }
  }
}

GET /products,cluster_two:products/_search
{
  "query": {
    "match": {"name": "laptop"}
  }
}
```

---

## Security Features

```json
// Create role
PUT _security/role/products_reader
{
  "indices": [{
    "names": ["products"],
    "privileges": ["read"]
  }]
}

// Create user
PUT _security/user/john
{
  "password": "password123",
  "roles": ["products_reader"],
  "full_name": "John Doe"
}
```

---

## Field Level Security

```json
PUT _security/role/limited_access
{
  "indices": [{
    "names": ["products"],
    "privileges": ["read"],
    "field_security": {
      "grant": ["name", "price"],
      "except": ["cost", "margin"]
    },
    "query": {
      "term": {"public": true}
    }
  }]
}
```

---

## Audit Logging

```yaml
# elasticsearch.yml
xpack.security.audit.enabled: true
xpack.security.audit.outputs: [index, logfile]
xpack.security.audit.index.events.include:
  - authentication_failed
  - access_denied
  - tampered_request
```

---

## Performance Profiling

```json
GET /products/_search
{
  "profile": true,
  "query": {
    "match": {"name": "laptop"}
  },
  "aggregations": {
    "categories": {
      "terms": {"field": "category"}
    }
  }
}
```

---

## Advanced Debugging

```bash
# Enable slow log
PUT /products/_settings
{
  "index.search.slowlog.threshold.query.debug": "0ms",
  "index.search.slowlog.level": "debug"
}

# Check hot threads
GET /_nodes/hot_threads?threads=3

# Task management
GET /_tasks?detailed=true&actions=*search
```

---

## Best Practices

1. Cache frequently used scripts
1. Test pipelines before production
1. Monitor transform performance
1. Use ILM for time-series data
1. Regular snapshot backups

---

## Common Pitfalls

1. Complex scripts impacting performance
1. Pipeline failures blocking ingestion
1. Percolator query explosion
1. Transform job resource consumption
1. Missing error handling

---

## Next Steps

1. Search Analytics and Monitoring
1. Performance metrics
1. A/B testing
1. Quality measurements
