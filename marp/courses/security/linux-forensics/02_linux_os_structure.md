# Understanding Linux OS Structure

## Course: Linux Forensics - Day 1 (continued)
- The `Linux` operating system is built on well-defined structures
- Understanding these structures is essential for forensic investigation
- Knowing where data lives helps locate evidence efficiently
- This module covers directory layout, services, users, and shells

---

## The Linux Filesystem Hierarchy Standard (FHS)

```tree
/
├── bin/      -> Essential command binaries
├── boot/     -> Boot loader files, kernel
├── dev/      -> Device files
├── etc/      -> System configuration files
├── home/     -> User home directories
├── lib/      -> Essential shared libraries
├── media/    -> Removable media mount points
├── mnt/      -> Temporary mount points
├── opt/      -> Optional application software
├── proc/     -> Virtual filesystem (process info)
├── root/     -> Root user home directory
├── run/      -> Runtime variable data
├── sbin/     -> System binaries
├── srv/      -> Service data
├── sys/      -> Virtual filesystem (kernel/hardware)
├── tmp/      -> Temporary files
├── usr/      -> User programs and data
└── var/      -> Variable data (logs, mail, spool)
```

---

## Forensically Important Directories: `/etc`

- System-wide configuration files
- Critical for understanding system state

```bash
# Key files for forensics
ls -la /etc/passwd          # User accounts
ls -la /etc/shadow          # Password hashes
ls -la /etc/group           # Group definitions
ls -la /etc/hostname        # System hostname
ls -la /etc/hosts           # Static host resolution
ls -la /etc/fstab           # Filesystem mount table
ls -la /etc/crontab         # Scheduled tasks
ls -la /etc/sudoers         # Sudo privileges
ls -la /etc/ssh/sshd_config # SSH server configuration
ls -la /etc/resolv.conf     # DNS configuration
```

---

## Forensically Important Directories: `/var`

```bash
# Log files - primary source of forensic evidence
ls -la /var/log/
# auth.log      - Authentication events
# syslog        - General system messages
# kern.log      - Kernel messages
# dpkg.log      - Package installation log
# apt/          - APT package manager logs
# wtmp          - Login records (binary)
# btmp          - Failed login records (binary)
# lastlog       - Last login info (binary)

# Other important /var directories
ls -la /var/spool/cron/     # User cron jobs
ls -la /var/mail/           # User mailboxes
ls -la /var/tmp/            # Persistent temp files
ls -la /var/lib/            # Application state data
```

---

## Forensically Important Directories: `/home`

```bash
# Each user has a home directory with personal data
ls -la /home/username/

# Hidden configuration files (dotfiles)
ls -la /home/username/.bashrc       # Bash configuration
ls -la /home/username/.bash_history # Command history
ls -la /home/username/.profile      # Login profile
ls -la /home/username/.ssh/         # SSH keys and config
ls -la /home/username/.gnupg/       # GPG keys
ls -la /home/username/.local/       # Local application data
ls -la /home/username/.config/      # XDG config directory
ls -la /home/username/.cache/       # Cached application data

# Browser data
ls -la /home/username/.mozilla/     # Firefox profiles
ls -la /home/username/.config/google-chrome/  # Chrome data
```

---

## Forensically Important Directories: `/proc`

- Virtual filesystem - exists only in memory
- Contains real-time process and system information
- Not present in disk images (live forensics only)

```bash
# System information
cat /proc/version         # Kernel version
cat /proc/cpuinfo         # CPU information
cat /proc/meminfo         # Memory statistics
cat /proc/cmdline         # Kernel boot parameters
cat /proc/mounts          # Currently mounted filesystems
cat /proc/partitions      # Known disk partitions

# Per-process information
ls /proc/1234/            # Process with PID 1234
cat /proc/1234/cmdline    # Command that started process
cat /proc/1234/environ    # Environment variables
cat /proc/1234/maps       # Memory mappings
ls -la /proc/1234/fd/     # Open file descriptors
cat /proc/1234/status     # Process status
```

---

## Forensically Important Directories: `/dev`

```bash
# Device files - interfaces to hardware and pseudo-devices
ls -la /dev/sda      # First SATA/SCSI disk
ls -la /dev/sda1     # First partition of sda
ls -la /dev/nvme0n1  # First NVMe disk
ls -la /dev/null     # Discard device (black hole)
ls -la /dev/zero     # Source of zero bytes
ls -la /dev/urandom  # Random number generator
ls -la /dev/tty*     # Terminal devices
ls -la /dev/pts/     # Pseudo-terminal slaves

# Block devices vs character devices
# b = block device (disks)
# c = character device (terminals, serial)
ls -la /dev/ | head -20
# brw-rw---- 1 root disk 8, 0 ... sda
# crw-rw-rw- 1 root root 1, 3 ... null
```

---

## The `/tmp` and `/var/tmp` Directories

- Frequently used by attackers to stage tools and malware
- `/tmp` is typically cleared on reboot
- `/var/tmp` persists across reboots

```bash
# Check for suspicious files in temp directories
ls -laR /tmp/
ls -laR /var/tmp/

# Check if /tmp is a separate tmpfs mount
mount | grep tmp
# tmpfs on /tmp type tmpfs (rw,nosuid,nodev)

# If tmpfs: data is in RAM only, lost on reboot
# If on disk: data may be recoverable from disk image

# Find recently modified files in /tmp
find /tmp -mtime -1 -ls
find /var/tmp -mtime -7 -ls
```

---

## The `/root` Directory

- Home directory for the root (superuser) account
- Contains root's personal configuration and history
- High-value target for forensic investigation

```bash
# Root's command history
cat /root/.bash_history

# Root's SSH configuration and keys
ls -la /root/.ssh/
cat /root/.ssh/authorized_keys
cat /root/.ssh/known_hosts

# Root's cron jobs
crontab -l -u root
cat /var/spool/cron/crontabs/root

# Root's mail
cat /var/mail/root
```

---

## Understanding `systemd`

- Modern `Linux` init system and service manager
- PID 1 - first process started by kernel
- Manages services, targets, timers, mounts, and more

```bash
# Check if system uses systemd
ps -p 1 -o comm=
# Output: systemd

# View systemd version
systemctl --version

# System boot time
systemd-analyze

# Boot time breakdown
systemd-analyze blame | head -10
```

---

## `systemd` Unit Types

| Unit Type | Extension   | Purpose                        |
|-----------|------------|--------------------------------|
| Service   | `.service` | Daemon or one-shot process     |
| Socket    | `.socket`  | IPC or network socket          |
| Timer     | `.timer`   | Scheduled activation           |
| Mount     | `.mount`   | Filesystem mount point         |
| Target    | `.target`  | Grouping of units              |
| Path      | `.path`    | File system path monitoring    |
| Device    | `.device`  | Kernel device                  |
| Slice     | `.slice`   | Resource management group      |

```bash
# List all unit types
systemctl -t help
```

---

## `systemd` Service Investigation

```bash
# List all services and their states
systemctl list-units --type=service --all

# Check status of a specific service
systemctl status sshd.service

# View service configuration file
systemctl cat sshd.service

# Find where service files are located
systemctl show -p FragmentPath sshd.service

# List enabled services (start at boot)
systemctl list-unit-files --state=enabled

# List failed services (may indicate issues)
systemctl list-units --failed
```

---

## `systemd` Service File Locations

```bash
# System service files (package-provided)
ls /lib/systemd/system/

# Administrator overrides (higher priority)
ls /etc/systemd/system/

# Runtime units (transient, lost on reboot)
ls /run/systemd/system/

# User service files
ls ~/.config/systemd/user/
```

- Forensic focus: look for unusual services in `/etc/systemd/system/`
- Attacker persistence often involves custom service files
- Compare against known-good baseline if available

---

## `systemd` Timers (Forensic Relevance)

- Timers can replace `cron` for scheduled tasks
- Attackers may use timers for persistence

```bash
# List all timers
systemctl list-timers --all

# Examine a timer
systemctl cat apt-daily.timer

# Look for suspicious timers
systemctl list-unit-files --type=timer | grep enabled

# Timer files locations
find /etc/systemd/ /lib/systemd/ -name "*.timer" -ls
```

---

## `systemd` Journal (`journald`)

```bash
# View full journal
journalctl

# Journal from current boot
journalctl -b

# Journal from previous boot
journalctl -b -1

# Filter by time range
journalctl --since "2025-01-15 10:00:00" --until "2025-01-15 12:00:00"

# Filter by service
journalctl -u sshd.service

# Filter by priority (0=emerg to 7=debug)
journalctl -p err

# Show kernel messages
journalctl -k

# Journal disk usage
journalctl --disk-usage
```

---

## `journalctl` Advanced Forensic Queries

```bash
# All authentication-related messages
journalctl _COMM=sshd
journalctl _COMM=sudo
journalctl _COMM=su

# Messages from specific user (by UID)
journalctl _UID=1000

# Export journal in JSON format for analysis
journalctl -o json-pretty > /evidence/journal_export.json

# Export in short format with timestamps
journalctl -o short-precise > /evidence/journal_full.log

# Binary journal files location
ls -la /var/log/journal/
# Organized by machine-id subdirectories
```

---

## User and Group Management

```bash
# /etc/passwd format:
# username:x:UID:GID:GECOS:home_dir:shell
cat /etc/passwd
# root:x:0:0:root:/root:/bin/bash
# www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
# john:x:1001:1001:John Doe:/home/john:/bin/bash

# /etc/group format:
# groupname:x:GID:member1,member2
cat /etc/group
# root:x:0:
# sudo:x:27:john,admin
# docker:x:999:john
```

---

## User Account Forensics

```bash
# List all user accounts
awk -F: '{print $1, $3, $7}' /etc/passwd

# Find accounts with UID 0 (root-equivalent)
awk -F: '$3 == 0 {print $1}' /etc/passwd

# Find accounts with login shells
awk -F: '$7 !~ /nologin|false/ {print $1, $7}' /etc/passwd

# Find recently created accounts
# Check /etc/passwd modification time
ls -la /etc/passwd

# Check for accounts added after system install
# Compare UIDs - system accounts typically < 1000
awk -F: '$3 >= 1000 && $3 < 65534 {print $1, $3}' /etc/passwd

# Check sudo group membership
getent group sudo
getent group wheel
```

---

## Group Membership Analysis

```bash
# List all groups a user belongs to
groups username
id username
# uid=1001(john) gid=1001(john) groups=1001(john),27(sudo),999(docker)

# Forensically interesting groups:
# sudo/wheel - can run commands as root
# docker     - can access Docker daemon (effectively root)
# disk       - can read raw disk devices
# adm        - can read many log files
# shadow     - can read /etc/shadow

# Find users in privileged groups
for group in sudo wheel docker disk adm; do
  echo "=== $group ==="
  getent group "$group" 2>/dev/null
done
```

---

## Login and Authentication Records

```bash
# Current logged-in users
who
w

# Last logins (reads /var/log/wtmp)
last
last -f /var/log/wtmp.1  # Previous rotated file

# Failed login attempts (reads /var/log/btmp)
sudo lastb

# Last login for each user
lastlog

# Authentication log
sudo cat /var/log/auth.log | tail -20

# SSH login attempts
sudo grep "sshd" /var/log/auth.log | grep "Accepted"
sudo grep "sshd" /var/log/auth.log | grep "Failed"
```

---

## Shell Basics for Forensics

### Common Shells
| Shell    | Path              | Config Files                |
|----------|------------------|-----------------------------|
| `bash`   | `/bin/bash`      | `.bashrc`, `.bash_profile`  |
| `zsh`    | `/bin/zsh`       | `.zshrc`, `.zprofile`       |
| `sh`     | `/bin/sh`        | `.profile`                  |
| `fish`   | `/usr/bin/fish`  | `config.fish`               |
| `dash`   | `/bin/dash`      | (minimal, no history)       |

```bash
# Check default shell for a user
getent passwd username | cut -d: -f7

# List available shells
cat /etc/shells
```

---

## Shell History Files

- One of the most valuable forensic artifacts
- Records commands typed by users

```bash
# Bash history
cat /home/user/.bash_history

# Zsh history (may include timestamps)
cat /home/user/.zsh_history

# History file size settings
grep HISTSIZE /home/user/.bashrc
# HISTSIZE=1000
# HISTFILESIZE=2000

# Bash history with timestamps (if HISTTIMEFORMAT was set)
HISTTIMEFORMAT="%F %T " history

# Check if history was disabled (anti-forensics indicator)
grep -i "HISTSIZE=0\|HISTFILESIZE=0\|unset HIST\|/dev/null" \
  /home/*/.bashrc /home/*/.bash_profile 2>/dev/null
```

---

## Shell Configuration Forensics

```bash
# Check all shell startup files for suspicious entries
for user_home in /home/* /root; do
  echo "=== $user_home ==="
  for rc in .bashrc .bash_profile .profile .bash_logout; do
    if [ -f "$user_home/$rc" ]; then
      echo "--- $rc ---"
      cat "$user_home/$rc"
    fi
  done
done

# Look for persistence mechanisms in shell configs
grep -rn "alias\|export\|source\|eval\|exec\|nc \|ncat\|/dev/tcp" \
  /home/*/.bashrc /home/*/.profile /root/.bashrc 2>/dev/null
```

---

## Scheduled Tasks: `cron`

```bash
# System crontab
cat /etc/crontab

# Cron directories (scripts here run automatically)
ls -la /etc/cron.d/
ls -la /etc/cron.daily/
ls -la /etc/cron.hourly/
ls -la /etc/cron.weekly/
ls -la /etc/cron.monthly/

# Per-user crontabs
ls -la /var/spool/cron/crontabs/
sudo cat /var/spool/cron/crontabs/root

# Cron format: minute hour day month weekday command
# Example: */5 * * * * /tmp/.hidden/beacon.sh
# Runs every 5 minutes - suspicious!
```

---

## Scheduled Tasks: `at` and `anacron`

```bash
# at - one-time scheduled commands
ls -la /var/spool/at/
atq  # List queued at jobs

# anacron - runs missed cron jobs
cat /etc/anacrontab

# Systemd timers (modern alternative to cron)
systemctl list-timers

# Check for suspicious scheduled tasks
find /etc/cron* /var/spool/cron -type f -exec ls -la {} \;
find /var/spool/at -type f -exec ls -la {} \;
```

---

## The Linux Boot Process

```diagram
1. BIOS/UEFI POST
       |
2. Boot Loader (GRUB2)
       |
3. Kernel Loading (vmlinuz)
       |
4. initramfs/initrd
       |
5. systemd (PID 1)
       |
6. default.target (multi-user/graphical)
       |
7. Login prompt / Display manager
```

```bash
# View boot configuration
cat /boot/grub/grub.cfg | grep -E "menuentry|linux\s"

# View kernel parameters used at boot
cat /proc/cmdline
```

---

## GRUB Configuration Forensics

```bash
# GRUB configuration
cat /etc/default/grub

# Key forensic indicators in GRUB config:
# - Single user mode booting
# - Modified kernel parameters
# - Custom boot entries

# Check for GRUB password protection
grep -r "password" /etc/grub.d/

# Boot log
journalctl -b 0 | head -50

# Previous kernels available
ls /boot/vmlinuz-*
```

---

## Kernel Modules

```bash
# List loaded kernel modules
lsmod

# Module details
modinfo module_name

# Check for suspicious modules (rootkits)
# Compare against known-good module list
lsmod | awk '{print $1}' | sort > /evidence/current_modules.txt

# Module load history
dmesg | grep -i "module"
journalctl -k | grep -i "module"

# Module files location
ls /lib/modules/$(uname -r)/

# Check module signing
grep CONFIG_MODULE_SIG /boot/config-$(uname -r)
```

---

## Network Configuration

```bash
# Network interfaces
ip addr show
ip link show

# Routing table
ip route show

# DNS configuration
cat /etc/resolv.conf
resolvectl status  # systemd-resolved

# Network connections
ss -tunapl
netstat -tunapl  # older systems

# Firewall rules
sudo iptables -L -n -v
sudo nft list ruleset  # nftables

# Network manager connections
nmcli connection show
```

---

## SSH Configuration Forensics

```bash
# SSH server configuration
cat /etc/ssh/sshd_config
# Key items: PermitRootLogin, PasswordAuthentication,
# AuthorizedKeysFile, Port

# SSH client configuration
cat /etc/ssh/ssh_config
cat /home/user/.ssh/config

# Authorized keys (who can log in)
cat /home/user/.ssh/authorized_keys

# Known hosts (where user has connected)
cat /home/user/.ssh/known_hosts

# SSH host keys (identify the server)
ls -la /etc/ssh/ssh_host_*

# SSH key fingerprints
for key in /etc/ssh/ssh_host_*_key.pub; do
  ssh-keygen -lf "$key"
done
```

---

## Installed Software

```bash
# Debian/Ubuntu - dpkg
dpkg -l                    # List all installed packages
dpkg -l | grep -i nginx    # Search for specific package
dpkg -L package_name       # List files from package

# Package installation log
cat /var/log/dpkg.log | tail -30
cat /var/log/apt/history.log | tail -50

# Red Hat/CentOS - rpm
rpm -qa                    # List all installed packages
rpm -ql package_name       # List files from package
rpm -V package_name        # Verify package integrity

# Snap packages
snap list

# Flatpak
flatpak list
```

---

## Package Integrity Verification

```bash
# Debian: verify installed packages against expected state
dpkg --verify
# Output shows modified files:
# ??5?????? c /etc/ssh/sshd_config   <- config modified
# ??5?????? /usr/bin/ls              <- BINARY MODIFIED (suspicious!)

# RPM: verify all packages
rpm -Va
# S = file Size differs
# M = Mode differs
# 5 = MD5 sum differs
# T = mTime differs
# U = User ownership differs
# G = Group ownership differs

# Check if a file belongs to any package
dpkg -S /usr/bin/ls
rpm -qf /usr/bin/ls
```

---

## Process Information

```bash
# List all processes
ps auxf

# Process tree
pstree -p

# Detailed process information
ps -eo pid,ppid,user,stat,start,time,comm,args

# Find processes running as root
ps -eo pid,user,comm | awk '$2 == "root"'

# Find processes with deleted binaries (suspicious)
ls -la /proc/*/exe 2>/dev/null | grep deleted

# Find processes listening on network ports
ss -tlnp
```

---

## Filesystem Types in Linux

| Filesystem | Description                    | Forensic Note             |
|-----------|--------------------------------|---------------------------|
| `ext4`    | Default Linux filesystem       | Journal aids recovery     |
| `xfs`     | High-performance (RHEL default)| Journal, good for large files|
| `btrfs`   | Copy-on-write filesystem       | Snapshots, checksums      |
| `zfs`     | Advanced filesystem            | Snapshots, integrity      |
| `tmpfs`   | RAM-based filesystem           | Volatile, lost on reboot  |
| `vfat`    | FAT32 (EFI, USB drives)       | No permissions, simple    |
| `ntfs`    | Windows filesystem             | NTFS-3G driver on Linux   |
| `squashfs`| Read-only compressed           | Used in snap packages     |

---

## `ext4` Filesystem Internals

```bash
# View ext4 filesystem information
sudo tune2fs -l /dev/sda2

# Key forensic fields:
# Filesystem created:       Wed Jan 15 10:30:00 2025
# Last mount time:          Mon Mar 10 08:15:00 2025
# Last write time:          Mon Mar 10 08:15:00 2025
# Mount count:              42
# Maximum mount count:      -1
# Filesystem state:         clean
# Errors behavior:          Continue

# View superblock information
sudo dumpe2fs /dev/sda2 | head -50
```

---

## `ext4` Journal

- The `ext4` journal records filesystem changes before committing them
- Can contain recently deleted file data

```bash
# Dump the journal
sudo debugfs -R "logdump" /dev/sda2 > /evidence/journal_dump.txt

# Interactive ext4 debugging
sudo debugfs -R "ls -l /home/user/" /dev/sda2
sudo debugfs -R "stat /etc/passwd" /dev/sda2
sudo debugfs -R "lsdel" /dev/sda2  # List deleted files

# Recover deleted file by inode number
sudo debugfs -R "dump <12345> /evidence/recovered_file" /dev/sda2
```

---

## File Permissions and Ownership

```bash
# Permission format: type|owner|group|others
# drwxr-xr-x  2 root root 4096 Jan 15 10:30 directory
# -rw-r--r--  1 john john  100 Jan 15 10:30 file.txt

# Numeric permissions
# r=4, w=2, x=1
# 755 = rwxr-xr-x
# 644 = rw-r--r--
# 777 = rwxrwxrwx  (overly permissive - suspicious)

# Find world-writable files (potential security issue)
find / -perm -o+w -type f 2>/dev/null

# Find files with no owner (may indicate deleted user)
find / -nouser -o -nogroup 2>/dev/null | head -20
```

---

## Special Permissions: SUID, SGID, Sticky Bit

```bash
# SUID (Set User ID) - runs as file owner
# -rwsr-xr-x = SUID set
find / -perm -4000 -type f 2>/dev/null
# Common legitimate SUID files:
# /usr/bin/passwd, /usr/bin/sudo, /usr/bin/su

# SGID (Set Group ID) - runs with group privileges
# -rwxr-sr-x = SGID set
find / -perm -2000 -type f 2>/dev/null

# Sticky bit on directories (only owner can delete)
# drwxrwxrwt = sticky bit set (e.g., /tmp)

# Find unusual SUID/SGID files (compare against baseline)
find / -perm -4000 -type f 2>/dev/null | sort > suid_files.txt
# Compare with known-good list to find anomalies
```

---

## File Timestamps (MAC Times)

```bash
# Three timestamps on ext4:
# mtime - Modification time (content changed)
# atime - Access time (content read)
# ctime - Change time (metadata changed)

# View timestamps
stat /etc/passwd
# Output:
#   Access: 2025-01-15 10:30:00.000000000 +0000
#   Modify: 2025-01-10 08:00:00.000000000 +0000
#   Change: 2025-01-10 08:00:00.000000000 +0000
#    Birth: 2024-06-01 12:00:00.000000000 +0000

# ext4 also stores birth (creation) time
# Access with debugfs:
sudo debugfs -R "stat <$(stat -c %i /etc/passwd)>" /dev/sda2
```

---

## Mount Options and `noatime`

```bash
# Check current mount options
mount | grep -E "sda|nvme"
# /dev/sda2 on / type ext4 (rw,relatime,errors=remount-ro)

# Common mount options affecting forensics:
# relatime - only update atime if older than mtime (default)
# noatime  - never update atime (no access time tracking)
# strictatime - always update atime

# Check fstab for mount options
cat /etc/fstab
# UUID=xxx /  ext4  errors=remount-ro,relatime  0  1

# Forensic mount (read-only, preserve timestamps)
sudo mount -o ro,noatime,noexec /dev/sdb1 /mnt/evidence
```

---

## Access Control Lists (ACLs)

```bash
# View ACLs on a file
getfacl /path/to/file

# Example output:
# file: path/to/file
# owner: john
# group: staff
# user::rw-
# user:bob:r--
# group::r--
# mask::r--
# other::---

# Find files with ACLs
getfacl -R /home/ 2>/dev/null | grep -B5 "user:"

# ACLs can grant hidden permissions not visible in ls -l
# The + sign in ls output indicates ACLs exist:
# -rw-r--r--+ 1 john staff 100 Jan 15 file.txt
```

---

## Extended Attributes

```bash
# List extended attributes
getfattr -d /path/to/file
lsattr /path/to/file

# Common attributes:
# i - immutable (cannot be modified/deleted even by root)
# a - append only
# s - secure deletion
# u - undeletable

# Find immutable files (may hide malicious files)
lsattr -R / 2>/dev/null | grep -E "^....i"

# Set/remove immutable attribute (for reference)
# sudo chattr +i /path/to/file   # Set immutable
# sudo chattr -i /path/to/file   # Remove immutable
```

---

## SELinux and AppArmor

```bash
# Check if SELinux is enabled
getenforce
sestatus

# Check SELinux context of files
ls -laZ /etc/passwd
# -rw-r--r--. root root system_u:object_r:passwd_file_t:s0

# Check if AppArmor is enabled
sudo aa-status

# AppArmor profiles
ls /etc/apparmor.d/

# Check for disabled security modules (suspicious)
dmesg | grep -iE "selinux|apparmor"
cat /proc/cmdline | grep -iE "selinux|apparmor"
# selinux=0 or apparmor=0 in boot parameters = disabled
```

---

## System Time and Timezone

```bash
# Current system time
date
timedatectl

# Timezone configuration
cat /etc/timezone
ls -la /etc/localtime
readlink /etc/localtime
# Output: /usr/share/zoneinfo/America/New_York

# NTP synchronization status
timedatectl timesync-status
chronyc tracking  # If using chrony
ntpq -p          # If using ntpd

# Hardware clock
sudo hwclock --show
```

- Accurate time is critical for forensic timeline analysis
- Check if NTP was configured (time may have been manipulated)

---

## Hostname and System Identification

```bash
# System hostname
hostname
hostname -f  # FQDN
cat /etc/hostname

# Machine ID (unique per installation)
cat /etc/machine-id

# System information
uname -a
cat /etc/os-release

# Hardware information
sudo dmidecode -t system | head -20
# Manufacturer, Product Name, Serial Number

# Last system install/update date
ls -la /var/log/installer/  # Debian/Ubuntu
rpm -qi basesystem | grep "Install Date"  # RHEL/CentOS
```

---

## Examining Startup Scripts

```bash
# SysV init scripts (legacy)
ls -la /etc/init.d/
ls -la /etc/rc*.d/

# Systemd generators (can create dynamic units)
ls /lib/systemd/system-generators/
ls /etc/systemd/system-generators/

# User login scripts executed in order:
# 1. /etc/profile
# 2. /etc/profile.d/*.sh
# 3. ~/.bash_profile (or ~/.profile)
# 4. ~/.bashrc

# Check for malicious additions
for f in /etc/profile.d/*.sh; do
  echo "=== $f ==="
  cat "$f"
done
```

---

## Environment Variables

```bash
# View all environment variables
env
printenv

# Forensically interesting variables
echo $PATH        # Where commands are found
echo $HOME        # User's home directory
echo $SHELL       # Default shell
echo $USER        # Current username
echo $HISTFILE    # History file location
echo $HISTSIZE    # History size
echo $LD_PRELOAD  # Library preloading (rootkit indicator!)

# Check for LD_PRELOAD in system files
grep -r "LD_PRELOAD" /etc/ 2>/dev/null
# If LD_PRELOAD is set system-wide, it's likely malicious
```

---

## System Logs Overview

```bash
# Traditional syslog files
/var/log/syslog        # General system log
/var/log/auth.log      # Authentication events
/var/log/kern.log      # Kernel messages
/var/log/daemon.log    # Daemon messages
/var/log/dmesg         # Boot-time kernel messages
/var/log/boot.log      # Boot process log
/var/log/faillog       # Failed login database
/var/log/lastlog       # Last login database
/var/log/wtmp          # Login history (binary)
/var/log/btmp          # Failed login history (binary)

# Application-specific logs
/var/log/apache2/      # Apache web server
/var/log/nginx/        # Nginx web server
/var/log/mysql/        # MySQL database
/var/log/mail.log      # Mail server
```

---

## Log Rotation

```bash
# Log rotation configuration
cat /etc/logrotate.conf
ls /etc/logrotate.d/

# Example rotation config:
# /var/log/syslog {
#     rotate 7
#     daily
#     compress
#     delaycompress
#     missingok
#     notifempty
# }

# Rotated logs
ls -la /var/log/syslog*
# syslog
# syslog.1
# syslog.2.gz
# syslog.3.gz

# Read compressed rotated logs
zcat /var/log/syslog.2.gz
zgrep "error" /var/log/syslog.*.gz
```

---

## Exercise: Linux Structure Investigation

### Tasks:
1. Map the filesystem structure of the target system
1. Identify all user accounts and their privileges
1. List all running services and scheduled tasks
1. Check shell histories for all users
1. Document system identification information

```bash
#!/bin/bash
# Quick system survey script
echo "=== System Info ==="
uname -a && cat /etc/os-release
echo "=== Users with shells ==="
awk -F: '$7 !~ /nologin|false/ {print}' /etc/passwd
echo "=== Enabled services ==="
systemctl list-unit-files --state=enabled --type=service
echo "=== Active timers ==="
systemctl list-timers
echo "=== Recent logins ==="
last | head -20
```

---

## Summary: Linux OS Structure

- The FHS defines where data is stored in `Linux`
- `/etc` contains system configuration - check for unauthorized changes
- `/var/log` contains system logs - primary evidence source
- `/home` and `/root` contain user artifacts and history
- `systemd` manages services - check for persistence mechanisms
- User accounts in `/etc/passwd` and `/etc/shadow`
- Shell history files record user commands
- `cron`, `at`, and `systemd` timers handle scheduled tasks
- File permissions, ACLs, and extended attributes control access
- Timestamps (MAC times) are essential for timeline analysis
- Log files are rotated - check compressed archives too

---

## Systemd Service Persistence Analysis

```bash
# Attackers create systemd services for persistence
# Look for unusual service files

# Recently created/modified service files
find /etc/systemd/system -name "*.service" -mtime -30 -ls

# Services with unusual ExecStart
for f in /etc/systemd/system/*.service; do
  if [ -f "$f" ]; then
    exec_line=$(grep "ExecStart" "$f" 2>/dev/null)
    if echo "$exec_line" | grep -qiE "/tmp|/dev/shm|/var/tmp|base64|curl|wget"; then
      echo "SUSPICIOUS: $f"
      echo "  $exec_line"
    fi
  fi
done

# Check service file timestamps vs package installation
dpkg -S /lib/systemd/system/ssh.service
# openssh-server: /lib/systemd/system/ssh.service
# If dpkg doesn't know about it, it's custom
```

---

## D-Bus and IPC Forensics

```bash
# D-Bus is Linux inter-process communication system
# May reveal active services and communication

# List D-Bus services
busctl list

# Monitor D-Bus messages (live)
sudo busctl monitor

# System bus services
busctl --system list

# User session bus
busctl --user list

# Introspect a service
busctl introspect org.freedesktop.systemd1 /

# D-Bus configuration
ls /etc/dbus-1/system.d/
ls /usr/share/dbus-1/system-services/

# Forensic value:
# - Identify inter-process communication patterns
# - Find services that shouldn't be running
# - Detect unauthorized service registration
```

---

## Capabilities Analysis

```bash
# Linux capabilities split root privileges into units
# More granular than SUID but equally dangerous

# Find files with capabilities
getcap -r / 2>/dev/null

# Common legitimate capabilities:
# /usr/bin/ping     cap_net_raw=ep
# /usr/bin/traceroute6 cap_net_raw=ep

# Dangerous capabilities to watch for:
# cap_sys_admin    - nearly equivalent to root
# cap_sys_ptrace   - can attach to any process
# cap_net_admin    - full network control
# cap_dac_override - bypass file permissions
# cap_setuid       - change UID

# Check capabilities of running process
cat /proc/1234/status | grep -i cap
# CapInh: 0000000000000000
# CapPrm: 0000003fffffffff
# CapEff: 0000003fffffffff

# Decode capability bitmask
capsh --decode=0000003fffffffff
```

---

## Namespaces and Container Isolation

```bash
# Namespaces isolate system resources
# Containers use namespaces extensively

# View namespaces of a process
ls -la /proc/1234/ns/
# cgroup -> cgroup:[...]
# ipc    -> ipc:[...]
# mnt    -> mnt:[...]
# net    -> net:[...]
# pid    -> pid:[...]
# user   -> user:[...]
# uts    -> uts:[...]

# List all namespaces
lsns

# Find processes in non-default namespaces
lsns | grep -v "4026531835"  # Default namespace ID varies

# Enter a namespace for investigation
sudo nsenter -t 1234 -m -u -i -n -p -- /bin/bash
# -m mount, -u UTS, -i IPC, -n network, -p PID
```

---

## Systemd Coredumps

```bash
# Systemd captures core dumps from crashed processes
# Valuable for forensic analysis of malware crashes

# List core dumps
coredumpctl list

# Show details of a specific dump
coredumpctl info PID

# Extract core dump file
coredumpctl dump PID -o /evidence/coredump.core

# Analyze with GDB
coredumpctl gdb PID

# Core dump storage location
ls /var/lib/systemd/coredump/

# Core dump configuration
cat /etc/systemd/coredump.conf
# Storage=external
# Compress=yes
# MaxUse=1G

# Forensic value:
# - Memory state at crash time
# - Stack trace reveals execution flow
# - May contain unencrypted sensitive data
```

---

## XDG Autostart

```bash
# XDG autostart runs applications on desktop login
# Another persistence mechanism

# System-wide autostart
ls /etc/xdg/autostart/

# Per-user autostart
ls /home/user/.config/autostart/

# Examine autostart entries
cat /home/user/.config/autostart/*.desktop
# [Desktop Entry]
# Type=Application
# Name=Update Service
# Exec=/tmp/.update/beacon
# Hidden=false
# X-GNOME-Autostart-enabled=true

# Check for suspicious entries
for f in /home/*/.config/autostart/*.desktop; do
  exec_line=$(grep "^Exec=" "$f" 2>/dev/null)
  echo "$f: $exec_line"
done
```

---

## PAM Module Analysis

```bash
# PAM (Pluggable Authentication Modules) controls authentication
# Compromised PAM modules can backdoor login

# PAM configuration
ls /etc/pam.d/
cat /etc/pam.d/common-auth
# auth required pam_unix.so nullok
# auth optional pam_permit.so  <- suspicious if unexpected!

# PAM module files
ls -la /lib/x86_64-linux-gnu/security/pam_*.so

# Verify PAM modules against package
dpkg -S /lib/x86_64-linux-gnu/security/pam_unix.so
# Expected: libpam-modules:amd64

# Check for unknown PAM modules
for mod in /lib/x86_64-linux-gnu/security/pam_*.so; do
  pkg=$(dpkg -S "$mod" 2>/dev/null)
  [ -z "$pkg" ] && echo "UNPACKAGED: $mod"
done

# Check PAM module hashes against known-good values
sha256sum /lib/x86_64-linux-gnu/security/pam_*.so
```

---

## Forensic Imaging of Linux Filesystems

```bash
# Different filesystems have different forensic properties

# ext4: Most common Linux filesystem
# - Journal stores recent operations
# - Inode timestamps include nanoseconds
# - Birth time (creation time) supported
# - Supports extended attributes
# - Deleted files recoverable via journal/inode

# XFS: Default on RHEL/CentOS 7+
# - High performance for large files
# - Journal, but less useful for recovery
# - Supports extended attributes
# - More difficult deleted file recovery

# Btrfs: Copy-on-write filesystem
# - Snapshots preserve previous file states
# - Checksums detect corruption
# - Built-in compression
# - send/receive for incremental backups
sudo btrfs subvolume list /
sudo btrfs subvolume snapshot -r / /snapshots/forensic
```

---

## Proc Filesystem Deep Dive

```bash
# /proc provides unique live forensic data

# System memory map
cat /proc/iomem | head -20

# Interrupt statistics
cat /proc/interrupts | head -10

# I/O port information
cat /proc/ioports | head -10

# Kernel command line (boot parameters)
cat /proc/cmdline
# root=UUID=xxx ro quiet splash

# Crypto information
cat /proc/crypto | head -20

# Lock statistics (debugging)
cat /proc/lock_stat 2>/dev/null | head -10

# Disk I/O statistics
cat /proc/diskstats

# Mounted filesystems with options
cat /proc/mounts

# Network protocol statistics
cat /proc/net/snmp
```

---

## Understanding Linux Security Modules

```bash
# Linux Security Modules (LSM) framework
# Provides mandatory access control

# Check which LSMs are active
cat /sys/kernel/security/lsm
# lockdown,capability,yama,apparmor

# Yama: ptrace scope control
cat /proc/sys/kernel/yama/ptrace_scope
# 0 = no restrictions
# 1 = only parent can ptrace children
# 2 = only admin can ptrace
# 3 = no ptrace at all

# Lockdown mode (restricts root capabilities)
cat /sys/kernel/security/lockdown
# [none] integrity confidentiality

# If lockdown is enabled:
# - Cannot access /dev/mem
# - Cannot load unsigned modules
# - Cannot modify kernel parameters
# This affects forensic tool availability
```

---

## Systemd-resolved and DNS Forensics

```bash
# systemd-resolved caches DNS queries
resolvectl status
resolvectl statistics

# Query cache contents
resolvectl query --cache example.com

# DNS over TLS configuration
cat /etc/systemd/resolved.conf
# DNSOverTLS=yes  <- encrypted DNS queries

# Alternative: check /etc/resolv.conf
cat /etc/resolv.conf
# May point to 127.0.0.53 (systemd-resolved stub)
# Or direct DNS servers

# DNS leak detection
# Check if custom DNS is configured to bypass corporate DNS
grep -r "nameserver\|dns" /etc/NetworkManager/ 2>/dev/null
grep -r "DNS=" /etc/systemd/resolved.conf

# Forensic note: DNS cache is volatile
# Capture it during live analysis before power off
resolvectl --json=short statistics > /evidence/dns_stats.json
```

---

## Login Session Tracking

```bash
# Detailed session tracking via utmp/wtmp

# Current sessions (utmp)
who -a
# NAME    LINE    TIME           IDLE  PID  COMMENT  EXIT
# system  boot    2025-01-15 08:00
# LOGIN   tty1    2025-01-15 08:01  5678
# john    pts/0   2025-01-15 10:30  .     9012  (192.168.1.50)

# Historical sessions (wtmp)
last -F  # Full timestamps
# john  pts/0  192.168.1.50  Mon Jan 15 10:30:00 2025 -
#                             Mon Jan 15 10:45:00 2025 (00:15)

# Failed logins (btmp)
sudo lastb -F
# root  ssh:notty  10.0.0.99  Mon Jan 15 10:28:00 2025 -
#                              Mon Jan 15 10:28:00 2025 (00:00)

# Last login per user
lastlog
# Username  Port  From          Latest
# root      pts/0 192.168.1.50  Mon Jan 15 10:30:00 +0000 2025
```

---

## Swap and Memory Pressure Forensics

```bash
# Swap contains paged-out memory - may have evidence

# Check swap usage
swapon -s
cat /proc/swaps
free -m

# Swap configuration
cat /etc/fstab | grep swap

# Memory pressure statistics
cat /proc/pressure/memory
# some avg10=0.00 avg60=0.00 avg300=0.00 total=0
# full avg10=0.00 avg60=0.00 avg300=0.00 total=0

# High memory pressure = more data in swap
# This means more evidence potentially in swap space

# OOM (Out of Memory) killer logs
dmesg | grep -i "oom\|out of memory"
journalctl | grep -i "oom\|out of memory"
# OOM events may indicate crypto mining or memory-intensive malware

# Swappiness setting (affects what goes to swap)
cat /proc/sys/vm/swappiness
# Higher value = more aggressive swapping
```
