# Development Workflow and Tools

---

## Development Workflow Overview

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="175" y="85" text-anchor="middle" font-size="12">Plan & Design</text>

  <rect x="325" y="50" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="400" y="85" text-anchor="middle" font-size="12">Develop</text>

  <rect x="550" y="50" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="625" y="85" text-anchor="middle" font-size="12">Build & Test</text>

  <rect x="100" y="200" width="150" height="60" fill="#ffeecc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="175" y="235" text-anchor="middle" font-size="12">Debug</text>

  <rect x="325" y="200" width="150" height="60" fill="#eeccff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="400" y="235" text-anchor="middle" font-size="12">Optimize</text>

  <rect x="550" y="200" width="150" height="60" fill="#ccffff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="625" y="235" text-anchor="middle" font-size="12">Deploy</text>

  <rect x="300" y="350" width="200" height="60" fill="#e6ffe6" stroke="#00cc00" stroke-width="3" rx="5"/>
  <text x="400" y="385" text-anchor="middle" font-size="14" font-weight="bold">Iterate</text>

  <path d="M 250 80 L 325 80" stroke="#333" stroke-width="2" marker-end="url(#w1)"/>
  <path d="M 475 80 L 550 80" stroke="#333" stroke-width="2" marker-end="url(#w1)"/>
  <path d="M 625 110 L 175 200" stroke="#333" stroke-width="2" marker-end="url(#w1)"/>
  <path d="M 250 235 L 325 235" stroke="#333" stroke-width="2" marker-end="url(#w1)"/>
  <path d="M 475 235 L 550 235" stroke="#333" stroke-width="2" marker-end="url(#w1)"/>
  <path d="M 625 260 L 400 350" stroke="#333" stroke-width="2" marker-end="url(#w1)"/>
  <path d="M 300 380 L 175 110" stroke="#0066cc" stroke-width="2" marker-end="url(#w1)" stroke-dasharray="5,5"/>

  <defs>
    <marker id="w1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## devtool Overview

Primary development tool for Yocto:
- Recipe creation
- Source modification
- Dependency tracking
- Recipe upgrading
- SDK workflow

Workspace concept:

```txt
workspace/
├── conf/
│   └── layer.conf
├── appends/
│   └── recipe_%.bbappend
├── recipes/
│   └── new-recipe/
└── sources/
    └── recipe-name/
```

---

## devtool Commands

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="300" y="50" width="200" height="60" fill="#ffcccc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="400" y="85" text-anchor="middle" font-size="13" font-weight="bold">devtool</text>

  <rect x="100" y="170" width="140" height="50" fill="#ccffcc" stroke="#000" stroke-width="2" rx="3"/>
  <text x="170" y="200" text-anchor="middle" font-size="11">add</text>

  <rect x="260" y="170" width="140" height="50" fill="#ccffcc" stroke="#000" stroke-width="2" rx="3"/>
  <text x="330" y="200" text-anchor="middle" font-size="11">modify</text>

  <rect x="420" y="170" width="140" height="50" fill="#ccffcc" stroke="#000" stroke-width="2" rx="3"/>
  <text x="490" y="200" text-anchor="middle" font-size="11">upgrade</text>

  <rect x="580" y="170" width="140" height="50" fill="#ccffcc" stroke="#000" stroke-width="2" rx="3"/>
  <text x="650" y="200" text-anchor="middle" font-size="11">finish</text>

  <rect x="180" y="280" width="140" height="50" fill="#ccccff" stroke="#000" stroke-width="2" rx="3"/>
  <text x="250" y="310" text-anchor="middle" font-size="11">build</text>

  <rect x="340" y="280" width="140" height="50" fill="#ccccff" stroke="#000" stroke-width="2" rx="3"/>
  <text x="410" y="310" text-anchor="middle" font-size="11">deploy</text>

  <rect x="500" y="280" width="140" height="50" fill="#ccccff" stroke="#000" stroke-width="2" rx="3"/>
  <text x="570" y="310" text-anchor="middle" font-size="11">reset</text>

  <path d="M 350 110 L 170 170" stroke="#333" stroke-width="1.5" marker-end="url(#w2)"/>
  <path d="M 380 110 L 330 170" stroke="#333" stroke-width="1.5" marker-end="url(#w2)"/>
  <path d="M 420 110 L 490 170" stroke="#333" stroke-width="1.5" marker-end="url(#w2)"/>
  <path d="M 450 110 L 650 170" stroke="#333" stroke-width="1.5" marker-end="url(#w2)"/>

  <defs>
    <marker id="w2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Creating New Recipes with devtool

From Git repository:

```bash
# Create recipe from Git
devtool add myapp https://github.com/user/myapp.git

# Specify branch
devtool add myapp https://github.com/user/myapp.git -a main

# From local source
devtool add myapp /path/to/source

# Fetch only (no build)
devtool add --fetch myapp https://github.com/user/myapp.git
```

Generated recipe location:

```bash
workspace/recipes/myapp/myapp_git.bb
```

---

## Modifying Existing Recipes

Extract and modify:

```bash
# Extract source for modification
devtool modify busybox

# Source location
cd workspace/sources/busybox

# Make changes
vim lib/parse.c
git add lib/parse.c
git commit -m "Fix parsing bug"

# Build modified recipe
devtool build busybox

# Deploy to target
devtool deploy-target busybox root@192.168.1.100
```

---

## devtool Workflow

```bash
# 1. Create workspace (if not exists)
devtool create-workspace

# 2. Modify recipe
devtool modify busybox

# 3. Make changes
cd workspace/sources/busybox
# ... edit files ...
git add .
git commit -m "Changes"

# 4. Build
devtool build busybox

# 5. Test on target
devtool deploy-target busybox root@target-ip

# 6. Update recipe
devtool update-recipe busybox

# 7. Finish and commit
devtool finish busybox meta-custom
```

---

## Recipe Upgrading

```bash
# Upgrade to newer version
devtool upgrade busybox -V 1.36.0

# Automatic version detection
devtool latest-version busybox

# Check what needs upgrading
devtool check-upgrade-status

# After manual fixes
devtool update-recipe busybox

# Complete upgrade
devtool finish busybox meta-custom
```

---

## Building and Testing

```bash
# Build recipe
devtool build myapp

# Build specific task
devtool build myapp:do_compile

# Clean build
devtool build myapp -c clean

# Run QA checks
devtool build myapp -c qa_check

# Build and create package
devtool build myapp && devtool package myapp
```

---

## Deploying to Target

```bash
# Deploy to running target
devtool deploy-target myapp root@192.168.1.100

# Undeploy from target
devtool undeploy-target myapp root@192.168.1.100

# Deploy with SSH options
devtool deploy-target myapp root@target -p 2222

# Deploy specific packages
devtool deploy-target myapp root@target --package myapp-dev
```

---

## Development Shell

Interactive development environment:

```bash
# Open development shell
bitbake -c devshell myapp

# Inside devshell
./configure --prefix=/usr
make
make install DESTDIR=$D

# With Python environment
bitbake -c devpyshell myapp
```

Environment in devshell:

```bash
echo $CC        # Cross compiler
echo $CFLAGS    # Compiler flags
echo $S         # Source directory
echo $B         # Build directory
echo $D         # Destination directory
```

---

## Interactive Python Shell

```bash
# Open Python shell
bitbake -c devpyshell myapp

# Inside devpyshell
>>> d.getVar('PN')
'myapp'
>>> d.getVar('DEPENDS')
'zlib openssl'

# Execute task
>>> bb.build.exec_func('do_compile', d)

# Modify variables
>>> d.setVar('MY_VAR', 'value')
```

---

## QEMU Testing

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="200" height="80" fill="#ffcccc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="200" y="135" text-anchor="middle" font-size="13" font-weight="bold">Host System</text>
  <text x="200" y="155" text-anchor="middle" font-size="11">Development</text>

  <rect x="500" y="100" width="200" height="80" fill="#ccffcc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="600" y="135" text-anchor="middle" font-size="13" font-weight="bold">QEMU Emulator</text>
  <text x="600" y="155" text-anchor="middle" font-size="11">Target Testing</text>

  <rect x="500" y="250" width="200" height="80" fill="#ccccff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="600" y="285" text-anchor="middle" font-size="13" font-weight="bold">Virtual Hardware</text>
  <text x="600" y="305" text-anchor="middle" font-size="11">ARM/x86/etc</text>

  <path d="M 300 140 L 500 140" stroke="#0066cc" stroke-width="2" marker-end="url(#w3)"/>
  <text x="400" y="130" text-anchor="middle" font-size="10">Deploy</text>

  <path d="M 600 180 L 600 250" stroke="#333" stroke-width="2" marker-end="url(#w3)"/>
  <text x="650" y="220" text-anchor="middle" font-size="10">Emulates</text>

  <defs>
    <marker id="w3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Running QEMU

Basic QEMU usage:

```bash
# Build image
bitbake core-image-minimal

# Run with runqemu
runqemu qemux86-64

# Run with network
runqemu qemux86-64 nographic slirp

# Run with serial console
runqemu qemux86-64 serial

# Custom kernel
runqemu qemux86-64 kernel=bzImage

# With KVM acceleration
runqemu qemux86-64 kvm
```

---

## QEMU Configuration

Advanced options:

```bash
# More memory
runqemu qemux86-64 qemuparams="-m 2048"

# More CPUs
runqemu qemux86-64 qemuparams="-smp 4"

# Port forwarding
runqemu qemux86-64 qemuparams="-device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::2222-:22"

# Shared directory
runqemu qemux86-64 qemuparams="-virtfs local,path=/host/path,mount_tag=host0,security_model=mapped,id=host0"
```

QEMU script wrapper:

```bash
#!/bin/bash
runqemu qemux86-64 nographic \
    qemuparams="-m 2048 -smp 4 -device e1000,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::2222-:22"
```

---

## SDK Generation

```bash
# Build SDK
bitbake -c populate_sdk core-image-minimal

# SDK location
tmp/deploy/sdk/poky-glibc-x86_64-core-image-minimal-cortexa9hf-neon-toolchain-3.1.sh

# Install SDK
./poky-glibc-x86_64-core-image-minimal-cortexa9hf-neon-toolchain-3.1.sh

# Default install location
/opt/poky/3.1

# Custom location
./sdk-installer.sh -d /home/user/sdk
```

---

## Using the SDK

Setup environment:

```bash
# Source environment
source /opt/poky/3.1/environment-setup-cortexa9hf-neon-poky-linux-gnueabi

# Verify
echo $CC
echo $CXX
echo $CFLAGS

# Compile application
$CC hello.c -o hello

# Check binary
file hello
```

SDK development:

```bash
# CMake project
cmake -DCMAKE_TOOLCHAIN_FILE=$OECORE_NATIVE_SYSROOT/usr/share/cmake/OEToolchainConfig.cmake ..
make

# Autotools project
./configure $CONFIGURE_FLAGS
make
```

---

## Extensible SDK (eSDK)

```bash
# Build eSDK
bitbake -c populate_sdk_ext core-image-minimal

# Install eSDK
./poky-glibc-x86_64-core-image-minimal-cortexa9hf-neon-toolchain-ext-3.1.sh

# Source environment
source /opt/poky/3.1/environment-setup-cortexa9hf-neon-poky-linux-gnueabi

# Use devtool in SDK
devtool add myapp https://github.com/user/myapp.git
devtool build myapp
```

eSDK advantages:
- Full BitBake environment
- Recipe development
- On-target testing
- Minimal host requirements

---

## Remote Debugging with GDB

Setup:

```bash
# On target (QEMU or hardware)
gdbserver :2345 /usr/bin/myapp

# On host with SDK
source environment-setup-cortexa9hf-neon-poky-linux-gnueabi
$GDB /path/to/myapp

# In GDB
(gdb) target remote target-ip:2345
(gdb) break main
(gdb) continue
(gdb) step
(gdb) print variable
(gdb) backtrace
```

---

## GDB Configuration

`.gdbinit`:

```bash
set sysroot /opt/poky/3.1/sysroots/cortexa9hf-neon-poky-linux-gnueabi
set substitute-path /usr/src/debug /opt/poky/3.1/sysroots/cortexa9hf-neon-poky-linux-gnueabi/usr/src/debug

# Auto-load safe path
add-auto-load-safe-path /opt/poky/3.1
```

Debug symbols:

```bash
# Include debug symbols in image
EXTRA_IMAGE_FEATURES += "dbg-pkgs"

# Per-package debug
IMAGE_INSTALL_append = " myapp-dbg"
```

---

## Performance Analysis

Profiling with perf:

```bash
# Add to image
IMAGE_INSTALL_append = " perf"

# On target
perf record -g ./myapp
perf report

# CPU profiling
perf stat ./myapp

# System-wide profiling
perf record -a -g sleep 10
perf report
```

---

## Application Tracing

Using strace:

```bash
# Add to image
IMAGE_INSTALL_append = " strace"

# On target
strace -o trace.log ./myapp
strace -e open,read,write ./myapp
strace -f ./myapp  # Follow forks
```

Using ltrace:

```bash
IMAGE_INSTALL_append = " ltrace"

# Trace library calls
ltrace ./myapp
ltrace -c ./myapp  # Summary
```

---

## System Profiling Tools

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="140" height="60" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="170" y="135" text-anchor="middle" font-size="12">perf</text>

  <rect x="260" y="100" width="140" height="60" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="330" y="135" text-anchor="middle" font-size="12">strace</text>

  <rect x="420" y="100" width="140" height="60" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="490" y="135" text-anchor="middle" font-size="12">ltrace</text>

  <rect x="580" y="100" width="140" height="60" fill="#ffeecc" stroke="#000" stroke-width="2"/>
  <text x="650" y="135" text-anchor="middle" font-size="12">valgrind</text>

  <rect x="300" y="250" width="200" height="80" fill="#ffffcc" stroke="#000" stroke-width="3"/>
  <text x="400" y="285" text-anchor="middle" font-size="14" font-weight="bold">Analysis Results</text>

  <path d="M 170 160 L 350 250" stroke="#333" stroke-width="1.5" marker-end="url(#w4)"/>
  <path d="M 330 160 L 380 250" stroke="#333" stroke-width="1.5" marker-end="url(#w4)"/>
  <path d="M 490 160 L 420 250" stroke="#333" stroke-width="1.5" marker-end="url(#w4)"/>
  <path d="M 650 160 L 450 250" stroke="#333" stroke-width="1.5" marker-end="url(#w4)"/>

  <defs>
    <marker id="w4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Memory Leak Detection

Valgrind:

```bash
# Add to image (large!)
IMAGE_INSTALL_append = " valgrind"

# Memory leak check
valgrind --leak-check=full ./myapp

# Detailed analysis
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./myapp

# Generate suppression file
valgrind --gen-suppressions=all ./myapp
```

---

## Log Management

systemd journal:

```bash
# View logs
journalctl -u myservice

# Follow logs
journalctl -u myservice -f

# Boot logs
journalctl -b

# Kernel messages
journalctl -k

# Priority filtering
journalctl -p err
```

Traditional syslog:

```bash
# Add syslog
IMAGE_INSTALL_append = " sysklogd"

# View logs
tail -f /var/log/messages
```

---

## Source Code Navigation

Using cscope:

```bash
# Generate cscope database
bitbake -c devshell linux-yocto
cscope -Rb

# In vim
:cs add cscope.out
:cs find g function_name
:cs find c function_name
```

Using ctags:

```bash
# Generate tags
ctags -R .

# In vim
:tag function_name
Ctrl-]  # Jump to definition
Ctrl-T  # Jump back
```

---

## Version Control Integration

Git workflow:

```bash
# Layer repository
meta-custom/
├── .git/
├── conf/
├── recipes-*/
└── README.md

# Commit recipe changes
git add recipes-apps/myapp/myapp_1.0.bb
git commit -m "Add myapp recipe"

# Tag releases
git tag -a v1.0 -m "Release 1.0"

# Branch for features
git checkout -b feature/new-driver
```

---

## Build History

Enable build history:

```bash
# In local.conf
INHERIT += "buildhistory"
BUILDHISTORY_COMMIT = "1"

# Build history location
buildhistory/
├── images/
├── packages/
└── sdk/
```

Analyzing build history:

```bash
# Compare builds
buildhistory-diff

# Package changes
buildhistory-diff -p busybox

# Image changes
buildhistory-diff -i core-image-minimal
```

---

## Testing Framework

```bash
# Runtime testing
inherit testimage

# Test cases
IMAGE_CLASSES += "testimage"
TEST_SUITES = "ping ssh df connman syslog"

# Run tests
bitbake core-image-minimal -c testimage

# Custom tests
recipes-test/
└── mytest/
    └── mytest.py
```

---

## Writing Test Cases

Python test:

```python
from oeqa.runtime.case import OERuntimeTestCase

class MyTest(OERuntimeTestCase):
    @classmethod
    def setUpClass(cls):
        cls.tc.target.run('systemctl start myservice')

    def test_service_running(self):
        status, output = self.target.run('systemctl is-active myservice')
        self.assertEqual(status, 0, 'Service not running')

    def test_network_connectivity(self):
        status, output = self.target.run('ping -c 1 8.8.8.8')
        self.assertEqual(status, 0, 'Network not available')
```

---

## ptest Framework

Package tests:

```bash
# In recipe
inherit ptest

RDEPENDS_${PN}-ptest += "make bash"

do_compile_ptest() {
    oe_runmake buildtest
}

do_install_ptest() {
    oe_runmake install-test DESTDIR=${D}${PTEST_PATH}
}
```

Running ptest:

```bash
# On target
ptest-runner myapp

# All ptests
ptest-runner
```

---

## Benchmarking

LMbench:

```bash
IMAGE_INSTALL_append = " lmbench"

# Run benchmarks
lmbench-run

# Specific tests
lat_mem_rd 1024 128
bw_mem 1024 rd
```

Custom benchmarks:

```bash
# Timing commands
time ./myapp

# System performance
vmstat 1
iostat 1
```

---

## BitBake UI Tools

Toaster web interface:

```bash
# Start Toaster
source toaster start

# Access at http://localhost:8000

# Configure build
# - Set machine
# - Select image
# - Add/remove layers
# - Start build

# Stop Toaster
source toaster stop
```

---

## BitBake Debugging

```bash
# Verbose output
bitbake -v myapp

# Debug output
bitbake -D myapp
bitbake -DD myapp  # More verbose

# Show environment
bitbake -e myapp | grep ^VARIABLE

# Dependency graph
bitbake -g myapp
# Creates: pn-buildlist, task-depends.dot

# Dry run
bitbake -n myapp
```

---

## Dependency Visualization

```bash
# Generate task dependency graph
bitbake -g core-image-minimal

# View with graphviz
dot -Tpng task-depends.dot -o task-depends.png

# Package dependencies
bitbake -g -u depexp core-image-minimal
```

Task visualization:

```bash
# Recipe dependencies
bitbake -g myapp
grep "myapp" pn-depends.dot

# Reverse dependencies
bitbake -g core-image-minimal
grep "zlib" pn-depends.dot
```

---

## Code Inspection Tools

Static analysis:

```bash
# In recipe
inherit codecheck

# Run checks
bitbake -c codecheck myapp
```

Linting:

```bash
# Python linting
IMAGE_INSTALL_append = " python3-pylint"

# Shell linting
IMAGE_INSTALL_append = " shellcheck"
```

---

## Development Best Practices

Incremental builds:

```bash
# Use shared state cache
SSTATE_DIR = "/path/to/shared/sstate-cache"

# Shared downloads
DL_DIR = "/path/to/shared/downloads"

# Use rm_work
INHERIT += "rm_work"
RM_WORK_EXCLUDE += "myapp"
```

Clean builds:

```bash
# Clean specific recipe
bitbake -c clean myapp

# Clean with sstate
bitbake -c cleansstate myapp

# Clean everything
bitbake -c cleanall myapp
```

---

## Debugging Recipe Failures

```bash
# Run task manually
bitbake -c compile myapp

# Keep failed build
BB_PRESERVE_FAILURE = "1"

# Interactive debugging
bitbake -c devshell myapp

# Log location
tmp/work/*/myapp/*/temp/log.do_compile
```

Common issues:
- Missing dependencies
- Wrong paths
- Configuration errors
- Compilation flags

---

## Patch Management

Creating patches:

```bash
# In devtool workspace
cd workspace/sources/myapp
git add modified-file.c
git commit -m "Fix bug"

# Generate patch
git format-patch -1

# Or use devtool
devtool update-recipe myapp
```

Applying patches:

```bash
# In recipe
SRC_URI += "file://0001-fix-bug.patch"

# Verify patch applies
bitbake -c patch myapp

# Fix patch conflicts
bitbake -c devshell myapp
```

---

## Continuous Development

File watching:

```bash
# Use devtool
devtool modify myapp

# Auto-rebuild on changes
while inotifywait -r workspace/sources/myapp/; do
    devtool build myapp
    devtool deploy-target myapp root@target
done
```

Hot reload:

```bash
# Deploy only changed files
rsync -avz workspace/sources/myapp/bin/ root@target:/usr/bin/

# Restart service
ssh root@target "systemctl restart myapp"
```

---

## Documentation Tools

Recipe documentation:

```bash
# Generate recipe info
bitbake-layers show-recipes myapp

# Recipe dependencies
bitbake -g myapp

# Layer info
bitbake-layers show-layers
```

Auto-documentation:

```bash
# Sphinx documentation
recipes-docs/
└── sphinx-doc/
    └── sphinx-doc.bb
```

---

## Team Collaboration

Shared configuration:

```bash
# Team build configuration
conf/site.conf:
SSTATE_DIR = "/nfs/shared/sstate-cache"
DL_DIR = "/nfs/shared/downloads"
TMPDIR = "/local/tmp/${USER}"
```

Layer index:

```bash
# Use layer index
bitbake-layers layerindex-fetch meta-custom
bitbake-layers layerindex-show-depends meta-custom
```

---

## Summary

Key workflow tools:
- devtool for recipe development
- QEMU for testing
- SDK for application development
- GDB for debugging
- Performance analysis tools

Best practices:
- Use devtool workflow
- Test in QEMU first
- Enable build history
- Write automated tests
- Document changes
- Use version control
