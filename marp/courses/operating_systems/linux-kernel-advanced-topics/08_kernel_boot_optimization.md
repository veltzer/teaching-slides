---
tags:
  - infrastructure:linux
  - concepts:kernel
  - concepts:boot
  - concepts:performance
level: advanced
category: operating-systems
audience:
  - audiences:developers

---

# Kernel Boot Time Optimization

---

## Boot Time Optimization Goals

Target boot times:
- Consumer electronics: < 1 second
- Automotive: < 2 seconds
- Industrial: < 5 seconds
- Medical devices: < 3 seconds

Every millisecond counts!

---

## Boot Process Timeline

![boot_process_timeline](svg/courses/operating_systems/linux-kernel-advanced-topics/08_kernel_boot_optimization/boot_process_timeline.svg)

---

## Measurement Tools

Essential tools for analysis:

```bash
# Kernel boot timing
CONFIG_PRINTK_TIME=y
CONFIG_BOOT_PRINTK_DELAY=y

# Bootchart
CONFIG_BOOTCHART=y

# Ftrace
CONFIG_FTRACE=y
CONFIG_FUNCTION_TRACER=y
CONFIG_FUNCTION_GRAPH_TRACER=y

# initcall_debug
initcall_debug=1  # kernel parameter
```

---

## Analyzing Boot Time

```bash
# Grab kernel timestamps
dmesg | grep -E "^\[[ ]*[0-9]+\."

# SystemD analysis
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain

# Generate boot chart
systemd-analyze plot > bootchart.svg
```

---

## Bootgraph

Visualize kernel boot:

```bash
# Enable initcall tracing
echo 'initcall_debug' >> /boot/cmdline

# Capture and analyze
dmesg > boot.log
scripts/bootgraph.pl boot.log > boot.svg
```

---

## Kernel Configuration

Remove unnecessary features:

```bash
# Disable unused subsystems
# CONFIG_SWAP is not set
# CONFIG_MODULES is not set
# CONFIG_BLOCK is not set  # If no block devices
# CONFIG_INPUT_MOUSE is not set
# CONFIG_VT is not set      # If no console needed

# Disable debugging
# CONFIG_DEBUG_KERNEL is not set
# CONFIG_FTRACE is not set
# CONFIG_PROFILING is not set
```

---

## Compression Options

![compression_options](svg/courses/operating_systems/linux-kernel-advanced-topics/08_kernel_boot_optimization/compression_options.svg)

---

## Choose Compression Wisely

```bash
# Fast decompression (recommended)
CONFIG_KERNEL_LZ4=y

# Balanced
CONFIG_KERNEL_LZO=y
CONFIG_KERNEL_GZIP=y

# Smallest size (slow)
CONFIG_KERNEL_XZ=y
CONFIG_KERNEL_LZMA=y
```

---

## Initcall Optimization

```c
/* Change initialization order */
/* From module_init() to earlier stages */

core_initcall(my_early_init);     /* Level 1 */
postcore_initcall(my_init);       /* Level 2 */
arch_initcall(my_init);            /* Level 3 */
subsys_initcall(my_init);          /* Level 4 */
fs_initcall(my_init);              /* Level 5 */
device_initcall(my_init);          /* Level 6 */
late_initcall(my_init);            /* Level 7 */
```

---

## Asynchronous Initialization

```c
/* Mark driver as async */
static struct platform_driver my_driver = {
    .driver = {
        .name = "my_driver",
        .probe_type = PROBE_PREFER_ASYNCHRONOUS,
    },
    .probe = my_probe,
};

/* Or use async probe */
static int my_probe(struct platform_device *pdev)
{
    /* Quick init here */

    /* Defer slow init */
    schedule_work(&my_init_work);

    return 0;
}
```

---

## Parallel Driver Initialization

```bash
# Enable async probing globally
CONFIG_DRIVERS_PROBE_DEFER=y

# Kernel parameter
driver_async_probe=*  # All drivers
driver_async_probe=mmc,usb  # Specific
```

---

## Defer Non-Critical Drivers

```c
/* Defer probe if resources not ready */
static int my_probe(struct platform_device *pdev)
{
    struct resource *res;

    res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    if (!res)
        return -EPROBE_DEFER;

    /* Continue initialization */
    return 0;
}
```

---

## Optimize Kernel Size

Smaller kernel = faster loading:

```bash
# Strip symbols
CONFIG_KALLSYMS=n

# Optimize for size
CONFIG_CC_OPTIMIZE_FOR_SIZE=y

# Remove unused code
CONFIG_LD_DEAD_CODE_DATA_ELIMINATION=y

# Minimal drivers
CONFIG_EMBEDDED=y
```

---

## Minimal Root Filesystem

```bash
# Use minimal initramfs
CONFIG_INITRAMFS_SOURCE="minimal.cpio"

# Compress initramfs
CONFIG_INITRAMFS_COMPRESSION_LZ4=y

# Skip unnecessary files
# Only include essential binaries
```

---

## Direct Kernel Boot

Skip initramfs entirely:

```bash
# Build drivers into kernel
CONFIG_MMC=y  # Not CONFIG_MMC=m

# Root device ready at boot
root=/dev/mmcblk0p1 rootwait

# No initramfs needed
CONFIG_INITRAMFS_SOURCE=""
```

---

## Quiet Boot

Reduce console output:

```bash
# Kernel parameters
quiet loglevel=0
console=ttyS0,115200n8

# Or disable console
console=
```

---

## Preset LPJ

Skip calibration delay:

```bash
# Measure once
dmesg | grep "lpj="
# Calibrating delay loop... 996.14 BogoMIPS (lpj=498073)

# Set in kernel parameters
lpj=498073
```

---

## No Probe Delays

```c
/* Remove unnecessary delays */

/* Bad - fixed delay */
msleep(100);  /* Remove if possible */

/* Good - poll for ready */
while (!device_ready() && timeout--)
    udelay(10);
```

---

## Optimize Device Initialization

```c
/* Parallelize independent operations */
static int my_probe(struct platform_device *pdev)
{
    /* Start all independent operations */
    start_clock_init();
    start_regulator_init();
    start_gpio_init();

    /* Wait for all to complete */
    wait_for_clock();
    wait_for_regulator();
    wait_for_gpio();

    return 0;
}
```

---

## Filesystem Optimization

Choose fast filesystem:

```bash
# SquashFS for read-only
CONFIG_SQUASHFS=y
CONFIG_SQUASHFS_LZ4=y

# F2FS for flash
CONFIG_F2FS_FS=y

# Disable unnecessary features
# CONFIG_EXT4_FS_POSIX_ACL is not set
# CONFIG_EXT4_FS_SECURITY is not set
```

---

## CPU Frequency

Start at maximum frequency:

```bash
# Set performance governor early
CONFIG_CPU_FREQ_DEFAULT_GOV_PERFORMANCE=y

# Or via kernel parameter
cpufreq.default_governor=performance
```

---

## Suspend to RAM Boot

Ultra-fast resume from suspend:

```bash
# Save state to RAM
echo mem > /sys/power/state

# Resume in < 100ms possible
# Requires maintaining power to RAM
```

---

## Hibernation Boot

Resume from disk:

```bash
# Save state to disk
echo disk > /sys/power/state

# Faster than full boot
# Slower than suspend to RAM
resume=/dev/mmcblk0p3
```

---

## Snapshot Boot

![snapshot_boot](svg/courses/operating_systems/linux-kernel-advanced-topics/08_kernel_boot_optimization/snapshot_boot.svg)

---

## XIP (Execute In Place)

Run code directly from flash:

```bash
# Configure XIP
CONFIG_XIP_KERNEL=y
CONFIG_XIP_PHYS_ADDR=0x10000000

# No copying to RAM needed
# Instant execution
# Requires NOR flash or similar
```

---

## Reduce Kernel Modules

Build drivers in kernel:

```bash
# Before (modules)
CONFIG_USB=m
CONFIG_MMC=m
# Boot time: load modules

# After (built-in)
CONFIG_USB=y
CONFIG_MMC=y
# Boot time: already loaded
```

---

## Optimize Userspace

Fast init system:

```bash
# Use BusyBox init
CONFIG_BUSYBOX=y

# Or minimal systemd
systemctl disable unnecessary.service

# Or custom init
exec /application  # Direct launch
```

---

## Prelink Libraries

Reduce dynamic linking time:

```bash
# Prelink all libraries
prelink -a

# Verify
prelink --print-cache
```

---

## Static Linking

Eliminate dynamic linking:

```bash
# Build statically
gcc -static -o app app.c

# Pros: Fast startup
# Cons: Larger size, no sharing
```

---

## Readahead

Preload files during boot:

```bash
# systemd readahead
systemctl enable systemd-readahead-collect
systemctl enable systemd-readahead-replay

# Custom readahead list
readahead-list /etc/readahead.files
```

---

## Boot Profiling Script

```bash
#!/bin/bash
# boot-profile.sh

# Parse dmesg for timing
dmesg | awk -F'[\[\]]' '
    /^\\[/ {
        time = $2
        sub(/^[ ]+/, "", $3)
        print time "\t" $3
    }
' | sort -n | head -20

# Find slow initcalls
dmesg | grep "initcall.*took" |
    sort -k8 -n -r | head -10
```

---

## Measuring Improvements

Track optimization progress:

```c
/* Add timing points */
ktime_t start, end;
s64 delta;

start = ktime_get();
/* Operation */
end = ktime_get();

delta = ktime_to_ms(ktime_sub(end, start));
pr_info("Operation took %lld ms\n", delta);
```

---

## Platform-Specific Tips

ARM platforms:
- Skip CPU errata workarounds if not needed
- Optimize ATAG/DTB passing
- Use compressed DTB

x86 platforms:
- Disable unused legacy support
- Skip BIOS/UEFI delays
- Use coreboot for fast boot

---

## Bootloader Optimization

U-Boot speedup:

```bash
# Reduce bootdelay
setenv bootdelay 0

# Skip network init
# CONFIG_CMD_NET is not set

# Direct boot
setenv bootcmd 'mmc read $loadaddr 0x800 0x4000; bootm'
```

---

## Falcon Mode

Skip U-Boot proper:

```bash
# SPL loads kernel directly
CONFIG_SPL_OS_BOOT=y

# Save ~200ms
# SPL → Kernel (skip U-Boot)
```

---

## Multi-Core Boot

Utilize all CPU cores early:

```c
/* Enable secondary CPUs ASAP */
static int __init early_smp_init(void)
{
    /* Bring up all CPUs */
    smp_init();

    /* Parallel initialization */
    on_each_cpu(per_cpu_init, NULL, 0);

    return 0;
}
early_initcall(early_smp_init);
```

---

## Memory Optimization

Faster memory initialization:

```bash
# Skip memory test
CONFIG_MEMTEST=n

# Reduce reserved memory
CONFIG_CMDLINE="mem=exact_size"

# Use huge pages
CONFIG_TRANSPARENT_HUGEPAGE=y
```

---

## Network Boot Optimization

Speed up network boot:

```bash
# Use static IP (skip DHCP)
ip=192.168.1.100::192.168.1.1:255.255.255.0

# Increase NFS read size
nfsroot=server:/path,rsize=32768

# Use TCP instead of UDP
nfsroot=server:/path,tcp
```

---

## Build Time Optimization

Link Time Optimization:

```bash
# Enable LTO
CONFIG_LTO_CLANG=y
# or
CONFIG_LTO_GCC=y

# Results in smaller, faster kernel
```

---

## Target Boot Times

Achievable targets:

| Device Type | Target | Achieved |
|------------|---------|----------|
| TV/STB | < 2s | 0.8s |
| Automotive | < 2s | 1.2s |
| Phone | < 1s | 0.6s |
| IoT Device | < 3s | 1.5s |

---

## Optimization Checklist

1. ✓ Measure baseline boot time
1. ✓ Remove unnecessary features
1. ✓ Use fast compression (LZ4)
1. ✓ Enable async probing
1. ✓ Optimize initcalls
1. ✓ Minimal rootfs
1. ✓ Quiet boot
1. ✓ Preset lpj
1. ✓ Performance CPU governor
1. ✓ Profile and iterate

---

## Common Bottlenecks

Typical slow points:
1. USB enumeration (100-500ms)
1. MMC/SD initialization (200-400ms)
1. Network DHCP (1-3s)
1. Filesystem mounting (100-300ms)
1. Driver probing (varies)

Solutions:
- Defer USB if not critical
- Optimize MMC voltage switching
- Use static IP
- Use faster filesystem
- Async driver probing

---

## Best Practices

1. Profile before optimizing
1. Set realistic targets
1. Focus on critical path
1. Defer non-essential items
1. Test on actual hardware
1. Document optimizations
1. Maintain optimization over time

---

## Summary

Boot optimization requires:
- Systematic measurement
- Understanding boot sequence
- Hardware-specific tuning
- Continuous profiling

Key techniques:
- Kernel configuration
- Async initialization
- Compression selection
- Driver optimization
