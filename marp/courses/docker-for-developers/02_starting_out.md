# Starting Out with Docker

---

## Installing Docker

![0](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/0.png)

---

## System Requirements

| Component | Linux | Windows | macOS |
|-----------|--------|----------|--------|
| OS Version | Ubuntu 22.04+ | Windows 10 Pro+ | macOS 10.15+ |
| Memory | 4GB minimum | 4GB minimum | 4GB minimum |
| CPU | 2 cores | 2 cores, Hyper-V | 2 cores |
| Disk Space | 20GB | 20GB | 20GB |

---

## Installation Steps: Ubuntu

![1](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/1.png)

---

## Verifying Installation

| Command | Purpose | Expected Output |
|---------|---------|----------------|
| `docker --version` | Check Docker version | Docker version X.X.X |
| `docker info` | System information | Docker system info |
| `docker run hello-world` | Test installation | Hello from Docker! |
| `docker ps` | List containers | Empty list or running containers |

---

## Running Your First Container

![2](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/2.png)

---

## Basic Docker Commands

| Command | Usage | Example |
|---------|--------|---------|
| `pull` | Download image | `docker pull ubuntu` |
| `run` | Run container | `docker run nginx` |
| `ps` | List containers | `docker ps -a` |
| `images` | List images | `docker images` |
| `stop` | Stop container | `docker stop container_id` |

---

## Docker Concepts: Image vs Container

![3](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/3.png)

---

## Image Basics

![4](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/4.png)

---

## Container States

![5](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/5.png)

---

## Docker Hub

![6](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/6.png)

---

## Image Naming Convention

| Component | Example | Description |
|-----------|---------|-------------|
| Registry | docker.io | Image registry host |
| Repository | nginx | Image name |
| Tag | latest | Image version |
| Full Name | docker.io/nginx:latest | Complete image reference |

---

## Basic Container Operations

![7](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/7.png)

---

## Common Networking Options

| Option | Usage | Example |
|--------|--------|---------|
| `-p` | Port mapping | `-p 8080:80` |
| `--network` | Network type | `--network bridge` |
| `-h` | Hostname | `-h mycontainer` |
| `--dns` | DNS servers | `--dns 8.8.8.8` |

---

## Best Practices for Beginners

![8](../../../out/mermaid/marp/courses/docker-for-developers/02_starting_out.md/8.png)
