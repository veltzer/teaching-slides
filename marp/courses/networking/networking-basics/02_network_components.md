# Network Components: Understanding the Differences

- Load Balancers
- Proxies
- Reverse Proxies
- NAT (Network Address Translation)
- Other Related Terms

---

## Load Balancer

- Distributes incoming network traffic across multiple servers
- Ensures no single server becomes overwhelmed
- Improves application responsiveness and availability

---

## Load Balancer

![load_balancer](svg/courses/networking/networking-basics/02_network_components/load_balancer.svg)

---

## Proxy Server

- Acts as an intermediary between clients and servers
- Can provide anonymity, security, and caching
- Often used to bypass restrictions or improve performance

---

## Proxy Server

![proxy_server](svg/courses/networking/networking-basics/02_network_components/proxy_server.svg)

---

## Reverse Proxy

- Sits in front of web servers and forwards client requests
- Provides benefits like load balancing, SSL termination, and caching
- Often used to enhance security and performance of web applications

---

## Reverse Proxy

![reverse_proxy](svg/courses/networking/networking-basics/02_network_components/reverse_proxy.svg)

---

## NAT (Network Address Translation)

- Modifies network address information in packet headers
- Allows multiple devices to share a single public IP address
- Enhances security by hiding internal network structure

---

## NAT (Network Address Translation)

![nat_network_address_translation](svg/courses/networking/networking-basics/02_network_components/nat_network_address_translation.svg)

---

## Other Related Terms

### Firewall
- Monitors and controls incoming and outgoing network traffic
- Establishes a barrier between trusted internal networks and untrusted external networks

### VPN (Virtual Private Network)
- Extends a private network across a public network
- Enables users to send and receive data across shared or public networks as if directly connected to the private network

---

## Comparison

| Term | Primary Function | Location | Direction |
|------|------------------|----------|-----------|
| Load Balancer | Distribute traffic | In front of servers | Inbound |
| Proxy | Intermediary for clients | Client side | Outbound |
| Reverse Proxy | Intermediary for servers | Server side | Inbound |
| NAT | IP address translation | Network boundary | Both |
| Firewall | Traffic filtering | Network boundary | Both |
| VPN | Secure remote access | Between networks | Both |

---

## Summary

- **Load Balancers** distribute traffic across servers
- **Proxies** act on behalf of clients
- **Reverse Proxies** act on behalf of servers
- **NAT** translates private to public IP addresses
- **Firewalls** filter network traffic
- **VPNs** provide secure remote network access

Each component plays a crucial role in modern network architecture!
