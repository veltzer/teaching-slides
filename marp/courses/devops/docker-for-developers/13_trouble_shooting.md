# Troubleshooting and Debugging

---

## Common Issues and Solutions

![common_issues_and_solutions](/svg/courses/devops/docker-for-developers/13_trouble_shooting/common_issues_and_solutions.svg)

---

## Docker Inspect Deep Dive

| Section | Information | Usage |
|---------|-------------|-------|
| Config | Container configuration | Check environment, cmd |
| State | Current state | Health, status, pid |
| NetworkSettings | Network configuration | IP, ports, networks |
| Mounts | Volume information | Storage configuration |

---

## Remote Debugging Techniques

![remote_debugging_techniques](/svg/courses/devops/docker-for-developers/13_trouble_shooting/remote_debugging_techniques.svg)

---

## Health Checks Implementation

![health_checks_implementation](/svg/courses/devops/docker-for-developers/13_trouble_shooting/health_checks_implementation.svg)

---

## Debug Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `docker logs` | View output | `docker logs -f container` |
| `docker exec` | Run commands | `docker exec -it container bash` |
| `docker inspect` | Check config | `docker inspect container` |
| `docker stats` | Monitor resources | `docker stats container` |

---

## Diagnostic Process

![diagnostic_process](/svg/courses/devops/docker-for-developers/13_trouble_shooting/diagnostic_process.svg)

---

## Common Error Messages

| Error | Possible Cause | Solution |
|-------|---------------|----------|
| Cannot connect to daemon | Docker not running | Start Docker service |
| Port already allocated | Port conflict | Change port mapping |
| OOM Killed | Out of memory | Increase memory limit |
| Image pull failed | Network/auth issue | Check credentials/network |

---

## Resource Monitoring

![resource_monitoring](/svg/courses/devops/docker-for-developers/13_trouble_shooting/resource_monitoring.svg)

---

## Network Debugging

| Tool | Purpose | Example |
|------|---------|---------|
| ping | Connectivity | `docker exec container ping host` |
| netstat | Port status | `docker exec container netstat -tulpn` |
| curl | HTTP testing | `docker exec container curl service` |
| dig | DNS lookup | `docker exec container dig domain` |

---

## Log Analysis

![log_analysis](/svg/courses/devops/docker-for-developers/13_trouble_shooting/log_analysis.svg)

---

## Performance Investigation

| Area | Check | Tool |
|------|-------|------|
| CPU | Usage patterns | top, stats |
| Memory | Memory consumption | stats, inspect |
| IO | Disk activity | iotop |
| Network | Traffic patterns | nethogs |

---

## Debug Mode Options

![debug_mode_options](/svg/courses/devops/docker-for-developers/13_trouble_shooting/debug_mode_options.svg)

---

## Container Recovery

| State | Action | Command |
|-------|--------|---------|
| Stopped | Start | `docker start container` |
| Unresponsive | Restart | `docker restart container` |
| Broken | Remove/Recreate | `docker rm; docker run` |
| Stuck | Force remove | `docker rm -f container` |

---

## Best Debugging Practices

![best_debugging_practices](/svg/courses/devops/docker-for-developers/13_trouble_shooting/best_debugging_practices.svg)
