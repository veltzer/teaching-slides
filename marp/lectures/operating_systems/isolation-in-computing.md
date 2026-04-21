---
tags:
- concepts:isolation
- concepts:security
- concepts:virtualization
- infrastructure:containers
level: intermediate
category: operating-systems
audience:
- audiences:developers
- audiences:devops

---
# Isolation in Computing
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What is Isolation?

![title](svg/lectures/operating_systems/isolation-in-computing/title.svg)

---

## What is Isolation?: Details

Isolation is the fundamental principle of separating components to prevent unwanted interaction
Key benefits:
1. Security - Prevent unauthorized access
1. Stability - Contain failures
1. Performance - Resource management
1. Maintainability - Clear boundaries

---

## Why Isolation Matters

Modern computing systems are complex ecosystems

Without isolation:
1. Single failure crashes everything
1. Security breaches spread unchecked
1. Resource conflicts degrade performance
1. Debugging becomes impossible

---

## Isolation as an Engineering Concept

Isolation is not just a computing concept - it's fundamental engineering

Examples:
1. Electrical circuits - fuses and breakers
1. Ships - watertight compartments
1. Buildings - fireproof walls
1. Manufacturing - clean rooms

---

## Core Principles of Isolation

1. **Separation** - Components operate independently
1. **Controlled Communication** - Defined interfaces only
1. **Fault Containment** - Problems don't propagate
1. **Resource Boundaries** - Limited resource consumption

---

## Types of Isolation

1. **Physical Isolation** - Air-gapped systems
1. **Logical Isolation** - Software boundaries
1. **Temporal Isolation** - Time-based separation
1. **Resource Isolation** - CPU, memory, I/O limits

---

## Trade-offs in Isolation

![trade_offs_in_isolation](svg/lectures/operating_systems/isolation-in-computing/trade_offs_in_isolation.svg)

---

## Operating System Isolation

Operating systems are the foundation of isolation in computing

Key mechanisms:
1. Process isolation
1. Memory protection
1. User permissions
1. Kernel/user space separation

---

## Process Isolation

Each process runs in its own address space

```c
// Process A
int data = 42;
// Cannot access Process B's memory

// Process B
int secret = 100;
// Cannot access Process A's memory
```

---

## Memory Protection Unit (MPU): Overview

Hardware enforces memory boundaries

---

## Memory Protection Unit (MPU)

![memory_protection_unit_mpu](svg/lectures/operating_systems/isolation-in-computing/memory_protection_unit_mpu.svg)

---

## Protection Rings: Overview

CPU privilege levels enforce isolation

---

## Protection Rings

![protection_rings](svg/lectures/operating_systems/isolation-in-computing/protection_rings.svg)

---

## System Calls - Controlled Access

User programs request kernel services through system calls

```c
// User space
int fd = open("/file.txt", O_RDONLY);
// Trap to kernel
// Kernel validates request
// Returns to user space
```

---

## File System Permissions

Unix-style permissions provide access control

```bash
-rwxr-xr-- 1 alice users 1024 file.txt
# Owner: read, write, execute
# Group: read, execute
# Others: read only
```

---

## Namespaces in Linux

Linux namespaces isolate system resources

1. **PID** - Process IDs
1. **Network** - Network stack
1. **Mount** - Filesystem mounts
1. **UTS** - Hostname
1. **IPC** - Inter-process communication
1. **User** - User and group IDs
1. **Cgroup** - Control groups
1. **Time** - System time

---

## Control Groups (cgroups)

Resource limits and accounting

```bash
# Limit memory to 512MB
echo 536870912 > /sys/fs/cgroup/memory/myapp/memory.limit_in_bytes

# Limit CPU to 50%
echo 50000 > /sys/fs/cgroup/cpu/myapp/cpu.cfs_quota_us
```

---

## Docker Isolation: Overview

Docker builds on Linux kernel features for container isolation

---

## Docker Isolation

![docker_isolation](svg/lectures/operating_systems/isolation-in-computing/docker_isolation.svg)

---

## Docker Namespaces

Each container gets its own namespaces

```bash
docker run --rm alpine ps aux
# PID 1 is the container's init process
# Cannot see host processes
```

---

## Docker Filesystem Isolation

Union filesystems provide layered isolation

```dockerfile
FROM ubuntu:22.04      # Base layer (read-only)
RUN apt-get update     # New layer
COPY app /app          # New layer
# Each layer is isolated
```

---

## Docker Network Isolation

Containers have isolated network stacks

```bash
# Create isolated network
docker network create mynet

# Run container in network
docker run --network mynet nginx
```

---

## Docker Resource Limits

Cgroups enforce resource constraints

```bash
docker run --memory="512m" --cpus="0.5" myapp
# Limited to 512MB RAM and 50% of one CPU
```

---

## Docker Security Features

1. **Capabilities** - Fine-grained permissions
1. **Seccomp** - System call filtering
1. **AppArmor/SELinux** - Mandatory access control
1. **User namespaces** - Root in container != host root

---

## Kubernetes Isolation: Overview

K8s adds orchestration-level isolation

---

## Kubernetes Isolation

![kubernetes_isolation](svg/lectures/operating_systems/isolation-in-computing/kubernetes_isolation.svg)

---

## Kubernetes Namespaces

Logical isolation of cluster resources

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production

---
apiVersion: v1
kind: Namespace
metadata:
  name: development
```

---

## Pod Isolation

Pods are the smallest isolation unit

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    fsGroup: 2000
```

---

## Network Policies

Fine-grained network isolation

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

---

## Resource Quotas

Namespace-level resource limits

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
```

---

## Pod Security Standards

Three levels of security isolation

1. **Privileged** - Unrestricted
1. **Baseline** - Minimal restrictions
1. **Restricted** - Heavily restricted

---

## RBAC - Role-Based Access Control

Who can do what in the cluster

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

---

## Virtual Machines - Strong Isolation: Overview

VMs provide hardware-level isolation

---

## Virtual Machines - Strong Isolation

![virtual_machines_strong_isolation](svg/lectures/operating_systems/isolation-in-computing/virtual_machines_strong_isolation.svg)

---

## Hardware Virtualization Extensions

Modern CPUs provide isolation support

1. **Intel VT-x / AMD-V** - CPU virtualization
1. **Intel VT-d / AMD-Vi** - I/O virtualization
1. **Intel EPT / AMD RVI** - Memory virtualization

---

## Microservices Architecture: Overview

Isolation through service boundaries

---

## Microservices Architecture

![microservices_architecture](svg/lectures/operating_systems/isolation-in-computing/microservices_architecture.svg)

---

## Service Mesh - Network Isolation

Sidecar proxies manage inter-service communication

```yaml
# Istio example
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: httpbin-policy
spec:
  selector:
    matchLabels:
      app: httpbin
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/sleep"]
```

---

## Sandboxing Technologies

1. **gVisor** - User-space kernel
1. **Firecracker** - Lightweight VMs
1. **Kata Containers** - VMs with container UX
1. **WebAssembly** - Browser and server sandboxing

---

## Language-Level Isolation

Programming languages provide isolation

```rust
// Rust ownership prevents data races
fn main() {
    let data = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        // data is moved, no sharing
        println!("{:?}", data);
    });
    // Cannot use data here - compile error
}
```

---

## Database Isolation Levels

ACID transactions provide data isolation

1. **Read Uncommitted** - No isolation
1. **Read Committed** - No dirty reads
1. **Repeatable Read** - No phantom reads
1. **Serializable** - Full isolation

---

## Cloud Provider Isolation

Multi-tenancy in cloud platforms

1. **VPCs** - Virtual Private Clouds
1. **Security Groups** - Network ACLs
1. **IAM** - Identity and Access Management
1. **Dedicated Hosts** - Physical isolation

---

## Zero Trust Architecture: Overview

Never trust, always verify

---

## Zero Trust Architecture

![zero_trust_architecture](svg/lectures/operating_systems/isolation-in-computing/zero_trust_architecture.svg)

---

## Future of Isolation

Emerging technologies and trends

1. **Confidential Computing** - Encrypted memory
1. **Homomorphic Encryption** - Compute on encrypted data
1. **Secure Enclaves** - Intel SGX, ARM TrustZone
1. **WASM System Interface** - Portable sandboxing

---

## Best Practices for Isolation

1. **Defense in Depth** - Multiple layers
1. **Principle of Least Privilege** - Minimal permissions
1. **Fail Secure** - Safe defaults
1. **Regular Audits** - Verify isolation
1. **Monitoring** - Detect breaches

---

## Common Isolation Failures

1. **Container Breakout** - Escaping to host
1. **Side-Channel Attacks** - Spectre, Meltdown
1. **Privilege Escalation** - Getting root
1. **Network Segmentation Bypass** - VLAN hopping

---

## Testing Isolation

Verify your isolation mechanisms

```bash
# Test container isolation
docker run --rm alpine cat /etc/passwd
# Should only see container users

# Test network isolation
kubectl run test --image=alpine --rm -it -- nc -zv service.namespace 80
# Should fail if isolated
```

---

## Performance Impact of Isolation

Isolation has costs

1. **Context Switching** - CPU overhead
1. **Memory Overhead** - Duplication
1. **Network Latency** - Additional hops
1. **Storage Overhead** - Separate filesystems

---

## Choosing the Right Isolation Level

Consider your requirements:

1. **Security Requirements** - Threat model
1. **Performance Needs** - Latency, throughput
1. **Resource Constraints** - Memory, CPU
1. **Operational Complexity** - Management overhead
1. **Compliance** - Regulatory requirements

---

## Conclusion

Isolation is fundamental to modern computing

Key takeaways:
1. Multiple layers provide defense in depth
1. Choose appropriate isolation for your needs
1. Understand the trade-offs
1. Test and verify your isolation
1. Stay updated on emerging threats

---

## Resources for Further Learning

1. **Books**
    - "Operating Systems: Three Easy Pieces"
    - "Container Security" by Liz Rice
1. **Documentation**
    - Linux kernel documentation
    - Docker security documentation
    - Kubernetes security best practices
1. **Tools**
    - `unshare` - Create namespaces
    - `nsenter` - Enter namespaces
    - `systemd-nspawn` - Container tool
