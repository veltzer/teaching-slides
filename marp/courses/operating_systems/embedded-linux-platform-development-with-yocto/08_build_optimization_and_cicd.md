# Build Optimization and CI/CD

---

## Build Performance Overview

![build_performance_overview](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/08_build_optimization_and_cicd/build_performance_overview.svg)

---

## Hardware Optimization

CPU and cores:

```bash
# In local.conf
BB_NUMBER_THREADS = "${@oe.utils.cpu_count()}"
PARALLEL_MAKE = "-j ${@oe.utils.cpu_count()}"

# Manual setting (recommended)
BB_NUMBER_THREADS = "16"
PARALLEL_MAKE = "-j 16"

# Conservative (avoid overload)
BB_NUMBER_THREADS = "8"
PARALLEL_MAKE = "-j 12"
```

Memory recommendations:
- Minimum: 8GB RAM
- Recommended: 16GB+ RAM
- Optimal: 32GB+ RAM
- Swap: 2x RAM size

---

## Storage Optimization

SSD vs HDD performance:

![storage_optimization](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/08_build_optimization_and_cicd/storage_optimization.svg)

---

## Filesystem Configuration

Best practices:

```bash
# Use ext4 with specific options
# /etc/fstab
/dev/sda1 /build ext4 noatime,nodiratime,data=writeback 0 2

# tmpfs for tmp directory
tmpfs /build/tmp tmpfs size=64G,noatime 0 0

# Separate partitions
/build/downloads  # Download cache
/build/sstate     # Shared state
/build/tmp        # Build workspace
```

I/O scheduler:

```bash
# Use deadline or noop for SSDs
echo deadline > /sys/block/sda/queue/scheduler

# Or in kernel cmdline
elevator=deadline
```

---

## Shared State Cache

Configuration:

```bash
# In local.conf
SSTATE_DIR = "/path/to/shared/sstate-cache"

# Network cache
SSTATE_DIR = "file:///nfs/sstate-cache"

# Multiple locations
SSTATE_MIRRORS = "file://.* http://someserver.tld/share/sstate/PATH;downloadfilename=PATH"

# Cache size monitoring
du -sh /path/to/sstate-cache
```

Cache maintenance:

```bash
# Clean old cache entries
./scripts/sstate-cache-management.sh --cache-dir=/path/to/sstate --remove-duplicated

# Remove entries older than 30 days
./scripts/sstate-cache-management.sh --cache-dir=/path/to/sstate --remove-old --days=30
```

---

## Download Mirrors

```bash
# In local.conf
DL_DIR = "/path/to/shared/downloads"

# Premirror (try first)
PREMIRRORS_prepend = "\
git://.*/.* http://mirror.example.com/sources/ \n \
ftp://.*/.* http://mirror.example.com/sources/ \n \
http://.*/.* http://mirror.example.com/sources/ \n \
https://.*/.* http://mirror.example.com/sources/ \n"

# Fallback mirrors
MIRRORS_prepend = "\
ftp://.*/.* http://downloads.yoctoproject.org/mirror/sources/ \n \
http://.*/.* http://downloads.yoctoproject.org/mirror/sources/ \n \
https://.*/.* http://downloads.yoctoproject.org/mirror/sources/ \n"

# Fetch from mirrors first
BB_FETCH_PREMIRRORONLY = "1"
```

---

## Build Directory Management

![build_directory_management](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/08_build_optimization_and_cicd/build_directory_management.svg)

---

## rm_work Class

Remove work directories after build:

```bash
# In local.conf
INHERIT += "rm_work"

# Exclude specific recipes
RM_WORK_EXCLUDE += "linux-yocto busybox myapp"

# Keep logs
RM_WORK_EXCLUDE += "temp"
```

Disk space savings:
- Without rm_work: ~150GB
- With rm_work: ~50GB
- Trade-off: Slower incremental builds

---

## Parallel Build Optimization

Task parallelism:

```bash
# BitBake parallel tasks
BB_NUMBER_THREADS = "16"

# Make parallel jobs
PARALLEL_MAKE = "-j 16"

# Package parallel jobs
PARALLEL_MAKEINST = "-j 16"

# Per-recipe limits
PARALLEL_MAKE_pn-linux-yocto = "-j 8"
PARALLEL_MAKE_pn-gcc = "-j 4"
```

Network parallelism:

```bash
# Parallel downloads
BB_NUMBER_PARSE_THREADS = "16"
BB_FETCH_PREMIRRORONLY = "0"
```

---

## Build Time Analysis

```bash
# Enable buildstats
INHERIT += "buildstats"

# Location
tmp/buildstats/

# Analyze with pybootchartgui
./scripts/pybootchartgui/pybootchartgui.py tmp/buildstats/20240115120000/

# Generate chart
./scripts/pybootchartgui/pybootchartgui.py -o build-chart.png tmp/buildstats/20240115120000/
```

Identify bottlenecks:

```bash
# Long-running tasks
find tmp/buildstats -name "do_*" -exec grep "Elapsed time" {} \; | sort -n

# Top time consumers
du -sh tmp/work/*/* | sort -h | tail -20
```

---

## Hash Equivalence Server

Accelerate builds with hash equivalence:

```bash
# Server setup (on shared host)
bitbake-hashserv

# Client configuration (in local.conf)
BB_HASHSERVE = "hashserv.example.com:8686"
BB_SIGNATURE_HANDLER = "OEEquivHash"

# Benefits
# - Share builds across teams
# - Faster clean builds
# - Better cache utilization
```

---

## Package Feed Server

```bash
# Build package feed
bitbake package-index

# Serve via HTTP
cd tmp/deploy/rpm
python3 -m http.server 8000

# In target image
# /etc/yum.repos.d/oe-remote.repo
[oe-remote]
name=OE Remote Feed
baseurl=http://buildserver:8000/cortexa9hf
enabled=1
gpgcheck=0
```

---

## CI/CD Architecture

![ci_cd_architecture](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/08_build_optimization_and_cicd/ci_cd_architecture.svg)

---

## Jenkins Integration

Jenkinsfile example:

```groovy
pipeline {
    agent {
        label 'yocto-builder'
    }

    environment {
        BUILD_DIR = "${WORKSPACE}/build"
        DL_DIR = "/shared/downloads"
        SSTATE_DIR = "/shared/sstate-cache"
    }

    stages {
        stage('Setup') {
            steps {
                sh 'source oe-init-build-env ${BUILD_DIR}'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    cd ${BUILD_DIR}
                    bitbake core-image-minimal
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'bitbake core-image-minimal -c testimage'
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'build/tmp/deploy/images/**/*'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
```

---

## GitLab CI/CD

`.gitlab-ci.yml`:
```yaml
variables:
  DL_DIR: /cache/downloads
  SSTATE_DIR: /cache/sstate-cache

stages:
  - build
  - test
  - deploy

build_image:
  stage: build
  tags:
    - yocto
  script:
    - source oe-init-build-env build
    - echo 'DL_DIR = "${DL_DIR}"' >> conf/local.conf
    - echo 'SSTATE_DIR = "${SSTATE_DIR}"' >> conf/local.conf
    - bitbake core-image-minimal
  artifacts:
    paths:
      - build/tmp/deploy/images/
    expire_in: 1 week
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - build/cache/

test_image:
  stage: test
  dependencies:
    - build_image
  script:
    - bitbake core-image-minimal -c testimage

deploy_staging:
  stage: deploy
  only:
    - develop
  script:
    - ./deploy-to-staging.sh
```

---

## GitHub Actions

`.github/workflows/yocto-build.yml`:

```yaml
name: Yocto Build

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: self-hosted

    steps:
    - uses: actions/checkout@v3

    - name: Setup Yocto
      run: |
        git clone git://git.yoctoproject.org/poky
        cd poky
        git checkout kirkstone

    - name: Initialize Build
      run: |
        source poky/oe-init-build-env build
        echo 'DL_DIR = "/cache/downloads"' >> conf/local.conf
        echo 'SSTATE_DIR = "/cache/sstate-cache"' >> conf/local.conf

    - name: Build Image
      run: |
        source poky/oe-init-build-env build
        bitbake core-image-minimal

    - name: Upload Artifacts
      uses: actions/upload-artifact@v3
      with:
        name: yocto-images
        path: build/tmp/deploy/images/
```

---

## Docker Build Environment

Dockerfile:

```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    gawk wget git diffstat unzip texinfo gcc \
    build-essential chrpath socat cpio python3 \
    python3-pip python3-pexpect xz-utils \
    debianutils iputils-ping python3-git \
    python3-jinja2 libegl1-mesa libsdl1.2-dev \
    pylint xterm python3-subunit mesa-common-dev

# Create build user
RUN useradd -m -s /bin/bash builder
USER builder
WORKDIR /home/builder

# Clone Poky
RUN git clone git://git.yoctoproject.org/poky
WORKDIR /home/builder/poky
RUN git checkout kirkstone

# Setup build environment
RUN source oe-init-build-env build

CMD ["/bin/bash"]
```

---

## Build in Docker

Docker Compose:

```yaml
version: '3.8'

services:
  yocto-builder:
    build: .
    volumes:
      - ./build:/home/builder/build
      - downloads:/downloads
      - sstate:/sstate-cache
    environment:
      - DL_DIR=/downloads
      - SSTATE_DIR=/sstate-cache
      - BB_NUMBER_THREADS=16
      - PARALLEL_MAKE=-j 16

volumes:
  downloads:
  sstate:
```

Usage:

```bash
docker-compose run yocto-builder
# Inside container
bitbake core-image-minimal
```

---

## CROPS (CROss PlatformS)

Using CROPS containers:

```bash
# Pull CROPS image
docker pull crops/poky:ubuntu-22.04

# Run with workspace
docker run --rm -it \
    -v $(pwd):/workdir \
    crops/poky:ubuntu-22.04 \
    --workdir=/workdir

# Inside container
source oe-init-build-env build
bitbake core-image-minimal
```

---

## Automated Testing

Test configuration:

```bash
# In local.conf
INHERIT += "testimage"
TEST_TARGET = "qemu"

# Test suites
TEST_SUITES = "ping ssh df connman syslog date"

# Custom tests
TEST_SUITES_append = " mytest"
```

Running tests:

```bash
# Build and test
bitbake core-image-minimal -c testimage

# Test results
tmp/log/oeqa/
```

---

## Test Case Development

Custom test suite:

```python
# meta-custom/lib/oeqa/runtime/cases/mytest.py
from oeqa.runtime.case import OERuntimeTestCase

class MyTestSuite(OERuntimeTestCase):

    def test_package_installed(self):
        status, output = self.target.run('which myapp')
        self.assertEqual(status, 0, 'myapp not installed')

    def test_service_running(self):
        status, output = self.target.run('systemctl is-active myservice')
        self.assertEqual(status, 0, 'myservice not running')

    def test_network_port(self):
        status, output = self.target.run('netstat -ln | grep :8080')
        self.assertEqual(status, 0, 'Port 8080 not listening')
```

---

## Performance Benchmarking

Benchmark suite:

```bash
# Add benchmarking tools
IMAGE_INSTALL_append = " lmbench iperf3 stress-ng"

# Automated benchmarks
inherit benchmark

do_benchmark() {
    # CPU benchmark
    stress-ng --cpu 4 --timeout 60s --metrics

    # Memory bandwidth
    lmbench-run

    # Network throughput
    iperf3 -c server -t 60
}
```

---

## Build Artifacts Management

Artifact structure:

```tree
artifacts/
├── images/
│   ├── core-image-minimal-qemux86-64.wic
│   ├── core-image-minimal-qemux86-64.manifest
│   └── bzImage
├── sdk/
│   └── poky-glibc-x86_64-core-image-minimal-sdk.sh
├── packages/
│   └── rpm/
└── buildhistory/
```

Versioning strategy:

```bash
# Version in filename
IMAGE_NAME = "${IMAGE_BASENAME}-${MACHINE}-${DATETIME}"
IMAGE_NAME[vardepsexclude] = "DATETIME"

# Git commit in version
PV = "1.0+git${SRCPV}"
```

---

## Reproducible Builds

Enable reproducibility:

```bash
# In local.conf
INHERIT += "reproducible_build"

# Source date epoch
SOURCE_DATE_EPOCH = "1609459200"

# Disable timestamps
REPRODUCIBLE_TIMESTAMP_ROOTFS = "${SOURCE_DATE_EPOCH}"

# Build ID
BUILD_ID = "reproducible"
```

Verification:

```bash
# Compare builds
diffoscope image1.wic image2.wic

# Hash verification
sha256sum image.wic
```

---

## Incremental Build Strategy

Optimize for development:

```bash
# Keep source after build
RM_WORK_EXCLUDE += "myapp linux-yocto"

# Incremental kernel builds
do_compile_append() {
    # Mark for incremental
    touch ${B}/.scmversion
}

# Fast iteration
devtool modify myapp
# ... make changes ...
devtool build myapp
devtool deploy-target myapp root@target
```

---

## Build Server Architecture

![build_server_architecture](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/08_build_optimization_and_cicd/build_server_architecture.svg)

---

## Multi-Machine Builds

Parallel builds for multiple targets:

```bash
# In CI script
machines="qemux86-64 qemuarm qemuarm64"

for machine in $machines; do
    (
        export MACHINE=$machine
        bitbake core-image-minimal &
    )
done
wait

# Or use multiconfig
BBMULTICONFIG = "qemux86-64 qemuarm qemuarm64"
bitbake multiconfig:qemux86-64:core-image-minimal \
        multiconfig:qemuarm:core-image-minimal \
        multiconfig:qemuarm64:core-image-minimal
```

---

## Build Notifications

Email notifications:

```bash
# Build completion notification
INHERIT += "buildhistory"

# Custom notification
do_notify_build_complete() {
    mail -s "Build Complete" team@example.com << EOF
Build completed successfully
Image: core-image-minimal
Machine: ${MACHINE}
Build time: ${BUILD_TIME}
EOF
}

addtask notify_build_complete after do_rootfs
```

Slack integration:

```bash
do_notify_slack() {
    curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
        -d '{"text":"Build completed: ${IMAGE_NAME}"}'
}
```

---

## Build Monitoring

Metrics collection:

```bash
# Enable buildstats
INHERIT += "buildstats"

# Collect metrics
tmp/buildstats/${DATETIME}/

# Parse and visualize
./scripts/buildstats-summary.py tmp/buildstats/
```

Resource monitoring:

```bash
# System monitor during build
while true; do
    echo "$(date) $(uptime) $(free -h)" >> build-monitor.log
    sleep 60
done
```

---

## Failure Handling

Error recovery:

```bash
# Continue on error
BB_NUMBER_THREADS = "1"
BB_CONTINUE = "1"

# Preserve failed builds
BB_PRESERVE_FAILURE = "1"

# Retry failed tasks
BB_DEFAULT_TASK_RETRIES = "3"
```

Notification on failure:

```bash
# In CI script
if ! bitbake core-image-minimal; then
    echo "Build failed" | mail -s "Build Failure" team@example.com
    exit 1
fi
```

---

## Build Cache Strategies

Local cache:

```bash
# Per-developer cache
SSTATE_DIR = "${HOME}/.yocto-cache/sstate"
DL_DIR = "${HOME}/.yocto-cache/downloads"
```

Team cache:

```bash
# Network cache
SSTATE_DIR = "file:///nfs/team/sstate-cache"
DL_DIR = "/nfs/team/downloads"

# HTTP cache
SSTATE_MIRRORS = "file://.* http://buildserver/sstate/PATH"
```

S3 cache:

```bash
# AWS S3 bucket
SSTATE_MIRRORS = "file://.* s3://bucket/sstate/PATH"
```

---

## Release Management

Version tagging:

```bash
# Git tags
git tag -a v1.0.0 -m "Release 1.0.0"

# Image versioning
IMAGE_VERSION = "1.0.0"
IMAGE_NAME = "${IMAGE_BASENAME}-${MACHINE}-${IMAGE_VERSION}"
```

Release checklist:
- Build all target machines
- Run automated tests
- Generate SDK
- Create release notes
- Tag repositories
- Archive artifacts
- Update documentation

---

## Summary

Optimization strategies:
- Hardware: SSD, RAM, CPU cores
- Configuration: Parallelism, caching
- Network: Mirrors, bandwidth
- Build server infrastructure
- Automated testing

CI/CD best practices:
- Automated builds
- Continuous testing
- Artifact management
- Reproducible builds
- Team collaboration
- Monitoring and notifications
