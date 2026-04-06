# Advanced Docker Storage and Volumes

Persistent data management for containers

---

## Agenda

- Storage drivers and how they work
- Copy-on-Write (`CoW`) mechanism
- Bind mounts vs named volumes vs `tmpfs`
- Volume drivers and plugins
- Data management patterns
- Backup and restore strategies
- Performance considerations

---

## Docker Storage Architecture

```diagram
┌─────────────────────────────────────────────┐
│              Container Layer (R/W)           │
├─────────────────────────────────────────────┤
│              Image Layer 3 (RO)              │
├─────────────────────────────────────────────┤
│              Image Layer 2 (RO)              │
├─────────────────────────────────────────────┤
│              Image Layer 1 (RO)              │
├─────────────────────────────────────────────┤
│              Base Image Layer (RO)           │
├─────────────────────────────────────────────┤
│           Storage Driver (overlay2)          │
├─────────────────────────────────────────────┤
│           Filesystem (ext4, xfs)             │
└─────────────────────────────────────────────┘
```

---

## Storage Drivers Comparison

| Driver       | Backing FS     | Status          | Performance |
|-------------|----------------|-----------------|-------------|
| `overlay2`  | `ext4`, `xfs`  | Recommended     | Excellent   |
| `fuse-overlayfs` | Any       | Rootless        | Good        |
| `btrfs`     | `btrfs`        | Stable          | Good        |
| `zfs`       | `zfs`          | Stable          | Good        |
| `devicemapper`| Direct-lvm   | Deprecated      | Good        |
| `vfs`       | Any            | Debug/testing   | Poor        |

```bash
# Check current storage driver
docker info --format '{{.Driver}}'

# Set in daemon.json
{
  "storage-driver": "overlay2"
}
```

---

## `overlay2` - How It Works

```bash
# overlay2 uses OverlayFS in the Linux kernel
# Each layer is a directory under /var/lib/docker/overlay2/

ls /var/lib/docker/overlay2/
# <layer-hash>/
#   ├── diff/        # Actual layer content
#   ├── merged/      # Union mount view (running containers only)
#   ├── work/        # OverlayFS work directory
#   ├── lower        # File pointing to parent layers
#   └── link         # Short symlink identifier

# View mount for a running container
mount | grep overlay
# overlay on /var/lib/docker/overlay2/<id>/merged type overlay
#   (lowerdir=...,upperdir=...,workdir=...)
```

---

## Copy-on-Write (`CoW`) Explained

```diagram
Read operation:
┌───────────────┐
│  Upper (R/W)  │  file not found → look in lower
├───────────────┤
│  Lower (RO)   │  ← file found here, read directly
└───────────────┘

Write operation (existing file):
┌───────────────┐
│  Upper (R/W)  │  ← file copied here, then modified
├───────────────┤
│  Lower (RO)   │  original unchanged
└───────────────┘

Delete operation:
┌───────────────┐
│  Upper (R/W)  │  ← whiteout file created
├───────────────┤
│  Lower (RO)   │  original still exists but hidden
└───────────────┘
```

---

## `CoW` Performance Implications

```bash
# CoW has a first-write penalty for large files
# Every first modification copies the entire file to the upper layer

# Example: modifying a 1GB database file
docker run -d --name db postgres:16
# First write to the database file:
#   1. Copy entire file from lower to upper layer
#   2. Modify the copy
#   3. Subsequent writes happen in upper (fast)

# This is why databases should ALWAYS use volumes!
docker run -d --name db \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

---

## Three Types of Mounts

```diagram
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Bind    │  │  Named   │  │  tmpfs   │      │
│  │  Mount   │  │  Volume  │  │  Mount   │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│       │              │              │            │
│   Host path     Docker-managed   RAM only       │
│   /home/user    /var/lib/docker   No disk I/O   │
│   /data/app     /volumes/...                    │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Bind Mounts

```bash
# Mount a host directory into the container
docker run -d --name web \
  -v /var/www/html:/usr/share/nginx/html \
  nginx

# Modern syntax with --mount
docker run -d --name web \
  --mount type=bind,source=/var/www/html,target=/usr/share/nginx/html \
  nginx

# Read-only bind mount
docker run -d --name web \
  -v /var/www/html:/usr/share/nginx/html:ro \
  nginx

# Bind mount a single file
docker run -d --name web \
  -v /path/to/nginx.conf:/etc/nginx/nginx.conf:ro \
  nginx
```

---

## Bind Mount Options

```bash
# Propagation modes
docker run -d \
  --mount type=bind,source=/data,target=/data,bind-propagation=shared \
  myapp

# Propagation options:
# rprivate  (default) - No propagation
# private   - No propagation
# rshared   - Bidirectional propagation
# shared    - Bidirectional propagation
# rslave    - One-way host→container
# slave     - One-way host→container

# SELinux labels
docker run -d \
  -v /data:/data:z \    # Shared label (multiple containers)
  myapp

docker run -d \
  -v /data:/data:Z \    # Private label (single container)
  myapp
```

---

## Named Volumes

```bash
# Create a named volume
docker volume create mydata

# Use the volume
docker run -d --name db \
  -v mydata:/var/lib/postgresql/data \
  postgres:16

# Volume persists after container removal
docker rm -f db
docker volume ls
# mydata still exists

# Inspect volume
docker volume inspect mydata
# {
#   "Driver": "local",
#   "Mountpoint": "/var/lib/docker/volumes/mydata/_data",
#   "Name": "mydata",
#   "Scope": "local"
# }
```

---

## Volume with Driver Options

```bash
# Create volume with specific options
docker volume create --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/exports/data \
  nfs-data

# Create volume with tmpfs backend
docker volume create --driver local \
  --opt type=tmpfs \
  --opt device=tmpfs \
  --opt o=size=100m,uid=1000 \
  tmpfs-vol

# Create volume bound to a specific host path
docker volume create --driver local \
  --opt type=none \
  --opt device=/data/myapp \
  --opt o=bind \
  local-data
```

---

## `tmpfs` Mounts

```bash
# Store data in memory only - never written to disk
docker run -d --name secure \
  --tmpfs /run:rw,noexec,nosuid,size=100m \
  myapp

# Modern syntax
docker run -d --name secure \
  --mount type=tmpfs,destination=/run,tmpfs-size=100m,tmpfs-mode=1777 \
  myapp

# Use cases:
# - Sensitive data (secrets, tokens)
# - Temporary files that don't need persistence
# - High-performance scratch space
# - Session storage
```

---

## Bind Mounts vs Named Volumes

| Feature            | Bind Mount              | Named Volume           |
|--------------------|------------------------|------------------------|
| Location           | Anywhere on host       | `/var/lib/docker/volumes` |
| Pre-populated      | No                     | Yes (from image)       |
| Portability        | Host-dependent         | Portable               |
| Managed by Docker  | No                     | Yes                    |
| Backup             | Standard tools         | `docker volume` commands|
| Permission issues  | Common                 | Rare                   |
| Driver support     | Local only             | Multiple drivers       |

---

## Volume Data Pre-Population

```bash
# Named volumes are pre-populated from image content
# if the target directory in the image has files

# Example: nginx has files in /usr/share/nginx/html
docker volume create web-content
docker run -d --name web \
  -v web-content:/usr/share/nginx/html \
  nginx

# Volume now contains nginx default files
docker run --rm -v web-content:/data alpine ls /data
# 50x.html  index.html

# Bind mounts do NOT pre-populate
docker run -d --name web2 \
  -v /tmp/empty:/usr/share/nginx/html \
  nginx
# /tmp/empty is empty - container sees empty directory
```

---

## Volume Plugins - NFS

```bash
# Using the local driver with NFS
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=addr=nfs-server.example.com,vers=4,rw,soft \
  --opt device=:/exports/docker-data \
  nfs-volume

# In docker-compose
volumes:
  nfs-data:
    driver: local
    driver_opts:
      type: nfs
      o: "addr=nfs-server.example.com,vers=4,rw,soft"
      device: ":/exports/docker-data"
```

---

## Volume Plugins - Cloud Storage

```bash
# REX-Ray plugin for AWS EBS
docker plugin install rexray/ebs

docker volume create --driver rexray/ebs \
  --opt size=100 \
  --opt volumetype=gp3 \
  ebs-data

# Azure File Storage
docker plugin install docker4x/cloudstor:azure

docker volume create --driver cloudstor:azure \
  --opt share=myshare \
  azure-data

# GCE Persistent Disk
docker volume create --driver gce \
  --opt size=100 \
  gce-data
```

---

## Volume Plugins - Distributed Storage

```bash
# GlusterFS
docker volume create --driver glusterfs \
  --opt servers=server1,server2,server3 \
  --opt volname=gv0 \
  gluster-data

# Portworx
docker volume create --driver pxd \
  --opt size=10 \
  --opt repl=3 \
  --opt io_profile=db \
  px-data

# CEPH RBD
docker volume create --driver rbd \
  --opt pool=docker \
  --opt size=10G \
  ceph-data
```

---

## Sharing Data Between Containers

```bash
# Pattern 1: Named volume shared between containers
docker volume create shared-data

docker run -d --name writer \
  -v shared-data:/data \
  alpine sh -c 'while true; do date >> /data/log.txt; sleep 1; done'

docker run -d --name reader \
  -v shared-data:/data:ro \
  alpine tail -f /data/log.txt

# Pattern 2: Volumes-from (copies volume mounts)
docker run -d --name data-container \
  -v /config -v /data \
  busybox true

docker run -d --volumes-from data-container myapp
docker run -d --volumes-from data-container:ro mybackup
```

---

## Backup and Restore Volumes

```bash
# Backup a named volume to a tar file
docker run --rm \
  -v mydata:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/mydata-backup.tar.gz -C /source .

# Restore from backup
docker volume create mydata-restored
docker run --rm \
  -v mydata-restored:/target \
  -v $(pwd):/backup:ro \
  alpine sh -c 'cd /target && tar xzf /backup/mydata-backup.tar.gz'

# Backup with timestamp
BACKUP_NAME="mydata-$(date +%Y%m%d-%H%M%S).tar.gz"
docker run --rm \
  -v mydata:/source:ro \
  -v /backups:/backup \
  alpine tar czf /backup/$BACKUP_NAME -C /source .
```

---

## Database Volume Backup Strategies

```bash
# PostgreSQL backup using pg_dump
docker exec postgres-db \
  pg_dump -U postgres mydb > backup.sql

# Or use a sidecar container
docker run --rm \
  --network db-net \
  -v /backups:/backup \
  postgres:16 \
  pg_dump -h postgres-db -U postgres mydb \
    > /backup/mydb-$(date +%F).sql

# MySQL backup
docker exec mysql-db \
  mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" mydb > backup.sql

# MongoDB backup
docker exec mongo-db \
  mongodump --archive > /backups/mongo-$(date +%F).archive
```

---

## Volume Lifecycle Management

```bash
# List all volumes
docker volume ls

# List dangling (unused) volumes
docker volume ls --filter dangling=true

# Remove a specific volume
docker volume rm mydata

# Remove all unused volumes
docker volume prune

# Remove all unused volumes (including named)
docker volume prune --all

# Force remove (no confirmation)
docker volume prune -f

# Volume with labels for management
docker volume create --label env=prod --label app=web web-data
docker volume ls --filter label=env=prod
```

---

## Storage Performance - Benchmarking

```bash
# Benchmark different storage options
# Test 1: Container writable layer (CoW)
docker run --rm alpine sh -c \
  'dd if=/dev/zero of=/tmp/test bs=1M count=1000 oflag=direct 2>&1'

# Test 2: Named volume
docker run --rm -v test-vol:/data alpine sh -c \
  'dd if=/dev/zero of=/data/test bs=1M count=1000 oflag=direct 2>&1'

# Test 3: Bind mount
docker run --rm -v /tmp/bench:/data alpine sh -c \
  'dd if=/dev/zero of=/data/test bs=1M count=1000 oflag=direct 2>&1'

# Test 4: tmpfs
docker run --rm --tmpfs /data:size=2G alpine sh -c \
  'dd if=/dev/zero of=/data/test bs=1M count=1000 2>&1'
```

---

## Storage Performance Comparison

```misc
Typical I/O throughput (sequential write):

tmpfs (RAM)         ████████████████████████████  ~2000 MB/s
Bind mount (SSD)    ██████████████████            ~1200 MB/s
Named volume (SSD)  █████████████████             ~1150 MB/s
Container layer     █████████████                 ~800 MB/s
NFS volume          ████████                      ~500 MB/s
```

- `tmpfs` is fastest (memory-speed) but non-persistent
- Named volumes and bind mounts have similar performance
- Container writable layer has `CoW` overhead
- Network volumes depend on network bandwidth and latency

---

## Storage Quotas and Limits

```bash
# Limit container writable layer size (overlay2 + xfs)
docker run -d --storage-opt size=10G myapp

# Requires XFS backing filesystem with pquota mount option
# /etc/fstab: /dev/sda1 /var/lib/docker xfs defaults,pquota 0 0

# Set default storage size in daemon.json
{
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.size=10G"
  ]
}

# Tmpfs size limit
docker run -d --tmpfs /tmp:size=100m myapp
```

---

## Docker Compose Volume Patterns

```yaml
services:
  web:
    image: nginx
    volumes:
      # Named volume
      - web-content:/usr/share/nginx/html
      # Bind mount
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      # tmpfs
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100000000  # 100MB

  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  web-content:
  pgdata:
    driver: local
```

---

## Advanced Compose Volume Configuration

```yaml
volumes:
  # External volume (must exist before compose up)
  existing-data:
    external: true

  # NFS volume
  nfs-data:
    driver: local
    driver_opts:
      type: nfs
      o: "addr=192.168.1.100,vers=4,rw"
      device: ":/exports/data"

  # Volume with labels
  app-data:
    labels:
      com.example.environment: "production"
      com.example.backup: "daily"

  # Named volume with custom driver
  cloud-data:
    driver: rexray/ebs
    driver_opts:
      size: "100"
      volumetype: "gp3"
```

---

## Handling Permissions with Volumes

```dockerfile
# Common issue: container user can't write to volume

# Solution 1: Set ownership in Dockerfile
FROM node:20-alpine
RUN mkdir -p /app/data && chown -R node:node /app/data
USER node
VOLUME /app/data

# Solution 2: Use entrypoint script to fix permissions
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
```

```bash
#!/bin/bash
# docker-entrypoint.sh
# Fix ownership if running as root
if [ "$(id -u)" = "0" ]; then
  chown -R appuser:appgroup /app/data
  exec gosu appuser "$@"
fi
exec "$@"
```

---

## Named Volume Init Container Pattern

```yaml
# Initialize volume data using an init container
services:
  init-data:
    image: myapp:latest
    volumes:
      - app-config:/config
    command: ["cp", "-r", "/defaults/.", "/config/"]
    restart: "no"

  app:
    image: myapp:latest
    volumes:
      - app-config:/config:ro
    depends_on:
      init-data:
        condition: service_completed_successfully

volumes:
  app-config:
```

---

## Cleaning Up Docker Disk Usage

```bash
# View disk usage summary
docker system df

# Detailed view
docker system df -v

# Example output:
# TYPE           TOTAL   ACTIVE   SIZE      RECLAIMABLE
# Images         25      5        8.5GB     6.2GB (72%)
# Containers     10      3        500MB     350MB (70%)
# Local Volumes  15      5        2.1GB     1.5GB (71%)
# Build Cache    -       -        3.2GB     3.2GB

# Full cleanup (unused images, containers, volumes, networks)
docker system prune --all --volumes

# Individual cleanup
docker image prune -a
docker container prune
docker volume prune
docker builder prune
```

---

## Summary - Docker Storage

- `overlay2` is the recommended storage driver with `CoW` semantics
- Use **named volumes** for persistent data (databases, uploads)
- Use **bind mounts** for development and config injection
- Use **`tmpfs`** for sensitive data and high-speed scratch space
- Never store important data in the container writable layer
- Volume plugins enable `NFS`, cloud storage, and distributed storage
- Pre-populate volumes from image content (named volumes only)
- Implement regular backup strategies for data volumes
- Monitor disk usage with `docker system df`
