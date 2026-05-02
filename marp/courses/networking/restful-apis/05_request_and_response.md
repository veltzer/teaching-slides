---
tags:
  - networking:rest
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Request and Response

---
## What This Chapter Covers

- Request bodies
- Response shapes
- Errors
- Validation
- Content negotiation

---
## JSON Bodies

- Standard for modern REST
- application/json
- Symmetric: requests and responses

---
## Status Code Classes

![status_class](svg/courses/networking/restful-apis/05_request_and_response/status_class.svg)

---
## Sample Request

```json
POST /users
{
    "name": "Alice",
    "email": "alice@example.com"
}
```

---
## Sample Response

```json
HTTP/1.1 201 Created
Location: /users/123
{
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "2024-01-01T00:00:00Z"
}
```

---
## Response Envelopes

- Wrap data: `{"data": {...}, "meta": {...}}`
- Or return data directly
- Pick one; be consistent
- Envelope helps with metadata

---
## Error Responses

- Use proper status code
- Body explains the error
- Don't return 200 for errors
- Stable error structure

---
## Sample Error

```json
HTTP/1.1 400 Bad Request
{
    "error": "validation_failed",
    "message": "Email is required",
    "details": [
        {"field": "email", "code": "required"}
    ]
}
```

---
## Problem Details (RFC 7807)

- Standard error format
- type, title, status, detail, instance
- Adopted by many APIs
- Worth considering

---
## Validation

- Validate inputs server-side
- Return 400 or 422 for invalid data
- List all errors, not just first
- Consistent error structure

---
## Idempotency

- Safe to retry
- GET, PUT, DELETE: idempotent by spec
- POST: use Idempotency-Key header
- Critical for payments

---
## Content Negotiation

- Accept: application/json
- Server returns matching format
- 406 Not Acceptable if unsupported
- Most APIs are JSON-only

---
## Compression

- Accept-Encoding: gzip
- Server returns Content-Encoding
- Big payload savings
- Usually transparent

---
## Common Request/Response Mistakes

- Returning 200 for errors
- Different error shape per endpoint
- HTML error pages from JSON APIs
- Missing Location header on 201
- Throwing on first validation error instead of collecting all
