---
tags:
  - infrastructure:linux
  - infrastructure:embedded
  - tools:yocto
  - concepts:kernel
level: advanced
category: embedded
audience:
  - audiences:developers
  - audiences:sysadmins

---

# Kernel and Device Integration

---

## Kernel Architecture in Yocto

![kernel_architecture_in_yocto](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/06_kernel_and_device_integration/kernel_architecture_in_yocto.svg)

---

## Linux Kernel in Yocto

Virtual kernel provider:

```bash
# In machine configuration
PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
PREFERRED_VERSION_linux-yocto = "5.15%"

# Kernel image type
KERNEL_IMAGETYPE = "zImage"
KERNEL_IMAGETYPE_qemux86-64 = "bzImage"

# Kernel features
KERNEL_FEATURES_append = " features/netfilter/netfilter.scc"
```

Available kernel recipes:
- `linux-yocto` - Reference kernel
- `linux-yocto-rt` - Real-time kernel
- `linux-yocto-tiny` - Minimal kernel
- Custom kernel recipes

---

## Kernel Recipe Structure

Basic kernel recipe:

```bash
# recipes-kernel/linux/linux-custom_5.15.bb
require recipes-kernel/linux/linux-yocto.inc

LINUX_VERSION = "5.15.80"
LINUX_VERSION_EXTENSION = "-custom"

SRCREV_machine = "abc123def456..."
SRCREV_meta = "789ghi012jkl..."

SRC_URI = "git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;name=machine;branch=linux-5.15.y \
           git://git.yoctoproject.org/yocto-kernel-cache;type=kmeta;name=meta;branch=yocto-5.15;destsuffix=${KMETA}"

COMPATIBLE_MACHINE = "myboard"
```

---

## Kernel Configuration Methods

![kernel_configuration_methods](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/06_kernel_and_device_integration/kernel_configuration_methods.svg)

---

## Using defconfig

Default configuration approach:

```bash
# In kernel recipe
SRC_URI += "file://defconfig"

# defconfig location
recipes-kernel/linux/linux-custom/defconfig

# Machine-specific defconfig
SRC_URI_append_myboard = " file://defconfig"
recipes-kernel/linux/linux-custom/myboard/defconfig
```

Creating defconfig:

```bash
# Build kernel with menuconfig
bitbake -c menuconfig virtual/kernel

# Copy resulting config
cp tmp/work/myboard-poky-linux-gnueabi/linux-custom/5.15/build/.config \
   meta-custom/recipes-kernel/linux/linux-custom/defconfig
```

---

## Configuration Fragments

Modular configuration:

```bash
# In recipe
SRC_URI += "file://network.cfg \
            file://usb.cfg \
            file://security.cfg"

# network.cfg
CONFIG_NETFILTER=y
CONFIG_IP_NF_IPTABLES=y
CONFIG_IP_NF_NAT=y

# usb.cfg
CONFIG_USB=y
CONFIG_USB_STORAGE=y
CONFIG_USB_GADGET=y

# security.cfg
CONFIG_SECURITY=y
CONFIG_SECURITYFS=y
CONFIG_SECURITY_SELINUX=y
```

---

## Kernel Features (SCC)

Structured configuration:

```bash
# In recipe
KERNEL_FEATURES_append = " features/netfilter/netfilter.scc \
                           features/usb/usb-gadget.scc"

# Custom feature
SRC_URI += "file://myfeature.scc"

# myfeature.scc
define KFEATURE_DESCRIPTION "Custom feature"
define KFEATURE_COMPATIBILITY board

kconf hardware myfeature.cfg
patch myfeature-fix.patch
```

---

## Device Tree Overview

![device_tree_overview](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/06_kernel_and_device_integration/device_tree_overview.svg)

---

## Device Tree Basics

Device tree structure:

```dts
/dts-v1/;

/ {
    model = "MyBoard";
    compatible = "mycompany,myboard";

    cpus {
        cpu@0 {
            device_type = "cpu";
            compatible = "arm,cortex-a9";
            reg = <0>;
        };
    };

    memory@80000000 {
        device_type = "memory";
        reg = <0x80000000 0x40000000>; // 1GB RAM
    };

    chosen {
        bootargs = "console=ttyS0,115200";
        stdout-path = &serial0;
    };
};
```

---

## Device Tree Nodes

Peripheral definition:

```dts
serial0: serial@12000000 {
    compatible = "ns16550a";
    reg = <0x12000000 0x1000>;
    interrupts = <0 26 4>;
    clocks = <&uart_clk>;
    status = "okay";
};

i2c0: i2c@13000000 {
    compatible = "mycompany,i2c";
    reg = <0x13000000 0x1000>;
    interrupts = <0 27 4>;
    #address-cells = <1>;
    #size-cells = <0>;

    eeprom@50 {
        compatible = "atmel,24c64";
        reg = <0x50>;
    };
};
```

---

## Device Tree in Yocto

Specifying device trees:

```bash
# In machine configuration
KERNEL_DEVICETREE = "myboard.dtb myboard-variant.dtb"

# Multiple device trees
KERNEL_DEVICETREE = "myboard-base.dtb \
                     myboard-lcd.dtb \
                     myboard-camera.dtb"
```

Device tree location:

```bash
# In kernel sources
arch/arm/boot/dts/myboard.dts

# Custom DTS in recipe
recipes-kernel/linux/linux-custom/myboard.dts
SRC_URI += "file://myboard.dts"
```

---

## Device Tree Overlays

Base and overlay concept:

```dts
// Base: myboard.dts
/ {
    model = "MyBoard Base";
    compatible = "mycompany,myboard";

    spi0: spi@14000000 {
        status = "disabled";
    };
};

// Overlay: myboard-spi.dtso
/dts-v1/;
/plugin/;

&spi0 {
    status = "okay";

    sensor@0 {
        compatible = "bosch,bme280";
        reg = <0>;
        spi-max-frequency = <1000000>;
    };
};
```

---

## Kernel Module Development

Out-of-tree module recipe:

```bash
# recipes-kernel/mymodule/mymodule_1.0.bb
SUMMARY = "Custom kernel module"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=..."

inherit module

SRC_URI = "file://Makefile \
           file://mymodule.c"

S = "${WORKDIR}"

# Module parameters
RPROVIDES_${PN} += "kernel-module-mymodule"
```

---

## Kernel Module Makefile

```makefile
# Makefile for out-of-tree module
obj-m := mymodule.o

SRC := $(shell pwd)

all:
    $(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules

modules_install:
    $(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install

clean:
    $(MAKE) -C $(KERNEL_SRC) M=$(SRC) clean
```

Module source:

```c
#include <linux/module.h>
#include <linux/kernel.h>

static int __init mymodule_init(void) {
    printk(KERN_INFO "MyModule: Loaded\n");
    return 0;
}

static void __exit mymodule_exit(void) {
    printk(KERN_INFO "MyModule: Unloaded\n");
}

module_init(mymodule_init);
module_exit(mymodule_exit);
MODULE_LICENSE("GPL");
```

---

## BSP Layer Structure

```tree
meta-myboard/
├── conf/
│   ├── layer.conf
│   └── machine/
│       └── myboard.conf
├── recipes-bsp/
│   ├── u-boot/
│   │   ├── u-boot_%.bbappend
│   │   └── files/
│   │       └── myboard-config.h
│   └── formfactor/
│       └── formfactor_0.0.bb
├── recipes-kernel/
│   └── linux/
│       ├── linux-yocto_%.bbappend
│       └── files/
│           ├── defconfig
│           └── myboard.dts
└── recipes-graphics/
    └── xorg-xserver/
        └── xserver-xf86-config_%.bbappend
```

---

## Machine Configuration

```bash
# conf/machine/myboard.conf
require conf/machine/include/arm/armv7a/tune-cortexa9.inc

# Hardware features
MACHINE_FEATURES = "ext2 ext3 serial usbhost usbgadget alsa screen"

# Serial console
SERIAL_CONSOLES = "115200;ttyS0"

# Kernel
PREFERRED_PROVIDER_virtual/kernel = "linux-custom"
KERNEL_IMAGETYPE = "zImage"
KERNEL_DEVICETREE = "myboard.dtb"

# Bootloader
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-custom"
UBOOT_MACHINE = "myboard_defconfig"

# Extra packages
MACHINE_ESSENTIAL_EXTRA_RDEPENDS = "kernel-modules"
MACHINE_EXTRA_RDEPENDS = "firmware-myboard"
```

---

## Bootloader Integration

U-Boot recipe:

```bash
# recipes-bsp/u-boot/u-boot-custom_2023.01.bb
require recipes-bsp/u-boot/u-boot.inc

DEPENDS += "dtc-native"

SRC_URI = "git://source.denx.de/u-boot/u-boot.git;protocol=https;branch=master"
SRCREV = "abc123..."

SRC_URI += "file://0001-add-board-support.patch \
            file://myboard_defconfig"

COMPATIBLE_MACHINE = "myboard"
```

U-Boot configuration:

```bash
# files/myboard_defconfig
CONFIG_ARM=y
CONFIG_ARCH_MYBOARD=y
CONFIG_SYS_MALLOC_F_LEN=0x2000
CONFIG_ENV_SIZE=0x2000
CONFIG_DEFAULT_DEVICE_TREE="myboard"
CONFIG_BOOTCOMMAND="run bootcmd_mmc0"
```

---

## Boot Process Flow

![boot_process_flow](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/06_kernel_and_device_integration/boot_process_flow.svg)

---

## Firmware Integration

Firmware recipe:

```bash
# recipes-bsp/firmware/firmware-myboard_1.0.bb
SUMMARY = "Firmware for MyBoard peripherals"
LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://LICENSE;md5=..."

SRC_URI = "https://vendor.com/firmware-${PV}.tar.gz"

S = "${WORKDIR}/firmware-${PV}"

do_install() {
    install -d ${D}${base_libdir}/firmware
    install -m 0644 wifi.bin ${D}${base_libdir}/firmware/
    install -m 0644 bluetooth.bin ${D}${base_libdir}/firmware/
}

FILES_${PN} = "${base_libdir}/firmware/*"

PACKAGE_ARCH = "${MACHINE_ARCH}"
```

---

## Graphics Driver Integration

GPU driver recipe:

```bash
# recipes-graphics/gpu-driver/gpu-driver_1.0.bb
SUMMARY = "GPU driver for MyBoard"
LICENSE = "Proprietary"

DEPENDS = "virtual/kernel"

inherit module

SRC_URI = "git://github.com/vendor/gpu-driver.git;protocol=https"

EXTRA_OEMAKE_append = " KCPPFLAGS=-I${STAGING_KERNEL_DIR}/include"

do_install_append() {
    install -d ${D}${includedir}
    install -m 0644 ${S}/include/*.h ${D}${includedir}

    install -d ${D}${libdir}
    install -m 0755 ${B}/libgpu.so.${PV} ${D}${libdir}
}

PACKAGES =+ "${PN}-libs"
FILES_${PN}-libs = "${libdir}/libgpu.so.*"
```

---

## Audio Support

ALSA configuration:

```bash
# In machine config
MACHINE_FEATURES += "alsa"

# ALSA state file
recipes-bsp/alsa-state/alsa-state.bbappend
SRC_URI_append_myboard = " file://asound.state"

# asound.state
state.MyBoardAudio {
    control.1 {
        name 'Master Playback Volume'
        value 80
    }
}
```

PulseAudio integration:

```bash
# In image recipe
IMAGE_INSTALL_append = " pulseaudio pulseaudio-server"

# Configuration
recipes-multimedia/pulseaudio/pulseaudio_%.bbappend
SRC_URI_append = " file://default.pa"
```

---

## Network Device Support

Ethernet driver:

```bash
# In kernel defconfig
CONFIG_NETDEVICES=y
CONFIG_ETHERNET=y
CONFIG_MYBOARD_ETH=y

# Device tree
ethernet@15000000 {
    compatible = "mycompany,ethernet-v1";
    reg = <0x15000000 0x1000>;
    interrupts = <0 30 4>;
    phy-mode = "rgmii";
    status = "okay";
};
```

WiFi support:

```bash
# Machine features
MACHINE_FEATURES += "wifi"

# Required packages
MACHINE_EXTRA_RDEPENDS += "linux-firmware-wifi \
                           wireless-tools \
                           wpa-supplicant"
```

---

## USB Support

USB host configuration:

```bash
# Kernel config fragment
CONFIG_USB=y
CONFIG_USB_EHCI_HCD=y
CONFIG_USB_STORAGE=y
CONFIG_USB_SERIAL=y

# Device tree
usb@16000000 {
    compatible = "generic-ehci";
    reg = <0x16000000 0x1000>;
    interrupts = <0 31 4>;
    status = "okay";
};
```

USB gadget mode:

```bash
CONFIG_USB_GADGET=y
CONFIG_USB_CONFIGFS=y
CONFIG_USB_CONFIGFS_SERIAL=y
CONFIG_USB_CONFIGFS_MASS_STORAGE=y

MACHINE_FEATURES += "usbgadget"
```

---

## Storage Interfaces

MMC/SD support:

```bash
# Kernel configuration
CONFIG_MMC=y
CONFIG_MMC_SDHCI=y
CONFIG_MMC_SDHCI_PLTFM=y

# Device tree
mmc0: mmc@17000000 {
    compatible = "mycompany,sdhci";
    reg = <0x17000000 0x1000>;
    interrupts = <0 32 4>;
    bus-width = <4>;
    max-frequency = <50000000>;
    status = "okay";
};

# WIC configuration for SD card
part /boot --source bootimg-partition --fstype=vfat --label boot --active --align 4 --size 64
part / --source rootfs --fstype=ext4 --label root --align 4
```

---

## NAND Flash Support

```bash
# Kernel configuration
CONFIG_MTD=y
CONFIG_MTD_NAND=y
CONFIG_MTD_UBI=y
CONFIG_UBIFS_FS=y

# Device tree
nand@18000000 {
    compatible = "mycompany,nand";
    reg = <0x18000000 0x1000>;
    #address-cells = <1>;
    #size-cells = <1>;

    partition@0 {
        label = "u-boot";
        reg = <0x0 0x100000>;
    };

    partition@100000 {
        label = "kernel";
        reg = <0x100000 0x800000>;
    };

    partition@900000 {
        label = "rootfs";
        reg = <0x900000 0x7700000>;
    };
};
```

---

## Display Support

Framebuffer configuration:

```bash
# Kernel config
CONFIG_FB=y
CONFIG_FB_MYBOARD=y
CONFIG_LOGO=y

# Device tree
display@19000000 {
    compatible = "mycompany,display";
    reg = <0x19000000 0x1000>;
    interrupts = <0 33 4>;

    display-timings {
        native-mode = <&timing0>;
        timing0: 1024x600 {
            clock-frequency = <45000000>;
            hactive = <1024>;
            vactive = <600>;
            hfront-porch = <20>;
            hback-porch = <140>;
            hsync-len = <20>;
            vfront-porch = <7>;
            vback-porch = <20>;
            vsync-len = <3>;
        };
    };
};
```

---

## Touch Screen Integration

```bash
# Kernel configuration
CONFIG_INPUT_TOUCHSCREEN=y
CONFIG_TOUCHSCREEN_GOODIX=y

# Device tree
&i2c0 {
    touchscreen@5d {
        compatible = "goodix,gt911";
        reg = <0x5d>;
        interrupt-parent = <&gpio1>;
        interrupts = <9 IRQ_TYPE_EDGE_FALLING>;
        irq-gpios = <&gpio1 9 GPIO_ACTIVE_HIGH>;
        reset-gpios = <&gpio1 10 GPIO_ACTIVE_HIGH>;
        touchscreen-size-x = <1024>;
        touchscreen-size-y = <600>;
    };
};

# Required packages
IMAGE_INSTALL_append = " tslib tslib-calibrate tslib-tests"
```

---

## GPIO and Pin Multiplexing

GPIO controller:

```dts
gpio1: gpio@1a000000 {
    compatible = "mycompany,gpio";
    reg = <0x1a000000 0x1000>;
    interrupts = <0 34 4>;
    gpio-controller;
    #gpio-cells = <2>;
    interrupt-controller;
    #interrupt-cells = <2>;
};

// Using GPIOs
leds {
    compatible = "gpio-leds";

    led0 {
        label = "status";
        gpios = <&gpio1 5 GPIO_ACTIVE_HIGH>;
        linux,default-trigger = "heartbeat";
    };
};
```

---

## Pin Control

```dts
pinctrl: pinctrl@1b000000 {
    compatible = "mycompany,pinctrl";
    reg = <0x1b000000 0x1000>;

    uart0_pins: uart0 {
        mux {
            function = "uart0";
            groups = "uart0_grp";
        };

        conf {
            pins = "uart0_tx", "uart0_rx";
            bias-pull-up;
        };
    };

    spi0_pins: spi0 {
        mux {
            function = "spi0";
            groups = "spi0_grp";
        };
    };
};

&uart0 {
    pinctrl-names = "default";
    pinctrl-0 = <&uart0_pins>;
};
```

---

## Power Management

CPU frequency scaling:

```bash
# Kernel configuration
CONFIG_CPU_FREQ=y
CONFIG_CPU_FREQ_GOV_PERFORMANCE=y
CONFIG_CPU_FREQ_GOV_POWERSAVE=y
CONFIG_CPU_FREQ_GOV_ONDEMAND=y

# Device tree
cpus {
    cpu@0 {
        operating-points = <
            /* kHz    uV */
            1000000 1350000
            800000  1200000
            600000  1100000
            400000  1000000
        >;
        clock-latency = <300000>;
    };
};
```

---

## Suspend/Resume Support

```bash
# Kernel configuration
CONFIG_SUSPEND=y
CONFIG_PM_SLEEP=y
CONFIG_PM_RUNTIME=y

# Power management driver
recipes-kernel/pm-driver/pm-driver_1.0.bb
```

Suspend trigger:

```bash
# Using systemd
IMAGE_INSTALL_append = " systemd-extra-utils"

# Suspend on idle
systemctl suspend

# Wake on GPIO
&gpio1 {
    wakeup-source;
};
```

---

## Real-Time Support

RT kernel:

```bash
# Use RT kernel
PREFERRED_PROVIDER_virtual/kernel = "linux-yocto-rt"

# RT features
DISTRO_FEATURES_append = " real-time"

# RT configuration
CONFIG_PREEMPT_RT=y
CONFIG_HIGH_RES_TIMERS=y
CONFIG_NO_HZ_FULL=y
```

RT testing:

```bash
IMAGE_INSTALL_append = " rt-tests stress-ng"

# Run cyclictest
cyclictest -p 99 -t -n -i 1000 -l 100000
```

---

## Custom Hardware Interfaces

SPI device:

```dts
&spi0 {
    status = "okay";

    adc@0 {
        compatible = "ti,ads1015";
        reg = <0>;
        spi-max-frequency = <1000000>;
        #address-cells = <1>;
        #size-cells = <0>;

        channel@0 {
            reg = <0>;
            ti,gain = <1>;
            ti,datarate = <4>;
        };
    };
};
```

---

## I2C Devices

```dts
&i2c1 {
    status = "okay";
    clock-frequency = <400000>;

    rtc@68 {
        compatible = "dallas,ds1307";
        reg = <0x68>;
    };

    sensor@76 {
        compatible = "bosch,bme280";
        reg = <0x76>;
    };

    eeprom@50 {
        compatible = "atmel,24c256";
        reg = <0x50>;
        pagesize = <64>;
    };
};
```

---

## Watchdog Timer

```bash
# Kernel configuration
CONFIG_WATCHDOG=y
CONFIG_WATCHDOG_CORE=y
CONFIG_MYBOARD_WATCHDOG=y

# Device tree
watchdog@1c000000 {
    compatible = "mycompany,watchdog";
    reg = <0x1c000000 0x1000>;
    timeout-sec = <30>;
};

# Userspace daemon
IMAGE_INSTALL_append = " watchdog"
```

---

## CAN Bus Support

```bash
# Kernel configuration
CONFIG_CAN=y
CONFIG_CAN_DEV=y
CONFIG_CAN_CALC_BITTIMING=y
CONFIG_CAN_FLEXCAN=y

# Device tree
can0: can@1d000000 {
    compatible = "fsl,flexcan";
    reg = <0x1d000000 0x1000>;
    interrupts = <0 35 4>;
    clocks = <&can_clk>;
    clock-frequency = <24000000>;
};

# CAN utilities
IMAGE_INSTALL_append = " can-utils"
```

---

## Summary

Key integration topics:
- Kernel recipe customization
- Configuration management
- Device tree fundamentals
- BSP layer organization
- Bootloader integration
- Hardware peripheral support

Best practices:
- Use defconfig + fragments
- Maintain clean device trees
- Organize BSP layers properly
- Document hardware dependencies
- Test on target hardware
- Version control configurations
