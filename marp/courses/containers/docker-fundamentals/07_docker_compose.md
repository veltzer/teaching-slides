---
tags:
  - infrastructure:docker
  - infrastructure:compose
level: beginner
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Docker Compose

---
## What This Chapter Covers

- The problem Compose solves
- The compose.yaml file structure
- Defining services, networks, volumes
- Building and running multi-container apps
- Environment files and variable substitution
- Scaling, profiles, overrides

---
## What Compose Is

- A way to define and run multi-container applications with one file
- One YAML file describes services, networks, volumes
- One command (`docker compose up`) starts everything
- Used heavily for local development and small deployments
- For production at scale: Kubernetes is the usual upgrade path

---
## Why Use Compose

- A single file replaces a script of `docker run` commands
- Version-controlled, reproducible, shareable
- Sane defaults: a network is created automatically; services can talk by name
- One command up, one command down, no leftovers
- Onboarding: `git clone && docker compose up` and your dev env is running

---
## A Minimal compose.yaml

```yaml
services:
  web:
    image: nginx:1.27-alpine
    ports:
      - "8080:80"
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pg-data:/var/lib/postgresql/data

volumes:
  pg-data:
```

- Two services: `web` and `db`
- Named volume for the DB
- `docker compose up` starts both

---
## Service Configuration

```yaml
services:
  api:
    build: ./api               # build from a Dockerfile
    image: myapi:dev
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://db/myapp
    depends_on:
      - db
    restart: unless-stopped
```

- `build`: path to a Dockerfile, or `{ context: ., dockerfile: Dockerfile.api }`
- `image`: name to tag (or pull) the image
- `depends_on`: start order (does *not* wait for "ready")

---
## Networks

```yaml
services:
  api: { ... networks: [back] }
  db:  { ... networks: [back] }
  web: { ... networks: [front, back] }

networks:
  front: {}
  back: {}
```

- Compose creates a default network if you don't define any
- Services on the same network find each other by service name (`db`, `api`)
- Multiple networks isolate concerns: `web` exposed; `db` not

---
## Volumes

```yaml
volumes:
  pg-data:
  uploads:
    driver: local

services:
  db:
    volumes:
      - pg-data:/var/lib/postgresql/data
  app:
    volumes:
      - uploads:/var/uploads
      - ./config:/etc/app:ro     # bind mount, read-only
```

- Named volumes are declared in the top-level `volumes:`
- Bind mounts use a path on the left
- `:ro` for read-only

---
## Running Compose

```bash
docker compose up                # foreground, attached
docker compose up -d             # detached
docker compose down              # stop and remove containers + default network
docker compose down -v           # also remove volumes (careful)
docker compose ps                # list services
docker compose logs -f api       # follow one service
docker compose exec api bash     # exec into a running service
```

- Compose v2 is the modern command (`docker compose`, with a space)
- v1 (`docker-compose`) is deprecated

---
## Building With Compose

```yaml
services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile.prod
      args:
        NODE_VERSION: "20"
    image: myapp/api:dev
```

```bash
docker compose build api          # build one service
docker compose build              # build all
docker compose up --build         # rebuild before starting
```

---
## Environment Variables

```yaml
services:
  api:
    environment:
      LOG_LEVEL: ${LOG_LEVEL:-info}
      DATABASE_URL: ${DATABASE_URL}
    env_file:
      - .env
```

- `${VAR}`: read from your shell env or `.env`
- `${VAR:-default}`: with a fallback
- `env_file`: load many vars at once
- Don't commit `.env` to git

---
## Scaling

```bash
docker compose up -d --scale api=3
```

- Spin up multiple replicas of one service
- Each gets its own container name (`project-api-1`, `-2`, `-3`)
- Useful for testing horizontal scaling locally
- For a load balancer, you'll need an additional service in front

---
## Profiles

```yaml
services:
  app: { ... }
  test:
    image: myapp:test
    profiles: ["testing"]
  debug:
    image: ms/debug
    profiles: ["debug"]
```

```bash
docker compose up                       # only services with no profile
docker compose --profile testing up     # include "testing" services
```

- Group services by purpose
- Don't run debug containers in production by accident

---
## Overrides

- `compose.override.yaml` is loaded automatically alongside `compose.yaml`
- Use it for dev-specific overrides (volume mounts, debug ports)
- Production: `docker compose -f compose.yaml -f compose.prod.yaml up -d`
- Layered config keeps the base file clean

---
## A Real-ish Example

```yaml
services:
  web:
    image: nginx:1.27-alpine
    ports: ["80:80"]
    depends_on: [api]
  api:
    build: ./api
    environment:
      DB_HOST: db
    depends_on: [db, cache]
  db:
    image: postgres:16-alpine
    environment: { POSTGRES_PASSWORD: secret }
    volumes: ["pg-data:/var/lib/postgresql/data"]
  cache:
    image: redis:7-alpine
volumes:
  pg-data:
```

---
## Common Mistakes

- `depends_on` without a healthcheck &#8594; api starts before db is *ready*
- Putting secrets in committed `compose.yaml` &#8594; use `.env` and `.gitignore` it
- Forgetting `down -v` &#8594; old volumes outlive the project
- Running `compose up` from the wrong directory &#8594; new project, new everything
- Treating Compose as production orchestration — it isn't, beyond a single host

---
## When To Outgrow Compose

- More than one host
- Real failover and self-healing
- Rolling updates with zero downtime
- Service mesh, ingress, RBAC
- All of the above &#8594; Kubernetes (or Nomad, ECS, etc.)

---
## What Docker Compose Provides

![compose_features](svg/courses/containers/docker-fundamentals/07_docker_compose/compose_features.svg)
