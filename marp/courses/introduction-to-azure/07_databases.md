# Azure Database Services

## Database Service Types

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Azure Database Services</text>
  <rect x="10" y="30" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="50" text-anchor="middle" font-size="11" font-weight="bold">Relational</text>
  <text x="95" y="66" text-anchor="middle" font-size="10">Azure SQL Database</text>
  <text x="95" y="80" text-anchor="middle" font-size="10">MySQL, PostgreSQL</text>
  <text x="95" y="93" text-anchor="middle" font-size="10">SQL Managed Instance</text>
  <rect x="210" y="30" width="170" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="50" text-anchor="middle" font-size="11" font-weight="bold">NoSQL</text>
  <text x="295" y="66" text-anchor="middle" font-size="10">Cosmos DB</text>
  <text x="295" y="80" text-anchor="middle" font-size="10">Table Storage</text>
  <text x="295" y="93" text-anchor="middle" font-size="10">Multi-model, global</text>
  <rect x="410" y="30" width="180" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="50" text-anchor="middle" font-size="11" font-weight="bold">Caching / Other</text>
  <text x="500" y="66" text-anchor="middle" font-size="10">Azure Cache (Redis)</text>
  <text x="500" y="80" text-anchor="middle" font-size="10">Azure Synapse</text>
  <text x="500" y="93" text-anchor="middle" font-size="10">Data Explorer</text>
  <rect x="60" y="120" width="480" height="65" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="140" text-anchor="middle" font-size="11" font-weight="bold">All Azure DB Services Include</text>
  <text x="300" y="158" text-anchor="middle" font-size="10">Automated backups | High availability | Encryption at rest</text>
  <text x="300" y="174" text-anchor="middle" font-size="10">Geo-replication | Monitoring | Auto-patching | Scaling</text>
</svg>

---

## Azure SQL Database
- Managed SQL Server
- Built-in intelligence
- Automatic tuning
- Scalable performance
- High availability

---

## SQL Database Deployment Options

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Azure SQL Deployment Options</text>
  <rect x="10" y="30" width="180" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="50" text-anchor="middle" font-size="11" font-weight="bold">SQL Database</text>
  <text x="100" y="66" text-anchor="middle" font-size="10">Fully managed</text>
  <text x="100" y="80" text-anchor="middle" font-size="10">Serverless option</text>
  <text x="100" y="94" text-anchor="middle" font-size="10">Elastic pools</text>
  <text x="100" y="106" text-anchor="middle" font-size="9" fill="#555">Best for: New apps</text>
  <rect x="210" y="30" width="180" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">Managed Instance</text>
  <text x="300" y="66" text-anchor="middle" font-size="10">Near 100% SQL compat</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">VNet integration</text>
  <text x="300" y="94" text-anchor="middle" font-size="10">Cross-DB queries</text>
  <text x="300" y="106" text-anchor="middle" font-size="9" fill="#555">Best for: Migration</text>
  <rect x="410" y="30" width="180" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="50" text-anchor="middle" font-size="11" font-weight="bold">SQL on VM</text>
  <text x="500" y="66" text-anchor="middle" font-size="10">Full SQL Server</text>
  <text x="500" y="80" text-anchor="middle" font-size="10">OS-level access</text>
  <text x="500" y="94" text-anchor="middle" font-size="10">Custom config</text>
  <text x="500" y="106" text-anchor="middle" font-size="9" fill="#555">Best for: Legacy apps</text>
  <rect x="60" y="130" width="480" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="148" text-anchor="middle" font-size="10" font-weight="bold">Purchasing Models</text>
  <text x="200" y="165" text-anchor="middle" font-size="10">vCore: Flexible compute/storage</text>
  <text x="430" y="165" text-anchor="middle" font-size="10">DTU: Bundled resources</text>
  <text x="300" y="180" text-anchor="middle" font-size="10">Serverless: Auto-pause, pay per second</text>
</svg>

---

## Service Tiers
1. General Purpose
1. Business Critical
1. Hyperscale
1. Basic
1. Standard

---

## SQL Database Features
- Automatic tuning
- Query performance insight
- Threat detection
- Vulnerability assessment
- Dynamic data masking

---

## High Availability
- Built-in redundancy
- Automatic backups
- Geo-replication
- Failover groups
- Zone redundancy

---

## SQL Security
- Authentication methods
- Authorization
- Row-level security
- Data encryption
- Auditing

---

## Azure Cosmos DB
- Multi-model database
- Global distribution
- Automatic scaling
- Multiple APIs
- Guaranteed performance

---

## Cosmos DB APIs

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Cosmos DB - Multiple API Support</text>
  <rect x="180" y="28" width="240" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">Cosmos DB Engine</text>
  <line x1="200" y1="63" x2="75" y2="80" stroke="#333" stroke-width="1"/>
  <line x1="260" y1="63" x2="210" y2="80" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="63" x2="340" y2="80" stroke="#333" stroke-width="1"/>
  <line x1="340" y1="63" x2="465" y2="80" stroke="#333" stroke-width="1"/>
  <rect x="10" y="80" width="130" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="98" text-anchor="middle" font-size="10" font-weight="bold">NoSQL API</text>
  <text x="75" y="115" text-anchor="middle" font-size="10">JSON documents</text>
  <rect x="155" y="80" width="110" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="210" y="98" text-anchor="middle" font-size="10" font-weight="bold">MongoDB</text>
  <text x="210" y="115" text-anchor="middle" font-size="10">Wire protocol</text>
  <rect x="280" y="80" width="120" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="340" y="98" text-anchor="middle" font-size="10" font-weight="bold">Cassandra</text>
  <text x="340" y="115" text-anchor="middle" font-size="10">Wide column</text>
  <rect x="415" y="80" width="100" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="465" y="98" text-anchor="middle" font-size="10" font-weight="bold">Gremlin</text>
  <text x="465" y="115" text-anchor="middle" font-size="10">Graph DB</text>
  <rect x="520" y="80" width="70" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="555" y="98" text-anchor="middle" font-size="10" font-weight="bold">Table</text>
  <text x="555" y="115" text-anchor="middle" font-size="9">Key-value</text>
  <rect x="60" y="145" width="480" height="42" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="162" text-anchor="middle" font-size="10" font-weight="bold">Global Distribution: Multi-region writes with single-digit ms latency</text>
  <text x="300" y="178" text-anchor="middle" font-size="10">5 consistency levels: Strong | Bounded | Session | Prefix | Eventual</text>
</svg>

---

## Cosmos DB Consistency
- Strong
- Bounded staleness
- Session
- Consistent prefix
- Eventual

---

## Partitioning Strategy
- Partition keys
- Logical partitions
- Physical partitions
- Synthetic keys
- Distribution

---

## Global Distribution
- Multi-region writes
- Automatic failover
- Conflict resolution
- Global endpoints
- Region management

---

## Cosmos DB Security
- Network security
- Authentication
- Authorization
- Encryption
- Auditing

---

## Azure MySQL
- Managed MySQL
- Community edition
- High availability
- Automated backups
- Scaling options

---

## MySQL Configuration
- Server parameters
- Performance settings
- Storage options
- Networking
- Security

---

## Azure PostgreSQL
- Managed PostgreSQL
- Single server
- Flexible server
- Hyperscale
- Extensions

---

## PostgreSQL Features
- High availability
- Automatic backups
- Point-in-time restore
- Query performance
- Monitoring

---

## Database Migration
- Azure Migrate
- Database Migration Service
- Offline migration
- Online migration
- Assessment tools

---

## Migration Process

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Database Migration Process</text>
  <rect x="10" y="35" width="100" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="55" text-anchor="middle" font-size="10" font-weight="bold">1. Assess</text>
  <text x="60" y="70" text-anchor="middle" font-size="10">DMA tool</text>
  <text x="60" y="82" text-anchor="middle" font-size="9">Compatibility</text>
  <line x1="110" y1="62" x2="130" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_databases)"/>
  <rect x="130" y="35" width="100" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="180" y="55" text-anchor="middle" font-size="10" font-weight="bold">2. Plan</text>
  <text x="180" y="70" text-anchor="middle" font-size="10">Schema map</text>
  <text x="180" y="82" text-anchor="middle" font-size="9">Size/perf reqs</text>
  <line x1="230" y1="62" x2="250" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_databases)"/>
  <rect x="250" y="35" width="100" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="10" font-weight="bold">3. Migrate</text>
  <text x="300" y="70" text-anchor="middle" font-size="10">DMS service</text>
  <text x="300" y="82" text-anchor="middle" font-size="9">Online/Offline</text>
  <line x1="350" y1="62" x2="370" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_databases)"/>
  <rect x="370" y="35" width="100" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="420" y="55" text-anchor="middle" font-size="10" font-weight="bold">4. Validate</text>
  <text x="420" y="70" text-anchor="middle" font-size="10">Test queries</text>
  <text x="420" y="82" text-anchor="middle" font-size="9">Data integrity</text>
  <line x1="470" y1="62" x2="490" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_databases)"/>
  <rect x="490" y="35" width="100" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="55" text-anchor="middle" font-size="10" font-weight="bold">5. Cutover</text>
  <text x="540" y="70" text-anchor="middle" font-size="10">Switch traffic</text>
  <text x="540" y="82" text-anchor="middle" font-size="9">Monitor</text>
  <rect x="60" y="110" width="230" height="75" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="175" y="128" text-anchor="middle" font-size="10" font-weight="bold">Offline Migration</text>
  <text x="175" y="145" text-anchor="middle" font-size="10">Full backup + restore</text>
  <text x="175" y="160" text-anchor="middle" font-size="10">Downtime required</text>
  <text x="175" y="175" text-anchor="middle" font-size="10">Simpler process</text>
  <rect x="310" y="110" width="230" height="75" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="425" y="128" text-anchor="middle" font-size="10" font-weight="bold">Online Migration</text>
  <text x="425" y="145" text-anchor="middle" font-size="10">Continuous replication</text>
  <text x="425" y="160" text-anchor="middle" font-size="10">Minimal downtime</text>
  <text x="425" y="175" text-anchor="middle" font-size="10">More complex</text>
  <defs>
    <marker id="arrowd3_06_databases" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Performance Monitoring
- Azure Monitor
- Query insights
- Performance recommendations
- Metrics
- Alerts

---

## Database Scaling
- Vertical scaling
- Horizontal scaling
- Auto-scaling
- Manual scaling
- Read replicas

---

## Backup and Recovery
- Automated backups
- Manual backups
- Long-term retention
- Geo-restore
- Point-in-time recovery

---

## Security Best Practices
- Network isolation
- Access control
- Data encryption
- Auditing
- Compliance

---

## Cost Optimization
- Right-sizing
- Reserved capacity
- Performance tiers
- Storage optimization
- Monitoring usage

---

## Database DevOps
- CI/CD integration
- Schema management
- Version control
- Deployment automation
- Testing

---

## High Availability Design

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Database High Availability Design</text>
  <rect x="130" y="30" width="150" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="55" text-anchor="middle" font-size="11" font-weight="bold">Primary Region</text>
  <rect x="330" y="30" width="150" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="405" y="55" text-anchor="middle" font-size="11" font-weight="bold">Secondary Region</text>
  <line x1="280" y1="50" x2="330" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_06_databases)"/>
  <text x="305" y="45" text-anchor="middle" font-size="9">Geo-repl</text>
  <rect x="80" y="85" width="100" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="130" y="107" text-anchor="middle" font-size="10">Read/Write</text>
  <rect x="200" y="85" width="100" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="250" y="107" text-anchor="middle" font-size="10">Zone Replica</text>
  <rect x="330" y="85" width="100" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="380" y="107" text-anchor="middle" font-size="10">Read Replica</text>
  <rect x="450" y="85" width="100" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="500" y="107" text-anchor="middle" font-size="10">Zone Replica</text>
  <line x1="180" y1="103" x2="200" y2="103" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="430" y1="103" x2="450" y2="103" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>
  <rect x="40" y="140" width="250" height="48" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="165" y="158" text-anchor="middle" font-size="10" font-weight="bold">Auto-failover Group</text>
  <text x="165" y="175" text-anchor="middle" font-size="10">Automatic failover if primary down</text>
  <rect x="310" y="140" width="250" height="48" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="435" y="158" text-anchor="middle" font-size="10" font-weight="bold">SLA Guarantees</text>
  <text x="435" y="175" text-anchor="middle" font-size="10">99.995% with zone redundancy</text>
  <defs>
    <marker id="arrowd4_06_databases" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Data Synchronization
- Data sync services
- Replication
- Change tracking
- ETL processes
- Integration

---

## Monitoring and Alerting
- Performance metrics
- Resource utilization
- Query performance
- Availability
- Security events

---

## Compliance and Governance
- Data residency
- Regulatory compliance
- Audit logging
- Policy enforcement
- Access reviews

---

## Database Networking
- Virtual network integration
- Private endpoints
- Service endpoints
- Firewall rules
- VPN connectivity

---

## Future Roadmap
- Service updates
- New features
- Performance improvements
- Security enhancements
- Integration capabilities
