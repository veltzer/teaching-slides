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
# Introduction to Containers and Docker

---
## What This Chapter Covers

- What containers are and why they matter
- Containers vs virtual machines
- A short history of container technology
- Docker's architecture: daemon, client, registry
- Installing Docker on Linux
- The Docker CLI at a glance

---
## What a Container Is

- A package that bundles an application with everything it needs to run
- Code, runtime, libraries, environment variables, configuration
- Runs as an isolated process on a shared kernel
- Starts in seconds, not minutes
- "Works on my machine" becomes "works the same everywhere"

---
## Container vs VM

![container_vs_vm](svg/courses/containers/docker-fundamentals/01_introduction_to_containers_and_docker/container_vs_vm.svg)

---
## Why Containers

- Consistent environments from laptop to production
- Lightweight — many containers per machine, not one big VM
- Fast startup makes scaling and CI/CD viable
- Standard packaging across languages and frameworks
- The unit that orchestrators (Kubernetes, Nomad) schedule

---
## Containers vs Virtual Machines

- VM: full guest OS on top of a hypervisor; gigabytes; minutes to boot
- Container: process(es) on the host kernel with isolation; megabytes; seconds to start
- VM gives stronger isolation; container gives better density and speed
- Modern infrastructure mixes both: VMs hold the host, containers hold the apps
- Pick by isolation needs and density goals

---
## Containers vs VMs Diagram

![containers_vs_vms](svg/courses/containers/docker-fundamentals/01_introduction_to_containers_and_docker/containers_vs_vms.svg)

---
## A Short History

- chroot (1979): the first filesystem isolation
- FreeBSD jails (2000): full process isolation
- Solaris Zones (2004): broader resource isolation
- LXC (2008): Linux containers using cgroups + namespaces
- Docker (2013): UX, image format, registry — what made containers go mainstream
- OCI (2015): Open Container Initiative standardised the format

---
## Docker Architecture

- **Docker Client** (`docker` CLI): what you type
- **Docker Daemon** (`dockerd`): runs on the host, does the actual work
- **Container Runtime** (containerd, runc): manages container lifecycles
- **Image Registry** (Docker Hub, ECR, GHCR): stores images
- The daemon talks to the kernel via cgroups and namespaces

---
## Daemon, Client, Registry Diagram

![docker_architecture](svg/courses/containers/docker-fundamentals/01_introduction_to_containers_and_docker/docker_architecture.svg)

---
## What Makes a Container Isolated

- **Namespaces**: separate views of processes, network, filesystem, users
- **Cgroups**: enforce CPU, memory, I/O limits
- **Capabilities**: limit which root operations a container can perform
- **Seccomp / AppArmor / SELinux**: restrict syscalls
- All Linux kernel features; Docker just orchestrates them

---
## Installing Docker on Linux

```bash
# Ubuntu / Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER  # log out and back in
docker --version
docker run hello-world
```

- The convenience script is fine for trying things
- For production: use the distro packages and pin versions
- macOS / Windows: Docker Desktop runs a small Linux VM under the hood

---
## The Docker CLI Map

- `docker run`: create and start a container
- `docker ps`: list running containers
- `docker images`: list local images
- `docker pull`: fetch an image from a registry
- `docker build`: build an image from a Dockerfile
- `docker exec`: run a command in a running container
- `docker logs`: stream container output

---
## A First Container

```bash
docker run -it ubuntu bash
```

- Pulls `ubuntu:latest` if not local
- Creates a container, attaches you to its bash session
- Inside: regular Linux, isolated from your host
- Exit the shell &#8594; container stops
- `docker run --rm` removes the container automatically when it exits

---
## A Long-Running Container

```bash
docker run -d -p 8080:80 nginx
docker ps
curl http://localhost:8080
```

- `-d`: detached (run in background)
- `-p 8080:80`: publish container port 80 on host port 8080
- `docker ps` confirms it's running
- Standard nginx welcome page served from the container

---
## Container Lifecycle

- **Created**: image instantiated, not yet started
- **Running**: actively executing
- **Paused**: SIGSTOP'd, holds memory but no CPU
- **Stopped**: process exited; container still exists
- **Removed**: container gone; data inside it is gone
- Common commands: `start`, `stop`, `pause`, `unpause`, `rm`

---
## Where Things Live

- `/var/lib/docker/`: images, container layers, volumes
- Containers run as `dockerd` child processes
- Logs go to JSON files by default (per-container)
- Networks are managed by Docker via Linux bridges and iptables
- Most users never need to look here directly

---
## Common Beginner Mistakes

- Confusing image with container (image is the template, container is the instance)
- Editing files inside a container expecting persistence — they're gone when the container is
- Running everything as root inside the container ("it works in dev")
- Pulling `:latest` and being surprised when behaviour changes
- Treating Docker like a VM — it's a process boundary, not a sandbox

---
## What's Next

- Images: how they're built, layered, and shared
- Running containers: arguments, lifecycle, debugging
- Dockerfile: building your own images
- Networking, storage, Compose, security

---
## Why Teams Adopt Containers

![container_benefits](svg/courses/containers/docker-fundamentals/01_introduction_to_containers_and_docker/container_benefits.svg)
