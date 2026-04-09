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

![redis_scaling_architectures](svg/courses/databases/redis/08_cluster_scalability/redis_scaling_architectures.svg)

---

## Master-Replica Architecture

![master_replica_architecture](svg/courses/databases/redis/08_cluster_scalability/master_replica_architecture.svg)

---

## Master-Replica Architecture - Details

- Master handles all writes
- Replicas handle read queries
- Read scaling only (not write scaling)
- Provides high availability
- Limited by master's capacity

---

## Client-Side Partitioning

![client_side_partitioning](svg/courses/databases/redis/08_cluster_scalability/client_side_partitioning.svg)

---

## Client-Side Partitioning - Details

- Application determines which Redis instance to use
- Consistent hashing or modulo-based distribution
- Simple to implement
- No additional infrastructure
- Drawbacks: Client complexity, inconsistent distribution

---

## Proxy-Based Partitioning

![proxy_based_partitioning](svg/courses/databases/redis/08_cluster_scalability/proxy_based_partitioning.svg)

---

## Proxy-Based Partitioning - Details

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

---

## Introduction to Redis Cluster

![introduction_to_redis_cluster](svg/courses/databases/redis/08_cluster_scalability/introduction_to_redis_cluster.svg)

---

## Redis Cluster Data Sharding

Redis Cluster uses a hash slot approach:

- 16,384 hash slots distributed across masters
- Each key maps to a hash slot using CRC16(key) % 16384
- Each master handles a subset of hash slots
- Entire keyspace distributed evenly

---

## Redis Cluster Data Sharding

![redis_cluster_data_sharding](svg/courses/databases/redis/08_cluster_scalability/redis_cluster_data_sharding.svg)

---

## Redis Cluster Topology

Minimum recommended configuration:

![redis_cluster_topology](svg/courses/databases/redis/08_cluster_scalability/redis_cluster_topology.svg)

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
1. Sets up replication relationships
1. Joins nodes into a cluster
1. Verifies configuration

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

![redis_cluster_client_connections](svg/courses/databases/redis/08_cluster_scalability/redis_cluster_client_connections.svg)

---

## Redis Cluster Connection Modes

Two connection modes:
1. **Smart clients**: Handle redirects automatically
1. **Cluster proxy**: Routes commands to correct node

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

![scaling_redis_cluster_adding_nodes](svg/courses/databases/redis/08_cluster_scalability/scaling_redis_cluster_adding_nodes.svg)

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
1. Moves keys in batches
1. Updates slot mappings
1. Verifies shard distribution

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

![redis_cluster_failover](svg/courses/databases/redis/08_cluster_scalability/redis_cluster_failover.svg)

---

## Redis Cluster Failover - Details

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

---

## Redis Cluster Availability

![redis_cluster_availability](svg/courses/databases/redis/08_cluster_scalability/redis_cluster_availability.svg)

---

## Redis Cluster Availability - Configuration

Configuration option:
```conf
# Allow writes when some slots not covered
cluster-require-full-coverage no
```

---

## Monitoring Redis Cluster

![monitoring_redis_cluster](svg/courses/databases/redis/08_cluster_scalability/monitoring_redis_cluster.svg)

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

![best_practices_for_redis_cluster](svg/courses/databases/redis/08_cluster_scalability/best_practices_for_redis_cluster.svg)

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
1. **Asynchronous replication**
1. **Race conditions during failover**

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

![functional_partitioning_example](svg/courses/databases/redis/08_cluster_scalability/functional_partitioning_example.svg)

---

## Functional Partitioning Benefits

- Simpler than full sharding
- Different configs per function
- Isolated performance profiles
- Targeted scaling

---

## Client-Side Sharding Example

![client_side_sharding_example](svg/courses/databases/redis/08_cluster_scalability/client_side_sharding_example.svg)

---

## Redis vs. Redis Cluster vs. Redis Enterprise

![redis_vs_redis_cluster_vs_redis_enterprise](svg/courses/databases/redis/08_cluster_scalability/redis_vs_redis_cluster_vs_redis_enterprise.svg)

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

---

## Disaster Recovery for Redis Cluster

![disaster_recovery_for_redis_cluster](svg/courses/databases/redis/08_cluster_scalability/disaster_recovery_for_redis_cluster.svg)

---

## Disaster Recovery Backup Approaches

Backup approaches:
1. **Coordinated RDB snapshots**
1. **Geo-distributed replicas**
1. **Cross-datacenter replication**

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
