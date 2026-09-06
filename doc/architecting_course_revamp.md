# Architecting Course — Revamp Progress

Tracks the restructuring work for `marp/courses/architecting/architecture-patterns/`.

## Status legend
- [ ] — not started
- [~] — in progress
- [x] — done
- [-] — decided not to do / superseded

---

## Decisions

- **Course role:** Catalog of architectural patterns + data-path/operations deep-dives at intermediate level. Keeps overlap with `modern-software-architecture/` (advanced) but at a different depth.
- **Final ordering** (planned):
    - 00 Title
    - 01 Introduction & Pattern Taxonomy (new)
    - 02 Communication Patterns
    - 03 System Architectures
    - 04 Internal Code Architectures
    - 05 Classic Structural Patterns
    - 06 Resiliency & Cross-Cutting Patterns
    - 07 Small-Scale Design Patterns (was 12)
    - 08 Database (was 5; absorb Mesh/Sharded from old ch 1)
    - 09 Isolation Levels (was 8)
    - 10 Caching (was 4)
    - 11 Queues (was 11)
    - 12 Kafka (was 9)
    - 13 Data Processing Engines (was 7)
    - 14 Data Lakes (was 6)
    - 15 Big Data (was 2; absorb Lambda/Kappa from old ch 1)
    - 16 Workflows (was 13)
    - 17 Monitoring (was 10; absorb Throttling from old ch 1)

---

## Phase 1: Quick fixes

- [x] Rename `03_borderline.md` to descriptive name (now ch 05)
- [x] Fix ch 2 stray "Modern Architecture Course" heading (gone in renumbering)
- [x] Delete duplicate Cache-Aside in old ch 3
- [x] Standardize ch 1 heading prefixes (Circuit Breaker, Saga, Kappa, Lambda)

## Phase 2: Split ch 1 into scope-based chapters

- [x] Extract Communication Patterns (Client-Server, Broker, P2P, Event Bus, Pub-Sub) into new ch 02
- [x] Extract System Architectures (Monolith, Modular Monolith, Microservices, SOA, EDA, Serverless, Space-Based, Share-Nothing) into new ch 03
- [x] Extract Internal Code Architectures (DDD, CQRS, Event Sourcing, Hexagonal, Clean, Onion, Microkernel) into new ch 04
- [x] Extract Classic Structural Patterns (Layered, Master-Slave, Pipe-Filter, Blackboard) from old ch 3 into new ch 05
- [x] Extract Resiliency & Cross-Cutting (Circuit Breaker, Bulkhead, Saga, Strangler Fig, BFF, API Gateway, ACL, DB-per-Service, Geode, Ambassador, Sidecar, Valet Key, Throttling) into new ch 06
- [x] Distribute Kappa/Lambda → Big Data; Mesh/Sharded → Database; Throttling stays in Resiliency chapter
    - Throttling is in ch 06. Mesh and Sharded pattern sections added to ch 08 (Overview/Diagram/Pros/Cons/When-to-Use, between Sharding Implementation and High Availability). Lambda/Kappa expanded in ch 15 from bare diagram-only slides to full pattern sections.

## Phase 3: New introduction chapter

- [x] Write 01 Introduction & Pattern Taxonomy

## Phase 4: Renumber data/ops chapters

- [x] Move ch 12 (Small-Scale) → 07
- [x] Move ch 5 (Database) → 08
- [x] Move ch 8 (Isolation) → 09
- [x] Move ch 4 (Caching) → 10
- [x] Move ch 11 (Queues) → 11 (unchanged)
- [x] Move ch 9 (Kafka) → 12
- [x] Move ch 7 (Data Processing) → 13
- [x] Move ch 6 (Data Lakes) → 14
- [x] Move ch 2 (Big Data) → 15
- [x] Move ch 13 (Workflows) → 16
- [x] Move ch 10 (Monitoring) → 17
- [x] Update SVG dir names to match
- [x] Update SVG path refs in each renamed file

## Phase 5: Title chapter polish

- [x] Make title H1 more descriptive than "Architecting" (now "Architecting Software Systems")

## Phase 6: Cross-chapter cleanup

- [x] Add summary slides to chapters that end abruptly (added in chs 02, 04, 05, 06)
- [x] Standardize diagram naming convention ("X Diagram")
    - ch 02: `Communication Diagram` → `Client-Server Diagram`; bare `Component Roles` → `Client-Server Component Roles`
    - ch 05: `Layer Diagram` → `Layered Diagram`
    - ch 07: `Interaction Diagram` → `MVC Interaction Diagram`; `Interpreter Diagram` → `Interpreter Pattern Diagram`; bare `Overview`/`Component Roles`/`Pros and Cons`/`When to Use` in MVC section prefixed with `MVC`
- [x] Add pattern-index slide in ch 06 (Resiliency)

## Phase 7: Build & verify

- [x] Run rsconstruct build; resolve spell/build errors
- [x] Verify all PDFs and SVG references
- [x] Final clean build (16 new PDFs built; no errors)
