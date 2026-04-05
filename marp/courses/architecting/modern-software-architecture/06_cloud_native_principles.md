# Cloud-Native Principles

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---
## What Does Cloud-Native Mean?

- An approach to building and running applications that fully exploit cloud computing
- Designed for horizontal scalability, resilience, and manageability
- Leverages containers, service meshes, microservices, and declarative APIs
- Defined by the `Cloud Native Computing Foundation` (`CNCF`)

---
## Cloud-Native vs Cloud-Hosted

| Aspect | Cloud-Hosted | Cloud-Native |
|--------|-------------|-------------|
| Architecture | Monolith on a VM | Microservices in containers |
| Scaling | Vertical | Horizontal, auto-scaling |
| State | Stateful servers | Stateless services |
| Deployment | Manual or scripted | Automated CI/CD pipelines |
| Resilience | Redundant hardware | Software-level fault tolerance |

---
## The 12-Factor App Methodology

- A set of best practices for building modern, portable, scalable applications
- Created by developers at `Heroku` based on real-world experience
- Applicable to any language and any cloud platform
- Each factor addresses a specific aspect of application design

---
## Factor 1: Codebase

- One codebase tracked in version control, many deploys
- A single repository per application
- Different environments (dev, staging, production) deploy the same code
- Multiple apps sharing code should extract shared libraries

---
## Factor 2: Dependencies

- Explicitly declare and isolate dependencies
- Use a dependency manifest (e.g., `requirements.txt`, `package.json`, `go.mod`)
- Never rely on system-wide packages being available
- Use tools that provide dependency isolation (virtual environments, containers)

---
## Factor 3: Config

- Store configuration in the environment, not in code
- Configuration varies between deploys; code does not
- Use environment variables for database URLs, API keys, and feature flags
- Never commit secrets to version control

---
## Config Example

```bash
# Bad: hardcoded in source
DATABASE_URL = "postgres://prod-db:5432/myapp"

# Good: read from environment
import os
DATABASE_URL = os.environ["DATABASE_URL"]
```

- Environment variables are language-agnostic and deploy-agnostic

---
## Factor 4: Backing Services

- Treat backing services as attached resources
- Databases, caches, message queues, and SMTP servers are all backing services
- Swap between local and third-party services by changing configuration
- No code change needed to switch from local `PostgreSQL` to `Amazon RDS`

---
## Backing Services Diagram

<div class="mermaid">
graph LR
    APP[Application] --> DB[(PostgreSQL)]
    APP --> CACHE[(Redis)]
    APP --> MQ[RabbitMQ]
    APP --> SMTP[SMTP Service]
    APP --> S3[Object Storage]
</div>

---
## Factor 5: Build, Release, Run

- Strict separation between build, release, and run stages
- Build: converts code into an executable bundle
- Release: combines build with configuration for a specific environment
- Run: launches the application in the execution environment

---
## Build, Release, Run Pipeline

<div class="mermaid">
graph LR
    CODE[Source Code] -->|Build| BUILD[Build Artifact]
    CONFIG[Config] --> RELEASE[Release]
    BUILD --> RELEASE
    RELEASE -->|Run| RUNTIME[Running Process]
</div>

---
## Factor 6: Processes

- Execute the application as one or more stateless processes
- Any data that needs to persist must be stored in a backing service
- Processes share nothing: no sticky sessions, no local file storage
- Each request can be handled by any instance

---
## Factor 7: Port Binding

- Export services via port binding
- The application is completely self-contained
- It binds to a port and listens for incoming requests
- No dependency on an external web server like `Apache` or `IIS`

---
## Factor 8: Concurrency

- Scale out via the process model
- Different types of work are handled by different process types
- Web processes handle HTTP requests
- Worker processes handle background jobs
- Each process type scales independently

---
## Concurrency Model

<div class="mermaid">
graph TD
    subgraph Web Processes
        W1[Web 1]
        W2[Web 2]
        W3[Web 3]
    end
    subgraph Worker Processes
        WK1[Worker 1]
        WK2[Worker 2]
    end
    subgraph Clock Processes
        CK1[Scheduler]
    end
    LB[Load Balancer] --> W1
    LB --> W2
    LB --> W3
    Q[Message Queue] --> WK1
    Q --> WK2
</div>

---
## Factor 9: Disposability

- Maximize robustness with fast startup and graceful shutdown
- Processes can be started and stopped at a moment's notice
- Fast startup enables rapid scaling and deployment
- Graceful shutdown finishes current requests before terminating

---
## Factor 10: Dev/Prod Parity

- Keep development, staging, and production as similar as possible
- Use the same backing services in all environments
- Reduce the time gap between code commit and production deploy
- Use containers to ensure identical environments everywhere

---
## Factor 11: Logs

- Treat logs as event streams
- Applications should not manage log files or routing
- Write log events to `stdout` and let the platform handle collection
- Use centralized logging tools like `ELK Stack`, `Fluentd`, or `Datadog`

---
## Factor 12: Admin Processes

- Run admin and management tasks as one-off processes
- Database migrations, console sessions, and cleanup scripts
- Run in the same environment and release as the application
- Use the same codebase and configuration

---
## Beyond 12 Factors

- The original 12 factors were published in 2011
- Modern cloud-native applications often add:
    - API First: design APIs before implementation
    - Telemetry: built-in metrics, logging, and tracing
    - Security: zero trust, encryption everywhere
    - Feature Flags: decouple deployment from release

---
## Stateless Services

- Do not store any client session data locally
- Every request contains all the information needed to process it
- State is externalized to databases, caches, or object stores
- Any instance can handle any request from any client

---
## Stateless Service Architecture

<div class="mermaid">
graph TD
    C[Client] --> LB[Load Balancer]
    LB --> I1[Instance 1]
    LB --> I2[Instance 2]
    LB --> I3[Instance 3]
    I1 --> R[(Redis Session Store)]
    I2 --> R
    I3 --> R
    I1 --> DB[(Database)]
    I2 --> DB
    I3 --> DB
</div>

---
## Benefits of Statelessness

- Horizontal scaling: add or remove instances freely
- Resilience: losing an instance loses no client state
- Simplicity: no session replication or sticky routing needed
- Portability: instances can run on any host

---
## Stateful Services

- Maintain state that must persist across requests
- Examples: databases, caches, message brokers, search indexes
- Require special handling for scaling, failover, and persistence
- Use persistent volumes and replication strategies

---
## Managing Stateful Services in the Cloud

- Use managed services when possible (`RDS`, `ElastiCache`, `Cloud SQL`)
- For self-managed: use `StatefulSets` in `Kubernetes`
- Implement data replication for high availability
- Plan for backup, restore, and disaster recovery

---
## Stateful vs Stateless Summary

| Aspect | Stateless | Stateful |
|--------|-----------|----------|
| Scaling | Trivial horizontal | Complex, requires rebalancing |
| Failure recovery | Replace instance | Restore state from replica |
| Deployment | Rolling update | Careful orchestration |
| Examples | API servers, web apps | Databases, caches |

---
## Designing for Elasticity

- Elasticity is the ability to automatically scale resources based on demand
- Scale out (add instances) when load increases
- Scale in (remove instances) when load decreases
- Minimize cost by matching capacity to actual demand

---
## Auto-Scaling Strategies

- Reactive: scale based on current metrics (CPU, memory, request count)
- Predictive: scale based on historical patterns (time of day, day of week)
- Scheduled: pre-scale for known events (product launches, sales)
- Custom metrics: scale on business-specific indicators (queue depth)

---
## Auto-Scaling Architecture

<div class="mermaid">
graph TD
    M[Metrics Collector] -->|CPU > 70%| AS[Auto Scaler]
    AS -->|Scale Out| IG[Instance Group]
    IG --> I1[Instance 1]
    IG --> I2[Instance 2]
    IG --> I3[Instance 3 - New]
    M -->|CPU < 30%| AS
    AS -->|Scale In| IG
</div>

---
## Designing for Scalability

- Identify bottlenecks before they become problems
- Use caching to reduce load on databases and external services
- Partition data to distribute load across multiple nodes
- Design APIs with pagination and rate limiting built in

---
## Horizontal vs Vertical Scaling

<svg viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="100" width="60" height="80" fill="#81C784" stroke="#333" stroke-width="1" rx="3"/>
  <rect x="20" y="20" width="60" height="80" fill="#A5D6A7" stroke="#333" stroke-width="1" rx="3"/>
  <text x="50" y="145" text-anchor="middle" font-size="10">Server</text>
  <text x="50" y="65" text-anchor="middle" font-size="10">More RAM/CPU</text>
  <text x="50" y="195" text-anchor="middle" font-size="11" font-weight="bold">Vertical</text>
  <rect x="200" y="100" width="50" height="80" fill="#64B5F6" stroke="#333" stroke-width="1" rx="3"/>
  <rect x="260" y="100" width="50" height="80" fill="#64B5F6" stroke="#333" stroke-width="1" rx="3"/>
  <rect x="320" y="100" width="50" height="80" fill="#64B5F6" stroke="#333" stroke-width="1" rx="3"/>
  <rect x="380" y="100" width="50" height="80" fill="#90CAF9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="145" text-anchor="middle" font-size="9">S1</text>
  <text x="280" y="145" text-anchor="middle" font-size="9">S2</text>
  <text x="340" y="145" text-anchor="middle" font-size="9">S3</text>
  <text x="400" y="145" text-anchor="middle" font-size="9">S4 New</text>
  <text x="310" y="195" text-anchor="middle" font-size="11" font-weight="bold">Horizontal</text>
</svg>

---
## Caching Strategies

- Client-side caching: browser cache, CDN edge caches
- Application-level caching: in-memory cache like `Redis` or `Memcached`
- Database query caching: materialized views, query result caching
- Cache-aside pattern: application checks cache first, loads from DB on miss

---
## Cache-Aside Pattern

<div class="mermaid">
sequenceDiagram
    participant App
    participant Cache
    participant DB
    App->>Cache: Get(key)
    Cache-->>App: Cache Miss
    App->>DB: Query
    DB-->>App: Data
    App->>Cache: Set(key, data)
    Note over App: Next request
    App->>Cache: Get(key)
    Cache-->>App: Cache Hit - Return Data
</div>

---
## Data Partitioning

- Horizontal partitioning (sharding): split rows across databases
- Vertical partitioning: split columns or tables across databases
- Functional partitioning: split by business capability
- Choose a partition key that distributes load evenly

---
## Cloud-Native Design Checklist

- Services are stateless and externalize state
- Configuration comes from the environment
- Dependencies are explicitly declared
- Logs stream to `stdout`
- Health checks are exposed for liveness and readiness
- Graceful shutdown handles in-flight requests
- Horizontal scaling is tested and automated

---
## Summary

- Cloud-native applications are designed for the dynamic nature of the cloud
- The 12-Factor methodology provides a foundation for portable, scalable apps
- Stateless services enable horizontal scaling and resilient deployments
- Elasticity matches resource capacity to actual demand
- Caching and partitioning are essential for scalability
- Design every service to be disposable, observable, and independently deployable
