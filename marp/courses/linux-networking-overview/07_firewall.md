# TCP/IP Firewall
## Chapter 7: IP Filtering and Security

---

## Chapter Overview

- Firewall Fundamentals
- IP Filtering Concepts
- Linux Firewall Architecture
- IPTables Framework
- Testing and Validation
- Security Best Practices

---

## What is a Firewall

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Firewall: Network Boundary Protection</text>
  <rect x="30" y="50" width="120" height="100" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="75" text-anchor="middle" font-size="12" font-weight="bold">Trusted</text>
  <text x="90" y="92" text-anchor="middle" font-size="10" fill="#666">Internal LAN</text>
  <text x="90" y="107" text-anchor="middle" font-size="10" fill="#666">192.168.x.x</text>
  <rect x="230" y="40" width="140" height="120" fill="#ffebee" stroke="#c62828" stroke-width="3" rx="5"/>
  <text x="300" y="65" text-anchor="middle" font-size="12" font-weight="bold" fill="#c62828">FIREWALL</text>
  <text x="300" y="85" text-anchor="middle" font-size="10" fill="#333">Rule Matching</text>
  <text x="300" y="100" text-anchor="middle" font-size="10" fill="#333">ACCEPT / DROP</text>
  <text x="300" y="115" text-anchor="middle" font-size="10" fill="#333">Stateful Inspect</text>
  <text x="300" y="130" text-anchor="middle" font-size="10" fill="#333">NAT / Logging</text>
  <rect x="450" y="50" width="120" height="100" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="75" text-anchor="middle" font-size="12" font-weight="bold">Untrusted</text>
  <text x="510" y="92" text-anchor="middle" font-size="10" fill="#666">Internet</text>
  <text x="510" y="107" text-anchor="middle" font-size="10" fill="#666">Public network</text>
  <line x1="150" y1="100" x2="230" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_06_firewall)"/>
  <line x1="370" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_06_firewall)"/>
  <defs>
    <marker id="arrowd0_06_firewall" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Firewall Types

1. **Packet Filtering**
    - Network layer filtering
    - IP/port based rules

1. **Stateful Inspection**
    - Connection tracking
    - Context-aware

1. **Application Layer**
    - Deep packet inspection
    - Protocol awareness

---

## IP Filtering Concepts

- Packet inspection
- Rule matching
- Policy enforcement
- Connection tracking
- NAT integration

---

## Packet Flow

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Packet Flow Through iptables Chains</text>
  <rect x="10" y="75" width="70" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="45" y="100" text-anchor="middle" font-size="10" font-weight="bold">Incoming</text>
  <rect x="110" y="35" width="90" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="57" text-anchor="middle" font-size="10" font-weight="bold">PREROUTING</text>
  <rect x="110" y="90" width="90" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="112" text-anchor="middle" font-size="10" font-weight="bold">INPUT</text>
  <rect x="255" y="90" width="90" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="112" text-anchor="middle" font-size="10" font-weight="bold">Local Process</text>
  <rect x="255" y="35" width="90" height="35" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="57" text-anchor="middle" font-size="10" font-weight="bold">FORWARD</text>
  <rect x="400" y="90" width="90" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="112" text-anchor="middle" font-size="10" font-weight="bold">OUTPUT</text>
  <rect x="400" y="35" width="90" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="52" text-anchor="middle" font-size="10" font-weight="bold">POST-</text>
  <text x="445" y="64" text-anchor="middle" font-size="10" font-weight="bold">ROUTING</text>
  <rect x="520" y="75" width="70" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="555" y="100" text-anchor="middle" font-size="10" font-weight="bold">Outgoing</text>
  <line x1="80" y1="95" x2="110" y2="52" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <line x1="200" y1="52" x2="255" y2="52" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <line x1="155" y1="70" x2="155" y2="90" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <line x1="200" y1="107" x2="255" y2="107" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <line x1="345" y1="107" x2="400" y2="107" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <line x1="345" y1="52" x2="400" y2="52" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <line x1="490" y1="52" x2="520" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <line x1="445" y1="90" x2="445" y2="70" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_06_firewall)"/>
  <text x="300" y="155" text-anchor="middle" font-size="10" fill="#666">Routing decision determines INPUT (local) vs FORWARD (transit)</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#666">OUTPUT chain handles locally-generated packets</text>
  <defs>
    <marker id="arrowd1_06_firewall" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Linux Firewall Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Linux Firewall Architecture Stack</text>
  <rect x="100" y="30" width="400" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="12" font-weight="bold">User Space: iptables / nftables CLI</text>
  <rect x="100" y="75" width="400" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="97" text-anchor="middle" font-size="12" font-weight="bold">Netfilter Framework (kernel hooks)</text>
  <rect x="100" y="120" width="190" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="195" y="142" text-anchor="middle" font-size="11" font-weight="bold">Connection Tracking</text>
  <rect x="310" y="120" width="190" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="405" y="142" text-anchor="middle" font-size="11" font-weight="bold">NAT Engine</text>
  <rect x="100" y="165" width="400" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="185" text-anchor="middle" font-size="11" font-weight="bold">Network Stack (IP layer)</text>
  <line x1="300" y1="65" x2="300" y2="75" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_06_firewall)"/>
  <line x1="300" y1="110" x2="300" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_06_firewall)"/>
  <line x1="300" y1="155" x2="300" y2="165" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_06_firewall)"/>
  <defs>
    <marker id="arrowd2_06_firewall" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## IPTables Basic Structure

Tables:
- filter (default)
- nat
- mangle
- raw

Chains:
- INPUT
- OUTPUT
- FORWARD
- PREROUTING
- POSTROUTING

---

## IPTables Rules Syntax

```bash
iptables -A CHAIN -p PROTOCOL -s SOURCE -d DEST \
        -j ACTION

# Example:
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

---

## Common IPTables Actions

| Action | Description |
|--------|-------------|
| ACCEPT | Allow packet |
| DROP | Silently discard |
| REJECT | Discard with response |
| LOG | Log the packet |
| SNAT | Source NAT |
| DNAT | Destination NAT |

---

## Basic Firewall Rules

```bash
# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

---

## Connection Tracking

```bash
# View connection tracking
cat /proc/net/nf_conntrack

# Connection states
- NEW
- ESTABLISHED
- RELATED
- INVALID
```

---

## NAT Configuration

```bash
# Source NAT (SNAT)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Destination NAT (DNAT)
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 \
         -j DNAT --to-destination 192.168.1.10
```

---

## Port Forwarding

```bash
# Forward HTTP traffic
iptables -t nat -A PREROUTING -p tcp --dport 80 \
         -j DNAT --to-destination 192.168.1.10:8080

# Enable forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward
```

---

## Rate Limiting

```bash
# Limit SSH connections
iptables -A INPUT -p tcp --dport 22 \
         -m state --state NEW \
         -m recent --set

iptables -A INPUT -p tcp --dport 22 \
         -m state --state NEW \
         -m recent --update --seconds 60 --hitcount 4 -j DROP
```

---

## Logging Rules

```bash
# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "IPTables-Dropped: " \
         --log-level 4

# View logs
tail -f /var/log/kern.log | grep IPTables
```

---

## Testing Configuration

```bash
# List all rules
iptables -L -v -n

# Test connectivity
nc -vz host port

# Simulate traffic
hping3 -S host -p port

# Monitor traffic
tcpdump -i interface 'tcp port port'
```

---

## Security Best Practices

1. Default deny policy
1. Explicit rules
1. Connection state tracking
1. Logging and monitoring
1. Regular audits
1. Backup configuration
1. Documentation

---

## Rule Organization

<div class="columns">
<div>

**Input Chain:**
- Loopback traffic
- Established connections
- Required services
- Default deny

</div>
<div>

**Output Chain:**
- Established connections
- Required services
- Default policy

</div>
</div>

---

## Common Attack Prevention

```bash
# Block invalid packets
iptables -A INPUT -m state --state INVALID -j DROP

# Prevent IP spoofing
iptables -A INPUT -s 127.0.0.0/8 ! -i lo -j DROP

# Block ping floods
iptables -A INPUT -p icmp --icmp-type echo-request \
         -m limit --limit 1/s -j ACCEPT
```

---

## Saving and Restoring

```bash
# Save rules
iptables-save > /etc/iptables/rules.v4

# Restore rules
iptables-restore < /etc/iptables/rules.v4

# Persistent configuration
apt-get install iptables-persistent
```

---

## Rule Maintenance

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Rule Maintenance Workflow</text>
  <rect x="20" y="35" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="55" text-anchor="middle" font-size="11" font-weight="bold">Edit Rules</text>
  <text x="75" y="72" text-anchor="middle" font-size="10" fill="#666">iptables -A/-D</text>
  <rect x="165" y="35" width="110" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="55" text-anchor="middle" font-size="11" font-weight="bold">Test Rules</text>
  <text x="220" y="72" text-anchor="middle" font-size="10" fill="#666">iptables -L -v -n</text>
  <rect x="310" y="35" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="365" y="55" text-anchor="middle" font-size="11" font-weight="bold">Save Rules</text>
  <text x="365" y="72" text-anchor="middle" font-size="10" fill="#666">iptables-save</text>
  <rect x="455" y="35" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="55" text-anchor="middle" font-size="11" font-weight="bold">Persist Config</text>
  <text x="515" y="72" text-anchor="middle" font-size="10" fill="#666">iptables-restore</text>
  <line x1="130" y1="60" x2="165" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_firewall)"/>
  <line x1="275" y1="60" x2="310" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_firewall)"/>
  <line x1="420" y1="60" x2="455" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_firewall)"/>
  <rect x="80" y="120" width="440" height="55" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="5" stroke-dasharray="5,3"/>
  <text x="300" y="142" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">Audit Cycle: Review logs, remove stale rules, update for new services</text>
  <text x="300" y="160" text-anchor="middle" font-size="10" fill="#666">Keep backup: iptables-save > /etc/iptables/rules.v4.bak before changes</text>
  <defs>
    <marker id="arrowd3_06_firewall" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Performance Optimization

1. Rule ordering
1. Chain organization
1. Connection tracking
1. State matching
1. Hardware offloading
1. Regular cleanup

---

## Debugging Tools

```bash
# Rule monitoring
watch iptables -nvL

# Packet tracing
iptables -t raw -A PREROUTING -p tcp --dport 80 -j TRACE

# Connection tracking
conntrack -L

# System logs
journalctl -f
```

---

## IPv6 Firewall

```bash
# IPv6 rules
ip6tables -A INPUT -p tcp --dport 80 -j ACCEPT

# Dual stack configuration
ip6tables-restore < /etc/iptables/rules.v6
```

---

## Summary

- Firewall concepts
- IPTables framework
- Rule configuration
- Security practices
- Testing methods
- Performance considerations
