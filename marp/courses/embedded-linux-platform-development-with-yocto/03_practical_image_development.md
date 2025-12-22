# Practical Image Development

---

## Image Development Workflow

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="175" y="85" text-anchor="middle" font-size="12">Choose Base</text>

  <rect x="300" y="50" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="375" y="85" text-anchor="middle" font-size="12">Select Packages</text>

  <rect x="500" y="50" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="575" y="85" text-anchor="middle" font-size="12">Configure Features</text>

  <rect x="100" y="200" width="150" height="60" fill="#ffeecc" stroke="#000" stroke-width="2"/>
  <text x="175" y="235" text-anchor="middle" font-size="12">Customize Rootfs</text>

  <rect x="300" y="200" width="150" height="60" fill="#eeccff" stroke="#000" stroke-width="2"/>
  <text x="375" y="235" text-anchor="middle" font-size="12">Build Image</text>

  <rect x="500" y="200" width="150" height="60" fill="#ccffff" stroke="#000" stroke-width="2"/>
  <text x="575" y="235" text-anchor="middle" font-size="12">Test & Deploy</text>

  <rect x="300" y="350" width="150" height="60" fill="#e6ffe6" stroke="#000" stroke-width="2"/>
  <text x="375" y="385" text-anchor="middle" font-size="12">Iterate</text>

  <path d="M 250 80 L 300 80" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 450 80 L 500 80" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 575 110 L 175 200" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 250 235 L 300 235" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 450 235 L 500 235" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 575 260 L 375 350" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 300 380 L 175 260" stroke="#0066cc" stroke-width="2" marker-end="url(#arrow)"/>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Core Image Types

Base images provided by Yocto:
- `core-image-minimal` - Minimal bootable image
- `core-image-minimal-dev` - Minimal with dev packages
- `core-image-base` - Console-only base
- `core-image-full-cmdline` - Full featured console
- `core-image-x11-base` - Basic X11 image
- `core-image-sato` - Mobile UI environment
- `core-image-weston` - Wayland/Weston image

---

## Image Size Comparison

| Image Type | Typical Size | Use Case |
|------------|-------------|----------|
| core-image-minimal | 8-12 MB | Embedded devices |
| core-image-base | 40-60 MB | Network appliances |
| core-image-full-cmdline | 100-150 MB | Servers |
| core-image-sato | 300-400 MB | UI devices |
| core-image-weston | 250-350 MB | Modern graphics |

---

## Creating Custom Images

Basic image recipe:

```bash
# recipes-core/images/custom-image.bb
SUMMARY = "Custom embedded Linux image"

IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"

IMAGE_LINGUAS = " "

LICENSE = "MIT"

inherit core-image

IMAGE_ROOTFS_SIZE ?= "8192"
IMAGE_ROOTFS_EXTRA_SPACE_append = "${@bb.utils.contains('DISTRO_FEATURES', 'systemd', ' + 4096', '', d)}"
```

---

## IMAGE_INSTALL Variable

Package selection:

```bash
# Base system
IMAGE_INSTALL = "packagegroup-core-boot"

# Add specific packages
IMAGE_INSTALL += "openssh dropbear"

# Conditional packages
IMAGE_INSTALL_append = "${@bb.utils.contains('MACHINE_FEATURES', 'wifi', ' wpa-supplicant', '', d)}"

# Development packages
IMAGE_INSTALL_append = " ${@bb.utils.contains('IMAGE_FEATURES', 'dev-pkgs', 'strace gdb', '', d)}"
```

---

## Package Groups

Creating package groups:

```bash
# recipes-core/packagegroup/packagegroup-custom.bb
SUMMARY = "Custom Package Group"

inherit packagegroup

PACKAGES = "\
    ${PN}-base \
    ${PN}-network \
    ${PN}-tools \
"

RDEPENDS_${PN}-base = "\
    bash \
    coreutils \
    util-linux \
"

RDEPENDS_${PN}-network = "\
    ethtool \
    iproute2 \
    iptables \
"

RDEPENDS_${PN}-tools = "\
    htop \
    tmux \
    vim \
"
```

---

## IMAGE_FEATURES

Common features:

```bash
# Enable features
IMAGE_FEATURES += "ssh-server-openssh"
IMAGE_FEATURES += "package-management"
IMAGE_FEATURES += "debug-tweaks"
IMAGE_FEATURES += "dev-pkgs"
IMAGE_FEATURES += "doc-pkgs"
IMAGE_FEATURES += "tools-debug"
IMAGE_FEATURES += "tools-profile"

# Feature combinations
IMAGE_FEATURES = "ssh-server-openssh package-management tools-debug"
```

---

## Feature Effects

| Feature | Effect |
|---------|---------|
| debug-tweaks | Empty root password, debug configs |
| ssh-server-* | SSH server (openssh/dropbear) |
| package-management | Runtime package manager |
| dev-pkgs | Development headers/libs |
| doc-pkgs | Documentation |
| tools-debug | Debugging tools (gdb, strace) |
| tools-profile | Profiling tools |
| read-only-rootfs | Read-only root filesystem |

---

## DISTRO_FEATURES

System-wide features:

```bash
# Common distro features
DISTRO_FEATURES = "alsa bluetooth ext2 ipv4 ipv6 usbhost"
DISTRO_FEATURES += "systemd pam"
DISTRO_FEATURES += "opengl vulkan"
DISTRO_FEATURES += "wayland x11"

# Remove features
DISTRO_FEATURES_remove = "x11"

# Systemd vs sysvinit
DISTRO_FEATURES_append = " systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"
DISTRO_FEATURES_BACKFILL_CONSIDERED = "sysvinit"
```

---

## MACHINE_FEATURES

Hardware capabilities:

```bash
# Common machine features
MACHINE_FEATURES = "ext2 ext3 serial usbhost"
MACHINE_FEATURES += "wifi bluetooth"
MACHINE_FEATURES += "screen touchscreen"
MACHINE_FEATURES += "alsa"

# Graphics
MACHINE_FEATURES += "egl opengl"

# Check in recipes
PACKAGECONFIG_append = "${@bb.utils.contains('MACHINE_FEATURES', 'bluetooth', ' bluez5', '', d)}"
```

---

## QEMU Development

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="50" width="400" height="300" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="400" y="80" text-anchor="middle" font-size="14" font-weight="bold">Host System</text>

  <rect x="250" y="120" width="300" height="180" fill="#e6f3ff" stroke="#0066cc" stroke-width="2"/>
  <text x="400" y="150" text-anchor="middle" font-size="12" font-weight="bold">QEMU</text>

  <rect x="280" y="180" width="240" height="80" fill="#fff0e6" stroke="#ff6600" stroke-width="2"/>
  <text x="400" y="210" text-anchor="middle" font-size="11">Guest Linux</text>
  <text x="400" y="230" text-anchor="middle" font-size="10">ARM/x86/MIPS/PPC</text>
  <text x="400" y="250" text-anchor="middle" font-size="10">Your Image</text>

  <text x="100" y="220" text-anchor="middle" font-size="11">Network</text>
  <text x="100" y="240" text-anchor="middle" font-size="11">Storage</text>
  <text x="100" y="260" text-anchor="middle" font-size="11">Display</text>

  <path d="M 140 220 L 280 220" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 140 240 L 280 240" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>
  <path d="M 140 260 L 280 260" stroke="#333" stroke-width="1" marker-end="url(#ar)"/>

  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Running QEMU Images

Basic commands:

```bash
# Run image
runqemu qemux86-64 core-image-minimal

# With options
runqemu qemux86-64 core-image-minimal nographic

# Specific kernel/rootfs
runqemu qemux86-64 tmp/deploy/images/qemux86-64/bzImage \
    tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.ext4

# Network options
runqemu qemux86-64 core-image-minimal slirp
```

---

## QEMU Configuration

Machine options:

```bash
# QEMU machines available
qemuarm      # ARM versatile
qemuarm64    # ARM 64-bit
qemux86      # x86 32-bit
qemux86-64   # x86 64-bit
qemumips     # MIPS
qemumips64   # MIPS 64-bit
qemuppc      # PowerPC
qemuriscv32  # RISC-V 32-bit
qemuriscv64  # RISC-V 64-bit
```

---

## Rootfs Customization

Post-processing commands:

```bash
# Add users
inherit extrausers
EXTRA_USERS_PARAMS = "\
    useradd -P password user1; \
    usermod -P newpass root; \
"

# Rootfs post-process
ROOTFS_POSTPROCESS_COMMAND += "do_custom_config;"

do_custom_config() {
    # Modify configuration files
    echo "custom-setting" >> ${IMAGE_ROOTFS}/etc/config

    # Set permissions
    chmod 600 ${IMAGE_ROOTFS}/etc/ssh/sshd_config
}
```

---

## Package Management

Runtime package management:

```bash
# Enable package management
IMAGE_FEATURES += "package-management"

# Package format
PACKAGE_CLASSES = "package_rpm"
# or package_deb, package_ipk

# Package feed configuration
PACKAGE_FEED_URIS = "http://192.168.1.100:8080"
PACKAGE_FEED_BASE_PATHS = "rpm"
PACKAGE_FEED_ARCHS = "all cortexa9hf_neon my_machine"
```

---

## Creating Package Feeds

```bash
# Create package index
bitbake package-index

# Serve packages
cd tmp/deploy/rpm
python3 -m http.server 8080

# On target device
smart update
smart install package-name
# or
dnf update
dnf install package-name
```

---

## Image Types and Formats

```bash
# Configure image types
IMAGE_FSTYPES = "ext4 tar.gz wic wic.gz"

# Image type specifics
IMAGE_FSTYPES_append_qemux86-64 = " iso hddimg"

# Compression
IMAGE_FSTYPES = "ext4.gz tar.bz2"

# Multiple types
IMAGE_FSTYPES = "ext4 squashfs ubifs"
```

---

## WIC Image Creation

```bash
# WIC configuration file
# sdimage-bootpart.wks
part /boot --source bootimg-partition --ondisk sda --fstype=vfat --label boot --active --align 1024 --size 64
part / --source rootfs --ondisk sda --fstype=ext4 --label platform --align 1024

bootloader --ptable gpt --timeout=10 --append="rootwait console=ttyS0,115200"
```

Using WIC:

```bash
# In image recipe
WKS_FILE = "sdimage-bootpart.wks"

# Or standalone
wic create sdimage-bootpart -e core-image-minimal
```

---

## Partition Layout

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="150" width="600" height="100" fill="#f5f5f5" stroke="#333" stroke-width="2"/>

  <rect x="100" y="150" width="80" height="100" fill="#ffcccc" stroke="#000" stroke-width="1"/>
  <text x="140" y="185" text-anchor="middle" font-size="11">Boot</text>
  <text x="140" y="205" text-anchor="middle" font-size="10">64MB</text>
  <text x="140" y="225" text-anchor="middle" font-size="10">FAT32</text>

  <rect x="180" y="150" width="300" height="100" fill="#ccffcc" stroke="#000" stroke-width="1"/>
  <text x="330" y="185" text-anchor="middle" font-size="11">Root FS</text>
  <text x="330" y="205" text-anchor="middle" font-size="10">2GB</text>
  <text x="330" y="225" text-anchor="middle" font-size="10">ext4</text>

  <rect x="480" y="150" width="150" height="100" fill="#ccccff" stroke="#000" stroke-width="1"/>
  <text x="555" y="185" text-anchor="middle" font-size="11">Data</text>
  <text x="555" y="205" text-anchor="middle" font-size="10">1GB</text>
  <text x="555" y="225" text-anchor="middle" font-size="10">ext4</text>

  <rect x="630" y="150" width="70" height="100" fill="#ffeecc" stroke="#000" stroke-width="1"/>
  <text x="665" y="185" text-anchor="middle" font-size="11">Swap</text>
  <text x="665" y="205" text-anchor="middle" font-size="10">512MB</text>

  <text x="400" y="130" text-anchor="middle" font-size="12" font-weight="bold">SD Card / eMMC Layout</text>
</svg>

---

## Init Systems

systemd configuration:

```bash
# Enable systemd
DISTRO_FEATURES_append = " systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"
VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"
DISTRO_FEATURES_BACKFILL_CONSIDERED = "sysvinit"

# systemd services
do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/myservice.service ${D}${systemd_unitdir}/system/
}

SYSTEMD_SERVICE_${PN} = "myservice.service"
SYSTEMD_AUTO_ENABLE = "enable"
```

---

## SysVinit Configuration

```bash
# SysVinit setup
VIRTUAL-RUNTIME_init_manager = "sysvinit"

# Init script installation
do_install_append() {
    install -d ${D}${sysconfdir}/init.d
    install -m 0755 ${WORKDIR}/myservice ${D}${sysconfdir}/init.d/
}

# Update-rc.d class
inherit update-rc.d
INITSCRIPT_NAME = "myservice"
INITSCRIPT_PARAMS = "defaults 80 20"
```

---

## Image Optimization

Size reduction techniques:

```bash
# Remove unnecessary packages
IMAGE_INSTALL_remove = "packagegroup-core-ssh-openssh"

# Strip locales
IMAGE_LINGUAS = ""

# Remove documentation
DISTRO_FEATURES_remove = "api-documentation"

# Optimize for size
FULL_OPTIMIZATION = "-Os -pipe ${DEBUG_FLAGS}"

# Use smaller alternatives
PREFERRED_PROVIDER_virtual/kernel = "linux-yocto-tiny"
```

---

## Read-Only Rootfs

```bash
# Enable read-only rootfs
IMAGE_FEATURES += "read-only-rootfs"

# Or via extra image features
EXTRA_IMAGE_FEATURES = "read-only-rootfs"

# Handle writable areas
VOLATILE_BINDS = "\
    /var/volatile/lib /var/lib\n\
    /var/volatile/cache /var/cache\n\
    /var/volatile/spool /var/spool\n\
"

# Persistent storage mount
read_only_rootfs_hook() {
    echo "/dev/mmcblk0p3 /data ext4 defaults 0 0" >> ${IMAGE_ROOTFS}/etc/fstab
}
```

---

## Security Hardening

Basic security measures:

```bash
# Remove debug features in production
IMAGE_FEATURES_remove = "debug-tweaks"

# Set root password
inherit extrausers
EXTRA_USERS_PARAMS = "usermod -P 'complex\$password' root;"

# Disable services
SYSTEMD_AUTO_ENABLE_${PN} = "disable"

# Security flags
require conf/distro/include/security_flags.inc
```

---

## Multi-Configuration Images

```bash
# Build multiple image variants
# conf/multiconfig/production.conf
IMAGE_FEATURES_remove = "debug-tweaks dev-pkgs"
EXTRA_IMAGE_FEATURES = "read-only-rootfs"

# conf/multiconfig/development.conf
IMAGE_FEATURES += "debug-tweaks dev-pkgs tools-debug"
EXTRA_IMAGE_FEATURES = "dbg-pkgs"

# Build both
bitbake multiconfig:production:custom-image multiconfig:development:custom-image
```

---

## Image Testing

Built-in test framework:

```bash
# Enable testing
IMAGE_CLASSES += "testimage"

# Configure tests
TEST_SUITES = "ping ssh df connman syslog rpm parselogs"

# Run tests
bitbake -c testimage core-image-minimal

# Custom test cases
TEST_SUITES += " mytest"
```

---

## Custom Test Cases

```python
# lib/oeqa/runtime/cases/mytest.py
from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends

class MyTest(OERuntimeTestCase):
    @OETestDepends(['ssh.SSHTest.test_ssh'])
    def test_custom_feature(self):
        status, output = self.target.run('my-command')
        self.assertEqual(status, 0, msg="Command failed: %s" % output)
```

---

## Image Manifest

Understanding manifests:

```bash
# Generated files
core-image-minimal-qemux86-64.manifest  # Package list
core-image-minimal-qemux86-64.rootfs-summary.txt  # Size analysis

# Content inspection
cat tmp/deploy/images/qemux86-64/*.manifest

# License manifest
tmp/deploy/licenses/core-image-minimal-qemux86-64/
```

---

## BSP Development

Machine configuration:

```bash
# conf/machine/my-board.conf
require conf/machine/include/arm/arch-armv7a.inc

MACHINE_FEATURES = "ext2 serial usbhost"
SERIAL_CONSOLES = "115200;ttyS0"

PREFERRED_PROVIDER_virtual/kernel = "linux-custom"
PREFERRED_VERSION_linux-custom = "5.15"

KERNEL_IMAGETYPE = "zImage"
KERNEL_DEVICETREE = "my-board.dtb"

IMAGE_FSTYPES = "tar.gz ext4 wic"
WKS_FILE = "my-board.wks"
```

---

## Bootloader Configuration

U-Boot integration:

```bash
# U-Boot recipe
PREFERRED_PROVIDER_virtual/bootloader = "u-boot"
PREFERRED_PROVIDER_u-boot = "u-boot-custom"

UBOOT_MACHINE = "my_board_config"
UBOOT_ENTRYPOINT = "0x80008000"
UBOOT_LOADADDRESS = "0x80008000"

# Boot script
UBOOT_ENV = "boot"
UBOOT_ENV_SUFFIX = "scr"
```

---

## Hardware Adaptation

Platform-specific configuration:

```bash
# GPIO configuration
MACHINE_FEATURES += "gpio"

# Display configuration
MACHINE_FEATURES += "screen"
DISPLAY_RESOLUTION = "1920x1080"

# Network interfaces
MACHINE_FEATURES += "wifi bluetooth"
WIFI_MODULES = "bcm4329"

# Power management
MACHINE_FEATURES += "suspend"
```

---

## Summary

Image development involves:
- Selecting appropriate base image
- Configuring features and packages
- Customizing rootfs
- Optimizing for size and security
- Testing thoroughly

Best practices:
- Start with minimal image
- Add features incrementally
- Test in QEMU first
- Document customizations
- Version control recipes
