---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# High Availability

---
## What This Chapter Covers

- Designing for resilience across availability zones
- Multi-datacenter deployment options and their limits
- Cross-cluster search and remote clusters
- Failover and load-balancing strategies
- Network resilience and fault detection tuning
- Disaster recovery testing
- Zero-downtime operations

---
## High Availability Goals

- Survive node, rack, and zone failures without data loss
- Keep the cluster searchable during component outages
- Maintain a stable master quorum at all times
- Recover automatically rather than via manual intervention
- Balance availability against cost and complexity
- HA is a property of design, not a single setting

---
## Replicas Are the Foundation

- At least one replica per primary for any HA cluster
- A replica must live on a different node than its primary
- Replicas serve search traffic and survive node loss
- Yellow health means replicas are missing — fix it promptly
- More replicas raise read throughput and resilience, at storage cost

```bash
PUT logs-*/_settings
{ "index.number_of_replicas": 1 }
```

---
## Dedicated Master Nodes

- Separate master-eligible nodes from data and ingest roles
- Masters manage cluster state, not search or indexing load
- Run exactly three dedicated masters for production HA
- Three masters tolerate the loss of one and keep quorum
- Isolating masters keeps the cluster stable under data-node stress

```yaml
node.roles: [ master ]
```

---
## Quorum and Voting

- The master quorum requires a majority of voting nodes
- Three master-eligible nodes need two online to elect a master
- Losing quorum makes the cluster read-only and unmanageable
- Never run two master-eligible nodes — that splits the vote
- Voting configuration is managed automatically by Elasticsearch

```bash
GET _cluster/state/metadata?filter_path=metadata.cluster_coordination
```

---
## Zone Awareness

- Shard allocation awareness spreads copies across zones
- Tag each node with its zone attribute
- Elasticsearch then keeps primary and replica in different zones
- Forced awareness reserves capacity for a full zone outage
- A zone failure leaves a complete copy of every shard

```yaml
node.attr.zone: us-east-1a
cluster.routing.allocation.awareness.attributes: zone
cluster.routing.allocation.awareness.force.zone.values: us-east-1a,us-east-1b,us-east-1c
```

---
## Quorum Across Three Zones

- Place one dedicated master in each of three zones
- Any single zone can fail and quorum survives
- Data nodes spread across the same three zones
- One replica plus three zones guarantees a surviving copy
- Two zones is not enough — losing one can lose quorum

---
## Why Not Stretch One Cluster Far

- A single cluster assumes low, stable inter-node latency
- The master heartbeats and replicates state continuously
- High-latency links cause false node failures and instability
- Network partitions across regions can break quorum
- Keep one cluster within a single low-latency region or metro
- Span regions with separate clusters plus replication, not one cluster

---
## Multi-Datacenter Options

- One cluster across nearby AZs in a single region: supported
- One cluster across distant regions: discouraged, fragile
- Independent clusters per region linked by CCR: recommended
- Cross-cluster search to query multiple clusters as one
- Choose based on latency, sovereignty, and RPO/RTO targets

---
## Remote Clusters

- Register another cluster as a named remote
- Foundation for cross-cluster search and replication
- Uses sniff or proxy connection modes
- Survives independent failure of either cluster
- Configure via cluster settings or `elasticsearch.yml`

```bash
PUT _cluster/settings
{
  "persistent": {
    "cluster.remote.dc_west.seeds": [ "10.0.2.10:9300" ]
  }
}
```

---
## Cross-Cluster Search

- Query indices on local and remote clusters in one request
- Prefix the index with the remote cluster name and a colon
- Each remote cluster executes its part and returns results
- Lets a single Kibana span multiple regional clusters
- Tune `skip_unavailable` so one remote outage is non-fatal

```bash
GET dc_west:logs-*,logs-*/_search
{ "query": { "match": { "level": "ERROR" } } }
```

---
## Failover Strategies

- Within a cluster, replicas fail over automatically on node loss
- Across clusters, use CCR to keep a warm standby in another region
- Promote a follower index to leader during a region failover
- Define clear RPO (data loss window) and RTO (recovery time)
- Document and rehearse the manual promotion steps

```bash
POST follower-logs/_ccr/pause_follow
POST follower-logs/_close
POST follower-logs/_ccr/unfollow
```

---
## Load Balancing With Coordinating Nodes

- Coordinating-only nodes route requests and merge results
- They offload search coordination from data nodes
- Place a load balancer in front of coordinating nodes
- Clients connect to the balancer, not to individual data nodes
- Scale coordinating nodes for heavy aggregation workloads

```yaml
node.roles: [ ]
```

---
## Client-Side Round Robin

- Official clients can hold a list of node addresses
- Requests are distributed round-robin across the list
- Clients sniff the cluster to discover nodes automatically
- Dead nodes are marked and skipped, then retried later
- Combine with a load balancer for layered resilience

```python
es = Elasticsearch(
    ["https://es1:9200", "https://es2:9200", "https://es3:9200"],
    sniff_on_start=True, sniff_on_node_failure=True)
```

---
## Network Resilience and Fault Detection

- The master pings nodes to detect failures (follower checks)
- Nodes ping the master to detect its loss (leader checks)
- Tune timeouts and retries for your network characteristics
- Too aggressive: false failures; too lax: slow detection
- Stable networks should keep defaults

```yaml
cluster.fault_detection.follower_check.interval: 1s
cluster.fault_detection.follower_check.timeout: 10s
cluster.fault_detection.follower_check.retry_count: 3
```

---
## Request Timeouts and Retries

- Set sensible timeouts on client requests to fail fast
- Use bulk retries with backoff for transient indexing errors
- Idempotent operations are safe to retry; design for it
- Circuit breakers protect nodes from memory exhaustion
- Monitor rejected tasks in the thread-pool queues

```bash
GET _cat/thread_pool/search,write?v&h=node_name,name,active,queue,rejected
```

---
## Disaster Recovery Testing

- An untested DR plan is not a plan
- Regularly restore snapshots into an isolated test cluster
- Rehearse CCR follower promotion to a standby region
- Run game-day exercises: kill a node, then a whole zone
- Measure actual RTO and RPO against your targets
- Document gaps and fix them before a real incident

---
## Zero-Downtime Operations

- Use rolling restarts so the cluster stays available
- Disable allocation only for the node being worked on
- Use index aliases to swap indices without client changes
- Reindex into a new index, then atomically repoint the alias
- Roll over time-series indices instead of mutating in place

```bash
POST _aliases
{ "actions": [
  { "remove": { "index": "app-v1", "alias": "app" } },
  { "add":    { "index": "app-v2", "alias": "app" } }
] }
```

---
## High Availability Checklist

- At least one replica, allocated across zones
- Exactly three dedicated masters, one per zone
- Allocation awareness configured and forced
- Coordinating nodes behind a load balancer
- CCR standby for cross-region disaster recovery
- DR drills scheduled and RTO/RPO validated

```bash
GET _cluster/health?level=indices
```
