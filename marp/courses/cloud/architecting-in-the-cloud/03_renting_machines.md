---
tags:
  - infrastructure:cloud
  - infrastructure:iaas
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---

# Renting Machines

---

## What Are Machines in the Cloud?
- Virtual machines running on shared physical hardware
- Hypervisor isolates tenants
- You get a slice of CPU, memory, storage, network
- Appears as a dedicated server to the OS
- Start and stop in seconds to minutes

---

## Virtual Machine Internals
- Host machine runs the hypervisor (Xen, KVM, Nitro)
- VMs share physical resources
- NUMA awareness for performance-sensitive workloads
- Hardware-assisted virtualization
- Noisy neighbor risk (mitigated by modern hypervisors)

---

## VM Internals

![vm_internals](svg/courses/cloud/architecting-in-the-cloud/03_renting_machines/vm_internals.svg)

---

## What is Your Responsibility?
- OS patches and updates
- Application installation and configuration
- Security hardening
- Monitoring and log management
- Backup strategy for data on the VM

---

## Provider Responsibility
- Physical hardware maintenance
- Hypervisor patches
- Network infrastructure
- Power, cooling, physical security
- Hardware replacement on failure

---

## Should You Get Your Own Machine?
- Default: shared tenancy (multi-tenant)
- Dedicated Instances: hardware not shared
- Dedicated Hosts: entire physical server
- Bare metal: no hypervisor
- Most workloads are fine with shared tenancy

---

## When to Use Dedicated/Bare Metal
- Licensing requirements (per-socket, per-core)
- Compliance requirements (isolated hardware)
- Performance-sensitive workloads (no noisy neighbors)
- Bring-your-own-license scenarios
- Cost: significantly more expensive

---

## Bare Metal Instances
- Physical server, no hypervisor
- AWS i3.metal, Azure dedicated hosts, GCP sole-tenant
- Maximum performance, direct hardware access
- Required for some specialized workloads
- Licensing, compliance, or performance requirements

---

## Choosing Between Instance Families
- General purpose: web servers, app servers, dev environments
- Compute optimized: batch processing, HPC, gaming
- Memory optimized: in-memory databases, real-time analytics
- Storage optimized: data warehousing, Hadoop
- Match workload characteristics to family

---

## Instance Family Selection

![instance_families](svg/courses/cloud/architecting-in-the-cloud/03_renting_machines/instance_family_selection.svg)

---

## Instance Sizing Strategy
- Start with the smallest size that meets requirements
- Monitor CPU, memory, network for 2-4 weeks
- Right-size based on actual utilization
- Use provider recommendations (Compute Optimizer)
- Re-evaluate quarterly

---

## Burstable Instances (T-series)
- Baseline CPU + burst credits
- Accumulate credits when CPU is low
- Spend credits during burst periods
- Unlimited mode: burst beyond credits (pay per vCPU-second)
- Great for variable workloads (web servers, dev environments)

---

## GPU and Accelerated Instances
- NVIDIA GPUs for ML training and inference
- AWS p4d/p5, Azure NC/ND, GCP A2/A3
- Also for rendering, HPC, scientific computing
- Very expensive: hundreds of $/hour
- Consider spot instances for training workloads

---

## EC2 Nitro System
- AWS custom hypervisor
- Hardware-level networking and storage
- Improved performance and security
- Enables bare metal instances
- Foundation for all modern AWS instances

---

## Security on Your Own Machine
- Harden the OS (CIS benchmarks)
- Disable unnecessary services
- Patch regularly and automatically
- Use Security Groups + host-based firewall
- Never expose management ports to the internet

---

## Instance Hardening Checklist
1. Use latest AMI/image with patches
1. Enable automatic security updates
1. Remove default accounts and keys
1. Configure host-based firewall
1. Install monitoring and log agents
1. Enable disk encryption

---

## Where Is My Machine, Anyway?
- You choose the Region
- You choose (or let the provider choose) the AZ
- You do not know the exact physical location
- Spread across AZs for availability
- Latency between AZs: low (1-2ms)

---

## Regions and Placement
- Choose Region for latency, compliance, cost
- Not all instance types available in all Regions
- Pricing varies by Region (US East is often cheapest)
- Placement Groups for network performance
- Cluster: low latency; Spread: fault isolation

---

## Cost Issues
- Instance pricing: on-demand, reserved, spot, savings plans
- Running instances always cost money (even idle)
- Stopped instances: no compute charge, but EBS charges remain
- Data transfer between AZs: charged
- Right-size and auto-scale to minimize waste

---

## Cost Optimization for Compute
- Right-size: match instance to actual utilization
- Use latest generation (better price/performance)
- Auto-scale: don't run instances you don't need
- Spot instances for interruptible workloads
- Reserved/Savings Plans for steady-state

---

## Organizing Your Machines
- Tags for identification (Name, Environment, Team)
- Resource Groups or naming conventions
- Auto Scaling Groups for fleets
- Infrastructure as Code for reproducibility
- Inventory management with SSM or Config

---

## Naming Conventions
- Consistent and informative
- Include: environment, service, role, index
- Example: prod-api-web-001
- Automated via launch templates
- Don't rely on names for automation (use tags)

---

## Instance Metadata and User Data
- Metadata service: instance ID, IP, IAM role, Region
- User Data: bootstrap script on first launch
- Install agents, configure software, join clusters
- IMDSv2 for secure metadata access
- Avoid storing secrets in user data

---

## Querying Instance Metadata

```bash
# IMDSv2 (recommended - token-based)
TOKEN=$(curl -s -X PUT \
  "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 300")

curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id

curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/local-ipv4
```

---

## Disks for Your Machines
- Boot volume: OS and application binaries
- Data volumes: application data, databases
- Ephemeral storage: temporary, lost on stop (instance store)
- EBS: persistent, survives stop/start
- Choose volume type based on IOPS and throughput needs

---

## EBS Volume Types Recap
- gp3: general purpose, most workloads (3,000 IOPS baseline)
- io2: high IOPS for databases (up to 64,000 IOPS)
- st1: throughput-optimized HDD (big data sequential reads)
- sc1: cold HDD (infrequent access, lowest cost)
- Instance Store: NVMe, highest performance, ephemeral

---

## Instance Store vs EBS
- Instance Store: physically attached, highest IOPS
- Instance Store: data lost on stop/terminate
- EBS: network-attached, persistent
- EBS: snapshots for backup
- Use instance store for caches and temp data

---

## EBS vs Instance Store

![ebs_store](svg/courses/cloud/architecting-in-the-cloud/03_renting_machines/ebs_vs_instance_store.svg)

---

## Snapshots and Backups
- EBS snapshots: point-in-time backup to S3
- Incremental: only changed blocks stored
- Automate with Data Lifecycle Manager
- Copy across Regions for DR
- Create AMIs from snapshots for cloning

---

## Create Snapshot and AMI

```bash
# Create a snapshot of an EBS volume
aws ec2 create-snapshot \
  --volume-id vol-abc123 \
  --description "Backup before upgrade"

# Create an AMI from a running instance
aws ec2 create-image \
  --instance-id i-0abc123 \
  --name "web-golden-v2.1" \
  --no-reboot
```

---

## Machine Images (AMIs/Images)
- Template for launching instances
- Contains OS, patches, applications, configuration
- Golden image pattern: pre-baked and tested
- Automate image building (Packer, EC2 Image Builder)
- Version and test images like code

---

## Golden Image vs Bootstrap: Details
- Golden image: everything pre-installed, fast launch
- Bootstrap: install at launch via user data, slow but flexible
- Hybrid: golden image + light bootstrap for configuration
- Golden images are preferred for production
- Bootstrap for development and experimentation

---

## Golden Image vs Bootstrap

![golden_image](svg/courses/cloud/architecting-in-the-cloud/03_renting_machines/golden_image_vs_bootstrap.svg)

---

## Fleet Management
- Manage hundreds or thousands of instances
- AWS Systems Manager, Azure Update Management
- Patch management across the fleet
- Run commands remotely (no SSH needed)
- Inventory and compliance tracking

---

## Spot Instances for Cost Optimization
- Use spare capacity at up to 90% discount
- 2-minute interruption notice (AWS)
- Great for batch processing, CI/CD, rendering
- Diversify across instance types and AZs
- Combine with on-demand for reliability

---

## Reserved Instances and Savings Plans
- Commit for 1 or 3 years for significant discounts
- Up to 72% savings vs on-demand
- Savings Plans: flexible across instance families
- Reserved Instances: specific instance type
- Commit to baseline, use on-demand/spot for peaks

---

## Instance Lifecycle Management
- Auto Scaling Groups manage instance lifecycle
- Launch Template defines configuration
- Scale out on demand, scale in when idle
- Replace unhealthy instances automatically
- Rolling updates for new AMIs

---

## Monitoring Your Machines
- CloudWatch metrics: CPU, network, disk
- CloudWatch Agent: memory, disk space (OS-level)
- Application-level metrics
- Set alarms on critical thresholds
- Dashboards for fleet-wide visibility

---

## Automation with Systems Manager
- Run Command: execute scripts without SSH
- Patch Manager: automated OS patching
- State Manager: enforce desired configuration
- Session Manager: browser-based terminal
- Maintenance Windows: scheduled operations

---

## Immutable Infrastructure
- Don't patch running instances
- Build new AMI, replace instances
- Infrastructure as Code defines everything
- Rollback by deploying previous AMI
- Eliminates configuration drift

---

## When NOT to Use VMs
- Stateless microservices: consider containers
- Event-driven workloads: consider serverless
- Simple web apps: consider PaaS
- VMs have the most overhead to manage
- Right tool for the right workload

---

## Placement Groups
- Cluster: low latency, high throughput between instances
- Spread: instances on different hardware (fault isolation)
- Partition: large distributed workloads (Hadoop, Kafka)
- Choose based on workload requirements
- Free to use, constraints on instance count

---

## Network Enhanced Instances
- Enhanced networking: higher bandwidth, lower latency
- ENA (Elastic Network Adapter): up to 100 Gbps
- EFA (Elastic Fabric Adapter): HPC, ML training
- Required for compute-intensive distributed workloads
- Available on most current-gen instance types

---

## Instance Profiles and IAM Roles
- Attach IAM role to EC2 instance via instance profile
- Applications get temporary credentials automatically
- No access keys in code or configuration
- Credentials rotated automatically
- Always use instance profiles, never embedded keys

---

## Tagging Strategy for Instances
- Name: human-readable identifier
- Environment: dev, staging, prod
- Team/Owner: accountability
- Project/CostCenter: cost allocation
- AutoShutdown: automation trigger

---

## Scheduled Instances
- Schedule non-production to stop at night and weekends
- Save 65-70% on dev/test environments
- AWS Instance Scheduler or Lambda + CloudWatch Events
- Tag-based: machines opt in to scheduling
- Exception handling for overnight jobs

---

## Windows Instances
- Full Windows Server support
- RDP access instead of SSH
- License included in instance price (or BYOL)
- Active Directory integration
- Systems Manager for management (no RDP needed)

---

## Linux Instance Best Practices
- Use Amazon Linux 2023 or Ubuntu LTS
- Enable SSM Agent for remote management
- Disable SSH password authentication
- Use Session Manager instead of SSH when possible
- CloudWatch Agent for OS-level metrics

---

## Cost Reporting for Compute
- Tag all instances for cost allocation
- Use Cost Explorer to analyze compute spend
- Identify idle and underutilized instances
- Track on-demand vs reserved vs spot mix
- Set budget alerts per team or project

---

## Compute Architecture Decision Tree
1. Can it be serverless? -> Lambda/Functions
1. Does it need containers? -> EKS/ECS/AKS/GKE
1. Does it need PaaS? -> Beanstalk/App Service
1. Does it need full OS control? -> EC2/VMs
1. Start simple, evolve as needed

---

## Compute Decision Tree

![compute_tree](svg/courses/cloud/architecting-in-the-cloud/03_renting_machines/compute_decision_tree.svg)

---

## Key Takeaways
- VMs in the cloud are flexible but still require management
- Secure, patch, and monitor your machines
- Choose the right instance type and size for your workload
- Organize with tags, automate with IaC
- Consider alternatives (containers, serverless) before defaulting to VMs
