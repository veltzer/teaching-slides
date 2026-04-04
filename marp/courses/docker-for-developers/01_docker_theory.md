# Docker Theory

---

## Container Evolution Timeline

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="60" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="85" text-anchor="middle" font-size="10">chroot (1979)</text>
  <rect x="130" y="60" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="180" y="85" text-anchor="middle" font-size="10">Jails (2000)</text>
  <rect x="250" y="60" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="85" text-anchor="middle" font-size="10">cgroups (2006)</text>
  <rect x="370" y="60" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="420" y="85" text-anchor="middle" font-size="10">LXC (2008)</text>
  <rect x="490" y="60" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="85" text-anchor="middle" font-size="10">Docker (2013)</text>
  <line x1="110" y1="80" x2="130" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="230" y1="80" x2="250" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="80" x2="370" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="80" x2="490" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="10" y1="120" x2="590" y2="120" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="300" y="140" text-anchor="middle" font-size="11" fill="#555">Evolution of Container Technology</text>
</svg>

---

## What is Docker?

- Container technology platform for application development
- Industry standard for containerization
- Ensures consistent environments across all stages
- Based on Linux container technology
- Open-source with enterprise features

---

## Docker Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="20" width="120" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="42" text-anchor="middle" font-size="11" font-weight="bold">Docker CLI</text>
  <text x="110" y="58" text-anchor="middle" font-size="10">docker build/run</text>
  <rect x="240" y="20" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="11" font-weight="bold">Docker Daemon</text>
  <text x="300" y="58" text-anchor="middle" font-size="10">dockerd (API)</text>
  <rect x="430" y="20" width="120" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="42" text-anchor="middle" font-size="11" font-weight="bold">Registry</text>
  <text x="490" y="58" text-anchor="middle" font-size="10">Docker Hub</text>
  <rect x="140" y="110" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="190" y="135" text-anchor="middle" font-size="10">Images</text>
  <rect x="260" y="110" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="310" y="135" text-anchor="middle" font-size="10">Containers</text>
  <rect x="380" y="110" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="430" y="135" text-anchor="middle" font-size="10">Networks</text>
  <line x1="170" y1="45" x2="240" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_00)"/>
  <line x1="360" y1="45" x2="430" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_00)"/>
  <line x1="300" y1="70" x2="300" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_00)"/>
  <defs><marker id="arrowd1_00" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Container vs VM Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="145" y="15" text-anchor="middle" font-size="12" font-weight="bold">Virtual Machines</text>
  <text x="455" y="15" text-anchor="middle" font-size="12" font-weight="bold">Containers</text>
  <rect x="20" y="150" width="250" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="145" y="172" text-anchor="middle" font-size="10">Infrastructure</text>
  <rect x="20" y="115" width="250" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="3"/>
  <text x="145" y="137" text-anchor="middle" font-size="10">Hypervisor</text>
  <rect x="20" y="25" width="80" height="88" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="60" y="55" text-anchor="middle" font-size="9">Guest OS</text>
  <text x="60" y="70" text-anchor="middle" font-size="9">App 1</text>
  <rect x="105" y="25" width="80" height="88" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="145" y="55" text-anchor="middle" font-size="9">Guest OS</text>
  <text x="145" y="70" text-anchor="middle" font-size="9">App 2</text>
  <rect x="190" y="25" width="80" height="88" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="230" y="55" text-anchor="middle" font-size="9">Guest OS</text>
  <text x="230" y="70" text-anchor="middle" font-size="9">App 3</text>
  <rect x="330" y="150" width="250" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="455" y="172" text-anchor="middle" font-size="10">Infrastructure</text>
  <rect x="330" y="115" width="250" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="455" y="137" text-anchor="middle" font-size="10">Host OS + Docker Engine</text>
  <rect x="330" y="25" width="80" height="88" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="370" y="55" text-anchor="middle" font-size="9">Bins/Libs</text>
  <text x="370" y="70" text-anchor="middle" font-size="9">App 1</text>
  <rect x="415" y="25" width="80" height="88" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="455" y="55" text-anchor="middle" font-size="9">Bins/Libs</text>
  <text x="455" y="70" text-anchor="middle" font-size="9">App 2</text>
  <rect x="500" y="25" width="80" height="88" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="540" y="55" text-anchor="middle" font-size="9">Bins/Libs</text>
  <text x="540" y="70" text-anchor="middle" font-size="9">App 3</text>
</svg>

---

## Common Docker Commands

| Category | Command | Purpose |
|----------|---------|----------|
| Images | `docker build` | Build an image |
| | `docker pull` | Download image |
| | `docker push` | Upload image |
| Containers | `docker run` | Start container |
| | `docker stop` | Stop container |
| | `docker rm` | Remove container |
| System | `docker info` | Show system info |
| | `docker version` | Show version |

---

## Docker Workflow

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="70" y="95" text-anchor="middle" font-size="11" font-weight="bold">Dockerfile</text>
  <text x="70" y="112" text-anchor="middle" font-size="10">Write</text>
  <rect x="160" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="210" y="95" text-anchor="middle" font-size="11" font-weight="bold">Build</text>
  <text x="210" y="112" text-anchor="middle" font-size="10">docker build</text>
  <rect x="300" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="350" y="95" text-anchor="middle" font-size="11" font-weight="bold">Image</text>
  <text x="350" y="112" text-anchor="middle" font-size="10">docker push</text>
  <rect x="440" y="75" width="120" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="95" text-anchor="middle" font-size="11" font-weight="bold">Container</text>
  <text x="500" y="112" text-anchor="middle" font-size="10">docker run</text>
  <line x1="120" y1="100" x2="160" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00)"/>
  <line x1="260" y1="100" x2="300" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00)"/>
  <line x1="400" y1="100" x2="440" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00)"/>
  <defs><marker id="arrowd3_00" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Docker Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="97" text-anchor="middle" font-size="11" fill="white">Docker</text>
  <text x="300" y="112" text-anchor="middle" font-size="11" fill="white">Engine</text>
  <ellipse cx="120" cy="45" rx="55" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="50" text-anchor="middle" font-size="10">Images</text>
  <ellipse cx="480" cy="45" rx="55" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="50" text-anchor="middle" font-size="10">Containers</text>
  <ellipse cx="120" cy="160" rx="55" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="165" text-anchor="middle" font-size="10">Networks</text>
  <ellipse cx="480" cy="160" rx="55" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="165" text-anchor="middle" font-size="10">Volumes</text>
  <line x1="245" y1="78" x2="170" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="78" x2="430" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="122" x2="170" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="122" x2="430" y2="145" stroke="#333" stroke-width="2"/>
</svg>

---

## Resource Management

| Resource | Description | Command |
|----------|-------------|---------|
| CPU | Limit CPU usage | `--cpus`, `--cpu-shares` |
| Memory | Set memory limits | `--memory`, `--memory-swap` |
| Storage | Manage disk space | `--storage-opt` |
| Network | Network settings | `--network`, `--port` |

---

## Container Lifecycle

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="80" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="50" y="105" text-anchor="middle" font-size="10">Created</text>
  <rect x="130" y="80" width="80" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="170" y="105" text-anchor="middle" font-size="10">Running</text>
  <rect x="250" y="80" width="80" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="290" y="105" text-anchor="middle" font-size="10">Paused</text>
  <rect x="370" y="80" width="80" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="105" text-anchor="middle" font-size="10">Stopped</text>
  <rect x="490" y="80" width="80" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="530" y="105" text-anchor="middle" font-size="10">Removed</text>
  <line x1="90" y1="100" x2="130" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrlc01)"/>
  <line x1="210" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrlc01)"/>
  <line x1="330" y1="100" x2="370" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrlc01)"/>
  <line x1="450" y1="100" x2="490" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrlc01)"/>
  <path d="M 290 80 Q 290 50 170 50 Q 170 50 170 80" fill="none" stroke="#333" stroke-width="1.5" marker-end="url(#arrlc01)"/>
  <text x="230" y="45" text-anchor="middle" font-size="9" fill="#555">unpause</text>
  <path d="M 410 80 Q 410 40 170 40 Q 170 40 170 80" fill="none" stroke="#333" stroke-width="1.5" marker-end="url(#arrlc01)"/>
  <text x="290" y="32" text-anchor="middle" font-size="9" fill="#555">restart</text>
  <defs><marker id="arrlc01" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Network Types

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="70" width="110" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="92" text-anchor="middle" font-size="11" font-weight="bold">Bridge</text>
  <text x="85" y="110" text-anchor="middle" font-size="9">Default, isolated</text>
  <rect x="170" y="70" width="110" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="92" text-anchor="middle" font-size="11" font-weight="bold">Host</text>
  <text x="225" y="110" text-anchor="middle" font-size="9">No isolation</text>
  <rect x="310" y="70" width="110" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="365" y="92" text-anchor="middle" font-size="11" font-weight="bold">Overlay</text>
  <text x="365" y="110" text-anchor="middle" font-size="9">Multi-host</text>
  <rect x="450" y="70" width="110" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="92" text-anchor="middle" font-size="11" font-weight="bold">None</text>
  <text x="505" y="110" text-anchor="middle" font-size="9">No network</text>
  <rect x="30" y="150" width="530" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="170" text-anchor="middle" font-size="10">Host Network Stack</text>
</svg>

---

## Security Model

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="97" text-anchor="middle" font-size="11" fill="white">Docker</text>
  <text x="300" y="112" text-anchor="middle" font-size="11" fill="white">Security</text>
  <ellipse cx="120" cy="45" rx="60" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="50" text-anchor="middle" font-size="10">Namespaces</text>
  <ellipse cx="480" cy="45" rx="60" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="50" text-anchor="middle" font-size="10">Capabilities</text>
  <ellipse cx="120" cy="160" rx="60" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="165" text-anchor="middle" font-size="10">Seccomp</text>
  <ellipse cx="480" cy="160" rx="60" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="165" text-anchor="middle" font-size="10">AppArmor</text>
  <line x1="245" y1="78" x2="175" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="78" x2="425" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="122" x2="175" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="122" x2="425" y2="145" stroke="#333" stroke-width="2"/>
</svg>

---

## Development Best Practices

| Area | Practice | Benefit |
|------|----------|---------|
| Images | Use official base images | Security, reliability |
| Layers | Minimize layers | Smaller images |
| Cache | Optimize build cache | Faster builds |
| Security | Non-root user | Better security |
| Configuration | Use environment variables | Flexibility |

---

## Troubleshooting Flow

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="75" width="100" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="70" y="95" text-anchor="middle" font-size="10" font-weight="bold">Identify</text>
  <text x="70" y="112" text-anchor="middle" font-size="9">docker logs</text>
  <rect x="155" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="95" text-anchor="middle" font-size="10" font-weight="bold">Inspect</text>
  <text x="205" y="112" text-anchor="middle" font-size="9">docker inspect</text>
  <rect x="290" y="75" width="100" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="340" y="95" text-anchor="middle" font-size="10" font-weight="bold">Debug</text>
  <text x="340" y="112" text-anchor="middle" font-size="9">docker exec</text>
  <rect x="425" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="95" text-anchor="middle" font-size="10" font-weight="bold">Fix</text>
  <text x="475" y="112" text-anchor="middle" font-size="9">Rebuild/Restart</text>
  <line x1="120" y1="100" x2="155" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrtf01)"/>
  <line x1="255" y1="100" x2="290" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrtf01)"/>
  <line x1="390" y1="100" x2="425" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrtf01)"/>
  <defs><marker id="arrtf01" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>
