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

## What is a Firewall?

![0](../../../out/mermaid/marp/courses/linux-networking-overview/06_firewall.md/0.png)

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

![1](../../../out/mermaid/marp/courses/linux-networking-overview/06_firewall.md/1.png)

---

## Linux Firewall Architecture

![2](../../../out/mermaid/marp/courses/linux-networking-overview/06_firewall.md/2.png)

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

![3](../../../out/mermaid/marp/courses/linux-networking-overview/06_firewall.md/3.png)

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
