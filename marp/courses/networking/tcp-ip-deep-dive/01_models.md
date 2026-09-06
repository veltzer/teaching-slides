---
tags:
  - networking:tcp-ip
  - concepts:layers
level: intermediate
category: networking
audience:
  - audiences:developers

---

# OSI and TCP/IP Models

---

## What This Chapter Covers

- The OSI seven-layer model
- The TCP/IP four-layer model
- How they relate
- Encapsulation
- Why we use both names

---

## Why Reference Models?

- Networking is layered by design
- Each layer has a defined responsibility
- Layers can change independently
- Models give us a shared vocabulary
- Real protocols don't always fit cleanly

---

## OSI Seven Layers

- 7 — Application
- 6 — Presentation
- 5 — Session
- 4 — Transport
- 3 — Network
- 2 — Data Link
- 1 — Physical
- "All People Seem To Need Data Processing"

---

## TCP/IP Four Layers

- Application
- Transport
- Internet
- Link
- Practical model for the Internet
- Maps roughly to OSI

---

## What Each Layer Does

![layer_responsibilities](svg/courses/networking/tcp-ip-deep-dive/01_models/layer_responsibilities.svg)

---

## Models Visualized

![models](svg/courses/networking/tcp-ip-deep-dive/01_models/models.svg)

---

## OSI Layer 1: Physical

- Bits on the wire
- Voltage levels, photons, radio
- Cables, connectors, hardware
- Out of scope for software developers
- Where errors start: bad cables, electrical interference

---

## OSI Layer 2: Data Link

- Frames between adjacent nodes
- Ethernet, Wi-Fi, point-to-point links
- MAC addresses
- Local area network domain
- Switches operate here

---

## OSI Layer 3: Network

- Packets across networks
- IP addresses (v4 and v6)
- Routing decisions
- Routers operate here
- Where the internet really lives

---

## OSI Layer 4: Transport

- Segments / datagrams
- TCP — reliable, ordered, connection-oriented
- UDP — best-effort, unordered, connectionless
- Ports identify processes
- End-to-end delivery

---

## OSI Layers 5-7

- Session — manages dialog (rarely a separate layer in practice)
- Presentation — encoding, encryption (TLS straddles 5/6)
- Application — HTTP, SMTP, DNS, etc
- TCP/IP collapses these into "Application"
- Most developers live here

---

## TCP/IP Layer Comparison

- TCP/IP Application = OSI 5+6+7
- TCP/IP Transport = OSI 4
- TCP/IP Internet = OSI 3
- TCP/IP Link = OSI 1+2
- The TCP/IP model fits actual protocols better

---

## Encapsulation

- Each layer wraps the layer above
- Application data → TCP segment → IP packet → Ethernet frame
- Each adds its own header
- Receiver strips headers in reverse order
- Layered isolation in practice

---

## Encapsulation Visualized

![encapsulation](svg/courses/networking/tcp-ip-deep-dive/01_models/encapsulation.svg)

---

## Why TLS Doesn't Fit Cleanly

- TLS is between Transport and Application
- Provides session and presentation features
- Real-world protocols don't always map to model layers
- The model is a guide; not a straitjacket
- Context matters more than strict layering

---

## What Crosses Each Layer

- Same network: Link layer (Ethernet)
- Same building: Internet layer (IP routes)
- Internet: Internet + Transport (firewalls, NAT)
- Application: HTTP, gRPC, etc end-to-end
- Each hop adds and strips headers

---

## Routers vs Switches

- Switch: Layer 2, forwards by MAC
- Router: Layer 3, forwards by IP
- Some devices do both (Layer 3 switches)
- Hubs (Layer 1) are obsolete
- Choose based on broadcast domain needs

---

## Real-World Devices

- Switch — single subnet, MAC learning
- Router — between subnets, IP forwarding
- Firewall — Layer 3-7, policy enforcement
- Load balancer — Layer 4 or Layer 7
- IDS/IPS — inspects payload at Layer 7

---

## Same vs Different Subnets

- Same subnet: ARP for MAC, frame directly to neighbor
- Different subnet: send to default gateway
- Gateway re-encapsulates and forwards
- Subnet is a Layer 3 boundary
- Critical for routing correctness

---

## TCP/IP Stack in OS

- NIC drivers handle Link layer
- Kernel handles Internet, Transport
- User space runs Applications
- Sockets API spans Transport + Application
- Different OS implementations; same protocols

---

## Network Protocol Mapping

- HTTP — Application
- TLS — between Transport and Application
- TCP / UDP — Transport
- IPv4 / IPv6 — Internet
- ARP — between Link and Internet (debated)
- Ethernet — Link

---

## Why Layer Discipline Matters

- Loose coupling between layers
- Replace IPv4 with IPv6 without changing apps
- Replace Ethernet with Wi-Fi without changing TCP
- Debugging starts at the lowest broken layer
- Misuse across layers creates fragile systems

---

## Course Roadmap

- Chapter 2: Link layer (Ethernet, MAC)
- Chapter 3: IP and subnetting
- Chapter 4: ARP and ICMP
- Chapter 5: TCP deep dive
- Chapter 6: UDP and DNS
- Chapter 7: Routing
- Chapter 8: Packet analysis with Wireshark

---

## Common Misconceptions

- "OSI is the truth" — it's a model; reality differs
- "TCP/IP and OSI are the same" — different layers, different counts
- "TLS is application layer" — it's between layers
- "Just learn HTTP" — the bottom matters when things break
- "Models are useless in practice" — they shape vocabulary and tooling

---

## Summary

- OSI: 7 layers; TCP/IP: 4
- Each layer has its responsibility
- Encapsulation wraps headers; receiver strips them
- Layer discipline enables independent evolution
- Models guide, but real protocols sometimes blur layers
