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
# Service Mapping Across Clouds

---

## Why Service Mapping Matters
- Understanding equivalents is foundational for multi-cloud
- Services are similar but never identical
- Feature gaps can break migration plans
- Naming differences cause confusion across teams
- A shared vocabulary reduces errors

---

## Compute: Virtual Machines
- AWS: EC2 (Elastic Compute Cloud)
- Azure: Virtual Machines
- GCP: Compute Engine
- All offer on-demand, reserved, and spot/preemptible options
- Instance type naming and specifications differ

---

## Compute: Instance Type Comparison
- AWS: m5.xlarge (4 vCPU, 16 GB)
- Azure: Standard_D4s_v5 (4 vCPU, 16 GB)
- GCP: n2-standard-4 (4 vCPU, 16 GB)
- Naming conventions are entirely different
- Use a reference table or mapping tool

---

## Creating a VM: AWS CLI

```bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type m5.xlarge \
  --key-name my-key \
  --subnet-id subnet-0123456789abcdef0 \
  --security-group-ids sg-0123456789abcdef0 \
  --tag-specifications \
    'ResourceType=instance,Tags=[{Key=Name,Value=web-server}]'
```

---

## Creating a VM: Azure CLI

```bash
az vm create \
  --resource-group my-rg \
  --name web-server \
  --image Ubuntu2204 \
  --size Standard_D4s_v5 \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --vnet-name my-vnet \
  --subnet my-subnet \
  --nsg my-nsg
```

---

## Creating a VM: gcloud CLI

```bash
gcloud compute instances create web-server \
  --zone=us-central1-a \
  --machine-type=n2-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --subnet=my-subnet \
  --tags=web-server \
  --metadata=ssh-keys="user:$(cat ~/.ssh/id_rsa.pub)"
```

---

## Key Differences in VM Creation
- AWS uses AMI IDs; Azure uses image URNs; GCP uses image families
- Azure requires a resource group; AWS and GCP do not
- GCP requires explicit zone; AWS uses AZ via subnet
- Security model: security groups (AWS), NSGs (Azure), firewall rules (GCP)
- All three require different authentication setup

---

## Compute Service Mapping

![compute](svg/courses/cloud/multi-cloud-strategy/03_service_mapping/compute_mapping.svg)

---

## Compute: Container Orchestration
- AWS: EKS (Elastic Kubernetes Service)
- Azure: AKS (Azure Kubernetes Service)
- GCP: GKE (Google Kubernetes Engine)
- All run standard Kubernetes
- Differences: networking plugins, node management, upgrade process

---

## Container Services: Beyond Kubernetes
- AWS: ECS (proprietary), Fargate (serverless containers)
- Azure: Container Instances (ACI), Container Apps
- GCP: Cloud Run (serverless containers)
- ECS is proprietary — Kubernetes is more portable
- Serverless container options are all provider-specific

---

<!-- SVG placeholder: container services comparison table across providers -->

## Container Services Comparison

---

## Serverless: Functions as a Service
- AWS: Lambda (pioneer, largest ecosystem)
- Azure: Functions (strong .NET integration)
- GCP: Cloud Functions (tight integration with Google services)
- Runtime support varies (Lambda supports custom runtimes)
- Pricing models are similar but not identical

---

## Serverless: Key Differences
- Maximum execution time: Lambda 15min, Azure Functions 60min, GCF 60min
- Memory limits: Lambda 10GB, Azure Functions 14GB, GCF 32GB
- Cold start behavior varies significantly
- Event source integration is entirely provider-specific
- Deployment packaging differs

---

## Object Storage
- AWS: S3 (Simple Storage Service)
- Azure: Blob Storage
- GCP: Cloud Storage
- S3 API is a de facto standard
- Storage tiers map roughly but pricing differs

---

## Object Storage Tiers Mapping
- Hot: S3 Standard / Hot / Standard
- Infrequent: S3 IA / Cool / Nearline
- Archive: S3 Glacier / Archive / Coldline
- Deep archive: S3 Glacier Deep Archive / Archive / Archive
- Lifecycle policies exist on all three but syntax differs

---

## Storage Service Mapping

![storage](svg/courses/cloud/multi-cloud-strategy/03_service_mapping/storage_mapping.svg)

---

## Creating a Storage Bucket: Three Clouds

```bash
# AWS
aws s3 mb s3://my-bucket-name --region us-east-1

# Azure
az storage account create --name mystorageacct \
  --resource-group my-rg --sku Standard_LRS
az storage container create --name my-container \
  --account-name mystorageacct

# GCP
gcloud storage buckets create gs://my-bucket-name \
  --location=us-central1
```

---

## Networking: Virtual Private Cloud
- AWS: VPC (Virtual Private Cloud)
- Azure: VNet (Virtual Network)
- GCP: VPC (global by default, subnets are regional)
- AWS and Azure VPCs are regional; GCP VPCs are global
- This difference fundamentally affects network design

---

## Networking: Key Differences
- AWS: explicit route tables per subnet
- Azure: system routes with optional UDRs
- GCP: routes are global, applied via network tags
- Peering: all three support VPC/VNet peering
- GCP global VPC simplifies multi-region but changes mental model

---

<!-- SVG placeholder: VPC architecture comparison across three providers -->

## VPC Architecture Comparison

---

## Load Balancing
- AWS: ALB (L7), NLB (L4), Classic LB (legacy)
- Azure: Application Gateway (L7), Load Balancer (L4)
- GCP: Cloud Load Balancing (global L7 and L4)
- GCP load balancers are global by default — unique advantage
- Feature sets differ in WAF, SSL, and routing capabilities

---

## Managed Databases: Relational
- AWS: RDS (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server), Aurora
- Azure: Azure SQL, Azure Database for MySQL/PostgreSQL
- GCP: Cloud SQL (MySQL, PostgreSQL, SQL Server), AlloyDB
- Open-source engines (PostgreSQL, MySQL) are most portable
- Aurora and AlloyDB offer enhanced performance but add lock-in

---

## Managed Databases: NoSQL
- AWS: DynamoDB (key-value/document)
- Azure: Cosmos DB (multi-model, multi-API)
- GCP: Bigtable (wide-column), Firestore (document)
- These are highly proprietary — migration is costly
- Cosmos DB is unique in supporting multiple query APIs

---

## Database Service Mapping

![databases](svg/courses/cloud/multi-cloud-strategy/03_service_mapping/database_mapping.svg)

---

## Messaging and Queuing
- AWS: SQS (queue), SNS (pub/sub), EventBridge (event bus)
- Azure: Service Bus (queue), Event Grid (event bus), Event Hubs (streaming)
- GCP: Pub/Sub (unified pub/sub and streaming)
- GCP Pub/Sub is simpler; AWS has more specialized services
- Consider Kafka (MSK, Event Hubs Kafka, Confluent) for portability

---

## AI and Machine Learning
- AWS: SageMaker, Bedrock, Rekognition, Comprehend
- Azure: Azure ML, OpenAI Service, Cognitive Services
- GCP: Vertex AI, Gemini API, Vision AI, Natural Language
- Azure has exclusive OpenAI API access
- GCP leads in custom model training infrastructure
- AI services are high lock-in — model APIs change frequently

---

<!-- SVG placeholder: comprehensive service mapping table across all three providers -->

## Complete Service Mapping Reference

---

## Identity and Access Management
- AWS: IAM (users, roles, policies in JSON)
- Azure: Entra ID (formerly Azure AD) + RBAC
- GCP: Cloud IAM (roles, service accounts, policy bindings)
- Policy syntax and permission granularity differ significantly
- Cross-cloud identity federation is possible but complex

---

## Monitoring and Observability
- AWS: CloudWatch (metrics, logs, alarms)
- Azure: Monitor (metrics, Log Analytics, alerts)
- GCP: Cloud Monitoring + Cloud Logging (formerly Stackdriver)
- Third-party tools (Datadog, Grafana, Prometheus) span all clouds
- Native tools are convenient but create observability lock-in

---

## Service Mapping Strategy
1. Inventory all services used in current workloads
1. Map each to equivalents on target clouds
1. Identify feature gaps that would require workarounds
1. Flag services with no equivalent (proprietary only)
1. Prioritize portable services for multi-cloud workloads
1. Accept provider-specific services where portability is not needed
