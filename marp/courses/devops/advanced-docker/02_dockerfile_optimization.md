# Advanced Dockerfile Techniques and Image Optimization

Building production-grade container images

---

## Agenda

- Multi-stage builds
- `BuildKit` features and optimizations
- Minimal base images
- Layer caching strategies
- Build arguments and secrets
- `Dockerfile` best practices
- Image analysis and optimization tools

---

## Multi-Stage Builds - Why?

**Problem:** Build tools inflate image size

```dockerfile
# BAD: Single stage - 900MB+ image
FROM golang:1.22
WORKDIR /app
COPY . .
RUN go build -o myapp
CMD ["./myapp"]
```

**Solution:** Separate build and runtime stages

```dockerfile
# GOOD: Multi-stage - ~15MB image
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o myapp

FROM alpine:3.19
COPY --from=builder /app/myapp /usr/local/bin/
CMD ["myapp"]
```

---

## Multi-Stage Build - Real Example

```dockerfile
# Stage 1: Build dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build application
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production image
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

---

## Multi-Stage - Copying from External Images

```dockerfile
# Copy from a specific external image
FROM alpine:3.19

# Copy a static binary from another image
COPY --from=busybox:uclibc /bin/busybox /bin/busybox

# Copy certificates for HTTPS
COPY --from=alpine:3.19 /etc/ssl/certs/ca-certificates.crt \
  /etc/ssl/certs/

# Copy timezone data
COPY --from=alpine:3.19 /usr/share/zoneinfo /usr/share/zoneinfo
```

---

## Multi-Stage - Targeting Specific Stages

```bash
# Build only the builder stage
docker build --target builder -t myapp:build .

# Build only the test stage
docker build --target test -t myapp:test .

# Build the final stage (default)
docker build -t myapp:latest .
```

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS deps
RUN npm ci

FROM deps AS test
COPY . .
RUN npm test

FROM deps AS production
COPY . .
RUN npm run build
CMD ["node", "dist/main.js"]
```

---

## `BuildKit` - Next Generation Builder

- Parallel build stage execution
- Improved caching mechanisms
- Build secrets support
- `SSH` forwarding for private repos
- Cache mount for package managers
- Inline build cache export

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Or set in daemon.json
{
  "features": {
    "buildkit": true
  }
}
```

---

## `BuildKit` - Cache Mounts

```dockerfile
# syntax=docker/dockerfile:1

# Cache apt packages
FROM ubuntu:22.04
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y python3 python3-pip

# Cache pip packages
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# Cache Go modules
FROM golang:1.22
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app ./...

# Cache npm packages
FROM node:20
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

---

## `BuildKit` - Build Secrets

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Mount a secret file - never stored in image layers
RUN --mount=type=secret,id=pip_conf,target=/etc/pip.conf \
    pip install -r requirements.txt

# Use with private git repos
RUN --mount=type=secret,id=github_token \
    GITHUB_TOKEN=$(cat /run/secrets/github_token) && \
    pip install git+https://${GITHUB_TOKEN}@github.com/org/private-repo.git
```

```bash
# Pass secrets at build time
docker build --secret id=pip_conf,src=./pip.conf \
             --secret id=github_token,src=./token.txt \
             -t myapp .
```

---

## `BuildKit` - SSH Forwarding

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine:3.19
RUN apk add --no-cache git openssh-client

# Clone a private repository using host SSH agent
RUN --mount=type=ssh \
    mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    git clone git@github.com:org/private-repo.git /app
```

```bash
# Forward SSH agent to build
docker build --ssh default -t myapp .

# Or specify a specific key
docker build --ssh default=$HOME/.ssh/id_rsa -t myapp .
```

---

## `BuildKit` - Parallel Execution

```dockerfile
# BuildKit executes independent stages in parallel

FROM golang:1.22 AS backend
WORKDIR /backend
COPY backend/ .
RUN go build -o server        # ──┐
                               #   │  These run in
FROM node:20 AS frontend       #   │  parallel!
WORKDIR /frontend              #   │
COPY frontend/ .               #   │
RUN npm ci && npm run build    # ──┘

FROM alpine:3.19
COPY --from=backend /backend/server /usr/local/bin/
COPY --from=frontend /frontend/dist /var/www/html/
CMD ["server"]
```

---

## `BuildKit` - External Cache Backend

```bash
# Export cache to registry
docker build \
  --cache-to type=registry,ref=registry.example.com/myapp:cache \
  --cache-from type=registry,ref=registry.example.com/myapp:cache \
  -t myapp .

# Export cache to local directory
docker build \
  --cache-to type=local,dest=/tmp/buildcache \
  --cache-from type=local,src=/tmp/buildcache \
  -t myapp .

# Inline cache (stored in the image itself)
docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from myapp:latest \
  -t myapp:latest .
```

---

## Minimal Base Images Comparison

| Base Image            | Size       | Packages  | Use Case              |
|-----------------------|------------|-----------|------------------------|
| `ubuntu:22.04`        | ~77MB      | Many      | General purpose        |
| `debian:bookworm-slim`| ~74MB      | Medium    | Debian-based apps      |
| `alpine:3.19`         | ~7MB       | Minimal   | Small footprint        |
| `distroless`          | ~2-20MB    | None      | Minimal runtime        |
| `scratch`             | 0MB        | Nothing   | Static binaries only   |
| `busybox`             | ~1.2MB     | Basic CLI | Lightweight tooling    |
| `chainguard/static`   | ~2MB       | None      | Hardened distroless     |

---

## Building with `scratch`

```dockerfile
# For statically linked binaries
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags='-w -s -extldflags "-static"' \
    -o /app/server

FROM scratch
# Need certs for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt \
  /etc/ssl/certs/
# Need timezone data if used
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

COPY --from=builder /app/server /server
ENTRYPOINT ["/server"]
```

---

## Google `Distroless` Images

```dockerfile
# Java application
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY . .
RUN ./gradlew bootJar

FROM gcr.io/distroless/java21-debian12
COPY --from=builder /app/build/libs/app.jar /app.jar
CMD ["app.jar"]

# Python application
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --target=/deps -r requirements.txt

FROM gcr.io/distroless/python3-debian12
COPY --from=builder /deps /deps
ENV PYTHONPATH=/deps
COPY . /app
WORKDIR /app
CMD ["main.py"]
```

---

## Layer Caching - How It Works

![layer_caching_how_it_works](svg/courses/devops/advanced-docker/02_dockerfile_optimization/layer_caching_how_it_works.svg)

---

## Layer Caching - How It Works

**Rule:** Once a layer cache is invalidated, all subsequent layers rebuild.

---

## Layer Caching - Optimization

```dockerfile
# BAD: Any source change invalidates npm install
COPY . .
RUN npm install
RUN npm run build

# GOOD: Separate dependency install from source copy
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build
```

```dockerfile
# GOOD for Python
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# GOOD for Go
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o /app
```

---

## `.dockerignore` - Protecting the Build Context

```gitignore
# .dockerignore
.git
.gitignore
.dockerignore
Dockerfile
docker-compose*.yml
README.md
LICENSE

# Dependencies (will be installed in container)
node_modules
vendor
__pycache__

# Build artifacts
dist
build
*.o
*.pyc

# IDE and OS files
.vscode
.idea
*.swp
.DS_Store

# Environment and secrets
.env
.env.*
*.pem
*.key
```

---

## Reducing Layer Count

```dockerfile
# BAD: Multiple RUN commands = multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y vim
RUN rm -rf /var/lib/apt/lists/*

# GOOD: Single RUN command = single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      git \
      vim && \
    rm -rf /var/lib/apt/lists/*
```

---

## Removing Unnecessary Files in the Same Layer

```dockerfile
# BAD: Temp files persist in lower layer even after deletion
RUN curl -O https://example.com/big-file.tar.gz
RUN tar xzf big-file.tar.gz
RUN rm big-file.tar.gz  # Still in previous layer!

# GOOD: Download, extract, and clean up in one layer
RUN curl -O https://example.com/big-file.tar.gz && \
    tar xzf big-file.tar.gz && \
    rm big-file.tar.gz

# GOOD: Use pipe to avoid saving to disk
RUN curl -sL https://example.com/big-file.tar.gz | \
    tar xz -C /opt/
```

---

## Build Arguments (`ARG`)

```dockerfile
# Build-time variables
ARG GO_VERSION=1.22
ARG APP_VERSION=latest

FROM golang:${GO_VERSION} AS builder
ARG APP_VERSION
WORKDIR /app
COPY . .
RUN go build -ldflags="-X main.version=${APP_VERSION}" -o /app/server

FROM alpine:3.19
COPY --from=builder /app/server /usr/local/bin/
CMD ["server"]
```

```bash
# Override at build time
docker build \
  --build-arg GO_VERSION=1.21 \
  --build-arg APP_VERSION=2.1.0 \
  -t myapp:2.1.0 .
```

---

## `ARG` vs `ENV`

```dockerfile
# ARG: Only available during build
ARG BUILD_DATE
ARG VERSION

# ENV: Available during build AND at runtime
ENV APP_ENV=production
ENV LOG_LEVEL=info

# Pattern: Use ARG to set ENV
ARG VERSION=latest
ENV APP_VERSION=${VERSION}

# ARG before FROM affects FROM only
ARG ALPINE_VERSION=3.19
FROM alpine:${ALPINE_VERSION}

# ARG after FROM needs re-declaration
ARG VERSION
RUN echo "Building version ${VERSION}"
```

---

## `ENTRYPOINT` vs `CMD` - Advanced Usage

```dockerfile
# Pattern 1: ENTRYPOINT as wrapper script
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["server", "--port", "8080"]

# Pattern 2: ENTRYPOINT for fixed command, CMD for default args
ENTRYPOINT ["python3"]
CMD ["app.py"]
# docker run myapp           → python3 app.py
# docker run myapp test.py   → python3 test.py

# Pattern 3: Exec form vs shell form
ENTRYPOINT ["nginx", "-g", "daemon off;"]  # exec form - PID 1
ENTRYPOINT nginx -g 'daemon off;'          # shell form - /bin/sh -c
```

---

## Entrypoint Wrapper Script Pattern

```bash
#!/bin/bash
# docker-entrypoint.sh
set -e

# Run database migrations on startup
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput
fi

# Create superuser if needed
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --noinput || true
fi

# Collect static files
python manage.py collectstatic --noinput

# Execute the main command
exec "$@"
```

```dockerfile
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## `HEALTHCHECK` Instruction

```dockerfile
# Basic HTTP health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
  CMD curl -f http://localhost:8080/health || exit 1

# TCP check (no curl needed)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD nc -z localhost 5432 || exit 1

# Custom health check script
COPY healthcheck.sh /usr/local/bin/
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD ["healthcheck.sh"]

# Disable inherited health check
HEALTHCHECK NONE
```

---

## `LABEL` for Metadata

```dockerfile
# OCI image spec labels
LABEL org.opencontainers.image.title="My Application"
LABEL org.opencontainers.image.description="Production web server"
LABEL org.opencontainers.image.version="2.1.0"
LABEL org.opencontainers.image.created="2026-03-10"
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.authors="team@example.com"
LABEL org.opencontainers.image.licenses="MIT"

# Multiple labels in one instruction
LABEL maintainer="ops@example.com" \
      environment="production" \
      com.example.release-date="2026-03-10"
```

```bash
# Query labels
docker inspect myapp --format '{{json .Config.Labels}}' | jq
docker images --filter "label=environment=production"
```

---

## Image Analysis with `docker history`

```bash
# View layer sizes
docker history myapp:latest

# Full output without truncation
docker history --no-trunc myapp:latest

# Format output
docker history --format "{{.Size}}\t{{.CreatedBy}}" myapp:latest

# Example output:
# 0B      CMD ["node" "server.js"]
# 15.2MB  RUN npm ci --only=production
# 1.2kB   COPY package*.json ./
# 0B      WORKDIR /app
# 178MB   base image layer
```

---
## `dive` - Image Layer Explorer

```bash
# Install dive
wget https://github.com/wagoodman/dive/releases/download/v0.12.0/\
dive_0.12.0_linux_amd64.deb
sudo dpkg -i dive_0.12.0_linux_amd64.deb
# Analyze an image
dive myapp:latest
# CI mode - fail if image efficiency is low
dive myapp:latest --ci
# Checks:
#   - Image efficiency score
#   - Wasted space
#   - Total image size
```

---
## `dive` - Image Layer Explorer

![total_image_size](svg/courses/devops/advanced-docker/02_dockerfile_optimization/total_image_size.svg)

---

## `docker scout` - Image Analysis

```bash
# Analyze image for vulnerabilities
docker scout cves myapp:latest

# Quick overview
docker scout quickview myapp:latest

# Compare two images
docker scout compare myapp:v2 --to myapp:v1

# Recommendations for base image
docker scout recommendations myapp:latest

# SBOM (Software Bill of Materials)
docker scout sbom myapp:latest
```

---

## Squashing Layers

```bash
# Squash all layers into one (experimental)
docker build --squash -t myapp:squashed .

# Alternative: export and import
docker run -d --name temp myapp:latest true
docker export temp | docker import - myapp:squashed
docker rm temp

# Squashing removes layer cache benefits
# Use judiciously - mainly for final distribution
```

---

## Multi-Platform Builds with `buildx`

```bash
# Create a multi-platform builder
docker buildx create --name multiplatform --use

# Build for multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t myapp:latest \
  --push .

# List supported platforms
docker buildx ls

# Inspect the builder
docker buildx inspect multiplatform
```

---

## Multi-Platform `Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM golang:1.22 AS builder
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# Cross-compile for the target platform
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -o /app/server

FROM alpine:3.19
COPY --from=builder /app/server /usr/local/bin/
CMD ["server"]
```

---

## `Dockerfile` Linting with `hadolint`

```bash
# Run hadolint
docker run --rm -i hadolint/hadolint < Dockerfile

# Example output:
# DL3008: Pin versions in apt-get install
# DL3009: Delete apt-get lists after installing
# DL3015: Avoid additional packages
# DL4006: Set the SHELL option -o pipefail
# SC2086: Double quote to prevent globbing
```

```dockerfile
# Before hadolint
RUN apt-get update && apt-get install -y python3

# After hadolint
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3=3.11.* && \
    rm -rf /var/lib/apt/lists/*
```

---

## Production `Dockerfile` Template

```dockerfile
# syntax=docker/dockerfile:1
ARG NODE_VERSION=20

FROM node:${NODE_VERSION}-alpine AS base
RUN apk add --no-cache tini
WORKDIR /app

FROM base AS deps
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

FROM base AS build
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build && npm prune --production

FROM base AS production
ENV NODE_ENV=production
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -D appuser
COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=build --chown=appuser:appgroup /app/dist ./dist
COPY --from=build --chown=appuser:appgroup /app/package.json ./
USER appuser
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/main.js"]
```

---

## Summary - Dockerfile Optimization

- Use multi-stage builds to separate build-time from runtime
- Enable `BuildKit` for parallel builds, cache mounts, and secrets
- Choose the smallest viable base image (`distroless` > `alpine` > `slim`)
- Order `Dockerfile` instructions from least to most frequently changing
- Use `.dockerignore` to minimize build context
- Combine `RUN` instructions and clean up in the same layer
- Lint with `hadolint`, analyze with `dive` and `docker scout`
- Build for multiple platforms with `buildx`
