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

![linux_network_architecture](svg/courses/networking/linux-networking-overview/02_linux_network_stack/linux_network_architecture.svg)

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

![network_device_operations](svg/courses/networking/linux-networking-overview/02_linux_network_stack/network_device_operations.svg)

---

## The Protocol Stack

**Layers:**
1. Socket Layer
1. Transport Layer
1. Network Layer
1. Link Layer

---

## Socket Layer Implementation

![socket_layer_implementation](svg/courses/networking/linux-networking-overview/02_linux_network_stack/socket_layer_implementation.svg)

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

![sk_buffer_management](svg/courses/networking/linux-networking-overview/02_linux_network_stack/sk_buffer_management.svg)

---

## Protocol Implementation

**TCP Implementation:**
- Connection handling
- Window management
- Congestion control
- Error recovery

---

## TCP State Machine

![tcp_state_machine](svg/courses/networking/linux-networking-overview/02_linux_network_stack/tcp_state_machine.svg)

---

## Network Layer (IP)

**Functions:**
- Routing
- Fragmentation
- Reassembly
- Header processing

---

## IP Header Processing

![ip_header_processing](svg/courses/networking/linux-networking-overview/02_linux_network_stack/ip_header_processing.svg)

---

## Link Layer Operations

**Key Functions:**
- Frame transmission
- Frame reception
- MAC addressing
- Error detection

---

## Network Device Queuing

![network_device_queuing](svg/courses/networking/linux-networking-overview/02_linux_network_stack/network_device_queuing.svg)

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

![netlink_interface](svg/courses/networking/linux-networking-overview/02_linux_network_stack/netlink_interface.svg)

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
