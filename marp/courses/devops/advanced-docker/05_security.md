---
tags:
  - tools:docker
  - infrastructure:containers
  - practices:devops
  - networking:networking
level: advanced
category: devops
audience:
  - audiences:developers

---
# Docker Security and Compliance

Hardening containers for production

---

## Agenda

- Docker daemon security
- `Linux` capabilities
- `Seccomp` profiles
- `AppArmor` and `SELinux`
- Docker Content Trust
- Image scanning and vulnerability management
- `CIS` Docker Benchmark
- Rootless `Docker`
- Runtime security

---

## The Docker Attack Surface

![the_docker_attack_surface](svg/courses/devops/advanced-docker/05_security/the_docker_attack_surface.svg)

---

## Docker Daemon Security

```bash
# The daemon runs as root - access = root on host
# Protect the docker socket!

# BAD: World-readable socket
ls -la /var/run/docker.sock
# srw-rw---- 1 root docker 0 ... /var/run/docker.sock

# BAD: Mounting docker socket in containers
docker run -v /var/run/docker.sock:/var/run/docker.sock myapp
# This gives the container full host root access!

# Limit docker group membership
# Anyone in the docker group effectively has root
getent group docker
```

---

## Daemon TLS Authentication

```bash
# Generate CA, server, and client certificates
# CA key
openssl genrsa -aes256 -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -out ca.pem

# Server key
openssl genrsa -out server-key.pem 4096
openssl req -new -key server-key.pem -out server.csr
openssl x509 -req -days 365 -in server.csr \
  -CA ca.pem -CAkey ca-key.pem -out server-cert.pem

# Configure daemon for TLS
{
  "tls": true,
  "tlsverify": true,
  "tlscacert": "/etc/docker/ca.pem",
  "tlscert": "/etc/docker/server-cert.pem",
  "tlskey": "/etc/docker/server-key.pem",
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"]
}
```

---

## Linux Capabilities

![linux_capabilities](svg/courses/devops/advanced-docker/05_security/linux_capabilities.svg)

---

## Linux Capabilities - Overview

```bash
# Traditional: binary root/non-root model
# Capabilities: fine-grained privileges

# Docker drops many capabilities by default
# Default capabilities kept:
# CHOWN, DAC_OVERRIDE, FSETID, FOWNER, MKNOD, NET_RAW,
# SETGID, SETUID, SETFCAP, SETPCAP, NET_BIND_SERVICE,
# SYS_CHROOT, KILL, AUDIT_WRITE

# View container capabilities
docker run --rm alpine sh -c 'cat /proc/1/status | grep Cap'
# CapPrm: 00000000a80425fb
# CapEff: 00000000a80425fb

# Decode capabilities
capsh --decode=00000000a80425fb
```

---

## Managing Capabilities

```bash
# Drop all capabilities
docker run --rm --cap-drop=ALL alpine id

# Drop all, then add only what's needed
docker run --rm \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  nginx

# Drop specific capabilities
docker run --rm \
  --cap-drop=NET_RAW \
  --cap-drop=MKNOD \
  alpine ping 8.8.8.8
# ping: permission denied (raw socket not allowed)

# NEVER use --privileged in production
# --privileged gives ALL capabilities + device access
docker run --privileged myapp  # DANGEROUS
```

---

## Capabilities Reference

| Capability          | Purpose                              | Drop? |
|---------------------|--------------------------------------|-------|
| `NET_RAW`           | Raw sockets (ping, ARP)             | Yes   |
| `SYS_ADMIN`        | Mount, sethostname, many things     | Yes   |
| `SYS_PTRACE`       | Trace/debug processes               | Yes   |
| `SYS_MODULE`       | Load kernel modules                 | Yes   |
| `NET_ADMIN`        | Network configuration               | Yes   |
| `SYS_TIME`         | Set system clock                    | Yes   |
| `NET_BIND_SERVICE`  | Bind to ports < 1024               | Maybe |
| `CHOWN`            | Change file ownership               | Maybe |
| `SETUID`/`SETGID`  | Change UID/GID                      | Maybe |

---

## `Seccomp` Profiles

```bash
# Seccomp filters system calls the container can make
# Docker's default profile blocks ~44 of ~300+ syscalls

# View default seccomp profile
docker info --format '{{.SecurityOptions}}'

# Run with the default profile (already applied)
docker run --rm alpine sh

# Disable seccomp (not recommended)
docker run --rm --security-opt seccomp=unconfined alpine sh

# Use a custom profile
docker run --rm \
  --security-opt seccomp=./my-seccomp-profile.json \
  alpine sh
```

---

## Custom `Seccomp` Profile

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "defaultErrnoRet": 1,
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "accept", "access", "arch_prctl", "bind", "brk",
        "clone", "close", "connect", "dup", "dup2",
        "execve", "exit", "exit_group", "fcntl", "fstat",
        "futex", "getdents64", "getpid", "getuid",
        "ioctl", "listen", "lseek", "mmap", "mprotect",
        "munmap", "nanosleep", "open", "openat", "pipe",
        "poll", "read", "recvfrom", "rt_sigaction",
        "rt_sigprocmask", "sendto", "set_tid_address",
        "socket", "stat", "write"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

---

## Generating `Seccomp` Profiles with `strace`

```bash
# Record syscalls made by your application
docker run --rm \
  --security-opt seccomp=unconfined \
  myapp strace -f -o /dev/stderr -e trace=%desc,%file,%process,%network \
  /app/server 2> syscalls.log

# Parse unique syscalls
grep -oP '^\w+' syscalls.log | sort -u > needed_syscalls.txt

# Use OCI seccomp profile generator
# https://github.com/containers/oci-seccomp-bpf-hook

docker run --rm \
  --annotation io.containers.trace-syscall="of:/tmp/profile.json" \
  myapp
```

---

## `AppArmor` Profiles

```bash
# Check if AppArmor is enabled
docker info --format '{{.SecurityOptions}}'
# [name=apparmor ...]

# Docker applies docker-default profile by default
# View loaded profiles
sudo aa-status

# Use a custom AppArmor profile
docker run --rm \
  --security-opt apparmor=my-custom-profile \
  alpine sh

# Disable AppArmor for a container
docker run --rm \
  --security-opt apparmor=unconfined \
  alpine sh
```

---

## Custom `AppArmor` Profile

```misc
# /etc/apparmor.d/docker-myapp
#include <tunables/global>

profile docker-myapp flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Deny all network access
  deny network,

  # Allow read-only access to /app
  /app/** r,

  # Allow execution of the app binary
  /app/server ix,

  # Allow read access to libraries
  /lib/** r,
  /usr/lib/** r,

  # Deny write to sensitive locations
  deny /etc/** w,
  deny /proc/** w,
  deny /sys/** w,
}
```

```bash
sudo apparmor_parser -r /etc/apparmor.d/docker-myapp
docker run --security-opt apparmor=docker-myapp myapp
```

---

## Read-Only Root Filesystem

```bash
# Make the root filesystem read-only
docker run -d --read-only --name secure-app myapp

# Apps that need to write temp files: use tmpfs
docker run -d --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --tmpfs /run:rw,noexec,nosuid,size=50m \
  --name secure-app myapp

# In Docker Compose
services:
  app:
    image: myapp
    read_only: true
    tmpfs:
      - /tmp:size=100m
      - /run:size=50m
```

---

## No New Privileges

```bash
# Prevent privilege escalation via setuid/setgid binaries
docker run --rm \
  --security-opt no-new-privileges:true \
  alpine sh

# In daemon.json (enforce globally)
{
  "no-new-privileges": true
}

# Verify
docker exec mycontainer cat /proc/1/status | grep NoNewPrivs
# NoNewPrivs: 1
```

---

## Docker Content Trust (`DCT`)

```bash
# Enable content trust - only pull signed images
export DOCKER_CONTENT_TRUST=1

# Pull unsigned image fails
docker pull unsigned-image:latest
# Error: remote trust data does not exist

# Sign and push an image
docker push myregistry.com/myapp:1.0
# Signing and pushing trust metadata

# Manage signing keys
docker trust key generate mykey
docker trust signer add --key mykey.pub mysigner \
  myregistry.com/myapp

# View trust data
docker trust inspect --pretty myregistry.com/myapp

# Sign an existing tag
docker trust sign myregistry.com/myapp:1.0
```

---
## Content Trust - Key Management

![content_trust_key_management](svg/courses/devops/advanced-docker/05_security/content_trust_key_management.svg)

---
## Content Trust - Key Management

```bash
# Key storage location
ls ~/.docker/trust/private/
# Backup root key (critical!)
tar czf docker-trust-keys.tar.gz ~/.docker/trust/
# Store securely offline
```

---

## Image Scanning with `Trivy`

```bash
# Install Trivy
sudo apt-get install trivy

# Scan an image for vulnerabilities
trivy image myapp:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL myapp:latest

# Output in JSON format
trivy image --format json -o results.json myapp:latest

# Scan in CI/CD - fail on critical vulns
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Scan a Dockerfile
trivy config Dockerfile

# Scan filesystem
trivy fs --security-checks vuln,config /path/to/project
```

---

## Image Scanning - `Trivy` Output Example

![image_scanning_trivy_output_example](svg/courses/devops/advanced-docker/05_security/image_scanning_trivy_output_example.svg)

---

## Image Scanning in CI/CD

```yaml
# GitHub Actions example
name: Security Scan
on: [push]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## `Docker Scout` - Vulnerability Management

```bash
# Analyze image
docker scout cves myapp:latest

# Quick overview with recommendations
docker scout quickview myapp:latest

# Compare versions
docker scout compare myapp:v2.0 --to myapp:v1.0

# View SBOM
docker scout sbom myapp:latest

# Policy compliance
docker scout policy myapp:latest

# Enable in Docker Desktop for continuous monitoring
# Settings → Docker Scout → Enable
```

---

## Secrets Management

```bash
# NEVER put secrets in Dockerfile or environment variables
# BAD:
ENV DATABASE_PASSWORD=supersecret
# This is visible in docker inspect and image history!

# Docker Swarm secrets
echo "mypassword" | docker secret create db_password -
docker service create --name web \
  --secret db_password \
  myapp

# Inside container, secret available at:
cat /run/secrets/db_password

# Docker Compose secrets
# docker-compose.yml:
services:
  web:
    image: myapp
    secrets:
      - db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## Secrets in `BuildKit`

```dockerfile
# syntax=docker/dockerfile:1

# Build-time secrets (never stored in layers)
FROM python:3.12-slim

# Mount secret during build
RUN --mount=type=secret,id=pip_token \
    PIP_TOKEN=$(cat /run/secrets/pip_token) && \
    pip install --extra-index-url \
    https://token:${PIP_TOKEN}@pypi.example.com/simple \
    -r requirements.txt

# The secret is NOT in any layer
```

```bash
docker build --secret id=pip_token,src=./pip_token.txt -t myapp .

# Verify: secret not in image
docker history myapp --no-trunc
# No trace of the secret value
```

---

## Running as Non-Root User

```dockerfile
# Create and use a non-root user
FROM node:20-alpine

# Create app user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Set ownership
WORKDIR /app
COPY --chown=appuser:appgroup . .
RUN npm ci --only=production

# Switch to non-root user
USER appuser

EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
# Verify the user
docker run --rm myapp id
# uid=1001(appuser) gid=1001(appgroup)
```

---

## Rootless Docker

```bash
# Install rootless Docker
dockerd-rootless-setuptool.sh install

# Set environment variables
export PATH=$HOME/bin:$PATH
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock

# Verify rootless mode
docker info --format '{{.SecurityOptions}}'
# [name=rootless ...]

# Limitations:
# - Cannot use --privileged
# - Cannot use host networking
# - Limited port range (>1024 by default)
# - Some storage drivers not available
# - No AppArmor support

# Enable privileged ports (optional)
sudo setcap cap_net_bind_service=ep ~/bin/rootlesskit
```

---

## CIS Docker Benchmark

```bash
# Run Docker Bench for Security
docker run --rm --net host --pid host --userns host \
  --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /usr/bin/containerd:/usr/bin/containerd:ro \
  -v /usr/bin/runc:/usr/bin/runc:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  docker/docker-bench-security
```

---

## CIS Benchmark - Key Categories

```misc
Section 1: Host Configuration
  1.1 - Ensure a separate partition for containers
  1.2 - Ensure container host is hardened
  1.3 - Ensure Docker is up to date

Section 2: Docker Daemon Configuration
  2.1 - Restrict network traffic between containers
  2.2 - Set logging level to info
  2.3 - Allow Docker to make changes to iptables
  2.4 - Do not use insecure registries
  2.5 - Enable content trust

Section 4: Container Images and Build Files
  4.1 - Ensure images are scanned for vulnerabilities
  4.2 - Create a user for the container
  4.6 - Add HEALTHCHECK instruction

Section 5: Container Runtime
  5.1 - Do not disable AppArmor
  5.2 - Verify SELinux security options
  5.3 - Restrict Linux kernel capabilities
  5.4 - Do not use privileged containers
```

---

## CIS Benchmark - Remediation Examples

```bash
# 2.1 - Restrict inter-container communication
# /etc/docker/daemon.json
{
  "icc": false
}

# 2.5 - Enable content trust
export DOCKER_CONTENT_TRUST=1

# 2.14 - Enable live restore
{
  "live-restore": true
}

# 5.10 - Limit memory for containers
docker run -d --memory=512m --memory-swap=1g myapp

# 5.12 - Mount container rootfs as read only
docker run -d --read-only myapp

# 5.25 - Restrict container from acquiring new privileges
docker run -d --security-opt no-new-privileges:true myapp
```

---

## Dockerfile Security Best Practices

```dockerfile
# 1. Use specific image tags (never :latest in production)
FROM node:20.11.1-alpine3.19

# 2. Verify downloaded files
RUN curl -fsSL https://example.com/app.tar.gz -o /tmp/app.tar.gz && \
    echo "expected_sha256  /tmp/app.tar.gz" | sha256sum -c - && \
    tar xzf /tmp/app.tar.gz -C /opt/ && \
    rm /tmp/app.tar.gz

# 3. Don't store secrets
# Use BuildKit secrets instead of ARG/ENV

# 4. Use COPY instead of ADD
COPY app.tar.gz /opt/   # Explicit, predictable
# ADD can auto-extract and fetch URLs - unexpected behavior

# 5. Run as non-root
USER 1001

# 6. Use read-only filesystem where possible
```

---

## Network Security Hardening

```bash
# Disable inter-container communication
{
  "icc": false
}

# Use internal networks for backend services
docker network create --internal backend-net

# Restrict published ports to localhost
docker run -d -p 127.0.0.1:5432:5432 postgres:16

# Disable userland proxy (use iptables only)
{
  "userland-proxy": false
}

# Use network policies in Swarm
docker network create --driver overlay \
  --opt encrypted \
  secure-overlay
```

---

## Resource Limits as Security

```bash
# Prevent resource exhaustion attacks
docker run -d \
  --memory=512m \
  --memory-swap=512m \
  --cpus=1.0 \
  --pids-limit=100 \
  --ulimit nofile=1024:2048 \
  --ulimit nproc=100:200 \
  --storage-opt size=10G \
  --restart=on-failure:5 \
  myapp

# In daemon.json (defaults for all containers)
{
  "default-ulimits": {
    "nofile": { "Name": "nofile", "Hard": 2048, "Soft": 1024 },
    "nproc": { "Name": "nproc", "Hard": 200, "Soft": 100 }
  }
}
```

---

## Runtime Security Monitoring

```bash
# Falco - runtime security monitoring
docker run -d --name falco \
  --privileged \
  -v /var/run/docker.sock:/host/var/run/docker.sock \
  -v /proc:/host/proc:ro \
  -v /etc:/host/etc:ro \
  falcosecurity/falco

# Falco detects:
# - Shell spawned in container
# - Unexpected outbound connections
# - Sensitive file access
# - Privilege escalation attempts
# - Container escape attempts

# Example Falco alerts:
# WARNING: Shell spawned in container (user=root container=web)
# CRITICAL: Sensitive file opened (file=/etc/shadow container=api)
```

---

## Security Checklist

```misc
Pre-deployment:
  □ Images scanned for vulnerabilities
  □ No secrets in images or environment variables
  □ Non-root user configured
  □ Minimal base image used
  □ Content trust enabled
  □ Dockerfile linted with hadolint

Runtime:
  □ Read-only root filesystem
  □ Capabilities dropped (--cap-drop=ALL + add needed)
  □ No privileged containers
  □ No new privileges (--security-opt no-new-privileges)
  □ Resource limits configured (memory, CPU, PIDs)
  □ Seccomp profile applied
  □ AppArmor/SELinux profile applied

Infrastructure:
  □ Docker daemon TLS enabled
  □ Docker socket not exposed to containers
  □ Inter-container communication restricted
  □ Logging and monitoring enabled
  □ CIS benchmark passing
```

---

## Summary - Docker Security

- Protect the `Docker` daemon socket and use `TLS` authentication
- Drop all capabilities, add back only what is needed
- Apply `seccomp` and `AppArmor` profiles to restrict syscalls
- Enable Docker Content Trust for signed images
- Scan images regularly with `Trivy` or `Docker Scout`
- Run containers as non-root with read-only filesystems
- Set resource limits to prevent denial of service
- Use `CIS` Docker Benchmark to audit your environment
- Consider rootless `Docker` for enhanced security
- Monitor runtime behavior with tools like `Falco`
