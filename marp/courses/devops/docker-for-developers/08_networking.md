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
# Networking with Docker

---

## Docker Network Types

![docker_network_types](svg/courses/devops/docker-for-developers/08_networking/docker_network_types.svg)

---

## Opening Ports

![opening_ports](svg/courses/devops/docker-for-developers/08_networking/opening_ports.svg)

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

![container_communication](svg/courses/devops/docker-for-developers/08_networking/container_communication.svg)

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

![dns_in_docker](svg/courses/devops/docker-for-developers/08_networking/dns_in_docker.svg)

---

## Network Security

![network_security](svg/courses/devops/docker-for-developers/08_networking/network_security.svg)

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

![custom_networks](svg/courses/devops/docker-for-developers/08_networking/custom_networks.svg)

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

![network_management](svg/courses/devops/docker-for-developers/08_networking/network_management.svg)

---

## Best Practices

![best_practices](svg/courses/devops/docker-for-developers/08_networking/best_practices.svg)

---

## Common Network Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Frontend-Backend | Separated networks | Web applications |
| Load Balancer | Port distribution | Scaled services |
| Service Discovery | Automatic discovery | Microservices |
| Network Isolation | Security separation | Multi-tenant apps |
