# Troubleshooting and Debugging

---

## Common Issues and Solutions

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Common Docker Issues</text>
  <rect x="20" y="30" width="130" height="55" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="85" y="50" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">Build Failures</text>
  <text x="85" y="68" text-anchor="middle" font-size="10">Missing deps</text>
  <text x="85" y="80" text-anchor="middle" font-size="9">Wrong base image</text>
  <rect x="160" y="30" width="130" height="55" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="225" y="50" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">Runtime Errors</text>
  <text x="225" y="68" text-anchor="middle" font-size="10">OOM killed</text>
  <text x="225" y="80" text-anchor="middle" font-size="9">Permission denied</text>
  <rect x="300" y="30" width="140" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="370" y="50" text-anchor="middle" font-size="10" font-weight="bold">Networking</text>
  <text x="370" y="68" text-anchor="middle" font-size="10">Port conflicts</text>
  <text x="370" y="80" text-anchor="middle" font-size="9">DNS resolution</text>
  <rect x="450" y="30" width="130" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="50" text-anchor="middle" font-size="10" font-weight="bold">Storage</text>
  <text x="515" y="68" text-anchor="middle" font-size="10">Disk full</text>
  <text x="515" y="80" text-anchor="middle" font-size="9">Volume mount errors</text>
  <rect x="80" y="105" width="440" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="300" y="122" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Debugging Toolkit</text>
  <text x="300" y="138" text-anchor="middle" font-size="10">docker logs | docker exec | docker inspect | docker stats</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#555">Always check logs first, then inspect container state</text>
</svg>

---

## Docker Inspect Deep Dive

| Section | Information | Usage |
|---------|-------------|-------|
| Config | Container configuration | Check environment, cmd |
| State | Current state | Health, status, pid |
| NetworkSettings | Network configuration | IP, ports, networks |
| Mounts | Volume information | Storage configuration |

---

## Remote Debugging Techniques

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_12_trouble_shooting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Remote Debugging with Docker</text>
  <rect x="20" y="35" width="140" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="55" text-anchor="middle" font-size="10" font-weight="bold">IDE Debugger</text>
  <text x="90" y="73" text-anchor="middle" font-size="10">localhost:9229</text>
  <text x="90" y="86" text-anchor="middle" font-size="9">Breakpoints set</text>
  <line x1="160" y1="65" x2="200" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_12_trouble_shooting)"/>
  <rect x="200" y="35" width="200" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="10" font-weight="bold">Docker Container</text>
  <text x="300" y="73" text-anchor="middle" font-size="10">-p 9229:9229</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">node --inspect=0.0.0.0:9229</text>
  <line x1="400" y1="65" x2="440" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_12_trouble_shooting)"/>
  <rect x="440" y="35" width="140" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="55" text-anchor="middle" font-size="10" font-weight="bold">Application</text>
  <text x="510" y="73" text-anchor="middle" font-size="10">Debug mode</text>
  <text x="510" y="86" text-anchor="middle" font-size="9">Pauses on break</text>
  <rect x="40" y="115" width="520" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="137" text-anchor="middle" font-size="10">Also: docker exec -it container bash for interactive shell access</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">Expose debug ports in development only, never in production</text>
</svg>

---

## Health Checks Implementation

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_12_trouble_shooting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Health Check Flow</text>
  <rect x="20" y="30" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="48" text-anchor="middle" font-size="10" font-weight="bold">Docker Daemon</text>
  <text x="85" y="62" text-anchor="middle" font-size="9">Runs HEALTHCHECK</text>
  <line x1="150" y1="50" x2="190" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_12_trouble_shooting)"/>
  <text x="170" y="42" font-size="9">interval</text>
  <rect x="190" y="30" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="255" y="48" text-anchor="middle" font-size="10" font-weight="bold">Health Probe</text>
  <text x="255" y="62" text-anchor="middle" font-size="9">curl / wget / CMD</text>
  <line x1="320" y1="40" x2="380" y2="40" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_12_trouble_shooting)"/>
  <text x="350" y="34" font-size="9">exit 0</text>
  <rect x="380" y="25" width="100" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="430" y="45" text-anchor="middle" font-size="10" fill="#2e7d32" font-weight="bold">Healthy</text>
  <line x1="320" y1="60" x2="380" y2="60" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd2_12_trouble_shooting)"/>
  <text x="350" y="73" font-size="9" fill="#c62828">exit 1</text>
  <rect x="380" y="50" width="100" height="30" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="430" y="70" text-anchor="middle" font-size="10" fill="#c62828" font-weight="bold">Unhealthy</text>
  <line x1="480" y1="65" x2="520" y2="65" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd2_12_trouble_shooting)"/>
  <rect x="520" y="50" width="70" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="555" y="70" text-anchor="middle" font-size="9">Restart?</text>
  <rect x="40" y="100" width="520" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="117" text-anchor="middle" font-size="10" font-weight="bold">Dockerfile HEALTHCHECK</text>
  <text x="300" y="135" text-anchor="middle" font-size="10">HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost/ || exit 1</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#555">docker inspect --format='{{.State.Health.Status}}' container</text>
</svg>

---

## Debug Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `docker logs` | View output | `docker logs -f container` |
| `docker exec` | Run commands | `docker exec -it container bash` |
| `docker inspect` | Check config | `docker inspect container` |
| `docker stats` | Monitor resources | `docker stats container` |

---

## Diagnostic Process

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_12_trouble_shooting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Diagnostic Flowchart</text>
  <rect x="20" y="30" width="110" height="40" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="75" y="48" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">Problem</text>
  <text x="75" y="62" text-anchor="middle" font-size="9">Container fails</text>
  <line x1="130" y1="50" x2="155" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_12_trouble_shooting)"/>
  <rect x="155" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="48" text-anchor="middle" font-size="10" font-weight="bold">docker logs</text>
  <text x="205" y="62" text-anchor="middle" font-size="9">Check output</text>
  <line x1="255" y1="50" x2="280" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_12_trouble_shooting)"/>
  <rect x="280" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="330" y="48" text-anchor="middle" font-size="10" font-weight="bold">docker inspect</text>
  <text x="330" y="62" text-anchor="middle" font-size="9">Check config</text>
  <line x1="380" y1="50" x2="405" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_12_trouble_shooting)"/>
  <rect x="405" y="30" width="80" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="48" text-anchor="middle" font-size="10" font-weight="bold">docker exec</text>
  <text x="445" y="62" text-anchor="middle" font-size="9">Shell in</text>
  <line x1="485" y1="50" x2="505" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_12_trouble_shooting)"/>
  <rect x="505" y="30" width="80" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="545" y="48" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">Fix</text>
  <text x="545" y="62" text-anchor="middle" font-size="9">Apply solution</text>
  <rect x="40" y="90" width="520" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="108" text-anchor="middle" font-size="10" font-weight="bold">Key questions at each step:</text>
  <text x="300" y="125" text-anchor="middle" font-size="10">Exit code? | Environment correct? | Ports open? | Volumes mounted? | Permissions?</text>
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="#555">If container exits immediately: docker run -it --entrypoint sh image</text>
</svg>

---

## Common Error Messages

| Error | Possible Cause | Solution |
|-------|---------------|----------|
| Cannot connect to daemon | Docker not running | Start Docker service |
| Port already allocated | Port conflict | Change port mapping |
| OOM Killed | Out of memory | Increase memory limit |
| Image pull failed | Network/auth issue | Check credentials/network |

---

## Resource Monitoring

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_12_trouble_shooting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Resource Monitoring Commands</text>
  <rect x="20" y="30" width="170" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="50" text-anchor="middle" font-size="10" font-weight="bold">docker stats</text>
  <text x="105" y="66" text-anchor="middle" font-size="10">CPU% | MEM | NET I/O</text>
  <text x="105" y="82" text-anchor="middle" font-size="10">Real-time dashboard</text>
  <rect x="215" y="30" width="170" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="10" font-weight="bold">docker top</text>
  <text x="300" y="66" text-anchor="middle" font-size="10">PID | USER | CMD</text>
  <text x="300" y="82" text-anchor="middle" font-size="10">Process listing</text>
  <rect x="410" y="30" width="170" height="65" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="50" text-anchor="middle" font-size="10" font-weight="bold">docker system df</text>
  <text x="495" y="66" text-anchor="middle" font-size="10">Images | Containers</text>
  <text x="495" y="82" text-anchor="middle" font-size="10">Disk usage</text>
  <rect x="60" y="110" width="230" height="40" fill="#ffebee" stroke="#c62828" stroke-width="1.5" rx="5"/>
  <text x="175" y="128" text-anchor="middle" font-size="10" fill="#c62828" font-weight="bold">Warning Signs</text>
  <text x="175" y="143" text-anchor="middle" font-size="10" fill="#c62828">CPU >80% | MEM >90%</text>
  <rect x="310" y="110" width="230" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="5"/>
  <text x="425" y="128" text-anchor="middle" font-size="10" fill="#2e7d32" font-weight="bold">Action</text>
  <text x="425" y="143" text-anchor="middle" font-size="10" fill="#2e7d32">Scale up or set limits</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"</text>
</svg>

---

## Network Debugging

| Tool | Purpose | Example |
|------|---------|---------|
| ping | Connectivity | `docker exec container ping host` |
| netstat | Port status | `docker exec container netstat -tulpn` |
| curl | HTTP testing | `docker exec container curl service` |
| dig | DNS lookup | `docker exec container dig domain` |

---

## Log Analysis

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_12_trouble_shooting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Log Collection Pipeline</text>
  <rect x="20" y="35" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="55" text-anchor="middle" font-size="10" font-weight="bold">Container</text>
  <text x="80" y="73" text-anchor="middle" font-size="10">stdout/stderr</text>
  <line x1="140" y1="62" x2="170" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_12_trouble_shooting)"/>
  <rect x="170" y="35" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="55" text-anchor="middle" font-size="10" font-weight="bold">Log Driver</text>
  <text x="230" y="73" text-anchor="middle" font-size="10">json-file, syslog</text>
  <line x1="290" y1="62" x2="320" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_12_trouble_shooting)"/>
  <rect x="320" y="35" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="380" y="55" text-anchor="middle" font-size="10" font-weight="bold">Aggregator</text>
  <text x="380" y="73" text-anchor="middle" font-size="10">Fluentd / ELK</text>
  <line x1="440" y1="62" x2="470" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_12_trouble_shooting)"/>
  <rect x="470" y="35" width="110" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="55" text-anchor="middle" font-size="10" font-weight="bold">Search</text>
  <text x="525" y="73" text-anchor="middle" font-size="10">Kibana, Grafana</text>
  <rect x="40" y="110" width="520" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="128" text-anchor="middle" font-size="10" font-weight="bold">Quick commands:</text>
  <text x="300" y="142" text-anchor="middle" font-size="10">docker logs -f --tail 100 --since 1h container_name</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">Always log to stdout/stderr -- let Docker handle log routing</text>
</svg>

---

## Performance Investigation

| Area | Check | Tool |
|------|-------|------|
| CPU | Usage patterns | top, stats |
| Memory | Memory consumption | stats, inspect |
| IO | Disk activity | iotop |
| Network | Traffic patterns | nethogs |

---

## Debug Mode Options

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Debug Mode Options</text>
  <rect x="20" y="30" width="270" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="48" text-anchor="middle" font-size="11" font-weight="bold">Runtime Debug Flags</text>
  <rect x="35" y="55" width="115" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="92" y="72" text-anchor="middle" font-size="10">--entrypoint sh</text>
  <text x="92" y="86" text-anchor="middle" font-size="9">Override CMD</text>
  <rect x="160" y="55" width="115" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="217" y="72" text-anchor="middle" font-size="10">-e DEBUG=1</text>
  <text x="217" y="86" text-anchor="middle" font-size="9">Verbose logging</text>
  <rect x="310" y="30" width="270" height="75" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="48" text-anchor="middle" font-size="11" font-weight="bold">Docker Daemon Debug</text>
  <rect x="325" y="55" width="115" height="40" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="382" y="72" text-anchor="middle" font-size="10">dockerd --debug</text>
  <text x="382" y="86" text-anchor="middle" font-size="9">Daemon logs</text>
  <rect x="450" y="55" width="115" height="40" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="507" y="72" text-anchor="middle" font-size="10">DOCKER_CLI_DEBUG</text>
  <text x="507" y="86" text-anchor="middle" font-size="9">CLI verbose</text>
  <rect x="20" y="120" width="560" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="5"/>
  <text x="300" y="138" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">Tip: docker run --rm -it --entrypoint sh myimage -- start a shell in any image</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#555">Use docker events to watch real-time container lifecycle events</text>
</svg>

---

## Container Recovery

| State | Action | Command |
|-------|--------|---------|
| Stopped | Start | `docker start container` |
| Unresponsive | Restart | `docker restart container` |
| Broken | Remove/Recreate | `docker rm; docker run` |
| Stuck | Force remove | `docker rm -f container` |

---

## Best Debugging Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Debugging Best Practices</text>
  <rect x="20" y="30" width="175" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="107" y="48" text-anchor="middle" font-size="10" font-weight="bold">1. Reproduce</text>
  <text x="107" y="65" text-anchor="middle" font-size="10">Same image tag</text>
  <text x="107" y="80" text-anchor="middle" font-size="10">Same env vars</text>
  <rect x="213" y="30" width="175" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="10" font-weight="bold">2. Isolate</text>
  <text x="300" y="65" text-anchor="middle" font-size="10">Minimal compose</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">One service at a time</text>
  <rect x="405" y="30" width="175" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="492" y="48" text-anchor="middle" font-size="10" font-weight="bold">3. Verify Fix</text>
  <text x="492" y="65" text-anchor="middle" font-size="10">Clean rebuild</text>
  <text x="492" y="80" text-anchor="middle" font-size="10">Test in CI</text>
  <rect x="20" y="110" width="270" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="155" y="128" text-anchor="middle" font-size="10" font-weight="bold">Do: version pin, health checks, logs</text>
  <text x="155" y="143" text-anchor="middle" font-size="10">Structured JSON logging</text>
  <rect x="310" y="110" width="270" height="40" fill="#ffebee" stroke="#c62828" stroke-width="1.5" rx="5"/>
  <text x="445" y="128" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">Avoid: latest tag, no limits, silent fails</text>
  <text x="445" y="143" text-anchor="middle" font-size="10" fill="#c62828">Ignoring exit codes</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#555">docker inspect -f '{{.State.ExitCode}}' container -- always check exit codes</text>
</svg>
