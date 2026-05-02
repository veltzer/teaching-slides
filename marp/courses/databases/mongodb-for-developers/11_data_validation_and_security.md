---
tags:
  - databases:mongodb
  - databases:security
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Data Validation and Security

---
## What This Chapter Covers

- Schema validation
- Authentication
- Authorisation / roles
- Encryption (at rest, in transit)
- Field-level encryption
- Auditing

---
## Security Layers

![security_layers](svg/courses/databases/mongodb-for-developers/11_data_validation_and_security/security_layers.svg)

---
## Schema Validation

```javascript
db.createCollection("users", {
    validator: {
        $jsonSchema: {
            required: ["email"],
            properties: {
                email: { bsonType: "string", pattern: "^.+@.+$" }
            }
        }
    }
});
```

- JSON Schema-style
- Strict / moderate level
- Server-side; defence in depth

---
## When To Validate

- Always for production collections
- Especially: high-value data, compliance
- Combine with app-side validation
- Schema validation is a safety net, not a primary guard

---
## Authentication

- Per-user credentials (username + password)
- SCRAM-SHA-256 (default)
- LDAP / Kerberos / X.509 in enterprise
- Atlas: integrated auth providers

---
## Authorisation

- Role-based access control
- Built-in roles: read, readWrite, dbAdmin, userAdmin
- Custom roles for fine-grained control
- Per-database; cluster-wide for admin

---
## Best Practice Permissions

- App users: readWrite on their database only
- Read-only analytics user: read
- No app uses dbOwner / root
- Audit periodically

---
## Encryption At Rest

- WiredTiger: enterprise feature
- KMIP key management
- Atlas: enabled by default
- Compliance check-mark

---
## Encryption In Transit

- TLS to the cluster
- Required in Atlas
- Self-signed for dev; CA for prod
- Required for compliance

---
## Field-Level Encryption

- Specific fields encrypted before sending to DB
- Driver handles
- Server can't read those fields
- Client-side keys; server-side queryable encryption (newer)

---
## Queryable Encryption

- MongoDB 6+
- Equality queries on encrypted fields
- Server holds encrypted index
- Strongest encryption; some performance cost

---
## Auditing

- Enterprise / Atlas feature
- Log: connections, commands, schema changes
- Forwarded to syslog / SIEM
- Compliance use case

---
## SQL Injection (NoSQL Equivalent)

- Don't pass raw user input as query operators
- "{ '$where': userInput }" — code injection
- Use the driver's typed APIs
- Validate input before queries

---
## Connection Security

- Don't expose MongoDB to the internet
- VPC + bastion / VPN
- IP allowlists in Atlas
- Strong passwords + auth always

---
## Backup Encryption

- Backups encrypted too
- Atlas: handled
- Self-hosted: encrypt the backup files
- Compliance requirement

---
## Common Security Mistakes

- App connecting as root
- No TLS in production
- Schema validation set to "moderate" but never enforced
- Unprotected MongoDB on the internet (still happens!)
- Backups in plaintext
