# Docker Under the Hood
---

## Virtual Machine Basics

![0](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/0.png)

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

![1](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/1.png)

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

![2](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/2.png)

---

## Docker Engine Components

![3](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/3.png)

---

## Container Runtime

![4](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/4.png)

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

![5](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/5.png)

---

## Storage Drivers

![6](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/6.png)

---

## Layer Architecture

![7](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/7.png)

---

## Networking Internals

![8](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/8.png)

---

## Security Architecture

![9](../../../out/mermaid/marp/courses/docker-for-developers/01_under_the_hood.md/9.png)
