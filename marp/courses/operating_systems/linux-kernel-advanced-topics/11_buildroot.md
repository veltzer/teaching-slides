---
tags:
  - infrastructure:linux
  - infrastructure:embedded
  - tools:buildroot
level: advanced
category: operating-systems
audience:
  - audiences:developers

---

# Buildroot

---

## Overview

Buildroot is:
- Simple build system
- Generates embedded Linux systems
- Uses familiar technologies
- Cross-compilation toolchain

Key features:
- `Kconfig` configuration
- `Makefile` based
- Minimal learning curve

---

## Buildroot Philosophy

### Design Principles

1. Simplicity over features
1. Small footprint
1. Fast builds
1. Easy to understand
1. No runtime package management

Best for:
- Simple embedded systems
- Quick prototypes
- Learning embedded Linux
- Resource-constrained devices

---

## Buildroot Architecture

![buildroot_architecture](svg/courses/operating_systems/linux-kernel-advanced-topics/11_buildroot/buildroot_architecture.svg)

---

## Getting Started

### Download and Setup

```bash
# Download Buildroot
wget https://buildroot.org/downloads/buildroot-2023.02.tar.gz
tar xzf buildroot-2023.02.tar.gz
cd buildroot-2023.02

# Configure for target
make qemu_x86_64_defconfig

# Customize configuration
make menuconfig

# Build
make
```

---

## Directory Structure

```tree
buildroot/
├── board/           # Board-specific files
├── configs/         # Defconfig files
├── dl/             # Downloaded packages
├── output/         # Build output
│   ├── build/      # Build directory
│   ├── host/       # Host tools
│   ├── images/     # Final images
│   └── target/     # Target filesystem
├── package/        # Package definitions
└── support/        # Support scripts
```

---

## Configuration System

### Menuconfig Interface

Main menu structure:
- Target options
- Build options
- Toolchain
- System configuration
- Kernel
- Target packages
- Filesystem images
- Bootloaders
- Host utilities

---

## Target Options

### Architecture Configuration

```bash
# Target Architecture
BR2_arm=y

# Target Architecture Variant
BR2_cortex_a9=y

# Floating point strategy
BR2_ARM_FPU_VFPV3D16=y

# Target ABI
BR2_ARM_EABIHF=y
```

---

## Build Options

### Build Configuration

```bash
# Download directory
BR2_DL_DIR="$(HOME)/buildroot-dl"

# Compiler cache
BR2_CCACHE=y
BR2_CCACHE_DIR="$(HOME)/.buildroot-ccache"

# Number of jobs
BR2_JLEVEL=8

# Enable compiler optimizations
BR2_OPTIMIZE_2=y
```

---

## Toolchain Options

![toolchain_options](svg/courses/operating_systems/linux-kernel-advanced-topics/11_buildroot/toolchain_options.svg)

---

## Internal Toolchain

### Toolchain Configuration

```bash
# C library
BR2_TOOLCHAIN_BUILDROOT_UCLIBC=y
# or BR2_TOOLCHAIN_BUILDROOT_GLIBC=y
# or BR2_TOOLCHAIN_BUILDROOT_MUSL=y

# GCC version
BR2_GCC_VERSION_11_X=y

# Kernel headers
BR2_KERNEL_HEADERS_5_15=y

# Additional options
BR2_TOOLCHAIN_BUILDROOT_CXX=y
BR2_TOOLCHAIN_BUILDROOT_FORTRAN=y
```

---

## External Toolchain

### Using Pre-built Toolchain

```bash
# External toolchain
BR2_TOOLCHAIN_EXTERNAL=y

# Custom toolchain
BR2_TOOLCHAIN_EXTERNAL_CUSTOM=y

# Toolchain path
BR2_TOOLCHAIN_EXTERNAL_PATH="/opt/arm-toolchain"

# Toolchain prefix
BR2_TOOLCHAIN_EXTERNAL_PREFIX="arm-linux-gnueabihf"
```

---

## System Configuration

### System Settings

```bash
# System hostname
BR2_TARGET_GENERIC_HOSTNAME="embedded"

# System banner
BR2_TARGET_GENERIC_ISSUE="Welcome to Buildroot"

# Root password
BR2_TARGET_GENERIC_ROOT_PASSWD="root"

# Init system
BR2_INIT_SYSTEMD=y
# or BR2_INIT_SYSV=y
# or BR2_INIT_BUSYBOX=y
```

---

## Package Infrastructure
### Package Types

---

## Package Types

![package_types](svg/courses/operating_systems/linux-kernel-advanced-topics/11_buildroot/package_types.svg)

---

## Creating Custom Package

### Package Directory

```tree
package/myapp/
├── Config.in
├── myapp.mk
└── myapp.hash
```

---

## Package Config.in

```bash
config BR2_PACKAGE_MYAPP
    bool "myapp"
    depends on BR2_USE_MMU
    select BR2_PACKAGE_LIBCURL
    help
      My application description.

      This is a demo application that
      shows Buildroot package creation.

      https://github.com/example/myapp
```

---

## Package Makefile

### myapp.mk

```makefile
################################
# myapp
################################

MYAPP_VERSION = 1.0
MYAPP_SITE = $(call github,example,myapp,v$(MYAPP_VERSION))
MYAPP_LICENSE = GPL-2.0+
MYAPP_LICENSE_FILES = COPYING
MYAPP_DEPENDENCIES = libcurl

define MYAPP_BUILD_CMDS
    $(MAKE) CC="$(TARGET_CC)" LD="$(TARGET_LD)" -C $(@D) all
endef

define MYAPP_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/myapp $(TARGET_DIR)/usr/bin
endef

$(eval $(generic-package))
```

---

## Package Hash File

### myapp.hash

```bash
# md5, sha1, sha256, sha512 from upstream
sha256  1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef  myapp-1.0.tar.gz

# Locally computed
sha256  abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890  COPYING
```

---

## Autotools Package

```makefile
HELLO_VERSION = 2.10
HELLO_SOURCE = hello-$(HELLO_VERSION).tar.gz
HELLO_SITE = https://ftp.gnu.org/gnu/hello
HELLO_LICENSE = GPL-3.0+
HELLO_LICENSE_FILES = COPYING

HELLO_CONF_OPTS = --disable-nls

$(eval $(autotools-package))
```

---

## CMake Package

```makefile
MYLIB_VERSION = 2.0
MYLIB_SITE = $(call github,example,mylib,v$(MYLIB_VERSION))
MYLIB_INSTALL_STAGING = YES
MYLIB_LICENSE = MIT
MYLIB_LICENSE_FILES = LICENSE

MYLIB_CONF_OPTS = \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_TESTS=OFF

$(eval $(cmake-package))
```

---

## Python Package

```makefile
PYTHON_MYMOD_VERSION = 1.2.3
PYTHON_MYMOD_SOURCE = mymod-$(PYTHON_MYMOD_VERSION).tar.gz
PYTHON_MYMOD_SITE = https://files.pythonhosted.org/packages/source/m/mymod
PYTHON_MYMOD_SETUP_TYPE = setuptools
PYTHON_MYMOD_LICENSE = BSD-3-Clause
PYTHON_MYMOD_LICENSE_FILES = LICENSE

$(eval $(python-package))
```

---

## Root Filesystem Customization

### Overlay Directory

```bash
# In menuconfig
BR2_ROOTFS_OVERLAY="board/myboard/rootfs-overlay"

# Directory structure
board/myboard/rootfs-overlay/
├── etc/
│   ├── init.d/
│   │   └── S99myservice
│   └── myapp.conf
└── usr/
    └── bin/
        └── custom-script
```

---

## Post-Build Scripts

### Custom Scripts

```bash
# Configuration
BR2_ROOTFS_POST_BUILD_SCRIPT="board/myboard/post-build.sh"
BR2_ROOTFS_POST_IMAGE_SCRIPT="board/myboard/post-image.sh"

# post-build.sh
#!/bin/sh
set -e

# Modify target filesystem
echo "Custom build" > ${TARGET_DIR}/etc/build-info

# Set permissions
chmod 755 ${TARGET_DIR}/usr/bin/myapp
```

---

## Users and Permissions

### users.txt

```bash
# username uid group gid password home shell groups comment
admin 1000 admin 1000 =admin /home/admin /bin/sh wheel Admin User
daemon -1 daemon -1 ! - - - Daemon User
```

Configuration:
```bash
BR2_ROOTFS_USERS_TABLES="board/myboard/users.txt"
```

---

## Device Table

### device_table.txt

```bash
# name type mode uid gid major minor
/dev/mmcblk0 b 660 0 6 179 0
/dev/ttyS0 c 666 0 5 4 64
/dev/random c 666 0 0 1 8
/tmp d 1777 0 0 - -
```

Configuration:
```bash
BR2_ROOTFS_DEVICE_TABLE="board/myboard/device_table.txt"
```

---

## Kernel Configuration

### Linux Kernel

```bash
# Use Linux kernel
BR2_LINUX_KERNEL=y

# Kernel version
BR2_LINUX_KERNEL_CUSTOM_VERSION=y
BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE="5.15.100"

# Kernel configuration
BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG=y
BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE="board/myboard/linux.config"

# Device Tree
BR2_LINUX_KERNEL_DTS_SUPPORT=y
BR2_LINUX_KERNEL_INTREE_DTS_NAME="myboard"
```

---

## Bootloader Configuration

### U-Boot

```bash
# Use U-Boot
BR2_TARGET_UBOOT=y

# U-Boot version
BR2_TARGET_UBOOT_CUSTOM_VERSION=y
BR2_TARGET_UBOOT_CUSTOM_VERSION_VALUE="2023.01"

# U-Boot board
BR2_TARGET_UBOOT_BOARD_DEFCONFIG="myboard"

# U-Boot binary format
BR2_TARGET_UBOOT_FORMAT_IMG=y
BR2_TARGET_UBOOT_SPL=y
```

---

## Filesystem Images

![filesystem_images](svg/courses/operating_systems/linux-kernel-advanced-topics/11_buildroot/filesystem_images.svg)

---

## Genimage Configuration

### genimage.cfg

```cfg
image sdcard.img {
    hdimage {
    }

    partition boot {
        partition-type = 0xC
        bootable = "true"
        image = "boot.vfat"
    }

    partition rootfs {
        partition-type = 0x83
        image = "rootfs.ext4"
    }
}

image boot.vfat {
    vfat {
        files = {
            "zImage",
            "myboard.dtb"
        }
    }
    size = 64M
}
```

---

## Defconfig Management

### Creating Defconfig

```bash
# Configure system
make menuconfig

# Save as defconfig
make savedefconfig

# Copy to configs/
cp defconfig configs/myboard_defconfig

# Use defconfig
make myboard_defconfig
```

---

## External Tree

### BR2_EXTERNAL

```bash
# Structure
mycompany/
├── Config.in
├── external.mk
├── external.desc
├── configs/
│   └── myboard_defconfig
├── package/
│   └── myapp/
└── board/
    └── myboard/

# Use external tree
make BR2_EXTERNAL=/path/to/mycompany menuconfig
```

---

## external.desc

```misc
name: MYCOMPANY
desc: My Company Buildroot customization
```

### Config.in

```bash
source "$BR2_EXTERNAL_MYCOMPANY_PATH/package/myapp/Config.in"
```

### external.mk

```makefile
include $(sort $(wildcard $(BR2_EXTERNAL_MYCOMPANY_PATH)/package/*/*.mk))
```

---

## Build Performance

### Optimization Tips

1. **Use ccache**
   ```bash
   BR2_CCACHE=y
   ```

1. **Parallel jobs**
   ```bash
   BR2_JLEVEL=8
   ```

1. **External toolchain**
   - Faster than building

1. **Shared download directory**
   - Between builds

---

## Debugging

### Build Issues

```bash
# Verbose build
make V=1

# Rebuild package
make myapp-rebuild

# Clean package
make myapp-clean

# Reconfigure package
make myapp-reconfigure

# Show package info
make myapp-show-depends
make myapp-show-version
```

---

## Graph Generation

### Dependency Graphs

```bash
# Full dependency graph
make graph-depends

# Package dependency
make myapp-graph-depends

# Build time graph
make graph-build

# Size graph
make graph-size
```

---

## Legal Information

### License Compliance

```bash
# Generate legal info
make legal-info

# Output location
output/legal-info/
├── host-licenses/
├── licenses/
├── manifest.csv
└── host-manifest.csv
```

---

## Testing Support

### Run-time Tests

```python
# support/testing/tests/package/test_myapp.py
import os
from tests.package.test_python import TestPythonPackageBase

class TestMyApp(TestPythonPackageBase):
    config = TestPythonPackageBase.config + \
        """
        BR2_PACKAGE_MYAPP=y
        """

    def test_run(self):
        self.login()
        self.run_cmd("myapp --version")
```

---

## Continuous Integration

### GitLab CI Example

```yaml
.buildroot_job:
  image: buildroot/base:latest
  before_script:
    - make myboard_defconfig

build:
  extends: .buildroot_job
  script:
    - make
  artifacts:
    paths:
      - output/images/
```

---

## Size Optimization

![size_optimization](svg/courses/operating_systems/linux-kernel-advanced-topics/11_buildroot/size_optimization.svg)

---

## Security Hardening

### Security Options

```bash
# Stack protection
BR2_SSP_STRONG=y

# FORTIFY_SOURCE
BR2_FORTIFY_SOURCE_2=y

# Position Independent Executables
BR2_PIE=y

# RELRO
BR2_RELRO_FULL=y
```

---

## Comparison with Yocto

| Aspect | Buildroot | Yocto |
|--------|-----------|-------|
| Learning | Days | Weeks |
| Build Time | Fast | Slow |
| Flexibility | Limited | High |
| Packages | 2500+ | 10000+ |
| Binary Packages | No | Yes |
| Layers | No | Yes |
| SDK | Basic | Advanced |

---

## When to Use Buildroot

### Good Fit

1. Simple embedded systems
1. Fixed-function devices
1. Quick prototypes
1. Learning embedded Linux
1. Small teams

### Not Ideal For

1. Complex products
1. Multiple variants
1. Package management needs
1. Compliance requirements
1. Large teams

---

## Migration Path

### From Buildroot to Yocto

When you need:
- More packages
- Runtime package management
- Multiple machine support
- Commercial support
- Compliance tools

Keep Buildroot for:
- Prototyping
- Simple products
- Resource constraints

---

## Best Practices

1. **Version Control**
   - Track configs
   - Use BR2_EXTERNAL
   - Tag releases

1. **Testing**
   - Automated builds
   - Runtime tests
   - Hardware testing

1. **Documentation**
   - Document customizations
   - Board setup guides
   - Build instructions

---

## Resources

### Documentation

- [Buildroot Manual](https://buildroot.org/docs.html)
- [Training Materials](https://bootlin.com/training/)
- Mailing list archives

### Community

- IRC: #buildroot
- Mailing list
- Annual Developers Meeting

---

## Summary

Buildroot provides:
- Simple build system
- Fast development cycle
- Minimal footprint
- Easy customization

Perfect for:
- Embedded devices
- Learning Linux
- Rapid prototyping
- Production systems with fixed requirements
