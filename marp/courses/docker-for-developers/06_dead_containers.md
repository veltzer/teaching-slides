# Dead Containers

---

## Container Lifecycle States

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_lifecycle" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="80" width="90" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="65" y="105" text-anchor="middle" font-size="11">Created</text>
  <rect x="140" y="80" width="90" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="185" y="105" text-anchor="middle" font-size="11">Running</text>
  <rect x="260" y="80" width="90" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="305" y="105" text-anchor="middle" font-size="11">Paused</text>
  <rect x="380" y="80" width="90" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="425" y="105" text-anchor="middle" font-size="11">Stopped</text>
  <rect x="500" y="80" width="90" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="545" y="105" text-anchor="middle" font-size="11">Dead</text>
  <line x1="110" y1="100" x2="138" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_lifecycle)"/>
  <line x1="230" y1="100" x2="258" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_lifecycle)"/>
  <line x1="350" y1="100" x2="378" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_lifecycle)"/>
  <line x1="470" y1="100" x2="498" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_lifecycle)"/>
  <path d="M 305 120 Q 305 155 185 155 Q 140 155 140 120" stroke="#333" stroke-width="1.5" fill="none" marker-end="url(#arrow_lifecycle)"/>
  <text x="225" y="168" text-anchor="middle" font-size="10" fill="#666">unpause</text>
  <path d="M 425 120 Q 425 45 185 45 Q 140 45 140 78" stroke="#2e7d32" stroke-width="1.5" fill="none" marker-end="url(#arrow_lifecycle)"/>
  <text x="300" y="38" text-anchor="middle" font-size="10" fill="#2e7d32">docker start (restart)</text>
</svg>

---

## How to See Dead Containers

| Command | Purpose | Example |
|---------|---------|---------|
| `docker ps -a` | List all containers | Shows running and stopped |
| `docker ps -f status=exited` | Filter by status | Shows only exited containers |
| `docker ps -q -f status=dead` | List dead container IDs | For scripting use |
| `docker inspect` | Detailed container info | Full configuration and state |

---

## Container Exit Codes

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Exit</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Codes</text>
  <ellipse cx="100" cy="45" rx="75" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="11">Code 0</text>
  <text x="100" y="57" text-anchor="middle" font-size="10" fill="#555">Normal exit</text>
  <ellipse cx="500" cy="45" rx="75" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="11">Code 1</text>
  <text x="500" y="57" text-anchor="middle" font-size="10" fill="#555">App error</text>
  <ellipse cx="100" cy="165" rx="75" ry="28" fill="#ffebee" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="11">Code 137</text>
  <text x="100" y="177" text-anchor="middle" font-size="10" fill="#555">OOM killed (SIGKILL)</text>
  <ellipse cx="500" cy="165" rx="75" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="11">Code 143</text>
  <text x="500" y="177" text-anchor="middle" font-size="10" fill="#555">SIGTERM received</text>
  <line x1="245" y1="78" x2="165" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="78" x2="435" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="245" y1="122" x2="165" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="122" x2="435" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Viewing Container Logs

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_05_dead_containers" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="50" width="140" height="70" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="75" text-anchor="middle" font-size="11" font-weight="bold">Dead Container</text>
  <text x="90" y="95" text-anchor="middle" font-size="10" fill="#555">Exited / Failed</text>
  <line x1="160" y1="85" x2="218" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_dead_containers)"/>
  <text x="190" y="77" text-anchor="middle" font-size="10" fill="#666">inspect</text>
  <rect x="220" y="40" width="160" height="90" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="62" text-anchor="middle" font-size="11" font-weight="bold">docker logs</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">docker logs &lt;id&gt;</text>
  <text x="300" y="95" text-anchor="middle" font-size="10">--tail 100</text>
  <text x="300" y="110" text-anchor="middle" font-size="10">--since 1h</text>
  <line x1="380" y1="85" x2="428" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_dead_containers)"/>
  <text x="404" y="77" text-anchor="middle" font-size="10" fill="#666">analyze</text>
  <rect x="430" y="50" width="150" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="75" text-anchor="middle" font-size="11" font-weight="bold">Root Cause</text>
  <text x="505" y="95" text-anchor="middle" font-size="10" fill="#555">Error messages</text>
  <text x="505" y="110" text-anchor="middle" font-size="10" fill="#555">Stack traces</text>
  <rect x="20" y="150" width="560" height="35" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="172" text-anchor="middle" font-size="10" fill="#555">Logs persist even after container stops - always check logs first</text>
</svg>

---

## Log Access Commands

| Command | Purpose | Options |
|---------|---------|---------|
| `docker logs <container>` | View logs | Basic log output |
| `docker logs -f <container>` | Follow logs | Real-time monitoring |
| `docker logs --tail 100` | Last N lines | Limited history |
| `docker logs --since 1h` | Time-based | Recent logs |

---

## Reviving Dead Containers

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_05_dead_containers" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="120" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="45" text-anchor="middle" font-size="11" font-weight="bold">Stopped</text>
  <line x1="80" y1="60" x2="80" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="240" y="20" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="45" text-anchor="middle" font-size="11" font-weight="bold">Docker CLI</text>
  <line x1="300" y1="60" x2="300" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="460" y="20" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="45" text-anchor="middle" font-size="11" font-weight="bold">Running</text>
  <line x1="520" y1="60" x2="520" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="80" y1="85" x2="298" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_05_dead_containers)"/>
  <text x="190" y="78" text-anchor="middle" font-size="10">docker start &lt;id&gt;</text>
  <line x1="300" y1="110" x2="518" y2="110" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_05_dead_containers)"/>
  <text x="410" y="103" text-anchor="middle" font-size="10">restart process</text>
  <line x1="520" y1="140" x2="302" y2="140" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrowd3_05_dead_containers)"/>
  <text x="410" y="133" text-anchor="middle" font-size="10">container running</text>
  <line x1="300" y1="165" x2="82" y2="165" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrowd3_05_dead_containers)"/>
  <text x="190" y="158" text-anchor="middle" font-size="10" fill="#4caf50">revived successfully</text>
</svg>

---

## Container Restart Policies

| Policy | Description | Use Case |
|--------|-------------|----------|
| no | Never restart | Short-lived tasks |
| on-failure | Restart on error | Background services |
| unless-stopped | Always restart except manual stop | Persistent services |
| always | Always restart | Critical services |

---

## Debugging Dead Containers

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_05_dead_containers" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="40" width="140" height="70" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="65" text-anchor="middle" font-size="11" font-weight="bold">Crashed</text>
  <text x="90" y="82" text-anchor="middle" font-size="10">Container</text>
  <text x="90" y="97" text-anchor="middle" font-size="10" fill="#555">exit code != 0</text>
  <line x1="160" y1="75" x2="218" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_05_dead_containers)"/>
  <rect x="220" y="30" width="160" height="90" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">Debug Steps</text>
  <text x="300" y="70" text-anchor="middle" font-size="10">1. docker logs &lt;id&gt;</text>
  <text x="300" y="85" text-anchor="middle" font-size="10">2. docker inspect &lt;id&gt;</text>
  <text x="300" y="100" text-anchor="middle" font-size="10">3. docker cp &lt;id&gt;:/path .</text>
  <text x="300" y="115" text-anchor="middle" font-size="10" fill="#555">Extract files for analysis</text>
  <line x1="380" y1="75" x2="438" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_05_dead_containers)"/>
  <rect x="440" y="40" width="140" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="65" text-anchor="middle" font-size="11" font-weight="bold">Fix + Restart</text>
  <text x="510" y="82" text-anchor="middle" font-size="10">Update image</text>
  <text x="510" y="97" text-anchor="middle" font-size="10" fill="#555">docker start &lt;id&gt;</text>
  <rect x="20" y="150" width="560" height="35" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="172" text-anchor="middle" font-size="10" fill="#555">Tip: use docker commit to save container state before removal</text>
</svg>

---

## Resource Monitoring

| Command | Information | Use |
|---------|-------------|-----|
| `docker stats` | Resource usage | Real-time monitoring |
| `docker events` | Container events | Event tracking |
| `docker top` | Running processes | Process inspection |
| `docker inspect` | Configuration | Detailed inspection |

---

## Recovery Strategies

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Recovery</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Strategies</text>
  <ellipse cx="100" cy="45" rx="75" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="11">Restart Policy</text>
  <text x="100" y="57" text-anchor="middle" font-size="10" fill="#555">--restart=on-failure</text>
  <ellipse cx="500" cy="45" rx="75" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="11">Health Checks</text>
  <text x="500" y="57" text-anchor="middle" font-size="10" fill="#555">HEALTHCHECK CMD</text>
  <ellipse cx="100" cy="165" rx="75" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="11">Orchestration</text>
  <text x="100" y="177" text-anchor="middle" font-size="10" fill="#555">Compose / Swarm</text>
  <ellipse cx="500" cy="165" rx="75" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="11">Monitoring</text>
  <text x="500" y="177" text-anchor="middle" font-size="10" fill="#555">Alerts + Auto-heal</text>
  <line x1="245" y1="78" x2="165" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="78" x2="435" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="245" y1="122" x2="165" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="122" x2="435" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Common Death Causes

| Cause | Symptoms | Solution |
|-------|----------|----------|
| OOM Kill | Exit 137 | Increase memory limit |
| Application Crash | Non-zero exit | Fix application code |
| Dependency Failure | Connection errors | Check dependencies |
| Permission Issues | Access denied | Fix permissions |

---

## Container Cleanup

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_05_dead_containers" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="40" width="140" height="60" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="62" text-anchor="middle" font-size="11" font-weight="bold">Dead Containers</text>
  <text x="90" y="80" text-anchor="middle" font-size="10" fill="#555">docker ps -a -f</text>
  <text x="90" y="93" text-anchor="middle" font-size="10" fill="#555">status=exited</text>
  <line x1="160" y1="70" x2="218" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_05_dead_containers)"/>
  <rect x="220" y="40" width="160" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="62" text-anchor="middle" font-size="11" font-weight="bold">Selective Remove</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">docker rm &lt;id&gt;</text>
  <text x="300" y="93" text-anchor="middle" font-size="10" fill="#555">one at a time</text>
  <line x1="380" y1="70" x2="438" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_05_dead_containers)"/>
  <rect x="440" y="40" width="140" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="62" text-anchor="middle" font-size="11" font-weight="bold">Bulk Cleanup</text>
  <text x="510" y="80" text-anchor="middle" font-size="10">docker container</text>
  <text x="510" y="93" text-anchor="middle" font-size="10">prune</text>
  <rect x="20" y="130" width="560" height="50" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="150" text-anchor="middle" font-size="10" fill="#555">docker system prune: removes all stopped containers, unused networks,</text>
  <text x="300" y="167" text-anchor="middle" font-size="10" fill="#555">dangling images, and build cache. Use -a to also remove unused images.</text>
</svg>

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Best</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Practices</text>
  <ellipse cx="100" cy="45" rx="75" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="11">--rm flag</text>
  <text x="100" y="57" text-anchor="middle" font-size="10" fill="#555">Auto-remove on exit</text>
  <ellipse cx="500" cy="45" rx="75" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="11">Resource Limits</text>
  <text x="500" y="57" text-anchor="middle" font-size="10" fill="#555">--memory, --cpus</text>
  <ellipse cx="100" cy="165" rx="75" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="11">Regular Prune</text>
  <text x="100" y="177" text-anchor="middle" font-size="10" fill="#555">Scheduled cleanup</text>
  <ellipse cx="500" cy="165" rx="75" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="11">Restart Policies</text>
  <text x="500" y="177" text-anchor="middle" font-size="10" fill="#555">Auto-recovery</text>
  <line x1="245" y1="78" x2="165" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="78" x2="435" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="245" y1="122" x2="165" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="122" x2="435" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>
