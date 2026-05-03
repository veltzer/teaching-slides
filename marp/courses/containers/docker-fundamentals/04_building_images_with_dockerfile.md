---
tags:
  - infrastructure:docker
  - infrastructure:dockerfile
level: beginner
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Building Images with Dockerfile

---
## What This Chapter Covers

- Dockerfile syntax
- The most-used instructions
- CMD vs ENTRYPOINT
- Build context and `.dockerignore`
- Layer caching and how to keep builds fast
- Multi-stage builds

---
## What a Dockerfile Is

- A text file with a sequence of instructions
- Each instruction creates an image layer
- `docker build` reads it, runs the instructions, produces an image
- Instructions in CAPS by convention; arguments follow on the same line
- Comments start with `#`

---
## Layers and Multi-stage

![dockerfile_layers](svg/courses/containers/docker-fundamentals/04_building_images_with_dockerfile/dockerfile_layers.svg)

---
## A Minimal Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

- Six lines, six layers
- `docker build -t myapp:1.0 .` builds it
- `docker run myapp:1.0` runs it

---
## FROM

- Always the first instruction (after optional ARG)
- Specifies the *base image*
- Multi-stage builds use multiple FROMs
- Pick small, well-maintained bases: `python:3.12-slim`, `node:20-alpine`, `eclipse-temurin:21-jre-alpine`
- `FROM scratch` for absolutely empty (rare; mostly Go binaries)

---
## RUN, COPY, ADD

- **RUN**: execute a command at build time (`apt-get install`, `pip install`)
- **COPY**: copy files from the build context into the image
- **ADD**: like COPY but also handles URLs and tarballs (use COPY unless you need ADD's extras)
- Each creates a new layer
- Combine RUN with `&&` to keep layer count down

---
## WORKDIR, ENV

- **WORKDIR**: sets the current directory for following instructions and the running container
- Like `cd`, but persists for subsequent layers
- **ENV**: set environment variables that persist in the running container
- `ENV PYTHONUNBUFFERED=1`
- Multiple `ENV` in one line is fine: `ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8`

---
## EXPOSE, USER

- **EXPOSE**: documents which port the container listens on (does *not* publish it)
- The publishing happens at `docker run -p ...`
- **USER**: switch to a non-root user for the rest of the image and container
- Best practice: don't run as root in production
- Create the user first: `RUN useradd -m app && USER app`

---
## CMD vs ENTRYPOINT

- **CMD**: the *default* command. Overridable at `docker run`.
- **ENTRYPOINT**: the *fixed* command. Args at `docker run` go *after* it.
- Pure CMD: `docker run image arg` replaces the CMD
- Pure ENTRYPOINT: `docker run image arg` appends `arg` to the entrypoint
- Use ENTRYPOINT for "this image *is* this binary"; CMD for default behaviour

---
## CMD vs ENTRYPOINT in Code

```dockerfile
ENTRYPOINT ["python", "main.py"]
CMD ["--config", "/etc/app.yaml"]
```

- `docker run myapp` &#8594; `python main.py --config /etc/app.yaml`
- `docker run myapp --debug` &#8594; `python main.py --debug`
- Use the JSON-array form (exec form) — avoids a shell wrapper

---
## Build Context

- The set of files Docker sends to the daemon at build time
- `docker build .` &#8594; the current directory is the context
- *Everything* in that directory gets sent (subject to `.dockerignore`)
- A bloated context slows every build
- Don't run `docker build` at `/` — you'll send your whole disk

---
## .dockerignore

```gitignore
node_modules/
*.log
.git/
.env
.venv/
__pycache__/
```

- Same syntax as `.gitignore`
- Excludes files from the build context
- Drastically speeds up builds for projects with big `node_modules` etc.
- Also keeps secrets out of the context (and out of the image)

---
## Layer Caching

- Docker caches each layer
- If a layer's inputs (instruction + previous layers + source files) haven't changed, the cache is reused
- Reorder instructions so the *most-changing* ones come last
- Common pattern: install dependencies (rarely change) before copying source (changes often)
- One bad cache miss can recompile everything from there down

---
## Cache-Friendly Ordering

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# Dependencies first — change rarely
COPY requirements.txt .
RUN pip install -r requirements.txt

# Source last — changes often
COPY . .
CMD ["python", "main.py"]
```

- Editing `main.py` reuses the dependency layer cache
- Adding a new dependency invalidates only from `requirements.txt` down

---
## Multi-Stage Builds

- A single Dockerfile with multiple `FROM` stages
- Build in one stage, copy artifacts to a smaller runtime stage
- Massive size reduction: from 1.5 GB to 50 MB is common
- The build tools (compilers, dev headers) never reach the final image
- Standard practice for Go, Rust, Java, modern Node

---
## Multi-Stage in Practice

```dockerfile
# Stage 1: build
FROM golang:1.22 AS builder
WORKDIR /src
COPY . .
RUN go build -o /app/server ./cmd/server

# Stage 2: runtime
FROM alpine:3.20
COPY --from=builder /app/server /app/server
USER 1000
ENTRYPOINT ["/app/server"]
```

- Two `FROM`s, each with `AS name`
- `COPY --from=builder` pulls artifacts across stages
- Final image: alpine + one binary, no Go toolchain

---
## Tagging During Build

```bash
docker build -t myapp:1.0 -t myapp:latest .
docker build -t registry.example.com/team/myapp:1.0 .
docker build --target builder -t myapp:dev .  # stop at named stage
```

- Multiple `-t` flags for multiple tags
- `--target` lets you build only up to a named stage (useful for CI debug)
- Use registry-prefixed tags right away if you'll push

---
## Build Arguments

```dockerfile
ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-alpine
```

```bash
docker build --build-arg NODE_VERSION=22 -t myapp .
```

- Available at build time only (not in the running container)
- Default value used if not passed
- Don't use ARG for secrets — they end up in the image history

---
## Common Mistakes

- Copying the entire repo before installing dependencies (cache busts on every code change)
- Running `apt-get install` without `--no-install-recommends` (bloats the image)
- Leaving package manager caches behind (`apt-get clean` or `rm -rf /var/lib/apt/lists/*`)
- Building as root, never adding USER (security smell)
- Using `:latest` base images (your build is non-reproducible)

---
## Dockerfile Best Practices

![dockerfile_best_practices](svg/courses/containers/docker-fundamentals/04_building_images_with_dockerfile/dockerfile_best_practices.svg)
