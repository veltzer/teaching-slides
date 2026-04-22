---
tags:
  - tools:elasticsearch
  - data-and-ai:search
  - data-and-ai:analytics
level: intermediate
category: database
audience:
  - audiences:developers

---
# Search Analytics and Monitoring

## Measuring and Improving Search Performance

---

## Search Analytics Overview

![search_analytics_overview](svg/courses/databases/elasticsearch-for-developers/15_analytics_monitoring/search_analytics_overview.svg)

---

## Key Search Metrics

1. **Query Volume**: Searches per second
1. **Response Time**: P50, P95, P99 latency
1. **Result Quality**: Click-through rate
1. **Zero Results**: Failed search rate
1. **User Satisfaction**: Session metrics

---

## Tracking Search Events

```python
class SearchEventTracker:
    def __init__(self, es):
        self.es = es
        self.index = "search_events"

    def track_search(self, event):
        self.es.index(
            index=self.index,
            document={
                "timestamp": datetime.now(),
                "session_id": event["session_id"],
                "user_id": event["user_id"],
                "query": event["query"],
                "filters": event["filters"],
                "results_count": event["results_count"],
                "response_time_ms": event["response_time"],
                "clicked_results": [],
                "search_type": event.get("type", "organic")
            }
        )
```

---

## Click Tracking Implementation

```javascript
class ClickTracker {
  trackClick(resultId, position, query) {
    const clickEvent = {
      timestamp: new Date(),
      session_id: this.getSessionId(),
      query: query,
      result_id: resultId,
      position: position,
      viewport_time_ms: this.getTimeInViewport(),
      action_type: "click"
    };

    // Send to analytics
    fetch('/api/analytics/click', {
      method: 'POST',
      body: JSON.stringify(clickEvent)
    });
  }

  trackImpression(results, query) {
    const impressions = results.map((r, i) => ({
      result_id: r.id,
      position: i + 1
    }));

    this.sendEvent('impression', {query, impressions});
  }
}
```

---

## Click-Through Rate Calculation

```python
def calculate_ctr(self, time_range="7d"):
    response = self.es.search(
        index="search_events",
        body={
            "query": {
                "range": {
                    "timestamp": {"gte": f"now-{time_range}"}
                }
            },
            "aggs": {
                "queries": {
                    "terms": {
                        "field": "query.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "total_searches": {"value_count": {"field": "query"}},
                        "with_clicks": {
                            "filter": {
                                "exists": {"field": "clicked_results"}
                            }
                        }
                    }
                }
            }
        }
    )

    return self.process_ctr_results(response)
```

---

## Zero Results Analysis

```python
class ZeroResultsAnalyzer:
    def identify_zero_results(self):
        return self.es.search(
            index="search_events",
            body={
                "query": {
                    "bool": {
                        "filter": [
                            {"term": {"results_count": 0}},
                            {"range": {"timestamp": {"gte": "now-24h"}}}
                        ]
                    }
                },
                "aggs": {
                    "failed_queries": {
                        "terms": {
                            "field": "query.keyword",
                            "size": 50
                        }
                    },
                    "by_category": {
                        "terms": {
                            "field": "filters.category.keyword"
                        }
                    }
                }
            }
        )
```

---

## Zero Results Analysis: Suggestions

```python
class ZeroResultsAnalyzer:
    def suggest_improvements(self, zero_result_queries):
        suggestions = []
        for query in zero_result_queries:
            # Check for typos
            if self.has_similar_successful_query(query):
                suggestions.append({
                    "query": query,
                    "suggestion": "Add fuzzy matching"
                })
            # Check for synonyms
            elif self.could_benefit_from_synonyms(query):
                suggestions.append({
                    "query": query,
                    "suggestion": "Add synonyms"
                })
        return suggestions
```

---

## Popular Queries Tracking

```python
def get_trending_queries(self, hours=24):
    current = self.es.search(
        index="search_events",
        body={
            "query": {
                "range": {"timestamp": {"gte": f"now-{hours}h"}}
            },
            "aggs": {
                "popular": {
                    "terms": {
                        "field": "query.keyword",
                        "size": 20
                    }
                }
            }
        }
    )

    previous = self.es.search(
        index="search_events",
        body={
            "query": {
                "range": {
                    "timestamp": {
                        "gte": f"now-{hours*2}h",
                        "lt": f"now-{hours}h"
                    }
                }
            },
            "aggs": {
                "popular": {
                    "terms": {"field": "query.keyword", "size": 20}
                }
            }
        }
    )

    return self.calculate_trends(current, previous)
```

---

## Search Session Analysis

```python
class SessionAnalyzer:
    def analyze_session(self, session_id):
        events = self.es.search(
            index="search_events",
            body={
                "query": {"term": {"session_id": session_id}},
                "sort": [{"timestamp": "asc"}]
            }
        )

        return {
            "session_id": session_id,
            "duration_seconds": self.calculate_duration(events),
            "searches_count": len(events["hits"]["hits"]),
            "refinements": self.count_refinements(events),
            "successful": self.has_successful_outcome(events),
            "path": self.extract_search_path(events)
        }

    def calculate_session_metrics(self):
        return {
            "avg_searches_per_session": 3.2,
            "avg_session_duration": 180,
            "refinement_rate": 0.45,
            "success_rate": 0.72
        }
```

---

## Query Performance Monitoring

```python
class PerformanceMonitor:
    def __init__(self, es):
        self.es = es
        self.thresholds = {
            "fast": 100,
            "acceptable": 500,
            "slow": 1000
        }

    def categorize_performance(self):
        return self.es.search(
            index="search_events",
            body={
                "aggs": {
                    "performance_buckets": {
                        "range": {
                            "field": "response_time_ms",
                            "ranges": [
                                {"key": "fast", "to": 100},
                                {"key": "acceptable", "from": 100, "to": 500},
                                {"key": "slow", "from": 500, "to": 1000},
                                {"key": "very_slow", "from": 1000}
                            ]
                        }
                    },
                    "percentiles": {
                        "percentiles": {
                            "field": "response_time_ms",
                            "percents": [50, 75, 90, 95, 99]
                        }
                    }
                }
            }
        )
```

---

## Slow Query Logging

```json
PUT /products/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.query.debug": "2s",
  "index.search.slowlog.threshold.query.trace": "500ms",
  "index.search.slowlog.threshold.fetch.warn": "1s",
  "index.search.slowlog.level": "info"
}
```

---

## Analyzing Slow Logs

```python
def parse_slow_logs(self, log_file):
    slow_queries = []

    with open(log_file, 'r') as f:
        for line in f:
            if 'slowlog.query' in line:
                match = re.search(
                    r'took\[([0-9.]+)ms\].*source\[(.*?)\]',
                    line
                )
                if match:
                    slow_queries.append({
                        'duration_ms': float(match.group(1)),
                        'query': json.loads(match.group(2)),
                        'timestamp': self.extract_timestamp(line)
                    })

    return self.analyze_patterns(slow_queries)
```

---

## A/B Testing Framework

```python
class ABTestManager:
    def __init__(self, es):
        self.es = es
        self.tests = {}

    def create_test(self, test_name, variants):
        self.tests[test_name] = {
            "created_at": datetime.now(),
            "variants": variants,
            "metrics": ["ctr", "conversion", "revenue"]
        }

    def assign_variant(self, user_id, test_name):
        hash_val = hashlib.md5(
            f"{user_id}{test_name}".encode()
        ).hexdigest()

        variant_index = int(hash_val, 16) % len(
            self.tests[test_name]["variants"]
        )

        return self.tests[test_name]["variants"][variant_index]

    def track_conversion(self, user_id, test_name, value=1.0):
        variant = self.assign_variant(user_id, test_name)

        self.es.index(
            index="ab_test_events",
            document={
                "test_name": test_name,
                "variant": variant,
                "user_id": user_id,
                "event_type": "conversion",
                "value": value,
                "timestamp": datetime.now()
            }
        )
```

---

## A/B Test Analysis

```python
def analyze_ab_test(self, test_name, metric="ctr"):
    results = self.es.search(
        index="ab_test_events",
        body={
            "query": {"term": {"test_name": test_name}},
            "aggs": {
                "variants": {
                    "terms": {"field": "variant.keyword"},
                    "aggs": {
                        "conversions": {
                            "filter": {"term": {"event_type": "conversion"}}
                        },
                        "impressions": {
                            "filter": {"term": {"event_type": "impression"}}
                        },
                        "ctr": {
                            "bucket_script": {
                                "buckets_path": {
                                    "clicks": "conversions._count",
                                    "views": "impressions._count"
                                },
                                "script": "params.clicks / params.views * 100"
                            }
                        }
                    }
                }
            }
        }
    )

    return self.calculate_significance(results)
```

---

## Statistical Significance

```python
import scipy.stats as stats

def calculate_significance(self, control, variant):
    # Calculate conversion rates
    control_rate = control["conversions"] / control["visitors"]
    variant_rate = variant["conversions"] / variant["visitors"]

    # Pooled probability
    pooled = (control["conversions"] + variant["conversions"]) / \
             (control["visitors"] + variant["visitors"])

    # Standard error
    se = math.sqrt(pooled * (1 - pooled) *
                   (1/control["visitors"] + 1/variant["visitors"]))

    # Z-score
    z_score = (variant_rate - control_rate) / se

    # P-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    return {
        "control_rate": control_rate,
        "variant_rate": variant_rate,
        "lift": (variant_rate - control_rate) / control_rate * 100,
        "p_value": p_value,
        "significant": p_value < 0.05
    }
```

---

## Search Quality Metrics

```python
class SearchQualityMetrics:
    def calculate_ndcg(self, results, relevance_scores):
        """Normalized Discounted Cumulative Gain"""
        dcg = sum(
            (2**rel - 1) / math.log2(i + 2)
            for i, rel in enumerate(relevance_scores)
        )

        ideal_scores = sorted(relevance_scores, reverse=True)
        idcg = sum(
            (2**rel - 1) / math.log2(i + 2)
            for i, rel in enumerate(ideal_scores)
        )

        return dcg / idcg if idcg > 0 else 0

    def calculate_map(self, queries_results):
        """Mean Average Precision"""
        ap_scores = []

        for query, results in queries_results.items():
            relevant_found = 0
            precision_sum = 0

            for i, result in enumerate(results):
                if result["relevant"]:
                    relevant_found += 1
                    precision_sum += relevant_found / (i + 1)

            if relevant_found > 0:
                ap_scores.append(precision_sum / relevant_found)

        return sum(ap_scores) / len(ap_scores) if ap_scores else 0
```

---

## User Feedback Collection

```python
class FeedbackCollector:
    def collect_explicit_feedback(self, user_id, query, result_id, rating):
        self.es.index(
            index="search_feedback",
            document={
                "user_id": user_id,
                "query": query,
                "result_id": result_id,
                "rating": rating,  # 1-5 stars
                "timestamp": datetime.now(),
                "type": "explicit"
            }
        )

    def collect_implicit_feedback(self, user_id, query, result_id, action):
        feedback_weight = {
            "click": 1.0,
            "add_to_cart": 2.0,
            "purchase": 3.0,
            "bookmark": 1.5,
            "share": 2.0
        }

        self.es.index(
            index="search_feedback",
            document={
                "user_id": user_id,
                "query": query,
                "result_id": result_id,
                "action": action,
                "weight": feedback_weight.get(action, 1.0),
                "timestamp": datetime.now(),
                "type": "implicit"
            }
        )
```

---

## Real-time Dashboard

```python
class SearchDashboard:
    def get_real_time_metrics(self):
        return {
            "current_qps": self.get_queries_per_second(),
            "active_users": self.get_active_users_count(),
            "avg_response_time": self.get_avg_response_time("1m"),
            "error_rate": self.get_error_rate("1m"),
            "top_queries": self.get_top_queries("1h", limit=10),
            "alerts": self.check_alerts()
        }

    def get_queries_per_second(self):
        response = self.es.search(
            index="search_events",
            body={
                "query": {
                    "range": {"timestamp": {"gte": "now-1m"}}
                },
                "aggs": {
                    "qps": {
                        "date_histogram": {
                            "field": "timestamp",
                            "fixed_interval": "1s"
                        }
                    }
                }
            }
        )

        buckets = response["aggregations"]["qps"]["buckets"]
        return sum(b["doc_count"] for b in buckets) / len(buckets)
```

---

## Alert Configuration

```python
class AlertManager:
    def __init__(self):
        self.alerts = [
            {
                "name": "high_response_time",
                "condition": lambda m: m["p95_latency"] > 1000,
                "message": "P95 latency exceeds 1 second"
            },
            {
                "name": "low_ctr",
                "condition": lambda m: m["ctr"] < 0.1,
                "message": "Click-through rate below 10%"
            },
            {
                "name": "high_zero_results",
                "condition": lambda m: m["zero_results_rate"] > 0.2,
                "message": "Zero results rate above 20%"
            }
        ]

    def check_alerts(self, metrics):
        triggered = []
        for alert in self.alerts:
            if alert["condition"](metrics):
                triggered.append({
                    "name": alert["name"],
                    "message": alert["message"],
                    "timestamp": datetime.now()
                })
                self.send_notification(alert)
        return triggered
```

---

## Query Expansion Analysis

```python
def analyze_query_expansions(self):
    """Track how users refine their queries"""
    sessions = self.es.search(
        index="search_events",
        body={
            "aggs": {
                "sessions": {
                    "terms": {"field": "session_id.keyword"},
                    "aggs": {
                        "queries": {
                            "top_hits": {
                                "size": 10,
                                "_source": ["query", "timestamp"],
                                "sort": [{"timestamp": "asc"}]
                            }
                        }
                    }
                }
            }
        }
    )

    expansion_patterns = []
    for session in sessions["aggregations"]["sessions"]["buckets"]:
        queries = [h["_source"]["query"]
                  for h in session["queries"]["hits"]["hits"]]

        if len(queries) > 1:
            expansion_patterns.append({
                "original": queries[0],
                "refinements": queries[1:],
                "pattern": self.classify_refinement(queries)
            })

    return expansion_patterns
```

---

## Search Funnel Analysis

![search_funnel_analysis](svg/courses/databases/elasticsearch-for-developers/15_analytics_monitoring/search_funnel_analysis.svg)

---

## Funnel Metrics Code

```python
def calculate_search_funnel(self, session_ids):
    funnel = {
        "searched": 0,
        "clicked": 0,
        "added_to_cart": 0,
        "purchased": 0
    }

    for session_id in session_ids:
        events = self.get_session_events(session_id)

        if any(e["type"] == "search" for e in events):
            funnel["searched"] += 1

            if any(e["type"] == "click" for e in events):
                funnel["clicked"] += 1

                if any(e["type"] == "add_to_cart" for e in events):
                    funnel["added_to_cart"] += 1

                    if any(e["type"] == "purchase" for e in events):
                        funnel["purchased"] += 1

    return self.calculate_conversion_rates(funnel)
```

---

## Personalization Tracking

```python
class PersonalizationMetrics:
    def measure_personalization_impact(self):
        personalized = self.es.search(
            index="search_events",
            body={
                "query": {"term": {"personalized": True}},
                "aggs": {
                    "ctr": {
                        "avg": {"field": "click_through_rate"}
                    }
                }
            }
        )

        non_personalized = self.es.search(
            index="search_events",
            body={
                "query": {"term": {"personalized": False}},
                "aggs": {
                    "ctr": {
                        "avg": {"field": "click_through_rate"}
                    }
                }
            }
        )

        return {
            "personalized_ctr": personalized["aggregations"]["ctr"]["value"],
            "standard_ctr": non_personalized["aggregations"]["ctr"]["value"],
            "improvement": self.calculate_improvement(
                personalized, non_personalized
            )
        }
```

---

## Mobile vs Desktop Analysis

```python
def compare_platforms(self):
    return self.es.search(
        index="search_events",
        body={
            "aggs": {
                "platforms": {
                    "terms": {"field": "platform.keyword"},
                    "aggs": {
                        "avg_response_time": {
                            "avg": {"field": "response_time_ms"}
                        },
                        "ctr": {
                            "avg": {"field": "click_through_rate"}
                        },
                        "conversion_rate": {
                            "avg": {"field": "conversion_rate"}
                        },
                        "bounce_rate": {
                            "avg": {"field": "bounce_rate"}
                        }
                    }
                }
            }
        }
    )
```

---

## Geographic Analysis

```python
def analyze_by_region(self):
    return self.es.search(
        index="search_events",
        body={
            "aggs": {
                "regions": {
                    "terms": {"field": "user_location.country.keyword"},
                    "aggs": {
                        "popular_queries": {
                            "terms": {"field": "query.keyword", "size": 5}
                        },
                        "avg_session_duration": {
                            "avg": {"field": "session_duration_seconds"}
                        },
                        "peak_hours": {
                            "date_histogram": {
                                "field": "timestamp",
                                "calendar_interval": "hour"
                            }
                        }
                    }
                }
            }
        }
    )
```

---

## Error Rate Monitoring

```python
class ErrorMonitor:
    def track_errors(self):
        return self.es.search(
            index="search_events",
            body={
                "query": {
                    "range": {"timestamp": {"gte": "now-1h"}}
                },
                "aggs": {
                    "error_types": {
                        "terms": {"field": "error_type.keyword"},
                        "aggs": {
                            "over_time": {
                                "date_histogram": {
                                    "field": "timestamp",
                                    "fixed_interval": "5m"
                                }
                            }
                        }
                    },
                    "error_rate": {
                        "filters": {
                            "filters": {
                                "errors": {"exists": {"field": "error"}},
                                "success": {"bool": {"must_not": {"exists": {"field": "error"}}}}
                            }
                        }
                    }
                }
            }
        )
```

---

## Relevance Feedback Loop

```python
class RelevanceFeedbackLoop:
    def update_relevance_signals(self):
        # Collect positive signals
        positive_signals = self.es.search(
            index="search_feedback",
            body={
                "query": {
                    "bool": {
                        "filter": [
                            {"range": {"timestamp": {"gte": "now-7d"}}},
                            {"range": {"rating": {"gte": 4}}}
                        ]
                    }
                },
                "aggs": {
                    "query_doc_pairs": {
                        "composite": {
                            "sources": [
                                {"query": {"terms": {"field": "query.keyword"}}},
                                {"doc": {"terms": {"field": "result_id.keyword"}}}
                            ]
                        }
                    }
                }
            }
        )

        # Update boost values
        for pair in positive_signals["aggregations"]["query_doc_pairs"]["buckets"]:
            self.update_document_boost(
                pair["key"]["doc"],
                pair["key"]["query"],
                pair["doc_count"]
            )
```

---

## Search Experimentation

```python
class SearchExperiment:
    def __init__(self, name, hypothesis, metrics):
        self.name = name
        self.hypothesis = hypothesis
        self.metrics = metrics
        self.start_time = datetime.now()

    def run_experiment(self, duration_days=14):
        control_config = self.get_current_config()
        treatment_config = self.apply_changes(control_config)

        # Run for specified duration
        while (datetime.now() - self.start_time).days < duration_days:
            user_id = self.get_current_user()
            variant = self.assign_to_variant(user_id)

            if variant == "treatment":
                results = self.search_with_config(treatment_config)
            else:
                results = self.search_with_config(control_config)

            self.track_metrics(user_id, variant, results)

        return self.analyze_results()
```

---

## Reporting Dashboard

```python
def generate_weekly_report(self):
    return {
        "period": "last_7_days",
        "summary": {
            "total_searches": self.get_total_searches("7d"),
            "unique_users": self.get_unique_users("7d"),
            "avg_ctr": self.get_average_ctr("7d"),
            "zero_results_rate": self.get_zero_results_rate("7d")
        },
        "trends": {
            "search_volume": self.get_volume_trend("7d"),
            "popular_queries": self.get_trending_queries("7d"),
            "emerging_queries": self.get_emerging_queries("7d")
        },
        "quality": {
            "slow_queries": self.get_slow_queries("7d"),
            "failed_queries": self.get_failed_queries("7d"),
            "improvement_opportunities": self.get_opportunities()
        },
        "recommendations": self.generate_recommendations()
    }
```

---

## Optimization Recommendations

```python
def generate_recommendations(self, analytics_data):
    recommendations = []

    # Check zero results rate
    if analytics_data["zero_results_rate"] > 0.15:
        recommendations.append({
            "priority": "high",
            "type": "content_gap",
            "action": "Add missing content for top zero-result queries",
            "queries": analytics_data["top_zero_results"]
        })

    # Check slow queries
    if analytics_data["p95_latency"] > 500:
        recommendations.append({
            "priority": "high",
            "type": "performance",
            "action": "Optimize slow queries",
            "queries": analytics_data["slowest_queries"]
        })

    # Check CTR
    if analytics_data["avg_ctr"] < 0.2:
        recommendations.append({
            "priority": "medium",
            "type": "relevance",
            "action": "Improve result relevance",
            "suggestions": ["Add synonyms", "Tune boosting", "Improve analyzers"]
        })

    return recommendations
```

---

## Continuous Improvement

![continuous_improvement](svg/courses/databases/elasticsearch-for-developers/15_analytics_monitoring/continuous_improvement.svg)

---

## Best Practices

1. Track everything but sample wisely
1. Focus on actionable metrics
1. Automate reporting and alerts
1. Run continuous experiments
1. Close the feedback loop
