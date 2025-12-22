# Layer Management and Recipes

---

## Layer Management Overview

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="400" fill="#f5f5f5" stroke="#333" stroke-width="2"/>

  <rect x="150" y="350" width="500" height="60" fill="#ffe6e6" stroke="#cc0000" stroke-width="2" rx="5"/>
  <text x="400" y="385" text-anchor="middle" font-size="14" font-weight="bold">BSP Layer (meta-bsp)</text>

  <rect x="200" y="270" width="400" height="60" fill="#e6ffe6" stroke="#00cc00" stroke-width="2" rx="5"/>
  <text x="400" y="305" text-anchor="middle" font-size="14" font-weight="bold">Distribution Layer (meta-distro)</text>

  <rect x="250" y="190" width="300" height="60" fill="#e6e6ff" stroke="#0000cc" stroke-width="2" rx="5"/>
  <text x="400" y="225" text-anchor="middle" font-size="14" font-weight="bold">Application Layer (meta-app)</text>

  <rect x="300" y="110" width="200" height="60" fill="#ffffe6" stroke="#cccc00" stroke-width="2" rx="5"/>
  <text x="400" y="145" text-anchor="middle" font-size="14" font-weight="bold">OE-Core (meta)</text>

  <text x="50" y="385" text-anchor="middle" font-size="11">Priority: 6</text>
  <text x="50" y="305" text-anchor="middle" font-size="11">Priority: 7</text>
  <text x="50" y="225" text-anchor="middle" font-size="11">Priority: 8</text>
  <text x="50" y="145" text-anchor="middle" font-size="11">Priority: 5</text>
</svg>
```

---

## Layer Anatomy

Standard layer structure:
```txt
meta-custom/
├── COPYING.MIT                    # License file
├── README                         # Layer documentation
├── conf/
│   ├── layer.conf                # Layer configuration
│   ├── machine/                  # Machine configs
│   └── distro/                   # Distribution configs
├── classes/                       # Custom classes
├── recipes-*/                     # Recipe directories
├── files/                         # Common files
└── lib/                          # Python libraries
```

---

## Layer Configuration File

`conf/layer.conf`:

```bash
# Layer identifier
BBPATH .= ":${LAYERDIR}"

# Recipe locations
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
            ${LAYERDIR}/recipes-*/*/*.bbappend"

# Layer name
BBFILE_COLLECTIONS += "custom-layer"
BBFILE_PATTERN_custom-layer = "^${LAYERDIR}/"
BBFILE_PRIORITY_custom-layer = "7"

# Layer dependencies
LAYERDEPENDS_custom-layer = "core openembedded-layer"
LAYERSERIES_COMPAT_custom-layer = "kirkstone langdale"
```

---

## Layer Priority System

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="175" y="125" text-anchor="middle" font-size="12">Priority: 5</text>
  <text x="175" y="145" text-anchor="middle" font-size="11">OE-Core</text>

  <rect x="325" y="100" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="400" y="125" text-anchor="middle" font-size="12">Priority: 6</text>
  <text x="400" y="145" text-anchor="middle" font-size="11">BSP Layer</text>

  <rect x="550" y="100" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="625" y="125" text-anchor="middle" font-size="12">Priority: 8</text>
  <text x="625" y="145" text-anchor="middle" font-size="11">App Layer</text>

  <rect x="300" y="250" width="200" height="80" fill="#ffffcc" stroke="#000" stroke-width="3"/>
  <text x="400" y="280" text-anchor="middle" font-size="14" font-weight="bold">Final Recipe</text>
  <text x="400" y="300" text-anchor="middle" font-size="11">Higher priority wins</text>

  <path d="M 175 160 L 350 250" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 400 160 L 400 250" stroke="#00cc00" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 625 160 L 450 250" stroke="#0000cc" stroke-width="3" marker-end="url(#arrow1)"/>

  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

---

## Creating a New Layer

```bash
# Using bitbake-layers command
bitbake-layers create-layer meta-mycompany

# Manual structure creation
mkdir -p meta-mycompany/{conf,classes,recipes-apps}
cd meta-mycompany

# Create layer.conf
cat > conf/layer.conf << 'EOF'
BBPATH .= ":${LAYERDIR}"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb"
BBFILE_COLLECTIONS += "mycompany"
BBFILE_PATTERN_mycompany = "^${LAYERDIR}/"
BBFILE_PRIORITY_mycompany = "7"
LAYERSERIES_COMPAT_mycompany = "kirkstone"
EOF

# Create README
echo "# My Company Layer" > README
```

---

## Adding Layers to Build

Manual addition to `conf/bblayers.conf`:

```bash
BBLAYERS ?= " \
  /path/to/poky/meta \
  /path/to/poky/meta-poky \
  /path/to/poky/meta-yocto-bsp \
  /path/to/meta-openembedded/meta-oe \
  /path/to/meta-mycompany \
  "
```

Using bitbake-layers:

```bash
bitbake-layers add-layer ../meta-mycompany
bitbake-layers show-layers
bitbake-layers remove-layer meta-mycompany
```

---

## Layer Dependencies

Declaring dependencies:

```bash
# In conf/layer.conf
LAYERDEPENDS_mycompany = "core openembedded-layer networking-layer"

# Version-specific dependency
LAYERDEPENDS_mycompany = "core:kirkstone openembedded-layer"
```

Checking dependencies:

```bash
bitbake-layers show-layers
bitbake-layers layerindex-fetch meta-qt5
bitbake-layers layerindex-show-depends meta-qt5
```

---

## Recipe Organization

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="200" height="60" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="200" y="85" text-anchor="middle" font-size="12">recipes-apps</text>

  <rect x="100" y="150" width="200" height="60" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="200" y="185" text-anchor="middle" font-size="12">recipes-core</text>

  <rect x="100" y="250" width="200" height="60" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="200" y="285" text-anchor="middle" font-size="12">recipes-kernel</text>

  <rect x="100" y="350" width="200" height="60" fill="#ffeecc" stroke="#000" stroke-width="2"/>
  <text x="200" y="385" text-anchor="middle" font-size="12">recipes-bsp</text>

  <rect x="400" y="50" width="300" height="60" fill="#f0f0f0" stroke="#666" stroke-width="1"/>
  <text x="550" y="85" text-anchor="middle" font-size="11">Application packages</text>

  <rect x="400" y="150" width="300" height="60" fill="#f0f0f0" stroke="#666" stroke-width="1"/>
  <text x="550" y="185" text-anchor="middle" font-size="11">System components</text>

  <rect x="400" y="250" width="300" height="60" fill="#f0f0f0" stroke="#666" stroke-width="1"/>
  <text x="550" y="285" text-anchor="middle" font-size="11">Kernel and modules</text>

  <rect x="400" y="350" width="300" height="60" fill="#f0f0f0" stroke="#666" stroke-width="1"/>
  <text x="550" y="385" text-anchor="middle" font-size="11">Bootloaders, firmware</text>

  <path d="M 300 80 L 400 80" stroke="#333" stroke-width="1" marker-end="url(#arrow2)"/>
  <path d="M 300 180 L 400 180" stroke="#333" stroke-width="1" marker-end="url(#arrow2)"/>
  <path d="M 300 280 L 400 280" stroke="#333" stroke-width="1" marker-end="url(#arrow2)"/>
  <path d="M 300 380 L 400 380" stroke="#333" stroke-width="1" marker-end="url(#arrow2)"/>

  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

---

## Recipe Naming Conventions

Standard naming:
- `packagename_version.bb` - Base recipe
- `packagename_version.bbappend` - Recipe extension
- `packagename.inc` - Include file
- `packagename-common.inc` - Shared definitions

Examples:

```txt
recipes-apps/myapp/
├── myapp_1.0.bb
├── myapp_1.1.bb
├── myapp.inc
└── files/
    ├── myapp.service
    └── config.ini
```

---

## Basic Recipe Structure

```bash
# recipes-apps/helloworld/helloworld_1.0.bb
SUMMARY = "Hello World Application"
DESCRIPTION = "Simple hello world C application"
HOMEPAGE = "https://example.com/helloworld"
SECTION = "examples"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://helloworld.c \
           file://Makefile"

S = "${WORKDIR}"

do_compile() {
    ${CC} ${CFLAGS} ${LDFLAGS} helloworld.c -o helloworld
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 helloworld ${D}${bindir}
}
```

---

## Recipe Variables

Essential variables:

```bash
# Metadata
SUMMARY = "Short description"
DESCRIPTION = "Longer description"
HOMEPAGE = "http://example.com"
SECTION = "apps"
PRIORITY = "optional"

# Licensing
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=..."

# Source location
SRC_URI = "git://github.com/example/repo.git;protocol=https;branch=master"
SRCREV = "abc123def456..."

# Build directory
S = "${WORKDIR}/git"
B = "${WORKDIR}/build"
```

---

## Source URI Schemes

Git repository:

```bash
SRC_URI = "git://github.com/user/repo.git;protocol=https;branch=main"
SRCREV = "${AUTOREV}"  # or specific commit hash
```

HTTP/HTTPS download:

```bash
SRC_URI = "https://example.com/package-${PV}.tar.gz"
SRC_URI[md5sum] = "abc123..."
SRC_URI[sha256sum] = "def456..."
```

Local files:

```bash
SRC_URI = "file://myapp.c \
           file://config.h \
           file://0001-fix-bug.patch"
```

---

## File Organization

```txt
recipes-apps/myapp/
├── myapp_1.0.bb
└── myapp/
    ├── myapp.c
    ├── config.h
    ├── myapp.service
    └── patches/
        ├── 0001-fix-compilation.patch
        └── 0002-update-config.patch
```

File search path:

```bash
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
SRC_URI += "file://custom-config.txt"
```

---

## Patching Workflow

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="175" y="135" text-anchor="middle" font-size="12">do_fetch</text>

  <rect x="300" y="100" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="375" y="135" text-anchor="middle" font-size="12">do_unpack</text>

  <rect x="500" y="100" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="575" y="135" text-anchor="middle" font-size="12">do_patch</text>

  <rect x="100" y="250" width="550" height="80" fill="#ffffcc" stroke="#000" stroke-width="2"/>
  <text x="375" y="285" text-anchor="middle" font-size="14" font-weight="bold">Patched Source Code</text>
  <text x="375" y="305" text-anchor="middle" font-size="11">Ready for compilation</text>

  <path d="M 250 130 L 300 130" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <path d="M 450 130 L 500 130" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <path d="M 575 160 L 575 250" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>

  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

---

## Creating Patches

Using devtool:

```bash
# Create workspace
devtool modify busybox

# Make changes to source
cd workspace/sources/busybox
# ... edit files ...

# Generate patches
devtool update-recipe busybox
```

Manual patch creation:

```bash
# In source directory
git add modified-file.c
git commit -m "Fix bug in processing"
git format-patch -1 -o /path/to/recipe/files/
```

---

## Applying Patches

In recipe:

```bash
SRC_URI += "file://0001-fix-buffer-overflow.patch \
            file://0002-add-feature.patch"

# Patch location
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

# Patch striplevel (default is 1)
SRC_URI += "file://myfix.patch;striplevel=0"

# Conditional patching
SRC_URI_append_arm = " file://arm-specific.patch"
```

---

## Recipe Inheritance

```bash
# Autotools-based project
inherit autotools

# CMake-based project
inherit cmake

# Python package
inherit setuptools3

# Kernel module
inherit module

# Systemd service
inherit systemd

# Multiple inheritance
inherit autotools pkgconfig systemd
```

---

## Autotools Class

For GNU autoconf/automake projects:

```bash
inherit autotools

# Default tasks provided:
# do_configure: runs ./configure
# do_compile: runs make
# do_install: runs make install

# Custom configure options
EXTRA_OECONF = "--enable-feature --with-lib=/usr"

# Custom make flags
EXTRA_OEMAKE = "CFLAGS='-O2 -g'"

# Disable parallel make
PARALLEL_MAKE = ""
```

---

## CMake Class

For CMake-based projects:

```bash
inherit cmake

# CMake options
EXTRA_OECMAKE = "-DENABLE_TESTS=ON \
                 -DCMAKE_BUILD_TYPE=Release"

# Custom build directory
B = "${WORKDIR}/build"

# Out-of-tree build (default with cmake)
OECMAKE_SOURCEPATH = "${S}"
OECMAKE_BUILDPATH = "${B}"
```

---

## Task Functions

Standard task structure:

```bash
do_compile() {
    # Compilation commands
    oe_runmake
}

do_install() {
    # Installation commands
    install -d ${D}${bindir}
    install -m 0755 ${B}/myapp ${D}${bindir}

    install -d ${D}${sysconfdir}
    install -m 0644 ${WORKDIR}/config.ini ${D}${sysconfdir}
}

do_configure_prepend() {
    # Run before do_configure
}

do_compile_append() {
    # Run after do_compile
}
```

---

## Task Dependencies

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="120" height="50" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="160" y="80" text-anchor="middle" font-size="11">do_fetch</text>

  <rect x="340" y="50" width="120" height="50" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="400" y="80" text-anchor="middle" font-size="11">do_unpack</text>

  <rect x="580" y="50" width="120" height="50" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="640" y="80" text-anchor="middle" font-size="11">do_patch</text>

  <rect x="100" y="150" width="120" height="50" fill="#ffeecc" stroke="#000" stroke-width="2"/>
  <text x="160" y="180" text-anchor="middle" font-size="11">do_configure</text>

  <rect x="340" y="150" width="120" height="50" fill="#eeccff" stroke="#000" stroke-width="2"/>
  <text x="400" y="180" text-anchor="middle" font-size="11">do_compile</text>

  <rect x="580" y="150" width="120" height="50" fill="#ccffff" stroke="#000" stroke-width="2"/>
  <text x="640" y="180" text-anchor="middle" font-size="11">do_install</text>

  <rect x="340" y="250" width="120" height="50" fill="#ffe6e6" stroke="#000" stroke-width="2"/>
  <text x="400" y="280" text-anchor="middle" font-size="11">do_package</text>

  <path d="M 220 75 L 340 75" stroke="#333" stroke-width="1.5" marker-end="url(#arr4)"/>
  <path d="M 460 75 L 580 75" stroke="#333" stroke-width="1.5" marker-end="url(#arr4)"/>
  <path d="M 640 100 L 160 150" stroke="#333" stroke-width="1.5" marker-end="url(#arr4)"/>
  <path d="M 220 175 L 340 175" stroke="#333" stroke-width="1.5" marker-end="url(#arr4)"/>
  <path d="M 460 175 L 580 175" stroke="#333" stroke-width="1.5" marker-end="url(#arr4)"/>
  <path d="M 640 200 L 400 250" stroke="#333" stroke-width="1.5" marker-end="url(#arr4)"/>

  <defs>
    <marker id="arr4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>
```

---

## Custom Task Definition

```bash
# Define new task
do_mytask() {
    echo "Executing custom task"
    # Task commands
}

# Add task to task graph
addtask mytask after do_compile before do_install

# Task dependencies
do_mytask[depends] = "otherpkg:do_populate_sysroot"
do_mytask[rdepends] = "runtime-package"

# Mark as nostamp (always run)
do_mytask[nostamp] = "1"
```

---

## Dependencies: DEPENDS vs RDEPENDS

Build-time dependencies (DEPENDS):

```bash
# Required during compilation
DEPENDS = "zlib openssl libxml2"

# Provider-based dependency
DEPENDS = "virtual/kernel virtual/libc"

# Task-specific dependency
do_compile[depends] = "curl:do_populate_sysroot"
```

Runtime dependencies (RDEPENDS):

```bash
# Required at runtime
RDEPENDS_${PN} = "python3 bash perl"

# Package-specific
RDEPENDS_${PN}-dev = "${PN}"
RDEPENDS_${PN}-tools = "${PN} python3-core"
```

---

## Package Splitting

```bash
# Default packages
PACKAGES = "${PN}-dbg ${PN}-staticdev ${PN}-dev ${PN}-doc ${PN}-locale ${PN}"

# File assignments
FILES_${PN} = "${bindir}/* ${libdir}/lib*.so.*"
FILES_${PN}-dev = "${includedir} ${libdir}/lib*.so ${libdir}/*.la"
FILES_${PN}-staticdev = "${libdir}/*.a"
FILES_${PN}-dbg = "${prefix}/src ${bindir}/.debug ${libdir}/.debug"
FILES_${PN}-doc = "${mandir} ${infodir} ${docdir}"

# Custom packages
PACKAGES =+ "${PN}-tools ${PN}-plugins"
FILES_${PN}-tools = "${bindir}/tool1 ${bindir}/tool2"
FILES_${PN}-plugins = "${libdir}/${PN}/plugins/*.so"
```

---

## Recipe Append Files

Extending existing recipes:

```bash
# meta-custom/recipes-core/busybox/busybox_%.bbappend

# Add custom configuration
SRC_URI += "file://custom.cfg"

# Modify install
do_install_append() {
    install -d ${D}${sysconfdir}/busybox
    install -m 0644 ${WORKDIR}/custom.cfg ${D}${sysconfdir}/busybox/
}

# Add runtime dependency
RDEPENDS_${PN} += "bash"
```

File path matching:

```bash
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
```

---

## Include Files

Common definitions:

```bash
# myapp-common.inc
HOMEPAGE = "https://example.com"
SECTION = "apps"
LICENSE = "MIT"

DEPENDS = "zlib openssl"

inherit cmake systemd

SYSTEMD_SERVICE_${PN} = "myapp.service"
```

Using in recipes:

```bash
# myapp_1.0.bb
require myapp-common.inc

SRC_URI = "https://example.com/myapp-${PV}.tar.gz"
SRC_URI[sha256sum] = "abc123..."
```

---

## PACKAGECONFIG System

Feature management:

```bash
# Default features
PACKAGECONFIG ??= "ssl ipv6 ${@bb.utils.filter('DISTRO_FEATURES', 'systemd', d)}"

# Feature definitions: enable,disable,depends,rdepends
PACKAGECONFIG[ssl] = "--with-ssl,--without-ssl,openssl,openssl"
PACKAGECONFIG[ipv6] = "--enable-ipv6,--disable-ipv6"
PACKAGECONFIG[systemd] = "--with-systemd,--without-systemd,systemd,systemd"
PACKAGECONFIG[tests] = "--enable-tests,--disable-tests,cppunit"

# Machine-specific
PACKAGECONFIG_append_arm = " neon"
PACKAGECONFIG[neon] = "--enable-neon,--disable-neon"
```

---

## Virtual Providers

Defining providers:

```bash
# In recipe
PROVIDES = "virtual/kernel"
PROVIDES = "virtual/bootloader"
PROVIDES = "virtual/libc"

# Multiple provides
PROVIDES = "virtual/libgl virtual/egl"
```

Selecting providers:

```bash
# In machine config or local.conf
PREFERRED_PROVIDER_virtual/kernel = "linux-custom"
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-custom"

# Version preference
PREFERRED_VERSION_linux-custom = "5.15%"
```

---

## Recipe Debugging

```bash
# Show environment
bitbake -e myapp | grep ^VARIABLE=

# List tasks
bitbake -c listtasks myapp

# Run specific task
bitbake -c compile myapp

# Development shell
bitbake -c devshell myapp

# Clean tasks
bitbake -c clean myapp
bitbake -c cleansstate myapp
bitbake -c cleanall myapp
```

---

## Using devtool

Create new recipe:

```bash
# From source
devtool add myapp https://github.com/example/myapp.git

# Modify existing recipe
devtool modify busybox

# Update recipe after changes
devtool update-recipe myapp

# Finish and add to layer
devtool finish myapp meta-custom
```

---

## Recipe Style Guidelines

Best practices:

```bash
# Order variables logically
SUMMARY = "..."
DESCRIPTION = "..."
HOMEPAGE = "..."
LICENSE = "..."
SECTION = "..."

# Group related variables
SRC_URI = "..."
SRCREV = "..."
S = "${WORKDIR}/git"

# Use proper indentation
do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/app ${D}${bindir}
}

# Add comments
# Fix bug #1234
SRC_URI += "file://fix-bug-1234.patch"
```

---

## Recipe Variables Reference

Path variables:

```bash
${WORKDIR}      # Build workspace
${S}            # Source directory
${B}            # Build directory
${D}            # Destination (install root)
${PN}           # Package name
${PV}           # Package version
${PR}           # Package revision
${STAGING_DIR}  # Staging directory
```

Installation paths:

```bash
${bindir}       # /usr/bin
${sbindir}      # /usr/sbin
${libdir}       # /usr/lib
${includedir}   # /usr/include
${sysconfdir}   # /etc
${datadir}      # /usr/share
```

---

## Conditional Compilation

Machine-specific:

```bash
SRC_URI_append_arm = " file://arm-optimizations.patch"
CFLAGS_append_arm = " -mfpu=neon"

do_compile_append_qemux86-64() {
    # x86-64 specific compile steps
}
```

Distribution features:

```bash
PACKAGECONFIG_append = "${@bb.utils.contains('DISTRO_FEATURES', 'x11', ' x11', '', d)}"

RDEPENDS_${PN} += "${@bb.utils.contains('DISTRO_FEATURES', 'wayland', 'wayland', 'x11', d)}"
```

---

## Python Functions in Recipes

```bash
python do_mytask() {
    import os

    workdir = d.getVar('WORKDIR')
    pn = d.getVar('PN')

    bb.note("Processing %s in %s" % (pn, workdir))

    # Execute shell command
    bb.build.exec_func('do_compile', d)
}

# Inline Python
VARIABLE = "${@'value1' if condition else 'value2'}"

# Python snippets
MY_VAR = "${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'yes', 'no', d)}"
```

---

## Recipe Testing

QA checks:

```bash
# Skip specific QA tests
INSANE_SKIP_${PN} = "dev-so ldflags"

# Package-specific skips
INSANE_SKIP_${PN}-dev = "staticdev"

# Add custom QA checks
inherit packageqa
ERROR_QA_append = " my-custom-check"
```

Runtime testing:

```bash
# Add to image for testing
IMAGE_INSTALL_append = " myapp"

# Run tests
inherit ptest
RDEPENDS_${PN}-ptest += "make bash"
```

---

## Advanced Recipe Techniques

Anonymous Python:

```bash
python __anonymous() {
    # Runs during parsing
    if d.getVar('PN') == 'special-package':
        d.setVar('SPECIAL_FLAG', '1')
}
```

Event handlers:

```bash
addhandler myevent_handler
myevent_handler[eventmask] = "bb.event.BuildStarted"
python myevent_handler() {
    bb.note("Build started")
}
```

---

## License Handling

```bash
# Single license
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123..."

# Multiple licenses
LICENSE = "GPLv2 & LGPLv2.1"
LIC_FILES_CHKSUM = "file://COPYING;md5=... \
                    file://COPYING.LIB;md5=..."

# Dual licensing
LICENSE = "GPLv2 | BSD"

# Per-package licensing
LICENSE_${PN} = "GPLv2"
LICENSE_${PN}-libs = "LGPLv2.1"
```

---

## Working with Git Repositories

```bash
# Basic git source
SRC_URI = "git://github.com/example/repo.git;protocol=https;branch=master"
SRCREV = "abc123def456..."

# Use latest (not recommended for production)
SRCREV = "${AUTOREV}"

# Submodules
SRC_URI = "git://github.com/example/repo.git;protocol=https;nobranch=1"
SRC_URI += "git://github.com/example/submod.git;protocol=https;destsuffix=git/submodule"

# Multiple repositories
SRC_URI = "git://github.com/example/main.git;name=main;branch=master \
           git://github.com/example/plugin.git;name=plugin;destsuffix=plugins"
SRCREV_main = "abc123..."
SRCREV_plugin = "def456..."
```

---

## Systemd Integration

```bash
inherit systemd

# Service file
SRC_URI += "file://myapp.service"

# Systemd variables
SYSTEMD_SERVICE_${PN} = "myapp.service"
SYSTEMD_AUTO_ENABLE = "enable"

# Install service file
do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/myapp.service ${D}${systemd_unitdir}/system
}

# Runtime dependency
RDEPENDS_${PN} += "systemd"
```

---

## User Management

```bash
inherit useradd

# Create user and group
USERADD_PACKAGES = "${PN}"
USERADD_PARAM_${PN} = "-u 1000 -d /home/myapp -s /bin/sh myapp"
GROUPADD_PARAM_${PN} = "-g 1000 myapp"

# Set file ownership
do_install_append() {
    chown -R myapp:myapp ${D}/var/lib/myapp
}
```

---

## Summary

Key concepts covered:
- Layer structure and management
- Recipe organization and naming
- Source management and patching
- Task execution and dependencies
- Package splitting and dependencies
- Advanced recipe techniques

Best practices:
- Organize layers logically
- Follow naming conventions
- Use classes effectively
- Document customizations
- Test thoroughly
