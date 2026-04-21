---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:azure
  - infrastructure:gcp
  - concepts:architecture
level: advanced
category: cloud
audience:
  - audiences:architects
  - audiences:managers

---
# Networking Across Clouds

---

## Why Cross-Cloud Networking Is Hard
- Each provider has its own networking model
- No native peering between AWS, Azure, and GCP
- Data transfer between clouds traverses the public internet by default
- Latency, bandwidth, and cost are all concerns
- Networking is the glue — and the bottleneck — of multi-cloud

---

## Cross-Cloud Connectivity Options
- Public internet with TLS (simplest, highest latency)
- Site-to-site VPN tunnels (encrypted, moderate latency)
- Dedicated interconnects via colocation (lowest latency, highest cost)
- SD-WAN solutions (managed overlay networks)
- Third-party network fabrics (Aviatrix, Alkira, Prosimo)

---

## Site-to-Site VPN
- IPsec tunnels between cloud VPCs/VNets
- AWS: Virtual Private Gateway or Transit Gateway
- Azure: VPN Gateway
- GCP: Cloud VPN (HA VPN for 99.99% SLA)
- Encrypted traffic over public internet
- Bandwidth limited to ~1.25 Gbps per tunnel (varies by provider)

---

## Dedicated Interconnects
- AWS: Direct Connect
- Azure: ExpressRoute
- GCP: Cloud Interconnect (Dedicated or Partner)
- Requires physical cross-connect at a colocation facility
- 1-100 Gbps links, lower latency than VPN
- Equinix, Megaport, and others offer multi-cloud cross-connects

---

## Cross-Cloud Networking

![networking](svg/courses/cloud/multi-cloud-strategy/06_networking/cross_cloud_networking.svg)

---

## Colocation as Multi-Cloud Hub
- Place network equipment in a carrier-neutral data center
- Establish direct connections to multiple clouds from one location
- Reduce latency between clouds to sub-millisecond
- Exchange data between clouds without egress fees
- Equinix Fabric, Megaport, PacketFabric offer this model

---

## Terraform: Cross-Cloud VPN (AWS Side)

```hcl
resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "multi-cloud-vpn-gw"
  }
}

resource "aws_customer_gateway" "gcp" {
  bgp_asn    = 65000
  ip_address = google_compute_ha_vpn_gateway.main.vpn_interfaces[0].ip_address
  type       = "ipsec.1"

  tags = {
    Name = "gcp-customer-gw"
  }
}

resource "aws_vpn_connection" "to_gcp" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.gcp.id
  type                = "ipsec.1"
  static_routes_only  = false

  tags = {
    Name = "aws-to-gcp-vpn"
  }
}
```

---

## Terraform: Cross-Cloud VPN (GCP Side)

```hcl
resource "google_compute_ha_vpn_gateway" "main" {
  name    = "multi-cloud-vpn-gw"
  network = google_compute_network.main.id
  region  = "us-central1"
}

resource "google_compute_external_vpn_gateway" "aws" {
  name            = "aws-vpn-gw"
  redundancy_type = "TWO_IPS_REDUNDANCY"

  interface {
    id         = 0
    ip_address = aws_vpn_connection.to_gcp.tunnel1_address
  }
  interface {
    id         = 1
    ip_address = aws_vpn_connection.to_gcp.tunnel2_address
  }
}

resource "google_compute_vpn_tunnel" "to_aws" {
  name                  = "gcp-to-aws-tunnel"
  vpn_gateway           = google_compute_ha_vpn_gateway.main.id
  peer_external_gateway = google_compute_external_vpn_gateway.aws.id
  shared_secret         = var.vpn_shared_secret
  vpn_gateway_interface = 0

  peer_external_gateway_interface = 0
}
```

---

## DNS and Traffic Management
- Global DNS for intelligent routing across clouds
- AWS Route 53, Azure Traffic Manager, GCP Cloud DNS
- Third-party: Cloudflare, NS1, Akamai
- Routing policies: latency-based, geographic, weighted, failover
- DNS is often the simplest multi-cloud load balancing mechanism

---

## DNS Traffic Management

![dns](svg/courses/cloud/multi-cloud-strategy/06_networking/dns_traffic_management.svg)

---

## DNS-Based Multi-Cloud Routing

```json
{
  "Comment": "Multi-cloud weighted routing",
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "api.example.com",
        "Type": "A",
        "SetIdentifier": "aws-primary",
        "Weight": 70,
        "AliasTarget": {
          "HostedZoneId": "Z2FDTNDATAQYW2",
          "DNSName": "aws-alb-123.us-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": true
        }
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "api.example.com",
        "Type": "A",
        "SetIdentifier": "gcp-secondary",
        "Weight": 30,
        "AliasTarget": {
          "HostedZoneId": "Z2FDTNDATAQYW2",
          "DNSName": "gcp-lb-456.example.com",
          "EvaluateTargetHealth": true
        }
      }
    }
  ]
}
```

---

## Data Transfer Costs
- Egress fees are the hidden tax of multi-cloud
- AWS: $0.09/GB to internet, $0.02/GB cross-region
- Azure: $0.087/GB to internet
- GCP: $0.12/GB to internet (premium tier)
- Inter-cloud transfer: typically full egress rate
- These costs add up quickly at scale

---

## Minimizing Data Transfer Costs
- Keep tightly coupled services on the same cloud
- Use data compression for cross-cloud communication
- Cache aggressively to reduce repeated transfers
- Batch data transfers during off-peak hours
- Consider colocation for high-volume exchange

---

## Network Architecture Patterns
- Hub-and-spoke: one cloud as hub, others as spokes
- Mesh: direct connections between all clouds
- Transit: dedicated transit network connecting all clouds
- Segmented: isolated workloads with minimal cross-cloud traffic
- Choose based on traffic patterns and latency requirements

---

## Latency Considerations
- Same region, same cloud: sub-millisecond
- Cross-region, same cloud: 10-100ms (depending on distance)
- Cross-cloud via VPN: 5-20ms additional overhead
- Cross-cloud via internet: variable, 10-50ms+ additional
- Application architecture must tolerate cross-cloud latency

---

## Security Across Cloud Networks
- Encrypt all cross-cloud traffic (VPN provides this)
- Implement zero-trust networking principles
- Centralize firewall policy management
- Use cloud-native tools per provider for intra-cloud security
- Third-party tools (Palo Alto, Fortinet) for unified policy

---

## Service Mesh for Multi-Cloud
- Istio, Linkerd, Consul Connect
- Unified service-to-service communication
- mTLS encryption between all services
- Traffic management, observability, and policy
- Multi-cluster and multi-cloud support built in
