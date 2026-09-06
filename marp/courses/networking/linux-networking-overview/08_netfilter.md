---
tags:
  - networking:firewall
  - networking:netfilter
  - infrastructure:linux
  - concepts:kernel
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:sysadmins

---

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

![what_are_netfilters](svg/courses/networking/linux-networking-overview/08_netfilter/what_are_netfilters.svg)

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

![packet_flow_through_hooks](svg/courses/networking/linux-networking-overview/08_netfilter/packet_flow_through_hooks.svg)

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
