# Azure Compute Services

## Types of Compute Services

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Azure Compute Services Spectrum</text>
  <text x="60" y="45" text-anchor="middle" font-size="10" fill="#555">More Control</text>
  <text x="540" y="45" text-anchor="middle" font-size="10" fill="#555">Less Control</text>
  <line x1="110" y1="40" x2="480" y2="40" stroke="#999" stroke-width="1" marker-end="url(#arrowd0_03_compute)"/>
  <rect x="15" y="55" width="120" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="75" text-anchor="middle" font-size="11" font-weight="bold">VMs</text>
  <text x="75" y="90" text-anchor="middle" font-size="10">IaaS</text>
  <text x="75" y="105" text-anchor="middle" font-size="10">Full OS control</text>
  <text x="75" y="118" text-anchor="middle" font-size="10">Custom software</text>
  <rect x="155" y="55" width="120" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="215" y="75" text-anchor="middle" font-size="11" font-weight="bold">App Service</text>
  <text x="215" y="90" text-anchor="middle" font-size="10">PaaS</text>
  <text x="215" y="105" text-anchor="middle" font-size="10">Web apps, APIs</text>
  <text x="215" y="118" text-anchor="middle" font-size="10">Managed runtime</text>
  <rect x="295" y="55" width="120" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="355" y="75" text-anchor="middle" font-size="11" font-weight="bold">AKS</text>
  <text x="355" y="90" text-anchor="middle" font-size="10">Containers</text>
  <text x="355" y="105" text-anchor="middle" font-size="10">Kubernetes</text>
  <text x="355" y="118" text-anchor="middle" font-size="10">Orchestration</text>
  <rect x="435" y="55" width="150" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="75" text-anchor="middle" font-size="11" font-weight="bold">Azure Functions</text>
  <text x="510" y="90" text-anchor="middle" font-size="10">Serverless</text>
  <text x="510" y="105" text-anchor="middle" font-size="10">Event-driven</text>
  <text x="510" y="118" text-anchor="middle" font-size="10">Pay-per-execution</text>
  <rect x="100" y="145" width="400" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="163" text-anchor="middle" font-size="10">Also: Container Instances (ACI) | Azure Batch | VM Scale Sets</text>
  <text x="300" y="178" text-anchor="middle" font-size="10">Choose based on control needs, scaling requirements, and cost</text>
  <defs>
    <marker id="arrowd0_03_compute" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Understanding Azure Virtual Machines
- Infrastructure as a Service
- Full control over OS
- Custom software
- Maximum flexibility

---

## VM Size Categories
1. General purpose
1. Compute optimized
1. Memory optimized
1. Storage optimized
1. GPU enabled
1. High performance

---

## Choosing the Right VM Size

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">VM Size Categories Decision Guide</text>
  <rect x="10" y="30" width="170" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="50" text-anchor="middle" font-size="11" font-weight="bold">B/D-series</text>
  <text x="95" y="65" text-anchor="middle" font-size="10">General Purpose</text>
  <text x="95" y="78" text-anchor="middle" font-size="9">Web servers, dev/test</text>
  <rect x="210" y="30" width="170" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="50" text-anchor="middle" font-size="11" font-weight="bold">F-series</text>
  <text x="295" y="65" text-anchor="middle" font-size="10">Compute Optimized</text>
  <text x="295" y="78" text-anchor="middle" font-size="9">Batch, gaming, analytics</text>
  <rect x="410" y="30" width="170" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="50" text-anchor="middle" font-size="11" font-weight="bold">E/M-series</text>
  <text x="495" y="65" text-anchor="middle" font-size="10">Memory Optimized</text>
  <text x="495" y="78" text-anchor="middle" font-size="9">Databases, caching</text>
  <rect x="10" y="100" width="170" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="120" text-anchor="middle" font-size="11" font-weight="bold">L-series</text>
  <text x="95" y="135" text-anchor="middle" font-size="10">Storage Optimized</text>
  <text x="95" y="148" text-anchor="middle" font-size="9">Big data, SQL, NoSQL</text>
  <rect x="210" y="100" width="170" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="120" text-anchor="middle" font-size="11" font-weight="bold">N-series</text>
  <text x="295" y="135" text-anchor="middle" font-size="10">GPU Enabled</text>
  <text x="295" y="148" text-anchor="middle" font-size="9">ML, rendering, HPC</text>
  <rect x="410" y="100" width="170" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="120" text-anchor="middle" font-size="11" font-weight="bold">H-series</text>
  <text x="495" y="135" text-anchor="middle" font-size="10">High Performance</text>
  <text x="495" y="148" text-anchor="middle" font-size="9">Simulations, modeling</text>
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#555">Tip: Start small, monitor, then right-size based on actual usage</text>
</svg>

---

## VM Best Practices
- Right-size VMs
- Use availability sets
- Implement backup strategy
- Monitor performance
- Apply security policies

---

## Creating a Virtual Machine
1. Choose subscription
1. Select resource group
1. Define VM name
1. Pick region
1. Select image
1. Configure size

---

## VM Configuration Options
- Operating System
- Authentication
- Inbound ports
- Networking
- Management
- Monitoring

---

## VM Storage Options
- OS disk
- Temporary disk
- Data disks
- Premium vs Standard
- Managed vs Unmanaged

---

## VM Networking
- Virtual networks
- Network interfaces
- Public IP
- Network security groups
- Load balancers

---

## VM Security
- Disk encryption
- Network security groups
- Azure Security Center
- Update management
- Antimalware

---

## VM Scale Sets
- Automatic scaling
- Load balanced VMs
- High availability
- Large-scale applications

---

## Scale Set Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">VM Scale Set Architecture</text>
  <rect x="200" y="25" width="200" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="47" text-anchor="middle" font-size="11" font-weight="bold">Load Balancer</text>
  <line x1="230" y1="60" x2="100" y2="80" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_03_compute)"/>
  <line x1="300" y1="60" x2="300" y2="80" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_03_compute)"/>
  <line x1="370" y1="60" x2="500" y2="80" stroke="#333" stroke-width="1" marker-end="url(#arrowd2_03_compute)"/>
  <rect x="30" y="80" width="130" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="100" text-anchor="middle" font-size="11" font-weight="bold">VM Instance 1</text>
  <text x="95" y="115" text-anchor="middle" font-size="10">Running</text>
  <rect x="235" y="80" width="130" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="100" text-anchor="middle" font-size="11" font-weight="bold">VM Instance 2</text>
  <text x="300" y="115" text-anchor="middle" font-size="10">Running</text>
  <rect x="440" y="80" width="130" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="100" text-anchor="middle" font-size="11" font-weight="bold">VM Instance N</text>
  <text x="505" y="115" text-anchor="middle" font-size="10">Auto-scaled</text>
  <rect x="100" y="145" width="180" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="190" y="162" text-anchor="middle" font-size="10" font-weight="bold">Scaling Rules</text>
  <text x="190" y="177" text-anchor="middle" font-size="10">CPU > 75% = scale out</text>
  <rect x="320" y="145" width="180" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="410" y="162" text-anchor="middle" font-size="10" font-weight="bold">Health Probes</text>
  <text x="410" y="177" text-anchor="middle" font-size="10">Auto-replace unhealthy</text>
  <defs>
    <marker id="arrowd2_03_compute" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Configuring Scale Sets
- Instance count
- Scaling rules
- Load balancing
- Update policy
- Health monitoring

---

## Azure App Service
- Platform as a Service
- Web applications
- API applications
- Mobile backends
- Containerized apps

---

## App Service Plans
- Shared compute
- Dedicated compute
- Premium
- Isolated
- Consumption

---

## App Service Features
- Auto-scaling
- Deployment slots
- Custom domains
- SSL certificates
- Authentication

---

## Deployment Options
- Visual Studio
- Git
- FTP
- ZIP deploy
- Container registry

---

## App Service Networking
- Inbound traffic
- Outbound traffic
- Network integration
- Private endpoints
- Hybrid connections

---

## Container Services Overview

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Azure Container Services Overview</text>
  <rect x="10" y="30" width="180" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="50" text-anchor="middle" font-size="11" font-weight="bold">Container Instances</text>
  <text x="100" y="66" text-anchor="middle" font-size="10">Simplest option</text>
  <text x="100" y="80" text-anchor="middle" font-size="10">Single container/group</text>
  <text x="100" y="94" text-anchor="middle" font-size="10">Per-second billing</text>
  <rect x="210" y="30" width="180" height="75" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">AKS (Kubernetes)</text>
  <text x="300" y="66" text-anchor="middle" font-size="10">Full orchestration</text>
  <text x="300" y="80" text-anchor="middle" font-size="10">Auto-scaling, self-heal</text>
  <text x="300" y="94" text-anchor="middle" font-size="10">Microservices</text>
  <rect x="410" y="30" width="180" height="75" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="50" text-anchor="middle" font-size="11" font-weight="bold">App Service</text>
  <text x="500" y="66" text-anchor="middle" font-size="10">Container support</text>
  <text x="500" y="80" text-anchor="middle" font-size="10">PaaS simplicity</text>
  <text x="500" y="94" text-anchor="middle" font-size="10">CI/CD built-in</text>
  <rect x="80" y="125" width="440" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="145" text-anchor="middle" font-size="11" font-weight="bold">Azure Container Registry (ACR)</text>
  <text x="300" y="162" text-anchor="middle" font-size="10">Private Docker registry for all container services</text>
  <text x="300" y="177" text-anchor="middle" font-size="10">Geo-replication | Vulnerability scanning | Build tasks</text>
</svg>

---

## Azure Kubernetes Service
- Managed Kubernetes
- Container orchestration
- Auto-scaling
- Self-healing
- Load balancing

---

## AKS Architecture
- Control plane
- Node pools
- Pods
- Services
- Storage

---

## Container Instances
- Fast deployment
- Per-second billing
- No orchestration
- Simple applications
- Batch processing

---

## Azure Functions
- Serverless compute
- Event-driven
- Pay-per-execution
- Automatic scaling
- Multiple languages

---

## Function Triggers
- HTTP
- Timer
- Queue
- Blob storage
- Event hub
- Service Bus

---

## Function Bindings
- Input bindings
- Output bindings
- Multiple bindings
- Custom bindings
- Chain functions

---

## Durable Functions
- Stateful functions
- Workflow orchestration
- Complex patterns
- Long-running tasks
- Error handling

---

## Azure Batch
- Large-scale parallel
- HPC applications
- Job scheduling
- Resource management
- Auto-scaling

---

## Cost Management
- Resource optimization
- Auto-shutdown
- Reserved instances
- Spot instances
- Budget alerts

---

## Monitoring Compute
- Azure Monitor
- Application Insights
- Log Analytics
- Metrics
- Alerts

---

## Disaster Recovery
- Backup solutions
- Site recovery
- High availability
- Business continuity
- Recovery testing

---

## Performance Optimization
- Right-sizing
- Scaling policies
- Load testing
- Performance testing
- Optimization tools
