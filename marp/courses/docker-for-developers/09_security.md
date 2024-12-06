# Security with Docker

---

## Security Context Overview

![0](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/0.png)

---

## Running as Non-Root

![1](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/1.png)

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

![2](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/2.png)

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

![3](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/3.png)

---

## Security Best Practices

![4](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/4.png)

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

![5](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/5.png)

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

![6](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/6.png)

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

![7](../../../out/mermaid/marp/courses/docker-for-developers/09_security.md/7.png)

---

## Filesystem Security

| Strategy | Implementation | Benefit |
|----------|---------------|----------|
| Read-only root | `--read-only` | Prevent modifications |
| Temporary storage | tmpfs | Secure scratch space |
| Volume permissions | chmod/chown | Access control |
| Mount options | :ro flag | Read-only access |
