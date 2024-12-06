# Networking with Docker

---

## Docker Network Types

![0](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/0.png)

---

## Opening Ports

![1](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/1.png)

---

## Port Mapping Syntax

| Command | Description | Example |
|---------|-------------|---------|
| `-p hostPort:containerPort` | Specific port mapping | `-p 8080:80` |
| `-p IP:hostPort:containerPort` | Interface specific | `-p 127.0.0.1:8080:80` |
| `-p containerPort` | Random host port | `-p 80` |
| `-P` | All exposed ports | `-P` |

---

## Network Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `docker network create` | Create network | `docker network create mynet` |
| `docker network connect` | Connect container | `docker network connect mynet cont1` |
| `docker network ls` | List networks | `docker network ls` |
| `docker network inspect` | Network details | `docker network inspect bridge` |

---

## Container Communication

![2](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/2.png)

---

## Network Drivers

| Driver | Use Case | Features |
|--------|----------|----------|
| bridge | Default networking | Container isolation |
| host | Performance | Direct host access |
| none | Security | No network access |
| overlay | Multi-host | Swarm networking |
| macvlan | Physical network | Direct network access |

---

## DNS in Docker

![3](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/3.png)

---

## Network Security

![4](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/4.png)

---

## Network Troubleshooting

| Issue | Command | Purpose |
|-------|---------|---------|
| Connectivity | `docker exec cont1 ping cont2` | Test connection |
| Port Mapping | `docker port container` | Check port mappings |
| Network Config | `docker network inspect` | View network details |
| DNS Resolution | `docker exec cont1 nslookup cont2` | Test DNS |

---

## Custom Networks

![5](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/5.png)

---

## Network Creation Options

| Option | Purpose | Example |
|--------|---------|---------|
| `--driver` | Set network driver | `--driver bridge` |
| `--subnet` | Define subnet | `--subnet 172.18.0.0/16` |
| `--gateway` | Set gateway | `--gateway 172.18.0.1` |
| `--ip-range` | Set IP range | `--ip-range 172.18.0.0/24` |

---

## Network Management

![6](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/6.png)

---

## Best Practices

![7](../../../out/mermaid/marp/courses/docker-for-developers/07_networking.md/7.png)

---

## Common Network Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Frontend-Backend | Separated networks | Web applications |
| Load Balancer | Port distribution | Scaled services |
| Service Discovery | Automatic discovery | Microservices |
| Network Isolation | Security separation | Multi-tenant apps |
