---
tags:
  - infrastructure:linux
  - audiences:sysadmin
level: intermediate
category: operating-systems
audience:
  - audiences:sysadmins
  - audiences:devops

---
# Network Services and Configuration
## Interfaces, DNS, DHCP, Firewalls, and Monitoring

---
## Network Interface Configuration

```bash
# View interfaces
ip addr show
ip link show

# Bring interface up/down
ip link set eth0 up
ip link set eth0 down

# Assign IP address
ip addr add 192.168.1.100/24 dev eth0

# Add default route
ip route add default via 192.168.1.1

# View routing table
ip route show
```

---
## The ip Command In Depth

```bash
# Show specific interface
ip addr show dev eth0

# Add multiple IPs to one interface
ip addr add 192.168.1.101/24 dev eth0
ip addr add 192.168.1.102/24 dev eth0

# Delete an address
ip addr del 192.168.1.101/24 dev eth0

# Show ARP/neighbor table
ip neigh show

# Add static ARP entry
ip neigh add 192.168.1.50 lladdr 00:11:22:33:44:55 dev eth0

# Show routing policy rules
ip rule show

# Add policy route
ip route add 10.0.0.0/8 via 192.168.1.254 table 100
ip rule add from 192.168.1.0/24 table 100
```

---
## Network Bonding and VLANs

```bash
# Install prerequisites
apt install ifenslave vlan

# Load bonding module
modprobe bonding

# Bond configuration (via netplan)
```

```yaml
# /etc/netplan/01-bond.yaml
network:
  version: 2
  bonds:
    bond0:
      interfaces: [eth0, eth1]
      parameters:
        mode: active-backup
        primary: eth0
        mii-monitor-interval: 100
      addresses: [192.168.1.100/24]
```

```bash
# VLAN tagging
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add 10.100.0.1/24 dev eth0.100
ip link set eth0.100 up
```

---
## Netplan (Ubuntu)

```yaml
# /etc/netplan/01-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

```bash
netplan apply
```

---
## Netplan Advanced Configuration

```yaml
# /etc/netplan/01-advanced.yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
        - 192.168.1.101/24
      routes:
        - to: default
          via: 192.168.1.1
        - to: 10.0.0.0/8
          via: 192.168.1.254
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
        search: [example.com, internal.example.com]
      mtu: 9000
```

```bash
# Validate configuration
netplan try     # apply with auto-revert
netplan generate  # generate backend config
```

---
## Name Resolution

```bash
# Static hosts
cat /etc/hosts
# 192.168.1.10  db-server db

# DNS resolver config
cat /etc/resolv.conf
# nameserver 8.8.8.8
# search example.com

# Name service switch
cat /etc/nsswitch.conf
# hosts: files dns myhostname
```

Resolution order is defined by `nsswitch.conf`: check `/etc/hosts` first, then `DNS`.

---
## systemd-resolved

```bash
# Modern DNS resolver on Ubuntu
systemctl status systemd-resolved

# View current DNS configuration
resolvectl status

# Query DNS
resolvectl query example.com

# Set DNS per interface
resolvectl dns eth0 8.8.8.8 8.8.4.4
resolvectl domain eth0 example.com

# Flush DNS cache
resolvectl flush-caches

# View cache statistics
resolvectl statistics
```

Note: `/etc/resolv.conf` is often a symlink to `systemd-resolved`'s stub.

---
## DHCP Server Configuration

```bash
# Install ISC DHCP server
apt install isc-dhcp-server
```

```config
# /etc/dhcp/dhcpd.conf
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    option domain-name "example.com";
    default-lease-time 600;
    max-lease-time 7200;
}

host printer {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 192.168.1.50;
}
```

---
## DHCP Advanced Options

```config
# /etc/dhcp/dhcpd.conf (continued)

# PXE boot support
allow booting;
allow bootp;
next-server 192.168.1.10;
filename "pxelinux.0";

# Failover (two DHCP servers)
failover peer "dhcp-failover" {
    primary;
    address 192.168.1.10;
    peer address 192.168.1.11;
    max-response-delay 30;
    max-unacked-updates 10;
    load balance max seconds 3;
}
```

```bash
# View current leases
cat /var/lib/dhcp/dhcpd.leases

# Test configuration
dhcpd -t -cf /etc/dhcp/dhcpd.conf
```

---
## Time Synchronization

```bash
# chrony (modern, preferred)
apt install chrony

# /etc/chrony/chrony.conf
# server ntp.ubuntu.com iburst
# pool 0.ubuntu.pool.ntp.org iburst

# Check synchronization
chronyc tracking
chronyc sources -v

# Set timezone
timedatectl set-timezone America/New_York
timedatectl status
```

---
## chrony Advanced Configuration

```config
# /etc/chrony/chrony.conf

# Multiple sources for accuracy
pool 0.ubuntu.pool.ntp.org iburst maxsources 4
server time.google.com iburst prefer

# Allow NTP clients on local network
allow 192.168.1.0/24

# Serve time even when not synced (stratum 10)
local stratum 10

# Log statistics
log tracking measurements statistics

# RTC (hardware clock) sync
rtcsync
```

```bash
# Force immediate sync
chronyc makestep

# Add NTP server at runtime
chronyc add server ntp.example.com iburst
```

---
## Firewall with nftables

```bash
# List current rules
nft list ruleset

# Create a basic firewall
nft add table inet filter
nft add chain inet filter input \
  '{ type filter hook input priority 0; policy drop; }'

# Allow loopback
nft add rule inet filter input \
  iif lo accept

# Allow established connections
nft add rule inet filter input \
  ct state established,related accept

# Allow SSH
nft add rule inet filter input \
  tcp dport 22 accept
```

---
## nftables Configuration File

```config
#!/usr/sbin/nft -f
# /etc/nftables.conf

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        iif lo accept
        ct state established,related accept
        ct state invalid drop
        tcp dport 22 accept
        tcp dport { 80, 443 } accept
        icmp type echo-request accept
        counter drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

---
## nftables: NAT and Port Forwarding

```bash
# Enable NAT (masquerade)
nft add table ip nat
nft add chain ip nat postrouting \
  '{ type nat hook postrouting priority 100; }'
nft add rule ip nat postrouting \
  oifname "eth0" masquerade

# Port forwarding (DNAT)
nft add chain ip nat prerouting \
  '{ type nat hook prerouting priority -100; }'
nft add rule ip nat prerouting \
  tcp dport 8080 dnat to 192.168.1.50:80

# Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1
```

---
## Firewall with iptables

```bash
# List rules
iptables -L -n -v

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established
iptables -A INPUT -m state \
  --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Save rules
iptables-save > /etc/iptables/rules.v4
```

---
## iptables Advanced Rules

```bash
# Rate limiting SSH connections
iptables -A INPUT -p tcp --dport 22 \
  -m conntrack --ctstate NEW \
  -m recent --set
iptables -A INPUT -p tcp --dport 22 \
  -m conntrack --ctstate NEW \
  -m recent --update --seconds 60 --hitcount 4 \
  -j DROP

# Log dropped packets
iptables -A INPUT -j LOG \
  --log-prefix "DROPPED: " --log-level 4

# Allow specific IP range
iptables -A INPUT -s 10.0.0.0/8 \
  -p tcp --dport 3306 -j ACCEPT

# Restore saved rules on boot
apt install iptables-persistent
```

---
## Network Monitoring: ss and tcpdump

```bash
# ss - socket statistics (replacement for netstat)
ss -tlnp              # listening TCP sockets
ss -ulnp              # listening UDP sockets
ss -s                 # socket summary
ss -tp state established  # established connections
```

```bash
# tcpdump - packet capture
tcpdump -i eth0                   # all traffic
tcpdump -i eth0 port 80           # HTTP traffic
tcpdump -i eth0 host 10.0.1.5    # specific host
tcpdump -i eth0 -w capture.pcap  # save to file
tcpdump -r capture.pcap          # read from file
```

---
## tcpdump Advanced Usage

```bash
# Capture with readable output
tcpdump -i eth0 -A port 80          # ASCII
tcpdump -i eth0 -X port 80          # hex + ASCII

# Complex filters
tcpdump -i eth0 'tcp port 80 and host 10.0.1.5'
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'
tcpdump -i eth0 'icmp'

# Capture DNS queries
tcpdump -i eth0 -n port 53

# Limit capture size
tcpdump -i eth0 -c 100 -s 96 -w small.pcap

# Rotate capture files
tcpdump -i eth0 -w capture-%H%M.pcap \
  -G 3600 -W 24   # new file every hour, keep 24
```

---
## Network Monitoring: nmap

```bash
# Host discovery
nmap -sn 192.168.1.0/24

# Port scan
nmap -sS 192.168.1.100

# Service detection
nmap -sV 192.168.1.100

# OS detection
nmap -O 192.168.1.100

# Comprehensive scan
nmap -A 192.168.1.100

# Scan specific ports
nmap -p 22,80,443 192.168.1.100
```

---
## Network Diagnostics

```bash
# Trace route to destination
traceroute example.com
mtr example.com           # interactive traceroute

# DNS lookup tools
dig example.com
dig +short example.com
dig MX example.com
nslookup example.com

# Check connectivity
ping -c 4 example.com
ping6 -c 4 ipv6.example.com

# Check if port is reachable
nc -zv example.com 443
timeout 3 bash -c '</dev/tcp/example.com/443' && echo open

# ARP table
ip neigh show
arp -a
```

---
## SSL/TLS Configuration

```bash
# Test SSL/TLS connection
openssl s_client -connect example.com:443

# Check certificate expiry
openssl s_client -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -dates

# Generate Diffie-Hellman parameters
openssl dhparam -out dhparam.pem 2048
```

Best practices:
- Disable TLS 1.0 and 1.1
- Use strong cipher suites
- Enable HSTS
- Use certificate automation (`certbot`/Let's Encrypt)

---
## SSL/TLS Testing and Debugging

```bash
# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# Show full certificate chain
openssl s_client -connect example.com:443 -showcerts

# Check cipher suites
openssl s_client -connect example.com:443 -cipher 'ECDHE'

# Test with SNI (Server Name Indication)
openssl s_client -connect example.com:443 \
  -servername example.com

# Verify certificate against CA
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt \
  server.crt
```

---
## VPN Overview

Common `VPN` solutions for `Linux`:
- `WireGuard` - modern, fast, simple
- `OpenVPN` - mature, widely supported
- `IPsec`/`StrongSwan` - enterprise, standards-based

```bash
# WireGuard quick setup
apt install wireguard
wg genkey | tee private.key | wg pubkey > public.key
```

```ini
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server_private_key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32
```

---
## WireGuard Complete Setup

```bash
# Server setup
wg genkey | tee /etc/wireguard/server.key | \
  wg pubkey > /etc/wireguard/server.pub

# Client setup (on client machine)
wg genkey | tee /etc/wireguard/client.key | \
  wg pubkey > /etc/wireguard/client.pub
```

```ini
# Client config: /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <client_private_key>
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = <server_public_key>
Endpoint = server.example.com:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

```bash
# Start/stop VPN
wg-quick up wg0
wg-quick down wg0
systemctl enable wg-quick@wg0
```

---
## IPv6 Configuration

```bash
# View IPv6 addresses
ip -6 addr show

# Add IPv6 address
ip -6 addr add 2001:db8::1/64 dev eth0

# Add IPv6 default route
ip -6 route add default via 2001:db8::fffe

# Enable/disable IPv6
sysctl -w net.ipv6.conf.all.disable_ipv6=0  # enable
sysctl -w net.ipv6.conf.all.disable_ipv6=1  # disable
```

```yaml
# Netplan IPv6 dual-stack
network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - 192.168.1.100/24
        - "2001:db8::100/64"
      routes:
        - to: default
          via: 2001:db8::1
```

---
## IPv6 Essentials

Key concepts:
1. `::1/128` - loopback
1. `fe80::/10` - link-local (auto-configured)
1. `2000::/3` - global unicast (routable)
1. `fd00::/8` - unique local (like RFC1918)

```bash
# Test IPv6 connectivity
ping -6 ::1
ping -6 fe80::1%eth0      # link-local needs interface

# IPv6 DNS lookup
dig AAAA example.com

# IPv6 firewall rules (nftables handles both)
nft add rule inet filter input \
  ip6 saddr 2001:db8::/32 accept
```

---
## Network Namespaces

Network namespaces provide isolated network stacks - the foundation of container networking.

```bash
# Create a namespace
ip netns add red
ip netns add blue

# List namespaces
ip netns list

# Create a veth pair connecting two namespaces
ip link add veth-red type veth peer name veth-blue
ip link set veth-red netns red
ip link set veth-blue netns blue

# Configure addresses inside namespaces
ip netns exec red ip addr add 10.0.0.1/24 dev veth-red
ip netns exec blue ip addr add 10.0.0.2/24 dev veth-blue
ip netns exec red ip link set veth-red up
ip netns exec blue ip link set veth-blue up

# Test connectivity
ip netns exec red ping 10.0.0.2
```

---

## Network Namespaces Diagram
![network_namespaces_diagram](svg/courses/operating_systems/linux-system-administration/06_network_services/network_namespaces_diagram.svg)

---

## Network Namespaces Diagram: Example

```bash
# Run a process inside a namespace
ip netns exec red bash
ip netns exec red python3 -m http.server 8080
# Delete namespace (cleans up interfaces)
ip netns del red
```

---
## Bridge Networking

A `bridge` connects multiple interfaces at Layer 2, like a virtual switch.

```bash
# Create a bridge
ip link add br0 type bridge
ip link set br0 up

# Add interfaces to the bridge
ip link set eth1 master br0
ip link set eth2 master br0

# Assign IP to the bridge
ip addr add 192.168.10.1/24 dev br0

# View bridge members
bridge link show
```

```yaml
# Netplan bridge configuration
network:
  version: 2
  bridges:
    br0:
      interfaces: [eth1, eth2]
      addresses: [192.168.10.1/24]
      dhcp4: false
```

---

## Traffic Shaping with tc: Overview

`tc` (traffic control) manages bandwidth and latency on interfaces.

---

## Traffic Shaping with tc

![traffic_shaping_with_tc](svg/courses/operating_systems/linux-system-administration/06_network_services/traffic_shaping_with_tc.svg)

---

## Traffic Shaping with tc: Example

```bash
# Limit bandwidth to 1Mbit on eth0
tc qdisc add dev eth0 root tbf \
  rate 1mbit burst 32kbit latency 400ms
# Add latency (simulate slow link)
tc qdisc add dev eth0 root netem delay 100ms 20ms
# View current rules
tc qdisc show dev eth0
# Remove all tc rules
tc qdisc del dev eth0 root
```

---
## Traffic Shaping: HTB Classes

```bash
# Hierarchical Token Bucket - allocate bandwidth
tc qdisc add dev eth0 root handle 1: htb default 30

# Parent class: 10Mbit total
tc class add dev eth0 parent 1: classid 1:1 \
  htb rate 10mbit ceil 10mbit

# High priority class: guaranteed 5Mbit
tc class add dev eth0 parent 1:1 classid 1:10 \
  htb rate 5mbit ceil 10mbit

# Low priority class: guaranteed 2Mbit
tc class add dev eth0 parent 1:1 classid 1:30 \
  htb rate 2mbit ceil 10mbit

# Classify SSH traffic as high priority
tc filter add dev eth0 parent 1:0 protocol ip \
  u32 match ip dport 22 0xffff flowid 1:10
```

---
## Network Troubleshooting Methodology

Follow a systematic bottom-up approach:

1. **Physical/Link Layer** - is the interface up?

    ```bash
    ip link show eth0
    ethtool eth0
    ```

1. **Network Layer** - do we have an IP? Can we reach the gateway?

    ```bash
    ip addr show eth0
    ping -c 2 192.168.1.1
    ```

1. **DNS** - does name resolution work?

    ```bash
    dig example.com
    cat /etc/resolv.conf
    ```

1. **Transport/Application** - is the port reachable?

    ```bash
    ss -tlnp
    nc -zv example.com 443
    curl -v https://example.com
    ```

---
## Proxy Configuration

```bash
# System-wide proxy (environment variables)
export http_proxy="http://proxy.example.com:3128"
export https_proxy="http://proxy.example.com:3128"
export no_proxy="localhost,127.0.0.1,.example.com"

# Persist in /etc/environment or /etc/profile.d/proxy.sh
```

```bash
# APT proxy
# /etc/apt/apt.conf.d/95proxy
# Acquire::http::Proxy "http://proxy.example.com:3128";
# Acquire::https::Proxy "http://proxy.example.com:3128";

# wget proxy
# ~/.wgetrc
# http_proxy = http://proxy.example.com:3128
# https_proxy = http://proxy.example.com:3128

# curl proxy
curl -x http://proxy.example.com:3128 https://example.com
```

---
## DNS Client Troubleshooting

```bash
# Check which DNS server is being used
resolvectl status
cat /etc/resolv.conf

# Query specific DNS server
dig @8.8.8.8 example.com

# Trace full DNS resolution path
dig +trace example.com

# Check for DNSSEC validation
dig +dnssec example.com

# Reverse DNS lookup
dig -x 93.184.216.34

# Check if systemd-resolved stub is active
ls -la /etc/resolv.conf
# Should symlink to ../run/systemd/resolve/stub-resolv.conf
```

```bash
# Common fix: DNS not resolving
systemctl restart systemd-resolved
resolvectl flush-caches
```

---
## iproute2 Advanced Usage

```bash
# Policy-based routing with multiple tables
ip route add default via 10.0.0.1 table 100
ip route add default via 10.0.1.1 table 200

# Route based on source address
ip rule add from 10.0.0.0/24 table 100
ip rule add from 10.0.1.0/24 table 200

# View all rules
ip rule show

# Monitor route and link changes in real time
ip monitor route
ip monitor link

# Show interface statistics
ip -s -s link show eth0

# Add GRE tunnel
ip tunnel add gre1 mode gre remote 203.0.113.1 \
  local 198.51.100.1 ttl 255
ip addr add 10.10.10.1/30 dev gre1
ip link set gre1 up
```

---
## NetworkManager vs systemd-networkd

| Feature | `NetworkManager` | `systemd-networkd` |
|---------|-----------------|-------------------|
| Target use | Desktops, laptops | Servers, containers |
| WiFi support | Full | Limited |
| VPN plugins | Many | None built-in |
| CLI tool | `nmcli` | `networkctl` |
| Config files | `/etc/NetworkManager/` | `/etc/systemd/network/` |
| Dynamic changes | Easy | Requires restart |

```bash
# NetworkManager
nmcli device status
nmcli con show
nmcli con add type ethernet ifname eth0 \
  con-name static ip4 192.168.1.100/24 gw4 192.168.1.1

# systemd-networkd
networkctl list
networkctl status eth0
```

---

## Network Boot (PXE): Overview

`PXE` (Preboot Execution Environment) allows machines to boot from the network using DHCP and TFTP.

---

## Network Boot (PXE)

![network_boot_pxe](svg/courses/operating_systems/linux-system-administration/06_network_services/network_boot_pxe.svg)

---

## Network Boot (PXE): Example

```bash
# Install TFTP server
apt install tftpd-hpa
# Place boot files in TFTP root
cp /usr/lib/PXELINUX/pxelinux.0 /srv/tftp/
cp /usr/lib/syslinux/modules/bios/ldlinux.c32 /srv/tftp/
# DHCP must provide next-server and filename
# /etc/dhcp/dhcpd.conf:
#   next-server 192.168.1.10;
#   filename "pxelinux.0";
```

---
## Wake-on-LAN

`WoL` sends a magic packet to power on remote machines over the network.

```bash
# Check if NIC supports WoL
ethtool eth0 | grep Wake-on
# Wake-on: d     (disabled)
# Wake-on: g     (enabled via magic packet)

# Enable WoL on the target machine
ethtool -s eth0 wol g

# Make persistent via systemd unit or netplan
# /etc/netplan/01-config.yaml:
#   ethernets:
#     eth0:
#       wakeonlan: true

# Send wake-up packet from another machine
apt install wakeonlan
wakeonlan AA:BB:CC:DD:EE:FF

# Send to specific subnet
wakeonlan -i 192.168.1.255 AA:BB:CC:DD:EE:FF
```

---
## ethtool for NIC Diagnostics

`ethtool` queries and configures network interface hardware settings.

```bash
# Show NIC details (speed, duplex, link status)
ethtool eth0

# Show driver and firmware info
ethtool -i eth0

# Show NIC statistics (errors, drops)
ethtool -S eth0

# Show ring buffer sizes
ethtool -g eth0

# Increase ring buffer to reduce packet drops
ethtool -G eth0 rx 4096 tx 4096

# Test NIC hardware loopback
ethtool -t eth0 online

# Enable/disable offloading features
ethtool -K eth0 tso off      # TCP segmentation offload
ethtool -K eth0 gro off      # generic receive offload
ethtool --show-offload eth0   # list all offload settings
```

---
## Network Performance Testing with iperf3

`iperf3` measures maximum achievable bandwidth between two endpoints.

```bash
# Start server on one machine
iperf3 -s

# Run client test from another machine
iperf3 -c 192.168.1.10

# Test UDP throughput (default is TCP)
iperf3 -c 192.168.1.10 -u -b 1G

# Bidirectional test
iperf3 -c 192.168.1.10 --bidir

# Test with multiple parallel streams
iperf3 -c 192.168.1.10 -P 4

# Test for a specific duration
iperf3 -c 192.168.1.10 -t 30

# Reverse mode (server sends to client)
iperf3 -c 192.168.1.10 -R

# Output in JSON for parsing
iperf3 -c 192.168.1.10 -J > results.json
```

---
## VXLAN Overlay Networks

`VXLAN` encapsulates Layer 2 frames in UDP packets, enabling overlay networks across Layer 3 boundaries.

```bash
# Create a VXLAN interface
ip link add vxlan100 type vxlan \
  id 100 \
  dstport 4789 \
  local 192.168.1.10 \
  remote 192.168.1.20 \
  dev eth0

ip addr add 10.200.0.1/24 dev vxlan100
ip link set vxlan100 up

# On the remote host (192.168.1.20)
ip link add vxlan100 type vxlan \
  id 100 \
  dstport 4789 \
  local 192.168.1.20 \
  remote 192.168.1.10 \
  dev eth0

ip addr add 10.200.0.2/24 dev vxlan100
ip link set vxlan100 up

# Test overlay connectivity
ping 10.200.0.2
```

VNI (VXLAN Network Identifier) allows up to 16 million isolated segments.

---
## keepalived for High Availability

`keepalived` provides `VRRP`-based failover for IP addresses across multiple servers.

```bash
# Install keepalived
apt install keepalived
```

```bash
# /etc/keepalived/keepalived.conf (MASTER)
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass secret123
    }
    virtual_ipaddress {
        192.168.1.200/24
    }
}
```

```bash
# BACKUP node: same config but
#   state BACKUP
#   priority 90

systemctl enable --now keepalived
# Monitor failover
journalctl -u keepalived -f
```

---
## Network Configuration Backup and Restore

```bash
# Backup all network configuration files
tar czf /backup/network-$(date +%F).tar.gz \
  /etc/netplan/ \
  /etc/hosts \
  /etc/hostname \
  /etc/resolv.conf \
  /etc/nsswitch.conf \
  /etc/nftables.conf \
  /etc/wireguard/ 2>/dev/null

# Backup current runtime state
ip addr show > /backup/ip-addr.txt
ip route show > /backup/ip-route.txt
ip rule show > /backup/ip-rule.txt
nft list ruleset > /backup/nft-ruleset.txt
```

```bash
# Restore network configuration
tar xzf /backup/network-2025-01-15.tar.gz -C /
netplan apply
systemctl restart nftables

# Verify connectivity after restore
ping -c 2 192.168.1.1
resolvectl query example.com
```

---
## /etc/network/interfaces (Legacy)

The traditional Debian/Ubuntu network configuration method, now replaced by `netplan` on modern systems.

```bash
# /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
    dns-search example.com

auto eth1
iface eth1 inet dhcp
```

```bash
# Manage interfaces with ifupdown
ifup eth0
ifdown eth0
ifquery eth0        # show configured parameters

# Still used in Debian, LXC containers, and
# older Ubuntu LTS systems (before 18.04)
```

---
## Wireless Networking Basics

```bash
# List wireless interfaces
iw dev

# Scan for available networks
iw dev wlan0 scan | grep -E "SSID|signal"

# Connect using NetworkManager (recommended)
nmcli device wifi list
nmcli device wifi connect "MyNetwork" \
  password "secret123"
nmcli connection show

# Connect using wpa_supplicant (manual)
wpa_passphrase "MyNetwork" "secret123" > \
  /etc/wpa_supplicant/wpa_supplicant.conf
wpa_supplicant -B -i wlan0 \
  -c /etc/wpa_supplicant/wpa_supplicant.conf
dhclient wlan0
```

```bash
# Monitor wireless link quality
iw dev wlan0 link
iwconfig wlan0
watch -n 1 'iw dev wlan0 station dump'
```

---
## Exercise: Configure Multi-Subnet Network

Set up a router connecting two subnets on a single Linux host:

```bash
# 1. Assign addresses to two interfaces
ip addr add 192.168.10.1/24 dev eth0
ip addr add 192.168.20.1/24 dev eth1

# 2. Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

# 3. Configure NAT for internet access from both subnets
nft add table ip nat
nft add chain ip nat postrouting \
  '{ type nat hook postrouting priority 100; }'
nft add rule ip nat postrouting \
  oifname "eth2" masquerade

# 4. Set up DHCP for each subnet
# Subnet 10: range 192.168.10.100-200
# Subnet 20: range 192.168.20.100-200

# 5. Verify routing between subnets
# From a host on subnet 10:
ping 192.168.20.1
traceroute 192.168.20.100

# 6. Add firewall rules to control inter-subnet traffic
nft add rule inet filter forward \
  ip saddr 192.168.10.0/24 ip daddr 192.168.20.0/24 \
  tcp dport { 22, 80, 443 } accept
```

---
## Network Interface Naming Schemes

Modern `Linux` uses predictable network interface names based on hardware topology.

| Prefix | Meaning |
|--------|---------|
| `en` | Ethernet |
| `wl` | Wireless LAN |
| `ww` | Wireless WAN (cellular) |

Naming schemes (in priority order):
1. `eno1` - onboard device index
1. `ens3` - PCI Express hotplug slot
1. `enp0s3` - PCI bus/slot/function
1. `enx001122334455` - MAC address

```bash
# View current interface names
ip link show

# Revert to legacy names (eth0, wlan0)
# Add to kernel command line via GRUB:
# net.ifnames=0 biosdevname=0

# Custom name via udev rule
# /etc/udev/rules.d/70-custom-net.rules
# SUBSYSTEM=="net", ACTION=="add", \
#   ATTR{address}=="00:11:22:33:44:55", NAME="mgmt0"

udevadm control --reload-rules && udevadm trigger
```

---
## ARP and Neighbor Discovery

`ARP` (Address Resolution Protocol) maps IP addresses to MAC addresses on local networks.

```bash
# View ARP/neighbor cache
ip neigh show
# 192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE

# Send ARP request to check host reachability
arping -c 3 192.168.1.1

# Send gratuitous ARP (announce our IP/MAC)
arping -U -I eth0 192.168.1.100

# Add a static ARP entry
ip neigh add 192.168.1.50 lladdr 00:11:22:33:44:55 \
  dev eth0 nud permanent

# Delete an ARP entry
ip neigh del 192.168.1.50 dev eth0
```

```bash
# ARP cache tuning via sysctl
# Time before entries expire (seconds)
sysctl net.ipv4.neigh.eth0.gc_stale_time
sysctl -w net.ipv4.neigh.default.gc_stale_time=120

# Maximum ARP table size
sysctl net.ipv4.neigh.default.gc_thresh3
```

---
## Network Troubleshooting: Packet Loss

Use a layered approach to identify where packet loss occurs.

```bash
# Basic connectivity test with loss statistics
ping -c 100 -i 0.2 192.168.1.1
# Watch for "packet loss" percentage

# mtr - combines ping and traceroute
# Shows loss at each hop
mtr -r -c 100 example.com
# Look for the first hop where loss appears

# traceroute with different protocols
traceroute example.com          # UDP (default)
traceroute -I example.com       # ICMP
traceroute -T -p 443 example.com  # TCP
```

Interpreting `mtr` results:
- Loss at a single hop but not beyond = that router deprioritizes ICMP (not real loss)
- Loss at a hop and all subsequent hops = real loss at that point
- Loss only at the final hop = destination issue

```bash
# Check local interface for errors/drops
ip -s link show eth0
ethtool -S eth0 | grep -i "error\|drop"
```

---
## Firewall Logging and Debugging

Enable logging in firewall rules to diagnose connectivity issues.

```bash
# nftables: add a log rule before a drop
nft add rule inet filter input \
  log prefix "NFT-INPUT-DROP: " level info counter drop

# nftables: log specific traffic for debugging
nft insert rule inet filter input \
  tcp dport 443 log prefix "HTTPS-IN: " accept

# View nftables log output
journalctl -k | grep "NFT-"
dmesg | grep "NFT-"
```

```bash
# iptables: LOG target
iptables -A INPUT -j LOG \
  --log-prefix "IPT-DROP: " --log-level 4

# Rate-limit logging to avoid flooding
iptables -A INPUT -m limit \
  --limit 5/min --limit-burst 10 \
  -j LOG --log-prefix "IPT-LIMIT: "

# Direct firewall logs to a separate file
# /etc/rsyslog.d/iptables.conf
# :msg, contains, "IPT-" /var/log/firewall.log
# & stop

systemctl restart rsyslog
tail -f /var/log/firewall.log
```

---

## Network Interfaces Overview

![network_interfaces_overview](svg/courses/operating_systems/linux-system-administration/06_network_services/network_interfaces_overview.svg)

---

## Firewall Overview

![firewall_overview](svg/courses/operating_systems/linux-system-administration/06_network_services/firewall_overview.svg)

---

## SSH Hardening

![ssh_hardening](svg/courses/operating_systems/linux-system-administration/06_network_services/ssh_hardening.svg)
