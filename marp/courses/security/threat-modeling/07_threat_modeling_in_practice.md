---
tags:
  - security:threat-modeling
  - concepts:microservices
  - concepts:cloud
  - concepts:apis
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:architects

---
# Threat Modeling in Practice

---
## What This Chapter Covers

- Microservices: service-to-service threats
- Cloud-specific threats and shared responsibility
- API security threat surface
- Threat libraries and reusing knowledge
- MITRE ATT&CK mapping

---
## Microservices Are a Threat Model Multiplier

- More services means more network calls
- Each call is a potential trust boundary
- Identity and authorization span multiple hops
- A single user request now touches dozens of components
- More attack surface, more defense in depth needed

---
## Service-to-Service Threats

- Spoofing — service A pretends to be service B
- Tampering — modified messages in flight
- Confused deputy — service A acts on behalf of attacker without checking
- Replay — captured messages re-sent later
- All resolved with: mutual TLS, signed tokens, request signing

---
## Microservices Threat Map

![microservices_threats](svg/courses/security/threat-modeling/07_threat_modeling_in_practice/microservices_threats.svg)

---
## API Gateway as Trust Boundary

- The major boundary between external and internal
- Authentication, authorization, rate limiting, validation
- A common single point of failure
- Threats: bypassed gateway via internal IP, gateway misconfiguration
- Defense: gateway enforces, services still verify

---
## Service Mesh Considerations

- Mesh handles mTLS, retries, observability
- Threats: misconfigured mesh policies, stale certificates
- Identities live in the mesh — sometimes too coarsely
- Authorization at the mesh layer plus the application layer
- Don't trust the mesh blindly — model what it actually enforces

---
## Container and Orchestration Threats

- Container escape to host
- Lateral movement between pods
- Privileged containers as a privilege-escalation path
- Image supply-chain compromise
- Mitigations: pod security, image signing, network policies, runtime detection

---
## Distributed Authentication

- OAuth2, OIDC, JWT — standard but complex
- Token leakage, refresh-token theft, scope creep
- Token signing keys are crown jewels
- Token expiration vs revocation timeliness
- Threat: long-lived tokens that cannot be revoked quickly

---
## Distributed Authorization

- "Who can do what" across many services
- Centralized policy (OPA, similar) vs per-service code
- Threat: services that re-implement authorization inconsistently
- Threat: implicit trust between internal services
- Pattern: zero-trust within the cluster

---
## Cloud Shared Responsibility

- Provider secures the infrastructure
- Customer secures the configuration and data
- Most cloud breaches are configuration errors
- Threat model the *configuration* of cloud services, not their internals
- Lock down by default; explicitly grant access

---
## Cloud-Specific Threats

- Public buckets — the most famous breach class
- Overprivileged IAM roles — confused deputy at scale
- Exposed metadata service — server-side request forgery target
- Misconfigured load balancers — bypassing internal protections
- Each cloud has a security best-practices checklist — start there

---
## IAM Threat Modeling

- Each role and policy is a potential privilege escalation path
- Cross-account roles — boundary between trust zones
- Service-linked roles — provider's identities in your account
- Identity federation — external IdPs as a new trust source
- Audit IAM as part of every threat model

---
## Storage and Data Access Threats

- Bucket / blob policies — can be public unintentionally
- Database access via public endpoints
- Backups — often less protected than primary
- Snapshot sharing across accounts
- Encryption keys — KMS access is access to data

---
## Network Threats in Cloud

- Security groups too permissive
- VPC peering creates implicit trust
- Egress filtering rarely as strong as ingress
- VPN/transit gateway misconfigurations
- Internal services exposed when they shouldn't be

---
## Serverless Threats

- Shorter-lived contexts — limited ability to detect persistent threats
- Function permissions tend to drift wide
- Cold-start latency considerations push trust assumptions
- Event-source injection — malicious events from queues, storage triggers
- Dependency confusion in package supply chain

---
## Web Application Threat Surface

![web_app_threats](svg/courses/security/threat-modeling/07_threat_modeling_in_practice/web_app_threats.svg)

---
## REST API Threat Surface

- Authentication on every endpoint, not just login
- Authorization per-resource, not just per-endpoint
- IDOR — using ID parameters to access others' data
- Mass assignment — accepting fields you didn't intend
- Rate limiting per user and per endpoint

---
## GraphQL Considerations

- Single endpoint changes the rate-limit model
- Query depth and complexity attacks
- Introspection in production reveals schema
- Authorization at the field level, not just the endpoint
- Persistent queries to limit attack surface

---
## API Authentication Threats

- API keys leaked in client code or logs
- JWT misconfigurations — alg=none, weak keys, missing audience
- OAuth flows misused for non-user contexts
- Long-lived API keys without rotation
- Token in URL — appears in logs, browser history, referer

---
## Input Validation Threats

- Injection: SQL, NoSQL, command, LDAP, XPath
- Deserialization of untrusted data
- Server-side request forgery via URL parameters
- File upload turned into RCE
- Validate at boundaries; sanitize where output is rendered

---
## Rate Limiting and Abuse

- Brute force — slow it down
- Account enumeration via different responses
- Resource exhaustion via expensive endpoints
- Bill exhaustion via cloud-native services
- Abuse-pattern detection at the application layer

---
## Threat Libraries

- Reusable lists of threats per system pattern
- Microsoft Threat Modeling Tool ships one
- OWASP threat library
- Industry-specific: PCI for payments, HIPAA for health
- Build your own organizational library — recurring threats become recurring defenses

---
## Building Your Threat Library

- Start with threats found in real reviews
- Capture: name, description, where it applies, common mitigations
- Tag by element type and methodology category
- Reuse in future reviews — speed and consistency
- Audit annually; threats become obsolete or evolve

---
## MITRE ATT&CK Framework

- Catalog of adversary tactics and techniques
- Tactics: the "why" (initial access, exfiltration)
- Techniques: the "how" (spear phishing, credential dumping)
- Used by red and blue teams alike
- Map your threats to ATT&CK for shared vocabulary with defenders

---
## ATT&CK in Threat Modeling

- For each identified threat, find the matching ATT&CK technique
- The technique page lists detection strategies
- Use detection strategies to drive logging and monitoring requirements
- Bridges threat modeling (design-time) and detection engineering (runtime)
- Increasingly common in security-mature teams

---
## Common Industry Patterns

- E-commerce — fraud, account takeover, payment threats
- SaaS — multi-tenancy, data isolation, IAM
- Finance — regulatory, AML, transactional integrity
- Healthcare — HIPAA, biometric data, medical device interfaces
- Each industry has known threat patterns — start with them

---
## Threat Modeling for ML Systems

- Training data poisoning
- Model inversion — extracting training data from models
- Membership inference — was X in the training set?
- Adversarial examples — inputs crafted to mislead
- Specialized methodology emerging — early days

---
## Anti-Patterns at Scale

- One person owns all threat models — bus-factor of one
- Threat models that nobody reads
- Models that show only the happy path
- "The framework handles it" without verification
- Compliance-only modeling that ignores real attackers

---
## Summary

- Microservices increase trust boundaries — model each
- Cloud threats are mostly configuration, not platform
- API surface needs auth-per-endpoint, validation everywhere
- Threat libraries make modeling repeatable and fast
- MITRE ATT&CK bridges modeling and detection
