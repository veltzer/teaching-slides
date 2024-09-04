# Writing Netfilter Modules
An Introduction with Examples

---

# Outline

1. Introduction to Netfilter
2. Netfilter Hook Points
3. Basic Structure of a Netfilter Module
4. Example: A Simple Packet Logger
5. Example: IP Address Blacklist
6. Compiling and Loading Netfilter Modules
7. Concurrency in Netfilter Modules
8. Best Practices and Considerations

---

# 1. Introduction to Netfilter

- Netfilter is the packet filtering framework in the Linux kernel
- It allows packet filtering, network address translation (NAT), and other packet mangling
- Netfilter provides a set of hooks in the networking stack
- Modules can register callback functions with these hooks

---

# 2. Netfilter Hook Points

Five main hook points:

1. `NF_INET_PRE_ROUTING`
2. `NF_INET_LOCAL_IN`
3. `NF_INET_FORWARD`
4. `NF_INET_LOCAL_OUT`
5. `NF_INET_POST_ROUTING`

Each hook point allows you to intercept and modify packets at different stages of processing.

---

# 3. Basic Structure of a Netfilter Module

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>

static struct nf_hook_ops nfho;

unsigned int hook_func(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    // Packet processing logic here
    return NF_ACCEPT;
}

int init_module()
{
    nfho.hook = hook_func;
    nfho.hooknum = NF_INET_PRE_ROUTING;
    nfho.pf = PF_INET;
    nfho.priority = NF_IP_PRI_FIRST;
    return nf_register_net_hook(&init_net, &nfho);
}

void cleanup_module()
{
    nf_unregister_net_hook(&init_net, &nfho);
}

MODULE_LICENSE("GPL");
```

---

# 4. Example: A Simple Packet Logger

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>

static struct nf_hook_ops nfho;

unsigned int hook_func(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    struct iphdr *iph;
    struct tcphdr *tcph;

    iph = ip_hdr(skb);
    if (iph->protocol == IPPROTO_TCP) {
        tcph = tcp_hdr(skb);
        printk(KERN_INFO "Source IP: %pI4, Dest IP: %pI4, Source Port: %u, Dest Port: %u\n",
               &iph->saddr, &iph->daddr, ntohs(tcph->source), ntohs(tcph->dest));
    }

    return NF_ACCEPT;
}

// init_module and cleanup_module as before

MODULE_LICENSE("GPL");
```

---

# 5. Example: IP Address Blacklist

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>

static struct nf_hook_ops nfho;

// Blacklisted IP address (example: 192.168.1.100)
#define BLACKLISTED_IP 0xC0A80164

unsigned int hook_func(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    struct iphdr *iph;
    iph = ip_hdr(skb);

    if (iph->saddr == htonl(BLACKLISTED_IP)) {
        printk(KERN_INFO "Dropping packet from blacklisted IP %pI4\n", &iph->saddr);
        return NF_DROP;
    }

    return NF_ACCEPT;
}

// init_module and cleanup_module as before

MODULE_LICENSE("GPL");
```

---

# 6. Compiling and Loading Netfilter Modules

1. Create a Makefile:

```makefile
obj-m += mymodule.o

all:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

2. Compile the module:
   ```
   make
   ```

3. Load the module:
   ```
   sudo insmod mymodule.ko
   ```

4. Unload the module:
   ```
   sudo rmmod mymodule
   ```

---

# 7. Concurrency in Netfilter Modules

## Hook Function Execution

- Hook functions can run on any CPU core
- Multiple instances of the same hook function can run in parallel on different cores
- Different hook functions can also run concurrently

---

# Concurrency Challenges

1. Shared Resource Access
   - Use appropriate synchronization mechanisms (e.g., spinlocks, RCU) when accessing shared data

2. Per-CPU Variables
   - Utilize `per_cpu` variables for better performance in concurrent scenarios

3. Execution Context

Understand the context in which your hook functions run (softirq context)
Use appropriate synchronization primitives based on the execution context

---

# Example: Using Spinlocks for Shared Data

```c
#include <linux/spinlock.h>

static DEFINE_SPINLOCK(my_lock);
static unsigned long my_counter = 0;

unsigned int hook_func(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    unsigned long flags;
    
    spin_lock_irqsave(&my_lock, flags);
    my_counter++;
    spin_unlock_irqrestore(&my_lock, flags);

    // Rest of the hook function...
    return NF_ACCEPT;
}
```

---

# Example: Using Per-CPU Variables

```c
#include <linux/percpu.h>

static DEFINE_PER_CPU(unsigned long, packet_count);

unsigned int hook_func(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    unsigned long *count = this_cpu_ptr(&packet_count);
    (*count)++;

    // Rest of the hook function...
    return NF_ACCEPT;
}
```

---

# Concurrency Considerations

- Minimize time spent in critical sections
- Be aware of potential deadlocks when using multiple locks
- Consider using RCU (Read-Copy-Update) for read-heavy workloads
- Use atomic operations for simple counters or flags
- Be cautious with memory allocation in hook functions (it can sleep)
