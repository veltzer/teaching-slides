# Application Development Patterns

## Building Production-Ready Search Applications

---

## Common Application Patterns

![common_application_patterns](/svg/courses/databases/elasticsearch-for-developers/13_app_patterns/common_application_patterns.svg)

---

## Search UI Architecture

```tree
// Frontend Component Structure
SearchApp
├── SearchBar
├── Filters
│   ├── CategoryFilter
│   ├── PriceRangeFilter
│   └── BrandFilter
├── Results
│   ├── ResultItem
│   └── Pagination
└── SearchAnalytics
```

---

## Search State Management

```javascript
const searchState = {
  query: "laptop",
  filters: {
    category: ["electronics"],
    priceRange: { min: 0, max: 1000 },
    brand: []
  },
  sort: { field: "price", order: "asc" },
  page: 1,
  pageSize: 20,
  results: [],
  facets: {},
  totalResults: 0
};
```

---

## Query Builder Pattern

```python
class QueryBuilder:
    def __init__(self):
        self.query = {"bool": {}}

    def add_text_search(self, text, fields):
        if "must" not in self.query["bool"]:
            self.query["bool"]["must"] = []
        self.query["bool"]["must"].append({
            "multi_match": {
                "query": text,
                "fields": fields
            }
        })
        return self

    def add_filter(self, field, value):
        if "filter" not in self.query["bool"]:
            self.query["bool"]["filter"] = []
        self.query["bool"]["filter"].append({
            "term": {field: value}
        })
        return self
```

---

## Facet Management

```javascript
class FacetManager {
  constructor(es) {
    this.es = es;
  }

  async buildFacets(query, selectedFilters) {
    const aggs = {
      all_categories: {
        terms: { field: "category.keyword" }
      },
      price_ranges: {
        range: {
          field: "price",
          ranges: [
            { to: 50 },
            { from: 50, to: 200 },
            { from: 200 }
          ]
        }
      }
    };

    return await this.es.search({
      query,
      aggs,
      size: 0
    });
  }
}
```

---

## Result Presentation

```javascript
function formatSearchResult(hit) {
  return {
    id: hit._id,
    score: hit._score,
    ...hit._source,
    highlights: hit.highlight || {},
    metadata: {
      index: hit._index,
      type: hit._type
    }
  };
}

function groupResults(results) {
  return results.reduce((acc, result) => {
    const category = result.category;
    if (!acc[category]) acc[category] = [];
    acc[category].push(result);
    return acc;
  }, {});
}
```

---

## Pagination Handler

```python
class PaginationHandler:
    def __init__(self, page_size=20):
        self.page_size = page_size

    def get_from_size(self, page):
        return {
            "from": (page - 1) * self.page_size,
            "size": self.page_size
        }

    def get_search_after(self, last_sort_values):
        return {
            "size": self.page_size,
            "search_after": last_sort_values
        }

    def calculate_pages(self, total_hits):
        return math.ceil(total_hits / self.page_size)
```

---

## Search History Tracking

```python
class SearchHistory:
    def __init__(self, es):
        self.es = es
        self.index = "search_history"

    async def track_search(self, user_id, query, filters, results_count):
        await self.es.index(
            index=self.index,
            document={
                "user_id": user_id,
                "query": query,
                "filters": filters,
                "results_count": results_count,
                "timestamp": datetime.now(),
                "session_id": self.get_session_id()
            }
        )

    async def get_popular_searches(self, days=7):
        return await self.es.search(
            index=self.index,
            body={
                "query": {
                    "range": {
                        "timestamp": {"gte": f"now-{days}d"}
                    }
                },
                "aggs": {
                    "popular": {
                        "terms": {"field": "query.keyword"}
                    }
                }
            }
        )
```

---

## Multi-tenancy Patterns

Three main approaches:
1. **Index per tenant**: Complete isolation
1. **Shared index with routing**: Balance
1. **Shared index with filters**: Simple

---

## Index Per Tenant

```python
class IndexPerTenantStrategy:
    def get_index_name(self, tenant_id):
        return f"tenant_{tenant_id}_products"

    def create_tenant_index(self, tenant_id):
        index_name = self.get_index_name(tenant_id)
        self.es.indices.create(
            index=index_name,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": self.get_standard_mappings()
            }
        )

    def search_tenant(self, tenant_id, query):
        return self.es.search(
            index=self.get_index_name(tenant_id),
            body=query
        )
```

---

## Shared Index with Routing

```python
class RoutingStrategy:
    def index_document(self, tenant_id, doc):
        return self.es.index(
            index="shared_products",
            routing=tenant_id,
            document={
                **doc,
                "tenant_id": tenant_id
            }
        )

    def search_tenant(self, tenant_id, query):
        return self.es.search(
            index="shared_products",
            routing=tenant_id,
            body={
                "query": {
                    "bool": {
                        "must": query,
                        "filter": {"term": {"tenant_id": tenant_id}}
                    }
                }
            }
        )
```

---

## Tenant Isolation with Aliases

```json
PUT /_aliases
{
  "actions": [
    {
      "add": {
        "index": "products_2024",
        "alias": "tenant_123_products",
        "filter": {"term": {"tenant_id": "123"}}
      }
    }
  ]
}
```

---

## Real-time Search Updates

![real_time_search_updates](/svg/courses/databases/elasticsearch-for-developers/13_app_patterns/real_time_search_updates.svg)

---

## Event-Driven Indexing

```python
import asyncio
from aiokafka import AIOKafkaConsumer

class EventIndexer:
    def __init__(self, es, kafka_config):
        self.es = es
        self.consumer = AIOKafkaConsumer(
            'product-events',
            **kafka_config
        )

    async def process_events(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                event = json.loads(msg.value)
                await self.handle_event(event)
        finally:
            await self.consumer.stop()

    async def handle_event(self, event):
        if event['type'] == 'product.created':
            await self.es.index(
                index='products',
                id=event['id'],
                document=event['data'],
                refresh='wait_for'
            )
```

---

## Change Data Capture

```python
class CDCProcessor:
    def __init__(self, es, db_connection):
        self.es = es
        self.db = db_connection

    def sync_changes(self, table, timestamp_field):
        last_sync = self.get_last_sync(table)

        query = f"""
            SELECT * FROM {table}
            WHERE {timestamp_field} > %s
            ORDER BY {timestamp_field}
        """

        changes = self.db.execute(query, [last_sync])

        bulk_actions = []
        for row in changes:
            bulk_actions.append({
                "index": {
                    "_index": table,
                    "_id": row['id']
                }
            })
            bulk_actions.append(row)

        if bulk_actions:
            self.es.bulk(body=bulk_actions)
            self.update_last_sync(table)
```

---

## Queue Integration

```python
from celery import Celery

app = Celery('search_tasks')

@app.task(max_retries=3)
def index_document(doc_id, doc_data):
    try:
        es.index(
            index='products',
            id=doc_id,
            document=doc_data
        )
    except Exception as e:
        raise self.retry(exc=e, countdown=60)

@app.task
def bulk_reindex(query_filter):
    docs = fetch_documents(query_filter)
    for batch in chunks(docs, 100):
        index_batch.delay(batch)
```

---

## Refresh Strategies

```python
class RefreshManager:
    def __init__(self, es):
        self.es = es
        self.pending_updates = []
        self.last_refresh = time.time()

    def add_update(self, update):
        self.pending_updates.append(update)

        if self.should_refresh():
            self.flush()

    def should_refresh(self):
        return (
            len(self.pending_updates) >= 100 or
            time.time() - self.last_refresh > 5
        )

    def flush(self):
        if self.pending_updates:
            self.es.bulk(body=self.pending_updates)
            self.es.indices.refresh(index='products')
            self.pending_updates = []
            self.last_refresh = time.time()
```

---

## Testing Search Functionality

```python
class SearchTestCase:
    def setup_method(self):
        self.test_index = "test_products"
        self.create_test_index()
        self.load_test_data()

    def test_text_search(self):
        results = self.search_service.search(
            query="laptop",
            filters={"category": "electronics"}
        )

        assert results['total'] > 0
        assert all(
            'laptop' in r['name'].lower()
            for r in results['hits']
        )

    def test_facet_counts(self):
        facets = self.search_service.get_facets()

        assert 'categories' in facets
        assert facets['categories']['electronics'] > 0
```

---

## Test Data Management

```python
class TestDataFactory:
    @staticmethod
    def create_product(overrides=None):
        product = {
            "id": str(uuid.uuid4()),
            "name": faker.commerce_product_name(),
            "price": random.uniform(10, 1000),
            "category": random.choice(["electronics", "books", "clothing"]),
            "in_stock": random.choice([True, False])
        }
        if overrides:
            product.update(overrides)
        return product

    @staticmethod
    def create_bulk_products(count=100):
        return [
            TestDataFactory.create_product()
            for _ in range(count)
        ]
```

---

## Search Quality Testing

```python
class SearchQualityTest:
    def __init__(self, es, test_queries):
        self.es = es
        self.test_queries = test_queries

    def evaluate_relevance(self):
        results = []
        for query in self.test_queries:
            response = self.es.search(
                index="products",
                body={"query": {"match": {"name": query['text']}}}
            )

            hits = response['hits']['hits']
            relevant = self.count_relevant(hits, query['expected'])

            results.append({
                "query": query['text'],
                "precision": relevant / len(hits) if hits else 0,
                "recall": relevant / len(query['expected'])
            })

        return results
```

---

## A/B Testing Framework

```python
class ABTestFramework:
    def __init__(self, es):
        self.es = es
        self.variants = {}

    def register_variant(self, name, search_config):
        self.variants[name] = search_config

    def get_variant(self, user_id):
        # Consistent assignment
        hash_value = hashlib.md5(user_id.encode()).hexdigest()
        return 'B' if int(hash_value, 16) % 2 == 0 else 'A'

    def execute_search(self, user_id, query):
        variant = self.get_variant(user_id)
        config = self.variants[variant]

        # Track variant
        self.track_impression(user_id, variant, query)

        return self.es.search(
            index="products",
            body=config.build_query(query)
        )
```

---

## Search Analytics

```python
class SearchAnalytics:
    def __init__(self, es):
        self.es = es

    def track_search(self, user_id, query, results_count, response_time):
        self.es.index(
            index="search_analytics",
            document={
                "user_id": user_id,
                "query": query,
                "results_count": results_count,
                "response_time": response_time,
                "timestamp": datetime.now(),
                "has_results": results_count > 0
            }
        )

    def get_zero_result_queries(self, days=7):
        return self.es.search(
            index="search_analytics",
            body={
                "query": {
                    "bool": {
                        "filter": [
                            {"term": {"has_results": False}},
                            {"range": {"timestamp": {"gte": f"now-{days}d"}}}
                        ]
                    }
                },
                "aggs": {
                    "queries": {
                        "terms": {"field": "query.keyword", "size": 100}
                    }
                }
            }
        )
```

---

## Click-through Tracking

```python
class ClickTracker:
    def track_click(self, user_id, query, result_id, position):
        self.es.index(
            index="click_events",
            document={
                "user_id": user_id,
                "query": query,
                "result_id": result_id,
                "position": position,
                "timestamp": datetime.now()
            }
        )

    def calculate_ctr(self, query):
        impressions = self.get_impressions(query)
        clicks = self.get_clicks(query)

        return {
            "query": query,
            "impressions": impressions,
            "clicks": clicks,
            "ctr": clicks / impressions if impressions > 0 else 0
        }
```

---

## Search Session Management

```python
class SearchSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.queries = []
        self.filters = {}
        self.results_viewed = []
        self.start_time = datetime.now()

    def add_query(self, query):
        self.queries.append({
            "text": query,
            "timestamp": datetime.now()
        })

    def add_filter(self, field, value):
        if field not in self.filters:
            self.filters[field] = []
        self.filters[field].append(value)

    def get_session_duration(self):
        return (datetime.now() - self.start_time).seconds
```

---

## Cache Warming

```python
class CacheWarmer:
    def __init__(self, es, cache):
        self.es = es
        self.cache = cache

    def warm_popular_queries(self):
        popular = self.get_popular_queries()

        for query in popular:
            result = self.es.search(
                index="products",
                body={"query": {"match": {"name": query}}}
            )

            cache_key = self.get_cache_key(query)
            self.cache.set(cache_key, result, ttl=3600)

    def schedule_warming(self):
        schedule.every(1).hours.do(self.warm_popular_queries)
```

---

## Error Recovery

```python
class SearchErrorHandler:
    def __init__(self, es, fallback_es):
        self.primary = es
        self.fallback = fallback_es

    def search_with_fallback(self, query):
        try:
            return self.primary.search(body=query)
        except ConnectionError:
            # Try fallback cluster
            return self.fallback.search(body=query)
        except RequestError as e:
            # Log and return empty results
            self.log_error(e)
            return self.empty_response()
```

---

## Rate Limiting

```python
from functools import wraps
import redis

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    def limit(self, key, max_requests=100, window=60):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                current = self.redis.incr(key)
                if current == 1:
                    self.redis.expire(key, window)

                if current > max_requests:
                    raise RateLimitExceeded()

                return func(*args, **kwargs)
            return wrapper
        return decorator
```

---

## Search API Versioning

```python
class SearchAPIVersionManager:
    def __init__(self):
        self.versions = {}

    def register_version(self, version, handler):
        self.versions[version] = handler

    def handle_request(self, version, request):
        if version not in self.versions:
            version = self.get_latest_version()

        handler = self.versions[version]
        return handler.process(request)

    def deprecate_version(self, version, sunset_date):
        self.versions[version].deprecated = True
        self.versions[version].sunset_date = sunset_date
```

---

## Monitoring Dashboard

```python
class SearchMonitor:
    def get_metrics(self):
        return {
            "qps": self.get_queries_per_second(),
            "avg_latency": self.get_average_latency(),
            "error_rate": self.get_error_rate(),
            "cache_hit_rate": self.get_cache_hit_rate(),
            "zero_results_rate": self.get_zero_results_rate(),
            "top_queries": self.get_top_queries(10)
        }

    def alert_on_anomaly(self, metric, threshold):
        current_value = self.get_metric_value(metric)
        if current_value > threshold:
            self.send_alert(f"{metric} exceeded threshold: {current_value}")
```

---

## Deployment Strategies

1. **Blue-Green**: Zero downtime updates
1. **Canary**: Gradual rollout
1. **Feature Flags**: Toggle features
1. **Index Versioning**: Schema migrations

---

## Index Migration Pattern

```python
class IndexMigration:
    def migrate(self, old_index, new_index, new_mappings):
        # Create new index
        self.es.indices.create(
            index=new_index,
            body={"mappings": new_mappings}
        )

        # Reindex data
        self.es.reindex(
            body={
                "source": {"index": old_index},
                "dest": {"index": new_index}
            }
        )

        # Switch alias
        self.es.indices.update_aliases(
            body={
                "actions": [
                    {"remove": {"index": old_index, "alias": "products"}},
                    {"add": {"index": new_index, "alias": "products"}}
                ]
            }
        )
```

---

## Best Practices Summary

1. Implement proper error handling
1. Use caching strategically
1. Monitor search quality metrics
1. Test with realistic data
1. Plan for scale from day one

---

## Common Anti-patterns

1. Not handling empty results
1. Ignoring search analytics
1. Over-caching stale data
1. Tight coupling to ES structure
1. Missing fallback strategies

---

## Next Steps

1. Advanced Developer Features
1. Scripting with Painless
1. Complex pipelines
1. Percolator patterns
