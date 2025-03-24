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

![0](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/0.png)

---

## Master-Replica Architecture

![1](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/1.png)

- Master handles all writes
- Replicas handle read queries
- Read scaling only (not write scaling)
- Provides high availability
- Limited by master's capacity

---

## Client-Side Partitioning

![2](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/2.png)

- Application determines which Redis instance to use
- Consistent hashing or modulo-based distribution
- Simple to implement
- No additional infrastructure
- Drawbacks: Client complexity, inconsistent distribution

---

## Proxy-Based Partitioning

![3](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/3.png)

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

![4](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/4.png)

---

## Redis Cluster Data Sharding

Redis Cluster uses a hash slot approach:

- 16,384 hash slots distributed across masters
- Each key maps to a hash slot using CRC16(key) % 16384
- Each master handles a subset of hash slots
- Entire keyspace distributed evenly

![5](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/5.png)

---

## Redis Cluster Topology

Minimum recommended configuration:

![6](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/6.png)

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

![7](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/7.png)

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

![9](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/9.png)

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

![11](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/11.png)

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

![12](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/12.png)

Configuration option:
```conf
# Allow writes when some slots not covered
cluster-require-full-coverage no
```

---

## Monitoring Redis Cluster

![13](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/13.png)

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

![14](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/14.png)

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

![15](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/15.png)

Benefits:
- Simpler than full sharding
- Different configs per function
- Isolated performance profiles
- Targeted scaling

---

## Client-Side Sharding Example

![16](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/16.png)

---

## Redis vs. Redis Cluster vs. Redis Enterprise

![17](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/17.png)

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

![19](../../../out/mermaid/marp/courses/redis/07_cluster_scalability.md/19.png)

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
