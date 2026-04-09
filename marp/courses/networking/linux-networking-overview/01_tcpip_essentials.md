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

![tcp_ip_protocol_stack](svg/courses/networking/linux-networking-overview/01_tcpip_essentials/tcp_ip_protocol_stack.svg)

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

![ip_packet_structure](svg/courses/networking/linux-networking-overview/01_tcpip_essentials/ip_packet_structure.svg)

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

![tcp_three_way_handshake](svg/courses/networking/linux-networking-overview/01_tcpip_essentials/tcp_three_way_handshake.svg)

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

![network_address_translation_nat](svg/courses/networking/linux-networking-overview/01_tcpip_essentials/network_address_translation_nat.svg)

---

## Network Address Translation (NAT)

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

![dns_resolution_process](svg/courses/networking/linux-networking-overview/01_tcpip_essentials/dns_resolution_process.svg)

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

![client_server_architecture](svg/courses/networking/linux-networking-overview/01_tcpip_essentials/client_server_architecture.svg)

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
