# Linux Namespaces
## Chapter 9: Resource Isolation and Control Groups

---

## Chapter Overview

- Namespace Concepts
- Types of Namespaces
- Control Groups (cgroups)
- Namespace Creation
- Namespace Management
- Network Priority
- Network Classification

---

## What are Namespaces

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_08_namespaces)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_08_namespaces)"/>
  <defs>
    <marker id="arrowd0_08_namespaces" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Types of Namespaces

1. Mount (mnt)
1. Process ID (pid)
1. Network (net)
1. IPC
1. UTS
1. User ID (user)
1. Control group (cgroup)

---

## Network Namespace Features

- Isolated network stack
- Private interfaces
- Private routing tables
- Private firewall rules
- Private sockets
- Private ports

---

## Creating Namespaces

```bash
# Create new network namespace
ip netns add myns

# List namespaces
ip netns list

# Execute command in namespace
ip netns exec myns command
```

---

## Namespace API

```c
// Clone with new namespace
int clone(int (*fn)(void *), void *stack, int flags, void *arg);

// Namespace flags
#define CLONE_NEWNS     0x00020000
#define CLONE_NEWUTS    0x04000000
#define CLONE_NEWIPC    0x08000000
#define CLONE_NEWPID    0x20000000
#define CLONE_NEWNET    0x40000000
#define CLONE_NEWUSER   0x10000000
#define CLONE_NEWCGROUP 0x02000000
```

---

## Creating Network Namespace

```c
int create_netns(void)
{
    int pid = clone(child_func,
                   stack + STACK_SIZE,
                   CLONE_NEWNET | SIGCHLD,
                   NULL);
    if (pid < 0) {
        perror("clone failed");
        return -1;
    }
    return pid;
}
```

---

## Virtual Interfaces

```bash
# Create veth pair
ip link add veth0 type veth peer name veth1

# Move one end to namespace
ip link set veth1 netns myns

# Configure interfaces
ip addr add 10.0.0.1/24 dev veth0
ip netns exec myns ip addr add 10.0.0.2/24 dev veth1
```

---

## Namespace Networking

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_08_namespaces)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_08_namespaces)"/>
  <defs>
    <marker id="arrowd1_08_namespaces" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Control Groups (cgroups)

```bash
# Create cgroup
mkdir /sys/fs/cgroup/net_cls/mygroup

# Set network class
echo 0x100001 > /sys/fs/cgroup/net_cls/mygroup/net_cls.classid

# Add process to cgroup
echo $$ > /sys/fs/cgroup/net_cls/mygroup/tasks
```

---

## Network Priority (net_prio)

```bash
# Set priority for interface
echo "eth0 5" > \
    /sys/fs/cgroup/net_prio/mygroup/net_prio.ifpriomap

# View priorities
cat /sys/fs/cgroup/net_prio/mygroup/net_prio.ifpriomap
```

---

## Network Classification (net_cls)

```bash
# Set traffic class
echo 0x100001 > \
    /sys/fs/cgroup/net_cls/mygroup/net_cls.classid

# Configure tc filter
tc filter add dev eth0 parent 1: \
    protocol ip prio 1 handle 1: \
    cgroup
```

---

## Inter-namespace Communication

```bash
# Create bridge
ip link add br0 type bridge
ip link set br0 up

# Connect namespaces
ip link set veth0 master br0
ip netns exec ns1 ip link set veth1 up
ip netns exec ns2 ip link set veth2 up
```

---

## DNS in Namespaces

```bash
# Copy resolv.conf
mkdir -p /etc/netns/myns
cp /etc/resolv.conf /etc/netns/myns/

# Custom DNS for namespace
echo "nameserver 8.8.8.8" > \
    /etc/netns/myns/resolv.conf
```

---

## Namespace Persistence

```bash
# Mount namespace directory
mount --bind /var/run/netns /var/run/netns

# Save namespace
ip netns add myns
ln -s /proc/$PID/ns/net /var/run/netns/myns
```

---

## Resource Limits with cgroups

```bash
# Set memory limit
echo "100M" > /sys/fs/cgroup/memory/mygroup/memory.limit_in_bytes

# Set CPU shares
echo "512" > /sys/fs/cgroup/cpu/mygroup/cpu.shares

# Set network priority
echo "10" > /sys/fs/cgroup/net_prio/mygroup/net_prio.priority
```

---

## Traffic Control Integration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_08_namespaces)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_08_namespaces)"/>
  <defs>
    <marker id="arrowd2_08_namespaces" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Monitoring Namespaces

```bash
# List processes in namespace
lsns -t net

# Show namespace details
ls -l /proc/$PID/ns/

# Monitor namespace traffic
ip netns exec myns tcpdump -i any
```

---

## Security Considerations

1. Namespace isolation
1. Resource limits
1. Network access control
1. User permissions
1. Process isolation
1. File system isolation

---

## Best Practices

1. Document namespace layout
1. Consistent naming
1. Resource management
1. Monitoring setup
1. Security configuration
1. Backup procedures

---

## Container Integration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_namespaces)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_namespaces)"/>
  <defs>
    <marker id="arrowd3_08_namespaces" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Troubleshooting

```bash
# Check namespace existence
ls -la /var/run/netns/

# Verify connectivity
ip netns exec myns ping 8.8.8.8

# Check routing
ip netns exec myns ip route show

# View interfaces
ip netns exec myns ip link show
```

---

## Performance Monitoring

```bash
# Monitor network usage
ip netns exec myns nethogs

# View interface statistics
ip netns exec myns ifconfig

# Monitor cgroup usage
cat /sys/fs/cgroup/net_cls/mygroup/memory.usage_in_bytes
```

---

## Summary

- Namespace concepts
- Resource isolation
- Network configuration
- cgroup management
- Traffic control
- Security considerations
