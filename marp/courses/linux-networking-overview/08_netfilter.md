# Netfilters
## Chapter 8: Network Packet Filtering Framework

---

## Chapter Overview

- User Space Implementation
- Hook Points
- Hook Functions
- Registration Process
- Removal Process
- Kernel Space Implementation

---

## What are Netfilters

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Netfilter: Kernel Packet Processing Framework</text>
  <rect x="30" y="30" width="160" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="50" text-anchor="middle" font-size="11" font-weight="bold">User Space</text>
  <text x="110" y="67" text-anchor="middle" font-size="10" fill="#666">iptables / nftables</text>
  <text x="110" y="82" text-anchor="middle" font-size="10" fill="#666">libnetfilter_queue</text>
  <text x="110" y="97" text-anchor="middle" font-size="10" fill="#666">conntrack CLI</text>
  <rect x="220" y="30" width="160" height="75" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">Netfilter Hooks</text>
  <text x="300" y="67" text-anchor="middle" font-size="10" fill="#666">PRE/POST ROUTING</text>
  <text x="300" y="82" text-anchor="middle" font-size="10" fill="#666">INPUT / OUTPUT</text>
  <text x="300" y="97" text-anchor="middle" font-size="10" fill="#666">FORWARD</text>
  <rect x="410" y="30" width="160" height="75" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="50" text-anchor="middle" font-size="11" font-weight="bold">Tables</text>
  <text x="490" y="67" text-anchor="middle" font-size="10" fill="#666">filter (default)</text>
  <text x="490" y="82" text-anchor="middle" font-size="10" fill="#666">nat / mangle</text>
  <text x="490" y="97" text-anchor="middle" font-size="10" fill="#666">raw / security</text>
  <line x1="190" y1="67" x2="220" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_07_netfilter)"/>
  <line x1="380" y1="67" x2="410" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_07_netfilter)"/>
  <rect x="30" y="130" width="540" height="45" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="5" stroke-dasharray="5,3"/>
  <text x="300" y="150" text-anchor="middle" font-size="11" fill="#333">Each hook point invokes registered callback functions (nf_hook_ops)</text>
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="#666">Verdicts: NF_ACCEPT | NF_DROP | NF_QUEUE | NF_STOLEN | NF_REPEAT</text>
  <defs>
    <marker id="arrowd0_07_netfilter" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Hook Points

```c
// Available hook points
enum nf_inet_hooks {
    NF_INET_PRE_ROUTING,
    NF_INET_LOCAL_IN,
    NF_INET_FORWARD,
    NF_INET_LOCAL_OUT,
    NF_INET_POST_ROUTING
};
```

---

## Hook Function Prototype

```c
unsigned int (*nf_hook_ops)(void *priv,
                           struct sk_buff *skb,
                           const struct nf_hook_state *state);

// Return values
#define NF_DROP     0
#define NF_ACCEPT   1
#define NF_STOLEN   2
#define NF_QUEUE    3
#define NF_REPEAT   4
```

---

## Implementing Hook Functions

```c
static unsigned int my_hook_func(void *priv,
                               struct sk_buff *skb,
                               const struct nf_hook_state *state)
{
    // Packet processing logic
    if (should_drop_packet(skb))
        return NF_DROP;

    return NF_ACCEPT;
}
```

---

## Hook Registration Structure

```c
struct nf_hook_ops {
    // Function to call
    nf_hookfn *hook;

    // Hook point to attach to
    struct net_device *dev;
    void *priv;
    u_int8_t pf;         // Protocol family
    unsigned int hooknum; // Hook number
    int priority;        // Priority in chain
};
```

---

## Registering a Netfilter

```c
static struct nf_hook_ops my_nfho = {
    .hook = my_hook_func,
    .pf = PF_INET,           // IPv4
    .hooknum = NF_INET_PRE_ROUTING,
    .priority = NF_IP_PRI_FIRST,
};

// Register the hook
nf_register_net_hook(&init_net, &my_nfho);
```

---

## Packet Flow Through Hooks

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Packet Flow Through Netfilter Hooks</text>
  <rect x="10" y="75" width="65" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="42" y="97" text-anchor="middle" font-size="10" font-weight="bold">NIC In</text>
  <rect x="95" y="75" width="80" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="135" y="90" text-anchor="middle" font-size="10" font-weight="bold">PRE-</text>
  <text x="135" y="102" text-anchor="middle" font-size="10" font-weight="bold">ROUTING</text>
  <rect x="195" y="40" width="60" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="60" text-anchor="middle" font-size="10" font-weight="bold">Routing</text>
  <rect x="195" y="120" width="70" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="140" text-anchor="middle" font-size="10" font-weight="bold">FORWARD</text>
  <rect x="275" y="75" width="60" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="305" y="97" text-anchor="middle" font-size="10" font-weight="bold">INPUT</text>
  <rect x="355" y="75" width="60" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="385" y="97" text-anchor="middle" font-size="10" font-weight="bold">Local</text>
  <rect x="435" y="75" width="60" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="465" y="97" text-anchor="middle" font-size="10" font-weight="bold">OUTPUT</text>
  <rect x="435" y="120" width="80" height="30" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="133" text-anchor="middle" font-size="10" font-weight="bold">POSTROUTING</text>
  <rect x="535" y="75" width="55" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="562" y="97" text-anchor="middle" font-size="10" font-weight="bold">NIC Out</text>
  <line x1="75" y1="92" x2="95" y2="92" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="175" y1="85" x2="195" y2="60" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="225" y1="70" x2="275" y2="88" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="225" y1="70" x2="225" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="335" y1="92" x2="355" y2="92" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="415" y1="92" x2="435" y2="92" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="265" y1="135" x2="435" y2="135" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="495" y1="92" x2="495" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <line x1="515" y1="135" x2="535" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_07_netfilter)"/>
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#666">5 hook points intercept packets at different stages of processing</text>
  <defs>
    <marker id="arrowd1_07_netfilter" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## User Space Implementation

```c
#include <linux/netfilter_ipv4.h>
#include <libnetfilter_queue/libnetfilter_queue.h>

static int callback(struct nfq_q_handle *qh,
                   struct nfgenmsg *nfmsg,
                   struct nfq_data *nfa,
                   void *data)
{
    // Process packet
    return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
}
```

---

## Queue Handler Setup

```c
struct nfq_handle *h;
struct nfq_q_handle *qh;

h = nfq_open();
if (!h) {
    fprintf(stderr, "Error: nfq_open()\n");
    exit(1);
}

qh = nfq_create_queue(h, 0, &callback, NULL);
if (!qh) {
    fprintf(stderr, "Error: nfq_create_queue()\n");
    exit(1);
}
```

---

## Packet Processing Loop

```c
int fd = nfq_fd(h);
char buf[4096];

while ((rv = recv(fd, buf, sizeof(buf), 0)) >= 0) {
    nfq_handle_packet(h, buf, rv);
}

nfq_destroy_queue(qh);
nfq_close(h);
```

---

## Kernel Space Implementation

```c
struct nf_hook_ops nfho = {
    .hook = hook_func,
    .hooknum = NF_INET_PRE_ROUTING,
    .pf = NFPROTO_IPV4,
    .priority = NF_IP_PRI_FIRST
};

static int __init my_module_init(void)
{
    return nf_register_net_hook(&init_net, &nfho);
}

static void __exit my_module_exit(void)
{
    nf_unregister_net_hook(&init_net, &nfho);
}
```

---

## Hook Priority Levels

```c
// Standard priority levels
#define NF_IP_PRI_FIRST      INT_MIN
#define NF_IP_PRI_CONNTRACK  -200
#define NF_IP_PRI_MANGLE     -150
#define NF_IP_PRI_NAT_DST    -100
#define NF_IP_PRI_FILTER     0
#define NF_IP_PRI_NAT_SRC    100
#define NF_IP_PRI_LAST       INT_MAX
```

---

## Packet Verdict Decisions

<div class="columns">
<div>

**Accept:**
- Continue processing
- Normal packet flow
- Next hook point

</div>
<div>

**Drop:**
- Discard packet
- Stop processing
- No notification

</div>
</div>

---

## Connection Tracking

```c
// Get connection tracking info
struct nf_conn *ct = nf_ct_get(skb, &ctinfo);
if (!ct)
    return NF_DROP;

// Check connection state
if (ctinfo == IP_CT_NEW) {
    // New connection logic
}
```

---

## Packet Manipulation

```c
static unsigned int hook_func(void *priv,
                            struct sk_buff *skb,
                            const struct nf_hook_state *state)
{
    struct iphdr *iph;

    if (!skb)
        return NF_ACCEPT;

    iph = ip_hdr(skb);
    if (iph->protocol == IPPROTO_TCP) {
        // Modify TCP packet
    }

    return NF_ACCEPT;
}
```

---

## Error Handling

```c
static unsigned int hook_func(void *priv,
                            struct sk_buff *skb,
                            const struct nf_hook_state *state)
{
    if (!skb)
        return NF_ACCEPT;

    if (skb_linearize(skb) < 0)
        return NF_DROP;

    if (!pskb_may_pull(skb, sizeof(struct iphdr)))
        return NF_DROP;

    return NF_ACCEPT;
}
```

---

## Performance Considerations

1. Hook placement
1. Processing overhead
1. Memory allocation
1. Packet copying
1. Lock contention
1. Queue management

---

## Debugging Tools

```bash
# View netfilter hooks
cat /proc/net/nf_hook_info

# Connection tracking
cat /proc/net/nf_conntrack

# Queue statistics
cat /proc/net/netfilter/nfnetlink_queue
```

---

## Best Practices

1. Proper error handling
1. Resource cleanup
1. Performance optimization
1. Security considerations
1. Documentation
1. Testing and validation

---

## Common Use Cases

1. Packet filtering
1. Connection tracking
1. NAT implementation
1. DDoS protection
1. Traffic monitoring
1. Custom protocols

---

## Summary

- Hook implementation
- Registration process
- Packet processing
- Connection tracking
- Performance considerations
- Best practices
