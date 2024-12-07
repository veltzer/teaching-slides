# Cluster Management with YARN

---
## YARN Architecture

### Overview
- Yet Another Resource Negotiator (YARN)
- Second generation Hadoop compute platform
- Separates resource management from processing model
- Enables multiple applications to share cluster resources

---
### Core Components
![0](../../../out/mermaid/marp/courses/apache-spark-with-python/05_yarn.md/0.png)

---
### Key Components Explained
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

### Client Mode
![1](../../../out/mermaid/marp/courses/apache-spark-with-python/05_yarn.md/1.png)

Characteristics:
- Driver runs on client machine
- Better for interactive applications
- Client must stay alive
- Good for development and debugging

---
### Cluster Mode
![2](../../../out/mermaid/marp/courses/apache-spark-with-python/05_yarn.md/2.png)

Characteristics:
- Driver runs on cluster
- Better for production
- Client can disconnect
- More reliable and scalable

---
### Configuration Examples
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

### Resource Allocation
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
### Memory Settings
```python
# Memory fraction settings
spark.conf.set("spark.memory.fraction", 0.8)
spark.conf.set("spark.memory.storageFraction", 0.3)

# Overflow settings
spark.conf.set("spark.yarn.executor.memoryOverhead", "4g")
```

---
### CPU Settings
```yaml
# CPU allocation
yarn.nodemanager.resource.cpu-vcores: 32
spark.executor.cores: 4
spark.task.cpus: 1
```

---
### Dynamic Allocation
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

### YARN Web UI
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
### Logging Configuration
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
### Metrics Collection
```python
# Configure metrics
spark.conf.set("spark.metrics.conf.*.sink.graphite.class",
               "org.apache.spark.metrics.sink.GraphiteSink")
spark.conf.set("spark.metrics.conf.*.sink.graphite.host", "graphite")
spark.conf.set("spark.metrics.conf.*.sink.graphite.port", "2003")
```

---
### Common Issues and Solutions

#### Resource Issues
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
#### Performance Issues
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
### Debugging Tools

#### Log Analysis
```bash
# Aggregate logs
yarn logs -applicationId <app_id> > application_logs.txt

# Search for errors
grep "ERROR" application_logs.txt
```

#### Metrics Visualization
![3](../../../out/mermaid/marp/courses/apache-spark-with-python/05_yarn.md/3.png)

---
## Best Practices

### Resource Planning
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
### Production Deployment
```yaml
# Security settings
spark.authenticate: true
spark.network.crypto.enabled: true

# High availability
yarn.resourcemanager.ha.enabled: true
yarn.resourcemanager.cluster-id: cluster1
```

---
### Monitoring Strategy
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
