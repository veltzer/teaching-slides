# Security and Compliance

---

## Security Overview

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="600" height="400" fill="#f5f5f5" stroke="#333" stroke-width="2"/>

  <rect x="150" y="100" width="200" height="70" fill="#ffcccc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="250" y="130" text-anchor="middle" font-size="12" font-weight="bold">Build Security</text>
  <text x="250" y="150" text-anchor="middle" font-size="10">Trusted sources</text>

  <rect x="450" y="100" width="200" height="70" fill="#ccffcc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="550" y="130" text-anchor="middle" font-size="12" font-weight="bold">System Hardening</text>
  <text x="550" y="150" text-anchor="middle" font-size="10">Attack surface</text>

  <rect x="150" y="220" width="200" height="70" fill="#ccccff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="250" y="250" text-anchor="middle" font-size="12" font-weight="bold">Secure Boot</text>
  <text x="250" y="270" text-anchor="middle" font-size="10">Chain of trust</text>

  <rect x="450" y="220" width="200" height="70" fill="#ffeecc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="550" y="250" text-anchor="middle" font-size="12" font-weight="bold">Runtime Security</text>
  <text x="550" y="270" text-anchor="middle" font-size="10">Monitoring</text>

  <rect x="250" y="340" width="300" height="70" fill="#ffffcc" stroke="#000" stroke-width="3" rx="5"/>
  <text x="400" y="375" text-anchor="middle" font-size="14" font-weight="bold">Secure Embedded System</text>

  <path d="M 250 170 L 350 340" stroke="#333" stroke-width="2" marker-end="url(#s1)"/>
  <path d="M 550 170 L 450 340" stroke="#333" stroke-width="2" marker-end="url(#s1)"/>
  <path d="M 250 290 L 350 340" stroke="#333" stroke-width="2" marker-end="url(#s1)"/>
  <path d="M 550 290 L 450 340" stroke="#333" stroke-width="2" marker-end="url(#s1)"/>

  <defs>
    <marker id="s1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Security Threats

Common attack vectors:
- Unauthorized access
- Code injection
- Buffer overflows
- Privilege escalation
- Network attacks
- Physical access
- Supply chain attacks

Defense strategy:
- Defense in depth
- Least privilege principle
- Secure by default
- Regular updates
- Monitoring and logging

---

## Security Features in Yocto

Built-in security features:

```bash
# In local.conf or distro config
DISTRO_FEATURES_append = " security"

# Core security features
DISTRO_FEATURES_append = " pam selinux smack apparmor"

# Additional hardening
EXTRA_IMAGE_FEATURES += "read-only-rootfs"

# Remove unnecessary features
DISTRO_FEATURES_remove = "x11 bluetooth"
```

---

## Minimal Attack Surface

Reduce image size:

```bash
# Start with minimal image
require recipes-core/images/core-image-minimal.bb

# Only essential packages
IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"

# Remove debug tools
EXTRA_IMAGE_FEATURES_remove = "debug-tweaks tools-debug"

# Disable unnecessary services
PACKAGECONFIG_remove_pn-systemd = "networkd resolved"
```

Size comparison:
- Full image: ~400MB
- Minimal image: ~10MB
- Custom secure: ~15-20MB

---

## User and Access Management

```bash
# Remove default users
EXTRA_USERS_PARAMS = "\
    userdel -r root; \
    "

# Create restricted users
EXTRA_USERS_PARAMS += "\
    useradd -p '' appuser; \
    usermod -L appuser; \
    "

# Disable root login
EXTRA_USERS_PARAMS += "\
    usermod -L root; \
    "

# SSH configuration
EXTRA_IMAGE_FEATURES_remove = "ssh-server-dropbear"
IMAGE_INSTALL_append = " openssh"
```

---

## Password Policies

Strong passwords:

```bash
# PAM configuration
IMAGE_INSTALL_append = " libpam"

# /etc/pam.d/common-password
recipes-core/base-files/base-files/common-password:
password requisite pam_pwquality.so retry=3 minlen=12 difok=3

# Password aging
EXTRA_USERS_PARAMS += "\
    chage -M 90 -m 7 -W 7 appuser; \
    "

# Account lockout
faillock --user appuser --reset
```

---

## Filesystem Security

Read-only root filesystem:

```bash
# In image recipe
EXTRA_IMAGE_FEATURES += "read-only-rootfs"

# Writable overlays
IMAGE_FEATURES_append = " overlayfs"

# Partition layout
part /boot --fstype=vfat --size=64M
part / --fstype=ext4 --size=2G --fsoptions=ro,nodev,noexec
part /var --fstype=ext4 --size=512M --fsoptions=nodev,nosuid
part /tmp --fstype=tmpfs --size=256M --fsoptions=nodev,nosuid,noexec
```

Mount options:

```bash
# /etc/fstab hardening
/dev/sda1 / ext4 ro,nodev,noexec 0 1
tmpfs /tmp tmpfs nodev,nosuid,noexec 0 0
tmpfs /var/tmp tmpfs nodev,nosuid,noexec 0 0
```

---

## Secure Boot Architecture

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="150" height="60" fill="#ffcccc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="175" y="85" text-anchor="middle" font-size="12" font-weight="bold">ROM Code</text>

  <rect x="325" y="50" width="150" height="60" fill="#ccffcc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="400" y="85" text-anchor="middle" font-size="12" font-weight="bold">U-Boot (Signed)</text>

  <rect x="550" y="50" width="150" height="60" fill="#ccccff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="625" y="85" text-anchor="middle" font-size="12" font-weight="bold">Kernel (Signed)</text>

  <rect x="100" y="200" width="150" height="60" fill="#ffeecc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="175" y="235" text-anchor="middle" font-size="12" font-weight="bold">RootFS (dmverity)</text>

  <rect x="325" y="200" width="150" height="60" fill="#eeccff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="400" y="235" text-anchor="middle" font-size="12" font-weight="bold">Applications</text>

  <rect x="550" y="200" width="150" height="60" fill="#ccffff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="625" y="235" text-anchor="middle" font-size="12" font-weight="bold">Secure Runtime</text>

  <path d="M 250 80 L 325 80" stroke="#00cc00" stroke-width="3" marker-end="url(#s2)"/>
  <path d="M 475 80 L 550 80" stroke="#00cc00" stroke-width="3" marker-end="url(#s2)"/>
  <path d="M 625 110 L 175 200" stroke="#00cc00" stroke-width="3" marker-end="url(#s2)"/>
  <path d="M 250 235 L 325 235" stroke="#00cc00" stroke-width="3" marker-end="url(#s2)"/>
  <path d="M 475 235 L 550 235" stroke="#00cc00" stroke-width="3" marker-end="url(#s2)"/>

  <text x="175" y="180" text-anchor="middle" font-size="10" fill="#00cc00">Verify</text>
  <text x="400" y="180" text-anchor="middle" font-size="10" fill="#00cc00">Verify</text>
  <text x="625" y="180" text-anchor="middle" font-size="10" fill="#00cc00">Verify</text>

  <defs>
    <marker id="s2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#00cc00"/>
    </marker>
  </defs>
</svg>

---

## Implementing Secure Boot

Key generation:

```bash
# Generate signing keys
openssl genrsa -out private.key 2048
openssl rsa -in private.key -pubout -out public.key

# Create signing certificate
openssl req -new -x509 -key private.key -out cert.crt
```

U-Boot signing:

```bash
# In u-boot recipe
UBOOT_SIGN_ENABLE = "1"
UBOOT_MKIMAGE_SIGN_ARGS = "-k /path/to/keys"

# FIT image configuration
KERNEL_CLASSES += "kernel-fitimage"
KERNEL_IMAGETYPE = "fitImage"
```

---

## dm-verity

Root filesystem verification:

```bash
# Enable dm-verity
IMAGE_CLASSES += "dm-verity-img"

# Generate hash tree
veritysetup format /dev/sda2 /dev/sda3

# Kernel cmdline
verity=/dev/sda2 verity_hash=/dev/sda3

# In image recipe
inherit dm-verity-img
DM_VERITY_IMAGE = "core-image-minimal"
DM_VERITY_IMAGE_TYPE = "ext4"
```

---

## Encryption

Full disk encryption:

```bash
# LUKS encryption
IMAGE_INSTALL_append = " cryptsetup"

# Setup encrypted partition
cryptsetup luksFormat /dev/sda3
cryptsetup luksOpen /dev/sda3 rootfs

# In initramfs
inherit image-live
INITRAMFS_IMAGE = "core-image-minimal-initramfs"
```

TPM integration:

```bash
# TPM support
IMAGE_INSTALL_append = " tpm2-tools tpm2-tss"

# Seal encryption key to TPM
tpm2_createprimary -C e -c primary.ctx
tpm2_create -C primary.ctx -i secret.key -u key.pub -r key.priv
tpm2_load -C primary.ctx -u key.pub -r key.priv -c key.ctx
```

---

## Network Security

Firewall configuration:

```bash
# iptables
IMAGE_INSTALL_append = " iptables"

# Default deny
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow specific services
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

---

## nftables

Modern firewall:

```bash
# Install nftables
IMAGE_INSTALL_append = " nftables"

# Configuration
recipes-connectivity/nftables/files/nftables.conf:
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        ct state established,related accept
        tcp dport 22 accept
        tcp dport 443 accept
    }
    chain forward {
        type filter hook forward priority 0; policy drop;
    }
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

---

## SELinux Integration

Enable SELinux:

```bash
# In distro config
DISTRO_FEATURES_append = " selinux"

# SELinux packages
IMAGE_INSTALL_append = " selinux-autorelabel"

# Policy type
PREFERRED_PROVIDER_virtual/refpolicy = "refpolicy-targeted"

# Kernel configuration
CONFIG_SECURITY_SELINUX=y
CONFIG_DEFAULT_SECURITY_SELINUX=y
```

SELinux modes:
- Enforcing: Blocks violations
- Permissive: Logs violations
- Disabled: No enforcement

---

## AppArmor

Alternative to SELinux:

```bash
# Enable AppArmor
DISTRO_FEATURES_append = " apparmor"

# Kernel config
CONFIG_SECURITY_APPARMOR=y
CONFIG_DEFAULT_SECURITY_APPARMOR=y

# Install profiles
IMAGE_INSTALL_append = " apparmor apparmor-profiles"

# Custom profile
/etc/apparmor.d/usr.bin.myapp:
#include <tunables/global>

/usr/bin/myapp {
    #include <abstractions/base>

    /usr/bin/myapp r,
    /etc/myapp/** r,
    /var/lib/myapp/** rw,
}
```

---

## SMACK

Simplified Mandatory Access Control:

```bash
# Enable SMACK
DISTRO_FEATURES_append = " smack"

# Kernel config
CONFIG_SECURITY_SMACK=y
CONFIG_DEFAULT_SECURITY_SMACK=y

# Label files
/usr/bin/myapp System::Privileged
/etc/myapp/* System::Config
/var/lib/myapp/* System::Data

# Access rules
System::Privileged System::Config r
System::Privileged System::Data rw
```

---

## CVE Tracking

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="180" height="70" fill="#ffcccc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="190" y="130" text-anchor="middle" font-size="12">CVE Database</text>
  <text x="190" y="150" text-anchor="middle" font-size="10">NVD, Mitre</text>

  <rect x="310" y="100" width="180" height="70" fill="#ccffcc" stroke="#000" stroke-width="2" rx="5"/>
  <text x="400" y="130" text-anchor="middle" font-size="12">CVE Check</text>
  <text x="400" y="150" text-anchor="middle" font-size="10">BitBake task</text>

  <rect x="520" y="100" width="180" height="70" fill="#ccccff" stroke="#000" stroke-width="2" rx="5"/>
  <text x="610" y="130" text-anchor="middle" font-size="12">Report</text>
  <text x="610" y="150" text-anchor="middle" font-size="10">Vulnerabilities</text>

  <rect x="250" y="250" width="300" height="80" fill="#ffffcc" stroke="#000" stroke-width="3" rx="5"/>
  <text x="400" y="285" text-anchor="middle" font-size="14" font-weight="bold">Patch/Update</text>

  <path d="M 280 135 L 310 135" stroke="#333" stroke-width="2" marker-end="url(#s3)"/>
  <path d="M 490 135 L 520 135" stroke="#333" stroke-width="2" marker-end="url(#s3)"/>
  <path d="M 610 170 L 400 250" stroke="#333" stroke-width="2" marker-end="url(#s3)"/>

  <defs>
    <marker id="s3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## CVE Checking in Yocto

Enable CVE checking:

```bash
# In local.conf
INHERIT += "cve-check"

# Update CVE database
bitbake -c fetch cve-update-db-native

# Check specific recipe
bitbake -c cve_check busybox

# Check all recipes
bitbake -k -c cve_check core-image-minimal
```

CVE report location:

```tree
tmp/deploy/cve/
├── core-image-minimal.cve
├── busybox.cve
└── openssl.cve
```

---

## CVE Patching

Apply CVE patches:

```bash
# In recipe
SRC_URI += "file://CVE-2023-1234.patch"

# Document CVE fix
CVE_CHECK_WHITELIST += "CVE-2023-1234"

# Version-specific patches
SRC_URI_append = " ${@bb.utils.contains('PV', '1.2.3', 'file://CVE-fix.patch', '', d)}"
```

Automated patching:

```bash
# Use devtool
devtool modify busybox
cd workspace/sources/busybox
git apply /path/to/CVE-patch
devtool update-recipe busybox
```

---

## License Compliance

License scanning:

```bash
# Generate license manifest
bitbake -c populate_lic core-image-minimal

# License report location
tmp/deploy/licenses/core-image-minimal/

# Check package licenses
bitbake -e busybox | grep ^LICENSE=
```

Compliance tracking:

```bash
# In local.conf
COPY_LIC_MANIFEST = "1"
COPY_LIC_DIRS = "1"

# Incompatible licenses
INCOMPATIBLE_LICENSE = "GPLv3 AGPL-3.0"
```

---

## SPDX Generation

Software Bill of Materials:

```bash
# Enable SPDX
INHERIT += "create-spdx"

# Generate SPDX documents
bitbake core-image-minimal

# SPDX location
tmp/deploy/spdx/

# SPDX format
IMAGE.spdx.json
package.spdx.json
```

SBOM analysis:

```bash
# Analyze dependencies
spdx-tools convert tmp/deploy/spdx/IMAGE.spdx.json

# Vulnerability scanning
grype sbom:tmp/deploy/spdx/IMAGE.spdx.json
```

---

## Supply Chain Security

Source verification:

```bash
# GPG signature verification
BB_SIGNATURE_HANDLER = "OEBasicHash"

# Download verification
SRC_URI[sha256sum] = "abc123..."
SRC_URI[md5sum] = "def456..."

# Git commit verification
SRCREV = "${AUTOREV}"
require recipes-kernel/linux/linux-yocto.inc
```

Trusted sources:

```bash
# Use specific mirrors
PREMIRRORS_prepend = "\
git://.*/.* https://trusted-mirror.com/git/MIRRORNAME \n \
"

# Disable untrusted sources
BB_ALLOWED_NETWORKS = "github.com gitlab.com trusted-mirror.com"
```

---

## Code Signing

Sign binaries:

```bash
# Install signing tools
IMAGE_INSTALL_append = " gnupg"

# Sign application
do_sign_binaries() {
    gpg --detach-sign ${D}${bindir}/myapp
}

addtask sign_binaries after do_install before do_package
```

Kernel module signing:

```bash
# Kernel config
CONFIG_MODULE_SIG=y
CONFIG_MODULE_SIG_ALL=y
CONFIG_MODULE_SIG_SHA256=y

# Signing key
MODSIGN_PRIVKEY = "/path/to/signing_key.priv"
MODSIGN_CERT = "/path/to/signing_key.x509"
```

---

## Runtime Security Monitoring

Intrusion detection:

```bash
# Install AIDE
IMAGE_INSTALL_append = " aide"

# Initialize database
aide --init
mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Check integrity
aide --check

# Update database
aide --update
```

Log monitoring:

```bash
# Install fail2ban
IMAGE_INSTALL_append = " fail2ban"

# Configuration
/etc/fail2ban/jail.local:
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

---

## Audit Framework

System auditing:

```bash
# Enable audit
IMAGE_INSTALL_append = " audit"

# Kernel config
CONFIG_AUDIT=y
CONFIG_AUDITSYSCALL=y

# Audit rules
/etc/audit/rules.d/audit.rules:
-w /etc/passwd -p wa -k passwd_changes
-w /etc/shadow -p wa -k shadow_changes
-w /usr/bin/ -p x -k binary_execution
-a always,exit -F arch=b64 -S execve -k exec
```

---

## Secure Communication

TLS/SSL configuration:

```bash
# Install OpenSSL
IMAGE_INSTALL_append = " openssl"

# Strong ciphers only
SSLCipherSuite HIGH:!aNULL:!MD5
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1

# Certificate management
recipes-connectivity/openssl/files/
├── server.crt
├── server.key
└── ca-bundle.crt
```

---

## VPN Integration

OpenVPN:

```bash
# Install OpenVPN
IMAGE_INSTALL_append = " openvpn"

# Configuration
/etc/openvpn/client.conf:
client
dev tun
proto udp
remote vpn.example.com 1194
ca ca.crt
cert client.crt
key client.key
cipher AES-256-CBC
```

WireGuard:

```bash
# Install WireGuard
IMAGE_INSTALL_append = " wireguard-tools"

# Configuration
/etc/wireguard/wg0.conf:
[Interface]
PrivateKey = <private-key>
Address = 10.0.0.2/24

[Peer]
PublicKey = <server-public-key>
Endpoint = vpn.example.com:51820
AllowedIPs = 10.0.0.0/24
```

---

## Hardening Checklist

System hardening:
- [ ] Minimal package installation
- [ ] Disable unnecessary services
- [ ] Read-only rootfs
- [ ] Secure boot enabled
- [ ] Strong passwords enforced
- [ ] Firewall configured
- [ ] SELinux/AppArmor enabled
- [ ] Latest security patches
- [ ] Encrypted storage
- [ ] Secure network protocols

Application hardening:
- [ ] Input validation
- [ ] Output encoding
- [ ] Memory safety
- [ ] Least privilege
- [ ] Secure defaults

---

## Security Testing

Penetration testing:

```bash
# Install testing tools
IMAGE_INSTALL_append = " nmap netcat"

# Port scanning
nmap -sV target-ip

# Vulnerability scanning
openvas-scanner
```

Fuzzing:

```bash
# AFL fuzzing
IMAGE_INSTALL_append = " afl"

# Fuzz application
afl-fuzz -i input/ -o output/ ./myapp @@
```

---

## Compliance Standards

Common standards:
- IEC 62443 (Industrial)
- ISO 27001 (Information Security)
- NIST Cybersecurity Framework
- CIS Benchmarks
- OWASP Guidelines
- PCI DSS (Payment)
- HIPAA (Healthcare)

Documentation requirements:
- Security architecture
- Threat model
- Risk assessment
- Incident response plan
- Audit logs

---

## Security Best Practices

Development:
- Security by design
- Threat modeling
- Code reviews
- Static analysis
- Security testing

Deployment:
- Least privilege
- Defense in depth
- Secure defaults
- Regular updates
- Monitoring and logging

Maintenance:
- Patch management
- Vulnerability scanning
- Security audits
- Incident response
- Continuous improvement

---

## Summary

Key security areas:
- Build security and supply chain
- System hardening and access control
- Secure boot and encryption
- Network security and firewalls
- Mandatory Access Control (MAC)
- CVE tracking and patching
- License compliance and SBOM

Best practices:
- Minimize attack surface
- Enable security features
- Regular security updates
- Continuous monitoring
- Compliance documentation
- Security testing and audits
