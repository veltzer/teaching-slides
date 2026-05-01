---
tags:
  - infrastructure:docker
  - infrastructure:security
level: beginner
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Docker Security Best Practices

---
## What This Chapter Covers

- Running as non-root
- Minimal base images
- Image vulnerability scanning
- Read-only filesystems
- Managing secrets
- Image signing and Content Trust
- Securing the Docker daemon

---
## Why Container Security Matters

- A container is a process, not a sandbox
- Misconfigured containers escalate to host compromise
- Vulnerable images stay in registries indefinitely
- Secrets baked into images leak forever
- These are *easy* mistakes — and easy to fix

---
## Run As Non-Root

```dockerfile
FROM node:20-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --chown=app:app . .
USER app
CMD ["node", "server.js"]
```

- Default container user is root unless you say otherwise
- Create a non-root user; switch with `USER`
- `--chown` on `COPY` to give the new user ownership
- A compromised container that's already non-root has fewer escalation paths

---
## Use Minimal Base Images

- `alpine`: ~5 MB; uses musl libc, may have edge cases
- `*-slim`: distro stripped to essentials (Debian slim ~80 MB)
- `distroless`: only the language runtime + your app — no shell, no package manager
- `scratch`: empty; only for static binaries (Go, Rust)
- Each MB removed is one less thing that can have a CVE

---
## Image Scanning

```bash
docker scout cves nginx:1.27
trivy image nginx:1.27
grype nginx:1.27
```

- Scan images for known vulnerabilities (CVEs)
- Many tools: `docker scout`, Trivy, Grype, Snyk, Anchore
- Run as part of CI; fail builds on critical CVEs you haven't accepted
- Keep base images current — most CVEs are fixed in the next patch release

---
## Read-Only Filesystems

```bash
docker run --read-only --tmpfs /tmp myapp
```

- Container can't write anywhere except mounted volumes / tmpfs
- App needs to write logs/cache somewhere — provide a tmpfs or volume
- Surprisingly compatible with most apps once configured
- Stops a compromised process from modifying its own binaries

---
## Drop Capabilities

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx
```

- Linux capabilities split root's privileges
- A container doesn't need most of them
- Drop everything, add back only what's required
- `NET_BIND_SERVICE` to bind ports < 1024; `CHOWN` for changing file ownership; etc.

---
## Seccomp Profiles

- Restrict which syscalls a container can make
- Docker ships a default profile that blocks ~50 risky syscalls
- Custom profiles for stricter security
- One layer of defence among many
- Combined with `--cap-drop`, dramatically reduces attack surface

---
## Secrets Management

- *Never* bake secrets into images: they live forever in layers
- *Don't* pass via environment variables in production (visible in `docker inspect`)
- Better: mount secrets as files via Docker Swarm secrets or Kubernetes Secrets
- For local dev: `.env` files outside git
- For prod: a real secrets manager (Vault, AWS Secrets Manager, etc.)

---
## Don't Bake Secrets, Examples

```dockerfile
# BAD
ENV DATABASE_PASSWORD=hunter2
COPY id_rsa /root/.ssh/

# Better
# inject at runtime via secrets manager / orchestrator
```

- Anyone who pulls your image can read these
- Removed in a later layer? Still in history
- Trust nobody including your future self

---
## Multi-Stage Builds for Security

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /server ./cmd/server

FROM gcr.io/distroless/static-debian12
COPY --from=build /server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

- The toolchain (with CVEs galore) never reaches the final image
- Final image: ~20 MB, no shell, no package manager
- Even an attacker who gets RCE has nothing to work with

---
## Content Trust and Signing

- Image tags are mutable; an attacker swapping `:latest` is undetectable without verification
- Docker Content Trust: TUF-based image signing
- Cosign / Sigstore: modern, widely adopted alternative
- CI signs after build; runtime verifies signatures before pulling
- Without signing, you're trusting the registry not to be compromised

---
## Securing the Daemon

- The Docker daemon runs as root and exposes a socket
- Anyone with access to `/var/run/docker.sock` is *equivalent to root*
- Don't put non-trusted users in the `docker` group
- Don't expose the daemon on TCP without TLS + client cert auth
- Mounting `docker.sock` into a container = giving the container root on the host

---
## Daemon Hardening Checklist

- Don't expose TCP unless required; if required, use TLS mutual auth
- Run rootless Docker where possible
- Set ulimits on the daemon
- Use user namespaces (`userns-remap`) to map container root to a non-root host user
- Audit Docker socket access — `docker.sock` is the keys to the kingdom

---
## Network Isolation

- Don't put untrusted services on the same Docker network as trusted ones
- Use multiple networks to segment
- `--network=none` for containers that don't need network at all
- Egress filtering: most containers don't need to make arbitrary outbound connections
- Most attacks pivot via the network

---
## Resource Limits = Security

- An attacker that consumes all CPU is a DoS
- `--memory`, `--cpus`, `--pids-limit` cap the damage
- A container without limits is one bad request away from taking down the host
- Set sensible defaults; tighten per service

---
## A Security Checklist

- [ ] Non-root USER in every Dockerfile
- [ ] Minimal base image (alpine / slim / distroless / scratch)
- [ ] Multi-stage builds to drop build tools
- [ ] Image scanned in CI; criticals fail the build
- [ ] No secrets in image layers
- [ ] Resource limits at runtime
- [ ] Read-only filesystem where the app allows
- [ ] Cap-drop ALL, add only what's needed
- [ ] Image signing in CI, verification at runtime

---
## Common Mistakes

- "We'll add security later" &#8594; rebuilding the foundation is expensive
- Mounting `docker.sock` into application containers
- Running scanned-but-unpatched base images for months
- Trusting `:latest` from public registries
- Treating containers as VMs and leaving them sloppy

---
## Course Wrap-Up

- Docker is the unit of modern application packaging
- Images are layered, immutable, content-addressable
- Containers are processes with isolation, not VMs
- Compose runs multi-container apps with one file
- Security is not optional; the defaults are reasonable but not enough
- Next steps: Kubernetes for production orchestration
