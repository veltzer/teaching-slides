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
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Linux Network Stack Layers</text>
  <rect x="100" y="25" width="400" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="45" text-anchor="middle" font-size="11">User Space: Applications (socket API)</text>
  <rect x="100" y="60" width="400" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="80" text-anchor="middle" font-size="11">Socket Layer: struct socket, proto_ops</text>
  <rect x="100" y="95" width="400" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="115" text-anchor="middle" font-size="11">Transport: TCP / UDP (struct sock)</text>
  <rect x="100" y="130" width="400" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="150" text-anchor="middle" font-size="11">Network: IP routing, netfilter hooks</text>
  <rect x="100" y="165" width="400" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="185" text-anchor="middle" font-size="11">Device/Link: net_device, drivers, NIC</text>
  <text x="60" y="45" text-anchor="middle" font-size="10" fill="#666">User</text>
  <text x="60" y="115" text-anchor="middle" font-size="10" fill="#666">Kernel</text>
  <line x1="25" y1="55" x2="95" y2="55" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
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
  <defs>
    <marker id="arrowd1_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">net_device Operations Flow</text>
  <rect x="30" y="30" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="85" y="52" text-anchor="middle" font-size="10">ndo_open()</text>
  <text x="85" y="66" text-anchor="middle" font-size="10">ndo_stop()</text>
  <rect x="170" y="30" width="120" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="230" y="52" text-anchor="middle" font-size="10">ndo_start_xmit()</text>
  <text x="230" y="66" text-anchor="middle" font-size="10">TX path</text>
  <rect x="320" y="30" width="120" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="380" y="52" text-anchor="middle" font-size="10">netif_rx()</text>
  <text x="380" y="66" text-anchor="middle" font-size="10">RX path / NAPI</text>
  <rect x="470" y="30" width="110" height="50" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="525" y="52" text-anchor="middle" font-size="10">ndo_get_stats()</text>
  <text x="525" y="66" text-anchor="middle" font-size="10">ndo_do_ioctl()</text>
  <line x1="140" y1="55" x2="170" y2="55" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_01_linux_network_stack)"/>
  <line x1="290" y1="55" x2="320" y2="55" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_01_linux_network_stack)"/>
  <line x1="440" y1="55" x2="470" y2="55" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_01_linux_network_stack)"/>
  <rect x="120" y="110" width="360" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="135" text-anchor="middle" font-size="11">struct net_device_ops (function pointers)</text>
  <line x1="300" y1="80" x2="300" y2="110" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_01_linux_network_stack)"/>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#666">Registered via register_netdev() during driver init</text>
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
  <defs>
    <marker id="arrowd2_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Socket Layer Architecture</text>
  <rect x="30" y="28" width="160" height="60" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="48" text-anchor="middle" font-size="11" font-weight="bold">struct socket</text>
  <text x="110" y="65" text-anchor="middle" font-size="10">state, type, ops</text>
  <text x="110" y="80" text-anchor="middle" font-size="10">file, sk, proto</text>
  <rect x="220" y="28" width="160" height="60" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="48" text-anchor="middle" font-size="11" font-weight="bold">struct sock (sk)</text>
  <text x="300" y="65" text-anchor="middle" font-size="10">protocol state</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">buffers, timers</text>
  <rect x="410" y="28" width="160" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="490" y="48" text-anchor="middle" font-size="11" font-weight="bold">proto_ops</text>
  <text x="490" y="65" text-anchor="middle" font-size="10">bind, connect</text>
  <text x="490" y="80" text-anchor="middle" font-size="10">sendmsg, recvmsg</text>
  <line x1="190" y1="58" x2="220" y2="58" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_01_linux_network_stack)"/>
  <line x1="380" y1="58" x2="410" y2="58" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_01_linux_network_stack)"/>
  <rect x="120" y="110" width="360" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="132" text-anchor="middle" font-size="11">sys_socket() / sys_bind() / sys_connect() / sys_sendmsg()</text>
  <line x1="300" y1="88" x2="300" y2="110" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_01_linux_network_stack)"/>
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="#666">System calls map to socket-&gt;ops-&gt;method()</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#666">BSD socket layer provides uniform interface</text>
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
  <defs>
    <marker id="arrowd3_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">sk_buff Data Flow</text>
  <rect x="30" y="30" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="90" y="50" text-anchor="middle" font-size="10" font-weight="bold">alloc_skb()</text>
  <text x="90" y="65" text-anchor="middle" font-size="10">Allocate buffer</text>
  <text x="90" y="78" text-anchor="middle" font-size="9" fill="#666">head, data, tail, end</text>
  <rect x="170" y="30" width="110" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="225" y="50" text-anchor="middle" font-size="10" font-weight="bold">skb_reserve()</text>
  <text x="225" y="65" text-anchor="middle" font-size="10">Reserve headroom</text>
  <text x="225" y="78" text-anchor="middle" font-size="9" fill="#666">for L2/L3 headers</text>
  <rect x="300" y="30" width="110" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="355" y="50" text-anchor="middle" font-size="10" font-weight="bold">skb_put()</text>
  <text x="355" y="65" text-anchor="middle" font-size="10">Add data at tail</text>
  <text x="355" y="78" text-anchor="middle" font-size="9" fill="#666">payload grows down</text>
  <rect x="430" y="30" width="110" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="485" y="50" text-anchor="middle" font-size="10" font-weight="bold">skb_push()</text>
  <text x="485" y="65" text-anchor="middle" font-size="10">Add header at head</text>
  <text x="485" y="78" text-anchor="middle" font-size="9" fill="#666">prepend headers</text>
  <line x1="150" y1="57" x2="170" y2="57" stroke="#333" stroke-width="1" marker-end="url(#arrowd3_01_linux_network_stack)"/>
  <line x1="280" y1="57" x2="300" y2="57" stroke="#333" stroke-width="1" marker-end="url(#arrowd3_01_linux_network_stack)"/>
  <line x1="410" y1="57" x2="430" y2="57" stroke="#333" stroke-width="1" marker-end="url(#arrowd3_01_linux_network_stack)"/>
  <rect x="50" y="110" width="500" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="85" y="130" font-size="10" fill="#666">head</text>
  <rect x="120" y="113" width="60" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="150" y="131" text-anchor="middle" font-size="9">headroom</text>
  <rect x="180" y="113" width="40" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="200" y="131" text-anchor="middle" font-size="9">L2</text>
  <rect x="220" y="113" width="40" height="28" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="240" y="131" text-anchor="middle" font-size="9">L3</text>
  <rect x="260" y="113" width="40" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="280" y="131" text-anchor="middle" font-size="9">L4</text>
  <rect x="300" y="113" width="180" height="28" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="390" y="131" text-anchor="middle" font-size="9">Payload Data</text>
  <text x="510" y="130" font-size="10" fill="#666">tail/end</text>
  <text x="300" y="168" text-anchor="middle" font-size="10" fill="#666">sk_buff manages packet data through all protocol layers</text>
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
  <defs>
    <marker id="arrowd5_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">IP Header Processing Path</text>
  <rect x="20" y="30" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="70" y="45" text-anchor="middle" font-size="10">NIC Driver</text>
  <text x="70" y="58" text-anchor="middle" font-size="10">netif_rx()</text>
  <rect x="150" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="45" text-anchor="middle" font-size="10">ip_rcv()</text>
  <text x="200" y="58" text-anchor="middle" font-size="10">validate header</text>
  <rect x="280" y="30" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="330" y="45" text-anchor="middle" font-size="10">ip_route_input</text>
  <text x="330" y="58" text-anchor="middle" font-size="10">routing decision</text>
  <rect x="150" y="100" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="115" text-anchor="middle" font-size="10">ip_local_deliver</text>
  <text x="200" y="128" text-anchor="middle" font-size="10">to transport</text>
  <rect x="410" y="30" width="100" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="460" y="45" text-anchor="middle" font-size="10">ip_forward()</text>
  <text x="460" y="58" text-anchor="middle" font-size="10">forward pkt</text>
  <rect x="410" y="100" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="460" y="115" text-anchor="middle" font-size="10">ip_output()</text>
  <text x="460" y="128" text-anchor="middle" font-size="10">send to NIC</text>
  <line x1="120" y1="50" x2="150" y2="50" stroke="#333" stroke-width="1" marker-end="url(#arrowd5_01_linux_network_stack)"/>
  <line x1="250" y1="50" x2="280" y2="50" stroke="#333" stroke-width="1" marker-end="url(#arrowd5_01_linux_network_stack)"/>
  <line x1="330" y1="70" x2="200" y2="100" stroke="#1565c0" stroke-width="1" marker-end="url(#arrowd5_01_linux_network_stack)"/>
  <line x1="380" y1="50" x2="410" y2="50" stroke="#c62828" stroke-width="1" marker-end="url(#arrowd5_01_linux_network_stack)"/>
  <line x1="460" y1="70" x2="460" y2="100" stroke="#333" stroke-width="1" marker-end="url(#arrowd5_01_linux_network_stack)"/>
  <text x="160" y="85" font-size="9" fill="#1565c0">local</text>
  <text x="395" y="42" font-size="9" fill="#c62828">fwd</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#666">Netfilter hooks called at PRE_ROUTING, FORWARD, LOCAL_IN, POST_ROUTING</text>
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
  <defs>
    <marker id="arrowd6_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Network Device Queuing</text>
  <rect x="20" y="30" width="110" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="75" y="48" text-anchor="middle" font-size="10">Transport Layer</text>
  <text x="75" y="62" text-anchor="middle" font-size="10">(TCP/UDP)</text>
  <rect x="160" y="30" width="120" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="48" text-anchor="middle" font-size="10">Queueing Disc</text>
  <text x="220" y="62" text-anchor="middle" font-size="10">(qdisc)</text>
  <rect x="310" y="30" width="110" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="365" y="48" text-anchor="middle" font-size="10">dev_queue_xmit</text>
  <text x="365" y="62" text-anchor="middle" font-size="10">TX queue</text>
  <rect x="450" y="30" width="110" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="505" y="48" text-anchor="middle" font-size="10">NIC Driver</text>
  <text x="505" y="62" text-anchor="middle" font-size="10">hard_start_xmit</text>
  <line x1="130" y1="52" x2="160" y2="52" stroke="#333" stroke-width="1" marker-end="url(#arrowd6_01_linux_network_stack)"/>
  <line x1="280" y1="52" x2="310" y2="52" stroke="#333" stroke-width="1" marker-end="url(#arrowd6_01_linux_network_stack)"/>
  <line x1="420" y1="52" x2="450" y2="52" stroke="#333" stroke-width="1" marker-end="url(#arrowd6_01_linux_network_stack)"/>
  <rect x="100" y="100" width="100" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="122" text-anchor="middle" font-size="10">pfifo_fast</text>
  <rect x="220" y="100" width="80" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="260" y="122" text-anchor="middle" font-size="10">HTB</text>
  <rect x="320" y="100" width="80" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="122" text-anchor="middle" font-size="10">SFQ</text>
  <rect x="420" y="100" width="80" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="460" y="122" text-anchor="middle" font-size="10">TBF</text>
  <text x="300" y="155" text-anchor="middle" font-size="11" fill="#666">Common Queue Disciplines</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#666">tc qdisc add dev eth0 root [discipline] [params]</text>
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
  <defs>
    <marker id="arrowd7_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
    <marker id="arrowd7b_01_linux_network_stack" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">NETLINK Interface</text>
  <rect x="30" y="30" width="240" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="150" y="50" text-anchor="middle" font-size="11" font-weight="bold">User Space</text>
  <text x="150" y="68" text-anchor="middle" font-size="10">ip, iproute2, NetworkManager</text>
  <text x="150" y="83" text-anchor="middle" font-size="10">socket(AF_NETLINK, ...)</text>
  <rect x="330" y="30" width="240" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="450" y="50" text-anchor="middle" font-size="11" font-weight="bold">Kernel Space</text>
  <text x="450" y="68" text-anchor="middle" font-size="10">NETLINK_ROUTE, NETLINK_XFRM</text>
  <text x="450" y="83" text-anchor="middle" font-size="10">NETLINK_NETFILTER, NETLINK_GENERIC</text>
  <line x1="270" y1="55" x2="330" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_01_linux_network_stack)"/>
  <line x1="330" y1="75" x2="270" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowd7b_01_linux_network_stack)"/>
  <text x="300" y="50" text-anchor="middle" font-size="9" fill="#666">send</text>
  <text x="300" y="90" text-anchor="middle" font-size="9" fill="#666">recv</text>
  <rect x="80" y="120" width="440" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="142" text-anchor="middle" font-size="11">Asynchronous, multicast-capable, bidirectional IPC</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#666">Replaces ioctl() for modern network configuration</text>
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
