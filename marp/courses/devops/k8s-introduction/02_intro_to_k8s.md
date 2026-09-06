---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - infrastructure:orchestration
  - practices:devops
  - tools:docker
level: beginner
category: devops
audience:
  - audiences:developers
  - audiences:devops
  - audiences:sysadmins

---

# Docker Fundamentals

---

## What is Docker?

1. Container runtime platform
1. Package applications with dependencies
1. Run anywhere consistently
1. Lightweight virtualization
1. Industry standard for containers

---

## Why Docker First?

1. Kubernetes orchestrates containers
1. Docker creates those containers
1. Understanding Docker is essential
1. Most common container runtime
1. Foundation for orchestration

---

## Docker vs Traditional Deployment

![docker_vs_traditional_deployment](svg/courses/devops/k8s-introduction/02_intro_to_k8s/docker_vs_traditional_deployment.svg)

---

## Container Benefits

1. **Isolation**: Apps don't interfere
1. **Portability**: Run anywhere
1. **Consistency**: Same everywhere
1. **Efficiency**: Share OS kernel
1. **Speed**: Start in seconds

---

## Docker Architecture

![docker_architecture](svg/courses/devops/k8s-introduction/02_intro_to_k8s/docker_architecture.svg)

---

## Key Docker Components

1. **Docker Client**: CLI interface
1. **Docker Daemon**: Background service
1. **Docker Images**: Read-only templates
1. **Docker Containers**: Running instances
1. **Docker Registry**: Image storage

---

## Docker Images

1. Read-only templates
1. Contains application code
1. Includes dependencies
1. Built in layers
1. Shareable and reusable

---

## Image Layers

![image_layers](svg/courses/devops/k8s-introduction/02_intro_to_k8s/image_layers.svg)

---

## Container vs Image

1. **Image**: Blueprint or template
1. **Container**: Running instance
1. **Image**: Read-only
1. **Container**: Read-write layer on top
1. **Image**: Stored in registry
1. **Container**: Runs on host

---

## Docker Installation

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install ca-certificates curl

# Add Docker GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

# Add repository
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

---

## Complete Installation

```bash
# Update package index again
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce docker-ce-cli \
  containerd.io docker-buildx-plugin \
  docker-compose-plugin

# Verify installation
sudo docker run hello-world
```

---

## Post-Installation Setup

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify without sudo
docker run hello-world

# Enable Docker on boot
sudo systemctl enable docker
```

---

## Basic Docker Commands

```bash
# Check version
docker --version

# System information
docker info

# List running containers
docker ps

# List all containers
docker ps -a

# List images
docker images
```

---

## Running First Container

```bash
# Run Ubuntu container
docker run ubuntu echo "Hello Docker"

# Run interactively
docker run -it ubuntu bash

# Run in background
docker run -d nginx

# Run with port mapping
docker run -d -p 8080:80 nginx
```

---

## Container Lifecycle

![container_lifecycle](svg/courses/devops/k8s-introduction/02_intro_to_k8s/container_lifecycle.svg)

---

## Managing Containers

```bash
# Start container
docker start container_id

# Stop container
docker stop container_id

# Restart container
docker restart container_id

# Pause container
docker pause container_id

# Remove container
docker rm container_id
```

---

## Docker Images Commands

```bash
# Pull image from registry
docker pull nginx:latest

# List images
docker images

# Remove image
docker rmi nginx:latest

# Tag image
docker tag nginx:latest mynginx:v1

# Search images
docker search ubuntu
```

---

## Dockerfile Basics

```dockerfile
# Base image
FROM ubuntu:22.04

# Metadata
LABEL maintainer="you@example.com"

# Run commands
RUN apt-get update && apt-get install -y nginx

# Copy files
COPY index.html /var/www/html/

# Expose port
EXPOSE 80

# Default command
CMD ["nginx", "-g", "daemon off;"]
```

---

## Dockerfile Instructions

1. **FROM**: Base image
1. **RUN**: Execute commands
1. **COPY**: Copy files from host
1. **ADD**: Copy and extract archives
1. **WORKDIR**: Set working directory
1. **ENV**: Environment variables
1. **EXPOSE**: Document ports
1. **CMD**: Default command
1. **ENTRYPOINT**: Main executable

---

## Building Images

```bash
# Build image from Dockerfile
docker build -t myapp:v1 .

# Build with different file
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build args
docker build --build-arg VERSION=1.0 -t myapp:v1 .

# View build history
docker history myapp:v1
```

---

## Multi-stage Builds

```dockerfile
# Build stage
FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Runtime stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

---

## Container Networking

![container_networking](svg/courses/devops/k8s-introduction/02_intro_to_k8s/container_networking.svg)

---

## Network Commands

```bash
# List networks
docker network ls

# Create network
docker network create mynetwork

# Inspect network
docker network inspect bridge

# Connect container
docker network connect mynetwork container_id

# Disconnect container
docker network disconnect mynetwork container_id
```

---

## Port Mapping

```bash
# Map port 8080 to container port 80
docker run -d -p 8080:80 nginx

# Map to specific IP
docker run -d -p 127.0.0.1:8080:80 nginx

# Map random port
docker run -d -P nginx

# Multiple ports
docker run -d -p 8080:80 -p 8443:443 nginx
```

---

## Docker Volumes

![docker_volumes](svg/courses/devops/k8s-introduction/02_intro_to_k8s/docker_volumes.svg)

---

## Volume Commands

```bash
# Create volume
docker volume create myvolume

# List volumes
docker volume ls

# Inspect volume
docker volume inspect myvolume

# Remove volume
docker volume rm myvolume

# Remove unused volumes
docker volume prune
```

---

## Using Volumes

```bash
# Named volume
docker run -d -v myvolume:/data nginx

# Bind mount
docker run -d -v /host/path:/container/path nginx

# Read-only mount
docker run -d -v /host/path:/container/path:ro nginx

# tmpfs mount
docker run -d --tmpfs /tmp nginx
```

---

## Container Logs

```bash
# View logs
docker logs container_id

# Follow logs
docker logs -f container_id

# Show timestamps
docker logs -t container_id

# Tail logs
docker logs --tail 50 container_id

# Since time
docker logs --since 2h container_id
```

---

## Executing Commands

```bash
# Execute command in running container
docker exec container_id ls -la

# Interactive shell
docker exec -it container_id bash

# As different user
docker exec -u www-data container_id whoami

# With environment variable
docker exec -e MY_VAR=value container_id env
```

---

## Container Inspection

```bash
# Inspect container
docker inspect container_id

# Format output
docker inspect -f '{{.State.Status}}' container_id

# Container IP
docker inspect -f \
  '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  container_id

# Environment variables
docker inspect -f '{{.Config.Env}}' container_id
```

---

## Resource Limits

```bash
# Memory limit
docker run -d --memory="512m" nginx

# CPU limit
docker run -d --cpus="1.5" nginx

# Both limits
docker run -d --memory="1g" --cpus="2" nginx

# Memory and swap
docker run -d --memory="1g" --memory-swap="2g" nginx
```

---

## Docker Compose Preview

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html

  database:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

---

## Container Best Practices

1. **One process per container**
1. **Use official base images**
1. **Minimize layers**
1. **Don't run as root**
1. **Use .dockerignore**

---

## Image Best Practices

1. **Use specific tags, not latest**
1. **Order Dockerfile efficiently**
1. **Remove unnecessary files**
1. **Use multi-stage builds**
1. **Scan for vulnerabilities**

---

## Security Considerations

1. **Never store secrets in images**
1. **Use read-only filesystems**
1. **Limit container capabilities**
1. **Use security scanning**
1. **Update base images regularly**

---

## Docker Registry

```bash
# Login to Docker Hub
docker login

# Push image
docker push username/myapp:v1

# Pull image
docker pull username/myapp:v1

# Logout
docker logout
```

---

## Private Registry

```bash
# Run local registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for local registry
docker tag myapp:v1 localhost:5000/myapp:v1

# Push to local registry
docker push localhost:5000/myapp:v1

# Pull from local registry
docker pull localhost:5000/myapp:v1
```

---

## Cleanup Commands

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune -a
```

---

## Docker and Kubernetes

![docker_and_kubernetes](svg/courses/devops/k8s-introduction/02_intro_to_k8s/docker_and_kubernetes.svg)

---

## Kubernetes Architecture Overview

![k8s_architecture](svg/courses/devops/k8s-introduction/02_intro_to_k8s/k8s_architecture.svg)

---

## Troubleshooting Containers

```bash
# Check container status
docker ps -a

# Check logs for errors
docker logs container_id

# Inspect configuration
docker inspect container_id

# Check resource usage
docker stats container_id

# Debug with shell
docker exec -it container_id /bin/sh
```

---

## Common Docker Issues

1. **Container exits immediately**: Check CMD/ENTRYPOINT
1. **Cannot connect to container**: Verify port mapping
1. **Permission denied**: Check file ownership
1. **Out of space**: Clean unused resources
1. **Slow builds**: Optimize Dockerfile layers

---

## Docker vs Processes

1. **Process**: Runs directly on host OS
1. **Container**: Isolated process with own filesystem
1. **Process**: Shares host resources directly
1. **Container**: Resource limits enforced
1. **Process**: No portability guarantee
1. **Container**: Portable across platforms

---

## Summary

1. Docker packages applications in containers
1. Containers provide isolation and portability
1. Images are templates for containers
1. Dockerfile defines how to build images
1. Docker is foundation for Kubernetes
