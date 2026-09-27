---
tags:
  - networking:http
  - architecture:load-balancing
  - networking:troubleshooting
level: advanced
category: networking
audience:
  - audiences:security-engineers
  - audiences:network-engineers
  - audiences:devops
  - audiences:sysadmins

---

# Introducing the BIG-IP System

---

## What This Chapter Covers

- The `BIG-IP` platform and the traffic management microkernel
- Full proxy architecture: two connections per client
- Virtual servers, pools, nodes, monitors and profiles
- Where iRules attach in the object model
- Initial setup and `tmsh` basics
- Archiving the configuration with `UCS` and `SCF`
- Support resources: `AskF5`, `iHealth`, `qkview`

---

## The BIG-IP Platform

- Application delivery controller from `F5`
- Hardware appliance, `vCMP` guest or Virtual Edition
- Modules: `LTM` (load balancing), `ASM` (`WAF`), `APM`, `DNS`, `AFM`
- One system image, modules enabled by license and provisioning
- Everything in this course runs on `LTM`

---

## Control Plane and Data Plane

![control_data_plane](svg/courses/networking/f5-bigip-advanced-irules/01_introducing_the_bigip_system/control_data_plane.svg)

---

## The Traffic Management Microkernel

- `TMM` is a user space process that owns the data plane
- One `TMM` instance pinned per CPU core, each with its own memory
- Runs its own `TCP/IP` stack, not the Linux one
- Polls the NICs directly; no interrupts, no kernel copies
- iRules execute inside `TMM`, on the packet path
- A slow iRule slows every connection on that core

---

## The Linux Host Side

- Management `GUI` (`httpd`), `tmsh`, `SSH`, `SNMP`
- `mcpd`: master control program, the configuration database
- Logging via `syslog-ng` to `/var/log/ltm`
- Monitors run from the host (`bigd`), not from `TMM`
- Host side is slow and shared; data plane is fast and isolated

---

## Full Proxy Architecture

![full_proxy](svg/courses/networking/f5-bigip-advanced-irules/01_introducing_the_bigip_system/full_proxy.svg)

---

## Why Full Proxy Matters

- Client side and server side are two separate `TCP` connections
- Each side has its own profiles: `TCP`, `SSL`, `HTTP`
- `BIG-IP` terminates the client, reads the request, then chooses a server
- Anything can be inspected or rewritten between the two sides
- This is the property that makes iRules possible
- Contrast: a packet forwarder can only pass or drop

---

## The Object Model

![object_model](svg/courses/networking/f5-bigip-advanced-irules/01_introducing_the_bigip_system/object_model.svg)

---

## Virtual Servers, Pools and Nodes

- Node: a backend `IP` address
- Pool member: a node plus a port, with a load balancing weight
- Pool: a set of members and a load balancing method
- Monitor: health check attached to a pool or node
- Virtual server: the listener (`IP:port`) that clients connect to
- The virtual server references profiles, a pool and iRules

---

## Where iRules Fit In

- iRules are a resource of the virtual server
- A virtual server can have zero, one or many iRules
- Profiles decide which events exist: no `HTTP` profile, no `HTTP_REQUEST`
- Policies and iRules both run after profiles parse the traffic
- Same iRule can be attached to many virtual servers

---

## Initial Setup

1. Set the management `IP` from the console or `config` utility
1. Activate the license and provision `LTM`
1. Create `VLANs` and self `IPs` for the internal and external networks
1. Create nodes, a pool and a virtual server
1. Save the configuration

```bash
tmsh create net vlan internal interfaces add { 1.1 }
tmsh create net self 10.1.1.5/24 vlan internal
tmsh create ltm pool web_pool members add { 10.1.1.10:80 10.1.1.11:80 } \
    monitor http
tmsh create ltm virtual vs_web destination 10.1.10.100:80 \
    pool web_pool profiles add { http }
tmsh save sys config
```

---

## Working With tmsh

- `tmsh` is the traffic management shell: full `CLI` for `BIG-IP`
- Every `GUI` action has a `tmsh` equivalent
- Interactive mode: type `tmsh`, then `list`, `create`, `modify`, `delete`
- Non-interactive: `tmsh <command>` from the `bash` prompt

```bash
tmsh list ltm virtual vs_web
tmsh list ltm pool web_pool
tmsh show ltm pool web_pool members
tmsh modify ltm virtual vs_web pool web_pool2
tmsh save sys config
```

---

## Archiving the Configuration

| Archive | Command | Contains |
| --- | --- | --- |
| `UCS` | `tmsh save sys ucs backup.ucs` | Config, certificates, keys, license, users |
| `SCF` | `tmsh save sys config file backup.scf` | Config only, single text file |

- `UCS` is the full backup: restore a replaced box with it
- `SCF` is readable text: diff it, review it, keep it in `git`
- Always take a `UCS` before a software upgrade
- Files land in `/var/local/ucs` and `/var/local/scf`

---

## F5 Support Resources

- `AskF5` (`my.f5.com`): knowledge base, release notes, `CVE` notices
- `iHealth`: upload a `qkview`, get a health report and known issues
- `qkview`: a diagnostic snapshot of config, logs and statistics
- `DevCentral`: community, iRule wiki, code share, Q&A
- Open a support case with a `qkview` attached, always

```bash
tmsh run util qkview
ls -l /var/tmp/*.qkview
```
