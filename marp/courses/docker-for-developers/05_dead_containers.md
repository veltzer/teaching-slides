# Dead Containers

---

## Container Lifecycle States

![0](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/0.png)

---

## How to See Dead Containers

| Command | Purpose | Example |
|---------|---------|---------|
| `docker ps -a` | List all containers | Shows running and stopped |
| `docker ps -f status=exited` | Filter by status | Shows only exited containers |
| `docker ps -q -f status=dead` | List dead container IDs | For scripting use |
| `docker inspect` | Detailed container info | Full configuration and state |

---

## Container Exit Codes

![1](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/1.png)

---

## Viewing Container Logs

![2](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/2.png)

---

## Log Access Commands

| Command | Purpose | Options |
|---------|---------|---------|
| `docker logs <container>` | View logs | Basic log output |
| `docker logs -f <container>` | Follow logs | Real-time monitoring |
| `docker logs --tail 100` | Last N lines | Limited history |
| `docker logs --since 1h` | Time-based | Recent logs |

---

## Reviving Dead Containers

![3](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/3.png)

---

## Container Restart Policies

| Policy | Description | Use Case |
|--------|-------------|----------|
| no | Never restart | Short-lived tasks |
| on-failure | Restart on error | Background services |
| unless-stopped | Always restart except manual stop | Persistent services |
| always | Always restart | Critical services |

---

## Debugging Dead Containers

![4](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/4.png)

---

## Resource Monitoring

| Command | Information | Use |
|---------|-------------|-----|
| `docker stats` | Resource usage | Real-time monitoring |
| `docker events` | Container events | Event tracking |
| `docker top` | Running processes | Process inspection |
| `docker inspect` | Configuration | Detailed inspection |

---

## Recovery Strategies

![5](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/5.png)

---

## Common Death Causes

| Cause | Symptoms | Solution |
|-------|----------|----------|
| OOM Kill | Exit 137 | Increase memory limit |
| Application Crash | Non-zero exit | Fix application code |
| Dependency Failure | Connection errors | Check dependencies |
| Permission Issues | Access denied | Fix permissions |

---

## Container Cleanup

![6](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/6.png)

---

## Best Practices

![7](../../../out/mermaid/marp/courses/docker-for-developers/05_dead_containers.md/7.png)
