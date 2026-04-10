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

![bitbake_architecture](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/03_bitbake_deep_dive/bitbake_architecture.svg)

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

## BitBake Variable Precedence

![bitbake_variable_precedence](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/03_bitbake_deep_dive/bitbake_variable_precedence.svg)

---

## Overrides System

![overrides_system](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/03_bitbake_deep_dive/overrides_system.svg)

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

![task_dependencies](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/03_bitbake_deep_dive/task_dependencies.svg)

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

![hash_calculation](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/03_bitbake_deep_dive/hash_calculation.svg)

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
