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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">eBPF: Safe Kernel Programmability</text>
  <rect x="20" y="30" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="50" text-anchor="middle" font-size="11" font-weight="bold">User Space</text>
  <text x="105" y="67" text-anchor="middle" font-size="10" fill="#666">C program compiled</text>
  <text x="105" y="82" text-anchor="middle" font-size="10" fill="#666">to eBPF bytecode</text>
  <rect x="215" y="30" width="170" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">Verifier + JIT</text>
  <text x="300" y="67" text-anchor="middle" font-size="10" fill="#666">Safety checks</text>
  <text x="300" y="82" text-anchor="middle" font-size="10" fill="#666">Native compilation</text>
  <rect x="410" y="30" width="170" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="50" text-anchor="middle" font-size="11" font-weight="bold">Kernel Hooks</text>
  <text x="495" y="67" text-anchor="middle" font-size="10" fill="#666">XDP, tc, kprobes</text>
  <text x="495" y="82" text-anchor="middle" font-size="10" fill="#666">tracepoints, LSM</text>
  <line x1="190" y1="65" x2="215" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_09_ebpf)"/>
  <line x1="385" y1="65" x2="410" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_09_ebpf)"/>
  <rect x="170" y="120" width="260" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="140" text-anchor="middle" font-size="11" font-weight="bold">eBPF Maps (shared data)</text>
  <text x="300" y="157" text-anchor="middle" font-size="10" fill="#666">Hash, Array, Ring Buffer, Per-CPU</text>
  <line x1="105" y1="100" x2="105" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="105" y1="145" x2="170" y2="145" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd0_09_ebpf)"/>
  <line x1="495" y1="100" x2="495" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="495" y1="145" x2="430" y2="145" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd0_09_ebpf)"/>
  <text x="300" y="192" text-anchor="middle" font-size="10" fill="#666">Maps enable data sharing between user space and kernel eBPF programs</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">eBPF Architecture: Load and Attach</text>
  <rect x="20" y="30" width="270" height="75" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="155" y="48" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">User Space</text>
  <rect x="35" y="55" width="80" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="75" y="72" text-anchor="middle" font-size="10">clang/LLVM</text>
  <text x="75" y="85" text-anchor="middle" font-size="10" fill="#666">Compile</text>
  <rect x="130" y="55" width="70" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="165" y="72" text-anchor="middle" font-size="10">bpf()</text>
  <text x="165" y="85" text-anchor="middle" font-size="10" fill="#666">syscall</text>
  <rect x="215" y="55" width="65" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="247" y="72" text-anchor="middle" font-size="10">libbpf</text>
  <text x="247" y="85" text-anchor="middle" font-size="10" fill="#666">loader</text>
  <rect x="310" y="30" width="270" height="75" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="445" y="48" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Kernel Space</text>
  <rect x="325" y="55" width="70" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="72" text-anchor="middle" font-size="10">Verifier</text>
  <text x="360" y="85" text-anchor="middle" font-size="10" fill="#666">Safety</text>
  <rect x="410" y="55" width="70" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="445" y="72" text-anchor="middle" font-size="10">JIT</text>
  <text x="445" y="85" text-anchor="middle" font-size="10" fill="#666">Compile</text>
  <rect x="495" y="55" width="75" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="532" y="72" text-anchor="middle" font-size="10">Attach</text>
  <text x="532" y="85" text-anchor="middle" font-size="10" fill="#666">Hook point</text>
  <line x1="115" y1="75" x2="130" y2="75" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_09_ebpf)"/>
  <line x1="200" y1="75" x2="215" y2="75" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_09_ebpf)"/>
  <line x1="280" y1="75" x2="325" y2="75" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd1_09_ebpf)"/>
  <line x1="395" y1="75" x2="410" y2="75" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_09_ebpf)"/>
  <line x1="480" y1="75" x2="495" y2="75" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_09_ebpf)"/>
  <rect x="20" y="125" width="560" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5" fill-opacity="0.3"/>
  <text x="120" y="145" text-anchor="middle" font-size="10" font-weight="bold">XDP (NIC driver)</text>
  <text x="260" y="145" text-anchor="middle" font-size="10" font-weight="bold">tc (traffic control)</text>
  <text x="400" y="145" text-anchor="middle" font-size="10" font-weight="bold">kprobes (tracing)</text>
  <text x="530" y="145" text-anchor="middle" font-size="10" font-weight="bold">LSM (security)</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#666">Available kernel hook points for eBPF program attachment</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">eBPF Verifier Pipeline</text>
  <rect x="20" y="40" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="60" text-anchor="middle" font-size="11" font-weight="bold">BPF Bytecode</text>
  <text x="80" y="78" text-anchor="middle" font-size="10" fill="#666">ELF .o file</text>
  <rect x="170" y="40" width="120" height="55" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="230" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Verifier</text>
  <text x="230" y="78" text-anchor="middle" font-size="10" fill="#666">DAG analysis</text>
  <rect x="320" y="40" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="380" y="60" text-anchor="middle" font-size="11" font-weight="bold">JIT Compiler</text>
  <text x="380" y="78" text-anchor="middle" font-size="10" fill="#666">Native x86/ARM</text>
  <rect x="470" y="40" width="110" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="60" text-anchor="middle" font-size="11" font-weight="bold">Execute</text>
  <text x="525" y="78" text-anchor="middle" font-size="10" fill="#666">At hook point</text>
  <line x1="140" y1="67" x2="170" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_09_ebpf)"/>
  <line x1="290" y1="67" x2="320" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_09_ebpf)"/>
  <line x1="440" y1="67" x2="470" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_09_ebpf)"/>
  <rect x="120" y="115" width="360" height="65" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="5" stroke-dasharray="5,3"/>
  <text x="300" y="135" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">Verifier Checks:</text>
  <text x="300" y="152" text-anchor="middle" font-size="10" fill="#666">No loops | Bounded execution | Valid memory access</text>
  <text x="300" y="167" text-anchor="middle" font-size="10" fill="#666">No null pointer deref | Proper map access | Stack bounds</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">eBPF Ecosystem Tools</text>
  <rect x="30" y="35" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="55" text-anchor="middle" font-size="11" font-weight="bold">bpftool</text>
  <text x="90" y="72" text-anchor="middle" font-size="10" fill="#666">Inspect & manage</text>
  <rect x="170" y="35" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="55" text-anchor="middle" font-size="11" font-weight="bold">bpftrace</text>
  <text x="230" y="72" text-anchor="middle" font-size="10" fill="#666">High-level tracing</text>
  <rect x="310" y="35" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="370" y="55" text-anchor="middle" font-size="11" font-weight="bold">BCC Toolkit</text>
  <text x="370" y="72" text-anchor="middle" font-size="10" fill="#666">Python + eBPF</text>
  <rect x="450" y="35" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="55" text-anchor="middle" font-size="11" font-weight="bold">libbpf</text>
  <text x="510" y="72" text-anchor="middle" font-size="10" fill="#666">C loader library</text>
  <rect x="30" y="110" width="120" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="130" text-anchor="middle" font-size="11" font-weight="bold">Cilium</text>
  <text x="90" y="147" text-anchor="middle" font-size="10" fill="#666">K8s networking</text>
  <rect x="170" y="110" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="130" text-anchor="middle" font-size="11" font-weight="bold">Falco</text>
  <text x="230" y="147" text-anchor="middle" font-size="10" fill="#666">Runtime security</text>
  <rect x="310" y="110" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="370" y="130" text-anchor="middle" font-size="11" font-weight="bold">Katran</text>
  <text x="370" y="147" text-anchor="middle" font-size="10" fill="#666">L4 load balancer</text>
  <rect x="450" y="110" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="130" text-anchor="middle" font-size="11" font-weight="bold">Pixie</text>
  <text x="510" y="147" text-anchor="middle" font-size="10" fill="#666">Observability</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">eBPF Development Workflow</text>
  <rect x="15" y="40" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="65" y="60" text-anchor="middle" font-size="10" font-weight="bold">Write C code</text>
  <text x="65" y="78" text-anchor="middle" font-size="10" fill="#666">SEC("xdp")</text>
  <rect x="140" y="40" width="100" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="190" y="60" text-anchor="middle" font-size="10" font-weight="bold">Compile</text>
  <text x="190" y="78" text-anchor="middle" font-size="10" fill="#666">clang -target bpf</text>
  <rect x="265" y="40" width="100" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="315" y="60" text-anchor="middle" font-size="10" font-weight="bold">Load + Verify</text>
  <text x="315" y="78" text-anchor="middle" font-size="10" fill="#666">bpf() syscall</text>
  <rect x="390" y="40" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="440" y="60" text-anchor="middle" font-size="10" font-weight="bold">Attach</text>
  <text x="440" y="78" text-anchor="middle" font-size="10" fill="#666">ip link / bpftool</text>
  <rect x="515" y="40" width="75" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="552" y="60" text-anchor="middle" font-size="10" font-weight="bold">Monitor</text>
  <text x="552" y="78" text-anchor="middle" font-size="10" fill="#666">trace_pipe</text>
  <line x1="115" y1="65" x2="140" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_ebpf)"/>
  <line x1="240" y1="65" x2="265" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_ebpf)"/>
  <line x1="365" y1="65" x2="390" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_ebpf)"/>
  <line x1="490" y1="65" x2="515" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_ebpf)"/>
  <rect x="60" y="115" width="480" height="55" fill="#e3f2fd" stroke="#1565c0" stroke-width="1" rx="5" stroke-dasharray="5,3"/>
  <text x="300" y="135" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">Key Tools: bpftool, bpftrace, libbpf, BCC toolkit</text>
  <text x="300" y="155" text-anchor="middle" font-size="10" fill="#666">Debug: bpf_trace_printk() | cat /sys/kernel/debug/tracing/trace_pipe</text>
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
