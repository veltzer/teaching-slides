---
tags:
  - infrastructure:docker
  - infrastructure:containers
level: beginner
category: containers
audience:
  - audiences:developers
  - audiences:devops

---

# Running Containers

---

## What This Chapter Covers

- The `docker run` command in depth
- Foreground vs background containers
- Container lifecycle commands
- Logs, stats, and `exec`
- CPU and memory limits
- Environment variables and configuration

---

## docker run, Decomposed

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

- `IMAGE`: which image to use
- `COMMAND` (optional): override the image's default command
- `OPTIONS`: many flags — `-d`, `-p`, `-v`, `--name`, `--rm`, `-e`, `--network`...
- Knowing the common options well covers 90% of daily use

---

## Most-Used run Options

- `-d`: detach (background)
- `-it`: interactive + tty (for shells)
- `--rm`: remove container when it exits
- `--name foo`: give it a memorable name
- `-p host:cont`: publish port
- `-e KEY=value`: environment variable
- `-v src:dst`: mount volume / bind

---

## Foreground Containers

```bash
docker run -it ubuntu bash
docker run --rm python:3.12 python -c "print(1+1)"
```

- Stdout / stderr stream to your terminal
- Exit when the process inside ends
- Good for ad-hoc work and testing
- Not what you want for long-running services

---

## Background Containers

```bash
docker run -d --name api -p 8080:80 nginx
docker ps
docker logs api
docker stop api
```

- `-d` returns immediately
- The container runs until its main process exits or you stop it
- `docker logs` retrieves recent stdout/stderr

---

## Lifecycle Commands

- `docker start NAME`: start a stopped container
- `docker stop NAME`: SIGTERM, then SIGKILL after timeout
- `docker restart NAME`: stop + start
- `docker pause / unpause`: SIGSTOP / SIGCONT
- `docker rm NAME`: remove (must be stopped first; `-f` to force)
- `docker kill NAME`: SIGKILL immediately

---

## Lifecycle Diagram

![lifecycle](svg/courses/containers/docker-fundamentals/03_running_containers/lifecycle.svg)

---

## Inspecting Containers

```bash
docker ps                    # running
docker ps -a                 # including stopped
docker inspect NAME          # full JSON
docker stats                 # live CPU/mem/IO
docker top NAME              # processes inside
```

- `inspect` is the deepest source of truth — networks, mounts, env, labels
- `stats` is your "is anything wrong" first stop

---

## Logs

```bash
docker logs api
docker logs -f api           # follow (like tail -f)
docker logs --tail 100 api
docker logs --since 5m api
```

- Default driver writes JSON files per container
- For high-traffic services, configure a remote driver (json-file rotation, journald, fluentd, etc.)
- Don't ssh into a container to read logs — let the host see them

---

## Exec: Running Commands Inside

```bash
docker exec -it api bash
docker exec api ls /etc
docker exec -e DEBUG=1 api /app/diagnose
```

- New process inside a running container
- Useful for debugging without restarting
- `-it` if you want a terminal
- For real long-term needs, build the image with the tool included

---

## Resource Limits

```bash
docker run -d --memory 512m --cpus 0.5 myapp
docker run -d --memory 1g --memory-swap 1g myapp
```

- `--memory`: hard limit; container OOM-killed past it
- `--cpus`: fractional CPUs (1.5 = 1.5 cores)
- `--memory-swap` equal to `--memory` disables swap
- Set limits in production — unbounded containers can starve neighbours

---

## Restart Policies

```bash
docker run -d --restart=always nginx
docker run -d --restart=unless-stopped nginx
docker run -d --restart=on-failure:5 myjob
```

- `no` (default), `always`, `unless-stopped`, `on-failure[:max]`
- Crucial for services that should auto-recover after host reboot
- Less crucial for one-off jobs

---

## Environment Variables

```bash
docker run -e DATABASE_URL=postgres://... \
           -e LOG_LEVEL=debug myapp
docker run --env-file .env myapp
```

- `-e KEY=value` for one or two
- `--env-file` for many
- Twelve-Factor App: configuration in environment, not in image
- Don't put secrets in environment unless you trust the host (use Docker secrets / orchestrator secrets for prod)

---

## Naming Containers

- Without `--name`, Docker invents `eager_einstein`-style names
- Cute, but bad for scripting
- `--name` gives a stable handle: `docker stop api` always means *the* api
- Names must be unique on the host
- For replicas, scope by label, not by trying to share a name

---

## Working Directory and User

```bash
docker run -w /app -u 1000:1000 myapp ./script.sh
```

- `-w /app`: cd to /app before running
- `-u 1000:1000`: run as UID 1000, GID 1000
- Default user is whatever the image set (often root)
- Best practice: build images with a non-root user

---

## A Short Workflow

```bash
docker run -d --name web --restart=unless-stopped \
           -p 8080:80 -e NGINX_HOST=example.com \
           --memory 256m --cpus 0.5 nginx:1.27-alpine

docker logs -f web
docker exec -it web sh
docker stop web && docker rm web
```

- Run in background, named, restartable, resource-limited
- Logs follow live
- Exec for ad-hoc inspection
- Clean up when done

---

## Common Mistakes

- Forgetting `-d` &#8594; terminal hijacked, hit Ctrl+C and the container dies
- Not setting `--restart` &#8594; service goes down on host reboot
- No resource limits &#8594; one container takes the whole host
- Editing files inside containers &#8594; gone after recreate
- Using `:latest` everywhere &#8594; restart pulls a different image

---

## Key docker run Flags

![run_options](svg/courses/containers/docker-fundamentals/03_running_containers/run_options.svg)
