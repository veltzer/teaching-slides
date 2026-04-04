# Linux Boot System
## Understanding systemd and Boot Process
---
## Linux Boot Sequence

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="30" width="95" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="57" y="52" text-anchor="middle" font-size="10" font-weight="bold">BIOS/UEFI</text>
  <text x="57" y="68" text-anchor="middle" font-size="8">POST, HW init</text>
  <rect x="125" y="30" width="85" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="167" y="52" text-anchor="middle" font-size="10" font-weight="bold">GRUB</text>
  <text x="167" y="68" text-anchor="middle" font-size="8">Bootloader</text>
  <rect x="230" y="30" width="85" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="272" y="52" text-anchor="middle" font-size="10" font-weight="bold">Kernel</text>
  <text x="272" y="68" text-anchor="middle" font-size="8">vmlinuz</text>
  <rect x="335" y="30" width="85" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="377" y="52" text-anchor="middle" font-size="10" font-weight="bold">initramfs</text>
  <text x="377" y="68" text-anchor="middle" font-size="8">Early root</text>
  <rect x="440" y="30" width="85" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="482" y="52" text-anchor="middle" font-size="10" font-weight="bold">systemd</text>
  <text x="482" y="68" text-anchor="middle" font-size="8">PID 1</text>
  <rect x="545" y="30" width="45" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="567" y="55" text-anchor="middle" font-size="8" font-weight="bold">Login</text>
  <line x1="105" y1="55" x2="125" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_11_boot_systemd)"/>
  <line x1="210" y1="55" x2="230" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_11_boot_systemd)"/>
  <line x1="315" y1="55" x2="335" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_11_boot_systemd)"/>
  <line x1="420" y1="55" x2="440" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_11_boot_systemd)"/>
  <line x1="525" y1="55" x2="545" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_11_boot_systemd)"/>
  <rect x="10" y="110" width="580" height="70" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="132" text-anchor="middle" font-size="11" font-weight="bold">Linux Boot Sequence</text>
  <text x="300" y="150" text-anchor="middle" font-size="10">Firmware -> Bootloader -> Kernel -> Init System -> User Space</text>
  <text x="300" y="168" text-anchor="middle" font-size="9">Each stage hands control to the next in sequence</text>
  <defs>
    <marker id="arrowd0_11_boot_systemd" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

1. BIOS/UEFI initialization
1. Bootloader (GRUB) loads kernel
1. Kernel initialization
1. systemd starts system
1. Services start in parallel
---
## Old SysV Init System

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="80" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="28" text-anchor="middle" font-size="10" font-weight="bold">RL 0</text>
  <text x="60" y="42" text-anchor="middle" font-size="8">Halt</text>
  <rect x="110" y="10" width="80" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="150" y="28" text-anchor="middle" font-size="10" font-weight="bold">RL 1</text>
  <text x="150" y="42" text-anchor="middle" font-size="8">Single User</text>
  <rect x="200" y="10" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="28" text-anchor="middle" font-size="10" font-weight="bold">RL 2</text>
  <text x="240" y="42" text-anchor="middle" font-size="8">Multi (no net)</text>
  <rect x="290" y="10" width="80" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="330" y="28" text-anchor="middle" font-size="10" font-weight="bold">RL 3</text>
  <text x="330" y="42" text-anchor="middle" font-size="8">Multi-user</text>
  <rect x="380" y="10" width="80" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="420" y="28" text-anchor="middle" font-size="10" font-weight="bold">RL 5</text>
  <text x="420" y="42" text-anchor="middle" font-size="8">Graphical</text>
  <rect x="470" y="10" width="80" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="28" text-anchor="middle" font-size="10" font-weight="bold">RL 6</text>
  <text x="510" y="42" text-anchor="middle" font-size="8">Reboot</text>
  <rect x="20" y="70" width="530" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="285" y="88" text-anchor="middle" font-size="11" font-weight="bold">SysV Init: /etc/init.d/ + /etc/rc{N}.d/</text>
  <text x="285" y="105" text-anchor="middle" font-size="9">Sequential startup: S01script -> S02script -> S03script...</text>
  <rect x="20" y="130" width="250" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="145" y="150" text-anchor="middle" font-size="10" font-weight="bold">SysV (Legacy)</text>
  <text x="145" y="168" text-anchor="middle" font-size="9">Sequential, slow boot</text>
  <rect x="300" y="130" width="250" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="425" y="150" text-anchor="middle" font-size="10" font-weight="bold">systemd (Modern)</text>
  <text x="425" y="168" text-anchor="middle" font-size="9">Parallel, dependency-based</text>
  <line x1="270" y1="155" x2="300" y2="155" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_11_boot_systemd)"/>
  <defs>
    <marker id="arrowd1_11_boot_systemd" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Traditional runlevels:
- 0: Halt
- 1: Single user
- 2: Multi-user (no networking)
- 3: Multi-user
- 4: User-defined
- 5: Graphical
- 6: Reboot

---
## systemd Introduction

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="10" width="200" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="12" font-weight="bold">systemd (PID 1)</text>
  <rect x="20" y="80" width="110" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="75" y="98" text-anchor="middle" font-size="10" font-weight="bold">systemctl</text>
  <text x="75" y="114" text-anchor="middle" font-size="8">Service mgmt</text>
  <rect x="145" y="80" width="110" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="200" y="98" text-anchor="middle" font-size="10" font-weight="bold">journald</text>
  <text x="200" y="114" text-anchor="middle" font-size="8">Logging</text>
  <rect x="270" y="80" width="110" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="325" y="98" text-anchor="middle" font-size="10" font-weight="bold">cgroups</text>
  <text x="325" y="114" text-anchor="middle" font-size="8">Resource ctrl</text>
  <rect x="395" y="80" width="110" height="45" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="450" y="98" text-anchor="middle" font-size="10" font-weight="bold">socket act.</text>
  <text x="450" y="114" text-anchor="middle" font-size="8">On-demand</text>
  <line x1="200" y1="50" x2="75" y2="80" stroke="#333" stroke-width="1"/>
  <line x1="250" y1="50" x2="200" y2="80" stroke="#333" stroke-width="1"/>
  <line x1="350" y1="50" x2="325" y2="80" stroke="#333" stroke-width="1"/>
  <line x1="400" y1="50" x2="450" y2="80" stroke="#333" stroke-width="1"/>
  <rect x="50" y="150" width="500" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="172" text-anchor="middle" font-size="10">Parallel startup | Dependency resolution | Declarative config</text>
</svg>

Key features:
- Service management
- Dependency resolution
- Parallel execution
- On-demand services
- Resource control
- Logging (journald)

---
## systemd Units

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="170" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="30" text-anchor="middle" font-size="11" font-weight="bold">.service</text>
  <text x="105" y="46" text-anchor="middle" font-size="9">Daemons, processes</text>
  <rect x="215" y="10" width="170" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">.socket</text>
  <text x="300" y="46" text-anchor="middle" font-size="9">IPC / network activation</text>
  <rect x="410" y="10" width="170" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="30" text-anchor="middle" font-size="11" font-weight="bold">.target</text>
  <text x="495" y="46" text-anchor="middle" font-size="9">Group of units</text>
  <rect x="20" y="70" width="170" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="90" text-anchor="middle" font-size="11" font-weight="bold">.mount</text>
  <text x="105" y="106" text-anchor="middle" font-size="9">Filesystem mounts</text>
  <rect x="215" y="70" width="170" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="90" text-anchor="middle" font-size="11" font-weight="bold">.timer</text>
  <text x="300" y="106" text-anchor="middle" font-size="9">Scheduled tasks (cron)</text>
  <rect x="410" y="70" width="170" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="90" text-anchor="middle" font-size="11" font-weight="bold">.device</text>
  <text x="495" y="106" text-anchor="middle" font-size="9">Hardware devices</text>
  <rect x="50" y="140" width="500" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="158" text-anchor="middle" font-size="10" font-weight="bold">Unit files: /etc/systemd/system/ and /lib/systemd/system/</text>
  <text x="300" y="172" text-anchor="middle" font-size="9">systemctl list-units --type=service | socket | timer</text>
</svg>

Common unit types:

```bash
# Service units
.service    # System services
.socket     # IPC/network sockets
.target     # Group of units
.mount      # Filesystem mounts
.timer      # Scheduled tasks
.device     # Hardware devices
```

---
## Basic systemctl Commands

```bash
# List units
systemctl list-units
systemctl list-units --type=service

# Check status
systemctl status nginx.service

# Start/stop service
systemctl start nginx.service
systemctl stop nginx.service

# Enable/disable on boot
systemctl enable nginx.service
systemctl disable nginx.service
```

---
## Service Management

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="230" y="10" width="140" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="33" text-anchor="middle" font-size="11" font-weight="bold">Active (running)</text>
  <rect x="30" y="80" width="100" height="35" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="103" text-anchor="middle" font-size="10" font-weight="bold">Inactive</text>
  <rect x="470" y="80" width="100" height="35" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="103" text-anchor="middle" font-size="10" font-weight="bold">Failed</text>
  <rect x="230" y="80" width="140" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="103" text-anchor="middle" font-size="10" font-weight="bold">Reloading</text>
  <line x1="130" y1="97" x2="230" y2="30" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd4_11_boot_systemd)"/>
  <text x="155" y="55" text-anchor="middle" font-size="9" fill="#2e7d32">start</text>
  <line x1="230" y1="30" x2="130" y2="97" stroke="#c62828" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd4_11_boot_systemd)"/>
  <text x="205" y="75" text-anchor="middle" font-size="9" fill="#c62828">stop</text>
  <line x1="370" y1="27" x2="470" y2="90" stroke="#c62828" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="445" y="55" text-anchor="middle" font-size="9" fill="#c62828">error</text>
  <line x1="300" y1="45" x2="300" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_11_boot_systemd)"/>
  <text x="330" y="65" text-anchor="middle" font-size="9">reload</text>
  <rect x="150" y="145" width="300" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="162" text-anchor="middle" font-size="10" font-weight="bold">restart = stop + start</text>
  <text x="300" y="178" text-anchor="middle" font-size="9">journalctl -u service = view logs</text>
  <defs>
    <marker id="arrowd4_11_boot_systemd" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Common operations:

```bash
# Manage service
systemctl start service
systemctl stop service
systemctl restart service
systemctl reload service
systemctl status service

# View service logs
journalctl -u service
```

---
## Writing systemd Service Files

Location: `/etc/systemd/system/myservice.service`

```ini
[Unit]
Description=My Custom Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/myapp
User=myuser
Group=mygroup
Restart=always

[Install]
WantedBy=multi-user.target
```

---
## Service File Sections

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="170" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="30" text-anchor="middle" font-size="11" font-weight="bold">[Unit]</text>
  <text x="105" y="48" text-anchor="middle" font-size="9">Description=</text>
  <text x="105" y="62" text-anchor="middle" font-size="9">After=network.target</text>
  <text x="105" y="76" text-anchor="middle" font-size="9">Requires= / Wants=</text>
  <rect x="215" y="10" width="170" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">[Service]</text>
  <text x="300" y="48" text-anchor="middle" font-size="9">Type=simple|forking</text>
  <text x="300" y="62" text-anchor="middle" font-size="9">ExecStart=/usr/bin/app</text>
  <text x="300" y="76" text-anchor="middle" font-size="9">Restart=always</text>
  <rect x="410" y="10" width="170" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="30" text-anchor="middle" font-size="11" font-weight="bold">[Install]</text>
  <text x="495" y="48" text-anchor="middle" font-size="9">WantedBy=</text>
  <text x="495" y="62" text-anchor="middle" font-size="9">multi-user.target</text>
  <text x="495" y="76" text-anchor="middle" font-size="9">(enable/disable)</text>
  <line x1="190" y1="50" x2="215" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_11_boot_systemd)"/>
  <line x1="385" y1="50" x2="410" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_11_boot_systemd)"/>
  <rect x="50" y="115" width="500" height="65" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" font-weight="bold">Service File: /etc/systemd/system/myservice.service</text>
  <text x="300" y="153" text-anchor="middle" font-size="9">[Unit] = metadata + dependencies | [Service] = how to run | [Install] = when to enable</text>
  <text x="300" y="168" text-anchor="middle" font-size="9">After editing: systemctl daemon-reload</text>
  <defs>
    <marker id="arrowd5_11_boot_systemd" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Common options:

```ini
# Unit section
Description=
After=
Requires=
Wants=

# Service section
Type=
ExecStart=
User=
Restart=

# Install section
WantedBy=
```

---
## Dependency Management

```bash
# View dependencies
systemctl list-dependencies nginx.service

# Check reverse dependencies
systemctl list-dependencies --reverse nginx.service

# Show unit dependencies
systemctl show -p "Requires" nginx.service
systemctl show -p "Wants" nginx.service
```

---
## rc.local Compatibility

For legacy support:

```bash
# Create rc-local service
/etc/systemd/system/rc-local.service

[Unit]
Description=RC Local
After=network.target

[Service]
Type=forking
ExecStart=/etc/rc.local
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

---
## Writing Custom init.d Scripts

```bash
#!/bin/bash
### BEGIN INIT INFO
# Provides:          myservice
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: My service
### END INIT INFO

case "$1" in
    start)
        echo "Starting service"
        ;;
    stop)
        echo "Stopping service"
        ;;
    restart)
        echo "Restarting service"
        ;;
    status)
        echo "Service status"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
```

---
## Systemd Targets

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="130" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="28" text-anchor="middle" font-size="10" font-weight="bold">rescue.target</text>
  <text x="85" y="44" text-anchor="middle" font-size="8">Single user (RL 1)</text>
  <rect x="165" y="10" width="130" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="28" text-anchor="middle" font-size="10" font-weight="bold">multi-user</text>
  <text x="230" y="44" text-anchor="middle" font-size="8">CLI mode (RL 3)</text>
  <rect x="310" y="10" width="130" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="28" text-anchor="middle" font-size="10" font-weight="bold">graphical</text>
  <text x="375" y="44" text-anchor="middle" font-size="8">GUI mode (RL 5)</text>
  <rect x="455" y="10" width="130" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="28" text-anchor="middle" font-size="10" font-weight="bold">reboot.target</text>
  <text x="520" y="44" text-anchor="middle" font-size="8">Reboot (RL 6)</text>
  <line x1="150" y1="32" x2="165" y2="32" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_11_boot_systemd)"/>
  <line x1="295" y1="32" x2="310" y2="32" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_11_boot_systemd)"/>
  <rect x="80" y="75" width="440" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="93" text-anchor="middle" font-size="10" font-weight="bold">Targets group units with dependencies (Wants= / Requires=)</text>
  <text x="300" y="110" text-anchor="middle" font-size="9">graphical.target depends on multi-user.target depends on basic.target</text>
  <rect x="40" y="140" width="250" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="165" y="158" text-anchor="middle" font-size="10" font-weight="bold">systemctl get-default</text>
  <text x="165" y="175" text-anchor="middle" font-size="9">Show current default target</text>
  <rect x="310" y="140" width="250" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="435" y="158" text-anchor="middle" font-size="10" font-weight="bold">systemctl isolate</text>
  <text x="435" y="175" text-anchor="middle" font-size="9">Switch to target immediately</text>
  <defs>
    <marker id="arrowd6_11_boot_systemd" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Target management:

```bash
# Get default target
systemctl get-default

# Set default target
systemctl set-default multi-user.target

# Switch target
systemctl isolate graphical.target
```

---
## Troubleshooting Boot Issues

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="170" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="30" text-anchor="middle" font-size="11" font-weight="bold">journalctl -b</text>
  <text x="105" y="48" text-anchor="middle" font-size="9">Current boot logs</text>
  <rect x="215" y="10" width="170" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">systemctl --failed</text>
  <text x="300" y="48" text-anchor="middle" font-size="9">List failed units</text>
  <rect x="410" y="10" width="170" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="30" text-anchor="middle" font-size="11" font-weight="bold">dmesg</text>
  <text x="495" y="48" text-anchor="middle" font-size="9">Kernel ring buffer</text>
  <line x1="105" y1="65" x2="105" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_11_boot_systemd)"/>
  <line x1="300" y1="65" x2="300" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_11_boot_systemd)"/>
  <line x1="495" y1="65" x2="495" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_11_boot_systemd)"/>
  <rect x="20" y="95" width="170" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="105" y="112" text-anchor="middle" font-size="9">Service-level issues</text>
  <text x="105" y="126" text-anchor="middle" font-size="9">journalctl -u svc</text>
  <rect x="215" y="95" width="170" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="112" text-anchor="middle" font-size="9">Dependency errors</text>
  <text x="300" y="126" text-anchor="middle" font-size="9">Missing config</text>
  <rect x="410" y="95" width="170" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="495" y="112" text-anchor="middle" font-size="9">Hardware / driver</text>
  <text x="495" y="126" text-anchor="middle" font-size="9">Early boot issues</text>
  <rect x="50" y="155" width="500" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="175" text-anchor="middle" font-size="10">Tip: Boot with systemd.unit=rescue.target for recovery mode</text>
  <defs>
    <marker id="arrowd7_11_boot_systemd" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Debug commands:

```bash
# View boot logs
journalctl -b

# Check failed units
systemctl --failed

# Boot messages
dmesg

# System status
systemctl status
```

---
## Best Practices

1. Service Management:

```bash
# Verify syntax
systemd-analyze verify myservice.service

# Test service
systemctl start myservice.service
systemctl status myservice.service
journalctl -u myservice.service
```

1. Security:

```ini
[Service]
# Restrict service
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
```
