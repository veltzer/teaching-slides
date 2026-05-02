---
tags:
  - databases:elasticsearch
  - practices:observability
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Search Analytics and Monitoring

---
## What This Chapter Covers

- Search logs
- A/B testing
- Cluster health metrics
- Index stats
- Alerting
- Tools

---
## Search Logs

- Log every search (or sample)
- query, user, time, result count
- Find: zero-result queries, slow queries
- Drives UX improvements

---
## Analytics Dimensions

![search_analytics](svg/courses/databases/elasticsearch-for-developers/15_search_analytics_and_monitoring/search_analytics.svg)

---
## Zero-Result Queries

- Surface gaps: missing inventory, typos
- "I searched for 'iphone' and got nothing"
- Fix: add synonyms, content, redirects

---
## Click-Through Rate

- Did users click any result?
- Per-query, per-position
- Low CTR: bad ranking
- Improve: tune relevance

---
## Search A/B Testing

- Two ranking functions
- Random assignment
- Compare: CTR, conversion
- Roll out winner

---
## Cluster Health

- GET _cluster/health
- Status: green / yellow / red
- Active shards, unassigned shards
- Monitor; alert on yellow / red

---
## Cat APIs

- Compact, table-formatted output
- `_cat/indices`, `_cat/shards`, `_cat/nodes`
- Quick ops checks
- Less verbose than JSON

---
## Node Stats

- `GET _nodes/stats`
- CPU, memory, heap, GC
- File system, OS
- Detailed; lots of metrics

---
## Index Stats

- GET /index/_stats
- Documents count, size, query count
- Per-shard stats
- For: capacity planning

---
## Hot Threads

- `GET _nodes/hot_threads`
- Top CPU users at this moment
- Find slow query culprits
- Operational diagnosis tool

---
## Slow Logs

- Log queries / indexing slower than threshold
- Per-index configuration
- Find unintended slow operations

---
## Kibana Stack Monitoring

- Built-in cluster monitoring
- Time-series of all the metrics
- Standard ops dashboard
- Free in basic license

---
## Prometheus Exporter

- elasticsearch_exporter
- Scrape metrics into Prometheus
- Dashboard in Grafana
- For non-Kibana stacks

---
## Alerting

- Alert on: cluster red, high latency, low disk
- Watcher (commercial), Kibana alerting (basic)
- Or: external (Prometheus, Datadog)

---
## Common Monitoring Mistakes

- No slow log
- No alert on cluster health
- Tracking only response time, not throughput
- No search logs (no learning loop)
- Ignoring zero-result queries
