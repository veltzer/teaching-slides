---
tags:
  - concepts:io
  - concepts:computer-architecture
  - concepts:pcie
  - concepts:interrupts
level: beginner
category: hardware
audience:
  - audiences:developers
  - audiences:sysadmins

---
# I/O Architecture and Bus Systems

---

## Table of Contents

1. I/O Architecture Overview
1. Bus Fundamentals
1. PCIe (PCI Express)
1. USB Architecture
1. SATA and NVMe
1. Interrupts: Hardware and Software
1. Polling vs Interrupts
1. DMA in Depth
1. I/O Scheduling
1. Device Drivers Overview

---
## I/O Architecture Overview: Overview

The I/O subsystem connects the CPU and memory to the outside world:
peripherals, storage, network, and user devices.

---
## I/O Architecture Overview

![i_o_architecture_overview](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/i_o_architecture_overview.svg)

---
## Bus Fundamentals: Comparison

A bus is a communication system that transfers data between components.

**Key bus characteristics:**

| Property | Description |
|----------|-------------|
| Width | Number of parallel data lines (bits per transfer) |
| Clock speed | Frequency of data transfers |
| Bandwidth | Width x Clock x Transfers_per_clock |
| Topology | Shared bus, point-to-point, switched fabric |
| Protocol | Rules for communication (addressing, arbitration) |

**Historical evolution:**

---
## Bus Fundamentals

![bus_fundamentals](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/bus_fundamentals.svg)

---
## PCIe: PCI Express: Details

PCIe is the primary high-speed bus in modern computers, used for GPUs,
NVMe SSDs, network cards, and more.

**Key concepts:**
- Serial, point-to-point (not shared bus)
- Scalable through "lanes" (x1, x2, x4, x8, x16)
- Each lane is a pair of differential signal lines (TX + RX)
- Full duplex: simultaneous send and receive

---
## PCIe: PCI Express

![pcie_pci_express](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/pcie_pci_express.svg)

---

## PCIe Generations

| Generation | Year | Per-Lane Rate | x1 Bandwidth | x16 Bandwidth |
|-----------|------|---------------|-------------|---------------|
| PCIe 1.0 | 2003 | 2.5 GT/s | 250 MB/s | 4 GB/s |
| PCIe 2.0 | 2007 | 5 GT/s | 500 MB/s | 8 GB/s |
| PCIe 3.0 | 2010 | 8 GT/s | ~1 GB/s | ~16 GB/s |
| PCIe 4.0 | 2017 | 16 GT/s | ~2 GB/s | ~32 GB/s |
| PCIe 5.0 | 2019 | 32 GT/s | ~4 GB/s | ~64 GB/s |
| PCIe 6.0 | 2022 | 64 GT/s | ~8 GB/s | ~128 GB/s |

Each generation doubles the bandwidth. GT/s = gigatransfers per second.
Actual data bandwidth is slightly less due to encoding overhead
(128b/130b encoding for PCIe 3.0+).

**Typical allocations:**
- GPU: PCIe x16
- NVMe SSD: PCIe x4
- Network card (25/100 GbE): PCIe x8 or x16
- WiFi card: PCIe x1

---

## PCIe Configuration Space

Every PCIe device has a configuration space that the OS reads to identify
and configure the device:

```bash
# List all PCIe devices
lspci

# Example output:
# 00:00.0 Host bridge: Intel Corporation...
# 00:02.0 VGA compatible controller: Intel Corporation...
# 01:00.0 3D controller: NVIDIA Corporation...
# 02:00.0 Non-Volatile memory controller: Samsung Electronics...

# Verbose info for a device
lspci -v -s 02:00.0

# Show PCIe link speed and width
lspci -vv -s 01:00.0 | grep -i "lnksta\|lnkcap"
# LnkCap: Speed 16GT/s, Width x16  (capable of)
# LnkSta: Speed 16GT/s, Width x16  (currently running)
```

PCIe BARs (Base Address Registers) tell the OS where device memory and
registers are mapped in the physical address space (MMIO).

---
## USB Architecture: Overview

USB (Universal Serial Bus) is a tiered-star topology for connecting
peripherals:

---
## USB Architecture

![usb_architecture](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/usb_architecture.svg)

---
## USB Architecture: Details

**Key design choices:**
- Host-controlled: all transfers are initiated by the host
- Up to 127 devices per host controller
- Hot-pluggable
- Provides power (up to 240W with USB PD)

---

## USB Generations

| Standard | Year | Speed | Name | Connector |
|----------|------|-------|------|-----------|
| USB 1.0 | 1996 | 1.5 Mbps | Low Speed | Type-A |
| USB 1.1 | 1998 | 12 Mbps | Full Speed | Type-A |
| USB 2.0 | 2000 | 480 Mbps | High Speed | Type-A, Mini, Micro |
| USB 3.0 | 2008 | 5 Gbps | SuperSpeed | Type-A (blue), Type-C |
| USB 3.1 | 2013 | 10 Gbps | SuperSpeed+ | Type-C |
| USB 3.2 | 2017 | 20 Gbps | SuperSpeed+ | Type-C (2 lanes) |
| USB4 | 2019 | 40 Gbps | USB4 | Type-C only |
| USB4 v2 | 2022 | 80 Gbps | USB4 v2 | Type-C only |

USB4 is based on the Thunderbolt 3 protocol and can tunnel PCIe and
DisplayPort signals through a USB-C cable.

---
## USB Transfer Types: Comparison

USB defines four transfer types for different use cases:

| Transfer Type | Use Case | Latency | Guaranteed BW | Error Recovery |
|--------------|----------|---------|---------------|----------------|
| Control | Configuration, setup | Low priority | No | Retry |
| Bulk | Mass storage, printing | Best-effort | No | Retry |
| Interrupt | Keyboard, mouse | Guaranteed polling | Yes | Retry |
| Isochronous | Audio, video | Guaranteed timing | Yes | No retry |

---
## USB Transfer Types

![usb_transfer_types](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/usb_transfer_types.svg)

---
## SATA and NVMe: Overview

Two storage interfaces with very different architectures:

---
## SATA and NVMe

![sata_and_nvme](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/sata_and_nvme.svg)

---
## SATA and NVMe: Comparison

| Feature | SATA (AHCI) | NVMe |
|---------|-------------|------|
| Interface | SATA 3.0 | PCIe (x2 or x4) |
| Max bandwidth | 600 MB/s | ~7 GB/s (PCIe 4.0 x4) |
| Command queues | 1 | Up to 65535 |
| Queue depth | 32 | 65536 per queue |
| Latency | ~100 us | ~10-20 us |
| CPU overhead | Higher (AHCI legacy) | Lower (streamlined) |
| Protocol | AHCI (designed for HDD) | NVMe (designed for flash) |

NVMe is ~10x faster than SATA for SSDs because it eliminates the
bottleneck of the SATA protocol (designed for spinning disks).

---

## Interrupts: Overview

An interrupt is a signal that tells the CPU to stop what it is doing
and handle an event.

```python
Normal execution:
┌─────────────────────────────────────────────────┐
│ Instr 1 │ Instr 2 │ Instr 3 │ Instr 4 │ Instr 5│
└─────────────────────────────────────────────────┘

With interrupt:
┌──────────┬────────────────────────┬──────────────┐
│ Instr 1  │   Interrupt Handler    │ Instr 2      │
│          │   (ISR)                │ (resume)     │
└──────────┴────────────────────────┴──────────────┘
           ^                        ^
           │ Interrupt arrives      │ IRET (return from interrupt)
           │ Save state             │ Restore state
```

**Types of interrupts:**
- **Hardware interrupts**: from external devices (keyboard, NIC, timer)
- **Software interrupts**: triggered by instructions (INT, SYSCALL)
- **Exceptions**: caused by CPU errors (divide by zero, page fault)

---
## Hardware Interrupt Flow: Overview

When a hardware device needs attention, this happens:

---
## Hardware Interrupt Flow

![hardware_interrupt_flow](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/hardware_interrupt_flow.svg)

---
## Hardware Interrupt Flow: Overview (2)

The APIC (Advanced Programmable Interrupt Controller) manages priorities
and routes interrupts to the correct CPU core in multi-core systems.

---

## Interrupt Types on x86

```asm
Interrupt Vector Table (IDT - Interrupt Descriptor Table):
┌────────┬────────────────────────────────┐
│ Vector │ Description                    │
├────────┼────────────────────────────────┤
│   0    │ Divide Error (#DE)             │
│   1    │ Debug (#DB)                    │
│   2    │ NMI (Non-Maskable Interrupt)   │
│   3    │ Breakpoint (#BP)               │
│   6    │ Invalid Opcode (#UD)           │
│   8    │ Double Fault (#DF)             │
│  13    │ General Protection Fault (#GP) │
│  14    │ Page Fault (#PF)               │
│ 32-255 │ User-defined / device IRQs     │
│  128   │ System call (int 0x80, legacy) │
└────────┴────────────────────────────────┘
```

**Exceptions** (vectors 0-31): generated by the CPU itself
- Faults: can be corrected, re-execute the instruction (e.g., page fault)
- Traps: reported after the instruction (e.g., breakpoint)
- Aborts: unrecoverable (e.g., double fault)

**External interrupts** (vectors 32-255): from devices via APIC

---

## MSI and MSI-X: Modern Interrupts

Legacy interrupts use physical interrupt lines (shared, limited).
Modern PCIe devices use **Message Signaled Interrupts** (MSI/MSI-X):

```bash
Legacy (line-based):
┌────────┐  IRQ pin  ┌──────┐  shared line  ┌─────┐
│ Device │──────────►│ APIC │◄──────────────│Dev B│
└────────┘           └──────┘               └─────┘
Problem: shared lines, need to poll all devices on that line

MSI-X (message-based):
┌────────┐  Memory write to  ┌─────┐
│ Device │  special address  │ CPU │
│        │──────────────────►│     │
└────────┘                   └─────┘
  No shared lines! Each device/queue gets its own vector.
```

**MSI-X advantages:**
- Up to 2048 interrupt vectors per device
- Each vector targets a specific CPU core (better load balancing)
- No sharing, no need to poll
- Lower latency
- Essential for NVMe (one interrupt per queue per core)

---

## Polling vs Interrupts

Two fundamental strategies for checking if a device needs attention:

```asm
Polling:
┌─────────────────────────────────────────────────────────┐
│ CPU repeatedly checks device status register            │
│                                                         │
│   while (device_status_reg & READY == 0) {              │
│       // busy wait -- CPU is wasting cycles             │
│   }                                                     │
│   // now handle the data                                │
└─────────────────────────────────────────────────────────┘

Interrupts:
┌─────────────────────────────────────────────────────────┐
│ CPU does other work until device sends interrupt        │
│                                                         │
│   enable_interrupt(device);                             │
│   // CPU does useful work...                            │
│   // ...                                                │
│   // INTERRUPT! → jump to ISR → handle data → return   │
└─────────────────────────────────────────────────────────┘
```

---

## Polling vs Interrupts: Tradeoffs

| Aspect | Polling | Interrupts |
|--------|---------|------------|
| CPU usage | Wastes cycles checking | CPU free until event |
| Latency | Predictable (poll interval) | Variable (ISR overhead) |
| Throughput (low load) | Wasteful | Efficient |
| Throughput (high load) | Can be efficient | Interrupt storm risk |
| Complexity | Simple | Complex (ISR, concurrency) |
| Power | High (CPU always busy) | Low (CPU can sleep) |
| Best for | High-frequency events | Infrequent events |

### Modern approach: hybrid (NAPI in Linux networking)

```c
Normal: interrupt-driven (low CPU, low latency)
        │
        │ Traffic increases
        v
High load: switch to polling mode
           (process packets in batches, avoid interrupt storm)
        │
        │ Traffic decreases
        v
Back to: interrupt-driven
```

This adaptive approach gives low latency at low load and high throughput
at high load.

---

## NAPI: Linux Network Polling

Linux uses NAPI (New API) for network drivers -- a hybrid approach:

```bash
┌─────────────────────────────────────────────────┐
│                NAPI Flow                        │
│                                                 │
│  1. Packet arrives → Hardware interrupt          │
│                                                 │
│  2. ISR (top half):                              │
│     - Disable further interrupts for this device │
│     - Schedule NAPI poll (softirq)               │
│                                                 │
│  3. NAPI poll (bottom half):                     │
│     - Process up to 'budget' packets             │
│     - If more packets: continue polling           │
│     - If no more packets:                         │
│       - Re-enable interrupts                      │
│       - Return to interrupt-driven mode           │
│                                                 │
│  Result: batched processing under high load,     │
│          low latency under low load              │
└─────────────────────────────────────────────────┘
```

At 100 Gbps, a NIC can receive ~150 million packets per second.
At that rate, interrupting per-packet would overwhelm the CPU.
NAPI processes hundreds of packets per poll cycle.

---

## DMA: Deep Dive

DMA (Direct Memory Access) is essential for high-performance I/O.
Without it, the CPU would be the bottleneck for all data transfers.

**DMA Descriptor Ring (used by NIC, NVMe, etc.):**

```bash
                    ┌──────────────────────────┐
                    │      DMA Descriptors     │
                    │      (Ring Buffer)       │
                    │                          │
                    │  ┌────┐ ┌────┐ ┌────┐   │
              ┌────►│  │ D0 │ │ D1 │ │ D2 │   │
              │     │  └──┬─┘ └──┬─┘ └──┬─┘   │
              │     │     │      │      │      │
  ┌───────┐   │     │  ┌──┴─┐ ┌──┴─┐ ┌──┴─┐   │
  │Device │───┘     │  │Buf0│ │Buf1│ │Buf2│   │
  │(NIC)  │         │  └────┘ └────┘ └────┘   │
  └───────┘         │  Memory buffers          │
                    └──────────────────────────┘

Each descriptor contains:
┌──────────────────────────────────────────┐
│ Buffer physical address                  │
│ Buffer length                            │
│ Status flags (owned by HW or SW)         │
│ Completion flags                         │
└──────────────────────────────────────────┘
```

The device reads descriptors, performs DMA to/from the buffers,
and marks descriptors as complete.

---
## DMA: Scatter-Gather: Overview

Modern DMA controllers support scatter-gather, which allows a single
DMA operation to transfer data to/from multiple non-contiguous memory
regions:

---
## DMA: Scatter-Gather

![dma_scatter_gather](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/dma_scatter_gather.svg)

---
## DMA: Scatter-Gather: Overview (2)

This avoids copying data into contiguous buffers, saving CPU time
and memory bandwidth. Essential for network stacks (packet headers
and payloads are often in different buffers).

---

## IOMMU: I/O Memory Management Unit

The IOMMU provides address translation and protection for DMA:

```bash
Without IOMMU:
┌────────┐  Physical address   ┌────────┐
│ Device │ ───────────────────►│ Memory │  Device can access ANY memory!
└────────┘                     └────────┘  Security risk!

With IOMMU:
┌────────┐  Device virtual    ┌────────┐  Physical    ┌────────┐
│ Device │  address           │ IOMMU  │  address     │ Memory │
│        │ ──────────────────►│        │─────────────►│        │
└────────┘                    └────────┘              └────────┘
                               Translates & validates
                               (like MMU for devices)
```

**IOMMU benefits:**
- **Security**: device can only access memory regions assigned to it
- **Virtualization**: VMs can safely pass devices through (VFIO)
- **64-bit DMA**: old 32-bit devices can address all of memory
- **Bounce buffer elimination**: no need to copy to low memory

Intel calls it VT-d, AMD calls it AMD-Vi.

---

## I/O Scheduling

When multiple I/O requests compete for a storage device, the I/O
scheduler decides the order:

**For HDDs (seeks are expensive):**

```bash
Disk head position: ───────────────►

  Request queue: 98, 183, 37, 122, 14, 124, 65, 67

  FIFO (no scheduling):
  98 → 183 → 37 → 122 → 14 → 124 → 65 → 67
  Total head movement: 640 tracks

  Elevator (SCAN):
  37 → 65 → 67 → 98 → 122 → 124 → 183 → 14
  Total head movement: 332 tracks (48% less seeking)
```

**For SSDs (no seek penalty):**
I/O scheduling is less important. Linux uses `none`/`noop` or `mq-deadline`.

```bash
# Check current scheduler
cat /sys/block/sda/queue/scheduler
# [mq-deadline] kyber bfq none

# Change scheduler
echo "none" > /sys/block/nvme0n1/queue/scheduler
```

---
## Linux I/O Schedulers: Comparison

| Scheduler | Best For | Strategy |
|-----------|----------|----------|
| `none` (noop) | NVMe SSDs | No reordering, direct submission |
| `mq-deadline` | SSDs, general | Deadline-based, prevents starvation |
| `bfq` | Desktop, latency-sensitive | Budget Fair Queuing, good for interactive |
| `kyber` | Fast SSDs | Lightweight, token-based |

**mq-deadline** maintains separate read and write queues with deadlines:

---
## Linux I/O Schedulers

![linux_i_o_schedulers](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/linux_i_o_schedulers.svg)

---
## Device Drivers: Overview: Overview

Device drivers are kernel modules that translate OS requests into
hardware-specific operations:

---
## Device Drivers: Overview

![device_drivers_overview](svg/courses/hardware/computer-architecture-fundamentals/04_io_and_buses/device_drivers_overview.svg)

---

## Device Driver Types in Linux

| Type | Interface | Examples |
|------|-----------|---------|
| Character | `/dev/ttyS0`, `/dev/random` | Serial ports, input devices |
| Block | `/dev/sda`, `/dev/nvme0n1` | Disks, SSDs |
| Network | `eth0`, `wlan0` | Ethernet, WiFi adapters |

```bash
# List loaded kernel modules (drivers)
lsmod

# Example output:
# Module                  Size  Used by
# nvidia               2461696  48
# e1000e                 286720  0
# snd_hda_intel           57344  2
# nvme                    49152  3
# xhci_hcd               90112  1  xhci_pci

# Info about a module
modinfo nvme
# filename:       /lib/modules/.../nvme.ko
# license:        GPL
# description:    NVM Express device driver

# View device major/minor numbers
ls -la /dev/sda /dev/nvme0n1
# brw-rw---- 1 root disk   8, 0 ... /dev/sda      (major 8, minor 0)
# brw-rw---- 1 root disk 259, 0 ... /dev/nvme0n1   (major 259, minor 0)
```

---

## Viewing I/O Information on Linux

```bash
# List all PCI devices with details
lspci -v

# List USB devices
lsusb
lsusb -t    # tree view showing bus topology

# List block devices
lsblk

# Example output:
# NAME        MAJ:MIN  SIZE TYPE MOUNTPOINT
# nvme0n1     259:0   512G disk
# ├─nvme0n1p1 259:1   512M part /boot/efi
# ├─nvme0n1p2 259:2   511G part /
# sda           8:0     2T disk
# └─sda1        8:1     2T part /data

# View interrupt statistics
cat /proc/interrupts

# View I/O statistics in real time
iostat -x 1

# View DMA mappings
cat /proc/iomem | head -20
```

---

## Interrupt Affinity and Performance

For high-performance I/O, you can pin interrupts to specific CPU cores:

```bash
# View interrupt counts per CPU core
cat /proc/interrupts | head -5
#            CPU0       CPU1       CPU2       CPU3
# 0:        45         0          0          0    IO-APIC  timer
# 1:        0          892        0          0    IO-APIC  i8042
# 8:        0          0          1          0    IO-APIC  rtc0
# 130:      0          0          0          5892 PCI-MSI  nvme0q1

# Set interrupt affinity (pin IRQ 130 to CPU 3)
echo 8 > /proc/irq/130/smp_affinity  # bitmask: CPU 3 = bit 3 = 0x8

# Or use irqbalance daemon for automatic balancing
systemctl status irqbalance
```

**Best practice for NVMe/NIC**: assign each device queue's interrupt to the
same CPU core that processes that queue. This keeps data in that core's
cache and avoids cross-core communication.

---

## Summary: I/O and Buses

| Topic | Key Points |
|-------|-----------|
| PCIe | Serial point-to-point, scalable lanes, doubles BW each gen |
| USB | Tiered-star, host-controlled, 4 transfer types |
| SATA vs NVMe | NVMe: PCIe direct, 65k queues, ~10x faster than SATA |
| Interrupts | Hardware (APIC), software (INT), exceptions (page fault) |
| MSI-X | Message-based interrupts, per-queue, no sharing |
| Polling vs IRQ | Hybrid (NAPI) is best: IRQ at low load, poll at high load |
| DMA | Device transfers data directly, scatter-gather for non-contiguous |
| IOMMU | Address translation and protection for device DMA |
| I/O scheduling | `none` for NVMe, `mq-deadline` for general use |
| Device drivers | Char, block, network; kernel modules in Linux |
