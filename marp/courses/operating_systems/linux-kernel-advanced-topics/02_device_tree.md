---
tags:
  - infrastructure:linux
  - concepts:kernel
  - concepts:device-tree
  - infrastructure:embedded
level: advanced
category: operating-systems
audience:
  - audiences:developers

---

# Device Tree

---

## What is Device Tree?: Details
1. Hardware description in a tree structure
1. Separates hardware config from kernel code
1. Human-readable text format
1. Compiled to binary for bootloader/kernel

---

## What is Device Tree?

![what_is_device_tree](svg/courses/operating_systems/linux-kernel-advanced-topics/02_device_tree/what_is_device_tree.svg)

---

## Device Tree History

1. **PowerPC origin**: Started with OpenFirmware
1. **ARM adoption**: Replaced board files (2011)
1. **Widespread use**: Now used by ARM, PowerPC, RISC-V
1. **Standardization**: devicetree.org specification

---

## DTS vs DTB vs DTSI

1. **DTS** (Device Tree Source)
    - Human-readable source file
    - `.dts` extension
1. **DTB** (Device Tree Blob)
    - Compiled binary format
    - `.dtb` extension
1. **DTSI** (Device Tree Source Include)
    - Common definitions
    - `.dtsi` extension

---

## Basic DTS Structure

```dts
/dts-v1/;

/ {
    model = "My Board";
    compatible = "vendor,board";

    cpus {
        cpu@0 {
            compatible = "arm,cortex-a53";
            reg = <0>;
        };
    };

    memory@80000000 {
        device_type = "memory";
        reg = <0x80000000 0x40000000>;
    };
};
```

---

## Device Tree Nodes

```dts
node-name@unit-address {
    property1 = <value>;
    property2 = "string";
    property3;  /* boolean property */

    child-node {
        /* nested node */
    };
};
```

---

## Node Naming Convention

1. **node-name**: Descriptive name (letters, digits, -, _)
1. **@unit-address**: Address from `reg` property
1. **Standard names**: `cpu`, `memory`, `ethernet`, `serial`

```dts
serial@10000000 {    /* name@address */
    compatible = "ns16550";
    reg = <0x10000000 0x100>;
};
```

---

## Property Types

```dts
/* Empty (boolean) */
property;

/* String */
property = "string value";

/* String list */
property = "string1", "string2";

/* Cells (32-bit values) */
property = <0x12345678>;

/* Cell array */
property = <0x1 0x2 0x3>;

/* Mixed */
property = "string", <0x123>;

/* Byte string */
property = [00 11 22 33];
```

---

## Compatible Property

1. Most specific to most general
1. Used for driver matching
1. Format: `"vendor,device"`

```dts
uart@10000000 {
    compatible = "vendor,uart-v2",
                 "vendor,uart",
                 "ns16550";
};
```

---

## Reg Property

Defines address and size of device registers

```dts
/* Single range */
reg = <base_address size>;

/* Multiple ranges */
device@10000000 {
    reg = <0x10000000 0x1000>,  /* Control regs */
          <0x10001000 0x1000>;   /* Data buffer */
};
```

---

## Address Cells and Size Cells

```dts
parent {
    #address-cells = <2>;  /* 64-bit addresses */
    #size-cells = <1>;     /* 32-bit sizes */

    child@100000000 {
        /* high 32-bits, low 32-bits, size */
        reg = <0x1 0x00000000 0x10000>;
    };
};
```

---

## Interrupt Specification

![interrupt_specification](svg/courses/operating_systems/linux-kernel-advanced-topics/02_device_tree/interrupt_specification.svg)

---

## Interrupt Properties

```dts
interrupt-controller@10000000 {
    compatible = "arm,gic-v3";
    interrupt-controller;
    #interrupt-cells = <3>;
    reg = <0x10000000 0x10000>;
};

device@20000000 {
    interrupts = <0 42 4>;
    /* GIC_SPI, IRQ 42, Active High Level */
    interrupt-parent = <&intc>;
};
```

---

## Interrupt Types

```dts
/* GIC interrupt types */
interrupts = <type irq_num flags>;

/* type: */
/* 0 = SPI (Shared Peripheral Interrupt) */
/* 1 = PPI (Private Peripheral Interrupt) */

/* flags: */
/* 1 = Rising Edge */
/* 2 = Falling Edge */
/* 4 = Active High Level */
/* 8 = Active Low Level */
```

---

## Clock Specification

```dts
clocks {
    osc: oscillator {
        compatible = "fixed-clock";
        #clock-cells = <0>;
        clock-frequency = <24000000>;
    };
};

uart@10000000 {
    compatible = "vendor,uart";
    clocks = <&osc>;
    clock-names = "baudclk";
};
```

---

## Pin Multiplexing

```dts
pinctrl@10000000 {
    compatible = "vendor,pinctrl";

    uart0_pins: uart0 {
        pins = "PA0", "PA1";
        function = "uart0";
        bias-pull-up;
    };
};

uart@20000000 {
    pinctrl-names = "default";
    pinctrl-0 = <&uart0_pins>;
};
```

---

## GPIO Specification

```dts
gpio0: gpio@10000000 {
    compatible = "vendor,gpio";
    gpio-controller;
    #gpio-cells = <2>;
    reg = <0x10000000 0x100>;
};

led {
    compatible = "gpio-leds";
    led0 {
        gpios = <&gpio0 5 GPIO_ACTIVE_HIGH>;
        label = "status";
    };
};
```

---

## Phandles and References

```dts
/* Define with label */
intc: interrupt-controller@10000000 {
    interrupt-controller;
    #interrupt-cells = <3>;
};

/* Reference with & */
device@20000000 {
    interrupt-parent = <&intc>;
};

/* Explicit phandle (rarely used) */
node {
    phandle = <1>;
};
```

---

## Device Tree Includes

```dts
/* Include DTSI file */
#include "soc.dtsi"
#include <dt-bindings/gpio/gpio.h>

/ {
    /* Override properties from included files */
    memory@80000000 {
        reg = <0x80000000 0x20000000>;
    };
};
```

---

## Overriding Properties

```dts
/* In soc.dtsi */
uart0: serial@10000000 {
    compatible = "ns16550";
    reg = <0x10000000 0x100>;
    status = "disabled";
};

/* In board.dts */
&uart0 {
    status = "okay";
    clock-frequency = <48000000>;
};
```

---

## Status Property

```dts
device@10000000 {
    compatible = "vendor,device";
    reg = <0x10000000 0x1000>;

    /* Status values: */
    status = "okay";       /* Enabled */
    status = "disabled";   /* Not available */
    status = "reserved";   /* Not for OS */
    status = "fail";       /* Detected error */
};
```

---

## Chosen Node

```dts
chosen {
    bootargs = "console=ttyS0,115200 root=/dev/mmcblk0p1";
    stdout-path = "serial0:115200n8";

    /* Initramfs location */
    linux,initrd-start = <0x82000000>;
    linux,initrd-end = <0x82800000>;
};
```

---

## Memory Node

```dts
memory@80000000 {
    device_type = "memory";
    reg = <0x80000000 0x40000000>;
    /* Base: 0x80000000, Size: 1GB */
};

/* Multiple memory banks */
memory@80000000 {
    reg = <0x80000000 0x40000000>,
          <0x100000000 0x40000000>;
};
```

---

## Reserved Memory

```dts
reserved-memory {
    #address-cells = <1>;
    #size-cells = <1>;
    ranges;

    /* Reserved for firmware */
    firmware@80000000 {
        reg = <0x80000000 0x100000>;
        no-map;
    };

    /* CMA pool */
    linux,cma {
        compatible = "shared-dma-pool";
        size = <0x4000000>;
        reusable;
    };
};
```

---

## Device Tree Compiler (DTC)

```bash
# Compile DTS to DTB
dtc -I dts -O dtb -o board.dtb board.dts

# Decompile DTB to DTS
dtc -I dtb -O dts -o board.dts board.dtb

# Check for errors
dtc -I dts -O null board.dts

# Include directories
dtc -i include/ -I dts -O dtb board.dts
```

---

## DTC Output Formats

```bash
# Different output formats
dtc -I dts -O dtb board.dts    # Binary blob
dtc -I dts -O dts board.dts    # Formatted DTS
dtc -I dts -O null board.dts   # Syntax check
dtc -I dts -O asm board.dts    # Assembly

# Read from filesystem
dtc -I fs -O dts /sys/firmware/devicetree/base
```

---

## Device Tree Validation

```bash
# Check with dt-validate
dt-validate board.dtb

# Check against schema
dt-doc-validate board.dts

# Kernel checker
scripts/dtc/dt_binding_check board.dts

# W=1 for warnings
make W=1 dtbs
```

---

## Common DT Errors

1. **Missing #address-cells/#size-cells**
1. **Wrong interrupt-cells count**
1. **Invalid reg format**
1. **Undefined phandle references**
1. **Duplicate node names**

```dts
/* ERROR: Missing #address-cells */
parent {
    child@100 {  /* Needs parent's #address-cells */
        reg = <0x100 0x10>;
    };
};
```

---

## Device Tree Bindings

```yaml
# Documentation/devicetree/bindings/serial/vendor,uart.yaml
properties:
  compatible:
    const: vendor,uart

  reg:
    maxItems: 1

  interrupts:
    maxItems: 1

  clocks:
    maxItems: 1

required:
  - compatible
  - reg
  - interrupts
```

---

## Device Tree Overlays

![device_tree_overlays](svg/courses/operating_systems/linux-kernel-advanced-topics/02_device_tree/device_tree_overlays.svg)

---

## Overlay Syntax

```dts
/dts-v1/;
/plugin/;

&i2c1 {
    #address-cells = <1>;
    #size-cells = <0>;

    sensor@48 {
        compatible = "ti,tmp102";
        reg = <0x48>;
    };
};

&gpio0 {
    led_pins: led {
        pins = "PA5";
        function = "gpio";
    };
};
```

---

## Applying Overlays

```bash
# Compile overlay
dtc -@ -I dts -O dtb -o overlay.dtbo overlay.dts

# Apply at runtime (configfs)
mkdir /sys/kernel/config/device-tree/overlays/my_overlay
cat overlay.dtbo > /sys/kernel/config/device-tree/overlays/my_overlay/dtbo

# U-Boot method
setenv overlays "overlay1.dtbo overlay2.dtbo"
load mmc 0:1 ${fdtoverlay_addr_r} ${overlays}
fdt apply ${fdtoverlay_addr_r}
```

---

## Runtime DT Modifications

```c
/* Kernel code to modify DT */
struct device_node *np;
struct property *prop;

np = of_find_node_by_path("/chosen");
prop = of_find_property(np, "bootargs", NULL);

/* Update property */
of_update_property(np, new_prop);

/* Add new property */
of_add_property(np, prop);
```

---

## Debugging Device Tree

```bash
# View compiled DT in kernel
ls /sys/firmware/devicetree/base/

# Check specific node
cat /sys/firmware/devicetree/base/compatible

# Find device by compatible
grep -r "vendor,device" /sys/firmware/devicetree/

# Kernel messages
dmesg | grep "device tree"
```

---

## OF (Open Firmware) Functions

```c
/* Find node by compatible */
np = of_find_compatible_node(NULL, NULL, "vendor,device");

/* Get property */
of_property_read_u32(np, "reg", &value);
of_property_read_string(np, "label", &str);

/* Parse phandle */
ph_np = of_parse_phandle(np, "clocks", 0);

/* Iterate children */
for_each_child_of_node(parent, child) {
    /* Process child */
}
```

---

## Platform Driver Binding

```c
static const struct of_device_id my_of_match[] = {
    { .compatible = "vendor,device-v1", .data = &v1_data },
    { .compatible = "vendor,device-v2", .data = &v2_data },
    { }
};
MODULE_DEVICE_TABLE(of, my_of_match);

static struct platform_driver my_driver = {
    .driver = {
        .name = "my-driver",
        .of_match_table = my_of_match,
    },
    .probe = my_probe,
    .remove = my_remove,
};
```

---

## DT Best Practices

1. **Use standard properties**: Follow existing bindings
1. **Document bindings**: Create YAML schemas
1. **Validate DTS**: Use dt-validate tools
1. **Keep it simple**: Don't over-engineer
1. **Version compatible strings**: Plan for updates
1. **Test thoroughly**: Verify on actual hardware

---

## Common Patterns

```dts
/* SoC peripherals */
soc {
    compatible = "simple-bus";
    #address-cells = <1>;
    #size-cells = <1>;
    ranges;

    uart0: serial@10000000 { ... };
    i2c0: i2c@10001000 { ... };
    spi0: spi@10002000 { ... };
};

/* Board-specific devices */
i2c0 {
    sensor@48 { ... };
    eeprom@50 { ... };
};
```

---

## Summary

1. Device Tree separates hardware description from code
1. Tree structure with nodes and properties
1. Compiled from DTS to DTB format
1. Standard properties for common hardware
1. Overlays enable runtime configuration
1. Critical for modern embedded Linux systems
