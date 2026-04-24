# Modern Software Architecture Course — Revamp Progress

Tracks the comprehensive restructuring work for `marp/courses/architecting/modern-software-architecture/`.

## Status legend
- [ ] — not started
- [~] — in progress
- [x] — done
- [-] — decided not to do / superseded

---

## Phase 1: Deduplicate existing content

- [x] **Ch 2** — remove Saga Pattern section (slides 402–415); keep in ch 7
- [x] **Ch 2** — remove Circuit Breaker section (slides 434–442); keep in ch 11
- [x] **Ch 2** — remove Backpressure / Rate Limiting section (slides 446–461); keep in ch 11
- [x] **Ch 2** — remove Observability Logs/Metrics/Traces teaser (slides 463–472); ch 12 owns this
- [x] **Ch 2** — remove Chaos Engineering section (slides 475–487); keep in ch 11
- [x] **Ch 2** — remove duplicate CAP diagram slide (keep one of the two)
- [x] **Ch 10** — remove duplicate K8s architecture SVG slide (keep one)
- [x] **Ch 11** — remove duplicate Cascade Effect slide (slide 52 duplicates 39)
- [x] **Ch 12** — remove duplicate Observability Pillars slide (keep one)
- [x] **Ch 13** — consolidate duplicate CI pipeline SVG slides

## Phase 2: Ch 2 cleanup

- [x] **Ch 2** — theory topics (FLP, Lamport, Vector clocks, BFT, Gossip, Split-Brain) woven inline alongside original content
- [x] **Ch 2** — theory topics placed in logical flow, not appended
- [x] **Ch 2** — regenerated Summary to reflect new content

## Phase 3: Re-ordering

- [x] Swap ch 6 (DDD) to appear before ch 4 (RDBMS) — new order: 01, 02, 03, 06→04, 04→05, 05→06, 07...
- [x] Verify all internal cross-references after renaming
- [x] Rename directories in `svg/courses/architecting/modern-software-architecture/` to match

## Phase 4: Extract deployment strategies

- [x] Moved Blue/Green, Canary, Rolling Update, Feature Flags into new ch 12 Release Strategies
- [x] Kept CI/CD pipelines, IaC, GitOps, Expand-and-Contract in ch 14
- [x] Renumbered: Monitoring moved 12→13, DevOps moved 13→14; chapters 15–19 added

## Phase 5: Trim bloat

- [-] **Ch 7** — Shared Database Anti-Pattern was already 1 slide; no change needed
- [x] **Ch 8** — compressed 12 one-slide factors into 4 grouped slides
- [x] **Ch 9** — removed duplicate Container vs VM SVG slide
- [x] **Ch 13** — removed Recreate Deployment slide

## Phase 6: Content fixes

- [x] **Ch 12** — nuanced the Shallow vs Deep Health Check advice
- [-] **Ch 5** — polyglot persistence already placed well; no move needed
- [x] **Ch 10** — added Operators / CRDs section (5 new slides)
- [x] **Ch 11** — expanded Service Mesh (sidecars, mTLS, traffic shaping, when not to use) (5 new slides)

## Phase 7: New chapters

- [x] **New chapter: Security Architecture**
    - OAuth2 / OIDC / JWT
    - mTLS
    - RBAC vs ABAC
    - Secrets management & rotation
    - Zero-trust networking
    - Threat modeling (STRIDE)
    - Architectural OWASP concerns
- [x] **New chapter: API Design**
    - Contract-first design
    - OpenAPI / AsyncAPI
    - Versioning strategy (expanded)
    - Consumer-driven contract testing
    - GraphQL trade-offs
    - API-first principle
- [x] **New chapter: Testing Distributed Systems**
    - Testing pyramid for microservices
    - Contract testing (Pact)
    - Integration vs end-to-end trade-offs
    - Shadow traffic / dark launches
    - Testing in production
    - Synthetic monitoring
- [x] **New chapter: Performance & Capacity Planning**
    - Little's Law
    - Back-of-envelope capacity math
    - Load testing (k6, Gatling, Locust)
    - Percentile-based SLOs
    - Cost modeling
- [x] **New chapter: Event Streaming & Data Pipelines**
    - Kafka architecture deep-dive
    - CDC (Debezium)
    - Outbox pattern
    - Stream processing (Flink, Kafka Streams)
    - Event sourcing at scale

## Phase 8: Build & verify

- [x] Run `rsconstruct build --verbose -j10` after each chapter edit
- [x] Run `scripts/check_md.py --images` to verify all image refs (runs inside rsconstruct)
- [x] Run `scripts/check_svg.py --dimensions --fonts --fit` (runs inside rsconstruct)
- [x] Final full build — 0 failures, all 19 chapters + title.pdf built

---

## Notes / decisions

- Chapter numbering will shift several times; track SVG directory renames alongside
- Every new chapter needs its own SVG directory under `svg/courses/architecting/modern-software-architecture/`
- New SVGs must use project palette, `viewBox="0 0 1280 720"`, content fit to `[40,1240] x [40,620]`
