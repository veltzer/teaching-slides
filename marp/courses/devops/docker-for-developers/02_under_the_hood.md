# Docker Under the Hood
---

## Virtual Machine Basics

![virtual_machine_basics](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/virtual_machine_basics.svg)

---

## How Virtual Machines Work

| Component | Role | Resource Impact |
|-----------|------|----------------|
| Guest OS | Complete OS copy | 5-20GB storage |
| Hypervisor | Resource management | 10-20% overhead |
| Virtual Hardware | Hardware emulation | Memory overhead |
| Host OS | Base system | Shared resource |

---

## VM Resource Allocation

- Full hardware virtualization
- Fixed memory allocation
- Dedicated virtual CPU cores
- Complete OS overhead
- Slow boot time (minutes)
- Full system isolation

---

## Containers vs VMs

![containers_vs_vms](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/containers_vs_vms.svg)

---

## Container Advantages

| Feature | Containers | Virtual Machines |
|---------|------------|------------------|
| Startup Time | Seconds | Minutes |
| Size | MBs | GBs |
| Resource Usage | Low overhead | High overhead |
| Isolation | Process-level | Full system |
| Portability | Very high | Limited |

---

## Docker Architecture

![docker_architecture](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/docker_architecture.svg)

---

## Docker Engine Components

![docker_engine_components](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/docker_engine_components.svg)

---

## Container Runtime

![container_runtime](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/container_runtime.svg)

---

## Namespace Isolation

| Namespace | Purpose | Isolation |
|-----------|---------|-----------|
| PID | Process isolation | Process tree |
| NET | Network isolation | Network stack |
| MNT | Filesystem isolation | Mount points |
| UTS | System isolation | Hostname |
| IPC | IPC isolation | IPC resources |
| USER | User isolation | User/group IDs |

---

## Control Groups (cgroups)

![control_groups_cgroups](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/control_groups_cgroups.svg)

---

## Storage Drivers

![storage_drivers](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/storage_drivers.svg)

---

## Layer Architecture

![layer_architecture](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/layer_architecture.svg)

---

## Networking Internals

![networking_internals](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/networking_internals.svg)

---

## Security Architecture

![security_architecture](../../../../svg/courses/devops/docker-for-developers/02_under_the_hood/security_architecture.svg)
