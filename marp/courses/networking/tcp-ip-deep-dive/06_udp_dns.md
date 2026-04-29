---
tags:
  - networking:tcp-ip
  - concepts:udp
  - concepts:dns
level: intermediate
category: networking
audience:
  - audiences:developers

---
# UDP, DNS, and DHCP

---
## What This Chapter Covers

- UDP basics
- When to choose UDP over TCP
- DNS resolution (review with focus on transport)
- DHCP lease negotiation
- QUIC: modern UDP-based transport

---
## UDP Design

- Connectionless: no handshake
- Best-effort: may lose, may reorder
- Stateless: nothing kept between datagrams
- Low overhead: 8-byte header
- Application handles reliability if it needs to

---
## UDP Header

```output
+----------+----------+
| Src Port | Dst Port |
+----------+----------+
|  Length  | Checksum |
+----------+----------+
|       Data          |
+---------------------+
```

- Just 8 bytes
- Length includes header + data
- Checksum optional in IPv4, mandatory in IPv6

---
## When to Use UDP

- DNS — small queries, fast response
- VoIP — late audio is worse than missing audio
- Video streaming — same logic
- Online games — real-time state
- Telemetry — lossy is OK

---
## TCP vs UDP

![tcp_vs_udp](svg/courses/networking/tcp-ip-deep-dive/06_udp_dns/tcp_vs_udp.svg)

---
## UDP and Reliability

- Application can add reliability if needed
- Sequence numbers, retransmits, ACKs
- More work; sometimes worth it
- QUIC is the modern way to do this

---
## DNS over UDP

- Default for most DNS queries
- Single packet request/response
- 512-byte limit traditionally
- Larger responses fall back to TCP
- EDNS extension allows larger UDP

---
## DNS over TCP

- Used when response > UDP size
- Zone transfers (AXFR)
- DNSSEC responses (often large)
- Modern: DoT/DoH always use TCP
- TCP fallback adds latency on miss

---
## DHCP

- Dynamic Host Configuration Protocol
- UDP-based
- Hands out IP address, gateway, DNS, etc
- Lease-based: renew before expiry
- DORA: Discover, Offer, Request, Acknowledge

---
## DHCP DORA Process

- Discover: broadcast "I need an IP"
- Offer: server proposes an address
- Request: client accepts the offer
- Acknowledge: server confirms
- Client now configured

---
## DHCP Visualized

![dhcp](svg/courses/networking/tcp-ip-deep-dive/06_udp_dns/dhcp.svg)

---
## DHCP Reservations

- Server gives same IP to specific MAC
- Effectively static, but managed centrally
- Convenient for printers, IoT, servers
- Avoids hardcoded configuration on devices
- Rotate reservations carefully

---
## DHCP Failure Modes

- DHCP server unreachable → 169.254.x.x (link-local)
- Lease expired without renew → temporary loss
- Conflicting reservations → bouncing IPs
- Rogue DHCP servers → wrong gateway/DNS
- Switch security: DHCP snooping

---
## NTP

- Network Time Protocol
- UDP port 123
- Tiny packets, high frequency
- Critical for log correlation, security, certs
- Stratum hierarchy: 0 (atomic) to 16 (unreachable)

---
## Why Time Matters

- TLS certificate validation
- Kerberos tickets
- Log correlation across systems
- Database transactions
- Security audit trails

---
## QUIC

- UDP-based transport from Google
- Standardized as RFC 9000
- Used by HTTP/3
- Encrypts everything (including transport metadata)
- Fixes head-of-line blocking from TCP+TLS

---
## QUIC Improvements

- 0-RTT or 1-RTT connection setup
- Multiplexing without head-of-line blocking
- Connection migration (IP changes)
- Always encrypted (no plaintext alternative)
- Better for mobile networks

---
## HTTP/3 over QUIC

- HTTP/2 over TCP had head-of-line blocking
- HTTP/3 over QUIC doesn't
- Each stream independent
- Better mobile performance
- Adoption growing fast

---
## Stream Control Transmission Protocol

- Stream Control Transmission Protocol
- Multi-streaming, multi-homing
- Reliable like TCP, message-oriented like UDP
- Used in telecom signaling
- Less common in general internet

---
## ICMP and UDP

- ICMP "port unreachable" replies tell sender app isn't there
- Used for traceroute (UDP variant)
- Discovery tools rely on it
- Filtering ICMP breaks UDP error reporting

---
## UDP Common Pitfalls

- No back-pressure → flooding
- No reordering protection
- MTU concerns (fragmentation)
- Firewalls drop unsolicited UDP often
- Stateful firewalls handle UDP loosely

---
## NAT and UDP

- NAT must guess the connection state
- Holds state per (src, dst, ports) tuple
- Times out faster than TCP entries
- VoIP and real-time web traffic need NAT traversal: STUN, TURN
- UDP hole punching for P2P

---
## Tools

- `tcpdump -p udp` — capture UDP
- `nc -u` — netcat over UDP
- `dig` — DNS over UDP/TCP
- `dhcping` — test DHCP servers
- `ntpq` — NTP statistics

---
## Performance Considerations

- UDP doesn't congestion-control by default
- Application must respect network capacity
- Real-time web protocols use bandwidth estimation
- Excessive UDP traffic hurts coexisting TCP
- Be a good citizen on shared networks

---
## Common Pitfalls

- Assuming UDP is always faster than TCP (sometimes slower under loss)
- Treating UDP as connectionless → forgetting NAT timeouts
- Building reliable apps without proper retransmit logic
- Filtering UDP without testing
- Ignoring MTU issues in UDP-heavy protocols

---
## Summary

- UDP: simple, fast, unreliable
- DNS, DHCP, NTP, gaming, streaming use UDP
- DNS over TCP for large responses; QUIC for HTTP/3
- DHCP's DORA gets devices configured
- Build reliability in app layer if needed; QUIC does it for you
