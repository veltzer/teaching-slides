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

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="500" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="300" y="85" text-anchor="middle" font-size="16" font-weight="bold">Configuration Files</text>
  <rect x="50" y="130" width="160" height="60" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="130" y="165" text-anchor="middle" font-size="14">Metadata</text>
  <rect x="220" y="130" width="160" height="60" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <text x="300" y="165" text-anchor="middle" font-size="14">BitBake</text>
  <rect x="390" y="130" width="160" height="60" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="470" y="165" text-anchor="middle" font-size="14">Recipes</text>
  <rect x="150" y="220" width="300" height="60" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-size="16" font-weight="bold">Build System</text>
  <rect x="150" y="310" width="300" height="60" fill="#e0f2f1" stroke="#00796b" stroke-width="2"/>
  <text x="300" y="345" text-anchor="middle" font-size="16" font-weight="bold">Output Images</text>
  <path d="M130 190 L300 220" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M300 190 L300 220" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M470 190 L300 220" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M300 280 L300 310" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#666"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="120" height="50" fill="#e3f2fd" stroke="#1976d2"/>
  <text x="110" y="80" text-anchor="middle" font-size="14">Parse</text>
  <rect x="200" y="50" width="120" height="50" fill="#f3e5f5" stroke="#7b1fa2"/>
  <text x="260" y="80" text-anchor="middle" font-size="14">Fetch</text>
  <rect x="350" y="50" width="120" height="50" fill="#e8f5e9" stroke="#388e3c"/>
  <text x="410" y="80" text-anchor="middle" font-size="14">Unpack</text>
  <rect x="50" y="130" width="120" height="50" fill="#fff3e0" stroke="#f57c00"/>
  <text x="110" y="160" text-anchor="middle" font-size="14">Patch</text>
  <rect x="200" y="130" width="120" height="50" fill="#fce4ec" stroke="#c2185b"/>
  <text x="260" y="160" text-anchor="middle" font-size="14">Configure</text>
  <rect x="350" y="130" width="120" height="50" fill="#e0f2f1" stroke="#00796b"/>
  <text x="410" y="160" text-anchor="middle" font-size="14">Compile</text>
  <rect x="125" y="210" width="120" height="50" fill="#f1f8e9" stroke="#689f38"/>
  <text x="185" y="240" text-anchor="middle" font-size="14">Install</text>
  <rect x="275" y="210" width="120" height="50" fill="#efebe9" stroke="#5d4037"/>
  <text x="335" y="240" text-anchor="middle" font-size="14">Package</text>
  <rect x="200" y="290" width="120" height="50" fill="#e8eaf6" stroke="#3f51b5"/>
  <text x="260" y="320" text-anchor="middle" font-size="14">Image</text>
  <path d="M170 75 L200 75" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M320 75 L350 75" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M110 100 L110 130" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M170 155 L200 155" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M320 155 L350 155" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M410 180 L335 210" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M110 180 L185 210" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M245 235 L275 235" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M335 260 L260 290" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M185 260 L260 290" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

```
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

```
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

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="125" y="85" text-anchor="middle" font-size="14" font-weight="bold">ext4</text>
  <rect x="225" y="50" width="150" height="60" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="300" y="85" text-anchor="middle" font-size="14" font-weight="bold">tar.gz</text>
  <rect x="400" y="50" width="150" height="60" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <text x="475" y="85" text-anchor="middle" font-size="14" font-weight="bold">wic</text>
  <rect x="50" y="140" width="150" height="60" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="125" y="175" text-anchor="middle" font-size="14" font-weight="bold">squashfs</text>
  <rect x="225" y="140" width="150" height="60" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="300" y="175" text-anchor="middle" font-size="14" font-weight="bold">ubifs</text>
  <rect x="400" y="140" width="150" height="60" fill="#e0f2f1" stroke="#00796b" stroke-width="2"/>
  <text x="475" y="175" text-anchor="middle" font-size="14" font-weight="bold">iso</text>
  <rect x="150" y="240" width="300" height="60" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="300" y="275" text-anchor="middle" font-size="16" font-weight="bold">IMAGE_FSTYPES</text>
</svg>

---

## WIC Image Creator

### wks File Example

```
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

<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="250" width="500" height="40" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <rect x="50" y="200" width="400" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <rect x="50" y="150" width="300" height="40" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
  <rect x="50" y="100" width="200" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="60" y="275" font-size="14">No Cache (4 hours)</text>
  <text x="60" y="225" font-size="14">DL_DIR (3 hours)</text>
  <text x="60" y="175" font-size="14">+ SSTATE (1 hour)</text>
  <text x="60" y="125" font-size="14">Incremental (15 min)</text>
  <text x="300" y="50" text-anchor="middle" font-size="16" font-weight="bold">Build Time Comparison</text>
</svg>

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