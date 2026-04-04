# Introduction to Cloud Computing

## What is Cloud Computing?
- Computing services over internet
- On-demand resources
- Pay-as-you-go model
- Scalable infrastructure
- Managed services

---

## Evolution of Computing

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="120" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="90" text-anchor="middle" font-size="11" font-weight="bold">Mainframes</text>
  <text x="80" y="105" text-anchor="middle" font-size="10">1960s-1970s</text>
  <text x="80" y="120" text-anchor="middle" font-size="10">Centralized</text>
  <rect x="185" y="60" width="120" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="245" y="90" text-anchor="middle" font-size="11" font-weight="bold">Client-Server</text>
  <text x="245" y="105" text-anchor="middle" font-size="10">1980s-1990s</text>
  <text x="245" y="120" text-anchor="middle" font-size="10">Distributed</text>
  <rect x="350" y="60" width="120" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="90" text-anchor="middle" font-size="11" font-weight="bold">Virtualization</text>
  <text x="410" y="105" text-anchor="middle" font-size="10">2000s</text>
  <text x="410" y="120" text-anchor="middle" font-size="10">Abstracted</text>
  <rect x="490" y="60" width="95" height="80" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="537" y="90" text-anchor="middle" font-size="11" font-weight="bold">Cloud</text>
  <text x="537" y="105" text-anchor="middle" font-size="10">2010s+</text>
  <text x="537" y="120" text-anchor="middle" font-size="10">On-Demand</text>
  <line x1="140" y1="100" x2="185" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_00_cloud_intro)"/>
  <line x1="305" y1="100" x2="350" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_00_cloud_intro)"/>
  <line x1="470" y1="100" x2="490" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_00_cloud_intro)"/>
  <defs>
    <marker id="arrowd0_00_cloud_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Key Characteristics
- Self-service provisioning
- Resource pooling
- Rapid elasticity
- Measured service
- Broad network access

---

## Cloud Service Models

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="180" height="160" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="42" text-anchor="middle" font-size="12" font-weight="bold">IaaS</text>
  <text x="100" y="58" text-anchor="middle" font-size="10">You manage:</text>
  <text x="100" y="73" text-anchor="middle" font-size="10">Apps, Data, Runtime</text>
  <text x="100" y="88" text-anchor="middle" font-size="10">OS, Middleware</text>
  <rect x="30" y="100" width="140" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="100" y="120" text-anchor="middle" font-size="10">Provider: VMs, Network</text>
  <rect x="30" y="138" width="140" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="100" y="158" text-anchor="middle" font-size="10">Provider: Storage, HW</text>
  <rect x="210" y="20" width="180" height="160" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="12" font-weight="bold">PaaS</text>
  <text x="300" y="58" text-anchor="middle" font-size="10">You manage:</text>
  <text x="300" y="73" text-anchor="middle" font-size="10">Apps, Data</text>
  <rect x="230" y="82" width="140" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="102" text-anchor="middle" font-size="10">Provider: Runtime, OS</text>
  <rect x="230" y="120" width="140" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="140" text-anchor="middle" font-size="10">Provider: Middleware</text>
  <rect x="230" y="150" width="140" height="22" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="165" text-anchor="middle" font-size="9">Provider: Infra</text>
  <rect x="410" y="20" width="180" height="160" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="42" text-anchor="middle" font-size="12" font-weight="bold">SaaS</text>
  <text x="500" y="58" text-anchor="middle" font-size="10">You manage:</text>
  <text x="500" y="73" text-anchor="middle" font-size="10">Configuration only</text>
  <rect x="430" y="82" width="140" height="90" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="500" y="110" text-anchor="middle" font-size="10">Provider manages</text>
  <text x="500" y="125" text-anchor="middle" font-size="10">everything:</text>
  <text x="500" y="140" text-anchor="middle" font-size="10">Apps to Hardware</text>
</svg>

---

## Infrastructure as a Service
- Virtual machines
- Storage
- Networks
- Maximum control
- Hardware abstraction

---

## Platform as a Service
- Development platforms
- Middleware
- Tools and services
- Reduced complexity
- Focus on applications

---

## Software as a Service
- Ready-to-use applications
- Web-based access
- Subscription model
- Automatic updates
- Minimal management

---

## Service Model Comparison
1. Management scope
1. Control level
1. Flexibility
1. Responsibility
1. Use cases

---

## Cloud Deployment Models
- Public cloud
- Private cloud
- Hybrid cloud
- Multi-cloud
- Community cloud

---

## Public Cloud
- Available to everyone
- Third-party provider
- Shared infrastructure
- Pay-as-you-go
- Global scale

---

## Private Cloud
- Single organization
- Dedicated resources
- Enhanced control
- Customization
- Compliance focus

---

## Hybrid Cloud
- Public + Private
- Workload flexibility
- Data sovereignty
- Cost optimization
- Risk management

---

## Multi-Cloud Strategy
- Multiple providers
- Service selection
- Risk mitigation
- Cost optimization
- Vendor independence

---

## Cloud Benefits

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="160" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="55" text-anchor="middle" font-size="12" font-weight="bold">Cost Savings</text>
  <text x="100" y="72" text-anchor="middle" font-size="10">No upfront CapEx</text>
  <rect x="220" y="30" width="160" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="12" font-weight="bold">Scalability</text>
  <text x="300" y="72" text-anchor="middle" font-size="10">Scale up/out on demand</text>
  <rect x="420" y="30" width="160" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="55" text-anchor="middle" font-size="12" font-weight="bold">Global Reach</text>
  <text x="500" y="72" text-anchor="middle" font-size="10">Deploy worldwide</text>
  <rect x="120" y="115" width="160" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="200" y="140" text-anchor="middle" font-size="12" font-weight="bold">Reliability</text>
  <text x="200" y="157" text-anchor="middle" font-size="10">Built-in redundancy</text>
  <rect x="320" y="115" width="160" height="60" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="140" text-anchor="middle" font-size="12" font-weight="bold">Security</text>
  <text x="400" y="157" text-anchor="middle" font-size="10">Advanced protection</text>
  <ellipse cx="300" cy="100" rx="280" ry="90" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
</svg>

---

## Cost Benefits
- Operational efficiency
- Capital expense reduction
- Pay-per-use model
- Reduced maintenance
- Resource optimization

---

## Scalability and Elasticity
- Vertical scaling
- Horizontal scaling
- Auto-scaling
- Load balancing
- Resource optimization

---

## Agility and Innovation
- Rapid deployment
- Quick experimentation
- Service integration
- Latest technologies
- Competitive advantage

---

## Global Reach
- Multiple regions
- Edge locations
- Content delivery
- Local presence
- Global redundancy

---

## Security in the Cloud
- Shared responsibility
- Advanced protection
- Compliance standards
- Regular updates
- Security tools

---

## Performance Considerations
- Network latency
- Resource allocation
- Service levels
- Monitoring
- Optimization

---

## Compliance and Governance
- Data sovereignty
- Industry standards
- Regulatory requirements
- Audit capabilities
- Policy enforcement

---

## Cost Management
- Resource tracking
- Budget planning
- Cost optimization
- Usage monitoring
- Chargeback models

---

## Migration Strategies
- Rehost (lift-and-shift)
- Refactor
- Rearchitect
- Rebuild
- Replace

---

## Cloud Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="180" y="10" width="240" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="12" font-weight="bold">Presentation Tier (CDN/Web)</text>
  <rect x="180" y="65" width="240" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="90" text-anchor="middle" font-size="12" font-weight="bold">Application Tier (APIs/Logic)</text>
  <rect x="180" y="120" width="240" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="145" text-anchor="middle" font-size="12" font-weight="bold">Data Tier (DB/Storage)</text>
  <rect x="10" y="40" width="130" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="75" y="65" text-anchor="middle" font-size="10" font-weight="bold">Users</text>
  <text x="75" y="80" text-anchor="middle" font-size="10">Web/Mobile</text>
  <rect x="460" y="40" width="130" height="60" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="525" y="65" text-anchor="middle" font-size="10" font-weight="bold">Security</text>
  <text x="525" y="80" text-anchor="middle" font-size="10">IAM / Firewall</text>
  <rect x="460" y="120" width="130" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="525" y="145" text-anchor="middle" font-size="10" font-weight="bold">Monitoring</text>
  <line x1="140" y1="70" x2="180" y2="30" stroke="#333" stroke-width="1" marker-end="url(#arrowd3_00_cloud_intro)"/>
  <line x1="300" y1="50" x2="300" y2="65" stroke="#333" stroke-width="1" marker-end="url(#arrowd3_00_cloud_intro)"/>
  <line x1="300" y1="105" x2="300" y2="120" stroke="#333" stroke-width="1" marker-end="url(#arrowd3_00_cloud_intro)"/>
  <text x="300" y="185" text-anchor="middle" font-size="11" fill="#555">Three-tier cloud architecture pattern</text>
  <defs>
    <marker id="arrowd3_00_cloud_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Best Practices
- Design principles
- Security measures
- Cost optimization
- Performance tuning
- Disaster recovery

---

## Future Trends
- Edge computing
- Serverless
- AI/ML integration
- IoT expansion
- Sustainable computing

---

## Industry Impact
- Digital transformation
- Business models
- Innovation speed
- Market competition
- Service delivery

---

## Getting Started
- Assessment
- Strategy development
- Provider selection
- Pilot projects
- Implementation plan

---

## Cloud Skills
- Technical expertise
- Architecture design
- Security knowledge
- Cost management
- Operations
