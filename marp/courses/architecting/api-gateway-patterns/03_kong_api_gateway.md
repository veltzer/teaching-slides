---
tags:
  - architecture:api-gateway
  - tools:kong
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Kong API Gateway

---
## What This Chapter Covers

- What Kong is
- Architecture: nginx + Lua + plugins
- Installation modes
- Services and routes
- Plugins: the extension model
- Admin API and Konnect
- When Kong fits

---
## What Kong Is

- Open-source API gateway
- Built on nginx + OpenResty (nginx + Lua)
- Plugin-driven: most features are plugins
- Massive plugin ecosystem
- The most-deployed gateway in the open-source world

---
## Architecture

- nginx for HTTP handling
- OpenResty for scripting
- Postgres or Cassandra for state (or DB-less mode)
- Plugins run in the request lifecycle
- Stateless data plane; stateful or stateless control plane

---
## Installation Modes

- **DB-mode**: traditional; central config in Postgres
- **DB-less**: declarative YAML; no DB; redeploy to change
- **Hybrid**: control plane (with DB) + many data planes
- DB-less is the modern choice for K8s
- Hybrid for multi-cluster / multi-region

---
## Services and Routes

```yaml
services:
  - name: users
    url: http://users-svc:8080
    routes:
      - name: users-route
        paths: ["/users"]
        strip_path: false
```

- Service: an upstream (your real service)
- Route: a URL pattern that maps to a service
- One service can have many routes

---
## Plugins

- Authentication: jwt, oauth2, key-auth, basic-auth
- Traffic control: rate-limiting, request-size-limiting
- Transformations: request-transformer, response-transformer
- Logging: file-log, http-log, syslog, datadog
- Hundreds available

---
## Plugin Configuration

```yaml
plugins:
  - name: rate-limiting
    service: users
    config:
      minute: 60
      policy: local
```

- Per-service or per-route
- Config is plugin-specific
- Order matters; documented in plugin docs

---
## Admin API

- REST API for managing Kong
- Add services, routes, plugins via HTTP
- Don't expose to the internet; admin port internal-only
- Tools (deck, decK) sync declarative config

---
## decK

- Tool for declarative Kong management
- One YAML file describes all services / routes / plugins
- `deck sync` applies it
- Same YAML across environments
- The GitOps approach to Kong

---
## Konnect

- Kong's hosted SaaS offering
- Control plane in the cloud
- Data planes you deploy yourself
- Web UI, analytics, RBAC built in
- Commercial; useful at scale

---
## Custom Plugins

- Lua scripts that hook into the request lifecycle
- Hook points: certificate, rewrite, access, header_filter, body_filter, log
- Extends Kong without forking
- Pure Lua API; well documented
- Used for company-specific requirements

---
## Kong vs Alternatives

- **Tyk**: similar feature set; less popular
- **Apigee**: more enterprise; more expensive
- **AWS API Gateway**: managed-only; AWS-coupled
- **Envoy**: lower-level building block
- Kong is mature middle-ground

---
## When Kong Fits

- You want open-source
- You want the plugin ecosystem
- You're comfortable with Lua
- You need to run on prem or multi-cloud
- You need fine-grained control

---
## When Kong Doesn't

- You're all-in on AWS (use API Gateway)
- You want managed-only operations
- Your needs are simple (nginx might do)
- Plugins don't cover your use case (might be Envoy time)

---
## Common Kong Mistakes

- Storing config only in DB; lost on outage
- Custom plugins without testing
- No rate-limiting on admin API
- Forgetting Lua's idiosyncrasies (single global state, blocking I/O)
- Treating Kong as a black box; not learning the request lifecycle
