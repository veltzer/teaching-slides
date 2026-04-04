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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="120" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="42" text-anchor="middle" font-size="10" font-weight="bold">Network</text>
  <text x="80" y="58" text-anchor="middle" font-size="9">bind, port</text>
  <text x="80" y="72" text-anchor="middle" font-size="9">timeout, TLS</text>
  <rect x="160" y="20" width="120" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="42" text-anchor="middle" font-size="10" font-weight="bold">Memory</text>
  <text x="220" y="58" text-anchor="middle" font-size="9">maxmemory</text>
  <text x="220" y="72" text-anchor="middle" font-size="9">eviction policy</text>
  <rect x="300" y="20" width="120" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="360" y="42" text-anchor="middle" font-size="10" font-weight="bold">Persistence</text>
  <text x="360" y="58" text-anchor="middle" font-size="9">save, appendonly</text>
  <text x="360" y="72" text-anchor="middle" font-size="9">fsync policy</text>
  <rect x="440" y="20" width="140" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="42" text-anchor="middle" font-size="10" font-weight="bold">Security</text>
  <text x="510" y="58" text-anchor="middle" font-size="9">requirepass, ACL</text>
  <text x="510" y="72" text-anchor="middle" font-size="9">TLS, rename-cmd</text>
  <rect x="80" y="110" width="200" height="60" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="180" y="132" text-anchor="middle" font-size="10" font-weight="bold">Replication</text>
  <text x="180" y="150" text-anchor="middle" font-size="9">replicaof, replica-read-only</text>
  <rect x="320" y="110" width="200" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="420" y="132" text-anchor="middle" font-size="10" font-weight="bold">Logging/Debug</text>
  <text x="420" y="150" text-anchor="middle" font-size="9">loglevel, slowlog, latency</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="250" height="70" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="42" text-anchor="middle" font-size="11" font-weight="bold">Critical Parameters</text>
  <text x="155" y="60" text-anchor="middle" font-size="10">maxmemory, bind, requirepass</text>
  <text x="155" y="75" text-anchor="middle" font-size="10">maxmemory-policy, protected-mode</text>
  <rect x="320" y="20" width="250" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="42" text-anchor="middle" font-size="11" font-weight="bold">Runtime Changeable</text>
  <text x="445" y="60" text-anchor="middle" font-size="10">CONFIG SET maxmemory 2gb</text>
  <text x="445" y="75" text-anchor="middle" font-size="10">CONFIG SET loglevel debug</text>
  <rect x="30" y="110" width="250" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="132" text-anchor="middle" font-size="11" font-weight="bold">Restart Required</text>
  <text x="155" y="150" text-anchor="middle" font-size="10">bind, port, daemonize</text>
  <text x="155" y="165" text-anchor="middle" font-size="10">cluster-enabled</text>
  <rect x="320" y="110" width="250" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="132" text-anchor="middle" font-size="11" font-weight="bold">Save to Disk</text>
  <text x="445" y="150" text-anchor="middle" font-size="10">CONFIG REWRITE</text>
  <text x="445" y="165" text-anchor="middle" font-size="10">persists runtime changes</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Eviction Policy Decision Tree</text>
  <rect x="200" y="30" width="200" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="50" text-anchor="middle" font-size="10">Is all data cacheable?</text>
  <line x1="250" y1="60" x2="120" y2="80" stroke="#333" stroke-width="1"/>
  <line x1="350" y1="60" x2="480" y2="80" stroke="#333" stroke-width="1"/>
  <text x="170" y="75" font-size="9">Yes</text>
  <text x="430" y="75" font-size="9">No (some persistent)</text>
  <rect x="30" y="82" width="180" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="120" y="102" text-anchor="middle" font-size="10">allkeys-lru / allkeys-lfu</text>
  <rect x="390" y="82" width="180" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="480" y="102" text-anchor="middle" font-size="10">volatile-lru / volatile-ttl</text>
  <rect x="30" y="125" width="180" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="120" y="145" text-anchor="middle" font-size="10">Best for pure caching</text>
  <rect x="390" y="125" width="180" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="480" y="145" text-anchor="middle" font-size="10">Only evicts keys with TTL</text>
  <rect x="150" y="165" width="300" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="185" text-anchor="middle" font-size="10">noeviction: returns errors (safest for data integrity)</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Performance Tuning Areas</text>
  <rect x="20" y="35" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="55" text-anchor="middle" font-size="10" font-weight="bold">Memory</text>
  <text x="105" y="72" text-anchor="middle" font-size="9">maxmemory limits</text>
  <text x="105" y="86" text-anchor="middle" font-size="9">activedefrag, lazyfree</text>
  <rect x="215" y="35" width="170" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="10" font-weight="bold">CPU</text>
  <text x="300" y="72" text-anchor="middle" font-size="9">io-threads (Redis 6+)</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">avoid KEYS, large O(N)</text>
  <rect x="410" y="35" width="170" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="55" text-anchor="middle" font-size="10" font-weight="bold">Network</text>
  <text x="495" y="72" text-anchor="middle" font-size="9">tcp-backlog, keepalive</text>
  <text x="495" y="86" text-anchor="middle" font-size="9">pipelining, connection pool</text>
  <rect x="120" y="120" width="170" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="142" text-anchor="middle" font-size="10" font-weight="bold">Persistence</text>
  <text x="205" y="160" text-anchor="middle" font-size="9">save intervals, fsync</text>
  <rect x="315" y="120" width="170" height="60" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="142" text-anchor="middle" font-size="10" font-weight="bold">OS Tuning</text>
  <text x="400" y="160" text-anchor="middle" font-size="9">overcommit, THP, swappiness</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="25" width="170" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="48" text-anchor="middle" font-size="10" font-weight="bold">redis-cli</text>
  <text x="105" y="65" text-anchor="middle" font-size="9">Built-in CLI tool</text>
  <text x="105" y="79" text-anchor="middle" font-size="9">--stat, --bigkeys</text>
  <rect x="215" y="25" width="170" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="10" font-weight="bold">Redis Insight</text>
  <text x="300" y="65" text-anchor="middle" font-size="9">GUI management</text>
  <text x="300" y="79" text-anchor="middle" font-size="9">Visual browser</text>
  <rect x="410" y="25" width="170" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="48" text-anchor="middle" font-size="10" font-weight="bold">Monitoring</text>
  <text x="495" y="65" text-anchor="middle" font-size="9">Grafana + Prometheus</text>
  <text x="495" y="79" text-anchor="middle" font-size="9">redis_exporter</text>
  <rect x="120" y="110" width="170" height="65" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="133" text-anchor="middle" font-size="10" font-weight="bold">redis-benchmark</text>
  <text x="205" y="150" text-anchor="middle" font-size="9">Performance testing</text>
  <text x="205" y="164" text-anchor="middle" font-size="9">Throughput/latency</text>
  <rect x="315" y="110" width="170" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="133" text-anchor="middle" font-size="10" font-weight="bold">redis-check-*</text>
  <text x="400" y="150" text-anchor="middle" font-size="9">redis-check-rdb</text>
  <text x="400" y="164" text-anchor="middle" font-size="9">redis-check-aof</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="15" width="250" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="35" text-anchor="middle" font-size="10" font-weight="bold">Explicit Expiration (TTL)</text>
  <text x="155" y="52" text-anchor="middle" font-size="9">EXPIRE key 3600</text>
  <text x="155" y="66" text-anchor="middle" font-size="9">SETEX key 60 value</text>
  <text x="155" y="80" text-anchor="middle" font-size="9">Key auto-deleted after TTL</text>
  <rect x="320" y="15" width="250" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="35" text-anchor="middle" font-size="10" font-weight="bold">Implicit Eviction</text>
  <text x="445" y="52" text-anchor="middle" font-size="9">When maxmemory reached</text>
  <text x="445" y="66" text-anchor="middle" font-size="9">Policy: LRU, LFU, TTL, random</text>
  <text x="445" y="80" text-anchor="middle" font-size="9">Automatic, based on config</text>
  <line x1="155" y1="100" x2="155" y2="130" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="445" y1="100" x2="445" y2="130" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
  <rect x="30" y="130" width="540" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="150" text-anchor="middle" font-size="10" font-weight="bold">Lazy expiration + Active expiration (sampling)</text>
  <text x="300" y="168" text-anchor="middle" font-size="9">Redis checks keys on access (lazy) and periodically samples expired keys (active)</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="120" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="40" text-anchor="middle" font-size="10" font-weight="bold">Memory</text>
  <text x="80" y="55" text-anchor="middle" font-size="9">used_memory</text>
  <text x="80" y="68" text-anchor="middle" font-size="9">fragmentation</text>
  <text x="80" y="81" text-anchor="middle" font-size="9">evicted_keys</text>
  <rect x="160" y="20" width="120" height="75" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="40" text-anchor="middle" font-size="10" font-weight="bold">Throughput</text>
  <text x="220" y="55" text-anchor="middle" font-size="9">ops/second</text>
  <text x="220" y="68" text-anchor="middle" font-size="9">hit/miss ratio</text>
  <text x="220" y="81" text-anchor="middle" font-size="9">commands/sec</text>
  <rect x="300" y="20" width="120" height="75" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="360" y="40" text-anchor="middle" font-size="10" font-weight="bold">Latency</text>
  <text x="360" y="55" text-anchor="middle" font-size="9">avg response</text>
  <text x="360" y="68" text-anchor="middle" font-size="9">p99 latency</text>
  <text x="360" y="81" text-anchor="middle" font-size="9">slow log</text>
  <rect x="440" y="20" width="140" height="75" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="40" text-anchor="middle" font-size="10" font-weight="bold">Connections</text>
  <text x="510" y="55" text-anchor="middle" font-size="9">connected_clients</text>
  <text x="510" y="68" text-anchor="middle" font-size="9">blocked_clients</text>
  <text x="510" y="81" text-anchor="middle" font-size="9">rejected_conns</text>
  <rect x="20" y="115" width="560" height="65" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" font-weight="bold">Alert Thresholds</text>
  <text x="300" y="152" text-anchor="middle" font-size="9">Memory > 80% | Hit ratio &lt; 90% | Latency > 5ms | Evictions increasing</text>
  <text x="300" y="168" text-anchor="middle" font-size="9">Use INFO command sections: server, clients, memory, stats, keyspace</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="130" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="42" text-anchor="middle" font-size="10" font-weight="bold">1. BGSAVE</text>
  <text x="95" y="60" text-anchor="middle" font-size="9">Create snapshot</text>
  <line x1="165" y1="50" x2="210" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_06_configuration)"/>
  <rect x="220" y="20" width="130" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="285" y="42" text-anchor="middle" font-size="10" font-weight="bold">2. Copy RDB</text>
  <text x="285" y="60" text-anchor="middle" font-size="9">To backup dir</text>
  <line x1="355" y1="50" x2="400" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_06_configuration)"/>
  <rect x="410" y="20" width="160" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="42" text-anchor="middle" font-size="10" font-weight="bold">3. Transfer</text>
  <text x="490" y="60" text-anchor="middle" font-size="9">Off-site / cloud</text>
  <rect x="30" y="100" width="540" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="122" text-anchor="middle" font-size="10">Recovery: Stop Redis -> Copy RDB to data dir -> Restart Redis</text>
  <rect x="30" y="148" width="540" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="170" text-anchor="middle" font-size="10">Always test recovery! Verify with DBSIZE and sample key checks</text>
  <defs>
    <marker id="arrowd7_06_configuration" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_06_configuration)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd8_06_configuration)"/>
  <defs>
    <marker id="arrowd8_06_configuration" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Sentinel for High Availability

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd9_06_configuration)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd9_06_configuration)"/>
  <defs>
    <marker id="arrowd9_06_configuration" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd10_06_configuration)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd10_06_configuration)"/>
  <defs>
    <marker id="arrowd10_06_configuration" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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
