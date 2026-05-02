---
tags:
  - databases:mongodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Change Streams and Real-Time Data

---
## What This Chapter Covers

- What change streams are
- Listening for changes
- Filtering
- Resume tokens
- Use cases
- Comparison with polling

---
## What Change Streams Are

- Subscribe to data changes
- Each change = one event
- Available since MongoDB 3.6
- Works on replica sets, sharded clusters
- Backed by oplog

---
## Change Streams Overview

![change_streams](svg/courses/databases/mongodb-for-developers/10_change_streams_and_real_time_data/change_streams.svg)

---
## Subscribing

```python
with db.users.watch() as stream:
    for change in stream:
        print(change)
```

- Blocking iterator
- Each iteration: a change event
- Run in background thread / async

---
## Event Shape

```json
{
  "_id": {...},
  "operationType": "insert",
  "ns": {"db": "...", "coll": "users"},
  "documentKey": {"_id": "..."},
  "fullDocument": {...}
}
```

- operationType: insert, update, delete, replace
- fullDocument on insert, optional otherwise

---
## Filtering

```python
pipeline = [
    {"$match": {"operationType": "insert"}}
]
db.users.watch(pipeline)
```

- Use aggregation pipeline
- Server-side filter
- Save bandwidth

---
## Resume Tokens

- Each event has a resume token
- Restart stream from a token
- Survive disconnects
- Build durable consumers

---
## Use Cases

- Real-time dashboards
- Cache invalidation
- Search indexes (sync to Elasticsearch)
- Audit trails
- Webhooks to external systems

---
## Polling vs Change Streams

- Polling: every N seconds, query for changes
- Change streams: pushed by DB
- Streams: lower latency, lower DB load
- Polling: simpler, works on standalone

---
## Per-Collection vs Per-Database

- `db.users.watch()`: one collection
- `db.watch()`: any collection in the DB
- `client.watch()`: any collection in any DB
- Pick scope appropriately

---
## Errors and Retries

- Server timeouts; network blips
- Always handle exceptions
- Use resume token to continue from where left off
- Long-running consumers: build resilient

---
## Pre / Post Images

- Update events: by default, only the change
- Optional: full pre and post images
- Required for: replication, audit
- Costs more space in oplog

---
## Limits

- Replica set required (not standalone)
- Oplog window: changes must still be in oplog
- For long disconnects: re-bootstrap data

---
## Performance

- Each watcher: a connection + cursor
- Filter at the server with pipeline
- Don't watch huge collections without filtering
- Scale: many watchers vs centralised consumer

---
## Real-World Pattern

- One service consumes change stream
- Publishes to Kafka / Pulsar
- Many downstreams subscribe
- "MongoDB &#8594; Kafka &#8594; consumers"
- Common in microservices

---
## Common Change Stream Mistakes

- Watching without filtering (too many events)
- Not handling reconnects (data loss)
- No resume token persistence
- Tightly coupling consumer to schema (changes break)
- Watching as a way to skip building proper events
