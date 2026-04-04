# Networking with Docker

---

## Docker Network Types

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Docker</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Networks</text>
  <ellipse cx="100" cy="45" rx="75" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="11">bridge</text>
  <text x="100" y="57" text-anchor="middle" font-size="10" fill="#555">Default, isolated</text>
  <ellipse cx="500" cy="45" rx="75" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="11">host</text>
  <text x="500" y="57" text-anchor="middle" font-size="10" fill="#555">Shares host network</text>
  <ellipse cx="100" cy="165" rx="75" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="11">overlay</text>
  <text x="100" y="177" text-anchor="middle" font-size="10" fill="#555">Multi-host (Swarm)</text>
  <ellipse cx="500" cy="165" rx="75" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="11">none</text>
  <text x="500" y="177" text-anchor="middle" font-size="10" fill="#555">No network access</text>
  <line x1="245" y1="78" x2="165" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="78" x2="435" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="245" y1="122" x2="165" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="122" x2="435" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Opening Ports

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_07_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="160" height="90" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="42" text-anchor="middle" font-size="11" font-weight="bold">Host Machine</text>
  <text x="100" y="62" text-anchor="middle" font-size="10">External port: 8080</text>
  <text x="100" y="82" text-anchor="middle" font-size="10" fill="#555">localhost:8080</text>
  <text x="100" y="100" text-anchor="middle" font-size="10" fill="#555">0.0.0.0:8080</text>
  <line x1="180" y1="65" x2="228" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_07_networking)"/>
  <text x="205" y="55" text-anchor="middle" font-size="10" fill="#666">-p</text>
  <rect x="230" y="20" width="160" height="90" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="310" y="42" text-anchor="middle" font-size="11" font-weight="bold">Docker Proxy</text>
  <text x="310" y="62" text-anchor="middle" font-size="10">Port mapping</text>
  <text x="310" y="82" text-anchor="middle" font-size="10">8080 -> 80</text>
  <text x="310" y="100" text-anchor="middle" font-size="10" fill="#555">iptables rules</text>
  <line x1="390" y1="65" x2="438" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_07_networking)"/>
  <rect x="440" y="20" width="140" height="90" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="42" text-anchor="middle" font-size="11" font-weight="bold">Container</text>
  <text x="510" y="62" text-anchor="middle" font-size="10">Internal port: 80</text>
  <text x="510" y="82" text-anchor="middle" font-size="10" fill="#555">EXPOSE 80</text>
  <text x="510" y="100" text-anchor="middle" font-size="10" fill="#555">in Dockerfile</text>
  <rect x="20" y="130" width="560" height="50" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="150" text-anchor="middle" font-size="10" fill="#555">docker run -p 8080:80 nginx</text>
  <text x="300" y="167" text-anchor="middle" font-size="10" fill="#555">EXPOSE alone does not publish ports - it is documentation only</text>
</svg>

---

## Port Mapping Syntax

| Command | Description | Example |
|---------|-------------|---------|
| `-p hostPort:containerPort` | Specific port mapping | `-p 8080:80` |
| `-p IP:hostPort:containerPort` | Interface specific | `-p 127.0.0.1:8080:80` |
| `-p containerPort` | Random host port | `-p 80` |
| `-P` | All exposed ports | `-P` |

---

## Network Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `docker network create` | Create network | `docker network create mynet` |
| `docker network connect` | Connect container | `docker network connect mynet cont1` |
| `docker network ls` | List networks | `docker network ls` |
| `docker network inspect` | Network details | `docker network inspect bridge` |

---

## Container Communication

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_07_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="10" width="560" height="180" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" fill="#555">User-defined bridge network: my-network</text>
  <rect x="40" y="45" width="130" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="68" text-anchor="middle" font-size="11" font-weight="bold">web-app</text>
  <text x="105" y="85" text-anchor="middle" font-size="10" fill="#555">172.18.0.2</text>
  <text x="105" y="100" text-anchor="middle" font-size="10" fill="#555">port 80</text>
  <line x1="170" y1="77" x2="228" y2="77" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_07_networking)"/>
  <line x1="228" y1="77" x2="170" y2="77" stroke="#666" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="200" y="68" text-anchor="middle" font-size="10" fill="#666">DNS</text>
  <rect x="230" y="45" width="140" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="68" text-anchor="middle" font-size="11" font-weight="bold">api-server</text>
  <text x="300" y="85" text-anchor="middle" font-size="10" fill="#555">172.18.0.3</text>
  <text x="300" y="100" text-anchor="middle" font-size="10" fill="#555">port 3000</text>
  <line x1="370" y1="77" x2="428" y2="77" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_07_networking)"/>
  <text x="400" y="68" text-anchor="middle" font-size="10" fill="#666">DNS</text>
  <rect x="430" y="45" width="140" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="68" text-anchor="middle" font-size="11" font-weight="bold">database</text>
  <text x="500" y="85" text-anchor="middle" font-size="10" fill="#555">172.18.0.4</text>
  <text x="500" y="100" text-anchor="middle" font-size="10" fill="#555">port 5432</text>
  <rect x="150" y="130" width="300" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="150" text-anchor="middle" font-size="10">Containers resolve each other by name</text>
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="#555">e.g., ping api-server from web-app</text>
</svg>

---

## Network Drivers

| Driver | Use Case | Features |
|--------|----------|----------|
| bridge | Default networking | Container isolation |
| host | Performance | Direct host access |
| none | Security | No network access |
| overlay | Multi-host | Swarm networking |
| macvlan | Physical network | Direct network access |

---

## DNS in Docker

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_07_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="45" text-anchor="middle" font-size="11" font-weight="bold">Container A</text>
  <line x1="80" y1="60" x2="80" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="230" y="20" width="140" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="45" text-anchor="middle" font-size="11" font-weight="bold">Docker DNS</text>
  <line x1="300" y1="60" x2="300" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="460" y="20" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="45" text-anchor="middle" font-size="11" font-weight="bold">Container B</text>
  <line x1="520" y1="60" x2="520" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="80" y1="85" x2="298" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_07_networking)"/>
  <text x="190" y="78" text-anchor="middle" font-size="10">resolve "db-server"</text>
  <line x1="300" y1="110" x2="82" y2="110" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrowd3_07_networking)"/>
  <text x="190" y="103" text-anchor="middle" font-size="10">IP: 172.18.0.4</text>
  <line x1="80" y1="140" x2="518" y2="140" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_07_networking)"/>
  <text x="300" y="133" text-anchor="middle" font-size="10">connect to 172.18.0.4:5432</text>
  <line x1="520" y1="170" x2="82" y2="170" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrowd3_07_networking)"/>
  <text x="300" y="163" text-anchor="middle" font-size="10" fill="#4caf50">connection established</text>
</svg>

---

## Network Security

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="270" height="180" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="30" text-anchor="middle" font-size="11" font-weight="bold">Frontend Network</text>
  <rect x="40" y="45" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="90" y="70" text-anchor="middle" font-size="10">web-app</text>
  <rect x="170" y="45" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="220" y="70" text-anchor="middle" font-size="10">api-gateway</text>
  <rect x="310" y="10" width="270" height="180" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="30" text-anchor="middle" font-size="11" font-weight="bold">Backend Network</text>
  <rect x="330" y="45" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="380" y="70" text-anchor="middle" font-size="10">api-server</text>
  <rect x="460" y="45" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="510" y="70" text-anchor="middle" font-size="10">database</text>
  <rect x="40" y="110" width="230" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="155" y="130" text-anchor="middle" font-size="10" fill="#555">web-app cannot reach database</text>
  <text x="155" y="148" text-anchor="middle" font-size="10" fill="#555">directly - network isolation</text>
  <rect x="330" y="110" width="230" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="445" y="130" text-anchor="middle" font-size="10" fill="#555">api-server bridges both</text>
  <text x="445" y="148" text-anchor="middle" font-size="10" fill="#555">networks as needed</text>
</svg>

---

## Network Troubleshooting

| Issue | Command | Purpose |
|-------|---------|---------|
| Connectivity | `docker exec cont1 ping cont2` | Test connection |
| Port Mapping | `docker port container` | Check port mappings |
| Network Config | `docker network inspect` | View network details |
| DNS Resolution | `docker exec cont1 nslookup cont2` | Test DNS |

---

## Custom Networks

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_07_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="160" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="52" text-anchor="middle" font-size="11" font-weight="bold">network create</text>
  <text x="100" y="70" text-anchor="middle" font-size="10">--driver bridge</text>
  <text x="100" y="85" text-anchor="middle" font-size="10" fill="#555">--subnet 172.20.0.0/16</text>
  <line x1="180" y1="62" x2="218" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_07_networking)"/>
  <rect x="220" y="30" width="160" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">network connect</text>
  <text x="300" y="70" text-anchor="middle" font-size="10">Attach containers</text>
  <text x="300" y="85" text-anchor="middle" font-size="10" fill="#555">to custom network</text>
  <line x1="380" y1="62" x2="418" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_07_networking)"/>
  <rect x="420" y="30" width="160" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="52" text-anchor="middle" font-size="11" font-weight="bold">Communicate</text>
  <text x="500" y="70" text-anchor="middle" font-size="10">Built-in DNS</text>
  <text x="500" y="85" text-anchor="middle" font-size="10" fill="#555">Name resolution</text>
  <rect x="20" y="120" width="560" height="60" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="140" text-anchor="middle" font-size="10" fill="#555">docker network create --driver bridge --subnet 172.20.0.0/16 my-net</text>
  <text x="300" y="157" text-anchor="middle" font-size="10" fill="#555">docker run --network my-net --name app1 myimage</text>
  <text x="300" y="172" text-anchor="middle" font-size="10" fill="#555">Containers on same custom network can resolve each other by name</text>
</svg>

---

## Network Creation Options

| Option | Purpose | Example |
|--------|---------|---------|
| `--driver` | Set network driver | `--driver bridge` |
| `--subnet` | Define subnet | `--subnet 172.18.0.0/16` |
| `--gateway` | Set gateway | `--gateway 172.18.0.1` |
| `--ip-range` | Set IP range | `--ip-range 172.18.0.0/24` |

---

## Network Management

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_07_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="45" text-anchor="middle" font-size="11" font-weight="bold">Admin</text>
  <line x1="80" y1="60" x2="80" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="240" y="20" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="45" text-anchor="middle" font-size="11" font-weight="bold">Docker Host</text>
  <line x1="300" y1="60" x2="300" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="460" y="20" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="45" text-anchor="middle" font-size="11" font-weight="bold">Network</text>
  <line x1="520" y1="60" x2="520" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="80" y1="85" x2="298" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd6_07_networking)"/>
  <text x="190" y="78" text-anchor="middle" font-size="10">docker network ls</text>
  <line x1="300" y1="105" x2="82" y2="105" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrowd6_07_networking)"/>
  <text x="190" y="98" text-anchor="middle" font-size="10">bridge, host, custom-net</text>
  <line x1="80" y1="130" x2="298" y2="130" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd6_07_networking)"/>
  <text x="190" y="123" text-anchor="middle" font-size="10">docker network prune</text>
  <line x1="300" y1="150" x2="518" y2="150" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd6_07_networking)"/>
  <text x="410" y="143" text-anchor="middle" font-size="10">remove unused networks</text>
  <line x1="520" y1="170" x2="302" y2="170" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrowd6_07_networking)"/>
  <text x="410" y="163" text-anchor="middle" font-size="10" fill="#4caf50">cleaned up</text>
</svg>

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Network</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Best Practices</text>
  <ellipse cx="100" cy="45" rx="75" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="11">Custom Networks</text>
  <text x="100" y="57" text-anchor="middle" font-size="10" fill="#555">Not default bridge</text>
  <ellipse cx="500" cy="45" rx="75" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="11">Least Privilege</text>
  <text x="500" y="57" text-anchor="middle" font-size="10" fill="#555">Minimal port expose</text>
  <ellipse cx="100" cy="165" rx="75" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="11">Isolation</text>
  <text x="100" y="177" text-anchor="middle" font-size="10" fill="#555">Separate networks</text>
  <ellipse cx="500" cy="165" rx="75" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="11">Use DNS Names</text>
  <text x="500" y="177" text-anchor="middle" font-size="10" fill="#555">Not IP addresses</text>
  <line x1="245" y1="78" x2="165" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="78" x2="435" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="245" y1="122" x2="165" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="122" x2="435" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Common Network Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Frontend-Backend | Separated networks | Web applications |
| Load Balancer | Port distribution | Scaled services |
| Service Discovery | Automatic discovery | Microservices |
| Network Isolation | Security separation | Multi-tenant apps |
