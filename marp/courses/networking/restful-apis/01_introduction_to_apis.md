---
tags:
  - networking:rest
level: beginner
category: networking
audience:
  - audiences:developers

---
# Introduction to APIs

---
## What This Chapter Covers

- What is an API
- Why APIs matter
- API styles
- Client-server model
- RESTful vs other styles

---
## What An API Is

- Application Programming Interface
- Contract between systems
- One service exposes capabilities; another consumes them
- Hides implementation

---
## Why APIs

- Reuse functionality
- Compose systems
- Cross-language interop
- Decoupling: change one side without breaking the other

---
## Web APIs

- APIs over HTTP
- Most common today
- Used by: web apps, mobile, integrations
- Language agnostic

---
## API Styles

- REST: resources + HTTP verbs
- GraphQL: query language
- RPC: remote procedure calls (gRPC, JSON-RPC)
- SOAP: legacy, XML-based

---
## Client-Server

- Client makes requests
- Server processes and responds
- Stateless or stateful
- Foundation of web

---
## Synchronous vs Asynchronous

- Sync: client waits for reply
- Async: callback, polling, webhooks
- Most REST is sync
- Long-running: async patterns

---
## API Consumers

- Frontend apps (web, mobile)
- Other backend services
- Third-party integrations
- Internal tools

---
## API Producers

- Build the API
- Document it
- Version it
- Operate it (uptime, performance)

---
## Why REST Won

- Built on HTTP, leverages caching, proxies
- Simple mental model
- Browser-friendly
- Tooling ubiquitous

---
## Rest's Limits

- Over- and under-fetching
- Many endpoints for related data
- Versioning is hard
- GraphQL and gRPC fill gaps

---
## Common API Mistakes

- No documentation
- Inconsistent naming
- Returning HTML errors from JSON APIs
- Versioning ignored until breaking change
- No deprecation policy
