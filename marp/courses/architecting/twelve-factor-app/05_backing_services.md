---
tags:
  - concepts:architecture
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Factor IV: Backing Services

---

## The Rule

- Treat backing services as attached resources
- A backing service is anything the app talks to over the network
- Swappable without code changes — only config changes

---

## Attached Resources

![attached_resources](svg/courses/architecting/twelve-factor-app/05_backing_services/attached_resources.svg)

---

## What Counts as a Backing Service

- Databases (Postgres, MySQL, MongoDB)
- Caches (Redis, Memcached)
- Message brokers (Kafka, RabbitMQ, NATS)
- Email senders (SES, SendGrid)
- Object stores (S3, Azure Blob)
- Third-party APIs (Stripe, Twilio)
- Internal services (other microservices)

---

## What "Attached Resource" Means

- The app addresses the resource by URL or DNS, not by class instance
- The app has no special knowledge of where the resource is or who runs it
- "Local Postgres in dev, RDS in prod, with no code change" is the goal

---

## Local vs Third-Party Resources

- A locally-managed Postgres and a third-party-managed Postgres are interchangeable
- Code shouldn't care about ownership
- Migration is a config change, not a code change
- This is the freedom factor IV gives you

---

## Anti-Patterns

- Hardcoded service hostnames
- Code that branches on "are we in dev?" to use a different service type
- Importing third-party SDKs that lock you to one provider
- "We can't switch from Stripe because the integration is everywhere"

---

## The Adapter Pattern Helps

- Wrap each backing service behind a small interface
- The app talks to the interface
- The implementation reads URL/credentials from config
- Swapping providers becomes implementing a new adapter

---

## Service Discovery

- Static config (env vars) works for most cases
- Dynamic discovery (Consul, Kubernetes services, DNS-SD) for elastic environments
- DNS plus a load balancer is the most common pattern
- Whatever the mechanism, the app sees a URL/hostname

---

## Resource Replacement at Runtime

- A backing service can be replaced without restarting the app
- Database failover, cache restart, broker rotation — the app reconnects
- Requires connection pooling and retry logic at the adapter level
- Not a magic property; it's an explicit capability the app builds

---

## Reasonable Compliance Test

- Can you point the app at a different Postgres instance with one env var change?
- Can you replace Redis with a different cache implementation cleanly?
- Can dev use a local SQS-mock and prod use real SQS without code changes?
- If yes, factor IV is satisfied

---

## Summary

- Backing services are addressed by URL/hostname through config
- Local and remote services are interchangeable
- Adapters insulate code from specific providers
- Replacement at runtime is a feature the app builds, not a default
