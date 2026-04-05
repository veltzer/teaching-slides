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
  <rect x="200" y="5" width="200" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="12" font-weight="bold">Application Layer</text>
  <text x="510" y="30" text-anchor="middle" font-size="10" fill="#555">HTTP, FTP, DNS</text>
  <rect x="200" y="50" width="200" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="75" text-anchor="middle" font-size="12" font-weight="bold">Transport Layer</text>
  <text x="510" y="75" text-anchor="middle" font-size="10" fill="#555">TCP, UDP</text>
  <rect x="200" y="95" width="200" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="120" text-anchor="middle" font-size="12" font-weight="bold">Internet Layer</text>
  <text x="510" y="120" text-anchor="middle" font-size="10" fill="#555">IP, ICMP, ARP</text>
  <rect x="200" y="140" width="200" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="165" text-anchor="middle" font-size="12" font-weight="bold">Network Access</text>
  <text x="510" y="165" text-anchor="middle" font-size="10" fill="#555">Ethernet, Wi-Fi</text>
  <text x="100" y="100" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">TCP/IP</text>
  <text x="100" y="116" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Model</text>
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
  <rect x="10" y="20" width="110" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="65" y="38" text-anchor="middle" font-size="11" font-weight="bold">Class A</text>
  <text x="65" y="55" text-anchor="middle" font-size="10">1.0.0.0 -</text>
  <text x="65" y="65" text-anchor="middle" font-size="10">126.255.255.255</text>
  <rect x="130" y="20" width="110" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="185" y="38" text-anchor="middle" font-size="11" font-weight="bold">Class B</text>
  <text x="185" y="55" text-anchor="middle" font-size="10">128.0.0.0 -</text>
  <text x="185" y="65" text-anchor="middle" font-size="10">191.255.255.255</text>
  <rect x="250" y="20" width="110" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="305" y="38" text-anchor="middle" font-size="11" font-weight="bold">Class C</text>
  <text x="305" y="55" text-anchor="middle" font-size="10">192.0.0.0 -</text>
  <text x="305" y="65" text-anchor="middle" font-size="10">223.255.255.255</text>
  <rect x="370" y="20" width="110" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="425" y="38" text-anchor="middle" font-size="11" font-weight="bold">Class D</text>
  <text x="425" y="55" text-anchor="middle" font-size="10">224.0.0.0 -</text>
  <text x="425" y="65" text-anchor="middle" font-size="10">239.255.255.255</text>
  <rect x="490" y="20" width="100" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="38" text-anchor="middle" font-size="11" font-weight="bold">Class E</text>
  <text x="540" y="55" text-anchor="middle" font-size="10">240.0.0.0 -</text>
  <text x="540" y="65" text-anchor="middle" font-size="10">255.255.255.255</text>
  <text x="65" y="100" text-anchor="middle" font-size="10" fill="#555">/8 prefix</text>
  <text x="185" y="100" text-anchor="middle" font-size="10" fill="#555">/16 prefix</text>
  <text x="305" y="100" text-anchor="middle" font-size="10" fill="#555">/24 prefix</text>
  <text x="425" y="100" text-anchor="middle" font-size="10" fill="#555">Multicast</text>
  <text x="540" y="100" text-anchor="middle" font-size="10" fill="#555">Reserved</text>
  <rect x="10" y="120" width="580" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3" opacity="0.3"/>
  <text x="20" y="140" font-size="10" fill="#333">Network bits:</text>
  <rect x="100" y="125" width="50" height="20" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="125" y="139" text-anchor="middle" font-size="10">8</text>
  <rect x="220" y="125" width="50" height="20" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="245" y="139" text-anchor="middle" font-size="10">16</text>
  <rect x="340" y="125" width="50" height="20" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="365" y="139" text-anchor="middle" font-size="10">24</text>
  <text x="20" y="175" font-size="10" fill="#333">Host bits:</text>
  <rect x="100" y="160" width="50" height="20" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="125" y="174" text-anchor="middle" font-size="10">24</text>
  <rect x="220" y="160" width="50" height="20" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="245" y="174" text-anchor="middle" font-size="10">16</text>
  <rect x="340" y="160" width="50" height="20" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="365" y="174" text-anchor="middle" font-size="10">8</text>
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
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="80" y="5" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="25" text-anchor="middle" font-size="12" font-weight="bold">Client</text>
  <rect x="420" y="5" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="25" text-anchor="middle" font-size="12" font-weight="bold">Server</text>
  <line x1="130" y1="40" x2="130" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="40" x2="470" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="130" y1="65" x2="470" y2="85" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_00_tcp_ip)"/>
  <text x="300" y="60" text-anchor="middle" font-size="11" fill="#1565c0" font-weight="bold">SYN (seq=x)</text>
  <line x1="470" y1="105" x2="130" y2="125" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowd2_00_tcp_ip)"/>
  <text x="300" y="103" text-anchor="middle" font-size="11" fill="#7b1fa2" font-weight="bold">SYN-ACK (seq=y, ack=x+1)</text>
  <line x1="130" y1="145" x2="470" y2="165" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd2_00_tcp_ip)"/>
  <text x="300" y="148" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">ACK (ack=y+1)</text>
  <text x="300" y="192" text-anchor="middle" font-size="10" fill="#555">Connection Established</text>
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
  <defs>
    <marker id="arrowd3_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="75" width="90" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="95" text-anchor="middle" font-size="11" font-weight="bold">Browser</text>
  <text x="55" y="110" text-anchor="middle" font-size="10">example.com?</text>
  <rect x="140" y="75" width="90" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="185" y="95" text-anchor="middle" font-size="11" font-weight="bold">Local DNS</text>
  <text x="185" y="110" text-anchor="middle" font-size="10">Resolver</text>
  <rect x="270" y="75" width="90" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="315" y="95" text-anchor="middle" font-size="11" font-weight="bold">Root DNS</text>
  <text x="315" y="110" text-anchor="middle" font-size="10">(.) servers</text>
  <rect x="400" y="75" width="90" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="95" text-anchor="middle" font-size="11" font-weight="bold">TLD DNS</text>
  <text x="445" y="110" text-anchor="middle" font-size="10">(.com)</text>
  <rect x="510" y="75" width="80" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="550" y="95" text-anchor="middle" font-size="10" font-weight="bold">Authoritative</text>
  <text x="550" y="110" text-anchor="middle" font-size="10">DNS</text>
  <line x1="100" y1="95" x2="140" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="230" y1="90" x2="270" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="360" y1="90" x2="400" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="490" y1="90" x2="510" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="510" y1="110" x2="490" y2="110" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="400" y1="110" x2="360" y2="110" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="270" y1="110" x2="230" y2="110" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <line x1="140" y1="105" x2="100" y2="105" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd3_00_tcp_ip)"/>
  <text x="300" y="55" text-anchor="middle" font-size="11" fill="#333">Query: "What is the IP of example.com?"</text>
  <text x="300" y="160" text-anchor="middle" font-size="11" fill="#2e7d32">Response: 93.184.216.34</text>
  <text x="55" y="175" text-anchor="middle" font-size="10" fill="#555">Step 1</text>
  <text x="185" y="175" text-anchor="middle" font-size="10" fill="#555">Step 2</text>
  <text x="315" y="175" text-anchor="middle" font-size="10" fill="#555">Step 3</text>
  <text x="445" y="175" text-anchor="middle" font-size="10" fill="#555">Step 4</text>
  <text x="550" y="175" text-anchor="middle" font-size="10" fill="#555">Step 5</text>
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
  <defs>
    <marker id="arrowd4_00_tcp_ip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="85" y="15" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Private Network</text>
  <rect x="20" y="25" width="120" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="42" text-anchor="middle" font-size="10">PC1: 192.168.1.10</text>
  <text x="80" y="55" text-anchor="middle" font-size="10">:3000</text>
  <rect x="20" y="70" width="120" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="87" text-anchor="middle" font-size="10">PC2: 192.168.1.11</text>
  <text x="80" y="100" text-anchor="middle" font-size="10">:4000</text>
  <rect x="20" y="115" width="120" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="132" text-anchor="middle" font-size="10">PC3: 192.168.1.12</text>
  <text x="80" y="145" text-anchor="middle" font-size="10">:5000</text>
  <rect x="220" y="55" width="140" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="290" y="80" text-anchor="middle" font-size="12" font-weight="bold">NAT Router</text>
  <text x="290" y="95" text-anchor="middle" font-size="10">Translation Table</text>
  <text x="290" y="110" text-anchor="middle" font-size="10" fill="#555">Public: 203.0.113.5</text>
  <rect x="440" y="55" width="140" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="80" text-anchor="middle" font-size="12" font-weight="bold">Internet</text>
  <text x="510" y="95" text-anchor="middle" font-size="11">Web Server</text>
  <text x="510" y="110" text-anchor="middle" font-size="10" fill="#555">93.184.216.34</text>
  <line x1="140" y1="45" x2="220" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_tcp_ip)"/>
  <line x1="140" y1="87" x2="220" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_tcp_ip)"/>
  <line x1="140" y1="132" x2="220" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_tcp_ip)"/>
  <line x1="360" y1="90" x2="440" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_tcp_ip)"/>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#555">All outbound traffic appears as 203.0.113.5 to external servers</text>
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
