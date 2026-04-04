# Azure Storage Services

## Storage Service Types

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Azure Storage Service Types</text>
  <rect x="10" y="30" width="135" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="77" y="50" text-anchor="middle" font-size="11" font-weight="bold">Blob Storage</text>
  <text x="77" y="66" text-anchor="middle" font-size="10">Unstructured data</text>
  <text x="77" y="80" text-anchor="middle" font-size="10">Images, videos</text>
  <text x="77" y="94" text-anchor="middle" font-size="10">Backups, logs</text>
  <rect x="155" y="30" width="135" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="222" y="50" text-anchor="middle" font-size="11" font-weight="bold">File Storage</text>
  <text x="222" y="66" text-anchor="middle" font-size="10">SMB file shares</text>
  <text x="222" y="80" text-anchor="middle" font-size="10">Lift-and-shift</text>
  <text x="222" y="94" text-anchor="middle" font-size="10">Hybrid scenarios</text>
  <rect x="300" y="30" width="135" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="367" y="50" text-anchor="middle" font-size="11" font-weight="bold">Table Storage</text>
  <text x="367" y="66" text-anchor="middle" font-size="10">NoSQL key-value</text>
  <text x="367" y="80" text-anchor="middle" font-size="10">Structured data</text>
  <text x="367" y="94" text-anchor="middle" font-size="10">Schema-less</text>
  <rect x="445" y="30" width="145" height="80" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="517" y="50" text-anchor="middle" font-size="11" font-weight="bold">Queue Storage</text>
  <text x="517" y="66" text-anchor="middle" font-size="10">Message queuing</text>
  <text x="517" y="80" text-anchor="middle" font-size="10">Async processing</text>
  <text x="517" y="94" text-anchor="middle" font-size="10">App decoupling</text>
  <rect x="100" y="130" width="400" height="55" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="150" text-anchor="middle" font-size="11" font-weight="bold">Storage Account (Unique namespace)</text>
  <text x="300" y="167" text-anchor="middle" font-size="10">All services share: encryption, redundancy, access keys, firewalls</text>
  <text x="300" y="180" text-anchor="middle" font-size="10">Endpoint: https://&lt;account&gt;.blob|file|table|queue.core.windows.net</text>
</svg>

---

## Storage Account Overview
- Unique namespace
- Global replication
- Data redundancy
- Security features
- Access tiers

---

## Storage Account Types
1. Standard general-purpose v2
1. Premium block blobs
1. Premium file shares
1. Premium page blobs

---

## Redundancy Options

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Storage Redundancy Options</text>
  <rect x="10" y="30" width="130" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="50" text-anchor="middle" font-size="11" font-weight="bold">LRS</text>
  <text x="75" y="65" text-anchor="middle" font-size="10">3 copies in</text>
  <text x="75" y="78" text-anchor="middle" font-size="10">1 data center</text>
  <text x="75" y="93" text-anchor="middle" font-size="9">99.999999999%</text>
  <rect x="155" y="30" width="130" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="50" text-anchor="middle" font-size="11" font-weight="bold">ZRS</text>
  <text x="220" y="65" text-anchor="middle" font-size="10">3 copies across</text>
  <text x="220" y="78" text-anchor="middle" font-size="10">3 avail. zones</text>
  <text x="220" y="93" text-anchor="middle" font-size="9">99.9999999999%</text>
  <rect x="310" y="30" width="130" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="50" text-anchor="middle" font-size="11" font-weight="bold">GRS</text>
  <text x="375" y="65" text-anchor="middle" font-size="10">6 copies across</text>
  <text x="375" y="78" text-anchor="middle" font-size="10">2 regions</text>
  <text x="375" y="93" text-anchor="middle" font-size="9">99.99999999999999%</text>
  <rect x="455" y="30" width="135" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="522" y="50" text-anchor="middle" font-size="11" font-weight="bold">GZRS</text>
  <text x="522" y="65" text-anchor="middle" font-size="10">ZRS + GRS</text>
  <text x="522" y="78" text-anchor="middle" font-size="10">Best durability</text>
  <text x="522" y="93" text-anchor="middle" font-size="9">Highest redundancy</text>
  <line x1="140" y1="65" x2="155" y2="65" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_04_storage)"/>
  <line x1="285" y1="65" x2="310" y2="65" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_04_storage)"/>
  <line x1="440" y1="65" x2="455" y2="65" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_04_storage)"/>
  <rect x="60" y="120" width="480" height="65" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="140" text-anchor="middle" font-size="11" font-weight="bold">Cost vs. Durability Tradeoff</text>
  <text x="300" y="158" text-anchor="middle" font-size="10">LRS (lowest cost) -----> GZRS (highest cost, best protection)</text>
  <text x="300" y="175" text-anchor="middle" font-size="10">RA-GRS/RA-GZRS: Add read access from secondary region</text>
  <defs>
    <marker id="arrowd1_04_storage" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Understanding Blob Storage
- Binary Large Objects
- Unstructured data
- Video, audio, images
- Documents, logs
- Backup data

---

## Blob Types
- Block blobs
- Append blobs
- Page blobs
- Each optimized for specific uses

---

## Blob Access Tiers
- Hot tier
- Cool tier
- Archive tier
- Lifecycle management

---

## Blob Storage Features
- Soft delete
- Versioning
- Change feed
- Static website hosting
- CORS support

---

## Azure Files Overview
- SMB file shares
- Native mounting
- Hybrid scenarios
- File-based apps
- Shared access

---

## File Share Configuration
- Share size limits
- File permissions
- Network access
- Authentication
- Encryption

---

## Azure Queue Storage
- Message queuing
- Asynchronous processing
- Application decoupling
- Load leveling
- Scalable workflows

---

## Queue Storage Concepts
- Queue service
- Queue names
- Messages
- Message lifecycle
- Visibility timeout

---

## Azure Table Storage
- NoSQL data store
- Key-value pairs
- Schema-less design
- Structured data
- Cost-effective

---

## Table Storage Components
- Tables
- Entities
- Properties
- Partition keys
- Row keys

---

## Storage Security

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Storage Security Layers</text>
  <rect x="50" y="28" width="500" height="165" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="46" text-anchor="middle" font-size="10" font-weight="bold">Network Security: Firewalls, VNet rules, Private Endpoints</text>
  <rect x="70" y="55" width="460" height="125" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="73" text-anchor="middle" font-size="10" font-weight="bold">Authentication: Shared Key, SAS Tokens, Azure AD</text>
  <rect x="90" y="82" width="420" height="85" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="100" text-anchor="middle" font-size="10" font-weight="bold">Authorization: RBAC, ACLs, Stored Access Policies</text>
  <rect x="110" y="108" width="380" height="48" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="126" text-anchor="middle" font-size="10" font-weight="bold">Data Protection</text>
  <text x="300" y="142" text-anchor="middle" font-size="10">Encryption at rest (SSE) | Encryption in transit (HTTPS/TLS)</text>
  <text x="300" y="155" text-anchor="middle" font-size="10">Soft delete | Versioning | Immutable storage</text>
</svg>

---

## Authentication Methods
- Shared Key
- SAS tokens
- Azure AD
- Anonymous access
- Service endpoints

---

## Shared Access Signatures
- Account SAS
- Service SAS
- User delegation SAS
- Time-limited access
- Specific permissions

---

## Storage Networking
- Public endpoints
- Private endpoints
- Service endpoints
- Network rules
- Firewall settings

---

## Data Protection
- Soft delete
- Point-in-time restore
- Immutable storage
- Backup
- Replication

---

## Storage Monitoring
- Metrics
- Diagnostics
- Activity logs
- Alerts
- Insights

---

## Performance Tiers
- Standard performance
- Premium performance
- IOPS limits
- Throughput limits
- Latency targets

---

## Cost Optimization
- Access tiers
- Lifecycle management
- Reserved capacity
- Right-sizing
- Monitoring usage

---

## Storage Management Tools
- Azure Portal
- Azure CLI
- PowerShell
- Storage Explorer
- REST API

---

## Lifecycle Management
- Automated tiering
- Deletion rules
- Policy-based actions
- Cost optimization
- Data governance

---

## Data Migration
- AzCopy
- Storage Explorer
- Data Box
- Import/Export service
- Migration tools

---

## Backup and Recovery
- Snapshot management
- Geo-replication
- Disaster recovery
- Business continuity
- Recovery testing

---

## Storage Integration
- Azure Functions
- Logic Apps
- Event Grid
- Service Bus
- API Management

---

## Best Practices
- Performance optimization
- Security hardening
- Cost management
- Monitoring strategy
- Access patterns

---

## Compliance and Governance
- Data residency
- Encryption requirements
- Access auditing
- Regulatory compliance
- Data sovereignty

---

## Storage Patterns
- Content distribution
- Data archival
- Backup storage
- Application data
- Media storage

---

## Future Roadmap
- Storage updates
- New features
- Performance improvements
- Security enhancements
- Integration capabilities
