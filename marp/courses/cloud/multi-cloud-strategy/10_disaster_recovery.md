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

# Disaster Recovery in Multi-Cloud

---

## DR Strategies

![dr_strategies](svg/courses/cloud/multi-cloud-strategy/10_disaster_recovery/dr_strategies.svg)

---

## Why Multi-Cloud DR?
- Single-cloud DR protects against Region failure
- Multi-cloud DR protects against provider-level failure
- Cloud provider outages do happen (AWS us-east-1, Azure AD, GCP networking)
- Regulatory requirements may mandate provider diversity
- Ultimate resilience: no single point of failure at the provider level

---

## Multi-Cloud DR vs Single-Cloud DR
- Single-cloud: replicate across Regions within one provider
- Multi-cloud: replicate across providers entirely
- Multi-cloud DR is significantly more complex
- Data format and API differences between providers
- Cost is higher but risk reduction can justify it

---

## RPO and RTO in Multi-Cloud
- RPO (Recovery Point Objective): how much data loss is acceptable
- RTO (Recovery Time Objective): how much downtime is acceptable
- Multi-cloud adds latency to replication (cross-provider network)
- Synchronous replication across clouds is rarely practical
- Typical multi-cloud RPO: minutes to hours, not seconds

---

## DR Strategy Spectrum
1. Backup to another cloud: lowest cost, highest RTO
1. Pilot light cross-cloud: minimal always-on footprint
1. Warm standby cross-cloud: scaled-down running copy
1. Active-active multi-cloud: lowest RTO, highest cost and complexity

---

## Multi-Cloud DR Architecture

![dr](svg/courses/cloud/multi-cloud-strategy/10_disaster_recovery/multi_cloud_dr.svg)

---

## Backup to Another Cloud
- Regular backups exported to a second cloud provider
- Example: AWS S3 backups replicated to Azure Blob Storage
- Rebuild infrastructure from IaC on the second cloud
- RTO: hours to days
- RPO: depends on backup frequency

---

## Pilot Light Cross-Cloud
- Core data replicated continuously to second cloud
- Minimal compute running (DNS, database replica)
- Scale up on failover event
- RTO: 30 minutes to hours
- Requires IaC for the second cloud ready to deploy

---

## Warm Standby Cross-Cloud
- Scaled-down but functional copy running on second cloud
- All components present at reduced capacity
- Traffic can be shifted quickly via DNS
- RTO: minutes to 30 minutes
- More expensive but dramatically faster recovery

---

## Active-Active Multi-Cloud
- Full production workload on both clouds simultaneously
- Global load balancer distributes traffic
- Database replication is the hardest part
- RTO: near zero (traffic shifts automatically)
- Most expensive and most complex to operate

---

## Data Replication Across Clouds
- No native cross-cloud replication (unlike cross-Region)
- Options: application-level replication, third-party tools, custom sync
- Database-specific: PostgreSQL logical replication, MySQL replication
- Object storage: rclone, custom sync with cloud SDKs
- Message queues: bridge patterns (Kafka MirrorMaker)

---

## Cross-Cloud DNS Failover

```hcl
# Terraform: Route 53 health check and failover
resource "aws_route53_health_check" "primary" {
  fqdn              = "app.aws.example.com"
  port              = 443
  type              = "HTTPS"
  request_interval  = 10
  failure_threshold = 3
}

resource "aws_route53_record" "failover_primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"
  set_identifier = "primary-aws"
  failover_routing_policy {
    type = "PRIMARY"
  }
  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }
  health_check_id = aws_route53_health_check.primary.id
}

```

---

## Cross-Cloud DNS Failover: Secondary

```hcl
resource "aws_route53_record" "failover_secondary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"
  set_identifier = "secondary-azure"
  failover_routing_policy {
    type = "SECONDARY"
  }
  alias {
    name                   = "azure-app-gw.example.com"
    zone_id                = "Z123456"
    evaluate_target_health = false
  }
}
```

---

## Failover Automation
- Manual failover is too slow for production
- Use health checks to trigger automated failover
- DNS-based failover is the simplest cross-cloud mechanism
- Consider DNS TTL: lower TTL = faster failover but more DNS queries
- Test automated failover regularly

---

## Database DR Across Clouds
- Most complex aspect of multi-cloud DR
- PostgreSQL: logical replication between AWS RDS and GCP Cloud SQL
- MySQL: native replication or tools like Debezium for CDC
- NoSQL: application-level sync or multi-master databases (CockroachDB, Spanner)
- Consider cloud-agnostic databases for easier cross-cloud DR

---

## Testing Multi-Cloud DR
- DR plan without testing is fiction
- Tabletop exercises: walk through the plan
- Partial failover: shift percentage of traffic to DR cloud
- Full failover: complete switchover to DR cloud
- Measure actual RPO and RTO against targets

---

## Key Takeaways
- Multi-cloud DR protects against provider-level outages
- Complexity and cost are significantly higher than single-cloud DR
- DNS-based failover is the simplest cross-cloud DR mechanism
- Data replication across clouds requires custom tooling
- Test DR regularly; untested plans will fail when needed
