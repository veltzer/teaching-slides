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
# Introduction to Embedded Linux with Yocto

---

## What is Embedded Linux?

Linux operating system tailored for embedded devices:
- Resource-constrained environments
- Specific hardware platforms
- Real-time requirements
- Custom functionality

Key characteristics:
- Minimal footprint
- Cross-compilation
- Hardware-specific drivers
- Deterministic behavior

---

## Traditional Embedded Linux Development

Manual approach challenges:
- Toolchain management
- Dependency resolution
- Package compilation order
- Root filesystem creation
- Hardware adaptation

Each project starts from scratch:
- No standardization
- Limited reusability
- Maintenance burden
- Documentation gaps

---

## Build System Evolution

![build_system_evolution](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/01_introduction_and_foundation/build_system_evolution.svg)

---

## Why Yocto?

Industry standard for embedded Linux:
- Used by major semiconductor vendors
- Powers automotive systems (AGL)
- IoT and industrial applications
- Telecommunications infrastructure

Key advantages:
- Reproducible builds
- Extensive hardware support
- Active community
- Commercial backing

---

## Yocto vs Alternatives

| Aspect | Yocto | Buildroot | OpenWrt |
|--------|-------|-----------|---------|
| Learning Curve | Steep | Moderate | Easy |
| Flexibility | Very High | High | Moderate |
| Build Time | Long | Short | Short |
| Customization | Extensive | Good | Limited |
| Package Count | 10,000+ | 2,500+ | 5,000+ |
| Enterprise Use | Primary | Secondary | Rare |

---

## When to Choose Yocto

Ideal for:
- Multi-platform products
- Long product lifecycles
- Compliance requirements
- Complex customization needs
- Team collaboration

Not ideal for:
- Quick prototypes
- Simple applications
- Resource-limited teams
- One-off projects

---

## Yocto Project Governance

![yocto_project_governance](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/01_introduction_and_foundation/yocto_project_governance.svg)

---

## Industry Adoption

Automotive:
- **AGL** (Automotive Grade Linux)
- Tesla, BMW, Mercedes-Benz
- Infotainment systems
- ADAS platforms

Industrial IoT:
- Factory automation
- Smart meters
- Medical devices
- Robotics

---

## Telecommunications

5G Infrastructure:
- **O-RAN** Alliance
- Base stations
- Edge computing
- Network equipment

Consumer Electronics:
- Smart TVs
- Set-top boxes
- Home automation
- Wearables

---

## Development Environment Requirements

Hardware requirements:
- CPU: 4+ cores recommended
- RAM: 8GB minimum, 16GB+ recommended
- Storage: 100GB+ free space
- SSD strongly recommended

Software requirements:
- Linux host (Ubuntu, Fedora, Debian)
- Git, Python 3
- Development packages
- Docker (optional)

---

## Host System Setup

```bash
# Ubuntu/Debian packages
sudo apt-get install gawk wget git diffstat unzip \
    texinfo gcc build-essential chrpath socat cpio \
    python3 python3-pip python3-pexpect xz-utils \
    debianutils iputils-ping python3-git \
    python3-jinja2 libegl1-mesa libsdl1.2-dev \
    pylint xterm python3-subunit mesa-common-dev
```

---

## Storage Considerations

Build space requirements:
- Source downloads: ~10GB
- Build workspace: ~50GB per configuration
- Shared state cache: ~20GB
- Deploy images: ~5GB

Optimization tips:
- Use SSD for build directory
- NFS for shared state cache
- Separate partition for builds
- Regular cleanup scripts

---

## Container-Based Development

CROPS (Cross Platform Support):

```bash
# Pull CROPS container
docker pull crops/poky

# Run with volume mounting
docker run --rm -it \
    -v /home/user/yocto:/workdir \
    crops/poky --workdir=/workdir
```

Benefits:
- Consistent environment
- No host contamination
- Easy CI/CD integration
- Team standardization

---

## Yocto Project Components

![yocto_project_components](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/01_introduction_and_foundation/yocto_project_components.svg)

---

## Poky Reference Distribution

What is Poky?
- Reference implementation
- Starting point for custom distributions
- Includes essential metadata
- Regular release cycle

Components:
- BitBake build tool
- OpenEmbedded-Core metadata
- Reference BSPs
- Documentation

---

## OpenEmbedded-Core

Core metadata providing:
- Base recipes
- Common classes
- Configuration templates
- Standard policies

Key directories:
- `meta/` - Core layer
- `meta-poky/` - Poky-specific
- `meta-yocto-bsp/` - Reference BSPs
- `scripts/` - Helper tools

---

## BitBake Build Engine

Task scheduler and executor:
- Parses metadata
- Resolves dependencies
- Executes tasks in parallel
- Manages shared state

Similar to:
- Make (but more powerful)
- Maven/Gradle (for embedded)
- Bazel (different domain)

---

## Metadata Layers

![metadata_layers](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/01_introduction_and_foundation/metadata_layers.svg)

---

## Build Workflow Overview

1. **Configuration Phase**
    - Set machine target
    - Choose distribution
    - Configure features

1. **Parsing Phase**
    - Read all metadata
    - Resolve variables
    - Generate task graph

1. **Execution Phase**
    - Fetch sources
    - Compile packages
    - Create root filesystem
    - Generate images

---

## Project Directory Structure

```tree
yocto-project/
├── build/              # Build workspace
│   ├── conf/          # Configuration
│   ├── tmp/           # Build output
│   └── downloads/     # Source cache
├── meta/              # Core layer
├── meta-poky/         # Poky layer
├── meta-yocto-bsp/    # Reference BSPs
└── meta-custom/       # Your layers
```

---

## Initial Build Setup

```bash
# Clone Poky
git clone git://git.yoctoproject.org/poky
cd poky
git checkout -b kirkstone origin/kirkstone

# Initialize build environment
source oe-init-build-env build

# Configure local.conf
echo 'MACHINE = "qemux86-64"' >> conf/local.conf
echo 'DL_DIR = "${TOPDIR}/../downloads"' >> conf/local.conf
echo 'SSTATE_DIR = "${TOPDIR}/../sstate-cache"' >> conf/local.conf
```

---

## First Build

```bash
# Build minimal image
bitbake core-image-minimal

# Run in QEMU
runqemu qemux86-64 core-image-minimal

# Image location
ls tmp/deploy/images/qemux86-64/
```

Build time expectations:
- First build: 1-3 hours
- Subsequent builds: 10-30 minutes
- Depends on hardware and network

---

## Understanding Build Output

Key directories:
- `tmp/deploy/images/` - Final images
- `tmp/deploy/rpm/` - Package feed
- `tmp/work/` - Build workspace
- `tmp/sysroots/` - Cross-compilation roots

Important files:
- `*.wic` - Disk images
- `*.tar.gz` - Root filesystems
- `*.manifest` - Package lists
- `bzImage` - Kernel image

---

## Build Configuration Files

`conf/local.conf`:

```bash
# Machine selection
MACHINE ?= "qemux86-64"

# Parallel execution
BB_NUMBER_THREADS = "8"
PARALLEL_MAKE = "-j 8"

# Package management
PACKAGE_CLASSES = "package_rpm"

# Features
EXTRA_IMAGE_FEATURES = "debug-tweaks"
```

---

## Layer Configuration

`conf/bblayers.conf`:

```bash
BBLAYERS ?= " \
  /path/to/poky/meta \
  /path/to/poky/meta-poky \
  /path/to/poky/meta-yocto-bsp \
  /path/to/meta-openembedded/meta-oe \
  /path/to/meta-custom \
  "
```

Layer management:

```bash
bitbake-layers show-layers
bitbake-layers add-layer ../meta-custom
```

---

## Common Build Commands

```bash
# Build specific recipe
bitbake virtual/kernel

# Clean recipe
bitbake -c clean busybox

# Rebuild from scratch
bitbake -c cleansstate core-image-minimal
bitbake core-image-minimal

# List tasks
bitbake -c listtasks core-image-minimal
```

---

## Troubleshooting Basics

Common issues:
- Disk space exhaustion
- Network timeouts
- Missing dependencies
- Configuration conflicts

Debug commands:

```bash
# Check environment
bitbake -e recipe | grep VARIABLE

# Dependency graph
bitbake -g core-image-minimal
```

---

## Performance Tips

Hardware optimization:
- Use SSD for build directory
- Maximize RAM allocation
- Enable CPU scaling
- Dedicated build machine

Configuration optimization:
- Shared state cache
- Download mirrors
- Parallel builds
- `rm_work` class

---

## Development Best Practices

1. **Version Control**
    - Track your layers
    - Tag releases
    - Document changes

1. **Layer Organization**
    - Logical separation
    - Clear naming
    - Minimal dependencies

1. **Build Automation**
    - CI/CD integration
    - Nightly builds
    - Automated testing

---

## Team Collaboration

Shared resources:
- Centralized downloads
- Network sstate cache
- Package feeds
- Documentation wiki

Communication:
- Layer maintainers
- Code reviews
- Build status
- Issue tracking

---

## Security Considerations

Build security:
- Trusted sources
- GPG verification
- CVE monitoring
- License compliance

Runtime security:
- Minimal attack surface
- Security features
- Update mechanism
- Secure boot

---

## License Management

Track licenses:

```bash
# Generate license manifest
bitbake -c populate_lic core-image-minimal

# Check specific package
bitbake -e busybox | grep ^LICENSE=
```

Compliance:
- GPL requirements
- Commercial licenses
- Export restrictions
- Attribution

---

## Documentation Resources

Official documentation:
- Yocto Project Manual
- BitBake User Manual
- Kernel Development Manual
- BSP Developer's Guide

Community resources:
- Mailing lists
- IRC channels
- Stack Overflow
- Training materials

---

## Getting Help

Where to ask:
- `yocto@lists.yoctoproject.org`
- `#yocto` on IRC
- Vendor support forums
- Commercial support

How to ask:
- Provide build configuration
- Include error logs
- Describe expected behavior
- List troubleshooting steps

---

## Summary

Key takeaways:
- Yocto provides structured embedded Linux development
- Industry-standard solution with broad adoption
- Steep learning curve but powerful capabilities
- Strong ecosystem and community support

Next steps:
- Set up development environment
- Complete first build
- Explore core concepts
- Start customization
