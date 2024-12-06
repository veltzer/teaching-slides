# Docker Theory

---

## Container Evolution Timeline

![0](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/0.png)

---

## What is Docker?

- Container technology platform for application development
- Industry standard for containerization
- Ensures consistent environments across all stages
- Based on Linux container technology
- Open-source with enterprise features

---

## Docker Architecture

![1](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/1.png)

---

## Container vs VM Architecture

![2](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/2.png)

---

## Common Docker Commands

| Category | Command | Purpose |
|----------|---------|----------|
| Images | `docker build` | Build an image |
| | `docker pull` | Download image |
| | `docker push` | Upload image |
| Containers | `docker run` | Start container |
| | `docker stop` | Stop container |
| | `docker rm` | Remove container |
| System | `docker info` | Show system info |
| | `docker version` | Show version |

---

## Docker Workflow

![3](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/3.png)

---

## Docker Components

![4](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/4.png)

---

## Resource Management

| Resource | Description | Command |
|----------|-------------|---------|
| CPU | Limit CPU usage | `--cpus`, `--cpu-shares` |
| Memory | Set memory limits | `--memory`, `--memory-swap` |
| Storage | Manage disk space | `--storage-opt` |
| Network | Network settings | `--network`, `--port` |

---

## Container Lifecycle

![5](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/5.png)

---

## Network Types

![6](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/6.png)

---

## Security Model

![7](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/7.png)

---

## Development Best Practices

| Area | Practice | Benefit |
|------|----------|---------|
| Images | Use official base images | Security, reliability |
| Layers | Minimize layers | Smaller images |
| Cache | Optimize build cache | Faster builds |
| Security | Non-root user | Better security |
| Configuration | Use environment variables | Flexibility |

---

## Troubleshooting Flow

![8](../../../out/mermaid/marp/courses/docker-for-developers/00_docker_theory.md/8.png)
