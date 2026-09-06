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

# Vendor Lock-In Assessment

---

## Where Lock-In Hides

![lock_in_vectors](svg/courses/cloud/multi-cloud-strategy/02_vendor_lock_in/lock_in_vectors.svg)

---

## What Is Vendor Lock-In?
- Dependency on a provider that makes switching costly
- Not just technical — also contractual and operational
- Exists on a spectrum from minimal to total
- Every cloud service creates some degree of lock-in
- The goal is managing lock-in, not eliminating it entirely

---

## The Lock-In Spectrum
- Low lock-in: VMs, block storage, standard containers
- Medium lock-in: managed databases, load balancers
- High lock-in: proprietary serverless, AI/ML services
- Extreme lock-in: deeply integrated PaaS (App Engine, Elastic Beanstalk)
- Assess each workload individually

<!-- SVG placeholder: lock-in spectrum diagram from low to extreme with service examples -->

---

## Lock-In Vectors: Compute
- VM images and machine types are mostly portable
- Auto-scaling configurations are provider-specific
- Placement groups and dedicated hosts differ
- GPU and specialized instance types vary
- Container workloads are the most portable compute option

---

## Lock-In Vectors: Storage
- Object storage APIs differ (S3, Blob, Cloud Storage)
- S3 API is a de facto standard — Azure and GCP partially support it
- Managed file systems (EFS, Azure Files, Filestore) differ
- Block storage is relatively portable
- Data gravity: moving large datasets is slow and expensive

---

## Lock-In Vectors: Databases
- Managed relational databases (RDS, Cloud SQL, Azure SQL) use standard engines
- Proprietary databases (DynamoDB, Cosmos DB, Bigtable) are strong lock-in
- Aurora, Spanner: enhanced but proprietary
- Open-source engines (PostgreSQL, MySQL) reduce lock-in
- Schema and query patterns may still create subtle lock-in

---

## Lock-In Vectors: Serverless
- AWS Lambda, Azure Functions, Google Cloud Functions
- Different runtime APIs and deployment models
- Event sources and triggers are provider-specific
- Cold start behavior varies significantly
- Serverless frameworks (Serverless.com) reduce but do not eliminate lock-in

---

## Lock-In Vectors: Identity and Access
- AWS IAM, Azure AD/Entra ID, Google Cloud IAM
- Policy languages and permission models differ greatly
- Service accounts and roles are not portable
- Federation helps but adds complexity
- Identity is one of the deepest lock-in vectors

---

## Lock-In Vectors: Networking
- VPC concepts are similar but implementations differ
- Security groups vs NSGs vs firewall rules
- Load balancer features and configuration vary
- DNS services (Route 53, Azure DNS, Cloud DNS) differ in capabilities
- Private connectivity options are provider-specific

---

## Data Gravity: Details
- Data attracts compute — not the other way around
- Moving petabytes between clouds takes weeks or months
- Egress costs make frequent data movement expensive
- Applications tend to cluster near their data
- Data location decisions have long-lasting consequences

---

## Data Gravity

![gravity](svg/courses/cloud/multi-cloud-strategy/02_vendor_lock_in/data_gravity.svg)

---

## Calculating Exit Costs
- Data egress fees (typically $0.08-0.12/GB)
- Staff time for migration engineering
- Application refactoring effort
- Testing and validation costs
- Business disruption during migration
- Retraining teams on new platform

---

## Proprietary vs Portable: Terraform Example

```hcl
# Proprietary: AWS DynamoDB (high lock-in)
resource "aws_dynamodb_table" "orders" {
  name         = "orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }
}

# Portable: PostgreSQL on any cloud (low lock-in)
resource "aws_db_instance" "orders" {
  engine         = "postgres"
  engine_version = "16.2"
  instance_class = "db.t3.medium"
  db_name        = "orders"
}
```

---

## Evaluating Portability: A Framework
1. List all cloud services consumed
1. Rate each on the lock-in spectrum (low/medium/high)
1. Estimate migration effort for each service
1. Calculate data egress costs
1. Identify open-source or cross-cloud alternatives
1. Prioritize based on business risk

---

## Lock-In Spectrum

![spectrum](svg/courses/cloud/multi-cloud-strategy/02_vendor_lock_in/lock_in_spectrum.svg)

---

## Managed Services vs Self-Managed Open Source
- Managed: lower ops burden, higher lock-in
- Self-managed: higher ops burden, higher portability
- Examples: RDS PostgreSQL vs self-hosted PostgreSQL on VMs
- Managed Kafka vs self-hosted Kafka
- Decision depends on team skills and portability requirements

---

## Open-Source Alternatives to Proprietary Services
- DynamoDB alternative: CockroachDB, ScyllaDB, Cassandra
- Lambda alternative: Knative, OpenFaaS
- SQS/SNS alternative: RabbitMQ, Kafka
- Cognito alternative: Keycloak
- CloudWatch alternative: Prometheus + Grafana

---

## Contractual Lock-In
- Enterprise agreements with spending commitments
- Reserved instances and savings plans
- Credits and promotional pricing
- Volume discounts tied to single-provider spend
- Negotiate flexibility clauses when signing contracts

---

## Building a Lock-In Mitigation Strategy
- Accept some lock-in where the value is clear
- Use open standards and open-source where practical
- Maintain abstraction layers for critical services
- Document provider-specific dependencies explicitly
- Review lock-in posture quarterly
