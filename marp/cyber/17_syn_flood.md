---
marp: true
---

# SYN Flood Attacks

---

## What is a SYN Flood Attack?

A SYN flood attack is a type of Denial of Service (DoS) attack that exploits the TCP three-way handshake process. The attacker sends a large number of TCP SYN (synchronize) requests to the target system, but never responds with the final ACK (acknowledgment) to complete the handshake.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: SYN
    Server->>Client: SYN-ACK
    Note right of Client: Attacker doesn't send ACK
