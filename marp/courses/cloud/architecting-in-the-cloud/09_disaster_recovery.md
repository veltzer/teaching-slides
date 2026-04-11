---
tags:
  - infrastructure:cloud
  - concepts:architecture
  - practices:disaster-recovery
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Disaster Recovery in the Cloud

---

## What is Disaster Recovery?
- Plan and process for recovering from major failures
- Not just backup: full service restoration
- Minimize downtime and data loss
- Protect against: hardware failure, natural disasters, human error
- Cloud makes DR accessible and affordable

---

## RPO and RTO
- RPO (Recovery Point Objective): how much data can you lose?
- RTO (Recovery Time Objective): how long can you be down?
- RPO = 0: no data loss (synchronous replication)
- RTO = 0: no downtime (active-active)
- Cost increases as RPO and RTO decrease

---

## RPO and RTO

![rpo_rto](svg/courses/cloud/architecting-in-the-cloud/09_disaster_recovery/rpo_rto_diagram.svg)

---

## DR Strategies Spectrum
1. Backup and Restore: lowest cost, highest RTO
1. Pilot Light: minimal always-on footprint
1. Warm Standby: scaled-down running copy
1. Multi-Site Active-Active: lowest RTO, highest cost

---

## DR Strategies Spectrum

![dr_spectrum](svg/courses/cloud/architecting-in-the-cloud/09_disaster_recovery/dr_strategies_spectrum.svg)

---

## Backup and Restore
- Regular backups to another Region
- Rebuild infrastructure from IaC on recovery
- Restore data from backups
- RTO: hours to days
- Cheapest option, suitable for non-critical systems

---

## Pilot Light
- Core components always running in DR Region
- Database replicated (but minimal compute)
- Scale up on failover
- RTO: tens of minutes
- Balance between cost and recovery speed

---

## Warm Standby
- Scaled-down but fully functional copy in DR Region
- All components running at reduced capacity
- Scale up on failover
- RTO: minutes
- More expensive but faster recovery

---

## Multi-Site Active-Active
- Full copy running in both Regions
- Traffic distributed across both
- Instant failover (no recovery needed)
- RTO: near zero
- Most expensive, most complex

---

## Using the Cloud as DR
- On-premises primary, cloud DR
- Replicate data to cloud continuously
- Stand up infrastructure from IaC on failure
- Cost-effective: pay for storage, not idle compute
- Faster than traditional DR sites

---

## Fault Tolerance vs Disaster Recovery
- Fault tolerance: survive component failure without interruption
- DR: recover from major disaster after interruption
- Multi-AZ: fault tolerance
- Multi-Region: disaster recovery
- Design for both, at appropriate levels

---

## Cloud DR Building Blocks
- Cross-Region replication (S3, RDS, DynamoDB)
- AMI/image copies across Regions
- Infrastructure as Code (rebuild in minutes)
- DNS failover (Route 53, Cloud DNS)
- Automated failover scripts

---

## S3 Cross-Region Replication

```bash
# Enable versioning (required for replication)
aws s3api put-bucket-versioning \
  --bucket my-primary-bucket \
  --versioning-configuration Status=Enabled

# Set up replication rule
aws s3api put-bucket-replication \
  --bucket my-primary-bucket \
  --replication-configuration '{
    "Role": "arn:aws:iam::123:role/replication",
    "Rules": [{
      "Status": "Enabled",
      "Destination": {
        "Bucket": "arn:aws:s3:::my-dr-bucket"
      }
    }]
  }'
```

---

## Database DR
- RDS Multi-AZ: automatic failover within Region
- RDS Cross-Region Read Replicas: promote on DR
- DynamoDB Global Tables: multi-Region active-active
- Aurora Global Database: under 1 minute failover
- Choose based on RPO/RTO requirements

---

## Testing DR
- DR plan without testing is just documentation
- Regular DR drills (quarterly or annually)
- Simulate real failures
- Measure actual RPO and RTO
- GameDays: intentional failure injection

---

## Chaos Engineering
- Deliberately inject failures to find weaknesses
- Netflix Chaos Monkey: random instance termination
- AWS Fault Injection Simulator
- Gremlin: commercial chaos platform
- Build confidence in your DR plan

---

## DR Automation
- Manual DR failover is slow and error-prone
- Automate failover with scripts and runbooks
- Use health checks to trigger automatic failover
- Route 53 health check + failover routing
- Practice automated failover regularly

---

## Patterns of DR in the Cloud
- DNS-based failover: simplest
- Database promotion: promote read replica
- Full stack redeployment from IaC
- Container migration: redeploy to another Region
- Data re-seeding from backups

---

## Multi-Region Data Replication
- S3 Cross-Region Replication
- RDS Cross-Region Read Replicas
- DynamoDB Global Tables
- Aurora Global Database (<1 second replication lag)
- Each has different RPO characteristics

---

## DNS-Based Failover
- Route 53 / Cloud DNS health checks
- Failover routing policy
- If primary Region unhealthy, route to DR Region
- Automated, no manual intervention
- TTL affects failover speed

---

## DNS Failover

![dns_failover](svg/courses/cloud/architecting-in-the-cloud/09_disaster_recovery/dns_failover.svg)

---

## Route 53 Failover Record

```json
{
  "Changes": [{
    "Action": "CREATE",
    "ResourceRecordSet": {
      "Name": "app.example.com",
      "Type": "A",
      "SetIdentifier": "primary",
      "Failover": "PRIMARY",
      "AliasTarget": {
        "HostedZoneId": "Z123",
        "DNSName": "alb-primary.us-east-1.elb.amazonaws.com",
        "EvaluateTargetHealth": true
      }
    }
  }]
}
```

---

## Backup Strategy
- 3-2-1 rule: 3 copies, 2 media types, 1 offsite
- Automate all backups
- Test restoration regularly (not just backup)
- Cross-Region backups for DR
- Retention policies based on compliance requirements

---

## Recovery Runbook Example
1. Confirm the outage (not a transient issue)
1. Notify the team and stakeholders
1. Execute failover (automated or manual)
1. Verify DR environment is operational
1. Monitor and stabilize
1. Plan failback when primary recovers

---

## DR Cost Optimization
- Backup and Restore: storage costs only
- Pilot Light: minimal compute (small instances)
- Warm Standby: reduced-size instances
- Use spot instances for DR testing
- Pay for full DR compute only when activated

---

## DR Documentation
- Document every step of the recovery process
- Runbooks for each failure scenario
- Contact information and escalation paths
- Dependencies and order of operations
- Keep documentation up to date (automate where possible)

---

## Storage DR Strategies
- S3 Cross-Region Replication: continuous
- EBS snapshots copied to DR Region: periodic
- EFS replication: AWS Backup cross-Region
- Glacier for long-term archive copies
- Automate all replication and copy jobs

---

## Application DR Considerations
- Stateless apps: easiest to recover (just redeploy)
- Stateful apps: data synchronization is the challenge
- DNS TTL affects failover speed
- Certificate management in DR Region
- Third-party integrations: update endpoints

---

## DR for Serverless
- Lambda functions: deploy to multiple Regions
- DynamoDB Global Tables: automatic multi-Region
- API Gateway: deploy to DR Region
- S3: cross-Region replication
- Serverless makes DR simpler (no servers to rebuild)

---

## Business Continuity Planning
- DR is part of broader business continuity
- Communication plan during outages
- Customer notification procedures
- Regulatory reporting requirements
- Regular tabletop exercises with stakeholders

---

## Key Takeaways
- Define RPO and RTO based on business requirements
- Choose DR strategy based on cost vs recovery speed
- Cloud makes DR affordable (pay for storage, not idle compute)
- Test DR regularly (untested plans will fail)
- Automate failover wherever possible
