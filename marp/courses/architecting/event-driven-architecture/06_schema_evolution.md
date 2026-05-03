---
tags:
  - concepts:schema
  - concepts:governance
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Event Schema Evolution and Governance

---
## What This Chapter Covers

- Why schemas matter in event-driven systems
- Compatibility modes: backward, forward, full
- Schema registries
- Versioning strategies
- Event contracts and ownership

---
## Why Schemas Matter

- Events outlive the code that produced them
- Consumers depend on shape, not just content
- An undocumented schema is a surprise waiting
- Without enforcement, drift is inevitable
- The schema is the contract

---
## The Compatibility Problem

- Producer publishes events with schema v1
- Consumers built against v1 read those events
- Producer wants to change the schema for v2
- Old consumers must still work with v2 events
- New consumers must still read v1 events from history

---
## Backward Compatibility

- New schema can read data written by old schema
- Adding optional fields with defaults is safe
- Removing required fields is not
- Renaming fields is not
- Most teams aim for backward compatibility

---
## Forward Compatibility

- Old schema can read data written by new schema
- Old code skips unknown fields
- Removing fields breaks; adding is safe
- Required for slow upgrades — old consumers continue working
- Combined with backward = full compatibility

---
## Full Compatibility

- Old reads new; new reads old
- The strictest constraint
- Effectively: no removed fields, no renamed fields, optional with defaults
- A high bar — but the safest contract
- Use for cross-team, cross-org events

---
## Compatibility Visualized

![schema_compatibility](svg/courses/architecting/event-driven-architecture/06_schema_evolution/schema_compatibility.svg)

---
## Registry Workflow

![registry_workflow](svg/courses/architecting/event-driven-architecture/06_schema_evolution/registry_workflow.svg)

---
## Schema Registries

- A central service that stores and validates schemas
- Producers register schemas before publishing
- Consumers fetch schemas to deserialize
- The registry enforces compatibility rules
- Confluent, AWS Glue, Apicurio are common

---
## How a Registry Helps

- Prevents incompatible schema changes from being deployed
- Provides a discoverable catalog of events
- Versions schemas; consumers pin or auto-upgrade
- Enables tooling: codegen, contract tests, dashboards
- A non-negotiable piece of infrastructure for serious EDA

---
## Confluent Schema Registry

- The most-used registry, especially with Kafka
- Supports Avro, Protobuf, JSON Schema
- Compatibility levels per topic
- Integrates with Kafka clients automatically
- Open-source core; commercial features

---
## Versioning Strategies

- Implicit: registry tracks versions; clients fetch by ID
- Embedded: version field inside the event
- Topic-based: `orders.v1`, `orders.v2` separate topics
- Each strategy has trade-offs
- Pick one and document it

---
## Implicit Versioning (Schema Registry)

- Each schema version has a unique ID stored in the registry
- Producer attaches schema ID to each event
- Consumer fetches schema by ID
- Transparent to application code
- Best when you have a registry already

---
## Embedded Versioning

- Field inside the event payload: `"version": 2`
- Consumer code branches per version
- Manual but explicit
- Works without a registry
- Code gets messy as versions accumulate

---
## Topic-Based Versioning

- New version means a new topic
- Producer publishes to multiple topics during transition
- Consumers gradually move
- Old topic eventually deprecated and deleted
- Heaviest, but cleanest separation

---
## Handling Breaking Changes

- Sometimes a breaking change is unavoidable
- Strategy 1: bump major version, run two streams in parallel
- Strategy 2: tombstone events to mark schema transitions
- Strategy 3: rebuild consumers before changing producer
- Coordinate across teams; never break silently

---
## Field Removal Strategy

- Mark field deprecated in producers; emit but ignore
- Update consumers to stop reading the field
- Wait for the deprecation period
- Stop emitting in producers
- The slow path is the safe path

---
## Field Addition Strategy

- Add as optional with a default
- Emit from producers immediately
- Consumers can read or ignore
- New consumers use the field; old consumers don't see it
- Easy because schemas allow optional fields

---
## Field Rename Strategy

- Don't rename — add a new field, deprecate the old
- Both fields populated for the deprecation period
- Consumers migrate one by one
- Eventually drop the old field
- "Rename" is forever in event-sourced systems

---
## Event Catalogs

- Discoverability matters as event count grows
- A central catalog: event name, schema, owner, consumers
- Searchable, queryable, linked to schema versions
- Tools: AsyncAPI, custom portals, Backstage
- Helps onboard new consumers quickly

---
## Event Ownership

- Each event has an owner (team, service)
- Owner is responsible for schema and behavior
- Changes require owner approval
- Like API ownership, but for events
- Document in CODEOWNERS or equivalent

---
## Producer-Consumer Contracts

- Beyond the schema: behavior expectations
- Frequency, ordering guarantees, retention
- Documented in human-readable form alongside the schema
- Consumer-driven contract testing where useful
- A contract is more than a JSON shape

---
## Contract Testing

- Producer publishes test events; consumers verify they can process
- Pact, Spring Cloud Contract, custom frameworks
- Catches breakage in CI before production
- Required for serious cross-team event flows
- Supplements compatibility checks; doesn't replace them

---
## Avro Schema Evolution

- Native compatibility checking via the Avro spec
- Default values enable additions without breakage
- Schema resolution maps writer's schema to reader's
- Strong fit with Kafka and Confluent ecosystem
- Industry standard for evolving binary events

---
## Protobuf Schema Evolution

- Numbered fields; never reuse a number
- Optional and repeated for safety
- `reserved` keyword to prevent accidental reuse
- Required is gone in proto3 — embrace it
- Buf provides linting and breaking-change detection

---
## JSON Schema Evolution

- Flexible but undisciplined by default
- Add `additionalProperties: false` to enforce strict mode
- Validate at the edges; don't trust JSON's permissiveness
- Tools: a JSON Schema validator
- Cleanest with explicit schema files in version control

---
## Common Pitfalls

- Treating events as transient and not versioning them
- Producer changes schema; consumers break in production
- Not having a registry until 100 services later
- Documentation that drifts from reality
- Renaming fields "just this once"

---
## Building a Governance Practice

- Schema reviews like code reviews
- Compatibility checks in CI
- Owner approval for changes
- Deprecation policy with dates
- Quarterly catalog audit

---
## Summary

- Schemas are the contract; respect it
- Backward, forward, or full — choose your compatibility
- Registries enforce compatibility automatically
- Avro and Protobuf have first-class evolution support
- Discipline scales; chaos doesn't
