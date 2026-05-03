---
tags:
  - databases:mongodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Development Tools and Environment

---
## What This Chapter Covers

- Local vs cloud (Atlas)
- mongosh
- Compass
- IDE plugins
- Docker
- Connection strings

---
## Local Install

- macOS: `brew install mongodb-community`
- Linux: distro package or tarball
- Windows: installer
- Service auto-starts

---
## Atlas

- MongoDB's hosted cloud
- Free tier: ~512MB
- Multi-cloud (AWS, GCP, Azure)
- Backups, monitoring included
- Default for new projects

---
## Docker

```bash
docker run -d -p 27017:27017 -v mongo-data:/data/db mongo:7
```

- Quick local DB
- Volume for persistence
- Fine for development

---
## Tooling Landscape

![tooling_landscape](svg/courses/databases/mongodb-for-developers/02_development_tools_and_environment/tooling_landscape.svg)

---
## mongosh

- Modern shell (replaces legacy `mongo`)
- JavaScript-like syntax
- Connect: `mongosh mongodb://localhost:27017`
- Run scripts inline or from file

---
## Compass

- GUI from MongoDB
- Free; cross-platform
- Browse collections, run queries, inspect schema
- Schema analyzer: infer document shapes

---
## IDE Plugins

- VS Code: MongoDB for VS Code
- IntelliJ: built-in (Ultimate)
- Browse, query, explain plans
- Inline within code

---
## Connection Strings

```misc
mongodb://user:pass@host:27017/dbname?retryWrites=true
mongodb+srv://user:pass@cluster.mongodb.net/dbname
```

- `mongodb+srv`: DNS-based for Atlas
- Options: timeouts, replicas, auth

---
## Connection String Anatomy

![connection_string](svg/courses/databases/mongodb-for-developers/02_development_tools_and_environment/connection_string.svg)

---
## Database Users

- Atlas: web UI
- Self-hosted: `db.createUser`
- Per-app users with limited permissions
- Don't use root in apps

---
## SSL/TLS

- Required for Atlas
- Optional for local
- Required for compliance
- Add `?tls=true` to connection string

---
## Multiple Environments

- Dev / staging / prod: separate clusters
- Different connection strings
- Don't share between
- Common pattern: env var `MONGO_URI`

---
## Connection Pooling

- Driver maintains a pool
- Default 100 connections per process
- Tune for high-concurrency apps
- Connection limits on Atlas tier

---
## Common Setup Mistakes

- App connecting as root
- TLS disabled in production
- One huge cluster for all envs
- Hardcoded connection strings
- Not pooling connections (single connection per request)
