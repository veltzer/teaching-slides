# Basic QEMU Usage for Kernel Development

---

Chapter Overview
- Booting kernels with QEMU
- Configuring virtual hardware
- Command-line options for kernel developers

---

QEMU Command Line Basics
- General syntax: qemu-system-[arch] [options] [disk_image]
- Common options: -m (memory), -smp (CPUs), -kernel, -append

---

Kernel Boot Process in QEMU

![basic_qemu_usage_for_kernel_development_1](/svg/courses/operating_systems/qemu-for-kernel-developers/03_qemu_basic_usage/basic_qemu_usage_for_kernel_development_1.svg)

---

Specifying the Kernel Image
- Using -kernel option
- Supported kernel formats
- Kernel image location considerations

---

Kernel Command Line Parameters
- Using -append option
- Common kernel parameters
- Debugging-related parameters

---

Initial RAM Disk (initrd/initramfs)
- Purpose of initrd/initramfs
- Using -initrd option
- Creating custom initrd for testing

---

Root Filesystem Options
- Using disk images as root filesystem
- Network-based root filesystems
- Implications for kernel testing

---

Virtual CPU Configuration
- Specifying CPU model with -cpu
- SMP configuration with -smp
- CPU feature enablement/disablement

---

Memory Configuration
- Setting memory size with -m
- Memory hotplug options
- Testing kernel memory management features

---

Block Device Emulation
- Types of emulated block devices
- Using -hda, -hdb, etc., options
- Attaching disk images and raw devices

---

Network Device Emulation
- Common virtual network adapters
- Basic networking with -net user
- Advanced networking with tap devices

---

Virtual Network Configuration

![basic_qemu_usage_for_kernel_development_2](/svg/courses/operating_systems/qemu-for-kernel-developers/03_qemu_basic_usage/basic_qemu_usage_for_kernel_development_2.svg)

---

PCI Device Emulation and Passthrough
- Emulating PCI devices
- PCI passthrough for testing drivers
- Using -device option

---

USB Device Emulation
- Emulating USB controllers and devices
- USB passthrough options
- Testing USB drivers in QEMU

---

Graphics and Display Options
- VGA emulation options
- Using -nographic for headless operation
- Connecting with VNC or SDL

---

Audio Device Emulation
- Emulating sound cards
- Audio backend configuration
- Testing audio drivers in QEMU

---

QEMU Monitor
- Accessing QEMU monitor (Ctrl-Alt-2 or -monitor)
- Useful monitor commands for kernel developers
- Using monitor to manipulate VM state

---

GDB Integration
- Setting up QEMU for GDB debugging (-s and -S options)
- Connecting GDB to QEMU
- Basic kernel debugging workflow

---

QEMU Tracing and Logging
- Enabling QEMU traces (-trace events)
- Understanding QEMU logs
- Using logs for kernel debugging

---

Snapshotting in QEMU
- Creating and managing snapshots
- Using snapshots for kernel testing
- Snapshot internal mechanics

---

Performance Tuning
- CPU throttling options
- I/O throttling
- Using KVM for near-native performance

---

QEMU and Kernel Modules
- Loading kernel modules in QEMU
- Testing module loading/unloading
- Debugging kernel modules

---

Multi-VM Scenarios
- Running multiple VMs
- Inter-VM communication
- Testing distributed kernel features

---

QEMU Networking Modes
- User networking (SLIRP)
- Bridged networking
- Custom network configurations

---

Storage Performance Testing
- Emulating different storage devices
- I/O scheduling testing
- Block layer benchmarking in QEMU

---

Memory Management Features
- Testing huge pages
- Memory ballooning
- NUMA emulation

---

QEMU Command-line Examples
- Booting a custom kernel with a specific rootfs
- Setting up a multi-core VM with custom networking
- Enabling KVM and performance options

---

Automated Testing with QEMU
- Scripting QEMU for automated tests
- Integrating with CI/CD pipelines
- Kernel regression testing strategies

---

Troubleshooting Common Issues
- Boot failures
- Networking problems
- Performance issues

---

Best Practices for Kernel Development with QEMU
- Organizing disk images and kernel builds
- Version control integration
- Documenting QEMU configurations
