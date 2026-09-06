---
tags:
  - data-and-ai:airflow
  - infrastructure:security
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers
  - audiences:devops

---

# Connections, Variables, and Security

---

## What This Chapter Covers

- Connections
- Variables
- Secrets backends
- Authentication
- Authorisation
- Best practices

---

## Connections

- Reusable definitions: host, user, password, port
- "postgres_default", "s3_default"
- Used by hooks / operators
- Centralised credential management

---

## Secrets Layers

![secrets_layers](svg/courses/data_engineering/apache-airflow/07_connections_variables_and_security/secrets_layers.svg)

---

## Defining A Connection

- UI: Admin &#8594; Connections
- CLI: `airflow connections add ...`
- Env var: `AIRFLOW_CONN_<NAME>`
- Code: less common

---

## Variables

- Key-value pairs
- For: configuration, environment-specific values
- Less structured than Connections
- "max_retries", "data_lake_path"

---

## Reading Variables

```python
from airflow.models import Variable
v = Variable.get('max_retries', default_var='3')
```

- In DAG code: lazy (don't read at top level)
- Better: use Jinja: `{{ var.value.max_retries }}`

---

## Secrets Backends

- HashiCorp Vault
- AWS Secrets Manager
- GCP Secret Manager
- Azure Key Vault
- External secret store; Airflow looks up

---

## Why Secrets Backend

- No secrets in metadata DB
- Centralised rotation
- Audit access
- Compliance

---

## Authentication

- LDAP, OAuth, Kerberos, custom
- Default: basic auth (username + password)
- For prod: integrate with company SSO

---

## Authorisation

- Roles: Admin, Op, User, Viewer, Public
- Per-DAG ACLs (in Airflow 2+)
- "Team A can only view team A's DAGs"

---

## RBAC

- Built-in: based on Flask-AppBuilder
- Roles + permissions
- Custom roles possible

---

## DAG-Level Permissions

- access_control argument on DAG
- Per-role permissions
- Useful for multi-tenant Airflow

---

## Audit Logs

- DB tables: dag_runs, task_instance, log
- View who triggered what
- Forward to external log system

---

## Network Security

- Webserver behind reverse proxy
- TLS for the UI
- Restrict /api access
- Don't expose to public internet directly

---

## Best Practices

- Secrets in a backend, not metadata DB
- SSO for users
- Per-DAG access control
- Audit log retention policy

---

## Common Security Mistakes

- Default admin password
- Webserver on public internet
- Secrets in Variables (encrypted but visible)
- No SSO; shared accounts
- No periodic credential rotation
