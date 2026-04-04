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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Information Tools</text>
  <rect x="20" y="30" width="120" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="80" y="50" text-anchor="middle" font-size="11" font-weight="bold">/proc/net</text>
  <text x="80" y="68" text-anchor="middle" font-size="10">kernel stats</text>
  <rect x="160" y="30" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="50" text-anchor="middle" font-size="11" font-weight="bold">netstat / ss</text>
  <text x="220" y="68" text-anchor="middle" font-size="10">connections</text>
  <rect x="300" y="30" width="120" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="50" text-anchor="middle" font-size="11" font-weight="bold">ip addr/link</text>
  <text x="360" y="68" text-anchor="middle" font-size="10">interface info</text>
  <rect x="440" y="30" width="130" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="505" y="50" text-anchor="middle" font-size="11" font-weight="bold">/sys/class/net</text>
  <text x="505" y="68" text-anchor="middle" font-size="10">device attrs</text>
  <rect x="80" y="100" width="440" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="122" text-anchor="middle" font-size="11">Read-only tools: safe for production monitoring</text>
  <text x="300" y="160" text-anchor="middle" font-size="10" fill="#666">Use these to gather data before making configuration changes</text>
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
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">ip Command Hierarchy</text>
  <rect x="225" y="25" width="150" height="30" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="45" text-anchor="middle" font-size="12" font-weight="bold">ip</text>
  <rect x="20" y="75" width="90" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="65" y="95" text-anchor="middle" font-size="10">ip addr</text>
  <rect x="120" y="75" width="90" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="165" y="95" text-anchor="middle" font-size="10">ip link</text>
  <rect x="220" y="75" width="90" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="265" y="95" text-anchor="middle" font-size="10">ip route</text>
  <rect x="320" y="75" width="90" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="365" y="95" text-anchor="middle" font-size="10">ip neigh</text>
  <rect x="420" y="75" width="90" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="465" y="95" text-anchor="middle" font-size="10">ip netns</text>
  <line x1="300" y1="55" x2="65" y2="75" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="55" x2="165" y2="75" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="55" x2="265" y2="75" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="55" x2="365" y2="75" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="55" x2="465" y2="75" stroke="#333" stroke-width="1"/>
  <text x="65" y="122" text-anchor="middle" font-size="9" fill="#666">show/add/del</text>
  <text x="65" y="133" text-anchor="middle" font-size="9" fill="#666">IP addresses</text>
  <text x="165" y="122" text-anchor="middle" font-size="9" fill="#666">set up/down</text>
  <text x="165" y="133" text-anchor="middle" font-size="9" fill="#666">MTU, flags</text>
  <text x="265" y="122" text-anchor="middle" font-size="9" fill="#666">show/add/del</text>
  <text x="265" y="133" text-anchor="middle" font-size="9" fill="#666">routing table</text>
  <text x="365" y="122" text-anchor="middle" font-size="9" fill="#666">ARP/NDP</text>
  <text x="365" y="133" text-anchor="middle" font-size="9" fill="#666">neighbors</text>
  <text x="465" y="122" text-anchor="middle" font-size="9" fill="#666">network</text>
  <text x="465" y="133" text-anchor="middle" font-size="9" fill="#666">namespaces</text>
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="#666">Replaces: ifconfig, route, arp, netstat</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Configuration Tools</text>
  <rect x="20" y="30" width="120" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="80" y="48" text-anchor="middle" font-size="11" font-weight="bold">ifconfig</text>
  <text x="80" y="66" text-anchor="middle" font-size="10">legacy config</text>
  <rect x="160" y="30" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="48" text-anchor="middle" font-size="11" font-weight="bold">ip link/addr</text>
  <text x="220" y="66" text-anchor="middle" font-size="10">modern config</text>
  <rect x="300" y="30" width="120" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="48" text-anchor="middle" font-size="11" font-weight="bold">route / ip route</text>
  <text x="360" y="66" text-anchor="middle" font-size="10">routing tables</text>
  <rect x="440" y="30" width="130" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="505" y="48" text-anchor="middle" font-size="11" font-weight="bold">iwconfig</text>
  <text x="505" y="66" text-anchor="middle" font-size="10">wireless setup</text>
  <rect x="80" y="100" width="440" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="122" text-anchor="middle" font-size="11">Write operations: require root privileges, affect live traffic</text>
  <text x="300" y="160" text-anchor="middle" font-size="10" fill="#666">Prefer ip (iproute2) over legacy net-tools (ifconfig, route, arp)</text>
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
  <defs>
    <marker id="arrowd3_03_network_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Performance Testing Tools</text>
  <rect x="20" y="30" width="120" height="60" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="80" y="50" text-anchor="middle" font-size="11" font-weight="bold">netperf</text>
  <text x="80" y="65" text-anchor="middle" font-size="10">TCP_STREAM</text>
  <text x="80" y="78" text-anchor="middle" font-size="10">UDP_STREAM</text>
  <rect x="160" y="30" width="120" height="60" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="50" text-anchor="middle" font-size="11" font-weight="bold">iperf3</text>
  <text x="220" y="65" text-anchor="middle" font-size="10">bandwidth</text>
  <text x="220" y="78" text-anchor="middle" font-size="10">bidirectional</text>
  <rect x="300" y="30" width="120" height="60" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="50" text-anchor="middle" font-size="11" font-weight="bold">nstat</text>
  <text x="360" y="65" text-anchor="middle" font-size="10">kernel stats</text>
  <text x="360" y="78" text-anchor="middle" font-size="10">SNMP counters</text>
  <rect x="440" y="30" width="130" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="505" y="50" text-anchor="middle" font-size="11" font-weight="bold">jnettop</text>
  <text x="505" y="65" text-anchor="middle" font-size="10">live traffic</text>
  <text x="505" y="78" text-anchor="middle" font-size="10">per-host stats</text>
  <rect x="80" y="110" width="440" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="128" text-anchor="middle" font-size="10">Measure: throughput, latency, packet loss, jitter</text>
  <text x="300" y="142" text-anchor="middle" font-size="10">Compare: baseline vs. current performance</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#666">Always establish baselines before troubleshooting</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowtap_03" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Tapping / Capture Tools</text>
  <rect x="20" y="30" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="80" y="48" text-anchor="middle" font-size="11" font-weight="bold">tcpdump</text>
  <text x="80" y="63" text-anchor="middle" font-size="10">CLI capture</text>
  <text x="80" y="76" text-anchor="middle" font-size="10">BPF filters</text>
  <rect x="160" y="30" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="48" text-anchor="middle" font-size="11" font-weight="bold">Wireshark</text>
  <text x="220" y="63" text-anchor="middle" font-size="10">GUI analysis</text>
  <text x="220" y="76" text-anchor="middle" font-size="10">protocol decode</text>
  <rect x="300" y="30" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="48" text-anchor="middle" font-size="11" font-weight="bold">netcat (nc)</text>
  <text x="360" y="63" text-anchor="middle" font-size="10">raw connections</text>
  <text x="360" y="76" text-anchor="middle" font-size="10">port scanning</text>
  <rect x="440" y="30" width="130" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="505" y="48" text-anchor="middle" font-size="11" font-weight="bold">tshark</text>
  <text x="505" y="63" text-anchor="middle" font-size="10">CLI Wireshark</text>
  <text x="505" y="76" text-anchor="middle" font-size="10">scriptable</text>
  <rect x="80" y="105" width="440" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="125" text-anchor="middle" font-size="11">Capture point: NIC --&gt; libpcap/AF_PACKET --&gt; user tool</text>
  <text x="300" y="160" text-anchor="middle" font-size="10" fill="#666">tcpdump -i eth0 -w capture.pcap / wireshark capture.pcap</text>
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
  <defs>
    <marker id="arrowd5_03_network_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">Debugging Workflow</text>
  <rect x="20" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="70" y="45" text-anchor="middle" font-size="10" font-weight="bold">ping</text>
  <text x="70" y="60" text-anchor="middle" font-size="9">connectivity</text>
  <rect x="140" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="190" y="45" text-anchor="middle" font-size="10" font-weight="bold">traceroute</text>
  <text x="190" y="60" text-anchor="middle" font-size="9">path analysis</text>
  <rect x="260" y="30" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="310" y="45" text-anchor="middle" font-size="10" font-weight="bold">nmap</text>
  <text x="310" y="60" text-anchor="middle" font-size="9">port scanning</text>
  <rect x="380" y="30" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="430" y="45" text-anchor="middle" font-size="10" font-weight="bold">tcpdump</text>
  <text x="430" y="60" text-anchor="middle" font-size="9">packet capture</text>
  <rect x="500" y="30" width="80" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="540" y="45" text-anchor="middle" font-size="10" font-weight="bold">ss</text>
  <text x="540" y="60" text-anchor="middle" font-size="9">socket info</text>
  <line x1="120" y1="50" x2="140" y2="50" stroke="#333" stroke-width="1" marker-end="url(#arrowd5_03_network_tools)"/>
  <line x1="240" y1="50" x2="260" y2="50" stroke="#333" stroke-width="1" marker-end="url(#arrowd5_03_network_tools)"/>
  <line x1="360" y1="50" x2="380" y2="50" stroke="#333" stroke-width="1" marker-end="url(#arrowd5_03_network_tools)"/>
  <line x1="480" y1="50" x2="500" y2="50" stroke="#333" stroke-width="1" marker-end="url(#arrowd5_03_network_tools)"/>
  <rect x="60" y="90" width="480" height="35" fill="#f9f9f9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="112" text-anchor="middle" font-size="11">L3 reachable? --&gt; Route OK? --&gt; Port open? --&gt; Traffic OK? --&gt; Sockets OK?</text>
  <text x="300" y="145" text-anchor="middle" font-size="10" fill="#666">Systematic approach: test layer by layer, bottom to top</text>
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
