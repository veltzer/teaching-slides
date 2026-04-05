# Redis Persistence

---

## Why Persistence Matters

Redis is an in-memory database, but offers persistence options:

- **Data durability**: Survive server restarts
- **Disaster recovery**: Backup and restore
- **Data migration**: Move data between instances
- **Point-in-time recovery**: Recover from failures
- **Warm starts**: Faster initialization with pre-loaded data

Without persistence, all data is lost when Redis restarts!

---

## Redis Persistence Options

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="52" text-anchor="middle" font-size="11" font-weight="bold">RDB</text>
  <text x="80" y="72" text-anchor="middle" font-size="10">Snapshots</text>
  <rect x="170" y="30" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="52" text-anchor="middle" font-size="11" font-weight="bold">AOF</text>
  <text x="230" y="72" text-anchor="middle" font-size="10">Append-Only</text>
  <rect x="320" y="30" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="380" y="52" text-anchor="middle" font-size="11" font-weight="bold">Hybrid</text>
  <text x="380" y="72" text-anchor="middle" font-size="10">RDB + AOF</text>
  <rect x="470" y="30" width="110" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="52" text-anchor="middle" font-size="11" font-weight="bold">None</text>
  <text x="525" y="72" text-anchor="middle" font-size="10">Pure cache</text>
  <rect x="20" y="110" width="560" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="135" text-anchor="middle" font-size="11">Durability increases left to right</text>
  <line x1="80" y1="155" x2="520" y2="155" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_05_persistence)"/>
  <text x="80" y="170" text-anchor="middle" font-size="9">More durable</text>
  <text x="520" y="170" text-anchor="middle" font-size="9">Less durable</text>
  <defs>
    <marker id="arrowd0_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## RDB (Redis Database) Snapshots

Point-in-time snapshots of the dataset:

- Creates a single compact binary file
- Snapshot represents Redis data at one moment
- Usually scheduled at specific intervals
- Can be created manually with commands
- Good for backups and disaster recovery

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_05_persistence)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd1_05_persistence)"/>
  <defs>
    <marker id="arrowd1_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## How RDB Snapshots Work

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="130" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="42" text-anchor="middle" font-size="11" font-weight="bold">Redis Parent</text>
  <text x="95" y="60" text-anchor="middle" font-size="10">Serves clients</text>
  <line x1="95" y1="85" x2="95" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_persistence)"/>
  <text x="115" y="105" font-size="9">fork()</text>
  <rect x="30" y="120" width="130" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="142" text-anchor="middle" font-size="11" font-weight="bold">Child Process</text>
  <text x="95" y="160" text-anchor="middle" font-size="10">Writes data</text>
  <line x1="170" y1="150" x2="260" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_persistence)"/>
  <rect x="270" y="120" width="130" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="335" y="142" text-anchor="middle" font-size="11">temp.rdb</text>
  <text x="335" y="160" text-anchor="middle" font-size="10">(writing...)</text>
  <line x1="410" y1="150" x2="450" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_persistence)"/>
  <text x="430" y="143" font-size="9">rename</text>
  <rect x="460" y="120" width="120" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="142" text-anchor="middle" font-size="11" font-weight="bold">dump.rdb</text>
  <text x="520" y="160" text-anchor="middle" font-size="10">(final file)</text>
  <defs>
    <marker id="arrowd2_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

1. Redis forks a child process
1. Child process writes all data to a temporary file
1. Child replaces previous RDB file with new one
1. Parent process never blocks (except during fork)

---

## Configuring RDB Snapshots

In `redis.conf`:

```redis
# Save after 900 sec (15 min) if at least 1 key changed
save 900 1

# Save after 300 sec (5 min) if at least 10 keys changed
save 300 10

# Save after 60 sec if at least 10000 keys changed
save 60 10000

# Filename for the RDB file
dbfilename dump.rdb

# Directory for RDB file
dir /var/lib/redis

# Disable RDB snapshots
save ""
```

---

## RDB Manual Commands

Trigger snapshots manually:

```bash
# Synchronous save (blocks Redis until complete)
SAVE

# Asynchronous save (forks process)
BGSAVE

# Last successful save timestamp
LASTSAVE
```

Example:
```bash
127.0.0.1:6379> BGSAVE
Background saving started
```

---

## RDB Advantages and Disadvantages

**Advantages**:
- Compact single-file format
- Perfect for backups
- Faster restarts than AOF
- Better performance impact
- Can be used for replicas

**Disadvantages**:
- More data loss in case of crashes
- Less frequent snapshots
- Fork can be expensive with large datasets
- Potential stalls during fork on low memory

---

## AOF (Append-Only File)

Log of all write operations that modify data:

- Logs every write operation as it occurs
- Higher durability than RDB
- Can be compacted/rewritten to save space
- Easier to understand (plain text commands)
- Better for recovery with less data loss

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_05_persistence)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd3_05_persistence)"/>
  <defs>
    <marker id="arrowd3_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Configuring AOF

In `redis.conf`:

```redis
# Enable AOF
appendonly yes

# AOF filename
appendfilename "appendonly.aof"

# fsync policy (always, everysec, no)
appendfsync everysec

# Automatic AOF rewriting
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

---

## AOF Sync Options

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="160" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="52" text-anchor="middle" font-size="11" font-weight="bold">always</text>
  <text x="100" y="70" text-anchor="middle" font-size="10">fsync every write</text>
  <rect x="220" y="30" width="160" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">everysec</text>
  <text x="300" y="70" text-anchor="middle" font-size="10">fsync once/second</text>
  <rect x="420" y="30" width="160" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="52" text-anchor="middle" font-size="11" font-weight="bold">no</text>
  <text x="500" y="70" text-anchor="middle" font-size="10">OS decides when</text>
  <rect x="20" y="110" width="160" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="100" y="130" text-anchor="middle" font-size="10">Safest, slowest</text>
  <text x="100" y="148" text-anchor="middle" font-size="10">~1ms data loss</text>
  <rect x="220" y="110" width="160" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="130" text-anchor="middle" font-size="10">Good compromise</text>
  <text x="300" y="148" text-anchor="middle" font-size="10">~1s data loss</text>
  <rect x="420" y="110" width="160" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="500" y="130" text-anchor="middle" font-size="10">Fastest, riskiest</text>
  <text x="500" y="148" text-anchor="middle" font-size="10">~30s data loss</text>
</svg>

---

## AOF Rewriting

AOF files grow continuously and need compaction:

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_05_persistence)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd5_05_persistence)"/>
  <defs>
    <marker id="arrowd5_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## AOF Rewriting Commands

Trigger AOF rewriting manually:

```bash
# Asynchronous AOF rewrite
BGREWRITEAOF
```

Example:
```bash
127.0.0.1:6379> BGREWRITEAOF
Background append only file rewriting started
```

---

## AOF Advantages and Disadvantages

**Advantages**:
- Better durability (less data loss)
- Automatic rewrites to manage file size
- Easier to understand and parse
- Safe append-only operations
- Per-command granularity

**Disadvantages**:
- Larger files than RDB
- Slower restart times
- Sometimes slower than RDB depending on fsync policy
- Potential bugs historically (though rare now)

---

## Hybrid Persistence

Combine both RDB and AOF (Redis 4.0+):

```redis
# Enable AOF
appendonly yes

# Enable RDB + AOF hybrid mode
aof-use-rdb-preamble yes
```

How it works:
- AOF file starts with RDB snapshot (preamble)
- Commands since snapshot are appended after
- Faster restarts than pure AOF
- Better durability than pure RDB

---

## Hybrid Persistence File Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="540" height="160" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="12" font-weight="bold">Hybrid AOF File Structure</text>
  <rect x="50" y="60" width="240" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="170" y="82" text-anchor="middle" font-size="11" font-weight="bold">RDB Preamble</text>
  <text x="170" y="100" text-anchor="middle" font-size="10">Binary snapshot (fast load)</text>
  <rect x="310" y="60" width="240" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="430" y="82" text-anchor="middle" font-size="11" font-weight="bold">AOF Commands</text>
  <text x="430" y="100" text-anchor="middle" font-size="10">Since last snapshot</text>
  <line x1="295" y1="85" x2="305" y2="85" stroke="#333" stroke-width="3"/>
  <text x="170" y="145" text-anchor="middle" font-size="10" fill="#1565c0">Fast restart</text>
  <text x="430" y="145" text-anchor="middle" font-size="10" fill="#7b1fa2">Minimal data loss</text>
  <line x1="50" y1="125" x2="550" y2="125" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
</svg>

Benefits:
- Fast loading (RDB portion)
- Minimal data loss (AOF portion)
- Optimal space usage

---

## No Persistence

Redis can run without persistence:

```redis
# Disable RDB
save ""

# Disable AOF
appendonly no
```

Use cases:
- Pure cache
- Temporary data
- Volatile session storage
- When durability is handled elsewhere
- Development/testing environments

---

## Monitoring Persistence

Monitor persistence operations:

```bash
# Check RDB and AOF status
INFO persistence

# Sample output
# Persistence
loading:0
rdb_changes_since_last_save:0
rdb_bgsave_in_progress:0
rdb_last_save_time:1592211444
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:0
rdb_current_bgsave_time_sec:-1
rdb_last_cow_size:0
aof_enabled:1
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_last_write_status:ok
aof_last_cow_size:0
```

---

## Persistence and Memory Usage

Copy-On-Write (COW) mechanism:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="15" width="160" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="38" text-anchor="middle" font-size="11" font-weight="bold">Parent Process</text>
  <text x="110" y="55" text-anchor="middle" font-size="10">Shared memory</text>
  <text x="110" y="72" text-anchor="middle" font-size="10">pages: A B C D</text>
  <rect x="30" y="105" width="160" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="128" text-anchor="middle" font-size="11" font-weight="bold">Child Process</text>
  <text x="110" y="145" text-anchor="middle" font-size="10">Reads shared pages</text>
  <text x="110" y="162" text-anchor="middle" font-size="10">for RDB dump</text>
  <line x1="200" y1="50" x2="280" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_05_persistence)"/>
  <text x="240" y="43" font-size="9">write to A</text>
  <rect x="290" y="15" width="130" height="70" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="355" y="38" text-anchor="middle" font-size="11" font-weight="bold">COW Copy</text>
  <text x="355" y="55" text-anchor="middle" font-size="10">Page A copied</text>
  <text x="355" y="72" text-anchor="middle" font-size="10">before write</text>
  <rect x="440" y="15" width="140" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="38" text-anchor="middle" font-size="10">B, C, D still shared</text>
  <text x="510" y="55" text-anchor="middle" font-size="10">Memory efficient</text>
  <text x="510" y="72" text-anchor="middle" font-size="10">until modified</text>
  <rect x="290" y="110" width="290" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="435" y="132" text-anchor="middle" font-size="10">Peak memory = base + modified pages only</text>
  <text x="435" y="150" text-anchor="middle" font-size="10">High write load = more COW memory usage</text>
  <defs>
    <marker id="arrowd7_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- Child process shares memory with parent process
- When parent modifies data, memory is copied (Copy-On-Write)
- Maximum memory usage = original + modified pages
- Can be significant with large datasets and high write loads

---

## Managing Persistence Performance

Minimize impact on main Redis process:

1. **Schedule during low-traffic periods**:
    - Configure `save` directives carefully
    - Use `cron` to trigger manual BGSAVE

1. **Allocate sufficient memory**:
    - Account for COW memory usage
    - Set `maxmemory` below total available RAM

1. **CPU considerations**:
    - Ensure multiple cores for forked processes
    - Monitor CPU usage during persistence operations

1. **Disk I/O optimization**:
    - Use fast storage (SSD/NVMe)
    - Separate Redis data from OS/swap

---

## Backup Strategies

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="25" width="120" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="48" text-anchor="middle" font-size="11" font-weight="bold">Redis</text>
  <text x="90" y="68" text-anchor="middle" font-size="10">BGSAVE</text>
  <line x1="155" y1="55" x2="210" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_05_persistence)"/>
  <rect x="220" y="25" width="120" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="280" y="48" text-anchor="middle" font-size="11" font-weight="bold">dump.rdb</text>
  <text x="280" y="68" text-anchor="middle" font-size="10">Local disk</text>
  <line x1="345" y1="55" x2="400" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_05_persistence)"/>
  <text x="370" y="48" font-size="9">copy</text>
  <rect x="410" y="25" width="160" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="48" text-anchor="middle" font-size="11" font-weight="bold">Off-site Storage</text>
  <text x="490" y="68" text-anchor="middle" font-size="10">S3 / NFS / remote</text>
  <rect x="30" y="110" width="540" height="60" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="132" text-anchor="middle" font-size="11" font-weight="bold">Retention Policy</text>
  <text x="300" y="152" text-anchor="middle" font-size="10">Daily (7d) | Weekly (4w) | Monthly (12m) - automate with cron</text>
  <defs>
    <marker id="arrowd8_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Best practices:
- Store backups off-server
- Implement retention policies (daily, weekly, monthly)
- Test backup restoration regularly
- Script and automate backup processes

---

## Recovery Procedures

Restoring from backups:

1. **RDB restore**:
    - Stop Redis
    - Copy RDB file to data directory
    - Start Redis

1. **AOF restore**:
    - Stop Redis
    - Copy AOF file to data directory
    - Start Redis

1. **Verification**:
    - Check Redis logs for successful loading
    - Verify data with sample queries
    - Monitor memory usage

---

## Corrupted AOF Recovery

If the AOF file becomes corrupted:

```bash
# Check and fix corrupted AOF file
redis-check-aof [--fix] <aof-file>
```

Example:
```bash
$ redis-check-aof --fix appendonly.aof
AOF analyzed: size=1052, ok_up_to=1024, diff=28
This will shrink the AOF from 1052 bytes to 1024 bytes
Continue? [y/N] y
Successfully truncated AOF
```

---

## Corrupted RDB Recovery

If the RDB file becomes corrupted:

```bash
# Check corrupted RDB file
redis-check-rdb <rdb-file>
```

Example:
```bash
$ redis-check-rdb dump.rdb
[offset 0] Checking RDB file dump.rdb
[offset 18] AUX FIELD redis-ver = '6.0.5'
[offset 32] AUX FIELD redis-bits = '64'
...
[offset 92] EOF is OK
```

Note: RDB files cannot be fixed - must restore from backup

---

## Point-in-Time Recovery

Combining RDB and AOF for point-in-time recovery:

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd9_05_persistence)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd9_05_persistence)"/>
  <defs>
    <marker id="arrowd9_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Persistence in Replicated Setup

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="10" width="200" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="28" text-anchor="middle" font-size="11" font-weight="bold">Master (writes)</text>
  <text x="300" y="45" text-anchor="middle" font-size="10">No persistence (optional)</text>
  <line x1="250" y1="60" x2="110" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd10_05_persistence)"/>
  <line x1="350" y1="60" x2="490" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd10_05_persistence)"/>
  <rect x="30" y="95" width="160" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="113" text-anchor="middle" font-size="11" font-weight="bold">Replica 1 (reads)</text>
  <text x="110" y="130" text-anchor="middle" font-size="10">AOF enabled</text>
  <rect x="410" y="95" width="160" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="113" text-anchor="middle" font-size="11" font-weight="bold">Replica 2 (backup)</text>
  <text x="490" y="130" text-anchor="middle" font-size="10">RDB snapshots</text>
  <rect x="120" y="155" width="360" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="177" text-anchor="middle" font-size="10">Offload persistence to replicas to reduce master load</text>
  <defs>
    <marker id="arrowd10_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Strategies:
- Distribute persistence load across replicas
- Configure different persistence strategies per role
- Use dedicated backup replicas

---

## Persistence for Replication

RDB's role in replication:

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd11_05_persistence)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd11_05_persistence)"/>
  <defs>
    <marker id="arrowd11_05_persistence" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- RDB file provides initial sync data
- Even with AOF enabled, replication uses RDB
- Partial resynchronization uses in-memory backlog

---

## Persistence in Redis Cluster

Redis Cluster persistence considerations:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="160" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="42" text-anchor="middle" font-size="11" font-weight="bold">Master A</text>
  <text x="110" y="60" text-anchor="middle" font-size="10">Slots 0-5460</text>
  <rect x="220" y="20" width="160" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="11" font-weight="bold">Master B</text>
  <text x="300" y="60" text-anchor="middle" font-size="10">Slots 5461-10922</text>
  <rect x="410" y="20" width="160" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="42" text-anchor="middle" font-size="11" font-weight="bold">Master C</text>
  <text x="490" y="60" text-anchor="middle" font-size="10">Slots 10923-16383</text>
  <rect x="50" y="95" width="120" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="117" text-anchor="middle" font-size="10">RDB + AOF</text>
  <rect x="240" y="95" width="120" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="117" text-anchor="middle" font-size="10">RDB + AOF</text>
  <rect x="430" y="95" width="120" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="490" y="117" text-anchor="middle" font-size="10">RDB + AOF</text>
  <rect x="60" y="145" width="480" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="162" text-anchor="middle" font-size="10">Each node persists independently -- coordinate backups cluster-wide</text>
  <text x="300" y="178" text-anchor="middle" font-size="10">Use consistent persistence config across all nodes</text>
</svg>

- Each node manages persistence independently
- Need consistent configuration across nodes
- Backups should be coordinated cluster-wide
- Recovery might involve entire cluster rebuild

---

## Persistence Performance Benchmarking

Measure impact of persistence options:

```bash
# Using redis-benchmark
redis-benchmark -t set,get -n 1000000

# Compare with different persistence options
# - No persistence
# - RDB only
# - AOF with different fsync options
# - RDB + AOF hybrid mode
```

Monitor:
- Throughput (operations/second)
- Latency (average and percentiles)
- Memory usage (resident set size)
- CPU usage during persistence operations
- Disk I/O (writes per second)

---

## Typical Performance Impact

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Persistence Performance Impact</text>
  <rect x="20" y="35" width="100" height="130" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="70" y="55" text-anchor="middle" font-size="10" font-weight="bold">None</text>
  <rect x="35" y="65" width="70" height="90" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="70" y="115" text-anchor="middle" font-size="10">0%</text>
  <rect x="140" y="35" width="100" height="130" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="190" y="55" text-anchor="middle" font-size="10" font-weight="bold">RDB</text>
  <rect x="155" y="85" width="70" height="70" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="190" y="125" text-anchor="middle" font-size="10">~2-5%</text>
  <rect x="260" y="35" width="100" height="130" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="310" y="55" text-anchor="middle" font-size="10" font-weight="bold">AOF/sec</text>
  <rect x="275" y="75" width="70" height="80" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="310" y="120" text-anchor="middle" font-size="10">~5-15%</text>
  <rect x="380" y="35" width="100" height="130" fill="#ffebee" stroke="#333" stroke-width="2" rx="3"/>
  <text x="430" y="55" text-anchor="middle" font-size="10" font-weight="bold">AOF/always</text>
  <rect x="395" y="60" width="70" height="95" fill="#ffebee" stroke="#333" stroke-width="1"/>
  <text x="430" y="115" text-anchor="middle" font-size="10">~30-50%</text>
  <rect x="500" y="35" width="80" height="130" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="3"/>
  <text x="540" y="55" text-anchor="middle" font-size="10" font-weight="bold">Hybrid</text>
  <rect x="510" y="80" width="60" height="75" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="540" y="122" text-anchor="middle" font-size="10">~5-15%</text>
  <text x="300" y="190" text-anchor="middle" font-size="10">Approximate throughput reduction (write-heavy workload)</text>
</svg>

Note:
- Actual percentages will vary based on workload
- Write-heavy workloads show greater impact
- Read-heavy workloads show minimal impact
- System specifications significantly influence results

---

## Persistence Best Practices

1. **Match persistence to durability requirements**:
    - Critical data: AOF with fsync=always
    - Important data: AOF with fsync=everysec
    - Cached data: RDB snapshots or no persistence

1. **Plan for disk space**:
    - Monitor AOF and RDB file sizes
    - Configure auto-rewrite thresholds
    - Implement backup rotation and cleanup

1. **Schedule around traffic patterns**:
    - Trigger BGSAVE during low traffic
    - Configure save directives accordingly

1. **Resource allocation**:
    - Allocate sufficient memory for COW
    - Fast storage for persistence files
    - Separate Redis data directory

---

## Trade-offs: Choosing the Right Strategy

Decision matrix based on requirements:

| Requirement | RDB | AOF (everysec) | AOF (always) | Hybrid |
|-------------|-----|----------------|--------------|--------|
| Performance | ✓✓✓ | ✓✓ | ✗ | ✓✓ |
| Durability | ✗ | ✓✓ | ✓✓✓ | ✓✓ |
| Recovery speed | ✓✓✓ | ✗ | ✗ | ✓✓ |
| Disk space | ✓✓✓ | ✗ | ✗ | ✓✓ |
| Setup complexity | ✓✓✓ | ✓✓ | ✓✓ | ✓ |

---

## Advanced: External Persistence

Alternative persistence approaches:

1. **External backups**:
    - LVM/filesystem snapshots
    - Storage-level snapshots
    - Database specific backup tools

1. **Diskless replication**:
    - Replicate without disk involvement
    - Useful for read-scaling

1. **Redis Enterprise**:
    - Advanced persistence options
    - ACID compliant durability

---

## Lab: Redis Persistence

1. **Exercise 1**: Configure RDB snapshots
1. **Exercise 2**: Set up and test AOF persistence
1. **Exercise 3**: Implement hybrid persistence
1. **Exercise 4**: Trigger manual backups
1. **Exercise 5**: Simulate server failure and recover
1. **Exercise 6**: Benchmark different persistence options
1. **Exercise 7**: Set up a backup strategy

---

## Summary

- Redis provides multiple persistence options
- RDB: Point-in-time snapshots, fast but less durable
- AOF: Command logging, durable but larger files
- Hybrid mode: Combines advantages of both
- No single "best" persistence strategy
- Choose based on durability, performance needs
- Implement proper backup and recovery procedures
- Test recovery scenarios regularly

Next chapter: Redis Configuration and Management
