# Azure Networking Services

## Core Networking Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_05_networking)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_05_networking)"/>
  <defs>
    <marker id="arrowd0_05_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Virtual Networks Overview
- Network isolation
- Subnet organization
- IP addressing
- Network security
- Connectivity options

---

## VNet Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_05_networking)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_05_networking)"/>
  <defs>
    <marker id="arrowd1_05_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## IP Addressing
- Address spaces
- Subnet ranges
- Public IPs
- Private IPs
- IPv4 and IPv6

---

## Subnet Planning
- Logical segmentation
- Address ranges
- Service requirements
- Future growth
- Subnet delegation

---

## Network Security Groups
- Security rules
- Inbound rules
- Outbound rules
- Priority ordering
- Default rules

---

## NSG Rule Components
1. Name
1. Priority
1. Source/Destination
1. Protocol
1. Port ranges
1. Action

---

## Application Security Groups
- Logical grouping
- Application-centric
- Simplified management
- Dynamic assignment
- Policy enforcement

---

## Azure Load Balancer
- Traffic distribution
- High availability
- Scale-out services
- Health probes
- Session persistence

---

## Load Balancer Types
- Public load balancer
- Internal load balancer
- Basic SKU
- Standard SKU
- Cross-zone balancing

---

## Application Gateway
- Web traffic routing
- SSL termination
- Cookie-based affinity
- URL-based routing
- WAF integration

---

## App Gateway Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_networking)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_networking)"/>
  <defs>
    <marker id="arrowd2_05_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Azure Firewall
- Managed service
- Network filtering
- Application rules
- Network rules
- Threat intelligence

---

## VPN Gateway
- Site-to-site VPN
- Point-to-site VPN
- VNet-to-VNet
- Multiple connections
- BGP routing

---

## ExpressRoute
- Private connectivity
- Layer 3 connectivity
- Global reach
- Multiple peerings
- High availability

---

## DNS Services
- Azure DNS
- Private DNS zones
- DNS resolution
- Custom domains
- Alias records

---

## Traffic Manager
- Global load balancing
- Routing methods
- Endpoint monitoring
- Nested profiles
- Performance routing

---

## Front Door
- Global load balancing
- SSL offload
- URL-based routing
- WAF protection
- Caching

---

## Network Watcher
- Connection monitor
- Packet capture
- Flow logs
- Diagnostic tools
- Troubleshooting

---

## DDoS Protection
- Always-on monitoring
- Adaptive tuning
- Attack metrics
- Attack analytics
- Cost protection

---

## Private Link
- Private endpoints
- Service connections
- Network isolation
- Cross-tenant access
- Global reach

---

## Service Endpoints
- Virtual network integration
- Direct connection
- Network isolation
- Optimized routing
- Service security

---

## Network Peering
- VNet peering
- Global VNet peering
- Transitive routing
- Gateway transit
- Cross-subscription

---

## Hybrid Connectivity

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_05_networking)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_05_networking)"/>
  <defs>
    <marker id="arrowd3_05_networking" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Network Security
- Defense in depth
- Zero trust
- Microsegmentation
- Access controls
- Monitoring

---

## Virtual WAN
- Global transit network
- Branch connectivity
- User VPN
- Traffic routing
- Security services

---

## Azure Bastion
- Secure RDP/SSH
- Browser-based
- No public IPs
- Integrated security
- Audit logging

---

## Network Monitoring
- Metrics
- Diagnostics
- Flow logs
- Network insights
- Alerting

---

## Performance Optimization
- Load balancing
- Traffic routing
- Caching
- Acceleration
- Scaling

---

## Cost Management
- Bandwidth pricing
- Service pricing
- Reserved instances
- Usage monitoring
- Optimization

---

## Disaster Recovery
- Geographic redundancy
- Failover options
- Business continuity
- Recovery testing
- Backup connectivity
