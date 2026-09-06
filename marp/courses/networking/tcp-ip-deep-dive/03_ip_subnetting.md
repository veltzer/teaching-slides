---
tags:
  - networking:tcp-ip
  - concepts:ip
  - concepts:subnetting
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:network-engineers

---

# IP Addressing and Subnetting

---

## What This Chapter Covers

- IPv4 and IPv6 addressing
- CIDR notation
- Subnetting basics
- Public, private, and reserved ranges
- NAT

---

## IPv4 Addressing

- 32-bit addresses
- Written as four octets: `192.168.1.10`
- Each octet 0-255
- ~4.3 billion total addresses
- Exhausted years ago — NAT and IPv6 fill the gap

---

## IPv6 Addressing

- 128-bit addresses
- Written in hex, 8 groups of 4: `2001:0db8::1`
- 3.4 × 10^38 addresses
- No NAT needed (in theory)
- Adoption growing; not everywhere

---

## CIDR Notation

- `192.168.1.0/24` — 24 bits for network, 8 for hosts
- The `/24` is the prefix length
- Replaces older "class A/B/C" notation
- More flexible: any boundary, not just /8/16/24
- Pronounced "slash twenty-four"

---

## Network and Host Bits

- /24 → 24 network bits, 8 host bits
- Network bits identify the subnet
- Host bits identify the device
- Network address: all host bits 0
- Broadcast address: all host bits 1

---

## Subnet Math Visualized

![cidr](svg/courses/networking/tcp-ip-deep-dive/03_ip_subnetting/cidr.svg)

---

## Common Subnet Sizes

- /32 — single host
- /30 — 4 addresses, 2 usable (point-to-point links)
- /24 — 256 addresses, 254 usable
- /16 — 65k addresses
- /8 — 16M addresses

---

## Subnet Masks

- /24 = 255.255.255.0
- /16 = 255.255.0.0
- /23 = 255.255.254.0
- Convert: count leading 1 bits
- Modern tools accept either CIDR or mask

---

## Private Address Ranges

- 10.0.0.0/8 — class A (16M addresses)
- 172.16.0.0/12 — class B (1M addresses)
- 192.168.0.0/16 — class C (65k addresses)
- Not routable on the internet
- For internal networks behind NAT

---

## Address Range Map

![private_ranges](svg/courses/networking/tcp-ip-deep-dive/03_ip_subnetting/private_ranges.svg)

---

## Special Reserved Ranges

- 127.0.0.0/8 — loopback (`localhost`)
- 169.254.0.0/16 — link-local (auto-config)
- 224.0.0.0/4 — multicast
- 0.0.0.0 — "any address" / default
- Don't use these as host addresses

---

## IPv6 Address Types

- Global unicast (2000::/3) — internet-routable
- Link-local (fe80::/10) — same subnet only
- Unique-local prefix — like RFC 1918
- Multicast (ff00::/8)
- No broadcast in IPv6 — use multicast

---

## IPv6 Notation Rules

- Leading zeros omitted: `2001:db8:0:0:0:0:0:1` → `2001:db8::1`
- Two colons replace consecutive zero groups (once per address)
- IPv4-mapped: `::ffff:192.0.2.1`
- All-zeros: `::` (default route)
- Loopback: `::1`

---

## Subnetting Example

- ISP gives you `203.0.113.0/24` (256 addresses)
- Need 4 subnets for departments
- Use /26: 64 addresses each, 4 subnets
- Subnets: .0/26, .64/26, .128/26, .192/26
- Each: 62 usable host addresses

---

## NAT: Network Address Translation

- Translates private IP to public
- One public IP, many private hosts
- Maintains a translation table by port
- Most home routers do this
- Critical for IPv4 conservation

---

## NAT Types

- Source NAT (SNAT) — outbound, change source
- Destination NAT (DNAT) — inbound, change destination
- 1:1 NAT — fixed mapping
- PAT (Port Address Translation) — many-to-one
- Each is appropriate to specific scenarios

---

## NAT Visualized

![nat](svg/courses/networking/tcp-ip-deep-dive/03_ip_subnetting/nat.svg)

---

## NAT Limitations

- Breaks end-to-end addressing
- Inbound connections need port forwarding
- VoIP and games need NAT traversal
- IPv6 was supposed to eliminate the need
- Carrier-grade NAT adds another layer

---

## Default Gateway

- Router that sends packets outside the subnet
- Each host has one (or more)
- "Default route" — `0.0.0.0/0`
- Configured per interface
- DHCP usually provides it

---

## DHCP Basics

- Dynamic Host Configuration Protocol
- Hands out IP, subnet mask, gateway, DNS
- Lease-based
- Discover, Offer, Request, Acknowledge (DORA)
- Used in most networks (excluding servers)

---

## Static vs Dynamic Allocation

- Servers: usually static
- Clients: usually DHCP
- Reservation: DHCP gives the same IP each time
- Document allocations to avoid conflicts
- Track in IP-address-management tools at scale

---

## Routing Table

- Tells the OS where to send packets
- Per destination prefix
- Most-specific match wins
- Default route catches the rest
- View with `ip route` (Linux), `route print` (Windows)

---

## Common Pitfalls

- Subnet masks copy-pasted wrong
- Default gateway not in the subnet
- Overlapping ranges across sites
- IPv4 and IPv6 routing inconsistent
- Forgetting that 0.0.0.0/0 is a real route

---

## Calculating Subnets

- Total addresses: 2^(32 - prefix)
- Usable hosts: total - 2 (network + broadcast)
- /30 = 4 - 2 = 2 usable
- /24 = 256 - 2 = 254 usable
- /31 has special semantics (RFC 3021)

---

## Aggregation and Summarization

- Combine specific routes into a summary
- 192.168.0.0/24 + 192.168.1.0/24 = 192.168.0.0/23
- Reduces routing table size
- Important on the internet
- Less critical on small networks

---

## Summary

- IPv4 is 32 bits; IPv6 is 128
- CIDR: `address/prefix` for any boundary
- Private ranges (RFC 1918) for internal networks
- NAT translates private to public; breaks end-to-end
- Subnetting math: addresses = 2^(32 - prefix)
