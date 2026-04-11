---
tags:
  - infrastructure:linux
  - infrastructure:embedded
  - tools:yocto
  - practices:deployment
level: advanced
category: embedded
audience:
  - audiences:developers
  - audiences:sysadmins

---
# Production Deployment

---

## Deployment Lifecycle

![deployment_lifecycle](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/10_production_deployment/deployment_lifecycle.svg)

---

## Release Management

Version strategy:

```bash
# Semantic versioning
DISTRO_VERSION = "1.2.3"

# Date-based versioning
DISTRO_VERSION = "2024.01"

# Git-based versioning
PV = "1.0+git${SRCPV}"

# Build metadata
IMAGE_VERSION_SUFFIX = "-${DATETIME}"
IMAGE_VERSION_SUFFIX[vardepsexclude] = "DATETIME"
```

Release tags:

```bash
# Tag layers
git tag -a v1.2.3 -m "Release 1.2.3"
git push origin v1.2.3

# Manifest repository
repo manifest -r -o release-1.2.3.xml
```

---

## Image Formats

![image_formats](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/10_production_deployment/image_formats.svg)

---

## WIC Images

Disk image creation:

```bash
# In image recipe
IMAGE_FSTYPES = "wic wic.bmap"

# WIC kickstart file
WKS_FILE = "custom-image.wks"

# custom-image.wks
part /boot --source bootimg-partition --ondisk sda --fstype=vfat --label boot --active --align 4 --size 64
part / --source rootfs --ondisk sda --fstype=ext4 --label root --align 4 --size 2G
part /data --ondisk sda --fstype=ext4 --label data --align 4 --size 1G

bootloader --ptable msdos --timeout=0 --append="rootwait console=ttyS0,115200"
```

Flash to device:

```bash
# Using dd
dd if=image.wic of=/dev/sdb bs=4M status=progress

# Using bmaptool (faster)
bmaptool copy image.wic.bz2 /dev/sdb
```

---

## Container Deployment

Docker image export:

```bash
# Create container image
INHERIT += "image-container"
IMAGE_FSTYPES += "docker"

# Build
bitbake core-image-minimal

# Load into Docker
docker load < tmp/deploy/images/*/core-image-minimal-*.docker

# Run container
docker run -it core-image-minimal
```

---

## OSTree/libostree

Atomic updates:

```bash
# Enable OSTree
DISTRO_FEATURES_append = " ostree"

# Install OSTree
IMAGE_INSTALL_append = " ostree"

# Create repository
ostree --repo=/srv/ostree init --mode=archive

# Commit image
ostree --repo=/srv/ostree commit \
    --branch=mydevice/main \
    --subject="Release 1.0" \
    /path/to/rootfs

# Deploy on device
ostree admin deploy mydevice/main
```

---

## Update Strategies

![update_strategies](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/10_production_deployment/update_strategies.svg)

---

## A/B Partition Updates

Dual boot configuration:

```bash
# WIC configuration
part /boot --source bootimg-partition --fstype=vfat --label boot --size 64M
part / --source rootfs --fstype=ext4 --label rootfs_a --size 2G
part /data --fstype=ext4 --label rootfs_b --size 2G
part /userdata --fstype=ext4 --label userdata --size 1G

# U-Boot environment
bootpart=0
setenv bootargs root=/dev/mmcblk0p${bootpart} rootwait
```

Update process:
1. Download to inactive partition
1. Verify downloaded image
1. Set boot flag to new partition
1. Reboot
1. Validate new system
1. Fall back if validation fails

---

## SWUpdate

Software update framework:

```bash
# Install SWUpdate
IMAGE_INSTALL_append = " swupdate swupdate-www"

# In image recipe
inherit swupdate

# SWU description file
sw-description:
software =
{
    version = "1.0.1";

    hardware-compatibility: [ "mydevice-v1" ];

    images: (
        {
            filename = "rootfs.ext4.gz";
            sha256 = "abc123...";

            type = "raw";
            device = "/dev/mmcblk0p2";
            compressed = true;
        }
    );

    scripts: (
        {
            filename = "post-install.sh";
            type = "postinstall";
        }
    );
}
```

---

## RAUC

Robust Auto-Update Controller:

```bash
# Install RAUC
IMAGE_INSTALL_append = " rauc"

# System configuration
/etc/rauc/system.conf:
[system]
compatible=mydevice
bootloader=uboot

[keyring]
path=/etc/rauc/ca.cert.pem

[slot.rootfs.0]
device=/dev/mmcblk0p2
type=ext4
bootname=A

[slot.rootfs.1]
device=/dev/mmcblk0p3
type=ext4
bootname=B
```

Create update bundle:

```bash
# Bundle manifest
rauc bundle --cert=cert.pem --key=key.pem \
    --signing-keyring=ca.cert.pem \
    bundle/ update.raucb
```

---

## Mender Integration

```bash
# Add Mender layer
BBLAYERS += "/path/to/meta-mender"

# In local.conf
INHERIT += "mender-full"

# Mender configuration
MENDER_SERVER_URL = "https://hosted.mender.io"
MENDER_TENANT_TOKEN = "your-token"

# Image type
IMAGE_FSTYPES_append = " mender"

# Partition layout
MENDER_STORAGE_DEVICE = "/dev/mmcblk0"
MENDER_BOOT_PART_SIZE_MB = "64"
MENDER_DATA_PART_SIZE_MB = "1024"
```

---

## OTA Update Architecture

![ota_update_architecture](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/10_production_deployment/ota_update_architecture.svg)

---

## Factory Provisioning

Initial setup process:

```bash
# Provisioning script
do_provision() {
    # Flash bootloader
    dd if=u-boot.img of=/dev/mmcblk0 bs=512 seek=1

    # Flash image
    bmaptool copy production-image.wic /dev/mmcblk0

    # Set serial number
    echo "SN-${SERIAL}" > /factory/serial

    # Generate device keys
    openssl genrsa -out /factory/device.key 2048
    openssl req -new -key /factory/device.key -out /factory/device.csr

    # Provision certificates
    curl -X POST https://ca.example.com/sign \
        --data-binary @/factory/device.csr \
        -o /factory/device.crt
}
```

---

## Device Initialization

First boot configuration:

```bash
# Systemd first-boot service
[Unit]
Description=First Boot Setup
ConditionPathExists=!/var/lib/first-boot-done

[Service]
Type=oneshot
ExecStart=/usr/bin/first-boot-setup.sh
ExecStartPost=/usr/bin/touch /var/lib/first-boot-done
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Setup script:

```bash
#!/bin/sh
# first-boot-setup.sh

# Expand root partition
resize2fs /dev/mmcblk0p2

# Generate SSH host keys
ssh-keygen -A

# Set unique hostname
echo "device-$(cat /factory/serial)" > /etc/hostname

# Register with backend
curl -X POST https://backend.example.com/register \
    -d "serial=$(cat /factory/serial)" \
    -d "version=$(cat /etc/version)"
```

---

## Remote Access

Secure remote access:

```bash
# VPN-based access
IMAGE_INSTALL_append = " openvpn wireguard-tools"

# SSH with key-only auth
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no

# Reverse SSH tunnel
autossh -M 0 -N -R 2222:localhost:22 tunnel@server.com

# WebRTC-based access (e.g., Webrtc.io)
IMAGE_INSTALL_append = " webrtc-streamer"
```

---

## Fleet Management

Device grouping:

```tree
fleet/
├── production/
│   ├── group-a/      # Geographic region
│   ├── group-b/
│   └── group-c/
├── staging/
└── development/
```

Update rollout strategy:
1. Canary deployment (1-5% devices)
1. Monitor for issues
1. Staged rollout (25%, 50%, 100%)
1. Rollback capability

---

## Health Monitoring

System health checks:

```bash
# Health monitoring service
[Unit]
Description=System Health Monitor

[Service]
Type=simple
ExecStart=/usr/bin/health-monitor.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

Monitoring script:

```bash
#!/bin/sh
while true; do
    # CPU temperature
    temp=$(cat /sys/class/thermal/thermal_zone0/temp)

    # Disk space
    disk=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

    # Memory usage
    mem=$(free | awk 'NR==2 {printf "%.0f", $3/$2*100}')

    # Send to backend
    curl -X POST https://monitoring.example.com/health \
        -d "device=${SERIAL}&temp=${temp}&disk=${disk}&mem=${mem}"

    sleep 300
done
```

---

## Log Aggregation

Centralized logging:

```bash
# rsyslog forwarding
IMAGE_INSTALL_append = " rsyslog"

# /etc/rsyslog.conf
*.* @@logserver.example.com:514

# Or use systemd journal forwarding
[Journal]
ForwardToSyslog=yes
```

Log rotation:

```bash
# /etc/logrotate.conf
/var/log/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## Crash Reporting

Automatic crash reporting:

```bash
# Enable core dumps
IMAGE_INSTALL_append = " systemd-coredump"

# Kernel crash dumps
CONFIG_CRASH_DUMP=y

# Automatic upload
do_crash_report() {
    if [ -f /var/lib/systemd/coredump/core.* ]; then
        tar czf crash-${SERIAL}-$(date +%s).tar.gz \
            /var/lib/systemd/coredump/core.*

        curl -X POST https://crashes.example.com/upload \
            -F "file=@crash-${SERIAL}-$(date +%s).tar.gz"
    fi
}
```

---

## Performance Metrics

Collect runtime metrics:

```bash
# Install collectd
IMAGE_INSTALL_append = " collectd"

# Configuration
/etc/collectd.conf:
LoadPlugin cpu
LoadPlugin memory
LoadPlugin disk
LoadPlugin network

<Plugin network>
    Server "metrics.example.com" "25826"
</Plugin>
```

Custom metrics:

```bash
# Application metrics
curl -X POST https://metrics.example.com/custom \
    -d "metric=app_requests&value=1234&device=${SERIAL}"
```

---

## Backup and Recovery

Automated backups:

```bash
# Backup script
do_backup() {
    # Backup configuration
    tar czf /data/backup-$(date +%Y%m%d).tar.gz \
        /etc \
        /var/lib/myapp

    # Upload to cloud
    aws s3 cp /data/backup-$(date +%Y%m%d).tar.gz \
        s3://backups/device-${SERIAL}/

    # Keep only last 7 backups
    find /data -name "backup-*.tar.gz" -mtime +7 -delete
}

# Scheduled backup
0 2 * * * /usr/bin/backup.sh
```

---

## Disaster Recovery

Recovery partition:

```bash
# WIC with recovery
part /boot --source bootimg-partition --fstype=vfat --size 64M
part / --source rootfs --fstype=ext4 --label rootfs --size 2G
part /recovery --source rootfs --fstype=ext4 --label recovery --size 2G
part /data --fstype=ext4 --label data --size 1G
```

Recovery boot:

```bash
# U-Boot recovery mode
if test ${recovery_mode} = 1; then
    setenv bootargs root=/dev/mmcblk0p3
else
    setenv bootargs root=/dev/mmcblk0p2
fi
```

---

## A/B Testing

Feature flags:

```bash
# Configuration service
IMAGE_INSTALL_append = " feature-flags-client"

# Feature check
if feature_enabled "new-algorithm"; then
    use_new_algorithm
else
    use_old_algorithm
fi

# Gradual rollout
percentage=10  # 10% of devices
if [ $((RANDOM % 100)) -lt $percentage ]; then
    enable_feature "new-algorithm"
fi
```

---

## Compliance Documentation

Required documentation:
- Bill of Materials (BOM)
- Software Bill of Materials (SBOM)
- License manifest
- Security audit logs
- Vulnerability reports
- Build manifests
- Test reports
- Deployment procedures

Automated generation:

```bash
# Generate compliance package
bitbake -c populate_lic core-image-minimal
bitbake -c create_spdx core-image-minimal

# Package documentation
tar czf compliance-docs-${VERSION}.tar.gz \
    tmp/deploy/licenses/ \
    tmp/deploy/spdx/ \
    buildhistory/
```

---

## Production Checklist

Pre-deployment:
- [ ] Security hardening complete
- [ ] All tests passing
- [ ] Performance validated
- [ ] Documentation updated
- [ ] Compliance verified
- [ ] Update mechanism tested
- [ ] Rollback procedure verified
- [ ] Monitoring configured
- [ ] Logs aggregated
- [ ] Backup system operational

Post-deployment:
- [ ] Initial health check
- [ ] Connectivity verified
- [ ] Services running
- [ ] Metrics reporting
- [ ] Update capability tested

---

## Field Deployment

Deployment phases:
1. **Pilot** - 1-10 devices
1. **Limited** - 10-100 devices
1. **Regional** - 100-1000 devices
1. **Full** - All devices

Success criteria:
- Zero critical failures
- <1% minor issues
- All metrics within range
- Positive user feedback
- Update success rate >99%

---

## Incident Response

Incident handling process:
1. Detection and alerting
1. Initial assessment
1. Containment
1. Root cause analysis
1. Remediation
1. Post-mortem

Automated response:

```bash
# Incident detection
if [ $error_rate -gt 10 ]; then
    # Alert team
    curl -X POST https://alerts.example.com/incident \
        -d "severity=high&device=${SERIAL}"

    # Collect diagnostics
    collect_logs

    # Self-healing attempt
    systemctl restart critical-service
fi
```

---

## Lifecycle Management

![lifecycle_management](svg/courses/operating_systems/embedded-linux-platform-development-with-yocto/10_production_deployment/lifecycle_management.svg)

---

## End-of-Life Management

EOL process:
1. Announce EOL date (12+ months ahead)
1. Final security updates
1. Migration path documentation
1. Decommissioning procedure
1. Data retention policy

Decommissioning:

```bash
#!/bin/sh
# Secure decommissioning

# Wipe sensitive data
shred -vfz -n 3 /dev/mmcblk0

# Remove from management
curl -X DELETE https://backend.example.com/devices/${SERIAL}

# Certificate revocation
curl -X POST https://ca.example.com/revoke \
    -d "serial=${SERIAL}"
```

---

## Summary

Key deployment topics:
- Release management and versioning
- Image formats and packaging
- Update strategies (A/B, atomic, delta)
- OTA frameworks (SWUpdate, RAUC, Mender)
- Factory provisioning
- Fleet management
- Monitoring and health checks
- Backup and disaster recovery

Best practices:
- Automate everything
- Test update mechanisms thoroughly
- Monitor continuously
- Plan for failure scenarios
- Document processes
- Maintain compliance
- Lifecycle planning
