---
tags:
  - infrastructure:linux
  - infrastructure:embedded
  - tools:yocto
level: advanced
category: operating-systems
audience:
  - audiences:developers

---
# Yocto Project

---

## Overview

The Yocto Project is:
- Open source collaboration project
- Provides templates and tools
- Creates custom Linux distributions
- Hardware agnostic

Key components:
- `BitBake` build engine
- `OpenEmbedded-Core` metadata
- `Poky` reference distribution

---

## Why Yocto?

### Benefits

1. Reproducible builds
1. Cross-platform support
1. Package management
1. License compliance
1. Long-term support

### Use Cases

- Embedded Linux systems
- IoT devices
- Automotive platforms
- Industrial applications

---

## Yocto Architecture

![yocto_architecture](svg/courses/operating_systems/linux-kernel-advanced-topics/10_yocto_project/yocto_architecture.svg)

---

## Core Components

### OpenEmbedded-Core

- Base layer
- Essential metadata
- Core recipes
- Common tasks

### Poky

- Reference distribution
- Build environment
- Testing platform
- Documentation

---

## BitBake Build System

### What is BitBake?

- Task scheduler
- Python-based
- Parallel execution
- Dependency resolution

```bash
# Basic BitBake command
bitbake <target>

# Example
bitbake core-image-minimal
```

---

## BitBake Workflow

![bitbake_workflow](svg/courses/operating_systems/linux-kernel-advanced-topics/10_yocto_project/bitbake_workflow.svg)

---

## Project Setup

### Getting Started

```bash
# Clone Poky
git clone git://git.yoctoproject.org/poky
cd poky

# Checkout release
git checkout -b kirkstone \
    origin/kirkstone

# Initialize environment
source oe-init-build-env
```

---

## Build Directory Structure

```tree
build/
├── conf/
│   ├── local.conf
│   ├── bblayers.conf
│   └── templateconf.cfg
├── tmp/
│   ├── work/
│   ├── deploy/
│   └── sysroots/
└── downloads/
```

---

## Configuration Files

### local.conf

```bash
# Machine selection
MACHINE = "qemux86-64"

# Distribution
DISTRO = "poky"

# Package format
PACKAGE_CLASSES = "package_rpm"

# Parallel execution
BB_NUMBER_THREADS = "8"
PARALLEL_MAKE = "-j 8"
```

---

## Layer Configuration

### bblayers.conf

```bash
BBLAYERS ?= " \
  /path/to/poky/meta \
  /path/to/poky/meta-poky \
  /path/to/poky/meta-yocto-bsp \
  /path/to/meta-custom \
  "
```

---

## Recipe Writing Basics

### Recipe Structure

```bash
SUMMARY = "Example application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=..."

SRC_URI = "git://github.com/example/app.git"
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/git"

inherit cmake

do_install() {
    install -d ${D}${bindir}
    install -m 0755 app ${D}${bindir}
}
```

---

## Recipe Components

### Variables

| Variable | Description |
|----------|-------------|
| `PN` | Package name |
| `PV` | Package version |
| `PR` | Package revision |
| `S` | Source directory |
| `D` | Destination directory |
| `WORKDIR` | Working directory |

---

## Tasks in Recipes

### Standard Tasks

```bash
do_fetch()      # Download source
do_unpack()     # Extract source
do_patch()      # Apply patches
do_configure()  # Configure build
do_compile()    # Build software
do_install()    # Install files
do_package()    # Create packages
```

---

## Dependencies

### Build Dependencies

```bash
# Build-time dependencies
DEPENDS = "libxml2 openssl"

# Runtime dependencies
RDEPENDS_${PN} = "python3-core"

# Recommendations
RRECOMMENDS_${PN} = "bash"
```

---

## Layer Management

### Creating a Layer

```bash
# Create layer
bitbake-layers create-layer meta-custom

# Add layer to build
bitbake-layers add-layer ../meta-custom

# Show layers
bitbake-layers show-layers
```

---

## Layer Structure

```tree
meta-custom/
├── conf/
│   └── layer.conf
├── recipes-apps/
│   └── myapp/
│       └── myapp_1.0.bb
├── recipes-kernel/
│   └── linux/
│       └── linux-yocto_%.bbappend
└── classes/
    └── custom.bbclass
```

---

## Layer Priority

### layer.conf

```bash
# Layer configuration
BBPATH .= ":${LAYERDIR}"

BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
            ${LAYERDIR}/recipes-*/*/*.bbappend"

# Layer priority (higher = override)
BBFILE_PRIORITY_custom = "6"

# Layer dependencies
LAYERDEPENDS_custom = "core"
LAYERSERIES_COMPAT_custom = "kirkstone"
```

---

## Image Customization

### Custom Image Recipe

```bash
require recipes-core/images/core-image-base.bb

IMAGE_FEATURES += "ssh-server-openssh"

IMAGE_INSTALL += " \
    packagegroup-core-boot \
    myapp \
    python3 \
    nginx \
    "

IMAGE_ROOTFS_SIZE = "8192"
IMAGE_ROOTFS_EXTRA_SPACE = "0"
```

---

## Package Groups

### packagegroup-custom.bb

```bash
SUMMARY = "Custom package group"

inherit packagegroup

RDEPENDS_${PN} = " \
    package1 \
    package2 \
    package3 \
    "
```

---

## Image Types

![image_types](svg/courses/operating_systems/linux-kernel-advanced-topics/10_yocto_project/image_types.svg)

---

## WIC Image Creator

### wks File Example

```bash
# partition table
part /boot --source bootimg-partition \
           --fstype=vfat --label boot --active --size 64

part / --source rootfs --fstype=ext4 --label root \
       --align 4096 --size 2G

part /data --fstype=ext4 --label data --size 1G

bootloader --timeout=0 --append="rootwait console=ttyS0"
```

---

## SDK Generation

### Building SDK

```bash
# Standard SDK
bitbake core-image-minimal -c populate_sdk

# Extended SDK
bitbake core-image-minimal -c populate_sdk_ext
```

### Installing SDK

```bash
# Install SDK
./poky-glibc-x86_64-core-image-minimal-*.sh

# Source environment
source /opt/poky/environment-setup-*
```

---

## DevTool Workflow

### Development Tool

```bash
# Add recipe to workspace
devtool add myapp https://github.com/example/myapp

# Modify source
devtool modify myapp

# Build changes
devtool build myapp

# Deploy to target
devtool deploy-target myapp root@192.168.1.100

# Create patches
devtool update-recipe myapp
```

---

## Package Management

### Runtime Package Management

```bash
# Enable package management
EXTRA_IMAGE_FEATURES += "package-management"

# Package feed
PACKAGE_FEED_URIS = "http://192.168.1.1:8080"

# On target
opkg update
opkg install package_name
```

---

## License Compliance

### License Tracking

```bash
# Enable license manifest
COPY_LIC_MANIFEST = "1"
COPY_LIC_DIRS = "1"

# Exclude licenses
INCOMPATIBLE_LICENSE = "GPL-3.0 LGPL-3.0"

# License report
bitbake -c create_license_report core-image-minimal
```

---

## Build Optimization

### Shared State Cache

```bash
# local.conf
SSTATE_DIR ?= "${TOPDIR}/sstate-cache"

# Share between builds
SSTATE_MIRRORS = "file://.* \
    http://server/sstate-cache/PATH"
```

---

## Download Directory

```bash
# Shared downloads
DL_DIR = "/shared/downloads"

# Premirrors
PREMIRRORS_prepend = "\
    git://.*/.* file:///local/mirror/ \n \
    https://.*/.* file:///local/mirror/ \n"
```

---

## Build Performance

![build_performance](svg/courses/operating_systems/linux-kernel-advanced-topics/10_yocto_project/build_performance.svg)

---

## Debugging Builds

### BitBake Debug Options

```bash
# Verbose output
bitbake -v recipe_name

# Debug output
bitbake -DDD recipe_name

# Environment dump
bitbake -e recipe_name > env.txt

# Dependency graph
bitbake -g recipe_name
```

---

## Common Issues

### Troubleshooting

1. **Fetch failures**
   ```bash
   bitbake recipe -c cleanall
   bitbake recipe -c fetch
   ```

1. **Signature changes**
   ```bash
   bitbake-diffsigs task-sig1.* task-sig2.*
   ```

1. **Missing dependencies**
   ```bash
   bitbake -k recipe_name
   ```

---

## Security Features

### Security Hardening

```bash
# Enable security flags
require conf/distro/include/security_flags.inc

# Additional features
DISTRO_FEATURES_append = " pam selinux"

# Security scanning
inherit cve-check
```

---

## Multiconfig Builds

### Multiple Configurations

```bash
# local.conf
BBMULTICONFIG = "arm x86"

# multiconfig/arm.conf
MACHINE = "qemuarm"

# multiconfig/x86.conf
MACHINE = "qemux86"

# Build both
bitbake multiconfig:arm:core-image-minimal \
        multiconfig:x86:core-image-minimal
```

---

## Container Support

### Docker Integration

```bash
# Container image
IMAGE_FSTYPES = "container"
IMAGE_TYPEDEP_container = "tar.gz"

# Minimal container
IMAGE_FEATURES = ""
IMAGE_LINGUAS = ""
```

---

## Production Deployment

### Release Management

1. **Version control**
    - Layer repos
    - Configuration management
    - Build reproducibility
1. **Automated builds**
    - CI/CD integration
    - Nightly builds
    - Testing
1. **Artifact management**
    - Image storage
    - Package feeds
    - SDK distribution

---

## Yocto vs Alternatives

| Feature | Yocto | Buildroot | OpenWrt |
|---------|-------|-----------|---------|
| Complexity | High | Low | Medium |
| Flexibility | High | Medium | Low |
| Package Count | 10000+ | 2500+ | 5000+ |
| Learning Curve | Steep | Gentle | Medium |
| Enterprise | Yes | Limited | No |

---

## Best Practices

1. **Layer Organization**
    - Separate BSP and application layers
    - Version control each layer
    - Document dependencies

1. **Recipe Management**
    - Use version numbers
    - Include license information
    - Test recipes independently

1. **Build Optimization**
    - Use shared state cache
    - Implement CI/CD
    - Monitor build times

---

## Resources

### Documentation

- [Yocto Project Documentation](https://docs.yoctoproject.org)
- [BitBake User Manual](https://docs.yoctoproject.org/bitbake)
- [OpenEmbedded Wiki](http://www.openembedded.org/wiki)

### Community

- Mailing lists
- IRC: #yocto
- Stack Overflow

---

## Summary

Yocto Project provides:
- Complete build framework
- Reproducible builds
- Extensive customization
- Professional support

Ideal for:
- Complex embedded systems
- Long-term products
- Compliance requirements
- Multi-platform support
