# Dead Containers

---

## Container Lifecycle States

![container_lifecycle_states](/svg/courses/devops/docker-for-developers/06_dead_containers/container_lifecycle_states.svg)

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

![container_exit_codes](/svg/courses/devops/docker-for-developers/06_dead_containers/container_exit_codes.svg)

---

## Viewing Container Logs

![viewing_container_logs](/svg/courses/devops/docker-for-developers/06_dead_containers/viewing_container_logs.svg)

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

![reviving_dead_containers](/svg/courses/devops/docker-for-developers/06_dead_containers/reviving_dead_containers.svg)

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

![debugging_dead_containers](/svg/courses/devops/docker-for-developers/06_dead_containers/debugging_dead_containers.svg)

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

![recovery_strategies](/svg/courses/devops/docker-for-developers/06_dead_containers/recovery_strategies.svg)

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

![container_cleanup](/svg/courses/devops/docker-for-developers/06_dead_containers/container_cleanup.svg)

---

## Best Practices

![best_practices](/svg/courses/devops/docker-for-developers/06_dead_containers/best_practices.svg)
