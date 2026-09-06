---
tags:
  - tools:docker
  - infrastructure:containers
  - practices:devops
  - networking:networking
level: advanced
category: devops
audience:
  - audiences:developers

---

# Docker in Production

Logging, monitoring, health checks, and lifecycle management

---

## Agenda

- Logging drivers and strategies
- Monitoring and observability
- Health checks and self-healing
- Resource constraints and tuning
- Container lifecycle management
- Graceful shutdown patterns
- Update and rollback strategies
- Production deployment patterns

---

## Docker Logging Architecture

![docker_logging_architecture](svg/courses/devops/advanced-docker/06_production/docker_logging_architecture.svg)

---

## Logging Drivers

| Driver        | Description                    | Supports `docker logs` |
|---------------|--------------------------------|:----------------------:|
| `json-file`   | Default, `JSON` format files  | Yes                    |
| `local`       | Optimized local storage        | Yes                    |
| `journald`    | `systemd` journal              | Yes                    |
| `syslog`      | `syslog` daemon                | No                     |
| `fluentd`     | `Fluentd` collector            | No                     |
| `splunk`      | `Splunk` `HTTP` Event Collector| No                     |
| `awslogs`     | `AWS CloudWatch` Logs          | No                     |
| `gcplogs`     | `Google Cloud` Logging         | No                     |
| `none`        | No logging                     | No                     |

---

## `json-file` Logging Driver

```bash
# Default driver - logs stored as JSON files
# Location: /var/lib/docker/containers/<id>/<id>-json.log

# Configure log rotation (critical for production!)
docker run -d \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=5 \
  --log-opt compress=true \
  --name web nginx

# Global configuration in daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5",
    "compress": "true"
  }
}

# View logs
docker logs web
docker logs --tail 100 --follow --timestamps web
```

---

## `local` Logging Driver

```bash
# Optimized local driver (recommended over json-file)
# Uses protobuf format, more efficient compression
docker run -d \
  --log-driver=local \
  --log-opt max-size=10m \
  --log-opt max-file=5 \
  --log-opt compress=true \
  --name web nginx

# Global config
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "50m",
    "max-file": "5"
  }
}

# Still supports docker logs command
docker logs web
```

---

## Centralized Logging with `Fluentd`

```yaml
# docker-compose.yml
services:
  fluentd:
    image: fluent/fluentd:v1.16
    volumes:
      - ./fluent.conf:/fluentd/etc/fluent.conf
    ports:
      - "24224:24224"

  web:
    image: nginx
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: "docker.{{.Name}}"
        fluentd-async: "true"

  api:
    image: myapp
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: "docker.{{.Name}}"
```

---

## `Fluentd` Configuration

```xml
# fluent.conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<filter docker.**>
  @type parser
  key_name log
  reserve_data true
  <parse>
    @type json
  </parse>
</filter>

<match docker.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  logstash_prefix docker
  <buffer>
    @type file
    path /fluentd/buffer
    flush_interval 5s
    chunk_limit_size 5m
  </buffer>
</match>
```

---

## ELK Stack for Docker Logging

```yaml
# docker-compose.yml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - es-data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.12.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

volumes:
  es-data:
```

---

## Structured Logging Best Practices

```bash
# Application should output structured JSON to stdout
# Example application log output:
# {"timestamp":"2026-03-10T10:30:00Z","level":"info",
#  "message":"Request processed","method":"GET",
#  "path":"/api/users","status":200,"duration_ms":45}

# Don't log to files inside the container
# Log to stdout/stderr and let Docker handle it

# Label-based log routing
docker run -d \
  --log-opt labels=app,environment \
  --label app=web \
  --label environment=production \
  --name web nginx

# Tag template variables
docker run -d \
  --log-opt tag="{{.Name}}/{{.ID}}" \
  --name web nginx
```

---

## Monitoring with `Prometheus`

```yaml
# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus:v2.50.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prom-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:10.3.0
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prom-data:
  grafana-data:
```

---

## `Prometheus` Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Monitor Docker daemon
  - job_name: 'docker'
    static_configs:
      - targets: ['host.docker.internal:9323']

  # Monitor cAdvisor
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  # Monitor Node Exporter
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # Monitor application
  - job_name: 'app'
    static_configs:
      - targets: ['web:8080']
    metrics_path: '/metrics'
```

---

## `cAdvisor` - Container Metrics

```yaml
# Add cAdvisor for per-container metrics
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.1
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    ports:
      - "8080:8080"
    privileged: true
    devices:
      - /dev/kmsg
```

```misc
Metrics provided:
- CPU usage per container
- Memory usage and limits
- Network I/O
- Filesystem I/O
- Container count and status
```

---

## Docker Daemon Metrics

```bash
# Enable metrics endpoint in daemon.json
{
  "metrics-addr": "0.0.0.0:9323",
  "experimental": true
}

# Available metrics:
# engine_daemon_container_states_containers{state="running"}
# engine_daemon_image_actions_seconds
# engine_daemon_network_actions_seconds
# process_cpu_seconds_total
# process_resident_memory_bytes

# View metrics
curl http://localhost:9323/metrics
```

---

## `docker stats` - Built-in Monitoring

```bash
# Live resource usage for all running containers
docker stats

# Specific containers
docker stats web api db

# One-shot (no streaming)
docker stats --no-stream

# Custom format
docker stats --format \
  "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

# Example output:
# NAME   CPU %   MEM USAGE / LIMIT    NET I/O          BLOCK I/O
# web    0.15%   45.2MiB / 512MiB     1.2kB / 500B     8.2MB / 0B
# api    2.30%   128MiB / 1GiB        50kB / 30kB      12MB / 5MB
# db     1.50%   256MiB / 2GiB        100kB / 80kB     50MB / 30MB
```

---

## Health Checks - Dockerfile

```dockerfile
# HTTP health check
FROM nginx:alpine
HEALTHCHECK --interval=30s --timeout=5s \
  --start-period=10s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# TCP health check
FROM postgres:16
HEALTHCHECK --interval=30s --timeout=5s \
  --start-period=30s --retries=3 \
  CMD pg_isready -U postgres || exit 1

# Custom script
FROM myapp
COPY healthcheck.sh /usr/local/bin/
HEALTHCHECK --interval=15s --timeout=5s \
  --start-period=20s --retries=3 \
  CMD ["healthcheck.sh"]
```

---

## Health Check Parameters

| Parameter        | Default | Description                          |
|------------------|---------|--------------------------------------|
| `--interval`     | 30s     | Time between checks                 |
| `--timeout`      | 30s     | Max time for check to complete      |
| `--start-period` | 0s      | Grace period for startup            |
| `--retries`      | 3       | Consecutive failures before unhealthy|

```bash
# Health check exit codes:
# 0 = healthy
# 1 = unhealthy

# Override at runtime
docker run -d \
  --health-cmd="curl -f http://localhost:8080/health || exit 1" \
  --health-interval=10s \
  --health-timeout=3s \
  --health-retries=3 \
  --health-start-period=15s \
  myapp
```

---

## Health Check - Advanced Script

```bash
#!/bin/bash
# healthcheck.sh - Comprehensive health check

# Check 1: Main process is running
if ! pgrep -x "node" > /dev/null; then
    echo "Main process not running"
    exit 1
fi

# Check 2: HTTP endpoint responds
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  http://localhost:3000/health)
if [ "$HTTP_STATUS" != "200" ]; then
    echo "HTTP health check failed: $HTTP_STATUS"
    exit 1
fi

# Check 3: Database connectivity
if ! node -e "require('./db').ping()" 2>/dev/null; then
    echo "Database connection failed"
    exit 1
fi

# Check 4: Disk space
DISK_USAGE=$(df /app/data | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "Disk usage critical: ${DISK_USAGE}%"
    exit 1
fi

echo "All checks passed"
exit 0
```

---

## Monitoring Health Status

```bash
# View health status
docker inspect --format='{{.State.Health.Status}}' myapp
# healthy | unhealthy | starting

# View health check history
docker inspect --format='{{json .State.Health}}' myapp | jq

# Output:
# {
#   "Status": "healthy",
#   "FailingStreak": 0,
#   "Log": [
#     {
#       "Start": "2026-03-10T10:00:00Z",
#       "End": "2026-03-10T10:00:01Z",
#       "ExitCode": 0,
#       "Output": "All checks passed"
#     }
#   ]
# }

# List only healthy/unhealthy containers
docker ps --filter health=healthy
docker ps --filter health=unhealthy
```

---

## Health Checks in Docker Compose

```yaml
services:
  web:
    image: myapp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    environment:
      POSTGRES_PASSWORD: secret
```

---

## Resource Constraints - CPU

```bash
# Limit CPU usage
docker run -d --cpus=2.0 myapp           # Max 2 cores
docker run -d --cpus=0.5 myapp           # Max 50% of one core
docker run -d --cpu-shares=512 myapp     # Relative weight (default 1024)
docker run -d --cpuset-cpus="0,2" myapp  # Pin to cores 0 and 2
docker run -d --cpuset-cpus="0-3" myapp  # Pin to cores 0 through 3

# CPU period and quota (advanced)
docker run -d \
  --cpu-period=100000 \
  --cpu-quota=50000 \
  myapp
# = 50% of one CPU (quota/period)
```

---

## Resource Constraints - Memory

```bash
# Hard memory limit
docker run -d --memory=512m myapp

# Memory + swap limit
docker run -d --memory=512m --memory-swap=1g myapp
# Swap available: 1g - 512m = 512m

# Disable swap
docker run -d --memory=512m --memory-swap=512m myapp

# Memory reservation (soft limit)
docker run -d --memory=1g --memory-reservation=512m myapp

# OOM score adjustment (-1000 to 1000)
docker run -d --oom-score-adj=-500 myapp  # Less likely to be killed
# Note: --kernel-memory was removed in Docker 20.10+ (cgroups v2)
```

---

## Resource Constraints - Compose

```yaml
services:
  web:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 512M
          pids: 100
        reservations:
          cpus: '0.5'
          memory: 256M
    ulimits:
      nofile:
        soft: 1024
        hard: 2048
      nproc:
        soft: 100
        hard: 200
    sysctls:
      net.core.somaxconn: 1024
      net.ipv4.tcp_syncookies: 0
```

---

## Graceful Shutdown - Signal Handling

```misc
Docker stop sequence:
1. docker stop <container>
2. Docker sends SIGTERM to PID 1
3. Wait for grace period (default 10s)
4. Docker sends SIGKILL if still running
```

```bash
# Customize grace period
docker stop --time=30 myapp

# In Compose
services:
  web:
    image: myapp
    stop_grace_period: 30s
    stop_signal: SIGQUIT  # Custom stop signal

# Common pitfall: shell form ENTRYPOINT doesn't forward signals
# BAD (shell form - PID 1 is /bin/sh, not your app):
ENTRYPOINT node server.js

# GOOD (exec form - your app is PID 1):
ENTRYPOINT ["node", "server.js"]
```

---

## Graceful Shutdown in Application Code

```javascript
// Node.js graceful shutdown
const server = require('./server');

const SHUTDOWN_TIMEOUT = 25000; // 25 seconds

function gracefulShutdown(signal) {
  console.log(`Received ${signal}. Starting graceful shutdown...`);

  // Stop accepting new connections
  server.close(() => {
    console.log('All connections closed.');
    process.exit(0);
  });

  // Force shutdown after timeout
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, SHUTDOWN_TIMEOUT);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

---

## Using `tini` as Init Process

```dockerfile
# tini handles signal forwarding and zombie reaping
FROM node:20-alpine
RUN apk add --no-cache tini

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
```

```bash
# Or use Docker's built-in init
docker run -d --init myapp

# Why tini/init matters:
# 1. PID 1 has special behavior in Linux
# 2. Default signal handling doesn't propagate to children
# 3. Zombie processes are not reaped without init
# 4. tini ensures clean signal forwarding and child reaping
```

---

## Container Restart Policies

```bash
# Never restart (default)
docker run -d --restart=no myapp

# Always restart
docker run -d --restart=always myapp

# Restart unless explicitly stopped
docker run -d --restart=unless-stopped myapp

# Restart on failure (with max retries)
docker run -d --restart=on-failure:5 myapp
```

| Policy            | On crash | On daemon restart | On `docker stop` |
|-------------------|----------|-------------------|-------------------|
| `no`              | No       | No                | No                |
| `always`          | Yes      | Yes               | No (restarts)     |
| `unless-stopped`  | Yes      | No (if stopped)   | No                |
| `on-failure:N`    | Yes (N)  | No                | No                |

---

## Container Update Strategies

```bash
# Blue-green deployment
docker run -d --name web-blue -p 8080:80 myapp:v1
# Deploy new version
docker run -d --name web-green -p 8081:80 myapp:v2
# Test green
curl http://localhost:8081/health
# Switch traffic (update load balancer)
# Remove old version
docker rm -f web-blue

# Rolling update with Compose
docker compose up -d --no-deps --scale web=3 web
# Update one at a time
docker compose up -d --no-deps web
```

---

## Swarm Rolling Updates

```bash
# Create service with update configuration
docker service create --name web \
  --replicas 6 \
  --update-parallelism 2 \
  --update-delay 10s \
  --update-failure-action rollback \
  --update-max-failure-ratio 0.25 \
  --update-order start-first \
  --rollback-parallelism 2 \
  --rollback-delay 5s \
  myapp:v1

# Perform rolling update
docker service update --image myapp:v2 web

# Monitor update progress
docker service ps web
docker service inspect --pretty web

# Manual rollback
docker service rollback web
```

---

## Swarm Update Configuration in Compose

```yaml
services:
  web:
    image: myapp:v2
    deploy:
      replicas: 6
      update_config:
        parallelism: 2
        delay: 10s
        failure_action: rollback
        max_failure_ratio: 0.25
        order: start-first
      rollback_config:
        parallelism: 2
        delay: 5s
        order: stop-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

---

## Production Compose Template

```yaml
# Compose v2+ ignores the top-level version key
services:
  web:
    image: myapp:${VERSION:-latest}
    read_only: true
    tmpfs:
      - /tmp:size=100m
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 512M
        reservations:
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"
    restart: unless-stopped
```

---

## Container Events and Lifecycle

```bash
# Watch container events in real-time
docker events

# Filter events
docker events --filter type=container
docker events --filter event=die
docker events --filter container=web

# Event types: create, start, stop, die, destroy,
# kill, pause, unpause, health_status, oom

# Format output
docker events --format '{{.Time}} {{.Type}} {{.Action}} {{.Actor.Attributes.name}}'

# Since/Until for historical events
docker events --since "2026-03-10T00:00:00" --until "2026-03-10T12:00:00"
```

---

## Automated Cleanup

```bash
# Cron job for Docker cleanup
cat > /etc/cron.daily/docker-cleanup << 'EOF'
#!/bin/bash
# Remove stopped containers older than 24h
docker container prune -f --filter "until=24h"

# Remove unused images older than 48h
docker image prune -a -f --filter "until=48h"

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Log disk usage
docker system df >> /var/log/docker-disk-usage.log
echo "---" >> /var/log/docker-disk-usage.log
EOF
chmod +x /etc/cron.daily/docker-cleanup
```

---

## Watchtower - Automatic Updates

```yaml
# Auto-update containers when new images are available
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=300
      - WATCHTOWER_INCLUDE_STOPPED=false
      - WATCHTOWER_NOTIFICATION_URL=slack://hook.slack.com/...
    command: --schedule "0 0 4 * * *"  # Daily at 4 AM

  web:
    image: myapp:latest
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
```

---

## Docker in Production - Anti-Patterns

![docker_in_production_anti_patterns](svg/courses/devops/advanced-docker/06_production/docker_in_production_anti_patterns.svg)

---

## Production Readiness Checklist

```misc
Image:
  □ Pinned base image version (tag + digest)
  □ Vulnerability scan passing
  □ Non-root user
  □ Minimal base image
  □ No secrets in image

Runtime:
  □ Health check configured
  □ Resource limits set (CPU, memory, PIDs)
  □ Read-only root filesystem
  □ Capabilities dropped
  □ Restart policy configured
  □ Graceful shutdown handling

Operations:
  □ Log rotation configured
  □ Centralized logging
  □ Metrics collection
  □ Alerting rules defined
  □ Backup strategy for volumes
  □ Update/rollback procedure documented
  □ Disaster recovery plan tested
```

---

## Summary - Docker in Production

- Configure log rotation to prevent disk exhaustion
- Use centralized logging (`Fluentd`, `ELK`) for observability
- Monitor with `Prometheus`, `cAdvisor`, and `Grafana`
- Implement health checks at every layer (container, service, app)
- Set resource constraints to prevent noisy neighbor issues
- Handle `SIGTERM` gracefully and use `tini` as init process
- Use rolling updates with automatic rollback on failure
- Automate cleanup of unused images, containers, and volumes
- Follow the production readiness checklist before deploying
