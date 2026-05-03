---
tags:
  - concepts:microservices
  - concepts:databases
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Data Management Patterns

---
## Database-per-Service

![database_per_service](svg/courses/architecting/microservices-architecture/07_data_management/database_per_service.svg)

---
## Database Per Service

- Each service has its own database
- No service reads or writes another service's database directly
- Cross-service data access goes through APIs
- This is the foundation of decoupling

---
## Why Database Per Service

- Independent schema evolution
- Independent scaling
- Independent technology choice (Postgres, MongoDB, Elasticsearch)
- Data ownership is unambiguous
- The service can change its model without breaking others

---
## The Cost: Distributed Data

- No cross-service joins
- No cross-service transactions
- Data duplication is inevitable
- Eventual consistency between services

---
## Cross-Service Joins

- The need: report combining order data and customer data
- The wrong fix: query across two service databases
- The right fix: a read model or a reporting service that aggregates
- Or: fetch from each service via API and join in code

---
## Cross-Service Transactions

- ACID transactions don't span services
- Use sagas (separate course): sequence of local transactions with compensations
- Don't use 2PC: it doesn't scale and breaks availability

---
## Data Duplication

- A service may need data owned by another service
- Pull on demand: query the API every time (latency, coupling)
- Cache: query and store locally with TTL (eventual consistency)
- Subscribe to events: keep a local read model up to date (most flexible)

---
## Event-Driven Data Sync

- Owning service publishes events when its data changes
- Subscribing services maintain local copies
- Each subscriber decides which fields to keep
- The owning service stays the source of truth

---
## CQRS Across Services

- Each service has its write model and its read models
- Read models can be built from local writes plus events from other services
- Per-service: see the CQRS course
- Across services: each subscribes to the events it cares about

---
## Saga Coordination Patterns

![saga_patterns](svg/courses/architecting/microservices-architecture/07_data_management/saga_patterns.svg)

---
## Outbox Pattern

- A service writes its state and an event in the same database transaction
- A separate process reads the outbox and publishes to the broker
- Guarantees: state and event are committed together (or both fail)
- Common solution to "I changed my row but the event didn't go out"

---
## Polyglot Persistence

- Pick the database that fits the service's workload
- Postgres for transactional state
- Elasticsearch for search
- Redis for caches and counters
- Object storage for blobs
- Different services can use different stores for different reasons

---
## Reference Data

- Some data is read-mostly and used by many services (countries, currencies)
- Don't have every service own its own copy of "list of countries"
- A reference data service serves it; or include it in a shared library
- "Reference" means "rarely changes"

---
## Reporting and Analytics

- Reports often need data from many services
- Build a separate analytics database
- Each service publishes events; an ETL or streaming process loads them into the analytics DB
- This is a read-only consumer of the system; it doesn't impose constraints back

---
## Anti-Patterns

- Shared database across services
- Cross-service ORM with foreign keys
- Distributed transactions (2PC)
- Direct database reads from another service
- "Just one shared cache for all services"

---
## Summary

- Database per service; no shared databases
- Cross-service data via APIs or events
- Eventual consistency is the cost; saga handles transactions
- Outbox pattern for "row + event" atomicity
- Polyglot persistence; reference data via a service
