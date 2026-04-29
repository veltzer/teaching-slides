---
tags:
  - networking:tcp-ip
  - concepts:arp
  - concepts:icmp
level: intermediate
category: networking
audience:
  - audiences:developers

---
# ARP and ICMP

---
## What This Chapter Covers

- ARP — Address Resolution Protocol
- ICMP — Internet Control Message Protocol
- Ping and traceroute
- Common failures and how to detect them
- Security considerations

---
## What ARP Does

- Maps IP addresses to MAC addresses on a LAN
- Required because Layer 3 forwarding ends with Layer 2 delivery
- "Who has 192.168.1.10? Tell 192.168.1.1"
- Cached in the ARP table
- Without ARP, no LAN traffic flows

---
## ARP Request and Reply

- Request: broadcast (ff:ff:ff:ff:ff:ff)
- Reply: unicast back to requester
- Both sides learn each other's MAC
- Cached for several minutes typically
- Ages out and re-resolves

---
## ARP Visualized

![arp_flow](svg/courses/networking/tcp-ip-deep-dive/04_arp_icmp/arp_flow.svg)

---
## Viewing the ARP Table

- Linux: `ip neigh show` or `arp -a`
- Windows: `arp -a`
- Entries: IP, MAC, state, age
- States: REACHABLE, STALE, FAILED
- Stale entries trigger a fresh ARP

---
## Gratuitous ARP

- A host announces its own mapping
- Sent on boot or address change
- Updates neighbors' caches
- Detects IP conflicts
- Used by failover (VRRP, keepalived)

---
## ARP Spoofing

- Attacker sends fake ARP replies
- Poisons neighbors' caches
- Redirects traffic through attacker
- Foundation of MITM attacks on LANs
- Defense: ARP inspection, static entries, encryption

---
## IPv6: NDP Replaces ARP

- Neighbor Discovery Protocol
- Uses ICMPv6
- More secure (Secure Neighbor Discovery)
- Includes router discovery and address autoconfig
- Same purpose, modern protocol

---
## What ICMP Does

- Network diagnostics and error reporting
- Not for data transfer
- Critical for IP to function
- Examples: ping, traceroute, "destination unreachable"
- Often filtered (poorly) by firewalls

---
## ICMP Message Types

- Echo Request (8) / Echo Reply (0) — ping
- Destination Unreachable (3)
- Time Exceeded (11) — traceroute
- Redirect (5) — better gateway hint
- Many more

---
## Ping

- Sends Echo Request, expects Echo Reply
- Measures round-trip time
- Tests reachability
- Doesn't tell you why something is unreachable — just that it is
- First diagnostic tool when something breaks

---
## Reading Ping Output

```output
PING example.com (93.184.216.34): 56 data bytes
64 bytes from 93.184.216.34: icmp_seq=0 ttl=56 time=12.3 ms
64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=12.1 ms
```

- TTL hint at hop count from source
- time = RTT
- icmp_seq lets you spot drops

---
## Traceroute

- Shows the path packets take
- Sends packets with increasing TTL
- Each router decrements TTL; replies with Time Exceeded
- Reveals each hop's IP
- Different tools use UDP, TCP, or ICMP

---
## Traceroute Variants

- `traceroute` (Linux) — UDP by default
- `traceroute -I` — ICMP
- `traceroute -T` — TCP (better through firewalls)
- `tracert` (Windows) — ICMP
- `mtr` — continuous traceroute with stats

---
## ICMP Filtering

- Many firewalls block ICMP for "security"
- Often blocks legitimate traceroute and Path MTU
- Better: allow specific ICMP types
- Echo, Time Exceeded, Frag-Needed must be allowed
- Total ICMP block creates mysterious failures

---
## Path MTU Discovery

- Sender sets "don't fragment" bit
- Router that needs to fragment sends ICMP back
- Sender lowers MTU
- Repeats until path is found
- Blocked ICMP → black-hole connections

---
## Destination Unreachable Codes

- 0 — Net unreachable
- 1 — Host unreachable
- 3 — Port unreachable (UDP)
- 4 — Fragmentation needed (Path MTU)
- 9-13 — Admin filtered
- Each tells you something different

---
## Common Diagnostic Workflow

- Can I reach the destination? → ping
- Where does it fail? → traceroute
- Is the route asymmetric? → mtr
- Is a port open? → nc, telnet, nmap
- Layer up: HTTP/TLS once L3/L4 works

---
## Real-World Failure Examples

- Ping works but app doesn't → firewall blocks the port
- Ping fails but app works → ICMP is filtered
- Inconsistent latency → asymmetric routing
- Some sites slow → MTU/MSS issue
- DNS works, IP doesn't → routing or NAT problem

---
## ICMP Tools

- `ping` — basic reachability
- `mtr` — best diagnostic for asymmetric paths
- `tcptraceroute` — through TCP-only firewalls
- `nmap -PE` — ICMP-based discovery
- `iputils` package on Linux

---
## ARP Tools

- `arp` (legacy) / `ip neigh` (modern) — view cache
- `arping` — Layer 2 ping by ARP
- `arpwatch` — monitor for spoofing
- Wireshark with `arp` filter
- Helpful for LAN diagnostics

---
## Common Pitfalls

- Blocking all ICMP — breaks Path MTU and traceroute
- Static ARP entries that go stale
- ARP storms in misconfigured networks
- Treating ping success as "service works"
- Ignoring intermittent ARP issues

---
## Best Practices

- Allow Echo + Frag-Needed + Time Exceeded ICMP
- Monitor ARP table size and aging
- Watch for duplicate IPs (gratuitous ARP)
- Use mtr for path quality investigation
- Don't filter ICMP without understanding the cost

---
## Summary

- ARP: IP → MAC on a LAN; cache and timeout
- ICMP: control and diagnostics, not data
- Ping and traceroute build on ICMP
- Don't filter ICMP wholesale — break things
- Both are essential plumbing; learn the failure modes
