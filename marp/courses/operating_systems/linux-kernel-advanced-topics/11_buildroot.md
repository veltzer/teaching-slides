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

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="50" width="300" height="50" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="300" y="80" text-anchor="middle" font-size="16" font-weight="bold">Kconfig (menuconfig)</text>
  <rect x="50" y="130" width="140" height="50" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="120" y="160" text-anchor="middle" font-size="14">Toolchain</text>
  <rect x="210" y="130" width="140" height="50" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <text x="280" y="160" text-anchor="middle" font-size="14">Packages</text>
  <rect x="370" y="130" width="140" height="50" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="440" y="160" text-anchor="middle" font-size="14">Filesystem</text>
  <rect x="150" y="210" width="300" height="50" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="300" y="240" text-anchor="middle" font-size="16" font-weight="bold">Make</text>
  <rect x="150" y="290" width="300" height="50" fill="#e0f2f1" stroke="#00796b" stroke-width="2"/>
  <text x="300" y="320" text-anchor="middle" font-size="16" font-weight="bold">Output Images</text>
  <path d="M300 100 L120 130" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M300 100 L280 130" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M300 100 L440 130" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M120 180 L280 210" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M280 180 L300 210" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M440 180 L320 210" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M300 260 L300 290" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#666"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="50" width="300" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="300" y="85" text-anchor="middle" font-size="16" font-weight="bold">Toolchain Type</text>
  <rect x="50" y="150" width="200" height="60" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="150" y="185" text-anchor="middle" font-size="14">Internal Toolchain</text>
  <rect x="300" y="150" width="200" height="60" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <text x="400" y="185" text-anchor="middle" font-size="14">External Toolchain</text>
  <text x="150" y="250" text-anchor="middle" font-size="12">Built by Buildroot</text>
  <text x="150" y="270" text-anchor="middle" font-size="12">GCC, binutils, libc</text>
  <text x="150" y="290" text-anchor="middle" font-size="12">Slower first build</text>
  <text x="400" y="250" text-anchor="middle" font-size="12">Pre-built toolchain</text>
  <text x="400" y="270" text-anchor="middle" font-size="12">Linaro, ARM, etc.</text>
  <text x="400" y="290" text-anchor="middle" font-size="12">Faster builds</text>
</svg>

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

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="120" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="110" y="85" text-anchor="middle" font-size="14">Generic</text>
  <rect x="190" y="50" width="120" height="60" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="250" y="85" text-anchor="middle" font-size="14">Autotools</text>
  <rect x="330" y="50" width="120" height="60" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <text x="390" y="85" text-anchor="middle" font-size="14">CMake</text>
  <rect x="470" y="50" width="120" height="60" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="530" y="85" text-anchor="middle" font-size="14">Python</text>
  <rect x="50" y="130" width="120" height="60" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="110" y="165" text-anchor="middle" font-size="14">Perl</text>
  <rect x="190" y="130" width="120" height="60" fill="#e0f2f1" stroke="#00796b" stroke-width="2"/>
  <text x="250" y="165" text-anchor="middle" font-size="14">Meson</text>
  <rect x="330" y="130" width="120" height="60" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="390" y="165" text-anchor="middle" font-size="14">QMake</text>
  <rect x="470" y="130" width="120" height="60" fill="#efebe9" stroke="#5d4037" stroke-width="2"/>
  <text x="530" y="165" text-anchor="middle" font-size="14">Golang</text>
  <rect x="150" y="230" width="300" height="60" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="300" y="265" text-anchor="middle" font-size="16" font-weight="bold">Package Infrastructure</text>
</svg>

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

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="50" fill="#e3f2fd" stroke="#1976d2"/>
  <text x="125" y="80" text-anchor="middle" font-size="14">tar</text>
  <rect x="225" y="50" width="150" height="50" fill="#f3e5f5" stroke="#7b1fa2"/>
  <text x="300" y="80" text-anchor="middle" font-size="14">ext2/3/4</text>
  <rect x="400" y="50" width="150" height="50" fill="#e8f5e9" stroke="#388e3c"/>
  <text x="475" y="80" text-anchor="middle" font-size="14">squashfs</text>
  <rect x="50" y="120" width="150" height="50" fill="#fff3e0" stroke="#f57c00"/>
  <text x="125" y="150" text-anchor="middle" font-size="14">ubifs</text>
  <rect x="225" y="120" width="150" height="50" fill="#fce4ec" stroke="#c2185b"/>
  <text x="300" y="150" text-anchor="middle" font-size="14">jffs2</text>
  <rect x="400" y="120" width="150" height="50" fill="#e0f2f1" stroke="#00796b"/>
  <text x="475" y="150" text-anchor="middle" font-size="14">cpio</text>
  <rect x="150" y="210" width="300" height="60" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="300" y="245" text-anchor="middle" font-size="16" font-weight="bold">genimage.cfg</text>
</svg>

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

```text
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

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="500" height="40" fill="#f5f5f5" stroke="#333"/>
  <rect x="50" y="50" width="400" height="40" fill="#ffcdd2" stroke="#d32f2f"/>
  <rect x="50" y="100" width="500" height="40" fill="#f5f5f5" stroke="#333"/>
  <rect x="50" y="100" width="300" height="40" fill="#c8e6c9" stroke="#4caf50"/>
  <rect x="50" y="150" width="500" height="40" fill="#f5f5f5" stroke="#333"/>
  <rect x="50" y="150" width="250" height="40" fill="#bbdefb" stroke="#1976d2"/>
  <rect x="50" y="200" width="500" height="40" fill="#f5f5f5" stroke="#333"/>
  <rect x="50" y="200" width="200" height="40" fill="#fff9c4" stroke="#fbc02d"/>
  <text x="60" y="75" font-size="12">Full glibc (150MB)</text>
  <text x="60" y="125" font-size="12">uClibc (80MB)</text>
  <text x="60" y="175" font-size="12">musl (60MB)</text>
  <text x="60" y="225" font-size="12">Static busybox (40MB)</text>
  <text x="300" y="280" text-anchor="middle" font-size="16" font-weight="bold">Filesystem Size Comparison</text>
</svg>

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
