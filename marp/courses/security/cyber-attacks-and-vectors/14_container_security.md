# Container Security Issues

---
## Security Risks with Containers
- Kernel Exploits
    - Containers share the host kernel
    - Vulnerability in the kernel can compromise all containers
- Privilege Escalation
    - Container runtime can be exploited to gain root access
- Insecure Configurations
    - Containers may run with unnecessary privileges or open ports
- Image Vulnerabilities
    - Base images or application images may contain vulnerabilities

---

## Container Attack Surface

![container_attack_surface](svg/courses/security/cyber-attacks-and-vectors/14_container_security/container_attack_surface.svg)

---

## Container Escape: Docker Socket

```bash
# If the Docker socket is mounted inside a container,
# an attacker can escape to the host

# Check if Docker socket is accessible
ls -la /var/run/docker.sock

# If accessible, attacker can create a privileged container
# that mounts the host filesystem:
docker run -v /:/hostfs -it alpine /bin/sh
# Now inside new container with host filesystem at /hostfs
chroot /hostfs
# Attacker is now effectively root on the host!

# NEVER mount Docker socket in production containers!
# Dockerfile anti-pattern:
# docker run -v /var/run/docker.sock:/var/run/docker.sock myapp
```

---

## Container Escape: Privileged Mode

```bash
# Privileged containers have full access to host devices
# docker run --privileged -it alpine /bin/sh

# Inside privileged container - escape to host:
# Mount host filesystem
mkdir /hostfs
mount /dev/sda1 /hostfs
chroot /hostfs

# Or access host network namespace
nsenter --target 1 --mount --uts --ipc --net --pid

# NEVER use --privileged in production!
# Use specific capabilities instead:
# docker run --cap-add NET_ADMIN myapp
```

---

## Vulnerable Dockerfile vs Secure Dockerfile

```dockerfile
# VULNERABLE Dockerfile
FROM ubuntu:latest          # Mutable tag, large image
RUN apt-get update && apt-get install -y curl wget vim
COPY . /app                 # May include .env, secrets
RUN pip install -r requirements.txt
USER root                   # Running as root!
EXPOSE 22 80 443 8080       # Too many ports
CMD ["python", "app.py"]
```

```dockerfile
# SECURE Dockerfile
FROM python:3.12-slim@sha256:abc123...  # Pinned digest
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser app.py .
USER appuser                # Non-root user
EXPOSE 8080                 # Only needed port
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/health
CMD ["python", "app.py"]
```

---

## Image Scanning

```bash
# Trivy - comprehensive container scanner
trivy image myapp:latest
# Scans for: OS vulnerabilities, application dependencies,
# misconfigurations, secrets

# Grype - vulnerability scanner
grype myapp:latest

# Docker Scout (built into Docker)
docker scout cves myapp:latest

# Scan for secrets in images
# Using trufflehog:
trufflehog docker --image myapp:latest

# Scan Dockerfile for misconfigurations
hadolint Dockerfile
# Checks for: running as root, using latest tag,
# missing USER instruction, etc.
```

| Tool          | Type                    | Focus                    |
|---------------|-------------------------|--------------------------|
| Trivy         | Multi-purpose scanner   | CVEs, secrets, IaC       |
| Grype         | Vulnerability scanner   | CVEs in images           |
| Hadolint      | Dockerfile linter       | Best practices           |
| Dockle        | Image linter            | CIS Benchmark compliance |
| Falco         | Runtime security        | Behavioral monitoring    |

---

## Kubernetes Security Misconfigurations

```yaml
# VULNERABLE Pod spec
apiVersion: v1
kind: Pod
metadata:
  name: vulnerable-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      privileged: true        # Full host access!
      runAsUser: 0             # Running as root!
    volumeMounts:
    - name: host-root
      mountPath: /hostfs
  volumes:
  - name: host-root
    hostPath:
      path: /                  # Host root mounted!
```

```yaml
# SECURE Pod spec
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp@sha256:abc123  # Pinned image digest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
    resources:
      limits:
        cpu: "500m"
        memory: "256Mi"
```

---

## Runtime Security with Falco

```yaml
# Falco rule to detect container escape attempts
- rule: Container Escape via mount
  desc: Detect mount commands inside containers
  condition: >
    spawned_process and container and
    proc.name = mount
  output: >
    Mount command run in container
    (user=%user.name command=%proc.cmdline
     container=%container.name image=%container.image.repository)
  priority: WARNING

- rule: Shell spawned in container
  desc: Detect interactive shell in production container
  condition: >
    spawned_process and container and
    proc.name in (bash, sh, zsh) and
    container.image.repository != "debug-tools"
  output: >
    Shell spawned in container
    (user=%user.name container=%container.name)
  priority: ALERT
```

---

## Mitigating Container Security Risks
- Use Hardened Operating System
    - Deploy containers on a minimal, hardened OS
- Implement Least Privilege
    - Run containers with minimal required privileges
- Secure Container Runtime
    - Keep container runtime (e.g., Docker) up-to-date
    - Use secure configurations and limit access
- Image Scanning and Management
    - Scan images for vulnerabilities, use trusted sources
    - Implement image lifecycle management

---
## Additional Security Controls

- Network Segmentation
    - Isolate containers using virtual networks or firewalls
- Logging and Monitoring
    - Implement centralized logging and monitoring
- Secure Orchestration
    - Use secure orchestration platforms (e.g., Kubernetes)
    - Enable role-based access control and audit trails
- Regular Updates and Patching
    - Keep containers, images, and host OS up-to-date

---

## Container Network Security

```bash
# Docker: Create isolated networks
docker network create --internal backend-net
# --internal prevents external access

# Run containers on isolated network
docker run --network backend-net --name db postgres
docker run --network backend-net --name app myapp

# Kubernetes Network Policy: deny all, allow specific
# networkpolicy.yaml:
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app-to-db
spec:
  podSelector:
    matchLabels:
      app: database
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - port: 5432
```

---
## Key Takeaways

- Containers introduce new security risks
- Implement security best practices:
    - Hardened OS, least privilege, secure runtime
    - Image scanning, network segmentation
    - Logging, monitoring, and regular updates
- Adopt a comprehensive container security strategy
- Stay vigilant and continuously improve security posture

---

## Exercise: Container Security Audit

1. Pull a popular base image and scan with Trivy
1. Write a deliberately vulnerable Dockerfile and fix it using hadolint
1. Demonstrate Docker socket escape in a test environment
1. Create a non-root container and verify it cannot escalate
1. Set up Falco to monitor runtime container behavior
1. Create Kubernetes NetworkPolicy to restrict pod communication
1. Build a CI/CD pipeline that blocks deployment of vulnerable images
