# Yocto Architecture Deep Dive

---

## Architecture Overview

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="400" fill="#f0f0f0" stroke="#333" stroke-width="2"/>

  <rect x="100" y="100" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="1"/>
  <text x="175" y="135" text-anchor="middle" font-size="12">Configuration</text>

  <rect x="300" y="100" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="1"/>
  <text x="375" y="135" text-anchor="middle" font-size="12">Metadata</text>

  <rect x="500" y="100" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="1"/>
  <text x="575" y="135" text-anchor="middle" font-size="12">BitBake</text>

  <rect x="100" y="220" width="250" height="60" fill="#ffeecc" stroke="#000" stroke-width="1"/>
  <text x="225" y="255" text-anchor="middle" font-size="12">Task Execution</text>

  <rect x="400" y="220" width="250" height="60" fill="#eeccff" stroke="#000" stroke-width="1"/>
  <text x="525" y="255" text-anchor="middle" font-size="12">Package Creation</text>

  <rect x="250" y="340" width="250" height="60" fill="#ccffff" stroke="#000" stroke-width="1"/>
  <text x="375" y="375" text-anchor="middle" font-size="12">Image Generation</text>

  <path d="M 175 160 L 225 220" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <path d="M 375 160 L 225 220" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <path d="M 575 160 L 525 220" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <path d="M 350 280 L 375 340" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <path d="M 525 280 L 375 340" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#000"/>
    </marker>
  </defs>
</svg>
```

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

```txt
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

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="80" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="175" y="95" text-anchor="middle" font-size="14" font-weight="bold">Recipes</text>
  <text x="175" y="115" text-anchor="middle" font-size="11">(.bb files)</text>

  <rect x="325" y="50" width="150" height="80" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="400" y="95" text-anchor="middle" font-size="14" font-weight="bold">Classes</text>
  <text x="400" y="115" text-anchor="middle" font-size="11">(.bbclass files)</text>

  <rect x="550" y="50" width="150" height="80" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="625" y="95" text-anchor="middle" font-size="14" font-weight="bold">Configuration</text>
  <text x="625" y="115" text-anchor="middle" font-size="11">(.conf files)</text>

  <rect x="100" y="200" width="150" height="80" fill="#ffeecc" stroke="#000" stroke-width="2"/>
  <text x="175" y="245" text-anchor="middle" font-size="14" font-weight="bold">Append Files</text>
  <text x="175" y="265" text-anchor="middle" font-size="11">(.bbappend)</text>

  <rect x="325" y="200" width="150" height="80" fill="#eeccff" stroke="#000" stroke-width="2"/>
  <text x="400" y="245" text-anchor="middle" font-size="14" font-weight="bold">Include Files</text>
  <text x="400" y="265" text-anchor="middle" font-size="11">(.inc files)</text>

  <rect x="550" y="200" width="150" height="80" fill="#ccffff" stroke="#000" stroke-width="2"/>
  <text x="625" y="245" text-anchor="middle" font-size="14" font-weight="bold">Patches</text>
  <text x="625" y="265" text-anchor="middle" font-size="11">(.patch files)</text>
</svg>
```

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

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="350" y="50" width="100" height="60" fill="#e6f3ff" stroke="#0066cc" stroke-width="2"/>
  <text x="400" y="85" text-anchor="middle" font-size="12" font-weight="bold">base</text>

  <rect x="250" y="150" width="100" height="60" fill="#fff0e6" stroke="#ff6600" stroke-width="2"/>
  <text x="300" y="185" text-anchor="middle" font-size="12">autotools</text>

  <rect x="450" y="150" width="100" height="60" fill="#fff0e6" stroke="#ff6600" stroke-width="2"/>
  <text x="500" y="185" text-anchor="middle" font-size="12">cmake</text>

  <rect x="150" y="250" width="100" height="60" fill="#e6ffe6" stroke="#00cc00" stroke-width="2"/>
  <text x="200" y="285" text-anchor="middle" font-size="12">pkgconfig</text>

  <rect x="350" y="250" width="100" height="60" fill="#e6ffe6" stroke="#00cc00" stroke-width="2"/>
  <text x="400" y="285" text-anchor="middle" font-size="12">systemd</text>

  <rect x="550" y="250" width="100" height="60" fill="#e6ffe6" stroke="#00cc00" stroke-width="2"/>
  <text x="600" y="285" text-anchor="middle" font-size="12">python3</text>

  <path d="M 400 110 L 300 150" stroke="#333" stroke-width="1" marker-end="url(#arrow)"/>
  <path d="M 400 110 L 500 150" stroke="#333" stroke-width="1" marker-end="url(#arrow)"/>
  <path d="M 300 210 L 200 250" stroke="#333" stroke-width="1" marker-end="url(#arrow)"/>
  <path d="M 300 210 L 400 250" stroke="#333" stroke-width="1" marker-end="url(#arrow)"/>
  <path d="M 500 210 L 600 250" stroke="#333" stroke-width="1" marker-end="url(#arrow)"/>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

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

```txt
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

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="300" y="50" width="200" height="60" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="400" y="85" text-anchor="middle" font-size="14" font-weight="bold">Configuration</text>

  <rect x="300" y="150" width="200" height="60" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="400" y="185" text-anchor="middle" font-size="14" font-weight="bold">Parsing</text>

  <rect x="300" y="250" width="200" height="60" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="400" y="285" text-anchor="middle" font-size="14" font-weight="bold">Task Execution</text>

  <rect x="300" y="350" width="200" height="60" fill="#ffeecc" stroke="#000" stroke-width="2"/>
  <text x="400" y="385" text-anchor="middle" font-size="14" font-weight="bold">Image Creation</text>

  <path d="M 400 110 L 400 150" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <path d="M 400 210 L 400 250" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <path d="M 400 310 L 400 350" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>

  <text x="550" y="85" text-anchor="start" font-size="11">Machine, Distro, Layers</text>
  <text x="550" y="185" text-anchor="start" font-size="11">Recipe analysis</text>
  <text x="550" y="285" text-anchor="start" font-size="11">Fetch, Compile, Package</text>
  <text x="550" y="385" text-anchor="start" font-size="11">Rootfs, Bootloader</text>

  <defs>
    <marker id="arr2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

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

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="120" height="50" fill="#ffcccc" stroke="#000" stroke-width="1"/>
  <text x="160" y="80" text-anchor="middle" font-size="12">do_fetch</text>

  <rect x="250" y="50" width="120" height="50" fill="#ccffcc" stroke="#000" stroke-width="1"/>
  <text x="310" y="80" text-anchor="middle" font-size="12">do_unpack</text>

  <rect x="400" y="50" width="120" height="50" fill="#ccccff" stroke="#000" stroke-width="1"/>
  <text x="460" y="80" text-anchor="middle" font-size="12">do_patch</text>

  <rect x="550" y="50" width="120" height="50" fill="#ffeecc" stroke="#000" stroke-width="1"/>
  <text x="610" y="80" text-anchor="middle" font-size="12">do_configure</text>

  <rect x="100" y="150" width="120" height="50" fill="#eeccff" stroke="#000" stroke-width="1"/>
  <text x="160" y="180" text-anchor="middle" font-size="12">do_compile</text>

  <rect x="250" y="150" width="120" height="50" fill="#ccffff" stroke="#000" stroke-width="1"/>
  <text x="310" y="180" text-anchor="middle" font-size="12">do_install</text>

  <rect x="400" y="150" width="120" height="50" fill="#ffe6e6" stroke="#000" stroke-width="1"/>
  <text x="460" y="180" text-anchor="middle" font-size="12">do_package</text>

  <rect x="550" y="150" width="120" height="50" fill="#e6ffe6" stroke="#000" stroke-width="1"/>
  <text x="610" y="180" text-anchor="middle" font-size="12">do_package_write</text>

  <path d="M 220 75 L 250 75" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 370 75 L 400 75" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 520 75 L 550 75" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 610 100 L 160 150" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 220 175 L 250 175" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 370 175 L 400 175" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 520 175 L 550 175" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>

  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

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

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="200" height="200" fill="#e6f3ff" stroke="#0066cc" stroke-width="2"/>
  <text x="200" y="130" text-anchor="middle" font-size="14" font-weight="bold">Build Directory</text>

  <rect x="120" y="150" width="160" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="200" y="175" text-anchor="middle" font-size="12">Task Execution</text>

  <rect x="120" y="210" width="160" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="200" y="235" text-anchor="middle" font-size="12">Hash Calculation</text>

  <rect x="500" y="100" width="200" height="200" fill="#fff0e6" stroke="#ff6600" stroke-width="2"/>
  <text x="600" y="130" text-anchor="middle" font-size="14" font-weight="bold">Sstate Cache</text>

  <rect x="520" y="150" width="160" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="600" y="175" text-anchor="middle" font-size="12">Cached Results</text>

  <rect x="520" y="210" width="160" height="40" fill="#fff" stroke="#333" stroke-width="1"/>
  <text x="600" y="235" text-anchor="middle" font-size="12">Hash Index</text>

  <path d="M 300 170 L 500 170" stroke="#00cc00" stroke-width="2" marker-end="url(#a3)"/>
  <text x="400" y="160" text-anchor="middle" font-size="11">Store</text>

  <path d="M 500 230 L 300 230" stroke="#0066cc" stroke-width="2" marker-end="url(#a3)"/>
  <text x="400" y="250" text-anchor="middle" font-size="11">Restore</text>

  <defs>
    <marker id="a3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

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

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="1"/>
  <text x="175" y="85" text-anchor="middle" font-size="12">Package Feed</text>

  <rect x="300" y="50" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="1"/>
  <text x="375" y="85" text-anchor="middle" font-size="12">Rootfs Creation</text>

  <rect x="500" y="50" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="1"/>
  <text x="575" y="85" text-anchor="middle" font-size="12">Image Formatting</text>

  <rect x="100" y="200" width="150" height="60" fill="#ffeecc" stroke="#000" stroke-width="1"/>
  <text x="175" y="235" text-anchor="middle" font-size="12">Post Processing</text>

  <rect x="300" y="200" width="150" height="60" fill="#eeccff" stroke="#000" stroke-width="1"/>
  <text x="375" y="235" text-anchor="middle" font-size="12">Compression</text>

  <rect x="500" y="200" width="150" height="60" fill="#ccffff" stroke="#000" stroke-width="1"/>
  <text x="575" y="235" text-anchor="middle" font-size="12">Deploy</text>

  <path d="M 250 80 L 300 80" stroke="#333" stroke-width="1" marker-end="url(#a4)"/>
  <path d="M 450 80 L 500 80" stroke="#333" stroke-width="1" marker-end="url(#a4)"/>
  <path d="M 575 110 L 175 200" stroke="#333" stroke-width="1" marker-end="url(#a4)"/>
  <path d="M 250 235 L 300 235" stroke="#333" stroke-width="1" marker-end="url(#a4)"/>
  <path d="M 450 235 L 500 235" stroke="#333" stroke-width="1" marker-end="url(#a4)"/>

  <defs>
    <marker id="a4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

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

```txt
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

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="200" r="40" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="400" y="205" text-anchor="middle" font-size="12">Recipe A</text>

  <circle cx="250" cy="100" r="35" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="250" y="105" text-anchor="middle" font-size="11">Recipe B</text>

  <circle cx="550" cy="100" r="35" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="550" y="105" text-anchor="middle" font-size="11">Recipe C</text>

  <circle cx="250" cy="300" r="35" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="250" y="305" text-anchor="middle" font-size="11">Recipe D</text>

  <circle cx="550" cy="300" r="35" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="550" y="305" text-anchor="middle" font-size="11">Recipe E</text>

  <path d="M 370 175 L 280 125" stroke="#333" stroke-width="1" marker-end="url(#a5)"/>
  <text x="325" y="145" text-anchor="middle" font-size="10">DEPENDS</text>

  <path d="M 430 175 L 520 125" stroke="#333" stroke-width="1" marker-end="url(#a5)"/>
  <text x="475" y="145" text-anchor="middle" font-size="10">DEPENDS</text>

  <path d="M 370 225 L 280 275" stroke="#0066cc" stroke-width="1" marker-end="url(#a5)"/>
  <text x="325" y="255" text-anchor="middle" font-size="10">RDEPENDS</text>

  <path d="M 430 225 L 520 275" stroke="#0066cc" stroke-width="1" marker-end="url(#a5)"/>
  <text x="475" y="255" text-anchor="middle" font-size="10">RDEPENDS</text>

  <defs>
    <marker id="a5" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

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
