---
tags:
  - infrastructure:docker
  - infrastructure:storage
level: beginner
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Docker Volumes and Storage

---
## What This Chapter Covers

- Why containers need help with persistence
- The three storage types: volumes, bind mounts, tmpfs
- Creating and managing volumes
- Sharing data between containers
- Backup and restore strategies

---
## The Problem

- A container's filesystem is *ephemeral*
- Stop and remove the container &#8594; data inside is gone
- For databases, uploads, generated files, cache: not acceptable
- Solution: write important data to mounted storage
- The container exits, the data lives on

---
## Three Storage Types

- **Volume**: managed by Docker, lives in `/var/lib/docker/volumes/`
- **Bind mount**: any host path mounted into the container
- **tmpfs**: memory-only, never written to disk

---
## When to Use Which

- **Volume**: production data, databases — Docker manages it
- **Bind mount**: dev workflow (mount your source dir into the container)
- **tmpfs**: secrets, session data — never touches disk

---
## Storage Diagram

![storage_types](svg/courses/containers/docker-fundamentals/06_docker_volumes_and_storage/storage_types.svg)

---
## Named Volumes

```bash
docker volume create pg-data
docker run -d --name db \
  -v pg-data:/var/lib/postgresql/data \
  postgres
```

- Docker creates and manages the volume
- Survives container removal
- Name persists; can be re-mounted into a new container
- Backed by `/var/lib/docker/volumes/pg-data/_data` on the host

---
## Anonymous Volumes

```bash
docker run -d -v /var/lib/postgresql/data postgres
```

- No name; Docker generates a random one
- Hard to find later
- Use named volumes instead — almost always better

---
## Bind Mounts

```bash
docker run -d -v "$(pwd)":/app -w /app node:20 npm test
```

- The host path on the left, container path on the right
- *Anything* on the host path appears inside
- Common for development: edit on host, container sees changes
- The container can write to the host filesystem — careful with permissions

---
## tmpfs Mounts

```bash
docker run --tmpfs /run/secrets:size=64m alpine
```

- Filesystem in RAM
- Never written to disk
- Useful for secrets you don't want persisted
- Lost when the container stops

---
## Listing and Inspecting Volumes

```bash
docker volume ls
docker volume inspect pg-data
docker volume rm pg-data           # only if not in use
docker volume prune                # remove unused volumes
```

- `inspect` shows where the volume lives on the host
- `prune` is convenient and dangerous — it deletes volumes not in use by any container

---
## Sharing Between Containers

```bash
docker run -d --name producer -v shared:/data alpine
docker run -d --name consumer -v shared:/data alpine
```

- Both containers see the same `/data`
- Writes from one are visible to the other immediately
- The shared volume can outlive both containers

---
## Read-Only Mounts

```bash
docker run -v config:/etc/app:ro myapp
docker run -v "$(pwd)/conf":/etc/app:ro myapp
```

- Append `:ro` for read-only
- Container can read but not modify
- Good for config files; the running app shouldn't be editing them anyway
- Reduces blast radius of a compromised container

---
## Backup Strategies

```bash
docker run --rm \
  -v pg-data:/source:ro \
  -v "$(pwd)":/backup \
  alpine tar czf /backup/pg-data-$(date +%F).tgz -C /source .
```

- Spin up a temporary container that mounts both the volume (read-only) and a host backup dir
- Tar the volume into the host dir
- Same idea in reverse for restore
- For databases: prefer the database's own backup tool (`pg_dump`, etc.)

---
## Restore From Backup

```bash
docker volume create pg-data-restore
docker run --rm \
  -v pg-data-restore:/target \
  -v "$(pwd)":/backup \
  alpine tar xzf /backup/pg-data-2026-05-01.tgz -C /target
```

- Create the empty volume
- Spin up a temp container, extract the tarball into it
- Start the real DB container against the new volume

---
## Volume Drivers

- Default driver: `local`
- Plugin drivers: NFS, Azure Files, AWS EFS, GlusterFS, Ceph
- Used in clusters where containers move between hosts
- Plain Docker on one host: `local` is almost always the right choice
- Configured at `docker volume create --driver`

---
## Storage Performance

- Bind mounts: native filesystem performance on Linux; *slow* on Mac/Windows (Docker Desktop)
- Volumes: same as bind mounts on Linux; faster than bind mounts on Mac/Win
- tmpfs: RAM speed
- For dev on Mac: use volumes for `node_modules`, bind for source
- For production: it's all Linux, all fast

---
## Permissions Gotchas

- Bind-mounted host file owned by UID 1000 on the host
- Container running as root sees a file owned by UID 1000 — fine to read
- Container running as `app` (UID 999) — may not be able to write
- Either align UIDs (`-u 1000:1000` on `docker run`) or fix file ownership
- Most beginner storage problems are permission problems

---
## Common Mistakes

- Forgetting to mount a volume &#8594; data lost on container removal
- Bind-mounting your home directory &#8594; security and performance problems
- `docker volume prune` in a hurry &#8594; deleted production data
- Sharing a volume between two writers without coordination &#8594; corruption
- Trusting bind mount performance on Mac/Windows for hot loops
