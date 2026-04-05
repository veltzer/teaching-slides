# Starting Out with Docker

---

## Installing Docker

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="62" text-anchor="middle" font-size="11" font-weight="bold">Linux</text>
  <text x="105" y="80" text-anchor="middle" font-size="9">apt/yum install</text>
  <text x="105" y="92" text-anchor="middle" font-size="9">docker-ce</text>
  <rect x="220" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="62" text-anchor="middle" font-size="11" font-weight="bold">macOS</text>
  <text x="295" y="80" text-anchor="middle" font-size="9">Docker Desktop</text>
  <text x="295" y="92" text-anchor="middle" font-size="9">HyperKit VM</text>
  <rect x="410" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="62" text-anchor="middle" font-size="11" font-weight="bold">Windows</text>
  <text x="485" y="80" text-anchor="middle" font-size="9">Docker Desktop</text>
  <text x="485" y="92" text-anchor="middle" font-size="9">WSL2 backend</text>
  <rect x="30" y="130" width="530" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="295" y="155" text-anchor="middle" font-size="10">All platforms: Docker CLI + Docker Daemon + containerd + runc</text>
</svg>

---

## System Requirements

| Component | Linux | Windows | macOS |
|-----------|--------|----------|--------|
| OS Version | Ubuntu 22.04+ | Windows 10 Pro+ | macOS 10.15+ |
| Memory | 4GB minimum | 4GB minimum | 4GB minimum |
| CPU | 2 cores | 2 cores, Hyper-V | 2 cores |
| Disk Space | 20GB | 20GB | 20GB |

---

## Installation Steps: Ubuntu

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="47" text-anchor="middle" font-size="10" font-weight="bold">1. Add repo</text>
  <text x="80" y="62" text-anchor="middle" font-size="9">GPG key + apt</text>
  <rect x="165" y="30" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="47" text-anchor="middle" font-size="10" font-weight="bold">2. Install</text>
  <text x="225" y="62" text-anchor="middle" font-size="9">docker-ce</text>
  <rect x="310" y="30" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="370" y="47" text-anchor="middle" font-size="10" font-weight="bold">3. Start</text>
  <text x="370" y="62" text-anchor="middle" font-size="9">systemctl enable</text>
  <rect x="455" y="30" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="47" text-anchor="middle" font-size="10" font-weight="bold">4. Verify</text>
  <text x="515" y="62" text-anchor="middle" font-size="9">hello-world</text>
  <line x1="140" y1="50" x2="165" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arr03inst)"/>
  <line x1="285" y1="50" x2="310" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arr03inst)"/>
  <line x1="430" y1="50" x2="455" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arr03inst)"/>
  <rect x="20" y="100" width="555" height="70" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="297" y="120" text-anchor="middle" font-size="10" font-weight="bold">Post-install: Add user to docker group</text>
  <text x="297" y="140" text-anchor="middle" font-size="10" font-family="monospace">sudo usermod -aG docker $USER</text>
  <text x="297" y="158" text-anchor="middle" font-size="9" fill="#555">Log out and back in for group changes to take effect</text>
  <defs><marker id="arr03inst" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Verifying Installation

| Command | Purpose | Expected Output |
|---------|---------|----------------|
| `docker --version` | Check Docker version | Docker version X.X.X |
| `docker info` | System information | Docker system info |
| `docker run hello-world` | Test installation | Hello from Docker! |
| `docker ps` | List containers | Empty list or running containers |

---

## Running Your First Container

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="40" text-anchor="middle" font-size="10" font-weight="bold">docker run</text>
  <text x="75" y="57" text-anchor="middle" font-size="9">Parse flags</text>
  <rect x="165" y="20" width="110" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="40" text-anchor="middle" font-size="10" font-weight="bold">Pull image</text>
  <text x="220" y="57" text-anchor="middle" font-size="9">If not local</text>
  <rect x="310" y="20" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="365" y="40" text-anchor="middle" font-size="10" font-weight="bold">Create</text>
  <text x="365" y="57" text-anchor="middle" font-size="9">Container layer</text>
  <rect x="455" y="20" width="110" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="40" text-anchor="middle" font-size="10" font-weight="bold">Start</text>
  <text x="510" y="57" text-anchor="middle" font-size="9">Run process</text>
  <line x1="130" y1="45" x2="165" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arr03run)"/>
  <line x1="275" y1="45" x2="310" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arr03run)"/>
  <line x1="420" y1="45" x2="455" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arr03run)"/>
  <rect x="20" y="100" width="545" height="70" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="292" y="120" text-anchor="middle" font-size="10" font-family="monospace">$ docker run -it ubuntu:22.04 /bin/bash</text>
  <text x="292" y="140" text-anchor="middle" font-size="9">-i = interactive (keep STDIN open) | -t = allocate pseudo-TTY</text>
  <text x="292" y="158" text-anchor="middle" font-size="9" fill="#555">You are now inside the container with a shell</text>
  <defs><marker id="arr03run" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Basic Docker Commands

| Command | Usage | Example |
|---------|--------|---------|
| `pull` | Download image | `docker pull ubuntu` |
| `run` | Run container | `docker run nginx` |
| `ps` | List containers | `docker ps -a` |
| `images` | List images | `docker images` |
| `stop` | Stop container | `docker stop container_id` |

---

## Docker Concepts: Image vs Container

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="200" height="160" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="45" text-anchor="middle" font-size="12" font-weight="bold">Image</text>
  <text x="130" y="65" text-anchor="middle" font-size="10">Read-only template</text>
  <text x="130" y="85" text-anchor="middle" font-size="10">Layered filesystem</text>
  <text x="130" y="105" text-anchor="middle" font-size="10">Built from Dockerfile</text>
  <text x="130" y="125" text-anchor="middle" font-size="10">Stored in registry</text>
  <text x="130" y="150" text-anchor="middle" font-size="9" fill="#555">Like a class definition</text>
  <rect x="370" y="20" width="200" height="160" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="45" text-anchor="middle" font-size="12" font-weight="bold">Container</text>
  <text x="470" y="65" text-anchor="middle" font-size="10">Running instance</text>
  <text x="470" y="85" text-anchor="middle" font-size="10">Writable layer on top</text>
  <text x="470" y="105" text-anchor="middle" font-size="10">Has process + state</text>
  <text x="470" y="125" text-anchor="middle" font-size="10">Ephemeral by default</text>
  <text x="470" y="150" text-anchor="middle" font-size="9" fill="#555">Like an object instance</text>
  <line x1="230" y1="100" x2="370" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arr03ic)"/>
  <text x="300" y="90" text-anchor="middle" font-size="10" font-weight="bold">run</text>
  <defs><marker id="arr03ic" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Image Basics

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="200" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="3"/>
  <text x="150" y="30" text-anchor="middle" font-size="10" font-weight="bold">Container R/W Layer</text>
  <rect x="50" y="45" width="200" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="62" text-anchor="middle" font-size="10">Application Code</text>
  <rect x="50" y="75" width="200" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="92" text-anchor="middle" font-size="10">Dependencies</text>
  <rect x="50" y="105" width="200" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="122" text-anchor="middle" font-size="10">Runtime (Python, Node)</text>
  <rect x="50" y="135" width="200" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="150" y="155" text-anchor="middle" font-size="10">Base OS (Ubuntu, Alpine)</text>
  <rect x="330" y="30" width="230" height="130" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="445" y="55" text-anchor="middle" font-size="10" font-weight="bold">Image Properties</text>
  <text x="445" y="75" text-anchor="middle" font-size="9">Immutable layers (read-only)</text>
  <text x="445" y="92" text-anchor="middle" font-size="9">Content-addressable (SHA256)</text>
  <text x="445" y="109" text-anchor="middle" font-size="9">Shared between containers</text>
  <text x="445" y="126" text-anchor="middle" font-size="9">Cached for fast builds</text>
  <text x="445" y="143" text-anchor="middle" font-size="9">Stored in registries</text>
</svg>

---

## Container States

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="80" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="50" y="105" text-anchor="middle" font-size="10">Created</text>
  <rect x="130" y="80" width="80" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="170" y="105" text-anchor="middle" font-size="10">Running</text>
  <rect x="250" y="80" width="80" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="290" y="105" text-anchor="middle" font-size="10">Paused</text>
  <rect x="370" y="80" width="80" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="105" text-anchor="middle" font-size="10">Exited</text>
  <rect x="490" y="80" width="80" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="530" y="105" text-anchor="middle" font-size="10">Dead</text>
  <line x1="90" y1="100" x2="130" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arr03st)"/>
  <line x1="210" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arr03st)"/>
  <line x1="330" y1="100" x2="370" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arr03st)"/>
  <line x1="450" y1="100" x2="490" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arr03st)"/>
  <path d="M 290 80 Q 290 50 170 50 Q 170 50 170 80" fill="none" stroke="#333" stroke-width="1.5" marker-end="url(#arr03st)"/>
  <text x="230" y="47" text-anchor="middle" font-size="9" fill="#555">unpause</text>
  <defs><marker id="arr03st" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Docker Hub

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="60" width="130" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="85" text-anchor="middle" font-size="10" font-weight="bold">Developer</text>
  <text x="95" y="102" text-anchor="middle" font-size="9">docker push</text>
  <text x="95" y="117" text-anchor="middle" font-size="9">docker pull</text>
  <rect x="230" y="40" width="140" height="110" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="65" text-anchor="middle" font-size="11" font-weight="bold">Docker Hub</text>
  <text x="300" y="85" text-anchor="middle" font-size="9">Official images</text>
  <text x="300" y="100" text-anchor="middle" font-size="9">Community images</text>
  <text x="300" y="115" text-anchor="middle" font-size="9">Private repos</text>
  <text x="300" y="130" text-anchor="middle" font-size="9">Automated builds</text>
  <rect x="440" y="60" width="130" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="85" text-anchor="middle" font-size="10" font-weight="bold">Production</text>
  <text x="505" y="102" text-anchor="middle" font-size="9">docker pull</text>
  <text x="505" y="117" text-anchor="middle" font-size="9">docker run</text>
  <line x1="160" y1="85" x2="230" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arr03hub)"/>
  <line x1="230" y1="105" x2="160" y2="105" stroke="#333" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arr03hub)"/>
  <line x1="370" y1="95" x2="440" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arr03hub)"/>
  <defs><marker id="arr03hub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Image Naming Convention

| Component | Example | Description |
|-----------|---------|-------------|
| Registry | docker.io | Image registry host |
| Repository | nginx | Image name |
| Tag | latest | Image version |
| Full Name | docker.io/nginx:latest | Complete image reference |

---

## Basic Container Operations

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <line x1="120" y1="45" x2="120" y2="185" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="45" x2="450" y2="185" stroke="#333" stroke-width="2"/>
  <rect x="60" y="15" width="120" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="120" y="35" text-anchor="middle" font-size="11">Docker CLI</text>
  <rect x="390" y="15" width="120" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="3"/>
  <text x="450" y="35" text-anchor="middle" font-size="11">Container</text>
  <line x1="120" y1="65" x2="450" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arr03ops)"/>
  <text x="285" y="60" text-anchor="middle" font-size="9">docker run (create + start)</text>
  <line x1="120" y1="95" x2="450" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arr03ops)"/>
  <text x="285" y="90" text-anchor="middle" font-size="9">docker exec -it bash</text>
  <line x1="120" y1="125" x2="450" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arr03ops)"/>
  <text x="285" y="120" text-anchor="middle" font-size="9">docker stop (SIGTERM)</text>
  <line x1="450" y1="155" x2="120" y2="155" stroke="#333" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arr03ops)"/>
  <text x="285" y="150" text-anchor="middle" font-size="9">exit code returned</text>
  <line x1="120" y1="175" x2="450" y2="175" stroke="#333" stroke-width="2" marker-end="url(#arr03ops)"/>
  <text x="285" y="170" text-anchor="middle" font-size="9">docker rm (cleanup)</text>
  <defs><marker id="arr03ops" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>
</svg>

---

## Common Networking Options

| Option | Usage | Example |
|--------|--------|---------|
| `-p` | Port mapping | `-p 8080:80` |
| `--network` | Network type | `--network bridge` |
| `-h` | Hostname | `-h mycontainer` |
| `--dns` | DNS servers | `--dns 8.8.8.8` |

---

## Best Practices for Beginners

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="97" text-anchor="middle" font-size="11" fill="white">Docker</text>
  <text x="300" y="112" text-anchor="middle" font-size="11" fill="white">Basics</text>
  <ellipse cx="120" cy="45" rx="65" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="50" text-anchor="middle" font-size="10">Use --rm flag</text>
  <ellipse cx="480" cy="45" rx="65" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="50" text-anchor="middle" font-size="10">Name containers</text>
  <ellipse cx="120" cy="160" rx="65" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="165" text-anchor="middle" font-size="10">Tag images</text>
  <ellipse cx="480" cy="160" rx="65" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="165" text-anchor="middle" font-size="10">Read logs first</text>
  <line x1="245" y1="78" x2="180" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="78" x2="420" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="122" x2="180" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="122" x2="420" y2="145" stroke="#333" stroke-width="2"/>
</svg>
