---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Security

---

## What This Chapter Covers

- Security features that are enabled by default in modern releases
- TLS/SSL for both transport and HTTP layers with certutil
- Authentication realms: native, file, and LDAP/Active Directory
- Role-based access control with cluster and index privileges
- API keys and tokens for programmatic access
- Field-level and document-level security
- Audit logging plus SAML and OIDC single sign-on

---

## Security Enabled by Default

- Since 8.x, security is on out of the box on new clusters
- First startup auto-generates certificates and the `elastic` password
- HTTPS and authentication are required from the start
- An enrollment token simplifies adding nodes and Kibana
- Disabling security is strongly discouraged for any real cluster

```yaml
xpack.security.enabled: true
xpack.security.enrollment.enabled: true
```

---

## The Two TLS Layers

- Transport layer: node-to-node traffic inside the cluster
- HTTP layer: client-to-cluster REST traffic (Kibana, apps)
- Transport TLS is mandatory once security is enabled
- HTTP TLS protects credentials and data in transit
- Each layer has its own keystore, truststore, and settings
- Verification modes: `full`, `certificate`, or `none`

---

## Generating Certificates with certutil

- `elasticsearch-certutil` builds a CA and node certificates
- Start with a CA, then issue per-node or cluster certs
- Store the resulting `.p12` files in the node `config/certs/`
- Protect private key passwords in the secure keystore

```bash
bin/elasticsearch-certutil ca --out elastic-ca.p12
bin/elasticsearch-certutil cert --ca elastic-ca.p12 \
  --name node1 --out node1.p12
bin/elasticsearch-keystore add \
  xpack.security.transport.ssl.keystore.secure_password
```

---

## Transport TLS Configuration

- Configure the transport SSL block in `elasticsearch.yml`
- Use `verification_mode: full` to validate hostnames and chain
- All nodes must trust the same CA to join the cluster

```yaml
xpack.security.transport.ssl:
  enabled: true
  verification_mode: full
  keystore.path: certs/node1.p12
  truststore.path: certs/node1.p12
```

---

## HTTP TLS Configuration

- Enables HTTPS on port 9200 for clients and Kibana
- Clients must trust the CA or present the right fingerprint
- Often uses a separate cert with the public DNS name

```yaml
xpack.security.http.ssl:
  enabled: true
  keystore.path: certs/http.p12
  truststore.path: certs/http.p12
```

---

## Authentication Realms

- A realm is an authentication backend; realms form a chain
- Built-in realms: `native`, `file`, `ldap`, `active_directory`
- Realms are tried in `order`; lower numbers checked first
- Mix internal and external realms in one chain
- Reserved users (`elastic`, `kibana_system`) live in native realm

```yaml
xpack.security.authc.realms:
  native.native1.order: 0
  file.file1.order: 1
```

---

## Native and File Realms

- Native realm stores users in a special ES index, managed via API
- File realm stores users in `users`/`users_roles` config files
- File realm survives even if the cluster index is unavailable
- Use the file realm for emergency/break-glass accounts
- Manage native users with the user management REST API

```bash
bin/elasticsearch-users useradd ops_admin -p secret -r superuser
```

---

## LDAP and Active Directory

- Externalize authentication to a corporate directory
- LDAP realm binds and searches for users and groups
- Active Directory realm is tailored to AD's structure
- Map directory groups to ES roles via role mapping
- Use a bind user (or bind DN) stored in the keystore

```yaml
xpack.security.authc.realms.ldap.ldap1:
  order: 2
  url: "ldaps://ldap.corp:636"
  bind_dn: "cn=esbind,ou=svc,dc=corp,dc=com"
  user_search.base_dn: "ou=users,dc=corp,dc=com"
  group_search.base_dn: "ou=groups,dc=corp,dc=com"
```

---

## Role-Based Access Control

- Authorization is driven entirely by roles
- A role grants cluster privileges and index privileges
- Cluster privileges: `monitor`, `manage`, `manage_ilm`, etc.
- Index privileges: `read`, `write`, `create_index`, `view_index_metadata`
- Assign roles to users directly or via role mapping

```bash
POST _security/role/logs_reader
{
  "cluster": ["monitor"],
  "indices": [
    { "names": ["logs-*"], "privileges": ["read", "view_index_metadata"] }
  ]
}
```

---

## Creating Users and Assigning Roles

- Create native users and attach one or more roles
- Roles are additive — the union of privileges applies
- Built-in roles cover common cases (`viewer`, `editor`, `kibana_admin`)

```bash
POST _security/user/jdoe
{
  "password": "changeme!",
  "roles": ["logs_reader", "kibana_admin"],
  "full_name": "Jane Doe",
  "email": "jdoe@corp.com"
}
```

---

## Role Mapping

- Maps external identities (LDAP/SAML/OIDC) to ES roles
- Rules match on username, groups, realm, or metadata
- Avoids managing users twice when using external auth

```bash
POST _security/role_mapping/ldap_admins
{
  "roles": ["superuser"],
  "enabled": true,
  "rules": {
    "all": [
      { "field": { "realm.name": "ldap1" } },
      { "field": { "groups": "cn=es-admins,ou=groups,dc=corp,dc=com" } }
    ]
  }
}
```

---

## API Keys and Tokens

- API keys give applications scoped, revocable credentials
- Keys can carry their own role descriptors (least privilege)
- Set an expiration; rotate and invalidate keys regularly
- Bearer tokens (OAuth2) suit short-lived interactive sessions

```bash
POST _security/api_key
{
  "name": "ingest-app",
  "expiration": "30d",
  "role_descriptors": {
    "writer": { "indices": [
      { "names": ["events-*"], "privileges": ["create_doc"] } ] }
  }
}
```

---

## Field- and Document-Level Security

- Field-level security limits which fields a role can read
- Document-level security filters which docs a role can see via a query
- Both are defined inside the index privileges of a role
- Useful for multi-tenant indices and PII restrictions

```bash
POST _security/role/tenant_a
{
  "indices": [{
    "names": ["shared-*"],
    "privileges": ["read"],
    "field_security": { "grant": ["title", "body"] },
    "query": { "term": { "tenant": "a" } }
  }]
}
```

---

## Audit Logging

- Records security-relevant events to a dedicated audit log
- Captures authentication success/failure, access granted/denied
- Include or exclude event categories to control volume
- Essential for compliance and forensic investigations

```yaml
xpack.security.audit.enabled: true
xpack.security.audit.logfile.events.include:
  - access_denied
  - authentication_failed
```

---

## SAML and OIDC Single Sign-On

- SAML and OIDC integrate Kibana with enterprise identity providers
- Configure a SAML or OIDC realm in `elasticsearch.yml`
- Kibana redirects users to the IdP for login
- Map IdP groups/claims to ES roles via role mapping
- Centralizes MFA and SSO policy at the identity provider

```yaml
xpack.security.authc.realms.saml.saml1:
  order: 3
  idp.metadata.path: saml/idp-metadata.xml
  idp.entity_id: "https://idp.corp/"
  sp.entity_id: "https://kibana.corp/"
  attributes.principal: "nameid"
  attributes.groups: "groups"
```

---

## Security Hardening Checklist

- Keep security enabled; never expose ES without auth/TLS
- Use `verification_mode: full` for transport and HTTP
- Apply least-privilege roles; avoid handing out `superuser`
- Prefer scoped, expiring API keys over shared passwords
- Maintain a file-realm break-glass account
- Enable audit logging and ship logs off-cluster

---

## Chapter Summary

- Security is on by default with auto-TLS and the `elastic` user
- certutil builds the CA and certs for transport and HTTP layers
- Realm chains support native, file, LDAP/AD, SAML, and OIDC
- RBAC grants cluster/index privileges, refined by FLS and DLS
- API keys provide scoped, revocable application access
- Audit logging and SSO round out an enterprise-ready posture
