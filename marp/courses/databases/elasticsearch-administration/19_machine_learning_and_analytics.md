---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# Machine Learning and Analytics

---
## What This Chapter Covers

- Machine learning features and anomaly detection
- Datafeeds, jobs, and dedicated ML nodes
- Transforms for entity-centric indices
- Pivot, latest, and continuous transforms
- Operating transforms: checkpointing and scheduling
- Graph analytics for connected data
- ML node sizing and job lifecycle for operators

---
## ML and Analytics for Operators

- ML features find patterns and anomalies without manual rules
- Transforms reshape raw event data into summary indices
- Graph analytics explores relationships between terms
- These are compute-heavy and belong on the right node roles
- As a DBA you manage capacity, lifecycle, and results storage
- Treat ML jobs and transforms as long-running stateful services

---
## ML Nodes

- ML work runs only on nodes with the `ml` role
- Anomaly detection and inference both consume ML node memory
- Native processes run off-heap, so size total RAM, not just heap

```yaml
node.roles: [ ml, remote_cluster_client ]
xpack.ml.enabled: true
```

- `xpack.ml.max_machine_memory_percent` caps ML memory use
- Isolate ML nodes so heavy jobs do not starve search and indexing

---
## Anomaly Detection: Concepts

- Anomaly detection learns a baseline, then flags deviations
- A job defines the analysis; a datafeed supplies the data
- The model adapts over time as new data arrives
- `bucket_span` sets the analysis granularity
- `detectors` define what metric and function to model
- Results carry an `anomaly_score` and `record_score`

---
## Defining an Anomaly Detection Job

- The job config sets buckets, detectors, and the field to influence

```json
PUT _ml/anomaly_detectors/response_times
{
  "analysis_config": {
    "bucket_span": "15m",
    "detectors": [
      { "function": "mean", "field_name": "response_ms",
        "by_field_name": "service" }
    ]
  },
  "data_description": { "time_field": "@timestamp" }
}
```

- `by_field_name` models each service independently
- Functions include `mean`, `max`, `count`, and `rare`

---
## Datafeeds

- A datafeed queries source indices and streams data to the job
- It can run over history and then continue in real time

```json
PUT _ml/datafeeds/datafeed-response_times
{
  "job_id": "response_times",
  "indices": ["metrics-*"],
  "query": { "match_all": {} }
}
```

- Start it to begin analysis; end times can be open for live feeds

```bash
POST _ml/datafeeds/datafeed-response_times/_start
```

- A real-time datafeed runs on the configured `frequency`

---
## Job Lifecycle

- Open a job to load its model into memory before running
- Start the datafeed to feed data; stop it to pause analysis
- Close the job to release ML node memory when idle

```bash
POST _ml/anomaly_detectors/response_times/_open
POST _ml/datafeeds/datafeed-response_times/_stop
POST _ml/anomaly_detectors/response_times/_close
```

- Open jobs hold memory even when no data flows
- Close jobs you are not actively using to free capacity

---
## Anomaly Results

- Results are written to internal `.ml-anomalies-*` indices
- Query them through the results API, not the raw indices

```bash
GET _ml/anomaly_detectors/response_times/results/buckets
{ "anomaly_score": 75 }
```

- `bucket` results summarize anomalies per time bucket
- `record` results pinpoint the specific anomalous entities
- Drive alerting off `anomaly_score` thresholds

---
## ML Node Sizing

- Each open job reserves a model memory limit on an ML node
- `model_memory_limit` defaults adapt to data but can be set explicitly

```json
PUT _ml/anomaly_detectors/big_job
{ "analysis_limits": { "model_memory_limit": "1024mb" } }
```

- Total open jobs must fit within the ML memory budget per node
- High-cardinality `by` and `partition` fields inflate model memory
- Plan ML node count from the sum of all concurrent job limits

---
## Transforms: Concepts

- Transforms turn event streams into entity-centric indices
- A pivot transform groups and aggregates into one doc per entity
- A latest transform keeps the most recent doc per entity
- Output goes to a normal index you can search and visualize
- Transforms can run once or continuously on a schedule
- They are ideal for building summary and reporting indices

---
## A Pivot Transform

- Group by an entity, then aggregate metrics per group

```json
PUT _transform/customer_summary
{
  "source": { "index": "orders-*" },
  "dest": { "index": "customer_summary" },
  "pivot": {
    "group_by": { "customer": { "terms": { "field": "customer_id" } } },
    "aggregations": {
      "total_spent": { "sum": { "field": "amount" } },
      "order_count": { "value_count": { "field": "order_id" } }
    }
  }
}
```

- The destination holds one summarized document per customer

---
## Continuous Transforms

- A continuous transform keeps the destination up to date
- It needs a time field as the sync marker and a check interval

```json
"sync": {
  "time": { "field": "@timestamp", "delay": "60s" }
},
"frequency": "1m"
```

- `delay` allows for late-arriving data before processing a window
- `frequency` controls how often it checks for new source data
- Only changed entities are recomputed on each run

---
## Operating Transforms: Checkpointing

- A transform advances through numbered checkpoints
- Each checkpoint processes the source changes since the last one
- Checkpoint state lets a transform resume after a restart

```bash
GET _transform/customer_summary/_stats
```

- Stats show `checkpointing`, processed docs, and any failures
- A growing gap between source and last checkpoint means it is behind
- Scale source query efficiency or `frequency` if it lags

---
## Transform Lifecycle

- Create, then start a transform to begin processing
- Stop it to pause; it resumes from its last checkpoint

```bash
POST _transform/customer_summary/_start
POST _transform/customer_summary/_stop
```

- Transforms run on `transform`-role nodes
- A failed transform stops; inspect stats, fix, then restart
- Never edit the destination index directly under a running transform

---
## Graph Analytics

- Graph analytics finds significantly connected terms
- It surfaces relationships rather than raw frequency
- Useful for recommendations, fraud links, and term associations

```json
POST /clickstream/_graph/explore
{
  "query": { "match": { "query.raw": "elasticsearch" } },
  "vertices": [ { "field": "product" } ],
  "connections": { "vertices": [ { "field": "category" } ] }
}
```

- Vertices are terms; connections are the links between them
- Significance scoring filters out merely popular but unrelated terms

---
## ML and Analytics Checklist

- Run ML and transforms on dedicated node roles
- Size ML nodes from the sum of open job memory limits
- Close anomaly jobs you are not using to free memory
- Alert on `anomaly_score` from the results API
- Use pivot transforms for entity summaries, latest for newest state
- Watch transform checkpointing stats for lag and failures
- Let transforms own their destination indices exclusively
