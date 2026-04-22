---
tags:
  - infrastructure:cloud
  - concepts:architecture
  - practices:devops
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Other Cloud Services

---

## Beyond the Core
- Cloud providers offer 200+ services each
- Most architectures use a handful
- Knowing what exists helps you avoid reinventing
- Managed services reduce operational burden
- This chapter covers important services we haven't discussed

---

## DevOps Services
- CI/CD pipelines in the cloud
- AWS CodePipeline/CodeBuild, Azure DevOps, Cloud Build
- GitHub Actions works across all clouds
- Container registries (ECR, ACR, Artifact Registry)
- Infrastructure as Code deployment services

---

## GitHub Actions Deploy to AWS

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
    - uses: actions/checkout@v4
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123:role/deploy
        aws-region: us-east-1
    - run: |
        aws s3 sync ./dist s3://my-app-bucket
        aws cloudfront create-invalidation \
          --distribution-id E123 --paths "/*"
```

---

## Source Control
- AWS CodeCommit (being deprecated), GitHub, GitLab
- Azure Repos (part of Azure DevOps)
- Cloud Source Repositories (GCP)
- Most organizations use GitHub or GitLab
- Integrate with cloud CI/CD pipelines

---

## CI/CD Pipeline Architecture
1. Developer pushes code
1. Build and unit test (CodeBuild, Cloud Build)
1. Static analysis and security scanning
1. Deploy to staging
1. Integration and E2E tests
1. Deploy to production (rolling, blue-green, canary)

---

## CI/CD Pipeline

![cicd](svg/courses/cloud/architecting-in-the-cloud/13_other_cloud_services/cicd_pipeline_architecture.svg)

---

## Artifact Management
- Store build artifacts and packages
- AWS CodeArtifact, Azure Artifacts, Artifact Registry
- npm, Maven, PyPI, NuGet packages
- Container images in container registries
- Dependency caching for faster builds

---

## Mobile Services
- Push notifications (SNS, Firebase Cloud Messaging)
- Mobile analytics (Pinpoint, App Center, Firebase Analytics)
- Authentication (Cognito, Azure AD B2C, Firebase Auth)
- API management for mobile backends
- Offline sync (AppSync, Firestore)

---

## Mobile Backend Architecture
- API Gateway for REST/GraphQL endpoints
- Lambda/Functions for serverless backend
- DynamoDB/Firestore for low-latency data
- S3/Blob for media storage
- Cognito/Firebase Auth for user management

---

## Testing Services
- Load testing: AWS does not have managed, use k6/Gatling
- Azure Load Testing (managed JMeter)
- Device testing: AWS Device Farm, Firebase Test Lab
- Chaos engineering: AWS FIS, Gremlin
- Test environments from IaC (ephemeral environments)

---

## AI and Machine Learning
- Pre-built AI services (vision, language, speech)
- AWS Rekognition, Azure AI services, Google Vision
- ML platforms: SageMaker, Azure ML, Vertex AI
- Managed training and inference infrastructure
- No PhD required for pre-built services

---

## AI Services Examples
- Image and video analysis
- Natural language processing
- Speech to text and text to speech
- Translation
- Document extraction and analysis
- Chatbots and conversational AI

---

## Data Analytics Services
- Data warehousing: Redshift, Synapse, BigQuery
- Real-time streaming: Kinesis, Event Hubs, Dataflow
- ETL: Glue, Data Factory, Dataflow
- Business intelligence: QuickSight, Power BI, Looker
- Data lakes: S3/ADLS/GCS + query engines

---

## IoT Services
- Device management and connectivity
- AWS IoT Core, Azure IoT Hub (GCP retired Cloud IoT Core in 2023)
- Edge computing on devices
- Data ingestion at massive scale
- Integration with analytics and ML

---

## Notification Services
- Email: SES, SendGrid
- SMS: SNS, Twilio integration
- Push notifications: SNS, Firebase
- In-app messaging
- Event-driven notifications via EventBridge

---

## Search Services
- Managed Elasticsearch/OpenSearch
- AWS OpenSearch, Azure AI Search, Elastic Cloud
- Full-text search, analytics, logging
- CloudSearch (AWS): simpler, less flexible
- Add search to applications without managing clusters

---

## API Management
- API Gateway: rate limiting, authentication, throttling
- AWS API Gateway, Azure API Management, Apigee (GCP)
- Usage plans and API keys
- Request/response transformation
- Developer portals and documentation

---

## API Gateway with SAM

```yaml
Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.12
      Handler: app.handler
      Events:
        GetOrder:
          Type: Api
          Properties:
            Path: /orders/{id}
            Method: get
        CreateOrder:
          Type: Api
          Properties:
            Path: /orders
            Method: post
```

---

## When to Use Managed Services
- Does the cloud offer a managed version? Use it.
- Will save weeks or months of engineering
- Built-in HA, scaling, patching, backups
- Operational burden is the hidden cost of self-managing
- Only self-manage when managed doesn't meet requirements

---

## Evaluating a New Cloud Service
1. Does it solve your actual problem?
1. What is the pricing model?
1. What are the limits and quotas?
1. What is the vendor lock-in risk?
1. What is the operational overhead?
1. Are there open-source alternatives?

---

## Blockchain and Ledger Services
- Amazon QLDB: immutable, cryptographically verifiable ledger
- Amazon Managed Blockchain
- Azure Confidential Ledger
- Use cases: supply chain, financial audit trails
- Niche but growing adoption

---

## Media Services
- Video transcoding: MediaConvert, Azure Media Services
- Live streaming: MediaLive, Azure Media Services
- Content delivery: CloudFront, Azure CDN
- Combine with S3 for media storage
- Scalable media pipelines

---

## Migration Services
- AWS Migration Hub, Azure Migrate, GCP Migrate
- Server migration: replicate VMs to cloud
- Database migration: DMS, Azure DMS
- Application migration: containerize and redeploy
- Migration assessment and planning tools

---

## Governance and Compliance Services
- AWS Control Tower: landing zone setup
- Azure Landing Zones: best-practice account structure
- GCP Organization Policy: guardrails
- Automated compliance checking
- Centralized governance across accounts

---

## Architecture Review Checklist: Details
- Is the architecture multi-AZ? Multi-Region if needed?
- Are all components scalable?
- Is state externalized (databases, caches, queues)?
- Is security layered (identity, network, encryption)?
- Is cost monitored and optimized?
- Is DR planned and tested?

---

## Architecture Review Checklist

![checklist](svg/courses/cloud/architecting-in-the-cloud/13_other_cloud_services/architecture_review_checklist.svg)

---

## Cost Optimization in Architecture
- Architect for cost from the start
- Right-size all resources
- Use serverless for variable workloads
- Reserved capacity for steady-state
- Monitor and optimize continuously

---

## Observability Architecture
- Metrics, logs, and traces: the three pillars
- Centralized logging (CloudWatch, ELK, Datadog)
- Distributed tracing (X-Ray, Jaeger)
- Custom metrics for business KPIs
- Alerting and on-call rotation

---

## Three Pillars of Observability

![observability](svg/courses/cloud/architecting-in-the-cloud/13_other_cloud_services/observability_three_pillars.svg)

---

## Multi-Tenancy Architecture
- Serve multiple customers from shared infrastructure
- Silo model: separate resources per tenant
- Pool model: shared resources, logical isolation
- Bridge model: mix of silo and pool
- Trade-off: cost efficiency vs isolation

---

## Multi-Tenancy Models

![tenancy](svg/courses/cloud/architecting-in-the-cloud/13_other_cloud_services/multi_tenancy_models.svg)

---

## Edge Computing: Details
- Run compute close to end users
- CloudFront Functions, Lambda@Edge
- Azure Edge Zones, GCP Distributed Cloud
- IoT edge processing
- Reduce latency for real-time applications

---

## Edge Computing

![edge](svg/courses/cloud/architecting-in-the-cloud/13_other_cloud_services/edge_computing.svg)

---

## Course Summary
- Cloud architecture requires new thinking
- Design for failure, scale horizontally, decouple
- Use managed services to reduce operational burden
- Choose the right compute (VMs, containers, serverless)
- Storage, queues, and caching are core building blocks
- Patterns guide you; anti-patterns warn you
- Security and cost are always architectural concerns

---

## Well-Architected Review
- Regular architecture reviews against best practices
- AWS Well-Architected Tool: self-assessment
- Identify risks and improvement opportunities
- Prioritize fixes by impact
- Embed reviews in project lifecycle

---

## Architecture Evolution
- Architecture is not a one-time activity
- Revisit as requirements change
- Monitor and measure real-world performance
- Refactor when patterns become anti-patterns
- The best architecture evolves with the business

---

## Recommended Reading
- AWS Well-Architected Framework whitepaper
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Building Microservices" by Sam Newman
- Cloud provider architecture centers
- Re:Invent, Ignite, and Next conference talks

---

## Thank You
- Questions and discussion
- Feedback welcome
- Apply these patterns in your own architectures
- Start simple, evolve as you learn
- The cloud is a powerful tool: use it wisely
