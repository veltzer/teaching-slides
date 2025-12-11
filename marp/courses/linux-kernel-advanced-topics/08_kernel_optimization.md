# Kernel Optimization

---

## Overview

Linux kernel optimization focuses on:
1. Reducing memory footprint
1. Improving performance
1. Minimizing latency
1. Decreasing kernel size

These optimizations are crucial for:
- Embedded systems
- Real-time applications
- Resource-constrained devices

---

## Optimization Goals

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="80" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="125" y="95" text-anchor="middle" font-size="16" font-weight="bold">Size</text>
  <rect x="225" y="50" width="150" height="80" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="300" y="95" text-anchor="middle" font-size="16" font-weight="bold">Performance</text>
  <rect x="400" y="50" width="150" height="80" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <text x="475" y="95" text-anchor="middle" font-size="16" font-weight="bold">Latency</text>
  <rect x="140" y="200" width="150" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="215" y="245" text-anchor="middle" font-size="16" font-weight="bold">Memory</text>
  <rect x="310" y="200" width="150" height="80" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="385" y="245" text-anchor="middle" font-size="16" font-weight="bold">Power</text>
  <path d="M125 130 L215 200" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M300 130 L215 200" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M300 130 L385 200" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M475 130 L385 200" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#666"/>
    </marker>
  </defs>
</svg>

---

## Kernel Size Optimization

### Configuration Options

Key `CONFIG_` options to disable:
- `CONFIG_DEBUG_KERNEL`
- `CONFIG_KALLSYMS`
- `CONFIG_BUG`
- `CONFIG_PRINTK`
- `CONFIG_SWAP`

---

## Minimal Configuration

```bash
# Start with minimal config
make allnoconfig

# Add only required features
make menuconfig

# Measure kernel size
ls -lh arch/x86/boot/bzImage
```

---

## Removing Unused Drivers

### Driver Analysis

```bash
# List loaded modules
lsmod > used_modules.txt

# Find unused built-in drivers
cat /proc/modules
```

Remove drivers for:
- Unused filesystems
- Unnecessary network protocols
- Unused hardware support

---

## Compiler Optimization Flags

### GCC Optimization Levels

```makefile
# In kernel Makefile
KBUILD_CFLAGS += -Os  # Size optimization
KBUILD_CFLAGS += -O2  # Performance
KBUILD_CFLAGS += -O3  # Aggressive
```

Trade-offs:
- `-Os`: Smallest code
- `-O2`: Balanced
- `-O3`: Fastest, larger

---

## Link Time Optimization (LTO)

Enable LTO for better optimization:

```bash
CONFIG_LTO_CLANG=y
# or
CONFIG_LTO_GCC=y
```

Benefits:
1. Cross-function optimization
1. Dead code elimination
1. Better inlining decisions

---

## Memory Footprint Reduction

### Memory Usage Analysis

```bash
# Check kernel memory usage
cat /proc/meminfo | grep Kernel

# Slab allocator stats
cat /proc/slabinfo

# Page allocation stats
cat /proc/pagetypeinfo
```

---

## Slab Allocator Tuning

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="500" height="60" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="300" y="85" text-anchor="middle" font-size="14" font-weight="bold">SLAB Cache</text>
  <rect x="70" y="70" width="60" height="30" fill="#bbdefb" stroke="#1976d2"/>
  <rect x="140" y="70" width="60" height="30" fill="#bbdefb" stroke="#1976d2"/>
  <rect x="210" y="70" width="60" height="30" fill="#c8e6c9" stroke="#4caf50"/>
  <rect x="280" y="70" width="60" height="30" fill="#bbdefb" stroke="#1976d2"/>
  <rect x="350" y="70" width="60" height="30" fill="#c8e6c9" stroke="#4caf50"/>
  <rect x="420" y="70" width="60" height="30" fill="#c8e6c9" stroke="#4caf50"/>
  <rect x="490" y="70" width="60" height="30" fill="#ffccbc" stroke="#ff5722"/>
  <text x="100" y="90" text-anchor="middle" font-size="12">Used</text>
  <text x="240" y="90" text-anchor="middle" font-size="12">Free</text>
  <text x="520" y="90" text-anchor="middle" font-size="12">Partial</text>
  <rect x="100" y="180" width="120" height="40" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="160" y="205" text-anchor="middle" font-size="14">SLUB</text>
  <rect x="240" y="180" width="120" height="40" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="300" y="205" text-anchor="middle" font-size="14">SLAB</text>
  <rect x="380" y="180" width="120" height="40" fill="#fef5e6" stroke="#ff9800" stroke-width="2"/>
  <text x="440" y="205" text-anchor="middle" font-size="14">SLOB</text>
  <text x="160" y="250" text-anchor="middle" font-size="12">Default</text>
  <text x="300" y="250" text-anchor="middle" font-size="12">Cache-friendly</text>
  <text x="440" y="250" text-anchor="middle" font-size="12">Minimal</text>
</svg>

---

## SLUB vs SLAB vs SLOB

Choose allocator based on needs:

| Allocator | Use Case | Memory Overhead |
|-----------|----------|-----------------|
| `SLUB` | General purpose | Medium |
| `SLAB` | Cache-heavy | High |
| `SLOB` | Embedded | Low |

---

## Stack Size Optimization

### Kernel Stack Configuration

```c
// Default: 8KB or 16KB
CONFIG_THREAD_SIZE_ORDER=2  // 16KB
CONFIG_THREAD_SIZE_ORDER=1  // 8KB

// Check stack usage
CONFIG_DEBUG_STACK_USAGE=y
```

Monitor with:
```bash
cat /proc/<pid>/stack
```

---

## Real-time Patches (PREEMPT_RT)

### Preemption Models

```bash
CONFIG_PREEMPT_NONE=y     # Server
CONFIG_PREEMPT_VOLUNTARY=y # Desktop
CONFIG_PREEMPT=y          # Low latency
CONFIG_PREEMPT_RT=y       # Real-time
```

---

## RT Patch Architecture

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="500" height="60" fill="#e8eaf6" stroke="#3f51b5" stroke-width="2"/>
  <text x="300" y="85" text-anchor="middle" font-size="16" font-weight="bold">User Space</text>
  <rect x="50" y="130" width="240" height="60" fill="#fff3e0" stroke="#ff9800" stroke-width="2"/>
  <text x="170" y="165" text-anchor="middle" font-size="14">Standard Kernel</text>
  <rect x="310" y="130" width="240" height="60" fill="#e8f5e9" stroke="#4caf50" stroke-width="2"/>
  <text x="430" y="165" text-anchor="middle" font-size="14">RT Kernel</text>
  <rect x="70" y="210" width="200" height="40" fill="#ffebee" stroke="#f44336"/>
  <text x="170" y="235" text-anchor="middle" font-size="12">Spinlocks</text>
  <rect x="330" y="210" width="200" height="40" fill="#e8f5e9" stroke="#4caf50"/>
  <text x="430" y="235" text-anchor="middle" font-size="12">RT Mutexes</text>
  <rect x="70" y="260" width="200" height="40" fill="#ffebee" stroke="#f44336"/>
  <text x="170" y="285" text-anchor="middle" font-size="12">IRQ Handlers</text>
  <rect x="330" y="260" width="200" height="40" fill="#e8f5e9" stroke="#4caf50"/>
  <text x="430" y="285" text-anchor="middle" font-size="12">Threaded IRQs</text>
  <rect x="70" y="310" width="200" height="40" fill="#ffebee" stroke="#f44336"/>
  <text x="170" y="335" text-anchor="middle" font-size="12">Softirqs</text>
  <rect x="330" y="310" width="200" height="40" fill="#e8f5e9" stroke="#4caf50"/>
  <text x="430" y="335" text-anchor="middle" font-size="12">RT Threads</text>
</svg>

---

## Latency Reduction Techniques

### Interrupt Threading

```c
// Convert to threaded IRQ
request_threaded_irq(irq, NULL,
    thread_handler,
    IRQF_ONESHOT,
    "device", dev);
```

Benefits:
- Preemptible handlers
- Priority control
- Better latency

---

## Priority Inheritance

Prevent priority inversion:

```c
struct rt_mutex lock;
rt_mutex_init(&lock);

rt_mutex_lock(&lock);
// Critical section
rt_mutex_unlock(&lock);
```

---

## CPU Isolation

### Isolate CPUs for RT Tasks

```bash
# Boot parameter
isolcpus=2,3

# Runtime isolation
echo 0 > /sys/devices/system/cpu/cpu2/online
echo 1 > /sys/devices/system/cpu/cpu2/online
```

Assign RT tasks:
```bash
taskset -c 2,3 ./rt_application
```

---

## Kernel Debugging Impact

### Debug Options Overhead

| Option | Performance Impact |
|--------|-------------------|
| `CONFIG_DEBUG_KERNEL` | 5-10% |
| `CONFIG_KASAN` | 3x slower |
| `CONFIG_DEBUG_SPINLOCK` | 10-15% |
| `CONFIG_LOCKDEP` | 20-30% |

---

## Removing Debug Features

Production kernel configuration:

```bash
# Disable all debug
CONFIG_DEBUG_KERNEL=n
CONFIG_DEBUG_INFO=n
CONFIG_FTRACE=n
CONFIG_KPROBES=n
CONFIG_DEBUG_FS=n
```

---

## Architecture-specific Optimizations

### ARM Optimizations

```bash
# ARM-specific
CONFIG_ARM_UNWIND=n
CONFIG_FRAME_POINTER=n
CONFIG_THUMB2_KERNEL=y
```

### x86 Optimizations

```bash
# x86-specific
CONFIG_X86_MSR=n
CONFIG_X86_CPUID=n
CONFIG_MICROCODE=n
```

---

## Performance Profiling Tools

### Perf Tool

```bash
# CPU profiling
perf record -a -g ./application
perf report

# Cache misses
perf stat -e cache-misses ./app

# Scheduling latency
perf sched latency
```

---

## Ftrace for Optimization

```bash
# Function tracer
echo function > /sys/kernel/debug/tracing/current_tracer
echo 1 > /sys/kernel/debug/tracing/tracing_on

# Read trace
cat /sys/kernel/debug/tracing/trace
```

---

## Latency Tracer

### IRQ Latency Analysis

```bash
# Enable IRQ tracer
echo irqsoff > /sys/kernel/debug/tracing/current_tracer

# Check max latency
cat /sys/kernel/debug/tracing/tracing_max_latency
```

---

## Static Analysis Tools

### Kernel Static Checkers

1. **Sparse**
   ```bash
   make C=1 CHECK=sparse
   ```

1. **Coccinelle**
   ```bash
   make coccicheck
   ```

1. **Smatch**
   ```bash
   make CHECK="smatch -p=kernel" C=1
   ```

---

## Dynamic Analysis

### Runtime Checking

```bash
# KASAN (Address Sanitizer)
CONFIG_KASAN=y

# KTSAN (Thread Sanitizer)
CONFIG_KTSAN=y

# KFENCE (Fence errors)
CONFIG_KFENCE=y
```

---

## Benchmarking Methodologies

### System Benchmarks

```bash
# Kernel compile test
time make -j$(nproc) bzImage

# I/O performance
fio --name=test --rw=randread --size=1G

# Network performance
netperf -H server_ip
```

---

## Memory Benchmark

```bash
# Memory bandwidth
mbw 256

# Cache performance
lat_mem_rd 512 16

# Memory latency
mlc --latency_matrix
```

---

## Boot Time Impact

### Measure Boot Components

```bash
# Kernel boot time
dmesg | grep "Freeing unused kernel"

# Initcall timing
dmesg | grep initcall

# Systemd analysis
systemd-analyze blame
```

---

## Optimization Trade-offs

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <polygon points="300,50 150,300 450,300" fill="none" stroke="#333" stroke-width="2"/>
  <circle cx="300" cy="50" r="40" fill="#f44336"/>
  <text x="300" y="55" text-anchor="middle" font-size="14" fill="white">Speed</text>
  <circle cx="150" cy="300" r="40" fill="#4caf50"/>
  <text x="150" y="305" text-anchor="middle" font-size="14" fill="white">Size</text>
  <circle cx="450" cy="300" r="40" fill="#2196f3"/>
  <text x="450" y="305" text-anchor="middle" font-size="14" fill="white">Features</text>
  <circle cx="300" cy="200" r="30" fill="#ff9800"/>
  <text x="300" y="205" text-anchor="middle" font-size="12" fill="white">Balance</text>
  <text x="300" y="380" text-anchor="middle" font-size="16" font-weight="bold">Choose Two</text>
</svg>

---

## Kernel Configuration Templates

### Embedded Template

```bash
# Minimal embedded config
CONFIG_EMBEDDED=y
CONFIG_EXPERT=y
CONFIG_SLOB=y
CONFIG_CC_OPTIMIZE_FOR_SIZE=y
CONFIG_SYSFS_DEPRECATED=n
```

---

## Real-time Template

```bash
# RT configuration
CONFIG_PREEMPT_RT=y
CONFIG_HIGH_RES_TIMERS=y
CONFIG_NO_HZ_FULL=y
CONFIG_RCU_NOCB_CPU=y
CONFIG_RT_GROUP_SCHED=y
```

---

## Performance Template

```bash
# Performance config
CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE=y
CONFIG_JUMP_LABEL=y
CONFIG_STATIC_KEYS_SELFTEST=n
CONFIG_LTO_CLANG_THIN=y
```

---

## Continuous Optimization

### CI/CD Integration

```yaml
# .gitlab-ci.yml
kernel_size_check:
  script:
    - make defconfig
    - make -j$(nproc)
    - size vmlinux
    - test $(size vmlinux | awk 'NR==2 {print $4}') -lt 10000000
```

---

## Best Practices

1. **Measure First**
   - Profile before optimizing
   - Identify bottlenecks
   - Set clear goals

1. **Incremental Changes**
   - One optimization at a time
   - Test each change
   - Document results

1. **Platform Testing**
   - Test on target hardware
   - Verify functionality
   - Check edge cases

---

## Common Pitfalls

### Avoid These Mistakes

1. Over-optimization
1. Removing essential features
1. Ignoring security
1. Not testing thoroughly
1. Optimizing wrong metrics

---

## Summary

Kernel optimization requires:
- Clear performance goals
- Systematic approach
- Careful measurement
- Thorough testing

Balance between:
- Size vs features
- Speed vs power
- Latency vs throughput