---
tags:
  - tools:docker
  - infrastructure:containers
  - practices:devops
  - networking:networking
level: intermediate
category: devops
audience:
  - audiences:developers

---

# Security with Docker

---

## Security Context Overview

![security_context_overview](svg/courses/devops/docker-for-developers/10_security/security_context_overview.svg)

---

## Running as Non-Root

![running_as_non_root](svg/courses/devops/docker-for-developers/10_security/running_as_non_root.svg)

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

![linux_capabilities](svg/courses/devops/docker-for-developers/10_security/linux_capabilities.svg)

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

![tuning_capabilities](svg/courses/devops/docker-for-developers/10_security/tuning_capabilities.svg)

---

## Security Best Practices

![security_best_practices](svg/courses/devops/docker-for-developers/10_security/security_best_practices.svg)

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

![security_scanning](svg/courses/devops/docker-for-developers/10_security/security_scanning.svg)

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

![access_control](svg/courses/devops/docker-for-developers/10_security/access_control.svg)

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

![network_security](svg/courses/devops/docker-for-developers/10_security/network_security.svg)

---

## Filesystem Security

| Strategy | Implementation | Benefit |
|----------|---------------|----------|
| Read-only root | `--read-only` | Prevent modifications |
| Temporary storage | tmpfs | Secure scratch space |
| Volume permissions | chmod/chown | Access control |
| Mount options | :ro flag | Read-only access |
