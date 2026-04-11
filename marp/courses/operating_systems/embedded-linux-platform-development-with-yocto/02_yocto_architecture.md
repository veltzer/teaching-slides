---
tags:
  - infrastructure:linux
  - infrastructure:embedded
  - tools:yocto
level: advanced
category: embedded
audience:
  - audiences:developers
  - audiences:sysadmins

---
# Yocto Architecture Deep Dive

---

## Architecture Overview

![architecture_overview](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/architecture_overview.svg)

---

## Core Components Relationship

BitBake + Metadata = Build System

Key relationships:
- BitBake reads metadata
- Metadata defines what to build
- Configuration controls how to build
- Layers organize metadata

All work together to:
- Parse recipes
- Execute tasks
- Generate packages
- Create images

---

## Poky Distribution

Reference distribution components:
- BitBake build tool
- OpenEmbedded-Core (OE-Core)
- Yocto-specific metadata
- Documentation and tools

Not a fork, but integration:
- Combines upstream projects
- Adds polish and testing
- Provides stable releases
- Reference implementation

---

## OpenEmbedded-Core

Foundation metadata:

```tree
meta/
├── classes/         # Base classes
├── conf/           # Core configuration
├── files/          # Common files
├── lib/            # Python libraries
├── recipes-bsp/    # Bootloaders
├── recipes-core/   # Essential packages
├── recipes-devtools/ # Development tools
├── recipes-extended/ # Extra packages
├── recipes-graphics/ # Graphics stack
├── recipes-kernel/   # Linux kernel
├── recipes-multimedia/ # Media libraries
├── recipes-rt/       # Real-time
├── recipes-sato/     # Sato UI
└── recipes-support/  # Support libraries
```

---

## Recipe Categories

BSP (Board Support Package):
- Bootloaders (U-Boot, GRUB)
- Kernel configuration
- Device trees
- Firmware files

Core:
- Init systems
- Base utilities
- Package managers
- Shell environments

---

## More Recipe Categories

Development:
- Compilers and toolchains
- Debuggers
- Build tools
- Version control

Extended:
- System daemons
- Network tools
- File utilities
- Administrative tools

---

## Metadata Types

![metadata_types](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/metadata_types.svg)

---

## Recipe Structure

```bash
DESCRIPTION = "Example application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=..."

SRC_URI = "git://github.com/example/app.git;protocol=https"
SRCREV = "abc123..."

S = "${WORKDIR}/git"

inherit cmake

DEPENDS = "libxml2 openssl"
RDEPENDS_${PN} = "python3"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/app ${D}${bindir}
}

FILES_${PN} = "${bindir}/app"
```

---

## Class Inheritance

![class_inheritance](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/class_inheritance.svg)

---

## Common Classes

Build system classes:
- `autotools` - GNU autoconf/automake
- `cmake` - CMake build system
- `meson` - Meson build system
- `qmake5` - Qt5 qmake

Packaging classes:
- `kernel` - Linux kernel recipes
- `module` - Kernel modules
- `image` - Image recipes
- `packagegroup` - Package collections

---

## Utility Classes

Development:
- `devshell` - Development shell
- `testimage` - Runtime testing
- `populate_sdk` - SDK generation
- `cross` - Cross-compilation tools

Features:
- `systemd` - systemd integration
- `update-rc.d` - SysV init
- `useradd` - User management
- `update-alternatives` - Alternative providers

---

## Configuration Files

Machine configuration:
```bash
# conf/machine/my-board.conf
require conf/machine/include/tune-cortexa9.inc

SERIAL_CONSOLES = "115200;ttyS0"
KERNEL_IMAGETYPE = "zImage"
KERNEL_DEVICETREE = "my-board.dtb"

MACHINE_FEATURES = "ext2 serial usbhost"
MACHINE_ESSENTIAL_EXTRA_RDEPENDS = "kernel-modules"

PREFERRED_PROVIDER_virtual/kernel = "linux-custom"
PREFERRED_VERSION_linux-custom = "5.15%"
```

---

## Distribution Configuration

```bash
# conf/distro/my-distro.conf
DISTRO = "my-distro"
DISTRO_NAME = "My Custom Distribution"
DISTRO_VERSION = "1.0"

DISTRO_FEATURES = "systemd pam usrmerge"
DISTRO_FEATURES_remove = "x11"

INIT_MANAGER = "systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"

PREFERRED_VERSION_python3 = "3.10%"
PACKAGE_CLASSES = "package_rpm"
```

---

## Layer Structure

```tree
meta-custom/
├── COPYING.MIT
├── README
├── conf/
│   └── layer.conf
├── classes/
│   └── custom.bbclass
├── recipes-apps/
│   └── myapp/
│       ├── myapp_1.0.bb
│       └── files/
│           └── myapp.service
├── recipes-kernel/
│   └── linux/
│       ├── linux-custom_5.15.bb
│       └── files/
│           └── defconfig
└── recipes-core/
    └── images/
        └── custom-image.bb
```

---

## Layer Configuration

```bash
# conf/layer.conf
BBPATH .= ":${LAYERDIR}"

BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
            ${LAYERDIR}/recipes-*/*/*.bbappend"

BBFILE_COLLECTIONS += "custom"
BBFILE_PATTERN_custom = "^${LAYERDIR}/"
BBFILE_PRIORITY_custom = "7"

LAYERDEPENDS_custom = "core openembedded-layer"
LAYERSERIES_COMPAT_custom = "kirkstone"
```

---

## Build Flow Phases

![build_flow_phases](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/build_flow_phases.svg)

---

## Parsing Phase Details

What happens during parsing:
1. Read configuration files
1. Locate all layers
1. Parse recipe files
1. Resolve dependencies
1. Expand variables
1. Generate task graph

Output:
- Task dependency tree
- Variable database
- Recipe cache

---

## Task Execution Model

![task_execution_model](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/task_execution_model.svg)

---

## Standard Tasks

Fetch tasks:
- `do_fetch` - Download sources
- `do_unpack` - Extract archives
- `do_patch` - Apply patches

Build tasks:
- `do_configure` - Configure build
- `do_compile` - Compile sources
- `do_install` - Install to staging

Package tasks:
- `do_package` - Split into packages
- `do_package_qa` - Quality checks
- `do_package_write_*` - Create packages

---

## Task Dependencies

Types of dependencies:
- Task dependencies within recipe
- Inter-recipe dependencies
- Runtime dependencies
- Build-time dependencies

Dependency declaration:

```bash
# Task dependency
do_compile[depends] = "virtual/kernel:do_populate_sysroot"

# Recipe dependency
DEPENDS = "zlib openssl"

# Runtime dependency
RDEPENDS_${PN} = "python3-core"
```

---

## Shared State Cache

![shared_state_cache](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/shared_state_cache.svg)

---

## Sstate Benefits

Performance improvements:
- Skip redundant compilation
- Share across builds
- Network cache sharing
- Incremental builds

Hash-based validation:
- Input hash (recipe, dependencies)
- Output hash (generated files)
- Automatic invalidation
- Reproducible builds

---

## Variable Expansion

Immediate expansion (`=`):

```bash
VAR = "value"
OTHER = "${VAR}"  # Expanded when parsed
```

Deferred expansion (`:=`):

```bash
VAR := "value"
OTHER := "${VAR}"  # Expanded when used
```

Conditional assignment (`?=`):

```bash
VAR ?= "default"  # Only if not set
```

---

## Override Mechanism

Machine overrides:

```bash
KERNEL_IMAGETYPE = "zImage"
KERNEL_IMAGETYPE_qemuarm = "zImage"
KERNEL_IMAGETYPE_qemux86-64 = "bzImage"
```

Conditional overrides:

```bash
PACKAGECONFIG ??= "openssl"
PACKAGECONFIG[openssl] = "--with-ssl,--without-ssl,openssl"
```

Append operations:

```bash
SRC_URI_append = " file://extra.patch"
DEPENDS_append_class-target = " virtual/libc"
```

---

## PACKAGECONFIG System

Feature configuration:

```bash
PACKAGECONFIG ??= "feature1 feature2"

# Format: "configure_opts_if_enabled,configure_opts_if_disabled,build_deps,runtime_deps"
PACKAGECONFIG[feature1] = "--enable-feature1,--disable-feature1,dep1,rdep1"
PACKAGECONFIG[feature2] = "--with-feature2,,dep2,rdep2"
```

Usage in recipes:

```bash
EXTRA_OECONF = "${PACKAGECONFIG_CONFARGS}"
```

---

## Virtual Providers

Abstract dependencies:

```bash
# Consumer recipe
DEPENDS = "virtual/kernel"

# Provider recipe
PROVIDES = "virtual/kernel"

# Machine configuration
PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
```

Common virtuals:
- `virtual/kernel` - Linux kernel
- `virtual/libc` - C library
- `virtual/bootloader` - Bootloader
- `virtual/xserver` - X server

---

## Recipe Versioning

Version selection:

```bash
# Prefer specific version
PREFERRED_VERSION_python3 = "3.10.%"

# Multiple versions available
recipes-devtools/python/
├── python3_3.9.14.bb
├── python3_3.10.8.bb
└── python3_3.11.0.bb
```

Version operators:
- `%` - Wildcard match
- `>=` - Minimum version
- `<=` - Maximum version

---

## Package Splitting

Automatic splitting:

```bash
PACKAGES = "${PN}-dbg ${PN}-staticdev ${PN}-dev ${PN}-doc ${PN} ${PN}-locale"

FILES_${PN} = "${bindir}/* ${sbindir}/*"
FILES_${PN}-dev = "${includedir} ${libdir}/*.so"
FILES_${PN}-doc = "${mandir} ${docdir}"
```

Custom packages:

```bash
PACKAGES =+ "${PN}-tools"
FILES_${PN}-tools = "${bindir}/tool1 ${bindir}/tool2"
RDEPENDS_${PN}-tools = "${PN}"
```

---

## Image Generation Process

![image_generation_process](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/image_generation_process.svg)

---

## Rootfs Assembly

Steps:
1. Install packages from feed
1. Run post-install scripts
1. Apply IMAGE_FEATURES
1. Execute ROOTFS_POSTPROCESS_COMMAND
1. Generate manifest
1. Create image files

Configuration:

```bash
IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_FEATURES = "ssh-server-openssh package-management"
IMAGE_LINGUAS = "en-us"
```

---

## Image Types

Common formats:
- `ext4` - Ext4 filesystem
- `tar.gz` - Compressed tarball
- `wic` - Partitioned disk image
- `squashfs` - Read-only compressed
- `ubifs` - NAND flash filesystem
- `cpio` - Initramfs archive

Configuration:

```bash
IMAGE_FSTYPES = "ext4 tar.gz wic"
WKS_FILE = "sdimage-bootpart.wks"
```

---

## WIC Image Creator

Partition definition (.wks):

```bash
# Boot partition
part /boot --source bootimg-partition --fstype=vfat --label boot --active --size 64

# Root partition
part / --source rootfs --fstype=ext4 --label root --size 2G

# Data partition
part /data --fstype=ext4 --label data --size 1G

# Bootloader
bootloader --ptable msdos
```

---

## Package Feeds

Repository structure:

```tree
tmp/deploy/rpm/
├── all/           # Architecture-independent
├── cortexa9hf/    # Machine-specific
├── my_machine/    # Board-specific
└── repodata/      # Repository metadata
```

Feed configuration:

```bash
PACKAGE_FEED_URIS = "http://myserver/feeds"
PACKAGE_FEED_BASE_PATHS = "rpm"
```

---

## Multiconfig Builds

Building multiple configurations:

```bash
# conf/multiconfig/arm.conf
MACHINE = "qemuarm"

# conf/multiconfig/x86.conf
MACHINE = "qemux86-64"

# local.conf
BBMULTICONFIG = "arm x86"

# Build both
bitbake multiconfig:arm:core-image-minimal multiconfig:x86:core-image-minimal
```

---

## Dependency Resolution

![dependency_resolution](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/02_yocto_architecture/dependency_resolution.svg)

---

## License Infrastructure

License tracking:

```bash
LICENSE = "GPLv2 & MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=..."

# Multiple licenses
LICENSE = "GPLv2 | BSD"
LICENSE_${PN} = "GPLv2"
LICENSE_${PN}-dev = "BSD"
```

License management:

```bash
# Exclude GPLv3
INCOMPATIBLE_LICENSE = "GPLv3"

# Commercial licenses
LICENSE_FLAGS = "commercial"
LICENSE_FLAGS_WHITELIST = "commercial_foo"
```

---

## Summary

Key architectural concepts:
- Metadata-driven build system
- Layer-based organization
- Task-based execution model
- Shared state acceleration
- Package management infrastructure

Understanding the architecture enables:
- Effective debugging
- Performance optimization
- Custom implementations
- Better troubleshooting
