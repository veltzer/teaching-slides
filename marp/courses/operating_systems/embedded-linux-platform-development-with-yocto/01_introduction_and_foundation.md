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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="80" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="125" y="95" text-anchor="middle" font-size="14">Manual Build</text>

  <rect x="250" y="50" width="150" height="80" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="325" y="95" text-anchor="middle" font-size="14">Build Scripts</text>

  <rect x="450" y="50" width="150" height="80" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="525" y="95" text-anchor="middle" font-size="14">Buildroot</text>

  <rect x="300" y="200" width="200" height="100" fill="#ffff99" stroke="#000" stroke-width="2"/>
  <text x="400" y="255" text-anchor="middle" font-size="16" font-weight="bold">Yocto Project</text>

  <path d="M 125 130 L 325 200" stroke="#000" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 325 130 L 400 200" stroke="#000" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 525 130 L 400 200" stroke="#000" stroke-width="2" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#000"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="300" y="50" width="200" height="60" fill="#e6f3ff" stroke="#0066cc" stroke-width="2" rx="5"/>
  <text x="400" y="85" text-anchor="middle" font-size="14" font-weight="bold">Linux Foundation</text>

  <rect x="300" y="150" width="200" height="60" fill="#fff0e6" stroke="#ff6600" stroke-width="2" rx="5"/>
  <text x="400" y="185" text-anchor="middle" font-size="14" font-weight="bold">Yocto Project</text>

  <rect x="100" y="250" width="150" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="2" rx="5"/>
  <text x="175" y="280" text-anchor="middle" font-size="12">Advisory Board</text>

  <rect x="325" y="250" width="150" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="2" rx="5"/>
  <text x="400" y="280" text-anchor="middle" font-size="12">Technical Team</text>

  <rect x="550" y="250" width="150" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="2" rx="5"/>
  <text x="625" y="280" text-anchor="middle" font-size="12">Member Orgs</text>

  <rect x="200" y="350" width="400" height="50" fill="#ffe6e6" stroke="#cc0000" stroke-width="2" rx="5"/>
  <text x="400" y="380" text-anchor="middle" font-size="12">Community Contributors</text>

  <path d="M 400 110 L 400 150" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 400 210 L 175 250" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 400 210 L 400 250" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 400 210 L 625 250" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 400 300 L 400 350" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="50" width="300" height="80" fill="#e6f3ff" stroke="#0066cc" stroke-width="2" rx="5"/>
  <text x="400" y="95" text-anchor="middle" font-size="16" font-weight="bold">Yocto Project</text>

  <rect x="100" y="200" width="150" height="60" fill="#fff0e6" stroke="#ff6600" stroke-width="2" rx="5"/>
  <text x="175" y="235" text-anchor="middle" font-size="14">Poky</text>

  <rect x="325" y="200" width="150" height="60" fill="#fff0e6" stroke="#ff6600" stroke-width="2" rx="5"/>
  <text x="400" y="235" text-anchor="middle" font-size="14">BitBake</text>

  <rect x="550" y="200" width="150" height="60" fill="#fff0e6" stroke="#ff6600" stroke-width="2" rx="5"/>
  <text x="625" y="235" text-anchor="middle" font-size="14">OpenEmbedded</text>

  <rect x="100" y="320" width="150" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="2" rx="5"/>
  <text x="175" y="350" text-anchor="middle" font-size="12">Reference Distro</text>

  <rect x="325" y="320" width="150" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="2" rx="5"/>
  <text x="400" y="350" text-anchor="middle" font-size="12">Build Engine</text>

  <rect x="550" y="320" width="150" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="2" rx="5"/>
  <text x="625" y="350" text-anchor="middle" font-size="12">Metadata</text>

  <path d="M 400 130 L 175 200" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M 400 130 L 400 200" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M 400 130 L 625 200" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M 175 260 L 175 320" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M 400 260 L 400 320" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M 625 260 L 625 320" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>

  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="300" width="600" height="60" fill="#ffe6e6" stroke="#cc0000" stroke-width="2"/>
  <text x="400" y="335" text-anchor="middle" font-size="14" font-weight="bold">Hardware Layer (BSP)</text>

  <rect x="150" y="220" width="500" height="60" fill="#e6ffe6" stroke="#00cc00" stroke-width="2"/>
  <text x="400" y="255" text-anchor="middle" font-size="14" font-weight="bold">Distribution Layer</text>

  <rect x="200" y="140" width="400" height="60" fill="#e6e6ff" stroke="#0000cc" stroke-width="2"/>
  <text x="400" y="175" text-anchor="middle" font-size="14" font-weight="bold">Application Layer</text>

  <rect x="250" y="60" width="300" height="60" fill="#ffffe6" stroke="#cccc00" stroke-width="2"/>
  <text x="400" y="95" text-anchor="middle" font-size="14" font-weight="bold">OpenEmbedded-Core</text>

  <text x="50" y="335" text-anchor="middle" font-size="12">Priority:</text>
  <text x="50" y="255" text-anchor="middle" font-size="12">7</text>
  <text x="50" y="175" text-anchor="middle" font-size="12">8</text>
  <text x="50" y="95" text-anchor="middle" font-size="12">5</text>
</svg>

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
