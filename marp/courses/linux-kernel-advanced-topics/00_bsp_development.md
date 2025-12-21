# Board Support Package (BSP) Development

---

## What is a BSP?

1. Software layer between hardware and OS kernel
1. Hardware-specific code and configurations
1. Enables Linux to run on specific hardware platforms

<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
<rect x="50" y="220" width="300" height="40" fill="#8B4513" stroke="black"/>
<text x="200" y="245" text-anchor="middle" fill="white">Hardware Platform</text>
<rect x="50" y="160" width="300" height="40" fill="#4169E1" stroke="black"/>
<text x="200" y="185" text-anchor="middle" fill="white">Board Support Package</text>
<rect x="50" y="100" width="300" height="40" fill="#32CD32" stroke="black"/>
<text x="200" y="125" text-anchor="middle">Linux Kernel</text>
<rect x="50" y="40" width="300" height="40" fill="#FFD700" stroke="black"/>
<text x="200" y="65" text-anchor="middle">Applications</text>
</svg>

---

## BSP Components

1. Bootloader configuration
1. Kernel configuration and patches
1. Device drivers
1. Device Tree or board files
1. Root filesystem
1. Build system integration

---

## BSP Architecture

<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="320" width="460" height="60" fill="#8B4513" stroke="black"/>
<text x="250" y="355" text-anchor="middle" fill="white">Hardware (SoC, Memory, Peripherals)</text>
<rect x="20" y="240" width="150" height="60" fill="#4169E1" stroke="black"/>
<text x="95" y="275" text-anchor="middle" fill="white">Bootloader</text>
<rect x="180" y="240" width="150" height="60" fill="#4169E1" stroke="black"/>
<text x="255" y="275" text-anchor="middle" fill="white">Device Tree</text>
<rect x="340" y="240" width="140" height="60" fill="#4169E1" stroke="black"/>
<text x="410" y="275" text-anchor="middle" fill="white">Drivers</text>
<rect x="20" y="160" width="460" height="60" fill="#32CD32" stroke="black"/>
<text x="250" y="195" text-anchor="middle">Linux Kernel</text>
<rect x="20" y="80" width="220" height="60" fill="#FFD700" stroke="black"/>
<text x="130" y="115" text-anchor="middle">Root Filesystem</text>
<rect x="260" y="80" width="220" height="60" fill="#FFD700" stroke="black"/>
<text x="370" y="115" text-anchor="middle">Applications</text>
</svg>

---

## Hardware Abstraction Concepts

1. **Platform independence**: Separate hardware-specific code
1. **Standardized interfaces**: Common APIs for different hardware
1. **Modularity**: Easy to port to new platforms

---

## Hardware Abstraction Layers

```c
/* Hardware-specific implementation */
struct platform_ops {
    void (*init)(void);
    void (*reset)(void);
    int (*get_cpu_freq)(void);
    int (*set_cpu_freq)(int freq);
};

/* Generic interface */
void platform_init(void) {
    if (platform->ops->init)
        platform->ops->init();
}
```

---

## Platform-Specific Initialization

1. CPU initialization
1. Memory controller setup
1. Clock configuration
1. Pin multiplexing
1. Interrupt controller setup
1. Peripheral initialization

---

## Boot Sequence

<svg viewBox="0 0 400 450" xmlns="http://www.w3.org/2000/svg">
<rect x="150" y="20" width="100" height="40" fill="#FF6347" stroke="black"/>
<text x="200" y="45" text-anchor="middle">Power On</text>
<line x1="200" y1="60" x2="200" y2="80" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="150" y="80" width="100" height="40" fill="#FFA500" stroke="black"/>
<text x="200" y="105" text-anchor="middle">ROM Code</text>
<line x1="200" y1="120" x2="200" y2="140" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="150" y="140" width="100" height="40" fill="#FFD700" stroke="black"/>
<text x="200" y="165" text-anchor="middle">SPL/MLO</text>
<line x1="200" y1="180" x2="200" y2="200" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="150" y="200" width="100" height="40" fill="#4169E1" stroke="black"/>
<text x="200" y="225" text-anchor="middle" fill="white">U-Boot</text>
<line x1="200" y1="240" x2="200" y2="260" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="150" y="260" width="100" height="40" fill="#32CD32" stroke="black"/>
<text x="200" y="285" text-anchor="middle">Kernel</text>
<line x1="200" y1="300" x2="200" y2="320" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="150" y="320" width="100" height="40" fill="#87CEEB" stroke="black"/>
<text x="200" y="345" text-anchor="middle">Init</text>
<line x1="200" y1="360" x2="200" y2="380" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="150" y="380" width="100" height="40" fill="#98FB98" stroke="black"/>
<text x="200" y="405" text-anchor="middle">Userspace</text>
<defs>
<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="black"/>
</marker>
</defs>
</svg>

---

## Board Files vs Device Tree

### Board Files (Legacy)
```c
static struct platform_device my_device = {
    .name = "my-device",
    .id = 0,
    .resource = my_resources,
    .dev = {
        .platform_data = &my_pdata,
    },
};
```

### Device Tree (Modern)
```dts
my_device@10000000 {
    compatible = "vendor,my-device";
    reg = <0x10000000 0x1000>;
    interrupts = <42>;
};
```

---

## Evolution: Board Files to Device Tree

1. **Board files**: C code compiled into kernel
1. **Problems**: Kernel bloat, no runtime configuration
1. **Device Tree**: Separate hardware description
1. **Benefits**: Smaller kernel, same kernel for multiple boards

---

## SoC Vendor BSP Structure

```txt
vendor-bsp/
├── bootloader/
│   ├── u-boot/
│   └── spl/
├── kernel/
│   ├── arch/arm/mach-vendor/
│   └── drivers/
├── devicetree/
│   └── vendor-soc.dtsi
└── tools/
    └── flash-tool/
```

---

## Vendor BSP Components

1. **Reference bootloader**: Usually U-Boot with vendor patches
1. **Kernel sources**: Vendor kernel fork with custom drivers
1. **Device trees**: Base DTB for SoC and reference boards
1. **Documentation**: Hardware reference manuals
1. **Tools**: Flashing utilities, debug tools

---

## Customizing Vendor BSPs

1. Start with vendor reference BSP
1. Create custom Device Tree for your board
1. Modify bootloader for your hardware
1. Add/modify drivers as needed
1. Configure kernel for your use case

---

## Custom Board Device Tree

```dts
#include "vendor-soc.dtsi"

/ {
    model = "My Custom Board";
    compatible = "mycompany,custom-board";

    memory@80000000 {
        reg = <0x80000000 0x20000000>;
    };

    leds {
        compatible = "gpio-leds";
        led0 {
            gpios = <&gpio1 2 GPIO_ACTIVE_HIGH>;
        };
    };
};
```

---

## BSP Directory Structure

```txt
my-bsp/
├── configs/
│   └── myboard_defconfig
├── board/
│   └── myboard/
│       ├── board.c
│       └── Makefile
├── dts/
│   └── myboard.dts
├── patches/
│   ├── kernel/
│   └── u-boot/
└── scripts/
    └── build.sh
```

---

## BSP Build Process

<svg viewBox="0 0 450 350" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="20" width="120" height="40" fill="#FFE4B5" stroke="black"/>
<text x="80" y="45" text-anchor="middle">Sources</text>
<rect x="160" y="20" width="120" height="40" fill="#FFE4B5" stroke="black"/>
<text x="220" y="45" text-anchor="middle">Patches</text>
<rect x="300" y="20" width="120" height="40" fill="#FFE4B5" stroke="black"/>
<text x="360" y="45" text-anchor="middle">Config</text>
<line x1="80" y1="60" x2="220" y2="100" stroke="black" stroke-width="2"/>
<line x1="220" y1="60" x2="220" y2="100" stroke="black" stroke-width="2"/>
<line x1="360" y1="60" x2="220" y2="100" stroke="black" stroke-width="2"/>
<rect x="160" y="100" width="120" height="40" fill="#87CEEB" stroke="black"/>
<text x="220" y="125" text-anchor="middle">Build System</text>
<line x1="220" y1="140" x2="220" y2="180" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
<rect x="70" y="180" width="100" height="40" fill="#98FB98" stroke="black"/>
<text x="120" y="205" text-anchor="middle">Bootloader</text>
<rect x="175" y="180" width="100" height="40" fill="#98FB98" stroke="black"/>
<text x="225" y="205" text-anchor="middle">Kernel</text>
<rect x="280" y="180" width="100" height="40" fill="#98FB98" stroke="black"/>
<text x="330" y="205" text-anchor="middle">RootFS</text>
<line x1="120" y1="220" x2="220" y2="260" stroke="black" stroke-width="2"/>
<line x1="225" y1="220" x2="220" y2="260" stroke="black" stroke-width="2"/>
<line x1="330" y1="220" x2="220" y2="260" stroke="black" stroke-width="2"/>
<rect x="160" y="260" width="120" height="40" fill="#FFD700" stroke="black"/>
<text x="220" y="285" text-anchor="middle">BSP Image</text>
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="black"/>
</marker>
</defs>
</svg>

---

## BSP Validation

1. **Hardware validation**
    - Memory tests
    - Peripheral enumeration
    - Clock verification
1. **Software validation**
    - Boot tests
    - Driver functionality
    - Performance benchmarks

---

## Hardware Validation Tests

```bash
# Memory test
memtester 100M 1

# CPU stress test
stress-ng --cpu 4 --timeout 60s

# Storage test
dd if=/dev/zero of=/tmp/test bs=1M count=100

# Network test
iperf3 -c server_ip
```

---

## BSP Testing Checklist

1. Boot from all supported media (SD, eMMC, NFS)
1. Verify all peripherals detected
1. Test power management states
1. Validate interrupt handling
1. Check thermal management
1. Stress test under load

---

## Common BSP Issues

1. **Boot failures**: Wrong memory configuration
1. **Missing devices**: Incorrect Device Tree
1. **Performance issues**: Wrong clock settings
1. **Instability**: Power supply problems
1. **Driver crashes**: Hardware/software mismatch

---

## Debugging BSP Issues

```bash
# Check kernel messages
dmesg | grep -i error

# Verify device tree
dtc -I fs /sys/firmware/devicetree/base

# Monitor interrupts
watch -n1 cat /proc/interrupts

# Check memory map
cat /proc/iomem
```

---

## BSP Documentation Requirements

1. **Hardware description**
    - SoC specifications
    - Board schematics
    - Pin mappings
1. **Software guide**
    - Build instructions
    - Flash procedures
    - Configuration options

---

## BSP Documentation Template

```markdown
## Board: MyCustom Board v1.0
### Hardware
- SoC: Vendor XYZ123
- RAM: 2GB DDR4
- Storage: 16GB eMMC
### Building
1. Configure: make myboard_defconfig
1. Build: make
### Flashing
1. Connect USB cable
1. Run: flash_tool image.bin
```

---

## BSP Maintenance

1. **Version control**: Git for tracking changes
1. **Patch management**: Organize patches by component
1. **Testing**: Automated CI/CD pipelines
1. **Updates**: Track vendor releases
1. **Security**: Monitor CVEs and apply fixes

---

## BSP Version Management

```bash
# Tag releases
git tag -a v1.0.0 -m "Initial BSP release"

# Branch for products
git checkout -b product-v1.0

# Track vendor updates
git remote add vendor https://vendor/bsp.git
git fetch vendor
```

---

## BSP Optimization Strategies

1. **Size optimization**
    - Remove unused drivers
    - Optimize kernel config
    - Compress binaries
1. **Boot time optimization**
    - Parallel initialization
    - Defer non-critical drivers
    - Optimize bootloader

---

## Memory Layout Planning

<svg viewBox="0 0 400 450" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="20" width="200" height="40" fill="#FF6347" stroke="black"/>
<text x="200" y="45" text-anchor="middle">0x00000000 - Boot ROM</text>
<rect x="100" y="60" width="200" height="40" fill="#FFA500" stroke="black"/>
<text x="200" y="85" text-anchor="middle">0x40000000 - SRAM</text>
<rect x="100" y="100" width="200" height="60" fill="#4169E1" stroke="black"/>
<text x="200" y="135" text-anchor="middle" fill="white">0x80000000 - DDR Base</text>
<rect x="100" y="160" width="200" height="40" fill="#32CD32" stroke="black"/>
<text x="200" y="185" text-anchor="middle">0x80008000 - Kernel</text>
<rect x="100" y="200" width="200" height="40" fill="#87CEEB" stroke="black"/>
<text x="200" y="225" text-anchor="middle">0x88000000 - Device Tree</text>
<rect x="100" y="240" width="200" height="40" fill="#98FB98" stroke="black"/>
<text x="200" y="265" text-anchor="middle">0x88100000 - Initramfs</text>
<rect x="100" y="280" width="200" height="100" fill="#FFE4B5" stroke="black"/>
<text x="200" y="335" text-anchor="middle">0x90000000 - User Space</text>
<rect x="100" y="380" width="200" height="40" fill="#DDA0DD" stroke="black"/>
<text x="200" y="405" text-anchor="middle">0xF0000000 - Peripherals</text>
</svg>

---

## BSP Security Considerations

1. **Secure boot chain**
    - Signed bootloader
    - Verified kernel
    - Encrypted filesystem
1. **Hardware security**
    - TrustZone configuration
    - Secure key storage
    - Hardware crypto acceleration

---

## Secure Boot Implementation

```c
/* Bootloader verification */
int verify_image(void *image, size_t size) {
    struct sig_header *sig;
    int ret;

    sig = (struct sig_header *)
          (image + size - sizeof(*sig));

    ret = rsa_verify(image, size - sizeof(*sig),
                     sig, public_key);

    return ret;
}
```

---

## BSP Power Management

1. **Clock gating**: Disable unused clocks
1. **Power domains**: Control power to subsystems
1. **Voltage scaling**: Adjust core voltages
1. **Sleep states**: Configure suspend modes

---

## Clock Tree Configuration

```dts
clocks {
    osc: oscillator {
        compatible = "fixed-clock";
        #clock-cells = <0>;
        clock-frequency = <24000000>;
    };

    pll: pll@10000000 {
        compatible = "vendor,pll";
        reg = <0x10000000 0x100>;
        clocks = <&osc>;
        #clock-cells = <1>;
    };
};
```

---

## BSP Performance Tuning

1. **CPU optimization**
    - Governor selection
    - Cache configuration
    - SMP balancing
1. **Memory optimization**
    - DDR timing
    - Memory bandwidth
    - Cache coherency

---

## Vendor BSP Integration

<svg viewBox="0 0 450 300" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="120" width="120" height="60" fill="#FFE4B5" stroke="black"/>
<text x="80" y="155" text-anchor="middle">Vendor BSP</text>
<rect x="160" y="120" width="120" height="60" fill="#87CEEB" stroke="black"/>
<text x="220" y="155" text-anchor="middle">Custom Code</text>
<rect x="300" y="120" width="120" height="60" fill="#98FB98" stroke="black"/>
<text x="360" y="155" text-anchor="middle">Product BSP</text>
<line x1="140" y1="150" x2="160" y2="150" stroke="black" stroke-width="2" marker-end="url(#arr)"/>
<line x1="280" y1="150" x2="300" y2="150" stroke="black" stroke-width="2" marker-end="url(#arr)"/>
<text x="80" y="210" text-anchor="middle">Updates</text>
<text x="220" y="210" text-anchor="middle">Features</text>
<text x="360" y="210" text-anchor="middle">Release</text>
<line x1="80" y1="180" x2="80" y2="195" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
<line x1="220" y1="180" x2="220" y2="195" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
<line x1="360" y1="180" x2="360" y2="195" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
<defs>
<marker id="arr" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="black"/>
</marker>
</defs>
</svg>

---

## BSP Best Practices

1. **Modular design**: Separate board-specific code
1. **Version control**: Track all changes
1. **Documentation**: Maintain comprehensive docs
1. **Testing**: Automated test suites
1. **Upstream first**: Contribute changes upstream
1. **Security**: Regular security audits

---

## Summary

1. BSP bridges hardware and Linux kernel
1. Consists of bootloader, kernel, drivers, Device Tree
1. Vendor BSPs need customization for products
1. Validation and testing are critical
1. Documentation ensures maintainability
1. Security must be considered from start
