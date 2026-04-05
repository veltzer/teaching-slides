# Containerization Recap

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---
## What Is a Container?

- A lightweight, standalone, executable package of software
- Includes the application, runtime, libraries, and system tools
- Shares the host OS kernel but is isolated from other containers
- Provides consistent behavior across environments

---
## Containers vs Virtual Machines

<div class="mermaid">
graph TD
    subgraph Virtual Machines
        HW1[Hardware] --> HV[Hypervisor]
        HV --> VM1[VM: Guest OS + App 1]
        HV --> VM2[VM: Guest OS + App 2]
    end
    subgraph Containers
        HW2[Hardware] --> OS[Host OS]
        OS --> CR[Container Runtime]
        CR --> C1[Container: App 1]
        CR --> C2[Container: App 2]
        CR --> C3[Container: App 3]
    end
</div>

---
## Container Advantages

- Start in seconds compared to minutes for VMs
- Use significantly less memory and disk space
- High density: run many containers on a single host
- Portable across any machine with the container runtime
- Immutable: same image in dev, staging, and production

---
## The Docker Ecosystem

- `Docker Engine` - the runtime that builds and runs containers
- `Docker CLI` - command-line tool for interacting with Docker
- `Docker Hub` - public registry for container images
- `Docker Compose` - tool for defining multi-container applications
- `Docker Desktop` - development environment for local machines

---
## Docker Architecture

<div class="mermaid">
graph TD
    CLI[Docker CLI] -->|REST API| D[Docker Daemon]
    D --> B[Image Builder]
    D --> CR[Container Runtime]
    D --> NW[Networking]
    D --> VOL[Volumes]
    CR --> C1[Container 1]
    CR --> C2[Container 2]
    B -->|Pull/Push| REG[Registry]
</div>

---
## Docker Images

- A read-only template used to create containers
- Built from a series of layers stacked on top of each other
- Each layer represents a set of filesystem changes
- Layers are cached and shared across images to save space

---
## Image Layers Visualization

<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="190" width="300" height="40" fill="#BBDEFB" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="215" text-anchor="middle" font-size="12">Base OS Layer (Ubuntu 22.04)</text>
  <rect x="50" y="145" width="300" height="40" fill="#C8E6C9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="170" text-anchor="middle" font-size="12">Runtime Layer (Python 3.11)</text>
  <rect x="50" y="100" width="300" height="40" fill="#FFF9C4" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="125" text-anchor="middle" font-size="12">Dependencies Layer (pip install)</text>
  <rect x="50" y="55" width="300" height="40" fill="#FFCCBC" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="80" text-anchor="middle" font-size="12">Application Layer (COPY app/)</text>
  <rect x="50" y="10" width="300" height="40" fill="#E1BEE7" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="35" text-anchor="middle" font-size="12">Writable Container Layer</text>
</svg>

---
## Basic Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir \
    -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

---
## Essential Docker Commands

```bash
# Build an image
docker build -t myapp:1.0 .

# Run a container
docker run -d -p 8080:8000 myapp:1.0

# List running containers
docker ps

# View logs
docker logs <container-id>

# Stop a container
docker stop <container-id>
```

---
## Docker Compose

- Define and run multi-container applications with a single file
- Uses `YAML` to describe services, networks, and volumes
- Start everything with `docker compose up`
- Ideal for local development environments

---
## Docker Compose Example

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=app
volumes:
  pgdata:
```

---
## Optimizing Images: Why It Matters

- Smaller images build faster and transfer faster
- Fewer packages mean a smaller attack surface
- Efficient layer caching speeds up CI/CD pipelines
- Optimized images reduce storage costs in registries

---
## Use Minimal Base Images

- `alpine` - around 5 MB, musl-based Linux
- `distroless` - contains only the application and runtime
- `slim` variants - stripped-down versions of standard images
- Avoid full OS images like `ubuntu` or `debian` unless necessary

---
## Base Image Comparison

| Base Image | Size | Use Case |
|-----------|------|----------|
| `ubuntu:22.04` | ~77 MB | General purpose |
| `python:3.11` | ~900 MB | Full Python environment |
| `python:3.11-slim` | ~120 MB | Stripped Python |
| `python:3.11-alpine` | ~50 MB | Minimal Python |
| `gcr.io/distroless/python3` | ~50 MB | Production Python |

---
## Multi-Stage Builds

- Use multiple `FROM` statements in a single Dockerfile
- Build stage compiles code and installs dependencies
- Final stage copies only the needed artifacts
- Dramatically reduces the final image size

---
## Multi-Stage Build Example

```dockerfile
# Build stage
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o server .

# Production stage
FROM gcr.io/distroless/static
COPY --from=builder /app/server /server
EXPOSE 8080
CMD ["/server"]
```

---
## Layer Caching Best Practices

- Order instructions from least to most frequently changing
- Copy dependency manifests before source code
- Use `.dockerignore` to exclude unnecessary files
- Combine related `RUN` commands to reduce layers

---
## Layer Caching Example

```dockerfile
# Good: dependencies change less often
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production
COPY . .
CMD ["node", "server.js"]
```

- If only source code changes, `npm ci` layer is cached

---
## The .dockerignore File

```text
.git
.gitignore
node_modules
*.md
Dockerfile
docker-compose.yml
.env
__pycache__
*.pyc
.coverage
tests/
```

- Reduces build context size and prevents sensitive files from entering images

---
## Security Best Practices

- Run containers as a non-root user
- Scan images for vulnerabilities with `Trivy`, `Snyk`, or `Grype`
- Pin base image versions to avoid unexpected changes
- Do not store secrets in images or environment variables at build time
- Use read-only filesystems where possible

---
## Non-Root User Example

```dockerfile
FROM node:20-alpine
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup . .
RUN npm ci --production
USER appuser
EXPOSE 3000
CMD ["node", "server.js"]
```

---
## Health Checks in Dockerfiles

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir \
    -r requirements.txt
HEALTHCHECK --interval=30s \
    --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health \
    || exit 1
EXPOSE 8000
CMD ["python", "app.py"]
```

---
## Container Networking

- Bridge network: default, containers on the same host communicate
- Host network: container shares the host network stack
- Overlay network: containers across multiple hosts communicate
- None: no networking, fully isolated container

---
## Container Networking Diagram

<div class="mermaid">
graph TD
    subgraph Bridge Network
        C1[Container 1] --- BR[Bridge]
        C2[Container 2] --- BR
        C3[Container 3] --- BR
    end
    BR --> HOST[Host Network Interface]
    HOST --> EXT[External Network]
</div>

---
## Volumes and Persistent Storage

- Containers are ephemeral; data is lost when they stop
- Volumes persist data beyond the container lifecycle
- Bind mounts map a host directory into the container
- Named volumes are managed by Docker and are portable

---
## Volume Types

```bash
# Named volume (managed by Docker)
docker run -v mydata:/app/data myapp

# Bind mount (host directory)
docker run -v /host/path:/app/data myapp

# Tmpfs mount (memory only)
docker run --tmpfs /app/tmp myapp
```

---
## Container Image Tagging Strategy

- Use semantic versioning: `myapp:1.2.3`
- Include the git commit SHA: `myapp:abc1234`
- Use `latest` only for development, never in production
- Tag images with the build date for auditability
- Immutable tags prevent accidental overwrites

---
## Private Container Registries

- `Docker Hub` - public and private repositories
- `Amazon ECR` - integrated with AWS services
- `Google Artifact Registry` - integrated with GCP
- `Azure Container Registry` - integrated with Azure
- `Harbor` - open-source self-hosted registry

---
## CI/CD Integration

<div class="mermaid">
graph LR
    CODE[Code Push] --> BUILD[Build Image]
    BUILD --> TEST[Run Tests]
    TEST --> SCAN[Security Scan]
    SCAN --> PUSH[Push to Registry]
    PUSH --> DEPLOY[Deploy to Cluster]
</div>

---
## Production Deployment Checklist

- Use multi-stage builds to minimize image size
- Pin all base image versions
- Run as non-root user
- Define health checks
- Set resource limits (CPU and memory)
- Scan for vulnerabilities before deploying
- Use a private registry with access controls
- Log to `stdout` and `stderr`

---
## Container Resource Limits

```bash
# Limit CPU and memory
docker run \
    --cpus="0.5" \
    --memory="256m" \
    --memory-swap="512m" \
    myapp:1.0
```

- Prevents a single container from consuming all host resources
- Essential for multi-tenant environments

---
## Container Logging Best Practices

- Write all logs to `stdout` and `stderr`
- Use structured logging (`JSON` format) for parsing
- Include request IDs for correlation across services
- Let the platform (Docker, Kubernetes) handle log collection
- Never write logs to files inside the container

---
## Summary

- Containers provide lightweight, portable, and consistent environments
- Docker is the standard tool for building and running containers
- Optimize images using minimal bases, multi-stage builds, and layer caching
- Secure containers by running as non-root and scanning for vulnerabilities
- Use health checks, resource limits, and proper logging in production
- Container registries and CI/CD integration automate the delivery pipeline
