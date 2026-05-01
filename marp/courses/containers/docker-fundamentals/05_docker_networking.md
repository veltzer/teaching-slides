---
tags:
  - infrastructure:docker
  - infrastructure:networking
level: beginner
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Docker Networking

---
## What This Chapter Covers

- The network drivers Docker ships with
- Default bridge vs user-defined bridge
- Creating and managing custom networks
- Container-to-container communication
- Publishing ports
- DNS inside Docker networks

---
## Network Drivers

- **bridge**: default; an isolated virtual network on the host
- **host**: container shares the host's network namespace
- **none**: no networking at all
- **overlay**: spans multiple Docker hosts (used by Swarm)
- **macvlan**: container gets its own MAC and IP on the physical network

---
## The Default Bridge

- Created automatically (`docker0`)
- Containers without explicit network attach to it
- Containers on it can reach each other by IP, *not* by name
- DNS-based service discovery doesn't work on the default bridge
- For real work: use a user-defined bridge instead

---
## User-Defined Bridges

```bash
docker network create app-net
docker run -d --name db --network app-net postgres
docker run -d --name api --network app-net myapi
```

- `api` can reach `db` by *name* — Docker provides DNS
- Cleaner isolation: containers on different user networks can't see each other
- Recommended pattern for multi-container apps

---
## Listing Networks

```bash
docker network ls
docker network inspect app-net
docker network rm app-net
```

- `ls` shows network ID, name, driver, scope
- `inspect` lists attached containers and the subnet
- Can't remove a network with attached containers

---
## Publishing Ports

```bash
docker run -d -p 8080:80 nginx              # host:8080 -> container:80
docker run -d -p 127.0.0.1:8080:80 nginx    # bind to localhost only
docker run -d -p 8080-8089:80 nginx         # range (rare)
docker run -d -P nginx                      # publish all EXPOSEd ports
```

- Without `-p`, the container's ports aren't reachable from the host
- `-p HOST:CONTAINER` is the most common form
- Bind to a specific host IP for security

---
## Inside vs Outside

- **Container-to-container** (same network): use the container *name* and its *internal* port
- **Host to container**: use the *host* and the *published* port
- **Container to host**: use `host.docker.internal` (Mac/Win) or the host's IP
- Common confusion: thinking the published port is the "real" port — it's a forwarding rule

---
## Network Topology

![networks](svg/courses/containers/docker-fundamentals/05_docker_networking/networks.svg)

---
## DNS Resolution

- Docker runs an embedded DNS server (`127.0.0.11`) for user-defined networks
- Resolves container names to their IPs on the same network
- `--network-alias` lets a container be reachable by additional names
- External DNS still works via `/etc/resolv.conf`
- For multi-host setups, use Kubernetes/Consul/Nomad service discovery

---
## Host Network Mode

```bash
docker run -d --network=host nginx
```

- Container shares the host's network stack directly
- No port forwarding, no isolation
- Performance: slightly faster (no NAT)
- Risk: container can bind to any host port; conflicts possible
- Linux only; Docker Desktop on Mac/Win simulates differently

---
## None Network Mode

```bash
docker run --network=none alpine sh
```

- Container has only `lo`; no other interfaces
- Use for batch jobs that need zero network access
- Surprisingly handy for security-sensitive computation

---
## Connecting Existing Containers

```bash
docker network connect app-net api
docker network disconnect app-net api
```

- A container can be on multiple networks at once
- Useful for "frontend on the public network, frontend + backend on the private one"
- Connect / disconnect at runtime

---
## Inspecting Container Networking

```bash
docker inspect api --format '{{json .NetworkSettings.Networks}}'
docker exec api ip a
docker exec api getent hosts db
```

- `inspect` shows IPs, gateways, MACs per network
- `ip a` inside the container is the canonical view
- `getent hosts` confirms DNS resolution works

---
## A Common Pitfall: Localhost Inside a Container

- `localhost` inside a container = the *container itself*, not the host
- An app inside trying to reach `localhost:5432` for the DB will fail
- Use the DB *container's name* on the same Docker network instead
- This trips up newcomers nearly every time

---
## Network Performance

- Bridge mode: NAT'd; small overhead per packet
- Host mode: native speed
- Overlay: VXLAN encapsulation; larger overhead, fine for most apps
- For high-throughput, host networking or `macvlan` may be required
- Most apps notice nothing

---
## Common Mistakes

- Two containers on different user networks expecting to talk &#8594; they can't, by design
- Hard-coding IPs &#8594; use names
- Forgetting `-p` &#8594; the container is up but unreachable from the host
- Publishing too many ports &#8594; widens attack surface
- Reusing the default bridge for new projects &#8594; lose DNS, lose isolation
