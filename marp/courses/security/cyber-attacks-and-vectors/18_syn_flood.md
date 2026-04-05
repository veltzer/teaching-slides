# SYN Flood Attacks
---

## What is a SYN Flood Attack

- A SYN flood attack is a type of Denial of Service (DoS) attack that exploits the TCP three-way handshake process
- The attacker sends a large number of TCP SYN (synchronize) requests to the target system
- The attacker never responds with the final ACK (acknowledgment) to complete the handshake
- This fills the server's connection backlog queue, preventing legitimate connections
- One of the oldest and most common network-layer DoS attacks

---
## TCP Three-Way Handshake Review

```
┌──────────────────────────────────────────────────────────┐
│          Normal TCP Three-Way Handshake                   │
│                                                          │
│  Client                            Server                │
│    │                                  │                   │
│    │  1. SYN (seq=100)               │                   │
│    │─────────────────────────────────>│                   │
│    │                                  │  Allocates TCB    │
│    │  2. SYN-ACK (seq=300, ack=101)  │  (Transmission    │
│    │<─────────────────────────────────│   Control Block)  │
│    │                                  │                   │
│    │  3. ACK (seq=101, ack=301)      │                   │
│    │─────────────────────────────────>│                   │
│    │                                  │  Connection       │
│    │  === Connection Established ===  │  ESTABLISHED      │
│    │                                  │                   │
└──────────────────────────────────────────────────────────┘
```

**Key points:**
- Step 1: Client sends SYN with initial sequence number
- Step 2: Server allocates resources (TCB) and responds with SYN-ACK
- Step 3: Client completes handshake with ACK
- The server allocates resources at step 2, BEFORE the handshake completes

---
## SYN Flood Mechanism

```
┌──────────────────────────────────────────────────────────┐
│          SYN Flood Attack                                 │
│                                                          │
│  Attacker                          Server                │
│  (spoofed IPs)                                           │
│    │  SYN (src=1.1.1.1)             │                    │
│    │────────────────────────────────>│ Backlog slot #1    │
│    │  SYN (src=2.2.2.2)             │                    │
│    │────────────────────────────────>│ Backlog slot #2    │
│    │  SYN (src=3.3.3.3)             │                    │
│    │────────────────────────────────>│ Backlog slot #3    │
│    │  ...                            │                    │
│    │  SYN (src=N.N.N.N)             │                    │
│    │────────────────────────────────>│ Backlog FULL!      │
│    │                                 │                    │
│    │  Server sends SYN-ACKs to       │                    │
│    │  spoofed IPs (no ACK returns)   │                    │
│    │                                 │                    │
│  Legitimate Client                   │                    │
│    │  SYN                            │                    │
│    │────────────────────────────────>│ REFUSED / DROPPED  │
│    │                                 │                    │
└──────────────────────────────────────────────────────────┘
```

---
## Half-Open Connection Queue

```
┌──────────────────────────────────────────────────────────┐
│          Server Connection Backlog                        │
│                                                          │
│  ┌─────────────────────────────────────────────┐         │
│  │  SYN Backlog Queue (default: 128-1024)      │         │
│  ├─────┬─────┬─────┬─────┬─────┬─────┬────────┤         │
│  │ TCB │ TCB │ TCB │ TCB │ TCB │ TCB │  ...   │         │
│  │ #1  │ #2  │ #3  │ #4  │ #5  │ #6  │        │         │
│  │WAIT │WAIT │WAIT │WAIT │WAIT │WAIT │  FULL  │         │
│  └─────┴─────┴─────┴─────┴─────┴─────┴────────┘         │
│                                                          │
│  Each half-open connection:                              │
│  - Allocates a Transmission Control Block (TCB)          │
│  - Consumes ~280-300 bytes of kernel memory              │
│  - Stays in SYN_RECV state for 75 seconds (default)     │
│  - Server retransmits SYN-ACK up to 5 times             │
│                                                          │
│  When queue is full, new legitimate SYNs are DROPPED     │
└──────────────────────────────────────────────────────────┘
```

---
## SYN Flood with IP Spoofing

- Attackers typically spoof the source IP address in SYN packets
- This means the SYN-ACK responses go to random/nonexistent hosts
- No RST comes back to free the backlog slot quickly
- Makes it very difficult to filter by source IP

| Spoofing Method     | Description                                | Effectiveness |
|---------------------|--------------------------------------------|---------------|
| Random spoofing     | Random source IPs per packet               | High          |
| Subnet spoofing     | IPs from same subnet as target             | Medium        |
| Reflector spoofing  | IPs of real hosts that will send RST       | Lower         |
| No spoofing         | Real attacker IP (easy to block)           | Low           |

---
## SYN Cookies: The Primary Defense

```
┌──────────────────────────────────────────────────────────┐
│          SYN Cookies Mechanism                            │
│                                                          │
│  Normal:                                                 │
│  Client SYN ──> Server allocates TCB ──> SYN-ACK        │
│                 (state stored in memory)                  │
│                                                          │
│  With SYN Cookies:                                       │
│  Client SYN ──> Server encodes state IN the SYN-ACK     │
│                 sequence number (no memory allocated!)    │
│                                                          │
│  SYN-ACK seq number encodes:                             │
│  ┌─────────────────────────────────────────┐             │
│  │  5 bits: time counter (t mod 32)        │             │
│  │  3 bits: MSS (Maximum Segment Size)     │             │
│  │  24 bits: hash(src_ip, src_port,        │             │
│  │           dst_ip, dst_port, t, secret)  │             │
│  └─────────────────────────────────────────┘             │
│                                                          │
│  When ACK arrives, server recalculates and validates     │
│  Only then allocates TCB and establishes connection      │
└──────────────────────────────────────────────────────────┘
```

- No state stored until the handshake completes
- Legitimate clients complete handshake normally
- Flood packets consume no server memory
- Trade-off: some TCP options (window scaling) may be lost

---
## Enabling SYN Cookies on Linux

```bash
# Check current SYN cookie status
cat /proc/sys/net/ipv4/tcp_syncookies
# 0 = disabled, 1 = enabled (when backlog is full), 2 = always

# Enable SYN cookies
sudo sysctl -w net.ipv4.tcp_syncookies=1

# Make persistent across reboots
echo "net.ipv4.tcp_syncookies = 1" | \
    sudo tee -a /etc/sysctl.d/99-syn-flood.conf

# Apply changes
sudo sysctl -p /etc/sysctl.d/99-syn-flood.conf
```

---
## Kernel Tuning Parameters

```bash
# /etc/sysctl.d/99-syn-flood.conf

# Enable SYN cookies (activated when backlog is full)
net.ipv4.tcp_syncookies = 1

# Increase the SYN backlog queue size (default: 128-1024)
net.ipv4.tcp_max_syn_backlog = 65535

# Reduce SYN-ACK retransmissions (default: 5, ~3 minutes)
net.ipv4.tcp_synack_retries = 2

# Reduce time in SYN_RECV state
net.ipv4.tcp_syn_retries = 2

# Increase the socket listen backlog
net.core.somaxconn = 65535

# Enable TCP timestamps (required for SYN cookies)
net.ipv4.tcp_timestamps = 1

# Recycle TIME_WAIT sockets faster
net.ipv4.tcp_tw_reuse = 1

# Increase available local ports
net.ipv4.ip_local_port_range = 1024 65535

# Increase max connection tracking entries
net.netfilter.nf_conntrack_max = 1000000
```

```bash
# Apply all settings
sudo sysctl --system

# Verify settings
sysctl net.ipv4.tcp_syncookies
sysctl net.ipv4.tcp_max_syn_backlog
sysctl net.core.somaxconn
```

---
## Monitoring SYN Flood Attacks

```bash
# Check for SYN_RECV connections (half-open)
ss -tn state syn-recv | wc -l

# Watch SYN_RECV count in real time
watch -n 1 'ss -tn state syn-recv | wc -l'

# Show SYN_RECV connections by source IP
ss -tn state syn-recv | awk '{print $5}' | \
    cut -d: -f1 | sort | uniq -c | sort -rn | head

# Monitor SYN cookie activations in kernel log
dmesg | grep -i "syn"
# Look for: "TCP: request_sock_TCP: Possible SYN flooding"

# Check connection states summary
ss -s
# Look for: synrecv count significantly higher than normal

# Monitor with netstat (older systems)
netstat -n --tcp | grep SYN_RECV | wc -l

# Check kernel SYN cookie statistics
cat /proc/net/snmp | grep -A1 "Tcp:"
# Look for: TCPSyncookiesSent, TCPSyncookiesRecv, TCPSyncookiesFailed
```

---
## iptables Rate Limiting

```bash
# Limit SYN packets per source IP (20 per second, burst of 50)
iptables -A INPUT -p tcp --syn \
    -m limit --limit 20/s --limit-burst 50 -j ACCEPT
iptables -A INPUT -p tcp --syn -j DROP

# Per-IP connection rate limiting with hashlimit
iptables -A INPUT -p tcp --dport 80 --syn \
    -m hashlimit --hashlimit-name syn_rate \
    --hashlimit-above 15/sec \
    --hashlimit-burst 20 \
    --hashlimit-mode srcip \
    -j DROP

# Limit concurrent half-open connections per IP
iptables -A INPUT -p tcp --syn \
    -m connlimit --connlimit-above 30 \
    --connlimit-mask 32 -j DROP

# Block invalid packets
iptables -A INPUT -m state --state INVALID -j DROP

# Log suspected SYN floods before dropping
iptables -A INPUT -p tcp --syn \
    -m limit --limit 1/s --limit-burst 3 \
    -j LOG --log-prefix "SYN_FLOOD: " --log-level 7
```

---
## nftables Equivalent

```bash
# Modern nftables rules for SYN flood protection
nft add table inet filter

nft add chain inet filter input { type filter hook input priority 0 \; }

# Drop invalid packets
nft add rule inet filter input ct state invalid drop

# Rate limit SYN packets per source IP
nft add rule inet filter input tcp flags syn \
    meter syn_flood { ip saddr limit rate 20/second burst 50 packets } \
    accept

nft add rule inet filter input tcp flags syn drop

# Connection limit per IP
nft add rule inet filter input tcp dport 80 tcp flags syn \
    meter conn_limit { ip saddr ct count over 30 } drop
```

---
## Testing with hping3

```bash
# IMPORTANT: Only test against systems you own or have
# explicit written authorization to test

# Basic SYN flood test (uses real source IP)
sudo hping3 -S --flood -p 80 target-server

# SYN flood with random spoofed source IPs
sudo hping3 -S --flood --rand-source -p 80 target-server

# SYN flood with specific rate (10,000 packets/sec)
sudo hping3 -S -p 80 --faster target-server

# SYN flood targeting specific port with spoofed source
sudo hping3 -S -p 443 -a 10.0.0.1 --flood target-server

# Flags explained:
#   -S          : Set SYN flag
#   --flood     : Send packets as fast as possible
#   --rand-source: Random spoofed source IPs
#   -p 80       : Target port 80
#   -a 10.0.0.1 : Spoof source IP as 10.0.0.1
#   --faster    : Send 10,000 packets per second
```

```bash
# Alternative: using scapy for more control
python3 -c "
from scapy.all import *
# Send 1000 SYN packets with random source IPs
for i in range(1000):
    ip = IP(src=RandIP(), dst='target-server')
    tcp = TCP(sport=RandShort(), dport=80, flags='S')
    send(ip/tcp, verbose=0)
"
```

> WARNING: SYN flood testing can disrupt network services. Only test in controlled lab environments or with explicit authorization.

---
## SYN Flood vs Other TCP Attacks

| Attack         | Mechanism                            | Layer   | Defense               |
|----------------|--------------------------------------|---------|-----------------------|
| SYN Flood      | Half-open connections fill backlog   | L4      | SYN cookies           |
| ACK Flood      | Massive ACK packets consume CPU      | L4      | Stateful firewall     |
| FIN Flood      | FIN packets for nonexistent sessions | L4      | Stateful firewall     |
| RST Attack     | Forged RST to kill connections       | L4      | TCP MD5 / TCP-AO      |
| Sockstress     | Tiny TCP window keeps conns open     | L4      | Timeout tuning        |
| Slowloris      | Slow HTTP headers exhaust threads    | L7      | Reverse proxy         |

---
## Hardware and Cloud Defenses

```
┌──────────────────────────────────────────────────────────┐
│          Defense in Depth Against SYN Floods              │
│                                                          │
│  ┌─────────────────┐                                     │
│  │  ISP / Transit   │  Upstream filtering (BGP Flowspec) │
│  └────────┬────────┘                                     │
│           v                                               │
│  ┌─────────────────┐                                     │
│  │  Cloud Scrubbing │  Cloudflare, AWS Shield, Akamai    │
│  │  Center          │  Absorbs volumetric attacks        │
│  └────────┬────────┘                                     │
│           v                                               │
│  ┌─────────────────┐                                     │
│  │  Hardware FW /   │  Stateful inspection, SYN proxy    │
│  │  IPS             │  Rate limiting at line speed       │
│  └────────┬────────┘                                     │
│           v                                               │
│  ┌─────────────────┐                                     │
│  │  OS Kernel       │  SYN cookies, backlog tuning       │
│  │  (Linux sysctl)  │  iptables/nftables rate limiting   │
│  └────────┬────────┘                                     │
│           v                                               │
│  ┌─────────────────┐                                     │
│  │  Application     │  Connection limits, timeouts       │
│  └─────────────────┘                                     │
└──────────────────────────────────────────────────────────┘
```

---
## SYN Proxy (Hardware Firewalls)

```
┌──────────────────────────────────────────────────────────┐
│          SYN Proxy Operation                              │
│                                                          │
│  Client          Firewall/Proxy          Server          │
│    │                  │                    │              │
│    │  SYN              │                    │              │
│    │─────────────────>│                    │              │
│    │                  │  (Firewall handles │              │
│    │  SYN-ACK         │   handshake first) │              │
│    │<─────────────────│                    │              │
│    │                  │                    │              │
│    │  ACK              │                    │              │
│    │─────────────────>│                    │              │
│    │                  │  Client is legit!  │              │
│    │                  │  SYN               │              │
│    │                  │───────────────────>│              │
│    │                  │  SYN-ACK           │              │
│    │                  │<───────────────────│              │
│    │                  │  ACK               │              │
│    │                  │───────────────────>│              │
│    │                  │                    │              │
│    │  === Proxied Connection Established === │             │
└──────────────────────────────────────────────────────────┘
```

- Firewall completes the three-way handshake on behalf of the server
- Only forwards the connection to the server if the client completes the handshake
- Flood traffic never reaches the backend server

---
## Complete Defense Configuration Example

```bash
#!/bin/bash
# SYN flood defense setup script for Linux servers

# 1. Kernel tuning
cat << 'SYSCTL' | sudo tee /etc/sysctl.d/99-syn-flood.conf
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
net.core.somaxconn = 65535
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65535
SYSCTL
sudo sysctl --system

# 2. iptables rules
# Drop invalid packets
sudo iptables -A INPUT -m state --state INVALID -j DROP

# SYN rate limiting per IP
sudo iptables -A INPUT -p tcp --syn \
    -m hashlimit --hashlimit-name syn_rate \
    --hashlimit-above 20/sec --hashlimit-burst 50 \
    --hashlimit-mode srcip -j DROP

# Connection limit per IP
sudo iptables -A INPUT -p tcp --syn \
    -m connlimit --connlimit-above 50 \
    --connlimit-mask 32 -j DROP

# 3. Save iptables rules
sudo iptables-save | sudo tee /etc/iptables/rules.v4

echo "[+] SYN flood defenses configured"
```

---
## Key Takeaways

- SYN floods exploit the TCP handshake by filling the server's half-open connection queue
- IP spoofing makes SYN floods difficult to filter by source address
- SYN cookies are the most important kernel-level defense (encode state in the SYN-ACK)
- Kernel tuning (backlog size, retry counts, timeouts) provides additional resilience
- iptables/nftables rate limiting adds a firewall-level defense layer
- Hardware SYN proxies and cloud scrubbing centers handle large-scale attacks
- Defense in depth: combine kernel tuning + firewall rules + upstream filtering
- Regular testing with hping3 in controlled environments validates your defenses
