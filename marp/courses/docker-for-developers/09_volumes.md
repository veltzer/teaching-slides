# Docker and Volumes

---

## Why Data Volumes?

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Container without volume: data lost -->
  <rect x="20" y="20" width="120" height="80" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="80" y="45" text-anchor="middle" font-size="11" fill="#333">Container</text>
  <text x="80" y="62" text-anchor="middle" font-size="10" fill="#c62828">Writable Layer</text>
  <text x="80" y="80" text-anchor="middle" font-size="10" fill="#c62828">Lost on remove</text>
  <!-- vs label -->
  <text x="165" y="65" font-size="16" fill="#333" font-weight="bold">vs</text>
  <!-- Container with volume: data persists -->
  <rect x="200" y="20" width="120" height="80" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="260" y="45" text-anchor="middle" font-size="11" fill="#333">Container</text>
  <text x="260" y="62" text-anchor="middle" font-size="10" fill="#1565c0">+ Volume Mount</text>
  <line x1="260" y1="100" x2="260" y2="130" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowVol0)"/>
  <rect x="200" y="130" width="120" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="260" y="152" text-anchor="middle" font-size="10" fill="#2e7d32">Persistent Volume</text>
  <text x="260" y="168" text-anchor="middle" font-size="10" fill="#2e7d32">Data survives</text>
  <!-- Benefits list -->
  <text x="370" y="40" font-size="11" fill="#333" font-weight="bold">Why Volumes?</text>
  <text x="370" y="60" font-size="10" fill="#555">- Persist data across restarts</text>
  <text x="370" y="78" font-size="10" fill="#555">- Share data between containers</text>
  <text x="370" y="96" font-size="10" fill="#555">- Decouple data from container</text>
  <text x="370" y="114" font-size="10" fill="#555">- Backup and migration support</text>
  <defs>
    <marker id="arrowVol0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#1565c0"/>
    </marker>
  </defs>
</svg>

---

## Types of Data Volumes

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Bind Mounts -->
  <rect x="20" y="20" width="160" height="160" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="100" y="42" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="bold">Bind Mounts</text>
  <text x="100" y="62" text-anchor="middle" font-size="10" fill="#555">Host path mapped</text>
  <text x="100" y="78" text-anchor="middle" font-size="10" fill="#555">to container path</text>
  <rect x="35" y="90" width="50" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="60" y="110" text-anchor="middle" font-size="9" fill="#e65100">Host FS</text>
  <line x1="85" y1="105" x2="110" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_08_volumes)"/>
  <rect x="110" y="90" width="55" height="30" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="3"/>
  <text x="137" y="110" text-anchor="middle" font-size="9" fill="#7b1fa2">Container</text>
  <text x="100" y="145" text-anchor="middle" font-size="9" fill="#555">-v /host:/container</text>
  <!-- Named Volumes -->
  <rect x="220" y="20" width="160" height="160" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">Named Volumes</text>
  <text x="300" y="62" text-anchor="middle" font-size="10" fill="#555">Docker-managed</text>
  <text x="300" y="78" text-anchor="middle" font-size="10" fill="#555">storage area</text>
  <rect x="235" y="90" width="55" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="262" y="110" text-anchor="middle" font-size="9" fill="#e65100">Docker</text>
  <line x1="290" y1="105" x2="310" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_08_volumes)"/>
  <rect x="310" y="90" width="55" height="30" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="3"/>
  <text x="337" y="110" text-anchor="middle" font-size="9" fill="#7b1fa2">Container</text>
  <text x="300" y="145" text-anchor="middle" font-size="9" fill="#555">-v name:/path</text>
  <!-- tmpfs Mounts -->
  <rect x="420" y="20" width="160" height="160" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="500" y="42" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">tmpfs Mounts</text>
  <text x="500" y="62" text-anchor="middle" font-size="10" fill="#555">In-memory only</text>
  <text x="500" y="78" text-anchor="middle" font-size="10" fill="#555">No disk persistence</text>
  <rect x="440" y="90" width="50" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="465" y="110" text-anchor="middle" font-size="9" fill="#e65100">RAM</text>
  <line x1="490" y1="105" x2="510" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_08_volumes)"/>
  <rect x="510" y="90" width="55" height="30" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="3"/>
  <text x="537" y="110" text-anchor="middle" font-size="9" fill="#7b1fa2">Container</text>
  <text x="500" y="145" text-anchor="middle" font-size="9" fill="#555">--tmpfs /path</text>
  <defs>
    <marker id="arrowd1_08_volumes" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Volume Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `docker volume create` | Create new volume | `docker volume create mydata` |
| `docker volume ls` | List volumes | `docker volume ls` |
| `docker volume inspect` | Volume details | `docker volume inspect mydata` |
| `docker volume rm` | Remove volume | `docker volume rm mydata` |

---

## Bind Mounts vs Named Volumes

| Feature | Bind Mounts | Named Volumes |
|---------|-------------|---------------|
| Location | Host-specified | Docker-managed |
| Portability | Less portable | More portable |
| Backup | Direct access | Docker commands |
| Performance | Host dependent | Optimized |
| Security | Host exposure | Better isolation |

---

## Working with Volumes

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Container A writes to volume -->
  <rect x="20" y="10" width="110" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="75" y="32" text-anchor="middle" font-size="11" fill="#1565c0">Container A</text>
  <text x="75" y="48" text-anchor="middle" font-size="10" fill="#555">Writer</text>
  <!-- Shared volume -->
  <rect x="200" y="70" width="200" height="60" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="300" y="95" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">Shared Named Volume</text>
  <text x="300" y="115" text-anchor="middle" font-size="10" fill="#555">/var/lib/docker/volumes/mydata</text>
  <!-- Container B reads from volume -->
  <rect x="470" y="10" width="110" height="50" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="525" y="32" text-anchor="middle" font-size="11" fill="#7b1fa2">Container B</text>
  <text x="525" y="48" text-anchor="middle" font-size="10" fill="#555">Reader</text>
  <!-- Arrows -->
  <line x1="75" y1="60" x2="220" y2="70" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_08_volumes)"/>
  <text x="120" y="58" font-size="10" fill="#1565c0">write</text>
  <line x1="525" y1="60" x2="380" y2="70" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowd2_08_volumes)"/>
  <text x="440" y="58" font-size="10" fill="#7b1fa2">read</text>
  <!-- Mount commands -->
  <text x="75" y="170" text-anchor="middle" font-size="9" fill="#555">-v mydata:/app/data</text>
  <text x="525" y="170" text-anchor="middle" font-size="9" fill="#555">-v mydata:/app/data:ro</text>
  <defs>
    <marker id="arrowd2_08_volumes" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Volume Backup Strategies

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Source volume -->
  <rect x="20" y="30" width="120" height="60" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="80" y="55" text-anchor="middle" font-size="11" fill="#1565c0" font-weight="bold">Source Volume</text>
  <text x="80" y="72" text-anchor="middle" font-size="10" fill="#555">mydata</text>
  <!-- Backup container -->
  <rect x="220" y="30" width="140" height="60" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="290" y="52" text-anchor="middle" font-size="11" fill="#e65100" font-weight="bold">Backup Container</text>
  <text x="290" y="70" text-anchor="middle" font-size="10" fill="#555">tar czf backup.tar.gz</text>
  <!-- Backup destination -->
  <rect x="440" y="30" width="130" height="60" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="505" y="55" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">Backup Archive</text>
  <text x="505" y="72" text-anchor="middle" font-size="10" fill="#555">Host / S3 / NFS</text>
  <!-- Arrows -->
  <line x1="140" y1="60" x2="220" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_volumes)"/>
  <text x="175" y="52" text-anchor="middle" font-size="9" fill="#555">mount</text>
  <line x1="360" y1="60" x2="440" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_volumes)"/>
  <text x="398" y="52" text-anchor="middle" font-size="9" fill="#555">export</text>
  <!-- Command example -->
  <rect x="60" y="120" width="480" height="55" fill="#f5f5f5" stroke="#999" stroke-width="1" rx="3"/>
  <text x="80" y="140" font-size="10" fill="#333" font-family="monospace">docker run --rm -v mydata:/source -v $(pwd):/backup</text>
  <text x="80" y="158" font-size="10" fill="#333" font-family="monospace">  alpine tar czf /backup/mydata.tar.gz -C /source .</text>
  <defs>
    <marker id="arrowd3_08_volumes" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Volume Drivers

| Driver | Purpose | Use Case |
|--------|---------|----------|
| local | Local storage | Single-host deployment |
| nfs | Network storage | Multi-host access |
| cifs | Windows shares | Windows integration |
| rexray | Cloud storage | Cloud deployment |

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Central hub -->
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="300" y="97" text-anchor="middle" font-size="11" fill="#1565c0" font-weight="bold">Volume Best</text>
  <text x="300" y="112" text-anchor="middle" font-size="11" fill="#1565c0" font-weight="bold">Practices</text>
  <!-- Named volumes -->
  <rect x="20" y="15" width="110" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="75" y="32" text-anchor="middle" font-size="10" fill="#2e7d32">Use Named</text>
  <text x="75" y="46" text-anchor="middle" font-size="10" fill="#2e7d32">Volumes</text>
  <line x1="130" y1="35" x2="235" y2="85" stroke="#333" stroke-width="1.5"/>
  <!-- Read-only mounts -->
  <rect x="470" y="15" width="110" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="525" y="32" text-anchor="middle" font-size="10" fill="#7b1fa2">Read-Only</text>
  <text x="525" y="46" text-anchor="middle" font-size="10" fill="#7b1fa2">When Possible</text>
  <line x1="470" y1="35" x2="365" y2="85" stroke="#333" stroke-width="1.5"/>
  <!-- Regular backups -->
  <rect x="20" y="145" width="110" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="75" y="162" text-anchor="middle" font-size="10" fill="#e65100">Regular</text>
  <text x="75" y="176" text-anchor="middle" font-size="10" fill="#e65100">Backups</text>
  <line x1="130" y1="165" x2="235" y2="115" stroke="#333" stroke-width="1.5"/>
  <!-- Cleanup unused -->
  <rect x="470" y="145" width="110" height="40" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="525" y="162" text-anchor="middle" font-size="10" fill="#c62828">Prune Unused</text>
  <text x="525" y="176" text-anchor="middle" font-size="10" fill="#c62828">Volumes</text>
  <line x1="470" y1="165" x2="365" y2="115" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Volume Lifecycle

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Create -->
  <rect x="10" y="75" width="80" height="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="50" y="95" text-anchor="middle" font-size="10" fill="#1565c0" font-weight="bold">Create</text>
  <text x="50" y="110" text-anchor="middle" font-size="9" fill="#555">volume create</text>
  <!-- Arrow -->
  <line x1="90" y1="97" x2="120" y2="97" stroke="#333" stroke-width="2" marker-end="url(#arrowLC)"/>
  <!-- Mount -->
  <rect x="120" y="75" width="80" height="45" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="160" y="95" text-anchor="middle" font-size="10" fill="#2e7d32" font-weight="bold">Mount</text>
  <text x="160" y="110" text-anchor="middle" font-size="9" fill="#555">docker run -v</text>
  <!-- Arrow -->
  <line x1="200" y1="97" x2="230" y2="97" stroke="#333" stroke-width="2" marker-end="url(#arrowLC)"/>
  <!-- Use -->
  <rect x="230" y="75" width="80" height="45" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="270" y="95" text-anchor="middle" font-size="10" fill="#e65100" font-weight="bold">In Use</text>
  <text x="270" y="110" text-anchor="middle" font-size="9" fill="#555">read/write</text>
  <!-- Arrow -->
  <line x1="310" y1="97" x2="340" y2="97" stroke="#333" stroke-width="2" marker-end="url(#arrowLC)"/>
  <!-- Unmount -->
  <rect x="340" y="75" width="80" height="45" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="380" y="95" text-anchor="middle" font-size="10" fill="#7b1fa2" font-weight="bold">Unmount</text>
  <text x="380" y="110" text-anchor="middle" font-size="9" fill="#555">container stop</text>
  <!-- Arrow -->
  <line x1="420" y1="97" x2="450" y2="97" stroke="#333" stroke-width="2" marker-end="url(#arrowLC)"/>
  <!-- Remove or Reuse -->
  <rect x="450" y="55" width="80" height="35" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="490" y="72" text-anchor="middle" font-size="10" fill="#c62828" font-weight="bold">Remove</text>
  <text x="490" y="85" text-anchor="middle" font-size="9" fill="#555">volume rm</text>
  <rect x="450" y="105" width="80" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="490" y="122" text-anchor="middle" font-size="10" fill="#2e7d32" font-weight="bold">Reuse</text>
  <text x="490" y="135" text-anchor="middle" font-size="9" fill="#555">re-mount</text>
  <!-- Note: volume persists independently -->
  <text x="300" y="175" text-anchor="middle" font-size="11" fill="#333" font-style="italic">Volumes persist independently of container lifecycle</text>
  <defs>
    <marker id="arrowLC" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Mounting Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `-v name:/path` | Named volume | `-v mydata:/app/data` |
| `-v /host:/container` | Bind mount | `-v /data:/app/data` |
| `--mount type=volume` | Mount flag | `--mount source=mydata,target=/app/data` |

---

## Data Migration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Old volume -->
  <rect x="20" y="25" width="130" height="65" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="85" y="48" text-anchor="middle" font-size="11" fill="#c62828" font-weight="bold">Old Volume</text>
  <text x="85" y="65" text-anchor="middle" font-size="10" fill="#555">Source data</text>
  <text x="85" y="80" text-anchor="middle" font-size="9" fill="#888">v1_data</text>
  <!-- Transfer container -->
  <rect x="220" y="25" width="160" height="65" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="11" fill="#e65100" font-weight="bold">Migration Container</text>
  <text x="300" y="65" text-anchor="middle" font-size="10" fill="#555">cp -a /source/. /dest/</text>
  <text x="300" y="80" text-anchor="middle" font-size="9" fill="#888">mounts both volumes</text>
  <!-- New volume -->
  <rect x="450" y="25" width="130" height="65" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="515" y="48" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">New Volume</text>
  <text x="515" y="65" text-anchor="middle" font-size="10" fill="#555">Migrated data</text>
  <text x="515" y="80" text-anchor="middle" font-size="9" fill="#888">v2_data</text>
  <!-- Arrows -->
  <line x1="150" y1="57" x2="220" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_08_volumes)"/>
  <text x="185" y="50" text-anchor="middle" font-size="9" fill="#555">read</text>
  <line x1="380" y1="57" x2="450" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_08_volumes)"/>
  <text x="415" y="50" text-anchor="middle" font-size="9" fill="#555">write</text>
  <!-- Command -->
  <rect x="40" y="120" width="520" height="55" fill="#f5f5f5" stroke="#999" stroke-width="1" rx="3"/>
  <text x="60" y="140" font-size="10" fill="#333" font-family="monospace">docker run --rm -v v1_data:/source -v v2_data:/dest</text>
  <text x="60" y="158" font-size="10" fill="#333" font-family="monospace">  alpine sh -c "cp -a /source/. /dest/"</text>
  <defs>
    <marker id="arrowd6_08_volumes" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Volume Security

| Consideration | Solution | Implementation |
|---------------|----------|----------------|
| Access Control | File permissions | `chmod`, `chown` |
| Mount options | Read-only mounts | `:ro` flag |
| SELinux | Labels | `z` or `Z` options |
| Isolation | Volume drivers | Network isolation |

---

## Common Volume Patterns

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Pattern 1: Database storage -->
  <rect x="10" y="10" width="175" height="80" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="97" y="30" text-anchor="middle" font-size="11" fill="#1565c0" font-weight="bold">Database Storage</text>
  <text x="97" y="48" text-anchor="middle" font-size="10" fill="#555">postgres_data volume</text>
  <text x="97" y="64" text-anchor="middle" font-size="9" fill="#888">-v pgdata:/var/lib/postgresql</text>
  <text x="97" y="80" text-anchor="middle" font-size="9" fill="#888">Named volume for durability</text>
  <!-- Pattern 2: Config injection -->
  <rect x="210" y="10" width="175" height="80" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="297" y="30" text-anchor="middle" font-size="11" fill="#e65100" font-weight="bold">Config Injection</text>
  <text x="297" y="48" text-anchor="middle" font-size="10" fill="#555">Bind mount config files</text>
  <text x="297" y="64" text-anchor="middle" font-size="9" fill="#888">-v ./nginx.conf:/etc/nginx.conf</text>
  <text x="297" y="80" text-anchor="middle" font-size="9" fill="#888">Host file into container</text>
  <!-- Pattern 3: Shared app data -->
  <rect x="410" y="10" width="175" height="80" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="497" y="30" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">Shared App Data</text>
  <text x="497" y="48" text-anchor="middle" font-size="10" fill="#555">Multi-container sharing</text>
  <text x="497" y="64" text-anchor="middle" font-size="9" fill="#888">App + Sidecar share volume</text>
  <text x="497" y="80" text-anchor="middle" font-size="9" fill="#888">logs, uploads, cache</text>
  <!-- Lower row: diagram showing shared volume pattern -->
  <rect x="120" y="110" width="80" height="35" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5" rx="3"/>
  <text x="160" y="132" text-anchor="middle" font-size="10" fill="#7b1fa2">App</text>
  <rect x="320" y="110" width="80" height="35" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5" rx="3"/>
  <text x="360" y="132" text-anchor="middle" font-size="10" fill="#7b1fa2">Sidecar</text>
  <rect x="200" y="160" width="200" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#2e7d32">Shared Volume: /app/logs</text>
  <line x1="160" y1="145" x2="250" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd7_08_volumes)"/>
  <line x1="360" y1="145" x2="350" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd7_08_volumes)"/>
  <defs>
    <marker id="arrowd7_08_volumes" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Performance Optimization

| Strategy | Implementation | Benefit |
|----------|---------------|---------|
| Mount caching | `:cached` flag | Better read performance |
| Delegation | `:delegated` flag | Better write performance |
| Volume plugins | Storage drivers | Optimized I/O |
| tmpfs | Memory storage | Fastest access |
