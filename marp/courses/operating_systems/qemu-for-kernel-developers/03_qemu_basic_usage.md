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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="25" width="100" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="45" text-anchor="middle" font-size="11" font-weight="bold">QEMU</text>
  <text x="60" y="60" text-anchor="middle" font-size="10">Loads kernel</text>
  <text x="60" y="73" text-anchor="middle" font-size="10">(-kernel flag)</text>
  <rect x="140" y="25" width="100" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="190" y="45" text-anchor="middle" font-size="11" font-weight="bold">BIOS/UEFI</text>
  <text x="190" y="60" text-anchor="middle" font-size="10">Firmware</text>
  <text x="190" y="73" text-anchor="middle" font-size="10">Init</text>
  <rect x="270" y="25" width="100" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="320" y="45" text-anchor="middle" font-size="11" font-weight="bold">Kernel</text>
  <text x="320" y="60" text-anchor="middle" font-size="10">Decompresses</text>
  <text x="320" y="73" text-anchor="middle" font-size="10">& boots</text>
  <rect x="400" y="25" width="100" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="450" y="45" text-anchor="middle" font-size="11" font-weight="bold">initramfs</text>
  <text x="450" y="60" text-anchor="middle" font-size="10">Early</text>
  <text x="450" y="73" text-anchor="middle" font-size="10">userspace</text>
  <rect x="490" y="110" width="100" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="130" text-anchor="middle" font-size="11" font-weight="bold">Root FS</text>
  <text x="540" y="145" text-anchor="middle" font-size="10">Full system</text>
  <text x="540" y="158" text-anchor="middle" font-size="10">running</text>
  <line x1="110" y1="52" x2="140" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_qemu_basic_usage)"/>
  <line x1="240" y1="52" x2="270" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_qemu_basic_usage)"/>
  <line x1="370" y1="52" x2="400" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_qemu_basic_usage)"/>
  <line x1="500" y1="80" x2="540" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_qemu_basic_usage)"/>
  <defs>
    <marker id="arrowd0_02_qemu_basic_usage" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="170" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="30" text-anchor="middle" font-size="11" font-weight="bold">Guest VM</text>
  <rect x="30" y="40" width="70" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="65" y="56" text-anchor="middle" font-size="10">virtio-net</text>
  <text x="65" y="70" text-anchor="middle" font-size="9">Guest NIC</text>
  <rect x="110" y="40" width="70" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="145" y="56" text-anchor="middle" font-size="10">eth0</text>
  <text x="145" y="70" text-anchor="middle" font-size="9">10.0.2.15</text>
  <rect x="230" y="30" width="140" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">QEMU SLIRP</text>
  <text x="300" y="67" text-anchor="middle" font-size="10">User-mode NAT</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">10.0.2.2 (gw)</text>
  <rect x="410" y="30" width="140" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="50" text-anchor="middle" font-size="11" font-weight="bold">Host Network</text>
  <text x="480" y="67" text-anchor="middle" font-size="10">Host NIC / Internet</text>
  <line x1="190" y1="60" x2="230" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_02_qemu_basic_usage)"/>
  <line x1="370" y1="60" x2="410" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_02_qemu_basic_usage)"/>
  <text x="300" y="120" text-anchor="middle" font-size="10" fill="#555">-net nic,model=virtio -net user,hostfwd=tcp::2222-:22</text>
  <defs>
    <marker id="arrowd1_02_qemu_basic_usage" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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
