# Cluster Management with YARN

---
## YARN Architecture

## Overview
- Yet Another Resource Negotiator (YARN)
- Second generation Hadoop compute platform
- Separates resource management from processing model
- Enables multiple applications to share cluster resources

---
## Core Components
<svg viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
  <!-- Client -->
  <rect x="50" y="50" width="120" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="110" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Client</text>

  <!-- Resource Manager -->
  <rect x="350" y="50" width="180" height="70" rx="5" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="2"/>
  <text x="440" y="75" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Resource Manager</text>
  <text x="440" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-style="italic">(Master)</text>

  <!-- Application Master -->
  <rect x="620" y="50" width="180" height="60" rx="5" fill="#d1f2eb" stroke="#55a3a0" stroke-width="2"/>
  <text x="710" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Application Master</text>

  <!-- Node Managers -->
  <rect x="100" y="250" width="150" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="175" y="285" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Node Manager 1</text>

  <rect x="350" y="250" width="150" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="425" y="285" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Node Manager 2</text>

  <rect x="600" y="250" width="150" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="675" y="285" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Node Manager n</text>

  <!-- Containers -->
  <rect x="80" y="380" width="90" height="50" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="1.5"/>
  <text x="125" y="408" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Container 1</text>

  <rect x="180" y="380" width="90" height="50" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="1.5"/>
  <text x="225" y="408" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Container 2</text>

  <rect x="330" y="380" width="90" height="50" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="1.5"/>
  <text x="375" y="408" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Container 3</text>

  <rect x="430" y="380" width="90" height="50" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="1.5"/>
  <text x="475" y="408" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Container 4</text>

  <rect x="580" y="380" width="90" height="50" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="1.5"/>
  <text x="625" y="408" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Container 5</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow10" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Client to Resource Manager -->
  <line x1="170" y1="80" x2="350" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>

  <!-- Resource Manager to Node Managers -->
  <line x1="380" y1="120" x2="175" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>
  <line x1="440" y1="120" x2="425" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>
  <line x1="500" y1="120" x2="675" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>

  <!-- Resource Manager to Application Master -->
  <line x1="530" y1="80" x2="620" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>

  <!-- Node Managers to Containers -->
  <line x1="145" y1="310" x2="125" y2="380" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>
  <line x1="205" y1="310" x2="225" y2="380" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>
  <line x1="395" y1="310" x2="375" y2="380" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>
  <line x1="455" y1="310" x2="475" y2="380" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>
  <line x1="645" y1="310" x2="625" y2="380" stroke="#666" stroke-width="2" marker-end="url(#arrow10)"/>

  <!-- Application Master to Containers (dashed lines for coordination) -->
  <line x1="650" y1="110" x2="125" y2="380" stroke="#999" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrow10)"/>
  <line x1="680" y1="110" x2="225" y2="380" stroke="#999" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrow10)"/>
  <line x1="710" y1="110" x2="375" y2="380" stroke="#999" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrow10)"/>
  <line x1="740" y1="110" x2="475" y2="380" stroke="#999" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrow10)"/>
  <line x1="770" y1="110" x2="625" y2="380" stroke="#999" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrow10)"/>
</svg>

---
## Key Components Explained
1. Resource Manager (RM)
    - Global resource scheduler
    - Manages application lifecycle
    - Arbitrates cluster resources
    - Single point of management

1. Node Manager (NM)
    - One per node in cluster
    - Manages containers and resources
    - Reports node health
    - Monitors resource usage

1. Application Master (AM)
    - One per application
    - Negotiates resources with RM
    - Works with NM to execute tasks
    - Monitors application progress

1. Container
    - Resource allocation unit
    - CPU, memory, disk, network
    - Execution environment for tasks
    - Managed by Node Manager

---
## YARN Deployment Modes

## Client Mode
<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Driver -->
  <rect x="50" y="120" width="100" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Driver</text>

  <!-- Client -->
  <rect x="210" y="120" width="100" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="260" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Client</text>

  <!-- Resource Manager -->
  <rect x="370" y="120" width="150" height="60" rx="5" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
  <text x="445" y="145" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Resource</text>
  <text x="445" y="165" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Manager</text>

  <!-- Node Manager -->
  <rect x="580" y="120" width="120" height="60" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="640" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Node Manager</text>

  <!-- Executor -->
  <rect x="760" y="120" width="100" height="60" rx="5" fill="#f8d7da" stroke="#dc3545" stroke-width="2"/>
  <text x="810" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Executor</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow11" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Flow -->
  <line x1="150" y1="150" x2="210" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow11)"/>
  <line x1="310" y1="150" x2="370" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow11)"/>
  <line x1="520" y1="150" x2="580" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow11)"/>
  <line x1="700" y1="150" x2="760" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrow11)"/>
</svg>

Characteristics:
- Driver runs on client machine
- Better for interactive applications
- Client must stay alive
- Good for development and debugging

---
## Cluster Mode
<svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Client -->
  <rect x="50" y="170" width="100" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Client</text>

  <!-- Resource Manager -->
  <rect x="220" y="170" width="150" height="60" rx="5" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
  <text x="295" y="195" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Resource</text>
  <text x="295" y="215" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Manager</text>

  <!-- Application Master -->
  <rect x="440" y="100" width="160" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="520" y="135" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Application Master</text>

  <!-- Driver (inside AM) -->
  <rect x="440" y="240" width="160" height="60" rx="5" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="2"/>
  <text x="520" y="275" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Driver</text>

  <!-- Node Manager -->
  <rect x="670" y="170" width="120" height="60" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="730" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Node Manager</text>

  <!-- Executor -->
  <rect x="860" y="170" width="100" height="60" rx="5" fill="#f8d7da" stroke="#dc3545" stroke-width="2"/>
  <text x="910" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Executor</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow12" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Client to Resource Manager -->
  <line x1="150" y1="200" x2="220" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arrow12)"/>

  <!-- Resource Manager to Application Master -->
  <line x1="370" y1="180" x2="440" y2="140" stroke="#666" stroke-width="2" marker-end="url(#arrow12)"/>

  <!-- Application Master to Driver -->
  <line x1="520" y1="160" x2="520" y2="240" stroke="#666" stroke-width="2" marker-end="url(#arrow12)"/>

  <!-- Application Master to Node Manager -->
  <line x1="600" y1="130" x2="670" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow12)"/>

  <!-- Node Manager to Executor -->
  <line x1="790" y1="200" x2="860" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arrow12)"/>
</svg>

Characteristics:
- Driver runs on cluster
- Better for production
- Client can disconnect
- More reliable and scalable

---
## Configuration Examples

```yaml
# Client Mode
spark-submit \
  --master yarn \
  --deploy-mode client \
  --executor-memory 20G \
  --num-executors 50 \
  application.py

# Cluster Mode
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --executor-memory 20G \
  --num-executors 50 \
  application.py
```

---
## Configuration and Tuning

## Resource Allocation

```yaml
# YARN Configuration
yarn.nodemanager.resource.memory-mb: 40960
yarn.nodemanager.resource.cpu-vcores: 32

# Spark Configuration
spark.executor.instances: 50
spark.executor.memory: 20g
spark.executor.cores: 4
spark.driver.memory: 10g
```

---
## Memory Settings

```python
# Memory fraction settings
spark.conf.set("spark.memory.fraction", 0.8)
spark.conf.set("spark.memory.storageFraction", 0.3)

# Overflow settings
spark.conf.set("spark.yarn.executor.memoryOverhead", "4g")
```

---
## CPU Settings

```yaml
# CPU allocation
yarn.nodemanager.resource.cpu-vcores: 32
spark.executor.cores: 4
spark.task.cpus: 1
```

---
## Dynamic Allocation

```yaml
# Enable dynamic allocation
spark.dynamicAllocation.enabled: true
spark.shuffle.service.enabled: true
spark.dynamicAllocation.minExecutors: 5
spark.dynamicAllocation.maxExecutors: 100
spark.dynamicAllocation.schedulerBacklogTimeout: 1s
```

---
## Monitoring and Debugging

## YARN Web UI
- Resource Manager UI (port 8088)
    - Cluster overview
    - Application status
    - Resource usage
    - Node health
- Node Manager UI (port 8042)
    - Container information
    - Node metrics
    - Log access
---
## Logging Configuration

```yaml
# YARN logging
yarn.log-aggregation-enable: true
yarn.nodemanager.log-dirs: /var/log/hadoop-yarn/containers
yarn.nodemanager.remote-app-log-dir: /tmp/logs

# Spark logging
spark.eventLog.enabled: true
spark.eventLog.dir: hdfs://namenode:8021/spark-logs
```

---
## Metrics Collection

```python
# Configure metrics
spark.conf.set("spark.metrics.conf.*.sink.graphite.class",
               "org.apache.spark.metrics.sink.GraphiteSink")
spark.conf.set("spark.metrics.conf.*.sink.graphite.host", "graphite")
spark.conf.set("spark.metrics.conf.*.sink.graphite.port", "2003")
```

---
## Common Issues and Solutions

## Resource Issues
1. Container Launch Failure

```yaml
# Increase memory overhead
spark.yarn.executor.memoryOverhead: 4096
```

1. Node Manager Issues

```bash
# Check Node Manager logs
yarn logs -applicationId application_1234567890_0001
```

---
## Performance Issues
1. Data Skew

```python
# Repartition data
df = df.repartition(200)
```

1. Memory Pressure

```yaml
# Adjust memory settings
spark.memory.fraction: 0.8
spark.memory.storageFraction: 0.3
```

---
## Debugging Tools

## Log Analysis

```bash
# Aggregate logs
yarn logs -applicationId <app_id> > application_logs.txt

# Search for errors
grep "ERROR" application_logs.txt
```

## Metrics Visualization
![3](../../../out/mermaid/marp/courses/apache-spark-with-python/05_yarn.md/3.png)

---
## Best Practices

## Resource Planning
1. Calculate Resources

```python
# Example calculation
num_executors = total_cores / cores_per_executor
executor_memory = (node_memory * 0.9) / executors_per_node
```

1. Set Limits

```yaml
spark.executor.memory: 20g
spark.executor.memoryOverhead: 4g
spark.executor.cores: 4
```

---
## Production Deployment

```yaml
# Security settings
spark.authenticate: true
spark.network.crypto.enabled: true

# High availability
yarn.resourcemanager.ha.enabled: true
yarn.resourcemanager.cluster-id: cluster1
```

---
## Monitoring Strategy
1. Set up alerts
1. Monitor key metrics
    - Resource utilization
    - Application progress
    - Error rates
    - Latency

---
## Summary
- YARN provides robust cluster management
- Multiple deployment modes for different uses
- Extensive configuration options
- Comprehensive monitoring tools
