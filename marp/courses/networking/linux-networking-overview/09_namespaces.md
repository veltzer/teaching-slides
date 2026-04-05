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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Linux Namespace Isolation</text>
  <rect x="20" y="30" width="560" height="160" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5" fill-opacity="0.3"/>
  <text x="300" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#7b1fa2">Linux Kernel</text>
  <rect x="40" y="60" width="155" height="110" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="117" y="80" text-anchor="middle" font-size="11" font-weight="bold">NS: default</text>
  <text x="117" y="97" text-anchor="middle" font-size="10" fill="#666">eth0, lo</text>
  <text x="117" y="112" text-anchor="middle" font-size="10" fill="#666">routing table</text>
  <text x="117" y="127" text-anchor="middle" font-size="10" fill="#666">iptables rules</text>
  <text x="117" y="142" text-anchor="middle" font-size="10" fill="#666">sockets, ports</text>
  <rect x="222" y="60" width="155" height="110" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="11" font-weight="bold">NS: myns1</text>
  <text x="300" y="97" text-anchor="middle" font-size="10" fill="#666">veth1, lo</text>
  <text x="300" y="112" text-anchor="middle" font-size="10" fill="#666">own routes</text>
  <text x="300" y="127" text-anchor="middle" font-size="10" fill="#666">own firewall</text>
  <text x="300" y="142" text-anchor="middle" font-size="10" fill="#666">own sockets</text>
  <rect x="405" y="60" width="155" height="110" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="482" y="80" text-anchor="middle" font-size="11" font-weight="bold">NS: myns2</text>
  <text x="482" y="97" text-anchor="middle" font-size="10" fill="#666">veth3, lo</text>
  <text x="482" y="112" text-anchor="middle" font-size="10" fill="#666">own routes</text>
  <text x="482" y="127" text-anchor="middle" font-size="10" fill="#666">own firewall</text>
  <text x="482" y="142" text-anchor="middle" font-size="10" fill="#666">own sockets</text>
  <text x="300" y="160" text-anchor="middle" font-size="10" fill="#7b1fa2">Each namespace has a fully isolated network stack</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Veth Pair Connecting Namespaces</text>
  <rect x="30" y="35" width="200" height="120" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="130" y="55" text-anchor="middle" font-size="11" font-weight="bold">Default Namespace</text>
  <rect x="60" y="65" width="140" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="130" y="87" text-anchor="middle" font-size="11">veth0 (10.0.0.1)</text>
  <text x="130" y="130" text-anchor="middle" font-size="10" fill="#666">ip addr add 10.0.0.1/24</text>
  <rect x="370" y="35" width="200" height="120" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="470" y="55" text-anchor="middle" font-size="11" font-weight="bold">Namespace: myns</text>
  <rect x="400" y="65" width="140" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="470" y="87" text-anchor="middle" font-size="11">veth1 (10.0.0.2)</text>
  <text x="470" y="130" text-anchor="middle" font-size="10" fill="#666">ip netns exec myns</text>
  <line x1="200" y1="82" x2="400" y2="82" stroke="#c62828" stroke-width="3" stroke-dasharray="8,4"/>
  <text x="300" y="77" text-anchor="middle" font-size="10" fill="#c62828" font-weight="bold">veth pair link</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#666">ip link add veth0 type veth peer name veth1 | ip link set veth1 netns myns</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Traffic Control with cgroups net_cls</text>
  <rect x="30" y="35" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="55" text-anchor="middle" font-size="11" font-weight="bold">Process</text>
  <text x="90" y="72" text-anchor="middle" font-size="10" fill="#666">cgroup: mygroup</text>
  <rect x="185" y="35" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="245" y="55" text-anchor="middle" font-size="11" font-weight="bold">net_cls</text>
  <text x="245" y="72" text-anchor="middle" font-size="10" fill="#666">classid 0x100001</text>
  <rect x="340" y="35" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="55" text-anchor="middle" font-size="11" font-weight="bold">tc (qdisc)</text>
  <text x="400" y="72" text-anchor="middle" font-size="10" fill="#666">Filter by classid</text>
  <rect x="495" y="35" width="80" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="535" y="55" text-anchor="middle" font-size="11" font-weight="bold">eth0</text>
  <text x="535" y="72" text-anchor="middle" font-size="10" fill="#666">Shaped</text>
  <line x1="150" y1="62" x2="185" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_08_namespaces)"/>
  <line x1="305" y1="62" x2="340" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_08_namespaces)"/>
  <line x1="460" y1="62" x2="495" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_08_namespaces)"/>
  <rect x="30" y="110" width="545" height="55" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="5" stroke-dasharray="5,3"/>
  <text x="300" y="132" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">net_prio: Set per-interface priority for cgroup processes</text>
  <text x="300" y="150" text-anchor="middle" font-size="10" fill="#666">echo "eth0 5" > /sys/fs/cgroup/net_prio/mygroup/net_prio.ifpriomap</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Container Networking with Namespaces</text>
  <rect x="20" y="30" width="560" height="160" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5" fill-opacity="0.2"/>
  <text x="300" y="48" text-anchor="middle" font-size="11" font-weight="bold" fill="#7b1fa2">Host (default namespace)</text>
  <rect x="40" y="55" width="130" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="73" text-anchor="middle" font-size="10" font-weight="bold">Container A</text>
  <text x="105" y="88" text-anchor="middle" font-size="10" fill="#666">net ns: ctn_a</text>
  <text x="105" y="103" text-anchor="middle" font-size="10" fill="#666">eth0 (veth pair)</text>
  <rect x="430" y="55" width="130" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="73" text-anchor="middle" font-size="10" font-weight="bold">Container B</text>
  <text x="495" y="88" text-anchor="middle" font-size="10" fill="#666">net ns: ctn_b</text>
  <text x="495" y="103" text-anchor="middle" font-size="10" fill="#666">eth0 (veth pair)</text>
  <rect x="210" y="55" width="180" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="300" y="72" text-anchor="middle" font-size="11" font-weight="bold">Linux Bridge (br0)</text>
  <text x="300" y="87" text-anchor="middle" font-size="10" fill="#666">L2 switching</text>
  <line x1="170" y1="80" x2="210" y2="75" stroke="#333" stroke-width="2"/>
  <line x1="390" y1="75" x2="430" y2="80" stroke="#333" stroke-width="2"/>
  <rect x="245" y="130" width="110" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="148" text-anchor="middle" font-size="10" font-weight="bold">eth0 (host NIC)</text>
  <text x="300" y="162" text-anchor="middle" font-size="10" fill="#666">NAT / routing</text>
  <line x1="300" y1="95" x2="300" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_namespaces)"/>
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
