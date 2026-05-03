---
tags:
  - networking:tcp-ip
  - tools:wireshark
  - concepts:troubleshooting
level: intermediate
category: networking
audience:
  - audiences:devops
  - audiences:network-engineers

---
# Packet Analysis and Troubleshooting

---
## What This Chapter Covers

- Wireshark and tcpdump basics
- Capture filters vs display filters
- Reading TCP and HTTP traces
- Systematic troubleshooting
- Common failure signatures

---
## Why Packet Analysis?

- The wire never lies
- Logs and metrics summarize; packets are the truth
- Diagnoses what code-level tools can't
- Required when networks misbehave
- Skill that distinguishes senior engineers

---
## tcpdump

- Command-line packet capture
- Available on every Linux/Unix
- Lightweight, scriptable
- Reads/writes pcap files
- Use on servers without GUI

---
## tcpdump Basics

```bash
sudo tcpdump -i eth0 -nn -w trace.pcap
sudo tcpdump -i eth0 'tcp port 80'
sudo tcpdump -r trace.pcap 'host 1.2.3.4'
```

- `-nn` — don't resolve names (faster)
- `-w` — write pcap
- BPF filters as the last argument

---
## Wireshark

- GUI packet analyzer
- Reads pcap files (often from tcpdump)
- Decodes hundreds of protocols
- Powerful display filters
- The standard for deep dives

---
## Capture vs Display Filters

- Capture filter: limits what's captured (BPF syntax)
- Display filter: filters what's shown (Wireshark syntax)
- Capture: `tcp port 443`
- Display: `tcp.port == 443 and ip.src == 10.0.0.1`
- Different syntax — easy mistake

---
## Common Display Filters

- `tcp.port == 443` — HTTPS
- `http` — HTTP traffic
- `tls.handshake` — TLS handshakes
- `tcp.analysis.flags` — issues TCP detected
- `dns` — DNS queries and responses

---
## Reading a TCP Trace

![tcp_trace](svg/courses/networking/tcp-ip-deep-dive/08_packet_analysis/tcp_trace.svg)

---
## TCP Stream Reassembly

- Wireshark joins packets into the original stream
- "Follow TCP stream" in the menu
- See the actual conversation as text
- Critical for HTTP debugging
- Same idea: "Follow HTTP stream"

---
## Sequence Number Analysis

- Wireshark shows relative seq numbers by default
- Click on a packet, see exact byte ranges
- Detect retransmissions, out-of-order, duplicates
- TCP analysis flags the anomalies
- The "Statistics → TCP Stream Graph" is gold

---
## Analyzing Packet Loss

- Wireshark marks "TCP Retransmission"
- "Duplicate ACK" indicates upstream loss
- "Out-of-order" suggests path issues
- Pattern of losses tells the story
- Quantitative: loss percentage in stream

---
## Diagnosing Slow Sessions

- Look at TCP RTT in stream graph
- Spikes in delay → congestion
- Initial slow start vs steady state
- Window size limits
- Application thinking vs network waiting

---
## TLS Decryption

- Wireshark can decrypt TLS with the session keys
- Set `SSLKEYLOGFILE` in browser/curl
- Provide the file in Wireshark preferences
- See decrypted HTTP/2 inside TLS
- Critical for modern app debugging

---
## DNS Analysis

- Filter `dns`
- Match queries to responses by ID
- Latency: response time minus query time
- Failures: NXDOMAIN, SERVFAIL
- Timeouts: missing responses

---
## HTTP Analysis

- Filter `http` for cleartext
- Status codes, headers, payloads
- "Time since previous frame" reveals server delays
- HTTP/2 needs decryption
- HTTP/3 (QUIC) needs special handling

---
## Systematic Troubleshooting

- Reproduce the issue while capturing
- Identify the relevant flow
- Check Layer 3 (routing, IP)
- Check Layer 4 (TCP handshake, retransmissions)
- Check Layer 7 (application)
- Each layer up only when the lower one is OK

---
## A Workflow Loop

![troubleshooting_workflow](svg/courses/networking/tcp-ip-deep-dive/08_packet_analysis/troubleshooting_workflow.svg)

---
## Capture Strategy

- Both ends if possible
- Reproduce reliably
- Tag captures clearly
- Use ring buffers for long captures
- Trim large files (`editcap`)

---
## tshark

- Command-line Wireshark
- Apply display filters in batch
- Extract specific fields
- Pipe to other tools
- Useful in scripts

---
## Common Patterns

- SYN sent, no SYN-ACK → firewall, server down, route issue
- SYN-ACK sent, no ACK → return path issue
- RST after data → app crashed, port reused
- Many retransmissions → loss or congestion
- Slow handshakes → DNS or routing latency

---
## Asymmetric Path Detection

- Capture on both ends
- Different round-trip times in each direction
- Hint at separate forward/return paths
- Stateful middle-boxes confused
- Common in multi-homed sites

---
## MTU/MSS Issues

- Look for ICMP "fragmentation needed"
- Or PSH packets that hang
- Symptom: TLS handshake completes, big response stalls
- TCP MSS = MTU - 40 typically
- Lower MSS on tunnels

---
## Performance Debugging

- TCP Stream Graph: time/sequence
- Identifies bottlenecks: client, server, network
- Long flat lines = waiting (not network)
- Steep slope = data flowing
- Helpful for "the server is slow" claims

---
## Tools Beyond Wireshark

- `iperf3` — bandwidth/latency tests
- `nuttcp` — similar
- `mtr` — continuous traceroute
- `ss` (Linux) — socket statistics
- `netstat` (legacy)

---
## Cloud Capture Quirks

- VPC flow logs help, but limited fields
- Some clouds offer "VPC traffic mirroring"
- Pcap on individual VMs always works
- Capture latency-sensitive paths near the source
- Document what you can/can't capture

---
## Common Pitfalls

- Capturing too much, drowning in data
- Wrong interface (loopback vs LAN)
- Display filter typos (silent empty results)
- TLS hides the interesting bits → decrypt
- Big captures crash Wireshark — use tshark + grep

---
## Best Practices

- Capture both ends when feasible
- Save raw pcap, use display filters for analysis
- Annotate findings in the case
- Build muscle memory for common filters
- Practice on known-good traces

---
## Course Recap

- OSI/TCP-IP models — vocabulary
- Link layer — Ethernet, MAC, switches
- IP and subnetting — CIDR, NAT
- ARP and ICMP — local and diagnostic
- TCP — reliability, flow, congestion
- UDP, DNS, DHCP, QUIC
- Routing — link-state and BGP
- Packet analysis — Wireshark, tcpdump

---
## Summary

- The wire is the truth; capture it
- tcpdump for headless servers; Wireshark for analysis
- Capture filter (BPF) at capture; display filter at analysis
- Layer-by-layer troubleshooting catches everything
- Practice on known scenarios before crisis hits
