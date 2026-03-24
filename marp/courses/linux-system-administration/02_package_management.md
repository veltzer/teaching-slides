# Package Management Deep Dive
## apt, dpkg, dnf, rpm, Repositories, and Source Builds

---
## Why Package Management Matters

- Consistent software installation and removal
- Automatic dependency resolution
- Security updates and patch management
- Reproducible system configuration
- Audit trail of installed software

Without package management:
- Manual dependency tracking
- No clean uninstall
- No automatic security updates
- Difficult to reproduce environments

---
## Package Management Ecosystem

<svg width="650" height="180" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="250" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="175" y="35" text-anchor="middle" font-size="12">Debian / Ubuntu</text>
  <rect x="350" y="10" width="250" height="40" fill="#fce4ec" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="35" text-anchor="middle" font-size="12">RHEL / Fedora</text>
  <rect x="70" y="70" width="90" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="115" y="93" text-anchor="middle" font-size="10">apt</text>
  <rect x="190" y="70" width="90" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="235" y="93" text-anchor="middle" font-size="10">dpkg</text>
  <rect x="370" y="70" width="90" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="415" y="93" text-anchor="middle" font-size="10">dnf/yum</text>
  <rect x="490" y="70" width="90" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="535" y="93" text-anchor="middle" font-size="10">rpm</text>
  <rect x="70" y="125" width="90" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="115" y="148" text-anchor="middle" font-size="10">.deb files</text>
  <rect x="370" y="125" width="90" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="415" y="148" text-anchor="middle" font-size="10">.rpm files</text>
  <text x="175" y="65" text-anchor="middle" font-size="9">High-level</text>
  <text x="475" y="65" text-anchor="middle" font-size="9">High-level</text>
  <line x1="115" y1="105" x2="115" y2="125" stroke="#333" stroke-width="1"/>
  <line x1="235" y1="105" x2="175" y2="125" stroke="#333" stroke-width="1"/>
  <line x1="415" y1="105" x2="415" y2="125" stroke="#333" stroke-width="1"/>
  <line x1="535" y1="105" x2="475" y2="125" stroke="#333" stroke-width="1"/>
</svg>

- `apt`/`dnf` are high-level: resolve dependencies, manage repos
- `dpkg`/`rpm` are low-level: install/remove individual packages

---
## dpkg: Low-Level Package Tool

```bash
# Install a .deb package
dpkg -i package.deb

# Remove a package (keep config)
dpkg -r nginx

# Remove with config (purge)
dpkg -P nginx

# List all installed packages
dpkg -l
dpkg -l | grep nginx

# List files installed by a package
dpkg -L nginx

# Find which package owns a file
dpkg -S /usr/sbin/nginx

# Show package info
dpkg -s nginx
```

---
## dpkg Advanced Usage

```bash
# Extract package without installing
dpkg -x package.deb /tmp/extracted/

# Extract control information
dpkg -e package.deb /tmp/control/

# View package contents without extracting
dpkg -c package.deb

# Reconfigure a package
dpkg-reconfigure tzdata
dpkg-reconfigure locales

# List packages in a specific state
dpkg -l | grep '^rc'    # removed but config remains
dpkg -l | grep '^iU'    # installed, needs update

# Fix interrupted installations
dpkg --configure -a
```

---
## Understanding dpkg Package States

```bash
# dpkg -l output format:
# Desired=Unknown/Install/Remove/Purge/Hold
# | Status=Not/Inst/Conf-files/Unpacked/Failed-cfg
# |/ Err?=(none)/Reinst-required
# ||/ Name    Version    Description
# ii  nginx   1.24.0-1   web server    (installed OK)
# rc  apache  2.4.58-1   web server    (removed, config left)
# hi  mysql   8.0.35-1   database      (hold, installed)
```

| Code | Meaning |
|------|---------|
| `ii` | Installed, OK |
| `rc` | Removed, config files remain |
| `un` | Unknown, not installed |
| `hi` | Hold, installed |
| `iU` | Installed, unpacked (needs configure) |

---
## apt: High-Level Package Tool

```bash
# Update package lists (always do first)
apt update

# Install a package
apt install nginx

# Install multiple packages
apt install nginx certbot python3-pip

# Remove a package (keep config)
apt remove nginx

# Remove with config
apt purge nginx

# Search for packages
apt search "web server"

# Show package details
apt show nginx

# List installed packages
apt list --installed
```

---
## apt Install Options

```bash
# Install specific version
apt install nginx=1.24.0-1ubuntu1

# Install without recommended packages
apt install --no-install-recommends nginx

# Simulate install (dry run)
apt install -s nginx

# Download only (don't install)
apt install -d nginx

# Reinstall a package
apt install --reinstall nginx

# Install from a .deb file (with dependency resolution)
apt install ./package.deb

# Answer yes to all prompts
apt install -y nginx
```

---
## apt Upgrade and Maintenance

```bash
# Upgrade all packages
apt upgrade

# Full upgrade (may remove packages if needed)
apt full-upgrade

# Remove unused dependencies
apt autoremove

# Clean package cache
apt clean             # remove all cached packages
apt autoclean         # remove only obsolete cache

# Check for broken dependencies
apt check

# Fix broken dependencies
apt --fix-broken install
apt install -f

# List upgradable packages
apt list --upgradable
```

---
## apt-mark: Managing Package State

```bash
# Hold a package (prevent upgrades)
apt-mark hold nginx
apt-mark unhold nginx

# Show held packages
apt-mark showhold

# Mark as manually installed
apt-mark manual nginx

# Mark as automatically installed (eligible for autoremove)
apt-mark auto libfoo

# List manually installed packages
apt-mark showmanual

# Show automatic packages
apt-mark showauto
```

Holding packages is critical for production systems where you need to control when specific packages get upgraded.

---
## apt-cache: Querying Package Information

```bash
# Search package descriptions
apt-cache search "web server"

# Show package details
apt-cache show nginx

# Show package dependencies
apt-cache depends nginx

# Show reverse dependencies (what depends on it)
apt-cache rdepends nginx

# Show available versions
apt-cache showpkg nginx

# Show installation policy (which repo)
apt-cache policy nginx

# Show package statistics
apt-cache stats
```

---
## apt-file: Finding Files in Packages

```bash
# Install apt-file
apt install apt-file
apt-file update

# Find which package contains a file
apt-file search /usr/bin/htop
apt-file search libssl.so

# List files in a package (even if not installed)
apt-file list nginx

# Search with regex
apt-file search --regexp 'bin/python3\.'

# Find packages providing a command
apt-file search --regexp 'bin/dig$'
```

This is invaluable when you get "command not found" or "library not found" errors.

---
## Repository Configuration (Debian/Ubuntu)

```bash
# Modern format: /etc/apt/sources.list.d/
cat /etc/apt/sources.list.d/ubuntu.sources
```

```txt
# DEB822 format (modern Ubuntu 24.04+)
Types: deb deb-src
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```txt
# One-line format (legacy)
deb http://archive.ubuntu.com/ubuntu noble main restricted
deb-src http://archive.ubuntu.com/ubuntu noble main restricted
```

Components: `main` (supported), `restricted` (proprietary drivers), `universe` (community), `multiverse` (non-free).

---
## Adding Third-Party Repositories

```bash
# Modern approach (apt-key is deprecated)
# Step 1: Download and store GPG key
curl -fsSL https://example.com/gpg.key | \
  gpg --dearmor -o /usr/share/keyrings/example.gpg

# Step 2: Add repository with key reference
echo "deb [signed-by=/usr/share/keyrings/example.gpg] \
  https://repo.example.com/ubuntu noble main" > \
  /etc/apt/sources.list.d/example.list

# Step 3: Update and install
apt update
apt install example-package
```

```bash
# Add a PPA (Ubuntu shortcut)
add-apt-repository ppa:some/ppa
apt update

# Remove a PPA
add-apt-repository --remove ppa:some/ppa
```

---
## Repository Pinning and Priorities

```bash
# /etc/apt/preferences.d/pin-nginx.pref
```

```txt
# Pin nginx from a specific repo
Package: nginx
Pin: origin repo.example.com
Pin-Priority: 900

# Block a package from upgrading
Package: mysql-server
Pin: release *
Pin-Priority: -1

# Prefer packages from backports
Package: *
Pin: release a=noble-backports
Pin-Priority: 400
```

| Priority | Behavior |
|----------|----------|
| < 0 | Never install |
| 0-99 | Install only if not installed |
| 100-499 | Install if newer than current |
| 500-999 | Preferred |
| >= 1000 | Force downgrade if needed |

---
## Package Management: dnf (RHEL/Fedora)

```bash
# Install
dnf install httpd

# Remove
dnf remove httpd

# Search
dnf search "web server"

# List installed packages
dnf list installed

# Show package info
dnf info httpd

# Check for updates
dnf check-update

# Upgrade all
dnf upgrade

# Upgrade specific package
dnf upgrade httpd

# History of transactions
dnf history
dnf history info 15
```

---
## dnf Advanced Usage

```bash
# Install from specific repo
dnf install --repo=epel htop

# Download only
dnf download httpd

# Download with dependencies
dnf download --resolve httpd

# Group operations
dnf group list
dnf group install "Development Tools"

# List available modules
dnf module list
dnf module enable nodejs:18
dnf module install nodejs:18

# Rollback a transaction
dnf history undo 15

# Clean cache
dnf clean all
```

---
## rpm: Low-Level Package Tool

```bash
# Install
rpm -ivh package.rpm

# Upgrade (install or upgrade)
rpm -Uvh package.rpm

# Remove
rpm -e httpd

# Query installed package
rpm -qi httpd           # info
rpm -ql httpd           # list files
rpm -qc httpd           # config files only
rpm -qd httpd           # documentation files only

# Query uninstalled .rpm file
rpm -qip package.rpm    # info
rpm -qlp package.rpm    # list files

# Find which package owns a file
rpm -qf /usr/sbin/httpd
```

---
## rpm Verification and Security

```bash
# Verify installed package
rpm -V httpd
# Output codes:
# S - Size, M - Mode, 5 - MD5, D - Device
# L - Link, U - User, G - Group, T - Time

# Verify all packages
rpm -Va

# Check package signature
rpm --checksig package.rpm

# Import GPG key
rpm --import https://example.com/RPM-GPG-KEY

# List imported keys
rpm -qa gpg-pubkey*

# Rebuild RPM database
rpm --rebuilddb
```

---
## Repository Configuration (RHEL/Fedora)

```ini
# /etc/yum.repos.d/custom.repo
[custom-repo]
name=Custom Repository
baseurl=https://repo.example.com/el9/$basearch/
enabled=1
gpgcheck=1
gpgkey=https://repo.example.com/RPM-GPG-KEY
sslverify=1
metadata_expire=86400
priority=10
```

```bash
# List configured repos
dnf repolist all

# Enable/disable repos
dnf config-manager --set-enabled custom-repo
dnf config-manager --set-disabled custom-repo

# Add EPEL repository
dnf install epel-release
```

---
## Creating Custom Repositories

```bash
# Debian/Ubuntu: create a local repo
mkdir -p /opt/local-repo/pool
cp *.deb /opt/local-repo/pool/

# Generate package index
cd /opt/local-repo
dpkg-scanpackages pool /dev/null | \
  gzip > pool/Packages.gz

# Add to sources
echo "deb [trusted=yes] file:///opt/local-repo pool/" \
  > /etc/apt/sources.list.d/local.list
apt update
```

```bash
# RHEL: create a local repo
dnf install createrepo_c
mkdir -p /opt/local-repo
cp *.rpm /opt/local-repo/
createrepo /opt/local-repo/
```

---
## Hosting a Repository with a Web Server

```bash
# Debian repo with apt-ftparchive
mkdir -p /var/www/repo/{pool,dists/stable/main/binary-amd64}
cp *.deb /var/www/repo/pool/

apt-ftparchive packages pool/ > \
  dists/stable/main/binary-amd64/Packages
gzip -k dists/stable/main/binary-amd64/Packages

apt-ftparchive release dists/stable/ > \
  dists/stable/Release

# Sign the release
gpg --armor --detach-sign -o dists/stable/Release.gpg \
  dists/stable/Release
gpg --armor --clearsign -o dists/stable/InRelease \
  dists/stable/Release
```

Serve via `nginx` or `Apache` at `http://repo.example.com/`.

---
## Building Software from Source

```bash
# Typical build process
wget https://example.com/software-1.0.tar.gz
tar xzf software-1.0.tar.gz
cd software-1.0

# Configure, compile, install
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install

# Install build dependencies (Debian)
apt install build-essential

# Use checkinstall to create a .deb
sudo checkinstall
```

---
## Managing Source Builds

```bash
# Install build dependencies for a package
apt build-dep nginx

# Rebuild a Debian package from source
apt source nginx
cd nginx-*/
dpkg-buildpackage -us -uc

# CMake-based builds
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j$(nproc)
sudo make install

# Using GNU stow for clean management
sudo make install DESTDIR=/usr/local/stow/myapp-1.0
cd /usr/local/stow
sudo stow myapp-1.0
```

---
## Building .deb Packages

```bash
# Create package directory structure
mkdir -p myapp-1.0/DEBIAN
mkdir -p myapp-1.0/usr/local/bin
mkdir -p myapp-1.0/etc/myapp

# Copy files
cp myapp myapp-1.0/usr/local/bin/
cp config.yml myapp-1.0/etc/myapp/
```

```txt
# myapp-1.0/DEBIAN/control
Package: myapp
Version: 1.0
Architecture: amd64
Maintainer: Admin <admin@example.com>
Depends: libc6 (>= 2.35)
Description: My custom application
 A longer description of what myapp does.
```

```bash
# Build the package
dpkg-deb --build myapp-1.0
# Result: myapp-1.0.deb
```

---
## Package Scripts (Pre/Post Install/Remove)

```bash
# DEBIAN/preinst  - before install
# DEBIAN/postinst - after install
# DEBIAN/prerm    - before remove
# DEBIAN/postrm   - after remove
```

```bash
#!/bin/bash
# DEBIAN/postinst
set -e

case "$1" in
    configure)
        # Create service user
        useradd -r -s /usr/sbin/nologin myapp || true
        # Enable and start service
        systemctl daemon-reload
        systemctl enable myapp
        systemctl start myapp
        ;;
esac
```

```bash
# Make scripts executable
chmod 755 myapp-1.0/DEBIAN/postinst
```

---
## Package Verification and Security

```bash
# Verify GPG signatures (Debian)
apt-key list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>

# Modern key management
curl -fsSL https://example.com/gpg.key | \
  gpg --dearmor -o /usr/share/keyrings/example.gpg

# Verify package checksums
debsums nginx           # check installed files
debsums -c              # show only changed files
debsums -a              # check all packages

# Check package authenticity
apt-cache policy nginx   # shows origin repo
apt-cache showpkg nginx  # shows versions and repos
```

---
## Snap and Flatpak

Alternative package formats with sandboxing:

```bash
# Snap (Ubuntu/Canonical)
snap install firefox
snap list
snap refresh firefox
snap remove firefox
snap info firefox

# Flatpak (cross-distro)
apt install flatpak
flatpak remote-add --if-not-exists flathub \
  https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.gimp.GIMP
flatpak list
flatpak update
```

| Feature | apt/dnf | Snap | Flatpak |
|---------|---------|------|---------|
| Sandboxing | No | Yes | Yes |
| Auto-update | Configurable | Yes | Yes |
| Size | Small | Larger | Larger |
| System integration | Full | Limited | Limited |

---
## Package Management Best Practices

1. Always run `apt update` before installing
1. Use `apt-mark hold` for critical packages in production
1. Pin specific versions for reproducibility
1. Use `--no-install-recommends` for minimal installs
1. Regularly run `apt autoremove` and `apt autoclean`
1. Verify GPG keys before adding third-party repos
1. Test package upgrades in staging first
1. Keep a record of manually installed packages
1. Use `unattended-upgrades` for security patches
1. Monitor `/var/log/apt/history.log` for audit trail

```bash
# Export list of manually installed packages
apt-mark showmanual > packages.txt

# Recreate on another system
xargs apt install -y < packages.txt
```

---
## Troubleshooting Package Issues

```bash
# Fix "dpkg was interrupted"
dpkg --configure -a

# Fix broken dependencies
apt --fix-broken install

# Fix locked database
# Check if apt/dpkg is running
ps aux | grep -E 'apt|dpkg'
# If not, remove lock files
rm /var/lib/dpkg/lock-frontend
rm /var/lib/apt/lists/lock

# Reinstall corrupted package
apt install --reinstall nginx

# Force overwrite conflicting files (use with caution)
dpkg -i --force-overwrite package.deb

# Reset package to default config
dpkg-reconfigure nginx
```

---
## Dependency Hell: Causes and Solutions

Dependency conflicts arise when packages require incompatible library versions.

```bash
# Diagnose dependency issues
apt-cache depends --recurse nginx | grep "Depends:"
apt-cache policy libssl3

# Common scenario: package A needs libfoo >= 2.0,
# package B needs libfoo < 2.0

# Solutions:
# 1. Use apt to resolve automatically
apt --fix-broken install

# 2. Simulate to see what would change
apt install -s problematic-package

# 3. Check reverse dependencies before removing
apt-cache rdepends --installed libfoo

# 4. Pin a specific version
echo "Package: libfoo
Pin: version 1.9*
Pin-Priority: 1001" > /etc/apt/preferences.d/libfoo
```

---
## Setting Up an `apt` Caching Proxy

An `apt-cacher-ng` proxy saves bandwidth when multiple machines install the same packages.

```bash
# Install on the proxy server
apt install apt-cacher-ng

# Default port: 3142
systemctl enable --now apt-cacher-ng

# Web UI: http://proxy-server:3142/acng-report.html
```

```bash
# Configure clients to use the proxy
echo 'Acquire::http::Proxy "http://proxy-server:3142";' \
  > /etc/apt/apt.conf.d/02proxy

# Test
apt update  # packages fetched via proxy

# Check cache statistics
ls -lh /var/cache/apt-cacher-ng/
```

---
## `apt` Caching Proxy Diagram

<svg width="600" height="160" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="45" text-anchor="middle" font-size="10">Client A</text>
  <rect x="10" y="80" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="105" text-anchor="middle" font-size="10">Client B</text>
  <rect x="200" y="45" width="150" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="275" y="65" text-anchor="middle" font-size="10">apt-cacher-ng</text>
  <text x="275" y="80" text-anchor="middle" font-size="9">:3142</text>
  <rect x="440" y="45" width="140" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="65" text-anchor="middle" font-size="10">Ubuntu Archive</text>
  <text x="510" y="80" text-anchor="middle" font-size="9">archive.ubuntu.com</text>
  <line x1="110" y1="40" x2="200" y2="65" stroke="#333" stroke-width="1" marker-end="url(#arr02b)"/>
  <line x1="110" y1="100" x2="200" y2="75" stroke="#333" stroke-width="1" marker-end="url(#arr02b)"/>
  <line x1="350" y1="70" x2="440" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arr02b)"/>
  <text x="395" y="60" text-anchor="middle" font-size="8">cache miss</text>
  <defs>
    <marker id="arr02b" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- First client downloads the package from the internet
- Subsequent clients get the cached copy instantly
- Ideal for labs, CI/CD pipelines, and air-gapped staging

---
## Comparing Package Versions Across Systems

```bash
# Export installed packages from system A
dpkg --get-selections > system-a-packages.txt

# On system B, compare
dpkg --get-selections > system-b-packages.txt
diff system-a-packages.txt system-b-packages.txt

# More detailed: compare with versions
dpkg-query -W -f '${Package}\t${Version}\n' > versions-a.txt
# (repeat on system B)
diff versions-a.txt versions-b.txt
```

```bash
# Using apt-show-versions for upgrade candidates
apt install apt-show-versions
apt-show-versions -u          # upgradable packages
apt-show-versions | grep -v uptodate  # not up to date
```

---
## Unattended Upgrades for Security Patches

```bash
# Install
apt install unattended-upgrades

# Enable
dpkg-reconfigure -plow unattended-upgrades
```

```bash
# /etc/apt/apt.conf.d/50unattended-upgrades
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";
Unattended-Upgrade::Mail "admin@example.com";
```

```bash
# Test dry run
unattended-upgrades --dry-run --debug

# Check logs
cat /var/log/unattended-upgrades/unattended-upgrades.log
```

---
## `apt` Transaction Simulation

Always simulate before making changes in production.

```bash
# Simulate an install (shows what would change)
apt install -s nginx
apt install --simulate nginx

# Simulate a full upgrade
apt full-upgrade -s

# Simulate removal (check for collateral damage)
apt remove -s libssl3

# Check what autoremove would clean up
apt autoremove -s
```

Key output to watch:
- "NEW" packages that will be installed
- Packages that will be "REMOVED" (collateral)
- "kept back" packages (held or broken deps)
- Download size and disk space impact

---
## `dpkg` Triggers

Triggers allow packages to defer expensive operations until all related packages are configured.

```bash
# View pending triggers
dpkg --triggers-only -a

# Common triggers you'll encounter:
# - ldconfig: rebuilds shared library cache
# - update-initramfs: regenerates initramfs
# - man-db: rebuilds man page index
# - desktop-file-utils: updates desktop database
```

```bash
# List trigger interests for a package
dpkg -s man-db | grep -i trigger

# Manually process pending triggers
dpkg --configure --pending

# If triggers are stuck, force processing
dpkg --configure -a --force-triggers
```

Triggers explain why `apt install` sometimes runs `update-initramfs` or `ldconfig` at the end.

---
## Package Downgrade Procedures

Rolling back to a previous package version when an upgrade causes issues:

```bash
# List available versions of a package
apt-cache madison nginx
apt list -a nginx

# Downgrade to a specific version
apt install nginx=1.22.1-1ubuntu1

# Hold the package to prevent re-upgrade
apt-mark hold nginx

# For dpkg, install an older .deb directly
dpkg -i nginx_1.22.1-1ubuntu1_amd64.deb
apt --fix-broken install  # resolve deps

# Download a specific version without installing
apt download nginx=1.22.1-1ubuntu1
```

```bash
# On RHEL/Fedora, use dnf history
dnf history list
dnf history undo 25   # revert transaction 25
dnf downgrade httpd-2.4.51
```

---
## Comparing `apt` vs `dnf` Side by Side

| Task | `apt` (Debian/Ubuntu) | `dnf` (RHEL/Fedora) |
|------|----------------------|---------------------|
| Update metadata | `apt update` | `dnf check-update` |
| Install | `apt install pkg` | `dnf install pkg` |
| Remove | `apt remove pkg` | `dnf remove pkg` |
| Search | `apt search text` | `dnf search text` |
| Upgrade all | `apt upgrade` | `dnf upgrade` |
| Show info | `apt show pkg` | `dnf info pkg` |
| List files | `dpkg -L pkg` | `rpm -ql pkg` |
| File owner | `dpkg -S /path` | `rpm -qf /path` |
| Clean cache | `apt clean` | `dnf clean all` |
| History | `/var/log/apt/history.log` | `dnf history` |
| Hold pkg | `apt-mark hold pkg` | `dnf versionlock pkg` |

---
## Virtual Packages

Virtual packages are not real packages but represent a capability that multiple packages can provide.

```bash
# Example: "mail-transport-agent" is virtual
apt-cache showpkg mail-transport-agent
# Provided by: postfix, exim4, sendmail, etc.

# See what provides a virtual package
apt-cache show mail-transport-agent 2>&1 | head -5

# Install any provider
apt install postfix
# This satisfies any dependency on "mail-transport-agent"
```

Common virtual packages:
- `mail-transport-agent` - MTA (postfix, exim4)
- `httpd` - web server (apache2, nginx)
- `java-runtime` - JRE (openjdk, default-jre)
- `awk` - awk implementation (gawk, mawk)
- `editor` - text editor (vim, nano)

---
## Essential Packages

Essential packages cannot be removed without the `--force-remove-essential` flag. They are critical for system operation.

```bash
# List essential packages
dpkg-query -W -f='${Package} ${Essential}\n' | grep yes

# Typical essential packages include:
# base-files, base-passwd, bash, coreutils,
# dash, debianutils, diffutils, dpkg, findutils,
# grep, gzip, libc-bin, login, sed, tar, util-linux
```

```bash
# Attempting to remove an essential package
apt remove coreutils
# "WARNING: The following essential packages will be removed"
# "This should NOT be done unless you know exactly what you are doing!"

# Protected packages (Priority: required/important)
apt-cache show dpkg | grep Priority
```

Never remove essential packages on a production system.

---
## Package Lifecycle

<svg width="650" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="70" y="55" text-anchor="middle" font-size="10">Available</text>
  <rect x="160" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="210" y="55" text-anchor="middle" font-size="10">Downloaded</text>
  <rect x="300" y="30" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="350" y="55" text-anchor="middle" font-size="10">Unpacked</text>
  <rect x="440" y="30" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="55" text-anchor="middle" font-size="10">Configured</text>
  <rect x="300" y="120" width="100" height="40" fill="#fce4ec" stroke="#333" stroke-width="2" rx="5"/>
  <text x="350" y="145" text-anchor="middle" font-size="10">Removed</text>
  <rect x="440" y="120" width="100" height="40" fill="#ffcdd2" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="145" text-anchor="middle" font-size="10">Purged</text>
  <line x1="120" y1="50" x2="160" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#arr02c)"/>
  <line x1="260" y1="50" x2="300" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#arr02c)"/>
  <line x1="400" y1="50" x2="440" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#arr02c)"/>
  <line x1="490" y1="70" x2="490" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arr02c)"/>
  <line x1="400" y1="140" x2="440" y2="140" stroke="#333" stroke-width="1.5" marker-end="url(#arr02c)"/>
  <text x="140" y="42" font-size="8">fetch</text>
  <text x="280" y="42" font-size="8">unpack</text>
  <text x="420" y="42" font-size="8">configure</text>
  <text x="500" y="100" font-size="8">remove</text>
  <text x="420" y="132" font-size="8">purge</text>
  <defs>
    <marker id="arr02c" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- **Available**: in repository, not installed
- **Downloaded**: `.deb` cached in `/var/cache/apt/archives/`
- **Unpacked**: files extracted, not yet configured
- **Configured**: post-install scripts run, service ready
- **Removed**: binaries gone, config files remain
- **Purged**: all files including config removed

---
## Exercise: Package Management Scenarios

1. Simulate installing `postgresql` and note all dependencies that would be added
1. Install `nginx`, then downgrade it to the previous available version and hold it
1. Find which package provides the file `/usr/bin/curl`
1. Create a local `apt` repository in `/opt/local-repo` with at least one `.deb` file
1. Compare the installed packages on your system with a fresh `packages.txt` export
1. Use `debsums` to verify the integrity of the `openssh-server` package files

```bash
# Helpful commands
apt install -s postgresql
apt-cache madison nginx
dpkg -S /usr/bin/curl
debsums openssh-server
```

Practice the full package lifecycle: install, verify, hold, downgrade, remove, and purge.

---
## Package Changelog and History

```bash
# View changelog for a package
apt changelog nginx

# Review apt history (what was installed/removed and when)
cat /var/log/apt/history.log
# Older logs are compressed
zcat /var/log/apt/history.log.*.gz

# Review dpkg-level log (more granular)
cat /var/log/dpkg.log
grep " install " /var/log/dpkg.log | tail -20
grep " remove " /var/log/dpkg.log | tail -20
```

```bash
# Find when a specific package was installed
grep nginx /var/log/dpkg.log

# On RHEL/Fedora, use dnf history
dnf history
dnf history info 15
```

Regularly reviewing package logs helps with auditing and troubleshooting.

---
## Debian Package Internals

A `.deb` file is an `ar` archive containing two compressed tarballs.

```bash
# View the ar archive structure
ar t package.deb
# debian-binary     (format version: "2.0")
# control.tar.zst   (metadata, scripts)
# data.tar.zst      (actual files)

# Extract manually without dpkg
ar x package.deb
tar xf control.tar.zst
tar xf data.tar.zst

# Inspect control file contents
cat control    # package name, version, depends
cat md5sums    # checksums for installed files
cat postinst   # post-installation script
```

```bash
# View contents without extracting
dpkg -c package.deb     # list files in data.tar
dpkg -I package.deb     # show control information
```

Understanding internals helps when debugging broken packages or building custom ones.

---
## apt Proxy and Offline Install

For disconnected or air-gapped systems, use `apt-offline` to download packages on a connected machine and transfer them.

```bash
# On the disconnected machine: generate a signature
apt-offline set offline-sig.sig --update
apt-offline set offline-sig.sig --install-packages nginx

# Transfer offline-sig.sig to a connected machine

# On the connected machine: download the packages
apt-offline get offline-sig.sig --bundle bundle.zip

# Transfer bundle.zip back to the disconnected machine

# On the disconnected machine: install the bundle
apt-offline install bundle.zip
apt install nginx
```

```bash
# Alternative: download .deb files manually
apt download nginx
apt-cache depends --recurse --no-recommends \
  --no-suggests --no-conflicts nginx | \
  grep "^\w" | sort -u | xargs apt download

# Copy .deb files to target and install
dpkg -i *.deb
apt --fix-broken install
```

---
## Package Management Automation

Automate package operations in scripts using `DEBIAN_FRONTEND=noninteractive` to suppress interactive prompts.

```bash
# Non-interactive install (no prompts)
export DEBIAN_FRONTEND=noninteractive
apt-get install -y nginx

# Pre-seed answers for debconf questions
echo "postfix postfix/main_mailer_type select Internet Site" | \
  debconf-set-selections
echo "postfix postfix/mailname string mail.example.com" | \
  debconf-set-selections
apt-get install -y postfix
```

```bash
# Scripting best practices
apt-get update -qq
apt-get install -y --no-install-recommends \
  nginx certbot python3-pip

# Check if a package is installed
dpkg -s nginx &>/dev/null && echo "installed"

# Idempotent install (only if missing)
dpkg -s nginx &>/dev/null || apt-get install -y nginx
```

Use `apt-get` instead of `apt` in scripts for stable, machine-readable output.
