# Redis Configuration and Management

---

## Redis Configuration Basics

Redis is configured through:

1. **Configuration file** (`redis.conf`)
1. **Command-line parameters**
1. **Runtime commands** (`CONFIG SET/GET`)

Default configuration file locations:
- `/etc/redis/redis.conf` (Linux packages)
- `/usr/local/etc/redis.conf` (macOS Homebrew)
- Source directory when compiled from source

---

## Redis Configuration File Structure

```conf
# Comments start with #
# Configuration format: keyword value

# Network configuration
bind 127.0.0.1
port 6379
protected-mode yes

# General configuration
daemonize yes
pidfile /var/run/redis/redis-server.pid
loglevel notice
logfile /var/log/redis/redis-server.log

# Memory and limits
maxmemory 100mb
maxmemory-policy allkeys-lru
```

---

## Redis Configuration Sections

![redis_configuration_sections](/svg/courses/databases/redis/07_configuration/redis_configuration_sections.svg)

---

## Viewing Configuration

```bash
# View all configuration parameters
redis-cli CONFIG GET *

# View specific configuration parameters
redis-cli CONFIG GET maxmemory
redis-cli CONFIG GET *max*

# Alternative - use INFO command
redis-cli INFO
```

Example:
```bash
127.0.0.1:6379> CONFIG GET maxmemory
1) "maxmemory"
2) "0"
```

---

## Changing Configuration at Runtime

```bash
# Change configuration during runtime
redis-cli CONFIG SET parameter value

# Examples
redis-cli CONFIG SET maxmemory 200mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
redis-cli CONFIG SET loglevel debug
```

Note: Not all parameters can be changed at runtime!

---

## Making Configuration Changes Permanent

Save runtime changes to configuration file:

```bash
# Save configuration to current redis.conf
redis-cli CONFIG REWRITE

# Alternative: manually edit redis.conf and restart
sudo nano /etc/redis/redis.conf
sudo systemctl restart redis
```

---

## Critical Configuration Parameters

![critical_configuration_parameters](/svg/courses/databases/redis/07_configuration/critical_configuration_parameters.svg)

---

## Network Configuration

```conf
# Interfaces to listen on (bind to all: bind 0.0.0.0)
bind 127.0.0.1 ::1

# Port to listen on
port 6379

# Listen on Unix socket
unixsocket /tmp/redis.sock
unixsocketperm 700

# Close idle connections (seconds, 0 = disable)
timeout 0

# TCP keepalive (seconds, 0 = disable)
tcp-keepalive 300

# Protected mode (reject connections when no bind/auth)
protected-mode yes
```

---

## Memory Management

```conf
# Maximum memory limit (0 = no limit)
maxmemory 1gb

# Eviction policy when maxmemory is reached
maxmemory-policy allkeys-lru

# Eviction sample size
maxmemory-samples 5

# Memory usage reporting precision
replica-ignore-maxmemory yes
```

Available policies:
- `noeviction`: Return errors when limit reached
- `allkeys-lru`: Evict least recently used keys
- `allkeys-lfu`: Evict least frequently used keys
- `volatile-lru`: Evict LRU keys with expiry set
- `volatile-lfu`: Evict LFU keys with expiry set
- `volatile-ttl`: Evict keys with nearest expiry
- `volatile-random`: Random keys with expiry
- `allkeys-random`: Random keys

---

## Choosing the Right Eviction Policy

![choosing_the_right_eviction_policy](/svg/courses/databases/redis/07_configuration/choosing_the_right_eviction_policy.svg)

---

## Security Configuration

```conf
# Authentication password (use strong passwords!)
requirepass "ComplexPasswordHere"

# Limit commands (Redis 6.0+)
rename-command FLUSHALL ""
rename-command CONFIG "ADMIN_CONFIG"

# Restrict access via ACLs (Redis 6.0+)
user default on >ComplexPasswordHere ~* &* +@all -@dangerous

# TLS/SSL settings (Redis 6.0+)
tls-port 6380
tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
tls-ca-cert-file /path/to/ca.crt
```

---

## Logging Configuration

```conf
# Log level (debug, verbose, notice, warning)
loglevel notice

# Log file location (empty for stdout)
logfile /var/log/redis/redis-server.log

# Log to syslog
syslog-enabled yes
syslog-ident redis
syslog-facility local0

# Syslog options
# Debug (7), Verbose (6), Notice (5), Warning (4)
syslog-level notice
```

---

## Client Configuration

```conf
# Maximum connected clients
maxclients 10000

# Timeout for client connections (seconds, 0 = disabled)
timeout 0

# TCP keepalive frequency (seconds)
tcp-keepalive 300

# Client output buffer limits (normal, replica, pubsub)
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

---

## Slow Log Configuration

The Slow Log records commands that exceed execution time threshold:

```conf
# Log threshold in microseconds (1000 = 1ms)
slowlog-log-slower-than 10000

# Maximum number of entries in slow log
slowlog-max-len 128
```

Commands to manage:

```bash
# Get the slow log
SLOWLOG GET [count]

# Get slow log length
SLOWLOG LEN

# Reset the slow log
SLOWLOG RESET
```

---

## Latency Monitoring

Redis latency diagnostics:

```conf
# Enable latency monitoring
latency-monitor-threshold 100
```

Latency commands:

```bash
# Get latest latency samples
LATENCY LATEST

# View latency timeline
LATENCY HISTORY command

# Get latency report
LATENCY DOCTOR
```

---

## Tuning Redis Performance

![tuning_redis_performance](/svg/courses/databases/redis/07_configuration/tuning_redis_performance.svg)

---

## System Parameters for Redis

Linux settings for optimal Redis performance:

```bash
# /etc/sysctl.conf
# Allow large memory pages
vm.overcommit_memory = 1

# Disable swap
vm.swappiness = 0

# Increase max connections
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535

# Avoid slow connections under load
net.ipv4.tcp_slow_start_after_idle = 0

# TCP keepalive settings
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_keepalive_intvl = 10
net.ipv4.tcp_keepalive_probes = 3
```

Apply with: `sudo sysctl -p`

---

## Redis Management Tools

![redis_management_tools](/svg/courses/databases/redis/07_configuration/redis_management_tools.svg)

---

## Redis CLI Essentials

```bash
# Basic connection
redis-cli

# Connect to specific host/port
redis-cli -h redis.example.com -p 6380

# Using password
redis-cli -a password
redis-cli --askpass

# Connect to replica
redis-cli -h replica.example.com

# Execute command directly
redis-cli SET mykey value
redis-cli GET mykey
```

---

## Redis CLI Advanced Usage

```bash
# Monitor all commands
redis-cli MONITOR

# Continuous stats
redis-cli --stat

# Latency monitoring
redis-cli --latency
redis-cli --latency-history
redis-cli --latency-dist

# Scan for big keys
redis-cli --bigkeys

# Memory analysis
redis-cli MEMORY USAGE key

# Introspection
redis-cli MEMORY DOCTOR
redis-cli MEMORY STATS
```

---

## Automatic Key Management

Key expiration and eviction:

1. **Explicit expiration**:
   ```bash
   EXPIRE key seconds
   EXPIREAT key timestamp
   SETEX key seconds value
   ```

1. **Implicit eviction**:
    - When `maxmemory` limit is reached
    - According to `maxmemory-policy`

![automatic_key_management](/svg/courses/databases/redis/07_configuration/automatic_key_management.svg)

---

## Administrative Commands

Essential Redis administrative commands:

```bash
# Get information and statistics
INFO [section]

# Server statistics
INFO server
INFO clients
INFO memory
INFO stats

# Database management
SELECT index
FLUSHDB
FLUSHALL

# Client management
CLIENT LIST
CLIENT KILL
CLIENT SETNAME "application:user"

# Debug and maintenance
DEBUG OBJECT key
MEMORY DOCTOR
```

---

## Monitoring Redis in Production

Key metrics to monitor:

![monitoring_redis_in_production](/svg/courses/databases/redis/07_configuration/monitoring_redis_in_production.svg)

---

## Memory Analysis

```bash
# Memory usage breakdown
redis-cli INFO memory

# Memory stats
redis-cli MEMORY STATS

# Memory used by key
redis-cli MEMORY USAGE mykey

# Sampling with SCAN
for key in $(redis-cli --scan); do
  redis-cli MEMORY USAGE "$key"
done

# Memory doctor
redis-cli MEMORY DOCTOR
```

Sample script:
```bash
redis-cli --scan --pattern 'user:*' | xargs -L 100 redis-cli MEMORY USAGE
```

---

## Identifying Memory Issues

Memory fragmentation in Redis:
- **mem_fragmentation_ratio < 1.0** - Redis needs more memory than available
- **mem_fragmentation_ratio 1.0-1.5** - Normal
- **mem_fragmentation_ratio > 1.5** - Significant fragmentation

```bash
# Check fragmentation ratio
redis-cli INFO memory | grep mem_fragmentation_ratio

# Find large keys
redis-cli --bigkeys

# Defragment memory (Redis 4.0+)
redis-cli CONFIG SET activedefrag yes
```

---

## Backup and Recovery

![backup_and_recovery](/svg/courses/databases/redis/07_configuration/backup_and_recovery.svg)

---

## Implementing a Backup Strategy

```bash
#!/bin/bash
# Example Redis backup script

# Backup directory
BACKUP_DIR="/var/backups/redis"
mkdir -p $BACKUP_DIR

# Timestamp
TIMESTAMP=$(date +%Y%m%d%H%M%S)

# Trigger BGSAVE
redis-cli BGSAVE
sleep 5  # Wait for BGSAVE to complete

# Copy RDB file
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis-$TIMESTAMP.rdb

# Compress backup
gzip $BACKUP_DIR/redis-$TIMESTAMP.rdb

# Keep last 7 days of backups
find $BACKUP_DIR -name "redis-*.rdb.gz" -mtime +7 -delete
```

---

## Upgrading Redis

Steps for safe Redis upgrades:

1. **Preparation**
    - Read release notes for breaking changes
    - Backup data before upgrade
    - Plan for downtime or use replication

1. **Upgrade process (standalone)**

    ```bash
    # Stop Redis
    systemctl stop redis

    # Upgrade package
    apt-get update && apt-get upgrade redis-server

    # Start Redis
    systemctl start redis
    ```

1. **Upgrade process (with replicas)**:
    - Upgrade replicas first
    - Promote a replica to master
    - Upgrade old master last

---

## Zero-Downtime Upgrades

![zero_downtime_upgrades](/svg/courses/databases/redis/07_configuration/zero_downtime_upgrades.svg)

---

## Redis Sentinel for High Availability

![redis_sentinel_for_high_availability](/svg/courses/databases/redis/07_configuration/redis_sentinel_for_high_availability.svg)

---

## Redis Sentinel Configuration

```conf
# sentinel.conf
port 26379
daemonize yes
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

Key concepts:
- Monitors Redis master and replicas
- Automatic failover if master fails
- Client notifications
- Requires at least 3 Sentinel instances
- Quorum (2 in example) needed for failover

---

## Redis Cluster for Scaling

![redis_cluster_for_scaling](/svg/courses/databases/redis/07_configuration/redis_cluster_for_scaling.svg)

---

## Key Redis Cluster Configuration

```conf
# Enable cluster mode
cluster-enabled yes

# Cluster configuration file
cluster-config-file nodes.conf

# Node timeout
cluster-node-timeout 5000

# Replicas per master
cluster-replica-validity-factor 10

# Cluster bus port
cluster-port 16379
```

Key commands:

```bash
# Create cluster
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1

# Check cluster state
redis-cli -c -p 7000 CLUSTER INFO
redis-cli -c -p 7000 CLUSTER NODES
```

---

## Lab: Redis Configuration and Management

1. **Exercise 1**: Create a custom Redis configuration
1. **Exercise 2**: Configure memory limits and eviction policy
1. **Exercise 3**: Set up basic security (authentication and command restrictions)
1. **Exercise 4**: Implement a backup strategy
1. **Exercise 5**: Configure and use Slow Log
1. **Exercise 6**: Use redis-cli for performance monitoring
1. **Exercise 7**: Create a simple Redis Sentinel setup

---

## Summary

- Redis configuration offers extensive customization
- Configuration can be managed via file or runtime commands
- Key areas: memory, network, security, persistence
- Performance tuning requires both Redis and system settings
- Monitoring is essential for production deployments
- Backup strategies should align with durability requirements
- High availability options: replication, Sentinel, Cluster
- Management tools simplify administration tasks

Next chapter: Redis Cluster and Scalability
