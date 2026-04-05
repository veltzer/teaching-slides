# Azure Networking Services

## Core Networking Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Core Azure Networking Components</text>
  <rect x="10" y="30" width="130" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="50" text-anchor="middle" font-size="11" font-weight="bold">VNet</text>
  <text x="75" y="65" text-anchor="middle" font-size="10">Network isolation</text>
  <text x="75" y="80" text-anchor="middle" font-size="10">Address spaces</text>
  <rect x="160" y="30" width="130" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="50" text-anchor="middle" font-size="11" font-weight="bold">Subnets</text>
  <text x="225" y="65" text-anchor="middle" font-size="10">Segmentation</text>
  <text x="225" y="80" text-anchor="middle" font-size="10">IP ranges</text>
  <rect x="310" y="30" width="130" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="50" text-anchor="middle" font-size="11" font-weight="bold">NSG</text>
  <text x="375" y="65" text-anchor="middle" font-size="10">Security rules</text>
  <text x="375" y="80" text-anchor="middle" font-size="10">Allow/Deny traffic</text>
  <rect x="460" y="30" width="130" height="65" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="50" text-anchor="middle" font-size="11" font-weight="bold">Load Balancer</text>
  <text x="525" y="65" text-anchor="middle" font-size="10">L4 distribution</text>
  <text x="525" y="80" text-anchor="middle" font-size="10">Health probes</text>
  <rect x="10" y="115" width="130" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="135" text-anchor="middle" font-size="11" font-weight="bold">App Gateway</text>
  <text x="75" y="150" text-anchor="middle" font-size="10">L7 routing</text>
  <text x="75" y="165" text-anchor="middle" font-size="10">WAF, SSL</text>
  <rect x="160" y="115" width="130" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="135" text-anchor="middle" font-size="11" font-weight="bold">VPN Gateway</text>
  <text x="225" y="150" text-anchor="middle" font-size="10">Encrypted tunnel</text>
  <text x="225" y="165" text-anchor="middle" font-size="10">Hybrid connect</text>
  <rect x="310" y="115" width="130" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="135" text-anchor="middle" font-size="11" font-weight="bold">Azure DNS</text>
  <text x="375" y="150" text-anchor="middle" font-size="10">Name resolution</text>
  <text x="375" y="165" text-anchor="middle" font-size="10">Custom domains</text>
  <rect x="460" y="115" width="130" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="135" text-anchor="middle" font-size="11" font-weight="bold">Azure Firewall</text>
  <text x="525" y="150" text-anchor="middle" font-size="10">Managed FW</text>
  <text x="525" y="165" text-anchor="middle" font-size="10">Threat intel</text>
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
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">VNet with Subnets and NSGs</text>
  <rect x="20" y="22" width="560" height="170" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="40" text-anchor="middle" font-size="11" font-weight="bold">VNet: 10.0.0.0/16</text>
  <rect x="35" y="50" width="160" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="115" y="68" text-anchor="middle" font-size="10" font-weight="bold">Web Subnet</text>
  <text x="115" y="82" text-anchor="middle" font-size="10">10.0.1.0/24</text>
  <rect x="50" y="93" width="50" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="75" y="105" text-anchor="middle" font-size="9">VM1</text>
  <rect x="110" y="93" width="50" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="135" y="105" text-anchor="middle" font-size="9">VM2</text>
  <rect x="220" y="50" width="160" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="68" text-anchor="middle" font-size="10" font-weight="bold">App Subnet</text>
  <text x="300" y="82" text-anchor="middle" font-size="10">10.0.2.0/24</text>
  <rect x="240" y="93" width="55" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="267" y="105" text-anchor="middle" font-size="9">AppSvc</text>
  <rect x="305" y="93" width="55" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="332" y="105" text-anchor="middle" font-size="9">API</text>
  <rect x="405" y="50" width="160" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="68" text-anchor="middle" font-size="10" font-weight="bold">DB Subnet</text>
  <text x="485" y="82" text-anchor="middle" font-size="10">10.0.3.0/24</text>
  <rect x="435" y="93" width="50" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="460" y="105" text-anchor="middle" font-size="9">SQL</text>
  <rect x="495" y="93" width="55" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="522" y="105" text-anchor="middle" font-size="9">Redis</text>
  <rect x="35" y="130" width="160" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="115" y="147" text-anchor="middle" font-size="10">NSG: Allow 80,443</text>
  <rect x="220" y="130" width="160" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="147" text-anchor="middle" font-size="10">NSG: Allow from Web</text>
  <rect x="405" y="130" width="160" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="485" y="147" text-anchor="middle" font-size="10">NSG: Allow from App</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#555">Traffic flows: Internet -> Web -> App -> DB (controlled by NSGs)</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Application Gateway Components</text>
  <rect x="10" y="30" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="50" text-anchor="middle" font-size="10" font-weight="bold">Client</text>
  <text x="60" y="65" text-anchor="middle" font-size="10">HTTPS</text>
  <line x1="110" y1="55" x2="140" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_networking)"/>
  <rect x="140" y="25" width="130" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="45" text-anchor="middle" font-size="10" font-weight="bold">Frontend</text>
  <text x="205" y="58" text-anchor="middle" font-size="10">Public/Private IP</text>
  <text x="205" y="72" text-anchor="middle" font-size="10">SSL Termination</text>
  <line x1="270" y1="55" x2="300" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_05_networking)"/>
  <rect x="300" y="25" width="130" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="365" y="45" text-anchor="middle" font-size="10" font-weight="bold">Routing Rules</text>
  <text x="365" y="58" text-anchor="middle" font-size="10">URL-based</text>
  <text x="365" y="72" text-anchor="middle" font-size="10">Path-based</text>
  <line x1="430" y1="55" x2="460" y2="45" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_05_networking)"/>
  <line x1="430" y1="55" x2="460" y2="75" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_05_networking)"/>
  <rect x="460" y="25" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="525" y="45" text-anchor="middle" font-size="10">Backend Pool A</text>
  <rect x="460" y="60" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="525" y="80" text-anchor="middle" font-size="10">Backend Pool B</text>
  <rect x="100" y="105" width="400" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="122" text-anchor="middle" font-size="10" font-weight="bold">Web Application Firewall (WAF)</text>
  <text x="300" y="137" text-anchor="middle" font-size="10">OWASP rules | Bot protection | Custom rules | Geo-filtering</text>
  <rect x="100" y="155" width="400" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="172" text-anchor="middle" font-size="10" font-weight="bold">Health Probes: Monitor backend availability and auto-failover</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Hybrid Connectivity Options</text>
  <rect x="10" y="35" width="150" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="55" text-anchor="middle" font-size="11" font-weight="bold">On-Premises</text>
  <text x="85" y="70" text-anchor="middle" font-size="10">Data Center</text>
  <text x="85" y="85" text-anchor="middle" font-size="10">VPN Device</text>
  <text x="85" y="98" text-anchor="middle" font-size="10">Local network</text>
  <rect x="430" y="35" width="160" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="55" text-anchor="middle" font-size="11" font-weight="bold">Azure VNet</text>
  <text x="510" y="70" text-anchor="middle" font-size="10">Cloud resources</text>
  <text x="510" y="85" text-anchor="middle" font-size="10">VPN Gateway</text>
  <text x="510" y="98" text-anchor="middle" font-size="10">VMs, Services</text>
  <rect x="190" y="30" width="210" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="52" text-anchor="middle" font-size="10" font-weight="bold">Site-to-Site VPN (IPsec)</text>
  <line x1="160" y1="48" x2="190" y2="48" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_05_networking)"/>
  <line x1="400" y1="48" x2="430" y2="48" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_05_networking)"/>
  <rect x="190" y="75" width="210" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="97" text-anchor="middle" font-size="10" font-weight="bold">ExpressRoute (Private)</text>
  <line x1="160" y1="93" x2="190" y2="93" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="93" x2="430" y2="93" stroke="#333" stroke-width="2"/>
  <rect x="60" y="130" width="220" height="55" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="170" y="148" text-anchor="middle" font-size="10" font-weight="bold">VPN: Encrypted over internet</text>
  <text x="170" y="163" text-anchor="middle" font-size="10">Up to 10 Gbps</text>
  <text x="170" y="178" text-anchor="middle" font-size="10">Lower cost, quick setup</text>
  <rect x="320" y="130" width="230" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="435" y="148" text-anchor="middle" font-size="10" font-weight="bold">ExpressRoute: Dedicated link</text>
  <text x="435" y="163" text-anchor="middle" font-size="10">Up to 100 Gbps</text>
  <text x="435" y="178" text-anchor="middle" font-size="10">Higher reliability, lower latency</text>
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
