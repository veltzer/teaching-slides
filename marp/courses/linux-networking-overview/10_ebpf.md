# eBPF Overview and Usage
## Chapter 10: Extended Berkeley Packet Filter

---

## Chapter Overview

- Introduction to eBPF
- Classic BPF vs eBPF
- eBPF Architecture
- Program Development
- Program Types
- Common Use Cases
- Available Tools

---

## What is eBPF

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_09_ebpf)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_09_ebpf)"/>
  <defs>
    <marker id="arrowd0_09_ebpf" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Evolution: cBPF to eBPF

<div class="columns">
<div>

**Classic BPF:**
- Simple filter rules
- Limited functionality
- Fixed registers
- No function calls

</div>
<div>

**Extended BPF:**
- Rich programming model
- Multiple program types
- Extended registers
- Function calls
- Maps
</div>
</div>

---

## eBPF Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_09_ebpf)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_09_ebpf)"/>
  <defs>
    <marker id="arrowd1_09_ebpf" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Program Types

```c
enum bpf_prog_type {
    BPF_PROG_TYPE_SOCKET_FILTER,
    BPF_PROG_TYPE_KPROBE,
    BPF_PROG_TYPE_XDP,
    BPF_PROG_TYPE_PERF_EVENT,
    BPF_PROG_TYPE_TRACEPOINT,
    // ... more types
};
```

---

## eBPF Maps

```c
struct bpf_map_def {
    __u32 type;
    __u32 key_size;
    __u32 value_size;
    __u32 max_entries;
    __u32 flags;
};

BPF_MAP_DEF(my_map) = {
    .type = BPF_MAP_TYPE_HASH,
    .key_size = sizeof(u32),
    .value_size = sizeof(u64),
    .max_entries = 10000,
};
```

---

## Simple XDP Program

```c
SEC("xdp")
int xdp_filter(struct xdp_md *ctx)
{
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    struct ethhdr *eth = data;

    if (data + sizeof(*eth) > data_end)
        return XDP_ABORTED;

    if (eth->h_proto == htons(ETH_P_IP))
        return XDP_DROP;

    return XDP_PASS;
}
```

---

## Program Verification

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_09_ebpf)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_09_ebpf)"/>
  <defs>
    <marker id="arrowd2_09_ebpf" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Helper Functions

```c
// Available helpers
enum bpf_func_id {
    BPF_FUNC_map_lookup_elem,
    BPF_FUNC_map_update_elem,
    BPF_FUNC_map_delete_elem,
    BPF_FUNC_trace_printk,
    // ... more helpers
};
```

---

## Map Operations

```c
// Map lookup
struct data_t *value;
u32 key = 1234;

value = bpf_map_lookup_elem(&my_map, &key);
if (!value)
    return XDP_ABORTED;

// Map update
u64 new_value = 5678;
bpf_map_update_elem(&my_map, &key, &new_value,
                    BPF_ANY);
```

---

## Tail Calls

```c
// Program array map
struct bpf_map_def SEC("maps") prog_array = {
    .type = BPF_MAP_TYPE_PROG_ARRAY,
    .key_size = sizeof(u32),
    .value_size = sizeof(u32),
    .max_entries = 10,
};

// Tail call
bpf_tail_call(ctx, &prog_array, index);
```

---

## XDP Programs

```c
SEC("xdp")
int xdp_stats(struct xdp_md *ctx)
{
    struct datarec *rec;
    __u32 key = 0;

    rec = bpf_map_lookup_elem(&stats_map, &key);
    if (!rec)
        return XDP_ABORTED;

    rec->packets++;
    rec->bytes += ctx->data_end - ctx->data;

    return XDP_PASS;
}
```

---

## Traffic Control (TC)

```c
SEC("tc")
int tc_example(struct __sk_buff *skb)
{
    void *data = (void *)(long)skb->data;
    void *data_end = (void *)(long)skb->data_end;
    struct ethhdr *eth = data;

    if (data + sizeof(*eth) > data_end)
        return TC_ACT_SHOT;

    return TC_ACT_OK;
}
```

---

## Tools and Utilities

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="150" rx="60" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="80" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="80" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="220" rx="50" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="220" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-size="12" fill="white">Core</text>
  <text x="150" y="85" text-anchor="middle" font-size="11">Concept 1</text>
  <text x="450" y="85" text-anchor="middle" font-size="11">Concept 2</text>
  <text x="150" y="225" text-anchor="middle" font-size="11">Concept 3</text>
  <text x="450" y="225" text-anchor="middle" font-size="11">Concept 4</text>
  <line x1="250" y1="130" x2="190" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="410" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="170" x2="190" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="170" x2="410" y2="200" stroke="#333" stroke-width="2"/>
</svg>

---

## bpftool Usage

```bash
# List programs
bpftool prog list

# Show map contents
bpftool map dump name my_map

# Load program
bpftool prog load prog.o /sys/fs/bpf/prog

# Attach program
bpftool net attach xdp id 123 dev eth0
```

---

## Performance Monitoring

```c
SEC("kprobe/tcp_sendmsg")
int trace_tcp_sendmsg(struct pt_regs *ctx)
{
    u64 ts = bpf_ktime_get_ns();
    u32 pid = bpf_get_current_pid_tgid();

    bpf_map_update_elem(&start_time, &pid, &ts,
                        BPF_ANY);
    return 0;
}
```

---

## Security Applications

```c
SEC("lsm/socket_connect")
int BPF_PROG(restrict_connect, struct socket *sock,
             struct sockaddr *addr, int addr_len)
{
    if (is_restricted_addr(addr))
        return -EPERM;

    return 0;
}
```

---

## Common Use Cases

1. Network filtering
1. Performance monitoring
1. Security enforcement
1. Load balancing
1. Traffic analysis
1. Resource accounting

---

## Best Practices

1. Program verification
1. Map sizing
1. Error handling
1. Performance optimization
1. Resource cleanup
1. Documentation

---

## Debugging Tools

```bash
# Debug output
bpf_trace_printk("Debug: %d\n", value);

# View debug output
cat /sys/kernel/debug/tracing/trace_pipe

# Program stats
bpftool prog show id 123
```

---

## Development Workflow

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_ebpf)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_ebpf)"/>
  <defs>
    <marker id="arrowd4_09_ebpf" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Map Management

```bash
# Create map
bpftool map create /sys/fs/bpf/my_map \
    type hash key 4 value 8 entries 10000

# Update map
bpftool map update name my_map \
    key 0x01 0x02 0x03 0x04 value 0x00 0x00 0x00 0x00

# Delete entry
bpftool map delete name my_map key 0x01 0x02 0x03 0x04
```

---

## Summary

- eBPF capabilities
- Program types
- Development process
- Tools and utilities
- Best practices
- Common use cases
