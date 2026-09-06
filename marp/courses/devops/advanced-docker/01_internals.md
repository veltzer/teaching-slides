---
tags:
  - tools:docker
  - infrastructure:containers
  - practices:devops
  - networking:networking
level: advanced
category: devops
audience:
  - audiences:developers

---

# Docker Internals and Architecture

Understanding what happens beneath the `docker` CLI

---

## Agenda

- The `Docker` engine architecture
- `containerd` and `runc`
- `Linux` namespaces in depth
- `cgroups` resource control
- The `OCI` specifications
- How a container actually starts
- Hands-on exploration of internals

---

## The Docker Engine - High Level

![the_docker_engine_high_level](svg/courses/devops/advanced-docker/01_internals/the_docker_engine_high_level.svg)

---

## `dockerd` - The Docker Daemon

- Listens on a `UNIX` socket (`/var/run/docker.sock`) or `TCP`
- Manages images, containers, networks, volumes
- Exposes the `Docker` `REST` `API`
- Delegates container execution to `containerd`

```bash
# Check daemon status
systemctl status docker

# View daemon configuration
cat /etc/docker/daemon.json

# Start daemon in debug mode
dockerd --debug
```

---

## `dockerd` Configuration

```json
{
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-address-pools": [
    {"base": "172.20.0.0/16", "size": 24}
  ],
  "live-restore": true,
  "debug": false,
  "tls": true,
  "tlscacert": "/etc/docker/ca.pem",
  "tlscert": "/etc/docker/server-cert.pem",
  "tlskey": "/etc/docker/server-key.pem"
}
```

---

## `containerd` - Container Runtime

- Industry-standard container runtime
- Manages the complete container lifecycle
- Image pull/push, storage, container execution
- Used by `Docker`, `Kubernetes`, and others
- Communicates via `gRPC` `API`

```bash
# containerd ships with its own CLI: ctr
sudo ctr namespaces list
sudo ctr containers list
sudo ctr images list

# Check containerd status
sudo systemctl status containerd
```

---

## `containerd` Architecture

![containerd_architecture](svg/courses/devops/advanced-docker/01_internals/containerd_architecture.svg)

---

## The Shim Process

- One shim per container (`containerd-shim-runc-v2`)
- Allows `containerd` to restart without killing containers
- Manages `STDIO` and exit status for the container
- Keeps container running even if daemon restarts

```bash
# Observe shim processes
ps aux | grep containerd-shim

# Each container has its own shim
docker run -d --name test1 nginx
docker run -d --name test2 alpine sleep 3600
ps aux | grep containerd-shim | grep -v grep
```

---

## `runc` - The OCI Runtime

- Reference implementation of the `OCI` Runtime Specification
- Actually creates and runs containers
- Low-level tool: sets up namespaces, `cgroups`, filesystem
- Executes the container process

```bash
# runc can be used directly
# Create an OCI bundle
mkdir -p mycontainer/rootfs
docker export $(docker create busybox) | \
  tar -C mycontainer/rootfs -xf -

# Generate spec
cd mycontainer
runc spec

# Run the container
sudo runc run my-container
```

---

## The `OCI` Runtime Spec (`config.json`)

```json
{
  "ociVersion": "1.0.2",
  "process": {
    "terminal": true,
    "user": { "uid": 0, "gid": 0 },
    "args": ["sh"],
    "env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
    "cwd": "/"
  },
  "root": {
    "path": "rootfs",
    "readonly": true
  },
  "linux": {
    "namespaces": [
      { "type": "pid" },
      { "type": "network" },
      { "type": "ipc" },
      { "type": "uts" },
      { "type": "mount" }
    ]
  }
}
```

---

## `OCI` Image Specification

- Defines how container images are built and distributed
- Image manifest, image index, layer format
- Content-addressable storage using `SHA256` digests

```bash
# Inspect an image manifest
docker manifest inspect nginx:latest

# Inspect image layers
docker inspect nginx:latest --format '{{.RootFS.Layers}}'

# View image history (layer by layer)
docker history nginx:latest --no-trunc
```

---

## `OCI` Distribution Specification

- Defines the `API` for distributing container images
- Registry `HTTP` `API` (v2)
- Push, pull, and content discovery

```bash
# Pull by digest (content-addressable)
docker pull nginx@sha256:abc123...

# List tags via registry API
curl -s https://registry.hub.docker.com/v2/library/nginx/tags/list

# Get manifest via API
curl -s -H "Accept: application/vnd.oci.image.manifest.v1+json" \
  https://registry.example.com/v2/myapp/manifests/latest
```

---

## Linux Namespaces - Overview

| Namespace | Flag            | Isolates                        |
|-----------|-----------------|----------------------------------|
| Mount     | `CLONE_NEWNS`   | Mount points                     |
| UTS       | `CLONE_NEWUTS`  | Hostname and domain name         |
| IPC       | `CLONE_NEWIPC`  | IPC resources                    |
| PID       | `CLONE_NEWPID`  | Process IDs                      |
| Network   | `CLONE_NEWNET`  | Network devices, stacks, ports   |
| User      | `CLONE_NEWUSER` | User and group IDs               |
| Cgroup    | `CLONE_NEWCGROUP`| Cgroup root directory           |

---

## PID Namespace

- Processes inside the container see their own PID tree
- PID 1 inside container is different from PID 1 on host

```bash
# Host sees all processes
ps aux | grep nginx

# Inside container, PID 1 is the main process
docker run --rm nginx ps aux
# PID 1 = nginx master process

# Inspect the PID namespace
docker run -d --name pidtest alpine sleep 3600
PID=$(docker inspect pidtest --format '{{.State.Pid}}')
sudo ls -la /proc/$PID/ns/pid
```

---

## PID Namespace - Hands On

```bash
# Create a new PID namespace with unshare
sudo unshare --pid --fork --mount-proc /bin/bash

# Inside the new namespace:
ps aux
# Only shows processes in this namespace
echo $$
# PID 1 or similar

# From another terminal, observe from host
ps aux | grep unshare
# Host sees the real PID
```

---

## Network Namespace

- Each container gets its own network stack
- Own interfaces, routing table, `iptables` rules, sockets
- `veth` pairs connect container namespace to host

```bash
# List network namespaces
sudo ip netns list

# Inspect container's network namespace
docker run -d --name nettest alpine sleep 3600
PID=$(docker inspect nettest --format '{{.State.Pid}}')
sudo nsenter -t $PID -n ip addr show

# Compare with host
ip addr show
```

---

## Network Namespace - veth Pairs

![network_namespace_veth_pairs](svg/courses/devops/advanced-docker/01_internals/network_namespace_veth_pairs.svg)

---

## Network Namespace - veth Pairs: Example

```bash
# See veth pairs
ip link show type veth
# See the bridge
brctl show docker0
# or
ip link show docker0
```

---

## Mount Namespace

- Isolates the filesystem mount table
- Container sees its own root filesystem
- Host mounts are not visible inside the container

```bash
# Container has its own mount table
docker run --rm alpine mount

# Compare with host
mount

# Using unshare to create mount namespace
sudo unshare --mount /bin/bash
# Mounts made here are invisible to the host
mount --bind /tmp /mnt
# Only visible in this namespace
```

---

## UTS Namespace

- Isolates hostname and domain name
- Each container can have its own hostname

```bash
# Container gets its own hostname (container ID by default)
docker run --rm alpine hostname

# Set custom hostname
docker run --rm --hostname myapp.local alpine hostname

# Using unshare
sudo unshare --uts /bin/bash
hostname container-test
hostname
# Shows container-test, host is unchanged
```

---

## User Namespace

- Maps `UID`/`GID` inside container to different `UID`/`GID` on host
- Root inside container can be non-root on host
- Significantly improves security

```bash
# Enable user namespace remapping in daemon.json
{
  "userns-remap": "default"
}

# Check the mapping
cat /etc/subuid
cat /etc/subgid

# Verify: root in container maps to non-root on host
docker run -d --name usertest alpine sleep 3600
PID=$(docker inspect usertest --format '{{.State.Pid}}')
cat /proc/$PID/uid_map
```

---

## Cgroups v1 vs v2

| Feature          | cgroups v1               | cgroups v2               |
|------------------|--------------------------|--------------------------|
| Hierarchy        | Multiple hierarchies     | Single unified hierarchy |
| Controllers      | Per-hierarchy            | Per-subtree              |
| Thread support   | Limited                  | Full                     |
| Pressure info    | No                       | `PSI` support            |
| Default on       | Older kernels            | Kernel 5.x+              |

```bash
# Check which version is in use
stat -fc %T /sys/fs/cgroup/
# tmpfs = v1, cgroup2fs = v2

# Or check mount
mount | grep cgroup
```

---

## Cgroups - CPU Control

```bash
# Limit CPU to 50% of one core
docker run -d --cpus="0.5" --name cpu-test alpine stress --cpu 4

# Limit to specific CPU cores
docker run -d --cpuset-cpus="0,1" --name cpu-pin alpine stress --cpu 4

# CPU shares (relative weight, default 1024)
docker run -d --cpu-shares=512 --name low-prio alpine stress --cpu 4
docker run -d --cpu-shares=2048 --name high-prio alpine stress --cpu 4

# View cgroup settings
cat /sys/fs/cgroup/cpu/docker/<container-id>/cpu.cfs_quota_us
cat /sys/fs/cgroup/cpu/docker/<container-id>/cpu.cfs_period_us
```

---

## Cgroups - Memory Control

```bash
# Limit memory to 256MB
docker run -d --memory=256m --name mem-test alpine stress --vm 1 --vm-bytes 512M

# Memory + swap limit
docker run -d --memory=256m --memory-swap=512m --name swap-test alpine sleep 3600

# Memory reservation (soft limit)
docker run -d --memory=512m --memory-reservation=256m --name soft-test alpine sleep 3600

# Disable OOM killer
docker run -d --memory=256m --oom-kill-disable --name no-oom alpine sleep 3600

# View memory stats
docker stats --no-stream mem-test
cat /sys/fs/cgroup/memory/docker/<container-id>/memory.usage_in_bytes
```

---

## Cgroups - I/O Control

```bash
# Limit block IO weight (10-1000)
docker run -d --blkio-weight=100 --name io-test alpine sleep 3600

# Limit read/write rate for specific device
docker run -d \
  --device-read-bps=/dev/sda:10mb \
  --device-write-bps=/dev/sda:10mb \
  --name io-limit alpine sleep 3600

# Limit IOPS
docker run -d \
  --device-read-iops=/dev/sda:1000 \
  --device-write-iops=/dev/sda:1000 \
  --name iops-limit alpine sleep 3600
```

---

## Cgroups - PIDs Limit

```bash
# Limit number of processes inside container
docker run -d --pids-limit=100 --name pids-test alpine sleep 3600

# Default pids limit is set in daemon.json
{
  "default-pids-limit": 200
}

# Fork bomb protection
docker run --rm --pids-limit=50 alpine sh -c \
  ':(){ :|:& };:'
# Will be stopped by pids limit
```

---

## How a Container Starts - Step by Step

![how_a_container_starts_step_by_step](svg/courses/devops/advanced-docker/01_internals/how_a_container_starts_step_by_step.svg)

---

## Tracing Container Startup

```bash
# Trace system calls during container creation
sudo strace -f -e trace=clone,unshare,mount,pivot_root \
  docker run --rm alpine echo hello 2>&1 | head -50

# Watch namespace creation in real-time
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_clone {
  printf("%s clone flags: %lx\n", comm, args->clone_flags);
}'

# Watch cgroup creation
sudo inotifywait -m -r /sys/fs/cgroup/
```

---

## `nsenter` - Entering Container Namespaces

```bash
# Enter all namespaces of a running container
docker run -d --name myapp nginx
PID=$(docker inspect myapp --format '{{.State.Pid}}')

# Enter with nsenter
sudo nsenter -t $PID --mount --uts --ipc --net --pid

# Enter only the network namespace
sudo nsenter -t $PID --net ip addr show

# Enter only the PID namespace
sudo nsenter -t $PID --pid --mount ps aux

# This is what "docker exec" does under the hood
docker exec myapp ps aux
```

---

## `/proc` and Container Introspection

```bash
# Examine a container process from the host
PID=$(docker inspect myapp --format '{{.State.Pid}}')

# View namespace symlinks
ls -la /proc/$PID/ns/

# View cgroup membership
cat /proc/$PID/cgroup

# View mount info
cat /proc/$PID/mountinfo

# View capabilities
cat /proc/$PID/status | grep Cap

# View environment
cat /proc/$PID/environ | tr '\0' '\n'
```

---

## Container Filesystem - OverlayFS

![container_filesystem_overlayfs](svg/courses/devops/advanced-docker/01_internals/container_filesystem_overlayfs.svg)

---

## Container Filesystem - OverlayFS: Example

```bash
# View overlay mount details
docker inspect myapp --format '{{.GraphDriver.Data}}'
# Examine the layers
ls /var/lib/docker/overlay2/
```

---

## Exploring OverlayFS Layers

```bash
# Start a container and make changes
docker run -d --name overlay-demo alpine sleep 3600
docker exec overlay-demo sh -c 'echo "hello" > /testfile'

# Find the overlay mount
MERGED=$(docker inspect overlay-demo \
  --format '{{.GraphDriver.Data.MergedDir}}')
UPPER=$(docker inspect overlay-demo \
  --format '{{.GraphDriver.Data.UpperDir}}')
LOWER=$(docker inspect overlay-demo \
  --format '{{.GraphDriver.Data.LowerDir}}')

# The new file is in the upper (writable) layer
ls $UPPER
cat $UPPER/testfile
```

---

## Alternative OCI Runtimes

| Runtime     | Description                              |
|-------------|------------------------------------------|
| `runc`      | Reference `OCI` runtime (default)        |
| `crun`      | Fast `OCI` runtime written in C          |
| `gVisor`    | Application kernel for sandboxing        |
| `Kata`      | Lightweight VMs as containers            |
| `youki`     | `OCI` runtime written in Rust            |
| `Firecracker` | Micro-VMs from `AWS`                  |

```bash
# Use an alternative runtime
docker run --runtime=runsc -d --name gvisor-test nginx
docker run --runtime=kata -d --name kata-test nginx
```

---

## Configuring Alternative Runtimes

```json
{
  "runtimes": {
    "runsc": {
      "path": "/usr/local/bin/runsc",
      "runtimeArgs": ["--network=sandbox"]
    },
    "kata": {
      "path": "/usr/bin/kata-runtime"
    },
    "crun": {
      "path": "/usr/bin/crun"
    }
  },
  "default-runtime": "runc"
}
```

```bash
sudo systemctl restart docker
```

---

## Docker API - Direct Interaction

```bash
# List containers via socket
curl --unix-socket /var/run/docker.sock \
  http://localhost/v1.43/containers/json | jq

# Create a container
curl --unix-socket /var/run/docker.sock \
  -X POST -H "Content-Type: application/json" \
  -d '{"Image":"alpine","Cmd":["echo","hello"]}' \
  http://localhost/v1.43/containers/create?name=api-test

# Start it
curl --unix-socket /var/run/docker.sock \
  -X POST \
  http://localhost/v1.43/containers/api-test/start

# Get logs
curl --unix-socket /var/run/docker.sock \
  http://localhost/v1.43/containers/api-test/logs?stdout=true
```

---

## Summary - Docker Internals

- `dockerd` orchestrates, `containerd` manages, `runc` executes
- `Linux` namespaces provide isolation (PID, network, mount, UTS, user, IPC)
- `cgroups` enforce resource limits (CPU, memory, I/O, PIDs)
- `OverlayFS` provides the layered filesystem
- `OCI` specifications ensure interoperability
- The shim process enables daemon-less container survival
- Everything is inspectable via `/proc`, `nsenter`, and the `Docker` `API`
