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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <g id="traditional">
    <rect x="50" y="50" width="300" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
    <text x="200" y="30" text-anchor="middle" font-weight="bold">Traditional</text>
    <rect x="60" y="280" width="280" height="60" fill="#666"/>
    <text x="200" y="315" text-anchor="middle" fill="white">Server</text>
    <rect x="60" y="200" width="280" height="70" fill="#888"/>
    <text x="200" y="240" text-anchor="middle" fill="white">Operating System</text>
    <rect x="70" y="100" width="80" height="90" fill="#ea4335"/>
    <text x="110" y="130" text-anchor="middle" fill="white" font-size="12">App A</text>
    <text x="110" y="150" text-anchor="middle" fill="white" font-size="10">Dependencies</text>
    <rect x="160" y="100" width="80" height="90" fill="#fbbc04"/>
    <text x="200" y="130" text-anchor="middle" fill="white" font-size="12">App B</text>
    <text x="200" y="150" text-anchor="middle" fill="white" font-size="10">Dependencies</text>
    <rect x="250" y="100" width="80" height="90" fill="#34a853"/>
    <text x="290" y="130" text-anchor="middle" fill="white" font-size="12">App C</text>
    <text x="290" y="150" text-anchor="middle" fill="white" font-size="10">Dependencies</text>
    <text x="200" y="80" text-anchor="middle" font-size="14" fill="red">Conflicts!</text>
  </g>
  <g id="docker">
    <rect x="450" y="50" width="300" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
    <text x="600" y="30" text-anchor="middle" font-weight="bold">Docker</text>
    <rect x="460" y="280" width="280" height="60" fill="#666"/>
    <text x="600" y="315" text-anchor="middle" fill="white">Server</text>
    <rect x="460" y="200" width="280" height="70" fill="#888"/>
    <text x="600" y="240" text-anchor="middle" fill="white">Operating System</text>
    <rect x="460" y="140" width="280" height="50" fill="#0066cc"/>
    <text x="600" y="170" text-anchor="middle" fill="white">Docker Engine</text>
    <rect x="470" y="70" width="80" height="60" fill="#4285f4" stroke="white" stroke-width="2"/>
    <text x="510" y="105" text-anchor="middle" fill="white" font-size="12">Container A</text>
    <rect x="560" y="70" width="80" height="60" fill="#4285f4" stroke="white" stroke-width="2"/>
    <text x="600" y="105" text-anchor="middle" fill="white" font-size="12">Container B</text>
    <rect x="650" y="70" width="80" height="60" fill="#4285f4" stroke="white" stroke-width="2"/>
    <text x="690" y="105" text-anchor="middle" fill="white" font-size="12">Container C</text>
  </g>
</svg>

---

## Container Benefits

1. **Isolation**: Apps don't interfere
1. **Portability**: Run anywhere
1. **Consistency**: Same everywhere
1. **Efficiency**: Share OS kernel
1. **Speed**: Start in seconds

---

## Docker Architecture

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="350" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Docker Architecture</text>
  <rect x="100" y="80" width="200" height="80" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Docker Client</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="12">docker build</text>
  <text x="200" y="150" text-anchor="middle" fill="white" font-size="12">docker run</text>
  <rect x="400" y="80" width="300" height="120" fill="#34a853" rx="5"/>
  <text x="550" y="110" text-anchor="middle" fill="white" font-weight="bold">Docker Daemon</text>
  <text x="550" y="135" text-anchor="middle" fill="white" font-size="12">Manages Images</text>
  <text x="550" y="155" text-anchor="middle" fill="white" font-size="12">Manages Containers</text>
  <text x="550" y="175" text-anchor="middle" fill="white" font-size="12">Manages Networks</text>
  <rect x="100" y="250" width="150" height="100" fill="#fbbc04" rx="5"/>
  <text x="175" y="280" text-anchor="middle" font-weight="bold">Images</text>
  <text x="175" y="305" text-anchor="middle" font-size="12">Ubuntu</text>
  <text x="175" y="325" text-anchor="middle" font-size="12">Nginx</text>
  <rect x="300" y="250" width="150" height="100" fill="#ea4335" rx="5"/>
  <text x="375" y="280" text-anchor="middle" fill="white" font-weight="bold">Containers</text>
  <text x="375" y="305" text-anchor="middle" fill="white" font-size="12">Running Apps</text>
  <text x="375" y="325" text-anchor="middle" fill="white" font-size="12">Isolated Process</text>
  <rect x="500" y="250" width="200" height="100" fill="#9c27b0" rx="5"/>
  <text x="600" y="280" text-anchor="middle" fill="white" font-weight="bold">Registry</text>
  <text x="600" y="305" text-anchor="middle" fill="white" font-size="12">Docker Hub</text>
  <text x="600" y="325" text-anchor="middle" fill="white" font-size="12">Private Registry</text>
  <path d="M 300 120 L 395 120" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 550 200 L 175 245" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 550 200 L 375 245" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 550 200 L 600 245" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="50" width="400" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Docker Image Layers</text>
  <rect x="250" y="270" width="300" height="50" fill="#666" rx="3"/>
  <text x="400" y="300" text-anchor="middle" fill="white">Base OS (Ubuntu)</text>
  <rect x="250" y="210" width="300" height="50" fill="#888" rx="3"/>
  <text x="400" y="240" text-anchor="middle" fill="white">System Libraries</text>
  <rect x="250" y="150" width="300" height="50" fill="#4285f4" rx="3"/>
  <text x="400" y="180" text-anchor="middle" fill="white">Application Runtime</text>
  <rect x="250" y="90" width="300" height="50" fill="#34a853" rx="3"/>
  <text x="400" y="120" text-anchor="middle" fill="white">Application Code</text>
  <text x="150" y="300" text-anchor="middle" font-size="12">Read-only</text>
  <text x="150" y="240" text-anchor="middle" font-size="12">Read-only</text>
  <text x="150" y="180" text-anchor="middle" font-size="12">Read-only</text>
  <text x="150" y="120" text-anchor="middle" font-size="12">Read-only</text>
  <text x="650" y="180" text-anchor="middle" font-size="14">Shared between</text>
  <text x="650" y="200" text-anchor="middle" font-size="14">containers</text>
</svg>

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

<svg viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
  <circle cx="150" cy="175" r="40" fill="#4285f4"/>
  <text x="150" y="180" text-anchor="middle" fill="white">Created</text>
  <circle cx="300" cy="175" r="40" fill="#34a853"/>
  <text x="300" y="180" text-anchor="middle" fill="white">Running</text>
  <circle cx="450" cy="175" r="40" fill="#fbbc04"/>
  <text x="450" y="180" text-anchor="middle">Paused</text>
  <circle cx="600" cy="175" r="40" fill="#ea4335"/>
  <text x="600" y="180" text-anchor="middle" fill="white">Stopped</text>
  <circle cx="450" cy="280" r="40" fill="#666"/>
  <text x="450" y="285" text-anchor="middle" fill="white">Removed</text>
  <path d="M 190 175 L 260 175" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="225" y="165" text-anchor="middle" font-size="12">start</text>
  <path d="M 340 175 L 410 175" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="375" y="165" text-anchor="middle" font-size="12">pause</text>
  <path d="M 450 135 Q 375 100 300 135" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="375" y="95" text-anchor="middle" font-size="12">unpause</text>
  <path d="M 490 175 L 560 175" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="525" y="165" text-anchor="middle" font-size="12">stop</text>
  <path d="M 600 215 L 490 240" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="545" y="235" text-anchor="middle" font-size="12">remove</text>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Docker Network Types</text>
  <rect x="100" y="80" width="150" height="100" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Bridge</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="11">Default network</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="11">Containers can</text>
  <text x="175" y="170" text-anchor="middle" fill="white" font-size="11">communicate</text>
  <rect x="275" y="80" width="150" height="100" fill="#34a853" rx="5"/>
  <text x="350" y="110" text-anchor="middle" fill="white" font-weight="bold">Host</text>
  <text x="350" y="130" text-anchor="middle" fill="white" font-size="11">No isolation</text>
  <text x="350" y="150" text-anchor="middle" fill="white" font-size="11">Share host</text>
  <text x="350" y="170" text-anchor="middle" fill="white" font-size="11">network</text>
  <rect x="450" y="80" width="150" height="100" fill="#fbbc04" rx="5"/>
  <text x="525" y="110" text-anchor="middle" font-weight="bold">None</text>
  <text x="525" y="130" text-anchor="middle" font-size="11">No networking</text>
  <text x="525" y="150" text-anchor="middle" font-size="11">Complete</text>
  <text x="525" y="170" text-anchor="middle" font-size="11">isolation</text>
  <rect x="625" y="80" width="125" height="100" fill="#ea4335" rx="5"/>
  <text x="687" y="110" text-anchor="middle" fill="white" font-weight="bold">Custom</text>
  <text x="687" y="130" text-anchor="middle" fill="white" font-size="11">User-defined</text>
  <text x="687" y="150" text-anchor="middle" fill="white" font-size="11">bridges</text>
  <rect x="100" y="220" width="650" height="100" fill="#e8f5e9" rx="5"/>
  <text x="425" y="250" text-anchor="middle" font-weight="bold">Container Network</text>
  <circle cx="200" cy="280" r="25" fill="#4285f4"/>
  <text x="200" y="285" text-anchor="middle" fill="white" font-size="12">C1</text>
  <circle cx="300" cy="280" r="25" fill="#4285f4"/>
  <text x="300" y="285" text-anchor="middle" fill="white" font-size="12">C2</text>
  <circle cx="400" cy="280" r="25" fill="#4285f4"/>
  <text x="400" y="285" text-anchor="middle" fill="white" font-size="12">C3</text>
  <line x1="225" y1="280" x2="275" y2="280" stroke="#666" stroke-width="2"/>
  <line x1="325" y1="280" x2="375" y2="280" stroke="#666" stroke-width="2"/>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Docker Storage Types</text>
  <g id="bind">
    <rect x="100" y="80" width="200" height="120" fill="#4285f4" rx="5"/>
    <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Bind Mounts</text>
    <rect x="120" y="130" width="160" height="50" fill="#fff" rx="3"/>
    <text x="200" y="150" text-anchor="middle" font-size="12">Host Path:</text>
    <text x="200" y="170" text-anchor="middle" font-size="11">/host/path:/container/path</text>
  </g>
  <g id="volume">
    <rect x="350" y="80" width="200" height="120" fill="#34a853" rx="5"/>
    <text x="450" y="110" text-anchor="middle" fill="white" font-weight="bold">Docker Volumes</text>
    <rect x="370" y="130" width="160" height="50" fill="#fff" rx="3"/>
    <text x="450" y="150" text-anchor="middle" font-size="12">Managed by Docker</text>
    <text x="450" y="170" text-anchor="middle" font-size="11">volume_name:/path</text>
  </g>
  <g id="tmpfs">
    <rect x="600" y="80" width="140" height="120" fill="#fbbc04" rx="5"/>
    <text x="670" y="110" text-anchor="middle" font-weight="bold">tmpfs</text>
    <rect x="610" y="130" width="120" height="50" fill="#fff" rx="3"/>
    <text x="670" y="150" text-anchor="middle" font-size="12">Memory only</text>
    <text x="670" y="170" text-anchor="middle" font-size="11">Temporary</text>
  </g>
  <rect x="100" y="230" width="640" height="80" fill="#e3f2fd" rx="5"/>
  <text x="420" y="255" text-anchor="middle" font-weight="bold">Container Filesystem</text>
  <text x="420" y="280" text-anchor="middle" font-size="12">Writable layer (ephemeral)</text>
  <text x="420" y="300" text-anchor="middle" font-size="12">Lost when container removed</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="300" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="200" y="30" text-anchor="middle" font-weight="bold">Docker</text>
  <rect x="75" y="150" width="250" height="150" fill="#4285f4" rx="5"/>
  <text x="200" y="180" text-anchor="middle" fill="white">Container Runtime</text>
  <text x="200" y="210" text-anchor="middle" fill="white" font-size="12">• Build images</text>
  <text x="200" y="235" text-anchor="middle" fill="white" font-size="12">• Run containers</text>
  <text x="200" y="260" text-anchor="middle" fill="white" font-size="12">• Manage storage</text>
  <text x="200" y="285" text-anchor="middle" fill="white" font-size="12">• Handle networking</text>
  <rect x="450" y="50" width="300" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="600" y="30" text-anchor="middle" font-weight="bold">Kubernetes</text>
  <rect x="475" y="150" width="250" height="150" fill="#326ce5" rx="5"/>
  <text x="600" y="180" text-anchor="middle" fill="white">Orchestration</text>
  <text x="600" y="210" text-anchor="middle" fill="white" font-size="12">• Schedule containers</text>
  <text x="600" y="235" text-anchor="middle" fill="white" font-size="12">• Scale applications</text>
  <text x="600" y="260" text-anchor="middle" fill="white" font-size="12">• Load balancing</text>
  <text x="600" y="285" text-anchor="middle" fill="white" font-size="12">• Self-healing</text>
  <path d="M 350 225 L 450 225" stroke="#666" stroke-width="3" marker-end="url(#arrowhead)"/>
  <text x="400" y="215" text-anchor="middle" font-size="12">Orchestrates</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

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
