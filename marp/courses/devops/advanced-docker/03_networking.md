# Docker Networking in Depth

Mastering container connectivity

---

## Agenda

- `Docker` network drivers
- Bridge networking deep dive
- Host and none networks
- Overlay networking
- `Macvlan` and `IPvlan`
- `DNS` and service discovery
- Network troubleshooting
- Custom network plugins

---

## Docker Network Drivers Overview

| Driver    | Scope   | Description                          |
|-----------|---------|--------------------------------------|
| `bridge`  | Local   | Default. Isolated network on host    |
| `host`    | Local   | Container shares host network stack  |
| `none`    | Local   | No networking                        |
| `overlay` | Swarm   | Multi-host networking                |
| `macvlan` | Local   | Assign MAC address to container      |
| `ipvlan`  | Local   | Share host MAC, separate IPs         |

```bash
# List available networks
docker network ls

# Inspect a network
docker network inspect bridge
```

---

## Default Bridge Network

```diagram
┌──────────────────────────────────────┐
│              Host                     │
│                                      │
│  ┌─────────┐       ┌─────────┐      │
│  │Container│       │Container│      │
│  │  eth0   │       │  eth0   │      │
│  │172.17.0.2│      │172.17.0.3│     │
│  └────┬────┘       └────┬────┘      │
│       │                  │           │
│   vethXXXX          vethYYYY        │
│       │                  │           │
│  ┌────┴──────────────────┴────┐      │
│  │       docker0 bridge       │      │
│  │        172.17.0.1          │      │
│  └────────────────────────────┘      │
│                                      │
│           eth0 (host)                │
└──────────────────────────────────────┘
```

---

## Default Bridge - Limitations

```bash
# Containers on default bridge can communicate by IP
docker run -d --name web1 nginx
docker run -d --name web2 nginx

# But DNS resolution does NOT work on default bridge
docker exec web1 ping web2
# ping: bad address 'web2'

# Must use IP addresses or links (deprecated)
WEB2_IP=$(docker inspect web2 --format '{{.NetworkSettings.IPAddress}}')
docker exec web1 ping $WEB2_IP
```

**Always use user-defined bridge networks in production.**

---

## User-Defined Bridge Networks

```bash
# Create a custom bridge network
docker network create --driver bridge \
  --subnet 10.10.0.0/24 \
  --gateway 10.10.0.1 \
  --ip-range 10.10.0.128/25 \
  --opt com.docker.network.bridge.name=br-myapp \
  myapp-net

# Run containers on custom network
docker run -d --name api --network myapp-net nginx
docker run -d --name db --network myapp-net postgres:16

# DNS resolution works!
docker exec api ping db
# PING db (10.10.0.129): 56 data bytes
```

---

## User-Defined Bridge - Features

| Feature                    | Default Bridge | User-Defined Bridge |
|----------------------------|:--------------:|:-------------------:|
| Automatic DNS resolution   | No             | Yes                 |
| Network isolation          | Basic          | Full                |
| Connect/disconnect live    | No             | Yes                 |
| Custom subnet              | No             | Yes                 |
| Link containers            | `--link` only  | Automatic           |

```bash
# Connect a running container to a network
docker network connect myapp-net existing-container

# Disconnect from a network
docker network disconnect bridge existing-container

# Container on multiple networks
docker run -d --name multi --network net1 nginx
docker network connect net2 multi
```

---

## Bridge Network - iptables Rules

```bash
# Docker manages iptables rules for networking
sudo iptables -t nat -L -n -v

# NAT for outbound traffic (MASQUERADE)
sudo iptables -t nat -L POSTROUTING -n -v
# MASQUERADE  all  --  172.17.0.0/16  0.0.0.0/0

# Port forwarding (DNAT)
docker run -d -p 8080:80 nginx
sudo iptables -t nat -L DOCKER -n -v
# DNAT  tcp  --  0.0.0.0/0  0.0.0.0/0  tcp dpt:8080 to:172.17.0.2:80

# Inter-container communication
sudo iptables -L DOCKER-ISOLATION-STAGE-1 -n -v
```

---

## Port Publishing Options

```bash
# Map host port to container port
docker run -d -p 8080:80 nginx

# Map to specific host interface
docker run -d -p 127.0.0.1:8080:80 nginx

# Random host port
docker run -d -p 80 nginx
docker port <container-id>
# 0.0.0.0:32768

# UDP port
docker run -d -p 5000:5000/udp myapp

# Multiple ports
docker run -d -p 80:80 -p 443:443 nginx

# Range of ports
docker run -d -p 8000-8010:8000-8010 myapp
```

---

## Host Network Mode

```bash
# Container shares host's network stack directly
docker run -d --network host --name web nginx

# No network isolation - container uses host ports directly
# No port mapping needed (or allowed)
curl localhost:80  # Works directly

# Performance: No NAT overhead
# Use case: High-performance networking, many ports
```

```diagram
┌──────────────────────────────┐
│           Host               │
│  ┌────────────────────────┐  │
│  │    Container Process   │  │
│  │  (uses host network)   │  │
│  └────────────────────────┘  │
│         eth0: 192.168.1.10   │
└──────────────────────────────┘
```

---

## None Network Mode

```bash
# Container with no network at all
docker run -d --network none --name isolated alpine sleep 3600

# Verify - no network interfaces (except loopback)
docker exec isolated ip addr show
# 1: lo: <LOOPBACK,UP,LOWER_UP>
#     inet 127.0.0.1/8 scope host lo

# Use cases:
# - Batch processing with no network needs
# - Security-sensitive workloads
# - Custom networking setup via nsenter
```

---

## Overlay Networks - Multi-Host Networking

```bash
# Initialize Docker Swarm (required for overlay)
docker swarm init

# Create overlay network
docker network create --driver overlay \
  --subnet 10.20.0.0/16 \
  --opt encrypted \
  myoverlay

# Deploy services on overlay network
docker service create --name web \
  --network myoverlay \
  --replicas 3 \
  nginx

docker service create --name api \
  --network myoverlay \
  --replicas 2 \
  myapp:latest
```

---

## Overlay Network Architecture

```diagram
┌─────────── Node 1 ───────────┐  ┌─────────── Node 2 ───────────┐
│                               │  │                               │
│  ┌─────────┐  ┌─────────┐    │  │  ┌─────────┐  ┌─────────┐   │
│  │ web.1   │  │ api.1   │    │  │  │ web.2   │  │ api.2   │   │
│  │10.20.0.3│  │10.20.0.4│    │  │  │10.20.0.5│  │10.20.0.6│   │
│  └────┬────┘  └────┬────┘    │  │  └────┬────┘  └────┬────┘   │
│       └──────┬─────┘         │  │       └──────┬─────┘        │
│         br-overlay           │  │         br-overlay          │
│              │               │  │              │              │
│         VXLAN tunnel ────────┼──┼──── VXLAN tunnel            │
│              │               │  │              │              │
│           eth0               │  │           eth0              │
└──────────────────────────────┘  └──────────────────────────────┘
```

---

## Overlay Network - VXLAN Details

- Uses `VXLAN` (Virtual Extensible LAN) encapsulation
- UDP port `4789` for data plane
- Gossip protocol on port `7946` for control plane
- Optional `IPSec` encryption between nodes

```bash
# Check VXLAN interfaces
ip -d link show type vxlan

# Monitor overlay traffic
sudo tcpdump -i eth0 port 4789 -n

# Verify encryption is enabled
docker network inspect myoverlay \
  --format '{{.Options}}'
# map[encrypted:]
```

---

## Overlay Network - Attachable

```bash
# Attachable overlay: standalone containers can join
docker network create --driver overlay \
  --attachable \
  dev-overlay

# Now standalone containers can connect
docker run -it --network dev-overlay alpine sh

# Useful for debugging services
docker run -it --network dev-overlay \
  nicolaka/netshoot \
  curl http://web:80
```

---

## `Macvlan` Networks

```bash
# Assign a real MAC address - container appears as physical device
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  macvlan-net

docker run -d --network macvlan-net \
  --ip=192.168.1.100 \
  --name macvlan-web nginx

# Container is accessible directly on the LAN
# Other machines can reach 192.168.1.100 directly
```

---

## `Macvlan` Network Architecture

```diagram
┌────────────── Physical Network ──────────────┐
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Router   │  │  Host    │  │ Other    │   │
│  │  .1       │  │  .10     │  │ Device   │   │
│  └──────────┘  │          │  │  .50     │   │
│                │Container │  └──────────┘   │
│                │  .100    │                  │
│                │(own MAC) │                  │
│                └──────────┘                  │
│           192.168.1.0/24                     │
└───────────────────────────────────────────────┘
```

**Limitation:** Host cannot communicate with `macvlan` containers directly (use `macvlan` sub-interface to work around).

---

## `Macvlan` - 802.1q Trunk Mode

```bash
# Create macvlan on VLAN-tagged sub-interface
docker network create -d macvlan \
  --subnet=10.10.10.0/24 \
  --gateway=10.10.10.1 \
  -o parent=eth0.10 \
  macvlan-vlan10

docker network create -d macvlan \
  --subnet=10.10.20.0/24 \
  --gateway=10.10.20.1 \
  -o parent=eth0.20 \
  macvlan-vlan20

# Containers on different VLANs
docker run -d --network macvlan-vlan10 --name app1 nginx
docker run -d --network macvlan-vlan20 --name app2 nginx
```

---

## `IPvlan` Networks

```bash
# L2 mode - like macvlan but shares host MAC
docker network create -d ipvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  -o ipvlan_mode=l2 \
  ipvlan-l2

# L3 mode - routing between subnets
docker network create -d ipvlan \
  --subnet=10.10.10.0/24 \
  -o parent=eth0 \
  -o ipvlan_mode=l3 \
  ipvlan-l3
```

| Feature     | `Macvlan`       | `IPvlan` L2     | `IPvlan` L3     |
|-------------|-----------------|-----------------|-----------------|
| MAC address | Unique per cnt  | Shared with host| Shared with host|
| Broadcast   | Yes             | Yes             | No              |
| Routing     | L2              | L2              | L3              |

---

## DNS and Service Discovery

```bash
# Docker's embedded DNS server: 127.0.0.11
docker run --rm --network myapp-net alpine cat /etc/resolv.conf
# nameserver 127.0.0.11

# Containers resolve each other by name
docker run -d --name redis --network myapp-net redis:7
docker run --rm --network myapp-net alpine ping redis
# PING redis (10.10.0.3): 56 data bytes

# Also resolves by network alias
docker run -d --name web --network myapp-net \
  --network-alias webserver \
  --network-alias frontend \
  nginx

docker run --rm --network myapp-net alpine ping webserver
docker run --rm --network myapp-net alpine ping frontend
```

---

## DNS Round-Robin Load Balancing

```bash
# Multiple containers with the same alias
docker network create mynet
docker run -d --name web1 --network mynet --network-alias web nginx
docker run -d --name web2 --network mynet --network-alias web nginx
docker run -d --name web3 --network mynet --network-alias web nginx

# DNS returns all IPs (round-robin)
docker run --rm --network mynet alpine nslookup web
# Name:      web
# Address 1: 10.10.0.2
# Address 2: 10.10.0.3
# Address 3: 10.10.0.4

# Each request may go to a different container
for i in $(seq 1 6); do
  docker run --rm --network mynet alpine ping -c 1 web 2>&1 | head -1
done
```

---

## Swarm Service Discovery - VIP Mode

```bash
# Create a service (default VIP mode)
docker service create --name web --replicas 3 \
  --network myoverlay nginx

# Service gets a Virtual IP
docker service inspect web \
  --format '{{range .Endpoint.VirtualIPs}}{{.Addr}}{{end}}'
# 10.20.0.5/24

# All requests to VIP are load-balanced across replicas
# Uses IPVS (Linux Virtual Server) in the kernel
```

```diagram
Client → VIP (10.20.0.5) → IPVS → Task 1 (10.20.0.6)
                                  → Task 2 (10.20.0.7)
                                  → Task 3 (10.20.0.8)
```

---

## Swarm Service Discovery - DNSRR Mode

```bash
# DNS Round-Robin mode (no VIP)
docker service create --name api --replicas 3 \
  --network myoverlay \
  --endpoint-mode dnsrr \
  myapp:latest

# DNS returns all task IPs directly
docker exec <container> nslookup api
# Returns multiple A records

# Use when:
# - External load balancer handles balancing
# - Client needs to know all backend IPs
# - Using non-HTTP protocols
```

---

## Custom DNS Configuration

```bash
# Set DNS servers for a container
docker run --dns 8.8.8.8 --dns 8.8.4.4 alpine nslookup google.com

# Add DNS search domain
docker run --dns-search example.com alpine nslookup myhost
# Resolves myhost.example.com

# Add /etc/hosts entries
docker run --add-host db.local:10.10.0.5 \
           --add-host api.local:10.10.0.6 \
           alpine cat /etc/hosts

# Global DNS config in daemon.json
{
  "dns": ["8.8.8.8", "8.8.4.4"],
  "dns-search": ["example.com"],
  "dns-opts": ["ndots:2"]
}
```

---

## Network Troubleshooting with `netshoot`

```bash
# The Swiss Army knife for network debugging
docker run -it --network myapp-net nicolaka/netshoot

# Tools included: curl, ping, dig, nslookup, tcpdump,
# iperf3, netstat, ss, ip, mtr, traceroute, etc.

# Debug a specific container's network
docker run -it --network container:web nicolaka/netshoot

# Debug host networking
docker run -it --network host nicolaka/netshoot

# Capture traffic on a container's network
docker run -it --network container:web nicolaka/netshoot \
  tcpdump -i eth0 -n port 80
```

---

## Network Performance Testing

```bash
# Run iperf3 server
docker run -d --name iperf-server --network mynet \
  networkstatic/iperf3 -s

# Run client test
docker run --rm --network mynet \
  networkstatic/iperf3 -c iperf-server

# Compare network modes:
# Bridge mode
docker run -d --name server-bridge networkstatic/iperf3 -s
docker run --rm --link server-bridge networkstatic/iperf3 -c server-bridge

# Host mode
docker run -d --network host --name server-host networkstatic/iperf3 -s
docker run --rm --network host networkstatic/iperf3 -c 127.0.0.1
# Host mode typically shows 20-30% better throughput
```

---

## Network Debugging Commands

```bash
# Inspect network details
docker network inspect myapp-net

# View container's network settings
docker inspect web --format '{{json .NetworkSettings}}' | jq

# Check connectivity between containers
docker exec web ping -c 3 db
docker exec web curl -s http://api:8080/health

# Check DNS resolution
docker exec web nslookup db
docker exec web dig +short api

# Check listening ports inside container
docker exec web ss -tlnp
docker exec web netstat -tlnp

# View iptables rules
sudo iptables -L -n -v
sudo iptables -t nat -L -n -v
```

---

## Network Security - Isolation

```bash
# Internal network - no external access
docker network create --internal secure-net

# Container can talk to others on the network
# but CANNOT reach the internet
docker run --rm --network secure-net alpine ping 8.8.8.8
# Network unreachable

# Disable inter-container communication on default bridge
{
  "icc": false
}

# Containers must use --link or explicit port publishing
# to communicate when ICC is disabled
```

---

## Docker Compose Networking

```yaml
# docker-compose.yml
services:
  web:
    image: nginx
    networks:
      - frontend
      - backend
    ports:
      - "80:80"

  api:
    image: myapp
    networks:
      - backend
      - database

  db:
    image: postgres:16
    networks:
      - database

networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 10.10.1.0/24
  backend:
    driver: bridge
  database:
    driver: bridge
    internal: true  # No external access
```

---

## IPv6 Networking

```bash
# Enable IPv6 in daemon.json
{
  "ipv6": true,
  "fixed-cidr-v6": "fd00::/64"
}

# Create dual-stack network
docker network create --ipv6 \
  --subnet 10.10.0.0/24 \
  --subnet fd00:dead:beef::/64 \
  dual-stack

# Run container with IPv6
docker run -d --network dual-stack --name web6 nginx

# Verify
docker exec web6 ip -6 addr show
docker exec web6 ping6 web6
```

---

## Network Plugins and CNI

```bash
# Install a network plugin (e.g., Weave)
docker plugin install weaveworks/net-plugin:latest_release

# Create network using plugin
docker network create --driver weaveworks/net-plugin:latest_release \
  weave-net

# Popular network plugins:
# - Weave Net: mesh overlay with encryption
# - Calico: L3 networking with BGP
# - Flannel: simple overlay networking
# - Cilium: eBPF-based networking and security
```

---

## Summary - Docker Networking

- **Bridge**: Default; use user-defined bridges for DNS and isolation
- **Host**: Maximum performance, no isolation
- **Overlay**: Multi-host with `VXLAN` tunneling
- **Macvlan**: Direct LAN access with unique MAC addresses
- **IPvlan**: Direct LAN access sharing host MAC
- DNS resolution is automatic on user-defined networks
- Service discovery via `VIP` (default) or `DNSRR` in Swarm
- Use `--internal` for networks that should not reach the internet
- Debug with `netshoot`, `tcpdump`, `iperf3`
- Choose the right driver based on performance and isolation needs
