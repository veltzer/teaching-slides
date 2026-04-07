# Best Practices and Common Pitfalls

## Building Robust Elasticsearch Applications

---

## Best Practices Overview

![best_practices_overview](svg/courses/databases/elasticsearch-for-developers/17_best_practices/best_practices_overview.svg)

---

## Data Modeling Best Practices

1. **Denormalize for performance**
1. **Use correct field types**
1. **Limit nested documents**
1. **Plan for growth**
1. **Version your mappings**

---

## Schema Design Principles

```json
{
  "mappings": {
    "_meta": {
      "version": "2.0.0",
      "created_by": "team_name",
      "created_at": "2024-01-15"
    },
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "price": {
        "type": "scaled_float",
        "scaling_factor": 100
      },
      "timestamp": {
        "type": "date",
        "format": "strict_date_time||epoch_millis"
      }
    }
  }
}
```

---

## Field Naming Conventions

```python
# Good naming conventions
field_names = {
    "user_id": "keyword",           # Snake case
    "created_at": "date",            # Clear purpose
    "is_active": "boolean",          # Boolean prefix
    "product_count": "integer",      # Descriptive
    "price_usd": "float",           # Include units
    "description_en": "text"         # Include language
}

# Avoid
bad_names = {
    "usr": "keyword",               # Too abbreviated
    "date": "date",                 # Too generic
    "flag": "boolean",              # Unclear purpose
    "data": "object"                # Too vague
}
```

---

## Mapping Explosion Prevention

```json
PUT /products/_settings
{
  "index.mapping.total_fields.limit": 1000,
  "index.mapping.depth.limit": 20,
  "index.mapping.nested_fields.limit": 50,
  "index.mapping.nested_objects.limit": 10000,
  "index.mapping.field_name_length.limit": 50
}
```

---

## Dynamic Mapping Strategy

```json
{
  "mappings": {
    "dynamic": "strict",
    "dynamic_templates": [
      {
        "strings_as_keywords": {
          "match_mapping_type": "string",
          "match": "*_id",
          "mapping": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      {
        "unindexed_longs": {
          "match": "*_internal",
          "mapping": {
            "type": "long",
            "index": false
          }
        }
      }
    ]
  }
}
```

---

## Query Best Practices

1. Use filters for non-scoring queries
1. Avoid wildcard queries at scale
1. Prefer term queries for exact matches
1. Use bool query effectively
1. Profile slow queries

---

## Efficient Query Patterns

```python
# Good: Use filter context
good_query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"title": "laptop"}}
            ],
            "filter": [
                {"term": {"category": "electronics"}},
                {"range": {"price": {"lte": 1000}}}
            ]
        }
    }
}

# Bad: Everything in query context
bad_query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"title": "laptop"}},
                {"term": {"category": "electronics"}},
                {"range": {"price": {"lte": 1000}}}
            ]
        }
    }
}
```

---

## Pagination Best Practices

```python
class PaginationStrategy:
    @staticmethod
    def choose_strategy(total_results, page_size):
        if total_results <= 10000:
            return "from_size"
        elif total_results <= 100000:
            return "search_after"
        else:
            return "pit_search_after"

    @staticmethod
    def implement_search_after(last_sort_values):
        return {
            "size": 20,
            "sort": [
                {"_score": "desc"},
                {"_id": "asc"}
            ],
            "search_after": last_sort_values
        }

    @staticmethod
    def implement_pit(pit_id, last_sort_values=None):
        query = {
            "size": 20,
            "pit": {
                "id": pit_id,
                "keep_alive": "1m"
            },
            "sort": [{"_shard_doc": "asc"}]
        }
        if last_sort_values:
            query["search_after"] = last_sort_values
        return query
```

---

## Bulk Indexing Best Practices

```python
def optimized_bulk_index(documents, es_client):
    """Optimized bulk indexing with best practices"""

    # Disable refresh during bulk
    es_client.indices.put_settings(
        index="products",
        body={"refresh_interval": "-1"}
    )

    try:
        # Process in optimal batches
        batch_size = 1000  # documents
        batch_bytes = 0
        batch = []

        for doc in documents:
            doc_bytes = len(json.dumps(doc))

            # Check size limits
            if (len(batch) >= batch_size or
                batch_bytes + doc_bytes > 5_000_000):

                # Send batch
                helpers.bulk(es_client, batch)
                batch = []
                batch_bytes = 0

            batch.append({
                "_index": "products",
                "_source": doc
            })
            batch_bytes += doc_bytes

        # Send remaining
        if batch:
            helpers.bulk(es_client, batch)

    finally:
        # Re-enable refresh
        es_client.indices.put_settings(
            index="products",
            body={"refresh_interval": "1s"}
        )
```

---

## Index Lifecycle Strategy

```yaml
# Time-based indices for logs
logs-2024.01.15
logs-2024.01.16
logs-2024.01.17

# Version-based for applications
products_v1 → products (alias)
products_v2 → (prepare)
products_v2 → products (switch)
```

---

## Alias Management

```python
class AliasManager:
    def zero_downtime_reindex(self, old_index, new_index):
        """Zero-downtime index migration"""

        # 1. Create new index with updated mappings
        self.es.indices.create(index=new_index, body=new_mappings)

        # 2. Reindex data
        self.es.reindex(
            body={
                "source": {"index": old_index},
                "dest": {"index": new_index}
            },
            wait_for_completion=False
        )

        # 3. Wait for reindex to complete
        self.wait_for_task_completion(task_id)

        # 4. Switch alias atomically
        self.es.indices.update_aliases(
            body={
                "actions": [
                    {"remove": {"index": old_index, "alias": "products"}},
                    {"add": {"index": new_index, "alias": "products"}}
                ]
            }
        )

        # 5. Delete old index after verification
        # self.es.indices.delete(index=old_index)
```

---

## Shard Sizing Guidelines

```python
def calculate_shard_configuration(data_size_gb, growth_rate, retention_days):
    """Calculate optimal shard configuration"""

    # Target shard size: 10-50GB
    target_shard_size = 30  # GB

    # Calculate total size with growth
    total_size = data_size_gb * (1 + growth_rate) * retention_days / 30

    # Calculate shards needed
    num_shards = max(1, int(total_size / target_shard_size))

    # Adjust for cluster size
    num_nodes = get_cluster_nodes()
    num_shards = max(num_shards, num_nodes)  # At least one per node

    # Round to nearest power of 2 for better distribution
    import math
    num_shards = 2 ** math.ceil(math.log2(num_shards))

    return {
        "number_of_shards": num_shards,
        "number_of_replicas": 1,  # Standard for HA
        "estimated_shard_size_gb": total_size / num_shards
    }
```

---

## Error Handling Patterns

```python
from elasticsearch import Elasticsearch, exceptions
import time

class RobustElasticsearchClient:
    def __init__(self, hosts, max_retries=3):
        self.es = Elasticsearch(hosts)
        self.max_retries = max_retries

    def safe_search(self, **kwargs):
        """Search with comprehensive error handling"""

        for attempt in range(self.max_retries):
            try:
                return self.es.search(**kwargs)

            except exceptions.ConnectionTimeout:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise

            except exceptions.RequestError as e:
                # Bad query - don't retry
                self.log_error("Query error", e)
                raise

            except exceptions.NotFoundError:
                # Index doesn't exist
                return {"hits": {"total": {"value": 0}, "hits": []}}

            except exceptions.AuthorizationException:
                # Auth issues - don't retry
                self.log_error("Authorization failed", e)
                raise
```

---

## Connection Pool Management

```python
from elasticsearch import Elasticsearch
from urllib3.util.retry import Retry

class ConnectionManager:
    @staticmethod
    def create_client():
        """Create client with proper connection management"""

        return Elasticsearch(
            ["host1:9200", "host2:9200", "host3:9200"],

            # Connection pool
            maxsize=25,

            # Sniffing
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniff_timeout=60,

            # Timeouts
            timeout=30,
            max_retries=3,
            retry_on_timeout=True,

            # HTTP compression
            http_compress=True,

            # SSL
            use_ssl=True,
            verify_certs=True,
            ssl_show_warn=False
        )
```

---

## Security Best Practices

```python
class SecurityBestPractices:
    def setup_secure_connection(self):
        """Configure secure Elasticsearch connection"""

        from elasticsearch import Elasticsearch
        import ssl

        # Create SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Use API keys instead of passwords
        es = Elasticsearch(
            ["https://localhost:9200"],
            api_key=("id", "api_key"),
            ssl_context=context,

            # Additional security headers
            headers={
                "X-Custom-Header": "value"
            }
        )

        return es

    def implement_field_level_security(self):
        """Example of field-level security"""

        return {
            "indices": [
                {
                    "names": ["products"],
                    "privileges": ["read"],
                    "field_security": {
                        "grant": ["name", "description", "price"],
                        "except": ["cost", "margin", "supplier_details"]
                    },
                    "query": {
                        "term": {"public": True}
                    }
                }
            ]
        }
```

---

## Monitoring and Alerting

```python
class MonitoringStrategy:
    def __init__(self, es):
        self.es = es
        self.thresholds = {
            "cluster_health": "yellow",
            "heap_usage_percent": 85,
            "disk_usage_percent": 90,
            "search_latency_ms": 1000,
            "indexing_rate": 100  # docs/sec
        }

    def check_cluster_health(self):
        health = self.es.cluster.health()

        alerts = []

        # Check status
        if health["status"] == "red":
            alerts.append({
                "severity": "critical",
                "message": "Cluster status is RED"
            })
        elif health["status"] == "yellow":
            alerts.append({
                "severity": "warning",
                "message": "Cluster status is YELLOW"
            })

        # Check unassigned shards
        if health["unassigned_shards"] > 0:
            alerts.append({
                "severity": "warning",
                "message": f"{health['unassigned_shards']} unassigned shards"
            })

        return alerts
```

---

## Performance Monitoring

```python
def monitor_performance_metrics():
    """Key metrics to monitor"""

    metrics = {
        # Query performance
        "search_latency": get_search_latency(),
        "search_rate": get_search_rate(),

        # Indexing performance
        "indexing_latency": get_indexing_latency(),
        "indexing_rate": get_indexing_rate(),

        # Resource usage
        "heap_usage": get_heap_usage(),
        "cpu_usage": get_cpu_usage(),
        "disk_io": get_disk_io(),

        # Cache effectiveness
        "query_cache_hit_rate": get_cache_hit_rate("query"),
        "request_cache_hit_rate": get_cache_hit_rate("request"),

        # Errors
        "circuit_breaker_trips": get_circuit_breaker_trips(),
        "rejected_threads": get_rejected_threads()
    }

    return metrics
```

---

## Common Mapping Pitfalls

```python
# PITFALL 1: Not using multi-fields
bad_mapping = {
    "title": {"type": "text"}  # Can't aggregate or sort
}

good_mapping = {
    "title": {
        "type": "text",
        "fields": {
            "keyword": {"type": "keyword"}  # For aggregations/sorting
        }
    }
}

# PITFALL 2: Wrong numeric type
bad_mapping = {
    "price": {"type": "float"}  # Precision issues with money
}

good_mapping = {
    "price": {
        "type": "scaled_float",
        "scaling_factor": 100  # Store cents as integer
    }
}

# PITFALL 3: Massive nested documents
bad_mapping = {
    "comments": {"type": "nested"}  # No limit!
}

good_mapping = {
    "comments": {
        "type": "nested",
        "properties": {...}
    }
}
# Plus setting: index.mapping.nested_objects.limit
```

---

## Common Query Pitfalls

```python
# PITFALL 1: Deep pagination
bad_query = {
    "from": 50000,  # Will fail or be very slow
    "size": 20
}

# PITFALL 2: Unbounded terms aggregation
bad_agg = {
    "aggs": {
        "all_users": {
            "terms": {
                "field": "user_id",
                "size": 2147483647  # Don't do this!
            }
        }
    }
}

# PITFALL 3: Wildcard at beginning
bad_query = {
    "query": {
        "wildcard": {
            "email": "*@example.com"  # Very expensive
        }
    }
}
```

---

## Common Indexing Pitfalls

```python
# PITFALL 1: Not using bulk API
def bad_indexing(documents):
    for doc in documents:  # One request per document
        es.index(index="products", document=doc)

# PITFALL 2: Frequent refreshes
bad_settings = {
    "index.refresh_interval": "1ms"  # Way too frequent
}

# PITFALL 3: Too many small indices
# Having 1000 indices with 1MB each instead of proper time-based indices

# PITFALL 4: Not handling failures
response = es.bulk(body=bulk_body)
# Not checking response["errors"]
```

---

## Common Performance Pitfalls

```python
# PITFALL 1: Not using filters
slow_query = {
    "query": {
        "bool": {
            "must": [  # Everything scores
                {"match": {"title": "laptop"}},
                {"term": {"category": "electronics"}},
                {"range": {"price": {"lte": 1000}}}
            ]
        }
    }
}

# PITFALL 2: Script queries without caching
bad_script = {
    "query": {
        "script": {
            "script": {
                "source": "doc['price'].value * 1.2 < params.max",
                "params": {"max": 1000}
            }
        }
    }
}

# PITFALL 3: Nested queries on large arrays
bad_nested = {
    "query": {
        "nested": {
            "path": "comments",  # 10000 comments per doc
            "query": {"match_all": {}}
        }
    }
}
```

---

## Development Workflow

```python
class DevelopmentWorkflow:
    """Best practice development workflow"""

    def __init__(self):
        self.environments = {
            "dev": "http://localhost:9200",
            "staging": "https://staging-es.company.com",
            "production": "https://es.company.com"
        }

    def deploy_mapping_change(self, new_mapping):
        """Safe mapping deployment"""

        # 1. Test in dev
        self.test_mapping_in_dev(new_mapping)

        # 2. Create new index in staging
        staging_index = f"products_v{get_next_version()}"
        self.create_index_staging(staging_index, new_mapping)

        # 3. Reindex sample data
        self.reindex_sample_data(staging_index)

        # 4. Run integration tests
        self.run_integration_tests(staging_index)

        # 5. Performance test
        self.run_performance_tests(staging_index)

        # 6. Deploy to production with alias swap
        if all_tests_pass():
            self.deploy_to_production(staging_index)
```

---

## Version Control for Elasticsearch

```python
# mappings/products_v2.json
{
    "version": "2.0.0",
    "changes": [
        "Added 'brand' field as keyword",
        "Changed 'description' analyzer to 'english'",
        "Added 'created_at' date field"
    ],
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "brand": {"type": "keyword"},  # NEW
            "description": {
                "type": "text",
                "analyzer": "english"  # CHANGED
            },
            "created_at": {"type": "date"}  # NEW
        }
    }
}

# migrations/002_add_brand_field.py
def upgrade():
    """Add brand field to products index"""
    reindex_with_script(
        source="products_v1",
        dest="products_v2",
        script="ctx._source.brand = 'Unknown'"
    )

def downgrade():
    """Remove brand field"""
    reindex(source="products_v2", dest="products_v1")
```

---

## Testing Strategies

```python
import pytest
from elasticsearch import Elasticsearch

class TestSearchFunctionality:
    @pytest.fixture
    def es_client(self):
        """Test client with test index"""
        es = Elasticsearch(["localhost:9200"])
        test_index = "test_products"

        # Create test index
        if es.indices.exists(index=test_index):
            es.indices.delete(index=test_index)

        es.indices.create(
            index=test_index,
            body=get_test_mapping()
        )

        yield es

        # Cleanup
        es.indices.delete(index=test_index)

    def test_search_relevance(self, es_client):
        """Test search returns relevant results"""

        # Index test data
        test_docs = create_test_documents()
        bulk_index(es_client, test_docs)
        es_client.indices.refresh(index="test_products")

        # Test search
        results = search_products("laptop")

        assert results["hits"]["total"]["value"] > 0
        assert "laptop" in results["hits"]["hits"][0]["_source"]["name"].lower()
```

---

## Documentation Best Practices

```python
class SearchService:
    """
    Service for handling product searches.

    Attributes:
        es_client: Elasticsearch client instance
        index_name: Name of the products index

    Example:
        >>> service = SearchService()
        >>> results = service.search("laptop", filters={"category": "electronics"})
    """

    def search(self, query: str, filters: dict = None, size: int = 20) -> dict:
        """
        Search for products.

        Args:
            query: Search query text
            filters: Optional filters to apply
            size: Number of results to return

        Returns:
            dict: Elasticsearch response with hits

        Raises:
            SearchException: If search fails

        Example:
            >>> results = service.search(
            ...     "gaming laptop",
            ...     filters={"price_range": {"min": 500, "max": 1500}}
            ... )
        """
        pass
```

---

## Capacity Planning

```python
def capacity_planning(requirements):
    """Plan Elasticsearch cluster capacity"""

    calculations = {
        # Storage calculation
        "raw_data_size_gb": requirements["daily_data_gb"] * requirements["retention_days"],
        "with_replica_gb": requirements["daily_data_gb"] * requirements["retention_days"] * 2,
        "with_overhead_gb": requirements["daily_data_gb"] * requirements["retention_days"] * 2.2,

        # Memory calculation
        "heap_needed_gb": calculate_heap_size(requirements),
        "total_ram_needed_gb": calculate_heap_size(requirements) * 2,

        # Node calculation
        "data_nodes_needed": calculate_data_nodes(requirements),
        "master_nodes": 3,  # For HA
        "coordinator_nodes": calculate_coordinator_nodes(requirements),

        # Shard calculation
        "total_shards": calculate_shard_count(requirements),
        "shards_per_node": calculate_shards_per_node(requirements)
    }

    return calculations
```

---

## Disaster Recovery

```python
class DisasterRecovery:
    def __init__(self):
        self.backup_repo = "s3_backup"

    def setup_snapshot_repository(self):
        """Configure snapshot repository"""

        self.es.snapshot.create_repository(
            repository=self.backup_repo,
            body={
                "type": "s3",
                "settings": {
                    "bucket": "elasticsearch-backups",
                    "region": "us-east-1",
                    "compress": True,
                    "chunk_size": "100m"
                }
            }
        )

    def create_snapshot_policy(self):
        """Automated snapshot policy"""

        self.es.slm.put_lifecycle(
            policy_id="daily-snapshots",
            body={
                "schedule": "0 0 2 * * ?",  # 2 AM daily
                "name": "<daily-snap-{now/d}>",
                "repository": self.backup_repo,
                "config": {
                    "indices": ["products*", "orders*"],
                    "include_global_state": False
                },
                "retention": {
                    "expire_after": "30d",
                    "min_count": 7,
                    "max_count": 30
                }
            }
        )
```

---

## Migration Checklist

```python
migration_checklist = {
    "pre_migration": [
        "Backup current data",
        "Document current mappings",
        "Identify breaking changes",
        "Test in staging environment",
        "Plan rollback strategy"
    ],

    "migration": [
        "Create new index with updated mappings",
        "Start dual writes (if applicable)",
        "Reindex data",
        "Verify data integrity",
        "Update aliases"
    ],

    "post_migration": [
        "Monitor error rates",
        "Check performance metrics",
        "Verify search quality",
        "Update documentation",
        "Clean up old indices"
    ],

    "rollback": [
        "Switch aliases back",
        "Stop dual writes",
        "Investigate issues",
        "Plan fixes"
    ]
}
```

---

## Production Readiness Checklist

```yaml
Infrastructure:
  ✓ High availability (3+ nodes)
  ✓ Proper heap sizing (50% RAM, max 32GB)
  ✓ SSD storage for hot data
  ✓ Network capacity planning
  ✓ Monitoring and alerting setup

Security:
  ✓ TLS/SSL enabled
  ✓ Authentication configured
  ✓ Role-based access control
  ✓ Audit logging enabled
  ✓ Field-level security (if needed)

Operations:
  ✓ Backup strategy implemented
  ✓ Disaster recovery plan
  ✓ Runbook documentation
  ✓ On-call rotation setup
  ✓ Capacity monitoring

Performance:
  ✓ Query performance tested
  ✓ Indexing rate validated
  ✓ Cache settings optimized
  ✓ Shard sizing appropriate
  ✓ Resource limits configured
```

---

## Debugging Tools

```bash
# Cluster health
GET /_cluster/health?pretty

# Allocation issues
GET /_cluster/allocation/explain

# Hot threads
GET /_nodes/hot_threads

# Task management
GET /_tasks?detailed=true&actions=*search

# Slow logs
GET /products/_settings/index.search.slowlog*

# Profile query
GET /products/_search
{
  "profile": true,
  "query": {...}
}
```

---

## Cost Optimization

```python
class CostOptimization:
    def optimize_storage_costs(self):
        """Strategies to reduce storage costs"""

        strategies = {
            "compression": {
                "codec": "best_compression",
                "savings": "10-20%"
            },

            "source_exclusion": {
                "excludes": ["internal_fields"],
                "savings": "5-15%"
            },

            "force_merge": {
                "max_num_segments": 1,
                "only_for": "read_only_indices",
                "savings": "10-30%"
            },

            "ilm_policies": {
                "hot": "SSD storage",
                "warm": "HDD storage",
                "cold": "Object storage",
                "savings": "40-60%"
            },

            "field_optimization": {
                "disable_unused": ["_all", "norms"],
                "savings": "5-10%"
            }
        }

        return strategies
```

---

## Scaling Strategies

![scaling_strategies](svg/courses/databases/elasticsearch-for-developers/17_best_practices/scaling_strategies.svg)

---

## Team Collaboration

```python
class ElasticsearchTeamStandards:
    """Team standards and practices"""

    naming_conventions = {
        "indices": "lowercase_with_underscores",
        "fields": "snake_case",
        "aliases": "descriptive_names",
        "pipelines": "process_type_description"
    }

    code_review_checklist = [
        "Mapping changes reviewed",
        "Query performance considered",
        "Error handling implemented",
        "Tests written",
        "Documentation updated"
    ]

    deployment_process = [
        "PR created with changes",
        "Automated tests pass",
        "Code review approved",
        "Staging deployment successful",
        "Production deployment scheduled"
    ]
```

---

## Continuous Improvement

```python
def improvement_cycle():
    """Continuous improvement process"""

    while True:
        # Measure
        metrics = collect_metrics()

        # Analyze
        bottlenecks = identify_bottlenecks
```
