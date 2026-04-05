# Security with Docker

---

## Security Context Overview

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="225" y="10" width="150" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="12" font-weight="bold">Docker Security</text>
  <rect x="30" y="80" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="105" text-anchor="middle" font-size="11">Namespaces</text>
  <rect x="170" y="80" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="105" text-anchor="middle" font-size="11">Capabilities</text>
  <rect x="310" y="80" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="370" y="105" text-anchor="middle" font-size="11">Seccomp</text>
  <rect x="450" y="80" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="105" text-anchor="middle" font-size="11">AppArmor</text>
  <rect x="100" y="150" width="160" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="180" y="175" text-anchor="middle" font-size="11">Image Scanning</text>
  <rect x="340" y="150" width="160" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="420" y="175" text-anchor="middle" font-size="11">Rootless Mode</text>
  <line x1="300" y1="50" x2="90" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="50" x2="230" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="50" x2="370" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="50" x2="510" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="180" y1="120" x2="180" y2="150" stroke="#333" stroke-width="1.5"/>
  <line x1="420" y1="120" x2="420" y2="150" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Running as Non-Root

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_09_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="170" height="140" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5" stroke-dasharray="5,3"/>
  <text x="105" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Root (UID 0)</text>
  <rect x="40" y="60" width="130" height="35" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="105" y="82" text-anchor="middle" font-size="10">Full privileges</text>
  <rect x="40" y="105" width="130" height="35" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="105" y="127" text-anchor="middle" font-size="10">Security risk</text>
  <line x1="190" y1="100" x2="230" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_09_security)"/>
  <text x="210" y="90" text-anchor="middle" font-size="10" fill="#333">USER</text>
  <rect x="230" y="30" width="170" height="140" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="315" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Non-Root User</text>
  <rect x="250" y="60" width="130" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="315" y="82" text-anchor="middle" font-size="10">Limited access</text>
  <rect x="250" y="105" width="130" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="315" y="127" text-anchor="middle" font-size="10">Least privilege</text>
  <line x1="400" y1="100" x2="440" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_09_security)"/>
  <rect x="440" y="55" width="140" height="90" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="510" y="80" text-anchor="middle" font-size="10" font-weight="bold">Best Practice</text>
  <text x="510" y="100" text-anchor="middle" font-size="10">RUN useradd -r app</text>
  <text x="510" y="118" text-anchor="middle" font-size="10">USER app</text>
</svg>

---

## User Configuration

| Instruction | Purpose | Example |
|-------------|---------|---------|
| USER | Set container user | `USER appuser` |
| WORKDIR | Set working directory | `WORKDIR /app` |
| COPY --chown | Set file ownership | `COPY --chown=appuser:appgroup` |
| RUN useradd | Create user | `RUN useradd -r appuser` |

---

## Linux Capabilities

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="580" height="180" fill="none" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="30" text-anchor="middle" font-size="12" font-weight="bold">Linux Capabilities Model</text>
  <rect x="30" y="45" width="160" height="65" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="110" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">All Capabilities</text>
  <text x="110" y="82" text-anchor="middle" font-size="10">SYS_ADMIN, NET_RAW</text>
  <text x="110" y="96" text-anchor="middle" font-size="10">CHOWN, SETUID...</text>
  <rect x="220" y="45" width="160" height="65" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="300" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">Default Set</text>
  <text x="300" y="82" text-anchor="middle" font-size="10">CHOWN, SETUID</text>
  <text x="300" y="96" text-anchor="middle" font-size="10">NET_BIND_SERVICE</text>
  <rect x="410" y="45" width="160" height="65" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="490" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Minimal Set</text>
  <text x="490" y="82" text-anchor="middle" font-size="10">--cap-drop ALL</text>
  <text x="490" y="96" text-anchor="middle" font-size="10">--cap-add needed</text>
  <text x="110" y="140" text-anchor="middle" font-size="10" fill="#c62828">--privileged</text>
  <text x="300" y="140" text-anchor="middle" font-size="10" fill="#e65100">docker run</text>
  <text x="490" y="140" text-anchor="middle" font-size="10" fill="#2e7d32">hardened</text>
  <line x1="190" y1="78" x2="220" y2="78" stroke="#333" stroke-width="2"/>
  <line x1="380" y1="78" x2="410" y2="78" stroke="#333" stroke-width="2"/>
  <text x="205" y="72" font-size="13">&gt;</text>
  <text x="395" y="72" font-size="13">&gt;</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">Reduce attack surface by dropping unnecessary capabilities</text>
</svg>

---

## Common Capabilities

| Capability | Purpose | Risk Level |
|------------|---------|------------|
| NET_BIND_SERVICE | Bind to ports < 1024 | Low |
| CHOWN | Change file ownership | Medium |
| SYS_ADMIN | System administration | High |
| NET_ADMIN | Network administration | High |

---

## Tuning Capabilities

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_09_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="15" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="40" text-anchor="middle" font-size="11" font-weight="bold">docker run</text>
  <line x1="150" y1="35" x2="200" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_security)"/>
  <rect x="200" y="10" width="200" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="10">--cap-drop ALL</text>
  <text x="300" y="48" text-anchor="middle" font-size="10">--cap-add NET_BIND_SERVICE</text>
  <line x1="400" y1="35" x2="440" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_security)"/>
  <rect x="440" y="15" width="140" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="510" y="40" text-anchor="middle" font-size="11" fill="#2e7d32">Hardened Container</text>
  <rect x="20" y="80" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="105" text-anchor="middle" font-size="11" font-weight="bold">Dockerfile</text>
  <line x1="150" y1="100" x2="200" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_security)"/>
  <rect x="200" y="75" width="200" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="95" text-anchor="middle" font-size="10">RUN useradd -r appuser</text>
  <text x="300" y="113" text-anchor="middle" font-size="10">USER appuser</text>
  <line x1="400" y1="100" x2="440" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_security)"/>
  <rect x="440" y="80" width="140" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="510" y="105" text-anchor="middle" font-size="11" fill="#2e7d32">Non-Root Container</text>
  <rect x="20" y="145" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="170" text-anchor="middle" font-size="11" font-weight="bold">seccomp</text>
  <line x1="150" y1="165" x2="200" y2="165" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_security)"/>
  <rect x="200" y="140" width="200" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="160" text-anchor="middle" font-size="10">--security-opt</text>
  <text x="300" y="178" text-anchor="middle" font-size="10">seccomp=profile.json</text>
  <line x1="400" y1="165" x2="440" y2="165" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_security)"/>
  <rect x="440" y="145" width="140" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="510" y="170" text-anchor="middle" font-size="11" fill="#2e7d32">Syscall Filtered</text>
</svg>

---

## Security Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="225" y="5" width="150" height="35" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="#c62828">Best Practices</text>
  <rect x="20" y="60" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="85" text-anchor="middle" font-size="10">Minimal Base Image</text>
  <rect x="160" y="60" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="85" text-anchor="middle" font-size="10">Non-Root User</text>
  <rect x="310" y="60" width="130" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="85" text-anchor="middle" font-size="10">Read-Only FS</text>
  <rect x="450" y="60" width="130" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="85" text-anchor="middle" font-size="10">Drop Capabilities</text>
  <rect x="90" y="130" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="155" text-anchor="middle" font-size="10">Scan Images</text>
  <rect x="235" y="130" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="155" text-anchor="middle" font-size="10">No Secrets in Layers</text>
  <rect x="380" y="130" width="130" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="155" text-anchor="middle" font-size="10">Seccomp Profiles</text>
  <line x1="300" y1="40" x2="85" y2="60" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="40" x2="225" y2="60" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="40" x2="375" y2="60" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="40" x2="515" y2="60" stroke="#333" stroke-width="1"/>
</svg>

---

## Secrets Management

| Method | Use Case | Implementation |
|--------|----------|----------------|
| Docker Secrets | Swarm mode | `docker secret create` |
| Environment Files | Development | `.env` files |
| External Stores | Production | Vault, AWS Secrets |
| Mounted Files | Custom solutions | Volume mounts |

---

## Security Scanning

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_09_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="40" width="120" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="60" text-anchor="middle" font-size="11" font-weight="bold">Docker Image</text>
  <text x="80" y="78" text-anchor="middle" font-size="10">myapp:latest</text>
  <line x1="140" y1="65" x2="180" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_09_security)"/>
  <rect x="180" y="30" width="140" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="250" y="52" text-anchor="middle" font-size="11" font-weight="bold">Scanner</text>
  <text x="250" y="70" text-anchor="middle" font-size="10">Trivy / Snyk /</text>
  <text x="250" y="85" text-anchor="middle" font-size="10">docker scout</text>
  <line x1="320" y1="55" x2="370" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_09_security)"/>
  <line x1="320" y1="75" x2="370" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_09_security)"/>
  <rect x="370" y="10" width="210" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="475" y="32" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">Pass: No CVEs</text>
  <text x="475" y="48" text-anchor="middle" font-size="10" fill="#2e7d32">Deploy to production</text>
  <rect x="370" y="75" width="210" height="50" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="475" y="97" text-anchor="middle" font-size="11" fill="#c62828" font-weight="bold">Fail: CVEs Found</text>
  <text x="475" y="113" text-anchor="middle" font-size="10" fill="#c62828">Fix and rebuild image</text>
  <text x="300" y="155" text-anchor="middle" font-size="10" fill="#555">Integrate scanning into CI/CD pipeline for every build</text>
</svg>

---

## Container Isolation

| Feature | Purpose | Implementation |
|---------|---------|----------------|
| Namespaces | Process isolation | Default |
| Cgroups | Resource control | Resource limits |
| Seccomp | System call filtering | Security profiles |
| AppArmor | Access control | Security profiles |

---

## Access Control

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_09_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Docker Access Control Layers</text>
  <rect x="20" y="30" width="560" height="55" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="50" y="52" font-size="11" fill="#c62828" font-weight="bold">Host OS</text>
  <text x="50" y="70" font-size="10">SELinux / AppArmor mandatory access control</text>
  <rect x="40" y="95" width="520" height="50" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="70" y="117" font-size="11" fill="#e65100" font-weight="bold">Docker Daemon</text>
  <text x="260" y="117" font-size="10">TLS auth, socket permissions, authorization plugins</text>
  <rect x="60" y="155" width="150" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="135" y="177" text-anchor="middle" font-size="10">User Namespaces</text>
  <rect x="225" y="155" width="150" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="300" y="177" text-anchor="middle" font-size="10">Seccomp Profiles</text>
  <rect x="390" y="155" width="150" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="465" y="177" text-anchor="middle" font-size="10">Capabilities</text>
  <line x1="135" y1="145" x2="135" y2="155" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="145" x2="300" y2="155" stroke="#333" stroke-width="1.5"/>
  <line x1="465" y1="145" x2="465" y2="155" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Security Auditing

| Area | Check | Tool |
|------|-------|------|
| Configuration | Docker bench | docker-bench-security |
| Vulnerabilities | Image scan | docker scan |
| Runtime | Activity monitor | docker top, stats |
| Access | Audit logs | auditd |

---

## Network Security

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd7_09_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="220" y="5" width="160" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="12" font-weight="bold">Docker Network</text>
  <rect x="20" y="70" width="120" height="55" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="80" y="90" text-anchor="middle" font-size="10" font-weight="bold">Frontend Net</text>
  <text x="80" y="108" text-anchor="middle" font-size="10">web, proxy</text>
  <rect x="240" y="70" width="120" height="55" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="300" y="90" text-anchor="middle" font-size="10" font-weight="bold">Backend Net</text>
  <text x="300" y="108" text-anchor="middle" font-size="10">api, worker</text>
  <rect x="460" y="70" width="120" height="55" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="520" y="90" text-anchor="middle" font-size="10" font-weight="bold">DB Net</text>
  <text x="520" y="108" text-anchor="middle" font-size="10">postgres, redis</text>
  <line x1="140" y1="97" x2="240" y2="97" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_09_security)"/>
  <line x1="360" y1="97" x2="460" y2="97" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_09_security)"/>
  <text x="190" y="90" text-anchor="middle" font-size="9" fill="#555">allowed</text>
  <text x="410" y="90" text-anchor="middle" font-size="9" fill="#555">allowed</text>
  <line x1="140" y1="115" x2="460" y2="115" stroke="#c62828" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="300" y="145" text-anchor="middle" font-size="10" fill="#c62828">Isolated: frontend cannot reach DB directly</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#555">Use custom bridge networks to segment container traffic</text>
</svg>

---

## Filesystem Security

| Strategy | Implementation | Benefit |
|----------|---------------|----------|
| Read-only root | `--read-only` | Prevent modifications |
| Temporary storage | tmpfs | Secure scratch space |
| Volume permissions | chmod/chown | Access control |
| Mount options | :ro flag | Read-only access |
