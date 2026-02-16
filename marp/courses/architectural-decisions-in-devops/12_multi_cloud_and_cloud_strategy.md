# Multi-Cloud and Cloud Strategy
---
## Why Cloud Strategy Matters

- Cloud is no longer "if" but "how"
- Choosing a strategy impacts cost, agility, and resilience
- Wrong decisions create years of technical debt
- Strategy must align with business goals, compliance, and team skills
- No single approach fits all organizations
---
## Cloud Deployment Models Overview

<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="40" width="220" height="240" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="130" y="30" text-anchor="middle" font-weight="bold" font-size="14" fill="#1565c0">Single Cloud</text>
  <rect x="50" y="70" width="160" height="50" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="130" y="100" text-anchor="middle" font-size="12">All workloads</text>
  <rect x="50" y="140" width="160" height="50" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="130" y="170" text-anchor="middle" font-size="12">One provider</text>
  <rect x="50" y="210" width="160" height="50" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="130" y="240" text-anchor="middle" font-size="12">Native services</text>
  <rect x="290" y="40" width="220" height="240" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-weight="bold" font-size="14" fill="#2e7d32">Multi-Cloud</text>
  <rect x="320" y="70" width="160" height="50" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="400" y="100" text-anchor="middle" font-size="12">Split workloads</text>
  <rect x="320" y="140" width="160" height="50" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="400" y="170" text-anchor="middle" font-size="12">Multiple providers</text>
  <rect x="320" y="210" width="160" height="50" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="400" y="240" text-anchor="middle" font-size="12">Abstraction layers</text>
  <rect x="560" y="40" width="220" height="240" rx="12" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="670" y="30" text-anchor="middle" font-weight="bold" font-size="14" fill="#e65100">Hybrid Cloud</text>
  <rect x="590" y="70" width="160" height="50" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="670" y="100" text-anchor="middle" font-size="12">On-prem + cloud</text>
  <rect x="590" y="140" width="160" height="50" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="670" y="170" text-anchor="middle" font-size="12">Connected fabric</text>
  <rect x="590" y="210" width="160" height="50" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="670" y="240" text-anchor="middle" font-size="12">Data locality</text>
</svg>

---
## Single Cloud Strategy

- All infrastructure and services on one cloud provider
- Examples: all-in on `AWS`, `Azure`, or `GCP`
- Deepest access to cloud-native features
- Single billing relationship and volume discounts
- Unified IAM, networking, and monitoring
- Smaller operations team needed
---
## Single Cloud Risks

- Complete dependency on one vendor
- Pricing changes impact entire infrastructure
- Outages affect all workloads simultaneously
- Negotiating leverage decreases over time
- Migration cost grows exponentially with adoption depth
---
## Multi-Cloud Strategy

- Workloads distributed across two or more cloud providers
- Different providers for different workloads (polyglot cloud)
- Same workload portable across providers (true multi-cloud)
- Requires abstraction layers or duplicated expertise
- Growing trend among enterprises
---
## Multi-Cloud Topology

<svg viewBox="0 0 800 360" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="10" width="300" height="60" rx="10" fill="#e1bee7" stroke="#6a1b9a" stroke-width="2"/>
  <text x="400" y="45" text-anchor="middle" font-weight="bold" font-size="14" fill="#6a1b9a">Orchestration / Abstraction Layer</text>
  <line x1="200" y1="70" x2="200" y2="130" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <line x1="400" y1="70" x2="400" y2="130" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <line x1="600" y1="70" x2="600" y2="130" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <rect x="80" y="130" width="240" height="100" rx="10" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="200" y="165" text-anchor="middle" font-weight="bold" font-size="13" fill="#e65100">AWS</text>
  <text x="200" y="190" text-anchor="middle" font-size="11">EKS, RDS, S3</text>
  <text x="200" y="210" text-anchor="middle" font-size="11">Compute workloads</text>
  <rect x="350" y="130" width="240" height="100" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="470" y="165" text-anchor="middle" font-weight="bold" font-size="13" fill="#1565c0">Azure</text>
  <text x="470" y="190" text-anchor="middle" font-size="11">AKS, SQL DB, Blob</text>
  <text x="470" y="210" text-anchor="middle" font-size="11">Enterprise / AD</text>
  <rect x="520" y="130" width="240" height="100" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="640" y="165" text-anchor="middle" font-weight="bold" font-size="13" fill="#2e7d32">GCP</text>
  <text x="640" y="190" text-anchor="middle" font-size="11">GKE, BigQuery, GCS</text>
  <text x="640" y="210" text-anchor="middle" font-size="11">ML / Analytics</text>
  <rect x="150" y="280" width="500" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="1.5"/>
  <text x="400" y="315" text-anchor="middle" font-size="13" fill="#6a1b9a">Unified Monitoring, Logging, and Security</text>
  <line x1="200" y1="230" x2="300" y2="280" stroke="#999" stroke-width="1.5"/>
  <line x1="470" y1="230" x2="400" y2="280" stroke="#999" stroke-width="1.5"/>
  <line x1="640" y1="230" x2="500" y2="280" stroke="#999" stroke-width="1.5"/>
</svg>

---
## Hybrid Cloud Strategy

<svg viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="50" width="300" height="250" rx="12" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="180" y="40" text-anchor="middle" font-weight="bold" font-size="14" fill="#c62828">On-Premises Data Center</text>
  <rect x="60" y="80" width="110" height="45" rx="6" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="115" y="107" text-anchor="middle" font-size="11">VMware / KVM</text>
  <rect x="190" y="80" width="110" height="45" rx="6" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="245" y="107" text-anchor="middle" font-size="11">Databases</text>
  <rect x="60" y="150" width="110" height="45" rx="6" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="115" y="177" text-anchor="middle" font-size="11">Active Directory</text>
  <rect x="190" y="150" width="110" height="45" rx="6" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="245" y="177" text-anchor="middle" font-size="11">Legacy Apps</text>
  <rect x="100" y="220" width="160" height="45" rx="6" fill="#ef9a9a" stroke="#c62828" stroke-width="1.5"/>
  <text x="180" y="247" text-anchor="middle" font-size="11" font-weight="bold">Sensitive Data</text>
  <rect x="370" y="100" width="80" height="140" rx="8" fill="#e0e0e0" stroke="#666" stroke-width="2"/>
  <text x="410" y="155" text-anchor="middle" font-size="10" fill="#333">VPN /</text>
  <text x="410" y="170" text-anchor="middle" font-size="10" fill="#333">Direct</text>
  <text x="410" y="185" text-anchor="middle" font-size="10" fill="#333">Connect</text>
  <line x1="330" y1="170" x2="370" y2="170" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="450" y1="170" x2="490" y2="170" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#666"/></marker></defs>
  <rect x="490" y="50" width="280" height="250" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="630" y="40" text-anchor="middle" font-weight="bold" font-size="14" fill="#1565c0">Public Cloud</text>
  <rect x="520" y="80" width="110" height="45" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="575" y="107" text-anchor="middle" font-size="11">Kubernetes</text>
  <rect x="640" y="80" width="110" height="45" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="695" y="107" text-anchor="middle" font-size="11">Serverless</text>
  <rect x="520" y="150" width="110" height="45" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="575" y="177" text-anchor="middle" font-size="11">CDN / Edge</text>
  <rect x="640" y="150" width="110" height="45" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="695" y="177" text-anchor="middle" font-size="11">ML Services</text>
  <rect x="560" y="220" width="160" height="45" rx="6" fill="#90caf9" stroke="#1565c0" stroke-width="1.5"/>
  <text x="640" y="247" text-anchor="middle" font-size="11" font-weight="bold">Burst Capacity</text>
</svg>

---
## Comparing the Three Approaches

| Aspect | Single Cloud | Multi-Cloud | Hybrid |
|--------|-------------|-------------|--------|
| Complexity | Low | High | Medium |
| Vendor lock-in | High | Low | Medium |
| Cost optimization | Good | Best potential | Variable |
| Team skills | Focused | Broad | Mixed |
| Compliance | Provider-dependent | Flexible | Strong |
---
## Vendor Lock-in: What It Really Means

- Lock-in is not just about compute instances
- The real lock-in comes from:
    - Managed databases (`DynamoDB`, `Cosmos DB`, `Spanner`)
    - Serverless platforms (`Lambda`, `Cloud Functions`)
    - Identity and access management (`IAM` policies)
    - Proprietary APIs and SDKs
    - Data egress costs making migration expensive
---
## The Lock-in Spectrum

<svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="lockgrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4caf50"/>
      <stop offset="50%" style="stop-color:#ff9800"/>
      <stop offset="100%" style="stop-color:#f44336"/>
    </linearGradient>
  </defs>
  <rect x="50" y="80" width="700" height="30" rx="15" fill="url(#lockgrad)"/>
  <text x="50" y="60" font-size="12" fill="#333">Low Lock-in</text>
  <text x="680" y="60" font-size="12" fill="#333">High Lock-in</text>
  <line x1="120" y1="110" x2="120" y2="140" stroke="#333" stroke-width="2"/>
  <text x="120" y="160" text-anchor="middle" font-size="11" fill="#333">VMs / IaaS</text>
  <line x1="250" y1="110" x2="250" y2="140" stroke="#333" stroke-width="2"/>
  <text x="250" y="160" text-anchor="middle" font-size="11" fill="#333">Kubernetes</text>
  <line x1="400" y1="110" x2="400" y2="140" stroke="#333" stroke-width="2"/>
  <text x="400" y="160" text-anchor="middle" font-size="11" fill="#333">Managed DB</text>
  <line x1="550" y1="110" x2="550" y2="140" stroke="#333" stroke-width="2"/>
  <text x="550" y="160" text-anchor="middle" font-size="11" fill="#333">Serverless</text>
  <line x1="680" y1="110" x2="680" y2="140" stroke="#333" stroke-width="2"/>
  <text x="680" y="160" text-anchor="middle" font-size="11" fill="#333">Proprietary AI/ML</text>
</svg>

---
## Embracing Cloud-Native Services

- Cloud-native services offer significant advantages:
    - Reduced operational burden (no patching, scaling, backups)
    - Better performance through provider optimization
    - Faster time-to-market
    - Built-in high availability
- Using `RDS` instead of self-managed `PostgreSQL` saves ops time
- Using `SQS` instead of self-managed `RabbitMQ` eliminates cluster management
---
## The Cost of Not Going Cloud-Native

- Running `Kubernetes` + `PostgreSQL` + `Kafka` yourself means:
    - Hiring and retaining specialized staff
    - Handling upgrades, patches, and security fixes
    - Managing backups and disaster recovery
    - 24/7 on-call rotation
- Estimate: 2-5 full-time engineers per major self-managed service
- The "portable" choice can be the more expensive choice
---
## When to Embrace or Avoid Lock-in

- Embrace lock-in when:
    - Organization is too small for multi-vendor negotiations
    - Time-to-market is the primary constraint
    - Provider native service is significantly superior
    - Workloads are unlikely to move in 3-5 years
- Avoid lock-in when:
    - Regulatory requirements mandate multi-provider capability
    - Data volumes make egress costs a serious concern
    - You need competitive pricing leverage
---
## Regulatory and Data Sovereignty

- Laws dictate where data can be stored and processed
- Key regulations:
    - `GDPR` (EU) - data must stay in EU or approved countries
    - `CCPA` (California) - consumer data protection rights
    - `PIPL` (China) - strict data localization requirements
    - `LGPD` (Brazil), `PDPA` (Singapore) - regional frameworks
- Multi-cloud helps: deploy in local providers per jurisdiction
---
## Data Sovereignty Map

<svg viewBox="0 0 800 380" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="30" width="180" height="130" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="130" y="55" text-anchor="middle" font-weight="bold" font-size="13" fill="#1565c0">North America</text>
  <text x="130" y="80" text-anchor="middle" font-size="10">CCPA (California)</text>
  <text x="130" y="100" text-anchor="middle" font-size="10">PIPEDA (Canada)</text>
  <text x="130" y="120" text-anchor="middle" font-size="10">HIPAA (Healthcare)</text>
  <text x="130" y="140" text-anchor="middle" font-size="10">FedRAMP (Gov)</text>
  <rect x="250" y="30" width="180" height="130" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="340" y="55" text-anchor="middle" font-weight="bold" font-size="13" fill="#2e7d32">Europe</text>
  <text x="340" y="80" text-anchor="middle" font-size="10">GDPR</text>
  <text x="340" y="100" text-anchor="middle" font-size="10">Data must stay in EU</text>
  <text x="340" y="120" text-anchor="middle" font-size="10">Schrems II ruling</text>
  <text x="340" y="140" text-anchor="middle" font-size="10">Right to erasure</text>
  <rect x="460" y="30" width="180" height="130" rx="10" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="550" y="55" text-anchor="middle" font-weight="bold" font-size="13" fill="#e65100">Asia-Pacific</text>
  <text x="550" y="80" text-anchor="middle" font-size="10">PIPL (China)</text>
  <text x="550" y="100" text-anchor="middle" font-size="10">PDPA (Singapore)</text>
  <text x="550" y="120" text-anchor="middle" font-size="10">APPI (Japan)</text>
  <text x="550" y="140" text-anchor="middle" font-size="10">Strict localization</text>
  <rect x="150" y="210" width="180" height="130" rx="10" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="240" y="235" text-anchor="middle" font-weight="bold" font-size="13" fill="#c62828">South America</text>
  <text x="240" y="260" text-anchor="middle" font-size="10">LGPD (Brazil)</text>
  <text x="240" y="280" text-anchor="middle" font-size="10">Inspired by GDPR</text>
  <text x="240" y="300" text-anchor="middle" font-size="10">Cross-border rules</text>
  <rect x="400" y="210" width="180" height="130" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="490" y="235" text-anchor="middle" font-weight="bold" font-size="13" fill="#6a1b9a">Middle East / Africa</text>
  <text x="490" y="260" text-anchor="middle" font-size="10">POPIA (South Africa)</text>
  <text x="490" y="280" text-anchor="middle" font-size="10">PDPL (Saudi Arabia)</text>
  <text x="490" y="300" text-anchor="middle" font-size="10">Emerging frameworks</text>
</svg>

---
## Cloud Strategy Decision Framework

- Ask these questions before choosing a strategy:
    - Where are our customers geographically?
    - What are our regulatory obligations?
    - What is our team's cloud expertise?
    - What is our budget for abstraction and tooling?
    - What is our risk tolerance for outages?
    - How likely is a future migration?
---
## Cloud-Agnostic Tooling

- Tools that work across cloud providers:
    - `Terraform` / `OpenTofu` for infrastructure
    - `Kubernetes` for container orchestration
    - `Prometheus` + `Grafana` for monitoring
    - `Vault` for secrets management
- Promise: write once, deploy anywhere
- Reality: "write once, debug everywhere"
- Each provider has different networking, IAM, storage, and DNS models
---
## The Lowest Common Denominator Problem

<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="200" height="250" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-weight="bold" font-size="13" fill="#1565c0">AWS Features</text>
  <rect x="70" y="70" width="160" height="25" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="150" y="87" text-anchor="middle" font-size="10">Lambda@Edge</text>
  <rect x="70" y="100" width="160" height="25" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="150" y="117" text-anchor="middle" font-size="10">DynamoDB Streams</text>
  <rect x="70" y="130" width="160" height="25" rx="4" fill="#90caf9" stroke="#1565c0" stroke-width="1.5"/>
  <text x="150" y="147" text-anchor="middle" font-size="10">S3 Object Storage</text>
  <rect x="70" y="160" width="160" height="25" rx="4" fill="#90caf9" stroke="#1565c0" stroke-width="1.5"/>
  <text x="150" y="177" text-anchor="middle" font-size="10">EC2 Compute</text>
  <rect x="70" y="190" width="160" height="25" rx="4" fill="#90caf9" stroke="#1565c0" stroke-width="1.5"/>
  <text x="150" y="207" text-anchor="middle" font-size="10">VPC Networking</text>
  <rect x="300" y="30" width="200" height="250" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="400" y="55" text-anchor="middle" font-weight="bold" font-size="13" fill="#2e7d32">GCP Features</text>
  <rect x="320" y="70" width="160" height="25" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="400" y="87" text-anchor="middle" font-size="10">Cloud Spanner</text>
  <rect x="320" y="100" width="160" height="25" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="400" y="117" text-anchor="middle" font-size="10">BigQuery ML</text>
  <rect x="320" y="130" width="160" height="25" rx="4" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="400" y="147" text-anchor="middle" font-size="10">GCS Object Storage</text>
  <rect x="320" y="160" width="160" height="25" rx="4" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="400" y="177" text-anchor="middle" font-size="10">GCE Compute</text>
  <rect x="320" y="190" width="160" height="25" rx="4" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="400" y="207" text-anchor="middle" font-size="10">VPC Networking</text>
  <rect x="560" y="100" width="200" height="160" rx="10" fill="#fff9c4" stroke="#f57f17" stroke-width="2.5"/>
  <text x="660" y="125" text-anchor="middle" font-weight="bold" font-size="13" fill="#f57f17">Common Subset</text>
  <rect x="580" y="140" width="160" height="25" rx="4" fill="#fff176" stroke="#f57f17" stroke-width="1"/>
  <text x="660" y="157" text-anchor="middle" font-size="10">Object Storage</text>
  <rect x="580" y="170" width="160" height="25" rx="4" fill="#fff176" stroke="#f57f17" stroke-width="1"/>
  <text x="660" y="187" text-anchor="middle" font-size="10">Compute VMs</text>
  <rect x="580" y="200" width="160" height="25" rx="4" fill="#fff176" stroke="#f57f17" stroke-width="1"/>
  <text x="660" y="217" text-anchor="middle" font-size="10">VPC Networking</text>
  <text x="660" y="250" text-anchor="middle" font-size="11" fill="#f57f17" font-style="italic">Only basic features!</text>
</svg>

---
## Abstraction Layer Architecture

<svg viewBox="0 0 800 360" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="10" width="600" height="50" rx="8" fill="#e1bee7" stroke="#6a1b9a" stroke-width="2"/>
  <text x="400" y="40" text-anchor="middle" font-weight="bold" font-size="14" fill="#6a1b9a">Application Code</text>
  <rect x="100" y="80" width="600" height="50" rx="8" fill="#ce93d8" stroke="#6a1b9a" stroke-width="2"/>
  <text x="400" y="110" text-anchor="middle" font-weight="bold" font-size="13" fill="#fff">Cloud Abstraction SDK</text>
  <rect x="100" y="150" width="600" height="50" rx="8" fill="#ba68c8" stroke="#6a1b9a" stroke-width="2"/>
  <text x="400" y="180" text-anchor="middle" font-weight="bold" font-size="13" fill="#fff">Provider Adapter Layer</text>
  <rect x="100" y="220" width="180" height="50" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="190" y="250" text-anchor="middle" font-weight="bold" font-size="12" fill="#e65100">AWS SDK</text>
  <rect x="310" y="220" width="180" height="50" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="400" y="250" text-anchor="middle" font-weight="bold" font-size="12" fill="#1565c0">Azure SDK</text>
  <rect x="520" y="220" width="180" height="50" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="610" y="250" text-anchor="middle" font-weight="bold" font-size="12" fill="#2e7d32">GCP SDK</text>
  <rect x="100" y="290" width="180" height="40" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="190" y="315" text-anchor="middle" font-size="11">AWS Services</text>
  <rect x="310" y="290" width="180" height="40" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="400" y="315" text-anchor="middle" font-size="11">Azure Services</text>
  <rect x="520" y="290" width="180" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="610" y="315" text-anchor="middle" font-size="11">GCP Services</text>
  <text x="50" y="40" text-anchor="middle" font-size="10" fill="#999">Layer 4</text>
  <text x="50" y="110" text-anchor="middle" font-size="10" fill="#999">Layer 3</text>
  <text x="50" y="180" text-anchor="middle" font-size="10" fill="#999">Layer 2</text>
  <text x="50" y="250" text-anchor="middle" font-size="10" fill="#999">Layer 1</text>
</svg>

---
## Cost of Abstraction Layers

- Engineering cost to build and maintain the abstraction
- Performance overhead from additional indirection
- Feature lag: new provider features take months to integrate
- Testing cost: every change must be verified on all providers
- Debugging complexity: issues may be in the abstraction, not the app
- Estimate: 1-3 full-time engineers to maintain a cloud abstraction
---
## Terraform as a Multi-Cloud Tool

- `Terraform` uses providers to abstract cloud resources
- Same HCL syntax, different providers underneath

```hcl
# AWS
resource "aws_instance" "web" {
  ami           = "ami-0c55b159"
  instance_type = "t3.micro"
}

# GCP
resource "google_compute_instance" "web" {
  machine_type = "e2-micro"
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
}
```

---
## Terraform Multi-Cloud Limitations

- Resource types are completely different across providers
- You cannot reuse the same `.tf` file for multiple clouds
- State management differs per provider
- Modules are provider-specific
- `Terraform` helps with consistency, not with portability
- True portability requires a wrapper layer on top of `Terraform`
---
## Kubernetes as a Portability Layer

- `Kubernetes` provides a consistent API across clouds
- Same `Deployment`, `Service`, `Ingress` manifests work on `EKS`, `AKS`, `GKE`
- But underlying details differ:
    - Load balancer implementations
    - Storage class drivers (`EBS CSI`, `Azure Disk`, `PD CSI`)
    - Networking (`CNI` plugins vary per provider)
    - Node auto-scaling behavior (`Karpenter` vs `Autopilot`)
---
## The Real Multi-Cloud Cost

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="25" text-anchor="middle" font-weight="bold" font-size="14" fill="#333">Hidden Costs of Multi-Cloud</text>
  <rect x="60" y="50" width="120" height="200" rx="4" fill="#ef5350" stroke="#c62828" stroke-width="1.5"/>
  <text x="120" y="160" text-anchor="middle" font-size="10" fill="#fff" font-weight="bold">Compute</text>
  <text x="120" y="175" text-anchor="middle" font-size="10" fill="#fff">+15-25%</text>
  <rect x="200" y="80" width="120" height="170" rx="4" fill="#ff7043" stroke="#d84315" stroke-width="1.5"/>
  <text x="260" y="175" text-anchor="middle" font-size="10" fill="#fff" font-weight="bold">Staff</text>
  <text x="260" y="190" text-anchor="middle" font-size="10" fill="#fff">+30-50%</text>
  <rect x="340" y="110" width="120" height="140" rx="4" fill="#ffa726" stroke="#e65100" stroke-width="1.5"/>
  <text x="400" y="190" text-anchor="middle" font-size="10" fill="#fff" font-weight="bold">Networking</text>
  <text x="400" y="205" text-anchor="middle" font-size="10" fill="#fff">+10-20%</text>
  <rect x="480" y="130" width="120" height="120" rx="4" fill="#ffca28" stroke="#f57f17" stroke-width="1.5"/>
  <text x="540" y="200" text-anchor="middle" font-size="11" font-weight="bold">Tooling</text>
  <text x="540" y="215" text-anchor="middle" font-size="10">+5-15%</text>
  <rect x="620" y="160" width="120" height="90" rx="4" fill="#ffee58" stroke="#f9a825" stroke-width="1.5"/>
  <text x="680" y="210" text-anchor="middle" font-size="11" font-weight="bold">Compliance</text>
  <text x="680" y="225" text-anchor="middle" font-size="10">+5-10%</text>
  <text x="400" y="280" text-anchor="middle" font-size="12" fill="#666" font-style="italic">Compared to single cloud baseline</text>
</svg>

---
## When Multi-Cloud Makes Sense

- Acquisitions bring different cloud footprints
- Best-of-breed services on different providers
    - `BigQuery` on GCP for analytics
    - `Azure AD` for enterprise identity
    - `AWS` for broadest service catalog
- Regulatory requirements across jurisdictions
- Genuine need for vendor negotiation leverage
---
## When Multi-Cloud Does Not Make Sense

- "We might need it someday" is not a strategy
- Small teams (under 50 engineers) rarely benefit
- If you are not using advanced cloud-native services
- If your workloads are simple web applications
- If you lack budget for the additional tooling and staff
---
## Disaster Recovery: Core Concepts

- `RPO` - Recovery Point Objective: how much data can you lose?
- `RTO` - Recovery Time Objective: how fast must you recover?
- These drive architecture and cost decisions
- Lower RPO/RTO means higher cost
- Must be defined per workload, not globally
---
## DR Tiers

| Tier | Strategy | RTO | RPO | Cost |
|------|----------|-----|-----|------|
| 1 | Backup and Restore | Hours | Hours | Low |
| 2 | Pilot Light | 30 min | Minutes | Medium |
| 3 | Warm Standby | Minutes | Seconds | High |
| 4 | Active-Active | Near zero | Near zero | Very High |
---
## Backup and Restore Architecture

<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="40" width="280" height="200" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="190" y="30" text-anchor="middle" font-weight="bold" font-size="14" fill="#2e7d32">Primary Region</text>
  <rect x="80" y="70" width="100" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="130" y="95" text-anchor="middle" font-size="11">App Servers</text>
  <rect x="200" y="70" width="100" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="250" y="95" text-anchor="middle" font-size="11">Database</text>
  <rect x="120" y="140" width="140" height="40" rx="6" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="190" y="165" text-anchor="middle" font-size="11" font-weight="bold">Scheduled Backups</text>
  <line x1="330" y1="160" x2="470" y2="160" stroke="#666" stroke-width="2" stroke-dasharray="8,4"/>
  <text x="400" y="150" text-anchor="middle" font-size="10" fill="#666">Periodic copy</text>
  <rect x="470" y="40" width="280" height="200" rx="10" fill="#fce4ec" stroke="#c62828" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="610" y="30" text-anchor="middle" font-weight="bold" font-size="14" fill="#c62828">DR Region (Cold)</text>
  <rect x="530" y="140" width="160" height="40" rx="6" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="610" y="165" text-anchor="middle" font-size="11">Backup Storage</text>
  <text x="610" y="100" text-anchor="middle" font-size="12" fill="#999" font-style="italic">No running infra</text>
  <text x="610" y="120" text-anchor="middle" font-size="12" fill="#999" font-style="italic">until failover</text>
</svg>

---
## Warm Standby Architecture

<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="40" width="340" height="200" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="200" y="30" text-anchor="middle" font-weight="bold" font-size="14" fill="#2e7d32">Primary Region (Full Scale)</text>
  <rect x="50" y="70" width="90" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="95" y="92" text-anchor="middle" font-size="10">App x10</text>
  <rect x="155" y="70" width="90" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="200" y="92" text-anchor="middle" font-size="10">Web x5</text>
  <rect x="260" y="70" width="90" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="305" y="92" text-anchor="middle" font-size="10">Cache x3</text>
  <rect x="100" y="130" width="200" height="35" rx="6" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="200" y="152" text-anchor="middle" font-size="10" font-weight="bold">Primary DB (Multi-AZ)</text>
  <rect x="100" y="185" width="200" height="35" rx="6" fill="#81c784" stroke="#2e7d32" stroke-width="1"/>
  <text x="200" y="207" text-anchor="middle" font-size="10">100% traffic</text>
  <line x1="370" y1="130" x2="430" y2="130" stroke="#1565c0" stroke-width="2.5"/>
  <text x="400" y="120" text-anchor="middle" font-size="9" fill="#1565c0">Sync</text>
  <text x="400" y="150" text-anchor="middle" font-size="9" fill="#1565c0">Replication</text>
  <rect x="430" y="40" width="340" height="200" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="600" y="30" text-anchor="middle" font-weight="bold" font-size="14" fill="#1565c0">DR Region (Reduced Scale)</text>
  <rect x="480" y="70" width="90" height="35" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="525" y="92" text-anchor="middle" font-size="10">App x2</text>
  <rect x="585" y="70" width="90" height="35" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="630" y="92" text-anchor="middle" font-size="10">Web x1</text>
  <rect x="530" y="130" width="200" height="35" rx="6" fill="#90caf9" stroke="#1565c0" stroke-width="1.5"/>
  <text x="630" y="152" text-anchor="middle" font-size="10" font-weight="bold">Read Replica DB</text>
  <rect x="530" y="185" width="200" height="35" rx="6" fill="#64b5f6" stroke="#1565c0" stroke-width="1"/>
  <text x="630" y="207" text-anchor="middle" font-size="10">0% traffic (standby)</text>
</svg>

---
## Active-Active Architecture

<svg viewBox="0 0 800 340" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="10" width="300" height="50" rx="10" fill="#e1bee7" stroke="#6a1b9a" stroke-width="2"/>
  <text x="400" y="40" text-anchor="middle" font-weight="bold" font-size="13" fill="#6a1b9a">Global Load Balancer / DNS</text>
  <line x1="300" y1="60" x2="180" y2="100" stroke="#6a1b9a" stroke-width="2"/>
  <line x1="500" y1="60" x2="620" y2="100" stroke="#6a1b9a" stroke-width="2"/>
  <text x="220" y="82" text-anchor="middle" font-size="10" fill="#6a1b9a">50% traffic</text>
  <text x="580" y="82" text-anchor="middle" font-size="10" fill="#6a1b9a">50% traffic</text>
  <rect x="40" y="100" width="280" height="220" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="180" y="125" text-anchor="middle" font-weight="bold" font-size="13" fill="#2e7d32">Region A (us-east-1)</text>
  <rect x="70" y="140" width="100" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="120" y="162" text-anchor="middle" font-size="10">App Cluster</text>
  <rect x="190" y="140" width="100" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="240" y="162" text-anchor="middle" font-size="10">Cache</text>
  <rect x="100" y="200" width="160" height="35" rx="6" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="180" y="222" text-anchor="middle" font-size="10" font-weight="bold">DB (Read/Write)</text>
  <rect x="100" y="260" width="160" height="35" rx="6" fill="#81c784" stroke="#2e7d32" stroke-width="1"/>
  <text x="180" y="282" text-anchor="middle" font-size="10">Active</text>
  <rect x="480" y="100" width="280" height="220" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="620" y="125" text-anchor="middle" font-weight="bold" font-size="13" fill="#1565c0">Region B (eu-west-1)</text>
  <rect x="510" y="140" width="100" height="35" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="560" y="162" text-anchor="middle" font-size="10">App Cluster</text>
  <rect x="630" y="140" width="100" height="35" rx="6" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="680" y="162" text-anchor="middle" font-size="10">Cache</text>
  <rect x="540" y="200" width="160" height="35" rx="6" fill="#90caf9" stroke="#1565c0" stroke-width="1.5"/>
  <text x="620" y="222" text-anchor="middle" font-size="10" font-weight="bold">DB (Read/Write)</text>
  <rect x="540" y="260" width="160" height="35" rx="6" fill="#64b5f6" stroke="#1565c0" stroke-width="1"/>
  <text x="620" y="282" text-anchor="middle" font-size="10">Active</text>
  <line x1="260" y1="217" x2="540" y2="217" stroke="#ff5722" stroke-width="2.5" stroke-dasharray="6,3"/>
  <text x="400" y="210" text-anchor="middle" font-size="10" fill="#ff5722" font-weight="bold">Bi-directional Replication</text>
</svg>

---
## Cross-Region Networking and Replication

- Connectivity options:
    - `VPC Peering` - direct, low-latency, same provider
    - `Transit Gateway` - hub-and-spoke model
    - `Direct Connect` / `ExpressRoute` - dedicated links
- Replication strategies:
    - **Synchronous**: zero data loss, higher latency
    - **Asynchronous**: minimal lag, possible data loss
    - **Eventual consistency**: replicas converge over time
---
## Multi-Region DNS Failover

```yaml
# Route 53 health check and failover example
Resources:
  PrimaryHealthCheck:
    Type: AWS::Route53::HealthCheck
    Properties:
      HealthCheckConfig:
        FullyQualifiedDomainName: "primary.example.com"
        Port: 443
        Type: HTTPS
        FailureThreshold: 3
  DNSRecord:
    Type: AWS::Route53::RecordSet
    Properties:
      Name: "app.example.com"
      Type: A
      SetIdentifier: "primary"
      Failover: PRIMARY
      HealthCheckId: !Ref PrimaryHealthCheck
```

---
## Cross-Cloud DR Architecture

<svg viewBox="0 0 800 340" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="400" height="45" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="400" y="32" text-anchor="middle" font-weight="bold" font-size="13" fill="#6a1b9a">External DNS (Cloudflare / NS1)</text>
  <line x1="300" y1="50" x2="180" y2="90" stroke="#6a1b9a" stroke-width="2"/>
  <line x1="500" y1="50" x2="620" y2="90" stroke="#6a1b9a" stroke-width="2"/>
  <rect x="40" y="90" width="280" height="230" rx="10" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="180" y="115" text-anchor="middle" font-weight="bold" font-size="14" fill="#e65100">AWS (Primary)</text>
  <rect x="70" y="130" width="100" height="35" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="120" y="152" text-anchor="middle" font-size="10">EKS Cluster</text>
  <rect x="190" y="130" width="100" height="35" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="240" y="152" text-anchor="middle" font-size="10">RDS Primary</text>
  <rect x="70" y="185" width="100" height="35" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="120" y="207" text-anchor="middle" font-size="10">S3 Buckets</text>
  <rect x="190" y="185" width="100" height="35" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="240" y="207" text-anchor="middle" font-size="10">ElastiCache</text>
  <rect x="100" y="245" width="160" height="30" rx="6" fill="#ffcc80" stroke="#e65100" stroke-width="1.5"/>
  <text x="180" y="265" text-anchor="middle" font-size="10" font-weight="bold">Live Traffic</text>
  <rect x="480" y="90" width="280" height="230" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="620" y="115" text-anchor="middle" font-weight="bold" font-size="14" fill="#2e7d32">GCP (DR Standby)</text>
  <rect x="510" y="130" width="100" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="560" y="152" text-anchor="middle" font-size="10">GKE Cluster</text>
  <rect x="630" y="130" width="100" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="680" y="152" text-anchor="middle" font-size="10">Cloud SQL</text>
  <rect x="510" y="185" width="100" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="560" y="207" text-anchor="middle" font-size="10">GCS Buckets</text>
  <rect x="630" y="185" width="100" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="680" y="207" text-anchor="middle" font-size="10">Memorystore</text>
  <rect x="540" y="245" width="160" height="30" rx="6" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="620" y="265" text-anchor="middle" font-size="10" font-weight="bold">Standby</text>
  <line x1="320" y1="170" x2="480" y2="170" stroke="#ff5722" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="400" y="163" text-anchor="middle" font-size="9" fill="#ff5722">Data Replication</text>
</svg>

---
## Testing and Automating DR

- Test your DR plan before you need it
- Tools: `Chaos Monkey`, `Gremlin`, `Litmus`
- Regular "Game Day" exercises simulate real failures
- All DR infrastructure must be defined in code
    - `Terraform`, `Pulumi`, or `CloudFormation` for infra
    - `Ansible` or scripts for failover orchestration
- No manual steps during high-stress failover events
---
## Multi-Region Data Consistency

- CAP theorem applies: you cannot have all three:
    - **Consistency**: all reads return the latest write
    - **Availability**: every request gets a response
    - **Partition tolerance**: system works despite network splits
- Multi-region systems must choose between CP and AP
- Most choose AP with eventual consistency
- Critical transactions may need CP with higher latency
---
## Egress Costs and Exit Strategy

- Cloud providers charge for outbound data transfer
- Typical egress costs:
    - `AWS`: $0.09/GB, `Azure`: $0.087/GB, `GCP`: $0.12/GB
- Cross-cloud replication can cost thousands per month
- Even with single cloud, plan for potential migration:
    - Use standard data formats (`Parquet`, `JSON`, `Avro`)
    - Avoid proprietary query languages where possible
    - Document all cloud-specific dependencies
---
## Cloud Strategy Anti-Patterns

- "Multi-cloud by accident" - no intentional strategy
- "Resume-driven multi-cloud" - using tools for learning, not value
- "All eggs in one basket" - no DR plan at all
- "Over-abstracted" - seven layers between app and cloud
- "Lift and shift forever" - running VMs without using cloud services
- "Cloud-native maximalist" - using every managed service available
---
## Decision Matrix: Choosing Your Strategy

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="700" height="40" rx="6" fill="#e1bee7" stroke="#6a1b9a" stroke-width="1.5"/>
  <text x="400" y="55" text-anchor="middle" font-weight="bold" font-size="13" fill="#6a1b9a">Cloud Strategy Decision Tree</text>
  <rect x="300" y="90" width="200" height="35" rx="6" fill="#fff9c4" stroke="#f57f17" stroke-width="1.5"/>
  <text x="400" y="112" text-anchor="middle" font-size="11">Regulatory constraints?</text>
  <line x1="300" y1="107" x2="200" y2="150" stroke="#666" stroke-width="1.5"/>
  <text x="240" y="130" font-size="10" fill="#2e7d32">Yes</text>
  <line x1="500" y1="107" x2="600" y2="150" stroke="#666" stroke-width="1.5"/>
  <text x="560" y="130" font-size="10" fill="#c62828">No</text>
  <rect x="100" y="150" width="200" height="35" rx="6" fill="#fff9c4" stroke="#f57f17" stroke-width="1.5"/>
  <text x="200" y="172" text-anchor="middle" font-size="11">Data in multiple regions?</text>
  <rect x="500" y="150" width="200" height="35" rx="6" fill="#fff9c4" stroke="#f57f17" stroke-width="1.5"/>
  <text x="600" y="172" text-anchor="middle" font-size="11">Team size > 50 engineers?</text>
  <line x1="150" y1="185" x2="100" y2="220" stroke="#666" stroke-width="1.5"/>
  <text x="115" y="205" font-size="10" fill="#2e7d32">Yes</text>
  <line x1="250" y1="185" x2="300" y2="220" stroke="#666" stroke-width="1.5"/>
  <text x="285" y="205" font-size="10" fill="#c62828">No</text>
  <line x1="550" y1="185" x2="500" y2="220" stroke="#666" stroke-width="1.5"/>
  <text x="515" y="205" font-size="10" fill="#2e7d32">Yes</text>
  <line x1="650" y1="185" x2="700" y2="220" stroke="#666" stroke-width="1.5"/>
  <text x="685" y="205" font-size="10" fill="#c62828">No</text>
  <rect x="30" y="220" width="150" height="35" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="105" y="242" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Multi-Cloud</text>
  <rect x="230" y="220" width="150" height="35" rx="6" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="305" y="242" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">Hybrid Cloud</text>
  <rect x="430" y="220" width="150" height="35" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="505" y="242" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">Consider Multi</text>
  <rect x="630" y="220" width="150" height="35" rx="6" fill="#e1bee7" stroke="#6a1b9a" stroke-width="2"/>
  <text x="705" y="242" text-anchor="middle" font-size="11" font-weight="bold" fill="#6a1b9a">Single Cloud</text>
</svg>

---
## Summary: Key Takeaways

- Start with business requirements, not technology preferences
- Single cloud is right for most organizations
- Multi-cloud adds real value only when justified by specific needs
- Abstraction layers are expensive to build and maintain
- The LCD problem limits what you can achieve portably
- DR and HA plans must be tested, not just documented
- Data sovereignty increasingly drives cloud strategy
- Always account for hidden costs: egress, staff, tooling
