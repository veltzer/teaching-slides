# Bootloader

---

## Bootloader Overview

The bootloader is the first software that runs when a system powers on

Key responsibilities:
1. Initialize basic hardware
1. Load the kernel into memory
1. Pass control to the kernel
1. Provide debugging capabilities

---

## Boot Stages

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect x="50" y="50" width="150" height="80" fill="#FFE6E6" stroke="black"/>
<text x="125" y="95" text-anchor="middle">ROM Boot</text>
<rect x="250" y="50" width="150" height="80" fill="#E6F2FF" stroke="black"/>
<text x="325" y="95" text-anchor="middle">SPL/MLO</text>
<rect x="450" y="50" width="150" height="80" fill="#E6FFE6" stroke="black"/>
<text x="525" y="95" text-anchor="middle">U-Boot</text>
<rect x="650" y="50" width="100" height="80" fill="#FFFFE6" stroke="black"/>
<text x="700" y="95" text-anchor="middle">Kernel</text>
<line x1="200" y1="90" x2="250" y2="90" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="400" y1="90" x2="450" y2="90" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="600" y1="90" x2="650" y2="90" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<text x="125" y="170">Hardware Init</text>
<text x="325" y="170">DRAM Init</text>
<text x="525" y="170">Full Bootloader</text>
<text x="700" y="170">OS Boot</text>
<defs>
<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="black"/>
</marker>
</defs>
</svg>

---

## Bootloader Responsibilities

1. Hardware initialization
    - CPU configuration
    - Memory controller setup
    - Clock initialization
1. Device enumeration
1. Loading kernel and initramfs
1. Setting up kernel parameters
1. Jumping to kernel entry point

---

## U-Boot Architecture

Universal Bootloader - most common bootloader for embedded Linux

Key features:
- Support for multiple architectures
- Extensive device drivers
- Network boot support
- Scripting capabilities
- Environment variables

---

## U-Boot Components

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="50" width="600" height="400" fill="#F0F0F0" stroke="black"/>
<text x="400" y="80" text-anchor="middle" font-weight="bold">U-Boot Architecture</text>
<rect x="150" y="120" width="200" height="60" fill="#FFE6E6" stroke="black"/>
<text x="250" y="155" text-anchor="middle">Board Support</text>
<rect x="450" y="120" width="200" height="60" fill="#E6F2FF" stroke="black"/>
<text x="550" y="155" text-anchor="middle">Device Drivers</text>
<rect x="150" y="220" width="200" height="60" fill="#E6FFE6" stroke="black"/>
<text x="250" y="255" text-anchor="middle">Commands</text>
<rect x="450" y="220" width="200" height="60" fill="#FFFFE6" stroke="black"/>
<text x="550" y="255" text-anchor="middle">Filesystems</text>
<rect x="300" y="320" width="200" height="60" fill="#FFE6FF" stroke="black"/>
<text x="400" y="355" text-anchor="middle">Core Services</text>
</svg>

---

## U-Boot Configuration

Configuration through Kconfig system:

```bash
make menuconfig
make <board>_defconfig
```

Key configuration files:
- `configs/<board>_defconfig`
- `include/configs/<board>.h`
- `board/<vendor>/<board>/`

---

## U-Boot Source Structure

```tree
u-boot/
├── arch/           # Architecture-specific code
├── board/          # Board-specific code
├── common/         # Common commands
├── configs/        # Board configurations
├── drivers/        # Device drivers
├── include/        # Header files
└── tools/          # Build tools
```

---

## Building U-Boot

```bash
# Configure for specific board
make CROSS_COMPILE=arm-linux-gnueabihf- \
     <board>_defconfig

# Build U-Boot
make CROSS_COMPILE=arm-linux-gnueabihf- -j8

# Output files
ls -la u-boot*
```

---

## SPL (Secondary Program Loader)

Small first-stage bootloader:
- Fits in limited SRAM
- Initializes DRAM
- Loads full U-Boot

```c
void board_init_f(ulong dummy)
{
    preloader_console_init();
    spl_dram_init();
    spl_mmc_load_image();
}
```

---

## U-Boot Environment Variables

Store configuration and boot parameters:

```bash
# Display all variables
printenv

# Set variable
setenv bootdelay 3

# Save to persistent storage
saveenv
```

---

## Common Environment Variables

- `bootcmd` - Default boot command
- `bootargs` - Kernel command line
- `bootdelay` - Delay before autoboot
- `ipaddr` - Board IP address
- `serverip` - TFTP server IP
- `loadaddr` - Memory load address

---

## U-Boot Commands

Essential commands:

```bash
# Memory operations
md 0x80000000          # Display memory
mm 0x80000000          # Modify memory
cp.b src dst len       # Copy memory

# Boot commands
bootm address          # Boot kernel
bootz address          # Boot zImage
```

---

## Loading Kernel

Multiple methods available:

```bash
# From MMC/SD
load mmc 0:1 0x82000000 zImage
load mmc 0:1 0x88000000 devicetree.dtb

# From network
tftp 0x82000000 zImage
tftp 0x88000000 devicetree.dtb

# From USB
usb start
load usb 0:1 0x82000000 zImage
```

---

## Boot Scripts

Automate boot process with scripts:

```bash
# Create boot script
setenv bootscript 'load mmc 0:1 0x82000000 zImage; \
                   load mmc 0:1 0x88000000 am335x.dtb; \
                   bootz 0x82000000 - 0x88000000'

# Execute script
run bootscript
```

---

## Device Tree in U-Boot

U-Boot uses Device Tree for:
- Hardware configuration
- Pin multiplexing
- Driver binding

```bash
# Load and boot with DTB
load mmc 0:1 ${fdt_addr} ${fdtfile}
fdt addr ${fdt_addr}
fdt resize
bootz ${loadaddr} - ${fdt_addr}
```

---

## FDT Commands

Manipulate Device Tree at runtime:

```bash
# Display DTB
fdt print /

# Modify property
fdt set /chosen bootargs "console=ttyS0,115200"

# Add node
fdt mknode / mynode
```

---

## Secure Boot

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="50" width="150" height="80" fill="#FFE6E6" stroke="black"/>
<text x="175" y="95" text-anchor="middle">ROM</text>
<rect x="300" y="50" width="150" height="80" fill="#E6F2FF" stroke="black"/>
<text x="375" y="95" text-anchor="middle">SPL (signed)</text>
<rect x="500" y="50" width="150" height="80" fill="#E6FFE6" stroke="black"/>
<text x="575" y="95" text-anchor="middle">U-Boot (signed)</text>
<text x="175" y="170">Verify SPL</text>
<text x="375" y="170">Verify U-Boot</text>
<text x="575" y="170">Verify Kernel</text>
<line x1="250" y1="90" x2="300" y2="90" stroke="green" stroke-width="3" marker-end="url(#greenarrow)"/>
<line x1="450" y1="90" x2="500" y2="90" stroke="green" stroke-width="3" marker-end="url(#greenarrow)"/>
<defs>
<marker id="greenarrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="green"/>
</marker>
</defs>
</svg>

---

## Implementing Secure Boot

Key components:
1. Hardware root of trust
1. Signed bootloader images
1. Certificate chain
1. Verification at each stage

```bash
# Sign U-Boot image
mkimage -A arm -T firmware -C none \
        -a 0x80008000 -e 0x80008000 \
        -n "U-Boot" -d u-boot.bin \
        -k keys -r u-boot-signed.img
```

---

## Verified Boot

FIT (Flattened Image Tree) images:

```dts
/dts-v1/;
/ {
    images {
        kernel {
            data = /incbin/("zImage");
            hash-1 {
                algo = "sha256";
            };
        };
    };
    configurations {
        default = "config-1";
        config-1 {
            kernel = "kernel";
            signature {
                algo = "sha256,rsa2048";
                key-name-hint = "dev";
            };
        };
    };
};
```

---

## Bootloader to Kernel Handoff

Information passed to kernel:
1. Machine type (ARM)
1. Memory information
1. Command line parameters
1. Device Tree blob
1. Initramfs location

---

## ATAGS vs Device Tree

Legacy ATAGS:
- Architecture-specific
- Limited information
- Deprecated

Modern Device Tree:
- Architecture-independent
- Comprehensive hardware description
- Standard format

---

## Kernel Boot Parameters

Common parameters:

```bash
setenv bootargs 'console=ttyS0,115200 \
                 root=/dev/mmcblk0p2 rw \
                 rootwait \
                 init=/sbin/init'
```

---

## Alternative Bootloaders

## Barebox

- Formerly U-Boot v2
- POSIX-like API
- Better driver model
- Smaller footprint

---

## Coreboot

- X86-focused
- Minimal initialization
- Payload architecture
- Fast boot times

---

## GRUB for Embedded

- UEFI support
- Complex boot scenarios
- Scripting capabilities
- Multi-OS support

---

## U-Boot Debugging

Debug techniques:

```bash
# Enable debug output
#define DEBUG

# Serial console output
printf("Debug: var=%d\n", var);

# Memory dumps
md.b 0x80000000 100

# Breakpoints with JTAG
```

---

## Common Boot Issues

1. No serial output
    - Wrong baudrate
    - Pin configuration
1. Hang during DRAM init
    - Timing parameters
    - Power sequencing
1. Kernel panic
    - Wrong machine ID
    - Missing DTB

---

## Boot Time Analysis

Measure boot stages:

```bash
# U-Boot timing
CONFIG_BOOTSTAGE=y
CONFIG_BOOTSTAGE_REPORT=y

# Show timing report
bootstage report
```

---

## Optimizing U-Boot

Reduce boot time:
1. Remove unnecessary features
1. Optimize environment size
1. Use faster storage
1. Falcon mode (skip U-Boot)

```bash
CONFIG_SPL_OS_BOOT=y  # Direct kernel boot
```

---

## Falcon Mode

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
<text x="400" y="30" text-anchor="middle" font-weight="bold">Normal vs Falcon Mode</text>
<text x="200" y="70">Normal:</text>
<rect x="50" y="80" width="80" height="50" fill="#FFE6E6" stroke="black"/>
<text x="90" y="110" text-anchor="middle">SPL</text>
<rect x="150" y="80" width="80" height="50" fill="#E6F2FF" stroke="black"/>
<text x="190" y="110" text-anchor="middle">U-Boot</text>
<rect x="250" y="80" width="80" height="50" fill="#E6FFE6" stroke="black"/>
<text x="290" y="110" text-anchor="middle">Kernel</text>
<text x="200" y="180">Falcon:</text>
<rect x="50" y="190" width="80" height="50" fill="#FFE6E6" stroke="black"/>
<text x="90" y="220" text-anchor="middle">SPL</text>
<rect x="150" y="190" width="80" height="50" fill="#E6FFE6" stroke="black"/>
<text x="190" y="220" text-anchor="middle">Kernel</text>
<line x1="130" y1="105" x2="150" y2="105" stroke="black" marker-end="url(#arrow)"/>
<line x1="230" y1="105" x2="250" y2="105" stroke="black" marker-end="url(#arrow)"/>
<line x1="130" y1="215" x2="150" y2="215" stroke="black" marker-end="url(#arrow)"/>
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6"/>
</marker>
</defs>
</svg>

---

## Network Boot

PXE/TFTP boot setup:

```bash
# DHCP configuration
setenv autoload no
dhcp

# TFTP boot
setenv serverip 192.168.1.100
tftp ${loadaddr} zImage
tftp ${fdt_addr} board.dtb
bootz ${loadaddr} - ${fdt_addr}
```

---

## USB Boot

Boot from USB devices:

```bash
# Initialize USB
usb start
usb tree

# Load from USB
usb dev 0
load usb 0:1 ${loadaddr} zImage
load usb 0:1 ${fdt_addr} board.dtb
```

---

## eMMC Boot Partitions

Special boot partitions:

```bash
# Switch to boot partition
mmc dev 0 1

# Write bootloader
mmc write ${loadaddr} 0 ${filesize}

# Enable boot partition
mmc bootpart enable 1 1 /dev/mmcblk0
```

---

## U-Boot Driver Model

Modern driver framework:

```c
static const struct udevice_id my_ids[] = {
    { .compatible = "vendor,device" },
    { }
};

U_BOOT_DRIVER(my_driver) = {
    .name = "my_driver",
    .id = UCLASS_SERIAL,
    .of_match = my_ids,
    .probe = my_probe,
    .ops = &my_ops,
};
```

---

## Board Initialization

Board-specific setup:

```c
int board_early_init_f(void)
{
    /* Configure pins */
    setup_iomux_uart();
    return 0;
}

int board_init(void)
{
    /* Setup peripherals */
    setup_i2c();
    setup_spi();
    return 0;
}
```

---

## Custom Commands

Add application-specific commands:

```c
static int do_mycommand(cmd_tbl_t *cmdtp,
                        int flag, int argc,
                        char * const argv[])
{
    printf("My custom command\n");
    return 0;
}

U_BOOT_CMD(
    mycommand, 1, 0, do_mycommand,
    "My custom command",
    "Usage: mycommand"
);
```

---

## Best Practices

1. Version control board configurations
1. Document boot parameters
1. Test recovery mechanisms
1. Implement watchdog support
1. Enable secure boot in production
1. Minimize boot time
1. Regular security updates

---

## Summary

Bootloader is critical for:
- Hardware initialization
- Loading operating system
- System recovery
- Security foundation

Key skills:
- U-Boot configuration
- Boot optimization
- Secure boot implementation
- Debugging boot issues
