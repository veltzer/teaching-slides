---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# Elastic Stack Integration

---
## What This Chapter Covers

- Administering Kibana: config, spaces, and saved objects
- Building Logstash pipelines with persistent queues
- Deploying Beats: Filebeat and Metricbeat
- Elastic Agent and Fleet management
- Choosing between ingest pipelines and Logstash
- Visualization and dashboards
- Stack monitoring

---
## The Elastic Stack

- Elasticsearch is the storage and search engine
- Kibana is the UI for search, visualization, and admin
- Logstash is a heavyweight ingestion and transform pipeline
- Beats are lightweight single-purpose data shippers
- Elastic Agent unifies shippers under Fleet management
- Together they form an end-to-end observability platform

---
## Kibana Administration: kibana.yml

- Configure how Kibana connects to Elasticsearch
- Bind the server host and port for client access
- Use a dedicated `kibana_system` service account
- Enable encrypted saved objects with a persistent key
- Keep the config under version control

```yaml
server.host: "0.0.0.0"
server.port: 5601
elasticsearch.hosts: ["https://es-coord:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "${KIBANA_PASSWORD}"
xpack.encryptedSavedObjects.encryptionKey: "${ENC_KEY}"
```

---
## Kibana Spaces

- Spaces partition Kibana into isolated work areas
- Each space has its own dashboards, visualizations, and indices
- Control which features appear in each space
- Combine with roles to scope team access cleanly
- Useful for separating teams, environments, or tenants

```bash
POST kbn:/api/spaces/space
{ "id": "ops", "name": "Operations",
  "disabledFeatures": ["ml", "canvas"] }
```

---
## Kibana Saved Objects

- Dashboards, visualizations, and data views are saved objects
- Export and import them to move config between environments
- Treat exports as code: version control and review them
- Manage them under Stack Management in the UI or via API
- Saved objects carry references that must resolve on import

```bash
POST kbn:/api/saved_objects/_export
{ "type": ["dashboard"], "includeReferences": true }
```

---
## Logstash Pipeline Structure

- A pipeline has three stages: input, filter, output
- Inputs receive data (beats, kafka, file, http)
- Filters parse and enrich each event
- Outputs send events to Elasticsearch or elsewhere
- Pipelines are defined in `.conf` files under `pipelines.yml`

---
## Logstash Pipeline Example

```output
input {
  beats { port => 5044 }
}
filter {
  grok { match => { "message" => "%{COMBINEDAPACHELOG}" } }
  date { match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ] }
}
output {
  elasticsearch {
    hosts => ["https://es-coord:9200"]
    index => "weblogs-%{+YYYY.MM.dd}"
    user => "logstash_writer"
    password => "${LS_PASSWORD}"
  }
}
```

---
## Logstash Persistent Queue

- By default Logstash uses an in-memory queue
- A persistent queue buffers events on disk
- Protects against data loss on crash or backpressure
- Decouples bursty inputs from slow outputs
- Size the queue for your peak throughput and retention

```yaml
queue.type: persisted
queue.max_bytes: 4gb
path.queue: /var/lib/logstash/queue
```

---
## Beats Overview

- Lightweight Go agents that ship one type of data
- Filebeat ships log files and container logs
- Metricbeat collects system and service metrics
- Packetbeat, Auditbeat, Heartbeat cover other domains
- Beats can send directly to Elasticsearch or via Logstash

---
## Filebeat Configuration

- Define inputs pointing at log paths
- Use modules for common services (nginx, system, mysql)
- Output to Elasticsearch or to Logstash, not both
- Filebeat tracks read offsets in its registry file
- Enable modules to get parsing and dashboards for free

```yaml
filebeat.inputs:
  - type: filestream
    paths:
      - /var/log/app/*.log
output.elasticsearch:
  hosts: ["https://es-coord:9200"]
  username: "beats_writer"
  password: "${BEATS_PASSWORD}"
```

---
## Metricbeat Configuration

- Collects metrics from the host and from services
- Modules expose metricsets at configurable periods
- The system module covers CPU, memory, disk, and network
- Service modules cover Elasticsearch, Kafka, Redis, and more
- Ships to the same outputs as Filebeat

```yaml
metricbeat.modules:
  - module: system
    metricsets: [cpu, memory, network, filesystem]
    period: 10s
```

---
## Elastic Agent

- A single unified agent replacing individual Beats
- One agent collects logs, metrics, and security data
- Configured centrally through integrations, not local files
- Reduces the sprawl of per-data-type shippers
- Can run standalone or, preferably, managed by Fleet

---
## Fleet and Fleet Server

- Fleet is the central management plane inside Kibana
- Fleet Server brokers between agents and Elasticsearch
- Push policies and integrations to agents centrally
- Upgrade and monitor agents from one place
- Agents enroll with Fleet using a generated token

```bash
elastic-agent enroll \
  --url=https://fleet-server:8220 \
  --enrollment-token=${ENROLL_TOKEN}
```

---
## Integrations

- Prebuilt packages for ingesting from specific sources
- Bundle data inputs, ingest pipelines, mappings, and dashboards
- Installed from the Kibana integrations catalog
- Applied to agents through Fleet policies
- Dramatically reduce manual pipeline and dashboard work

---
## Ingest Pipelines vs Logstash

- Ingest pipelines run inside Elasticsearch on ingest nodes
- Lightweight, no extra hosts, configured via API
- Logstash runs separately and handles heavy transforms
- Use ingest pipelines for simple enrichment at scale
- Use Logstash for buffering, complex parsing, and many outputs
- Many architectures combine both as needed

---
## Ingest Pipeline Example

- Define processors that run in order on each document
- Common processors: grok, set, rename, convert, geoip
- Attach the pipeline to an index or index template
- Test the pipeline with the simulate API before use

```bash
PUT _ingest/pipeline/weblog
{
  "processors": [
    { "grok": { "field": "message",
                "patterns": ["%{COMBINEDAPACHELOG}"] } },
    { "geoip": { "field": "clientip" } }
  ]
}
```

---
## Visualization and Dashboards

- Data views (formerly index patterns) define searchable fields
- Lens is the modern drag-and-drop visualization builder
- Combine visualizations into dashboards for an overview
- Use filters and time ranges for interactive exploration
- Share dashboards or embed them in other tools
- Export dashboards as saved objects for promotion

---
## Stack Monitoring

- Monitor Elasticsearch, Kibana, Logstash, and Beats health
- Prefer Metricbeat-based collection over legacy self-monitoring
- Ship monitoring data to a separate monitoring cluster
- Watch JVM heap, GC, indexing rate, and search latency
- Set alerts on cluster health, disk usage, and node loss

```yaml
xpack.monitoring.elasticsearch.collection.enabled: false
```

---
## Stack Integration Checklist

- Kibana on a dedicated service account with an encryption key
- Spaces and roles scoped per team
- Saved objects and dashboards exported into version control
- Logstash persistent queues sized for peak load
- Beats or Elastic Agent shipping through Fleet policies
- Stack monitoring sent to a separate cluster with alerts
