---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:iaas
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:managers

---
# Core Compute Services

---

## Compute in the Cloud
- Run applications without owning hardware
- Multiple compute models available
- Virtual machines, containers, serverless
- Choose the model that fits your workload
- Scale compute capacity up and down

---

## Amazon EC2 Overview
- Elastic Compute Cloud
- Virtual servers in the cloud
- Resizable compute capacity
- Complete control over instances
- Pay per second of usage

---

## EC2 Instance Lifecycle: Details
1. Launch (from an AMI)
1. Pending (booting up)
1. Running (billing starts)
1. Stopping / Stopped (no compute charges, EBS charges remain)
1. Shutting down / Terminated (instance deleted)

---

## EC2 Instance Lifecycle

![ec2_instance_lifecycle](svg/courses/cloud/introduction-to-aws/02_core_compute_services/ec2_instance_lifecycle.svg)

---

## Amazon Machine Images (AMIs)
- Pre-configured templates for instances
- Contains OS, application server, applications
- AWS provides many standard AMIs
- AWS Marketplace: third-party AMIs
- Region-specific (can be copied across Regions)

---

## Creating Custom AMIs
- Launch an instance, configure it
- Create an image from the running instance
- Use that AMI to launch identical instances
- Golden image pattern for consistency
- Faster launches than bootstrapping

---

## Instance Families At A Glance

![instance_families](svg/courses/cloud/introduction-to-aws/02_core_compute_services/instance_families.svg)

---

## EC2 Instance Types: General Purpose
- t3, t3a: burstable performance, web servers
- m6i, m6a: balanced compute/memory/networking
- Good for web applications, small databases
- t3 accumulates CPU credits when idle
- Most common starting point

---

## EC2 Instance Types: Compute Optimized
- c6i, c6a, c7g: high-performance processors
- Batch processing
- Media transcoding
- Scientific modeling
- Machine learning inference

---

## EC2 Instance Types: Memory Optimized
- r6i, r6a: high memory-to-CPU ratio
- x2idn: up to 4 TB of RAM
- In-memory databases (Redis, Memcached)
- Real-time big data analytics
- High-performance databases

---

## EC2 Instance Types: Storage and Accelerated
- i3, i4i: high sequential read/write (NVMe)
- d3: dense HDD storage, data warehousing
- p4d, p5: GPU instances for ML training
- inf2: AWS Inferentia for ML inference
- g5: graphics-intensive applications

---

## Instance Type Naming Convention
- Example: m6i.xlarge
- m = family (General Purpose)
- 6 = generation
- i = processor (Intel)
- xlarge = size (vCPUs and memory)

---

## Choosing the Right Instance Type
- Match type to workload requirements
- Consider CPU, memory, storage, networking
- Start small, scale up as needed
- Use CloudWatch metrics to right-size
- Benchmark before committing

---

## EC2 Pricing: On-Demand
- Pay by the second (minimum 60 seconds)
- No upfront commitment
- Most flexible option
- Best for unpredictable workloads
- Full price, no discounts

---

## EC2 Pricing: Reserved Instances
- 1 or 3 year commitment
- Up to 72% savings vs On-Demand
- Standard RI: fixed instance type
- Convertible RI: can change instance type
- Payment: all upfront, partial, or no upfront

---

## EC2 Pricing: Savings Plans
- Commit to $/hour of usage for 1 or 3 years
- Compute Savings Plan: any instance family, Region, OS
- EC2 Instance Savings Plan: specific family and Region
- More flexible than Reserved Instances
- Up to 66% savings

---

## EC2 Pricing: Spot Instances
- Bid on unused EC2 capacity
- Up to 90% savings vs On-Demand
- Can be interrupted with 2-minute warning
- Great for fault-tolerant workloads
- Batch processing, CI/CD, data analysis

---

## EC2 Pricing: Dedicated
- Dedicated Instances: hardware not shared with others
- Dedicated Hosts: entire physical server
- Compliance or licensing requirements
- Most expensive option
- Use only when required

---

## EC2 Pricing Comparison

![ec2_pricing_comparison](svg/courses/cloud/introduction-to-aws/02_core_compute_services/ec2_pricing_comparison.svg)

---

## Key Pairs
- SSH access to Linux instances
- RDP access to Windows instances
- Public key stored on instance
- Private key kept by you
- Create or import at launch time

---

## Security Groups
- Instance-level virtual firewall
- Stateful: return traffic automatically allowed
- Allow rules only (no deny rules)
- Default: deny all inbound, allow all outbound
- Can reference other Security Groups

---

## Security Group Examples
- Web server: allow port 80/443 from 0.0.0.0/0
- SSH access: allow port 22 from your IP only
- Database: allow port 3306 from web server SG
- Multiple SGs can be attached to one instance
- Changes take effect immediately

---

## User Data and Metadata
- User Data: bootstrap script run at first launch
- Install packages, configure software
- Instance Metadata: info about the instance
- Available at http://169.254.169.254/latest/meta-data/
- Retrieve instance ID, IP, IAM role credentials

---

## User Data Bootstrap Script

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from $(hostname)</h1>" \
  > /var/www/html/index.html
```

---

## Security Group CLI Example

```bash
# Create a security group
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Allow HTTP and SSH"

# Allow HTTP from anywhere
aws ec2 authorize-security-group-ingress \
  --group-name web-sg \
  --protocol tcp --port 80 \
  --cidr 0.0.0.0/0
```

---

## Elastic Load Balancing (ELB)
- Distributes incoming traffic across targets
- Increases availability and fault tolerance
- Health checks for target instances
- Integrates with Auto Scaling
- Managed service (no servers to maintain)

---

## Types of Load Balancers
- Application Load Balancer (Layer 7): HTTP/HTTPS
- Network Load Balancer (Layer 4): TCP/UDP, ultra-low latency
- Gateway Load Balancer (Layer 3): third-party appliances
- Classic Load Balancer (legacy): avoid for new deployments

---

## ALB Features
- Path-based routing (/api, /images)
- Host-based routing (a.example.com, b.example.com)
- Sticky sessions
- WebSocket support
- Native integration with WAF

---

## Auto Scaling Overview
- Automatically adjust number of EC2 instances
- Scale out when demand increases
- Scale in when demand decreases
- Maintain desired capacity
- Integrates with ELB for traffic distribution

---

## Auto Scaling Components
- Launch Template: instance configuration
- Auto Scaling Group: collection of instances
- Scaling Policies: when and how to scale
- Cooldown Periods: prevent rapid scaling
- Scheduled Scaling: predictable demand patterns

---

## Auto Scaling Architecture

![auto_scaling_architecture](svg/courses/cloud/introduction-to-aws/02_core_compute_services/auto_scaling_architecture.svg)

---

## Scaling Policy Types
- Target Tracking: maintain a metric at a target (e.g., 50% CPU)
- Step Scaling: scale by amount based on alarm severity
- Simple Scaling: scale by fixed amount on alarm
- Predictive Scaling: ML-based forecast
- Target Tracking is the recommended starting point

---

## EC2 Best Practices
- Use the latest generation instance types
- Right-size instances based on actual usage
- Use Auto Scaling for variable workloads
- Spread across multiple Availability Zones
- Use Spot Instances for fault-tolerant workloads
- Tag all resources for cost tracking
