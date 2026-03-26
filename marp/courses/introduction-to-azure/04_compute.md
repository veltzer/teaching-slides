# Azure Compute Services

## Types of Compute Services

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_compute)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_compute)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_compute)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_compute)"/>
  <defs>
    <marker id="arrowd1_03_compute" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_compute)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_compute)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_03_compute)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_03_compute)"/>
  <defs>
    <marker id="arrowd3_03_compute" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
