# BitBake Deep Dive

---

## What is BitBake?

Generic task execution engine:
- Processes metadata
- Manages dependencies
- Executes tasks in parallel
- Handles caching

Originally from OpenEmbedded:
- Inspired by Portage (Gentoo)
- Python-based implementation
- Domain-specific language
- Extensible architecture

---

## BitBake Architecture

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="400" fill="#f5f5f5" stroke="#333" stroke-width="2"/>

  <rect x="150" y="100" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="1"/>
  <text x="225" y="135" text-anchor="middle" font-size="12">Parser</text>

  <rect x="350" y="100" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="1"/>
  <text x="425" y="135" text-anchor="middle" font-size="12">Cache</text>

  <rect x="550" y="100" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="1"/>
  <text x="625" y="135" text-anchor="middle" font-size="12">Scheduler</text>

  <rect x="150" y="250" width="150" height="60" fill="#ffeecc" stroke="#000" stroke-width="1"/>
  <text x="225" y="285" text-anchor="middle" font-size="12">Data Store</text>

  <rect x="350" y="250" width="150" height="60" fill="#eeccff" stroke="#000" stroke-width="1"/>
  <text x="425" y="285" text-anchor="middle" font-size="12">Fetcher</text>

  <rect x="550" y="250" width="150" height="60" fill="#ccffff" stroke="#000" stroke-width="1"/>
  <text x="625" y="285" text-anchor="middle" font-size="12">Task Executor</text>

  <text x="400" y="380" text-anchor="middle" font-size="14" font-weight="bold">BitBake Core</text>
</svg>

---

## Recipe Anatomy

Basic recipe structure:
```bash
SUMMARY = "Short description"
DESCRIPTION = "Longer description of the package"
HOMEPAGE = "https://example.com"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=..."

SRC_URI = "https://example.com/app-${PV}.tar.gz"
SRC_URI[md5sum] = "abc123..."
SRC_URI[sha256sum] = "def456..."

inherit autotools

DEPENDS = "zlib openssl"
RDEPENDS_${PN} = "bash"
```

---

## Variable Types

```bash
# Simple assignment
VAR = "value"

# Weak assignment (default value)
VAR ?= "default"

# Weak weak assignment (weaker than ?)
VAR ??= "weakest"

# Immediate expansion
VAR := "${OTHER_VAR}"

# Append
VAR += "additional"
VAR_append = " more"

# Prepend
VAR =+ "before "
VAR_prepend = "prefix "

# Remove
VAR_remove = "unwanted"
```

---

## Variable Expansion

```bash
# Basic expansion
PATH = "/usr/bin"
FULL_PATH = "${PATH}:/usr/local/bin"

# Python expressions
PV = "1.2.3"
MAJOR = "${@d.getVar('PV').split('.')[0]}"

# Conditional expansion
VAR = "${@'yes' if d.getVar('ENABLE_FEATURE') == '1' else 'no'}"

# Shell functions
VAR = "${@os.path.basename(d.getVar('SRC_URI').split()[0])}"
```

---

## Overrides System

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="50" width="400" height="60" fill="#e6f3ff" stroke="#0066cc" stroke-width="2"/>
  <text x="400" y="85" text-anchor="middle" font-size="14" font-weight="bold">VAR = "default"</text>

  <rect x="100" y="150" width="200" height="50" fill="#fff0e6" stroke="#ff6600" stroke-width="1"/>
  <text x="200" y="180" text-anchor="middle" font-size="12">VAR_arm = "arm-value"</text>

  <rect x="350" y="150" width="200" height="50" fill="#fff0e6" stroke="#ff6600" stroke-width="1"/>
  <text x="450" y="180" text-anchor="middle" font-size="12">VAR_x86 = "x86-value"</text>

  <rect x="100" y="250" width="200" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="1"/>
  <text x="200" y="280" text-anchor="middle" font-size="12">VAR_append_arm = " extra"</text>

  <rect x="350" y="250" width="200" height="50" fill="#e6ffe6" stroke="#00cc00" stroke-width="1"/>
  <text x="450" y="280" text-anchor="middle" font-size="12">VAR_class-native = "native"</text>

  <text x="650" y="180" text-anchor="middle" font-size="11">Machine overrides</text>
  <text x="650" y="280" text-anchor="middle" font-size="11">Class overrides</text>
</svg>

---

## OVERRIDES Variable

Override chain:

```bash
# Default overrides
OVERRIDES = "linux:x86-64:intel-corei7-64:machine:pn-recipe"

# Custom overrides
MACHINEOVERRIDES = "x86:x86-64:intel-corei7-64"
DISTROOVERRIDES = "poky"
CLASSOVERRIDE = "class-target"

# Applied in order (last wins)
VAR = "base"
VAR_x86 = "x86 specific"
VAR_x86-64 = "x86-64 specific"  # This wins for x86-64
```

---

## Conditional Syntax

```bash
# Python conditionals
python () {
    if d.getVar('DISTRO') == 'poky':
        d.setVar('EXTRA_OECONF', '--enable-poky')

    machine = d.getVar('MACHINE')
    if machine.startswith('qemu'):
        d.appendVar('IMAGE_FEATURES', ' debug-tweaks')
}

# Inline Python
KERNEL_FEATURES_append = "${@bb.utils.contains('DISTRO_FEATURES', 'systemd', ' cfg/systemd', '', d)}"
```

---

## Tasks Definition

```bash
# Shell task
do_compile() {
    oe_runmake
}

# Python task
python do_custom() {
    bb.note("Executing custom task")
    src = d.getVar('S')
    bb.utils.mkdirhier(d.getVar('B'))
}

# Task flags
do_compile[dirs] = "${B}"
do_compile[depends] = "virtual/kernel:do_populate_sysroot"
do_compile[nostamp] = "1"
do_compile[network] = "1"
```

---

## Task Dependencies

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="120" height="50" fill="#ffcccc" stroke="#000" stroke-width="1"/>
  <text x="160" y="130" text-anchor="middle" font-size="12">do_fetch</text>

  <rect x="300" y="100" width="120" height="50" fill="#ccffcc" stroke="#000" stroke-width="1"/>
  <text x="360" y="130" text-anchor="middle" font-size="12">do_unpack</text>

  <rect x="500" y="100" width="120" height="50" fill="#ccccff" stroke="#000" stroke-width="1"/>
  <text x="560" y="130" text-anchor="middle" font-size="12">do_configure</text>

  <rect x="300" y="250" width="120" height="50" fill="#ffeecc" stroke="#000" stroke-width="1"/>
  <text x="360" y="280" text-anchor="middle" font-size="12">do_compile</text>

  <path d="M 220 125 L 300 125" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="260" y="115" text-anchor="middle" font-size="10">depends</text>

  <path d="M 360 150 L 360 250" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="380" y="200" text-anchor="middle" font-size="10">deptask</text>

  <path d="M 420 125 L 500 125" stroke="#0066cc" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="460" y="115" text-anchor="middle" font-size="10">rdeptask</text>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Task Flags

Common task flags:

```bash
# Directory setup
do_compile[dirs] = "${B} ${S}"

# Dependencies
do_compile[depends] = "recipe:do_task"
do_compile[deptask] = "do_populate_sysroot"
do_compile[rdeptask] = "do_package_write"

# Execution control
do_compile[nostamp] = "1"       # Always run
do_compile[noexec] = "1"        # Skip execution
do_compile[network] = "1"       # Allow network access
do_compile[fakeroot] = "1"      # Run under fakeroot
```

---

## Class System

```bash
# Base class inheritance
inherit base

# Multiple inheritance
inherit autotools pkgconfig

# Conditional inheritance
inherit ${@bb.utils.contains('PACKAGECONFIG', 'systemd', 'systemd', '', d)}

# Class implementation (classes/example.bbclass)
EXPORT_FUNCTIONS do_configure do_compile

python example_do_configure() {
    bb.build.exec_func('base_do_configure', d)
    # Additional configuration
}

example_do_compile() {
    oe_runmake
}
```

---

## Common Classes

Build systems:
- `autotools` - ./configure && make
- `cmake` - CMake projects
- `meson` - Meson build
- `setuptools3` - Python packages

Packaging:
- `package` - Package splitting
- `package_rpm/deb/ipk` - Package formats
- `packagegroup` - Package collections

Utilities:
- `pkgconfig` - pkg-config support
- `gettext` - Internationalization
- `update-rc.d` - Init scripts

---

## Fetcher System

```bash
# Git repository
SRC_URI = "git://github.com/project/repo.git;protocol=https;branch=main"
SRCREV = "${AUTOREV}"

# HTTP/HTTPS
SRC_URI = "https://example.com/file-${PV}.tar.gz"

# Local files
SRC_URI = "file://patch.diff \
           file://config.conf"

# Multiple sources
SRC_URI = "https://example.com/main.tar.gz \
           git://github.com/deps/lib.git;destsuffix=git/lib;name=lib"

SRCREV_lib = "abc123"
```

---

## Fetcher Features

Advanced options:

```bash
# Shallow clones
BB_GIT_SHALLOW = "1"
BB_GIT_SHALLOW_DEPTH = "1"

# Download directory
DL_DIR ?= "${TOPDIR}/downloads"

# Premirrors
PREMIRRORS_prepend = "\
    git://.*/.* file://${TOPDIR}/local-mirror/ \n \
    https://.*/.* file://${TOPDIR}/local-mirror/ \n \
"

# Fetch restrictions
BB_NO_NETWORK = "1"
BB_ALLOWED_NETWORKS = "*.example.com"
```

---

## Events System

```bash
# Event handlers
addhandler myhandler
myhandler[eventmask] = "bb.event.BuildStarted bb.event.BuildCompleted"

python myhandler() {
    if isinstance(e, bb.event.BuildStarted):
        bb.note("Build started at %s" % time.strftime('%Y%m%d-%H%M%S'))
    elif isinstance(e, bb.event.BuildCompleted):
        bb.note("Build completed")
}

# Common events
# bb.event.ParseStarted/Completed
# bb.event.BuildStarted/Completed
# bb.event.TaskStarted/Succeeded/Failed
# bb.event.RecipeParsed
```

---

## Data Store API

```python
# Python API
python do_example() {
    # Get variables
    value = d.getVar('VARIABLE')
    expanded = d.getVar('VARIABLE', True)

    # Set variables
    d.setVar('VARIABLE', 'value')
    d.appendVar('VARIABLE', ' extra')
    d.prependVar('VARIABLE', 'prefix ')

    # Delete variables
    d.delVar('VARIABLE')

    # Expand expressions
    result = d.expand('${VARIABLE}')
}
```

---

## BitBake Command Line

Basic commands:

```bash
# Parse metadata
bitbake -p

# Build target
bitbake core-image-minimal

# Specific task
bitbake -c compile busybox

# Force rebuild
bitbake -f -c compile busybox

# Clean
bitbake -c clean busybox
bitbake -c cleansstate busybox
```

---

## Environment Inspection

```bash
# Show environment
bitbake -e recipe > environment.txt

# Show specific variable
bitbake -e recipe | grep ^VARIABLE=

# Show variable history
bitbake -e recipe | grep -A20 "^# \$VARIABLE"

# Interactive shell
bitbake -c devshell recipe

# Python shell
bitbake -c devpyshell recipe
```

---

## Dependency Graphs

```bash
# Generate dependency graphs
bitbake -g core-image-minimal

# Output files:
# task-depends.dot - Task dependencies
# recipe-depends.dot - Recipe dependencies
# pn-buildlist - Build order

# Visualize with graphviz
dot -Tpdf task-depends.dot -o task-depends.pdf

# Simplified graphs
bitbake -g -u taskexp core-image-minimal
```

---

## Debugging BitBake

```bash
# Debug output levels
bitbake -D recipe      # Debug
bitbake -DD recipe     # Debug + verbose
bitbake -DDD recipe    # Maximum verbosity

# Verbose output
bitbake -v recipe

# Dry run
bitbake -n recipe

# Show versions
bitbake -s

# List tasks
bitbake -c listtasks recipe
```

---

## bitbake-layers Tool

```bash
# Show layers
bitbake-layers show-layers

# Add layer
bitbake-layers add-layer ../meta-custom

# Remove layer
bitbake-layers remove-layer meta-custom

# Show overlayed recipes
bitbake-layers show-overlayed

# Show recipes
bitbake-layers show-recipes

# Create layer
bitbake-layers create-layer meta-new
```

---

## Cache Management

Cache types:

```bash
# Parse cache
cache/

# Shared state
sstate-cache/

# Persistent data
persistent/

# Clear cache
bitbake -c cleanall recipe

# Invalidate cache
touch conf/local.conf
```

---

## Shared State Mechanism

```bash
# Sstate configuration
SSTATE_DIR ?= "${TOPDIR}/sstate-cache"

# Sstate mirrors
SSTATE_MIRRORS = "\
    file://.* http://sstate.example.com/PATH;downloadfilename=PATH \
"

# Hash equivalence
BB_HASHSERVE = "auto"
BB_HASHSERVE_UPSTREAM = "hashserv.yoctoproject.org:8687"

# Signature handler
BB_SIGNATURE_HANDLER = "OEEquivHash"
```

---

## Hash Calculation

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="300" fill="#f5f5f5" stroke="#333" stroke-width="2"/>

  <rect x="150" y="100" width="150" height="40" fill="#ffcccc" stroke="#000" stroke-width="1"/>
  <text x="225" y="125" text-anchor="middle" font-size="12">Recipe Variables</text>

  <rect x="150" y="160" width="150" height="40" fill="#ccffcc" stroke="#000" stroke-width="1"/>
  <text x="225" y="185" text-anchor="middle" font-size="12">Task Code</text>

  <rect x="150" y="220" width="150" height="40" fill="#ccccff" stroke="#000" stroke-width="1"/>
  <text x="225" y="245" text-anchor="middle" font-size="12">Dependencies</text>

  <rect x="400" y="160" width="100" height="40" fill="#ffeecc" stroke="#000" stroke-width="2"/>
  <text x="450" y="185" text-anchor="middle" font-size="12" font-weight="bold">HASH</text>

  <rect x="550" y="160" width="120" height="40" fill="#eeccff" stroke="#000" stroke-width="1"/>
  <text x="610" y="185" text-anchor="middle" font-size="12">Sstate Cache</text>

  <path d="M 300 120 L 400 180" stroke="#333" stroke-width="1" marker-end="url(#arr)"/>
  <path d="M 300 185 L 400 180" stroke="#333" stroke-width="1" marker-end="url(#arr)"/>
  <path d="M 300 240 L 400 180" stroke="#333" stroke-width="1" marker-end="url(#arr)"/>
  <path d="M 500 180 L 550 180" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>

  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Parallel Execution

Configuration:

```bash
# Number of BitBake threads
BB_NUMBER_THREADS = "16"

# Make parallelism
PARALLEL_MAKE = "-j 16"

# Limit parallel tasks per recipe
BB_NUMBER_PARSE_THREADS = "8"

# CPU pressure regulation
BB_PRESSURE_MAX_CPU = "1000"
BB_PRESSURE_MAX_IO = "1000"
BB_PRESSURE_MAX_MEMORY = "1000"
```

---

## Network Configuration

```bash
# Proxy settings
export http_proxy="http://proxy.example.com:8080"
export https_proxy="http://proxy.example.com:8080"
export no_proxy="localhost,127.0.0.1"

# In configuration
ENV_PROXY_SETTINGS = "http_proxy https_proxy no_proxy"

# Git proxy
GIT_PROXY_COMMAND = "oe-git-proxy"

# Network access control
BB_NO_NETWORK = "0"
BB_ALLOWED_NETWORKS = "*.yoctoproject.org"
```

---

## Error Handling

```bash
# Error reporting
ERR_REPORT_DIR = "${LOG_DIR}/error-report"

# Abort on errors
BB_DISKMON_DIRS = "\
    STOPTASKS,${TMPDIR},1G,100K \
    STOPTASKS,${DL_DIR},1G,100K \
    STOPTASKS,${SSTATE_DIR},1G,100K \
    STOPTASKS,/tmp,100M,100K \
    ABORT,${TMPDIR},100M,1K \
    ABORT,${DL_DIR},100M,1K \
"
```

---

## Performance Monitoring

```bash
# Build statistics
INHERIT += "buildstats"
BUILDSTATS_BASE = "${TMPDIR}/buildstats/"

# Build history
INHERIT += "buildhistory"
BUILDHISTORY_DIR = "${TOPDIR}/buildhistory"
BUILDHISTORY_COMMIT = "1"

# Profile data
BB_GENERATE_MIRROR_TARBALLS = "1"
```

---

## Custom Variables

```bash
# Define custom variables
MY_CUSTOM_VAR = "value"
MY_CUSTOM_VAR[doc] = "Documentation for the variable"

# Export to tasks
export MY_CUSTOM_VAR

# Use in recipes
inherit mylayer

EXTRA_OECONF_append = " ${@bb.utils.contains('MY_CUSTOM_VAR', 'value', '--enable-feature', '', d)}"
```

---

## Include Mechanism

```bash
# Include files
include another.inc

# Require files (error if not found)
require required.inc

# Conditional include
include ${@bb.utils.contains('DISTRO', 'poky', 'poky.inc', 'default.inc', d)}

# Layer includes
require recipes-core/base/base_${PV}.inc
```

---

## BBMASK

Exclude recipes:

```bash
# Mask specific recipes
BBMASK = "meta-custom/recipes-broken/"

# Multiple patterns
BBMASK += "|meta-other/recipes-.*/broken.*.bb"

# Exclude versions
BBMASK += "|.*_git.bb"
```

---

## Summary

BitBake mastery requires understanding:
- Variable expansion and overrides
- Task system and dependencies
- Class inheritance
- Fetcher capabilities
- Event handling
- Debugging techniques

Key concepts:
- Everything is metadata
- Tasks execute in dependency order
- Hashing enables caching
- Parallelism speeds builds
