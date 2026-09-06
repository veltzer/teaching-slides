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

# The Red Hat Family: rpm, yum, and dnf

---

## Tooling Layers

![rpm_lifecycle](svg/courses/operating_systems/linux-package-managers/03_rpm_and_dnf/rpm_lifecycle.svg)

---

## What Is a `.rpm` File?

`.rpm` is the package format used by `RHEL`, `CentOS Stream`, `Rocky`, `Alma`, `Fedora`, `openSUSE`, `Amazon Linux`, and others.

- A binary archive containing
    - a metadata header (name, version, dependencies, signatures)
    - a `cpio` archive of files
- Self-contained: every `.rpm` carries its own dependencies declaration and signature
- Signed with `GPG` and verified at install time

Unlike `.deb` you don't usually take a `.rpm` apart by hand. `rpm -qp` and `rpm2cpio` exist if you must.

---

## Anatomy of an RPM Package

![rpm_anatomy](svg/courses/operating_systems/linux-package-managers/03_rpm_and_dnf/rpm_anatomy.svg)

---

## Inspecting an `.rpm` Without Installing

```bash
# Info: name, version, summary, description
rpm -qip httpd-2.4.62-1.fc40.x86_64.rpm

# What files would it install?
rpm -qlp httpd-2.4.62-1.fc40.x86_64.rpm

# What does it depend on?
rpm -qpR httpd-2.4.62-1.fc40.x86_64.rpm

# What scripts does it run?
rpm -qp --scripts httpd-2.4.62-1.fc40.x86_64.rpm

# Extract files to a directory (no install)
mkdir /tmp/httpd && cd /tmp/httpd
rpm2cpio /path/to/httpd*.rpm | cpio -idmv
```

`rpm -qp` (query a package file) is the read-only mode you want for auditing.

---

## `rpm`: The Low-Level Tool

```bash
# Install (verbose, with hash bar)
rpm -ivh httpd-2.4.62-1.fc40.x86_64.rpm

# Upgrade or install if not present
rpm -Uvh httpd-2.4.62-1.fc40.x86_64.rpm

# Freshen (upgrade only if already installed)
rpm -Fvh httpd-2.4.62-1.fc40.x86_64.rpm

# Remove
rpm -e httpd

# Query installed
rpm -qa                # all installed packages
rpm -qi httpd          # info about installed
rpm -ql httpd          # files
rpm -qc httpd          # config files only
rpm -qd httpd          # docs only
rpm -qf /usr/sbin/httpd   # which package owns this file?
```

Like `dpkg`, `rpm` does *not* fetch and does *not* resolve dependencies.

---

## `rpm` Verification

`rpm -V` checks installed files against the metadata recorded at install time.

```bash
rpm -V httpd
# Output is per-file. Codes:
# S — file Size differs
# M — Mode (permissions) differs
# 5 — MD5 sum differs
# D — Device major/minor differs
# L — readLink path differs
# U — User ownership differs
# G — Group ownership differs
# T — mTime differs

# Verify everything
rpm -Va

# Verify a package's signature
rpm --checksig package.rpm

# Import a vendor's GPG key
rpm --import https://example.com/RPM-GPG-KEY
rpm -qa gpg-pubkey*    # what keys are trusted?
```

This is your "did anything tamper with my files?" tool.

---

## `yum` → `dnf` → `dnf5`

- `yum` was the original high-level tool on `RHEL`/`Fedora`
- `dnf` replaced `yum` as the default in `Fedora 22` and `RHEL 8`
- `dnf5` is the C++ rewrite, default in newer Fedora
- On most modern systems, `yum` is just a symlink or thin wrapper around `dnf`

The everyday commands are nearly identical. Use `dnf` going forward; `yum` is legacy muscle memory.

---

## Everyday `dnf`

```bash
# Refresh metadata happens automatically; force it with:
dnf check-update

# Install
dnf install httpd

# Remove
dnf remove httpd

# Search
dnf search "web server"

# Show details
dnf info httpd

# What's installed?
dnf list installed

# Upgrade everything
dnf upgrade

# Upgrade one thing
dnf upgrade httpd

# Show all available versions
dnf list --showduplicates httpd
```

---

## `dnf history`: A Real Audit Log

This is one of `dnf`'s killer features over `apt`.

```bash
# Every transaction with timestamp and user
dnf history

# Details of one transaction
dnf history info 25

# Undo it (uninstall what was installed, reinstall what was removed)
sudo dnf history undo 25

# Redo
sudo dnf history redo 25

# Roll the system back to the state at transaction 20
sudo dnf history rollback 20
```

`apt` has nothing this clean built-in. On `RHEL`/`Fedora`, you can revert a bad upgrade with one command.

---

## `dnf` Groups and Modules

```bash
# Groups: pre-defined bundles of related packages
dnf group list
dnf group install "Development Tools"
dnf group info "Server with GUI"
dnf group remove "Development Tools"
```

```bash
# Modules (RHEL 8+): multiple parallel streams of one app
dnf module list nodejs
# Name      Stream    Profiles    Summary
# nodejs    18        common      Node.js JavaScript runtime
# nodejs    20 [d]    common      Node.js JavaScript runtime

dnf module enable nodejs:20
dnf module install nodejs:20/common
dnf module reset nodejs       # back to default stream
dnf module disable nodejs
```

Modules are how RHEL ships, e.g., both `Node.js 18` and `20` from one repo.

---

## Repositories: `/etc/yum.repos.d/`

Each repo is one `.repo` file, one or more `[section]` blocks per file.

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
# Show all configured repos
dnf repolist all

# Enable / disable a repo persistently
sudo dnf config-manager --set-enabled custom-repo
sudo dnf config-manager --set-disabled custom-repo

# Use a repo just for one command
sudo dnf --enablerepo=custom-repo install foo
sudo dnf --disablerepo='*' --enablerepo=baseos install bar
```

Always set `gpgcheck=1`. A repo that asks you to disable `gpgcheck` is asking you to lower your guard.

---

## `EPEL` and Other Common Third-Party Repos

`EPEL` (Extra Packages for Enterprise Linux) is the canonical third-party repo for `RHEL` and clones.

```bash
# RHEL/Rocky/Alma 9
sudo dnf install epel-release
sudo dnf install htop ncdu jq
```

Other notable repos:

- `RPM Fusion` — multimedia `codec` packages and other things Fedora won't ship
- `Copr` — Fedora's `PPA` equivalent: per-user build hosting
- vendor repos: `Docker`, `MongoDB`, `PostgreSQL`, `Microsoft`, `Google Cloud`, ...

```bash
# Enable a Copr repo
sudo dnf copr enable user/project
sudo dnf install thatproject
```

---

## Building Your Own `.rpm` with `rpmbuild`

The minimum you need is a `.spec` file.

```bash
sudo dnf install rpm-build rpmdevtools
rpmdev-setuptree     # creates ~/rpmbuild/{SOURCES,SPECS,...}
```

```config
# ~/rpmbuild/SPECS/myapp.spec
Name:           myapp
Version:        1.0
Release:        1%{?dist}
Summary:        My custom application
License:        MIT
Source0:        myapp-%{version}.tar.gz
BuildRequires:  gcc make

%description
A small example application.

%prep
%setup -q

%build
make

%install
make install DESTDIR=%{buildroot}

%files
/usr/local/bin/myapp

%changelog
* Mon Apr 28 2026 You <you@example.com> - 1.0-1
- initial package
```

```bash
rpmbuild -ba ~/rpmbuild/SPECS/myapp.spec
# -> .rpm in ~/rpmbuild/RPMS/, .src.rpm in SRPMS/
```

---

## Signing Your `.rpm`

Unsigned `.rpm`s install only if you disable `gpgcheck`. Sign them.

```bash
# Generate a signing key
gpg --gen-key

# Tell rpm which key to use (in ~/.rpmmacros)
echo "%_gpg_name Your Name <you@example.com>" >> ~/.rpmmacros

# Sign an .rpm in place
rpm --addsign myapp-1.0-1.x86_64.rpm

# Export your public key for users to import
gpg --export -a 'Your Name' > RPM-GPG-KEY-myapp
```

A signed package + a published key + `gpgcheck=1` in the repo definition = a chain of trust.

---

## Side-by-Side: `apt` vs `dnf`

| Task | `apt` (Debian/Ubuntu) | `dnf` (RHEL/Fedora) |
|---|---|---|
| Refresh metadata | `apt update` | `dnf check-update` |
| Install | `apt install pkg` | `dnf install pkg` |
| Remove | `apt remove pkg` | `dnf remove pkg` |
| Purge config | `apt purge pkg` | (not separate) |
| Search | `apt search text` | `dnf search text` |
| Info | `apt show pkg` | `dnf info pkg` |
| Upgrade all | `apt upgrade` | `dnf upgrade` |
| List files | `dpkg -L pkg` | `rpm -ql pkg` |
| File owner | `dpkg -S /path` | `rpm -qf /path` |
| Hold | `apt-mark hold pkg` | `dnf versionlock pkg` |
| History | `/var/log/apt/history.log` | `dnf history` |
| Rollback | (manual) | `dnf history undo N` |
| Clean | `apt clean` | `dnf clean all` |

---

## Why You Might Prefer One Over the Other

`apt` strengths:

- Larger package selection on the user-facing side (Ubuntu's `universe`)
- `apt-file` and `apt-cache` are very pleasant
- `Debian`'s policy and stability story
- Massive community knowledge base

`dnf` strengths:

- Real transactional history with built-in rollback
- First-class modules for parallel software streams
- Cleaner config file syntax
- `rpm -V` integrity verification by default
- Tighter signature enforcement (default `gpgcheck=1`)

Most of the time, the choice is made *for* you by your distribution. Knowing both is a useful muscle when you change jobs.

---

## A Word on `zypper`, `pacman`, and `apk`

You will sooner or later hit a non-Debian, non-Red Hat system. The vocabulary translates.

```bash
# openSUSE: zypper, on top of rpm
zypper install httpd
zypper remove httpd
zypper update
zypper search httpd

# Arch Linux: pacman
pacman -S httpd       # Sync (install)
pacman -R httpd       # Remove
pacman -Syu           # Sync database, system upgrade
pacman -Ss httpd      # Search

# Alpine Linux: apk
apk add httpd
apk del httpd
apk update && apk upgrade
apk search httpd
```

Same model, different keystrokes. Once you know `apt` and `dnf`, the rest is muscle memory.
