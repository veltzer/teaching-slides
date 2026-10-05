---
tags:
  - architecture:load-balancing
  - networking:tcp-ip
  - networking:troubleshooting
  - practices:sysadmin
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Configuring High Availability

---

## What This Chapter Covers

- High availability concepts: active-standby and active-active
- The three `HA` addresses: `ConfigSync`, failover and mirroring
- Device trust between `BIG-IP` systems
- Sync-failover device groups
- Traffic groups and floating self `IP` addresses
- Synchronizing the configuration between devices
- Failover triggers: network failover, `HA` groups, `VLAN` fail-safe
- Connection and persistence mirroring
- Testing failover and verifying that traffic keeps flowing

---

## Why One BIG-IP Is Not Enough

- Every application behind the `BIG-IP` depends on it
- A single device is a single point of failure
- Hardware fails, software upgrades need a reboot, licenses expire
- `HA` lets a second device take over the traffic in seconds
- Maintenance becomes routine: upgrade the standby, fail over, upgrade the other
- Goal of this chapter: two lab systems that act as one

---

## The Basic Idea

- Two (or more) `BIG-IP` systems share the same configuration
- The addresses that clients and servers use float between them
- At any moment exactly one device answers for each floating address
- Devices exchange heartbeats and watch each other
- When the active device stops answering, the peer claims the addresses
- Clients and servers see the same `IP` and `MAC` behavior, just a different box

---

## Active-Standby Topology

![ha_pair_topology](svg/courses/networking/f5-bigip-fundamentals/09_configuring_high_availability/ha_pair_topology.svg)

---

## Active-Standby and Active-Active

| Aspect | Active-standby | Active-active |
| --- | --- | --- |
| Traffic groups | One, active on one device | Two or more, spread over devices |
| Normal load | One device carries all traffic | Each device carries part of it |
| Failover result | Standby takes everything | Survivor carries both groups |

---

## Operating Each HA Mode

| Aspect | Active-standby | Active-active |
| --- | --- | --- |
| Capacity planning | Simple: one box must fit all | Each box must fit the total load |
| Troubleshooting | Easy: one place to look | Harder: traffic is split |
| Typical use | Most deployments | Squeezing value from both boxes |

---

## A Word on Active-Active

- Sounds like double the capacity, but it is not
- If both devices run at 70%, one device must run at 140% after a failure
- Each device must still be sized for the full load
- Benefit: the standby hardware is warm and proven, not idle
- Cost: more traffic groups, more floating addresses, more to reason about
- Start with active-standby; move to active-active only for a clear reason

---

## The Building Blocks

![trust_group_traffic_layers](svg/courses/networking/f5-bigip-fundamentals/09_configuring_high_availability/trust_group_traffic_layers.svg)

---

## The Order of Work

1. Prepare each device on its own: license, provisioning, `VLAN`s, self `IP`s
1. Set the `HA` addresses on each device: `ConfigSync`, failover, mirroring
1. Build device trust from one device
1. Create a sync-failover device group with both devices
1. Run the first config sync
1. Create floating self `IP`s in a traffic group
1. Build the application objects once, then sync
1. Test failover

---

## What Each Device Keeps Local

- Management `IP`, hostname, license, provisioning
- Interfaces, trunks and `VLAN`s
- Non-floating self `IP` addresses (`traffic-group-local-only`)
- Device certificate and `HA` address settings
- Everything else is shared: pools, virtual servers, profiles, monitors, iRules
- Rule of thumb: if it names the hardware, it is local

---

## Configuring High Availability Options

- Each device advertises three kinds of `HA` addresses
- Set them on each device under Device Management > Devices > (this device)
- Use self `IP` addresses on a dedicated `HA` `VLAN` where possible
- Non-floating self `IP`s only: floating addresses move, these must not
- Port lockdown on the `HA` self `IP` must allow the `HA` ports (`Allow Default`)

---

## The Three HA Addresses

| Address | Purpose | Recommended setting |
| --- | --- | --- |
| `ConfigSync` | Carries config changes between members | `HA` `VLAN` self `IP` |
| Failover unicast | Heartbeats, `UDP` 1026 | `HA` `VLAN` self `IP` plus management `IP` |
| Failover multicast | Heartbeats on hardware with serial link | Optional, management interface |

---

## Mirroring Addresses

| Address | Purpose | Recommended setting |
| --- | --- | --- |
| Primary mirroring | Connection and persistence state | `HA` `VLAN` self `IP` |
| Secondary mirroring | Backup path for mirroring | Another `VLAN` self `IP` |

---

## Setting the HA Addresses With tmsh

```bash
# on bigip1 (self IP 10.1.30.245 on VLAN ha)
tmsh modify cm device bigip1.lab.local \
    configsync-ip 10.1.30.245 \
    unicast-address { { ip 10.1.30.245 } { ip 192.168.1.245 } } \
    mirror-ip 10.1.30.245
# on bigip2
tmsh modify cm device bigip2.lab.local \
    configsync-ip 10.1.30.246 \
    unicast-address { { ip 10.1.30.246 } { ip 192.168.1.246 } } \
    mirror-ip 10.1.30.246
```

- Two unicast failover addresses give two independent heartbeat paths
- The device name must match `tmsh list cm device` on each box

---

## Establishing Device Trust

- Devices must trust each other before they share anything
- Each `BIG-IP` has a device certificate created at install time
- Trust is built by exchanging and confirming those certificates
- Done once, from one device, against the peer management `IP`
- Requires the peer admin user and password at that moment only
- After trust is built, members talk over mutual `TLS`

---

## How Device Trust Is Built

![device_trust](svg/courses/networking/f5-bigip-fundamentals/09_configuring_high_availability/device_trust.svg)

---

## Device Trust in the GUI and tmsh

- GUI: Device Management > Device Trust > Device Trust Members > Add
- Enter the peer management `IP`, admin user and password
- Verify the certificate fingerprint and the device name, then finish

```bash
tmsh modify cm trust-domain Root ca-devices add { 192.168.1.246 } \
    name bigip2.lab.local username admin password '<peer-password>'
tmsh show cm device-group device_trust_group
```

- Peer authority: a full member that can also sign other members
- Subordinate: a member that cannot add others to the domain

---

## Resetting Device Trust

- Needed after a hostname change, a certificate expiry or a broken build
- Device Management > Device Trust > Reset Device Trust
- Resetting removes the device from the trust domain and its device groups
- Re-add the peer afterwards and re-create the device group
- Always check the device name first: trust is bound to it

```bash
tmsh delete cm trust-domain Root
tmsh list cm device bigip1.lab.local
```

---

## Device Groups

- A device group is a set of trusted devices that share something
- Sync-failover: shares configuration and can fail over traffic groups
- Sync-only: shares configuration objects in a folder, no failover
- A device can be in one sync-failover group
- `device_trust_group` is created automatically; do not use it for sync
- Lab: one sync-failover group `dg_ha` with both devices

---

## Creating a Sync-Failover Device Group

```bash
tmsh create cm device-group dg_ha \
    devices add { bigip1.lab.local bigip2.lab.local } \
    type sync-failover auto-sync disabled network-failover enabled
tmsh run cm config-sync to-group dg_ha
tmsh show cm sync-status
```

- GUI: Device Management > Device Groups > Create
- Group type `Sync-Failover`, add both devices to Includes
- Network failover enabled: required for VE, no serial cable

---

## Device Group Options

| Option | Default | Meaning |
| --- | --- | --- |
| Automatic Sync | Disabled | Push every change immediately to the group |
| Full Sync | Disabled | Send the whole config instead of the changes |
| Maximum Incremental Sync Size | 1024 KB | Above this a full sync is sent |

---

## Failover and Save Options

| Option | Default | Meaning |
| --- | --- | --- |
| Network Failover | Enabled | Heartbeats over the network |
| Save on Auto Sync | Disabled | Write config to disk after each auto sync |

- Manual sync is the safer choice while learning: you choose when to push

---

## Traffic Groups

- A traffic group is a set of floating objects that fail over together
- Floating self `IP`s, virtual addresses, `SNAT` and `NAT` addresses
- `traffic-group-1` exists by default and is floating
- `traffic-group-local-only` holds objects that never move
- Each traffic group is active on exactly one device at a time
- Failover moves a traffic group, not a whole device

---

## Floating Self IP Addresses

- Servers use the `BIG-IP` as their default gateway
- That gateway must survive a failover, so it must float
- Create a floating self `IP` in `traffic-group-1` on each traffic `VLAN`
- The floating `MAC` follows the address (`MAC` masquerade optional)
- After failover the new active device sends gratuitous `ARP`s

```bash
tmsh create net self float_internal address 10.1.20.240/24 \
    vlan internal traffic-group traffic-group-1 allow-service default
tmsh create net self float_external address 10.1.10.240/24 \
    vlan external traffic-group traffic-group-1
```

---

## Floating Versus Non-Floating Self IPs

| Property | Non-floating self `IP` | Floating self `IP` |
| --- | --- | --- |
| Traffic group | `traffic-group-local-only` | `traffic-group-1` (or other) |
| Synced to peer | No | Yes |
| Owner | Always this device | Current active device |
| Used for | Monitors, `HA` addresses, management of the box | Server gateway, `SNAT` auto map |
| Lab value | `.245` / `.246` | `.240` |

---

## Virtual Addresses Belong to Traffic Groups Too

- Every virtual server destination creates a virtual address object
- The virtual address is assigned to a traffic group, `traffic-group-1` by default
- The active device for that group answers `ARP` for the address
- Moving a virtual address to another traffic group moves its virtual servers

```bash
tmsh list ltm virtual-address 10.1.10.100 traffic-group
tmsh modify ltm virtual-address 10.1.10.200 traffic-group traffic-group-2
```

---

## Active-Active With Two Traffic Groups

![active_active_traffic_groups](svg/courses/networking/f5-bigip-fundamentals/09_configuring_high_availability/active_active_traffic_groups.svg)

---

## Choosing Where a Traffic Group Runs

- Failover method per traffic group: load aware, `HA` order or `HA` score
- `HA` order: an ordered list of preferred devices
- Auto failback: return to the preferred device when it recovers
- Auto failback is off by default: two failover events instead of one
- Force a traffic group to the peer: Device Management > Traffic Groups > Force to Standby

```bash
tmsh modify cm traffic-group traffic-group-2 ha-order { bigip2.lab.local bigip1.lab.local }
tmsh run sys failover standby traffic-group traffic-group-2
```

---

## Synchronizing the Configuration

![config_sync_direction](svg/courses/networking/f5-bigip-fundamentals/09_configuring_high_availability/config_sync_direction.svg)

---

## Sync Status Messages

| Status | Meaning | Action |
| --- | --- | --- |
| In Sync | All members have the same config | None |
| Changes Pending | One member has newer changes | Sync that member to the group |
| Awaiting Initial Sync | New group, nothing synced yet | Sync from the device with the config |

---

## Sync Problem Messages

| Status | Meaning | Action |
| --- | --- | --- |
| Not All Devices Synced | Some members lag behind | Sync, then check connectivity |
| Sync Failure | A member rejected the change | Read `/var/log/ltm`, fix, sync again |
| Disconnected | Peer unreachable on `ConfigSync` address | Check `HA` `VLAN`, self `IP`, port lockdown |

---

## Running a Sync

```bash
tmsh show cm sync-status
tmsh run cm config-sync to-group dg_ha
tmsh run cm config-sync from-group dg_ha
```

```output
Sync Summary
Status         Changes Pending
Summary        There is a possible change conflict between bigip1 and bigip2.
Details        dg_ha: Changes Pending
               bigip1.lab.local: connected (for 734 seconds)
```

- Always sync from the device where the change was made
- Conflict: both sides changed; decide which one wins before syncing

---

## Config Sync Habits

- Make changes on one device only, usually the active one
- Sync immediately after each change, before testing failover
- Save on both devices: `tmsh save sys config` is not synced by itself
- Take a `UCS` on each device before large changes
- Never sync a partly built configuration to production peers
- Check the time: `NTP` drift between members breaks sync

---

## How Failover Is Decided

![failover_triggers](svg/courses/networking/f5-bigip-fundamentals/09_configuring_high_availability/failover_triggers.svg)

---

## Failover Triggers

| Trigger | What it watches | Typical setting |
| --- | --- | --- |
| Network failover | Peer heartbeats on `UDP` 1026 | Two unicast paths |
| `HA` group | Health score of trunks and pools | Threshold per traffic group |
| `VLAN` fail-safe | Any traffic seen on a `VLAN` | Critical `VLAN`s only |
| System fail-safe | `tmm`, `mcpd`, `bigd` daemons | On by default |
| Gateway fail-safe | Reachability of a gateway pool | Upstream router pool |
| Manual | Admin command | Maintenance windows |

---

## Network Failover

- Each device sends heartbeats to the peer unicast addresses
- No heartbeat within the timeout: the peer is presumed dead
- Default timeout is 3 seconds
- Use at least two paths: `HA` `VLAN` and management network
- If all paths fail but both devices live: both go active (split brain)
- Split brain shows up as `ARP` flapping and duplicate address warnings

---

## HA Groups

- An `HA` group scores the health of objects the device depends on
- Objects: pools, trunks, clusters (on chassis)
- Each object has a weight and a minimum member threshold
- The traffic group moves to the device with the higher score
- Example: fail over when fewer than 2 of 3 web servers are up on this side

```bash
tmsh create sys ha-group ha_web pools add { web_pool { weight 30 threshold 2 } }
tmsh modify cm traffic-group traffic-group-1 ha-group ha_web
```

---

## VLAN Fail-Safe

- Watches a `VLAN` for any received traffic
- After half the timeout with no traffic, the device sends probes (`ARP`)
- After the full timeout with no traffic, the action fires
- Actions: failover, restart all, reboot
- Use on `VLAN`s whose loss would make the device useless
- Too short a timeout on a quiet `VLAN` causes false failover events

```bash
tmsh modify net vlan internal failsafe enabled failsafe-timeout 90 \
    failsafe-action failover
```

---

## Connection and Persistence Mirroring

![connection_mirroring](svg/courses/networking/f5-bigip-fundamentals/09_configuring_high_availability/connection_mirroring.svg)

---

## Mirroring Explained

- Without mirroring, failover drops every open connection
- Short `HTTP` requests simply retry: most web apps do not need mirroring
- Long-lived sessions (`FTP`, database, `SSH`, `VPN`) do benefit
- Connection mirroring: enabled per virtual server
- Persistence mirroring: enabled per persistence profile
- Both cost `CPU` and bandwidth on the mirroring link

```bash
tmsh modify ltm virtual vs_ftp mirror enabled
tmsh modify ltm persistence source-addr src_persist mirror enabled
```

---

## What Survives a Failover

| Item | Without mirroring | With mirroring |
| --- | --- | --- |
| Configuration | Yes (synced) | Yes |
| New connections | Yes | Yes |
| Open `TCP` connections | No, reset or timeout | Yes |
| Persistence records | No, clients may move | Yes |
| `SSL` sessions | No, new handshake | No, new handshake |
| Statistics | No | No |

---

## Testing Failover

1. Confirm `In Sync` and note which device is active
1. Start a continuous client test from the client network
1. Force the active device to standby
1. Watch the client test and the status on both devices
1. Fail back and repeat with a pulled cable or a disabled interface

```bash
while true; do curl -s -o /dev/null -w '%{http_code} %{time_total}\n' \
    http://10.1.10.100/; sleep 0.5; done
tmsh run sys failover standby
tmsh show cm failover-status
```

---

## Reading Failover Status

```bash
tmsh show cm failover-status
tmsh show cm traffic-group
```

```output
Name              Device             Status   Next Active
traffic-group-1   bigip1.lab.local   standby  false
traffic-group-1   bigip2.lab.local   active   false
```

- The prompt shows the state too: `[admin@bigip2:Active:In Sync]`
- `/var/log/ltm` logs every state change with the reason

---

## Troubleshooting HA

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Both devices active | Heartbeats not reaching peer | Unicast addresses, port lockdown |
| Sync stays Disconnected | `ConfigSync` address unreachable | `ping` peer `HA` self `IP` |
| Trust fails | Hostname or time mismatch | Device name, `NTP` |

---

## Troubleshooting Traffic After Failover

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Servers lose gateway after failover | Gateway is a non-floating self `IP` | Server default route |
| Failover but clients still hit old box | Upstream `ARP` cache | Gratuitous `ARP`, `MAC` masquerade |

---

## Lab: Build the HA Pair

1. On `bigip2`, repeat the initial setup with `.246` addresses
1. Create the `ha` `VLAN` (`10.1.30.0/24`) and self `IP`s on both devices
1. Set `ConfigSync`, failover and mirroring addresses on both
1. Add `bigip2` to the trust domain from `bigip1`
1. Create `dg_ha`, sync `bigip1` to the group
1. Create floating self `IP`s `.240` on the external and internal `VLAN`s
1. Point the web servers to `10.1.20.240` as their gateway

---

## Lab: Prove It Works

1. Run the `curl` loop against `vs_web` and record the active device
1. Force the active device to standby and count failed requests
1. Change a pool on the active device, observe `Changes Pending`, sync
1. Enable connection mirroring on a virtual server, repeat with a long download
1. Disable the external interface on the active device and watch `VLAN` fail-safe
1. Take a `UCS` on each device when done

---

## Key Takeaways

- `HA` is built in layers: trust domain, device group, traffic groups
- Traffic groups move floating addresses; devices keep their local ones
- Servers must use a floating self `IP` as their gateway
- Sync from the device you changed, and check the status after each change
- Use more than one heartbeat path to avoid split brain
- Mirroring is for long-lived connections, not for every virtual server
- Test failover before production does it for you
