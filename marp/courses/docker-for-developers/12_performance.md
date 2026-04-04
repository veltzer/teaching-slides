# Performance Optimization

---

## Image Size Optimization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Image Size Comparison</text>
  <rect x="20" y="30" width="130" height="120" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="85" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">ubuntu:22.04</text>
  <rect x="35" y="58" width="100" height="80" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="85" y="78" text-anchor="middle" font-size="10">~77MB base</text>
  <text x="85" y="95" text-anchor="middle" font-size="10">apt, bash, coreutils</text>
  <text x="85" y="112" text-anchor="middle" font-size="10">+ build tools</text>
  <text x="85" y="129" text-anchor="middle" font-size="10">= ~900MB</text>
  <rect x="170" y="30" width="130" height="120" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="235" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">node:18-slim</text>
  <rect x="185" y="58" width="100" height="60" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="235" y="78" text-anchor="middle" font-size="10">~50MB base</text>
  <text x="235" y="95" text-anchor="middle" font-size="10">node runtime</text>
  <text x="235" y="112" text-anchor="middle" font-size="10">= ~200MB</text>
  <rect x="320" y="30" width="130" height="120" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="385" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">alpine:3.18</text>
  <rect x="335" y="58" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="385" y="78" text-anchor="middle" font-size="10">~5MB base</text>
  <text x="385" y="92" text-anchor="middle" font-size="10">= ~50MB</text>
  <rect x="470" y="30" width="110" height="120" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="525" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">distroless</text>
  <rect x="485" y="58" width="80" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="525" y="78" text-anchor="middle" font-size="10">~2MB</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">Smaller base images reduce attack surface and pull times</text>
</svg>

---

## Layer Caching Strategy

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Dockerfile Layer Order for Caching</text>
  <rect x="20" y="30" width="260" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="150" y="50" text-anchor="middle" font-size="10">FROM node:18-alpine</text>
  <text x="440" y="50" font-size="10" fill="#2e7d32">Cached (rarely changes)</text>
  <rect x="20" y="65" width="260" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="4"/>
  <text x="150" y="85" text-anchor="middle" font-size="10">COPY package*.json ./</text>
  <text x="440" y="85" font-size="10" fill="#2e7d32">Cached (deps stable)</text>
  <rect x="20" y="100" width="260" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="150" y="120" text-anchor="middle" font-size="10">RUN npm install</text>
  <text x="440" y="120" font-size="10" fill="#1565c0">Cached if deps unchanged</text>
  <rect x="20" y="135" width="260" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="4"/>
  <text x="150" y="155" text-anchor="middle" font-size="10">COPY . .</text>
  <text x="440" y="155" font-size="10" fill="#e65100">Invalidated on code change</text>
  <rect x="20" y="170" width="260" height="25" fill="#ffebee" stroke="#c62828" stroke-width="1.5" rx="4"/>
  <text x="150" y="187" text-anchor="middle" font-size="10">RUN npm run build</text>
  <text x="440" y="187" font-size="10" fill="#c62828">Rebuilds every time</text>
  <line x1="310" y1="40" x2="310" y2="185" stroke="#333" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="330" y="30" font-size="10" fill="#555" font-weight="bold">Cache status</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_11_performance" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Monitoring Stack</text>
  <rect x="20" y="35" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="55" text-anchor="middle" font-size="11" font-weight="bold">docker stats</text>
  <text x="80" y="73" text-anchor="middle" font-size="10">CPU / Memory</text>
  <line x1="140" y1="62" x2="170" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_11_performance)"/>
  <rect x="170" y="35" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="55" text-anchor="middle" font-size="11" font-weight="bold">cAdvisor</text>
  <text x="230" y="73" text-anchor="middle" font-size="10">Per-container</text>
  <line x1="290" y1="62" x2="320" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_11_performance)"/>
  <rect x="320" y="35" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="380" y="55" text-anchor="middle" font-size="11" font-weight="bold">Prometheus</text>
  <text x="380" y="73" text-anchor="middle" font-size="10">Time series DB</text>
  <line x1="440" y1="62" x2="470" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_11_performance)"/>
  <rect x="470" y="35" width="110" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="55" text-anchor="middle" font-size="11" font-weight="bold">Grafana</text>
  <text x="525" y="73" text-anchor="middle" font-size="10">Dashboards</text>
  <rect x="80" y="120" width="440" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="142" text-anchor="middle" font-size="10">Metrics: CPU %, Memory usage, Network I/O, Disk I/O, Container restarts</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#555">Set alerts for resource thresholds to detect issues early</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_11_performance" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Cgroup Resource Controls</text>
  <rect x="20" y="30" width="560" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="40" y="50" font-size="11" font-weight="bold">Host Resources</text>
  <rect x="40" y="58" width="120" height="35" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="4"/>
  <text x="100" y="80" text-anchor="middle" font-size="10">CPU: 8 cores</text>
  <rect x="175" y="58" width="120" height="35" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="4"/>
  <text x="235" y="80" text-anchor="middle" font-size="10">Memory: 16GB</text>
  <rect x="310" y="58" width="120" height="35" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="4"/>
  <text x="370" y="80" text-anchor="middle" font-size="10">Disk I/O</text>
  <rect x="445" y="58" width="120" height="35" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="4"/>
  <text x="505" y="80" text-anchor="middle" font-size="10">Network</text>
  <line x1="100" y1="105" x2="100" y2="125" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_11_performance)"/>
  <line x1="300" y1="105" x2="300" y2="125" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_11_performance)"/>
  <line x1="500" y1="105" x2="500" y2="125" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_11_performance)"/>
  <rect x="20" y="125" width="170" height="45" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="105" y="143" text-anchor="middle" font-size="10" font-weight="bold">Container A</text>
  <text x="105" y="160" text-anchor="middle" font-size="10">--cpus=2 --memory=4g</text>
  <rect x="215" y="125" width="170" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="143" text-anchor="middle" font-size="10" font-weight="bold">Container B</text>
  <text x="300" y="160" text-anchor="middle" font-size="10">--cpus=1 --memory=2g</text>
  <rect x="410" y="125" width="170" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="143" text-anchor="middle" font-size="10" font-weight="bold">Container C</text>
  <text x="495" y="160" text-anchor="middle" font-size="10">--cpus=4 --memory=8g</text>
  <text x="300" y="192" text-anchor="middle" font-size="10" fill="#555">Cgroups enforce resource limits per container</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_11_performance" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Storage Driver Performance</text>
  <rect x="20" y="30" width="170" height="70" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="105" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">overlay2</text>
  <text x="105" y="68" text-anchor="middle" font-size="10">Default, best perf</text>
  <text x="105" y="83" text-anchor="middle" font-size="10">Copy-on-write</text>
  <rect x="215" y="30" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">Named Volumes</text>
  <text x="300" y="68" text-anchor="middle" font-size="10">Managed by Docker</text>
  <text x="300" y="83" text-anchor="middle" font-size="10">Best for databases</text>
  <rect x="410" y="30" width="170" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="50" text-anchor="middle" font-size="11" font-weight="bold">Bind Mounts</text>
  <text x="495" y="68" text-anchor="middle" font-size="10">Host path access</text>
  <text x="495" y="83" text-anchor="middle" font-size="10">Dev hot-reload</text>
  <rect x="60" y="120" width="200" height="35" fill="#ffebee" stroke="#c62828" stroke-width="1.5" rx="4"/>
  <text x="160" y="142" text-anchor="middle" font-size="10" fill="#c62828">Avoid writing to container layer</text>
  <rect x="340" y="120" width="200" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="4"/>
  <text x="440" y="142" text-anchor="middle" font-size="10" fill="#2e7d32">Use tmpfs for temp data</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#555">Choose storage strategy based on I/O pattern and persistence needs</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">CPU Constraint Options</text>
  <rect x="20" y="30" width="270" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="48" text-anchor="middle" font-size="11" font-weight="bold">--cpus (Fractional)</text>
  <rect x="35" y="55" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="90" y="72" text-anchor="middle" font-size="10">--cpus=0.5</text>
  <text x="90" y="87" text-anchor="middle" font-size="10">Half a core</text>
  <rect x="160" y="55" width="110" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="215" y="72" text-anchor="middle" font-size="10">--cpus=2.0</text>
  <text x="215" y="87" text-anchor="middle" font-size="10">Two full cores</text>
  <rect x="310" y="30" width="270" height="75" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="48" text-anchor="middle" font-size="11" font-weight="bold">--cpuset-cpus (Pinning)</text>
  <rect x="325" y="55" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="380" y="72" text-anchor="middle" font-size="10">--cpuset-cpus=0,1</text>
  <text x="380" y="87" text-anchor="middle" font-size="10">Pin to cores 0,1</text>
  <rect x="450" y="55" width="110" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="505" y="72" text-anchor="middle" font-size="10">--cpu-shares=512</text>
  <text x="505" y="87" text-anchor="middle" font-size="10">Relative weight</text>
  <rect x="60" y="120" width="480" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="138" text-anchor="middle" font-size="10">--cpus is a hard limit; --cpu-shares only applies under contention</text>
  <text x="300" y="153" text-anchor="middle" font-size="10" fill="#555">Use --cpus for predictable behavior, --cpu-shares for flexible sharing</text>
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#555">Monitor with: docker stats --format "{{.Name}}: {{.CPUPerc}}"</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_11_performance" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">HEALTHCHECK Lifecycle</text>
  <rect x="20" y="35" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="55" text-anchor="middle" font-size="10" font-weight="bold">Starting</text>
  <text x="75" y="72" text-anchor="middle" font-size="10">Grace period</text>
  <line x1="130" y1="60" x2="160" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_11_performance)"/>
  <rect x="160" y="35" width="120" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="220" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">Healthy</text>
  <text x="220" y="72" text-anchor="middle" font-size="10">Check passes</text>
  <line x1="280" y1="60" x2="310" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_11_performance)"/>
  <rect x="310" y="35" width="120" height="50" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="370" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">Unhealthy</text>
  <text x="370" y="72" text-anchor="middle" font-size="10">Retries exceeded</text>
  <line x1="430" y1="60" x2="460" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_11_performance)"/>
  <rect x="460" y="35" width="120" height="50" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="520" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">Restart</text>
  <text x="520" y="72" text-anchor="middle" font-size="10">if restart policy</text>
  <rect x="40" y="105" width="520" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="122" text-anchor="middle" font-size="10">HEALTHCHECK --interval=30s --timeout=3s --retries=3</text>
  <text x="300" y="138" text-anchor="middle" font-size="10">CMD curl -f http://localhost/ || exit 1</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">Health checks enable orchestrators to auto-replace failing containers</text>
</svg>

---

## Best Practices Summary

| Area | Practice | Benefit |
|------|----------|---------|
| Images | Use multi-stage builds | Smaller images |
| Cache | Optimize layer order | Faster builds |
| Resources | Set appropriate limits | Better stability |
| Monitoring | Regular health checks | Early detection |
