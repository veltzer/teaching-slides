---
tags:
  - concepts:architecture
  - infrastructure:cloud-native
  - concepts:twelve-factor
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Cloud-Native Principles

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
## Twelve Factor App

![twelve_factor_app](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/twelve_factor_app.svg)

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

![backing_services_diagram](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/backing_services_diagram.svg)

---
## Factor 5: Build, Release, Run

- Strict separation between build, release, and run stages
- Build: converts code into an executable bundle
- Release: combines build with configuration for a specific environment
- Run: launches the application in the execution environment

---
## Build, Release, Run Pipeline

![build_release_run_pipeline](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/build_release_run_pipeline.svg)

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

![concurrency_model](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/concurrency_model.svg)

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

![stateless_service_architecture](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/stateless_service_architecture.svg)

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

![auto_scaling_architecture](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/auto_scaling_architecture.svg)

---
## Designing for Scalability

- Identify bottlenecks before they become problems
- Use caching to reduce load on databases and external services
- Partition data to distribute load across multiple nodes
- Design APIs with pagination and rate limiting built in

---
## Horizontal vs Vertical Scaling

![horizontal_vs_vertical_scaling](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/horizontal_vs_vertical_scaling.svg)

---
## Caching Strategies

- Client-side caching: browser cache, CDN edge caches
- Application-level caching: in-memory cache like `Redis` or `Memcached`
- Database query caching: materialized views, query result caching
- Cache-aside pattern: application checks cache first, loads from DB on miss

---
## Cache-Aside Pattern

![cache_aside_pattern](svg/courses/architecting/modern-software-architecture/08_cloud_native_principles/cache_aside_pattern.svg)

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
