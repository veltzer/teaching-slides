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
# Core System Architecture
## Filesystem, Boot Process, and systemd

---

## Linux Filesystem Hierarchy Standard (FHS)
![linux_filesystem_hierarchy_standard_fhs](svg/courses/operating_systems/linux-system-administration/02_core_system_architecture/linux_filesystem_hierarchy_standard_fhs.svg)

---
## Linux Filesystem Hierarchy Standard (FHS)
- `/bin`, `/sbin` - essential binaries
- `/etc` - system configuration
- `/var` - variable data (logs, mail, spool)
- `/usr` - user programs and libraries
- `/tmp` - temporary files

---
## Key FHS Directories

| Directory | Purpose |
|-----------|---------|
| `/boot` | Kernel and bootloader files |
| `/dev` | Device files |
| `/proc` | Process and kernel info (virtual) |
| `/sys` | Hardware/driver info (virtual) |
| `/opt` | Optional/third-party software |
| `/srv` | Service data |
| `/run` | Runtime data since last boot |

---
## The /usr Hierarchy

Modern `Linux` merges `/bin` -> `/usr/bin` and `/sbin` -> `/usr/sbin`.

| Directory | Purpose |
|-----------|---------|
| `/usr/bin` | User commands |
| `/usr/sbin` | System admin commands |
| `/usr/lib` | Shared libraries |
| `/usr/include` | C header files |
| `/usr/share` | Architecture-independent data |
| `/usr/local` | Locally installed software |
| `/usr/src` | Source code (e.g., kernel headers) |

```bash
# Verify the merge on Ubuntu
ls -la /bin    # symlink to /usr/bin
ls -la /sbin   # symlink to /usr/sbin
```

---
## The /var Hierarchy

```bash
# Variable data that changes during operation
/var/log/       # System and application logs
/var/cache/     # Application cache data
/var/spool/     # Queued data (mail, print)
/var/lib/       # Persistent application state
/var/tmp/       # Temporary files (survive reboot)
/var/run/       # Runtime data (symlink to /run)
/var/mail/      # User mailboxes
```

Important: `/var/log` and `/var/cache` can grow large. Consider separate partitions for production.

---
## Exploring the FHS

```bash
# Find where a command lives
which nginx
type -a python3

# Find all config files for a package
dpkg -L nginx | grep /etc/

# Find what's consuming space
du -sh /var/log/* | sort -rh | head -10

# Check which filesystems are mounted where
findmnt --real

# View inode usage (can run out before disk space)
df -i
```

---

## The Boot Process Overview
![the_boot_process_overview](svg/courses/operating_systems/linux-system-administration/02_core_system_architecture/the_boot_process_overview.svg)

---
## The Boot Process Overview
1. Firmware (BIOS/UEFI) performs POST and finds boot device
1. Bootloader (`GRUB2`) loads kernel and `initramfs`
1. Kernel initializes hardware and mounts root filesystem
1. `systemd` (PID 1) starts all services

---
## BIOS vs UEFI

| Feature | BIOS | UEFI |
|---------|------|------|
| Partition table | MBR | GPT |
| Max disk size | 2 TB | 9.4 ZB |
| Boot partition | First sector | ESP (`/boot/efi`) |
| Secure Boot | No | Yes |
| Boot speed | Slower | Faster |
| Interface | Text | Graphical (optional) |

```bash
# Check if system is UEFI or BIOS
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "BIOS"

# View EFI boot entries
efibootmgr -v
```

---
## GRUB2 Bootloader

```bash
# Main config (generated, do NOT edit)
/boot/grub/grub.cfg

# Edit these instead:
/etc/default/grub              # GRUB settings
/etc/grub.d/                   # Script fragments

# Common settings in /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DEFAULT=0
GRUB_CMDLINE_LINUX="quiet splash"
GRUB_CMDLINE_LINUX_DEFAULT=""

# Regenerate config after changes
update-grub          # Debian/Ubuntu
grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL
```

---
## initramfs

Initial RAM filesystem loaded by the bootloader alongside the kernel.

```bash
# List contents of initramfs
lsinitramfs /boot/initrd.img-$(uname -r)

# Regenerate initramfs
update-initramfs -u

# Regenerate for all kernels
update-initramfs -u -k all

# Create with specific modules
update-initramfs -c -k $(uname -r)
```

Purpose:
- Load drivers needed to mount root filesystem
- Handle encrypted root partitions
- Assemble RAID/LVM before root mount

---
## systemd Overview

- Replacement for SysV `init`
- Parallel service startup
- On-demand activation (socket, D-Bus, path)
- Manages: services, mounts, timers, sockets, targets

```bash
# Check systemd version
systemd --version

# View the boot process tree
systemd-analyze critical-chain

# Boot time analysis
systemd-analyze blame

# Overall boot time
systemd-analyze time
```

---
## systemd Unit Types

| Unit Type | Extension | Purpose |
|-----------|-----------|---------|
| Service | `.service` | Daemons and processes |
| Socket | `.socket` | IPC/network sockets |
| Target | `.target` | Groups of units |
| Mount | `.mount` | Filesystem mounts |
| Timer | `.timer` | Scheduled tasks |
| Path | `.path` | File-based activation |
| Slice | `.slice` | Resource management groups |
| Scope | `.scope` | External process groups |

---
## systemd Targets (Runlevels)

Targets group units into meaningful states:

| Target | SysV Runlevel | Purpose |
|--------|---------------|---------|
| `poweroff.target` | 0 | System halt |
| `rescue.target` | 1 | Single-user mode |
| `multi-user.target` | 3 | Multi-user, no GUI |
| `graphical.target` | 5 | Multi-user with GUI |
| `reboot.target` | 6 | System reboot |

```bash
# View current target
systemctl get-default

# Change default target
systemctl set-default multi-user.target

# Switch target at runtime
systemctl isolate rescue.target
```

---
## systemctl Usage

```bash
# Start, stop, restart a service
systemctl start nginx
systemctl stop nginx
systemctl restart nginx

# Enable/disable at boot
systemctl enable nginx
systemctl disable nginx

# Check status
systemctl status nginx

# List all active services
systemctl list-units --type=service --state=running
```

---
## systemctl Advanced Usage

```bash
# Reload service config without restart
systemctl reload nginx

# Reload or restart (if reload not supported)
systemctl reload-or-restart nginx

# Mask a service (prevent starting entirely)
systemctl mask nginx
systemctl unmask nginx

# Show unit dependencies
systemctl list-dependencies nginx.service

# Show all failed units
systemctl --failed

# Show unit properties
systemctl show nginx.service -p MainPID
```

---
## Writing a systemd Unit File

```ini
[Unit]
Description=My Custom Application
After=network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/myapp
Restart=on-failure
RestartSec=5
User=myapp
Group=myapp

[Install]
WantedBy=multi-user.target
```

Save to `/etc/systemd/system/myapp.service`, then `systemctl daemon-reload`.

---
## Unit File: Service Types

| Type | Behavior |
|------|----------|
| `simple` | Default. Process started by `ExecStart` is the main process |
| `forking` | Process forks and parent exits. Use `PIDFile=` |
| `oneshot` | Process exits after finishing. Good for scripts |
| `notify` | Like `simple`, but sends notification when ready |
| `idle` | Like `simple`, but waits for other jobs to finish |

```ini
# Example: forking daemon
[Service]
Type=forking
PIDFile=/run/myapp/myapp.pid
ExecStart=/usr/local/bin/myapp --daemon
ExecReload=/bin/kill -HUP $MAINPID
```

---
## Unit File: Advanced Directives

```ini
[Service]
# Environment
Environment=NODE_ENV=production
EnvironmentFile=/etc/myapp/env

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

# Security hardening
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
NoNewPrivileges=yes
ReadWritePaths=/var/lib/myapp

# Watchdog
WatchdogSec=30
```

---
## systemd Timers

Timers replace traditional `cron` jobs with better logging and dependency management.

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# List active timers
systemctl list-timers --all
```

---
## systemd Timer: Calendar Expressions

```cron
OnCalendar=hourly
OnCalendar=daily
OnCalendar=weekly
OnCalendar=monthly
OnCalendar=*-*-* 04:00:00          # daily at 4am
OnCalendar=Mon..Fri *-*-* 09:00    # weekdays at 9am
OnCalendar=*-*-01 00:00:00         # first of month
OnCalendar=*:0/15                  # every 15 minutes
```

```bash
# Validate calendar expressions
systemd-analyze calendar "Mon..Fri *-*-* 09:00"

# Corresponding service unit is required
# backup.timer triggers backup.service
```

---
## systemd Timer vs Service Example

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily Backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=backup
```

```bash
# Enable and start the timer
systemctl enable --now backup.timer

# Manually trigger the service
systemctl start backup.service

# Check timer status
systemctl status backup.timer
journalctl -u backup.service --since today
```

---
## journalctl and the Journal

```bash
# View all logs
journalctl

# Follow logs in real time
journalctl -f

# Logs for a specific unit
journalctl -u nginx.service

# Logs since last boot
journalctl -b

# Logs from a time range
journalctl --since "2024-01-01" --until "2024-01-02"

# Show only errors and above
journalctl -p err
```

---
## journalctl Advanced Usage

```bash
# Show logs from previous boot
journalctl -b -1

# Kernel messages only
journalctl -k

# Output as JSON
journalctl -u nginx -o json-pretty

# Show disk usage of journal
journalctl --disk-usage

# Vacuum old entries
journalctl --vacuum-time=30d
journalctl --vacuum-size=500M

# Filter by executable
journalctl /usr/sbin/sshd

# Combine filters
journalctl -u nginx -p err --since "1 hour ago"
```

---
## Journal Persistence Configuration

```bash
# By default, journal may be volatile (RAM only)
# Make it persistent:
mkdir -p /var/log/journal
systemd-tmpfiles --create --prefix /var/log/journal
systemctl restart systemd-journald
```

```ini
# /etc/systemd/journald.conf
[Journal]
Storage=persistent
SystemMaxUse=500M
SystemKeepFree=1G
MaxRetentionSec=1month
MaxFileSec=1week
Compress=yes
```

---
## The /proc Filesystem

Virtual filesystem exposing kernel and process information:

```bash
# CPU info
cat /proc/cpuinfo

# Memory info
cat /proc/meminfo

# Running processes
ls /proc/[0-9]*

# Kernel command line
cat /proc/cmdline

# Per-process info
cat /proc/<PID>/status
cat /proc/<PID>/maps
cat /proc/<PID>/fd/
```

---
## Useful /proc Entries

```bash
# System uptime (seconds)
cat /proc/uptime

# Load average
cat /proc/loadavg

# Mounted filesystems
cat /proc/mounts

# Network statistics
cat /proc/net/dev

# Disk statistics
cat /proc/diskstats

# Kernel version
cat /proc/version

# Interrupt statistics
cat /proc/interrupts
```

---
## The /sys Filesystem

Exposes kernel objects (devices, drivers, buses):

```bash
# List block devices
ls /sys/block/

# View device attributes
cat /sys/block/sda/size
cat /sys/block/sda/queue/scheduler

# Network interface settings
cat /sys/class/net/eth0/address
cat /sys/class/net/eth0/speed
```

---
## Practical /sys Usage

```bash
# Change I/O scheduler
echo "mq-deadline" > /sys/block/sda/queue/scheduler

# Check available schedulers
cat /sys/block/sda/queue/scheduler

# View CPU frequency
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq

# View thermal zones (temperature)
cat /sys/class/thermal/thermal_zone0/temp

# Control laptop brightness
cat /sys/class/backlight/*/brightness

# View power supply status
cat /sys/class/power_supply/BAT0/status
```

---
## Kernel Tuning with sysctl

```bash
# View all parameters
sysctl -a

# View specific parameter
sysctl net.ipv4.ip_forward

# Set temporarily
sysctl -w net.ipv4.ip_forward=1

# Set permanently in /etc/sysctl.conf
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p
```

Common tunable parameters:
- `vm.swappiness` - swap aggressiveness
- `net.core.somaxconn` - max socket connections
- `fs.file-max` - max open file descriptors

---
## Important sysctl Parameters

```bash
# Network performance
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_max_syn_backlog = 8192

# Security
net.ipv4.conf.all.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0

# Memory
vm.overcommit_memory = 0
vm.dirty_ratio = 20
vm.dirty_background_ratio = 10

# Apply from drop-in directory
ls /etc/sysctl.d/
```

---
## Shared Libraries

```bash
# List shared libraries for a binary
ldd /usr/bin/python3

# View library search path
cat /etc/ld.so.conf

# Update library cache
ldconfig

# Add custom library path
echo "/opt/mylib/lib" > /etc/ld.so.conf.d/mylib.conf
ldconfig

# Check library cache
ldconfig -p | grep libssl
```

---
## Shared Library Troubleshooting

```bash
# "error while loading shared libraries" fix:
# 1. Find the missing library
apt-file search libfoo.so

# 2. Install the package that provides it
apt install libfoo-dev

# 3. Or add the path and rebuild cache
echo "/path/to/lib" > /etc/ld.so.conf.d/custom.conf
ldconfig

# LD_LIBRARY_PATH for temporary override
export LD_LIBRARY_PATH=/opt/custom/lib:$LD_LIBRARY_PATH

# LD_PRELOAD to override specific libraries
LD_PRELOAD=/path/to/custom/libc.so ./myprogram

# Check symbol resolution
nm -D /usr/lib/x86_64-linux-gnu/libssl.so
```

---
## Kernel Modules

Loadable kernel modules extend the kernel at runtime without rebooting.

```bash
# List loaded modules
lsmod

# Show module info
modinfo e1000e
modinfo ext4

# Load a module
modprobe br_netfilter

# Remove a module
modprobe -r br_netfilter

# Load with parameters
modprobe bonding mode=1 miimon=100

# List module parameters
modinfo -p ext4
```

---
## Kernel Module Configuration

```bash
# Persist module loading at boot
echo "br_netfilter" > /etc/modules-load.d/bridge.conf

# Set module parameters permanently
echo "options bonding mode=1 miimon=100" > \
  /etc/modprobe.d/bonding.conf

# Blacklist a module (prevent loading)
echo "blacklist nouveau" > \
  /etc/modprobe.d/blacklist-nouveau.conf

# Force regenerate initramfs after module changes
update-initramfs -u
```

```bash
# Verify a module is blacklisted
modprobe -n --first-time nouveau 2>&1
# Output: "modprobe: FATAL: Module nouveau is in blacklist"
```

---
## Device Management with `udev`

`udev` dynamically manages `/dev` entries when hardware is detected.

```bash
# Monitor device events in real time
udevadm monitor

# Query device attributes
udevadm info -a -n /dev/sda

# Trigger device re-detection
udevadm trigger

# Reload udev rules
udevadm control --reload-rules
```

```bash
# Custom udev rule: /etc/udev/rules.d/99-usb.rules
# Assign a persistent name to a USB drive
SUBSYSTEM=="block", ATTRS{serial}=="ABC123", \
  SYMLINK+="myusbdrive"
```

---
## `udev` Rule Examples

```bash
# /etc/udev/rules.d/99-custom.rules

# Set permissions on a device
KERNEL=="ttyUSB0", MODE="0666", GROUP="dialout"

# Run a script when a device is added
ACTION=="add", SUBSYSTEM=="usb", \
  ATTRS{idVendor}=="1234", \
  RUN+="/usr/local/bin/usb-handler.sh"

# Create persistent network interface names
SUBSYSTEM=="net", ACTION=="add", \
  ATTR{address}=="00:11:22:33:44:55", \
  NAME="lan0"
```

```bash
# Test a rule without applying
udevadm test /sys/class/net/eth0
```

---
## `systemd` Socket Activation

Socket activation starts services on-demand when a connection arrives.

```ini
# /etc/systemd/system/myapp.socket
[Unit]
Description=MyApp Socket

[Socket]
ListenStream=8080
Accept=false

[Install]
WantedBy=sockets.target
```

```bash
# Enable the socket (not the service)
systemctl enable --now myapp.socket

# The service starts only when traffic hits port 8080
systemctl status myapp.service  # inactive until first request

# List all listening sockets
systemctl list-sockets
```

---

## Socket Activation Benefits
![socket_activation_benefits](svg/courses/operating_systems/linux-system-administration/02_core_system_architecture/socket_activation_benefits.svg)

---
## Socket Activation Benefits
- Faster boot: services start only when needed
- No port conflicts: `systemd` holds sockets during restarts
- Zero-downtime restarts: connections queue while service restarts
- Reduced memory usage on idle systems

---
## Control Groups (`cgroups`)

`cgroups` limit and account for resource usage per process group.

```bash
# View cgroup hierarchy
systemd-cgls

# Show resource usage per cgroup
systemd-cgtop

# Set CPU limit on a service
systemctl set-property nginx.service CPUQuota=50%

# Set memory limit
systemctl set-property nginx.service MemoryMax=512M

# View current resource limits for a service
systemctl show nginx.service -p CPUQuota,MemoryMax
```

---
## `cgroups` in Unit Files

```ini
[Service]
# CPU controls
CPUQuota=200%           # 2 full cores max
CPUWeight=100           # relative weight (default 100)

# Memory controls
MemoryMax=1G            # hard limit (OOM kill)
MemoryHigh=800M         # soft limit (throttle)
MemorySwapMax=0         # disable swap for this unit

# I/O controls
IOWeight=50             # relative I/O weight
IOReadBandwidthMax=/dev/sda 50M
IOWriteBandwidthMax=/dev/sda 20M

# Process limits
TasksMax=512            # max number of tasks
```

```bash
# Verify limits are applied
cat /sys/fs/cgroup/system.slice/nginx.service/memory.max
```

---
## Kernel Parameters for Production

Recommended `sysctl` settings for production servers:

```bash
# /etc/sysctl.d/99-production.conf
# Harden network stack
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_tw_reuse = 1
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_keepalive_time = 600

# Memory management
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.min_free_kbytes = 65536

# File descriptor limits
fs.file-max = 2097152
fs.inotify.max_user_watches = 524288
```

```bash
# Apply and verify
sysctl --system
sysctl -a | grep vm.swappiness
```

---
## systemd Resource Control with `cgroups` v2

`cgroups` v2 provides a unified hierarchy for resource management.

```bash
# Check if cgroups v2 is active
mount | grep cgroup2
stat -fc %T /sys/fs/cgroup/

# View the unified hierarchy
ls /sys/fs/cgroup/
cat /sys/fs/cgroup/cgroup.controllers
```

```bash
# Create a transient resource-limited scope
systemd-run --scope -p MemoryMax=256M \
  -p CPUQuota=50% ./my-heavy-task

# Apply persistent overrides via drop-in
systemctl edit nginx.service
# [Service]
# MemoryMax=1G
# CPUQuota=200%
# TasksMax=1024

# Inspect effective cgroup limits
systemctl show nginx.service -p EffectiveCPUs
cat /sys/fs/cgroup/system.slice/nginx.service/cpu.max
```

---
## `systemd-tmpfiles`: Managing Temporary Files

`systemd-tmpfiles` creates, cleans, and removes volatile and temporary files.

```bash
# Configuration directories (priority order)
/etc/tmpfiles.d/       # admin overrides
/run/tmpfiles.d/       # runtime
/usr/lib/tmpfiles.d/   # package defaults
```

```ini
# /etc/tmpfiles.d/myapp.conf
# Type  Path                 Mode  User   Group  Age
d       /run/myapp           0755  myapp  myapp  -
f       /run/myapp/state     0644  myapp  myapp  -
D       /tmp/myapp-cache     0750  myapp  myapp  7d
```

```bash
# Apply tmpfiles configuration
systemd-tmpfiles --create
systemd-tmpfiles --clean
systemd-tmpfiles --remove

# Preview what would happen
systemd-tmpfiles --create --dry-run
```

---
## `systemd-sysusers`: Managing System Users

`systemd-sysusers` declaratively creates system users and groups at boot or package install.

```ini
# /etc/sysusers.d/myapp.conf
# Type  Name    ID     GECOS              Home
u       myapp   -      "My Application"   /var/lib/myapp
g       mygroup -      -                  -
m       myapp   mygroup
```

```bash
# Apply sysusers configuration
systemd-sysusers

# Preview changes
systemd-sysusers --dry-run

# List existing sysuser configs
ls /usr/lib/sysusers.d/
```

Advantages over manual `useradd`:
- Declarative and idempotent
- Runs early in boot before services start
- Automatically assigns UIDs from the system range

---
## `systemd-networkd` Overview

`systemd-networkd` is a built-in network manager for servers (alternative to `NetworkManager`).

```ini
# /etc/systemd/network/20-wired.network
[Match]
Name=eth0

[Network]
DHCP=yes

[DHCPv4]
UseDNS=true
```

```ini
# Static IP configuration
# /etc/systemd/network/20-static.network
[Match]
Name=eth0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=8.8.8.8
DNS=8.8.4.4
```

```bash
# Enable and start
systemctl enable --now systemd-networkd
networkctl list
networkctl status eth0
```

---
## Boot Troubleshooting: Rescue and Emergency Mode

When a system fails to boot normally, use rescue or emergency mode.

```bash
# Enter rescue mode (single-user with basic services)
systemctl isolate rescue.target
# Or at GRUB: append "systemd.unit=rescue.target"

# Enter emergency mode (minimal, root only)
systemctl isolate emergency.target
# Or at GRUB: append "systemd.unit=emergency.target"
```

| Mode | Root FS | Services | Use Case |
|------|---------|----------|----------|
| Rescue | Read-write | Minimal | Fix configs, services |
| Emergency | Read-only | None | Fix `/etc/fstab`, disk issues |

```bash
# In emergency mode, remount root as read-write
mount -o remount,rw /
# Fix the issue, then reboot
systemctl reboot
```

---
## GRUB Recovery Procedures

When GRUB itself is broken or the kernel fails to load:

```bash
# At GRUB menu, press 'e' to edit boot entry
# Add to linux line: "init=/bin/bash" for a root shell
# Or: "rd.break" to break into initramfs

# Reinstall GRUB from a live USB
mount /dev/sda2 /mnt
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
chroot /mnt
grub-install /dev/sda
update-grub
exit && reboot
```

```bash
# Recover from GRUB rescue prompt
grub rescue> ls                    # list partitions
grub rescue> set root=(hd0,gpt2)
grub rescue> set prefix=(hd0,gpt2)/boot/grub
grub rescue> insmod normal
grub rescue> normal
```

---
## Kernel Crash Dumps with `kdump`

`kdump` captures kernel memory when a crash (panic) occurs for post-mortem analysis.

```bash
# Install kdump tools
apt install linux-crashdump kdump-tools

# Enable kdump (reserves memory for crash kernel)
# /etc/default/grub
# GRUB_CMDLINE_LINUX="crashkernel=256M"
update-grub && reboot
```

```bash
# Verify kdump is active
kdump-config show
systemctl status kdump-tools

# Crash dumps are saved to /var/crash/
ls /var/crash/

# Analyze a crash dump
apt install crash
crash /usr/lib/debug/boot/vmlinux-$(uname -r) \
  /var/crash/dump.202401150930
```

---

## Device Mapper Overview

The device mapper (`dm`) is a kernel framework for mapping block devices. It underpins `LVM`, `LUKS`, and `multipath`.

---

## Device Mapper Overview

![device_mapper_overview](svg/courses/operating_systems/linux-system-administration/02_core_system_architecture/device_mapper_overview.svg)

---

## Device Mapper Overview

![device_mapper_overview](svg/courses/operating_systems/linux-system-administration/02_core_system_architecture/device_mapper_overview.svg)

---
## Device Mapper Overview
The device mapper (`dm`) is a kernel framework for mapping block devices. It underpins `LVM`, `LUKS`, and `multipath`.
```bash
# List device mapper devices
dmsetup ls
dmsetup info
dmsetup table    # show mapping tables
ls -l /dev/mapper/
```

---
## `/dev` Special Files

Key special device files every admin should know:

| Device | Purpose |
|--------|---------|
| `/dev/null` | Discards all data written to it |
| `/dev/zero` | Produces infinite zero bytes |
| `/dev/urandom` | Cryptographically secure random bytes |
| `/dev/full` | Always returns "disk full" on write |
| `/dev/tty` | Current terminal |
| `/dev/loop*` | Loop devices for mounting files |
| `/dev/mapper/*` | Device mapper virtual devices |

```bash
# Common usage patterns
command > /dev/null 2>&1          # discard output
dd if=/dev/zero of=file bs=1M count=100  # create empty file
head -c 32 /dev/urandom | base64  # generate random token
```

---
## Exercise: System Architecture Exploration

Perform the following tasks on your lab system:

1. Identify whether the system uses `UEFI` or `BIOS` and list the boot entries
1. Measure the boot time using `systemd-analyze` and find the 5 slowest services
1. Write a custom `systemd` unit file for a simple script that logs the date to `/var/log/myapp.log` every run
1. Create a `systemd` timer that triggers the service every 10 minutes
1. Apply the following `sysctl` parameters and verify they are active after reboot:
    - `vm.swappiness=10`
    - `net.ipv4.tcp_fin_timeout=15`
1. Use `systemd-tmpfiles` to create a configuration that ensures `/run/exercise` exists with mode `0755`
1. Explore `cgroups` by limiting a `stress` process to 256M of memory using `systemd-run`

```bash
# Hint: install stress for the last task
apt install stress
systemd-run --scope -p MemoryMax=256M stress --vm 1 --vm-bytes 512M
```

---
## Kernel Version Management

```bash
# Check running kernel version
uname -r
# Example: 6.8.0-41-generic

# List all installed kernels
dpkg -l | grep linux-image

# Remove old kernels (keep current + one previous)
apt autoremove --purge

# Manually remove a specific old kernel
apt remove --purge linux-image-6.5.0-35-generic

# DKMS (Dynamic Kernel Module Support)
# Automatically rebuilds third-party modules
# when a new kernel is installed
dkms status
dkms autoinstall -k $(uname -r)
```

```bash
# Pin a kernel to prevent removal
apt-mark hold linux-image-$(uname -r)

# On RHEL/Fedora
rpm -qa | grep kernel
dnf remove kernel-5.14.0-362.el9
```

---
## Understanding Load Average

Load average represents the average number of processes in a runnable or uninterruptible state.

```bash
# View load average (1, 5, 15 minute averages)
uptime
cat /proc/loadavg

# Compare to CPU count
nproc
# Load average < nproc = system is not overloaded
# Load average > nproc = processes are waiting
```

```bash
# Investigate high load
# Check for CPU-bound processes
top -bn1 | head -20

# Check for I/O-bound processes (D state)
ps aux | awk '$8 ~ /D/'

# Monitor in real time
vmstat 1 5
# Look at: r (runnable), b (blocked/IO-wait)

# Check I/O wait percentage
iostat -x 1 3
```

Rule of thumb: sustained load average above 2x `nproc` warrants investigation.

---
## File Descriptors and Limits

```bash
# System-wide maximum file descriptors
cat /proc/sys/fs/file-max
sysctl fs.file-max

# Currently open file descriptors system-wide
cat /proc/sys/fs/file-nr
# Format: allocated  free  maximum

# Per-process limits
ulimit -n          # soft limit (current shell)
ulimit -Hn         # hard limit

# Count open FDs for a specific process
ls /proc/<PID>/fd | wc -l
lsof -p <PID> | wc -l
```

```bash
# Increase system-wide limit
sysctl -w fs.file-max=2097152

# Increase per-user limits in /etc/security/limits.conf
# *  soft  nofile  4096
# *  hard  nofile  65536

# For systemd services, use LimitNOFILE= in unit files
```

---
## Locale and Timezone Configuration

```bash
# View current locale settings
localectl status
locale

# Set system locale
localectl set-locale LANG=en_US.UTF-8

# List available locales
localectl list-locales

# Generate a new locale
dpkg-reconfigure locales
# Or manually:
locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8
```

```bash
# View current timezone
timedatectl status

# Set timezone
timedatectl set-timezone America/New_York
timedatectl list-timezones | grep America

# Enable NTP synchronization
timedatectl set-ntp true

# Check NTP sync status
timedatectl timesync-status
```
