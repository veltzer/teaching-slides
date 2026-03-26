# TCP/IP Fundamentals
## Understanding the Internet's Core Protocols
---

## What is TCP/IP?
- Transmission Control Protocol/Internet Protocol
- Foundation of the internet and modern networking
- Suite of protocols that enable reliable data transmission
- Developed in the 1970s by DARPA

---

## The TCP/IP Protocol Stack
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_00_tcp_ip)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_00_tcp_ip)"/>
  <defs>
    <marker id="arrowd0_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Protocol Stack Details
- Application Layer: HTTP, FTP, SMTP, DNS
- Transport Layer: TCP, UDP
- Internet Layer: IP, ICMP, ARP
- Network Access Layer: Ethernet, Wi-Fi

---

## IP Addressing
- Unique identifier for devices on a network
- IPv4: 32-bit address (e.g., 192.168.1.1)
- IPv6: 128-bit address (e.g., 2001:0db8:85a3:0000:0000:8a2e:0370:7334)
- Divided into network and host portions

---

## IP Address Classes (IPv4)
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_00_tcp_ip)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_00_tcp_ip)"/>
  <defs>
    <marker id="arrowd1_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Subnetting
- Dividing networks into smaller networks
- Uses subnet masks to define network boundaries
- Enhances network management and security
- Example: 255.255.255.0 (/24 notation)

---

## IP Packet Structure

```text
+------------------------+
|       IP Header        |
+------------------------+
|    Source IP Address   |
+------------------------+
| Destination IP Address |
+------------------------+
|         Data          |
+------------------------+
```

---

## TCP vs UDP
### Key Differences

| TCP | UDP |
|-----|-----|
| Connection-oriented | Connectionless |
| Reliable | Best effort |
| Ordered delivery | No order guarantee |
| Flow control | No flow control |

---

## TCP Three-Way Handshake
<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_00_tcp_ip)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd2_00_tcp_ip)"/>
  <defs>
    <marker id="arrowd2_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## TCP Flow Control
- Prevents overwhelming receivers
- Uses sliding window mechanism
- Window size adjusts dynamically
- Enables efficient data transfer

---

## TCP Congestion Control
- Slow Start
- Congestion Avoidance
- Fast Retransmit
- Fast Recovery

---

## UDP Characteristics
- Lightweight protocol
- No connection establishment
- No guarantee of delivery
- Ideal for real-time applications

---

## Common Applications

| Protocol | Port | Use Case |
|----------|------|----------|
| HTTP | 80 | Web browsing |
| HTTPS | 443 | Secure web |
| FTP | 21 | File transfer |
| DNS | 53 | Name resolution |

---

## Domain Name System (DNS)
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <defs>
    <marker id="arrowd3_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## ARP (Address Resolution Protocol)
- Maps IP addresses to MAC addresses
- Essential for local network communication
- Maintains ARP cache for efficiency
- Broadcast-based protocol

---

## ICMP (Internet Control Message Protocol)
- Network diagnostic tool
- Error reporting
- Echo request/reply (ping)
- Path MTU discovery

---

## Network Security Basics
- Firewalls
- Access Control Lists
- Encryption (IPSec)
- Network Address Translation (NAT)

---

## NAT Operation
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_tcp_ip)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_tcp_ip)"/>
  <defs>
    <marker id="arrowd4_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## IPv6 Features
- Larger address space
- Built-in security (IPSec)
- Simplified header format
- Better QoS support
- No need for NAT

---

## IPv6 Address Types
- Unicast
- Multicast
- Anycast
- Link-local
- Site-local

---

## Quality of Service (QoS)
- Traffic prioritization
- Bandwidth allocation
- Delay management
- Loss prevention
- Service guarantees

---

## Common Network Issues
- Packet loss
- Latency
- Jitter
- Congestion
- DNS resolution problems

---

## Troubleshooting Tools
- ping
- traceroute/tracert
- nslookup/dig
- netstat
- Wireshark

---

## Best Practices
- Regular monitoring
- Security updates
- Documentation
- Redundancy
- Backup systems

---

## Future of TCP/IP
- IPv6 adoption
- QUIC protocol
- Network automation
- SDN integration
- Enhanced security

---

## Review & Key Takeaways
- TCP/IP is fundamental to networking
- Understanding layers helps troubleshooting
- Security is critical
- Protocol selection matters
- Continuous evolution
