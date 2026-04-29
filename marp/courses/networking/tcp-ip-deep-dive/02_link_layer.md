---
tags:
  - networking:tcp-ip
  - concepts:ethernet
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Link Layer: Ethernet and MAC

---
## What This Chapter Covers

- Ethernet framing
- MAC addresses
- Switching and learning
- Broadcast and collision domains
- VLANs

---
## Ethernet History

- Invented at Xerox in 1973
- Standardized as IEEE 802.3
- Started at 10 Mbps; now 100+ Gbps
- Wired and wireless variants
- Most-used Layer 2 protocol on Earth

---
## Ethernet Frame Structure

```output
+----------+--------+--------+----------+----------------+--------+
| Preamble |  Dst   |  Src   | Type-field |    Payload     |  Frame-Check   |
| 7 bytes  | 6 bytes| 6 bytes| 2 bytes   | 46-1500 bytes  | 4 bytes|
+----------+--------+--------+----------+----------------+--------+
```

- Preamble for sync; not always counted
- Header is small relative to payload
- The frame-check field is a CRC-32 for integrity

---
## Frame Visualized

![frame](svg/courses/networking/tcp-ip-deep-dive/02_link_layer/frame.svg)

---
## Type Field

- 0x0800 — IPv4
- 0x86DD — IPv6
- 0x0806 — ARP
- 0x8100 — VLAN tag (802.1Q)
- Tells receiver how to interpret payload

---
## MAC Addresses

- 48 bits, 6 bytes
- Written as `aa:bb:cc:11:22:33`
- First 3 bytes: Organizationally Unique Identifier (OUI)
- Last 3 bytes: vendor-assigned
- Globally unique by convention

---
## MAC Address Types

- Unicast — single recipient
- Multicast — group
- Broadcast — all (`ff:ff:ff:ff:ff:ff`)
- Locally administered — software-set, not OUI-derived
- Bit 0 of first byte: I/G (individual/group)

---
## How Switches Work

- Receive frame on a port
- Look at source MAC, learn which port it's on
- Look at destination MAC
- If known, forward only to that port
- If unknown, flood to all ports (except input)

---
## MAC Learning Table

- Switch maintains a per-port table
- MAC address → egress port
- Aging timeout removes stale entries
- Eventually correct for any topology
- Visible via `show mac address-table` on enterprise gear

---
## Broadcast Domain

- The set of devices a broadcast reaches
- One per subnet (Layer 3 boundary)
- Switches don't separate; routers do
- Big broadcast domains hurt performance
- VLANs split a switch into many domains

---
## Collision Domain (Historical)

- Hubs broadcast everything to all ports
- Collisions when two devices transmit at once
- Switches eliminated this — one collision domain per port
- Modern Ethernet is full-duplex; no collisions
- Mostly historical interest now

---
## VLANs

- 802.1Q tag in the frame header
- 12 bits → 4096 VLAN IDs
- Logical segmentation on a physical switch
- Each VLAN is its own broadcast domain
- Scales L2 segregation

---
## VLAN Tagging

- Frames on trunk ports carry VLAN ID
- Frames on access ports are untagged (in their VLAN)
- Trunk between switches preserves VLANs
- Routers route between VLANs
- Used heavily in enterprise networks

---
## Spanning Tree Protocol

- Prevents loops in switched networks
- Loops cause broadcast storms
- Spanning Tree Protocol elects a root, blocks redundant paths
- Failover when active path dies
- Modern variants of Spanning Tree exist for faster convergence and per-VLAN trees

---
## Wi-Fi as Link Layer

- 802.11 standard
- Same MAC concepts
- Different framing details
- Encryption at the link layer (WPA2/WPA3)
- Bridges to Ethernet via access points

---
## MTU

- Maximum Transmission Unit
- Standard Ethernet: 1500 bytes
- Jumbo frames: 9000 bytes (data center)
- Mismatch causes fragmentation or drops
- Path MTU Discovery finds the smallest

---
## Mismatched MTU Problems

- Tunnels (VPN, GRE) reduce effective MTU
- "Black hole" if ICMP "fragmentation needed" is dropped
- Web pages load partially
- Symptom: small requests work, large ones hang
- Fix: lower MTU on tunnel interface

---
## Common Misconceptions

- "Switches are routers" — they're not; different layers
- "MAC addresses are random" — they have structure
- "VLANs are security boundaries" — only with router policy
- "Broadcasts are free" — they multiply with bad design
- "MTU never matters" — until it does, badly

---
## Tools for Link Layer

- `ip link show` — interfaces and state
- `arp -a` — neighbor cache
- `ethtool` — NIC settings
- Wireshark — full frame inspection
- Switch CLI — for managed switches

---
## Performance Considerations

- Hardware offloads: TSO, GRO, checksum
- Pause frames (802.3x) for flow control
- Link-aggregation control protocol bonds links
- Jumbo frames in storage networks
- Each is a knob; defaults are sensible

---
## Common Pitfalls

- VLAN misconfiguration cuts off subnets
- Spanning-tree loops bring down switches
- MAC flooding attacks (rare now)
- Asymmetric MTU on tunnels
- Layer 2 issues hidden behind Layer 3 symptoms

---
## Summary

- Ethernet frames: src + dst MAC + type + payload + check
- Switches learn and forward by MAC
- Broadcast domains scale poorly without VLANs
- Spanning Tree prevents loops in switched topologies
- Most issues you'll see are MTU, VLANs, and spanning tree
