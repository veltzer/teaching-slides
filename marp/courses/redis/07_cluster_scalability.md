# Redis Cluster and Scalability

---

## Redis Scalability Challenges

As data and traffic grow, single Redis instances face limitations:

- **Memory capacity**: Single instance memory limit
- **Throughput**: CPU becomes bottleneck
- **Network bandwidth**: Connection saturation
- **Single point of failure**: Reliability concerns

Scaling strategies:
- **Vertical scaling**: Larger server (limited)
- **Horizontal scaling**: Multiple servers
- **Functional partitioning**: Separate instances by function
- **Data partitioning**: Divide data across instances

---

## Redis Scaling Architectures

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd0_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Master-Replica Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd1_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- Master handles all writes
- Replicas handle read queries
- Read scaling only (not write scaling)
- Provides high availability
- Limited by master's capacity

---

## Client-Side Partitioning

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd2_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- Application determines which Redis instance to use
- Consistent hashing or modulo-based distribution
- Simple to implement
- No additional infrastructure
- Drawbacks: Client complexity, inconsistent distribution

---

## Proxy-Based Partitioning

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd3_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- Proxy handles routing (Twemproxy, Envoy, Nginx)
- Transparent to clients
- Connection pooling
- Centralized monitoring
- Drawbacks: Additional network hop, maintenance

---

## Introduction to Redis Cluster

Redis Cluster is the official Redis distributed solution:

- Native, server-side sharding
- Automatic fail-over
- No single point of failure
- Linear scalability
- Introduced in Redis 3.0
- Production-ready since Redis 3.2

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd4_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Cluster Data Sharding

Redis Cluster uses a hash slot approach:

- 16,384 hash slots distributed across masters
- Each key maps to a hash slot using CRC16(key) % 16384
- Each master handles a subset of hash slots
- Entire keyspace distributed evenly

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd5_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Cluster Topology

Minimum recommended configuration:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd6_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Cluster Key Points

1. **Shared-nothing architecture**:
    - No central coordination point
    - Peer-to-peer communication

1. **Gossip protocol**:
    - Nodes exchange information
    - Failure detection
    - Cluster state consensus

1. **Hash slot migration**:
    - Move slots between nodes
    - Enables online scaling and rebalancing

1. **Automatic failover**:
    - Replica promotion to master
    - Configuration update and propagation

---

## Redis Cluster Prerequisites

Requirements for Redis Cluster setup:

1. **Redis version**: 3.0+ (5.0+ recommended)
1. **Node connectivity**: All nodes must communicate
1. **TCP ports**:
    - Client port (e.g., 6379)
    - Cluster bus port (client port + 10000, e.g., 16379)
1. **Cluster-enabled configuration**:

    ```conf
    cluster-enabled yes
    cluster-config-file nodes.conf
    cluster-node-timeout 5000
    ```
1. **Persistence**: Same configuration on all nodes
1. **Memory**: Sufficient memory for data + overhead

---

## Setting Up Redis Cluster: Configuration

Basic Redis Cluster node configuration:

```conf
# Base configuration
port 7000
daemonize yes
pidfile /var/run/redis/redis-7000.pid
logfile /var/log/redis/redis-7000.log
dir /var/lib/redis/7000/

# Cluster configuration
cluster-enabled yes
cluster-config-file nodes-7000.conf
cluster-node-timeout 5000
```

For each node:
- Use a different port (7000, 7001, 7002, etc.)
- Use a different data directory
- Adjust log file and pid file paths

---

## Creating a Redis Cluster

Using the redis-cli tool:

```bash
# Create a 3 master, 3 replica cluster
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1
```

Steps performed:
1. Assigns slots to masters
2. Sets up replication relationships
3. Joins nodes into a cluster
4. Verifies configuration

Alternative: `redis-cli --cluster help` for other commands

---

## Redis Cluster Key Commands

```bash
# Connect to cluster (note -c flag)
redis-cli -c -p 7000

# Cluster information
CLUSTER INFO

# Node information
CLUSTER NODES

# Slot distribution
CLUSTER SLOTS

# Resharding/Slot management
CLUSTER SETSLOT
CLUSTER GETKEYSINSLOT

# Add nodes
CLUSTER MEET
CLUSTER REPLICATE

# Manual failover
CLUSTER FAILOVER
```

---

## Redis Cluster Client Connections

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_07_cluster_scalability)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd7_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd7_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Two connection modes:
1. **Smart clients**: Handle redirects automatically
2. **Cluster proxy**: Routes commands to correct node

---

## Hash Tags for Key Colocation

Redis Cluster requires related keys on the same node for multi-key operations.

Hash Tags solve this by using part of the key for hash calculation:

```redis
user:{123}:profile  → Hash on "123"
user:{123}:sessions → Hash on "123"
user:{123}:cart     → Hash on "123"
```

All keys with the same hash tag `{123}` will be assigned to the same hash slot.

---

## Redis Cluster Limitations

1. **Multi-key operations**:
    - Limited to keys in the same hash slot
    - MGET, MSET, DEL multiple keys
    - Transactions with WATCH
    - Lua scripts with multiple keys

1. **Command restrictions**:
    - KEYS (use SCAN instead)
    - FLUSHALL/FLUSHDB (per-node only)
    - SELECT (only DB 0 available)

1. **No ability to ensure strong consistency**:
    - Some writes may be lost during failover
    - Designed for performance over consistency

---

## Scaling Redis Cluster: Adding Nodes

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd9_07_cluster_scalability)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd9_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd9_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Resharding a Redis Cluster

Using redis-cli cluster tools:

```bash
# Reshard to move 1000 slots from node A to node B
redis-cli --cluster reshard 127.0.0.1:7000 \
  --cluster-from [node-A-id] \
  --cluster-to [node-B-id] \
  --cluster-slots 1000
```

Steps performed:
1. Prepares nodes for slot migration
2. Moves keys in batches
3. Updates slot mappings
4. Verifies shard distribution

---

## Redis Cluster Resharding Process

---

## Removing Nodes from Redis Cluster

```bash
# Remove a replica
redis-cli --cluster del-node 127.0.0.1:7000 [node-id]

# Remove a master (requires resharding first)
# 1. Reshard all slots to other masters
redis-cli --cluster reshard 127.0.0.1:7000 \
  --cluster-from [node-id] \
  --cluster-to [destination-node-id] \
  --cluster-slots [all-slots-count]

# 2. Then remove the empty master
redis-cli --cluster del-node 127.0.0.1:7000 [node-id]
```

Important: Never remove a master with assigned slots!

---

## Redis Cluster Failover

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd11_07_cluster_scalability)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd11_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd11_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

1. Automatic failover:
    - Replica detects master is down (subjective down)
    - Multiple nodes agree (objective down)
    - Replica with highest replication offset becomes master

1. Manual failover:

    ```bash
    # On a replica:
    CLUSTER FAILOVER
    ```

---

## Redis Cluster Availability

Cluster fails when:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd12_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd12_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd12_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Configuration option:
```conf
# Allow writes when some slots not covered
cluster-require-full-coverage no
```

---

## Monitoring Redis Cluster

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd13_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd13_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd13_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Cluster Monitoring Tools

1. **Built-in tools**:

    ```bash
    redis-cli --cluster info 127.0.0.1:7000
    redis-cli --cluster check 127.0.0.1:7000
    redis-cli -c -p 7000 CLUSTER NODES
    ```

1. **Visualization tools**:
    - Redis Insight
    - RedisGraph for cluster topology
    - Custom dashboards (Grafana)

1. **Metrics to watch**:
    - Slot distribution
    - Memory usage per node
    - Keyspace hits/misses
    - Network metrics
    - Cluster bus traffic

---

## Best Practices for Redis Cluster

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd14_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd14_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd14_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Key Design for Redis Cluster

Design your keys with sharding in mind:

1. **Use hash tags for related data**:

```redis
user:{userId}:profile
user:{userId}:sessions
```

1. **Avoid cross-slot operations** (or use hash tags):
    - MGET/MSET
    - Lua scripts with multiple keys
    - SUNION/SINTER across sets

1. **Distribute keys evenly**:
    - Avoid hash tag hotspots
    - Monitor key distribution

1. **Consider key expiration**:
    - TTL works per node
    - Expired keys free memory locally

---

## Redis Cluster Consistency Guarantees

Redis Cluster is "eventually consistent":

- No strong consistency guarantees
- Can lose writes during network partitions
- CAP theorem trade-off: Favors availability and partition tolerance

Potential consistency issues:
1. **Split-brain during partitions**
2. **Asynchronous replication**
3. **Race conditions during failover**

For stronger consistency:
- Use appropriate wait commands
- Implement client-side retry logic
- Consider Redis Enterprise

---

## Scaling Redis Without Cluster

Alternative scaling approaches:

1. **Functional partitioning**:
    - Separate instances by function
    - Example: sessions, cache, messaging

1. **Application-level sharding**:
    - Client determines shard
    - Consistent hashing algorithms

1. **Proxy-based solutions**:
    - Twemproxy (Twitter)
    - Envoy (Lyft)
    - Redis Cluster Proxy

1. **Redis Enterprise**:
    - Commercial solution
    - More features and guarantees

---

## Functional Partitioning Example

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd15_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd15_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd15_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Benefits:
- Simpler than full sharding
- Different configs per function
- Isolated performance profiles
- Targeted scaling

---

## Client-Side Sharding Example

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd16_07_cluster_scalability)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd16_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd16_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis vs. Redis Cluster vs. Redis Enterprise

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd17_07_cluster_scalability)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd17_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd17_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Data Migration Strategies

When migrating to Redis Cluster:

1. **Offline migration**:
    - Export data (DUMP/SAVE)
    - Create cluster
    - Import data

1. **Shadow writing**:
    - Write to both old and new systems
    - Verify data consistency
    - Switch reads to new system

1. **Gradual feature migration**:
    - Move one feature at a time
    - Minimize risk
    - Easier rollback

---

## Performance Tuning Redis Cluster

Key areas for optimization:

1. **Network optimization**:
    - Minimize latency between nodes
    - Separate client and cluster bus networks
    - Sufficient bandwidth

1. **Memory settings**:
    - Proper `maxmemory` settings
    - Appropriate eviction policies
    - Leave headroom for resharding

1. **Client connection handling**:
    - Connection pooling
    - Pipelining where appropriate
    - Minimize redirects (use hash tags)

1. **Monitoring and adjusting**:
    - Track latency and throughput
    - Identify hot keys/slots
    - Rebalance as needed

---

## Disaster Recovery for Redis Cluster

DR strategies for Redis Cluster:

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd19_07_cluster_scalability)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd19_07_cluster_scalability)"/>
  <defs>
    <marker id="arrowd19_07_cluster_scalability" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Backup approaches:
1. **Coordinated RDB snapshots**
2. **Geo-distributed replicas**
3. **Cross-datacenter replication**

Remember:
- Test recovery regularly
- Document procedures
- Automate where possible

---

## Lab: Redis Cluster

1. **Exercise 1**: Set up a 3-master, 3-replica Redis Cluster
1. **Exercise 2**: Test failover by shutting down a master
1. **Exercise 3**: Add a new node to the cluster
1. **Exercise 4**: Migrate slots to balance the cluster
1. **Exercise 5**: Design keys with hash tags for related data
1. **Exercise 6**: Test cluster performance with redis-benchmark
1. **Exercise 7**: Implement a cluster monitoring dashboard

---

## Summary

- Redis Cluster provides horizontal scaling and high availability
- Hash slot-based sharding distributes data across nodes
- Node-to-node gossip protocol manages cluster state
- Key design crucial for effective sharding
- Automatic failover handles node failures
- Online resharding enables dynamic scaling
- Trade-offs: some consistency guarantees for performance
- Alternative scaling options exist for different needs

Next chapter: Integrating Redis with Applications
