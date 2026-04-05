# Docker Under the Hood
---

## Virtual Machine Basics

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="150" width="500" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="172" text-anchor="middle" font-size="11">Physical Hardware (CPU, RAM, Disk, NIC)</text>
  <rect x="50" y="115" width="500" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="137" text-anchor="middle" font-size="11">Hypervisor (Type 1 or Type 2)</text>
  <rect x="60" y="20" width="140" height="90" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="42" text-anchor="middle" font-size="10" font-weight="bold">VM 1</text>
  <text x="130" y="58" text-anchor="middle" font-size="9">Guest OS</text>
  <text x="130" y="73" text-anchor="middle" font-size="9">Bins/Libs</text>
  <text x="130" y="88" text-anchor="middle" font-size="9">Application</text>
  <rect x="230" y="20" width="140" height="90" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="10" font-weight="bold">VM 2</text>
  <text x="300" y="58" text-anchor="middle" font-size="9">Guest OS</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Bins/Libs</text>
  <text x="300" y="88" text-anchor="middle" font-size="9">Application</text>
  <rect x="400" y="20" width="140" height="90" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="42" text-anchor="middle" font-size="10" font-weight="bold">VM 3</text>
  <text x="470" y="58" text-anchor="middle" font-size="9">Guest OS</text>
  <text x="470" y="73" text-anchor="middle" font-size="9">Bins/Libs</text>
  <text x="470" y="88" text-anchor="middle" font-size="9">Application</text>
</svg>

---

## How Virtual Machines Work

| Component | Role | Resource Impact |
|-----------|------|----------------|
| Guest OS | Complete OS copy | 5-20GB storage |
| Hypervisor | Resource management | 10-20% overhead |
| Virtual Hardware | Hardware emulation | Memory overhead |
| Host OS | Base system | Shared resource |

---

## VM Resource Allocation

- Full hardware virtualization
- Fixed memory allocation
- Dedicated virtual CPU cores
- Complete OS overhead
- Slow boot time (minutes)
- Full system isolation

---

## Containers vs VMs

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="30" width="100" height="140" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="55" text-anchor="middle" font-size="10" font-weight="bold">VM</text>
  <text x="80" y="75" text-anchor="middle" font-size="9">Full OS</text>
  <text x="80" y="90" text-anchor="middle" font-size="9">GBs size</text>
  <text x="80" y="105" text-anchor="middle" font-size="9">Minutes boot</text>
  <text x="80" y="120" text-anchor="middle" font-size="9">Heavy</text>
  <text x="80" y="135" text-anchor="middle" font-size="9">isolation</text>
  <rect x="170" y="20" width="40" height="160" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="190" y="105" text-anchor="middle" font-size="11" font-weight="bold" transform="rotate(-90,190,105)">vs</text>
  <rect x="250" y="30" width="100" height="140" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="10" font-weight="bold">Container</text>
  <text x="300" y="75" text-anchor="middle" font-size="9">Shared OS</text>
  <text x="300" y="90" text-anchor="middle" font-size="9">MBs size</text>
  <text x="300" y="105" text-anchor="middle" font-size="9">Seconds boot</text>
  <text x="300" y="120" text-anchor="middle" font-size="9">Process</text>
  <text x="300" y="135" text-anchor="middle" font-size="9">isolation</text>
  <rect x="400" y="50" width="170" height="110" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="485" y="75" text-anchor="middle" font-size="10" font-weight="bold">Key Difference</text>
  <text x="485" y="95" text-anchor="middle" font-size="9">Containers share the</text>
  <text x="485" y="110" text-anchor="middle" font-size="9">host kernel; VMs run</text>
  <text x="485" y="125" text-anchor="middle" font-size="9">their own kernel</text>
</svg>

---

## Container Advantages

| Feature | Containers | Virtual Machines |
|---------|------------|------------------|
| Startup Time | Seconds | Minutes |
| Size | MBs | GBs |
| Resource Usage | Low overhead | High overhead |
| Isolation | Process-level | Full system |
| Portability | Very high | Limited |

---

## Docker Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="130" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="45" text-anchor="middle" font-size="11" font-weight="bold">Docker CLI</text>
  <text x="85" y="62" text-anchor="middle" font-size="9">REST API calls</text>
  <rect x="200" y="20" width="180" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="290" y="45" text-anchor="middle" font-size="11" font-weight="bold">Docker Daemon</text>
  <text x="290" y="62" text-anchor="middle" font-size="9">dockerd (manages objects)</text>
  <rect x="430" y="20" width="140" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="45" text-anchor="middle" font-size="11" font-weight="bold">containerd</text>
  <text x="500" y="62" text-anchor="middle" font-size="9">Container runtime</text>
  <rect x="430" y="120" width="140" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="145" text-anchor="middle" font-size="11" font-weight="bold">runc</text>
  <text x="500" y="162" text-anchor="middle" font-size="9">OCI runtime</text>
  <line x1="150" y1="50" x2="200" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arr02a)"/>
  <line x1="380" y1="50" x2="430" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arr02a)"/>
  <line x1="500" y1="80" x2="500" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arr02a)"/>
  <defs><marker id="arr02a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Docker Engine Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="97" text-anchor="middle" font-size="11" fill="white">Docker</text>
  <text x="300" y="112" text-anchor="middle" font-size="11" fill="white">Engine</text>
  <ellipse cx="120" cy="45" rx="60" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="50" text-anchor="middle" font-size="10">REST API</text>
  <ellipse cx="480" cy="45" rx="60" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="50" text-anchor="middle" font-size="10">containerd</text>
  <ellipse cx="120" cy="160" rx="60" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="165" text-anchor="middle" font-size="10">Docker CLI</text>
  <ellipse cx="480" cy="160" rx="60" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="165" text-anchor="middle" font-size="10">runc</text>
  <line x1="245" y1="78" x2="175" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="78" x2="425" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="122" x2="175" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="122" x2="425" y2="145" stroke="#333" stroke-width="2"/>
</svg>

---

## Container Runtime

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="130" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="50" text-anchor="middle" font-size="10" font-weight="bold">docker run</text>
  <text x="85" y="67" text-anchor="middle" font-size="9">User command</text>
  <rect x="190" y="30" width="130" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="255" y="50" text-anchor="middle" font-size="10" font-weight="bold">containerd</text>
  <text x="255" y="67" text-anchor="middle" font-size="9">Manages lifecycle</text>
  <rect x="360" y="30" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="50" text-anchor="middle" font-size="10" font-weight="bold">shim</text>
  <text x="410" y="67" text-anchor="middle" font-size="9">Daemonless</text>
  <rect x="500" y="30" width="80" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="50" text-anchor="middle" font-size="10" font-weight="bold">runc</text>
  <text x="540" y="67" text-anchor="middle" font-size="9">Spawn</text>
  <rect x="190" y="120" width="390" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="385" y="140" text-anchor="middle" font-size="10">Linux Kernel: namespaces + cgroups + seccomp</text>
  <text x="385" y="157" text-anchor="middle" font-size="9">Process isolation and resource control</text>
  <line x1="150" y1="55" x2="190" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arr02rt)"/>
  <line x1="320" y1="55" x2="360" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arr02rt)"/>
  <line x1="460" y1="55" x2="500" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arr02rt)"/>
  <line x1="410" y1="80" x2="410" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arr02rt)"/>
  <defs><marker id="arr02rt" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Namespace Isolation

| Namespace | Purpose | Isolation |
|-----------|---------|-----------|
| PID | Process isolation | Process tree |
| NET | Network isolation | Network stack |
| MNT | Filesystem isolation | Mount points |
| UTS | System isolation | Hostname |
| IPC | IPC isolation | IPC resources |
| USER | User isolation | User/group IDs |

---

## Control Groups (cgroups)

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="15" width="560" height="170" fill="none" stroke="#333" stroke-width="1" stroke-dasharray="4,4" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold">cgroup hierarchy</text>
  <rect x="50" y="50" width="110" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="72" text-anchor="middle" font-size="10" font-weight="bold">CPU</text>
  <text x="105" y="90" text-anchor="middle" font-size="9">--cpus, shares</text>
  <rect x="185" y="50" width="110" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="72" text-anchor="middle" font-size="10" font-weight="bold">Memory</text>
  <text x="240" y="90" text-anchor="middle" font-size="9">--memory, swap</text>
  <rect x="320" y="50" width="110" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="72" text-anchor="middle" font-size="10" font-weight="bold">Block I/O</text>
  <text x="375" y="90" text-anchor="middle" font-size="9">read/write bps</text>
  <rect x="455" y="50" width="110" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="72" text-anchor="middle" font-size="10" font-weight="bold">PIDs</text>
  <text x="510" y="90" text-anchor="middle" font-size="9">--pids-limit</text>
  <rect x="50" y="120" width="515" height="45" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="140" text-anchor="middle" font-size="10">Each container gets its own cgroup with resource limits enforced by the kernel</text>
  <text x="300" y="155" text-anchor="middle" font-size="9" fill="#555">Prevents any single container from consuming all host resources</text>
</svg>

---

## Storage Drivers

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="97" text-anchor="middle" font-size="11" fill="white">Storage</text>
  <text x="300" y="112" text-anchor="middle" font-size="11" fill="white">Drivers</text>
  <ellipse cx="120" cy="45" rx="60" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="50" text-anchor="middle" font-size="10">overlay2</text>
  <ellipse cx="480" cy="45" rx="60" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="50" text-anchor="middle" font-size="10">devicemapper</text>
  <ellipse cx="120" cy="160" rx="60" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="165" text-anchor="middle" font-size="10">btrfs</text>
  <ellipse cx="480" cy="160" rx="60" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="165" text-anchor="middle" font-size="10">zfs</text>
  <line x1="245" y1="78" x2="175" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="78" x2="425" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="122" x2="175" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="122" x2="425" y2="145" stroke="#333" stroke-width="2"/>
</svg>

---

## Layer Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="250" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="3"/>
  <text x="175" y="30" text-anchor="middle" font-size="10" font-weight="bold">Container Layer (R/W)</text>
  <rect x="50" y="45" width="250" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="175" y="64" text-anchor="middle" font-size="10">COPY app.py /app (Layer 4)</text>
  <rect x="50" y="78" width="250" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="175" y="97" text-anchor="middle" font-size="10">RUN pip install (Layer 3)</text>
  <rect x="50" y="111" width="250" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="175" y="130" text-anchor="middle" font-size="10">RUN apt-get install (Layer 2)</text>
  <rect x="50" y="144" width="250" height="28" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="175" y="163" text-anchor="middle" font-size="10">FROM ubuntu:22.04 (Base Layer)</text>
  <text x="400" y="30" text-anchor="middle" font-size="10" fill="#c62828">Writable</text>
  <text x="400" y="97" text-anchor="middle" font-size="10" fill="#1565c0">Read-only</text>
  <text x="400" y="163" text-anchor="middle" font-size="10" fill="#2e7d32">Shared</text>
  <line x1="310" y1="25" x2="360" y2="25" stroke="#c62828" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="310" y1="92" x2="360" y2="92" stroke="#1565c0" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="310" y1="158" x2="360" y2="158" stroke="#2e7d32" stroke-width="1" stroke-dasharray="3,3"/>
</svg>

---

## Networking Internals

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="15" width="120" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="40" text-anchor="middle" font-size="10" font-weight="bold">Container A</text>
  <text x="110" y="57" text-anchor="middle" font-size="9">eth0 (veth pair)</text>
  <rect x="250" y="15" width="120" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="310" y="40" text-anchor="middle" font-size="10" font-weight="bold">Container B</text>
  <text x="310" y="57" text-anchor="middle" font-size="9">eth0 (veth pair)</text>
  <rect x="100" y="100" width="250" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="122" text-anchor="middle" font-size="11">docker0 bridge (172.17.0.1)</text>
  <rect x="100" y="155" width="250" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="225" y="175" text-anchor="middle" font-size="10">Host eth0 (iptables NAT)</text>
  <rect x="430" y="100" width="140" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="122" text-anchor="middle" font-size="10">External Network</text>
  <line x1="110" y1="75" x2="110" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="310" y1="75" x2="310" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="225" y1="135" x2="225" y2="155" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="117" x2="430" y2="117" stroke="#333" stroke-width="2" marker-end="url(#arr02ni)"/>
  <defs><marker id="arr02ni" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Security Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="500" height="180" fill="none" stroke="#333" stroke-width="1" stroke-dasharray="4,4" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">Defense in Depth</text>
  <rect x="70" y="45" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="65" text-anchor="middle" font-size="10" font-weight="bold">Namespaces</text>
  <text x="120" y="82" text-anchor="middle" font-size="9">Visibility</text>
  <rect x="190" y="45" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="65" text-anchor="middle" font-size="10" font-weight="bold">cgroups</text>
  <text x="240" y="82" text-anchor="middle" font-size="9">Resources</text>
  <rect x="310" y="45" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="360" y="65" text-anchor="middle" font-size="10" font-weight="bold">Seccomp</text>
  <text x="360" y="82" text-anchor="middle" font-size="9">Syscalls</text>
  <rect x="430" y="45" width="100" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="65" text-anchor="middle" font-size="10" font-weight="bold">Capabilities</text>
  <text x="480" y="82" text-anchor="middle" font-size="9">Privileges</text>
  <rect x="70" y="120" width="460" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="140" text-anchor="middle" font-size="10">AppArmor / SELinux mandatory access control profiles</text>
  <text x="300" y="157" text-anchor="middle" font-size="9" fill="#555">read-only rootfs, no-new-privileges, user remapping</text>
</svg>
