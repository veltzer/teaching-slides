# Linux Network Command Line Tools
## Chapter 4: System Administration and Monitoring

---

## Tool Categories

1. Information Tools
1. Low-level Tools
1. Configuration Tools
1. Performance Tools
1. Tapping Tools
1. Quality Control Tools
1. Debugging Tools

---

## Information Tools Overview

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="150" rx="60" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="80" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="80" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="220" rx="50" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="220" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-size="12" fill="white">Core</text>
  <text x="150" y="85" text-anchor="middle" font-size="11">Concept 1</text>
  <text x="450" y="85" text-anchor="middle" font-size="11">Concept 2</text>
  <text x="150" y="225" text-anchor="middle" font-size="11">Concept 3</text>
  <text x="450" y="225" text-anchor="middle" font-size="11">Concept 4</text>
  <line x1="250" y1="130" x2="190" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="410" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="170" x2="190" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="170" x2="410" y2="200" stroke="#333" stroke-width="2"/>
</svg>

---

## /proc Filesystem Navigation

**Key Directories:**

```bash
/proc/[pid]/fd/     # File descriptors
/proc/net/          # Network information
/proc/sys/net/      # Network parameters
/proc/net/dev       # Interface statistics
/proc/net/route     # Routing tables
```

---

## netstat Usage

```bash
# Common commands
netstat -tupln    # TCP/UDP listening ports
netstat -r        # Routing table
netstat -i        # Interface statistics
netstat -s        # Protocol statistics
```

Example output:

```bash
Proto Recv-Q Send-Q Local Address  Foreign Address  State
tcp        0      0 0.0.0.0:80    0.0.0.0:*       LISTEN
tcp        0      0 0.0.0.0:22    0.0.0.0:*       LISTEN
```

---

## `ip` Command Suite

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_network_tools)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_network_tools)"/>
  <defs>
    <marker id="arrowd1_03_network_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## `ip` addr Commands

```bash
# Display addresses
ip addr show

# Add/Remove addresses
ip addr add 192.168.1.10/24 dev eth0
ip addr del 192.168.1.10/24 dev eth0

# Set interface up/down
ip link set eth0 up
ip link set eth0 down
```

---

## `ss` (Socket Statistics)

```bash
# Common commands
ss -tuln       # TCP/UDP listening sockets
ss -ta         # All TCP sockets
ss -s          # Summary statistics
ss -p          # Show processes
```

---
## Low-level Tools

<div class="columns">
<div>

**ethtool:**
- Link status
- Driver info
- NIC settings
- Statistics

</div>
<div>

**mii-tool:**
- PHY status
- Link modes
- Auto-negotiation
- Forced modes

</div>
</div>

---

## `ethtool` Commands

```bash
# Get driver information
ethtool eth0

# Show interface statistics
ethtool -S eth0

# Modify interface settings
ethtool -s eth0 speed 1000 duplex full

# Check link status
ethtool -i eth0
```

---

## ARP Management

```bash
# View ARP cache
arp -n

# Add static entry
arp -s 192.168.1.100 00:11:22:33:44:55

# Delete entry
arp -d 192.168.1.100
```

---

## Configuration Tools Overview

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="150" rx="60" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="80" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="80" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="220" rx="50" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="220" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-size="12" fill="white">Core</text>
  <text x="150" y="85" text-anchor="middle" font-size="11">Concept 1</text>
  <text x="450" y="85" text-anchor="middle" font-size="11">Concept 2</text>
  <text x="150" y="225" text-anchor="middle" font-size="11">Concept 3</text>
  <text x="450" y="225" text-anchor="middle" font-size="11">Concept 4</text>
  <line x1="250" y1="130" x2="190" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="410" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="170" x2="190" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="170" x2="410" y2="200" stroke="#333" stroke-width="2"/>
</svg>

---

## `ifconfig` Usage

```bash
# Basic interface configuration
ifconfig eth0 192.168.1.10 netmask 255.255.255.0 up

# View interface status
ifconfig -a

# Enable/Disable interface
ifconfig eth0 up
ifconfig eth0 down
```

---

## Network Interface Scripts

```bash
# Using ifup/ifdown
ifup eth0
ifdown eth0

# Configuration location
/etc/network/interfaces    # Debian-based
/etc/sysconfig/network-scripts/ifcfg-*  # RedHat-based
```

---

## Routing Commands

```bash
# View routing table
route -n

# Add static route
route add -net 192.168.2.0/24 gw 192.168.1.1

# Delete route
route del -net 192.168.2.0/24
```

---

## Wireless Tools

```bash
# Show wireless interfaces
iwconfig

# Scan for networks
iwlist wlan0 scan

# Set wireless parameters
iwconfig wlan0 essid "NetworkName"
iwconfig wlan0 key 1234567890
```

---

## Performance Tools

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_03_network_tools)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_03_network_tools)"/>
  <defs>
    <marker id="arrowd3_03_network_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## jnettop Usage

```bash
# Monitor traffic by host
jnettop -i eth0

# Monitor specific traffic
jnettop -i eth0 'dst port 80'

# Display refresh rate
jnettop -u 2
```

---

## Network Performance Testing

```bash
# Using netperf
netperf -H server.example.com    # TCP_STREAM test
netperf -t UDP_STREAM -H server  # UDP test

# Using network statistics
nstat -az    # Show all stats with zeros
rtacct       # Show routing statistics
```

---

## Tapping Tools Overview

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="150" rx="60" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="80" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="80" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="220" rx="50" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="220" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-size="12" fill="white">Core</text>
  <text x="150" y="85" text-anchor="middle" font-size="11">Concept 1</text>
  <text x="450" y="85" text-anchor="middle" font-size="11">Concept 2</text>
  <text x="150" y="225" text-anchor="middle" font-size="11">Concept 3</text>
  <text x="450" y="225" text-anchor="middle" font-size="11">Concept 4</text>
  <line x1="250" y1="130" x2="190" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="410" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="170" x2="190" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="170" x2="410" y2="200" stroke="#333" stroke-width="2"/>
</svg>

---

## nc (netcat) Usage

```bash
# Create server
nc -l 1234

# Connect to server
nc server.example.com 1234

# Port scanning
nc -zv server.example.com 20-30

# File transfer
nc -l 1234 > received_file
nc server.example.com 1234 < file_to_send
```

---

## tcpdump Examples

```bash
# Capture basic traffic
tcpdump -i eth0

# Capture with details
tcpdump -i eth0 -nn -v

# Filter traffic
tcpdump 'port 80'
tcpdump 'host 192.168.1.10'
```

---

## Quality Control with tc

```bash
# Add traffic shaping
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms

# Set priority queuing
tc qdisc add dev eth0 root handle 1: prio

# Add filters
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 \
    match ip dst 192.168.1.0/24 flowid 1:1
```

---

## tc Queuing Disciplines

<div class="columns">
<div>

**Classes:**
- prio
- tbf
- htb
- sfq
- red

</div>
<div>

**Parameters:**
- rate
- burst
- latency
- priority

</div>
</div>

---
## Debugging Tools

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_03_network_tools)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_03_network_tools)"/>
  <defs>
    <marker id="arrowd5_03_network_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## ping Usage

```bash
# Basic ping
ping example.com

# Specific count
ping -c 4 example.com

# Different packet size
ping -s 1500 example.com

# Interval
ping -i 0.2 example.com
```

---

## traceroute Analysis

```bash
# Basic trace
traceroute example.com

# TCP traceroute
traceroute -T example.com

# UDP traceroute
traceroute -U example.com

# With timing
traceroute -n -w 2 example.com
```

---

## nmap Network Scanning

```bash
# Basic scan
nmap server.example.com

# Port range scan
nmap -p 20-100 server.example.com

# Service version detection
nmap -sV server.example.com

# OS detection
nmap -O server.example.com
```

---

## Tool Selection Guide

| Task | Primary Tool | Alternative |
|------|-------------|-------------|
| Interface Config | ip | ifconfig |
| Connection Info | ss | netstat |
| Packet Capture | tcpdump | wireshark |
| Performance | netperf | iperf |
| Debugging | ping | mtr |

---

## Best Practices

1. Regular monitoring
1. Documentation
1. Security considerations
1. Performance baselines
1. Automated testing
1. Log analysis
1. Change management

---

## Summary

- Information gathering tools
- Configuration management
- Performance monitoring
- Network debugging
- Traffic analysis
- Quality of service
