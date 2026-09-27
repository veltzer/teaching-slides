---
tags:
  - infrastructure:linux
  - security:forensics
  - security:security
level: advanced
category: security
audience:
  - audiences:security-professionals

---

# Network Forensics and Intrusion Tracing

## Course: Linux Forensics - Day 4 (continued)
- Network evidence connects a host compromise to the wider attack
- Packet captures reveal exfiltration, command channels, and lateral movement
- This module covers `pcap` analysis, session reconstruction, and traffic IOCs
- Sources: captured `pcap` files, host firewall logs, and carved memory packets

---

## Where Network Evidence Comes From

- Pre-captured `pcap` files from a tap, span port, or IDS
- Live capture on the host during authorized live response
- Packets carved from a RAM image (recovered socket buffers)
- Host-side corroboration: `auth.log`, firewall logs, `/proc/net`

```bash
# Authorized live capture, written straight to evidence
tcpdump -i any -w /evidence/live_capture.pcap -s 0

# Hash the capture immediately so integrity is provable
sha256sum /evidence/live_capture.pcap > /evidence/live_capture.pcap.sha256
```

- Treat a `pcap` like any other exhibit: hash it, log it, work on a copy

---

## Triaging a Capture with `tshark`

```bash
# Protocol breakdown: what is even in this capture?
tshark -r /evidence/capture.pcap -q -z io,phs

# Conversations ranked by bytes (spot the big talkers)
tshark -r /evidence/capture.pcap -q -z conv,tcp

# Every DNS query name
tshark -r /evidence/capture.pcap -Y "dns.flags.response==0" \
  -T fields -e dns.qry.name

# HTTP requests with host and URI
tshark -r /evidence/capture.pcap -Y "http.request" \
  -T fields -e http.host -e http.request.uri
```

- Start wide with the protocol hierarchy, then drill into suspects
- `tshark` is the command-line Wireshark: scriptable and headless

---

## Reconstructing a Session

```bash
# List TCP streams, then follow one end to end
tshark -r /evidence/capture.pcap -q -z conv,tcp
tshark -r /evidence/capture.pcap -q -z follow,tcp,ascii,7

# Reconstruct an SSH conversation's metadata
tshark -r /evidence/capture.pcap -Y "ssh" \
  -T fields -e frame.time -e ip.src -e ip.dst -e ssh.message_code
```

- SSH payload is encrypted, but timing, volume, and direction still tell a story
- A long outbound SSH flow after a login is a classic exfiltration signature
- Follow the stream to read any cleartext protocol in full

---

## Extracting Files from Traffic

```bash
# Export every object HTTP carried in the capture
tshark -r /evidence/capture.pcap --export-objects http,/evidence/http_out/

# Carve transferred files by signature as a cross-check
foremost -t all -i /evidence/capture.pcap -o /evidence/pcap_carved/

# Reassemble raw TCP flows to disk
tcpflow -r /evidence/capture.pcap -o /evidence/flows/
```

- Recovered files become their own exhibits: hash and analyze each
- Compare carved output against exported objects to catch missed transfers
- In Wireshark this is File then Export Objects

---

## Command-and-Control and Lateral Movement

- C2 beacons show as regular, small, outbound connections to one endpoint
- Look for fixed intervals, identical packet sizes, and odd ports
- Lateral movement appears as internal-to-internal SSH, SMB, or WinRM

```bash
# Rank destinations by connection count to expose beaconing
tshark -r /evidence/capture.pcap -T fields -e ip.dst \
  | sort | uniq -c | sort -rn | head

# Inter-arrival times to one suspected C2 host
tshark -r /evidence/capture.pcap -Y "ip.dst==203.0.113.5" \
  -T fields -e frame.time_delta
```

- Steady deltas across many connections point to automated beaconing

---

## DNS Tunneling and Covert Channels

- DNS tunneling smuggles data inside query names to a controlled domain
- Signs: very long subdomains, high query volume, rare record types
- MiTM and ARP spoofing show as duplicate IPs or gratuitous ARP

```bash
# Suspiciously long DNS query names
tshark -r /evidence/capture.pcap -Y "dns.flags.response==0" \
  -T fields -e dns.qry.name | awk '{ if (length($0) > 50) print }'

# TXT / NULL records that legitimate browsing rarely triggers
tshark -r /evidence/capture.pcap -Y "dns.qry.type==16 || dns.qry.type==10"

# Detect duplicate-address / ARP-spoof warnings
tshark -r /evidence/capture.pcap -Y "arp.duplicate-address-detected"
```

---

## Building Network IOCs for the Report

```bash
# Distinct external endpoints the host contacted
tshark -r /evidence/capture.pcap -T fields -e ip.dst \
  | sort -u > /evidence/ioc_ips.txt

# All resolved domains, deduplicated
tshark -r /evidence/capture.pcap -Y "dns" \
  -T fields -e dns.qry.name | sort -u > /evidence/ioc_domains.txt
```

- Turn findings into a clean list of IPs, domains, ports, and timestamps
- Correlate each IOC back to a host process from earlier analysis
- IOCs let responders sweep the rest of the estate for the same intrusion

---

## Exercise: Network Forensics

Analyze the provided capture from a compromised host.

Deliverables:
1. 1. The protocol hierarchy and top three conversations by volume
1. 1. A reconstructed SSH session showing the suspected exfiltration flow
1. 1. Any files recovered from the traffic, with hashes
1. 1. An IOC list of external IPs and domains, tied to a host process
