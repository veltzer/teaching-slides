# Linux System Administration
## Course Overview

---
## What This Course Covers

- Managing `Linux` systems in production environments
- Storage, networking, security, and monitoring
- Hands-on exercises on `Ubuntu` 24.04
- 5-day intensive course

---
## Target Audience

- System administrators managing `Linux` in production
- `DevOps` engineers needing solid `Linux` skills
- IT professionals transitioning to `Linux`-based infrastructure

---
## Prerequisites

- Basic `Linux` command line experience
- Familiarity with text editors (`vim`/`nano`)
- Understanding of basic networking concepts

---
## Course Objectives

1. Manage system architecture, boot process, and packages
1. Configure storage, filesystems, and backups
1. Implement user management and system hardening
1. Set up network services and firewalls
1. Monitor performance and plan disaster recovery

---
## Course Structure

![course_structure](/svg/courses/operating_systems/linux-system-administration/01_introduction/course_structure.svg)

---
## Day-by-Day Schedule

| Day | Topics |
|-----|--------|
| Day 1 | Core System Architecture, FHS, Boot, `systemd` |
| Day 2 | Storage Management, Filesystems, Backups |
| Day 3 | User Management, Security, `SSH` |
| Day 4 | Network Services, Firewalls, VPN |
| Day 5 | Monitoring, Maintenance, Automation |

---
## Optional Modules

Depending on time and audience needs:
- Network Services (`nginx`, `Apache`, `HAProxy`, `Postfix`)
- `LVM` and `RAID`
- `SELinux`/`AppArmor`
- `DNS` Server Administration
- Containerization (`Docker`, `Podman`)
- Air-Gapped Environment Management

---
## Lab Environment

- `Ubuntu` 24.04 LTS (real or virtual machines)
- Root or `sudo` access required
- Network connectivity between lab machines
- Recommended: at least 2 VMs per student

---
## Lab Setup Verification

```bash
# Verify Ubuntu version
lsb_release -a

# Verify sudo access
sudo whoami

# Verify network connectivity
ping -c 3 <partner-vm-ip>

# Verify disk space
df -h /

# Verify internet access (for package downloads)
curl -s https://archive.ubuntu.com > /dev/null && \
  echo "OK" || echo "No internet"
```

---
## Key Resources

- Man pages: `man <command>`, `man 5 <config-file>`
- Info pages: `info <command>`
- `/usr/share/doc/` - package documentation
- `systemd` docs: `systemctl --help`, `man systemd.unit`
- Online: `Linux` kernel docs, distribution wikis

---
## Conventions Used in This Course

- `#` prompt means run as `root`
- `$` prompt means run as regular user
- `<placeholder>` means replace with actual value
- Commands shown are for `Ubuntu`/`Debian`; `RHEL`/`Fedora` equivalents noted where different
- All exercises assume `Ubuntu` 24.04 unless stated otherwise

---
## Linux Distributions Landscape

![linux_distributions_landscape](/svg/courses/operating_systems/linux-system-administration/01_introduction/linux_distributions_landscape.svg)

This course focuses on `Ubuntu`/`Debian` with `RHEL`/`Fedora` equivalents noted.

---
## Exercise: Verify Your Lab Environment

Complete the following checklist on your lab VMs:

1. Confirm `Ubuntu` version is 24.04 using `lsb_release -a`
1. Verify you can run `sudo` commands without errors
1. Ping your partner VM to confirm network connectivity
1. Check that `/` has at least 10GB free with `df -h /`
1. Identify your kernel version with `uname -r`
1. Confirm `systemd` is PID 1 with `ps -p 1 -o comm=`

```bash
# Quick validation script
#!/bin/bash
echo "=== OS ===" && lsb_release -ds
echo "=== Kernel ===" && uname -r
echo "=== Sudo ===" && sudo whoami
echo "=== Disk ===" && df -h / | tail -1
echo "=== PID 1 ===" && ps -p 1 -o comm=
```

---
## Exercise: Explore the System

Try these tasks and record your findings:

1. List all running services with `systemctl list-units --type=service --state=running`
1. Count how many packages are installed using `dpkg -l | grep '^ii' | wc -l`
1. Find which package provides the `ip` command with `dpkg -S $(which ip)`
1. Check system uptime with `uptime`
1. Review recent `dmesg` output for hardware messages

Discuss with your partner:
- What services are running that you did not expect?
- How much RAM does your VM have? (`free -h`)
- What block devices are available? (`lsblk`)

---
## Linux Release Cycle and Support

LTS (Long-Term Support) vs regular releases:

| Release Type | Support Period | Use Case |
|-------------|---------------|----------|
| `Ubuntu` LTS | 5 years (10 with ESM) | Production servers |
| `Ubuntu` interim | 9 months | Development, testing |
| `RHEL` | 10 years | Enterprise production |
| `Debian` stable | ~3 years | Servers, stability |

```bash
# Check current release and support status
lsb_release -a
ubuntu-distro-info --supported

# Check kernel version and HWE status
uname -r
# HWE kernels (e.g., 6.8.0-xx-generic) bring
# newer hardware support to LTS releases

# Install HWE kernel on Ubuntu LTS
apt install linux-generic-hwe-24.04
```

Plan upgrades before EOL (End of Life) to maintain security patches.

---
## Getting Help: Man Pages In Depth

Man pages are organized into numbered sections:

| Section | Content |
|---------|---------|
| 1 | User commands (`ls`, `grep`) |
| 2 | System calls (`open`, `read`) |
| 3 | Library functions (`printf`, `malloc`) |
| 4 | Special files (`/dev/null`) |
| 5 | File formats (`/etc/passwd`, `fstab`) |
| 6 | Games |
| 7 | Miscellaneous (protocols, conventions) |
| 8 | System administration (`mount`, `iptables`) |

```bash
# Read a specific section
man 5 passwd         # file format, not the command
man 8 mount          # admin command

# Search man pages by keyword
apropos filesystem
man -k partition

# One-line description of a command
whatis rsync

# Search within a man page: press / then type pattern
```

---
## Getting Help: Online Resources

When man pages are not enough, use these trusted sources:

1. **Stack Exchange** sites
    - `serverfault.com` for sysadmin questions
    - `unix.stackexchange.com` for general `Linux`/`Unix`
    - `askubuntu.com` for `Ubuntu`-specific issues
1. **Distribution wikis**
    - `wiki.archlinux.org` - excellent technical depth
    - `help.ubuntu.com` - official `Ubuntu` docs
    - `wiki.debian.org` - `Debian`-specific guides
1. **Mailing lists and chat**
    - Distribution-specific mailing lists
    - `IRC` channels on `Libera.Chat` (`#ubuntu`, `#debian`)
    - `Matrix` rooms (modern alternative to `IRC`)
1. **Official documentation**
    - `kernel.org/doc` for kernel docs
    - `systemd.io` for `systemd` docs
    - `man7.org` for comprehensive man pages online
