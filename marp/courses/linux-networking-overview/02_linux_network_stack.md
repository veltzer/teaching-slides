# The Linux Networking Stack
## Chapter 2: Architecture and Implementation

---

## Chapter Overview

- Network Device Drivers and `net_device`
- Linux Protocol Stack Implementation
- Socket Interface
- Protocol-Socket Communication
- Link Layer Operations
- User Space API Access

---

## Linux Network Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_01_linux_network_stack)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_01_linux_network_stack)"/>
  <defs>
    <marker id="arrowd0_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Network Device Interface

**Key Components:**
- `net_device` structure
- Device registration
- Interface flags
- Statistics tracking
- Queue management

---

## The net_device Structure

```c
struct net_device {
    char            name[IFNAMSIZ];
    unsigned long   state;
    struct net_device_stats stats;
    const struct net_device_ops *netdev_ops;
    const struct ethtool_ops *ethtool_ops;
    unsigned int    flags;
    // ... more fields
};
```

---

## Network Device States

**Common States:**
- `__LINK_STATE_START`
- `__LINK_STATE_PRESENT`
- `__LINK_STATE_NOCARRIER`
- `__LINK_STATE_LINKWATCH_PENDING`
- `__LINK_STATE_DORMANT`

---

## Network Device Operations

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_01_linux_network_stack)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_01_linux_network_stack)"/>
  <defs>
    <marker id="arrowd1_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## The Protocol Stack

**Layers:**
1. Socket Layer
1. Transport Layer
1. Network Layer
1. Link Layer

---

## Socket Layer Implementation

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_01_linux_network_stack)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_01_linux_network_stack)"/>
  <defs>
    <marker id="arrowd2_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Socket Structure

```c
struct socket {
    socket_state            state;
    short                   type;
    const struct proto_ops  *ops;
    struct file            *file;
    struct sock            *sk;
    const struct proto     *proto;
};
```

---

## Socket States

| State | Description |
|-------|-------------|
| SS_FREE | Not allocated |
| SS_UNCONNECTED | Unconnected |
| SS_CONNECTING | In process of connecting |
| SS_CONNECTED | Connected |
| SS_DISCONNECTING | In process of disconnecting |

---

## Protocol Operations

**Key Operations:**
- `create()`
- `bind()`
- `connect()`
- `accept()`
- `sendmsg()`
- `recvmsg()`

---

## Socket Buffer (sk_buff)

```c
struct sk_buff {
    struct sk_buff        *next;
    struct sk_buff        *prev;
    struct sock          *sk;
    struct net_device    *dev;
    unsigned int          len;
    unsigned char        *data;
    // ... more fields
};
```

---

## SK Buffer Management

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_01_linux_network_stack)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_01_linux_network_stack)"/>
  <defs>
    <marker id="arrowd3_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Protocol Implementation

**TCP Implementation:**
- Connection handling
- Window management
- Congestion control
- Error recovery

---

## TCP State Machine

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="40" width="300" height="70" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="14">Diagram</text>
</svg>

---

## Network Layer (IP)

**Functions:**
- Routing
- Fragmentation
- Reassembly
- Header processing

---

## IP Header Processing

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_01_linux_network_stack)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_01_linux_network_stack)"/>
  <defs>
    <marker id="arrowd5_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Link Layer Operations

**Key Functions:**
- Frame transmission
- Frame reception
- MAC addressing
- Error detection

---

## Network Device Queuing

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_01_linux_network_stack)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_01_linux_network_stack)"/>
  <defs>
    <marker id="arrowd6_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Queue Disciplines (qdisc)

**Types:**
- FIFO
- Priority
- Fair queuing
- Token bucket
- Hierarchical

---

## User Space API

**Key Interfaces:**
- Socket API
- NETLINK
- IOCTL
- Proc filesystem
- Sysfs

---

## Socket API Functions

| Function | Purpose |
|----------|---------|
| socket() | Create socket |
| bind() | Bind to address |
| listen() | Listen for connections |
| accept() | Accept connection |
| connect() | Initiate connection |
| send/recv | Data transfer |

---

## NETLINK Interface

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_01_linux_network_stack)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_01_linux_network_stack)"/>
  <defs>
    <marker id="arrowd7_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## IOCTL Operations

**Common Operations:**
- Get/Set interface flags
- Get/Set interface address
- Get/Set routing table
- Get/Set ARP table

---

## Proc Filesystem

**Key Files:**
- `/proc/net/dev`
- `/proc/net/tcp`
- `/proc/net/udp`
- `/proc/net/route`
- `/proc/net/arp`

---

## Sysfs Network Interface

**Location:** `/sys/class/net`

**Per-device entries:**
- `address`
- `mtu`
- `flags`
- `statistics`
- `queues`

---

## Debug and Monitoring

**Tools:**
- `netstat`
- `ss`
- `ip`
- `ethtool`
- `tcpdump`

---

## Performance Considerations

- Interrupt handling
- Buffer management
- Queue optimization
- Protocol overhead
- Memory allocation

---

## Summary

- Complex layered architecture
- Efficient packet handling
- Flexible device interface
- Rich user space API
- Extensive monitoring capabilities
