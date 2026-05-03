---
tags:
  - networking:tcp-ip
  - concepts:routing
level: intermediate
category: networking
audience:
  - audiences:network-engineers
  - audiences:devops

---
# Routing

---
## What This Chapter Covers

- Routing fundamentals
- Static vs dynamic routing
- Distance-vector and link-state algorithms
- BGP and the major Interior Gateway Protocols
- Cloud-era routing realities

---
## What Is Routing?

- Deciding where to forward a packet
- Per-router decision based on destination IP
- Each router only knows the next hop
- Repeated hop-by-hop until delivery
- The internet works hop by hop

---
## Routing Table

- Destination prefix → next hop, interface
- Most-specific match wins (longest prefix match)
- Default route catches unmatched
- Per-protocol metrics for tie-breaking
- View: `ip route show` (Linux)

---
## Routing Decision Visualized

![routing](svg/courses/networking/tcp-ip-deep-dive/07_routing/routing.svg)

---
## Static Routing

- Manually configured routes
- Simple, predictable
- Doesn't adapt to failures
- Fine for small networks
- Dangerous at scale (operational burden)

---
## Dynamic Routing

- Routers exchange topology information
- Routes update when links go up/down
- Different protocols, different scopes
- Convergence: time to settle after change
- The default for any non-trivial network

---
## Protocol Families

![routing_protocols](svg/courses/networking/tcp-ip-deep-dive/07_routing/routing_protocols.svg)

---
## Distance-Vector

- Each router knows distance + next hop per destination
- Tells neighbors what it knows
- Bellman-Ford algorithm
- Examples include the older distance-vector protocols
- Slow convergence on big topologies

---
## Link-State

- Each router knows the full topology
- Floods link state updates to all
- Each router computes shortest path locally
- Examples include the major link-state protocols
- Faster convergence, more memory

---
## Open Shortest Path First

- Open Shortest Path First
- Most-used Interior Gateway Protocol
- Link-state algorithm
- Areas for hierarchical scaling
- Standard in enterprise

---
## Areas

- Area 0 (backbone)
- Other areas connect to it
- Reduces flooding scope
- Stub areas, not-so-stubby areas
- Key for scalability

---
## BGP

- Border Gateway Protocol
- The protocol of the internet
- Path-vector algorithm (each AS hop is a step)
- Policy-driven, not just shortest
- Carries hundreds of thousands of routes

---
## BGP Visualized

![bgp_path](svg/courses/networking/tcp-ip-deep-dive/07_routing/bgp_path.svg)

---
## External vs Internal BGP

- External BGP: between different autonomous systems
- Internal BGP: within same AS (usually full mesh or route reflectors)
- Different rules, different uses
- Internal BGP doesn't change AS path
- Route reflectors scale internal BGP

---
## BGP Path Selection

- Highest local preference
- Shortest AS path
- Origin (interior beats exterior beats incomplete)
- Lowest MED
- External over internal BGP
- Many tie-breakers
- Policy reigns

---
## BGP Communities

- Tags attached to routes
- Used for policy: which routes to accept, prefer, advertise
- Standard or custom communities
- Critical for traffic engineering
- Provider-specific tags too

---
## Route Filtering

- Don't accept anything you don't expect
- Prefix lists, AS-path filters, route maps
- Bogon filtering (private/reserved ranges)
- Resource Public Key Infrastructure for cryptographic validation
- Defenses against route hijacks

---
## Anycast

- Same IP advertised from many locations
- BGP routes to the closest
- Used by DNS roots, CDN PoPs, Google
- Fast failover when one location fails
- Foundation of geographic load balancing

---
## Equal-Cost Multi-Path

- Equal-Cost Multi-Path
- Multiple equal routes to same destination
- Hash-based load distribution
- Per-flow consistency typically
- Used in data centers heavily

---
## Cloud Routing Reality

- Cloud providers manage most routing
- VPC routes, transit gateways, peering
- Route tables per subnet
- Less BGP at the user level (mostly)
- More routing policy, less protocol

---
## Software-Defined Networking

- Centralized control plane
- Programmable forwarding
- OpenFlow, programmable RIBs, P4
- Cloud-native routing trends this way
- Traditional routing protocols still important

---
## Common Pitfalls

- Forgetting default route
- Asymmetric routing (going one way, returning another)
- BGP misconfig → leak prefixes globally
- Static routes left behind after migration
- Convergence storms after a major outage

---
## Routing Tools

- `ip route` (Linux), `route print` (Windows)
- `traceroute` / `mtr` for path
- `bird`, `frr`, `quagga` — open source routers
- BGP looking glasses (public)
- `bgpq3` for prefix lists from internet registries

---
## Asymmetric Routing

- Outbound and inbound paths differ
- Common in multi-homed setups
- Confuses stateful firewalls
- Source-IP routing helps
- Common cause of "works one way" issues

---
## Public-Key Route Authorization

- Resource Public Key Infrastructure
- Cryptographically signs prefix-AS bindings
- Validates BGP announcements
- Defends against hijacks (BGP leaks)
- Adoption growing; required by some peers

---
## Multi-Cloud Routing

- Pre-arranged peering or transit
- Direct Connect / ExpressRoute / Cloud Interconnect
- Carrier-managed routing
- IPsec VPNs as fallback
- Latency, cost, complexity all factor

---
## Common Operational Patterns

- Route aggregation reduces table size
- Communities express intent across hops
- Looking glasses for transparency
- Peering exchanges for performance
- ASN reservation per organization

---
## Summary

- Routing: each hop decides next hop based on prefix match
- Static for small/predictable; dynamic for everything else
- Link-state inside an autonomous system; BGP for inter-domain
- Cloud abstracts but doesn't eliminate routing
- Cryptographic validation raises the bar against hijacks
