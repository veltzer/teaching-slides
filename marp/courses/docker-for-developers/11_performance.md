# Performance Optimization

---

## Image Size Optimization

![0](../../../out/mermaid/marp/courses/docker-for-developers/11_performance.md/0.png)

---

## Layer Caching Strategy

![1](../../../out/mermaid/marp/courses/docker-for-developers/11_performance.md/1.png)

---

## Resource Limits and Constraints

| Resource | Flag | Purpose | Example |
|----------|------|---------|---------|
| CPU | --cpus | Limit CPU usage | `--cpus=2` |
| Memory | --memory | Set memory limit | `--memory=1g` |
| Swap | --memory-swap | Set swap limit | `--memory-swap=2g` |
| IO | --device-write-bps | Limit disk IO | `--device-write-bps=/dev/sda:1mb` |

---

## Monitoring and Metrics

![2](../../../out/mermaid/marp/courses/docker-for-developers/11_performance.md/2.png)

---

## Build Optimization Techniques

| Technique | Implementation | Benefit |
|-----------|---------------|----------|
| Layer ordering | Most stable first | Better cache usage |
| Multi-stage | Separate build/run | Smaller final image |
| Cache mounting | `--mount=type=cache` | Faster builds |
| Parallel builds | BuildKit | Reduced build time |

---

## Resource Usage Monitoring

![3](../../../out/mermaid/marp/courses/docker-for-developers/11_performance.md/3.png)

---

## Network Performance

| Aspect | Optimization | Impact |
|--------|-------------|---------|
| DNS | Custom resolvers | Faster lookups |
| Network mode | Host networking | Better performance |
| Port binding | Efficient mapping | Reduced overhead |
| Container links | Direct communication | Lower latency |

---

## Storage Optimization

![4](../../../out/mermaid/marp/courses/docker-for-developers/11_performance.md/4.png)

---

## Memory Management

| Strategy | Implementation | Purpose |
|----------|---------------|----------|
| Limit setting | --memory | Prevent OOM |
| Swap control | --memory-swap | Control swap usage |
| OOM priority | --oom-score-adj | Set OOM priority |
| Memory reserve | --memory-reservation | Soft limit |

---

## CPU Optimization

![5](../../../out/mermaid/marp/courses/docker-for-developers/11_performance.md/5.png)

---

## Performance Testing

| Test Type | Tool | Metrics |
|-----------|------|---------|
| Load testing | Apache Bench | Requests/second |
| Resource monitoring | docker stats | CPU/Memory usage |
| Network testing | iperf | Network throughput |
| Disk IO | fio | IO performance |

---

## Container Health Monitoring

![6](../../../out/mermaid/marp/courses/docker-for-developers/11_performance.md/6.png)

---

## Best Practices Summary

| Area | Practice | Benefit |
|------|----------|---------|
| Images | Use multi-stage builds | Smaller images |
| Cache | Optimize layer order | Faster builds |
| Resources | Set appropriate limits | Better stability |
| Monitoring | Regular health checks | Early detection |
