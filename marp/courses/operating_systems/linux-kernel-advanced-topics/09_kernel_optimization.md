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

![optimization_goals](svg/courses/operating_systems/linux-kernel-advanced-topics/09_kernel_optimization/optimization_goals.svg)

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

![slab_allocator_tuning](svg/courses/operating_systems/linux-kernel-advanced-topics/09_kernel_optimization/slab_allocator_tuning.svg)

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

![rt_patch_architecture](svg/courses/operating_systems/linux-kernel-advanced-topics/09_kernel_optimization/rt_patch_architecture.svg)

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

![optimization_trade_offs](svg/courses/operating_systems/linux-kernel-advanced-topics/09_kernel_optimization/optimization_trade_offs.svg)

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
