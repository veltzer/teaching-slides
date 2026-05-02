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
# The Debian Family: dpkg and apt

---
## apt &amp; dpkg Workflow

![apt_workflow](svg/courses/operating_systems/linux-package-managers/02_dpkg_and_apt/apt_workflow.svg)

---
## What Is a `.deb` File?

A `.deb` is the package format used by `Debian`, `Ubuntu`, `Mint`, `Raspbian`, `Kali`, and many derivatives.

```bash
# A .deb is just an ar archive
ar t nginx_1.24.0-1_amd64.deb
# debian-binary
# control.tar.zst
# data.tar.zst
```

- `debian-binary` — format version (always `2.0` in practice)
- `control.tar.*` — metadata: package name, version, dependencies, scripts
- `data.tar.*` — the actual files that will land on your disk

You can take a `.deb` apart with standard tools and no `dpkg` at all.

---
## Inspecting a `.deb` Without Installing It

```bash
# What package is this and what does it depend on?
dpkg -I nginx_1.24.0-1_amd64.deb

# What files would this package install?
dpkg -c nginx_1.24.0-1_amd64.deb

# Extract files to a directory (do not install)
dpkg -x nginx_1.24.0-1_amd64.deb /tmp/nginx-files/

# Extract control information
dpkg -e nginx_1.24.0-1_amd64.deb /tmp/nginx-control/
ls /tmp/nginx-control/
# control  md5sums  postinst  postrm  preinst  prerm
```

This is the right way to audit a `.deb` you got from a stranger.

---
## `dpkg`: The Low-Level Tool

```bash
# Install a single .deb file (no dependency resolution)
dpkg -i package.deb

# Remove (keep config files)
dpkg -r nginx

# Purge (remove config too)
dpkg -P nginx

# List installed packages
dpkg -l
dpkg -l | grep nginx

# What files did this package install?
dpkg -L nginx

# Which package owns this file?
dpkg -S /usr/sbin/nginx
```

`dpkg` does *not* fetch from the internet and does *not* resolve dependencies. It works on the file in front of it.

---
## `dpkg` Package States

```output
# dpkg -l output format:
# Desired=Unknown/Install/Remove/Purge/Hold
# | Status=Not/Inst/Conf-files/Unpacked/Failed-cfg
# |/ Err?=(none)/Reinst-required
# ||/ Name    Version    Description
# ii  nginx   1.24.0-1   web server     (installed OK)
# rc  apache2 2.4.58-1   web server     (removed, config left)
# hi  mysql   8.0.35-1   database       (hold, installed)
```

| Code | Meaning |
|---|---|
| `ii` | Installed, configured, OK |
| `rc` | Removed, config files remain |
| `hi` | Held, installed |
| `iU` | Installed, unpacked, needs configure |
| `un` | Not installed |

The single most common surprise: `rc` packages still take up `/etc` space until you `purge`.

---
## `apt`: The High-Level Tool

```bash
# Refresh package lists from configured repositories
apt update

# Install
apt install nginx

# Remove (keep config)
apt remove nginx

# Purge (remove config too)
apt purge nginx

# Search package descriptions
apt search "web server"

# Show details
apt show nginx

# List installed packages
apt list --installed
```

`apt` is the friendly front-end. It downloads, resolves dependencies, and calls `dpkg` for you.

---
## `apt` Install Options Worth Knowing

```bash
# Install a specific version
apt install nginx=1.24.0-1ubuntu1

# Don't pull in "Recommended" packages — leaner install
apt install --no-install-recommends nginx

# Dry run: what would happen?
apt install -s nginx

# Download .deb files but don't install
apt install -d nginx

# Reinstall an already-installed package
apt install --reinstall nginx

# Install a local .deb with full dependency resolution
apt install ./package.deb
```

`-s` (simulate) is your safety net. Use it before any production change.

---
## Upgrades and Maintenance

```bash
# Upgrade installed packages (won't remove anything)
apt upgrade

# Full upgrade (allowed to remove packages to satisfy deps)
apt full-upgrade

# Drop unused dependencies left over from removals
apt autoremove

# Clean cached .deb files in /var/cache/apt/archives/
apt clean
apt autoclean

# What can be upgraded?
apt list --upgradable
```

`upgrade` is conservative, `full-upgrade` is aggressive. Read the prompt carefully — `full-upgrade` will quietly remove packages.

---
## `apt-mark`: Holding Packages

```bash
# Pin a package — never upgrade it
apt-mark hold nginx
apt-mark unhold nginx

# What's currently held?
apt-mark showhold

# Mark as manually installed (won't be autoremoved)
apt-mark manual nginx

# Mark as automatic (eligible for autoremove)
apt-mark auto libfoo

# What did the user explicitly install?
apt-mark showmanual

# What's only there as a dependency?
apt-mark showauto
```

In production, `hold` what matters and `apt upgrade` will leave it alone.

---
## `apt-cache` and `apt-file`: Querying

```bash
# Search descriptions
apt-cache search "web server"

# Show all available versions
apt-cache madison nginx

# Where would this package come from? (which repo wins)
apt-cache policy nginx

# What does this depend on?
apt-cache depends nginx

# What depends on this?
apt-cache rdepends nginx
```

```bash
# Find which package contains a file (even uninstalled packages)
apt install apt-file
apt-file update
apt-file search /usr/bin/dig
apt-file search libssl.so
```

`apt-file` is the answer to "command not found, what do I install?".

---
## Repositories: `sources.list.d`

```bash
# Modern systems split each repo into its own file
ls /etc/apt/sources.list.d/

# DEB822 format (Ubuntu 24.04+, Debian 12+)
cat /etc/apt/sources.list.d/ubuntu.sources
```

```config
Types: deb deb-src
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```config
# Legacy one-line format, still supported
deb http://archive.ubuntu.com/ubuntu noble main restricted
```

Components on Ubuntu: `main` (supported free), `restricted` (proprietary drivers), `universe` (community), `multiverse` (non-free).

---
## Adding a Third-Party Repository the Right Way

The deprecated `apt-key` is gone. Today you keep the key in its own file and reference it from the repo definition.

```bash
# 1. Download the GPG key, dearmor, store it
curl -fsSL https://example.com/gpg.key | \
  sudo gpg --dearmor -o /usr/share/keyrings/example.gpg

# 2. Add the repository, pointing at that key
echo "deb [signed-by=/usr/share/keyrings/example.gpg] \
  https://repo.example.com/ubuntu noble main" | \
  sudo tee /etc/apt/sources.list.d/example.list

# 3. Update and install
sudo apt update
sudo apt install example-package
```

`signed-by` scopes the trust: that key only validates *that* repository.

---
## Pinning and Priorities

Pinning controls which version of a package wins when multiple repos offer it.

```config
# /etc/apt/preferences.d/pin-nginx.pref
Package: nginx
Pin: origin repo.example.com
Pin-Priority: 900

# Block a package from ever installing
Package: mysql-server
Pin: release *
Pin-Priority: -1
```

| Priority | Behavior |
|---|---|
| < 0 | Never install |
| 1–99 | Only install if not already installed |
| 100–499 | Install if newer than current |
| 500–999 | Preferred (default for repos) |
| ≥ 1000 | Force, even downgrade |

---
## Building a `.deb` By Hand

```bash
# Layout the file tree the package will install
mkdir -p myapp-1.0/DEBIAN
mkdir -p myapp-1.0/usr/local/bin
cp myapp myapp-1.0/usr/local/bin/
```

```config
# myapp-1.0/DEBIAN/control
Package: myapp
Version: 1.0
Architecture: amd64
Maintainer: Admin <admin@example.com>
Depends: libc6 (>= 2.35)
Description: My custom application
 A longer description goes here.
```

```bash
# Build it
dpkg-deb --build myapp-1.0
# -> myapp-1.0.deb
```

This is the simplest possible `.deb`. Real packages add `postinst`/`prerm` scripts and a `changelog`.

---
## Maintainer Scripts

A package can run code at four points in its lifecycle.

```bash
# DEBIAN/preinst   — before files are unpacked
# DEBIAN/postinst  — after files are in place
# DEBIAN/prerm     — before files are removed
# DEBIAN/postrm    — after files are removed
```

```bash
#!/bin/bash
# DEBIAN/postinst
set -e
case "$1" in
    configure)
        useradd -r -s /usr/sbin/nologin myapp || true
        systemctl daemon-reload
        systemctl enable --now myapp
        ;;
esac
```

These scripts run as `root` during install. They are powerful — and a frequent source of bugs.

---
## Troubleshooting `apt`/`dpkg`

```bash
# "dpkg was interrupted" — finish the half-done install
sudo dpkg --configure -a

# Broken dependencies — let apt fix them
sudo apt --fix-broken install

# Locked database (no other apt is running)
ps aux | grep -E 'apt|dpkg'   # confirm nothing is running
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/apt/lists/lock

# Reinstall a broken package
sudo apt install --reinstall nginx

# Reset a package's config to defaults
sudo dpkg-reconfigure tzdata
```

When in doubt: `dpkg --configure -a` then `apt --fix-broken install`. That fixes most messes.

---
## `apt` History and Audit Trail

```bash
# What did apt do, and when?
cat /var/log/apt/history.log
zcat /var/log/apt/history.log.*.gz   # older, rotated

# More granular: every dpkg action
cat /var/log/dpkg.log
grep " install " /var/log/dpkg.log | tail -20

# When was nginx installed?
grep nginx /var/log/dpkg.log | head -5

# Verify installed file integrity
sudo apt install debsums
sudo debsums -c   # only show changed files
```

For audit and incident response, `dpkg.log` and `debsums` are gold.

---
## Non-Interactive `apt` for Scripts and CI

```bash
# Suppress all interactive prompts
export DEBIAN_FRONTEND=noninteractive

# Pre-seed answers for prompty packages
echo "postfix postfix/main_mailer_type select Internet Site" | \
  sudo debconf-set-selections
echo "postfix postfix/mailname string mail.example.com" | \
  sudo debconf-set-selections

apt-get install -y postfix
```

```bash
# Idempotent install: only if missing
dpkg -s nginx >/dev/null 2>&1 || apt-get install -y nginx
```

Use `apt-get` (not `apt`) in scripts — its output and CLI are stable. `apt`'s output is for humans.
