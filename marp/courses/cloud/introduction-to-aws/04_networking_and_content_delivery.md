---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:networking
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:managers

---
# Networking and Content Delivery

---

## Networking in AWS
- Virtual networks you fully control
- Isolation, security, connectivity
- Mirrors traditional networking concepts
- Software-defined: change in minutes
- Foundation for every AWS architecture

---

## Amazon VPC Overview
- Virtual Private Cloud
- Logically isolated section of AWS
- You control the network configuration
- Subnets, route tables, gateways
- One or more VPCs per Region

---

## VPC CIDR Blocks
- Define IP address range for your VPC
- Example: 10.0.0.0/16 (65,536 addresses)
- Cannot overlap with other connected VPCs
- Choose carefully (cannot change later)
- Secondary CIDR blocks can be added

---

## VPC and Subnet CLI Example

```bash
# Create a VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create a public subnet
aws ec2 create-subnet \
  --vpc-id vpc-abc123 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

# Create a private subnet
aws ec2 create-subnet \
  --vpc-id vpc-abc123 \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1a
```

---

## Subnets
- Divide a VPC into smaller segments
- Each subnet lives in one Availability Zone
- Public subnet: has route to Internet Gateway
- Private subnet: no direct internet access
- Recommended: one public + one private per AZ

---

## VPC Components
- Route Tables: traffic routing rules
- Internet Gateway: internet access for public subnets
- NAT Gateway: outbound internet for private subnets
- Elastic IPs: static public IP addresses
- All configurable and automatable

---

## Internet Gateway
- Allows communication between VPC and internet
- Horizontally scaled, redundant, highly available
- One per VPC
- Attach to VPC, add route in public subnet route table
- No bandwidth constraints

---

## NAT Gateway
- Network Address Translation
- Allows private subnet instances to reach internet
- Blocks inbound internet traffic
- Managed service (no patching)
- Charged per hour and per GB processed

---

## Route Tables
- Rules that determine where traffic goes
- Each subnet associated with one route table
- Local route: traffic within VPC (automatic)
- Internet Gateway route: 0.0.0.0/0 -> igw-xxx
- NAT Gateway route: 0.0.0.0/0 -> nat-xxx

---

## Public vs Private Subnets
- Public: route to Internet Gateway, direct internet access
- Private: no direct internet route
- Web servers, load balancers -> public
- Databases, application servers -> private
- Defense in depth through network isolation

---

## VPC Architecture

![vpc_architecture](svg/courses/cloud/introduction-to-aws/04_networking_and_content_delivery/vpc_architecture.svg)

---

## Security Groups
- Instance-level virtual firewall
- Stateful: return traffic automatically allowed
- Allow rules only (no deny rules)
- Evaluate all rules before deciding
- Applied at the network interface level

---

## Security Group Rules
- Inbound: control incoming traffic
- Outbound: control outgoing traffic
- Specify protocol, port range, source/destination
- Source can be CIDR, IP, or another Security Group
- Changes take effect immediately

---

## Network ACLs
- Subnet-level firewall
- Stateless: must allow return traffic explicitly
- Allow and deny rules
- Rules evaluated in order by number
- Default NACL allows all traffic

---

## Security Groups vs NACLs
- Security Groups: instance-level, stateful, allow only
- NACLs: subnet-level, stateless, allow and deny
- Use Security Groups as primary defense
- Use NACLs for additional subnet-level control
- Both work together for defense in depth

---

## Security Groups vs NACLs

![security_groups_vs_nacls](svg/courses/cloud/introduction-to-aws/04_networking_and_content_delivery/security_groups_vs_nacls.svg)

---

## Elastic IP Addresses
- Static public IPv4 addresses
- Persist across instance stop/start
- Associated with an instance or network interface
- Charged when not associated with a running instance
- Limited to 5 per Region (can request more)

---

## Amazon Route 53
- Managed DNS service
- Domain name registration
- Health checking and routing
- 100% availability SLA
- Named after DNS port 53

---

## Route 53 Hosted Zones
- Public Hosted Zone: route internet traffic
- Private Hosted Zone: route within VPCs
- Contains DNS records (A, AAAA, CNAME, MX, etc.)
- Charged per hosted zone and per query
- Supports DNSSEC

---

## Route 53 Routing Policies
- Simple: single resource
- Weighted: distribute traffic by percentage
- Latency-based: route to lowest-latency Region
- Failover: active-passive failover
- Geolocation: route by user location
- Multivalue: return multiple healthy records

---

## Route 53 Record Example

```bash
# Create a weighted routing record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456 \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.example.com",
        "Type": "A",
        "SetIdentifier": "us-east",
        "Weight": 70,
        "TTL": 300,
        "ResourceRecords": [{"Value": "1.2.3.4"}]
      }
    }]
  }'
```

---

## Route 53 Health Checks
- Monitor endpoint health
- HTTP, HTTPS, or TCP checks
- Configurable interval and failure threshold
- Integrate with routing policies for failover
- CloudWatch alarms on health check status

---

## Amazon CloudFront
- Content Delivery Network (CDN)
- 400+ edge locations worldwide
- Caches content close to users
- Reduces latency for end users
- Integrates with S3, EC2, ELB, and external origins

---

## CloudFront Distributions
- Web distribution: HTTP/HTTPS content
- Origin: where content comes from (S3, ALB, custom)
- Behaviors: path patterns and caching rules
- Cache policies: TTL, headers, cookies
- Invalidation: clear cached content

---

## CloudFront Distribution Flow

![cloudfront_distribution](svg/courses/cloud/introduction-to-aws/04_networking_and_content_delivery/cloudfront_distribution.svg)

---

## CloudFront Security
- HTTPS with custom SSL certificates
- Origin Access Control (OAC) for S3
- AWS WAF integration (web application firewall)
- AWS Shield for DDoS protection
- Geo-restriction: block by country

---

## CloudFront Use Cases
- Static asset delivery (images, CSS, JS)
- Dynamic content acceleration
- Video streaming (live and on-demand)
- API acceleration
- Whole-site delivery

---

## VPC Peering
- Connect two VPCs privately
- Traffic stays on AWS backbone
- Works across Regions and accounts
- No transitive peering
- Non-overlapping CIDR blocks required

---

## VPC Endpoints
- Private connection to AWS services
- Traffic stays within AWS network
- Gateway Endpoints: S3, DynamoDB (free)
- Interface Endpoints: most other services (charged)
- Avoids NAT Gateway costs and internet exposure

---

## AWS Transit Gateway
- Hub-and-spoke connectivity
- Connect multiple VPCs and on-premises networks
- Single gateway, simplified management
- Route tables for traffic control
- Scales to thousands of VPCs
