---
tags:
  - practices:devops
  - concepts:architecture
  - practices:ci-cd
  - infrastructure:infrastructure-as-code
level: advanced
category: devops
audience:
  - audiences:architects
  - audiences:devops
  - audiences:managers

---

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

![containerization_decision_matrix](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/containerization_decision_matrix.svg)

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

![overhead_and_complexity_costs](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/overhead_and_complexity_costs.svg)

---

## Hidden Costs of Containerization

1. Image registry management and storage costs
1. Networking complexity (`CNI` plugins, service mesh)
1. Monitoring and logging require container-aware tooling
1. Security scanning of images in the CI pipeline
1. Team skill ramp-up and operational maturity

---

## Container Runtime Landscape

![container_runtime_landscape](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/container_runtime_landscape.svg)

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

![choosing_a_runtime](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/choosing_a_runtime.svg)

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

![base_image_strategies_overview](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/base_image_strategies_overview.svg)

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

![container_layer_architecture](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/container_layer_architecture.svg)

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

![multi_stage_builds_the_concept](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/multi_stage_builds_the_concept.svg)

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

```gitignore
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

![layer_optimization](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/layer_optimization.svg)

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

![container_image_lifecycle](svg/courses/devops/architectural-decisions-in-devops/06_containerization_decisions/container_image_lifecycle.svg)

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
