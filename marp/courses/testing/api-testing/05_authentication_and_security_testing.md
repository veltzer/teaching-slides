---
tags:
  - testing:api
  - security:authentication
level: intermediate
category: testing
audience:
  - audiences:qa
  - audiences:security

---
# Authentication and Security Testing

---
## What This Chapter Covers

- Auth in tests
- Test users
- Token management
- Common security checks
- Fuzzing

---
## Auth In Tests

- Real auth flow once: get token
- Reuse across tests
- Refresh when expired
- Or: shortcut for test envs

---
## Test Users

- Dedicated test accounts
- Different roles (admin, member, guest)
- Don't use real user data

---
## Token Management

- Cache tokens per role
- Refresh transparently
- Don't commit secrets

---
## Authorisation Tests

- Same endpoint, different roles
- Verify allowed actions
- Verify denials (403)
- Critical for multi-tenant

---
## Tenant Isolation

- User from tenant A: cannot access tenant B
- Test by manipulating ids
- Common bug class

---
## OWASP API Top 10

- Broken Object Level Auth
- Broken Authentication
- Excessive Data Exposure
- Lack of Rate Limiting
- Broken Function Level Auth
- Mass Assignment
- Security Misconfig
- Injection
- Improper Asset Mgmt
- Insufficient Logging

---
## Object Level Auth Tests

- Most common API vuln
- Tester accesses other users' data
- Manipulate id in URL
- Should be 403 or 404

---
## Rate Limit Tests

- Send burst above limit
- Verify 429
- Verify backoff applied

---
## Injection

- SQL, NoSQL, command, header injection
- Crafted inputs that should be rejected
- Should fail validation, not crash

---
## Mass Assignment

- Send extra fields server should ignore
- Verify they don't update protected attrs (e.g., is_admin)

---
## Excessive Data Exposure

- Response includes internal fields
- Tester reviews each endpoint
- Fix: explicit DTOs

---
## Fuzzing

- Random / property-based inputs
- Find crashes, schema violations
- Tools: Schemathesis, Restler

---
## Penetration Testing

- Goes beyond automated tests
- Hands-on probing
- Periodic, by trained testers

---
## Common Security-Testing Mistakes

- Testing only happy path; auth-bypass slips through
- Same token reused across all tests
- No tenant-isolation tests
- Skipping mass-assignment checks
- Treating pen-test as one-off; never repeated
