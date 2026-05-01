---
tags:
  - databases:elasticsearch
  - databases:ingestion
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Data Ingestion

---
## What This Chapter Covers

- Single document ingestion
- Bulk API
- Logstash
- Beats
- Ingest pipelines
- Throughput

---
## Single Document

```http
POST /products/_doc
{ "name": "Widget", "price": 19.99 }
```

- Auto-generated ID
- Or PUT with explicit ID
- Each is a round trip

---
## Bulk API

```http
POST /_bulk
{ "index": { "_index": "products" } }
{ "name": "A", "price": 1 }
{ "index": { "_index": "products" } }
{ "name": "B", "price": 2 }
```

- Many ops in one request
- Newline-delimited JSON
- Massive throughput improvement

---
## Bulk Sizing

- 5-15MB per bulk request typical
- 1000-5000 documents
- Larger: server memory pressure
- Smaller: per-request overhead

---
## Logstash

- ETL pipeline
- Input: beats, syslog, kafka, file
- Filter: grok, mutate, geoip
- Output: elasticsearch
- Heavy; declining vs alternatives

---
## Beats

- Lightweight shippers
- Filebeat, Metricbeat, Packetbeat, Auditbeat
- Each: a focused agent
- Output to ES or Logstash

---
## Filebeat

- Tail log files
- Send to ES (or Logstash)
- Module-based for common formats
- Standard for log shipping

---
## Ingest Pipelines

- Server-side processing on ingestion
- Add fields, parse, transform
- Lighter than Logstash
- Run on ingest nodes

---
## Pipeline Example

```json
PUT /_ingest/pipeline/parse_log
{
    "processors": [
        { "grok": { "field": "message", "patterns": ["..."] } },
        { "date": { "field": "timestamp", "formats": [...] } }
    ]
}
```

---
## Direct From Application

- Application logs to a queue
- Worker consumes; bulk indexes ES
- Backpressure handling
- Standard for high-throughput apps

---
## Date-Based Indexes

- One index per day / week / month
- "logs-2026-05-01"
- Easier to drop old data
- ILM (Index Lifecycle Management) automates

---
## ILM

- Hot &#8594; warm &#8594; cold &#8594; delete
- Move from fast to slow nodes
- Save cost on old data
- Standard for log clusters

---
## Common Ingestion Mistakes

- Document-at-a-time ingestion (slow)
- Bulk too large (OOM)
- No retries on bulk rejections (data lost)
- Logstash for simple ETL when ingest pipelines would do
- No ILM (cluster fills up)
