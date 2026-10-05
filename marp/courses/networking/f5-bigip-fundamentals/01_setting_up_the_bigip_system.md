---
tags:
  - networking:tcp-ip
  - networking:dns
  - architecture:load-balancing
  - practices:sysadmin
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Setting Up the BIG-IP System

---

## What This Chapter Covers

- What `BIG-IP` is and where `LTM` fits
- The platform: `TMM` data plane and the Linux control plane
- Full proxy architecture: client side and server side
- Initial setup: management interface, license, provisioning
- Device certificate and platform properties
- Network: interfaces, `VLAN`s, self `IP` addresses, routes
- `NTP` and `DNS` settings
- Archiving the configuration
- `F5` support resources: `AskF5`, `iHealth`, `qkview`

---

## What Is BIG-IP?

- An application delivery controller (`ADC`) from `F5`
- Sits between clients and the servers that run an application
- Terminates client connections and opens its own to the servers
- Load balances, translates addresses, offloads `TCP`, `HTTP` and `SSL`
- Applies security and traffic policies on the way through
- One software image (`TMOS`), many modules enabled by license

---

## BIG-IP Modules

| Module | Purpose |
| --- | --- |
| `LTM` | Local Traffic Manager: load balancing and traffic processing |
| `DNS` (formerly `GTM`) | Global server load balancing across data centers |
| `ASM` / `Advanced WAF` | Web application firewall |
| `APM` | Access Policy Manager: authentication, `VPN`, `SSO` |
| `AFM` | Advanced Firewall Manager: network firewall, `DDoS` |
| `AVR` | Application Visibility and Reporting: analytics |

- This course is about `LTM` only; every other module builds on it

---

## BIG-IP Platforms

| Platform | Form | Typical use |
| --- | --- | --- |
| `iSeries` appliance | Dedicated hardware with `FPGA` offload | Data center edge, high throughput |
| `VELOS` / `rSeries` | Chassis or appliance running tenants | Large consolidated deployments |
| `vCMP` guest | Virtual instance on `F5` hardware | Isolating teams on shared hardware |
| Virtual Edition (`VE`) | VM on `VMware`, `KVM`, `Hyper-V` | Labs, private cloud |
| `VE` in public cloud | `AWS`, `Azure`, `GCP` images | Cloud application delivery |

- Same `TMOS` software and same configuration on all of them
- Our lab uses two Virtual Edition systems

---

## Data Plane and Control Plane

![platform_planes](svg/courses/networking/f5-bigip-fundamentals/01_setting_up_the_bigip_system/platform_planes.svg)

---

## The Traffic Management Microkernel

- `TMM` is the process that carries all application traffic
- One `TMM` instance per CPU core, each with its own memory
- Runs its own `TCP/IP` stack, separate from the Linux kernel
- Handles load balancing, profiles, `SSL`, iRules and policies
- Hardware platforms add `FPGA` and `SSL` chips that `TMM` drives
- If `TMM` stops, traffic stops; the management `GUI` may still work

---

## The Linux Host Side

- `CentOS` based host that runs management services
- `mcpd`: master control program, holds the running configuration
- `httpd`: the Configuration utility (web `GUI`)
- `bigd`: runs health monitors against nodes and pool members
- `sshd`, `tmsh`, `snmpd`, `syslog-ng`
- Management traffic uses the host stack, not `TMM`

---

## Full Proxy Architecture

![full_proxy](svg/courses/networking/f5-bigip-fundamentals/01_setting_up_the_bigip_system/full_proxy.svg)

---

## Why a Full Proxy Matters

- The client finishes its `TCP` handshake with `BIG-IP`, not the server
- `BIG-IP` opens a separate connection to the chosen server
- Each side gets its own `TCP` settings, tuned for its network
- `BIG-IP` can read the full request before choosing a server
- `SSL` can be decrypted, inspected and re-encrypted in the middle
- A packet based load balancer can only forward or drop packets

---

## Initial Setup Sequence

![setup_sequence](svg/courses/networking/f5-bigip-fundamentals/01_setting_up_the_bigip_system/setup_sequence.svg)

---

## Configuring the Management Interface

- The management port (`mgmt`) is out of band, served by the Linux host
- On a new system, log in on the console as `root` (default password `default`)
- Run the `config` utility to set the management `IP`, mask and gateway
- Then browse to `https://<mgmt-ip>` and log in as `admin`
- Both `root` and `admin` passwords must be changed at first login

```bash
config
tmsh list sys management-ip
tmsh list sys management-route
```

---

## Management Interface From tmsh

```bash
tmsh create sys management-ip 192.168.1.245/24
tmsh create sys management-route default gateway 192.168.1.1
tmsh modify sys httpd allow replace-all-with { 192.168.1.0/24 }
tmsh modify sys sshd allow replace-all-with { 192.168.1.0/24 }
tmsh save sys config
```

- Restrict `GUI` and `SSH` to the admin network
- Never expose the management port to the internet

---

## Activating the Software License

- A base registration key identifies the product and the modules bought
- Automatic activation: `BIG-IP` contacts the `F5` license server directly
- Manual activation: copy the dossier, paste it at `activate.f5.com`, paste back the license
- System > License in the Configuration utility
- License file lives in `/config/bigip.license`
- Lab `VE` systems use trial or evaluation keys

```bash
tmsh show sys license
get_dossier -b XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX
```

---

## Provisioning Modules and Resources

- Licensing a module makes it available; provisioning turns it on
- Provisioning allocates CPU, memory and disk to each module
- System > Resource Provisioning
- Changing provisioning restarts services and interrupts traffic

```bash
tmsh modify sys provision ltm level nominal
tmsh show sys provision
```

---

## Provisioning Levels

| Level | Meaning |
| --- | --- |
| `none` | Module disabled, no resources |
| `minimum` | Smallest allocation, enough to run |
| `nominal` | Normal share of resources once all modules get their minimum |
| `dedicated` | All resources go to this one module; others must be `none` |

- Standard choice for an `LTM` box: `ltm` at `nominal`
- Over-provisioning a small `VE` makes it unstable: watch memory

---

## Importing a Device Certificate

- The device certificate secures the Configuration utility and device trust
- A new system generates a self-signed certificate
- Browsers warn about it; production replaces it with a CA signed one
- System > Certificate Management > Device Certificate Management
- Files: `/config/httpd/conf/ssl.crt/server.crt` and `ssl.key/server.key`
- Device trust between `BIG-IP` systems (day 3) also uses these certificates

---

## Specifying Platform Properties

- Host name: fully qualified, e.g. `bigip1.lab.local`
- Root and admin passwords
- `SSH` access and allowed source addresses
- Management port speed and duplex if needed
- Time zone (set under the `NTP` settings)

```bash
tmsh modify sys global-settings hostname bigip1.lab.local
tmsh modify auth password root
tmsh modify auth user admin prompt-for-password
```

---

## Lab Network Layout

![lab_network](svg/courses/networking/f5-bigip-fundamentals/01_setting_up_the_bigip_system/lab_network.svg)

---

## Network Objects

| Object | What it is | Lab example |
| --- | --- | --- |
| Interface | A physical or virtual port | `1.1`, `1.2`, `1.3` |
| Trunk | Several interfaces bundled with `LACP` | not used in the lab |
| `VLAN` | A layer 2 network bound to interfaces | `external`, `internal`, `ha` |
| Self `IP` | `BIG-IP` own address on a `VLAN` | `10.1.10.245/24` |
| Route | Where to send traffic for other networks | default via `10.1.10.1` |

- `TMM` only answers on self `IP` addresses and virtual addresses

---

## Interfaces and VLANs

- Interfaces are named `slot.port`: `1.1`, `1.2`
- A `VLAN` can be untagged on an interface or tagged with an 802.1Q tag
- One interface can carry many tagged `VLAN`s
- Network > `VLAN`s > `VLAN` List

```bash
tmsh show net interface
tmsh create net vlan external interfaces add { 1.1 { untagged } }
tmsh create net vlan internal interfaces add { 1.2 { untagged } }
tmsh create net vlan ha interfaces add { 1.3 { untagged } }
```

---

## Self IP Addresses

- A self `IP` gives `BIG-IP` an address on a `VLAN`
- Needed for `ARP`, for routing, and to reach servers on that `VLAN`
- Static self `IP`s belong to one device; floating ones move on failover
- Port lockdown controls which services answer on the self `IP`

```bash
tmsh create net self ext_self address 10.1.10.245/24 \
    vlan external allow-service none
tmsh create net self int_self address 10.1.20.245/24 \
    vlan internal allow-service none
tmsh create net self ha_self address 10.1.30.245/24 \
    vlan ha allow-service default
```

---

## Port Lockdown Options

| Setting | Services answered on the self `IP` |
| --- | --- |
| `Allow None` | Nothing except `ICMP` (default on new self `IP`s) |
| `Allow Default` | A fixed list: `SSH`, `HTTPS`, `SNMP`, `DNS`, `HA` ports |
| `Allow All` | Every port |
| `Allow Custom` | Only the protocols and ports you list |

- Use `Allow None` on networks facing clients
- The `HA` network needs `Allow Default` for sync and failover traffic

---

## Routes

- Connected networks are known automatically from self `IP`s
- Add a default route so `TMM` can reach clients beyond the gateway
- Management routes and `TMM` routes are separate tables

```bash
tmsh create net route default gw 10.1.10.1
tmsh list net route
tmsh show net route
```

| Table | Used by | Command |
| --- | --- | --- |
| `TMM` routes | Application traffic | `tmsh list net route` |
| Management routes | `GUI`, `SSH`, monitors from host | `tmsh list sys management-route` |

---

## Configuring NTP

- Accurate time is required for logs, certificates and `HA` sync
- Config sync between `BIG-IP` systems fails with large clock skew
- System > Configuration > Device > `NTP`

```bash
tmsh modify sys ntp servers replace-all-with { 0.pool.ntp.org 1.pool.ntp.org }
tmsh modify sys ntp timezone Asia/Jerusalem
ntpq -pn
```

- In `ntpq` output, a `*` marks the server currently selected

---

## Configuring DNS

- `BIG-IP` resolves names for `NTP` servers, license activation, updates
- Monitors and some features can use host names
- System > Configuration > Device > `DNS`

```bash
tmsh modify sys dns name-servers replace-all-with { 10.1.1.53 8.8.8.8 }
tmsh modify sys dns search replace-all-with { lab.local }
tmsh list sys dns
dig @10.1.1.53 www.f5.com
```

---

## Archiving the BIG-IP Configuration

- An archive is a `UCS` file: a full backup of the system
- System > Archives > Create
- Take one after initial setup and before every change window
- Copy archives off the box: a dead box takes its archives with it

```bash
tmsh save sys ucs /var/local/ucs/bigip1_initial.ucs
tmsh list sys ucs
tmsh load sys ucs /var/local/ucs/bigip1_initial.ucs
```

---

## Archive Formats Compared

| | `UCS` | `SCF` |
| --- | --- | --- |
| Format | Compressed tar archive | Single text file |
| Contents | Config, license, certificates, keys, users | Configuration only |
| Restores license | Yes (same device) | No |
| Readable and diffable | No | Yes |
| Typical use | Backup and disaster recovery | Templating, review, `git` |
| Command | `tmsh save sys ucs` | `tmsh save sys config file` |

- `UCS` with private keys can be encrypted: `passphrase` option

---

## F5 Support Resources

| Resource | What you get |
| --- | --- |
| `AskF5` (`my.f5.com`) | Knowledge base `K` articles, release notes, security advisories |
| `iHealth` | Upload a `qkview`, get diagnostics and known issue matches |
| `qkview` | Diagnostic snapshot of config, logs, statistics |
| `DevCentral` | Community answers, iRules code, articles |
| Support case | Engineer help; always attach a `qkview` |

---

## From Problem to Answer

![support_flow](svg/courses/networking/f5-bigip-fundamentals/01_setting_up_the_bigip_system/support_flow.svg)

---

## Creating a Diagnostic Snapshot

- System > Support > New Support Snapshot
- Or from the command line:

```bash
qkview
ls -l /var/tmp/*.qkview
scp root@192.168.1.245:/var/tmp/bigip1.qkview .
```

- Upload at `ihealth.f5.com` and read the Diagnostics tab
- `qkview` contains configuration: treat it as sensitive data
- Large log files are truncated; use `-s0` for full logs if asked

---

## Lab: Set Up the First BIG-IP

1. Log in on the console and set the management `IP` with `config`
1. Browse to the Configuration utility and run the Setup Utility
1. License the system and provision `LTM` at `nominal`
1. Set host name `bigip1.lab.local` and change both passwords
1. Create `VLAN`s `external`, `internal`, `ha` and their self `IP`s
1. Add the default route via `10.1.10.1`
1. Configure `NTP` and `DNS`, verify with `ntpq -pn` and `dig`
1. Save a `UCS` named `bigip1_initial.ucs` and copy it off the box

---

## Key Takeaways

- `BIG-IP` is a full proxy: two connections, two independent `TCP` stacks
- `TMM` carries traffic; the Linux host manages the box
- License enables modules, provisioning turns them on
- `VLAN`s, self `IP`s and routes give `TMM` its network presence
- Correct time and name resolution are prerequisites, not extras
- Archive early, archive often, and keep archives off the box
