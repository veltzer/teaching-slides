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
# Docker and Volumes

---

## Why Data Volumes?

![why_data_volumes](svg/courses/devops/docker-for-developers/09_volumes/why_data_volumes.svg)

---

## Types of Data Volumes

![types_of_data_volumes](svg/courses/devops/docker-for-developers/09_volumes/types_of_data_volumes.svg)

---

## Volume Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `docker volume create` | Create new volume | `docker volume create mydata` |
| `docker volume ls` | List volumes | `docker volume ls` |
| `docker volume inspect` | Volume details | `docker volume inspect mydata` |
| `docker volume rm` | Remove volume | `docker volume rm mydata` |

---

## Bind Mounts vs Named Volumes

| Feature | Bind Mounts | Named Volumes |
|---------|-------------|---------------|
| Location | Host-specified | Docker-managed |
| Portability | Less portable | More portable |
| Backup | Direct access | Docker commands |
| Performance | Host dependent | Optimized |
| Security | Host exposure | Better isolation |

---

## Working with Volumes

![working_with_volumes](svg/courses/devops/docker-for-developers/09_volumes/working_with_volumes.svg)

---

## Volume Backup Strategies

![volume_backup_strategies](svg/courses/devops/docker-for-developers/09_volumes/volume_backup_strategies.svg)

---

## Volume Drivers

| Driver | Purpose | Use Case |
|--------|---------|----------|
| local | Local storage | Single-host deployment |
| nfs | Network storage | Multi-host access |
| cifs | Windows shares | Windows integration |
| rexray | Cloud storage | Cloud deployment |

---

## Best Practices

![best_practices](svg/courses/devops/docker-for-developers/09_volumes/best_practices.svg)

---

## Volume Lifecycle

![volume_lifecycle](svg/courses/devops/docker-for-developers/09_volumes/volume_lifecycle.svg)

---

## Mounting Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `-v name:/path` | Named volume | `-v mydata:/app/data` |
| `-v /host:/container` | Bind mount | `-v /data:/app/data` |
| `--mount type=volume` | Mount flag | `--mount source=mydata,target=/app/data` |

---

## Data Migration

![data_migration](svg/courses/devops/docker-for-developers/09_volumes/data_migration.svg)

---

## Volume Security

| Consideration | Solution | Implementation |
|---------------|----------|----------------|
| Access Control | File permissions | `chmod`, `chown` |
| Mount options | Read-only mounts | `:ro` flag |
| SELinux | Labels | `z` or `Z` options |
| Isolation | Volume drivers | Network isolation |

---

## Common Volume Patterns

![common_volume_patterns](svg/courses/devops/docker-for-developers/09_volumes/common_volume_patterns.svg)

---

## Performance Optimization

| Strategy | Implementation | Benefit |
|----------|---------------|---------|
| Mount caching | `:cached` flag | Better read performance |
| Delegation | `:delegated` flag | Better write performance |
| Volume plugins | Storage drivers | Optimized I/O |
| tmpfs | Memory storage | Fastest access |
