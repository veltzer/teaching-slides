# Introduction to Microsoft Azure

## What is Azure?
- Microsoft's cloud platform
- Global infrastructure
- Integrated services
- Enterprise scale
- Continuous innovation

---

## Azure History

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <!-- Timeline axis -->
  <line x1="30" y1="80" x2="570" y2="80" stroke="#0078d4" stroke-width="2"/>
  <!-- 2008 -->
  <circle cx="60" cy="80" r="6" fill="#0078d4"/>
  <text x="60" y="68" text-anchor="middle" font-size="10" font-weight="bold" fill="#0078d4">2008</text>
  <text x="60" y="102" text-anchor="middle" font-size="9" fill="#333">Announced</text>
  <!-- 2010 -->
  <circle cx="180" cy="80" r="6" fill="#0078d4"/>
  <text x="180" y="68" text-anchor="middle" font-size="10" font-weight="bold" fill="#0078d4">2010</text>
  <text x="180" y="102" text-anchor="middle" font-size="9" fill="#333">GA Launch</text>
  <!-- 2014 -->
  <circle cx="300" cy="80" r="6" fill="#0078d4"/>
  <text x="300" y="68" text-anchor="middle" font-size="10" font-weight="bold" fill="#0078d4">2014</text>
  <text x="300" y="102" text-anchor="middle" font-size="9" fill="#333">Renamed Azure</text>
  <!-- 2017 -->
  <circle cx="420" cy="80" r="6" fill="#0078d4"/>
  <text x="420" y="68" text-anchor="middle" font-size="10" font-weight="bold" fill="#0078d4">2017</text>
  <text x="420" y="102" text-anchor="middle" font-size="9" fill="#333">60+ Regions</text>
  <!-- 2023 -->
  <circle cx="540" cy="80" r="6" fill="#0078d4"/>
  <text x="540" y="68" text-anchor="middle" font-size="10" font-weight="bold" fill="#0078d4">2023</text>
  <text x="540" y="102" text-anchor="middle" font-size="9" fill="#333">AI &amp; Copilot</text>
</svg>

---

## Global Infrastructure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="280" ry="90" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="300" y="20" text-anchor="middle" font-size="11" fill="#555">60+ Azure Regions Worldwide</text>
  <rect x="30" y="40" width="110" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="60" text-anchor="middle" font-size="11" font-weight="bold">Americas</text>
  <text x="85" y="75" text-anchor="middle" font-size="10">East US, West US</text>
  <text x="85" y="88" text-anchor="middle" font-size="10">Brazil, Canada</text>
  <rect x="170" y="55" width="110" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="75" text-anchor="middle" font-size="11" font-weight="bold">Europe</text>
  <text x="225" y="90" text-anchor="middle" font-size="10">West Europe, UK</text>
  <text x="225" y="103" text-anchor="middle" font-size="10">France, Germany</text>
  <rect x="320" y="55" width="110" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="75" text-anchor="middle" font-size="11" font-weight="bold">Asia Pacific</text>
  <text x="375" y="90" text-anchor="middle" font-size="10">Japan, Australia</text>
  <text x="375" y="103" text-anchor="middle" font-size="10">India, Korea</text>
  <rect x="460" y="40" width="110" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="60" text-anchor="middle" font-size="11" font-weight="bold">Middle East</text>
  <text x="515" y="75" text-anchor="middle" font-size="10">UAE, Qatar</text>
  <text x="515" y="88" text-anchor="middle" font-size="10">South Africa</text>
  <rect x="170" y="130" width="260" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="150" text-anchor="middle" font-size="11" font-weight="bold">Availability Zones per Region</text>
  <text x="300" y="168" text-anchor="middle" font-size="10">3+ independent data centers with isolated power, cooling, networking</text>
</svg>

---

## Azure Regions
- Geographic areas
- Multiple data centers
- Data residency
- Service availability
- Performance optimization

---

## Availability Zones
- Physical separation
- Independent power
- Networking
- Cooling
- High availability

---

## Core Azure Services
1. Compute
1. Storage
1. Networking
1. Databases
1. AI/ML

---

## Service Categories

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="200" height="35" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="27" text-anchor="middle" font-size="12" font-weight="bold">Management Groups</text>
  <line x1="300" y1="40" x2="300" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_01_azure_intro)"/>
  <rect x="200" y="50" width="200" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="72" text-anchor="middle" font-size="12" font-weight="bold">Subscriptions</text>
  <line x1="250" y1="85" x2="150" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_01_azure_intro)"/>
  <line x1="350" y1="85" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_01_azure_intro)"/>
  <rect x="50" y="100" width="190" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="145" y="122" text-anchor="middle" font-size="12" font-weight="bold">Resource Group A</text>
  <rect x="360" y="100" width="190" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="455" y="122" text-anchor="middle" font-size="12" font-weight="bold">Resource Group B</text>
  <line x1="95" y1="135" x2="65" y2="150" stroke="#333" stroke-width="1"/>
  <line x1="145" y1="135" x2="145" y2="150" stroke="#333" stroke-width="1"/>
  <line x1="195" y1="135" x2="225" y2="150" stroke="#333" stroke-width="1"/>
  <rect x="20" y="150" width="80" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="60" y="172" text-anchor="middle" font-size="10">VM</text>
  <rect x="110" y="150" width="80" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="172" text-anchor="middle" font-size="10">Storage</text>
  <rect x="200" y="150" width="80" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="240" y="172" text-anchor="middle" font-size="10">SQL DB</text>
  <line x1="405" y1="135" x2="385" y2="150" stroke="#333" stroke-width="1"/>
  <line x1="505" y1="135" x2="505" y2="150" stroke="#333" stroke-width="1"/>
  <rect x="340" y="150" width="80" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="380" y="172" text-anchor="middle" font-size="10">App Svc</text>
  <rect x="460" y="150" width="80" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="500" y="172" text-anchor="middle" font-size="10">Functions</text>
  <defs>
    <marker id="arrowd2_01_azure_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Management Structure
- Management groups
- Subscriptions
- Resource groups
- Resources
- Organization

---

## Azure Subscriptions
- Billing boundary
- Access control
- Resource limits
- Environment isolation
- Cost management

---

## Resource Groups
- Logical containers
- Resource organization
- Access control
- Policy application
- Lifecycle management

---

## Azure Resource Manager
- Deployment control
- Access management
- Resource organization
- Template-based deployment
- Consistent management

---

## Identity Services
- Azure Active Directory
- Single sign-on
- Multi-factor auth
- Conditional access
- Identity protection

---

## Security Features
- Network security
- Data protection
- Identity management
- Threat protection
- Compliance tools

---

## Monitoring Tools
- Azure Monitor
- Application Insights
- Log Analytics
- Alerts
- Dashboards

---

## Cost Management
- Pricing calculator
- Cost analysis
- Budgets
- Recommendations
- Optimization

---

## Support Options
- Basic
- Developer
- Standard
- Professional
- Premier

---

## Azure Service Levels
- Free services
- Basic services
- Standard services
- Premium services
- Custom solutions

---

## Compliance Standards
- Industry compliance
- Regional standards
- Security certifications
- Audit reports
- Documentation

---

## Azure Marketplace
- Pre-built solutions
- Third-party services
- Templates
- Consulting services
- Integration tools

---

## Development Tools
- Visual Studio
- VS Code
- SDKs
- Azure DevOps
- GitHub integration

---

## Azure CLI and PowerShell
- Command-line tools
- Automation
- Scripting
- Resource management
- Configuration

---

## Integration Services
- Logic Apps
- Service Bus
- Event Grid
- API Management
- Functions

---

## Azure Solutions
- Web applications
- Mobile backends
- IoT solutions
- AI/ML services
- Analytics platforms

---

## Industry Solutions
- Healthcare
- Financial services
- Manufacturing
- Retail
- Government

---

## Partner Ecosystem
- Solution providers
- Managed services
- System integrators
- Training partners
- Consultants

---

## Getting Started
- Free account
- Learning resources
- Documentation
- Training paths
- Certifications

---

## Best Practices
- Architecture design
- Security implementation
- Cost optimization
- Performance tuning
- Operational excellence

---

## Future Roadmap
- Service evolution
- New features
- Industry focus
- Innovation areas
- Strategic direction

---

## Success Stories
- Enterprise adoption
- Digital transformation
- Innovation examples
- Business outcomes
- Learning lessons

---

## Next Steps
- Account creation
- Service exploration
- Skills development
- Implementation planning
- Resource allocation
