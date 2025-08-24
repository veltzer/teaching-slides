# Processes in Linux

---

## Chapter Overview

1. **Process Tree and Init**
1. **Process Creation**
1. **Process States**
1. **Waiting and Zombies**
1. **Fork and Exec**
1. **Containers and Systemd**
1. **Advanced Process Management**

---

## What is a Process?

## Definition:
- **Running instance** of a program
- Has its own **memory space**
- Owns **resources** (files, sockets)
- Identified by **PID** (Process ID)
- Scheduled by the **kernel**

---

## Process vs Program

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="300" height="300" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="200" y="30" text-anchor="middle" font-size="16" font-weight="bold">Program (on disk)</text>
  <rect x="70" y="80" width="260" height="40" fill="#2980B9" stroke="#333" stroke-width="1"/>
  <text x="200" y="105" text-anchor="middle" fill="white" font-size="12">Binary executable</text>
  <rect x="70" y="140" width="260" height="40" fill="#2980B9" stroke="#333" stroke-width="1"/>
  <text x="200" y="165" text-anchor="middle" fill="white" font-size="12">Static data</text>
  <rect x="70" y="200" width="260" height="40" fill="#2980B9" stroke="#333" stroke-width="1"/>
  <text x="200" y="225" text-anchor="middle" fill="white" font-size="12">No state</text>

  <rect x="450" y="50" width="300" height="300" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="600" y="30" text-anchor="middle" font-size="16" font-weight="bold">Process (in memory)</text>
  <rect x="470" y="80" width="260" height="40" fill="#C0392B" stroke="#333" stroke-width="1"/>
  <text x="600" y="105" text-anchor="middle" fill="white" font-size="12">Code + Data</text>
  <rect x="470" y="140" width="260" height="40" fill="#C0392B" stroke="#333" stroke-width="1"/>
  <text x="600" y="165" text-anchor="middle" fill="white" font-size="12">Stack + Heap</text>
  <rect x="470" y="200" width="260" height="40" fill="#C0392B" stroke="#333" stroke-width="1"/>
  <text x="600" y="225" text-anchor="middle" fill="white" font-size="12">PID, State, Resources</text>
  <rect x="470" y="260" width="260" height="40" fill="#C0392B" stroke="#333" stroke-width="1"/>
  <text x="600" y="285" text-anchor="middle" fill="white" font-size="12">CPU context</text>
</svg>

---

## The Process Tree

```txt
systemd (PID 1)
├── systemd-journald
├── systemd-networkd
├── sshd
│   └── sshd (user session)
│       └── bash
│           └── vim
├── cron
├── nginx
│   ├── nginx (worker)
│   └── nginx (worker)
└── docker
    └── container-init
        └── application
```

---

## Process Hierarchy

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="50" r="30" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="400" y="55" text-anchor="middle" fill="white" font-size="12">init (1)</text>

  <circle cx="200" cy="150" r="25" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">sshd</text>

  <circle cx="400" cy="150" r="25" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="400" y="155" text-anchor="middle" fill="white" font-size="11">cron</text>

  <circle cx="600" cy="150" r="25" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="600" y="155" text-anchor="middle" fill="white" font-size="11">nginx</text>

  <circle cx="150" cy="250" r="25" fill="#2ECC71" stroke="#333" stroke-width="2"/>
  <text x="150" y="255" text-anchor="middle" fill="white" font-size="11">bash</text>

  <circle cx="250" cy="250" r="25" fill="#2ECC71" stroke="#333" stroke-width="2"/>
  <text x="250" y="255" text-anchor="middle" fill="white" font-size="11">bash</text>

  <circle cx="550" cy="250" r="25" fill="#2ECC71" stroke="#333" stroke-width="2"/>
  <text x="550" y="255" text-anchor="middle" fill="white" font-size="11">worker</text>

  <circle cx="650" cy="250" r="25" fill="#2ECC71" stroke="#333" stroke-width="2"/>
  <text x="650" y="255" text-anchor="middle" fill="white" font-size="11">worker</text>

  <line x1="380" y1="75" x2="220" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="80" x2="400" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="420" y1="75" x2="580" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="190" y1="175" x2="160" y2="225" stroke="#333" stroke-width="2"/>
  <line x1="210" y1="175" x2="240" y2="225" stroke="#333" stroke-width="2"/>
  <line x1="590" y1="175" x2="560" y2="225" stroke="#333" stroke-width="2"/>
  <line x1="610" y1="175" x2="640" y2="225" stroke="#333" stroke-width="2"/>

  <text x="400" y="350" text-anchor="middle" font-size="12">Every process has exactly one parent (except init)</text>
</svg>

---

## Init Process (PID 1)

## Special Properties:

1. **First user-space process**
1. **Parent of all processes**
1. **Cannot die** (kernel panic if it does)
1. **Adopts orphans**
1. **Reaps zombies**
1. **Handles system startup/shutdown**

---

## Modern Init Systems

| System | Used By | Features |
|--------|---------|----------|
| **systemd** | Most modern distros | Parallel, dependencies |
| **SysV init** | Old systems | Sequential, scripts |
| **OpenRC** | Gentoo, Alpine | Dependency-based |
| **runit** | Void Linux | Supervision |
| **Upstart** | Old Ubuntu | Event-driven |

---

## Systemd Architecture

```txt
systemd (PID 1)
├── System Services
│   ├── systemd-journald (logging)
│   ├── systemd-networkd (network)
│   ├── systemd-resolved (DNS)
│   └── systemd-timesyncd (NTP)
├── User Sessions
│   └── systemd --user
│       ├── dbus
│       └── user services
└── Targets
    ├── multi-user.target
    ├── graphical.target
    └── rescue.target
```

---

## Systemd Unit Files

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target
Requires=postgresql.service

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/start
ExecStop=/opt/myapp/bin/stop
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## Container Initialization

## Docker Init Problem:

```dockerfile
# Bad: app doesn't handle signals
FROM ubuntu
CMD ["/app/myapp"]

# Good: proper init system
FROM ubuntu
RUN apt-get install -y dumb-init
ENTRYPOINT ["dumb-init", "--"]
CMD ["/app/myapp"]
```

---

## Container Init Systems

```c
// Minimal init (dumb
