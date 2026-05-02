---
tags:
  - architecture:system-design
  - architecture:load-balancing
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Load Balancing

---
## What This Chapter Covers

- What load balancing is
- L4 vs L7
- Algorithms
- Health checks
- Sticky sessions
- Tools: HAProxy, nginx, ELB
- Common pitfalls

---
## What Load Balancing Is

- Distribute traffic across multiple servers
- Increase capacity beyond one server
- Survive server failures
- Smooth load
- Foundation of scalable systems

---
## Strategies Overview

![lb_strategies](svg/courses/architecting/system-design/03_load_balancing/lb_strategies.svg)

---
## Layer 4 (Transport)

- Operates on TCP / UDP
- Doesn't understand the application protocol
- Fast (less per-packet work)
- Examples: HAProxy in TCP mode, AWS NLB
- Use for: non-HTTP, performance-critical

---
## Layer 7 (Application)

- Understands HTTP, gRPC
- Can route by URL, header, cookie
- Can do TLS termination, compression
- Slower than L4, more flexible
- Examples: nginx, AWS ALB, Envoy

---
## Algorithms: Round Robin

- Each request goes to the next backend in turn
- Simple, fair when backends are equal
- Doesn't know which backend is busy
- Default in many tools

---
## Algorithms: Least Connections

- Pick the backend with the fewest active connections
- Better when request durations vary
- Slightly more state to track
- Common default in modern LBs

---
## Algorithms: Weighted

- Each backend has a weight; gets proportional traffic
- Use for: heterogeneous backends
- "Big server gets 2x the traffic of the small one"
- Mostly: prefer uniform fleets

---
## Algorithms: Hash-Based

- Hash a key (e.g., client IP); always route to same backend
- Sticky sessions without cookies
- Helps cache locality
- Drawback: rebalances when fleet changes

---
## Health Checks

- LB pings each backend periodically
- Unhealthy backends removed from pool
- Active checks: ping; passive: detect failures from real traffic
- Tune frequency: too often = chatty; too rare = slow recovery

---
## Sticky Sessions

- Same client always hits same backend
- Useful for: in-memory session, cache locality
- Risk: hot backend can't be relieved
- Better: stateless servers, cookie-based session in DB

---
## Tools: nginx

- Versatile L7 LB
- HTTP, gRPC, WebSocket support
- Lua scripting
- Free, ubiquitous
- The default for many setups

---
## Tools: HAProxy

- Strong L4 + L7 LB
- Very mature, very fast
- Excellent observability
- Used at scale (Stripe, GitHub)

---
## Tools: Cloud LBs

- AWS ALB, NLB, Classic LB
- GCP Load Balancing
- Azure Load Balancer
- Managed, integrated with other cloud services
- Pay per request + per hour

---
## DNS Load Balancing

- Multiple A records for one domain
- Client picks (or fails over)
- Cross-region traffic distribution
- TTL matters: low for fast failover; high for caching
- Often: DNS at the global tier; LB at the regional tier

---
## Common LB Mistakes

- One LB, single point of failure
- No health checks
- Sticky sessions without need
- Same algorithm for all services
- Forgetting to drain connections during deploy
