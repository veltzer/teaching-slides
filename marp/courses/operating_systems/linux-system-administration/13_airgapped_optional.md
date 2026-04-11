---
tags:
  - infrastructure:linux
  - audiences:sysadmin
level: intermediate
category: operating-systems
audience:
  - audiences:sysadmins
  - audiences:devops

---
# Maintaining Linux in Air-Gapped Environments (Optional)
## Offline Package Management, Security, and Updates

---
## What is an Air-Gapped Environment?

- Systems physically isolated from the internet
- Common in: military, critical infrastructure, healthcare, finance
- Challenges:
    - No direct package downloads
    - No automatic security updates
    - Manual transfer of all software
    - Increased documentation burden

---
## Air-Gap Architecture

Red lines represent the air gap - no network connection crosses this boundary.

---

## Air-Gap Architecture

![air_gap_architecture](svg/courses/operating_systems/linux-system-administration/13_airgapped_optional/air_gap_architecture.svg)

---
## Local Repository Management

```bash
# Create a local mirror (on connected machine)
apt-mirror

# Or use apt-get to download packages
apt-get download nginx
apt-get download --print-uris nginx | \
  awk '{print $1}' > urls.txt

# Download with all dependencies
apt-get install --download-only -o \
  Dir::Cache::archives=/media/usb/packages nginx

# Create local repo structure
dpkg-scanpackages /media/usb/packages \
  /dev/null | gzip > Packages.gz
```

---
## Building a Complete Local Mirror

```bash
# apt-mirror configuration
# /etc/apt/mirror.list
set base_path    /opt/mirror
set mirror_path  $base_path/mirror
set skel_path    $base_path/skel
set var_path     $base_path/var

deb http://archive.ubuntu.com/ubuntu noble \
  main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu noble-security \
  main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu noble-updates \
  main restricted universe multiverse
```

```bash
# Run the mirror (downloads ~200GB+)
apt-mirror

# On air-gapped system
echo "deb file:///opt/mirror/mirror/archive.ubuntu.com/ubuntu noble main" \
  > /etc/apt/sources.list
apt update
```

---
## Package Transport Mechanisms

Transfer methods for air-gapped systems:
1. Removable media (USB drives, DVDs)
1. One-way data diodes
1. Cross-domain transfer stations

```bash
# On connected system: download and verify
apt-get download --print-uris <packages> > list.txt
wget -i list.txt -P /media/transfer/

# Generate checksums
sha256sum /media/transfer/*.deb > checksums.txt

# On air-gapped system: verify and install
sha256sum -c checksums.txt
dpkg -i /media/transfer/*.deb
```

---
## Dependency Resolution for Offline Install

```bash
# Download package and ALL dependencies
apt-get install --download-only -o \
  Dir::Cache::archives=/tmp/packages nginx

# Alternative: use apt-rdepends
apt install apt-rdepends
apt-rdepends nginx | grep -v "^ " | \
  xargs apt-get download -o \
  Dir::Cache::archives=/tmp/packages

# Create installable bundle
cd /tmp/packages
dpkg-scanpackages . /dev/null | gzip > Packages.gz

# On air-gapped system
echo "deb [trusted=yes] file:///media/usb/packages ./" \
  > /etc/apt/sources.list.d/local.list
apt update
apt install nginx
```

---
## Security Patch Evaluation

Process for evaluating patches in isolated environments:

1. Monitor CVE databases on connected systems
1. Assess relevance to air-gapped environment
1. Download and test patches in staging
1. Document patch impact analysis
1. Transfer through approved mechanism
1. Apply in maintenance window

```bash
# Check installed package versions
dpkg -l | grep <package>

# Check for known vulnerabilities
apt-get changelog <package>
```

---
## CVE Monitoring for Air-Gapped Systems

```bash
# On connected system: check Ubuntu CVE tracker
# https://ubuntu.com/security/cves

# Download CVE database for offline use
wget https://cve.mitre.org/data/downloads/allitems.csv.gz

# Check specific package vulnerabilities
apt-get changelog openssl | grep CVE

# Ubuntu Security Notices (USN)
# Subscribe to ubuntu-security-announce mailing list

# Generate report of installed package versions
dpkg -l > installed_packages_$(date +%F).txt

# Compare against vulnerability database offline
# Map installed versions to known CVEs
```

---
## Update Verification Procedures

```bash
# Verify package signatures
dpkg-sig --verify package.deb

# Verify GPG signatures
gpg --verify package.deb.sig package.deb

# Compare checksums against published values
sha256sum -c SHA256SUMS

# Test in staging environment first
# Use LVM snapshots for rollback capability
lvcreate -L 5G -s -n pre-update-snap \
  /dev/vg/root
```

---
## System Update Protocols

1. **Pre-update**: snapshot, backup, document current state
1. **Staging**: apply updates to test environment
1. **Validation**: run test suite, verify services
1. **Approval**: change control board sign-off
1. **Production**: apply during maintenance window
1. **Post-update**: verify all services, update docs

```bash
# Document current state
dpkg --get-selections > package-list-before.txt
systemctl list-units --state=running > \
  services-before.txt
```

---
## Update Rollback Procedures

```bash
# Pre-update: create LVM snapshot
lvcreate -L 10G -s -n pre-update /dev/vg/root

# If update fails: rollback
lvconvert --merge /dev/vg/pre-update
reboot

# Package-level rollback
apt install package=<previous-version>

# Keep old .deb files for rollback
apt-get install -d package   # download only
cp /var/cache/apt/archives/package_old.deb /backup/

# Compare before/after
diff package-list-before.txt package-list-after.txt
```

---
## Vulnerability Management

- Maintain an offline CVE database
- Regular vulnerability scanning with offline tools

```bash
# OpenSCAP for compliance scanning
apt install libopenscap8 ssg-base

# Run SCAP scan
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results results.xml \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml

# Generate HTML report
oscap xccdf generate report results.xml > report.html
```

---
## Compliance Scanning Deep Dive

```bash
# CIS Benchmark scanning
oscap xccdf eval \
  --profile cis_level1_server \
  --results results.xml \
  --report report.html \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml

# View available profiles
oscap info /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml

# Remediate findings automatically (use with caution)
oscap xccdf eval \
  --remediate \
  --profile cis_level1_server \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml

# Lynis - system security auditing
apt install lynis
lynis audit system
```

---
## Documentation and Emergency Procedures

Required documentation:
- Hardware and software inventory
- Network diagrams (even if isolated)
- Approved software baseline
- Update procedures and change logs
- Emergency contact list
- Disaster recovery runbooks

Emergency procedures:
- Known-good system image backups
- Boot media with rescue tools
- Documented rollback procedures
- Offline diagnostic tools and manuals

---
## Configuration Management in Air-Gapped Environments

```bash
# Use Ansible in pull mode (no network needed)
# Store playbooks on local git server

# Local git repository
git init --bare /opt/ansible-repo.git

# Ansible pull (runs from local repo)
ansible-pull -U file:///opt/ansible-repo.git \
  -i localhost, playbook.yml

# Version control all configs
etckeeper init
etckeeper commit "Initial config"

# Track changes over time
cd /etc
git log --oneline
git diff HEAD~1
```

---
## Media Transfer Security

```bash
# Scan removable media before use
clamscan -r /media/usb/

# Write-protect media after preparation
# Use hardware write-protect switches on USB drives

# Log all media transfers
echo "$(date) - Transfer USB-001 - alice - \
  nginx update packages" >> /var/log/media-transfers.log

# Wipe media after use
shred -vfz -n 3 /dev/sdb

# Encrypted transfers
gpg --encrypt --recipient admin@example.com \
  packages.tar.gz
```

---
## Best Practices for Isolated Systems

1. Maintain a complete software baseline document
1. Use configuration management (`Ansible` with local control)
1. Implement file integrity monitoring (`AIDE`)
1. Regular backup and restore testing
1. Strict change control processes
1. Audit all media transfers
1. Keep offline copies of critical documentation
1. Test all updates in staging before production
1. Maintain spare hardware for critical components
1. Regular security assessments with offline tools

---
## Air-Gap Network Architecture

![air_gap_network_architecture](svg/courses/operating_systems/linux-system-administration/13_airgapped_optional/air_gap_network_architecture.svg)

---
## Offline Container Registry

Run a private container registry inside the air-gapped network:

```bash
# On connected system: pull and save images
docker pull nginx:1.25
docker pull postgres:16
docker save nginx:1.25 postgres:16 > images.tar

# Transfer images.tar via approved media

# On air-gapped system: load images
docker load < images.tar

# Run a local registry
docker run -d -p 5000:5000 --restart=always \
  --name registry registry:2

# Tag and push to local registry
docker tag nginx:1.25 localhost:5000/nginx:1.25
docker push localhost:5000/nginx:1.25

# Configure clients to use local registry
# /etc/docker/daemon.json
```

```json
{
  "insecure-registries": ["registry.local:5000"]
}
```

---
## Offline Ansible Management

```bash
# On connected system: download Ansible and deps
pip download ansible -d /media/transfer/ansible-pkgs/

# Transfer to air-gapped system
pip install --no-index \
  --find-links=/media/usb/ansible-pkgs/ ansible

# Download Ansible collections offline
ansible-galaxy collection download \
  community.general -p /media/transfer/collections/

# Install collections on air-gapped system
ansible-galaxy collection install \
  -p /opt/ansible/collections \
  /media/usb/collections/community-general-*.tar.gz

# Run playbooks from local git repo
ansible-pull -U file:///opt/ansible-repo.git \
  -i inventory.yml site.yml

# Schedule with cron for drift correction
# 0 */4 * * * ansible-pull -U file:///opt/ansible-repo.git site.yml
```

---
## Hardware Security Modules in Air-Gapped Systems

`HSM` devices provide tamper-proof key storage:

```bash
# List available PKCS#11 tokens
pkcs11-tool --list-slots

# Generate a key pair on the HSM
pkcs11-tool --module /usr/lib/libsofthsm2.so \
  --keypairgen --key-type rsa:2048 \
  --label "signing-key"

# Sign packages with HSM-stored key
gpg --card-status
gpg --sign --local-user HSM-KEY-ID package.deb

# Use HSM for SSH authentication
ssh-keygen -D /usr/lib/libsofthsm2.so
# Add the public key to authorized_keys
```

Use cases in air-gapped environments:
- Package signing and verification
- Disk encryption key management (`LUKS`)
- TLS certificate management for internal services
- Secure boot key storage

---
## Audit Trail and Chain of Custody

```bash
# Enable comprehensive auditd logging
apt install auditd

# Track all file changes in critical paths
auditctl -w /etc -p wa -k etc-changes
auditctl -w /usr/bin -p wa -k binary-changes

# Log all media mount events
auditctl -a always,exit -F arch=b64 \
  -S mount -k media-mount

# Search audit logs
ausearch -k media-mount --start today
aureport --file --summary
```

Maintain a transfer log for every media crossing the air gap:

| Field | Example |
|-------|---------|
| Date/time | 2026-03-24 14:30 |
| Operator | alice |
| Media ID | USB-0042 |
| Contents | nginx 1.25 security patch |
| Source hash | `sha256:a1b2c3...` |
| Approved by | bob (ticket #1234) |

---
## USB Device Policy Enforcement

Control which USB devices are allowed in the air-gapped environment:

```bash
# Block all USB storage by default
echo 'blacklist usb-storage' > \
  /etc/modprobe.d/usb-storage.conf
update-initramfs -u

# Use udev rules for fine-grained control
# /etc/udev/rules.d/99-usb-policy.rules
# Allow only specific approved USB drives by serial
ACTION=="add", SUBSYSTEM=="block", \
  ENV{ID_SERIAL_SHORT}!="APPROVED001|APPROVED002", \
  ATTR{removable}=="1", \
  RUN+="/bin/sh -c 'echo 1 > /sys$devpath/device/delete'"
```

```bash
# Log all USB device connections
# /etc/udev/rules.d/98-usb-logging.rules
ACTION=="add", SUBSYSTEM=="usb", \
  RUN+="/usr/local/bin/log-usb.sh '%E{ID_VENDOR}' \
  '%E{ID_SERIAL_SHORT}'"

# USBGuard for comprehensive USB device control
apt install usbguard
usbguard generate-policy > /etc/usbguard/rules.conf
systemctl enable usbguard

# List connected devices and their policy
usbguard list-devices
# Allow a specific device
usbguard allow-device 12
```

---
## Network Diode Configuration

A data diode enforces one-way data flow at the hardware level:

```bash
# Software-based one-way transfer using UDP
# Sender side (internet zone)
tar czf - /opt/packages/ | \
  socat - UDP-SENDTO:diode-ip:9999

# Receiver side (air-gapped zone)
socat UDP-RECV:9999 - | tar xzf - -C /opt/incoming/
```

Design principles for diode configurations:
- Hardware diodes physically cut the return fiber/wire
- Software diodes use `iptables` with strict one-way rules
- Always verify integrity of received data with checksums

```bash
# iptables one-way rule (software diode)
# On the transfer gateway:
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -j DROP

# Verify no return traffic is possible
iptables -L FORWARD -n -v
```

Data diodes are required in many compliance frameworks (`NIST`, `IEC 62443`).

---
## Offline Monitoring Tools

Monitor air-gapped systems without external connectivity:

```bash
# Prometheus + Grafana running locally
# Pull metrics from local exporters only

# Node exporter for system metrics
apt install prometheus-node-exporter
systemctl enable prometheus-node-exporter

# Local Prometheus configuration
# /etc/prometheus/prometheus.yml
```

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'nodes'
    static_configs:
      - targets:
        - 'localhost:9100'
        - '10.0.0.2:9100'
        - '10.0.0.3:9100'
```

```bash
# AIDE for file integrity monitoring
apt install aide
aide --init
mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
# Run daily check via cron
aide --check

# Collect logs centrally with rsyslog
# /etc/rsyslog.d/50-central.conf
# *.* @logserver.local:514
```

---
## Exercise: Air-Gapped Package Update Pipeline

Build a complete offline update workflow:

1. On the connected staging system:

```bash
# Download a specific security update with deps
apt-get download -o \
  Dir::Cache::archives=/tmp/transfer openssl
apt-rdepends openssl | grep -v "^ " | \
  xargs apt-get download -o \
  Dir::Cache::archives=/tmp/transfer
```

1. Generate integrity manifests:

```bash
cd /tmp/transfer
sha256sum *.deb > SHA256SUMS
gpg --sign SHA256SUMS
```

1. Transfer to air-gapped system via approved USB
1. On the air-gapped system, verify and install:

```bash
gpg --verify SHA256SUMS.gpg SHA256SUMS
sha256sum -c SHA256SUMS
dpkg -i *.deb
```

1. Verify the update was applied:

```bash
dpkg -l openssl
openssl version
```

1. Document the transfer in the audit log with date, operator, media ID, and approval ticket number
