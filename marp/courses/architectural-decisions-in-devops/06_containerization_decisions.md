# Containerization Decisions

---

## Why Containerization Matters

1. Containers fundamentally changed how we deploy software
1. Not every workload benefits from containerization
1. Choosing the right runtime, base image, and strategy is critical
1. Poor decisions compound into tech debt across the pipeline

---

## When to Containerize

1. Microservices with independent deployment cycles
1. Applications requiring environment consistency
1. Workloads that benefit from horizontal scaling
1. CI/CD pipelines needing reproducible builds
1. Teams practicing polyglot development

---

## When NOT to Containerize

1. Bare-metal performance-critical workloads (HPC, GPU-bound)
1. Stateful applications tightly coupled to the host OS
1. Legacy monoliths with no refactoring plan
1. Applications requiring direct hardware access
1. Simple scripts or cron jobs with minimal dependencies

---

## Containerization Decision Matrix

<svg viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Should You Containerize?</text>
  <rect x="250" y="40" width="200" height="40" fill="#ffd54f" stroke="#333" stroke-width="2" rx="5"/>
  <text x="350" y="65" text-anchor="middle" font-size="12">New workload?</text>
  <line x1="300" y1="80" x2="150" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="80" x2="550" y2="120" stroke="#333" stroke-width="2"/>
  <text x="210" y="100" font-size="11" fill="#333">No</text>
  <text x="470" y="100" font-size="11" fill="#333">Yes</text>
  <rect x="50" y="120" width="200" height="40" fill="#ffd54f" stroke="#333" stroke-width="2" rx="5"/>
  <text x="150" y="145" text-anchor="middle" font-size="12">Worth refactoring?</text>
  <rect x="450" y="120" width="200" height="40" fill="#ffd54f" stroke="#333" stroke-width="2" rx="5"/>
  <text x="550" y="145" text-anchor="middle" font-size="12">Needs bare metal?</text>
  <line x1="100" y1="160" x2="60" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="160" x2="240" y2="200" stroke="#333" stroke-width="2"/>
  <text x="65" y="185" font-size="11" fill="#333">No</text>
  <text x="220" y="185" font-size="11" fill="#333">Yes</text>
  <line x1="500" y1="160" x2="460" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="600" y1="160" x2="640" y2="200" stroke="#333" stroke-width="2"/>
  <text x="465" y="185" font-size="11" fill="#333">No</text>
  <text x="620" y="185" font-size="11" fill="#333">Yes</text>
  <rect x="10" y="200" width="100" height="35" fill="#ef5350" stroke="#333" stroke-width="1" rx="5"/>
  <text x="60" y="222" text-anchor="middle" font-size="11" fill="white">Keep as-is</text>
  <rect x="190" y="200" width="100" height="35" fill="#66bb6a" stroke="#333" stroke-width="1" rx="5"/>
  <text x="240" y="222" text-anchor="middle" font-size="11" fill="white">Containerize</text>
  <rect x="410" y="200" width="100" height="35" fill="#66bb6a" stroke="#333" stroke-width="1" rx="5"/>
  <text x="460" y="222" text-anchor="middle" font-size="11" fill="white">Containerize</text>
  <rect x="590" y="200" width="100" height="35" fill="#ef5350" stroke="#333" stroke-width="1" rx="5"/>
  <text x="640" y="222" text-anchor="middle" font-size="11" fill="white">Run on host</text>
</svg>

---

## Workload Suitability: Stateless Services

1. REST APIs and `gRPC` services are ideal candidates
1. Easy to scale horizontally behind a load balancer
1. No persistent state to manage inside the container
1. Example: a `Node.js` API serving JSON responses

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY src/ ./src/
CMD ["node", "src/server.js"]
```

---

## Workload Suitability: Stateful Workloads

1. Databases can run in containers but require careful planning
    - Persistent volumes must be properly configured
    - Managed services (RDS, Cloud SQL) are often preferable
1. Batch jobs benefit from clean, isolated environments
    - `Kubernetes` `Jobs` and `CronJobs` provide scheduling
    - Easy to parallelize across nodes

---

## Workload Suitability: Machine Learning

1. Training workloads often need GPU access
    - `NVIDIA Container Toolkit` enables GPU passthrough
    - Adds complexity to the container runtime
1. Inference workloads containerize well
    - Stateless prediction services scale horizontally
1. Large model files inflate image sizes
    - Use volume mounts or model registries instead

---

## Overhead and Complexity Costs

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Container Overhead Spectrum</text>
  <defs>
    <linearGradient id="grad_overhead" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#66bb6a"/>
      <stop offset="50%" style="stop-color:#ffd54f"/>
      <stop offset="100%" style="stop-color:#ef5350"/>
    </linearGradient>
  </defs>
  <rect x="50" y="50" width="600" height="30" fill="url(#grad_overhead)" stroke="#333" stroke-width="1" rx="5"/>
  <text x="50" y="100" font-size="12" fill="#333">Low overhead</text>
  <text x="580" y="100" font-size="12" fill="#333">High overhead</text>
  <line x1="100" y1="120" x2="100" y2="145" stroke="#333" stroke-width="2"/>
  <text x="100" y="160" text-anchor="middle" font-size="11">Stateless API</text>
  <line x1="250" y1="120" x2="250" y2="145" stroke="#333" stroke-width="2"/>
  <text x="250" y="160" text-anchor="middle" font-size="11">Web App</text>
  <line x1="400" y1="120" x2="400" y2="145" stroke="#333" stroke-width="2"/>
  <text x="400" y="160" text-anchor="middle" font-size="11">Database</text>
  <line x1="520" y1="120" x2="520" y2="145" stroke="#333" stroke-width="2"/>
  <text x="520" y="160" text-anchor="middle" font-size="11">GPU workload</text>
  <line x1="620" y1="120" x2="620" y2="145" stroke="#333" stroke-width="2"/>
  <text x="620" y="160" text-anchor="middle" font-size="11">Real-time sys</text>
  <rect x="50" y="190" width="280" height="80" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="190" y="215" text-anchor="middle" font-size="12" font-weight="bold">Worth containerizing</text>
  <text x="190" y="235" text-anchor="middle" font-size="11">Benefits outweigh costs</text>
  <text x="190" y="255" text-anchor="middle" font-size="11">Scaling, portability, isolation</text>
  <rect x="370" y="190" width="280" height="80" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="510" y="215" text-anchor="middle" font-size="12" font-weight="bold">Evaluate carefully</text>
  <text x="510" y="235" text-anchor="middle" font-size="11">Complexity may not justify</text>
  <text x="510" y="255" text-anchor="middle" font-size="11">Consider alternatives</text>
</svg>

---

## Hidden Costs of Containerization

1. Image registry management and storage costs
1. Networking complexity (`CNI` plugins, service mesh)
1. Monitoring and logging require container-aware tooling
1. Security scanning of images in the CI pipeline
1. Team skill ramp-up and operational maturity

---

## Container Runtime Landscape

<svg viewBox="0 0 700 320" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Container Runtime Stack</text>
  <rect x="100" y="240" width="500" height="50" fill="#90a4ae" stroke="#333" stroke-width="2" rx="5"/>
  <text x="350" y="270" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Linux Kernel (cgroups, namespaces, seccomp)</text>
  <rect x="100" y="180" width="500" height="50" fill="#78909c" stroke="#333" stroke-width="2" rx="5"/>
  <text x="350" y="210" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Low-level Runtime (runc, crun, gVisor)</text>
  <rect x="100" y="120" width="500" height="50" fill="#546e7a" stroke="#333" stroke-width="2" rx="5"/>
  <text x="350" y="150" text-anchor="middle" font-size="14" fill="white" font-weight="bold">High-level Runtime (containerd, CRI-O)</text>
  <rect x="150" y="50" width="150" height="50" fill="#42a5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="80" text-anchor="middle" font-size="13" fill="white" font-weight="bold">Docker</text>
  <rect x="400" y="50" width="150" height="50" fill="#66bb6a" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="80" text-anchor="middle" font-size="13" fill="white" font-weight="bold">Kubernetes</text>
  <line x1="225" y1="100" x2="225" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="475" y1="100" x2="475" y2="120" stroke="#333" stroke-width="2"/>
</svg>

---

## Docker: The Pioneer

1. Most widely known container platform
1. Includes build tools, CLI, and runtime in one package
1. Uses `containerd` under the hood since Docker 1.11
1. `Docker Compose` simplifies multi-container local dev
1. Adds overhead compared to direct `containerd` usage

```bash
# Docker wraps containerd
docker info | grep "Server Version"
docker info | grep "containerd"
```

---

## `containerd`: The Industry Standard

1. Graduated CNCF project
1. Default runtime for `Kubernetes` since v1.24
1. Manages complete container lifecycle
    - Image pull, storage, execution, supervision
1. Smaller footprint than full `Docker` daemon
1. Used by major cloud providers (EKS, GKE, AKS)

---

## `CRI-O`: Kubernetes-Native Runtime

1. Built specifically for `Kubernetes`
1. Implements the Container Runtime Interface (`CRI`)
1. Minimal scope: only does what `Kubernetes` needs
1. Default runtime on `OpenShift`
1. Smaller attack surface than `Docker` or `containerd`

---

## Runtime Comparison

| Feature | `Docker` | `containerd` | `CRI-O` |
|---------|----------|--------------|---------|
| K8s support | via `cri-dockerd` | Native CRI | Native CRI |
| Build tools | Built-in | Separate | Separate |
| Footprint | Larger | Medium | Smallest |
| Dev experience | Best | Minimal | Minimal |
| Production use | Common | Most common | OpenShift |

---

## Low-Level Runtimes: `runc` vs `crun`

1. `runc` is the reference OCI runtime written in `Go`
    - Default for `Docker` and `containerd`
    - Maintained by the Open Container Initiative
1. `crun` is an alternative written in `C`
    - Faster startup times (up to 2x)
    - Lower memory footprint
    - Default for `Podman` and `CRI-O`

---

## Sandboxed Runtimes: `gVisor` and `Kata`

1. `gVisor` (`runsc`) intercepts syscalls with a user-space kernel
    - Strong isolation without full VM overhead
    - Some syscalls unsupported; check compatibility
1. `Kata Containers` runs each container in a lightweight VM
    - Near-native performance with VM-level isolation
    - Higher memory usage per container
1. Use when multi-tenant isolation is critical

---

## Choosing a Runtime

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Runtime Selection Guide</text>
  <rect x="50" y="50" width="180" height="100" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="140" y="75" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565c0">Development</text>
  <text x="140" y="100" text-anchor="middle" font-size="11">Docker Desktop</text>
  <text x="140" y="118" text-anchor="middle" font-size="11">or Podman</text>
  <text x="140" y="138" text-anchor="middle" font-size="11">Build + Run + Debug</text>
  <rect x="260" y="50" width="180" height="100" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="350" y="75" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">Production K8s</text>
  <text x="350" y="100" text-anchor="middle" font-size="11">containerd</text>
  <text x="350" y="118" text-anchor="middle" font-size="11">or CRI-O</text>
  <text x="350" y="138" text-anchor="middle" font-size="11">Lean + Standard</text>
  <rect x="470" y="50" width="180" height="100" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="560" y="75" text-anchor="middle" font-size="13" font-weight="bold" fill="#e65100">High Security</text>
  <text x="560" y="100" text-anchor="middle" font-size="11">gVisor or Kata</text>
  <text x="560" y="118" text-anchor="middle" font-size="11">with containerd</text>
  <text x="560" y="138" text-anchor="middle" font-size="11">Isolation + Safety</text>
  <rect x="50" y="190" width="600" height="50" fill="#f5f5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="350" y="210" text-anchor="middle" font-size="12">All runtimes use the same OCI images.</text>
  <text x="350" y="228" text-anchor="middle" font-size="12">Your Dockerfiles work everywhere.</text>
</svg>

---

## Rootless Containers

1. Containers run without `root` privileges on the host
1. The container `UID 0` maps to an unprivileged host UID
1. Limits damage from container breakout attacks
1. Supported by `Docker`, `Podman`, `containerd`

```bash
# Run Docker in rootless mode
dockerd-rootless-setuptool.sh install
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
docker run hello-world
```

---

## Rootless vs Rootful: Trade-offs

| Aspect | Rootful | Rootless |
|--------|---------|----------|
| Networking | Full capabilities | Limited (no raw sockets) |
| Port binding | Any port | Ports > 1024 by default |
| Storage | `overlayfs` native | `fuse-overlayfs` |
| Performance | Native | Slight overhead |
| Security | Root on host | Unprivileged |

---

## `Podman`: Rootless by Default

1. Daemonless container engine from Red Hat
1. Rootless mode is the default, not an add-on
1. CLI compatible with `Docker` commands
1. No central daemon means no single point of failure
1. Uses `crun` as its default low-level runtime

```bash
# Podman is a drop-in replacement
alias docker=podman
podman run --rm -it alpine sh
```

---

## Security Implications of Runtime Choices

1. Rootful `Docker` daemon is a high-value attack target
    - Any user in the `docker` group effectively has root
1. Rootless containers limit blast radius
1. `Seccomp` profiles restrict available syscalls
1. `AppArmor` / `SELinux` provide mandatory access control
1. Read-only root filesystem prevents runtime tampering

```bash
docker run --read-only --security-opt \
  no-new-privileges alpine sh
```

---

## Base Image Strategies Overview

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Base Image Size Comparison</text>
  <text x="45" y="85" text-anchor="end" font-size="12">Scratch</text>
  <rect x="50" y="70" width="10" height="25" fill="#4caf50" stroke="#333" stroke-width="1"/>
  <text x="70" y="88" font-size="11">0 MB</text>
  <text x="45" y="125" text-anchor="end" font-size="12">Distroless</text>
  <rect x="50" y="110" width="30" height="25" fill="#66bb6a" stroke="#333" stroke-width="1"/>
  <text x="90" y="128" font-size="11">~2 MB</text>
  <text x="45" y="165" text-anchor="end" font-size="12">Alpine</text>
  <rect x="50" y="150" width="40" height="25" fill="#81c784" stroke="#333" stroke-width="1"/>
  <text x="100" y="168" font-size="11">~7 MB</text>
  <text x="45" y="205" text-anchor="end" font-size="12">Debian slim</text>
  <rect x="50" y="190" width="130" height="25" fill="#ffd54f" stroke="#333" stroke-width="1"/>
  <text x="190" y="208" font-size="11">~80 MB</text>
  <text x="45" y="245" text-anchor="end" font-size="12">Ubuntu</text>
  <rect x="50" y="230" width="180" height="25" fill="#ff9800" stroke="#333" stroke-width="1"/>
  <text x="240" y="248" font-size="11">~120 MB</text>
  <text x="45" y="285" text-anchor="end" font-size="12">Full Debian</text>
  <rect x="50" y="270" width="250" height="25" fill="#ef5350" stroke="#333" stroke-width="1"/>
  <text x="310" y="288" font-size="11">~180 MB</text>
</svg>

---

## `scratch`: The Empty Base

1. Literally nothing -- zero bytes, no shell, no libraries
1. Only works with statically compiled binaries
1. Smallest possible attack surface
1. Perfect for `Go`, `Rust`, or statically linked `C` binaries

```dockerfile
FROM scratch
COPY myapp /myapp
ENTRYPOINT ["/myapp"]
```

---

## Alpine Linux Images

1. Based on `musl` libc and `BusyBox`, approximately 7 MB
1. Includes `apk` package manager and a shell for debugging
1. Watch out for `musl` vs `glibc` compatibility issues
    - `DNS` resolution behaves differently under `musl`
    - `Python` wheels often compiled for `glibc` only
    - `Node.js` native addons may need recompilation
1. Consider `-slim` variants if you hit compatibility issues

---

## Distroless Images

1. Google-maintained images with minimal contents
1. No shell, no package manager, no unnecessary binaries
1. Available for `Java`, `Python`, `Node.js`, `Go`, `.NET`
1. Reduced CVE count by eliminating unused packages
1. Use `:debug` tag or `kubectl debug` for troubleshooting

```dockerfile
FROM gcr.io/distroless/java21-debian12
COPY target/app.jar /app.jar
CMD ["app.jar"]
```

---

## Container Layer Architecture

<svg viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Container Image Layers</text>
  <rect x="150" y="270" width="400" height="40" fill="#78909c" stroke="#333" stroke-width="2" rx="3"/>
  <text x="350" y="295" text-anchor="middle" font-size="12" fill="white">Base OS Layer (read-only)</text>
  <rect x="150" y="220" width="400" height="40" fill="#90a4ae" stroke="#333" stroke-width="2" rx="3"/>
  <text x="350" y="245" text-anchor="middle" font-size="12" fill="white">Runtime Dependencies (read-only)</text>
  <rect x="150" y="170" width="400" height="40" fill="#b0bec5" stroke="#333" stroke-width="2" rx="3"/>
  <text x="350" y="195" text-anchor="middle" font-size="12">Application Libraries (read-only)</text>
  <rect x="150" y="120" width="400" height="40" fill="#cfd8dc" stroke="#333" stroke-width="2" rx="3"/>
  <text x="350" y="145" text-anchor="middle" font-size="12">Application Code (read-only)</text>
  <rect x="150" y="60" width="400" height="40" fill="#e8f5e9" stroke="#66bb6a" stroke-width="2" rx="3" stroke-dasharray="5,3"/>
  <text x="350" y="85" text-anchor="middle" font-size="12" fill="#2e7d32">Container Writable Layer</text>
  <text x="120" y="85" text-anchor="end" font-size="11" fill="#2e7d32">R/W</text>
  <text x="120" y="145" text-anchor="end" font-size="11" fill="#666">R/O</text>
  <text x="120" y="195" text-anchor="end" font-size="11" fill="#666">R/O</text>
  <text x="120" y="245" text-anchor="end" font-size="11" fill="#666">R/O</text>
  <text x="120" y="295" text-anchor="end" font-size="11" fill="#666">R/O</text>
  <text x="580" y="290" font-size="11" fill="#666">Shared</text>
  <text x="580" y="240" font-size="11" fill="#666">Shared</text>
  <text x="580" y="145" font-size="11" fill="#666">Per-image</text>
  <text x="580" y="85" font-size="11" fill="#2e7d32">Per-container</text>
</svg>

---

## Custom Base Images

1. Organizations should maintain curated base images
1. Pre-baked with security patches and compliance tooling
1. Published to an internal registry
1. Enforced via policy (e.g., `OPA Gatekeeper`)
1. Reduces duplication across teams

```dockerfile
# Organizational base image
FROM internal-registry.company.com/base/python:3.12
LABEL maintainer="platform-team@company.com"
```

---

## Managing Custom Base Image Pipelines

1. Automate base image builds with CI/CD
1. Trigger rebuilds when upstream images update
1. Run vulnerability scans before publishing
1. Version with semantic tags, not just `latest`
1. Notify downstream teams of breaking changes

```yaml
# Example CI trigger
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly rebuild
  push:
    paths: ['base-images/**']
```

---

## Image Tagging Strategies

1. Never rely solely on `latest` in production
1. Use immutable tags: `v1.2.3`, commit SHA, build ID
1. Tag base images with the upstream version + patch date
1. Use digest pinning for maximum reproducibility

```dockerfile
# Mutable tag (avoid in production)
FROM python:3.12

# Immutable digest (reproducible)
FROM python@sha256:a1b2c3d4e5f6...
```

---

## Multi-Stage Builds: The Concept

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Multi-Stage Build Flow</text>
  <defs>
    <marker id="arrow_ms" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="50" width="200" height="200" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="130" y="75" text-anchor="middle" font-size="13" font-weight="bold" fill="#e65100">Stage 1: Build</text>
  <rect x="50" y="90" width="160" height="25" fill="#ffe0b2" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="130" y="107" text-anchor="middle" font-size="11">Full OS + compilers</text>
  <rect x="50" y="125" width="160" height="25" fill="#ffe0b2" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="130" y="142" text-anchor="middle" font-size="11">Source code</text>
  <rect x="50" y="160" width="160" height="25" fill="#ffe0b2" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="130" y="177" text-anchor="middle" font-size="11">Build dependencies</text>
  <rect x="50" y="195" width="160" height="25" fill="#ffcc80" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="130" y="212" text-anchor="middle" font-size="11" font-weight="bold">Compiled artifact</text>
  <line x1="230" y1="207" x2="290" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow_ms)"/>
  <text x="270" y="165" font-size="11" fill="#333">COPY</text>
  <rect x="300" y="80" width="180" height="150" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="390" y="105" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">Stage 2: Runtime</text>
  <rect x="320" y="120" width="140" height="25" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="390" y="137" text-anchor="middle" font-size="11">Minimal base image</text>
  <rect x="320" y="155" width="140" height="25" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="390" y="172" text-anchor="middle" font-size="11" font-weight="bold">Compiled artifact</text>
  <line x1="480" y1="155" x2="540" y2="155" stroke="#333" stroke-width="2" marker-end="url(#arrow_ms)"/>
  <rect x="550" y="110" width="120" height="90" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="610" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565c0">Final Image</text>
  <text x="610" y="165" text-anchor="middle" font-size="11">Small</text>
  <text x="610" y="180" text-anchor="middle" font-size="11">Secure</text>
</svg>

---

## Multi-Stage Build: Go Example

```dockerfile
# Stage 1: Build
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server

# Stage 2: Runtime
FROM scratch
COPY --from=builder /server /server
ENTRYPOINT ["/server"]
```

- Build image: ~800 MB
- Final image: ~10 MB

---

## Multi-Stage Build: Java Example

```dockerfile
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime only
FROM gcr.io/distroless/java21-debian12
COPY --from=build /app/target/*.jar /app.jar
CMD ["app.jar"]
```

---

## Multi-Stage Build: Node.js Example

```dockerfile
# Stage 1: Install all dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM deps AS build
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
CMD ["node", "dist/index.js"]
```

---

## Build Cache Optimization

1. Order `Dockerfile` instructions from least to most frequently changing
1. Copy dependency files before source code
1. Use `.dockerignore` to exclude unnecessary files
1. Leverage `BuildKit` cache mounts for package managers

```dockerfile
# Cache mount for pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

---

## `.dockerignore` Best Practices

1. Exclude everything by default, then whitelist
1. Reduces build context size and speeds up builds
1. Prevents secrets from leaking into the image

```text
# .dockerignore
*
!src/
!package.json
!package-lock.json
!tsconfig.json
.git
.env
*.md
node_modules
```

---

## Image Scanning and Vulnerability Management

1. Scan images in CI before pushing to registry
1. Use tools like `Trivy`, `Grype`, or `Snyk`
1. Set severity thresholds to fail builds
1. Scan base images separately from application layers
1. Rebuild images regularly to pick up OS patches

```bash
# Scan with Trivy
trivy image --severity HIGH,CRITICAL \
  --exit-code 1 myapp:latest
```

---

## Reducing Image Size: Practical Tips

1. Remove package manager caches in the same `RUN` layer
1. Combine related `RUN` commands with `&&`
1. Use `--no-install-recommends` for `apt`
1. Delete temporary files in the build layer

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
```

---

## Layer Optimization

<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Layer Optimization: Before vs After</text>
  <rect x="30" y="45" width="300" height="210" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="5"/>
  <text x="180" y="65" text-anchor="middle" font-size="13" font-weight="bold" fill="#c62828">Before (5 layers, 450 MB)</text>
  <rect x="50" y="80" width="260" height="30" fill="#ef9a9a" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="180" y="100" text-anchor="middle" font-size="10">RUN apt-get update</text>
  <rect x="50" y="115" width="260" height="30" fill="#ef9a9a" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="180" y="135" text-anchor="middle" font-size="10">RUN apt-get install gcc</text>
  <rect x="50" y="150" width="260" height="30" fill="#ef9a9a" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="180" y="170" text-anchor="middle" font-size="10">RUN pip install deps</text>
  <rect x="50" y="185" width="260" height="30" fill="#ef9a9a" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="180" y="205" text-anchor="middle" font-size="10">RUN apt-get remove gcc</text>
  <rect x="50" y="220" width="260" height="25" fill="#ef9a9a" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="180" y="237" text-anchor="middle" font-size="10">gcc still in earlier layer!</text>
  <rect x="380" y="45" width="300" height="210" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="5"/>
  <text x="530" y="65" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">After (2 layers, 120 MB)</text>
  <rect x="400" y="80" width="260" height="80" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="530" y="110" text-anchor="middle" font-size="10">RUN apt-get update &&</text>
  <text x="530" y="125" text-anchor="middle" font-size="10">apt-get install gcc &&</text>
  <text x="530" y="140" text-anchor="middle" font-size="10">pip install deps && apt-get remove gcc</text>
  <rect x="400" y="170" width="260" height="35" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="530" y="192" text-anchor="middle" font-size="10">COPY app /app</text>
  <text x="530" y="230" text-anchor="middle" font-size="12" fill="#2e7d32">gcc removed in same layer = gone</text>
</svg>

---

## `BuildKit` Features

1. Enabled by default in Docker 23.0+
1. Parallel execution of independent build stages
1. Better caching with cache mounts and bind mounts
1. Secret mounts to avoid leaking credentials
1. SSH agent forwarding for private repo access

```bash
# Enable BuildKit (older Docker versions)
export DOCKER_BUILDKIT=1

# Use secret mount
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

---

## Image Signing and Provenance

1. Sign images with `cosign` (Sigstore project)
1. Verify signatures before deployment
1. Attach SBOMs (Software Bill of Materials) to images
1. Use `SLSA` provenance for supply chain security

```bash
# Sign an image with cosign
cosign sign myregistry.com/myapp:v1.2.3

# Verify before deploying
cosign verify myregistry.com/myapp:v1.2.3
```

---

## Container Image Lifecycle

<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="25" text-anchor="middle" font-size="16" font-weight="bold">Image Lifecycle Pipeline</text>
  <defs>
    <marker id="arrow_lc" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="60" width="100" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="70" y="82" text-anchor="middle" font-size="11" font-weight="bold">Code</text>
  <text x="70" y="98" text-anchor="middle" font-size="10">Commit</text>
  <line x1="120" y1="85" x2="150" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow_lc)"/>
  <rect x="155" y="60" width="100" height="50" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="205" y="82" text-anchor="middle" font-size="11" font-weight="bold">Build</text>
  <text x="205" y="98" text-anchor="middle" font-size="10">Multi-stage</text>
  <line x1="255" y1="85" x2="285" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow_lc)"/>
  <rect x="290" y="60" width="100" height="50" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="340" y="82" text-anchor="middle" font-size="11" font-weight="bold">Scan</text>
  <text x="340" y="98" text-anchor="middle" font-size="10">Trivy/Grype</text>
  <line x1="390" y1="85" x2="420" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow_lc)"/>
  <rect x="425" y="60" width="100" height="50" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2" rx="5"/>
  <text x="475" y="82" text-anchor="middle" font-size="11" font-weight="bold">Sign</text>
  <text x="475" y="98" text-anchor="middle" font-size="10">Cosign</text>
  <line x1="525" y1="85" x2="555" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow_lc)"/>
  <rect x="560" y="60" width="110" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="615" y="82" text-anchor="middle" font-size="11" font-weight="bold">Registry</text>
  <text x="615" y="98" text-anchor="middle" font-size="10">Push + Tag</text>
  <line x1="615" y1="110" x2="615" y2="145" stroke="#333" stroke-width="2" marker-end="url(#arrow_lc)"/>
  <rect x="500" y="150" width="230" height="50" fill="#e0f2f1" stroke="#00695c" stroke-width="2" rx="5"/>
  <text x="615" y="172" text-anchor="middle" font-size="11" font-weight="bold">Deploy</text>
  <text x="615" y="188" text-anchor="middle" font-size="10">K8s / ECS / Nomad</text>
</svg>

---

## Policy Enforcement for Images

1. Restrict which registries are allowed in production
1. Require image signing verification at admission
1. Enforce base image standards with `OPA` or `Kyverno`
1. Block images running as `root` user

```yaml
# Kyverno policy: require approved registry
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-approved-base
spec:
  rules:
    - name: check-image
      match:
        resources:
          kinds: ["Pod"]
      validate:
        message: "Use approved base images"
        pattern:
          spec:
            containers:
              - image: "registry.company.com/*"
```

---

## Summary: Key Decision Points

1. **Containerize when** portability and consistency matter
1. **Skip containers when** bare-metal performance is essential
1. **Use `containerd`** for production `Kubernetes` workloads
1. **Prefer rootless** containers for improved security posture
1. **Choose distroless or Alpine** to minimize attack surface
1. **Always use multi-stage builds** to keep images small
1. **Automate scanning and signing** in your CI pipeline
