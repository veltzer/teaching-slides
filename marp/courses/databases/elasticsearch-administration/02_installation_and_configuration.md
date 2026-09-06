---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Installation and Configuration

---

## What This Chapter Covers

- System requirements and sizing guidelines
- Installation methods and packages
- Directory structure and file layout
- elasticsearch.yml core configuration
- JVM configuration and heap sizing
- Network and transport settings
- Starting and stopping services with systemd
- Cluster bootstrapping

---

## System Requirements

- 64-bit Linux is the recommended production OS
- Modern multi-core CPUs; more cores aid concurrency
- Fast local SSD/NVMe storage strongly preferred
- Avoid network-attached storage for data nodes where possible
- Java is bundled with Elasticsearch (no separate JDK install)
- Reliable, low-latency network between nodes

---

## Sizing Guidelines

- Plan capacity around data volume, retention, and query load
- Keep RAM generous; split between JVM heap and OS file cache
- Heap ≤ 50% of RAM and ≤ ~31 GB (compressed object pointers)
- Aim for shards roughly 10–50 GB each for log/time-series data
- Avoid over-sharding: too many small shards waste heap
- Leave headroom for replicas and growth

---

## Installation Methods

- Archive: `tar.gz` (Linux) — flexible, manual setup
- Debian package: `.deb` via apt repository
- RPM package: `.rpm` via yum/dnf repository
- Container: official Docker image
- Kubernetes: ECK operator
- Packages integrate with systemd; archives run from any directory

---

## Installing the tar.gz Archive

- Download, extract, and run as a non-root user
- Self-contained under the extracted directory

```bash
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-linux-x86_64.tar.gz
tar -xzf elasticsearch-9.0.0-linux-x86_64.tar.gz
cd elasticsearch-9.0.0/
./bin/elasticsearch
```

---

## Installing the deb/rpm Packages

- Packages install to system paths and register a systemd service
- Use the Elastic apt or yum repository for upgrades

```bash
# Debian/Ubuntu
sudo apt-get install elasticsearch

# RHEL/CentOS/Rocky
sudo dnf install elasticsearch
```

---

## Running with Docker

- Pull the official image and run a container
- Mount volumes for persistent data

```bash
docker run --name es01 \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -v es-data:/usr/share/elasticsearch/data \
  docker.elastic.co/elasticsearch/elasticsearch:9.0.0
```

---

## Directory Structure (Archive)

- `bin/` — executables (elasticsearch, elasticsearch-keystore)
- `config/` — elasticsearch.yml, jvm.options, log4j2.properties
- `data/` — shard data (set `path.data`)
- `logs/` — log files (set `path.logs`)
- `plugins/` — installed plugins
- `modules/` — bundled modules

---

## Directory Structure (Packages)

- Config: `/etc/elasticsearch/`
- Data: `/var/lib/elasticsearch/`
- Logs: `/var/log/elasticsearch/`
- Binaries: `/usr/share/elasticsearch/`
- Systemd defaults: `/etc/default/elasticsearch` (deb) or `/etc/sysconfig/elasticsearch` (rpm)
- Keep data and logs off the root filesystem in production

---

## Configuring Paths

- Separate data and logs onto appropriate volumes
- `path.data` may list multiple paths (one shard per path)

```yaml
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
```

---

## elasticsearch.yml: Cluster and Node Identity

- All nodes in a cluster must share `cluster.name`
- Each node should have a unique, meaningful `node.name`

```yaml
cluster.name: prod-search
node.name: ${HOSTNAME}
```

---

## elasticsearch.yml: Network Settings

- `network.host` controls which interfaces the node binds to
- Setting a non-loopback host triggers production bootstrap checks
- HTTP API listens on port 9200; transport on 9300

```yaml
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300
```

---

## Discovery and Cluster Formation

- `discovery.seed_hosts` lists addresses to contact for forming a cluster
- `cluster.initial_master_nodes` seeds the very first election only

```yaml
discovery.seed_hosts:
  - 10.0.0.11:9300
  - 10.0.0.12:9300
  - 10.0.0.13:9300
cluster.initial_master_nodes:
  - es-node-1
  - es-node-2
  - es-node-3
```

---

## Important: initial_master_nodes

- Only used the first time a brand-new cluster bootstraps
- Lists the `node.name` values of the initial master-eligible nodes
- Must be removed (or left harmless) after the cluster forms
- Never set it on nodes joining an existing cluster
- Misuse can split a cluster into two separate clusters

---

## JVM Configuration

- JVM options live in `config/jvm.options` and `jvm.options.d/`
- Prefer a drop-in file in `jvm.options.d/` for custom settings
- Set min and max heap to the same value to avoid resizing pauses

```properties
# config/jvm.options.d/heap.options
-Xms16g
-Xmx16g
```

---

## Heap Sizing Rules

- Set heap to no more than 50% of physical RAM
- Keep the remaining RAM for the Lucene OS file cache
- Stay at or below ~31 GB to keep compressed ordinary object pointers
- Above ~32 GB, pointers grow and effective memory drops
- Larger machines: run multiple nodes rather than huge heaps

---

## Network and Transport

- HTTP (9200): REST/client traffic, Kibana, applications
- Transport (9300): inter-node communication within the cluster
- Restrict ports with firewalls; expose 9200 only where needed
- Use dedicated, low-latency networking between nodes
- TLS should secure both HTTP and transport in production

---

## System-Level Tuning

- Disable swap or set `bootstrap.memory_lock: true`
- Raise file descriptor and `vm.max_map_count` limits
- These are enforced by bootstrap checks in production mode

```yaml
bootstrap.memory_lock: true
```

```bash
sudo sysctl -w vm.max_map_count=262144
```

---

## Starting and Stopping with systemd

- Packages register an `elasticsearch` systemd service
- Enable it to start on boot

```bash
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
sudo systemctl status elasticsearch
```

---

## Verifying the Installation

- Confirm the node responds and check cluster health
- Security is on by default; use credentials/TLS as configured

```bash
curl -k -u elastic:$PASSWORD https://localhost:9200
curl -k -u elastic:$PASSWORD https://localhost:9200/_cluster/health?pretty
```

---

## Cluster Bootstrapping Checklist

- Configure `cluster.name`, `node.name`, `network.host` on every node
- Set `discovery.seed_hosts` on all nodes
- Set `cluster.initial_master_nodes` only on first bootstrap
- Size heap consistently across nodes
- Start master-eligible nodes, confirm election, then start data nodes
- Verify cluster health reaches green before going live
