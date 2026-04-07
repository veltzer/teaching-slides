# Starting Out with Docker

---

## Installing Docker

![installing_docker](/svg/courses/devops/docker-for-developers/03_starting_out/installing_docker.svg)

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

![installation_steps_ubuntu](/svg/courses/devops/docker-for-developers/03_starting_out/installation_steps_ubuntu.svg)

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

![running_your_first_container](/svg/courses/devops/docker-for-developers/03_starting_out/running_your_first_container.svg)

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

![docker_concepts_image_vs_container](/svg/courses/devops/docker-for-developers/03_starting_out/docker_concepts_image_vs_container.svg)

---

## Image Basics

![image_basics](/svg/courses/devops/docker-for-developers/03_starting_out/image_basics.svg)

---

## Container States

![container_states](/svg/courses/devops/docker-for-developers/03_starting_out/container_states.svg)

---

## Docker Hub

![docker_hub](/svg/courses/devops/docker-for-developers/03_starting_out/docker_hub.svg)

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

![basic_container_operations](/svg/courses/devops/docker-for-developers/03_starting_out/basic_container_operations.svg)

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

![best_practices_for_beginners](/svg/courses/devops/docker-for-developers/03_starting_out/best_practices_for_beginners.svg)
