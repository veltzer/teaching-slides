# Docker and Volumes

---

## Why Data Volumes?

![0](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/0.png)

---

## Types of Data Volumes

![1](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/1.png)

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

![2](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/2.png)

---

## Volume Backup Strategies

![3](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/3.png)

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

![4](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/4.png)

---

## Volume Lifecycle

![5](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/5.png)

---

## Mounting Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `-v name:/path` | Named volume | `-v mydata:/app/data` |
| `-v /host:/container` | Bind mount | `-v /data:/app/data` |
| `--mount type=volume` | Mount flag | `--mount source=mydata,target=/app/data` |

---

## Data Migration

![6](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/6.png)

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

![7](../../../out/mermaid/marp/courses/docker-for-developers/08_volumes.md/7.png)

---

## Performance Optimization

| Strategy | Implementation | Benefit |
|----------|---------------|---------|
| Mount caching | `:cached` flag | Better read performance |
| Delegation | `:delegated` flag | Better write performance |
| Volume plugins | Storage drivers | Optimized I/O |
| tmpfs | Memory storage | Fastest access |
