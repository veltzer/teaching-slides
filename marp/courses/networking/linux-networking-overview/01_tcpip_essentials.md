# TCP/IP Essentials
## Chapter 1: Introduction to Computer Networks

---

## Course Overview
- Fundamentals of TCP/IP Protocol Suite
- Core Network Protocols: TCP, UDP, IP
- Essential Network Components
- Protocol Architecture and Implementation

---

## What is TCP/IP

- **Protocol Suite**: Collection of communication protocols
- **Internet Standard**: Forms the foundation of internet communications
- **Layered Architecture**: Organized in conceptual layers
- **Open Standard**: Freely available and implementable

---

## TCP/IP Protocol Stack

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="580" height="180" fill="#f9f9f9" stroke="#ccc" stroke-width="1" rx="5"/>
  <text x="110" y="25" text-anchor="middle" font-size="11" font-weight="bold">TCP/IP Model</text>
  <text x="400" y="25" text-anchor="middle" font-size="11" font-weight="bold">OSI Model</text>
  <rect x="30" y="35" width="160" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="57" text-anchor="middle" font-size="11">Application</text>
  <rect x="30" y="75" width="160" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="97" text-anchor="middle" font-size="11">Transport</text>
  <rect x="30" y="115" width="160" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="137" text-anchor="middle" font-size="11">Internet</text>
  <rect x="30" y="155" width="160" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="177" text-anchor="middle" font-size="11">Network Access</text>
  <rect x="280" y="35" width="160" height="22" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="50" text-anchor="middle" font-size="10">Application</text>
  <rect x="280" y="57" width="160" height="22" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="72" text-anchor="middle" font-size="10">Presentation</text>
  <rect x="280" y="79" width="160" height="22" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="94" text-anchor="middle" font-size="10">Session</text>
  <rect x="280" y="101" width="160" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="116" text-anchor="middle" font-size="10">Transport</text>
  <rect x="280" y="123" width="160" height="22" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="138" text-anchor="middle" font-size="10">Network</text>
  <rect x="280" y="145" width="160" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="160" text-anchor="middle" font-size="10">Data Link</text>
  <rect x="280" y="167" width="160" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="182" text-anchor="middle" font-size="10">Physical</text>
  <line x1="190" y1="52" x2="280" y2="52" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="190" y1="92" x2="280" y2="112" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="190" y1="132" x2="280" y2="134" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="190" y1="172" x2="280" y2="167" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="535" y="57" font-size="10" fill="#666">Layer 7</text>
  <text x="535" y="116" font-size="10" fill="#666">Layer 4</text>
  <text x="535" y="138" font-size="10" fill="#666">Layer 3</text>
  <text x="535" y="182" font-size="10" fill="#666">Layer 1</text>
</svg>

---

## Internet Protocol (IP)

**Core Functions:**
- Network addressing
- Packet routing
- Fragmentation and reassembly

**Key Features:**
- Connectionless protocol
- Best-effort delivery
- No guarantee of:
    - Delivery
    - Ordering
    - Integrity

---

## IP Addressing

**IPv4:**
- 32-bit addresses
- Format: xxx.xxx.xxx.xxx
- Example: 192.168.1.1

**IPv6:**
- 128-bit addresses
- Format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx
- Example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334

---

## IP Packet Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">IP Packet Encapsulation</text>
  <rect x="30" y="30" width="540" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="50" y="52" font-size="11">Ethernet Header</text>
  <rect x="130" y="30" width="440" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="52" font-size="11">IP Header</text>
  <rect x="250" y="30" width="320" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="270" y="52" font-size="11">TCP/UDP Header</text>
  <rect x="400" y="30" width="170" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="420" y="52" font-size="11">Payload Data</text>
  <rect x="30" y="80" width="540" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="100" text-anchor="middle" font-size="11">Layer 2: Ethernet Frame (14 bytes header)</text>
  <rect x="130" y="115" width="440" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="350" y="135" text-anchor="middle" font-size="11">Layer 3: IP Packet (20 bytes header)</text>
  <rect x="250" y="150" width="320" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="410" y="170" text-anchor="middle" font-size="11">Layer 4: TCP(20B) / UDP(8B) Segment</text>
</svg>

---

## Transmission Control Protocol (TCP)

**Key Features:**
- Connection-oriented
- Reliable data delivery
- Flow control
- Error detection
- Ordered delivery

**Use Cases:**
- Web browsing (HTTP)
- Email (SMTP)
- File transfer (FTP)

---

## TCP Three-Way Handshake

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_00_tcpip_essentials" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="80" y="10" width="90" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="125" y="30" text-anchor="middle" font-size="12" font-weight="bold">Client</text>
  <rect x="430" y="10" width="90" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="3"/>
  <text x="475" y="30" text-anchor="middle" font-size="12" font-weight="bold">Server</text>
  <line x1="125" y1="40" x2="125" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="475" y1="40" x2="475" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="125" y1="70" x2="475" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_00_tcpip_essentials)"/>
  <text x="300" y="65" text-anchor="middle" font-size="11" fill="#1565c0">SYN (seq=x)</text>
  <line x1="475" y1="110" x2="125" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_00_tcpip_essentials)"/>
  <text x="300" y="108" text-anchor="middle" font-size="11" fill="#7b1fa2">SYN-ACK (seq=y, ack=x+1)</text>
  <line x1="125" y1="150" x2="475" y2="170" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_00_tcpip_essentials)"/>
  <text x="300" y="148" text-anchor="middle" font-size="11" fill="#2e7d32">ACK (ack=y+1)</text>
  <text x="300" y="195" text-anchor="middle" font-size="10" fill="#666">Connection Established</text>
</svg>

---

## TCP Segment Structure

| Field | Size | Purpose |
|-------|------|---------|
| Source Port | 16 bits | Sender's port |
| Destination Port | 16 bits | Receiver's port |
| Sequence Number | 32 bits | Data ordering |
| ACK Number | 32 bits | Next expected byte |
| Window | 16 bits | Flow control |

---

## User Datagram Protocol (UDP)

**Characteristics:**
- Connectionless
- Unreliable delivery
- No flow control
- No error recovery
- Minimal overhead

**Common Uses:**
- DNS queries
- Streaming media
- Online gaming
- VoIP

---

## TCP vs UDP Comparison

<div class="columns">
<div>

### TCP
- Connection-oriented
- Reliable
- Ordered delivery
- Flow control
- Error recovery
- Higher overhead

</div>
<div>

### UDP
- Connectionless
- Unreliable
- No ordering
- No flow control
- No error recovery
- Lower overhead

</div>
</div>

---

## Network Components Overview

1. **Router**
1. **Switch**
1. **Modem**
1. **Gateway**
1. **Server**
1. **Client**

---

## Router

**Purpose:**
- Connects different networks
- Makes forwarding decisions
- Operates at Layer 3 (IP)

**Functions:**
- Packet forwarding
- Path selection
- Route optimization

---

## Switch

**Purpose:**
- Connects devices within same network
- Operates at Layer 2 (Ethernet)

**Functions:**
- MAC address learning
- Frame forwarding
- Loop prevention
- VLAN support

---

## Modem

**Types:**
- Cable modem
- DSL modem
- Fiber modem

**Functions:**
- Signal modulation/demodulation
- Digital-to-analog conversion
- Physical media interface

---

## Gateway

**Purpose:**
- Protocol translation
- Network interconnection
- Security enforcement

**Types:**
- Protocol gateways
- Security gateways
- Application gateways

---

## Network Address Translation (NAT)

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_00_tcpip_essentials" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Network Address Translation</text>
  <rect x="20" y="50" width="120" height="100" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="80" y="75" text-anchor="middle" font-size="11" font-weight="bold">Private LAN</text>
  <text x="80" y="95" text-anchor="middle" font-size="10">192.168.1.10</text>
  <text x="80" y="110" text-anchor="middle" font-size="10">192.168.1.11</text>
  <text x="80" y="125" text-anchor="middle" font-size="10">192.168.1.12</text>
  <rect x="220" y="60" width="140" height="80" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="290" y="85" text-anchor="middle" font-size="12" font-weight="bold">NAT Router</text>
  <text x="290" y="105" text-anchor="middle" font-size="10">192.168.1.1 (int)</text>
  <text x="290" y="120" text-anchor="middle" font-size="10">203.0.113.5 (ext)</text>
  <rect x="440" y="65" width="130" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="90" text-anchor="middle" font-size="12" font-weight="bold">Internet</text>
  <text x="505" y="110" text-anchor="middle" font-size="10">Public Servers</text>
  <line x1="140" y1="100" x2="220" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcpip_essentials)"/>
  <line x1="360" y1="100" x2="440" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_00_tcpip_essentials)"/>
  <text x="180" y="92" text-anchor="middle" font-size="9" fill="#666">Private IP</text>
  <text x="400" y="92" text-anchor="middle" font-size="9" fill="#666">Public IP</text>
  <text x="290" y="160" text-anchor="middle" font-size="10" fill="#666">src: 192.168.1.10 --&gt; src: 203.0.113.5</text>
  <text x="290" y="175" text-anchor="middle" font-size="10" fill="#666">Translation table maps internal:port to external:port</text>
</svg>

**Benefits:**
- IP address conservation
- Network security
- Network isolation

---

## Types of NAT

1. **Static NAT**
    - One-to-one mapping
    - Fixed translations
1. **Dynamic NAT**
    - Many-to-many mapping
    - Pool of public IPs
1. **PAT (Port Address Translation)**
    - Many-to-one mapping
    - Most common type

---
## Domain Name System (DNS)

**Purpose:**
- Name resolution
- Service discovery
- Load balancing

**Components:**
- DNS servers
- DNS resolvers
- DNS records
- DNS zones
---
## DNS Resolution Process

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_00_tcpip_essentials" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">DNS Resolution Process</text>
  <rect x="10" y="30" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="50" y="55" text-anchor="middle" font-size="10">Client</text>
  <rect x="130" y="30" width="80" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="170" y="48" text-anchor="middle" font-size="10">Local</text>
  <text x="170" y="60" text-anchor="middle" font-size="10">Resolver</text>
  <rect x="250" y="30" width="80" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="290" y="48" text-anchor="middle" font-size="10">Root</text>
  <text x="290" y="60" text-anchor="middle" font-size="10">DNS</text>
  <rect x="370" y="30" width="80" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="410" y="48" text-anchor="middle" font-size="10">TLD</text>
  <text x="410" y="60" text-anchor="middle" font-size="10">DNS</text>
  <rect x="490" y="30" width="90" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="535" y="48" text-anchor="middle" font-size="10">Authoritative</text>
  <text x="535" y="60" text-anchor="middle" font-size="10">DNS</text>
  <line x1="90" y1="50" x2="130" y2="50" stroke="#333" stroke-width="1" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <text x="110" y="44" text-anchor="middle" font-size="9" fill="#666">1</text>
  <line x1="210" y1="45" x2="250" y2="45" stroke="#1565c0" stroke-width="1" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <text x="230" y="40" text-anchor="middle" font-size="9" fill="#1565c0">2</text>
  <line x1="250" y1="55" x2="210" y2="55" stroke="#1565c0" stroke-width="1" stroke-dasharray="3,3" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <line x1="210" y1="90" x2="370" y2="90" stroke="#7b1fa2" stroke-width="1" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <text x="290" y="85" text-anchor="middle" font-size="9" fill="#7b1fa2">3. Query TLD server</text>
  <line x1="370" y1="100" x2="210" y2="100" stroke="#7b1fa2" stroke-width="1" stroke-dasharray="3,3" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <line x1="210" y1="120" x2="490" y2="120" stroke="#2e7d32" stroke-width="1" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <text x="350" y="115" text-anchor="middle" font-size="9" fill="#2e7d32">4. Query authoritative server</text>
  <line x1="490" y1="130" x2="210" y2="130" stroke="#2e7d32" stroke-width="1" stroke-dasharray="3,3" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <text x="350" y="145" text-anchor="middle" font-size="9" fill="#2e7d32">5. Return IP address</text>
  <line x1="130" y1="160" x2="90" y2="160" stroke="#333" stroke-width="1" stroke-dasharray="3,3" marker-end="url(#arrowd4_00_tcpip_essentials)"/>
  <text x="110" y="155" text-anchor="middle" font-size="9" fill="#333">6</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#666">Iterative DNS resolution with caching at resolver</text>
</svg>

---
## DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | example.com → 93.184.216.34 |
| AAAA | IPv6 address | example.com → 2606:2800:220:1:248:1893:25c8:1946 |
| CNAME | Alias | www → example.com |
| MX | Mail server | example.com → mail.example.com |
| NS | Name server | example.com → ns1.example.com |
---
## Client-Server Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_00_tcpip_essentials" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Client-Server Architecture</text>
  <rect x="30" y="40" width="130" height="130" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="95" y="60" text-anchor="middle" font-size="11" font-weight="bold">Clients</text>
  <text x="95" y="80" text-anchor="middle" font-size="10">Web Browser</text>
  <text x="95" y="95" text-anchor="middle" font-size="10">Email Client</text>
  <text x="95" y="110" text-anchor="middle" font-size="10">FTP Client</text>
  <text x="95" y="125" text-anchor="middle" font-size="10">SSH Client</text>
  <rect x="240" y="55" width="120" height="100" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="12" font-weight="bold">Network</text>
  <text x="300" y="100" text-anchor="middle" font-size="10">TCP/IP</text>
  <text x="300" y="115" text-anchor="middle" font-size="10">Protocols</text>
  <text x="300" y="130" text-anchor="middle" font-size="10">Ports</text>
  <rect x="440" y="40" width="130" height="130" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="505" y="60" text-anchor="middle" font-size="11" font-weight="bold">Servers</text>
  <text x="505" y="80" text-anchor="middle" font-size="10">Apache/Nginx</text>
  <text x="505" y="95" text-anchor="middle" font-size="10">Postfix/SMTP</text>
  <text x="505" y="110" text-anchor="middle" font-size="10">vsftpd/FTP</text>
  <text x="505" y="125" text-anchor="middle" font-size="10">OpenSSH</text>
  <line x1="160" y1="95" x2="240" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_00_tcpip_essentials)"/>
  <line x1="240" y1="115" x2="160" y2="115" stroke="#333" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd5_00_tcpip_essentials)"/>
  <line x1="360" y1="95" x2="440" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_00_tcpip_essentials)"/>
  <line x1="440" y1="115" x2="360" y2="115" stroke="#333" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd5_00_tcpip_essentials)"/>
  <text x="200" y="88" text-anchor="middle" font-size="9" fill="#666">Request</text>
  <text x="200" y="130" text-anchor="middle" font-size="9" fill="#666">Response</text>
</svg>

---
## Server Types

**Common Servers:**
- Web servers (Apache, Nginx)
- Mail servers (Postfix, Exchange)
- File servers (FTP, SMB)
- Database servers (MySQL, PostgreSQL)
- Application servers (Tomcat, Node.js)

---
## Client Applications

**Types:**
- Web browsers
- Email clients
- FTP clients
- Terminal emulators
- Custom applications

**Protocols:**
- HTTP/HTTPS
- SMTP/IMAP/POP3
- FTP/SFTP
- SSH

---
## Network Security Fundamentals

**Key Areas:**
1. Authentication
1. Authorization
1. Encryption
1. Access Control
1. Monitoring
1. Incident Response

---

## Common Network Protocols

| Protocol | Port | Purpose |
|----------|------|---------|
| HTTP | 80 | Web traffic |
| HTTPS | 443 | Secure web traffic |
| FTP | 21 | File transfer |
| SSH | 22 | Secure shell |
| SMTP | 25 | Email sending |
| DNS | 53 | Name resolution |

---

## Summary

- TCP/IP is the foundation of modern networking
- Understanding protocols is crucial
- Network components work together
- Security is essential
- DNS and NAT are key services
